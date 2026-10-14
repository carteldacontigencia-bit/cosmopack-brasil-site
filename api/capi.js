/* POST /api/capi — Envia eventos ao Meta Conversions API.
   Aceita: InitiateCheckout, Purchase.
   Dados do usuário são hasheados (SHA-256) antes do envio. */

import { cors } from './_defanti/catalog.js';
import { createHash } from 'node:crypto';

const META_PIXEL_ID = process.env.META_PIXEL_ID || '';
const META_ACCESS_TOKEN = process.env.META_CAPI_TOKEN || '';
const ALLOWED_EVENTS = ['InitiateCheckout', 'Purchase'];

function hash(v) {
  return v ? createHash('sha256').update(v.trim().toLowerCase()).digest('hex') : '';
}

export default async function handler(req, res) {
  cors(res);
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  if (!META_PIXEL_ID || !META_ACCESS_TOKEN) {
    return res.status(200).json({ sent: false, reason: 'not_configured' });
  }

  const body = req.body;
  const eventName = body?.eventName;
  if (!eventName || !ALLOWED_EVENTS.includes(eventName)) {
    return res.status(400).json({ error: 'Evento inválido.' });
  }

  const eventId = body.eventId || eventName.toLowerCase() + '_' + Date.now();

  const event = {
    event_name: eventName,
    event_time: Math.floor(Date.now() / 1000),
    event_id: eventId,
    event_source_url: (process.env.SITE_URL || 'https://defantistore.vercel.app') + '/',
    action_source: 'website',
    user_data: {
      em: body.email ? [hash(body.email)] : [],
      ph: body.phone ? [hash(body.phone)] : [],
      client_ip_address: req.headers['x-forwarded-for']?.split(',')[0]?.trim() || '',
      client_user_agent: req.headers['user-agent'] || '',
      fbc: body.fbc || '',
      fbp: body.fbp || ''
    },
    custom_data: {
      currency: 'BRL',
      value: body.value || '0',
      content_ids: body.contentIds || [],
      content_type: 'product',
      num_items: body.numItems || 0
    }
  };

  if (body.orderCode) event.custom_data.order_id = body.orderCode;

  try {
    const resp = await fetch(
      `https://graph.facebook.com/v21.0/${META_PIXEL_ID}/events`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: [event], access_token: META_ACCESS_TOKEN })
      }
    );
    console.log('[capi] ' + eventName + ' id=' + eventId + ' status=' + resp.status);
    return res.status(200).json({ sent: true, fbStatus: resp.status });
  } catch (err) {
    console.error('[capi] error ' + eventName + ' id=' + eventId, err.message);
    return res.status(200).json({ sent: false, reason: 'fetch_error' });
  }
}
