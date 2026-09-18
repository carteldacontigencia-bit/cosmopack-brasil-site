/* Meta Pixel para las paginas de venta.
   ────────────────────────────────────────────────────────────────
   El ID va escrito aqui a proposito: estas paginas son estaticas, no
   pasan por ninguna funcion, asi que no pueden leer una variable de
   entorno. Y no es un secreto: el Pixel ID viaja en el HTML de
   cualquier sitio que lo use, es publico por naturaleza. Lo que si es
   secreto es el token de la Conversions API, y ese vive solo en el
   servidor.

   QUE SE DISPARA AQUI, Y PARA QUIEN:

   PageView y ViewContent se mandan para TODO visitante, no solo para
   quien viene de anuncio. Es distinto de lo que hace assets/pixel.js en
   la pantalla de pago, y es a proposito: sin PageView de todos, Meta no
   puede armar publicos de retargeting ni aprender como es la gente que
   llega. Los eventos de checkout si se limitan al trafico de anuncio,
   para que la atribucion de venta no se ensucie.

   El nombre del producto se lee del atributo data-producto de la propia
   etiqueta <script>, para que las tres paginas compartan este archivo.

   Si Meta esta caido o bloqueado por el navegador, la pagina sigue
   funcionando igual: aqui no cuelga nada de la venta.               */

const PIXEL_ID = '4479089439026636';

(function () {
  var etiqueta = document.currentScript;
  var producto = (etiqueta && etiqueta.dataset.producto) || document.title;
  var valor = etiqueta && etiqueta.dataset.valor;
  var moneda = (etiqueta && etiqueta.dataset.moneda) || 'MXN';

  if (!window.fbq) {
    var n = (window.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    });
    n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://connect.facebook.net/en_US/fbevents.js';
    document.head.appendChild(s);
  }

  window.fbq('init', PIXEL_ID);
  window.fbq('track', 'PageView');

  var datos = { content_name: producto, content_type: 'product' };
  if (valor) { datos.value = Number(valor); datos.currency = moneda; }
  window.fbq('track', 'ViewContent', datos);
})();
