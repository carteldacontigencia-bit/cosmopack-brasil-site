/* GET /api/pix-status?id=<pixId> — Consulta status do PIX.
   O frontend faz polling a cada 5s. Nunca retorna PII.
   Quando detecta pagamento, envia Purchase ao Meta CAPI. */

import { cors } from './_defanti/catalog.js';
import { createHash } from 'node:crypto';

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const SKALE_API = 'https://api.skalepayments.com.br';
const PAGSENSE_API = 'https://api.pagsense.com/v1';
const PAGSENSE_PUBLIC = process.env.PAGSENSE_PUBLIC_KEY || '';
const PAGSENSE_SECRET = process.env.PAGSENSE_SECRET_KEY || '';
const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_ACCESS_TOKEN = process.env.META_CAPI_TOKEN || '';

const sentEvents = new Set();

async function checkMock(pixId) {
  return { status: 'pending' };
}

async function checkPagSense(pixId) {
  const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');
  const resp = await fetch(`${PAGSENSE_API}/transactions/${encodeURIComponent(pixId)}`, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Basic ${auth}`
    }
  });

  if (!resp.ok) {
    console.error('[pix-status] pagsense error status=' + resp.status);
    return { status: 'error' };
  }

  const data = await resp.json();
  const rawStatus = (data.status || '').toLowerCase();

  if (rawStatus === 'paid' || rawStatus === 'confirmed' || rawStatus === 'approved') {
    return { status: 'paid', txData: data };
  }
  if (rawStatus === 'expired' || rawStatus === 'canceled' || rawStatus === 'cancelled') {
    return { status: 'expired' };
  }
  if (rawStatus === 'refunded') {
    return { status: 'refunded' };
  }
  return { status: 'pending' };
}

function hash(v) {
  return v ? createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';
}

async function sendPurchaseCapi(pixId, txData, req) {
  if (!META_PIXEL_ID || !META_ACCESS_TOKEN) return;
  if (sentEvents.has(pixId)) return;
  sentEvents.add(pixId);

  const email = txData?.customer?.email || txData?.email || '';
  const phone = txData?.customer?.phone || txData?.phone || '';
  const amount = txData?.amount ? (txData.amount / 100).toFixed(2) : '0';
  const orderId = txData?.external_id || txData?.id || pixId;

  const event = {
    event_name: 'Purchase',
    event_time: Math.floor(Date.now() / 1000),
    event_id: 'purchase_' + orderId,
    event_source_url: (process.env.SITE_URL || 'https://casaecia.vercel.app') + '/',
    action_source: 'website',
    user_data: {
      em: email ? [hash(email)] : [],
      ph: phone ? [hash(phone)] : [],
      client_ip_address: req.headers['x-forwarded-for']?.split(',')[0]?.trim() || '',
      client_user_agent: req.headers['user-agent'] || ''
    },
    custom_data: {
      currency: 'BRL',
      value: amount,
      order_id: orderId
    }
  };

  try {
    const resp = await fetch(
      `https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: [event], access_token: META_ACCESS_TOKEN })
      }
    );
    console.log('[pix-status] capi Purchase order=' + orderId + ' status=' + resp.status);
  } catch (err) {
    console.error('[pix-status] capi error order=' + orderId, err.message);
  }
}

async function checkSkalePay(pixId) {
  const resp = await fetch(`${SKALE_API}/v1/charges/${encodeURIComponent(pixId)}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${GATEWAY_KEY}`
    }
  });

  if (!resp.ok) {
    console.error('[pix-status] skalepay error status=' + resp.status);
    return { status: 'error' };
  }

  const data = await resp.json();
  const rawStatus = (data.status || data.payment_status || '').toLowerCase();

  if (rawStatus === 'paid' || rawStatus === 'confirmed' || rawStatus === 'approved') {
    return { status: 'paid' };
  }
  if (rawStatus === 'expired' || rawStatus === 'canceled' || rawStatus === 'cancelled') {
    return { status: 'expired' };
  }
  if (rawStatus === 'refunded') {
    return { status: 'refunded' };
  }
  return { status: 'pending' };
}

export default async function handler(req, res) {
  cors(res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const pixId = req.query.id;
  if (!pixId || typeof pixId !== 'string' || pixId.length > 100) {
    return res.status(400).json({ error: 'ID inválido.' });
  }

  try {
    let result;
    if (GATEWAY === 'pagsense') {
      result = await checkPagSense(pixId);
    } else if (GATEWAY === 'skalepay') {
      result = await checkSkalePay(pixId);
    } else if (GATEWAY === 'mock') {
      result = await checkMock(pixId);
    } else {
      return res.status(500).json({ status: 'error' });
    }

    if (result.status === 'paid' && result.txData) {
      sendPurchaseCapi(pixId, result.txData, req).catch(() => {});
    }

    return res.status(200).json({ status: result.status });
  } catch (err) {
    console.error('[pix-status] error', err.message);
    return res.status(500).json({ status: 'error' });
  }
}
