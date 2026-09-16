# NORDHORN — página de produto em pt-BR

Tradução para português (Brasil) da página do kit de 3 cuecas boxer + Crocs grátis,
originalmente publicada em inglês.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `template-pt.html` | Página traduzida com marcadores `__IMG_0__` … `__IMG_13__` no lugar das imagens. |
| `montar.py` | Injeta as imagens no template e gera `index-pt.html`. |
| `index-pt.html` | Versão gerada. **No repositório está com placeholders cinza**, não com as fotos reais. |

As 14 imagens do original são data URIs em base64 (~600 KB) e não foram versionadas aqui.

## Como gerar a versão final

Coloque o HTML original (em inglês, com as imagens embutidas) nesta pasta e rode:

```bash
python3 montar.py index.html
```

O script extrai os 14 data URIs na ordem em que aparecem — 7 slides do carrossel e
7 miniaturas —, valida a quantidade e sobrescreve `index-pt.html`.

Para regenerar apenas a prévia com placeholders:

```bash
python3 montar.py --placeholders
```

## O que foi adaptado

- Todo o conteúdo visível, além de `lang`, `title`, `alt`, `aria-label` e as strings
  dentro do JavaScript.
- Preço em **R$ 97,90**; moeda nos termos como reais (BRL).
- Tamanhos de cueca em **P / M / G / GG**.
- Tamanhos do Crocs em numeração **BR**, com as colunas EU e comprimento do pé
  mantidas como referência do fabricante.
- Políticas reescritas para a legislação brasileira: CDC (arrependimento de 7 dias
  pelo art. 49, vício de produto durável em 90 dias pelo art. 26, soluções do art. 18),
  LGPD no lugar do GDPR britânico, Decreto 7.962/2013 e Marco Civil.

## Pendências antes de publicar

1. **E-mail de contato** — `contato@nordhorn.com.br` é um valor provisório, usado em 4
   lugares. Substituir pelo endereço real.
2. **Dados da empresa** — o Decreto 7.962/2013 (art. 2º, I) exige razão social, CNPJ e
   endereço físico visíveis no site. Há um comentário HTML marcando o local no modal
   de Contato.
3. **Prazo de entrega** — os 5–9 dias úteis vieram do texto original e precisam ser
   conferidos por região.
4. **Revisão jurídica** — o texto foi adaptado, não redigido por advogado.
