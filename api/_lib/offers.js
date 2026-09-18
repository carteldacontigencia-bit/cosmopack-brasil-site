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
