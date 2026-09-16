#!/usr/bin/env python3
"""
Monta o HTML traduzido (pt-BR) reinserindo as imagens.

Uso:
    python3 montar.py original.html            -> gera index-pt.html com as imagens originais
    python3 montar.py --placeholders           -> gera index-pt.html com imagens cinza (preview)

O template 'template-pt.html' contem 14 marcadores __IMG_0__ .. __IMG_13__,
na mesma ordem em que as imagens aparecem no arquivo original
(7 slides do carrossel + 7 miniaturas).
"""
import base64
import re
import sys
from pathlib import Path

AQUI = Path(__file__).parent
TEMPLATE = AQUI / "template-pt.html"
SAIDA = AQUI / "index-pt.html"
TOTAL = 14

LEGENDAS = [
    "1", "2", "3", "4", "5", "6", "7",
    "1", "2", "3", "4", "5", "6", "7",
]


def placeholder(rotulo: str) -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">'
        '<rect width="600" height="600" fill="#e6e6ea"/>'
        '<text x="300" y="300" font-family="Helvetica,Arial" font-size="40" '
        'fill="#8a8a94" text-anchor="middle" dominant-baseline="middle">'
        f'imagem {rotulo}</text></svg>'
    )
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + b64


def extrair(origem: Path) -> list:
    html = origem.read_text(encoding="utf-8", errors="replace")
    uris = re.findall(r'src="(data:image/[^"]+)"', html)
    if len(uris) != TOTAL:
        sys.exit(
            f"ERRO: encontrei {len(uris)} imagens em {origem.name}, "
            f"mas o template espera {TOTAL}."
        )
    return uris


def main() -> None:
    args = sys.argv[1:]
    if args and args[0] == "--placeholders":
        uris = [placeholder(r) for r in LEGENDAS]
        origem = "placeholders"
    elif args:
        uris = extrair(Path(args[0]))
        origem = args[0]
    else:
        sys.exit(__doc__)

    html = TEMPLATE.read_text(encoding="utf-8")
    for i, uri in enumerate(uris):
        marcador = f"__IMG_{i}__"
        if marcador not in html:
            sys.exit(f"ERRO: marcador {marcador} nao encontrado no template.")
        html = html.replace(marcador, uri)

    restantes = re.findall(r"__IMG_\d+__", html)
    if restantes:
        sys.exit(f"ERRO: marcadores nao substituidos: {restantes}")

    SAIDA.write_text(html, encoding="utf-8")
    print(f"OK -> {SAIDA}  ({SAIDA.stat().st_size/1024:.0f} KB, imagens: {origem})")


if __name__ == "__main__":
    main()
