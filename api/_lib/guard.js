/* Puerta de entrada compartida: método, origen, tamaño del cuerpo y
   límite por IP. Devuelve { req, body } o responde y devuelve null. */
import { cfg } from './env.js';

const MAX_BODY = 4 * 1024;

/* Límite por IP en memoria. En serverless cada instancia tiene el suyo,
   así que frena ráfagas de un mismo cliente, no un ataque distribuido;
   para eso hace falta el firewall de la plataforma. Se dice aquí para no
   dar una sensación de protección que no existe. */
const golpes = new Map();

function limitar(ip, max, ventanaMs) {
  const ahora = Date.now();
  const previo = golpes.get(ip);
  if (!previo || ahora - previo.desde > ventanaMs) {
    golpes.set(ip, { desde: ahora, n: 1 });
    if (golpes.size > 5000) for (const [k, v] of golpes) if (ahora - v.desde > ventanaMs) golpes.delete(k);
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
  if (!limitar(ip, rate, windowMs)) {
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
