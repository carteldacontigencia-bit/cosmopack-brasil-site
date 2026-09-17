/* ───────────────────────────────────────────────────────────────
   XPag — capa compartida.
   Todo lo que toca las credenciales vive del lado del servidor.
   El Client Secret NUNCA se envía al navegador.
   ─────────────────────────────────────────────────────────────── */

const PROD_BASE = 'https://api.xpag.global';

/* Credenciales públicas del sandbox, documentadas por XPag. No mueven
   dinero: sirven para probar el flujo completo antes de ir a producción. */
const SANDBOX_ID = 'xpagsandbox_00000000';
const SANDBOX_SECRET = '202620262026202620262026';

export const isSandbox = process.env.XPAG_SANDBOX === '1';

export const BASE = process.env.XPAG_BASE_URL || PROD_BASE;

function credentials() {
  if (isSandbox) return { id: SANDBOX_ID, secret: SANDBOX_SECRET };
  const id = process.env.XPAG_CLIENT_ID;
  const secret = process.env.XPAG_CLIENT_SECRET;
  if (!id || !secret) {
    throw Object.assign(new Error('XPAG_CLIENT_ID / XPAG_CLIENT_SECRET no configurados'), {
      code: 'config_missing',
    });
  }
  return { id, secret };
}

/* ── Catálogo ───────────────────────────────────────────────────
   El precio vive AQUÍ, no en el navegador. Si el importe viniera del
   cliente, cualquiera podría pedir la cobranza por $1 y recibir el
   producto. El front sólo manda el id del producto.
   OXXO acepta de 10 a 10.000 MXN (límite de XPag).                */
export const PRODUCTS = {
  azucar: {
    name: 'Azúcar en Equilibrio — 55 Remedios Naturales',
    amount: 47.9,
    currency: 'MXN',
    description: 'Azúcar en Equilibrio (ebook + 3 bonos)',
  },
  raices: {
    name: 'Raíces Olvidadas — 55 Remedios Naturales',
    amount: 47.9,
    currency: 'MXN',
    description: 'Raíces Olvidadas (ebook + bonos)',
  },
  pulmones: {
    name: 'Pulmones Libres — método para dejar de fumar',
    amount: 97.0,
    currency: 'MXN',
    description: 'Pulmones Libres (guía + 3 bonos)',
  },
};

export function getProduct(id) {
  const p = PRODUCTS[String(id || '')];
  if (!p) throw Object.assign(new Error('Producto no encontrado'), { code: 'product_unknown' });
  return p;
}

/* ── Llamada a la API ──────────────────────────────────────────── */
export async function xpag(path, { method = 'GET', body, timeoutMs = 12000 } = {}) {
  const { id, secret } = credentials();
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeoutMs);
  try {
    const res = await fetch(BASE + path, {
      method,
      headers: {
        'X-Client-Id': id,
        'X-Client-Secret': secret,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: ctl.signal,
    });
    const text = await res.text();
    let data;
    try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
    return { httpStatus: res.status, data };
  } finally {
    clearTimeout(t);
  }
}

/* ── Errores ───────────────────────────────────────────────────
   XPag garantiza que error_code es estable entre idiomas y versiones,
   así que la lógica va por código y el texto de error del proveedor
   nunca se muestra crudo al comprador.                            */
const MENSAJES = {
  amount_below_min: 'El importe es menor al mínimo que acepta este método de pago.',
  amount_above_limit: 'El importe supera el máximo de este método de pago.',
  amount_unavailable: 'Ese importe no está disponible en este momento. Intenta de nuevo en unos minutos.',
  invalid_amount: 'Importe inválido.',
  currency_not_enabled: 'La moneda no está habilitada en esta cuenta.',
  currency_not_supported: 'Moneda no soportada.',
  kyc_required: 'La cuenta de cobro aún no está verificada.',
  permission_denied: 'La llave de API no tiene permiso para cobrar.',
  key_inactive: 'La llave de API está inactiva.',
  invalid_credentials: 'Credenciales de cobro inválidas.',
  missing_credentials: 'Credenciales de cobro ausentes.',
  rate_limited: 'Demasiados intentos. Espera un momento y vuelve a intentar.',
  provider_unavailable: 'El servicio de pagos no responde. Intenta de nuevo en unos minutos.',
  maintenance: 'El servicio de pagos está en mantenimiento.',
  duplicate: 'Esta operación ya fue procesada.',
  cashin_failed: 'No pudimos generar el pago. Intenta de nuevo.',
};

/* Estos sí conviene reintentar con el MISMO external_id, para no duplicar. */
export const REINTENTABLES = new Set(['provider_unavailable', 'rate_limited']);

export function mensajeDeError(code) {
  return MENSAJES[code] || 'No pudimos generar el pago. Intenta de nuevo en unos minutos.';
}

/* ── Identificador de venta ────────────────────────────────────
   external_id es NUESTRO: XPag no lo genera, sólo lo devuelve en el
   webhook. Uno por venta, así cada compra tiene su propia CLABE y una
   no cae encima de otra.                                          */
export function nuevoExternalId(productId) {
  const rand = crypto.randomUUID().replace(/-/g, '').slice(0, 10);
  return `${productId}-${Date.now().toString(36)}-${rand}`.toUpperCase();
}

/* ── CORS ──────────────────────────────────────────────────────
   Cerrado al origen del sitio. SITE_ORIGIN vacío = mismo origen
   (el caso normal cuando el checkout se sirve del mismo dominio).  */
export function aplicarCors(req, res) {
  const permitido = process.env.SITE_ORIGIN;
  if (permitido) {
    const origin = req.headers.origin;
    if (origin && origin === permitido) {
      res.setHeader('Access-Control-Allow-Origin', permitido);
      res.setHeader('Vary', 'Origin');
    }
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(204).end(); return true; }
  return false;
}

export async function leerJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  const trozos = [];
  for await (const c of req) trozos.push(c);
  const texto = Buffer.concat(trozos).toString('utf8');
  if (!texto) return {};
  try { return JSON.parse(texto); } catch { return {}; }
}

/* ── Estado normalizado ────────────────────────────────────────
   /consult-transaction devuelve un OBJETO cuando se consulta por
   transaction_id/request_number, y una LISTA (payments[]) cuando se
   consulta por external_id o clabe. Las dos formas caen aquí.      */
export function normalizarEstado(data) {
  if (!data || data.ok === false) return { status: 'unknown' };

  if (Array.isArray(data.payments)) {
    const pagado = data.payments.find((p) => p.status === 'confirmed');
    if (pagado) {
      return {
        status: 'confirmed',
        amount: pagado.amount,
        currency: pagado.currency,
        e2e: pagado.e2e,
        transaction_id: pagado.transaction_id,
        external_id: pagado.external_id,
      };
    }
    if (!data.payments.length) return { status: 'pending' };
    const ultimo = data.payments[data.payments.length - 1];
    return { status: ultimo.status || 'pending', amount: ultimo.amount, currency: ultimo.currency };
  }

  return {
    status: data.status || 'unknown',
    amount: data.amount,
    currency: data.currency,
    e2e: data.e2e,
    transaction_id: data.transaction_id || data.request_number,
    external_id: data.external_id,
  };
}
