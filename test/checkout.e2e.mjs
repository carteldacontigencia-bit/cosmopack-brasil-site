/* Recorre la pantalla de pago en Chromium contra el mock.
   Requiere: node test/mock-xpag.mjs &  y  node test/dev-server.mjs &  */
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';

const URL_BASE = 'http://127.0.0.1:8080';
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

let fallos = 0;
const errores = [];
const ok = (c, etiqueta, visto) => {
  console.log(`${c ? '  ok  ' : ' FALLA'} ${etiqueta}${visto !== undefined ? '  -> ' + JSON.stringify(visto) : ''}`);
  if (!c) fallos++;
};

const simular = (payload) => fetch('http://127.0.0.1:8787/__simular', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'X-Client-Id': 'a', 'X-Client-Secret': 'b' },
  body: JSON.stringify(payload),
}).then((r) => r.json());

const nav = await chromium.launch({ executablePath: CHROME });

async function pagina(ancho = 390) {
  const ctx = await nav.newContext({ viewport: { width: ancho, height: 844 } });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errores.push('pageerror: ' + e.message));
  p.on('console', (m) => { if (m.type() === 'error' && !/favicon|ERR_CERT|fbevents/.test(m.text())) errores.push('console: ' + m.text()); });
  return { ctx, p };
}

/* ── 1. SPEI: formulario, beneficiario, datos ── */
console.log('\n1) SPEI en movil (390px)');
let { ctx, p } = await pagina();
await p.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });

ok((await p.textContent('#ofTotal')).includes('100'), 'el total sale del servidor', (await p.textContent('#ofTotal')).trim());
ok(Boolean(await p.getAttribute('#website', 'tabindex')), 'el campo trampa esta fuera del recorrido de teclado');
const trampa = await p.evaluate(() => {
  const r = document.getElementById('website').getBoundingClientRect();
  return { izq: Math.round(r.left), dentro: r.right > 0 && r.left < innerWidth };
});
ok(trampa.dentro === false, 'el campo trampa queda fuera de la ventana', trampa);

await p.click('#enviar');
ok((await p.textContent('#errName')).length > 0, 'valida el nombre antes de enviar', (await p.textContent('#errName')).trim());

await p.fill('#name', 'Ana López');
await p.click('#enviar');
await p.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });

const clabe = (await p.textContent('#vClabe')).trim();
ok(clabe === '0123 4567 8901 2345 67', 'CLABE agrupada de 4 en 4', clabe);
const lineasClabe = await p.evaluate(() => {
  const e = document.getElementById('vClabe');
  return Math.round(e.getBoundingClientRect().height / parseFloat(getComputedStyle(e).lineHeight));
});
ok(lineasClabe === 1, 'la CLABE no se parte en dos renglones', lineasClabe);
ok((await p.textContent('#vImporte')).includes('100'), 'importe exacto visible');
ok((await p.textContent('#vBanco')).includes('STP'), 'banco destino visible');

/* El nombre del extracto, que es el principal motivo de abandono */
ok(await p.isVisible('#cajaBenef'), 'la caja del beneficiario esta visible');
ok((await p.textContent('#benefNombre')).trim() === 'Zypher', 'muestra el beneficiario real', (await p.textContent('#benefNombre')).trim());
const textoBenef = (await p.textContent('#benefTexto')).trim();
ok(textoBenef.includes('Zypher') && textoBenef.includes('Marca de Prueba'),
  'explica que el extracto dira otro nombre', textoBenef.slice(0, 90));
const posBenef = await p.evaluate(() => {
  const b = document.getElementById('cajaBenef').getBoundingClientRect().top;
  const c = document.getElementById('vClabe').getBoundingClientRect().top;
  return { benef: Math.round(b), clabe: Math.round(c) };
});
ok(posBenef.benef < posBenef.clabe, 'el beneficiario va ARRIBA de la CLABE', posBenef);

/* ── 2. Selector de banco ── */
console.log('\n2) Selector de banco');
const chips = await p.$$eval('#chipsBanco .chip', (els) => els.map((e) => e.textContent.trim()));
ok(chips.length === 6, 'seis bancos', chips);
ok(['BBVA', 'Banorte', 'Santander', 'Citibanamex', 'Nu'].every((b) => chips.includes(b)), 'incluye los cinco pedidos');
await p.click('#chipsBanco .chip:nth-child(1)');
await p.waitForSelector('#pasos:not([hidden])');
const pasos = await p.$$eval('#pasosLista li', (els) => els.map((e) => e.textContent.trim()));
ok(pasos.length >= 5, 'el paso a paso tiene varios pasos', pasos.length);
ok(pasos.some((s) => s.includes('100')), 'un paso lleva el importe ya puesto', pasos.find((s) => s.includes('100')));
ok(pasos.some((s) => /REF123456|PRINCIPAL-/.test(s)), 'un paso lleva el concepto ya puesto', pasos.find((s) => /REF123456|PRINCIPAL-/.test(s)));
ok(!pasos.some((s) => s.includes('{importe}') || s.includes('{concepto}')), 'no quedan marcadores sin sustituir');

