/* GET /api/sync-purchases — Endpoint temporário.
   Busca vendas pagas na PagSense e envia Purchase ao Meta CAPI. */

import { cors } from './_defanti/catalog.js';
import { createHash } from 'node:crypto';

const PAGSENSE_API = 'https://api.pagsense.com/v1';
const PAGSENSE_PUBLIC = process.env.PAGSENSE_PUBLIC_KEY || '';
const PAGSENSE_SECRET = process.env.PAGSENSE_SECRET_KEY || '';
const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_ACCESS_TOKEN = process.env.META_CAPI_TOKEN || '';

function hash(v) {
  return v ? createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';
}

export default async function handler(req, res) {
  cors(res);
  if (req.method === 'OPTIONS') return res.status(204).end();

  if (!META_PIXEL_ID || !META_ACCESS_TOKEN) {
    return res.status(200).json({
      error: 'Variáveis não encontradas.',
      META_PIXEL_ID: META_PIXEL_ID ? 'OK (' + META_PIXEL_ID.slice(0, 4) + '...)' : 'VAZIO',
      META_CAPI_TOKEN: META_ACCESS_TOKEN ? 'OK (' + META_ACCESS_TOKEN.slice(0, 4) + '...)' : 'VAZIO'
    });
  }
  if (!PAGSENSE_PUBLIC || !PAGSENSE_SECRET) {
    return res.status(200).json({ error: 'PagSense keys não configuradas.' });
  }

  const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');

  try {
    const resp = await fetch(`${PAGSENSE_API}/all/transactions`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Basic ${auth}`
      }
    });

    if (!resp.ok) {
      return res.status(200).json({ error: 'PagSense error status=' + resp.status });
    }

    const transactions = await resp.json();
    const list = Array.isArray(transactions) ? transactions : transactions?.data || transactions?.transactions || [];

    const results = [];

    for (const tx of list) {
      const status = (tx.status || '').toLowerCase();
      if (status !== 'paid' && status !== 'confirmed' && status !== 'approved') continue;

      const email = tx.customer?.email || tx.email || '';
      const phone = tx.customer?.phone || tx.phone || '';
      const amount = tx.amount ? (tx.amount / 100).toFixed(2) : '0';
      const orderId = tx.external_id || tx.id || tx.insertId || '';

      const event = {
        event_name: 'Purchase',
        event_time: tx.paid_at ? Math.floor(new Date(tx.paid_at).getTime() / 1000) : Math.floor(Date.now() / 1000),
        event_id: 'purchase_' + orderId,
        event_source_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/',
        action_source: 'website',
        user_data: {
          em: email ? [hash(email)] : [],
          ph: phone ? [hash(phone)] : []
        },
        custom_data: {
          currency: 'BRL',
          value: amount,
          order_id: orderId
        }
      };

      const fbResp = await fetch(
        `https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ data: [event], access_token: META_ACCESS_TOKEN })
        }
      );

      const fbData = await fbResp.json();
      results.push({ orderId, amount, fbStatus: fbResp.status, fbResponse: fbData });
    }

    return res.status(200).json({ total: list.length, sent: results.length, results });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
