/* Identificador de venta y enlace de acceso firmado.
   ──────────────────────────────────────────────────────────────
   No hay base de datos y no hace falta: el enlace de acceso lleva el
   external_id y una firma HMAC. Para entregar, el servidor verifica la
   firma y RECONSULTA a XPag. Quien pagó por OXXO vuelve horas después
   con su mismo enlace y, si ya confirmó, entra.
   Sin ACCESS_SECRET no se firma ni se verifica nada. */
import { createHmac, timingSafeEqual, randomUUID } from 'node:crypto';
import { cfg, requireConfig } from './env.js';

export function nuevoExternalId(ofertaId) {
  const r = randomUUID().replace(/-/g, '').slice(0, 12);
  return `${ofertaId}-${Date.now().toString(36)}-${r}`.toUpperCase();
}

const b64u = (b) => Buffer.from(b).toString('base64url');

function firma(externalId) {
  requireConfig('accessSecret');
  return createHmac('sha256', cfg.accessSecret).update(externalId).digest('base64url').slice(0, 32);
}

export function tokenDeAcceso(externalId) {
  return `${b64u(externalId)}.${firma(externalId)}`;
}

/* Devuelve el external_id sólo si la firma cuadra. Comparación en tiempo
   constante para no filtrar información por el tiempo de respuesta. */
export function externalIdDeToken(token) {
  if (typeof token !== 'string' || token.length > 300) return null;
  const i = token.lastIndexOf('.');
  if (i < 1) return null;
  let externalId;
  try { externalId = Buffer.from(token.slice(0, i), 'base64url').toString('utf8'); }
  catch { return null; }
  if (!/^[A-Z0-9-]{8,80}$/.test(externalId)) return null;
  const dada = Buffer.from(token.slice(i + 1));
  let esperada;
  try { esperada = Buffer.from(firma(externalId)); } catch { return null; }
  if (dada.length !== esperada.length) return null;
  return timingSafeEqual(dada, esperada) ? externalId : null;
}
