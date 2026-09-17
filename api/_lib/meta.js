/* Meta Conversions API — el Purchase que se dispara desde el SERVIDOR.
   ──────────────────────────────────────────────────────────────────
   Por qué existe: el Purchase del navegador sólo llega si la persona
   tiene la pantalla abierta cuando el pago confirma. En SPEI ocurre, son
   minutos. En OXXO no: se paga en la tienda horas después y casi nadie
   vuelve a abrir la página. Sin este envío, esas ventas son invisibles
   para Meta y el algoritmo optimiza en contra, creyendo que el anuncio
   no convierte.

   Se manda con event_id = e2e, el mismo que usa el navegador. Meta
   deduplica por (event_name, event_id), así que cuando los dos llegan
   —el caso del SPEI— la venta cuenta una sola vez.

   Sin META_CAPI_TOKEN no hace nada y lo dice en el log.

   Calidad de coincidencia: aquí no hay cookies _fbp/_fbc, porque quien
   llama es el gateway, no el navegador del comprador. Se manda lo que sí
   se puede recuperar sin almacenar nada: el identificador de la venta y
   el nombre del pagador que devuelve XPag. La coincidencia es más pobre
   que la del evento del navegador, pero una venta contada con señal
   modesta vale más que una venta no contada. */

import { createHash } from 'node:crypto';
import { cfg } from './env.js';

const VERSION = 'v21.0';

/* Meta exige los identificadores en SHA-256 de un valor normalizado:
   minúsculas y sin espacios alrededor. */
const hash = (v) => createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex');

export async function enviarCompra({ eventId, value, currency, externalId, payerName }) {
  const pixelId = process.env.META_PIXEL_ID;
  const token = process.env.META_CAPI_TOKEN;

  if (!pixelId || !token) {
    console.log('[meta] sin META_PIXEL_ID o META_CAPI_TOKEN: no se envia Purchase');
    return { enviado: false, motivo: 'sin_config' };
  }
  if (!eventId) {
    console.warn('[meta] sin event_id: no se envia, se contaria dos veces');
    return { enviado: false, motivo: 'sin_event_id' };
  }

  const user_data = {};
  if (externalId) user_data.external_id = hash(externalId);
  if (payerName) {
    /* Meta quiere nombre y apellido por separado. Si sólo viene uno, va
       como nombre y ya. */
    const partes = String(payerName).trim().split(/\s+/);
    if (partes[0]) user_data.fn = hash(partes[0]);
    if (partes.length > 1) user_data.ln = hash(partes[partes.length - 1]);
  }

  const evento = {
    event_name: 'Purchase',
    event_time: Math.floor(Date.now() / 1000),
    event_id: String(eventId),
    action_source: 'website',
    ...(cfg.publicUrl ? { event_source_url: `${cfg.publicUrl}/pago` } : {}),
    user_data,
    custom_data: {
      value: Number(value) || 0,
      currency: currency || 'MXN',
    },
  };

  const cuerpo = { data: [evento], access_token: token };
  /* Código de prueba de Events Manager: deja ver el evento en vivo sin
     ensuciar las métricas. */
  if (process.env.META_TEST_EVENT_CODE) cuerpo.test_event_code = process.env.META_TEST_EVENT_CODE;

  const base = process.env.META_API_BASE || 'https://graph.facebook.com';
  const ctl = new AbortController();
  const tiempo = setTimeout(() => ctl.abort(), 8000);
  try {
    const r = await fetch(`${base}/${VERSION}/${pixelId}/events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cuerpo),
      signal: ctl.signal,
    });
    const texto = await r.text();
    let data; try { data = JSON.parse(texto); } catch { data = { raw: texto.slice(0, 200) }; }

    if (!r.ok) {
      /* Nunca se reintenta desde aquí: el webhook debe responder rápido.
         Si Meta falla, se pierde ese evento, y es preferible a bloquear
         la entrega del producto. Queda en el log para poder revisarlo. */
      console.error('[meta] Purchase rechazado', r.status, data?.error?.message || data);
      return { enviado: false, motivo: 'rechazado', http: r.status };
    }
    console.log('[meta] Purchase enviado', { event_id: eventId, recibidos: data.events_received });
    return { enviado: true, recibidos: data.events_received };
  } catch (e) {
    console.error('[meta] fallo de red hacia Meta:', e.name);
    return { enviado: false, motivo: 'red' };
  } finally {
    clearTimeout(tiempo);
  }
}
