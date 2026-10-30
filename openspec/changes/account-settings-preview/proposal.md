# Proposal

## Why

A seção Configurações ainda apresenta somente um aviso. A Etapa 23.2 oferece uma prévia organizada por tipo autenticado antes da integração de leitura e edição do perfil.

## What Changes

- Mostrar blocos específicos de ADOTANTE e ONG dentro da Home protegida.
- Reutilizar componentes visuais, sem novos estados, rotas, salvamento ou chamadas HTTP.
- Usar somente nome da sessão; demais campos vazios e somente leitura. Consentimentos desligados e indisponíveis.
- Documentar entrega visual parcial de RF-03/RF-07 e validar offline.

## Capabilities

### New Capabilities

- `account-settings-preview`: prévia privada e responsiva das configurações por tipo de conta.

### Modified Capabilities

Nenhuma. Requisitos de propriedade e autenticação existentes permanecem; esta entrega não implementa edição operacional.

## Impact

`pet_finder/home.py`, novo módulo visual de configurações, testes offline e documentação. Nenhuma alteração em autenticação, cadastro, serviços, XanoScripts ou dependências. Sem publicação ou arquivamento.
