/* GET /api/pix-status?id=<pixId> — Consulta status do PIX.
   O frontend faz polling a cada 5s. Nunca retorna PII. */

import { cors } from './_defanti/catalog.js';

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const SKALE_API = 'https://api.skalepayments.com.br';

async function checkMock(pixId) {
  return { status: 'pending' };
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
    if (GATEWAY === 'skalepay') {
      result = await checkSkalePay(pixId);
    } else if (GATEWAY === 'mock') {
      result = await checkMock(pixId);
    } else {
      return res.status(500).json({ status: 'error' });
    }
    return res.status(200).json(result);
  } catch (err) {
    console.error('[pix-status] error', err.message);
    return res.status(500).json({ status: 'error' });
  }
}
