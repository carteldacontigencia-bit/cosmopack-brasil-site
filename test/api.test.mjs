/* Pruebas de los handlers contra el mock. Requiere el mock en :8787.
   node test/mock-xpag.mjs &  y luego  node test/api.test.mjs */

process.env.XPAG_BASE_URL = 'http://127.0.0.1:8787';
process.env.XPAG_CLIENT_ID = 'test_id';
process.env.XPAG_CLIENT_SECRET = 'test_secret';
process.env.ACCESS_SECRET = 'secreto-de-prueba-largo-y-aleatorio';
process.env.WEBHOOK_KEY = 'clave-de-webhook-de-prueba';
process.env.PUBLIC_URL = 'http://127.0.0.1:8080';
process.env.BRAND_NAME = 'Marca de Prueba';
process.env.PRODUCT_URL = 'http://127.0.0.1:8080/gracias-prueba.html';
process.env.SITE_ORIGIN = 'http://127.0.0.1:8080';

const create = (await import('../api/create.js')).default;
const status = (await import('../api/status.js')).default;
const access = (await import('../api/access.js')).default;
const webhook = (await import('../api/webhook.js')).default;
const contact = (await import('../api/contact.js')).default;
const { OFERTAS } = await import('../api/_lib/offers.js');

const PRECIO = OFERTAS.principal.amount;

let fallos = 0;
const ok = (c, etiqueta, visto) => {
  console.log(`${c ? '  ok  ' : ' FALLA'} ${etiqueta}${visto !== undefined ? '  -> ' + JSON.stringify(visto) : ''}`);
  if (!c) fallos++;
};

function res() {
  const o = { code: 0, body: null, headers: {} };
  o.status = (c) => { o.code = c; return o; };
  o.json = (b) => { o.body = b; return o; };
  o.redirect = (c, loc) => { o.code = c; o.headers.Location = loc; return o; };
  o.end = () => o;
  o.setHeader = (k, v) => { o.headers[k] = v; };
  return o;
}
let nIp = 0;
const ipUnica = () => `203.0.113.${(nIp++ % 250) + 1}`;
const req = (method, body, query = {}, headers = {}) => ({
  method, body, query,
  headers: {
    origin: 'http://127.0.0.1:8080',
    'x-forwarded-for': ipUnica(),
    ...headers,
  },
});
/* Para probar el limitador hace falta repetir DESDE LA MISMA IP. */
const reqMismaIp = (ip, body) => ({
  method: 'POST', body, query: {},
  headers: { origin: 'http://127.0.0.1:8080', 'x-forwarded-for': ip },
});

const simular = (payload) => fetch('http://127.0.0.1:8787/__simular', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Client-Id': 'a', 'X-Client-Secret': 'b' },
  body: JSON.stringify(payload),
}).then((r) => r.json());

const capturarLogs = async (fn) => {
  const logs = [];
  const l = console.log, w = console.warn, e = console.error;
  console.log = console.warn = console.error = (...a) => logs.push(a.map(String).join(' '));
  try { await fn(); } finally { console.log = l; console.warn = w; console.error = e; }
  return logs.join(' | ');
};

console.log(`\nPrecio del catalogo: ${PRECIO} MXN`);

console.log('\n1) SPEI — camino feliz');
let r = res();
await create(req('POST', { offer: 'principal', name: 'Ana Lopez', method: 'spei' }), r);
ok(r.code === 200 && r.body.ok, 'devuelve 200');
ok(r.body.clabe === '012345678901234567', 'trae la CLABE');
ok(r.body.bank_name && r.body.beneficiary === 'Zypher', 'trae banco y beneficiario', r.body.beneficiary);
ok(r.body.brand === 'Marca de Prueba', 'trae la marca para comparar con el beneficiario');
ok(r.body.amount === PRECIO, 'importe del catalogo', r.body.amount);
ok(typeof r.body.access_token === 'string' && r.body.access_token.includes('.'), 'trae token de acceso');
const cuerpo = JSON.stringify(r.body);
ok(!cuerpo.includes('test_secret') && !cuerpo.includes(process.env.ACCESS_SECRET),
  'NINGUN secreto sale al navegador');
const pedido = r.body;

console.log('\n2) El precio no viene del navegador');
r = res();
await create(req('POST', { offer: 'principal', name: 'Ana Lopez', method: 'spei', amount: 1, price: 1 }), r);
ok(r.body.amount === PRECIO, 'amount del cliente ignorado', r.body.amount);

