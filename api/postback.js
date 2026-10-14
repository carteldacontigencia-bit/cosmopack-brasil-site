/* POST /api/postback — Webhook do gateway de pagamento.
   Recebe notificação de PIX pago. Re-consulta o gateway
   antes de confiar no payload (evita fraude).
   Dispara evento Purchase no Meta CAPI se confirmado.
   Nunca loga PII — apenas código do pedido e status. */

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const SKALE_API = 'https://api.skalepayments.com.br';
const PAGSENSE_API = 'https://api.pagsense.com/v1';
const PAGSENSE_PUBLIC = process.env.PAGSENSE_PUBLIC_KEY || '';
const PAGSENSE_SECRET = process.env.PAGSENSE_SECRET_KEY || '';
const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_ACCESS_TOKEN = process.env.META_ACCESS_TOKEN || '';

async function verifyWithGateway(pixId) {
  if (GATEWAY === 'mock') return { verified: true, status: 'paid' };

  if (GATEWAY === 'pagsense') {
    const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');
    const resp = await fetch(`${PAGSENSE_API}/transactions/${encodeURIComponent(pixId)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Authorization': `Basic ${auth}` }
    });
    if (!resp.ok) {
      console.error('[postback] pagsense verify error status=' + resp.status);
      return { verified: false, status: 'error' };
    }
    const data = await resp.json();
    const rawStatus = (data.status || '').toLowerCase();
    const isPaid = rawStatus === 'paid' || rawStatus === 'confirmed' || rawStatus === 'approved';
    return { verified: isPaid, status: isPaid ? 'paid' : rawStatus };
  }

  if (GATEWAY === 'skalepay') {
    const resp = await fetch(`${SKALE_API}/v1/charges/${encodeURIComponent(pixId)}`, {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${GATEWAY_KEY}` }
    });
    if (!resp.ok) {
      console.error('[postback] skalepay verify error status=' + resp.status);
      return { verified: false, status: 'error' };
    }
    const data = await resp.json();
    const rawStatus = (data.status || data.payment_status || '').toLowerCase();
    const isPaid = rawStatus === 'paid' || rawStatus === 'confirmed' || rawStatus === 'approved';
    return { verified: isPaid, status: isPaid ? 'paid' : rawStatus };
  }

  throw new Error('Gateway não configurado para verificação.');
}

async function sendPurchaseEvent(pixId, body, req) {
  if (!META_PIXEL_ID || !META_ACCESS_TOKEN) return;

  const crypto = await import('node:crypto');
  const hash = (v) => v ? crypto.createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';

  let email = '';
  let phone = '';
  let value = '0';
  let orderId = String(pixId);

  if (GATEWAY === 'pagsense') {
    try {
      const auth = Buffer.from(`${PAGSENSE_PUBLIC}:${PAGSENSE_SECRET}`).toString('base64');
      const resp = await fetch(`${PAGSENSE_API}/transactions/${encodeURIComponent(pixId)}`, {
        method: 'GET',
        headers: { 'Accept': 'application/json', 'Authorization': `Basic ${auth}` }
      });
      if (resp.ok) {
        const tx = await resp.json();
        email = tx.customer?.email || tx.email || '';
        phone = tx.customer?.phone || tx.phone || '';
        value = tx.amount ? (tx.amount / 100).toFixed(2) : '0';
        orderId = tx.external_id || tx.id || pixId;
      }
    } catch (e) {
      console.error('[postback] pagsense fetch for capi error', e.message);
    }
  }

  const eventData = {
    data: [{
      event_name: 'Purchase',
      event_time: Math.floor(Date.now() / 1000),
      event_id: 'purchase_' + orderId,
      event_source_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/',
      action_source: 'website',
      user_data: {
        em: email ? [hash(email)] : [],
        ph: phone ? [hash(phone)] : [],
        client_ip_address: req.headers['x-forwarded-for']?.split(',')[0]?.trim() || '',
        client_user_agent: req.headers['user-agent'] || ''
      },
      custom_data: {
        currency: 'BRL',
        value: value,
        order_id: orderId
      }
    }],
    access_token: META_ACCESS_TOKEN
  };

  try {
    const resp = await fetch(
      `https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(eventData)
      }
    );
    console.log('[postback] capi event_id=purchase_' + orderId + ' status=' + resp.status);
  } catch (err) {
    console.error('[postback] capi error order=' + orderId, err.message);
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const body = req.body;
    const pixId = body?.insertId || body?.id || body?.charge_id || body?.pixId || body?.data?.id || body?.originalTransactionId;
    if (!pixId) return res.status(400).json({ error: 'Missing pixId' });

    console.log('[postback] received pixId=' + String(pixId).slice(0, 20));

    const verification = await verifyWithGateway(pixId);
    if (!verification.verified || verification.status !== 'paid') {
      console.log('[postback] not verified pixId=' + String(pixId).slice(0, 20));
      return res.status(200).json({ received: true, action: 'ignored' });
    }

    console.log('[postback] confirmed paid pixId=' + String(pixId).slice(0, 20));

    await sendPurchaseEvent(pixId, body, req);

    return res.status(200).json({ received: true, action: 'confirmed' });
  } catch (err) {
    console.error('[postback] error', err.message);
    return res.status(500).json({ error: 'Internal error' });
  }
}
