/* Lógica de la pantalla de pago.
   ─────────────────────────────────────────────────────────────────
   Lo que decide la venta y por qué está así:

   · La referencia SOBREVIVE. Se guarda en localStorage por 24 h. Si la
     persona se va al app del banco y el navegador descarta la pestaña,
     al volver encuentra la MISMA CLABE, todavía esperando pago.
   · El estado se consulta cada pocos segundos y también en cuanto la
     pestaña vuelve a estar visible, que es justo el momento en que
     alguien regresa del banco.
   · El nombre del beneficiario se muestra ANTES de salir al banco.
   · Copiar tiene alternativa manual: si el navegador bloquea el
     portapapeles, se selecciona el texto y se dice qué hacer.
   ───────────────────────────────────────────────────────────────── */

import { crearI18n, ORDEN_BANCOS } from './i18n.js';
import { crearPixel } from './pixel.js';

const { t, pasosBanco } = crearI18n();
const $ = (id) => document.getElementById(id);
const ver = (el, si = true) => { el.hidden = !si; };

const CLAVE_ORDEN = 'vm_orden';
const CLAVE_BANCO = 'vm_banco';
const VIDA_MS = 24 * 60 * 60 * 1000;

let cfg = { brand: null, pixel_id: null, ref_hours: 24, sandbox: false, offers: [], bumps: [] };
let oferta = null;
let orden = null;
let pixel = crearPixel(null);
let timer = null;
let relojTimer = null;

const pesos = (n, moneda = 'MXN') =>
  new Intl.NumberFormat('es-MX', { style: 'currency', currency: moneda }).format(Number(n));

/* ── Persistencia ───────────────────────────────────────────────── */
function guardarOrden(o) {
  try { localStorage.setItem(CLAVE_ORDEN, JSON.stringify({ ...o, guardado: Date.now() })); }
  catch { /* modo privado o sin espacio: la pantalla sigue funcionando */ }
}
function leerOrden() {
  try {
    const raw = localStorage.getItem(CLAVE_ORDEN);
    if (!raw) return null;
    const o = JSON.parse(raw);
    if (!o?.access_token || !o?.guardado) return null;
    if (Date.now() - o.guardado > VIDA_MS) { localStorage.removeItem(CLAVE_ORDEN); return null; }
    return o;
  } catch { return null; }
}
function olvidarOrden() {
  try { localStorage.removeItem(CLAVE_ORDEN); } catch { /* ignora */ }
}

/* ── Textos estáticos ───────────────────────────────────────────── */
function pintarTextos() {
  const pares = {
    txtSeguro: 'seguro', txtTotal: 'total', ofIncluye: 'oferta_incluye',
    tForm: 'titulo_form', pForm: 'ayuda_form', lNombre: 'label_nombre',
    lMetodo: 'como_pagar', mSpei: 'spei_titulo', mSpeiNota: 'spei_nota',
    mOxxo: 'oxxo_titulo', mOxxoNota: 'oxxo_nota', legalForm: 'legal_form',
    speiH: 'spei_h', speiP: 'spei_p', kClabe: 'k_clabe', kImporte: 'k_importe',
    kBanco: 'k_banco', kConcepto: 'k_concepto', avisoExacto: 'aviso_exacto',
    tuBanco: 'tu_banco', oxxoH: 'oxxo_h', oxxoP: 'oxxo_p', kRefOxxo: 'k_ref_oxxo',
    kImporteOxxo: 'k_importe', oxxoExacto: 'oxxo_exacto', oxxoComision: 'oxxo_comision',
    oxxoDemora: 'oxxo_demora', guardaTitulo: 'guarda_titulo', guardaP: 'guarda_p',
    contactoTitulo: 'contacto_titulo', contactoP: 'contacto_p', contactoOk: 'contacto_ok',
    benefTitulo: 'benef_titulo', confH: 'conf_h', confP: 'conf_p', confBtn: 'conf_btn',
  };
  for (const [id, clave] of Object.entries(pares)) { const el = $(id); if (el) el.textContent = t(clave); }
  $('enviar').textContent = t('btn_continuar');
  $('btnNueva').textContent = t('btn_nueva');
  $('name').placeholder = t('ph_nombre');
  /* Estos dos viven en el bloque "Guarda tu acceso", que se quito de la
     pantalla. Si vuelve el HTML, vuelven a llenarse solos. */
  if ($('btnContacto')) $('btnContacto').textContent = t('contacto_btn');
  if ($('whatsapp')) $('whatsapp').placeholder = t('ph_whatsapp');
  $('vBarcode').alt = t('k_ref_oxxo');
  for (const b of document.querySelectorAll('[data-copia]')) {
    b.textContent = b.dataset.copia === 'vClabe' ? t('copiar_clabe') : t('copiar');
  }
  $('avisoPruebaTxt').textContent = t('modo_prueba');
}

