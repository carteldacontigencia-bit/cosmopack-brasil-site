/* GET /api/config — lo poco que el front necesita del entorno.
   Sólo valores PUBLICOS: el Pixel ID es público por naturaleza (va en el
   HTML de cualquier sitio). Aquí nunca sale una credencial. */
import { guard } from './_lib/guard.js';
import { cfg, isSandbox } from './_lib/env.js';
import { OFERTAS, publica } from './_lib/offers.js';

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'GET', rate: 60, windowMs: 60_000 });
  if (!g) return;

  res.setHeader('Cache-Control', 'public, max-age=120');
  res.status(200).json({
    ok: true,
    sandbox: isSandbox(),
    brand: cfg.brand || null,
    pixel_id: process.env.META_PIXEL_ID || null,
    /* Horas de validez que se muestran en pantalla. La documentación de
       XPag no expone vencimiento para MXN, así que este número es una
       política nuestra, configurable, no un dato del gateway. */
    ref_hours: Number(process.env.REF_HOURS || 24),
    offers: Object.values(OFERTAS).map(publica),
  });
}
