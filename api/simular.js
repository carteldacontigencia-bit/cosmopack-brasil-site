/* POST /api/simular  — SOLO EN SANDBOX
   ─────────────────────────────────────────────────────────────────
   Existe para probar lo unico que no se puede probar de otra forma:
   que el comprador reciba los PDFs solo, despues de que el pago
   confirma. Sin esto habria que ir a una tienda OXXO a pagar de
   verdad para saber si la entrega funciona.

   Fuera de sandbox NO EXISTE: responde 404 antes de mirar nada mas,
   asi que al quitar XPAG_SANDBOX se apaga solo. No hay una bandera que
   alguien pueda olvidar encendida.

   Pide el mismo token firmado que /api/status, de modo que nadie pueda
   tocar cobranzas ajenas probando identificadores.

   La respuesta incluye el codigo de error crudo de XPag. En cualquier
   otro endpoint eso seria una fuga; aqui es justamente el trabajo: si
   /sandbox/simulate espera otros nombres de campo, la pantalla lo dice
   en vez de fallar en silencio.                                     */
import { guard, fallo } from './_lib/guard.js';
import { isSandbox } from './_lib/env.js';
import { xpag, estadoDe } from './_lib/xpag.js';
import { externalIdDeToken } from './_lib/order.js';

const RESULTADOS = new Set(['paid', 'failed', 'expired']);

export default async function handler(req, res) {
  if (!isSandbox()) return res.status(404).end();

  const g = await guard(req, res, { method: 'POST', rate: 30, windowMs: 60_000 });
  if (!g) return;

  const externalId = externalIdDeToken(g.body?.t);
  if (!externalId) return fallo(res, 400, 'err_token');

  const outcome = RESULTADOS.has(g.body?.outcome) ? g.body.outcome : 'paid';

  /* El transaction_id no se acepta del navegador: se vuelve a pedir a
     XPag a partir del external_id firmado. */
  let est;
  try {
    est = await estadoDe({ externalId });
  } catch (e) {
    return fallo(res, 502, 'err_busy');
  }
  const tx = est.transaction_id;
  if (!tx) return res.status(200).json({ ok: false, nota: 'XPag todavia no da transaction_id', estado: est.status });

  const r = await xpag('/sandbox/simulate', {
    method: 'POST',
    body: { transaction_id: tx, request_number: tx, outcome },
  });

  res.status(200).json({
    ok: r.http < 400,
    http: r.http,
    /* Crudo A PROPOSITO, y solo aqui: es lo que deja ver si el cuerpo
       que mandamos tiene los nombres que XPag espera. */
    respuesta: r.data,
  });
}
