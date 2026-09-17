# Checkout XPag — SPEI y OXXO (MXN)

Checkout propio para las landings, sobre la API de XPag
(`https://api.xpag.global`). Sin intermediario y sin link externo.

## Lo que hay aquí

```
api/_xpag.js      credenciales, catálogo de precios, mapa de errores
api/checkout.js   POST — crea la cobranza, devuelve CLABE o referencia OXXO
api/status.js     GET  — ¿ya pagó? (pregunta a XPag, no a una base propia)
api/webhook.js    POST — receptor del webhook, con verificación obligatoria
public/checkout.html  la página que ve el comprador
vercel.json       runtime y la ruta /checkout
```

## Métodos disponibles

XPag en MXN da **SPEI** (transferencia a una CLABE) y **OXXO** (voucher en
efectivo, de 10 a 10.000 MXN). **No hay tarjeta ni meses sin intereses**: la
copia de las landings que los prometía fue corregida.

## Desplegar

1. Subir esta carpeta a Vercel (o mover `api/` y `public/` a la raíz del
   proyecto que ya tengas ahí).
2. Variables de entorno en el panel de Vercel:

   | Variable | Para qué |
   |---|---|
   | `XPAG_CLIENT_ID` | Dashboard XPag → API |
   | `XPAG_CLIENT_SECRET` | Dashboard XPag → API. **Nunca en el HTML.** |
   | `XPAG_WEBHOOK_URL` | `https://TU-DOMINIO/api/webhook` |
   | `SITE_ORIGIN` | opcional: `https://tudominio.com`, cierra el CORS |
   | `XPAG_SANDBOX` | `1` para probar sin mover dinero; quitar en producción |

3. Los botones de las landings ya apuntan a `/checkout?p=azucar`,
   `?p=raices` y `?p=pulmones`.

## Probar sin mover dinero

Poner `XPAG_SANDBOX=1`. Usa las credenciales públicas de prueba de XPag,
la página muestra una banda naranja de aviso y ninguna petición toca
adquirente, saldo ni transacción real.

Para confirmar un pago de prueba y disparar el webhook, XPag expone
`POST /sandbox/simulate`:

```bash
curl -X POST https://api.xpag.global/sandbox/simulate \
  -H 'X-Client-Id: xpagsandbox_00000000' \
  -H 'X-Client-Secret: 202620262026202620262026' \
  -H 'Content-Type: application/json' \
  -d '{"transaction_id":"SBX-...","outcome":"paid"}'
```

`outcome` acepta `paid`, `failed` y `expired`: conviene probar los tres.

## Decisiones que conviene conocer

**El precio vive en el servidor.** `PRODUCTS` en `_xpag.js` es la única
fuente. El navegador manda un id de producto, nunca un importe. Si el
importe viniera del cliente, cualquiera pediría la cobranza por $1.

**El webhook no se cree nada.** La documentación de XPag no describe firma
HMAC. Sin firma, quien descubra la URL puede postear
`{"status":"confirmed"}` y llevarse el producto. Así que `webhook.js` trata
el POST sólo como aviso de "algo cambió" y vuelve a preguntar por
`GET /consult-transaction`; libera únicamente si XPag responde
`confirmed`. Si XPag agrega firma más adelante, se verifica además de esto,
no en lugar de esto.

**El estado sale de XPag.** `status.js` consulta la API en vez de una tabla
propia, así que la pantalla del comprador no puede quedar desincronizada
del pago real.

**Un `external_id` por venta.** Lo genera el servidor. XPag no lo genera:
sólo lo devuelve en el webhook. Uno por venta significa que dos compras
nunca colisionan.

**OXXO con `generateCheckout:false`.** La documentación especifica campo por
campo la respuesta cruda (`payee_data.reference` y `payee_data.barcode`),
mientras que para la página hospedada no dice cómo se llama el campo con la
URL. Así que la pintamos nosotros y no dependemos de un campo que no
podemos verificar.

**MED (disputa PIX) revoca.** Llega con `status: "med"` en el mismo
`transaction_id` de la cobranza y el líquido se retira del saldo, así que el
acceso se cancela.

## Lo que falta para entregar por correo

El flujo cobra y confirma tal cual está: la página detecta el pago y muestra
el acceso. Para **mandar el PDF por correo** hacen falta dos piezas que
necesitan almacenamiento, y están marcadas con `TODO` en `webhook.js`:

1. **Guardar `{ external_id → email }`** al crear la cobranza. El correo se
   captura en el checkout y no viaja en el webhook.
2. **Deduplicar por `e2e`.** El webhook puede llegar más de una vez para el
   mismo pago; sin esa guarda el comprador recibe el correo tres veces.

Con Vercel KV son unas 20 líneas, más el proveedor de correo (Resend,
Postmark, SES).

## Errores

Se tratan por `error_code`, que XPag garantiza estable entre idiomas y
versiones. El texto del proveedor nunca se muestra crudo al comprador: hay
un mapa a español en `_xpag.js`. `provider_unavailable` y `rate_limited` son
los únicos reintentables, y se reintentan con el **mismo** `external_id`
para no duplicar la venta.

## Pruebas

`test/` trae un mock del API de XPag con las respuestas exactas de la
documentación, porque `api.xpag.global` no siempre es alcanzable desde un
entorno de build.

```bash
node test/mock-xpag.mjs &      # mock del API en :8787
node test/handlers.test.mjs    # 23 pruebas de los tres handlers
node test/dev-server.mjs &     # sirve public/ y enruta /api/* en :8080
node test/checkout.e2e.mjs     # recorre la página en Chromium
```

La prueba que más importa es la 7: un webhook falsificado que dice
`{"status":"confirmed"}` sin que nadie haya pagado **no** libera el
producto, porque el handler vuelve a preguntarle a XPag y recibe
`pending`.

### Antes de cobrar de verdad: verificar el contrato

Las pruebas de arriba corren contra el mock, así que confirman la lógica
pero **no** que XPag devuelva los campos con los nombres que el código
lee. Eso lo confirma:

```bash
node test/verificar-contrato.mjs
```

Pega el sandbox real y comprueba, uno por uno, los campos de los que
dependen los handlers: `clabe`, `bank_name`, `beneficiary`,
`payee_data.reference`, `payee_data.barcode`, `transaction_id`, `status`,
`error_code`, y si `/consult-transaction?external_id=` responde con
`payments[]` o con un objeto suelto. También distingue un bloqueo de
proxy de un error de XPag, para no reportar verde en falso.

Con credenciales propias en vez del sandbox:

```bash
XPAG_CLIENT_ID=... XPAG_CLIENT_SECRET=... node test/verificar-contrato.mjs
```

Ahí las cobranzas que crea son **reales** (quedan pendientes, nadie las
paga). Con el sandbox no se mueve nada.
