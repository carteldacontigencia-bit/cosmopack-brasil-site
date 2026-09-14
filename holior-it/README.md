# Holior IT — página de produto em italiano

Recriação completa da página `holior.com/products/wormwood-cc` traduzida para italiano,
mantendo cores, tipografia e estrutura do original.

## Sistema de design extraído do original

| Token | Valor | Onde aparece |
|---|---|---|
| Verde-lima | `#C9DE80` | CTAs, badges, títulos sobre fundo escuro, ticker |
| Azul-petróleo | `#071F2A` · `#0E1C25` · `#0D2F3A` | fundos escuros, header da tabela, FAQ |
| Borda teal | `#184D54` | bordas de cards e tabela comparativa |
| Fundos claros | `#F4F4F4` · `#F5F3EE` · `#F6F9EB` · `#E8EDEE` | seções alternadas |
| Vermelho | `#B30007` | ícones "X" na comparação |
| Texto | `#464646` · `#606060` · `#221E20` | corpo |

Fontes (as mesmas do original): **Baloo 2** para títulos (600/700), **Lato** para o corpo,
carregadas via Google Fonts. Montserrat fica como fallback do tema Dawn.

## Seções (na ordem do original)

1. Ticker rolante de claims
2. Produto principal — galeria, seletor de 3 formatos, ATC, selos, 4 abas
3. "Perché Fidarsi di Holior?" — selos de confiança
4. "Non Ignorare Questi Primi Sintomi" — 6 sintomas
5. "Perché Tutto Ciò che Hai Provato Ha Fallito" — 4 motivos
6. Carrossel de citações de mídia
7. "Perché Eliminare i Parassiti È Importante Oggi" — 3 cards
8. Comparação antes/depois em pills + vídeo
9. "Scopri Perché gli Esperti Scelgono Holior" — ciclo de vida
10. Ingredientes — 6 cards
11. Estatísticas 95 / 87 / 91 / 84%
12. Tabela comparativa + carrossel de avaliações
13. Garantia de 30 dias
14. FAQ — 8 perguntas
15. Rodapé + disclaimer

## Como usar na Shopify

**Opção rápida** — Loja online → Páginas → nova página → editor HTML (`<>`) → cole tudo
que está entre `<body>` e `</body>`, e o bloco `<style>` junto.

**Opção recomendada** — crie `sections/holior-it.liquid` no tema:
cole o `<style>` + o HTML do `<body>`, depois adicione um `{% schema %}` com os campos
que você quer editar pelo painel (títulos, preços, imagens).

### Antes de publicar

- **Imagens e vídeo** apontam para o CDN da holior.com. Faça upload dos seus próprios
  arquivos em Conteúdo → Arquivos e troque as URLs.
- **Preços** estão em EUR com formatação italiana (`29,99 €`). Ajuste conforme seu catálogo.
- O botão "Aggiungi al Carrello" é estático — conecte ao `/cart/add` ou ao form do produto.
- Os links do rodapé apontam para `/policies/*` — funcionam assim que as políticas
  existirem na sua loja.

### Sobre os claims

O texto é a tradução fiel do original americano, incluindo as alegações sobre parasitas.
Na Itália/UE, alegações de saúde em integratori alimentari são reguladas pelo
Reg. CE 1924/2006 e pela notifica ao Ministero della Salute — uma revisão jurídica antes
de publicar é recomendável. Há um disclaimer no rodapé, mas ele não substitui essa revisão.
