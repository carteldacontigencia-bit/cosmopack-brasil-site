/* Pruebas de los módulos verificables sin red: validación de entrada y
   firma del enlace de acceso. Se ejecuta con: node test/lib.test.mjs */

process.env.ACCESS_SECRET = 'secreto-de-prueba-suficientemente-largo';

const { nombreLimpio, importeLimpio, cayoEnLaTrampa, metodoLimpio, whatsappLimpio } =
  await import('../api/_lib/sanitize.js');
const { tokenDeAcceso, externalIdDeToken, nuevoExternalId } =
  await import('../api/_lib/order.js');

let fallos = 0;
const ok = (cond, etiqueta, visto) => {
  console.log(`${cond ? '  ok  ' : ' FALLA'} ${etiqueta}${visto !== undefined ? '  -> ' + JSON.stringify(visto) : ''}`);
  if (!cond) fallos++;
};

console.log('\nNombre');
for (const [entrada, esperado] of [
  ['María José', 'María José'],
  ['  Ana   López  ', 'Ana López'],
  ['José Ángel Ñuño', 'José Ángel Ñuño'],
  ['Ana-Luisa Pérez', 'Ana-Luisa Pérez'],
  ['MARIA DEL CARMEN', 'MARIA DEL CARMEN'],
]) ok(nombreLimpio(entrada) === esperado, `acepta "${entrada.trim()}"`, nombreLimpio(entrada));

/* "DROP TABLE users" son solo letras y espacios, asi que PASA, y debe
   pasar: vetar palabras rechazaria nombres legitimos y no protegeria de
   nada. La inyeccion no se evita filtrando palabras sino no concatenando
   en SQL (aqui no hay SQL); el nombre viaja como valor JSON a XPag. Lo
   que si se rechaza son las FORMAS peligrosas. */
ok(nombreLimpio('DROP TABLE users') === 'DROP TABLE users',
  'letras y espacios pasan aunque parezcan SQL', nombreLimpio('DROP TABLE users'));

const NULO = String.fromCharCode(0);
for (const malo of [
  'Jo', '<script>alert(1)</script>', 'Ana 123', 'ana@correo.com',
  'Maria' + NULO, 'a'.repeat(61), '', '   ', null, undefined, 42, {},
  '{{7*7}}', '../../etc/passwd', 'Ana\\nLopez', 'Ana"Lopez', "Ana'; --",
]) ok(nombreLimpio(malo) === null, 'rechaza ' + JSON.stringify(malo ?? null).slice(0, 26));

console.log('\nImporte (min 100, max 10000)');
const RANGO = { min: 100, max: 10000 };
ok(importeLimpio(499, RANGO) === 499, 'entero');
ok(importeLimpio('499.90', RANGO) === 499.9, 'decimal con punto');
ok(importeLimpio('499,90', RANGO) === 499.9, 'decimal con coma (teclado MX)');
for (const malo of [99.99, 10000.01, 0, -100, 'NaN', Infinity, '100.999', '  ', null, [], '100; DROP'])
  ok(importeLimpio(malo, RANGO) === null, 'rechaza ' + JSON.stringify(malo ?? null));

console.log('\nTrampa y metodo');
ok(cayoEnLaTrampa({ website: 'http://spam' }) === true, 'detecta robot');
ok(cayoEnLaTrampa({ website: '' }) === false, 'humano pasa');
ok(cayoEnLaTrampa({}) === false, 'campo ausente pasa');
ok(metodoLimpio('spei') === 'spei' && metodoLimpio('oxxo') === 'oxxo', 'metodos validos');
ok(metodoLimpio('card') === null && metodoLimpio('') === null, 'otro metodo rechazado');

console.log('\nWhatsApp MX');
ok(whatsappLimpio('55 1234 5678') === '525512345678', '10 digitos');
ok(whatsappLimpio('+52 55 1234 5678') === '525512345678', 'con +52');
ok(whatsappLimpio('+521 55 1234 5678') === '525512345678', 'con +521');
ok(whatsappLimpio('123') === null, 'corto rechazado');

console.log('\nToken de acceso (HMAC)');
const id = nuevoExternalId('oferta1');
const tok = tokenDeAcceso(id);
ok(externalIdDeToken(tok) === id, 'ida y vuelta');
ok(!tok.includes(process.env.ACCESS_SECRET), 'el token NO contiene el secreto');
ok(externalIdDeToken(tok.slice(0, -1) + 'x') === null, 'firma alterada rechazada');
ok(externalIdDeToken(Buffer.from(id).toString('base64url') + '.loquesea') === null, 'firma inventada rechazada');
ok(externalIdDeToken(Buffer.from('OTRA-VENTA-999').toString('base64url') + '.' + tok.split('.')[1]) === null,
  'firma de otra venta rechazada');
ok(externalIdDeToken(Buffer.from(id).toString('base64url')) === null, 'sin firma rechazado');
for (const malo of ['', '.', 'a.b', null, 42, 'x'.repeat(400)])
  ok(externalIdDeToken(malo) === null, 'rechaza ' + JSON.stringify(malo ?? null).slice(0, 20));
ok(tok !== tokenDeAcceso(nuevoExternalId('oferta1')), 'dos ventas, dos tokens distintos');
const ids = new Set(Array.from({ length: 500 }, () => nuevoExternalId('o')));
ok(ids.size === 500, '500 external_id sin colision', ids.size);

console.log('\nSin ACCESS_SECRET configurado');
delete process.env.ACCESS_SECRET;
let lanzo = false;
try { tokenDeAcceso('X'); } catch { lanzo = true; }
ok(lanzo, 'firmar sin secreto lanza error');
ok(externalIdDeToken(tok) === null, 'verificar sin secreto devuelve null (no entrega)');

console.log(`\n${fallos === 0 ? 'TODAS LAS PRUEBAS PASARON' : fallos + ' FALLARON'}`);
process.exit(fallos ? 1 : 0);
