# Design System — Pet Finder

## 1. Identidade e princípios

- **Nome:** Pet Finder.
- **Personalidade:** acolhedora e amigável.
- **Objetivo visual:** transmitir confiança, cuidado e proximidade durante o processo de adoção responsável.
- **Tecnologia:** interface implementada exclusivamente com Reflex, usando os componentes e estados existentes no projeto.
- **Tipografia:** manter a família de sistema herdada do Reflex/Radix; não introduzir fontes externas sem decisão arquitetural.
- **Arredondamento:** moderado. Os raios variam por componente e devem continuar diferentes quando o uso atual justificar.
- **Abrangência:** aplica-se a todas as telas novas e às telas existentes sempre que forem modificadas.
- **Fonte dos valores:** a tela de login em `Pet_Finder/Pet_Finder.py`. Este documento registra usos observados; os nomes semânticos são documentação e ainda não são constantes exportadas pelo código.

## 2. Paleta de cores

Os valores HEX/RGBA abaixo foram conferidos no código. Os nomes à esquerda formalizam semanticamente os usos aprovados; ainda não existem como tokens centralizados em Python ou CSS.

| Token semântico documentado | Valor exato | Finalidade observada | Origem | Situação |
|---|---|---|---|---|
| `primary` | `#7C3AED` | Ícones, checkbox, links, borda de foco e início do gradiente do botão principal. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L78), [linha 229](../Pet_Finder/Pet_Finder.py#L229), [linha 264](../Pet_Finder/Pet_Finder.py#L264) | Valor observado; função semântica aprovada |
| `primary-hover` | `#6D28D9` | Início do gradiente de hover do botão Entrar. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L270) | Valor observado; função semântica aprovada |
| `primary-strong` | `#5B21B6` | Fim do gradiente principal, badge, controle de senha e mensagens informativas. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L66), [linha 213](../Pet_Finder/Pet_Finder.py#L213), [linha 251](../Pet_Finder/Pet_Finder.py#L251) | Valor observado; função semântica aprovada |
| `primary-deep` | `#4C1D95` | Nome Pet Finder e fim do gradiente de hover. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L54), [linha 270](../Pet_Finder/Pet_Finder.py#L270) | Valor observado; função semântica aprovada |
| `lilac-soft` | `#EDE9FE` | Fim do gradiente do símbolo da marca. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L49) | Valor observado; função semântica aprovada |
| `lilac-surface` | `#F5F3FF` | Fundo do botão mostrar/ocultar senha, avisos informativos e trecho do fundo geral. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L212), [linha 252](../Pet_Finder/Pet_Finder.py#L252), [linha 384](../Pet_Finder/Pet_Finder.py#L384) | Valor observado; função semântica aprovada |
| `background-soft` | `#F8F7FC` | Fundo dos slots de ícone e início do gradiente da página. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L84), [linha 384](../Pet_Finder/Pet_Finder.py#L384) | Valor observado; função semântica aprovada |
| `background-cool` | `#EEF2FF` | Fim do gradiente geral da página. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L384) | Valor observado; função semântica aprovada |
| `text-primary` | `#1F2937` | Título principal, texto digitado e texto dos cadastros visuais. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L58), [linha 101](../Pet_Finder/Pet_Finder.py#L101), [linha 288](../Pet_Finder/Pet_Finder.py#L288) | Valor observado; função semântica aprovada |
| `text-label` | `#374151` | Rótulos E-mail/Senha e texto da checkbox. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L75), [linha 231](../Pet_Finder/Pet_Finder.py#L231) | Valor observado; função semântica aprovada |
| `text-secondary` | `#6B7280` | Texto de apresentação, placeholder e convite de cadastro. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L61), [linha 111](../Pet_Finder/Pet_Finder.py#L111), [linha 282](../Pet_Finder/Pet_Finder.py#L282) | Valor observado; função semântica aprovada |
| `surface` | `#FFFFFF` / `#ffffff` | Fundo dos campos, painel branco, cadastros e texto branco do botão/painel roxo. Varia apenas a capitalização no código. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L98), [linha 325](../Pet_Finder/Pet_Finder.py#L325), [linha 265](../Pet_Finder/Pet_Finder.py#L265) | Valor observado; função semântica aprovada |
| `border-default` | `#D1D5DB` | Borda dos slots e campos de texto, com espessura de 1 px. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L81), [linha 99](../Pet_Finder/Pet_Finder.py#L99) | Valor observado; função semântica aprovada |
| `border-subtle` | `#E5E7EB` | Borda dos controles visuais de cadastro. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L290) | Valor observado; função semântica aprovada |
| `focus-ring` | Borda `#7C3AED`; anel `rgba(124, 58, 237, 0.5)` | Foco do campo: contorno de 2 px, offset de 2 px. O botão usa um anel distinto `rgba(124, 58, 237, 0.2)`, 3 px, offset de 2 px. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L106), [linha 107](../Pet_Finder/Pet_Finder.py#L107), [linha 271](../Pet_Finder/Pet_Finder.py#L271) | Valores observados; os dois estados permanecem distintos |
| `feedback-error` | Texto `#B91C1C`; fundo `#FEF2F2`; borda `#FECACA` | Caixa de validação de erro. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L240), [linha 241](../Pet_Finder/Pet_Finder.py#L241), [linha 242](../Pet_Finder/Pet_Finder.py#L242) | Valores observados; conjunto formalizado |
| `feedback-info` | Texto `#5B21B6`; fundo `#F5F3FF`; borda `#DDD6FE` | Caixa de informação. | [Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L251), [linha 252](../Pet_Finder/Pet_Finder.py#L252), [linha 253](../Pet_Finder/Pet_Finder.py#L253) | Valores observados; conjunto formalizado |

### 2.1. Gradientes, transparências e sombras

Os valores transparentes são mantidos como RGBA; não devem ser convertidos em HEX opaco:

- Símbolo da marca: `linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L49).
- Badge: `rgba(124, 58, 237, 0.08)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L70).
- Botão principal: `linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%)`; hover `linear-gradient(135deg, #6D28D9 0%, #4C1D95 100%)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L264), [linha 270](../Pet_Finder/Pet_Finder.py#L270).
- Fundo da página: radial `rgba(196,181,253,0.45)` sobre `linear-gradient(135deg, #F8F7FC 0%, #F5F3FF 35%, #EEF2FF 100%)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L384).
- Painel roxo: overlay `rgba(79, 70, 229, 0.82)`, `rgba(91, 33, 182, 0.8)` e `rgba(124, 58, 237, 0.75)` sobre a foto externa; texto auxiliar branco a `0.82` de opacidade — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L332), [linha 335](../Pet_Finder/Pet_Finder.py#L335), [linha 366](../Pet_Finder/Pet_Finder.py#L366).
- Sombras: botão `0 12px 30px rgba(124, 58, 237, 0.22)`; painel branco `0 24px 50px rgba(91, 33, 182, 0.12)`; painel roxo `0 24px 50px rgba(91, 33, 182, 0.2)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L268), [linha 328](../Pet_Finder/Pet_Finder.py#L328), [linha 374](../Pet_Finder/Pet_Finder.py#L374).
- Borda do painel branco: `rgba(124, 58, 237, 0.08)` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L326).

## 3. Tipografia

### 3.1. Família e origem

O projeto não declara `font_family` nem inclui arquivos de fonte. Os componentes Radix renderizados no navegador usam o stack herdado `-apple-system, BlinkMacSystemFont, "Segoe UI (Custom)", Roboto, "Helvetica Neue", "Open Sans (Custom)", system-ui, sans-serif`, seguido de famílias de emoji. O `body` também usa o fallback `ui-sans-serif, system-ui, sans-serif`. A lista efetiva varia conforme navegador e plataforma; não é uma fonte própria do Pet Finder.

### 3.2. Escala observada

| Elemento | Declarado no código | Medida observada no navegador |
|---|---|---|
| Título da área de login | Radix `size="7"`, `line_height="1.15"`, peso 700 | 28 px; linha 32,2 px |
| Título do painel roxo | Radix `size="6"`, peso 700 | 24 px; linha 30 px |
| Texto introdutório | `1rem`, peso padrão 400 | 16 px; linha 24 px |
| Nome Pet Finder | `1.15rem`, peso 700 | 18,4 px pela raiz de 16 px |
| Emoji/símbolo da marca | `1.7rem` | 27,2 px pela raiz de 16 px |
| Rótulos de campo | `0.9rem`, peso 600 | 14,4 px; linha 21,6 px |
| Badge | `0.8rem`, peso 600 | 12,8 px; linha 19,2 px |
| Convite de cadastro | `0.95rem`, peso 400 | 15,2 px; linha 22,8 px |
| Mensagem de erro/informação | `0.9rem`/500 e `0.85rem`/500 | 14,4 px e 13,6 px; linha herdada do tema |
| Botão Entrar | peso 700; tamanho não definido | 14 px; linha 20 px herdada do Radix |
| Links | peso 600; tamanho não definido | 16 px; linha 24 px herdada do Radix |

Os valores em `rem`, pesos e presets de heading são declarados na tela; conversões em pixels e linhas não explicitamente definidas são resultado observado do tema/ambiente atual. Para novas telas, manter o stack de sistema e reutilizar os presets Radix e tamanhos documentados, sem introduzir uma fonte externa.

## 4. Dimensões, formas e espaçamentos

| Propriedade | Valores observados | Origem/observação |
|---|---|---|
| Layout geral | máximo `1180px`; painéis com máximo `560px`; largura responsiva `100%`, `100%`, `43%` | `rx.flex` com `wrap="wrap"`, `align="stretch"` — [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L376) |
| Altura mínima da página | `100vh` | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L385) |
| Campo e slot de ícone | `3.15rem` (50,4 px em raiz 16 px) | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L79) |
| Botão principal | `3.2rem` (51,2 px em raiz 16 px) | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L263) |
| Botão mostrar/ocultar | mínimo `2.8rem`; posicionado no wrapper em `right="0.35rem"`, `top="50%"`, `translateY(-50%)` | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L207) |
| Raios | `0.8rem` avisos/cadastros; `0.85rem` campos e toggle; `0.9rem` botão e símbolo; `1.8rem` painel branco; `2rem` painel roxo; `999px` badge | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L47), [linha 69](../Pet_Finder/Pet_Finder.py#L69), [linha 94](../Pet_Finder/Pet_Finder.py#L94), [linha 267](../Pet_Finder/Pet_Finder.py#L267), [linha 327](../Pet_Finder/Pet_Finder.py#L327), [linha 369](../Pet_Finder/Pet_Finder.py#L369) |
| Borda | campos `1px solid #D1D5DB`; cadastros `1px solid #E5E7EB`; painel branco `1px solid rgba(124, 58, 237, 0.08)` | A borda dos campos é visualmente compartilhada entre o slot do ícone e o input. |
| Paddings | página x `[1rem, 2rem, 4rem]`, y `[1.5rem, 2rem, 3rem]`; painel branco x `[1.1rem, 1.4rem, 2.2rem]`, y `[1.5rem, 2rem, 2.4rem]`; painel roxo `[1.3rem, 1.7rem, 2.3rem]` | Arrays são valores responsivos; [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L323), [linha 370](../Pet_Finder/Pet_Finder.py#L370), [linha 386](../Pet_Finder/Pet_Finder.py#L386) |
| Outros paddings explícitos | badge x `0.9rem`, y `0.45rem`; slot do ícone x `0.9rem`; input esquerdo `1rem`; senha direita `3.75rem`; avisos `0.8rem 0.9rem`; cadastro `0.85rem 1rem` | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L67), [linha 80](../Pet_Finder/Pet_Finder.py#L80), [linha 103](../Pet_Finder/Pet_Finder.py#L103), [linha 155](../Pet_Finder/Pet_Finder.py#L155), [linha 244](../Pet_Finder/Pet_Finder.py#L244), [linha 289](../Pet_Finder/Pet_Finder.py#L289) |
| Gaps | tokens Radix `spacing="0", "2", "3", "4", "5"`; checkbox usa o default Radix `spacing="2"` | São tokens da biblioteca, não uma escala local de pixels. |
| Contorno de foco | campo: 2 px, offset 2 px; botão: 3 px, offset 2 px | [Pet_Finder/Pet_Finder.py](../Pet_Finder/Pet_Finder.py#L104), [linha 271](../Pet_Finder/Pet_Finder.py#L271) |
| Sombras | `0 12px 30px`, `0 24px 50px` com RGBA roxos documentados acima | Suaves; aplicadas ao CTA e aos dois painéis. |

## 5. Padrões dos componentes

### Campos de texto

Fundo branco, texto `#1F2937`, placeholder `#6B7280`, borda de 1 px `#D1D5DB`, raios laterais de `0.85rem`, padding esquerdo `1rem` e altura `3.15rem`. O foco troca a borda para roxo e mostra anel de 2 px. O ícone fica num slot lilás à esquerda; os dois inputs compartilham altura e alinhamento.

### Campo de senha e visibilidade

O campo mantém os estilos do input padrão. O botão do olho usa variante Radix `soft`, fundo `#F5F3FF`, ícone de 16 px e fica alinhado verticalmente dentro do wrapper. `LoginState.show_password` alterna `password`/`text`. Não há estados de erro ou desabilitado específicos do campo além do comportamento padrão da biblioteca.

### Botão principal

Gradiente roxo `#7C3AED` → `#5B21B6`, texto branco, peso 700, altura `3.2rem`, raio `0.9rem` e sombra `0 12px 30px rgba(124, 58, 237, 0.22)`. Hover e foco explícitos estão registrados acima. A propriedade `disabled` está ligada a `is_loading`; não há cor/estilo disabled próprio documentado.

### Checkbox e rótulo

Checkbox Radix de tamanho `2`, cor de seleção `#7C3AED`, rótulo clicável junto ao controle e cor `#374151`. O valor inicial do estado é marcado. Não há estilo disabled explícito.

### Links e ícones

Links usam roxo `#7C3AED` e peso 600. Os links de recuperação/cadastro têm `href="#"` e permanecem placeholders; não constituem rotas. Ícones de campo têm 18 px e roxo; olho tem 16 px e cinza `#6B7280`; benefícios do painel usam emoji decorativos. Hover/foco de links e nomes acessíveis específicos para botões apenas com ícone não estão definidos localmente.

### Cards, painéis e mensagens

Painel branco: fundo `#FFFFFF`, raio `1.8rem`, borda translúcida roxa e sombra `0 24px 50px rgba(91, 33, 182, 0.12)`. Painel ilustrativo: raio `2rem`, foto externa com overlay roxo e sombra `0 24px 50px rgba(91, 33, 182, 0.2)`. Avisos de erro e informação usam raios `0.8rem`, paddings `0.8rem 0.9rem` e as cores semânticas indicadas na paleta.

## 6. Responsividade

### Regras explícitas

- `rx.flex` usa direção em linha, `wrap="wrap"` e `align="stretch"`; os painéis ficam lado a lado quando o espaço permite e empilham no mobile.
- A largura de cada painel é `100%`, `100%`, `43%` nos três primeiros níveis responsivos do array.
- Os paddings da página e dos painéis usam arrays responsivos; não há media queries próprias nem `set_breakpoints()` no projeto.

### Breakpoints herdados do Reflex

A instalação atual define os nomes e limites padrão em `reflex_base.breakpoints`: `xs=30em`, `sm=48em`, `md=62em`, `lg=80em`, `xl=96em`; o nível `initial` começa em `0px`. Não há overrides no projeto. Valores em `em` são mantidos como fornecidos pela biblioteca; conversões para px dependem do tamanho de fonte raiz.

### Comportamento observado

Nos tamanhos observados no navegador, o layout ficou empilhado em viewport mobile de `375px` e em duas colunas no desktop de `1440px`; em `375px` não houve rolagem horizontal. O limiar efetivo entre layouts não foi medido isoladamente. Alturas variam com conteúdo e mensagens, não são alturas fixas do Design System.

## 7. Acessibilidade e consistência

- Campos têm rótulos visíveis; a checkbox usa um elemento label que associa o texto clicável ao controle.
- Os inputs têm texto escuro, placeholder definido e foco roxo visível; o botão principal também tem foco explícito.
- Os controles mantêm foco/seleção pelos componentes Reflex/Radix. O projeto não define uma meta numérica WCAG nem registra cálculo de contraste; não se declara conformidade global sem essa verificação.
- Pendente: estilo disabled explícito; foco visual local para checkbox/links; nome acessível explícito para o botão do olho; relação semântica/estado ao anunciar mensagens; decisão de acessibilidade para imagem definida como background.
- Não introduzir novas cores ou estados para cobrir essas pendências sem decisão e verificação.

## 8. Regras para novos desenvolvimentos

1. Consultar este documento antes de criar qualquer tela.
2. Aplicar os mesmos padrões a telas existentes sempre que forem modificadas.
3. Reutilizar os tokens semânticos documentados; não inventar cores, fontes, raios ou espaçamentos quando já houver equivalente.
4. Se um padrão visual oficial mudar, atualizar este documento na mesma mudança.
5. Manter a interface em Reflex e usar seus componentes/estados; não adicionar outra tecnologia de frontend sem aprovação arquitetural.
6. Esta versão documenta tokens, mas não os centraliza em código. Um módulo Python compartilhado pertence a uma mudança futura separada.
7. A imagem do pug usa uma URL externa no protótipo; reavaliar hospedagem/localização e disponibilidade antes da preparação para produção.
