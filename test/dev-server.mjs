/* Servidor de desarrollo: sirve public/ y enruta /api/* a los handlers,
   como hace Vercel. Puerto 8080. */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

process.env.XPAG_BASE_URL ||= 'http://127.0.0.1:8787';
process.env.XPAG_CLIENT_ID ||= 'test_id';
process.env.XPAG_CLIENT_SECRET ||= 'test_secret';
process.env.ACCESS_SECRET ||= 'secreto-de-prueba-largo-y-aleatorio';
process.env.WEBHOOK_KEY ||= 'clave-de-webhook-de-prueba';
process.env.PUBLIC_URL ||= 'http://127.0.0.1:8080';
process.env.BRAND_NAME ||= 'Marca de Prueba';
process.env.PRODUCT_URL ||= 'http://127.0.0.1:8080/gracias-prueba.html';
process.env.REF_HOURS ||= '24';
/* Las pruebas se repiten desde 127.0.0.1: sin esto el limitador las frena. */
process.env.RATE_CREATE ||= '500';

const RAIZ = new URL('../', import.meta.url).pathname;

/* Las MISMAS cabeceras que Vercel aplica en produccion, leidas del
   propio vercel.json. Sin esto el servidor de pruebas era mas permisivo
   que el sitio real: una pagina con <style> dentro del HTML se veia
   perfecta aqui y salia SIN FORMATO publicada, porque la politica
   declara style-src 'self' y el navegador bloquea el bloque en linea.
   Eso ya paso una vez con la pagina de entrega. */
const REGLAS = JSON.parse(fs.readFileSync(path.join(RAIZ, 'vercel.json'), 'utf8')).headers || [];
/* Los "source" que usa este vercel.json —/(.*), /api/(.*) y la
   alternancia de gracias/descargas— ya son expresiones regulares
   validas, asi que se usan tal cual. Vercel acepta mas sintaxis
   (:parametros, modificadores); si algun dia se usa alguna, hay que
   traducirla aqui. */
const aRegex = (fuente) => new RegExp('^' + fuente + '$');
function cabecerasDe(ruta) {
  const out = {};
  for (const r of REGLAS) {
    if (aRegex(r.source).test(ruta)) for (const h of r.headers) out[h.key] = h.value;
  }
  return out;
}
const rutas = {};
for (const n of ['config', 'create', 'status', 'access', 'webhook', 'contact']) {
  rutas['/api/' + n] = (await import(`../api/${n}.js`)).default;
}

const TIPOS = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.pdf': 'application/pdf',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};

http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  const h = rutas[url.pathname];
  if (h) {
    req.query = Object.fromEntries(url.searchParams);
    /* Las cabeceras de vercel.json tambien valen para /api/*. Ningun
       handler pone las mismas claves, asi que no hay que decidir cual
       gana -- y es a proposito: una regla por cabecera, en un solo
       sitio. */
    for (const [k, v] of Object.entries(cabecerasDe(url.pathname))) res.setHeader(k, v);
    const setHeader = res.setHeader.bind(res);
    res.status = (c) => { res.statusCode = c; return res; };
    res.json = (o) => { setHeader('Content-Type', 'application/json'); res.end(JSON.stringify(o)); return res; };
    res.redirect = (c, loc) => { res.statusCode = c; setHeader('Location', loc); res.end(); return res; };
    try { return await h(req, res); }
    catch (e) {
      console.error('[dev] handler lanzo:', e);
      if (!res.headersSent) { res.statusCode = 500; res.end('{"ok":false,"error":"err_generic"}'); }
      return;
    }
  }

  let f = url.pathname === '/' || url.pathname === '/pago' ? '/checkout.html' : url.pathname;
  /* Vercel sirve /carpeta/ como /carpeta/index.html. Sin esto las
     paginas de venta no se podian probar aqui: daban 404. */
  if (f.endsWith('/')) f += 'index.html';
  const abs = path.join(RAIZ, path.normalize(f).replace(/^(\.\.[/\\])+/, ''));
  try {
    const buf = fs.readFileSync(abs);
    res.writeHead(200, {
      'Content-Type': TIPOS[path.extname(abs)] || 'application/octet-stream',
      ...cabecerasDe(url.pathname),
    });
    res.end(buf);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<p>no encontrado</p>');
  }
}).listen(8080, () => console.log('dev en :8080'));
