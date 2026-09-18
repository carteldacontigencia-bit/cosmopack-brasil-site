/* GET /api/access?t=<token>
   Puerta de entrega. Verifica la firma, RECONSULTA a XPag y solo
   entonces redirige a la pagina con los PDFs. Quien pago en OXXO vuelve
   horas despues con el mismo enlace y entra.

   El redirect no protege el destino: si PRODUCT_URL fuera adivinable o
   indexable, cualquiera llega sin pagar. Debe ser una ruta aleatoria y
   con noindex. */
import { guard, fallo } from './_lib/guard.js';
import { BUMPS } from './_lib/offers.js';
import { cfg } from './_lib/env.js';
import { estadoDe } from './_lib/xpag.js';
import { externalIdDeToken, bumpsDeExternalId } from './_lib/order.js';

export default async function handler(req, res) {
  const g = await guard(req, res, { method: 'GET', rate: 30, windowMs: 60_000 });
  if (!g) return;

  const externalId = externalIdDeToken(req.query?.t);
  if (!externalId) return fallo(res, 403, 'err_token');

  let est;
  try { est = await estadoDe({ externalId }); }
  catch (e) {
    console.error('[access] consulta fallo:', e.code || e.name);
    return fallo(res, 503, 'err_busy');
  }

  if (est.status !== 'confirmed') {
    /* Todavia no pagado: no se entrega, y se dice en que estado esta para
       que la pantalla pueda explicarlo. */
    return res.status(402).json({ ok: false, error: 'err_not_paid', status: est.status });
  }

  if (!cfg.productUrl) {
    console.error('[access] falta PRODUCT_URL');
    return fallo(res, 500, 'err_config');
  }

  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');

  /* Los extras comprados viajan en la redireccion, con su ruta.
     La pagina de entrega es estatica y no puede verificar nada, asi que
     la proteccion NO es esconder el bloque: es que la ruta lleva un
     segmento aleatorio y solo sale de aqui, para quien pago. Quien
     compro solo lo principal nunca ve esas rutas y no puede adivinarlas.

     Cuales compro se lee del external_id, que va firmado: agregarse una
     letra a mano rompe la firma y no entra nada. */
  const comprados = bumpsDeExternalId(externalId)
    .map((id) => BUMPS[id])
    .map((b) => ({ t: b.descripcion, r: `${b.ruta}/${b.archivo}`, p: b.paginas }));

  const destino = comprados.length
    ? `${cfg.productUrl}${cfg.productUrl.includes('?') ? '&' : '?'}x=`
      + Buffer.from(JSON.stringify(comprados)).toString('base64url')
    : cfg.productUrl;

  res.redirect(302, destino);
}
