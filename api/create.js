/* POST /api/create — crea la cobranza en XPag.
   Devuelve al navegador solo las instrucciones de pago y el token de
   acceso. Ni credenciales ni importes vienen del cliente. */
import { guard, fallo } from './_lib/guard.js';
import { cfg, isSandbox } from './_lib/env.js';
import { xpag, claveDeError, REINTENTABLES } from './_lib/xpag.js';
import { getOferta, publica } from './_lib/offers.js';
import { nuevoExternalId, tokenDeAcceso } from './_lib/order.js';
import { nombreLimpio, metodoLimpio, cayoEnLaTrampa } from './_lib/sanitize.js';

export default async function handler(req, res) {
  /* 30 por minuto y por IP por defecto: holgado a proposito, porque en
     Mexico muchas personas comparten IP de operadora. Ajustable con
     RATE_CREATE. */
  const g = await guard(req, res, {
    method: 'POST',
    rate: Number(process.env.RATE_CREATE || 30),
    windowMs: 60_000,
  });
  if (!g) return;
  const { body } = g;

  /* Trampa: se responde como si todo hubiera ido bien, sin crear nada.
     Explicar el rechazo solo le ensena al robot a evitarlo. */
  if (cayoEnLaTrampa(body)) return res.status(202).json({ ok: false, error: 'err_generic' });

  const nombre = nombreLimpio(body.name);
  if (!nombre) return fallo(res, 400, 'err_name', { field: 'name' });

  const metodo = metodoLimpio(body.method);
  if (!metodo) return fallo(res, 400, 'err_method');

  const oferta = getOferta(body.offer);
  if (!oferta) return fallo(res, 400, 'err_offer');

  const externalId = nuevoExternalId(oferta.id);

  let token;
  try { token = tokenDeAcceso(externalId); }
  catch { console.error('[create] falta ACCESS_SECRET'); return fallo(res, 500, 'err_config'); }

  const webhookUrl = cfg.publicUrl && cfg.webhookKey
    ? `${cfg.publicUrl}/api/webhook?k=${encodeURIComponent(cfg.webhookKey)}`
    : undefined;
  if (!webhookUrl) console.warn('[create] sin webhook_url: falta PUBLIC_URL o WEBHOOK_KEY');

  /* Cobranza dinamica: se manda amount, asi el importe queda fijo en la
     cobranza y el pagador no puede pagar otra cantidad. */
  const payload = {
    currency: oferta.currency,
    amount: oferta.amount,
    external_id: externalId,
    description: oferta.descripcion,
    ...(webhookUrl ? { webhook_url: webhookUrl } : {}),
  };
  if (metodo === 'oxxo') {
    payload.method = 'OXXO';
    payload.payerData = { name: nombre };
    /* generateCheckout:false devuelve el voucher crudo en payee_data, que
       es la forma que la documentacion especifica campo por campo. La
       pagina hospedada no documenta el nombre del campo con la URL. */
    payload.generateCheckout = false;
  } else {
    payload.name = nombre;
  }

  let r;
  try {
    r = await xpag('/cashin', { method: 'POST', body: payload });
  } catch (e) {
    if (e.code === 'config_missing') {
      console.error('[create] credenciales ausentes:', e.faltan);
      return fallo(res, 500, 'err_config');
    }
    console.error('[create] red hacia XPag:', e.name);
    return fallo(res, 502, 'err_busy', { retryable: true, external_id: externalId });
  }

  if (r.http >= 400 || r.data.ok === false) {
    const code = r.data.error_code || 'cashin_failed';
    console.error('[create] XPag rechazo', r.http, code, externalId);
    /* Se devuelve el external_id para que un reintento reutilice el mismo
       y no duplique la venta. */
    return fallo(res, r.http >= 500 ? 502 : 422, claveDeError(code), {
      retryable: REINTENTABLES.has(code), external_id: externalId,
    });
  }

  const d = r.data;
  const salida = {
    ok: true,
    sandbox: Boolean(d.sandbox) || isSandbox(),
    method: metodo,
    external_id: externalId,
    transaction_id: d.transaction_id || d.request_number || null,
    access_token: token,
    offer: publica(oferta),
    amount: oferta.amount,
    currency: oferta.currency,
    /* La documentacion pide mostrar banco y beneficiario junto a la CLABE:
       que el pagador vea STP y el nombre sube la conversion del SPEI. */
    bank_name: d.bank_name || null,
    beneficiary: d.beneficiary || null,
    brand: cfg.brand || null,
  };

  if (metodo === 'oxxo') {
    const pd = d.payee_data || {};
    salida.reference = pd.reference || d.reference || null;
    salida.barcode = pd.barcode || pd.barcode_url || d.barcode || null;
    /* En la caja del OXXO, escanear un codigo de barras es mucho menos
       propenso a error que teclear la referencia. Si XPag no lo manda,
       queda anotado QUE nombres de campo si vinieron, para saber si lo
       llama de otra manera en vez de suponerlo. */
    if (!salida.barcode) {
      console.warn('[create] OXXO sin barcode. payee_data:', Object.keys(pd), 'raiz:', Object.keys(d));
    }
    if (!salida.reference) {
      console.error('[create] OXXO sin referencia:', Object.keys(d));
      return fallo(res, 502, 'err_oxxo');
    }
  } else {
    salida.clabe = d.clabe || null;
    salida.reference = d.reference || null;
    if (!salida.clabe) {
      console.error('[create] SPEI sin clabe:', Object.keys(d));
      return fallo(res, 502, 'err_spei');
    }
  }

  res.status(200).json(salida);
}
