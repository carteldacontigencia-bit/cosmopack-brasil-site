/* GET /api/config — lo poco que el front necesita del entorno.
   Sólo valores PUBLICOS: el Pixel ID es público por naturaleza (va en el
   HTML de cualquier sitio). Aquí nunca sale una credencial. */
import { guard } from './_lib/guard.js';
import { cfg, isSandbox, estadoDelEntorno } from './_lib/env.js';
import { OFERTAS, publica, BUMPS, BUMPS_VISIBLES, bumpPublico } from './_lib/offers.js';

const hostDe = (u) => { try { return new URL(u).host; } catch { return null; } };

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'GET', rate: 60, windowMs: 60_000 });
  if (!g) return;

  /* El Cache-Control lo pone vercel.json: no-store para todo /api/*.
     Antes este handler pedia 120s de cache y quedaban dos reglas
     peleando por la misma cabecera. Ademas la respuesta ahora lleva el
     diagnostico del entorno, que no debe quedarse guardado en un CDN. */
  const entorno = estadoDelEntorno();
  res.status(200).json({
    ok: true,
    sandbox: isSandbox(),
    /* Qué casillas de Vercel siguen vacías. Sólo nombres, nunca
       valores: sirve para configurar sin adivinar. */
    listo: entorno.listo,
    faltan: entorno.faltan,
    avisos: entorno.avisos,
    brand: cfg.brand || null,
    /* SOLO el host de PUBLIC_URL, que es publico por definicion: es la
       direccion del propio sitio. Sirve para ver de un vistazo si apunta
       aqui. Si no apunta, la URL del webhook que se le manda a XPag va a
       un sitio equivocado y el OXXO deja de entregarse solo -- sin error
       visible en ninguna parte, porque el SPEI sigue funcionando por el
       sondeo. Es el tipo de fallo que solo aparece cuando alguien ya
       pago. */
    public_url_host: hostDe(cfg.publicUrl),
    pixel_id: process.env.META_PIXEL_ID || null,
    /* Horas de validez que se muestran en pantalla. La documentación de
       XPag no expone vencimiento para MXN, así que este número es una
       política nuestra, configurable, no un dato del gateway. */
    ref_hours: Number(process.env.REF_HOURS || 24),
    offers: Object.values(OFERTAS).map(publica),
    /* Solo los que se ensenan en el checkout, y solo su id, importe y
       claves de texto. La ruta del archivo NO sale de aqui: esa la
       manda /api/access, y solo a quien pago. */
    bumps: BUMPS_VISIBLES.filter((id) => BUMPS[id]).map((id) => bumpPublico(BUMPS[id])),
  });
}
