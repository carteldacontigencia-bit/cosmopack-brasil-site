/* GET /api/sync-purchases — Endpoint temporário.
   Busca vendas pagas e envia Purchase ao Meta CAPI.
   Funciona com PagSense ou XPag dependendo do que estiver configurado. */

import { createHash } from 'node:crypto';

const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_TOKEN = process.env.META_CAPI_TOKEN || '';
const PAGSENSE_API = 'https://api.pagsense.com/v1';
const PAGSENSE_PUBLIC = process.env.PAGSENSE_PUBLIC_KEY || '';
const PAGSENSE_SECRET = process.env.PAGSENSE_SECRET_KEY || '';

function hash(v) {
  return v ? createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';
}

async function sendToMeta(event) {
  const resp = await fetch(
    `https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data: [event], access_token: META_TOKEN })
    }
  );
  return { status: resp.status, data: await resp.json() };
}

async function viaPagSense() {
  const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');
  const resp = await fetch(`${PAGSENSE_API}/all/transactions`, {
    method: 'GET',
    headers: { 'Accept': 'application/json', 'Authorization': `Basic ${auth}` }
  });
  if (!resp.ok) throw new Error('PagSense error ' + resp.status);
  const raw = await resp.json();
  const list = Array.isArray(raw) ? raw : raw?.data || raw?.transactions || [];
  const results = [];

  for (const tx of list) {
    const s = (tx.status || '').toLowerCase();
    if (s !== 'paid' && s !== 'confirmed' && s !== 'approved') continue;

    const email = tx.customer?.email || tx.email || '';
    const phone = tx.customer?.phone || tx.phone || '';
    const amount = tx.amount ? (tx.amount / 100).toFixed(2) : '0';
    const orderId = tx.external_id || tx.id || tx.insertId || '';

    const fb = await sendToMeta({
      event_name: 'Purchase',
      event_time: tx.paid_at ? Math.floor(new Date(tx.paid_at).getTime() / 1000) : Math.floor(Date.now() / 1000),
      event_id: 'purchase_' + orderId,
      event_source_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/',
      action_source: 'website',
      user_data: {
        em: email ? [hash(email)] : [],
        ph: phone ? [hash(phone)] : []
      },
      custom_data: { currency: 'BRL', value: amount, order_id: orderId }
    });
    results.push({ orderId, amount, fb });
  }
  return { gateway: 'pagsense', total: list.length, sent: results.length, results };
}

async function viaXPag() {
  const { xpag } = await import('./_lib/xpag.js');
  const { enviarCompra } = await import('./_lib/meta.js');
  const r = await xpag('/consult-transaction?status=confirmed');
  if (r.http >= 400) throw new Error('XPag error ' + r.http);

  const payments = Array.isArray(r.data?.payments) ? r.data.payments
    : Array.isArray(r.data) ? r.data : [r.data];
  const results = [];

  for (const p of payments) {
    if (!p || (p.status && p.status !== 'confirmed')) continue;
    const eventId = p.e2e || p.external_id || p.transaction_id;
    if (!eventId) continue;
    const result = await enviarCompra({
      eventId, value: p.amount, currency: p.currency,
      externalId: p.external_id, payerName: p.payer_name,
    });
    results.push({ external_id: p.external_id, amount: p.amount, result });
  }
  return { gateway: 'xpag', total: payments.length, sent: results.length, results };
}

export default async function handler(req, res) {
  if (req.method === 'OPTIONS') return res.status(204).end();

  if (!META_PIXEL_ID || !META_TOKEN) {
    return res.status(200).json({
      error: 'Variáveis não encontradas.',
      META_PIXEL_ID: META_PIXEL_ID ? 'OK' : 'VAZIO',
      META_CAPI_TOKEN: META_TOKEN ? 'OK' : 'VAZIO'
    });
  }

  try {
    let result;
    if (PAGSENSE_PUBLIC && PAGSENSE_SECRET) {
      result = await viaPagSense();
    } else {
      result = await viaXPag();
    }
    return res.status(200).json(result);
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
