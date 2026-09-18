#!/usr/bin/env python3
"""
Control de calidad de los PDF.

    ../.venv/bin/python revisar.py

Hace dos comprobaciones, las dos por una razón concreta:

1. ALTURA DE LOS BLOQUES, medida al ancho real de la caja de texto (122 mm).
   Es el punto donde es fácil equivocarse: si se mide con el navegador en su
   ancho normal (1280 px), una ficha parece de 140 mm cuando en la hoja mide
   218 y se parte en dos. Aquí se abre la página con el viewport puesto en
   461 px = 122 mm, que es lo que de verdad va a haber en el papel.

2. APROVECHAMIENTO DE CADA HOJA, sobre el PDF ya impreso. Busca dónde llega
   la última tinta oscura dentro de la caja de texto, así que detecta las
   páginas que quedaron casi vacías porque algo no cupo y saltó.
"""

import glob
import os
import sys

import pypdfium2 as pdfium
from playwright.sync_api import sync_playwright

import build

ANCHO_MM = 122          # caja de texto: 148 de hoja - 13 y 13 de margen
ALTO_UTIL_MM = 178      # 210 de hoja - 15 de margen arriba - 17 abajo
ANCHO_PX = round(ANCHO_MM * 96 / 25.4)

BLOQUES = ".remedio, .dia, .ingrediente, .caja, .caja-alerta, .caja-suave, .tarjeta, .dos"


def medir_alturas():
    print(f"1) Altura de los bloques al ancho real de impresión "
          f"({ANCHO_MM} mm = {ANCHO_PX} px)\n")
    problemas = 0
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=build.chromium(),
                                 args=["--no-sandbox"])
        pg = nav.new_page(viewport={"width": ANCHO_PX, "height": 900})
        for nombre in build.ENTREGABLES:
            mod = __import__(f"contenido.{nombre}", fromlist=["x"])
            pg.set_content(build.pagina_html(mod.cuerpo({})), wait_until="load")
            pg.emulate_media(media="print")
            bloques = pg.evaluate("""(sel) => [...document.querySelectorAll(sel)].map(el => {
                const t = el.querySelector('h3, h4');
                return {t: (t ? t.innerText : el.innerText).split('\\n')[0].slice(0, 44),
                        h: +(el.getBoundingClientRect().height * 25.4 / 96).toFixed(0),
                        c: el.className.split(' ')[0]};
            })""", BLOQUES)
            grandes = sorted([b for b in bloques if b["h"] > ALTO_UTIL_MM],
                             key=lambda b: -b["h"])
            problemas += len(grandes)
            altos = [b["h"] for b in bloques] or [0]
            print(f"   {mod.META['archivo']:<34} {len(bloques):>3} bloques · "
                  f"máx {max(altos):>3}mm · {len(grandes)} no caben")
            for b in grandes[:8]:
                print(f"        {b['h']:>3}mm  .{b['c']}  {b['t']}")
        nav.close()
    return problemas


def ultima_tinta(pagina):
    im = pagina.render(scale=0.5).to_pil().convert("L")
    w, h = im.size
    px = im.load()
    x0, x1 = int(w * 0.12), int(w * 0.88)
    y0, y1 = int(h * 0.06), int(h * 0.92)
    ultima = y0
    for y in range(y0, y1):
        if any(px[x, y] < 205 for x in range(x0, x1, 3)):
            ultima = y
    return (ultima - y0) / (y1 - y0)


def medir_hojas():
    print("\n2) Aprovechamiento de cada hoja del PDF impreso\n")
    flojas_total = 0
    for f in sorted(glob.glob(str(build.SALIDA / "*.pdf"))):
        doc = pdfium.PdfDocument(f)
        flojas = [(i + 1, ultima_tinta(doc[i])) for i in range(len(doc))]
        flojas = [(n, o) for n, o in flojas if o < 0.45]
        flojas_total += len(flojas)
        print(f"   {os.path.basename(f):<34} {len(doc):>3} hojas · "
              f"{len(flojas):>2} por debajo del 45%")
        if flojas:
            print("        " + ", ".join(f"p{n} ({o:.0%})" for n, o in flojas[:20]))
    return flojas_total


if __name__ == "__main__":
    a = medir_alturas()
    b = medir_hojas()
    print(f"\nBloques que no caben: {a} · Hojas flojas: {b}")
    sys.exit(0)
