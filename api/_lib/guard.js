/* Puerta de entrada compartida: método, origen, tamaño del cuerpo y
   límite por IP. Devuelve { req, body } o responde y devuelve null. */
import { cfg } from './env.js';

const MAX_BODY = 4 * 1024;

/* Límite por IP en memoria.
   ────────────────────────────────────────────────────────────────
   Dos limitaciones que conviene tener presentes en lugar de suponer
   una protección que no existe:

   1. En serverless cada instancia lleva su propio contador, así que
      esto frena ráfagas de un mismo cliente, no un ataque distribuido.
      Para eso hace falta el firewall de la plataforma.

   2. Las operadoras móviles de México comparten IP pública entre
      muchísimos clientes (NAT). Un límite apretado no frena al
      atacante y sí puede bloquear a compradores reales de la misma
      operadora en un pico de tráfico. Por eso el valor por defecto es
      holgado y se puede subir con RATE_CREATE sin tocar el código. */
const golpes = new Map();

/* La clave incluye el endpoint, no solo la IP.
   Con un unico contador por IP, la consulta de estado —que corre cada 6
   segundos mientras la persona espera— se comia el presupuesto de
   /api/create y /api/contact, y el comprador acababa bloqueandose a si
   mismo. Cada ruta lleva su propio balde. */
function limitar(clave, max, ventanaMs) {
  const ahora = Date.now();
  const previo = golpes.get(clave);
  if (!previo || ahora - previo.desde > ventanaMs) {
    golpes.set(clave, { desde: ahora, n: 1 });
    if (golpes.size > 5000) {
      for (const [k, v] of golpes) if (ahora - v.desde > ventanaMs) golpes.delete(k);
    }
    return true;
  }
  previo.n += 1;
  return previo.n <= max;
}

export function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  return (Array.isArray(xff) ? xff[0] : (xff || '')).split(',')[0].trim()
    || req.headers['x-real-ip'] || 'desconocida';
}

export async function guard(req, res, {
  method = 'POST', rate = 12, windowMs = 60_000, checkOrigin = true,
} = {}) {
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') {
    if (cfg.siteOrigin && req.headers.origin === cfg.siteOrigin) {
      res.setHeader('Access-Control-Allow-Origin', cfg.siteOrigin);
      res.setHeader('Vary', 'Origin');
    }
    res.setHeader('Access-Control-Allow-Methods', `${method},OPTIONS`);
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.status(204).end();
    return null;
  }

  if (req.method !== method) {
    res.status(405).json({ ok: false, error: 'method' });
    return null;
  }

  /* Origen: sólo cuando SITE_ORIGIN está configurado. Se exige en las
     peticiones del navegador (traen Origin); el webhook del gateway no
     pasa por aquí con checkOrigin. */
  if (checkOrigin && cfg.siteOrigin) {
    const origin = req.headers.origin;
    if (origin && origin !== cfg.siteOrigin) {
      res.status(403).json({ ok: false, error: 'origin' });
      return null;
    }
    res.setHeader('Access-Control-Allow-Origin', cfg.siteOrigin);
    res.setHeader('Vary', 'Origin');
  }

  const ip = clientIp(req);
  const ruta = (req.url || '').split('?')[0] || 'sin-ruta';
  if (!limitar(`${ip}|${ruta}`, rate, windowMs)) {
    res.setHeader('Retry-After', String(Math.ceil(windowMs / 1000)));
    res.status(429).json({ ok: false, error: 'rate' });
    return null;
  }

  if (method === 'GET') return { ip, body: {} };

  const largo = Number(req.headers['content-length'] || 0);
  if (largo > MAX_BODY) {
    res.status(413).json({ ok: false, error: 'size' });
    return null;
  }

  let body = req.body;
  if (!body || typeof body !== 'object') {
    const trozos = [];
    let total = 0;
    for await (const c of req) {
      total += c.length;
      if (total > MAX_BODY) { res.status(413).json({ ok: false, error: 'size' }); return null; }
      trozos.push(c);
    }
    const texto = Buffer.concat(trozos).toString('utf8');
    try { body = texto ? JSON.parse(texto) : {}; }
    catch { res.status(400).json({ ok: false, error: 'json' }); return null; }
  }
  return { ip, body };
}

/* Error hacia el navegador: sin detalle interno, nunca el mensaje del
   proveedor ni el stack. El detalle va al log del servidor. */
export function fallo(res, http, clave, extra = {}) {
  res.status(http).json({ ok: false, error: clave, ...extra });
}
