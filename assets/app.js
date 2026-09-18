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

let cfg = { brand: null, pixel_id: null, ref_hours: 24, sandbox: false, offers: [] };
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
  $('btnContacto').textContent = t('contacto_btn');
  $('name').placeholder = t('ph_nombre');
  $('whatsapp').placeholder = t('ph_whatsapp');
  $('vBarcode').alt = t('k_ref_oxxo');
  for (const b of document.querySelectorAll('[data-copia]')) {
    b.textContent = b.dataset.copia === 'vClabe' ? t('copiar_clabe') : t('copiar');
  }
  $('avisoPrueba').textContent = t('modo_prueba');
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
  }

  const guardada = leerOrden();
  if (guardada) { orden = guardada; mostrarPago(); return; }

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
        offer: oferta?.id, name: nombre, method: metodo,
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
  ver($('avisoPrueba'), Boolean(orden.sandbox || cfg.sandbox));

  const importe = pesos(orden.amount, orden.currency);
  const concepto = orden.reference || orden.external_id;

  /* El nombre del extracto. Si no coincide con la marca, se explica; es
     la diferencia entre transferir y abandonar. */
  if (orden.beneficiary) {
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

  const enlace = `${location.origin}/api/access?t=${encodeURIComponent(orden.access_token)}`;
  $('vEnlace').textContent = enlace;
  $('vEnlace').dataset.plano = enlace;

  $('txtPedido').textContent = t('pedido', { id: orden.external_id });
  arrancarReloj();
  arrancarConsulta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* La CLABE son 18 dígitos que se teclean en el banco: agrupados de 4 en
   4 se leen sin perder la cuenta. */
const agrupar = (s) => String(s || '').replace(/(.{4})/g, '$1 ').trim();

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

/* ── Contacto opcional, después de tener la referencia ──────────── */
$('btnContacto').addEventListener('click', async () => {
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
