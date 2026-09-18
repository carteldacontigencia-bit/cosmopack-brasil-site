# Entregáveis — Azúcar en Equilibrio (Abuela Mei)

Os 4 PDFs do produto, gerados a partir de código. O texto fica separado do
layout: para mudar uma dose você edita um arquivo de conteúdo, não o HTML.

## O que tem em `out/`

| Arquivo | Páginas | O que é |
|---|---|---|
| `Azucar-en-Equilibrio.pdf` | 95 | Ebook principal — 55 remédios em 7 capítulos, cada um com dose, hora e advertência |
| `Bono-1-Reto-de-30-Dias.pdf` | 31 | Calendário dia 1 a 30, em 4 semanas, com revisão semanal |
| `Bono-2-Guia-del-Mercado.pdf` | 31 | Guia de compras: como reconhecer, preço justo em MXN, substitutos |
| `Bono-3-SOS-Antojo-de-Dulce.pdf` | 19 | Protocolo de 10 minutos + 12 resgates + cartão recortável |

## Order bumps (produtos separados, não incluídos na oferta principal)

| Arquivo | Páginas | O que é |
|---|---|---|
| `Recetario-del-Corazon.pdf` | 41 | 24 remédios para pressão e colesterol, em 4 capítulos |
| `Las-Noches-de-la-Abuela.pdf` | 29 | 18 remédios e gestos para dormir, em 3 capítulos |
| `Manos-y-Rodillas.pdf` | 29 | 18 remédios para dor articular, em 3 capítulos |

Os três seguem os mesmos critérios do livro principal e trazem cada um o
seu capítulo de triagem próprio, porque cada tema tem o seu risco:

- **Corazón** — a pressão alta não se sente. O capítulo de segurança abre
  com medir, não com tomar. Fora o orozuz (sobe a pressão, derruba o
  potássio) e fora a toranja de todas as receitas (choca com estatinas e
  amlodipino).
- **Noches** — levantar 3 vezes para urinar pode ser açúcar alto ou
  próstata, e ronco com pausas pode ser apneia. Os dois vão na triagem,
  antes de qualquer chá, senão o bônus entretém em vez de ajudar.
- **Manos** — articulação vermelha, quente e inchada de repente pode ser
  gota ou infecção, que se trata em horas. E a árnica nunca se toma:
  tem página própria.

Todos em espanhol do México, A5 (148×210 mm), corpo 12pt — tamanho escolhido
para leitura no celular sem zoom, que é o público de 45 a 70+ da página de
vendas. Cada PDF tem marcadores (índice lateral do leitor de PDF), metadados
e índice com números de página reais.

## Como regenerar

```bash
cd entregables
../.venv/bin/python build.py            # os quatro
../.venv/bin/python build.py ebook      # só um
../.venv/bin/python revisar.py          # controle de qualidade
```

Se o `.venv` não existir (container novo):

```bash
python3 -m venv .venv
.venv/bin/pip install playwright pypdf pypdfium2 pillow
```

O Chromium já vem na imagem; o `build.py` acha sozinho.

## Onde mexer

| Quero mudar | Arquivo |
|---|---|
| Um remédio (dose, hora, advertência) | `contenido/remedios.py` |
| Carta, capítulo de segurança, índices | `contenido/ebook.py` |
| Um dia do desafio | `contenido/bono1_reto30.py` |
| Preços do mercado | `contenido/bono2_mercado.py` |
| Protocolo do antojo | `contenido/bono3_sos.py` |
| Cores, fontes, tamanhos | `css/print.css` |
| Capa, ficha, caixas (o HTML) | `libro.py` |

## Duas coisas que não são óbvias

**Por que o build imprime duas vezes.** O Chromium não suporta as caixas de
margem do CSS (`@bottom-center`), então não dá para numerar o índice
diretamente. Cada capítulo e cada ficha escreve um token invisível na página.
A primeira impressão serve para o `pypdf` ler em que página caiu cada token;
a segunda já sai com o índice numerado de verdade. Os marcadores do PDF saem
do mesmo mapa.

**Por que medir na largura certa importa.** Ao medir a altura dos blocos com
o navegador na largura normal (1280px), uma ficha parecia ter 140mm quando no
papel tinha 218mm — e estourava para uma segunda página, desperdiçando uma
folha por remédio. O `revisar.py` mede com o viewport em 461px (= 122mm, a
caixa de texto real). Rode-o sempre depois de mexer no CSS.

## Sobre o conteúdo de saúde

O material é de cuidado caseiro tradicional e está escrito para **acompanhar**
o tratamento, nunca substituir. Isso não é só o aviso legal do rodapé — está
na estrutura:

- O capítulo de segurança vem **antes** dos remédios, não no fim.
- Toda planta com efeito hipoglicemiante avisa, na própria ficha, que **soma**
  ao efeito da metformina, das sulfonilureias e da insulina.
- Tem tabela de interações por medicamento, sinais de hipoglicemia com a regra
  15/15, e a lista de sinais que pedem médico e não chá.
- Os banhos de pé são todos **mornos e curtos**, com aviso de não usar se
  houver ferida — pé com neuropatia queima sem avisar.
- As mistelas são **sem álcool e sem açúcar**, e o livro explica por quê:
  álcool com glibenclamida ou insulina pode causar hipoglicemia noturna.
- O Bono 3 abre separando **antojo de hipoglicemia real**, porque os sintomas
  se parecem e o tratamento é o oposto.
- Ficaram de fora arruda, absinto, raiz de tejocote e outras de toxicidade
  conhecida, por tradicionais que sejam.

Se for publicar, vale uma revisão por profissional de saúde local antes —
sobretudo nas doses e nas interações.
