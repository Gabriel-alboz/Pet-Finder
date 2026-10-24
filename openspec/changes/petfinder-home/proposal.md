# Proposal

## Why

O projeto tem login e cadastro, mas ainda não oferece uma área de descoberta que ajude adotantes a navegar por pets, ONGs e próximos passos. Uma Home em Reflex cria esse ponto de entrada sem apresentar registros ou resultados de compatibilidade que o Xano ainda não fornece.

## What Changes

- Adicionar uma Home responsiva com navegação lateral e seções de início, pets, ONGs, quiz e conta.
- Apresentar dados reais apenas quando houver endpoint e contrato confirmado; enquanto ausentes, mostrar estados vazios e pendências de forma explícita.
- Manter login e cadastro existentes e não simular sessão, logout, perfil, quiz, favoritos ou solicitação de adoção.
- Documentar os contratos Xano ainda necessários para ativar dados e operações da Home.

## Capabilities

### New Capabilities

- `petfinder-home`: navegação e experiência de descoberta de pets e ONGs, com estados honestos para recursos ainda indisponíveis.

### Modified Capabilities

Nenhuma.

## Impact

- Reflex: nova rota `/home`, estado e componentes na aplicação existente.
- Xano: nenhuma alteração remota; o snapshot disponível não possui tabelas ou endpoints de pets, ONGs, quiz, adoção, favoritos ou perfil completo.
- Autenticação: o login atual não cria sessão; esta mudança não protege a rota nem oferece logout até existir um fluxo de sessão verificável.
- Dependências: nenhuma nova dependência prevista.
