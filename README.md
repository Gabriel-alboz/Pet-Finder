# Pet Finder

Plataforma acadêmica de adoção responsável que aproxima **ADOTANTES** e **ONGs**. A visão do produto inclui pesquisa por filtros, quiz **opcional** de compatibilidade, comunicação privada e solicitações de adoção.

## Estado atual

- Cadastro ADOTANTE/ONG integrado ao Xano, com validações e orientação para login após sucesso.
- Login por e-mail/senha integrado a `auth/login` e `auth/me`, Home protegida e logout local implementados.
- O responsável informou teste manual bem-sucedido com conta existente e acesso à Home. Isso não comprova recarga, logout ou todos os cenários de proteção no navegador.
- Home responsiva com seções Início, ONGs, Pets, Quiz, Chats e Configurações. Catálogos, quiz, edição de perfil e Chats são **interfaces demonstrativas**, sem integração de dados dessas funcionalidades.
- Chats tem somente navegação e estado vazio, sem mensagens reais.
- Etapa 23.2: Configurações possui prévias específicas de ADOTANTE/ONG, somente leitura e sem salvamento. Apenas nome vem da sessão; consentimentos estão desligados e indisponíveis. [Detalhes e limites](docs/account-settings-preview.md).

Detalhes e evidências em [Estado do projeto](docs/project-status.md). Recursos futuros não devem ser apresentados como implementados.

## Tecnologias

Python, Reflex (0.9.12 fixado em `requirements.txt`), Xano, Git/GitHub e OpenSpec. O frontend é exclusivamente Reflex. Os perfis são `ADOTANTE` e `ONG`, identificados pelo `account_type` autenticado; `role` não substitui essa classificação.

Workspace Xano 151970, branch publicada `v1`, plano Free sem branch isolada disponível neste ambiente.

## Execução local — PowerShell

Requer Python compatível com o Reflex fixado, ambiente virtual e dependências de build do Reflex. O ambiente atual utiliza Python 3.14. Consulte as skills do projeto ao preparar um ambiente novo.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:XANO_API_BASE_URL = 'https://x8ki-letl-twmt.n7.xano.io/api:yFqRLsBC:v1'
.venv\Scripts\reflex.exe run --env prod --single-port 2>&1 | Tee-Object -FilePath (Join-Path $env:TEMP 'petfinder-reflex.log')
```

O comando de inicialização é `reflex run`; usamos modo prod local conforme as orientações do projeto. Leia a URL/porta no terminal e acesse `/login` ou `/`. `/register` é público; `/home` exige sessão válida. As seções da Home, inclusive Chats, não possuem rotas independentes. Para escolher portas disponíveis, consulte `reflex run --help`.

`XANO_API_BASE_URL` deve existir no **processo backend** Reflex, apontando ao grupo Authentication publicado via HTTPS. Essa URL é pública, não uma credencial. Não versionar senhas, tokens de usuários ou credenciais CLI/Meta API. A aplicação não precisa de credenciais administrativas para login/cadastro. Sem a variável, o login apresenta indisponibilidade de configuração.

Prod local não possui hot reload: reinicie após alterações. Não executar testes funcionais automaticamente contra live: até `auth/me` registra auditoria.

## Verificação offline

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\reflex.exe compile --dry
openspec validate --all --strict
git diff --check
```

Testes simulados e compilação não substituem inspeção visual ou validação integrada autorizada. Ver resultados em [Estado do projeto](docs/project-status.md).

## Limitações e evolução

A sessão é transitória no servidor Reflex, sem persistência confiável entre acessos, abas, reinícios ou workers. “Mantenha-me conectado” está desabilitado. Logout limpa a sessão local e **não revoga** o token Xano. Contas sem `account_type` válido não são classificadas automaticamente. Recuperação de senha não está integrada à interface.

São futuros: filtros, configurações de perfis, visibilidade consentida de adotantes para ONGs, gestão de pets, chat privado, quiz com dados reais e solicitações. Nenhum backend dessas funcionalidades foi criado nesta etapa.

## Documentação

- [Visão](docs/project-overview.md) e [modelo conceitual](docs/domain-model.md).
- [Estado e evidências](docs/project-status.md), [RF-01 a RF-10](docs/functional-requirements.md) e [roadmap](docs/roadmap.md).
- [Arquitetura](docs/architecture.md), [login e sessão](docs/login-integration.md), [contratos Xano](docs/xano-authentication-setup.md) e [dependências da Home](docs/home-backend-dependencies.md).
- [Design System](docs/design-system.md), [AGENTS](AGENTS.md) e [planejamento desta etapa](openspec/changes/consolidate-project-and-chat-preview/proposal.md).

Mudanças no Xano, publicações, alterações de dados e operações Git de publicação exigem autorização específica. Preservar trabalhos locais anteriores e separar planejamento de entregas verificadas.