console.log('\n3) Validacion y trampa');
r = res(); await create(req('POST', { offer: 'principal', name: 'Jo', method: 'spei' }), r);
ok(r.code === 400 && r.body.error === 'err_name', 'nombre corto rechazado', r.body.error);
r = res(); await create(req('POST', { offer: 'principal', name: '<script>x</script>', method: 'spei' }), r);
ok(r.code === 400, 'nombre con etiquetas rechazado');
r = res(); await create(req('POST', { offer: 'principal', name: 'Ana Lopez', method: 'card' }), r);
ok(r.code === 400 && r.body.error === 'err_method', 'metodo invalido rechazado');
r = res(); await create(req('POST', { offer: 'inexistente', name: 'Ana Lopez', method: 'spei' }), r);
ok(r.code === 400 && r.body.error === 'err_offer', 'oferta desconocida rechazada');
r = res(); await create(req('POST', { offer: 'principal', name: 'Ana Lopez', method: 'spei', website: 'spam' }), r);
ok(r.code === 202 && !r.body.ok, 'trampa: responde sin crear cobranza', r.code);
r = res(); await create(req('GET', {}), r);
ok(r.code === 405, 'GET rechazado');
r = res(); await create(req('POST', { name: 'Ana Lopez' }, {}, { origin: 'https://sitio-ajeno.com' }), r);
ok(r.code === 403 && r.body.error === 'origin', 'origen ajeno rechazado');
r = res(); await create(req('POST', {}, {}, { 'content-length': '999999' }), r);
ok(r.code === 413, 'cuerpo enorme rechazado');

console.log('\n4) OXXO');
r = res();
await create(req('POST', { offer: 'principal', name: 'Luis Hernandez', method: 'oxxo' }), r);
ok(r.code === 200 && r.body.reference === '8204240000119882', 'trae la referencia');
ok(String(r.body.barcode || '').endsWith('.png'), 'trae el codigo de barras');
const pedidoOxxo = r.body;

console.log('\n5) external_id unico por venta');
const ids = new Set();
for (let i = 0; i < 6; i++) {
  const q = res();
  await create(req('POST', { offer: 'principal', name: 'Ana Lopez', method: 'spei' }), q);
  ids.add(q.body.external_id);
}
ok(ids.size === 6, 'seis ventas, seis identificadores', ids.size);

console.log('\n6) Estado — solo con token firmado');
r = res(); await status(req('GET', null, { t: pedido.access_token, tx: pedido.transaction_id }), r);
ok(r.code === 200 && r.body.status === 'pending', 'pendiente antes de pagar', r.body.status);
r = res(); await status(req('GET', null, { t: 'inventado.firma' }), r);
ok(r.code === 400 && r.body.error === 'err_token', 'token invalido rechazado');
r = res(); await status(req('GET', null, {}), r);
ok(r.code === 400, 'sin token: 400');

console.log('\n7) Acceso antes de pagar: NO entrega');
r = res(); await access(req('GET', null, { t: pedido.access_token }), r);
ok(r.code === 402 && r.body.error === 'err_not_paid', 'devuelve 402, no redirige', r.code);
ok(!r.headers.Location, 'sin cabecera Location');
r = res(); await access(req('GET', null, { t: 'basura' }), r);
ok(r.code === 403, 'token basura: 403');

console.log('\n8) Webhook FALSIFICADO (nadie pago)');
let logs = await capturarLogs(async () => {
  r = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'confirmed', amount: PRECIO,
    transaction_id: pedido.transaction_id, external_id: pedido.external_id, e2e: 'E-FALSO',
  }, { k: process.env.WEBHOOK_KEY }), r);
});
ok(r.code === 200, 'responde 200 igual (para que el gateway no reintente)');
ok(!logs.includes('PAGO CONFIRMADO'), 'NO entrega el producto', logs.slice(0, 80));

console.log('\n9) Webhook sin la clave de la URL');
logs = await capturarLogs(async () => {
  r = res();
  await webhook(req('POST', { type: 'cashin', status: 'confirmed' }, { k: 'clave-equivocada' }), r);
});
ok(r.code === 404, 'clave equivocada: 404 y no dice por que', r.code);
logs = await capturarLogs(async () => {
  r = res();
  await webhook(req('POST', { type: 'cashin', status: 'confirmed' }, {}), r);
});
ok(r.code === 404, 'sin clave: 404');

