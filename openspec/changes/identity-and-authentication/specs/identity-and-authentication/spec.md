# Spec Delta

## Purpose

Estabelece a identidade autenticável de adotantes e ONGs e as regras de acesso necessárias para proteger os dados privados de cada conta no Pet Finder.

## ADDED Requirements

### Requirement: Account types

O sistema SHALL reconhecer somente os tipos de conta `ADOTANTE` e `ONG` para os cadastros deste Change. O tipo SHALL ser definido pelo fluxo de cadastro correspondente, persistido no backend e não poderá ser alterado pela edição de perfil.

#### Scenario: Create an adopter account
- **WHEN** uma pessoa conclui o cadastro de adotante com dados válidos
- **THEN** a conta criada é identificada no backend como `ADOTANTE`

#### Scenario: Create an NGO account
- **WHEN** uma organização conclui o cadastro de ONG com dados válidos
- **THEN** a conta criada é identificada no backend como `ONG`

#### Scenario: Reject account type modification
- **WHEN** uma conta tenta alterar seu tipo por uma operação de perfil
- **THEN** o backend rejeita a alteração e mantém o tipo original

### Requirement: Adopter registration

O sistema SHALL oferecer cadastro de adotante exigindo nome completo, CPF, e-mail, telefone, senha, data de nascimento, endereço, cidade e UF. O backend SHALL rejeitar campos ausentes ou inválidos, validar o CPF e garantir que ele não esteja associado a outro adotante. O sistema SHALL aceitar somente uma UF válida e não poderá gerar CPF.

#### Scenario: Register adopter with valid required data
- **WHEN** o cadastro contém todos os campos obrigatórios e cada valor passa pela validação aplicável
- **THEN** o backend cria uma conta do tipo `ADOTANTE` e seus dados de adotante

#### Scenario: Reject incomplete or invalid adopter data
- **WHEN** o cadastro de adotante contém campo obrigatório ausente ou valor inválido, incluindo CPF inválido, data inválida ou UF não reconhecida
- **THEN** o backend rejeita o cadastro sem criar uma conta

#### Scenario: Reject duplicate adopter CPF
- **WHEN** um cadastro de adotante usa CPF já associado a outro adotante
- **THEN** o backend rejeita o cadastro sem criar uma segunda associação para esse CPF

### Requirement: NGO registration

O sistema SHALL oferecer cadastro de ONG exigindo nome da ONG, CNPJ, e-mail, telefone, senha, endereço, cidade, UF e descrição. O backend SHALL rejeitar campos ausentes ou inválidos, validar o CNPJ e garantir que ele não esteja associado a outra ONG. Cada ONG SHALL possuir exatamente uma conta neste escopo, e o sistema não oferecerá associação de funcionários, membros ou contas adicionais. O sistema SHALL aceitar somente uma UF válida e não poderá gerar CNPJ.

#### Scenario: Register NGO with valid required data
- **WHEN** o cadastro contém todos os campos obrigatórios e cada valor passa pela validação aplicável
- **THEN** o backend cria uma conta do tipo `ONG` associada a uma única ONG

#### Scenario: Reject incomplete or invalid NGO data
- **WHEN** o cadastro de ONG contém campo obrigatório ausente ou valor inválido, incluindo CNPJ inválido ou UF não reconhecida
- **THEN** o backend rejeita o cadastro sem criar uma conta ou ONG

#### Scenario: Reject duplicate NGO CNPJ
- **WHEN** um cadastro de ONG usa CNPJ já associado a outra ONG
- **THEN** o backend rejeita o cadastro sem criar uma segunda associação para esse CNPJ

#### Scenario: Reject additional account for the same NGO
- **WHEN** uma tentativa de cadastro cria uma segunda conta para a mesma ONG
- **THEN** o backend rejeita a associação adicional

### Requirement: Unique authentication email

O e-mail SHALL ser um identificador de autenticação válido e único entre todas as contas, independentemente do tipo. A unicidade SHALL ser garantida no backend e não depender somente da validação do frontend.

#### Scenario: Reject email used by another account type
- **WHEN** uma pessoa tenta cadastrar e-mail já utilizado por uma conta de qualquer tipo
- **THEN** o backend rejeita o cadastro e mantém uma única conta associada ao e-mail

