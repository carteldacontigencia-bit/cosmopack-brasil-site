/* GET /api/status?t=<token de acceso>
   El navegador pregunta si ya cayo el pago. La respuesta sale de XPag,
   no de un almacen propio, asi que no puede quedar desincronizada.
   Se acepta SOLO el token firmado: sin el no se puede sondear el estado
   de ventas ajenas probando identificadores. */
import { guard, fallo } from './_lib/guard.js';
import { estadoDe } from './_lib/xpag.js';
import { externalIdDeToken } from './_lib/order.js';

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'GET', rate: 90, windowMs: 60_000 });
  if (!g) return;

  const externalId = externalIdDeToken(req.query?.t);
  if (!externalId) return fallo(res, 400, 'err_token');

  const txId = typeof req.query?.tx === 'string' && /^[\w.-]{1,64}$/.test(req.query.tx)
    ? req.query.tx : null;

  let est;
  try {
    est = await estadoDe({ transactionId: txId, externalId });
  } catch (e) {
    console.error('[status] consulta fallo:', e.code || e.name);
    return res.status(200).json({ ok: true, status: 'unknown' });
  }

  res.status(200).json({
    ok: true,
    status: est.status,
    amount: est.amount ?? null,
    currency: est.currency ?? null,
    /* e2e es unico por pago: el front lo usa como id de evento del pixel
       para no contar la misma compra dos veces. */
    event_id: est.status === 'confirmed' ? (est.e2e || externalId) : null,
  });
}
