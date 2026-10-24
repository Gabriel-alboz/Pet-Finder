# Chat Preview

## Purpose

Oferecer acesso autenticado à apresentação inicial de Chats, distinguindo a interface demonstrativa da comunicação privada futura do Pet Finder.

## ADDED Requirements

### Requirement: Shared authenticated Chats navigation
The system SHALL oferecer Chats no menu desktop e mobile da Home, com o mesmo estilo, hover e indicação de seleção dos demais itens, reutilizando a proteção atual.

#### Scenario: Authenticated account opens Chats
- **WHEN** uma conta ADOTANTE ou ONG autenticada seleciona Chats
- **THEN** a seção Chats é selecionada dentro de `/home` e o menu mobile é fechado

#### Scenario: Missing or expired session
- **WHEN** um visitante sem sessão válida tenta navegar para Chats
- **THEN** o acesso é bloqueado pelo mecanismo existente e o visitante é encaminhado para `/login`

### Requirement: Explicit demonstrative empty state
The system SHALL mostrar título, subtítulo e estado vazio de Chats, indicando que a integração ainda não existe e sem criar conversas ou realizar chamadas de mensagens.

#### Scenario: Chats preview opens
- **WHEN** a seção Chats é exibida
- **THEN** aparecem `Chats`, `Converse com ONGs e adotantes e acompanhe suas conversas.`, `Você ainda não possui conversas.` e `Quando iniciar uma conversa, ela aparecerá aqui.`
- **AND** há um ícone de mensagens e um aviso de interface demonstrativa sem backend

### Requirement: Preserve existing flows
The system SHALL preservar login, cadastro, Home e sessão existentes, identificando filtros e edição de conta como recursos futuros.

#### Scenario: Future account features
- **WHEN** uma conta vê a seção de configurações
- **THEN** as indicações futuras correspondem exclusivamente ao `account_type` autenticado e não permitem operações de edição
