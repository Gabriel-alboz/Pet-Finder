# Spec Delta

## Purpose

Apresentar configurações de conta por tipo autenticado, com privacidade e indicação explícita dos limites demonstrativos antes da integração de perfis.

## ADDED Requirements

### Requirement: Authenticated account-specific preview
O sistema SHALL mostrar somente os blocos do account_type autenticado dentro da Home existente, sem inferir o tipo de role.

#### Scenario: Adopter opens settings
- **WHEN** ADOTANTE autenticado abre Configurações
- **THEN** vê Meus dados, Sobre mim, Pet que procuro, Privacidade e visibilidade e Segurança da conta, sem seções exclusivas de ONG

#### Scenario: NGO opens settings
- **WHEN** ONG autenticada abre Configurações
- **THEN** vê Dados da organização, Sobre a ONG, Localização e contato, Meus pets e Segurança da conta, sem preferências de adotante

#### Scenario: Session unavailable or type unknown
- **WHEN** sessão está inválida ou tipo não é reconhecido
- **THEN** nenhum dado de perfil é apresentado

### Requirement: Honest non-persistent fields
O sistema SHALL apresentar campos somente leitura e aviso de prévia sem salvamento, usando apenas nome seguro da sessão e valores vazios, sem chamadas de perfil, novos estados de dados pessoais ou mensagens de sucesso. E-mail SHALL permanecer vazio e somente leitura enquanto não estiver disponível com segurança.

#### Scenario: Inspect preview controls
- **WHEN** a pessoa consulta os campos e descrições
- **THEN** campos não aceitam edição, não existe envio ou salvamento e os limites visuais são 1000 caracteres para apresentação/pet e 2000 para descrição institucional

### Requirement: Privacy and unavailable operations
O sistema SHALL manter os dois consentimentos desligados e desabilitados, informar que preferências não são compartilhadas e mostrar gestão de pets e novas ações de segurança como indisponíveis.

#### Scenario: Inspect consent and pet management
- **WHEN** a pessoa consulta privacidade ou gestão de pets
- **THEN** não pode consentir, iniciar contato nem cadastrar pet, e nenhum dado de contato é publicado

### Requirement: Responsive shared navigation
O sistema SHALL preservar menu desktop/mobile, autenticação e logout existentes, usando layout adaptável e rótulos acessíveis sem exigir uma nova rota.

#### Scenario: Narrow viewport
- **WHEN** Configurações é apresentada em celular ou tablet
- **THEN** campos empilham quando necessário, textos quebram linha e menu compartilhado continua acessível
