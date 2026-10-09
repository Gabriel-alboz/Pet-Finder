# Design

## Context

Consulte `proposal.md` para a motivação. A tela de login e seus valores visuais estão concentrados em `Pet_Finder/Pet_Finder.py`; `rxconfig.py` habilita Tailwind v4 e Radix Themes, e `requirements.txt` fixa Reflex 0.9.12. Não há módulo de tokens nem arquivos CSS do projeto.

O contexto permanente do OpenSpec era ignorado por erro de indentação em `openspec/config.yaml`. O bloco foi preservado como string YAML válida, agora inclui a referência ao Design System e foi reconhecido pelo CLI 1.13.2 tanto em `openspec context` quanto em `openspec instructions proposal`.

## Goals / Non-Goals

**Goals:**

- Criar uma fonte de referência em português com valores rastreáveis ao código, separando estilos explícitos dos herdados de Reflex/Radix.
- Fazer com que agentes consultem o documento ao planejar mudanças de interface e ao implementar telas.
- Registrar como pendentes os estados ou requisitos não definidos na implementação atual.

**Non-Goals:**

- Alterar a tela de login, os estilos, componentes, rotas ou comportamentos existentes.
- Criar tokens executáveis, módulo Python de tema, componentes compartilhados ou CSS global.
- Alterar Xano, dados, dependências, templates globais, skills geradas ou configurações do usuário.

## Decisions

### Documentar os valores antes de centralizá-los no código

`docs/design-system.md` registra nomes semânticos e os valores observados em `Pet_Finder/Pet_Finder.py`, incluindo origens por linha. Isso torna explícito que os nomes são uma referência documental nesta etapa, não constantes importáveis. Uma futura mudança de centralização poderá migrar um ou mais estilos, com revisão própria e sem refatorar toda a tela agora.

Alternativa considerada: criar imediatamente um módulo de tema ou substituir estilos inline. Rejeitada porque a instrução atual limita o escopo a documentação/configuração e a interface já funciona.

### Usar dois pontos de entrada para as instruções

`AGENTS.md` recebe uma regra breve para o trabalho do agente no projeto. `openspec/config.yaml` mantém o contexto arquitetural e aponta para `docs/design-system.md` para mudanças de interface; o CLI confirmou esse contexto no payload de instruções de artefato. `CLAUDE.md` continua apontando para `AGENTS.md` e não precisa duplicar conteúdo.

Alternativas consideradas: copiar todo o Design System para instruções, ou editar comandos OPSX/skills geradas. Rejeitadas para evitar duplicação e alterações em arquivos gerenciados. `openspec update` não será executado nesta mudança.

### Tratar a mudança como documental

O change usa `schema: spec-driven` e `skip_specs: true`. O CLI marcou `specs` como `skipped`; não há requisitos de comportamento a inventar. `proposal.md`, `design.md` e `tasks.md` documentam objetivo, abordagem e verificações.

### Registrar estados não definidos, sem preencher lacunas com escolhas novas

O documento diferencia padrões presentes de pendências como cores de disabled, política numérica de contraste, foco local de links/checkbox, nome acessível do botão de olho e armazenamento futuro da imagem externa. Nenhum valor novo será introduzido para completar essas categorias.

## Risks / Trade-offs

- [Os estilos inline podem divergir do documento ao longo do tempo] → `AGENTS.md` e o contexto OpenSpec exigem consultar e atualizar o documento quando uma regra oficial mudar.
- [Valores Radix podem depender da versão/plataforma] → Registrar a versão verificada e separar tokens explícitos do projeto de valores herdados.
- [A imagem depende de um host externo] → Preservar a escolha do protótipo e reavaliar disponibilidade/hospedagem antes da produção.
- [A correção do contexto usa um scalar YAML quoted com quebras escapadas] → Validar o parser OpenSpec e o campo `context` de instruções, não apenas a aparência do arquivo.

## Migration Plan

1. Documentar os estilos atuais sem alterar o frontend.
2. Adicionar a referência curta em `AGENTS.md` e no contexto OpenSpec válido.
3. Validar YAML, resolução de contexto/schema/templates, diff e estado do Git.
4. Em outra mudança aprovada, avaliar centralização de tokens, acessibilidade pendente e imagem para produção.

## Open Questions

Nenhuma decisão necessária para este escopo. Os itens ainda sem implementação são identificados como pendências no Design System, sem impedir sua publicação documental.