/* ── 3. Copiar ── */
console.log('\n3) Copiar');
await ctx.grantPermissions(['clipboard-read', 'clipboard-write']);
await p.click('[data-copia="vClabe"]');
await p.waitForTimeout(250);
ok((await p.textContent('[data-copia="vClabe"]')).includes('Copiado'), 'el boton confirma la copia');
const portapapeles = await p.evaluate(() => navigator.clipboard.readText());
ok(portapapeles === '012345678901234567', 'copia los 18 digitos SIN espacios', portapapeles);

/* ── 4. La referencia SOBREVIVE a que se descarte la pestana ── */
console.log('\n4) Persistencia (se recarga como si el navegador hubiera descartado la pestana)');
const pedidoAntes = (await p.textContent('#txtPedido')).trim();
const enlaceAntes = (await p.textContent('#vEnlace')).trim();
await p.reload({ waitUntil: 'load' });
await p.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
ok(await p.isHidden('#secForm'), 'no vuelve a pedir el formulario');
ok((await p.textContent('#vClabe')).trim() === clabe, 'la MISMA CLABE tras recargar', (await p.textContent('#vClabe')).trim());
ok((await p.textContent('#txtPedido')).trim() === pedidoAntes, 'el mismo numero de pedido');
ok((await p.textContent('#vEnlace')).trim() === enlaceAntes, 'el mismo enlace de acceso');

/* ── 5. Validez con cuenta regresiva ── */
console.log('\n5) Validez');
const validez1 = (await p.textContent('#txtValidez')).trim();
ok(/\d{2}:\d{2}:\d{2}/.test(validez1), 'muestra cuenta regresiva', validez1);
await p.waitForTimeout(1600);
ok((await p.textContent('#txtValidez')).trim() !== validez1, 'el reloj avanza');

/* ── 6. Guarda tu acceso ── */
console.log('\n6) Enlace de acceso y contacto opcional');
ok(enlaceAntes.includes('/api/access?t='), 'el enlace apunta a la puerta de entrega', enlaceAntes.slice(0, 60));
await p.fill('#whatsapp', '55 1234 5678');
await p.click('#btnContacto');
await p.waitForSelector('#contactoOk:not([hidden])', { timeout: 5000 });
ok(true, 'acepta el WhatsApp opcional despues de tener la referencia');

/* ── 7. Vuelve del banco: consulta al recuperar visibilidad ── */
console.log('\n7) Pago confirmado al volver a la pestana');
const externalId = pedidoAntes.match(/(PRINCIPAL-[A-Z0-9-]+)/)?.[1];
ok(Boolean(externalId), 'se pudo leer el external_id de la pantalla', externalId);
await simular({ external_id: externalId, outcome: 'paid' });
/* Se simula el regreso del app del banco sin esperar el ciclo de 6 s. */
await p.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
await p.waitForSelector('#secOk:not([hidden])', { timeout: 10000 });
ok(true, 'la pantalla pasa a confirmado');
const href = await p.getAttribute('#confBtn', 'href');
ok(href.includes('/api/access?t='), 'el boton lleva a la puerta de entrega');

/* ── 8. OXXO ── */
console.log('\n8) OXXO');
await ctx.close();
({ ctx, p } = await pagina());
await p.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
await p.fill('#name', 'Luis Hernández');
await p.check('input[value="oxxo"]');
await p.click('#enviar');
await p.waitForSelector('#panelOxxo:not([hidden])', { timeout: 8000 });
ok((await p.textContent('#vRefOxxo')).replace(/\s/g, '') === '8204240000119882', 'referencia OXXO visible');
ok(await p.isVisible('#cajaBarcode'), 'muestra el codigo de barras');
const comision = (await p.textContent('#oxxoComision')).toLowerCase();
ok(comision.includes('comisi'), 'avisa de la comision de la tienda');
const demora = (await p.textContent('#oxxoDemora')).toLowerCase();
ok(demora.includes('hora'), 'avisa de que tarda horas en confirmarse');
ok(await p.isHidden('#panelSpei'), 'no muestra el panel de SPEI');

/* ── 9. Escritorio y desbordes ── */
console.log('\n9) Escritorio 1280px');
await ctx.close();
({ ctx, p } = await pagina(1280));
await p.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
const scrollX = await p.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
ok(scrollX === false, 'sin scroll horizontal');

/* ── 10. Ingles ── */
console.log('\n10) Traducciones');
await p.goto(`${URL_BASE}/pago?lang=en`, { waitUntil: 'load' });
const enTexto = (await p.textContent('#tForm')).trim();
ok(/who is|payment/i.test(enTexto), 'el sitio responde en ingles con ?lang=en', enTexto);
await p.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
ok(/nombre|pago/i.test((await p.textContent('#tForm')).trim()), 'por defecto en espanol');

console.log('\nerrores de JS en la pagina:', errores.length ? errores : 'ninguno');
if (errores.length) fallos += errores.length;
await nav.close();
console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' FALLARON'}`);
process.exit(fallos ? 1 : 0);
