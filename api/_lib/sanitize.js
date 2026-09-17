/* Validación de lo que llega del navegador. */

/* Nombre: sólo letras (con acentos), espacios, apóstrofo y guion.
   Se normaliza a NFC y se colapsan los espacios. */
export function nombreLimpio(v) {
  const s = String(v ?? '').normalize('NFC').replace(/\s+/g, ' ').trim();
  if (s.length < 3 || s.length > 60) return null;
  if (!/^[\p{L}][\p{L} '’-]*[\p{L}]$/u.test(s)) return null;
  return s;
}

/* Importe: número de verdad, dos decimales como máximo. El precio real
   NO sale de aquí: esto sólo comprueba la forma antes de cotejar con la
   tabla del servidor. */
export function importeLimpio(v, { min, max }) {
  const n = typeof v === 'number' ? v : Number(String(v ?? '').replace(',', '.'));
  if (!Number.isFinite(n)) return null;
  const centavos = Math.round(n * 100);
  if (Math.abs(n * 100 - centavos) > 1e-6) return null;
  const val = centavos / 100;
  if (val < min || val > max) return null;
  return val;
}

/* Campo trampa: los robots rellenan todo lo que ven. Si viene con algo,
   se descarta la petición sin explicar por qué. */
export const cayoEnLaTrampa = (body) => Boolean(String(body?.website ?? '').trim());

export const metodoLimpio = (v) => (v === 'oxxo' ? 'oxxo' : v === 'spei' ? 'spei' : null);

export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

/* WhatsApp de México: 10 dígitos, o con 52 / +52 delante. */
export function whatsappLimpio(v) {
  const d = String(v ?? '').replace(/\D/g, '');
  if (d.length === 10) return `52${d}`;
  if (d.length === 12 && d.startsWith('52')) return d;
  if (d.length === 13 && d.startsWith('521')) return `52${d.slice(3)}`;
  return null;
}