/* ── Arranque ───────────────────────────────────────────────────── */
async function arrancar() {
  pintarTextos();
  try {
    const r = await fetch('/api/config');
    if (r.ok) { const d = await r.json(); if (d.ok) cfg = { ...cfg, ...d }; }
  } catch { /* sigue con los valores por defecto */ }

  ver($('avisoPrueba'), Boolean(cfg.sandbox));
  $('marca').textContent = cfg.brand || '';
  pixel = crearPixel(cfg.pixel_id);

  oferta = cfg.offers?.[0] || null;
  if (oferta) {
    $('ofNombre').textContent = t(oferta.nombreClave);
    $('ofTotal').textContent = pesos(oferta.amount, oferta.currency);
    pintarBumps();
  }

  const guardada = leerOrden();
  /* Una cobranza guardada del sandbox NO puede sobrevivir al paso a
     produccion, ni al reves. Su CLABE apunta a una cuenta de pruebas:
     quien la tuviera en el aparato veria datos viejos y transferiria
     dinero real a una cuenta que no cobra. Si la bandera no coincide con
     la del servidor, se tira y se empieza de cero. */
  if (guardada && Boolean(guardada.sandbox) !== Boolean(cfg.sandbox)) {
    console.warn('[checkout] cobranza guardada de otro entorno, descartada');
    olvidarOrden();
  } else if (guardada) {
    orden = guardada;
    mostrarPago();
    return;
  }

  ver($('secForm'));
  if (oferta) pixel.iniciarCheckout({ value: oferta.amount, currency: oferta.currency, externalId: 'form' });
}

/* ── Envío del formulario ───────────────────────────────────────── */
$('form').addEventListener('submit', async (ev) => {
  ev.preventDefault();
  for (const id of ['errName', 'errGeneral']) $(id).textContent = '';

  const nombre = $('name').value.trim();
  if (nombre.length < 3) { $('errName').textContent = t('err_name'); $('name').focus(); return; }

  const metodo = document.querySelector('input[name=method]:checked')?.value || 'spei';
  const boton = $('enviar');
  boton.disabled = true;
  boton.textContent = t('btn_generando');

  try {
    const r = await fetch('/api/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        offer: oferta?.id, name: nombre, method: metodo, bumps: bumpsMarcados(),
        website: $('website').value,
      }),
    });
    const d = await r.json();
    if (!r.ok || !d.ok) {
      $('errGeneral').textContent = t(d.error || 'err_generic');
      boton.disabled = false;
      boton.textContent = t(d.retryable ? 'btn_reintentar' : 'btn_continuar');
      return;
    }
    orden = d;
    guardarOrden(orden);
    pixel.iniciarCheckout({ value: d.amount, currency: d.currency, externalId: d.external_id });
    mostrarPago();
  } catch {
    $('errGeneral').textContent = t('err_red');
    boton.disabled = false;
    boton.textContent = t('btn_reintentar');
  }
});

