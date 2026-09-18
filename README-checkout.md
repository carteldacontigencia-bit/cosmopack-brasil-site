# Checkout propio — SPEI y OXXO (MXN) sobre XPag

Página estática más funciones serverless en `/api`. Sin tarjeta, sin
registro, sin login. **Sin base de datos.**

## Archivos

```
api/_lib/env.js        configuración (getters, lee el entorno en vivo)
api/_lib/guard.js      método, origen, tamaño del cuerpo, límite por IP
api/_lib/xpag.js       cliente de XPag y error_code → clave de traducción
api/_lib/order.js      external_id por venta y enlace de acceso firmado
api/_lib/sanitize.js   nombre, importe, método, trampa, WhatsApp MX
api/_lib/offers.js     TABLA DE PRECIOS (única fuente de verdad)

api/config.js          valores públicos para el front
api/create.js          crea la cobranza → CLABE o referencia OXXO
api/status.js          ¿ya pagó? (pregunta a XPag, no a un almacén)
api/access.js          puerta de entrega: verifica, reconsulta, redirige
api/webhook.js         recibe el aviso de XPag y lo VERIFICA
api/contact.js         WhatsApp opcional, después de la referencia

checkout.html          la pantalla
assets/app.js          lógica: persistencia, sondeo, copiar, bancos
assets/i18n.js         TODOS los textos, es y en, en un solo archivo
assets/pixel.js        Meta Pixel
assets/checkout.css    estilos
assets/gracias.css     estilos de la pagina de entrega

test/                  mock de XPag + tres suites
vercel.json            cabeceras de seguridad y rutas
.env.example           las variables que hay que llenar
```

## Desplegar

1. Importar el repo en Vercel. Sin framework, sin build command.
2. Copiar las variables de `.env.example` en Settings → Environment
   Variables. Generar los dos secretos con `openssl rand -base64 48`.
3. Empezar con `XPAG_SANDBOX=1`. La pantalla muestra una banda naranja y
   ninguna petición toca dinero real.
4. Probar: abrir `/pago`, generar una referencia, y confirmarla con
   `POST /sandbox/simulate` de XPag (`outcome`: `paid`, `failed`,
   `expired` — conviene probar los tres).
5. Cambiar a credenciales propias y **borrar** `XPAG_SANDBOX`.

## Saber qué falta configurar: `/api/config`

Abrir `https://TU-SITIO/api/config` en el navegador. Responde, entre
otras cosas:

```json
{ "sandbox": true, "listo": true, "faltan": [], "avisos": ["META_CAPI_TOKEN"] }
```

- `faltan` — sin esas variables **no se puede vender**. `listo` es
  `false` mientras quede alguna.
- `avisos` — se vende, pero se pierde algo: sin `META_CAPI_TOKEN` las
  ventas por OXXO no llegan a Meta; sin `BRAND_NAME` la pantalla no
  puede explicar el nombre del beneficiario.

Salen **sólo los nombres**, nunca los valores ni su longitud. Los
nombres ya están en `.env.example`, que es público, y todo lo que puede
faltar falla cerrado: sin `WEBHOOK_KEY` el webhook responde 404 a todo,
sin `ACCESS_SECRET` no se firma ningún enlace. Saber que falta no sirve
para entrar.

En sandbox no pide `XPAG_CLIENT_ID` ni `XPAG_CLIENT_SECRET`: ahí las
credenciales son las públicas de XPag y van en el código.

## Sin base de datos: cómo funciona la entrega

El enlace de acceso es `/api/access?t=<external_id>.<firma HMAC>`.

Al abrirlo, el servidor verifica la firma (comparación en tiempo
constante) y **reconsulta el pago a XPag**. Sólo redirige a los PDFs si
XPag responde `confirmed`.

Eso resuelve el caso del OXXO, que confirma horas después: la persona
vuelve con el mismo enlace y entra. No hay estado local que pueda
desincronizarse del pago real, y no hay servicio extra que mantener.

