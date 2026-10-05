# Proposal

## Why

Pet Finder precisa de uma base de identidade que diferencie adotantes e ONGs sem permitir que uma conta acesse dados privados de outra. A estrutura Xano versionada já oferece autenticação genérica, mas ainda não representa os dois tipos de conta nem os dados e regras exigidos pelo domínio.

## What Changes

- Definir cadastro de adotantes e ONGs com os campos obrigatórios, validações e identificadores próprios previstos para cada tipo.
- Definir e validar no backend e-mail globalmente único, CPF único entre adotantes e CNPJ único entre ONGs; o tipo da conta não poderá ser alterado pelo perfil.
- Definir login compartilhado, identificação do tipo de conta, encaminhamento para a área correspondente, logout e proteção de áreas privadas.
- Definir autorização e isolamento no backend para que cada conta acesse e edite somente os próprios dados permitidos.
- Adaptar a autenticação genérica já existente no Xano somente após avaliar compatibilidade; preservar os fluxos existentes que não conflitem e impedir que senhas, tokens ou dados de credenciais sejam registrados em logs.
- Manter fora do escopo pets, busca, match e solicitações de adoção, bem como contas adicionais ou membros de uma ONG.

## Capabilities

### New Capabilities

- `identity-and-authentication`: cadastro, autenticação, classificação de contas, autorização e isolamento de dados para adotantes e ONGs.

### Modified Capabilities

Nenhuma. O projeto ainda não possui especificações OpenSpec existentes.

## Impact

- Frontend Reflex existente em `Pet_Finder/`, atualmente ainda no scaffold inicial; não será introduzida outra tecnologia de frontend.
- Autenticação, persistência, validações e controle de acesso no Xano, tomando como ponto de partida `xano/table/user.xs` e os endpoints genéricos em `xano/api/authentication/`.
- A tabela Xano atual usa `role` com `admin/member`, e signup/login e redefinição de senha enviam registros de usuário como metadados de eventos. A compatibilidade desses papéis e a proteção efetiva de logs precisam ser resolvidas antes de qualquer alteração aplicada.
- Nenhuma alteração física no banco, endpoint, interface ou código é realizada por esta proposta.