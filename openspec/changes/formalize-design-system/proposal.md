# Proposal

## Why

Os estilos atuais do Pet Finder estão definidos diretamente na tela de login e ainda não há uma referência única para guiar novas telas. Formalizar os valores já existentes e torná-los consultáveis por agentes reduz divergências sem alterar o comportamento ou o visual atual.

## What Changes

- Documentar a identidade, paleta, tipografia herdada, dimensões, componentes e responsividade observados na interface atual em `docs/design-system.md`.
- Referenciar o documento nas instruções compartilhadas de `AGENTS.md` e no contexto OpenSpec.
- Corrigir a sintaxe do contexto em `openspec/config.yaml` sem remover as regras arquiteturais existentes.
- Registrar pendências, inclusive a URL externa da imagem, sem introduzir novos tokens, dependências ou mudanças de interface.

## Capabilities

### New Capabilities

Nenhuma. Esta mudança formaliza documentação e instruções; não cria comportamento de produto.

### Modified Capabilities

Nenhuma. `openspec/specs/` não contém capabilities existentes e não há alteração de requisitos funcionais. O change declara `skip_specs: true`.

## Impact

Afeta `docs/design-system.md`, `AGENTS.md`, `openspec/config.yaml` e os artefatos desta mudança. Não altera o frontend Reflex, Xano, dados, dependências, rotas ou comportamento de autenticação.
