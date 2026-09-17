#!/usr/bin/env node
/* ───────────────────────────────────────────────────────────────────
   Verifica que el XPag REAL devuelve los campos de los que depende el
   checkout. Usa el sandbox: no mueve dinero.

   Córrelo desde TU máquina (no desde un entorno con egreso bloqueado):

       node test/verificar-contrato.mjs

   Con tus credenciales de producción, en vez del sandbox:

       XPAG_CLIENT_ID=... XPAG_CLIENT_SECRET=... node test/verificar-contrato.mjs

   Si todo sale verde, el mock con el que se probó el código coincide con
   la realidad. Si algo sale rojo, ese campo cambió y hay que ajustar el
   handler que lo lee, no adivinar.
   ─────────────────────────────────────────────────────────────────── */

const BASE = process.env.XPAG_BASE_URL || 'https://api.xpag.global';
const ID = process.env.XPAG_CLIENT_ID || 'xpagsandbox_00000000';
const SECRET = process.env.XPAG_CLIENT_SECRET || '202620262026202620262026';
const esSandbox = ID === 'xpagsandbox_00000000';

let fallos = 0;
const V = (c) => (c ? '  ok  ' : ' FALLA');
const ok = (cond, etiqueta, visto) => {
  console.log(`${V(cond)} ${etiqueta}${visto !== undefined ? `  →  ${JSON.stringify(visto)}` : ''}`);
  if (!cond) fallos++;
};

