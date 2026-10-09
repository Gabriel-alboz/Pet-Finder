<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** � up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above � do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs � components, state management, events, styling, database, routing, authentication � use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available � always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

## Projeto

Este projeto é o Pet Finder, uma plataforma web para adoção responsável de animais.

O sistema possui dois grupos principais de usuários:
- pessoas interessadas em adotar animais;
- ONGs responsáveis pelos animais disponíveis para adoção.

As principais funcionalidades do projeto incluem:
- cadastro e acesso de usuários e ONGs;
- cadastro e gerenciamento de animais;
- busca e descoberta de animais;
- sistema de match entre usuários e animais;
- solicitações de adoção;
- gerenciamento de solicitações pelas ONGs.

## Frontend

O frontend do projeto deve ser implementado exclusivamente com Reflex.

Utilize os mecanismos próprios do Reflex para componentes,
estado, eventos, páginas e interação.

Não introduza outra tecnologia de frontend para substituir
ou complementar o Reflex, salvo quando houver uma alteração
arquitetural explicitamente aprovada.

## Design System do Pet Finder

Antes de criar telas ou alterar estilos de telas existentes, consulte `docs/design-system.md` e reutilize os padrões documentados. Não introduza cores, fontes, raios ou espaçamentos arbitrários quando já houver um padrão aplicável. Atualize o documento quando um padrão visual oficial mudar. A interface permanece exclusiva de Reflex.

## Desenvolvimento

O desenvolvimento deve seguir uma abordagem incremental.

Antes de implementar uma funcionalidade:
1. analisar o contexto do projeto;
2. utilizar o OpenSpec para organizar a mudança;
3. revisar a proposta e as especificações;
4. somente depois implementar a mudança.

Não implementar o sistema inteiro de uma só vez.

Preservar a separação entre:
- contexto e visão geral do projeto;
- modelo conceitual do domínio;
- especificações do sistema;
- mudanças em desenvolvimento;
- implementação física.

## Tecnologias

Frontend: Reflex.

Backend e persistência: Xano.

Especificação e organização das mudanças: OpenSpec.

## Segurança e integridade

Preservar a segurança da aplicação e a integridade dos dados.

Não expor credenciais, tokens ou informações sensíveis no código,
arquivos versionados ou documentação.

Qualquer alteração arquitetural deve ser explicitamente aprovada
antes de ser incorporada ao projeto.