El enlace se guarda en el aparato por 24 h, así que si el navegador
descarta la pestaña mientras la persona está en el app del banco, al
volver encuentra la misma CLABE.

**La página de los PDFs necesita una ruta aleatoria y `noindex`.** El
redirect verifica el pago, pero no puede impedir que alguien comparta la
URL final una vez que la tiene.

Los archivos van en `descargas/<segmento aleatorio>/`, no sueltos en
`descargas/`: `/descargas/Azucar-en-Equilibrio.pdf` es el nombre del
producto y cualquiera lo escribe. Con el segmento, el archivo está tan
protegido como la propia página de entrega. Una prueba comprueba que sin
el segmento la ruta da 404.

`entregables/` —el generador de los PDFs, con los mismos archivos en
`out/` bajo nombres adivinables— está en `.vercelignore`. Vercel no
ejecuta Python: si subiera, serviría esos `.pdf` tal cual y el producto
entero quedaría gratis en `/entregables/out/`.

Al regenerar los PDFs hay que copiarlos otra vez:

```bash
cp entregables/out/*.pdf descargas/e41b9fb5ec65061a/
```

## Decisiones de seguridad

**El precio vive en el servidor.** `api/_lib/offers.js` es la única
fuente. El navegador manda un id de oferta, nunca un importe. Probado:
mandar `amount: 1` en el cuerpo no cambia nada.

**El webhook no se cree nada.** La documentación de XPag no describe
firma HMAC. Así que la URL lleva un secreto (`WEBHOOK_KEY`, comparado en
tiempo constante) **y** el cuerpo se trata sólo como aviso de que algo
cambió: el handler vuelve a preguntar por `/consult-transaction` y
libera únicamente con `confirmed`. Una prueba forja un webhook que dice
`confirmed` sin que nadie haya pagado y comprueba que no se entrega.

**El estado sólo se consulta con el token firmado**, para que nadie pueda
sondear ventas ajenas probando identificadores.

**Los errores salen por clave de traducción**, nunca con el texto del
proveedor ni con el detalle interno.

**MED (disputa)** llega en el mismo `transaction_id` y revoca el acceso.

## Límite por IP: dos cosas que no protege

1. En serverless cada instancia lleva su contador, así que frena ráfagas
   de un mismo cliente, no un ataque distribuido. Para eso hace falta el
   firewall de la plataforma.
2. Las operadoras móviles de México comparten IP entre muchos clientes
   (NAT). Por eso el valor por defecto es holgado (30/min, ajustable con
   `RATE_CREATE`): un límite apretado no frena al atacante y sí bloquea
   compradores reales en un pico.

Cada endpoint lleva su propio balde. Antes compartían uno y el sondeo de
estado —que corre cada 6 s mientras la persona espera— se comía el cupo
de crear la cobranza.

## Pruebas

```bash
node test/mock-xpag.mjs &      # mock del API de XPag en :8787
node test/lib.test.mjs         # 74 · validación, firma del acceso, diagnóstico
node test/api.test.mjs         # 60 · los seis handlers
node test/dev-server.mjs &     # sirve el sitio y enruta /api/* en :8080
node test/checkout.e2e.mjs     # 58 · la pantalla, la entrega y la politica
```

El mock reproduce las respuestas de la documentación campo por campo,
porque `api.xpag.global` no es alcanzable desde el entorno de build.

**Lo que las pruebas NO demuestran:** que XPag real devuelva los campos
con los nombres que el código lee. Eso se confirma corriendo, desde una
máquina con salida a internet, una petición al sandbox y comparando la
respuesta con `test/mock-xpag.mjs`.

## La política estricta sólo cubre donde hay dinero