/* ── Pantalla de pago ───────────────────────────────────────────── */
function mostrarPago() {
  ver($('secForm'), false);
  ver($('secOk'), false);
  ver($('secPago'));
  ver($('avisoPrueba'), Boolean(cfg.sandbox));
  /* Los botones de simulacion aparecen cuando ya hay una cobranza que
     simular, no antes. */
  /* Los botones dependen del servidor de AHORA, no de lo que dijera la
     cobranza guardada: /api/simular responde 404 fuera de sandbox, asi
     que ensenarlos seria ofrecer algo que no existe. */
  ver($('simBotones'), Boolean(cfg.sandbox));

  const importe = pesos(orden.amount, orden.currency);
  const concepto = orden.reference || orden.external_id;

  /* El nombre del extracto. Si no coincide con la marca, se explica; es
     la diferencia entre transferir y abandonar. */
  /* Solo en SPEI. En la caja del OXXO nadie enseña un beneficiario: se
     entrega efectivo contra una referencia. El titulo decia "antes de ir
     a tu banco", que ahi no significa nada. */
  if (orden.beneficiary && orden.method !== 'oxxo') {
    const marca = orden.brand || cfg.brand;
    $('benefNombre').textContent = orden.beneficiary;
    $('benefTexto').textContent = marca && marca.trim() && marca.trim().toLowerCase() !== orden.beneficiary.trim().toLowerCase()
      ? t('benef_distinto', { beneficiario: orden.beneficiary, marca })
      : t('benef_igual', { beneficiario: orden.beneficiary });
    ver($('cajaBenef'));
  }

  if (orden.method === 'oxxo') {
    ver($('panelOxxo'));
    $('vRefOxxo').textContent = agrupar(orden.reference);
    $('vRefOxxo').dataset.plano = orden.reference || '';
    $('vImporteOxxo').textContent = importe;
    if (orden.barcode) { $('vBarcode').src = orden.barcode; ver($('cajaBarcode')); }
    $('txtEspera').textContent = t('esperando_oxxo');
  } else {
    ver($('panelSpei'));
    $('vClabe').textContent = agrupar(orden.clabe);
    $('vClabe').dataset.plano = orden.clabe || '';
    $('vImporte').textContent = importe;
    if (orden.bank_name) { $('vBanco').textContent = orden.bank_name; ver($('cajaBanco')); }
    $('vConcepto').textContent = concepto;
    $('vConcepto').dataset.plano = concepto;
    $('txtEspera').textContent = t('esperando');
    pintarChipsBanco(importe, concepto);
  }

  /* El bloque "Guarda tu acceso" se quito de la pantalla. Este codigo se
     queda, protegido, para que devolverlo sea recuperar el HTML y ya. */
  const enlace = `${location.origin}/api/access?t=${encodeURIComponent(orden.access_token)}`;
  if ($('vEnlace')) {
    $('vEnlace').textContent = enlace;
    $('vEnlace').dataset.plano = enlace;
  }

  $('txtPedido').textContent = t('pedido', { id: orden.external_id });
  arrancarReloj();
  arrancarConsulta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* La CLABE son 18 dígitos que se teclean en el banco: agrupados de 4 en
   4 se leen sin perder la cuenta. */
/* Agrupa de 4 en 4 SOLO si son puros digitos, como la CLABE: los
   espacios ayudan a teclear sin saltarse un numero. Una referencia con
   letras o guion bajo se muestra tal cual -- partida quedaba
   "sbx_ b8ca 210d", que parece rota y hace dudar de si los espacios son
   parte del codigo. */
const agrupar = (s) => {
  const v = String(s || '');
  return /^\d+$/.test(v) ? v.replace(/(.{4})/g, '$1 ').trim() : v;
};

function pintarChipsBanco(importe, concepto) {
  const cont = $('chipsBanco');
  cont.textContent = '';
  for (const id of ORDEN_BANCOS) {
    const { nombre } = pasosBanco(id);
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'chip';
    b.textContent = nombre;
    b.addEventListener('click', () => {
      for (const o of cont.children) o.classList.toggle('on', o === b);
      const { nombre: n, pasos } = pasosBanco(id);
      $('pasosTitulo').textContent = t('pasos_titulo', { banco: n });
      const ol = $('pasosLista');
      ol.textContent = '';
      for (const p of pasos) {
        const li = document.createElement('li');
        li.textContent = p.split('{importe}').join(importe).split('{concepto}').join(concepto);
        ol.appendChild(li);
      }
      ver($('pasos'));
      try { localStorage.setItem(CLAVE_BANCO, id); } catch { /* ignora */ }
    });
    cont.appendChild(b);
  }
  let previo = null;
  try { previo = localStorage.getItem(CLAVE_BANCO); } catch { /* ignora */ }
  if (previo) {
    const i = ORDEN_BANCOS.indexOf(previo);
    if (i >= 0) cont.children[i].click();
  }
}

/* ── Copiar, con alternativa manual ─────────────────────────────── */
document.addEventListener('click', async (ev) => {
  const b = ev.target.closest('[data-copia]');
  if (!b) return;
  const el = $(b.dataset.copia);
  const texto = el.dataset.plano || el.textContent.trim();
  const manual = { vClabe: 'manualClabe', vRefOxxo: 'manualRef', vEnlace: 'manualEnlace' }[b.dataset.copia];

  const hecho = () => {
    const antes = b.textContent;
    b.textContent = t('copiado');
    b.classList.add('hecho');
    setTimeout(() => { b.textContent = antes; b.classList.remove('hecho'); }, 2000);
  };

  try {
    if (!navigator.clipboard?.writeText) throw new Error('sin api');
    await navigator.clipboard.writeText(texto);
    hecho();
    return;
  } catch { /* sigue al plan B */ }

  /* Plan B: seleccionar el texto y decir qué hacer. Nunca se deja a la
     persona sin forma de llevarse el número. */
  try {
    const rango = document.createRange();
    rango.selectNodeContents(el);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(rango);
    if (document.execCommand && document.execCommand('copy')) { hecho(); return; }
  } catch { /* ignora */ }

  if (manual) { const m = $(manual); m.textContent = t('copia_manual'); ver(m); }
});

/* ── Reloj de validez ───────────────────────────────────────────
   La documentación de XPag no expone vencimiento para MXN, así que este
   plazo es una política nuestra (REF_HOURS). Al llegar a cero NO se
   declara muerta la referencia: se ofrece generar otra y se sigue
   consultando, porque puede seguir siendo válida y matarla en pantalla
   costaría ventas. */
function arrancarReloj() {
  clearInterval(relojTimer);
  const horas = Number(cfg.ref_hours || 24);
  const fin = (orden.guardado || Date.now()) + horas * 3600 * 1000;
  const tic = () => {
    const resta = fin - Date.now();
    if (resta <= 0) {
      $('txtValidez').textContent = t('vencida');
      ver($('btnNueva'));
      clearInterval(relojTimer);
      return;
    }
    const s = Math.floor(resta / 1000);
    const hh = String(Math.floor(s / 3600)).padStart(2, '0');
    const mm = String(Math.floor((s % 3600) / 60)).padStart(2, '0');
    const ss = String(s % 60).padStart(2, '0');
    $('txtValidez').textContent = `${t('validez', { horas })} ${t('validez_restante', { reloj: `${hh}:${mm}:${ss}` })}`;
  };
  tic();
  relojTimer = setInterval(tic, 1000);
}

let consultarAhora = () => {};

/* ── Simulacion (solo sandbox) ───────────────────────────────
   Prueba lo unico que no se puede probar de otra forma: que el
   comprador reciba los PDFs solo, cuando el pago confirma. El endpoint
   responde 404 sin XPAG_SANDBOX, asi que esto se apaga solo al pasar a
   produccion.

   No toca la pantalla a mano: deja que el sondeo normal descubra el
   cambio, que es exactamente lo que pasa con un pago real. Si la
   pantalla cambia sola despues de pulsar, la entrega funciona. */
document.querySelectorAll('button.sim').forEach((b) => {
  b.addEventListener('click', async () => {
    if (!orden?.access_token) return;
    const botones = document.querySelectorAll('button.sim');
    botones.forEach((x) => { x.disabled = true; });
    $('simNota').textContent = '...';
    try {
      const r = await fetch('/api/simular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ t: orden.access_token, outcome: b.dataset.outcome }),
      });
      const d = await r.json();
      /* El detalle crudo se muestra a proposito: si XPag espera otros
         nombres de campo, se ve aqui en vez de fallar en silencio. */
      $('simNota').textContent = d.ok
        ? 'XPag acepto. Esperando que la pantalla lo note sola...'
        : `XPag respondio ${d.http || r.status}: ${JSON.stringify(d.respuesta || d)}`.slice(0, 220);
      if (d.ok) consultarAhora();
    } catch {
      $('simNota').textContent = 'No se pudo llamar a /api/simular';
    }
    botones.forEach((x) => { x.disabled = false; });
  });
});