console.log('\n10) Pago real, luego webhook y acceso');
await simular({ transaction_id: pedido.transaction_id, outcome: 'paid' });
logs = await capturarLogs(async () => {
  r = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'confirmed',
    transaction_id: pedido.transaction_id, external_id: pedido.external_id, e2e: 'E-REAL',
  }, { k: process.env.WEBHOOK_KEY }), r);
});
ok(logs.includes('PAGO CONFIRMADO'), 'ahora si entrega');
r = res(); await status(req('GET', null, { t: pedido.access_token }), r);
ok(r.body.status === 'confirmed', 'status confirmado por external_id (lista payments[])');
ok(Boolean(r.body.event_id), 'devuelve event_id para el pixel', r.body.event_id);
r = res(); await status(req('GET', null, { t: pedido.access_token, tx: pedido.transaction_id }), r);
ok(r.body.status === 'confirmed', 'status confirmado por transaction_id (objeto suelto)');
r = res(); await access(req('GET', null, { t: pedido.access_token }), r);
ok(r.code === 302 && r.headers.Location === process.env.PRODUCT_URL, 'acceso redirige al material', r.code);
ok(r.headers['X-Robots-Tag']?.includes('noindex'), 'la entrega va con noindex');

console.log('\n11) El token de una venta no abre otra');
r = res(); await access(req('GET', null, { t: pedidoOxxo.access_token }), r);
ok(r.code === 402, 'la venta OXXO sin pagar sigue cerrada aunque la otra ya pago', r.code);

console.log('\n12) OXXO confirma horas despues: el mismo enlace entra');
await simular({ transaction_id: pedidoOxxo.transaction_id, outcome: 'paid' });
r = res(); await access(req('GET', null, { t: pedidoOxxo.access_token }), r);
ok(r.code === 302, 'con el enlace guardado, entra sin nada almacenado de nuestro lado', r.code);

console.log('\n13) MED (disputa) revoca');
logs = await capturarLogs(async () => {
  r = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'med',
    transaction_id: pedido.transaction_id, external_id: pedido.external_id,
  }, { k: process.env.WEBHOOK_KEY }), r);
});
ok(logs.includes('REVOCAR ACCESO'), 'dispara la revocacion');

console.log('\n14) Contacto opcional');
r = res(); await contact(req('POST', { t: pedido.access_token, whatsapp: '55 1234 5678' }), r);
ok(r.code === 200 && r.body.ok, 'acepta WhatsApp con token valido');
r = res(); await contact(req('POST', { t: 'basura', whatsapp: '5512345678' }), r);
ok(r.code === 403, 'sin token valido no es buzon abierto');
r = res(); await contact(req('POST', { t: pedido.access_token, whatsapp: '123' }), r);
ok(r.code === 400, 'numero corto rechazado');

console.log('\n15) Limite por IP (y que RATE_CREATE lo gobierne)');
process.env.RATE_CREATE = '5';   /* el valor de produccion es 30 */
const IP = '198.51.100.7';
let ultimo = 0, bloqueadas = 0;
for (let i = 0; i < 9; i++) {
  const q = res();
  await create(reqMismaIp(IP, { offer: 'principal', name: 'Ana Lopez', method: 'spei' }), q);
  ultimo = q.code;
  if (q.code === 429) bloqueadas++;
}
ok(bloqueadas > 0, `frena la rafaga desde una sola IP (${bloqueadas} de 9 bloqueadas con RATE_CREATE=5)`);
ok(ultimo === 429, 'la ultima de la rafaga es 429', ultimo);
const otra = res();
await create(reqMismaIp('198.51.100.8', { offer: 'principal', name: 'Ana Lopez', method: 'spei' }), otra);
ok(otra.code === 200, 'otra IP no queda castigada por la rafaga ajena', otra.code);
delete process.env.RATE_CREATE;

console.log('\n16) Purchase de Meta desde el servidor');
/* Es el motivo de que exista el envio server-side: en OXXO la persona
   paga en la tienda y casi nunca reabre la pantalla, asi que el evento
   del navegador no llega nunca. */
process.env.META_API_BASE = 'http://127.0.0.1:8788';
process.env.META_PIXEL_ID = '4479089439026636';
process.env.META_CAPI_TOKEN = 'token-de-prueba';
await fetch('http://127.0.0.1:8788/__limpiar');

