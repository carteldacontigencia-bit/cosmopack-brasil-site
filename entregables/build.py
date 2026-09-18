#!/usr/bin/env python3
"""
Genera los PDF de Azúcar en Equilibrio.

    ../.venv/bin/python build.py            # los cuatro
    ../.venv/bin/python build.py ebook      # uno solo

Cómo funciona, en corto:

1. Cada entregable vive en contenido/<modulo>.py y expone META, portada(),
   cuerpo(paginas) y, si quiere, final().
2. La portada y la página de cierre se imprimen aparte, con margen 0, para
   que el color sangre de orilla a orilla y no les caiga el número de página.
3. El cuerpo se imprime dos veces. La primera pasada sirve para leer con
   pypdf en qué página quedó cada ancla invisible; la segunda ya lleva el
   índice numerado de verdad.
4. Se unen las partes, se les pone el árbol de marcadores y los metadatos.

Chromium no soporta las cajas de margen de CSS (@bottom-center), así que el
número de página se dibuja con la plantilla de pie de Playwright y las
fuentes de la marca van incrustadas en base64 dentro de assets/fonts/fonts.css.
"""

import glob
import importlib
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

import libro

AQUI = Path(__file__).parent
CSS = (AQUI / "css/print.css").read_text(encoding="utf-8")
FUENTES = (AQUI / "assets/fonts/fonts.css").read_text(encoding="utf-8")
SALIDA = AQUI / "out"
TMP = AQUI / ".tmp"

ENTREGABLES = ["ebook", "bono1_reto30", "bono2_mercado", "bono3_sos",
                "corazon", "noches", "manos"]

# margen del cuerpo; tiene que coincidir con el @page de print.css
MARGEN = {"top": "15mm", "bottom": "17mm", "left": "13mm", "right": "13mm"}


def pagina_html(cuerpo, margen_cero=False, titulo=""):
    extra = """
    @page { size: 148mm 210mm; margin: 0; }
    body { margin: 0; }
    """ if margen_cero else ""
    return f"""<!doctype html>
<html lang="es-MX"><head><meta charset="utf-8"><title>{titulo}</title>
<style>{FUENTES}</style>
<style>{CSS}</style>
<style>{extra}</style>
</head><body>{cuerpo}</body></html>"""


def pie(titulo):
    """Pie de página: filete, título corto a la izquierda, número al centro."""
    return f"""<div style="width:100%;font-family:Arial,Helvetica,sans-serif;
      font-size:8px;color:#6B6355;padding:0 13mm;margin-top:3mm;
      -webkit-print-color-adjust:exact;">
  <div style="border-top:0.5px solid #E4DAC6;padding-top:2mm;
       display:flex;justify-content:space-between;align-items:center;">
    <span style="letter-spacing:.06em;">{titulo}</span>
    <span style="font-weight:700;color:#3A5240;font-size:9px;"
          class="pageNumber"></span>
    <span style="letter-spacing:.06em;">Abuela Mei</span>
  </div>
</div>"""


def imprimir(page, html, destino, margen_cero=False, titulo_pie=None):
    page.set_content(html, wait_until="load")
    page.emulate_media(media="print")
    opciones = dict(
        path=str(destino),
        format="A5",
        prefer_css_page_size=True,
        print_background=True,
    )
    if margen_cero:
        opciones["margin"] = {"top": "0", "bottom": "0", "left": "0", "right": "0"}
    else:
        opciones["margin"] = MARGEN
        if titulo_pie:
            opciones["display_header_footer"] = True
            opciones["header_template"] = "<div></div>"
            opciones["footer_template"] = pie(titulo_pie)
    page.pdf(**opciones)


def anclas_por_pagina(pdf):
    """token -> número de página (1 = primera hoja del cuerpo)."""
    mapa = {}
    for i, pg in enumerate(PdfReader(str(pdf)).pages, start=1):
        try:
            texto = pg.extract_text() or ""
        except Exception:
            texto = ""
        for token in re.findall(r"\[\[([A-Za-z0-9_]+)\]\]", texto):
            mapa.setdefault(token, i)
    return mapa


