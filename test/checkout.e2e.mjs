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

/* El precio se lee del servidor, que es su unica fuente. Escrito a mano
   aqui, cada cambio de precio rompia las pruebas por el motivo
   equivocado. */
const { OFERTAS } = await import('../api/_lib/offers.js');
const PRECIO = String(OFERTAS.principal.amount);

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

ok((await p.textContent('#ofTotal')).includes(PRECIO), 'el total sale del servidor', (await p.textContent('#ofTotal')).trim());
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
ok((await p.textContent('#vImporte')).includes(PRECIO), 'importe exacto visible');
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
ok(pasos.some((x) => x.includes(PRECIO)), 'un paso lleva el importe ya puesto', pasos.find((x) => x.includes(PRECIO)));
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
await p.reload({ waitUntil: 'load' });
await p.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
ok(await p.isHidden('#secForm'), 'no vuelve a pedir el formulario');
ok((await p.textContent('#vClabe')).trim() === clabe, 'la MISMA CLABE tras recargar', (await p.textContent('#vClabe')).trim());
ok((await p.textContent('#txtPedido')).trim() === pedidoAntes, 'el mismo numero de pedido');

/* ── 5. Validez con cuenta regresiva ── */
console.log('\n5) Validez');
const validez1 = (await p.textContent('#txtValidez')).trim();
ok(/\d{2}:\d{2}:\d{2}/.test(validez1), 'muestra cuenta regresiva', validez1);
await p.waitForTimeout(1600);
ok((await p.textContent('#txtValidez')).trim() !== validez1, 'el reloj avanza');

/* ── 6. El bloque "Guarda tu acceso" ya no esta ──
   Se quito a peticion del vendedor. El campo de WhatsApp ademas decia
   "te lo mandamos" y /api/contact nunca mando nada: solo anotaba el
   numero en el log.

   Lo que esto cuesta esta medido justo abajo, en la prueba 7: quien
   vuelve en el mismo navegador sigue entrando. Quien borre el
   historial o cambie de telefono, ya no. */
console.log('\n6) El bloque de enlace y WhatsApp ya no se ensena');
ok(!(await p.$('#vEnlace')), 'no se ensena el enlace de acceso en pantalla');
ok(!(await p.$('#whatsapp')), 'ni el campo de WhatsApp');
ok(!(await p.$('#btnContacto')), 'ni su boton');
ok(errores.length === 0, 'y el codigo que los llenaba no revienta sin ellos', errores);

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

/* El generador de los PDFs no se publica, o el producto entero seria
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

/* ── 12b. La pagina de venta y el cobro dicen el mismo precio ──
   Son dos archivos distintos: el precio real vive en offers.js y el de
   la pagina esta escrito en el HTML. Si se separan, la persona hace
   clic en "$140" y la pantalla de pago le pide otra cosa -- que es el
   momento exacto en que deja de confiar y se va. */
console.log('\n12b) El precio coincide en los dos lados');
{
  const html = await (await fetch(`${URL_BASE}/azucar-en-equilibrio/`)).text();
  const sinComentarios = html.replace(/<!--[\s\S]*?-->/g, '');

  const enElBloque = (sinComentarios.match(/<div class="preco"><span>\$<\/span>(\d+)<\/div>/) || [])[1];
  ok(enElBloque === PRECIO, 'el bloque de oferta lleva el precio del servidor', { pagina: enElBloque, servidor: PRECIO });

  const enElBoton = (sinComentarios.match(/POR \$(\d+)/) || [])[1];
  ok(enElBoton === PRECIO, 'y el boton de compra tambien', { boton: enElBoton, servidor: PRECIO });

  /* El precio tachado tiene que ser MAYOR que el que se cobra, o el
     descuento no existe y el bloque miente. */
  const ancla = (sinComentarios.match(/De \$(\d+) MXN por/) || [])[1];
  ok(ancla && Number(ancla) > Number(PRECIO), 'el precio tachado es mayor que el que se cobra', { tachado: ancla, cobrado: PRECIO });
}

