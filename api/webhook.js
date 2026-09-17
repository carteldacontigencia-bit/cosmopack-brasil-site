/* POST /api/webhook?k=<WEBHOOK_KEY>
   ─────────────────────────────────────────────────────────────────
   La documentacion de XPag no describe firma HMAC en el webhook. Sin
   firma, quien descubra la URL podria postear {"status":"confirmed"} y
   llevarse el producto. Por eso:
     1. la URL lleva un secreto (WEBHOOK_KEY), comparado en tiempo
        constante;
     2. el cuerpo NO se cree: se usa solo como aviso de "algo cambio" y
        se vuelve a preguntar por /consult-transaction.
   Solo se libera cuando XPag responde confirmed.
   ───────────────────────────────────────────────────────────────── */
import { timingSafeEqual } from 'node:crypto';
import { guard } from './_lib/guard.js';
import { cfg } from './_lib/env.js';
import { estadoDe } from './_lib/xpag.js';

function claveValida(dada) {
  const esperada = cfg.webhookKey;
  if (!esperada) return false;
  const a = Buffer.from(String(dada || ''));
  const b = Buffer.from(esperada);
  return a.length === b.length && timingSafeEqual(a, b);
}

export default async function handler(req, res) {
  /* checkOrigin:false — el POST viene del gateway, no de un navegador. */
  const g = await guard(req, res, { method: 'POST', rate: 300, windowMs: 60_000, checkOrigin: false });
  if (!g) return;

  if (!claveValida(req.query?.k)) {
    console.warn('[webhook] clave de URL invalida');
    return res.status(404).end();
  }

  const ev = g.body;

  /* Siempre 200: devolver error solo provoca reintentos que no arreglan
     nada de nuestro lado. */
  const responder = (nota) => {
    console.log('[webhook]', nota, {
      type: ev.type, status_recibido: ev.status,
      external_id: ev.external_id, e2e: ev.e2e, origin: ev.origin,
    });
    res.status(200).json({ received: true });
  };

  if (ev.type !== 'cashin') return responder('no es cashin, ignorado');

  const ref = ev.transaction_id || ev.request_number || ev.external_id;
  if (!ref) return responder('sin identificador, ignorado');

  /* MED: una entrada confirmada fue disputada. Llega en el MISMO
     transaction_id y el liquido se retira del saldo, asi que se revoca. */
  if (ev.status === 'med') {
    await revocar({ external_id: ev.external_id, e2e: ev.e2e });
    return responder('MED: acceso revocado');
  }

  const porTx = Boolean(ev.transaction_id || ev.request_number);
  let est;
  try {
    est = await estadoDe(porTx ? { transactionId: ref } : { externalId: ref });
  } catch (e) {
    return responder(`no se pudo verificar (${e.code || e.name}), no se libera`);
  }

  if (est.status !== 'confirmed') return responder(`XPag dice "${est.status}", no se libera`);

  await entregar({
    external_id: est.external_id || ev.external_id,
    e2e: est.e2e || ev.e2e,
    amount: est.amount, currency: est.currency,
  });
  return responder('verificado y entregado');
}

/* La entrega en si la hace /api/access cuando el comprador abre su
   enlace: verifica la firma, reconsulta y redirige. Es lo que permite
   que el pago por OXXO, que confirma horas despues, funcione sin
   almacenar nada.

   Este gancho queda para lo que SI necesita empujarse desde el servidor
   (avisar por WhatsApp, o el Purchase server-side del pixel con
   e2e como id de evento). Sin las variables de entorno correspondientes
   no hace nada. */
async function entregar(pago) {
  console.log('[entrega] PAGO CONFIRMADO', pago);
}

async function revocar(info) {
  console.warn('[entrega] REVOCAR ACCESO', info);
}
