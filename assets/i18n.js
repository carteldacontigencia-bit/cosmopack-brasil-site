/* Todos los textos del sitio, en un solo archivo.
   Idioma por defecto: es-MX. Se puede forzar con ?lang=en
   Las claves de error las devuelve el servidor (nunca texto del
   proveedor), asi que el idioma se resuelve aqui. */

export const TEXTOS = {
  es: {
    /* ── Oferta y formulario ── */
    oferta_principal_nombre: 'Plan completo',
    oferta_incluye: 'Acceso inmediato · para siempre',
    total: 'Total',
    titulo_form: '¿A nombre de quién va el pago?',
    ayuda_form: 'Sólo tu nombre. Nada más.',
    label_nombre: 'Nombre completo',
    ph_nombre: 'Tu nombre',
    como_pagar: '¿Cómo quieres pagar?',
    spei_titulo: 'Transferencia SPEI',
    spei_nota: 'Desde la app de tu banco. Se confirma en minutos.',
    oxxo_titulo: 'Efectivo en OXXO',
    oxxo_nota: 'Te damos una referencia y pagas en la tienda.',
    btn_continuar: 'Continuar',
    btn_generando: 'Generando tu pago…',
    btn_reintentar: 'Intentar de nuevo',
    legal_form: 'Pago único. Sin suscripción y sin tarjeta.',

    /* ── SPEI ── */
    spei_h: 'Transfiere desde tu banco',
    spei_p: 'Abre tu app, elige transferir a otra cuenta (SPEI) y usa estos datos.',
    k_clabe: 'CLABE',
    k_importe: 'Importe exacto',
    k_banco: 'Banco destino',
    k_beneficiario: 'Beneficiario',
    k_referencia: 'Referencia',
    k_concepto: 'Concepto',
    copiar: 'Copiar',
    copiar_clabe: 'Copiar CLABE',
    copiado: '¡Copiado!',
    copia_manual: 'Selecciona el número y cópialo a mano.',
    aviso_exacto: 'Transfiere el importe exacto. Si mandas otra cantidad, el pago no se relaciona con tu compra.',

    /* ── El nombre del extracto: principal motivo de abandono ── */
    benef_titulo: 'Antes de ir a tu banco, lee esto',
    benef_distinto: 'Tu banco va a mostrar el nombre {beneficiario}, no {marca}. Es correcto: {beneficiario} es la empresa que procesa el cobro. Continúa con la transferencia.',
    benef_igual: 'Tu banco mostrará el nombre {beneficiario}. Es la cuenta correcta.',

    /* ── Selector de banco ── */
    tu_banco: '¿Con qué banco vas a transferir?',
    banco_generico: 'Otro banco',
    pasos_titulo: 'Paso a paso en {banco}',
    paso_monto: 'Importe: {importe}',
    paso_concepto: 'Concepto: {concepto}',

    /* ── OXXO ── */
    oxxo_h: 'Paga en cualquier OXXO',
    oxxo_p: 'Muestra esta referencia en la caja y paga en efectivo.',
    k_ref_oxxo: 'Referencia OXXO',
    oxxo_comision: 'La tienda puede cobrarte una comisión pequeña por el servicio. Es de OXXO, no nuestra.',
    oxxo_demora: 'El pago en efectivo tarda en confirmarse: normalmente unas horas, a veces hasta el día siguiente. Guarda tu enlace de acceso y vuelve cuando quieras.',
    oxxo_exacto: 'Paga el importe exacto que aparece arriba.',

    /* ── Espera y validez ── */
    esperando: 'Esperando tu pago. Esta pantalla se actualiza sola.',
    esperando_oxxo: 'Esperando el pago en tienda. Puedes cerrar esta página.',
    validez: 'Esta referencia sirve durante {horas} horas.',
    validez_restante: 'Tiempo restante: {reloj}',
    vencida: 'Esta referencia venció. Genera una nueva.',
    btn_nueva: 'Generar una nueva',
    pedido: 'Tu número de pedido es {id}.',

    /* ── Guarda tu acceso ── */
    guarda_titulo: 'Guarda tu acceso',
    guarda_p: 'Este enlace es tuyo y te lleva al material en cuanto el pago se confirme. Guárdalo antes de salir.',
    guarda_copiar: 'Copiar mi enlace de acceso',
    contacto_titulo: '¿Te lo mandamos también por WhatsApp?',
    contacto_p: 'Opcional. Sirve para que no pierdas el acceso si cierras el navegador.',
    ph_whatsapp: '55 1234 5678',
    contacto_btn: 'Guardar',
    contacto_ok: 'Listo, lo tenemos.',

    /* ── Confirmado ── */
    conf_h: '¡Pago confirmado!',
    conf_p: 'Tu material ya está disponible.',
    conf_btn: 'Abrir mi material',
    conf_pedido: 'Pedido {id}',

    /* ── Errores (claves que devuelve el servidor) ── */
    err_name: 'Escribe tu nombre completo, sólo letras.',
    err_method: 'Elige cómo quieres pagar.',
    err_offer: 'Esa oferta no está disponible.',
    err_min: 'El importe es menor al mínimo de este método.',
    err_max: 'El importe supera el máximo de este método.',
    err_amount: 'Importe inválido.',
    err_amount_rail: 'Ese importe no está disponible ahora. Intenta en unos minutos.',
    err_duplicate: 'Esta operación ya se procesó.',
    err_busy: 'El servicio de pagos no responde. Intenta de nuevo en un momento.',
    err_maintenance: 'El servicio de pagos está en mantenimiento.',
    err_account: 'El cobro no está disponible en este momento.',
    err_config: 'El cobro aún no está configurado.',
    err_spei: 'No pudimos generar los datos de transferencia. Intenta con OXXO.',
    err_oxxo: 'No pudimos generar el voucher. Intenta con transferencia.',
    err_token: 'Este enlace no es válido.',
    err_not_paid: 'Todavía no vemos tu pago. Si acabas de pagar, espera unos minutos.',
    err_contact: 'Escribe un WhatsApp o un correo válido.',
    err_red: 'Se cayó la conexión. Revisa tu internet e intenta otra vez.',
    err_generic: 'No pudimos generar el pago. Intenta de nuevo.',

    l_bumps: '¿Quieres agregar algo más?',
    bump_corazon_nombre: 'Recetario del Corazón',
    bump_corazon_texto: 'Presión y colesterol. 24 remedios en 41 páginas, con su dosis, su hora y su advertencia.',
    bump_noches_nombre: 'Las Noches de la Abuela',
    bump_noches_texto: 'Para dormir y para los despertares de madrugada. 18 remedios en 29 páginas.',
    bump_manos_nombre: 'Manos y Rodillas',
    bump_manos_texto: 'Para la mano tiesa de la mañana y la rodilla de la escalera. 18 remedios en 29 páginas.',
    bump_agregar: 'Sí, agregar',

    modo_prueba: 'Modo de prueba — ningún cargo real',
    seguro: 'Pago seguro',
  },

  en: {
    oferta_principal_nombre: 'Full plan',
    oferta_incluye: 'Instant access · yours to keep',
    total: 'Total',
    titulo_form: 'Who is the payment from?',
    ayuda_form: 'Just your name. Nothing else.',
    label_nombre: 'Full name',
    ph_nombre: 'Your name',
    como_pagar: 'How would you like to pay?',
    spei_titulo: 'SPEI transfer',
    spei_nota: 'From your banking app. Confirms in minutes.',
    oxxo_titulo: 'Cash at OXXO',
    oxxo_nota: 'We give you a reference and you pay in store.',
    btn_continuar: 'Continue',
    btn_generando: 'Creating your payment…',
    btn_reintentar: 'Try again',
    legal_form: 'One-time payment. No subscription, no card.',

    spei_h: 'Transfer from your bank',
    spei_p: 'Open your app, choose transfer to another account (SPEI) and use these details.',
    k_clabe: 'CLABE',
    k_importe: 'Exact amount',
    k_banco: 'Destination bank',
    k_beneficiario: 'Account holder',
    k_referencia: 'Reference',
    k_concepto: 'Description',
    copiar: 'Copy',
    copiar_clabe: 'Copy CLABE',
    copiado: 'Copied!',
    copia_manual: 'Select the number and copy it manually.',
    aviso_exacto: 'Transfer the exact amount. A different amount will not be matched to your order.',

    benef_titulo: 'Before you go to your bank, read this',
    benef_distinto: 'Your bank will show the name {beneficiario}, not {marca}. That is correct: {beneficiario} is the company processing the payment. Go ahead with the transfer.',
    benef_igual: 'Your bank will show the name {beneficiario}. That is the right account.',

    tu_banco: 'Which bank are you transferring from?',
    banco_generico: 'Another bank',
    pasos_titulo: 'Step by step in {banco}',
    paso_monto: 'Amount: {importe}',
    paso_concepto: 'Description: {concepto}',

    oxxo_h: 'Pay at any OXXO',
    oxxo_p: 'Show this reference at the counter and pay in cash.',
    k_ref_oxxo: 'OXXO reference',
    oxxo_comision: 'The store may charge a small service fee. That fee is OXXO’s, not ours.',
    oxxo_demora: 'Cash payments take a while to confirm: usually a few hours, sometimes until the next day. Save your access link and come back any time.',
    oxxo_exacto: 'Pay the exact amount shown above.',

    esperando: 'Waiting for your payment. This screen updates by itself.',
    esperando_oxxo: 'Waiting for the in-store payment. You can close this page.',
    validez: 'This reference is valid for {horas} hours.',
    validez_restante: 'Time left: {reloj}',
    vencida: 'This reference expired. Generate a new one.',
    btn_nueva: 'Generate a new one',
    pedido: 'Your order number is {id}.',

    guarda_titulo: 'Save your access',
    guarda_p: 'This link is yours and opens the material as soon as the payment confirms. Save it before you leave.',
    guarda_copiar: 'Copy my access link',
    contacto_titulo: 'Want it on WhatsApp too?',
    contacto_p: 'Optional. It means you will not lose access if you close the browser.',
    ph_whatsapp: '55 1234 5678',
    contacto_btn: 'Save',
    contacto_ok: 'Got it.',

    conf_h: 'Payment confirmed!',
    conf_p: 'Your material is ready.',
    conf_btn: 'Open my material',
    conf_pedido: 'Order {id}',

    err_name: 'Enter your full name, letters only.',
    err_method: 'Choose how you want to pay.',
    err_offer: 'That offer is not available.',
    err_min: 'The amount is below this method’s minimum.',
    err_max: 'The amount is above this method’s maximum.',
    err_amount: 'Invalid amount.',
    err_amount_rail: 'That amount is unavailable right now. Try again in a few minutes.',
    err_duplicate: 'This operation was already processed.',
    err_busy: 'The payment service is not responding. Try again in a moment.',
    err_maintenance: 'The payment service is under maintenance.',
    err_account: 'Payments are unavailable right now.',
    err_config: 'Payments are not set up yet.',
    err_spei: 'We could not create the transfer details. Try OXXO instead.',
    err_oxxo: 'We could not create the voucher. Try a transfer instead.',
    err_token: 'This link is not valid.',
    err_not_paid: 'We do not see your payment yet. If you just paid, give it a few minutes.',
    err_contact: 'Enter a valid WhatsApp number or email.',
    err_red: 'The connection dropped. Check your internet and try again.',
    err_generic: 'We could not create the payment. Please try again.',

    l_bumps: 'Want to add anything else?',
    bump_corazon_nombre: 'Heart Recipe Book',
    bump_corazon_texto: 'Blood pressure and cholesterol. 24 remedies over 41 pages, each with its dose, its time and its warning.',
    bump_noches_nombre: "Grandma's Nights",
    bump_noches_texto: 'For falling asleep and for waking at 3am. 18 remedies over 29 pages.',
    bump_manos_nombre: 'Hands and Knees',
    bump_manos_texto: 'For stiff morning hands and the knee on the stairs. 18 remedies over 29 pages.',
    bump_agregar: 'Yes, add it',

    modo_prueba: 'Test mode — no real charge',
    seguro: 'Secure payment',
  },
};