const qOxxo = res();
await create(req('POST', { offer: 'principal', name: 'Luis Hernandez', method: 'oxxo' }), qOxxo);
const ventaOxxo = qOxxo.body;
await simular({ transaction_id: ventaOxxo.transaction_id, outcome: 'paid' });
await capturarLogs(async () => {
  const q = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'confirmed', amount: PRECIO, currency: 'MXN',
    transaction_id: ventaOxxo.transaction_id, external_id: ventaOxxo.external_id,
    e2e: 'E-OXXO-REAL',
  }, { k: process.env.WEBHOOK_KEY }), q);
});
const enviados = await (await fetch('http://127.0.0.1:8788/__recibidos')).json();
ok(enviados.length === 1, 'el webhook mando UN Purchase a Meta', enviados.length);
const ev = enviados[0]?.data?.[0] || {};
ok(enviados[0]?.pixelId === '4479089439026636', 'al Pixel ID correcto', enviados[0]?.pixelId);
ok(ev.event_name === 'Purchase', 'evento Purchase', ev.event_name);
ok(ev.action_source === 'website', 'action_source website');
ok(ev.custom_data?.value === PRECIO && ev.custom_data?.currency === 'MXN', 'valor y moneda', ev.custom_data);
ok(Boolean(ev.event_id), 'lleva event_id para deduplicar', ev.event_id);
ok(/^[a-f0-9]{64}$/.test(ev.user_data?.external_id || ''), 'external_id en SHA-256', (ev.user_data?.external_id || '').slice(0, 16) + '...');
ok(/^[a-f0-9]{64}$/.test(ev.user_data?.fn || ''), 'nombre del pagador en SHA-256 (recuperado de XPag)');
const crudo = JSON.stringify(enviados[0]);
ok(!crudo.includes('Luis') && !crudo.includes('Hernandez'), 'NINGUN dato personal viaja en claro');
ok(crudo.includes('token-de-prueba'), 'el token va en el cuerpo, no en la URL');
/* El pais no es una suposicion: SPEI y OXXO solo existen en Mexico. Es
   una señal de coincidencia mas, y aqui hacen falta, porque el evento
   del servidor no lleva las cookies _fbp/_fbc del navegador. */
ok(/^[a-f0-9]{64}$/.test(ev.user_data?.country || ''), 'manda pais, que el carril de pago ya implica');
/* Y ni un solo campo puede ir sin cifrar, hoy ni cuando alguien agregue
   otro mañana. */
const sinCifrar = Object.entries(ev.user_data || {}).filter(([, v]) => !/^[a-f0-9]{64}$/.test(String(v)));
ok(sinCifrar.length === 0, 'TODOS los campos de user_data van en SHA-256', sinCifrar.map(([k]) => k));

console.log('\n17) Un pago confirmado dos veces no manda dos Purchase distintos');
await fetch('http://127.0.0.1:8788/__limpiar');
for (let i = 0; i < 2; i++) {
  await capturarLogs(async () => {
    const q = res();
    await webhook(req('POST', {
      type: 'cashin', status: 'confirmed', amount: PRECIO, currency: 'MXN',
      transaction_id: ventaOxxo.transaction_id, external_id: ventaOxxo.external_id,
    }, { k: process.env.WEBHOOK_KEY }), q);
  });
}
const repetidos = await (await fetch('http://127.0.0.1:8788/__recibidos')).json();
const idsEvento = new Set(repetidos.map((r) => r.data[0].event_id));
ok(idsEvento.size === 1, 'el mismo event_id en los reenvios, para que Meta deduplique', [...idsEvento]);

console.log('\n18) Sin token de Meta no se envia nada');
await fetch('http://127.0.0.1:8788/__limpiar');
delete process.env.META_CAPI_TOKEN;
await capturarLogs(async () => {
  const q = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'confirmed',
    transaction_id: ventaOxxo.transaction_id, external_id: ventaOxxo.external_id,
  }, { k: process.env.WEBHOOK_KEY }), q);
});
const nada = await (await fetch('http://127.0.0.1:8788/__recibidos')).json();
ok(nada.length === 0, 'no se envia nada y la entrega sigue funcionando', nada.length);
process.env.META_CAPI_TOKEN = 'token-de-prueba';

console.log('\n19) Si Meta falla, la entrega NO se rompe');
process.env.META_API_BASE = 'http://127.0.0.1:9999';  /* nadie escucha */
let entregoIgual = '';
entregoIgual = await capturarLogs(async () => {
  const q = res();
  await webhook(req('POST', {
    type: 'cashin', status: 'confirmed',
    transaction_id: ventaOxxo.transaction_id, external_id: ventaOxxo.external_id,
  }, { k: process.env.WEBHOOK_KEY }), q);
  ok(q.code === 200, 'el webhook responde 200 aunque Meta este caido', q.code);
});
ok(entregoIgual.includes('PAGO CONFIRMADO'), 'el pago se sigue dando por entregado');
const accesoIgual = res();
await access(req('GET', null, { t: ventaOxxo.access_token }), accesoIgual);
ok(accesoIgual.code === 302, 'y el comprador entra a su material', accesoIgual.code);
process.env.META_API_BASE = 'http://127.0.0.1:8788';