/* ── Order bumps ─────────────────────────────────────
   Van DESMARCADOS a proposito. Marcados de origen convierten mas, pero
   aqui se paga por transferencia: ver un importe distinto al esperado ya
   dentro del app del banco es abandono, y no te enteras de por que. En
   Mexico ademas es cobro no autorizado expresamente, que es tema de
   PROFECO.

   El total de la pantalla es solo informativo. Quien cobra es el
   servidor, que suma de su propia tabla: el navegador manda ids, nunca
   cantidades. */
function bumpsMarcados() {
  return [...document.querySelectorAll('#bumps input:checked')].map((i) => i.value);
}

function totalConBumps() {
  const extra = bumpsMarcados()
    .reduce((s, id) => s + (cfg.bumps.find((b) => b.id === id)?.amount || 0), 0);
  return (oferta?.amount || 0) + extra;
}

function pintarBumps() {
  const cont = $('bumps');
  if (!cont || !Array.isArray(cfg.bumps) || !cfg.bumps.length || !oferta) return;
  cont.textContent = '';

  for (const b of cfg.bumps) {
    const lab = document.createElement('label');
    lab.className = 'bump';

    const inp = document.createElement('input');
    inp.type = 'checkbox';
    inp.value = b.id;
    inp.checked = false;

    const txt = document.createElement('span');
    const nombre = document.createElement('b');
    nombre.textContent = t(b.nombreClave);
    const mas = document.createElement('span');
    mas.className = 'bump-mas';
    mas.textContent = '  +' + pesos(b.amount, oferta.currency);
    nombre.appendChild(mas);
    const desc = document.createElement('span');
    desc.className = 'bump-txt';
    desc.textContent = t(b.textoClave);
    txt.append(nombre, desc);

    inp.addEventListener('change', () => {
      $('ofTotal').textContent = pesos(totalConBumps(), oferta.currency);
    });

    lab.append(inp, txt);
    cont.appendChild(lab);
  }

  $('lBumps').textContent = t('l_bumps');
  ver($('fsBumps'));
}

