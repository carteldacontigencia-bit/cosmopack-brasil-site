/* Cliente de la API de XPag + traducción de error_code. */
import { cfg, requireConfig } from './env.js';

export async function xpag(path, { method = 'GET', body, timeoutMs = 12_000 } = {}) {
  requireConfig('clientId', 'clientSecret');
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeoutMs);
  try {
    const r = await fetch(cfg.xpagBase + path, {
      method,
      headers: {
        'X-Client-Id': cfg.clientId,
        'X-Client-Secret': cfg.clientSecret,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: ctl.signal,
    });
    const texto = await r.text();
    let data;
    try { data = texto ? JSON.parse(texto) : {}; } catch { data = { raw: texto.slice(0, 200) }; }
    return { http: r.status, data };
  } finally { clearTimeout(t); }
}

/* error_code es estable entre idiomas y versiones, así que la lógica va
   por código. Se devuelve una CLAVE de traducción, no un texto: el
   idioma lo resuelve el front con su archivo de textos. */
const CLAVE = {
  amount_below_min: 'err_min',
  amount_above_limit: 'err_max',
  amount_unavailable: 'err_amount_rail',
  invalid_amount: 'err_amount',
  duplicate: 'err_duplicate',
  rate_limited: 'err_busy',
  provider_unavailable: 'err_busy',
  maintenance: 'err_maintenance',
  kyc_required: 'err_account',
  permission_denied: 'err_account',
  key_inactive: 'err_account',
  invalid_credentials: 'err_account',
  missing_credentials: 'err_account',
  currency_not_enabled: 'err_account',
  currency_not_supported: 'err_account',
  cashin_failed: 'err_generic',
};

export const REINTENTABLES = new Set(['provider_unavailable', 'rate_limited']);
export const claveDeError = (code) => CLAVE[code] || 'err_generic';

/* /consult-transaction devuelve un OBJETO por transaction_id y una LISTA
   (payments[]) por external_id o clabe. Las dos formas caen aquí. */
export function normalizar(data) {
  if (!data || data.ok === false) return { status: 'unknown' };
  if (Array.isArray(data.payments)) {
    const pagado = data.payments.find((p) => p.status === 'confirmed');
    const p = pagado || data.payments[data.payments.length - 1];
    if (!p) return { status: 'pending' };
    return {
      status: pagado ? 'confirmed' : (p.status || 'pending'),
      amount: p.amount, currency: p.currency, e2e: p.e2e,
      transaction_id: p.transaction_id, external_id: p.external_id,
      payer_name: p.payer_name || null,
    };
  }
  return {
    status: data.status || 'unknown',
    amount: data.amount, currency: data.currency, e2e: data.e2e,
    transaction_id: data.transaction_id || data.request_number,
    external_id: data.external_id,
    payer_name: data.payer_name || null,
  };
}

/* Consulta preferente por transaction_id (registro único en cobranza
   dinámica); external_id como respaldo. 404 = todavía sin depósito. */
export async function estadoDe({ transactionId, externalId }) {
  const q = transactionId
    ? `transaction_id=${encodeURIComponent(transactionId)}`
    : `external_id=${encodeURIComponent(externalId)}`;
  const r = await xpag(`/consult-transaction?${q}`);
  if (r.http === 404) return { status: 'pending' };
  if (r.http >= 400) return { status: 'unknown' };
  return normalizar(r.data);
}
