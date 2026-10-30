# Estado do projeto — Etapa 23.3.2 (somente local)

## Etapa 23.3.2 — consulta de perfil preparada somente localmente

Criado `xano/api/authentication/account/profile_GET.xs` com Bearer obrigatório, consulta por `$auth.id`, projeções por tipo, documentos mascarados e defaults para JSON legado. **Não publicado e não integrado ao Reflex.** Sem PATCH, alteração de schema ou escrita/auditoria. RF-03/RF-07 continuam parciais. [Contrato e limites](account-profile-read.md).

Nova conferência administrativa de user/Authentication e login/me/signup, sem registros ou execução de APIs da aplicação. Snapshot separado em `backups/xano-definitions/20261030T230124178457Z-account-profile`, com manifesto/IDs/horário/hashes; não é backup de registros nem exportação completa do grupo. Sintaxe XanoScript aprovada sem avisos; testes estáticos/offline e publicação futura possuem limites descritos no contrato.

Validação: **53 testes Python aprovados**, incluindo 11 verificações novas estáticas/aritméticas do contrato; sintaxe Python válida; XanoScript validado oficialmente com zero avisos; `reflex compile --dry` aprovado; seis mudanças OpenSpec aprovadas em modo estrito; `git diff --check` sem erros, com avisos LF/CRLF no Windows. Snapshot verificado por hashes. Os XanoScripts anteriores e todos os arquivos do frontend/autenticação/cadastro/serviços permaneceram idênticos ao início. Nenhum teste funcional live, publicação, commit, push ou deploy. Cabeçalhos HTTP efetivos, filtros em runtime, cache e políticas de histórico ainda dependem de revisão/teste controlado autorizado.

Atualização em 30/10/2026: Configurações possui prévias somente leitura para ADOTANTE e ONG, integradas à seção `account` da Home. Somente nome seguro da sessão é preenchido; e-mail e demais campos ficam vazios. Não há consulta detalhada, edição, salvamento, publicação de contato ou consentimento operacional. RF-03/RF-07 têm entrega visual parcial. Ver [limites e validação](account-settings-preview.md). O histórico da Etapa 21 abaixo permanece identificado como tal.

## Validação da Etapa 23.2

### Correção 23.2.1 — exibição do nome

O responsável relatou layout correto e nome ausente no teste visual. A inspeção offline confirmou nome em `LoginState`, serialização e `value` reativo; não há uso de `default_value`. Foi identificada regra Radix que aplica cor e WebkitTextFillColor ao input interno somente leitura, independentemente da cor do contêiner. A correção explicita essas propriedades somente no campo de nome, seguindo o tratamento do login e preservando o Design System. Não altera autenticação ou outros campos. A causa visual específica relatada não foi reproduzida em navegador; confirmar exibição após carregar a versão corrigida.

Validação desta correção: **42 testes offline aprovados** (três novos), incluindo nomes de ADOTANTE/ONG, atualização por revalidação simulada, ausência de sessão, expiração, tipo inválido, logout, vínculo reativo, somente leitura e proibição de HTTP real. `reflex compile --dry` aprovado; cinco mudanças OpenSpec válidas; `git diff --check` sem erros (somente avisos LF/CRLF). Alterações preexistentes preservadas; nenhuma consulta/alteração Xano, commit, push ou deploy.

### Resultado anterior da Etapa 23.2

- Sintaxe: quatro arquivos Python alterados/criados analisados com AST, sem erros.
- Testes offline: **39 aprovados**, incluindo oito testes novos de Configurações. Um teste antigo de avisos foi substituído pela cobertura dos blocos reais. HTTP simulado/proibido, sem testes live.
- `reflex compile --dry`: aprovado em Reflex 0.9.12.
- `openspec validate --all --strict`: cinco mudanças aprovadas, sem arquivamento.
- `git diff --check`: sem erros de whitespace; avisos LF/CRLF de normalização no Windows.
- Rotas, login, cadastro, estado de sessão, cliente Xano, dependências e XanoScripts sem alterações no diff.
- Responsividade validada estruturalmente por estilos gerados, sem inspeção visual de pixels. Roteiro desktop/tablet/mobile pendente em [Configurações](account-settings-preview.md).
- Sem consulta funcional ou alteração Xano, commit, push ou deploy.

## Histórico consolidado da Etapa 21

Referência consolidada em 24/10/2026, baseada no código e no histórico informado pelo responsável. Nenhuma consulta funcional ao Xano live nesta etapa. Ver [arquitetura](architecture.md), [requisitos](functional-requirements.md) e [roadmap](roadmap.md).

## Implementação e evidências

