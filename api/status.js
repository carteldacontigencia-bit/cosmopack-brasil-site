/* GET /api/status?external_id=... — el navegador pregunta cada pocos
   segundos si ya cayó el pago. La respuesta sale de XPag, no de una
   base de datos nuestra, así que no puede quedar desincronizada. */

import { aplicarCors, xpag, normalizarEstado } from './_xpag.js';

export default async function handler(req, res) {
  if (aplicarCors(req, res)) return;
  if (req.method !== 'GET') {
    return res.status(405).json({ ok: false, error: 'Método no permitido' });
  }

  const externalId = String(req.query?.external_id || '').trim();
  const txId = String(req.query?.transaction_id || '').trim();
  if (!externalId && !txId) {
    return res.status(400).json({ ok: false, error: 'Falta el identificador.' });
  }

  /* Preferimos transaction_id: en cobranza dinámica devuelve el registro
     único. external_id devuelve una lista; normalizarEstado cubre las dos. */
  const query = txId
    ? `transaction_id=${encodeURIComponent(txId)}`
    : `external_id=${encodeURIComponent(externalId)}`;

  let r;
  try {
    r = await xpag(`/consult-transaction?${query}`);
  } catch {
    return res.status(502).json({ ok: false, status: 'unknown' });
  }

  /* 404 = todavía no hay depósito registrado. Para el comprador eso es
     "seguimos esperando", no un error. */
  if (r.httpStatus === 404) {
    return res.status(200).json({ ok: true, status: 'pending' });
  }
  if (r.httpStatus >= 400) {
    return res.status(200).json({ ok: true, status: 'unknown' });
  }

  const estado = normalizarEstado(r.data);
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).json({ ok: true, status: estado.status, amount: estado.amount, currency: estado.currency });
}
