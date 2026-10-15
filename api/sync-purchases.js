/* GET /api/sync-purchases — Endpoint temporário.
   Consulta vendas recentes no XPag e envia Purchase ao Meta CAPI
   para as que já estão confirmadas. */

import { guard } from './_lib/guard.js';
import { enviarCompra } from './_lib/meta.js';
import { xpag, normalizar } from './_lib/xpag.js';

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'GET', rate: 10, windowMs: 60_000 });
  if (!g) return;

  const pixelId = process.env.META_PIXEL_ID;
  const token = process.env.META_CAPI_TOKEN;

  if (!pixelId || !token) {
    return res.status(200).json({
      error: 'Variáveis não encontradas.',
      META_PIXEL_ID: pixelId ? 'OK (' + pixelId.slice(0, 4) + '...)' : 'VAZIO',
      META_CAPI_TOKEN: token ? 'OK (' + token.slice(0, 4) + '...)' : 'VAZIO'
    });
  }

  try {
    const r = await xpag('/consult-transaction?status=confirmed');

    if (r.http >= 400) {
      return res.status(200).json({ error: 'XPag error status=' + r.http, data: r.data });
    }

    const payments = Array.isArray(r.data?.payments) ? r.data.payments
      : Array.isArray(r.data) ? r.data : [r.data];

    const results = [];

    for (const p of payments) {
      if (!p || (p.status && p.status !== 'confirmed')) continue;

      const eventId = p.e2e || p.external_id || p.transaction_id;
      if (!eventId) continue;

      const result = await enviarCompra({
        eventId,
        value: p.amount,
        currency: p.currency,
        externalId: p.external_id,
        payerName: p.payer_name,
      });

      results.push({
        external_id: p.external_id,
        amount: p.amount,
        result
      });
    }

    return res.status(200).json({
      total_payments: payments.length,
      sent: results.length,
      results
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