console.log('\n20) Cada endpoint con su propio cupo');
const IP2 = '198.51.100.99';
const reqIp = (metodo, body, query, ruta) => ({
  method: metodo, body, query,
  url: ruta,
  headers: { origin: 'http://127.0.0.1:8080', 'x-forwarded-for': IP2 },
});
/* 40 sondeos de estado, como quien espera en la pantalla de pago. */
let sondeos429 = 0;
for (let i = 0; i < 40; i++) {
  const q = res();
  await status(reqIp('GET', null, { t: pedido.access_token }, '/api/status'), q);
  if (q.code === 429) sondeos429++;
}
/* Tras todo ese sondeo, crear una cobranza desde la MISMA IP debe seguir
   permitido: antes compartian contador y esto devolvia 429. */
const tras = res();
await create(reqIp('POST', { offer: 'principal', name: 'Ana Lopez', method: 'spei' }, {}, '/api/create'), tras);
ok(tras.code === 200, 'sondear el estado no agota el cupo de crear cobranza', tras.code);
const trasContacto = res();
await contact(reqIp('POST', { t: pedido.access_token, whatsapp: '5512345678' }, {}, '/api/contact'), trasContacto);
ok(trasContacto.code === 200, 'ni el de guardar el contacto', trasContacto.code);

console.log('\n20b) El diagnostico dice a donde apunta PUBLIC_URL');
{
  /* La URL del webhook se arma con PUBLIC_URL. Si apunta a un dominio
     viejo, XPag avisa a un sitio que ya no existe: el SPEI sigue
     funcionando porque la pantalla pregunta sola, pero el OXXO deja de
     entregarse -- y no hay ningun error visible. Por eso el host sale en
     el diagnostico, para verlo sin entrar a la consola de Vercel. */
  const config = (await import('../api/config.js')).default;

  const q = res();
  await config({ ...req('GET'), method: 'GET' }, q);
  ok(q.body.public_url_host === '127.0.0.1:8080', 'muestra el host de PUBLIC_URL', q.body.public_url_host);

  /* Nunca la URL entera ni nada mas: es el host y punto. */
  ok(!JSON.stringify(q.body).includes('/gracias-'), 'no filtra la ruta de entrega');

  const guardado = process.env.PUBLIC_URL;
  delete process.env.PUBLIC_URL;
  delete process.env.SITE_ORIGIN;
  const q2 = res();
  await config({ ...req('GET'), method: 'GET' }, q2);
  ok(q2.body.public_url_host === null, 'sin PUBLIC_URL devuelve null, no revienta', q2.body.public_url_host);
  ok(q2.body.avisos.includes('PUBLIC_URL'), 'y lo reclama en avisos');
  process.env.PUBLIC_URL = guardado;
  process.env.SITE_ORIGIN = guardado;
}

console.log('\n21) El simulador no existe fuera de sandbox');
{
  /* Esta suite corre SIN XPAG_SANDBOX. El endpoint tiene que responder
     404 antes de mirar nada: sin esto, cualquiera podria marcar su
     propio pago como confirmado y llevarse el producto. No hay una
     bandera aparte que alguien pueda olvidar encendida -- se apaga solo
     al quitar XPAG_SANDBOX. */
  const simular = (await import('../api/simular.js')).default;
  delete process.env.XPAG_SANDBOX;

  const q1 = res();
  await simular(req('POST', { t: pedido.access_token, outcome: 'paid' }), q1);
  ok(q1.code === 404, 'sin XPAG_SANDBOX responde 404', q1.code);
  ok(q1.body === null, 'y no dice nada de por que', q1.body);

  /* Con token invalido tampoco, y por el mismo 404: no distingue. */
  const q2 = res();
  await simular(req('POST', { t: 'basura', outcome: 'paid' }), q2);
  ok(q2.code === 404, 'un token invalido recibe el mismo 404', q2.code);

  /* Y con sandbox encendido si atiende, para que la prueba demuestre
     que el 404 viene de la bandera y no de que el modulo este roto. */
  process.env.XPAG_SANDBOX = '1';
  const q3 = res();
  await simular(req('POST', { t: 'basura', outcome: 'paid' }), q3);
  ok(q3.code === 400, 'en sandbox si atiende (y rechaza el token malo)', q3.code);
  delete process.env.XPAG_SANDBOX;
}

console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' FALLARON'}`);
process.exit(fallos ? 1 : 0);