| Módulo | Implementação observada | Evidência e limite |
|---|---|---|
| Login | Formulário, e-mail/senha, POST login, GET me, erros seguros, redirecionamento | Testes offline com mocks. **Teste manual informado pelo responsável:** conta existente autenticou e acessou a Home. Não é teste executado pelo agente |
| Sessão/proteção | Estado privado servidor, validade local, guarda `/home`, bloqueio de eventos, logout local | Testes offline; recarga, logout, acesso direto e expiração no navegador não estão integralmente validados manualmente |
| Cadastro ADOTANTE/ONG | Formulários/validações, POST signup, aviso para login | Cadastros bem-sucedidos foram informados no histórico pelo responsável. Nenhum usuário criado nesta etapa; sem nova prova ponta a ponta nem suíte dedicada completa de cadastro |
| Home | Layout responsivo, menu comum desktop/mobile, nome/tipo e sair | Componentes preservados; compilação/testes estruturais não substituem inspeção visual autenticada |
| Chats | Item selecionável, seção vazia e aviso demonstrativo | Somente interface e navegação local, sem backend, mensagens ou histórico |
| ONGs/Pets | Seções vazias e avisos de futura pesquisa | Sem listagens/filtros reais ou resultados fictícios |
| Quiz | Seção demonstrativa e acesso pelo banner | Sem perguntas, algoritmo, resultados ou persistência; será opcional |
| Configurações | Prévia somente leitura por tipo autenticado, blocos de dados, descrição, segurança e preferências/privacidade ou pets | Etapa 23.2: sem leitura detalhada Xano, edição, salvamento ou consentimento; somente nome da sessão |
| Auditoria Xano | Cópias locais com metadados restritos e leitura histórica protegida | Seis publicações e validação estrutural informadas como concluídas na Etapa 17; não reexecutadas aqui |

## Login: concluído e parcial

O cliente usa `authToken` apenas no servidor para buscar identidade e validar `user_id`/`account_type`. Tipos aceitos: ADOTANTE/ONG; `role` não define perfil. Credenciais inválidas, respostas inesperadas, conta não classificada, limite e indisponibilidade recebem mensagens controladas. Home existente é o destino após sucesso.

“Mantenha-me conectado” está desabilitado e desmarcado. Não existe sessão durável entre acessos, abas, workers ou reinícios. Reload pode funcionar se o estado for conservado e revalidado, sem garantia. Logout é local, sem revogar o token Xano. “Esqueceu sua senha?” ainda não possui fluxo operacional no frontend.

O teste manual informado comprova somente o cenário relatado: autenticação e chegada à Home. Não generalizar para logout, proteção de todas as rotas ou reconexão.

## Cadastro

Dados comuns: nome, e-mail, senha/confirmação, telefone e endereço (endereço, cidade, UF). ADOTANTE acrescenta CPF e nascimento; ONG acrescenta CNPJ e descrição institucional. Campos específicos compõem os perfis correspondentes no contrato Xano. Há validações locais de obrigatoriedade, e-mail, dígitos verificadores CPF/CNPJ, telefone, UF, data, senha e confirmação.

Após sucesso, informa a necessidade de login e limpa senhas; não autentica automaticamente. Erros de duplicidade não revelam qual conta existe. O backend é a autoridade das validações. Pendências: consistência de política de senha (local admite letras acentuadas; backend exige letra ASCII), privacidade dos estados de cadastro e unicidade de documentos sob concorrência. Nenhuma alteração nesses fluxos nesta etapa.

## Limitações

- Apenas cadastro e identidade/sessão têm integração frontend com Xano; os demais módulos são demonstrações ou planejamento.
- Até `auth/me` grava auditoria: consulta funcional não é teste sem efeitos remotos.
- Contas antigas sem classificação válida precisam de tratamento administrativo autorizado, sem inferir ADOTANTE/ONG.
- URL base é pública; runtime não requer credenciais administrativas. Não versionar segredos.
- Plano Free sem branches isoladas no ambiente atual: novas mudanças exigem autorização, backup, verificação de concorrência e reversão analisada.
- Não há chat real, notificações, gestão de pets, filtros operacionais ou solicitações.
- Alterações locais herdadas foram preservadas; o diff global não representa apenas a Etapa 21.

## Validação da Etapa 21

- Sintaxe Python: aprovada nos dois arquivos Python desta etapa.
- Testes offline: **32 aprovados** (24 anteriores e 8 novos), sem acesso ao live.
- `reflex compile --dry`: aprovado na versão instalada.
- OpenSpec: **4 mudanças aprovadas** em `validate --all --strict`; nenhum arquivamento.
- `git diff --check`: o diff global ainda acusa whitespace preexistente em XanoScripts, com saída idêntica ao inventário inicial. Não foi corrigido porque `.xs` está fora do escopo. Verificação dos arquivos alterados nesta etapa sem novos erros.
- Comparação de hashes com o início: login, cadastro, autenticação, serviço Xano, `.gitignore`, testes anteriores e todos os XanoScripts preservados.

Navegação foi validada com estados locais dos dois perfis e sessões inválidas; UI por árvore de componentes/compilação, sem inspeção visual de pixels no navegador. O servidor prod eventualmente já aberto precisa ser reiniciado para carregar os arquivos novos; não foi reiniciado nem houve deploy nesta etapa.

Teste manual posterior: observar desktop/mobile; abrir Chats e voltar; conferir seleção/hover; recarregar `/home`; acesso anônimo direto; logout. Não executar automaticamente contra live. Usar conta existente com autorização, sem registrar credenciais.

## Prioridades

Finalizar matriz manual de autenticação e decidir infraestrutura de sessão persistente. Depois, integrar configurações, gestão de pets e pesquisa com contratos aprovados; chat, quiz real e solicitações seguem o [roadmap](roadmap.md). RF-01 a RF-10 dependem de integração futura; RF-06 e, após a Etapa 23.2, RF-03/RF-07 têm apenas entrega visual parcial.