#### Scenario: Reject malformed email
- **WHEN** um cadastro contém e-mail fora do formato aceito
- **THEN** o backend rejeita o cadastro

### Requirement: Protected credential handling

O sistema SHALL usar o mecanismo seguro de autenticação do Xano para armazenar senhas, sem armazená-las em texto puro. Senhas SHALL NOT aparecer em logs, código, documentação ou respostas de API. Credenciais e tokens reais SHALL NOT ser incluídos em código ou documentação. Tokens de autenticação SHALL ser expostos somente no fluxo necessário para estabelecer a autenticação e nunca em logs ou documentação.

#### Scenario: Store password using Xano authentication
- **WHEN** uma conta é criada ou sua senha é atualizada
- **THEN** o Xano armazena a senha usando seu mecanismo seguro de autenticação, sem persistir texto puro

#### Scenario: Exclude credentials from logs and profile responses
- **WHEN** um evento de autenticação é registrado ou dados de conta são retornados fora do fluxo de autenticação
- **THEN** senha, material de senha e token não aparecem nos metadados de log nem na resposta

#### Scenario: Keep real credentials out of source and documentation
- **WHEN** código ou documentação do projeto é criado ou alterado
- **THEN** nenhum valor real de senha, credencial ou token é incluído

### Requirement: Shared login and account destination

O sistema SHALL oferecer um fluxo de login compartilhado por adotantes e ONGs, recebendo e-mail e senha. Após autenticação válida, o sistema SHALL identificar o tipo da conta e encaminhar o usuário à área correspondente. Credenciais inválidas SHALL ser rejeitadas.

#### Scenario: Login as adopter
- **WHEN** uma conta `ADOTANTE` fornece credenciais válidas
- **THEN** o sistema estabelece a autenticação e direciona a conta à área do adotante

#### Scenario: Login as NGO
- **WHEN** uma conta `ONG` fornece credenciais válidas
- **THEN** o sistema estabelece a autenticação e direciona a conta ao painel da ONG

#### Scenario: Reject invalid credentials
- **WHEN** as credenciais fornecidas não autenticam uma conta
- **THEN** o sistema não estabelece uma sessão autenticada

### Requirement: Logout invalidates authentication

Usuários autenticados SHALL poder encerrar a autenticação. Após o logout, a sessão correspondente SHALL ser invalidada pelo backend conforme o mecanismo utilizado, e requisições protegidas feitas com a sessão encerrada SHALL ser recusadas.

#### Scenario: Use a session after logout
- **WHEN** uma conta encerra sua sessão e tenta usar a mesma sessão em uma operação protegida
- **THEN** o backend recusa a operação por falta de autenticação válida

### Requirement: Protect private areas

O sistema SHALL impedir que usuários não autenticados acessem áreas privadas. A proteção no frontend SHALL complementar, mas não substituir, a autenticação e autorização aplicadas no backend.

#### Scenario: Navigate directly to a private area without authentication
- **WHEN** um usuário não autenticado acessa diretamente uma área privada
- **THEN** o acesso é impedido e o usuário é direcionado à autenticação ou recebe resposta apropriada

### Requirement: Account data ownership and authorization

O backend SHALL autorizar operações sobre dados de conta com base na identidade autenticada e no tipo de conta, permitindo acesso e edição somente aos próprios dados permitidos. CPF, CNPJ e tipo da conta não poderão ser alterados por uma operação comum de edição de perfil. Uma conta SHALL NOT acessar ou modificar dados privados de outra conta; uma conta de adotante SHALL NOT acessar recursos privados de ONG.

#### Scenario: Read and edit own permitted account data
- **WHEN** uma conta autenticada solicita leitura ou edição de dados próprios permitidos para seu tipo
- **THEN** o backend autoriza a operação

#### Scenario: Access another account's private data
- **WHEN** uma conta tenta ler ou modificar dados privados pertencentes a outra conta
- **THEN** o backend rejeita a operação

#### Scenario: Change CPF, CNPJ, or account type through profile editing
- **WHEN** uma conta tenta alterar CPF, CNPJ ou tipo usando edição comum de perfil
- **THEN** o backend rejeita a alteração

#### Scenario: Adopter accesses private NGO resources
- **WHEN** uma conta `ADOTANTE` tenta acessar um recurso privado destinado a uma ONG
- **THEN** o backend rejeita o acesso