/* Pasos dentro de cada app. El importe y el concepto se rellenan solos.
   Los nombres de los bancos no se traducen. */
export const BANCOS = {
  bbva: {
    nombre: 'BBVA',
    es: ['Entra a BBVA México y toca Transferir.', 'Elige Transferir a otros bancos.', 'Toca Nueva cuenta y pega la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto pon: {concepto}', 'Confirma con tu Clave o huella.'],
    en: ['Open BBVA México and tap Transfer.', 'Choose Transfer to other banks.', 'Tap New account and paste the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description put: {concepto}', 'Confirm with your PIN or fingerprint.'],
  },
  banorte: {
    nombre: 'Banorte',
    es: ['Entra a Banorte Móvil y toca Transferencias.', 'Elige Otros bancos (SPEI).', 'Agrega la cuenta con la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto pon: {concepto}', 'Confirma con tu token.'],
    en: ['Open Banorte Móvil and tap Transfers.', 'Choose Other banks (SPEI).', 'Add the account using the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description put: {concepto}', 'Confirm with your token.'],
  },
  santander: {
    nombre: 'Santander',
    es: ['Entra a SuperMóvil y toca Transferir.', 'Elige A otros bancos.', 'Captura la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto pon: {concepto}', 'Confirma con tu SuperToken.'],
    en: ['Open SuperMóvil and tap Transfer.', 'Choose To other banks.', 'Enter the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description put: {concepto}', 'Confirm with your SuperToken.'],
  },
  citibanamex: {
    nombre: 'Citibanamex',
    es: ['Entra a Citibanamex Móvil y toca Transferencias.', 'Elige Otros bancos nacionales.', 'Captura la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto pon: {concepto}', 'Confirma con tu NetKey.'],
    en: ['Open Citibanamex Móvil and tap Transfers.', 'Choose Other national banks.', 'Enter the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description put: {concepto}', 'Confirm with your NetKey.'],
  },
  nu: {
    nombre: 'Nu',
    es: ['Entra a Nu y toca Transferir.', 'Elige A otra cuenta o banco.', 'Pega la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto pon: {concepto}', 'Confirma con tu PIN.'],
    en: ['Open Nu and tap Transfer.', 'Choose To another account or bank.', 'Paste the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description put: {concepto}', 'Confirm with your PIN.'],
  },
  otro: {
    nombre: null,
    es: ['Entra a la app de tu banco y busca Transferir o SPEI.', 'Elige transferir a otro banco.', 'Captura la CLABE de 18 dígitos.', 'Escribe el importe: {importe}', 'En Concepto o Referencia pon: {concepto}', 'Confirma con tu método de seguridad.'],
    en: ['Open your banking app and find Transfer or SPEI.', 'Choose transfer to another bank.', 'Enter the 18-digit CLABE.', 'Enter the amount: {importe}', 'In Description or Reference put: {concepto}', 'Confirm with your security method.'],
  },
};

export const ORDEN_BANCOS = ['bbva', 'banorte', 'santander', 'citibanamex', 'nu', 'otro'];

export function crearI18n() {
  const pedido = new URLSearchParams(location.search).get('lang');
  const lang = pedido === 'en' ? 'en' : 'es';
  const dic = TEXTOS[lang];
  const t = (clave, vars) => {
    let s = dic[clave] ?? TEXTOS.es[clave] ?? clave;
    if (vars) for (const [k, v] of Object.entries(vars)) s = s.split(`{${k}}`).join(v);
    return s;
  };
  const pasosBanco = (id) => {
    const b = BANCOS[id] || BANCOS.otro;
    return { nombre: b.nombre || t('banco_generico'), pasos: b[lang] || b.es };
  };
  return { lang, t, pasosBanco };
}