/* ── Consulta de estado ─────────────────────────────────────────── */
function arrancarConsulta() {
  clearTimeout(timer);
  const inicio = Date.now();

  const programar = () => {
    /* Primeros 20 min cada 6 s; después cada minuto. El OXXO puede tardar
       horas y no tiene sentido machacar el endpoint. */
    const espera = Date.now() - inicio > 20 * 60 * 1000 ? 60_000 : 6_000;
    timer = setTimeout(consultar, espera);
  };

  async function consultar() {
    if (!orden?.access_token) return;
    try {
      const url = `/api/status?t=${encodeURIComponent(orden.access_token)}`
        + (orden.transaction_id ? `&tx=${encodeURIComponent(orden.transaction_id)}` : '');
      const d = await (await fetch(url)).json();
      if (d.status === 'confirmed') { confirmar(d); return; }
      if (d.status === 'expired' || d.status === 'failed') {
        $('txtEspera').textContent = t('vencida');
        ver($('btnNueva'));
        return;
      }
    } catch { /* red caída: se reintenta en el siguiente ciclo */ }
    programar();
  }

  programar();
  /* Deja que la simulacion fuerce una consulta inmediata. */
  consultarAhora = () => { clearTimeout(timer); consultar(); };

  /* El momento en que alguien vuelve del app del banco. */
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && orden?.access_token && $('secOk').hidden) {
      clearTimeout(timer);
      consultar();
    }
  });
}

/* ── Confirmado ─────────────────────────────────────────────────── */
function confirmar(d) {
  clearTimeout(timer);
  clearInterval(relojTimer);
  ver($('secPago'), false);
  ver($('secOk'));
  $('confBtn').href = `/api/access?t=${encodeURIComponent(orden.access_token)}`;
  $('confPedido').textContent = t('conf_pedido', { id: orden.external_id });

  /* Purchase sólo aquí: después de que el servidor verificó el pago
     contra XPag. eventID = e2e, único por pago. */
  pixel.compra({
    value: d.amount ?? orden.amount,
    currency: d.currency ?? orden.currency,
    eventId: d.event_id || orden.external_id,
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ── Contacto opcional, después de tener la referencia ──────────────
   El bloque se quito de la pantalla, asi que este manejador solo se
   engancha si el HTML vuelve. */
$('btnContacto')?.addEventListener('click', async () => {
  $('errContacto').textContent = '';
  const valor = $('whatsapp').value.trim();
  if (!valor) { $('errContacto').textContent = t('err_contact'); return; }
  try {
    const r = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ t: orden.access_token, whatsapp: valor }),
    });
    const d = await r.json();
    if (!r.ok || !d.ok) { $('errContacto').textContent = t(d.error || 'err_contact'); return; }
    ver($('contactoOk'));
    $('whatsapp').disabled = true;
    $('btnContacto').disabled = true;
  } catch { $('errContacto').textContent = t('err_red'); }
});

$('btnNueva').addEventListener('click', () => {
  olvidarOrden();
  location.href = location.pathname + location.search;
});

arrancar();
