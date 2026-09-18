"""
Piezas de armado de los PDFs de Azúcar en Equilibrio.

Cada entregable (el ebook y los 3 bonos) es un módulo en contenido/ que
llama a estas funciones. La idea es que el texto quede separado del
formato: para cambiar una dosis se edita el módulo de contenido, no el
HTML, y para cambiar cómo se ve una ficha se edita aquí o en css/print.css.

Las anclas: cada ficha y cada capítulo escribe un token invisible en la
página (color del papel, 6pt). Después de la primera impresión se lee el
PDF con pypdf, se ve en qué página cayó cada token y con eso se numera el
índice en la segunda impresión. Es la única forma de tener un índice con
números reales usando Chromium, que no soporta las cajas de margen de CSS.
"""

import html as _html

# registro de la pasada actual: token -> (titulo, nivel)
ANCLAS: dict[str, tuple[str, int]] = {}


def reset():
    ANCLAS.clear()


def e(t):
    """Escapa texto que viene del contenido."""
    return _html.escape(str(t), quote=False)


def ancla(token, titulo=None, nivel=1):
    """Marca invisible para numerar el índice y armar los marcadores del PDF."""
    if titulo:
        ANCLAS[token] = (titulo, nivel)
    return f'<span class="ancla">[[{token}]]</span>'


# ------------------------------------------------------------------
# portada
# ------------------------------------------------------------------
def portada(sello, titulo_html, sub, cuenta, autor="de la Abuela Mei",
            nota=None, hoja="&#10047;"):
    nota = nota or (
        "Guía de cuidado casero de uso tradicional, de carácter informativo. "
        "No es un medicamento y no sustituye la consulta ni el tratamiento médico."
    )
    return f"""<div class="portada">
  <div class="portada-sello">{sello}</div>
  <div class="portada-hoja">{hoja}</div>
  <h1>{titulo_html}</h1>
  <div class="portada-linea"></div>
  <p class="portada-sub">{sub}</p>
  <div class="portada-pie">
    <div class="portada-cuenta">{cuenta}</div>
    <div class="portada-autor">{autor}</div>
    <p class="portada-nota">{nota}</p>
  </div>
</div>"""


# ------------------------------------------------------------------
# estructura
# ------------------------------------------------------------------
def capitulo(etiqueta, titulo, sub="", cuantos="", token=None, nivel=0):
    a = ancla(token, titulo, nivel) if token else ""
    sub = f'<p class="apertura-sub">{sub}</p>' if sub else ""
    cnt = f'<span class="apertura-cuantos">{cuantos}</span>' if cuantos else ""
    return f"""<section class="apertura">{a}
  <div class="apertura-num">{etiqueta}</div>
  <h2>{titulo}</h2>
  {sub}
  {cnt}
</section>"""


def seccion(titulo, token=None, nivel=1):
    a = ancla(token, titulo, nivel) if token else ""
    return f'<h2 class="seccion">{a}{titulo}</h2>'


def sub(titulo):
    return f'<h3 class="sub">{titulo}</h3>'


def mini(titulo):
    return f'<h4 class="mini">{titulo}</h4>'


def parrafo(txt, clase=""):
    c = f' class="{clase}"' if clase else ""
    return f"<p{c}>{txt}</p>"


def entrada(txt):
    return f'<p class="entrada">{txt}</p>'


def filete():
    return '<div class="filete"></div>'


def regla():
    return '<hr class="regla">'


def salto():
    return '<div class="salto"></div>'


def lista(items, clase="lista"):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="{clase}">{li}</ul>'


def lista_no(items):
    return lista(items, "lista lista-no")


def lista_pt(items):
    return lista(items, "lista lista-pt")


def numerada(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<ol class="lista-num">{li}</ol>'


def caja(titulo, cuerpo, tipo=""):
    """tipo: '' | 'verde' | 'alerta' | 'suave'"""
    clase = {"": "caja", "verde": "caja caja-verde",
             "alerta": "caja-alerta", "suave": "caja-suave"}[tipo]
    t = f"<h4>{titulo}</h4>" if titulo else ""
    return f'<div class="{clase}">{t}{cuerpo}</div>'


def tabla(encabezados, filas, clase=""):
    th = "".join(f"<th>{h}</th>" for h in encabezados)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas)
    c = f' class="{clase}"' if clase else ""
    return f"<table{c}><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


