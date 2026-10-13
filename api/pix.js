/* POST /api/pix — Gera cobrança PIX.
   Calcula o preço no servidor (nunca confia no browser).
   Gateway configurado via PAYMENT_GATEWAY env var. */

import { calcTotal, calcShipping, findProduct, cors } from './_defanti/catalog.js';

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const GATEWAY_URL = process.env.GATEWAY_API_URL || '';

function validateCPF(cpf) {
  const d = cpf.replace(/\D/g, '');
  if (d.length !== 11 || /^(\d)\1{10}$/.test(d)) return false;
  for (let t = 9; t < 11; t++) {
    let sum = 0;
    for (let i = 0; i < t; i++) sum += +d[i] * (t + 1 - i);
    let r = (sum * 10) % 11;
    if (r === 10) r = 0;
    if (+d[t] !== r) return false;
  }
  return true;
}

function generateCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = 'DF-';
  for (let i = 0; i < 8; i++) code += chars[Math.floor(Math.random() * chars.length)];
  return code;
}

async function createPixMock(order) {
  const code = '00020126580014br.gov.bcb.pix0136' +
    'mock-' + order.code.toLowerCase() +
    '520400005303986540' + (order.total / 100).toFixed(2) +
    '5802BR5913DEFANTI STORE6015DUQUE DE CAXIAS62070503***6304';
  return {
    ok: true,
    pixId: 'mock_' + Date.now(),
    orderCode: order.code,
    pixCode: code,
    qrImage: '',
    qrCode: code,
    expiresIn: 1800
  };
}

async function createPixReal(order) {
  // Placeholder — will be implemented when gateway is chosen
  // Supports: pagarme, mercadopago, asaas
  throw new Error('Gateway "' + GATEWAY + '" não configurado. Defina PAYMENT_GATEWAY e GATEWAY_API_KEY.');
}

export default async function handler(req, res) {
  cors(res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ ok: false, error: 'Method not allowed' });

  try {
    const body = req.body;
    if (!body || !body.items || !body.customer) {
      return res.status(400).json({ ok: false, error: 'Dados incompletos.' });
    }

    // Validate customer
    const { name, cpf, email, phone } = body.customer;
    if (!name || name.trim().split(/\s+/).length < 2) {
      return res.status(400).json({ ok: false, error: 'Nome completo obrigatório.' });
    }
    if (!validateCPF(cpf)) {
      return res.status(400).json({ ok: false, error: 'CPF inválido.' });
    }
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return res.status(400).json({ ok: false, error: 'E-mail inválido.' });
    }

    // Validate items exist and recalculate prices server-side
    for (const item of body.items) {
      const p = findProduct(item.id);
      if (!p) return res.status(400).json({ ok: false, error: `Produto "${item.id}" não encontrado.` });
      if (item.qty < 1 || item.qty > 10) {
        return res.status(400).json({ ok: false, error: 'Quantidade inválida.' });
      }
      // Check per-CPF limit
      if (p.maxPerCpf) {
        const totalQty = body.items.filter(i => i.id === item.id).reduce((s, i) => s + i.qty, 0);
        if (totalQty > p.maxPerCpf) {
          return res.status(400).json({ ok: false, error: `Limite de ${p.maxPerCpf} unidade(s) para "${p.name}".` });
        }
      }
    }

    // Server-side price calculation
    const subtotal = calcTotal(body.items);
    const tier = calcShipping(body.items);
    const shippingId = body.shipping?.id;
    const shippingPrice = shippingId && tier.prices[shippingId] != null ? tier.prices[shippingId] : 0;
    const total = subtotal + shippingPrice;

    const order = {
      code: generateCode(),
      customer: { name: name.trim(), cpf: cpf.replace(/\D/g, ''), email: email.trim().toLowerCase(), phone: (phone || '').replace(/\D/g, '') },
      address: body.address || {},
      items: body.items,
      shipping: { id: shippingId, price: shippingPrice },
      subtotal,
      total,
      createdAt: new Date().toISOString()
    };

    // No PII in logs
    console.log('[pix] order=' + order.code + ' total=' + total + ' items=' + body.items.length);

    let result;
    if (GATEWAY === 'mock') {
      result = await createPixMock(order);
    } else {
      result = await createPixReal(order);
    }

    return res.status(200).json(result);
  } catch (err) {
    console.error('[pix] error code=unknown', err.message);
    return res.status(500).json({ ok: false, error: 'Erro interno. Tente novamente.' });
  }
}
