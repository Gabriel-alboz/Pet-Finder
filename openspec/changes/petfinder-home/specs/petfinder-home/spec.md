# Spec Delta

## Purpose

Define uma área principal responsiva para orientar adotantes entre descoberta de pets, organizações, quiz e conta, sem apresentar dados ou ações como disponíveis quando não houver contrato funcional no backend.

## ADDED Requirements

### Requirement: Home navigation
O sistema SHALL oferecer uma área Home com navegação acessível entre início, pets, ONGs, quiz e conta. A seção selecionada SHALL ser identificável visualmente e a navegação SHALL funcionar em telas estreitas.

#### Scenario: Navigate between sections
- **WHEN** a pessoa seleciona uma seção do menu
- **THEN** o conteúdo correspondente é apresentado e a seção ativa fica destacada sem recarregar a aplicação inteira

#### Scenario: Use navigation on a small screen
- **WHEN** a pessoa acessa a Home em uma tela estreita
- **THEN** os controles de navegação permanecem acessíveis sem provocar rolagem horizontal

### Requirement: Honest pet and NGO discovery states
O sistema SHALL apresentar pets e ONGs somente com registros retornados por endpoints disponíveis e compatíveis. Quando não houver endpoint ou registros, SHALL informar a indisponibilidade ou estado vazio sem exibir dados fictícios, fotos ilustrativas como registros, quantidade inventada ou verificação não confirmada.

#### Scenario: Pet catalog contract is unavailable
- **WHEN** não existe endpoint de listagem de pets configurado e confirmado
- **THEN** a Home e a seção de pets informam que o catálogo ainda não está conectado e não mostram cards fictícios

#### Scenario: NGO catalog contract is unavailable
- **WHEN** não existe endpoint de listagem de ONGs configurado e confirmado
- **THEN** a seção de ONGs informa a indisponibilidade sem apresentar organizações simuladas

#### Scenario: Backend returns an empty catalog
- **WHEN** um endpoint disponível retorna uma lista vazia
- **THEN** o sistema apresenta um estado vazio apropriado sem confundi-lo com erro de conexão

### Requirement: Compatibility results are truthful
O sistema SHALL apresentar compatibilidades como resultados somente quando existirem respostas do quiz e resultados fornecidos pelo backend. Na ausência de quiz ou cálculo disponível, SHALL explicar a pendência e não inventar pontuação ou recomendação.

#### Scenario: Compatibility service is unavailable
- **WHEN** não existe quiz ou serviço de compatibilidade disponível
- **THEN** a seção orienta a pessoa sobre a indisponibilidade e não mostra porcentagens ou pets recomendados fictícios

### Requirement: Account actions respect available authentication
O sistema SHALL exibir dados de perfil, proteger áreas privadas e encerrar sessão somente quando houver fluxo de autenticação implementado e válido. Na ausência de sessão, SHALL identificar que a conta não está conectada e oferecer navegação para o login sem declarar logout ou autenticação concluídos.

#### Scenario: No authenticated session exists
- **WHEN** a Home não dispõe de uma sessão verificável
- **THEN** ela não apresenta nome, tipo de conta ou dados de perfil fictícios e não simula uma operação de logout

### Requirement: No unsupported adoption operations
O sistema SHALL iniciar uma solicitação de adoção, favorito, edição de perfil ou operação semelhante somente por meio de endpoint existente e autorizado. Se o fluxo não existir, SHALL informar que a operação ainda não está disponível.

#### Scenario: Adoption endpoint is unavailable
- **WHEN** a pessoa tenta iniciar uma adoção e não existe fluxo de solicitação confirmado
- **THEN** o sistema informa a indisponibilidade sem confirmar ou persistir uma solicitação
