# Design

## Context

Ver motivação em `proposal.md`. A Home usa seções locais, um menu compartilhado desktop/mobile e a proteção existente de `LoginState`. Os documentos anteriores ainda descrevem fases sem integração. Há alterações locais anteriores que precisam permanecer intactas.

## Goals / Non-Goals

Entregar navegação e estado vazio de Chats, documentar evidências e planejar RF-01 a RF-10. Não criar backend, alterar autenticação, cadastro, XanoScripts ou recursos remotos.

## Decisions

- Reutilizar `HomeState.open_section`, `_nav_item`, `_sidebar`, `_section_heading` e `_empty_state`, preservando hover, seleção e responsividade. Uma rota nova duplicaria a organização atual sem necessidade.
- Chats permanece dentro de `/home`, sob `require_auth`, `can_view_home` e a validação de eventos existente. Nenhuma sessão adicional.
- Avisos de conta usam somente `LoginState.account_type`, derivado do backend; valor desconhecido não recebe opções de nenhum perfil.
- Manter `docs/project-status.md` como referência de evidências e `docs/functional-requirements.md` como catálogo RF, com links nos demais documentos. Não duplicar especificações de autenticação nem reescrever tarefas históricas.
- Testar navegação e bloqueio com estados locais e mocks. Compilar não significa comprovar UX em navegador nem login live.

## Risks / Trade-offs

- Interface vazia pode parecer chat operacional → aviso explícito de demonstração, sem botões de envio ou conversas fictícias.
- Sessão transitória já existente → documentar limites; não alterar sua implementação nesta etapa.
- Diff contém trabalho anterior → comparar hashes com o inventário inicial e não corrigir whitespace herdado de `.xs`.
- Mudanças não aparecem em servidor prod antigo → requer reinicialização local para inspeção visual; não fazer deploy.

## Migration Plan

Mudança exclusivamente local, sem migração. Preservar trabalhos anteriores. Eventual reversão limita-se aos trechos desta etapa mediante análise de diff; não utilizar restauração geral.