/* ── 12c. Order bumps en pantalla ── */
console.log('\n12c) Order bumps');
{
  const ctxB = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const pB = await ctxB.newPage();
  await pB.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });

  const cajas = await pB.$$('#bumps input[type=checkbox]');
  ok(cajas.length === 2, 'se ensenan dos extras, no tres', cajas.length);

  /* Marcados de origen convierten mas y aqui son un problema: con
     transferencia, un importe distinto al esperado ya dentro del app del
     banco es abandono, y ademas es cobro no autorizado expresamente. */
  const marcadas = await pB.$$eval('#bumps input:checked', (x) => x.length);
  ok(marcadas === 0, 'ninguno viene marcado de origen', marcadas);

  ok((await pB.textContent('#ofTotal')).includes(PRECIO), 'el total empieza en el precio base');

  await cajas[0].check();
  const conUno = (await pB.textContent('#ofTotal')).trim();
  ok(conUno.includes('229'), 'al marcar, el total sube en pantalla', conUno);

  await cajas[0].uncheck();
  ok((await pB.textContent('#ofTotal')).includes(PRECIO), 'al desmarcar, vuelve');

  /* Y lo que manda es el servidor: se marca uno y se comprueba el
     importe que llega a la pantalla de pago. */
  await cajas[1].check();
  await pB.fill('#name', 'Ana Lopez');
  await pB.click('#enviar');
  await pB.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
  const importe = (await pB.textContent('#vImporte')).trim();
  ok(importe.includes('199'), 'la referencia se genera por el total con extra', importe);

  /* Camino completo con extra: pagar y recibir los archivos de mas. */
  await pB.click('button.sim[data-outcome="paid"]');
  await pB.waitForSelector('#secOk:not([hidden])', { timeout: 15000 });
  const href = await pB.getAttribute('#confBtn', 'href');
  const r = await fetch(URL_BASE + href, { redirect: 'manual' });
  const destino = r.headers.get('location') || '';
  ok(/[?&]x=/.test(destino), 'el enlace de entrega lleva el extra comprado');

  /* La pagina de entrega tiene que ensenarlo, y el archivo bajar. */
  await pB.goto(destino, { waitUntil: 'load' });
  const extras = await pB.$$eval('#extras a.archivo', (as) => as.map((a) => a.getAttribute('href')));
  ok(extras.length === 1, 'la pagina de entrega ensena un extra', extras.length);
  const pdf = await fetch(URL_BASE + extras[0]);
  const buf = Buffer.from(await pdf.arrayBuffer());
  ok(pdf.status === 200 && buf.slice(0, 5).toString() === '%PDF-',
    'y el archivo baja de verdad', `${pdf.status} · ${(buf.length / 1048576).toFixed(1)} MB`);

  /* Sin el parametro, la pagina no ensena nada de mas. */
  await pB.goto(`${URL_BASE}/gracias-e41b9fb5ec65061a.html`, { waitUntil: 'load' });
  ok(!(await pB.isVisible('#cajaExtras')), 'sin comprar extras, la pagina no los ensena');

  /* Y el HTML de la pagina NO puede llevar las rutas escritas, o
     cualquiera que compre lo principal se las lleva gratis. */
  const html = await (await fetch(`${URL_BASE}/gracias-e41b9fb5ec65061a.html`)).text();
  for (const carpeta of ['c7f2a91e40b8d356', '5b04e8c2d1f7a690', '9a3e17d6b085c4f2']) {
    ok(!html.includes(carpeta), `la ruta del extra no esta en el HTML (${carpeta.slice(0, 6)}...)`);
  }
  const js = await (await fetch(`${URL_BASE}/assets/extras.js`)).text();
  ok(!/c7f2a91e|5b04e8c2|9a3e17d6/.test(js), 'ni en el JavaScript de la pagina');

  await ctxB.close();
}

/* ── 13a. Una cobranza del sandbox no puede sobrevivir a produccion ──
   Paso de verdad: al quitar XPAG_SANDBOX, el navegador seguia
   ensenando la cobranza vieja guardada en el aparato -- con la CLABE de
   una cuenta de pruebas y la banda naranja encima. Un comprador real
   habria transferido dinero a una cuenta que no cobra. */
console.log('\n13a) Cobranza guardada de otro entorno');
{
  const ctxS = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const pS = await ctxS.newPage();
  await pS.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
  await pS.fill('#name', 'Ana Lopez');
  await pS.click('#enviar');
  await pS.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
  const clabeVieja = (await pS.textContent('#vClabe')).trim();

  /* Vuelve a entrar en el MISMO aparato: la referencia tiene que seguir
     ahi, que es justo para lo que se guarda. */
  await pS.reload({ waitUntil: 'load' });
  await pS.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
  ok((await pS.textContent('#vClabe')).trim() === clabeVieja,
    'en el mismo entorno la referencia sobrevive a recargar');

  /* Ahora el servidor deja de estar en sandbox. */
  await pS.route('**/api/config', async (r) => {
    const orig = await r.fetch();
    const d = await orig.json();
    await r.fulfill({ json: { ...d, sandbox: false } });
  });
  await pS.reload({ waitUntil: 'load' });
  await pS.waitForSelector('#secForm:not([hidden])', { timeout: 8000 });
  ok(true, 'al cambiar de entorno vuelve al formulario, no a la CLABE vieja');
  ok(!(await pS.isVisible('#avisoPrueba')), 'y la banda de prueba desaparece');
  ok(!(await pS.isVisible('#simBotones')), 'y los botones de simular tambien');
  await ctxS.close();
}

