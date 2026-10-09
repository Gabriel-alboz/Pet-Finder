# Tasks

## 1. Documentar o Design System observado

- [x] 1.1 Criar `docs/design-system.md` com tokens semânticos derivados apenas dos valores verificados em `Pet_Finder/Pet_Finder.py`, incluindo origens por linha.
- [x] 1.2 Documentar tipografia herdada, dimensões, componentes, estados presentes e pendentes e regras responsivas, verificando Reflex/Radix e os breakpoints instalados.

## 2. Integrar as instruções dos agentes

- [x] 2.1 Corrigir o YAML do contexto existente sem remover conteúdo e incluir a referência ao Design System; verificar parsing e presença da referência em `openspec instructions`.
- [x] 2.2 Adicionar a regra curta em `AGENTS.md`, preservar o bloco gerenciado e confirmar que `CLAUDE.md` continua apontando para `AGENTS.md`.

## 3. Verificação final

- [x] 3.1 Executar `openspec --version`, `openspec context`, `openspec list --specs --json` e `openspec templates --schema spec-driven --json`; registrar schema, contexto e templates resolvidos.
- [x] 3.2 Executar validação OpenSpec e `git diff --check`; conferir arquivos criados/modificados e confirmar que UI, dependências, assets, Xano e alterações preexistentes não foram tocados.