# ------------------------------------------------------------------
# ficha de remedio
# ------------------------------------------------------------------
def remedio(n, nombre, tipo, para, ingredientes, preparacion,
            dosis, hora, advertencia, token=None):
    a = ancla(token or f"r{n:02d}", f"{n}. {nombre}", 2)
    ing = "".join(f"<li>{i}</li>" for i in ingredientes)
    prep = "".join(f"<li>{p}</li>" for p in preparacion)
    return f"""<div class="remedio">{a}
  <div class="remedio-top">
    <div class="remedio-num">{n:02d}</div>
    <h3>{nombre}</h3>
  </div>
  <span class="remedio-tipo">{tipo}</span>
  <p class="remedio-para">{para}</p>
  <div class="fila">
    <div class="fila-et">Lo que lleva</div>
    <div class="fila-va"><ul>{ing}</ul></div>
  </div>
  <div class="fila">
    <div class="fila-et">Cómo se hace</div>
    <div class="fila-va"><ol>{prep}</ol></div>
  </div>
  <div class="fila fila-clave">
    <div class="fila-et">Dosis</div>
    <div class="fila-va">{dosis}</div>
  </div>
  <div class="fila fila-clave">
    <div class="fila-et">A qué hora</div>
    <div class="fila-va">{hora}</div>
  </div>
  <div class="fila-adv">
    <div class="fila-et">Advertencia</div>
    <div>{advertencia}</div>
  </div>
</div>"""


# ------------------------------------------------------------------
# ficha de ingrediente (Bono 2)
# ------------------------------------------------------------------
def ingrediente(nombre, otros, filas, ojo=None, token=None):
    a = ancla(token, nombre, 2) if token else ""
    ot = f'<p class="otros">{otros}</p>' if otros else ""
    fl = "".join(
        f'<div class="ing-fila"><div class="et">{et}</div><div class="va">{va}</div></div>'
        for et, va in filas)
    oj = f'<div class="ing-ojo">{ojo}</div>' if ojo else ""
    return f'<div class="ingrediente">{a}<h3>{nombre}</h3>{ot}{fl}{oj}</div>'


# ------------------------------------------------------------------
# día del reto (Bono 1)
# ------------------------------------------------------------------
def dia(n, etiqueta, titulo, momentos, gesto=None, token=None):
    a = ancla(token, f"Día {n}", 2) if token else ""
    mm = "".join(
        f'<div class="momento"><div class="cuando">{c}</div><div class="que">{q}</div></div>'
        for c, q in momentos)
    g = f'<div class="dia-gesto"><b>El gesto de hoy:</b> {gesto}</div>' if gesto else ""
    return f"""<div class="dia">{a}
  <div class="dia-top">
    <div class="dia-num">{n}</div>
    <div class="dia-tit"><div class="dia-eti">{etiqueta}</div><h3>{titulo}</h3></div>
    <div class="dia-marca"></div>
  </div>
  {mm}{g}
</div>"""


# ------------------------------------------------------------------
# índice — se numera con el mapa de la primera pasada
# ------------------------------------------------------------------
def indice(entradas, paginas):
    """entradas: lista de ('grupo', texto) | ('cap', token, texto) | ('it', token, texto)"""
    out = ['<div class="indice">']
    for ent in entradas:
        if ent[0] == "grupo":
            out.append(f'<div class="indice-grupo">{ent[1]}</div>')
            continue
        kind, token, texto = ent
        p = paginas.get(token, "")
        cls = "idx idx-cap" if kind == "cap" else "idx"
        out.append(
            f'<div class="{cls}"><span class="idx-t">{texto}</span>'
            f'<span class="idx-l"></span><span class="idx-p">{p}</span></div>')
    out.append("</div>")
    return "".join(out)


# ------------------------------------------------------------------
# cierre
# ------------------------------------------------------------------
LEGAL = (
    "<b>Aviso legal.</b> Este material es una guía de cuidado casero de uso "
    "tradicional, con fines informativos y educativos. No es un medicamento, "
    "no constituye consulta médica y no sustituye el diagnóstico, el "
    "tratamiento ni el seguimiento de un profesional de la salud. No "
    "suspendas ni modifiques por tu cuenta ningún medicamento para la "
    "diabetes, la presión o el corazón. Varias plantas de uso tradicional "
    "pueden interactuar con la metformina, las sulfonilureas, la insulina, "
    "los anticoagulantes y los medicamentos para la presión: consulta a tu "
    "médico antes de empezar. Si tienes embarazo, lactancia, enfermedad del "
    "riñón o del hígado, o una cirugía programada, consulta antes de usar "
    "cualquiera de estos remedios."
)


def cierre(titulo, cuerpo, legal=None):
    return f"""<section class="cierre">
  <h2>{titulo}</h2>
  {cuerpo}
  <p class="legal">{legal or LEGAL}</p>
</section>"""
