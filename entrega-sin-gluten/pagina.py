# -*- coding: utf-8 -*-
"""
Arma entrega.html — la pantalla que ve el comprador después de pagar.

Las miniaturas son las portadas reales de los PDF, renderizadas acá y
pegadas como data: URI, así la página no depende de ningún archivo
externo para verse. Los PDF sí van aparte, como archivos publicados al
lado de la página, y la página se los entrega al visitante con la
capacidad `downloads`.
"""

import base64
import io
import os

import pypdfium2 as pdfium

AQUI = os.path.dirname(os.path.abspath(__file__))

PRODUCTOS = [
    dict(
        archivo="Recetas-de-Pan-Trenzado-Sin-Gluten.pdf",
        titulo="Recetas de Pan Trenzado",
        bajada="Sin gluten y sin leche",
        texto="La trenza paso a paso, de 3, 4 y 6 tiras, con harina de arroz, "
              "de maíz y de tapioca. Incluye el armado ilustrado, que es "
              "donde todo el mundo se traba la primera vez.",
        etiqueta="Libro principal",
    ),
    dict(
        archivo="Guia-de-Fermentacion-Natural-Sin-Gluten.pdf",
        titulo="Guía de Fermentación Natural",
        bajada="Masa madre sin gluten, por Chef Elena Sánchez",
        texto="Cómo levantar y mantener tu masa madre sin gluten, día por día, "
              "con harina de arroz y de trigo sarraceno. Más harinas de teff, "
              "sorgo, almendras y lino para darle sabor y estructura.",
        etiqueta="Guía",
    ),
]


def portada(ruta, ancho=340):
    doc = pdfium.PdfDocument(ruta)
    im = doc[0].render(scale=0.55).to_pil().convert("RGB")
    im.thumbnail((ancho, ancho * 2))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def tarjetas():
    from pypdf import PdfReader
    out = []
    for i, p in enumerate(PRODUCTOS):
        ruta = os.path.join(AQUI, "archivos", p["archivo"])
        paginas = len(PdfReader(ruta).pages)
        mb = os.path.getsize(ruta) / 1024 / 1024
        b64 = portada(ruta)
        out.append(f"""
      <article class="item">
        <img class="tapa" src="data:image/jpeg;base64,{b64}"
             alt="Portada de {p['titulo']}" width="340" height="481">
        <div class="ficha">
          <p class="etiqueta">{p['etiqueta']}</p>
          <h3>{p['titulo']}</h3>
          <p class="bajada">{p['bajada']}</p>
          <p class="cuerpo">{p['texto']}</p>
          <p class="datos"><span>{paginas} páginas</span><span>PDF · {mb:.1f} MB</span></p>
          <button class="bajar" type="button"
                  data-archivo="archivos/{p['archivo']}"
                  data-nombre="{p['archivo']}" id="b{i}">
            <span class="rotulo">Descargar</span>
          </button>
          <p class="aviso-bajar" id="a{i}" hidden></p>
        </div>
      </article>""")
    return "".join(out)


