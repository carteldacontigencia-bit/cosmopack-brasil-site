/* Ejercita los tres handlers como lo haría Vercel, contra el mock. */
process.env.XPAG_BASE_URL = 'http://127.0.0.1:8787';
process.env.XPAG_CLIENT_ID = 'test_id';
process.env.XPAG_CLIENT_SECRET = 'test_secret';
process.env.XPAG_WEBHOOK_URL = 'https://ejemplo.com/api/webhook';

const checkout = (await import('../api/checkout.js')).default;
const status   = (await import('../api/status.js')).default;
const webhook  = (await import('../api/webhook.js')).default;

function res() {
  const o = { code: 0, body: null, headers: {} };
  o.status = (c) => { o.code = c; return o; };
  o.json = (b) => { o.body = b; return o; };
  o.end = () => o; o.setHeader = (k, v) => { o.headers[k] = v; };
  return o;
}
const req = (method, body, query = {}) => ({ method, body, query, headers: {} });
let fallos = 0;
const ok = (cond, etiqueta, extra='') => { console.log(`${cond ? '  ok  ' : ' FALLA'} ${etiqueta}${extra?' — '+extra:''}`); if(!cond) fallos++; };

console.log('\n1) SPEI — camino feliz');
let r = res(); await checkout(req('POST', { product:'azucar', name:'Juan Pérez', email:'juan@correo.com', method:'spei' }), r);
ok(r.code === 200 && r.body.ok, 'devuelve 200');
ok(r.body.clabe === '012345678901234567', 'trae la CLABE');
ok(r.body.bank_name && r.body.beneficiary, 'trae banco y beneficiario');
ok(r.body.amount === 47.9, 'importe del catálogo, no del cliente', String(r.body.amount));
ok(!JSON.stringify(r.body).includes('test_secret'), 'el secreto NO sale al cliente');
const pedido = r.body;

console.log('\n2) El cliente NO puede fijar el precio');
r = res(); await checkout(req('POST', { product:'azucar', name:'Juan Pérez', email:'j@c.com', method:'spei', amount: 1, price: 1 }), r);
ok(r.body.amount === 47.9, 'amount del cliente ignorado', String(r.body.amount));

console.log('\n3) Validación de entrada');
r = res(); await checkout(req('POST', { product:'azucar', name:'Jo', email:'j@c.com' }), r);
ok(r.code === 400 && r.body.field === 'name', 'nombre corto rechazado');
r = res(); await checkout(req('POST', { product:'azucar', name:'Juan Pérez', email:'no-es-correo' }), r);
ok(r.code === 400 && r.body.field === 'email', 'correo inválido rechazado');
r = res(); await checkout(req('POST', { product:'inexistente', name:'Juan Pérez', email:'j@c.com' }), r);
ok(r.code === 400, 'producto desconocido rechazado');
r = res(); await checkout(req('GET', null, { product: 'azucar' }), r);
ok(r.code === 200 && r.body.amount === 47.9 && !r.body.clabe, 'GET devuelve precio y NO crea cobranza');
r = res(); await checkout(req('GET', null, {}), r);
ok(r.code === 404, 'GET sin producto: 404');
r = res(); await checkout(req('DELETE', {}), r);
ok(r.code === 405, 'DELETE rechazado');

console.log('\n4) OXXO');
r = res(); await checkout(req('POST', { product:'azucar', name:'Luis Hernandez', email:'luis@correo.com', method:'oxxo' }), r);
ok(r.code === 200 && r.body.reference === '8204240000119882', 'trae la referencia');
ok(r.body.barcode?.endsWith('.png'), 'trae el código de barras');

console.log('\n5) external_id único por venta');
const ids = new Set();
for (let i = 0; i < 5; i++) { const q = res(); await checkout(req('POST', { product:'azucar', name:'Ana López', email:'a@c.com' }), q); ids.add(q.body.external_id); }
ok(ids.size === 5, 'cinco ventas, cinco external_id', `${ids.size}/5`);

console.log('\n6) Estado antes de pagar');
r = res(); await status(req('GET', null, { external_id: pedido.external_id }), r);
ok(r.code === 200 && r.body.status === 'pending', 'pendiente');
r = res(); await status(req('GET', null, { external_id: 'NO-EXISTE' }), r);
ok(r.body.status === 'pending', '404 de XPag se traduce a pendiente, no a error');
r = res(); await status(req('GET', null, {}), r);
ok(r.code === 400, 'sin identificador: 400');

console.log('\n7) Webhook FALSO (nadie pagó) — no debe liberar');
const logs = []; const origLog = console.log, origErr = console.warn;
console.log = (...a) => logs.push(a.join(' '));
r = res(); await webhook(req('POST', { type:'cashin', status:'confirmed', amount:47.9, transaction_id: pedido.transaction_id, external_id: pedido.external_id, e2e:'E-FALSO' }), r);
console.log = origLog;
ok(r.code === 200, 'responde 200 igual (para que XPag no reintente)');
ok(!logs.join(' ').includes('PAGO CONFIRMADO'), 'NO entregó el producto', logs.join(' | ').slice(0,90));

console.log('\n8) Pago real en el mock, luego el webhook');
await fetch('http://127.0.0.1:8787/__pagar', { method:'POST', headers:{'Content-Type':'application/json','X-Client-Id':'a','X-Client-Secret':'b'}, body: JSON.stringify({ transaction_id: pedido.transaction_id }) });
logs.length = 0; console.log = (...a) => logs.push(a.join(' '));
r = res(); await webhook(req('POST', { type:'cashin', status:'confirmed', transaction_id: pedido.transaction_id, external_id: pedido.external_id, e2e:'E-REAL' }), r);
console.log = origLog;
ok(logs.join(' ').includes('PAGO CONFIRMADO'), 'ahora sí entrega');
r = res(); await status(req('GET', null, { external_id: pedido.external_id }), r);
ok(r.body.status === 'confirmed', 'status refleja confirmado (lista payments[])');
r = res(); await status(req('GET', null, { transaction_id: pedido.transaction_id }), r);
ok(r.body.status === 'confirmed', 'status por transaction_id (objeto suelto)');

console.log('\n9) MED (disputa) revoca');
logs.length = 0; const warns = [];
console.warn = (...a) => warns.push(a.join(' ')); console.log = (...a) => logs.push(a.join(' '));
r = res(); await webhook(req('POST', { type:'cashin', status:'med', transaction_id: pedido.transaction_id, external_id: pedido.external_id }), r);
console.log = origLog; console.warn = origErr;
ok(warns.join(' ').includes('REVOCAR ACCESO'), 'dispara la revocación');

console.log('\n10) Error del proveedor se traduce a español, sin filtrar el mensaje crudo');
process.env.XPAG_BASE_URL = 'http://127.0.0.1:8787';
r = res(); await checkout(req('POST', { product:'azucar', name:'Test Usuario', email:'t@c.com', method:'oxxo' }), r);
const guardar = (await import('../api/_xpag.js'));
ok(typeof guardar.mensajeDeError('amount_below_min') === 'string' && !guardar.mensajeDeError('amount_below_min').includes('Valor'), 'amount_below_min traducido');

console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' PRUEBA(S) FALLARON'}`);
process.exit(fallos ? 1 : 0);
