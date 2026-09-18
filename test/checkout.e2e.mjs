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

/* Una violacion de CSP no lanza excepcion: el navegador la anota en la
   consola y sigue, con la pagina rota. Por eso se vigila aparte. */
const csp = [];

async function pagina(ancho = 390) {
  const ctx = await nav.newContext({ viewport: { width: ancho, height: 844 } });
  const p = await ctx.newPage();
  p.on('console', (m) => {
    const t = m.text();
    if (/Content Security Policy|Refused to (apply|load|execute)/i.test(t)) csp.push(t.slice(0, 160));
  });
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

/* ── 11. Pagina de entrega ──
   Un enlace roto aqui es una venta cobrada y un producto no entregado,
   asi que se comprueba que CADA archivo baja de verdad, no solo que el
   <a> existe. */
console.log('\n11) Pagina de entrega');
await p.goto(`${URL_BASE}/gracias-e41b9fb5ec65061a.html`, { waitUntil: 'load' });
const enlaces = await p.$$eval('a.archivo', (as) => as.map((a) => ({
  href: a.getAttribute('href'),
  titulo: a.querySelector('b')?.textContent.trim(),
})));
ok(enlaces.length === 4, 'los 4 entregables estan en la pagina', enlaces.length);
ok(!(await p.$('.pendiente')), 'ya no queda ningun bloque "pendiente"');

for (const { href, titulo } of enlaces) {
  const r = await fetch(URL_BASE + href);
  const buf = Buffer.from(await r.arrayBuffer());
  ok(r.status === 200 && buf.slice(0, 5).toString() === '%PDF-',
    `baja un PDF real: ${titulo}`, `${r.status} · ${(buf.length / 1048576).toFixed(1)} MB`);
}

/* El producto entero no puede quedar en una ruta adivinable. */
const desnudo = await fetch(`${URL_BASE}/descargas/Azucar-en-Equilibrio.pdf`);
ok(desnudo.status === 404, 'sin el segmento aleatorio no se baja nada', desnudo.status);

/* ── 12. La politica de seguridad de verdad ──
   El servidor de pruebas aplica las cabeceras de vercel.json, asi que
   aqui se ve lo mismo que en produccion. Esto existe porque la pagina
   de entrega salio publicada SIN FORMATO: tenia los estilos dentro del
   HTML y la politica declara style-src 'self', sin 'unsafe-inline'. En
   local se veia perfecta. */
console.log('\n12) Politica de seguridad');

/* Donde hay dinero: politica estricta, y las paginas escritas para
   cumplirla. */
for (const ruta of ['/pago', '/gracias-e41b9fb5ec65061a.html']) {
  const r = await fetch(URL_BASE + ruta);
  const html = await r.text();
  ok(!/<style[\s>]/i.test(html), `${ruta}: sin bloque <style> en el HTML`);
  ok(!/\sstyle=["']/i.test(html), `${ruta}: sin atributos style=`);
  ok(Boolean(r.headers.get('content-security-policy')), `${ruta}: sirve la politica estricta`);
}
ok(Boolean((await fetch(`${URL_BASE}/api/config`)).headers.get('content-security-policy')),
  '/api/config: sirve la politica estricta');

/* Y donde NO: las paginas de venta y el sitio viejo llevan CSS y
   JavaScript dentro del HTML. Aplicarles la politica estricta las deja
   sin formato -- ya paso con la pagina de entrega. Reescribirlas es
   posible; hacerlo a escondidas con una cabecera, no. */
for (const ruta of ['/azucar-en-equilibrio/']) {
  const r = await fetch(URL_BASE + ruta);
  ok(r.headers.get('content-security-policy') === null,
    `${ruta}: sin politica estricta, no se rompe`);
  ok(r.headers.get('x-content-type-options') === 'nosniff',
    `${ruta}: pero si las cabeceras que no rompen nada`);
}

/* La raiz del dominio ya no puede ser un 404: la pagina de Cosmo Pack
   se borro y el sitio pasa a ser el de las ofertas. Redireccion, no
   reescritura, para que la pagina de venta tenga UNA sola direccion y
   no se parta la medicion entre / y /azucar-en-equilibrio/. */
const raiz = await fetch(URL_BASE + '/', { redirect: 'manual' });
ok([301, 302, 307, 308].includes(raiz.status), 'la raiz redirige, no da 404', raiz.status);
ok(raiz.headers.get('location') === '/azucar-en-equilibrio/', 'y va a la pagina de venta', raiz.headers.get('location'));

/* Y la prueba definitiva: que los estilos LLEGUEN a aplicarse. */
await p.goto(`${URL_BASE}/gracias-e41b9fb5ec65061a.html`, { waitUntil: 'load' });
const caja = await p.$eval('a.archivo', (a) => getComputedStyle(a).display);
ok(caja === 'flex', 'los cards de descarga se ven como cards, no como texto suelto', caja);

/* ── 13. Ningun rastreador ajeno ──
   Raices se tradujo de otra pagina y venia con el Google Tag Manager, el
   Microsoft Clarity y el UTMify del dueño original: los datos de
   nuestros visitantes iban a sus cuentas. Se quitaron. Esta prueba
   existe para que no vuelvan sin que nadie lo note al copiar bloques
   entre paginas. */
console.log('\n13) Paginas de venta publicadas');

/* Lo que .vercelignore excluye no existe en el sitio. Raices y Pulmones
   estan fuera mientras les falten TODAS las imagenes y su liga de pago
   sea un marcador: una pagina rota con un boton muerto vende menos que
   ninguna pagina. */
for (const d of ['raices-olvidadas', 'pulmones-libres']) {
  const r = await fetch(`${URL_BASE}/${d}/`);
  ok(r.status === 404, `${d}: sin terminar, no se publica`, r.status);
}
/* Y el generador de los PDFs tampoco, o el producto entero seria
   gratis para quien escriba la ruta. */
ok((await fetch(`${URL_BASE}/entregables/out/Azucar-en-Equilibrio.pdf`)).status === 404,
  'el generador de PDFs no se publica');
const PERMITIDOS = ['127.0.0.1', 'fonts.googleapis.com', 'fonts.gstatic.com', 'connect.facebook.net'];
for (const d of ['azucar-en-equilibrio']) {
  const ctx2 = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const p2 = await ctx2.newPage();
  const ajenos = new Set();
  p2.on('request', (r) => {
    const h = new URL(r.url()).hostname;
    if (!PERMITIDOS.includes(h)) ajenos.add(h);
  });
  /* Se intercepta el script de Meta: en las pruebas no hay salida a
     internet, y lo que interesa es QUE eventos se piden, no que Meta
     conteste. */
  const eventos = [];
  await p2.route('https://connect.facebook.net/**', (r) => r.fulfill({ body: '', contentType: 'text/javascript' }));
  await p2.addInitScript(() => {
    window.__ev = [];
    window.fbq = function () { window.__ev.push([...arguments]); };
    window.fbq.queue = []; window.fbq.loaded = true; window.fbq.push = window.fbq;
  });
  await p2.goto(`${URL_BASE}/${d}/`, { waitUntil: 'load' });
  ok(ajenos.size === 0, `${d}: no llama a ningun tercero`, [...ajenos]);

  /* Ninguna imagen rota. La pagina de Azucar salio publicada con los 11
     archivos de assets/ ausentes: cuadros grises donde iba la portada y
     las vistas del libro. Una portada rota en una pagina de venta es
     dinero de anuncio tirado. */
  const rotas = await p2.evaluate(() => [...document.images]
    .filter((i) => !(i.complete && i.naturalWidth > 0))
    .map((i) => (i.currentSrc || i.getAttribute('src') || '').split('/').pop()));
  ok(rotas.length === 0, `${d}: sin imagenes rotas`, rotas);

  const disparados = await p2.evaluate(() => window.__ev.map((e) => e.slice(0, 2).join(' ')));
  ok(disparados.some((e) => e.includes('init 4479089439026636')), `${d}: inicia el pixel correcto`);
  ok(disparados.some((e) => e.includes('track PageView')), `${d}: manda PageView`);
  ok(disparados.some((e) => e.includes('track ViewContent')), `${d}: manda ViewContent`);
  const html = await (await fetch(`${URL_BASE}/${d}/`)).text();
  ok(!/vovomei|utmify|clarity\.ms/i.test(html.replace(/<!--[\s\S]*?-->/g, '')),
    `${d}: sin rastros del original en el codigo`);
  await ctx2.close();
}

console.log('violaciones de la politica:', csp.length ? csp : 'ninguna');
if (csp.length) fallos += csp.length;

console.log('\nerrores de JS en la pagina:', errores.length ? errores : 'ninguno');
if (errores.length) fallos += errores.length;
await nav.close();
console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' FALLARON'}`);
process.exit(fallos ? 1 : 0);
