# Proposal

## Why

A documentação contém descrições anteriores à integração de autenticação. É necessário distinguir código operacional, evidências de teste e visão futura, e preparar a navegação de Chats sem criar uma integração de mensagens.

## What Changes

- Consolidar documentação de arquitetura, estado atual, requisitos RF-01 a RF-10 e roadmap.
- Acrescentar Chats ao menu compartilhado desktop/mobile e uma seção vazia demonstrativa na Home protegida existente.
- Incluir avisos de funcionalidades futuras nas seções Pets, ONGs e Conta, sem ações operacionais.
- Preservar autenticação, cadastro, alterações preexistentes e todos os recursos Xano.

## Capabilities

### New Capabilities

- `chat-preview`: navegação autenticada para uma interface de Chats explicitamente demonstrativa.

### Modified Capabilities

Nenhuma especificação consolidada existente. As mudanças anteriores de Home e autenticação permanecem preservadas; os requisitos futuros ficam centralizados em `docs/functional-requirements.md`.

## Impact

Somente `Pet_Finder/home.py`, testes offline, documentação e estes artefatos OpenSpec. Nenhum endpoint, tabela, XanoScript, serviço ou mecanismo de sessão será alterado. Não haverá nova rota: Chats será uma seção local de `/home`.
