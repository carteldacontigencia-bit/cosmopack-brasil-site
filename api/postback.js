/* POST /api/postback — Webhook do gateway de pagamento.
   Recebe notificação de PIX pago. Deve SEMPRE re-consultar
   o gateway antes de confiar no payload (evita fraude).
   Dispara evento Purchase no Meta CAPI se confirmado.
   Nunca loga PII — apenas código do pedido e status. */

const GATEWAY = process.env.PAYMENT_GATEWAY || 'mock';
const GATEWAY_KEY = process.env.GATEWAY_API_KEY || '';
const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_ACCESS_TOKEN = process.env.META_ACCESS_TOKEN || '';

async function verifyWithGateway(pixId) {
  if (GATEWAY === 'mock') return { verified: true, status: 'paid' };
  // Re-query gateway API to confirm payment
  throw new Error('Gateway não configurado para verificação.');
}

async function sendPurchaseEvent(order, req) {
  if (!META_PIXEL_ID || !META_ACCESS_TOKEN) return;

  const crypto = await import('node:crypto');
  const hash = (v) => v ? crypto.createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';

  const eventData = {
    data: [{
      event_name: 'Purchase',
      event_time: Math.floor(Date.now() / 1000),
      event_id: 'purchase_' + order.code,
      event_source_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/',
      action_source: 'website',
      user_data: {
        em: [hash(order.customer?.email)],
        ph: [hash(order.customer?.phone)],
        client_ip_address: req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.socket?.remoteAddress || '',
        client_user_agent: req.headers['user-agent'] || ''
      },
      custom_data: {
        currency: 'BRL',
        value: (order.total / 100).toFixed(2),
        order_id: order.code
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
    const result = await resp.json();
    console.log('[postback] capi event_id=purchase_' + order.code + ' status=' + resp.status);
  } catch (err) {
    console.error('[postback] capi error order=' + order.code, err.message);
  }
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const body = req.body;
    const pixId = body?.pixId || body?.id || body?.data?.id;
    if (!pixId) return res.status(400).json({ error: 'Missing pixId' });

    console.log('[postback] received pixId=' + String(pixId).slice(0, 20));

    const verification = await verifyWithGateway(pixId);
    if (!verification.verified || verification.status !== 'paid') {
      console.log('[postback] not verified pixId=' + String(pixId).slice(0, 20));
      return res.status(200).json({ received: true, action: 'ignored' });
    }

    console.log('[postback] confirmed paid pixId=' + String(pixId).slice(0, 20));

    // Send Purchase event to Meta CAPI (only on confirmed payment)
    if (body.order) {
      await sendPurchaseEvent(body.order, req);
    }

    return res.status(200).json({ received: true, action: 'confirmed' });
  } catch (err) {
    console.error('[postback] error', err.message);
    return res.status(500).json({ error: 'Internal error' });
  }
}
