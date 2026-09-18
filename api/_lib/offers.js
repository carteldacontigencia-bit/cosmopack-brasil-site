/* Tabla de precios. VIVE AQUI, en el servidor. El navegador solo manda
   el id de la oferta: si el importe llegara del cliente, cualquiera
   pediria la cobranza por un peso. */

/* OXXO acepta de 10 a 10.000 MXN (limite de XPag). */
export const LIMITES = { min: 10, max: 10000 };

export const OFERTAS = {
  principal: {
    id: 'principal',
    amount: 140,
    currency: 'MXN',
    /* Clave de traduccion, no texto: el idioma lo resuelve el front. */
    nombreClave: 'oferta_principal_nombre',
    /* Lo que ve XPag en el extracto y en el panel. */
    descripcion: 'Plan digital',
  },
};

/* ── Order bumps ──────────────────────────────────────────────────
   Extras que se marcan ANTES de generar la referencia. Con SPEI y OXXO
   ese es el unico momento en que subir el importe no cuesta nada: la
   persona todavia no ha tecleado nada en el banco. Un upsell despues
   del pago la obligaria a hacer una segunda transferencia, o a volver
   al OXXO -- y eso no lo hace nadie.

   El importe vive aqui, igual que el de la oferta principal y por el
   mismo motivo. El navegador manda ids, nunca cantidades.

   'ruta' es la carpeta de descarga, con su segmento aleatorio: saber la
   ruta ES el permiso. Por eso no aparece nunca en el HTML de la pagina
   de entrega -- se la manda /api/access solo a quien pago. */
export const BUMPS = {
  corazon: {
    id: 'corazon',
    amount: 89,
    nombreClave: 'bump_corazon_nombre',
    textoClave: 'bump_corazon_texto',
    descripcion: 'Recetario del Corazon',
    archivo: 'Recetario-del-Corazon.pdf',
    ruta: 'descargas/c7f2a91e40b8d356',
    paginas: 41,
  },
  noches: {
    id: 'noches',
    amount: 59,
    nombreClave: 'bump_noches_nombre',
    textoClave: 'bump_noches_texto',
    descripcion: 'Las Noches de la Abuela',
    archivo: 'Las-Noches-de-la-Abuela.pdf',
    ruta: 'descargas/5b04e8c2d1f7a690',
    paginas: 29,
  },
  manos: {
    id: 'manos',
    amount: 59,
    nombreClave: 'bump_manos_nombre',
    textoClave: 'bump_manos_texto',
    descripcion: 'Manos y Rodillas',
    archivo: 'Manos-y-Rodillas.pdf',
    ruta: 'descargas/9a3e17d6b085c4f2',
    paginas: 29,
  },
};

/* Cuales se ENSENAN en el checkout. Tres marean y tumban la conversion
   de la oferta principal, que es la que paga el anuncio: se dejan dos y
   se rotan. El tercero sirve para el rescate de quien no pago. */
export const BUMPS_VISIBLES = ['corazon', 'noches'];

/* Acepta solo ids conocidos, sin repetir y en orden fijo: asi el
   external_id que se arma con ellos es siempre el mismo para la misma
   compra. */
export function bumpsLimpios(lista) {
  if (!Array.isArray(lista)) return [];
  const vistos = new Set();
  for (const x of lista) {
    const id = String(x || '').toLowerCase();
    if (BUMPS[id]) vistos.add(id);
  }
  return Object.keys(BUMPS).filter((id) => vistos.has(id));
}

export const totalCon = (oferta, ids) =>
  oferta.amount + ids.reduce((s, id) => s + BUMPS[id].amount, 0);

export const bumpPublico = (b) => ({
  id: b.id, amount: b.amount,
  nombreClave: b.nombreClave, textoClave: b.textoClave,
});

export const OFERTA_POR_DEFECTO = 'principal';

export function getOferta(id) {
  const o = OFERTAS[String(id || OFERTA_POR_DEFECTO)];
  if (!o) return null;
  if (o.amount < LIMITES.min || o.amount > LIMITES.max) return null;
  return o;
}

/* Lo que se puede exponer al navegador: nunca la descripcion interna. */
export const publica = (o) => ({
  id: o.id, amount: o.amount, currency: o.currency, nombreClave: o.nombreClave,
});
