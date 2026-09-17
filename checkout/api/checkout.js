/* POST /api/checkout — crea la cobranza en XPag y devuelve al navegador
   SÓLO las instrucciones de pago. Ni el secreto ni el importe pasan por
   el cliente: el importe sale del catálogo del servidor. */

import {
  aplicarCors, leerJson, xpag, getProduct, nuevoExternalId,
  mensajeDeError, REINTENTABLES, isSandbox,
} from './_xpag.js';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export default async function handler(req, res) {
  if (aplicarCors(req, res)) return;

  /* GET = sólo los datos de exhibición del producto (nombre e importe).
     El precio se sirve desde aquí en vez de duplicarlo en el JavaScript,
     así la pantalla nunca muestra un precio distinto al que se cobra. */
  if (req.method === 'GET') {
    try {
      const p = getProduct(req.query?.product);
      res.setHeader('Cache-Control', 'public, max-age=300');
      return res.status(200).json({
        ok: true, name: p.name, amount: p.amount, currency: p.currency,
      });
    } catch {
      return res.status(404).json({ ok: false, error: 'Producto no disponible.' });
    }
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Método no permitido' });
  }

  const body = await leerJson(req);
  const metodo = body.method === 'oxxo' ? 'oxxo' : 'spei';
  const nombre = String(body.name || '').trim().slice(0, 80);
  const email = String(body.email || '').trim().slice(0, 120);

  if (nombre.length < 3) {
    return res.status(400).json({ ok: false, error: 'Escribe tu nombre completo.', field: 'name' });
  }
  if (!EMAIL_RE.test(email)) {
    return res.status(400).json({ ok: false, error: 'Revisa tu correo: ahí te llega el libro.', field: 'email' });
  }

  let producto;
  try {
    producto = getProduct(body.product);
  } catch {
    return res.status(400).json({ ok: false, error: 'Producto no disponible.' });
  }

  const externalId = nuevoExternalId(String(body.product));
  const webhookUrl = process.env.XPAG_WEBHOOK_URL;

  /* Cobranza dinámica: mandamos amount, así el importe queda fijo en la
     cobranza y el comprador no puede pagar otra cosa. */
  const payload = {
    currency: producto.currency,
    amount: producto.amount,
    external_id: externalId,
    description: producto.description,
    ...(webhookUrl ? { webhook_url: webhookUrl } : {}),
  };

  if (metodo === 'oxxo') {
    payload.method = 'OXXO';
    payload.payerData = { name: nombre, email };
    /* generateCheckout:false devuelve el voucher crudo en payee_data
       (reference + barcode), que es la forma que la documentación
       especifica campo por campo. La página hospedada (true) no trae
       documentado el nombre del campo de la URL, así que la pintamos
       nosotros y no dependemos de un campo que no podemos verificar. */
    payload.generateCheckout = false;
  } else {
    payload.name = nombre;
  }

  let respuesta;
  try {
    respuesta = await xpag('/cashin', { method: 'POST', body: payload });
  } catch (e) {
    if (e.code === 'config_missing') {
      console.error('[checkout] credenciales no configuradas');
      return res.status(500).json({ ok: false, error: 'El cobro no está configurado todavía.' });
    }
    console.error('[checkout] fallo de red hacia XPag:', e.name);
    return res.status(502).json({ ok: false, error: 'El servicio de pagos no responde. Intenta de nuevo.', retryable: true });
  }

  const { httpStatus, data } = respuesta;

  if (httpStatus >= 400 || data.ok === false) {
    const code = data.error_code || 'cashin_failed';
    /* El external_id se devuelve para que un reintento reutilice el mismo
       y no duplique la venta. */
    console.error('[checkout] XPag rechazó:', httpStatus, code, externalId);
    return res.status(httpStatus >= 500 ? 502 : 422).json({
      ok: false,
      error: mensajeDeError(code),
      code,
      retryable: REINTENTABLES.has(code),
      external_id: externalId,
    });
  }

  /* Lo que sale hacia el navegador. Nada de lo que no necesite. */
  const salida = {
    ok: true,
    sandbox: Boolean(data.sandbox) || isSandbox,
    method: metodo,
    external_id: externalId,
    amount: producto.amount,
    currency: producto.currency,
    product_name: producto.name,
    transaction_id: data.transaction_id || data.request_number || null,
  };

  if (metodo === 'oxxo') {
    const pd = data.payee_data || {};
    salida.reference = pd.reference || data.reference || null;
    salida.barcode = pd.barcode || null;
    if (!salida.reference) {
      console.error('[checkout] OXXO sin referencia en la respuesta', Object.keys(data));
      return res.status(502).json({ ok: false, error: 'No pudimos generar el voucher. Intenta con transferencia.' });
    }
  } else {
    salida.clabe = data.clabe || null;
    salida.reference = data.reference || null;
    /* La documentación pide mostrar banco y beneficiario junto a la CLABE:
       el pagador ver "STP" y el nombre sube la conversión del SPEI. */
    salida.bank_name = data.bank_name || null;
    salida.beneficiary = data.beneficiary || null;
    if (!salida.clabe) {
      console.error('[checkout] SPEI sin clabe en la respuesta', Object.keys(data));
      return res.status(502).json({ ok: false, error: 'No pudimos generar los datos de transferencia. Intenta de nuevo.' });
    }
  }

  res.status(200).json(salida);
}