`/pago`, `/checkout.html`, `/gracias-*` y `/api/*` llevan
`Content-Security-Policy`. El resto del sitio —las páginas de venta y el
sitio viejo de Cosmo Pack— **no**, y es a propósito: llevan CSS y
JavaScript dentro del HTML, así que la política estricta las dejaría sin
formato. Todas reciben igual las cabeceras que no rompen nada (HSTS,
nosniff, Referrer-Policy, X-Frame-Options, Permissions-Policy).

Ampliarla al resto exige reescribir esas páginas: la de Azúcar tiene 23
atributos `style=` y un `<script>` en línea; el sitio de Cosmo Pack,
otros 4 y uno. Es trabajo real, no una línea de configuración.

Dos pruebas vigilan las dos mitades: que las pantallas de pago sirvan la
política, y que las páginas de venta **no** la reciban.

## Nada de CSS dentro del HTML (en las pantallas de pago)

La política de esas pantallas declara `style-src 'self'`, sin `'unsafe-inline'`.
Un bloque `<style>` o un atributo `style=` en el HTML queda **bloqueado
por el navegador** y la página sale sin formato. Pasó con la página de
entrega: en local se veía perfecta y publicada eran links sueltos.

El servidor de pruebas ahora lee `vercel.json` y aplica las mismas
cabeceras, así que la diferencia entre local y producción desapareció.
Dos pruebas lo cubren: que no haya `<style>` ni `style=` en las páginas,
y que un card de descarga calcule `display: flex` de verdad.

Debilitar la política para permitir CSS en línea sería la otra salida, y
es peor: `'unsafe-inline'` abre la puerta a inyección de estilos.

## El Purchase de Meta se manda dos veces, a propósito

Desde el **navegador**, cuando la pantalla detecta la confirmación. Y
desde el **servidor** (`api/_lib/meta.js`), en el webhook, después de
verificar el pago contra XPag.

Los dos llevan el mismo `event_id` (el `e2e`, único por pago), así que
Meta deduplica y la venta cuenta una sola vez.

No es redundancia: el evento del navegador sólo llega si la persona tiene
la pantalla abierta cuando el pago confirma. En SPEI ocurre, son minutos.
**En OXXO no**: se paga en la tienda horas después y casi nadie vuelve a
abrir la página. Sin el envío del servidor, esas ventas serían invisibles
para Meta y el algoritmo optimizaría en contra, creyendo que el anuncio
no convierte.

El evento del servidor no tiene las cookies `_fbp`/`_fbc`, porque quien
llama es el gateway y no el navegador del comprador. Va con lo que se
puede recuperar sin almacenar nada: el identificador de la venta y el
nombre del pagador que devuelve XPag, los dos en SHA-256. La coincidencia
es más pobre que la del evento del navegador, pero una venta contada con
señal modesta vale más que una venta no contada.

Si Meta falla o está caído, no se rompe nada: el producto se entrega por
el enlace firmado, que no depende de Meta. Hay una prueba que apunta el
envío a un puerto donde no escucha nadie y comprueba que el comprador
entra igual.

## Lo que afecta la conversión

- **El nombre del beneficiario va arriba, antes de la CLABE.** Si no
  coincide con `BRAND_NAME`, la pantalla explica que el banco mostrará
  otro nombre. Es el principal motivo de abandono en México.
- **La cuenta regresiva de validez es una política nuestra**
  (`REF_HOURS`), no un dato de XPag, que no expone vencimiento para MXN.
  Al llegar a cero la pantalla ofrece generar otra referencia pero
  **sigue consultando**: declarar muerta una referencia que quizá siga
  viva cuesta ventas.
- **El formulario pide sólo el nombre.** El WhatsApp se pide después, ya
  con la referencia en pantalla. Quien paga en OXXO y pierde el enlace
  pierde el acceso, así que ese campo es la red de seguridad.
- **Copiar tiene plan B**: si el navegador bloquea el portapapeles, se
  selecciona el texto y se dice qué hacer.
- **La CLABE nunca se parte** en dos renglones: un número cortado se
  teclea mal y el pago no se concilia.
