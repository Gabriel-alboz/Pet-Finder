# Proposal

## Why

Configurações ainda não consulta o perfil completo. A Etapa 23.3.2 prepara uma consulta privada segura em XanoScript local, sem publicar nem alterar a autenticação existente.

## What Changes

- Criar somente GET account/profile autenticado, identificado por $auth.id, com resposta por allowlist.
- Mascarar documentos válidos mostrando apenas dois dígitos; tratar dados legados sem migração.
- Definir defaults seguros e projeções tipadas para campos futuros, sem implementar edição ou descoberta.
- Guardar cópia separada das definições publicadas, IDs, horário e hashes, sem registros ou segredos.
- Validar sintaxe XanoScript e contratos estaticamente/offline, documentando limites de execução.

## Capabilities

### New Capabilities

- `own-account-profile-read`: consulta privada dos próprios dados permitidos, sem efeitos persistentes.

### Modified Capabilities

Nenhuma. Preservar identidade/autenticação e prévia visual. RF-03/RF-07 continuam parciais.

## Impact

Novo xano/api/authentication/account/profile_GET.xs, testes offline, documentação e backups/xano-definitions separado do diretório sincronizável. Sem frontend, PATCH, schema, migração, publicação ou testes funcionais live.
