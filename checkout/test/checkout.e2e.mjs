import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const errores=[];
const p=await b.newPage({viewport:{width:390,height:844}});
p.on('pageerror',e=>errores.push('pageerror: '+e.message));
p.on('console',m=>{ if(m.type()==='error') errores.push('console: '+m.text()); });

await p.goto('http://127.0.0.1:8080/checkout?p=azucar',{waitUntil:'load'});
console.log('titulo:', await p.title());
console.log('total mostrado:', (await p.textContent('#resumenTotal')).trim() || '(vacío)');

/* validación del lado del cliente */
await p.click('#enviar');
console.log('error de nombre:', (await p.textContent('#errName')).trim());

await p.fill('#name','Ana López');
await p.fill('#email','no-es-correo');
await p.click('#enviar');
console.log('error de correo:', (await p.textContent('#errEmail')).trim());

/* SPEI */
await p.fill('#email','ana@correo.com');
await p.click('#enviar');
await p.waitForSelector('#instrucciones:not(.oculto)',{timeout:8000});
console.log('CLABE en pantalla:', (await p.textContent('#vClabe')).trim());
console.log('importe:', (await p.textContent('#vMonto')).trim());
console.log('banco:', (await p.textContent('#vBanco')).trim());
console.log('beneficiario:', (await p.textContent('#vBenef')).trim());
const pedidoId=(await p.textContent('#vPedido')).trim();
console.log('pedido:', pedidoId);
await p.screenshot({path:'/tmp/co-spei.png'});

/* copiar */
await p.context().grantPermissions(['clipboard-read','clipboard-write']);
await p.click('[data-copia="vClabe"]');
await p.waitForTimeout(250);
console.log('boton copiar dice:', (await p.textContent('[data-copia="vClabe"]')).trim());

/* pagar en el mock y esperar que la pagina lo detecte sola */
const est=await (await fetch('http://127.0.0.1:8080/api/status?external_id='+encodeURIComponent(pedidoId))).json();
console.log('status antes de pagar:', est.status);
const tx=(await (await fetch('http://127.0.0.1:8080/api/status?external_id='+encodeURIComponent(pedidoId))).json());
await fetch('http://127.0.0.1:8787/__pagar',{method:'POST',headers:{'Content-Type':'application/json','X-Client-Id':'a','X-Client-Secret':'b'},body:JSON.stringify({transaction_id:pedidoId})});
/* el mock indexa por transaction_id; pagamos por el external_id tambien */
const lista=await (await fetch('http://127.0.0.1:8787/consult-transaction?external_id='+encodeURIComponent(pedidoId),{headers:{'X-Client-Id':'a','X-Client-Secret':'b'}})).json();
if(lista.payments) await fetch('http://127.0.0.1:8787/__pagar',{method:'POST',headers:{'Content-Type':'application/json','X-Client-Id':'a','X-Client-Secret':'b'},body:JSON.stringify({transaction_id:lista.payments[0].id})});
console.log('esperando que la pagina detecte el pago (hasta 20s)...');
await p.waitForSelector('#confirmado:not(.oculto)',{timeout:20000});
console.log('pantalla de exito:', (await p.textContent('#confirmado h2')).trim(), '| correo:', (await p.textContent('#vEmailOk')).trim());
await p.screenshot({path:'/tmp/co-exito.png'});

/* OXXO */
const p2=await b.newPage({viewport:{width:390,height:844}});
p2.on('pageerror',e=>errores.push('pageerror(oxxo): '+e.message));
await p2.goto('http://127.0.0.1:8080/checkout?p=pulmones',{waitUntil:'load'});
await p2.fill('#name','Luis Hernandez'); await p2.fill('#email','luis@correo.com');
await p2.check('input[value="oxxo"]');
await p2.click('#enviar');
await p2.waitForSelector('#panelOxxo:not(.oculto)',{timeout:8000});
console.log('referencia OXXO:', (await p2.textContent('#vRefOxxo')).trim(), '| importe:', (await p2.textContent('#vMontoOxxo')).trim());
await p2.screenshot({path:'/tmp/co-oxxo.png'});

/* escritorio */
const p3=await b.newPage({viewport:{width:1280,height:900}});
await p3.goto('http://127.0.0.1:8080/checkout?p=azucar',{waitUntil:'load'});
const scroll=await p3.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+1);
console.log('scroll horizontal en 1280px:', scroll);
await p3.screenshot({path:'/tmp/co-desktop.png'});

console.log('\nerrores de JS:', errores.length?errores:'ninguno');
await b.close();