def unir(partes, destino, meta, marcadores):
    """Une las partes, cuelga los marcadores y escribe los metadatos."""
    w = PdfWriter()
    desplazamiento = {}
    for nombre, ruta in partes:
        inicio = len(w.pages)
        w.append(str(ruta))
        desplazamiento[nombre] = inicio

    padres = {}
    for token, (titulo, nivel) in marcadores.items():
        pag = meta["_paginas"].get(token)
        if not pag:
            continue
        indice = desplazamiento["cuerpo"] + pag - 1
        if indice >= len(w.pages):
            continue
        padre = padres.get(nivel - 1) if nivel > 0 else None
        item = w.add_outline_item(titulo, indice, parent=padre)
        padres[nivel] = item
        for n in list(padres):
            if n > nivel:
                padres.pop(n)

    w.add_metadata({
        "/Title": meta["titulo_pdf"],
        "/Author": meta.get("autor", "Abuela Mei"),
        "/Subject": meta.get("asunto", ""),
        "/Keywords": meta.get("claves", ""),
        "/Creator": "Azúcar en Equilibrio · Abuela Mei",
    })
    w.page_mode = "/UseOutlines"
    with open(destino, "wb") as f:
        w.write(f)
    return len(w.pages)


def construir(nombre, page):
    mod = importlib.import_module(f"contenido.{nombre}")
    meta = dict(mod.META)
    TMP.mkdir(exist_ok=True)
    SALIDA.mkdir(exist_ok=True)

    partes = []

    # --- portada, aparte y a sangre ---
    libro.reset()
    tapa = TMP / f"{nombre}-portada.pdf"
    imprimir(page, pagina_html(mod.portada(), margen_cero=True), tapa,
             margen_cero=True)
    partes.append(("portada", tapa))

    # --- cuerpo, primera pasada: solo para saber dónde cayó cada ancla ---
    libro.reset()
    p1 = TMP / f"{nombre}-cuerpo-1.pdf"
    imprimir(page, pagina_html(mod.cuerpo({})), p1,
             titulo_pie=meta["pie"])
    paginas = anclas_por_pagina(p1)

    # --- cuerpo, segunda pasada: índice ya numerado ---
    libro.reset()
    p2 = TMP / f"{nombre}-cuerpo-2.pdf"
    imprimir(page, pagina_html(mod.cuerpo(paginas)), p2,
             titulo_pie=meta["pie"])
    marcadores = dict(libro.ANCLAS)
    # el índice pudo moverse una hoja al llenarse los números: se relee
    paginas = anclas_por_pagina(p2)
    partes.append(("cuerpo", p2))

    # --- cierre, aparte y a sangre ---
    if hasattr(mod, "final"):
        libro.reset()
        fin = TMP / f"{nombre}-final.pdf"
        imprimir(page, pagina_html(mod.final(), margen_cero=True), fin,
                 margen_cero=True)
        partes.append(("final", fin))

    meta["_paginas"] = paginas
    destino = SALIDA / meta["archivo"]
    hojas = unir(partes, destino, meta, marcadores)
    kb = destino.stat().st_size / 1024
    print(f"  {meta['archivo']:<42} {hojas:>3} páginas  {kb:>7.0f} KB")
    return destino


def chromium():
    """El Chromium de la imagen, que no siempre es el que espera Playwright."""
    for patron in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                   "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        encontrados = sorted(glob.glob(patron))
        if encontrados:
            return encontrados[-1]
    return None


def main():
    pedidos = sys.argv[1:] or ENTREGABLES
    print("Generando entregables de Azúcar en Equilibrio\n")
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(
            executable_path=chromium(),
            args=["--no-sandbox", "--font-render-hinting=none"])
        page = navegador.new_page()
        for nombre in pedidos:
            construir(nombre, page)
        navegador.close()
    print("\nListo. Los archivos están en entregables/out/")


if __name__ == "__main__":
    main()
