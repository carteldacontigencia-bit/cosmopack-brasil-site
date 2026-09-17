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
