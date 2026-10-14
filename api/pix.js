/* POST /api/pix — Gera cobrança PIX.
   Calcula o preço no servidor (nunca confia no browser).
   Gateways: PagSense, Skale Pay, ou mock. */

import { calcTotal, calcShipping, findProduct, cors } from './_defanti/catalog.js';

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const SKALE_API = 'https://api.skalepayments.com.br';
const PAGSENSE_API = 'https://api.pagsense.com/v1';
const PAGSENSE_PUBLIC = process.env.PAGSENSE_PUBLIC_KEY || '';
const PAGSENSE_SECRET = process.env.PAGSENSE_SECRET_KEY || '';

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

async function createPixSkalePay(order) {
  const resp = await fetch(`${SKALE_API}/v1/charges`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${GATEWAY_KEY}`
    },
    body: JSON.stringify({
      amount: order.total,
      method: 'pix',
      customer: {
        name: order.customer.name,
        document: order.customer.cpf,
        email: order.customer.email,
        phone: order.customer.phone || undefined
      },
      description: `Pedido ${order.code} - Defanti Store`,
      external_id: order.code,
      postback_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/api/postback'
    })
  });

  if (!resp.ok) {
    const errBody = await resp.text();
    console.error('[pix] skalepay error status=' + resp.status + ' body=' + errBody.slice(0, 200));
    throw new Error('Erro no gateway de pagamento.');
  }

  const data = await resp.json();

  return {
    ok: true,
    pixId: data.id || data.charge_id || data.transaction_id,
    orderCode: order.code,
    pixCode: data.pix_code || data.pix?.code || data.qr_code || data.brcode || '',
    qrImage: data.pix_qrcode || data.pix?.qr_code_url || data.qr_code_url || '',
    qrCode: data.pix_code || data.pix?.code || data.qr_code || data.brcode || '',
    expiresIn: data.expires_in || data.pix?.expires_in || 1800
  };
}

async function createPixPagSense(order) {
  const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');
  const siteUrl = process.env.SITE_URL || 'https://defantistore.vercel.app';

  const items = order.items.map(item => {
    const p = findProduct(item.id);
    const unitPrice = item.isBump
      ? Math.round((order.subtotal - calcTotal(order.items.filter(i => !i.isBump))) / order.items.filter(i => i.isBump).reduce((n, i) => n + i.qty, 0))
      : p.price;
    return {
      title: p.name,
      description: p.name,
      unitPrice: unitPrice,
      quantity: item.qty,
      tangible: true
    };
  });

  if (order.shipping.price > 0) {
    items.push({
      title: 'Frete',
      description: 'Frete ' + (order.shipping.id || 'padrao'),
      unitPrice: order.shipping.price,
      quantity: 1,
      tangible: true
    });
  }

  const payload = {
    paymentMethod: 'pix',
    amount: order.total,
    isInfoProducts: false,
    postbackUrl: `${siteUrl}/api/postback`,
    customer: {
      name: order.customer.name,
      email: order.customer.email,
      phone: order.customer.phone || ''
    },
    document: {
      number: order.customer.cpf,
      type: 'cpf'
    },
    items,
    shipping: {
      cost: order.shipping.price,
      method: order.shipping.id || 'padrao',
      estimated_delivery: '5 a 10 dias úteis',
      tracking_code: '',
      address: {
        street: order.address.street || '',
        streetNumber: order.address.number || '',
        zipCode: (order.address.cep || '').replace(/\D/g, ''),
        neighborhood: order.address.neighborhood || '',
        city: order.address.city || '',
        state: order.address.state || '',
        country: 'BR',
        complement: order.address.complement || ''
      }
    }
  };

  const resp = await fetch(`${PAGSENSE_API}/transactions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Basic ${auth}`
    },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const errBody = await resp.text();
    console.error('[pix] pagsense error status=' + resp.status + ' body=' + errBody.slice(0, 300));
    throw new Error('Erro no gateway de pagamento.');
  }

  const data = await resp.json();

  return {
    ok: true,
    pixId: String(data.insertId || data.id),
    orderCode: order.code,
    pixCode: data.pix_code || data.pixCode || data.brcode || data.qr_code || '',
    qrImage: data.pix_qrcode || data.qr_code_url || '',
    qrCode: data.pix_code || data.pixCode || data.brcode || data.qr_code || '',
    expiresIn: data.expires_in || 1800
  };
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

    for (const item of body.items) {
      const p = findProduct(item.id);
      if (!p) return res.status(400).json({ ok: false, error: `Produto "${item.id}" não encontrado.` });
      if (item.qty < 1 || item.qty > 10) {
        return res.status(400).json({ ok: false, error: 'Quantidade inválida.' });
      }
      if (p.maxPerCpf) {
        const totalQty = body.items.filter(i => i.id === item.id).reduce((s, i) => s + i.qty, 0);
        if (totalQty > p.maxPerCpf) {
          return res.status(400).json({ ok: false, error: `Limite de ${p.maxPerCpf} unidade(s) para "${p.name}".` });
        }
      }
    }

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

    console.log('[pix] order=' + order.code + ' total=' + total + ' items=' + body.items.length + ' gateway=' + GATEWAY);

    let result;
    if (GATEWAY === 'pagsense') {
      result = await createPixPagSense(order);
    } else if (GATEWAY === 'skalepay') {
      result = await createPixSkalePay(order);
    } else if (GATEWAY === 'mock') {
      result = await createPixMock(order);
    } else {
      return res.status(500).json({ ok: false, error: 'Gateway não configurado.' });
    }

    return res.status(200).json(result);
  } catch (err) {
    console.error('[pix] error code=unknown', err.message);
    return res.status(500).json({ ok: false, error: 'Erro interno. Tente novamente.' });
  }
}
