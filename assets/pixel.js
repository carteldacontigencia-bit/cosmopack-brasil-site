/* Meta Pixel.
   ──────────────────────────────────────────────────────────────
   Dos reglas del briefing, implementadas aqui:

   1. Los eventos de checkout sólo se disparan para quien VIENE DE
      ANUNCIO. Se detecta por fbclid, gclid, ttclid o utm_source/medium
      en la URL, y se recuerda en sessionStorage para que sobreviva la
      navegación dentro del sitio.

   2. El Purchase se dispara SÓLO tras la confirmación real, con un
      eventID único por cobranza (el e2e que devuelve XPag, que es único
      por pago), y con una marca en localStorage para no contarlo dos
      veces si la persona recarga o vuelve horas después.

   Sin PIXEL_ID no se carga nada: ni el script de Meta.               */

const CLAVE_ANUNCIO = 'vm_de_anuncio';
const PREFIJO_ENVIADO = 'vm_px_';

let listo = false;

function vieneDeAnuncio() {
  try {
    if (sessionStorage.getItem(CLAVE_ANUNCIO) === '1') return true;
    if (sessionStorage.getItem(CLAVE_ANUNCIO) === '0') return false;
  } catch { /* sin storage: se decide sólo por la URL */ }

  const q = new URLSearchParams(location.search);
  const marcas = ['fbclid', 'gclid', 'ttclid', 'msclkid', 'utm_source', 'utm_medium', 'utm_campaign'];
  const deAnuncio = marcas.some((m) => q.get(m));
  try { sessionStorage.setItem(CLAVE_ANUNCIO, deAnuncio ? '1' : '0'); } catch { /* ignora */ }
  return deAnuncio;
}

/* Carga el script de Meta una sola vez y sólo si hay ID y tráfico de
   anuncio. El dominio está permitido en la CSP de vercel.json. */
function cargar(pixelId) {
  if (listo || !pixelId) return listo;
  if (!window.fbq) {
    const n = (window.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    });
    n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://connect.facebook.net/en_US/fbevents.js';
    document.head.appendChild(s);
  }
  window.fbq('init', pixelId);
  listo = true;
  return true;
}

function yaEnviado(clave) {
  try { return localStorage.getItem(PREFIJO_ENVIADO + clave) === '1'; } catch { return false; }
}
function marcarEnviado(clave) {
  try { localStorage.setItem(PREFIJO_ENVIADO + clave, '1'); } catch { /* ignora */ }
}

export function crearPixel(pixelId) {
  const activo = Boolean(pixelId) && vieneDeAnuncio();
  if (activo) cargar(pixelId);

  return {
    activo,

    /* Empieza el checkout: se abrió la pantalla de pago. */
    iniciarCheckout({ value, currency, externalId }) {
      if (!activo) return false;
      const clave = `ic_${externalId}`;
      if (yaEnviado(clave)) return false;
      window.fbq('track', 'InitiateCheckout',
        { value, currency, content_type: 'product' },
        { eventID: `ic_${externalId}` });
      marcarEnviado(clave);
      return true;
    },

    /* Compra: SÓLO tras confirmación verificada contra XPag.
       eventID = e2e, único por pago, así Meta deduplica si el mismo
       evento llega también por la Conversions API del servidor. */
    compra({ value, currency, eventId }) {
      if (!activo || !eventId) return false;
      const clave = `pu_${eventId}`;
      if (yaEnviado(clave)) return false;
      window.fbq('track', 'Purchase',
        { value, currency },
        { eventID: String(eventId) });
      marcarEnviado(clave);
      return true;
    },
  };
}
