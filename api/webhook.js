/* POST /api/webhook — receptor del webhook de XPag.
   ────────────────────────────────────────────────────────────────
   La documentación de XPag no describe firma HMAC en el webhook. Sin
   firma, cualquiera que descubra esta URL podría postear
   {"status":"confirmed"} y llevarse el producto. Por eso este handler
   NO confía en el cuerpo: lo usa sólo como aviso de "algo cambió" y
   vuelve a preguntarle a XPag por /consult-transaction. Sólo libera
   cuando XPag confirma.
   ──────────────────────────────────────────────────────────────── */

import { aplicarCors, leerJson, xpag, normalizarEstado } from './_xpag.js';

export default async function handler(req, res) {
  if (aplicarCors(req, res)) return;
  if (req.method !== 'POST') return res.status(405).end();

  const evento = await leerJson(req);

  /* Se responde 200 de inmediato en todos los casos: si devolvemos error,
     XPag reintenta y no hay nada que reintentar de su lado. */
  const responder = (nota) => {
    console.log('[webhook]', nota, {
      type: evento.type, status_recibido: evento.status,
      external_id: evento.external_id, e2e: evento.e2e,
    });
    res.status(200).json({ received: true });
  };

  if (evento.type !== 'cashin') return responder('no es cashin, ignorado');

  const ref = evento.transaction_id || evento.request_number || evento.external_id;
  if (!ref) return responder('sin identificador, ignorado');

  /* MED: una entrada ya confirmada fue disputada por el pagador. Llega en
     el MISMO transaction_id de la cobranza original y el líquido se
     retira del saldo, así que el acceso se revoca. */
  if (evento.status === 'med') {
    await revocarAcceso({ external_id: evento.external_id, e2e: evento.e2e, motivo: 'med' });
    return responder('MED: acceso revocado');
  }

  const esTransaccion = Boolean(evento.transaction_id || evento.request_number);
  const query = esTransaccion
    ? `transaction_id=${encodeURIComponent(ref)}`
    : `external_id=${encodeURIComponent(ref)}`;

  let verificado;
  try {
    const r = await xpag(`/consult-transaction?${query}`);
    if (r.httpStatus >= 400) return responder(`consulta devolvió ${r.httpStatus}, no se libera`);
    verificado = normalizarEstado(r.data);
  } catch {
    return responder('no se pudo verificar contra XPag, no se libera');
  }

  if (verificado.status !== 'confirmed') {
    return responder(`XPag dice "${verificado.status}", no se libera`);
  }

  await entregar({
    external_id: verificado.external_id || evento.external_id,
    e2e: verificado.e2e || evento.e2e,
    amount: verificado.amount,
    currency: verificado.currency,
  });

  return responder('verificado y entregado');
}

/* ── Entrega ────────────────────────────────────────────────────
   Aquí va lo que pasa cuando el pago es real: mandar el correo con el
   PDF, dar de alta en el área de miembros, avisar por WhatsApp.

   Dos cosas que hacen falta antes de enchufar un correo aquí:

   1. IDEMPOTENCIA. El webhook puede llegar más de una vez para el mismo
      pago. Hay que guardar el `e2e` (único por pago, es la llave de
      reconciliación que indica la documentación) y salir temprano si ya
      se entregó, o el comprador recibe el correo tres veces.

   2. ALMACENAMIENTO. Para mandar el correo hace falta el email del
      comprador, que se captura en /api/checkout y no viaja en el webhook.
      Hay que guardar { external_id → email } al crear la cobranza.

   Mientras no haya almacén, el flujo funciona igual: la página del
   checkout consulta /api/status y muestra el acceso en pantalla cuando
   XPag confirma. Esto sólo queda registrado en los logs.            */
async function entregar(pago) {
  console.log('[entrega] PAGO CONFIRMADO', pago);
  // TODO: guardar e2e para no duplicar, y enviar el acceso por correo.
}

async function revocarAcceso(info) {
  console.warn('[entrega] REVOCAR ACCESO', info);
  // TODO: bloquear la descarga / dar de baja al comprador.
}
