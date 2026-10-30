# Spec Delta

## Purpose

Consultar exclusivamente o próprio perfil autenticado por meio de uma projeção privada e previsível, sem divulgar documentos completos ou produzir alterações persistentes.

## ADDED Requirements

### Requirement: Authenticated ownership
O endpoint SHALL exigir autenticação válida, obter a conta pelo contexto autenticado e não aceitar identidade de proprietário como entrada. Conta ausente SHALL receber erro genérico notfound e tipo diferente de ADOTANTE/ONG SHALL receber accessdenied.

#### Scenario: Own account
- **WHEN** ADOTANTE ou ONG autenticado solicita seu perfil
- **THEN** somente o registro da identidade autenticada é consultado

#### Scenario: Missing authentication or invalid account
- **WHEN** falta autenticação válida, o registro está ausente ou o tipo não é reconhecido
- **THEN** o acesso falha sem resposta de perfil ou exposição de dados internos

### Requirement: Explicit private response
A resposta SHALL conter data com id, name, email, account_type, phone, address, city, uf, adopter_profile e ngo_profile. Apenas o perfil correspondente SHALL ser preenchido. Credenciais, role, nascimento e chaves JSON desconhecidas SHALL ser excluídos.

#### Scenario: Adopter projection
- **WHEN** o tipo é ADOTANTE
- **THEN** adopter_profile contém apenas cpf_masked, about_me, adoption_preferences e consents, enquanto ngo_profile é null

#### Scenario: NGO projection
- **WHEN** o tipo é ONG
- **THEN** ngo_profile contém apenas cnpj_masked e description, enquanto adopter_profile é null

### Requirement: Document masking and legacy safety
CPF/CNPJ SHALL revelar no máximo os dois últimos dígitos, somente após formato e verificadores válidos. Valores ausentes, inválidos ou de tipo inesperado SHALL produzir null. Perfis não objetos SHALL usar valores seguros de apresentação sem migração. Campos futuros SHALL ser reconstruídos por allowlist e tipo, com consentimentos false quando não forem booleanos true explícitos.

#### Scenario: Document validation
- **WHEN** documento é inválido, ausente, repetido ou tem dígitos verificadores incorretos
- **THEN** a máscara é null sem incluir o valor em erros

#### Scenario: Missing or malformed JSON
- **WHEN** perfil, preferências ou consentimentos não possuem a estrutura esperada
- **THEN** a resposta usa textos/listas vazios, sexo e documento null e consentimentos false, sem modificar registros

### Requirement: Read-only and cache protection
A consulta SHALL não gravar dados/auditoria nem executar integrações com efeitos persistentes. Respostas SHALL instruir no-store e não usar cache compartilhado de perfis. O endpoint SHALL permanecer somente local até autorização de publicação.

#### Scenario: Local delivery
- **WHEN** a Etapa 23.3.2 é entregue
- **THEN** existem arquivo e verificações locais, sem publicação, integração Reflex ou execução funcional no Xano
