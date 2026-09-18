/* POST /api/contact — WhatsApp o correo OPCIONAL, pedido despues de que
   la referencia ya existe, para no alargar el formulario de compra.
   Se exige el token firmado para que no sirva de buzon abierto.
   Sin almacen configurado solo queda en el log del servidor; se dice
   asi en lugar de dar a entender que se guarda en algun sitio. */
import { guard, fallo } from './_lib/guard.js';
import { externalIdDeToken } from './_lib/order.js';
import { whatsappLimpio, EMAIL_RE } from './_lib/sanitize.js';

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'POST', rate: 10, windowMs: 60_000 });
  if (!g) return;

  const externalId = externalIdDeToken(g.body?.t);
  if (!externalId) return fallo(res, 403, 'err_token');

  const wa = g.body.whatsapp ? whatsappLimpio(g.body.whatsapp) : null;
  const email = typeof g.body.email === 'string' && EMAIL_RE.test(g.body.email.trim())
    ? g.body.email.trim().slice(0, 120) : null;

  if (!wa && !email) return fallo(res, 400, 'err_contact');

  console.log('[contacto]', { external_id: externalId, whatsapp: wa, email });
  res.status(200).json({ ok: true });
}
