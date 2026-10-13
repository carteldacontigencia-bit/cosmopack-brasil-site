/* GET /api/pix-status?id=<pixId> — Consulta status do PIX.
   O frontend faz polling a cada 5s. Nunca retorna PII. */

import { cors } from './_defanti/catalog.js';

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';

async function checkMock(pixId) {
  return { status: 'pending' };
}

async function checkReal(pixId) {
  throw new Error('Gateway não configurado.');
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
    if (GATEWAY === 'mock') {
      result = await checkMock(pixId);
    } else {
      result = await checkReal(pixId);
    }
    return res.status(200).json(result);
  } catch (err) {
    console.error('[pix-status] error', err.message);
    return res.status(500).json({ status: 'error' });
  }
}