/* ── 13b. La pantalla del OXXO no es la del banco ── */
console.log('\n13b) OXXO');
{
  const ctxO = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const pO = await ctxO.newPage();
  await pO.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
  await pO.check('input[name="method"][value="oxxo"]');
  await pO.fill('#name', 'Luis Hernandez');
  await pO.click('#enviar');
  await pO.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });

  ok(await pO.isVisible('#panelOxxo'), 'muestra el panel de OXXO');
  ok(!(await pO.isVisible('#panelSpei')), 'y no el de transferencia');

  /* La caja del beneficiario es cosa del banco: en la caja del OXXO se
     entrega efectivo contra una referencia y nadie enseña un nombre. El
     titulo decia "antes de ir a tu banco". */
  ok(!(await pO.isVisible('#cajaBenef')), 'sin la caja de beneficiario, que es del banco');

  /* Una referencia con letras no se parte en grupos de 4: "sbx_ b8ca
     210d" parece rota y hace dudar de si los espacios van tecleados. */
  const refTexto = (await pO.textContent('#vRefOxxo')).trim();
  const refPlana = await pO.getAttribute('#vRefOxxo', 'data-plano');
  ok(/^\d+$/.test(refPlana) || !/\s/.test(refTexto),
    'la referencia con letras se muestra entera, sin espacios', refTexto);
  ok(refPlana && refPlana.length > 6, 'y el valor a copiar va sin espacios', refPlana);

  await ctxO.close();

  /* Y ahora la forma que devuelve el sandbox REAL: con letras. Hace
     falta un contexto nuevo porque la pantalla recuerda la referencia
     anterior en el aparato y se salta el formulario -- que es
     justamente lo que tiene que hacer con un comprador real. */
  const ctxO2 = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const pO2 = await ctxO2.newPage();
  await pO2.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
  await pO2.check('input[name="method"][value="oxxo"]');
  await pO2.fill('#name', 'Prueba Sandbox');
  await pO2.click('#enviar');
  await pO2.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });
  const conLetras = (await pO2.textContent('#vRefOxxo')).trim();
  ok(/^sbx_/.test(conLetras), 'llega una referencia con letras', conLetras);
  ok(!/\s/.test(conLetras), 'y se muestra entera, sin partir en grupos de 4', conLetras);
  await ctxO2.close();
}

/* ── 14. EL CAMINO COMPLETO: pagar → recibir ──
   Lo unico que de verdad importa y lo ultimo que faltaba probar. Se
   hace con el boton de simulacion, que es el mismo camino que sigue un
   pago real: XPag marca confirmado, el sondeo de la pantalla lo
   descubre solo, y el enlace firmado entrega los PDFs.
   Nada aqui se empuja a mano: si la pantalla cambia, es porque
   funciono. */
console.log('\n14) De pagar a recibir, sin tocar nada');
{
  const ctx3 = await nav.newContext({ viewport: { width: 390, height: 844 } });
  const p3 = await ctx3.newPage();
  await p3.goto(`${URL_BASE}/pago`, { waitUntil: 'load' });
  await p3.fill('#name', 'Ana Lopez');
  await p3.click('#enviar');
  await p3.waitForSelector('#secPago:not([hidden])', { timeout: 8000 });

  const clabe = (await p3.textContent('#vClabe')).replace(/\s/g, '');
  ok(/^\d{18}$/.test(clabe), 'la CLABE tiene 18 digitos', clabe);

  const botonSim = await p3.$('button.sim[data-outcome="paid"]');
  ok(Boolean(botonSim), 'en sandbox aparece el boton de simular');
  ok(await p3.isVisible('#simBotones'), 'y esta visible');

  await botonSim.click();

  /* La pantalla de exito NO se fuerza: la descubre el sondeo. */
  await p3.waitForSelector('#secOk:not([hidden])', { timeout: 15000 });
  ok(true, 'la pantalla pasa a confirmada sola, por el sondeo');

  /* Y el enlace de entrega tiene que llevar a los PDFs de verdad. */
  const href = await p3.getAttribute('#confBtn', 'href');
  ok(/^\/api\/access\?t=/.test(href), 'el boton lleva al enlace firmado', href);

  const entrega = await fetch(URL_BASE + href, { redirect: 'manual' });
  ok(entrega.status === 302, 'el enlace redirige, no da error', entrega.status);
  const destino = entrega.headers.get('location');
  ok(/gracias-/.test(destino || ''), 'y va a la pagina de entrega', destino);

  await ctx3.close();
}

/* Un token valido NO basta si el pago no confirmo: el enlace
   reconsulta a XPag cada vez. */
{
  const r = await fetch(`${URL_BASE}/api/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Origin: URL_BASE },
    body: JSON.stringify({ offer: 'principal', name: 'Sin Pagar', method: 'spei' }),
  });
  const pendiente = await r.json();
  const sinPagar = await fetch(`${URL_BASE}/api/access?t=${encodeURIComponent(pendiente.access_token)}`, { redirect: 'manual' });
  ok(sinPagar.status !== 302 || !/gracias-/.test(sinPagar.headers.get('location') || ''),
    'sin pagar, el mismo enlace NO entrega', sinPagar.status);
}

console.log('violaciones de la politica:', csp.length ? csp : 'ninguna');
if (csp.length) fallos += csp.length;

console.log('\nerrores de JS en la pagina:', errores.length ? errores : 'ninguno');
if (errores.length) fallos += errores.length;
await nav.close();
console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' FALLARON'}`);
process.exit(fallos ? 1 : 0);
