/* Muestra los order bumps que esta persona compro.
   ────────────────────────────────────────────────────────────────
   La lista llega en ?x=, puesta por /api/access despues de verificar el
   pago contra XPag. Aqui NO se verifica nada y no hace falta: lo que
   protege el archivo no es esconder el bloque, es que su ruta lleva un
   segmento aleatorio y solo sale del servidor, para quien pago. Quien
   compro nada mas lo principal nunca ve esas rutas.

   Si el parametro viene roto o falta, la pagina se queda como estaba y
   los cuatro archivos de siempre siguen ahi. */
(function () {
  var x = new URLSearchParams(location.search).get('x');
  if (!x) return;

  var lista;
  try {
    lista = JSON.parse(decodeURIComponent(escape(atob(
      x.replace(/-/g, '+').replace(/_/g, '/')))));
  } catch (e) { return; }
  if (!Array.isArray(lista) || !lista.length) return;

  var caja = document.getElementById('extras');
  lista.forEach(function (it) {
    if (!it || typeof it.r !== 'string' || !/^descargas\//.test(it.r)) return;
    var a = document.createElement('a');
    a.className = 'archivo';
    a.href = '/' + it.r;
    a.setAttribute('download', '');
    a.innerHTML =
      '<span class="icono">PDF</span>' +
      '<span><b></b><span></span></span>' +
      '<span class="flecha" aria-hidden="true">&darr;</span>';
    a.querySelector('b').textContent = String(it.t || 'Material');
    a.querySelector('span span').textContent =
      (it.p ? it.p + ' páginas · ' : '') + 'Tuyo para siempre';
    caja.appendChild(a);
  });

  if (caja.children.length) document.getElementById('cajaExtras').hidden = false;
})();
