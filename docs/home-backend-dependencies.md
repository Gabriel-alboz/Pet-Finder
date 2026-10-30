# Home — navegação e dependências de backend

## Situação atual

A Home existente está em `Pet_Finder/home.py`, registrada como `/home` em `Pet_Finder/Pet_Finder.py`. `LoginState.require_auth` protege a entrada, `can_view_home` controla conteúdo e os eventos da navegação verificam a sessão no servidor. Não é uma rota pública.

Cadastro, login e consulta de identidade já usam Xano via serviço existente. **O catálogo da Home não está conectado.** Nome/tipo do rodapé vêm da sessão autenticada; isso não significa integração das listagens. Ver [arquitetura](architecture.md) e [evidências](project-status.md).

## Navegação e conteúdo

| Seção local | Implementação atual | Dependência futura |
|---|---|---|
| Início | Hero, atalhos para Pets/Quiz/ONGs, busca desabilitada e estados vazios | Catálogo, destaques e pesquisa reais |
| ONGs | Estado vazio e aviso de pesquisa por estado/cidade | RF-01: dados institucionais públicos, listagem e filtros autorizados |
| Pets | Estado vazio e texto de filtros futuros; quiz opcional | RF-02/08: animais, propriedade, disponibilidade e pesquisa combinada |
| Quiz | Estado demonstrativo, sem perguntas/regras/resultados | RF-09: critérios, preferências, catálogo e recomendações |
| Chats | Título, subtítulo, ícone e vazio, aviso de interface demonstrativa | RF-05/06: conversas, participantes, mensagens e autorização |
| Configurações | Prévia por tipo, campos somente leitura, consentimentos desligados, pets indisponíveis e logout local | RF-03/07 parciais: pendentes leitura detalhada, edição de campos permitidos e consentimento persistente |

`HomeState.active_section` seleciona conteúdo sem novas rotas. Menu desktop e mobile compartilham componentes, hover e seleção; navegação fecha o menu mobile. Não há rota independente `/chats`; acesso ocorre na Home protegida. Não existem conversas fictícias, filtros que aparentem funcionar ou ações de persistência nessas seções.

## Contratos ainda necessários

O catálogo físico/endpoints de pets, listagem pública de ONGs, consentimento para descoberta de adotantes, configurações, chat, quiz e solicitações precisam ser especificados e aprovados. Perfis JSON em `user` não comprovam a existência desses contratos. Não inventar nomes de tabelas nem endpoints.

Separar busca direta e quiz: nenhum usuário deve precisar responder quiz para pesquisar pets. A ONG gerenciará somente seus animais; adoção e mensagens precisam de autorização entre as partes. Ver [requisitos](functional-requirements.md) e [roadmap](roadmap.md).

## Validação e limites

Testes locais podem verificar seleção de Chats, fechamento mobile, bloqueio por sessão inválida e estrutura dos componentes sem acessar Xano. Compilar não comprova aparência em todos os viewports. Testes manuais autenticados, recarga/logout e catálogo real exigem evidências próprias e autorização antes de operações live.

Workspace 151970, v1, plano Free sem branch isolada disponível. A Etapa 21 não altera serviços, sessão, cadastro ou XanoScripts e não executa operações remotas.
