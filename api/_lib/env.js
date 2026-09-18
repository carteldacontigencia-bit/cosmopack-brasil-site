/* Configuracion. Nada de credenciales en el codigo ni en el front.
   Se lee con getters, no en el import: asi refleja el entorno en el
   momento de usarse y es comprobable en pruebas. */
const SANDBOX_ID = 'xpagsandbox_00000000';
const SANDBOX_SECRET = '202620262026202620262026';

const env = (k, def = '') => process.env[k] || def;

export const isSandbox = () => process.env.XPAG_SANDBOX === '1';

export const cfg = {
  get xpagBase() { return env('XPAG_BASE_URL', 'https://api.xpag.global'); },
  get clientId() { return isSandbox() ? SANDBOX_ID : env('XPAG_CLIENT_ID'); },
  get clientSecret() { return isSandbox() ? SANDBOX_SECRET : env('XPAG_CLIENT_SECRET'); },
  /* Secreto propio: firma los enlaces de acceso. Sin el, no se entrega nada. */
  get accessSecret() { return env('ACCESS_SECRET'); },
  /* Secreto en la URL del webhook: /api/webhook?k=... */
  get webhookKey() { return env('WEBHOOK_KEY'); },
  get siteOrigin() { return env('SITE_ORIGIN'); },
  get publicUrl() { return env('PUBLIC_URL', env('SITE_ORIGIN')); },
  get brand() { return env('BRAND_NAME'); },
  get productUrl() { return env('PRODUCT_URL'); },
};

export function requireConfig(...claves) {
  const faltan = claves.filter((k) => !cfg[k]);
  if (faltan.length) {
    const e = new Error('config_missing');
    e.code = 'config_missing';
    e.faltan = faltan;
    throw e;
  }
}

/* ── Diagnóstico de entorno ───────────────────────────────────────────
   Devuelve QUÉ VARIABLES FALTAN, por nombre. Nunca el valor, nunca la
   longitud. Los nombres ya están publicados en .env.example, así que no
   revelan nada; y todo lo que puede faltar falla cerrado (sin
   WEBHOOK_KEY el webhook responde 404 a todo, sin ACCESS_SECRET no se
   firma ningún enlace), de modo que saber que falta no sirve para
   entrar. Existe porque, sin esto, configurar Vercel es adivinar a
   ciegas: la pantalla da un error genérico y no dice cuál casilla
   quedó vacía. */
export function estadoDelEntorno() {
  const hay = (k) => Boolean(process.env[k]);
  const faltan = [];   /* sin esto no se puede vender */
  const avisos = [];   /* se vende, pero se pierde algo */

  if (!isSandbox()) {
    if (!hay('XPAG_CLIENT_ID')) faltan.push('XPAG_CLIENT_ID');
    if (!hay('XPAG_CLIENT_SECRET')) faltan.push('XPAG_CLIENT_SECRET');
  }
  if (!hay('ACCESS_SECRET')) faltan.push('ACCESS_SECRET');
  if (!hay('PRODUCT_URL')) faltan.push('PRODUCT_URL');

  if (!hay('WEBHOOK_KEY')) avisos.push('WEBHOOK_KEY');
  if (!hay('PUBLIC_URL') && !hay('SITE_ORIGIN')) avisos.push('PUBLIC_URL');
  if (!hay('BRAND_NAME')) avisos.push('BRAND_NAME');
  if (!hay('META_PIXEL_ID')) avisos.push('META_PIXEL_ID');
  if (!hay('META_CAPI_TOKEN')) avisos.push('META_CAPI_TOKEN');

  return { listo: faltan.length === 0, faltan, avisos };
}