async function llamar(path, { method = 'GET', body } = {}) {
  const r = await fetch(BASE + path, {
    method,
    headers: {
      'X-Client-Id': ID,
      'X-Client-Secret': SECRET,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const texto = await r.text();
  let data; try { data = JSON.parse(texto); } catch { data = { raw: texto.slice(0, 400) }; }
  return { http: r.status, data };
}

const marca = `CONTRATO-${Date.now().toString(36)}`.toUpperCase();

console.log(`\nBase: ${BASE}`);
console.log(`Modo: ${esSandbox ? 'SANDBOX (credenciales públicas, no mueve dinero)' : 'CREDENCIALES PROPIAS'}\n`);

/* ── 0. ¿Se alcanza el host? ──────────────────────────────────
   Un proxy corporativo o de entorno también responde 403, y confundirlo
   con un 403 de XPag haría que este script reporte cosas falsas. Así que
   primero se distingue una cosa de la otra. */
console.log('0) Alcance de red');
{
  let r;
  try {
    r = await llamar('/balance');
  } catch (e) {
    console.log(` FALLA no se pudo conectar a ${BASE}  →  ${e.cause?.code || e.name}`);
    console.log('\n  Revisa DNS, firewall o proxy. Este script necesita salida a internet.\n');
    process.exit(1);
  }
  const cuerpo = JSON.stringify(r.data);
  const bloqueado = /allowlist|egress|proxy|tunnel|forbidden by policy/i.test(cuerpo);
  ok(!bloqueado, `se alcanza ${BASE}`, bloqueado ? r.data : { http: r.http });
  if (bloqueado) {
    console.log('\n  La respuesta no viene de XPag sino de un proxy de red:');
    console.log('  ' + cuerpo.slice(0, 300));
    console.log('\n  Corre este script desde una máquina con salida libre, o');
    console.log('  autoriza el host api.xpag.global en la configuración de red.\n');
    process.exit(1);
  }

  /* Ahora sí: 401/403 vienen de XPag. */
  ok(r.http !== 401, 'las credenciales no son rechazadas (401)', { http: r.http });
  if (r.http === 401) {
    console.log(`\n  XPag rechazó las credenciales: ${r.data.error_code || ''} ${r.data.error || ''}`);
    console.log('  Revísalas en Dashboard → API antes de seguir.\n');
    process.exit(1);
  }
  if (r.http === 403) {
    console.log(`  nota: /balance dio 403 (${r.data.error_code || 'sin código'}). Suele ser la permiso`);
    console.log('        "balance" faltante en la llave, o KYC pendiente. El cash-in puede');
    console.log('        funcionar igual, así que el script sigue.');
  }
}

/* ── 2. Cash-in SPEI ─────────────────────────────────────────── */
console.log('\n2) Cash-in SPEI (MXN) — los campos que lee api/checkout.js');
let speiTx = null;
{
  const { http, data } = await llamar('/cashin', {
    method: 'POST',
    body: { currency: 'MXN', amount: 47.9, name: 'Prueba Contrato',
            description: 'Verificación de contrato', external_id: `${marca}-SPEI` },
  });
  ok(http < 400 && data.ok !== false, 'la cobranza se crea', { http, error_code: data.error_code });
  if (http >= 400) {
    console.log('  respuesta completa:', JSON.stringify(data, null, 2));
  } else {
    ok(typeof data.clabe === 'string' && data.clabe.length >= 16, 'data.clabe (18 dígitos)', data.clabe);
    ok('bank_name' in data, 'data.bank_name — se muestra junto a la CLABE', data.bank_name);
    ok('beneficiary' in data, 'data.beneficiary — se muestra junto a la CLABE', data.beneficiary);
    ok(Boolean(data.transaction_id || data.request_number), 'transaction_id / request_number', data.transaction_id || data.request_number);
    ok('status' in data, 'data.status', data.status);
    speiTx = data.transaction_id || data.request_number;
    const desconocidos = Object.keys(data).filter((k) => ![
      'ok','sandbox','reference','clabe','amount','fee','currency','request_number',
      'transaction_id','status','bank_name','beneficiary','static','open_value','external_id',
    ].includes(k));
    if (desconocidos.length) console.log('  nota: campos no previstos en la respuesta →', desconocidos.join(', '));
  }
}

/* ── 3. Cash-in OXXO ─────────────────────────────────────────── */
console.log('\n3) Cash-in OXXO — generateCheckout:false');
{
  const { http, data } = await llamar('/cashin', {
    method: 'POST',
    body: { currency: 'MXN', method: 'OXXO', amount: 250, generateCheckout: false,
            payerData: { name: 'Prueba Contrato', email: 'prueba@correo.com' },
            external_id: `${marca}-OXXO` },
  });
  ok(http < 400 && data.ok !== false, 'el voucher se crea', { http, error_code: data.error_code });
  if (http >= 400) {
    console.log('  respuesta completa:', JSON.stringify(data, null, 2));
  } else {
    const pd = data.payee_data || {};
    ok(Boolean(pd.reference || data.reference), 'payee_data.reference', pd.reference || data.reference);
    ok(Boolean(pd.barcode), 'payee_data.barcode (URL de imagen)', pd.barcode);
    if (!pd.barcode) console.log('  → sin barcode: la página muestra sólo la referencia, sin código de barras.');
  }
}

/* ── 4. Consulta de estado ───────────────────────────────────── */
console.log('\n4) Consulta — los campos que leen api/status.js y api/webhook.js');
if (speiTx) {
  {
    const { http, data } = await llamar(`/consult-transaction?transaction_id=${encodeURIComponent(speiTx)}`);
    ok(http < 400, 'consulta por transaction_id responde', { http });
    ok('status' in data, 'devuelve status (objeto suelto)', data.status);
    ok(!Array.isArray(data.payments), 'por transaction_id NO es lista', Array.isArray(data.payments));
  }
  {
    const { http, data } = await llamar(`/consult-transaction?external_id=${encodeURIComponent(`${marca}-SPEI`)}`);
    ok(http < 400 || http === 404, 'consulta por external_id responde', { http });
    if (http < 400) {
      const esLista = Array.isArray(data.payments);
      ok(esLista || 'status' in data, 'devuelve payments[] o status', esLista ? `payments[${data.payments.length}]` : data.status);
      console.log(`  → forma por external_id: ${esLista ? 'LISTA payments[]' : 'OBJETO suelto'} (normalizarEstado cubre las dos)`);
    }
  }
} else {
  console.log('  omitido: no hubo cobranza SPEI que consultar');
}

/* ── 5. Simulación de pago (sólo sandbox) ────────────────────── */
if (esSandbox && speiTx) {
  console.log('\n5) /sandbox/simulate — confirmar y disparar el webhook');
  const { http, data } = await llamar('/sandbox/simulate', {
    method: 'POST', body: { transaction_id: speiTx, outcome: 'paid' },
  });
  ok(http < 400 && data.ok !== false, 'la simulación responde', { http, error_code: data.error_code });
  if (http < 400) {
    await new Promise((r) => setTimeout(r, 1500));
    const c = await llamar(`/consult-transaction?transaction_id=${encodeURIComponent(speiTx)}`);
    ok(c.data.status === 'confirmed', 'tras simular, el estado es confirmed', c.data.status);
    console.log('  → si tu XPAG_WEBHOOK_URL ya está configurada, revisa los logs: debió llegar el POST.');
  }
} else if (!esSandbox) {
  console.log('\n5) /sandbox/simulate — omitido (estás con credenciales propias)');
  console.log('   Las cobranzas de arriba son REALES y quedan pendientes. Cancélalas o ignóralas.');
}

/* ── 6. Errores ──────────────────────────────────────────────── */
console.log('\n6) error_code — la lógica del checkout se apoya en esto');
{
  const { http, data } = await llamar('/cashin', {
    method: 'POST',
    body: { currency: 'MXN', method: 'OXXO', amount: 1, generateCheckout: false, external_id: `${marca}-MIN` },
  });
  ok(http >= 400 || data.ok === false, 'OXXO por 1 MXN es rechazado (mínimo 10)', { http });
  ok(typeof data.error_code === 'string', 'la respuesta trae error_code', data.error_code);
}

console.log(`\n${fallos === 0
  ? 'CONTRATO CONFIRMADO — el XPag real coincide con lo que el código espera.'
  : `${fallos} PUNTO(S) NO COINCIDEN — manda esta salida y ajusto el handler.`}\n`);
process.exit(fallos ? 1 : 0);