HTML = """<title>Delicias Sin Gluten</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Karla:wght@400;500;700&family=Parisienne&display=swap">
<style>
:root{
  --masa:#FBF7EE; --miga:#FFFFFF; --horno:#2B2118; --gris:#6E6254;
  --corteza:#9C6B1F; --sello:#A81E26; --linea:#E8DFCE; --verde:#3F6B44;
  --sombra:0 1px 2px rgba(60,44,26,.05), 0 8px 24px -12px rgba(60,44,26,.18);
  --display:'Archivo','Helvetica Neue',Arial,sans-serif;
  --texto:'Karla','Helvetica Neue',Arial,sans-serif;
  --firma:'Parisienne',cursive;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --masa:#161110; --miga:#211A15; --horno:#F3EBDD; --gris:#A79B8A;
    --corteza:#E3AD52; --sello:#E4737A; --linea:#352B22; --verde:#8CBE90;
    --sombra:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --masa:#161110; --miga:#211A15; --horno:#F3EBDD; --gris:#A79B8A;
  --corteza:#E3AD52; --sello:#E4737A; --linea:#352B22; --verde:#8CBE90;
  --sombra:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--masa); color:var(--horno);
  font-family:var(--texto); font-size:17px; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}
.envoltorio{width:100%; max-width:660px; margin-inline:auto; padding-inline:20px}
h1,h2,h3{font-family:var(--display); font-weight:800; line-height:1.15;
  letter-spacing:-.015em; text-wrap:balance; margin:0}
p{margin:0}
a{color:var(--corteza)}

/* ---------- barra de marca ---------- */
.marca{
  border-bottom:1px solid var(--linea); background:var(--masa);
  padding-block:14px; text-align:center;
}
.marca span{font-family:var(--firma); font-size:27px; color:var(--sello); line-height:1}

/* ---------- confirmación ---------- */
.cabecera{padding-block:44px 8px; text-align:center}
.tilde{
  width:46px; height:46px; margin:0 auto 18px; border-radius:50%;
  background:var(--verde); display:grid; place-items:center;
}
.tilde svg{width:22px; height:22px; display:block}
.cabecera h1{font-size:clamp(27px,6.4vw,37px); margin-bottom:12px}
.cabecera .sub{color:var(--gris); font-size:17px; max-width:44ch; margin-inline:auto}

/* ---------- títulos de sección ---------- */
.seccion{padding-block:40px}
.rotulo-seccion{
  font-family:var(--texto); font-size:12px; font-weight:700;
  letter-spacing:.14em; text-transform:uppercase; color:var(--corteza);
  margin-bottom:8px;
}
.seccion h2{font-size:clamp(21px,4.6vw,26px); margin-bottom:6px}
.seccion .intro{color:var(--gris); font-size:16px; margin-bottom:22px; max-width:56ch}

/* ---------- descargas ---------- */
.lista{display:flex; flex-direction:column; gap:20px}
.item{
  background:var(--miga); border:1px solid var(--linea); border-radius:14px;
  padding:20px; display:grid; gap:18px; grid-template-columns:118px 1fr;
  box-shadow:var(--sombra);
}
.tapa{
  width:100%; height:auto; max-width:100%; border-radius:6px;
  box-shadow:0 2px 6px rgba(60,44,26,.18), 0 10px 22px -12px rgba(60,44,26,.3);
  align-self:start;
}
.ficha{min-width:0}
.etiqueta{
  font-size:11px; font-weight:700; letter-spacing:.12em; text-transform:uppercase;
  color:var(--corteza); margin-bottom:5px;
}
.ficha h3{font-size:20px; margin-bottom:3px}
.bajada{font-size:14px; color:var(--sello); font-weight:700; margin-bottom:9px}
.cuerpo{font-size:15px; color:var(--gris); margin-bottom:12px}
.datos{display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px}
.datos span{
  font-size:12px; font-weight:700; color:var(--gris);
  border:1px solid var(--linea); border-radius:99px; padding:3px 10px;
  font-variant-numeric:tabular-nums;
}
.bajar{
  width:100%; font-family:var(--texto); font-size:16px; font-weight:700;
  background:var(--horno); color:var(--masa); border:0; border-radius:10px;
  padding:14px 18px; cursor:pointer; min-height:48px;
  transition:transform .15s ease, opacity .15s ease;
}
.bajar:hover{transform:translateY(-1px)}
.bajar:active{transform:translateY(0)}
.bajar[disabled]{opacity:.62; cursor:default; transform:none}
.bajar.ok{background:var(--verde); color:#fff}
.aviso-bajar{font-size:14px; color:var(--gris); margin-top:9px}
.aviso-bajar a{font-weight:700}

/* ---------- pasos ---------- */
.pasos{display:flex; flex-direction:column; gap:16px; counter-reset:paso}
.paso{display:grid; grid-template-columns:30px 1fr; gap:14px; align-items:start}
.paso::before{
  counter-increment:paso; content:counter(paso);
  font-family:var(--display); font-weight:800; font-size:15px;
  color:var(--corteza); border:1.5px solid var(--corteza); border-radius:50%;
  width:30px; height:30px; display:grid; place-items:center; line-height:1;
}
.paso h3{font-size:17px; margin-bottom:2px}
.paso p{font-size:15px; color:var(--gris)}

/* ---------- nota ---------- */
.nota{
  background:var(--miga); border:1px solid var(--linea);
  border-left:3px solid var(--corteza); border-radius:0 12px 12px 0;
  padding:20px 22px;
}
.nota h3{font-size:17px; margin-bottom:8px}
.nota p{font-size:15px; color:var(--gris)}
.nota p + p{margin-top:9px}
.nota b{color:var(--horno)}

/* ---------- preguntas ---------- */
details{border-bottom:1px solid var(--linea)}
details summary{
  font-family:var(--display); font-weight:700; font-size:16.5px;
  padding:16px 30px 16px 0; cursor:pointer; list-style:none; position:relative;
  min-height:48px; display:flex; align-items:center;
}
details summary::-webkit-details-marker{display:none}
details summary::after{
  content:'+'; position:absolute; right:4px; font-size:22px;
  color:var(--corteza); font-weight:500; line-height:1;
}
details[open] summary::after{content:'\\2212'}
details .r{font-size:15.5px; color:var(--gris); padding-bottom:18px; max-width:60ch}
details .r p + p{margin-top:9px}

/* ---------- pie ---------- */
.pie{
  border-top:1px solid var(--linea); margin-top:36px;
  padding-block:32px 44px; text-align:center;
}
.pie .firma{font-family:var(--firma); font-size:25px; color:var(--sello); margin-bottom:12px}
.pie p{font-size:14.5px; color:var(--gris); max-width:50ch; margin-inline:auto}
.contacto{
  display:inline-block; margin-top:14px; font-family:var(--texto);
  font-weight:700; font-size:15px; color:var(--horno);
  background:var(--miga); border:1px solid var(--linea);
  border-radius:99px; padding:10px 20px; user-select:all;
}
.legal{margin-top:24px; font-size:12.5px; line-height:1.55; color:var(--gris); opacity:.85}

:focus-visible{outline:3px solid var(--corteza); outline-offset:3px; border-radius:6px}
@media (prefers-reduced-motion: reduce){*{transition:none !important}}

@media (max-width:520px){
  .item{grid-template-columns:1fr; gap:14px}
  .tapa{width:132px; justify-self:start}
}
</style>

<header class="marca"><span>Delicias Sin Gluten</span></header>

<div class="envoltorio">

  <section class="cabecera">
    <div class="tilde" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3"
           stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.2 5.2L20 7"/></svg>
    </div>
    <h1>Listo, ya es tuyo</h1>
    <p class="sub">Descargá los archivos desde acá. Quedan tuyos para siempre
      y podés volver a esta página cuando quieras.</p>
  </section>

  <section class="seccion">
    <p class="rotulo-seccion">Tus archivos</p>
    <h2>Descargá tu material</h2>
    <p class="intro">Tocá el botón de cada uno. Se va a abrir un cartel para
      confirmar la descarga — aceptalo y el PDF queda guardado en tu equipo.</p>
    <div class="lista">__TARJETAS__</div>
  </section>

  <section class="seccion">
    <p class="rotulo-seccion">Por dónde empezar</p>
    <h2>Tu primera semana</h2>
    <p class="intro">Si nunca amasaste sin gluten, este es el orden que menos
      frustración te va a dar.</p>
    <div class="pasos">
      <div class="paso"><div>
        <h3>Empezá por la trenza, no por la masa madre</h3>
        <p>La trenza sale con levadura común y en una tarde. La masa madre
          tarda entre 7 y 10 días en estar lista, así que conviene arrancarla
          en paralelo, no antes.</p>
      </div></div>
      <div class="paso"><div>
        <h3>Comprá las tres harinas base</h3>
        <p>Arroz, tapioca (mandioca) y maíz. Con esas tres hacés todo el libro
          de trenzas. Las de teff y sorgo son para después, cuando quieras
          cambiarle el sabor.</p>
      </div></div>
      <div class="paso"><div>
        <h3>Recién ahí, la masa madre</h3>
        <p>Cuando ya te salga la trenza, abrí la guía de fermentación y
          arrancá el fermento. Son cinco minutos por día durante una semana,
          y después te dura años.</p>
      </div></div>
    </div>
  </section>

  <section class="seccion">
    <p class="rotulo-seccion">Importante</p>
    <h2>Sobre el gluten en estas recetas</h2>
    <div class="nota">
      <h3>El «trigo sarraceno» no tiene gluten</h3>
      <p>En la guía de fermentación vas a leer <b>harina de trigo sarraceno</b>
        y te vas a asustar. Es un nombre confuso: el sarraceno o alforfón
        <b>no es trigo</b> ni es un cereal, y no tiene gluten. Es seguro para
        celíacos.</p>
      <p>Lo que sí importa es la <b>contaminación cruzada</b>: si sos celíaco,
        comprá harinas con la etiqueta «sin TACC», usá utensilios y horno
        limpios, y no compartas el tostador ni la tabla con pan común. Una
        receta sin gluten deja de serlo en una cocina contaminada.</p>
      <p>La avena merece la misma atención: es sin gluten por naturaleza, pero
        casi siempre viaja contaminada. Si la usás, que diga «sin TACC» en el
        paquete.</p>
    </div>
  </section>

  <section class="seccion">
    <p class="rotulo-seccion">Guardalo bien</p>
    <h2>Que no se te pierda</h2>
    <p class="intro">El error más común es descargar el archivo y no encontrarlo
      nunca más. Treinta segundos ahora te lo evitan.</p>
    <div class="pasos">
      <div class="paso"><div>
        <h3>En el celular</h3>
        <p>Después de descargar, buscá el PDF en <b>Archivos</b> (iPhone) o en
          <b>Descargas</b> (Android). Movelo a una carpeta que se llame
          «Recetas» y así lo tenés a mano en la cocina.</p>
      </div></div>
      <div class="paso"><div>
        <h3>Guardá también esta página</h3>
        <p>Agregala a favoritos o mandate el link por WhatsApp a vos misma. Si
          perdés el archivo, volvés acá y lo descargás de nuevo.</p>
      </div></div>
      <div class="paso"><div>
        <h3>Mandate una copia por mail</h3>
        <p>Es la forma más segura: el mail no se borra cuando cambiás de
          teléfono, y podés abrirlo desde cualquier lado.</p>
      </div></div>
    </div>
  </section>

  <section class="seccion">
    <p class="rotulo-seccion">Preguntas</p>
    <h2>Dudas frecuentes</h2>
    <details open>
      <summary>Toqué descargar y no pasó nada</summary>
      <div class="r"><p>Fijate si apareció un cartel de confirmación y quedó
        esperando: hay que aceptarlo. Si no aparece, probá desde otro navegador
        o desde la computadora. Si sigue sin andar, escribinos y te mandamos
        los archivos por mail.</p></div>
    </details>
    <details>
      <summary>¿Cómo abro un PDF?</summary>
      <div class="r"><p>En el celular se abre solo al tocarlo. En la computadora,
        con cualquier navegador o con Adobe Reader, que es gratis. No necesitás
        instalar nada raro.</p></div>
    </details>
    <details>
      <summary>¿Lo puedo imprimir?</summary>
      <div class="r"><p>Sí, es tuyo. Imprimilo entero o solo las recetas que
        uses. Muchas prefieren imprimir la del armado de la trenza y dejarla
        pegada en la cocina.</p></div>
    </details>
    <details>
      <summary>¿Estas recetas sirven para celíacos?</summary>
      <div class="r"><p>Las recetas están formuladas sin gluten: usan harina de
        arroz, maíz, tapioca, sorgo, teff y trigo sarraceno, que no lo contienen.
        Aun así, leé la sección de arriba sobre contaminación cruzada — con
        celiaquía, el cuidado en la cocina importa tanto como la receta.</p></div>
    </details>
    <details>
      <summary>¿Puedo compartirlo con una amiga?</summary>
      <div class="r"><p>Preferimos que no. Es material con derechos de autor y
        cada copia que se regala es lo que hace que estos libros dejen de
        producirse. Pasale el link de compra y listo.</p></div>
    </details>
  </section>

  <footer class="pie">
    <p class="firma">Delicias Sin Gluten</p>
    <p>¿Algo no funcionó o querés preguntar algo de una receta? Escribinos y
      te respondemos.</p>
    <p class="contacto" id="contacto">__CONTACTO__</p>
    <p class="legal">Material con derechos de autor. Prohibida su reproducción,
      distribución o reventa. Las recetas tienen fines informativos y
      gastronómicos: si tenés celiaquía, alergia alimentaria u otra condición
      de salud, consultá con tu médico o nutricionista sobre tu alimentación.</p>
  </footer>
</div>

<script>
(function(){
  var caps = null;
  var pendiente = window.claude && window.claude.use
      ? window.claude.use("downloads").catch(function(){ return null; })
      : Promise.resolve(null);

  pendiente.then(function(d){ caps = d; });

  function texto(el, msg, html){
    if(html){ el.innerHTML = msg; } else { el.textContent = msg; }
    el.hidden = false;
  }

  document.querySelectorAll(".bajar").forEach(function(btn){
    var aviso = document.getElementById("a" + btn.id.slice(1));
    var rotulo = btn.querySelector(".rotulo");
    btn.addEventListener("click", function(){
      if(btn.disabled) return;
      btn.disabled = true;
      aviso.hidden = true;
      rotulo.textContent = "Preparando\\u2026";

      Promise.resolve(pendiente).then(function(){
        if(!caps){
          throw { code: "unavailable" };
        }
        return fetch(btn.dataset.archivo).then(function(r){
          if(!r.ok) throw { code: "fetch" };
          return r.blob();
        }).then(function(blob){
          return caps.save({ filename: btn.dataset.nombre, data: blob });
        });
      }).then(function(){
        btn.classList.add("ok");
        rotulo.textContent = "Descargado";
        texto(aviso, "Gu\\u00e1rdalo en una carpeta que encuentres despu\\u00e9s.");
        setTimeout(function(){
          btn.disabled = false;
          btn.classList.remove("ok");
          rotulo.textContent = "Descargar de nuevo";
        }, 4000);
      }).catch(function(e){
        btn.disabled = false;
        rotulo.textContent = "Descargar";
        var c = e && e.code;
        if(c === "declined"){
          texto(aviso, "Cancelaste la descarga. Tocá el botón otra vez cuando quieras.");
        } else if(c === "rate_limited"){
          texto(aviso, "Esperá unos segundos y probá de nuevo.");
        } else {
          texto(aviso, 'No se pudo descargar desde acá. Abrilo en otra pestaña: ' +
            '<a href="' + btn.dataset.archivo + '" target="_blank" rel="noopener">' +
            btn.dataset.nombre + '</a>', true);
        }
      });
    });
  });
})();
</script>
"""


def main():
    # Sin contacto real no se inventa uno: el marcador tiene que verse.
    contacto = os.environ.get(
        "CONTACTO_ENTREGA",
        "&#9998; Reemplazar por tu WhatsApp o tu mail de soporte")
    html = HTML.replace("__TARJETAS__", tarjetas()).replace("__CONTACTO__", contacto)
    destino = os.path.join(AQUI, "entrega.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"entrega.html — {os.path.getsize(destino)/1024:.0f} KB")


if __name__ == "__main__":
    main()
