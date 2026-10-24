# Domain Model — Pet Finder

## 1. Visão geral do domínio

O Pet Finder possui como domínio principal a adoção responsável de animais.

O sistema conecta pessoas interessadas em adotar animais e organizações responsáveis por animais disponíveis para adoção.

Os principais conceitos do domínio são:

* Usuário;
* ONG;
* Animal;
* Perfil de adoção;
* Match;
* Solicitação de adoção.

Os conceitos representam elementos do domínio e seus relacionamentos. Este documento não define o modelo físico do banco de dados.

## 2. Usuário

Representa uma pessoa que utiliza o sistema com o objetivo de encontrar animais compatíveis e realizar solicitações de adoção.

### Responsabilidade

Permitir que uma pessoa mantenha suas informações de usuário e utilize os recursos relacionados à busca e adoção de animais.

### Principais informações conceituais

* identificação;
* nome;
* informações de contato;
* credenciais de acesso;
* informações relacionadas às preferências de adoção.

### Relacionamentos

* Um usuário pode manter um perfil de adoção; responder ao quiz não é obrigatório.
* Um usuário pode receber vários matches com animais.
* Um usuário pode realizar várias solicitações de adoção.
* Cada solicitação de adoção é realizada por um único usuário.

## 3. ONG

Representa uma organização responsável por animais disponíveis para adoção.

### Responsabilidade

Cadastrar e administrar os animais sob sua responsabilidade e gerenciar as solicitações de adoção recebidas.

### Principais informações conceituais

* identificação;
* nome da organização;
* informações de contato;
* informações institucionais;
* credenciais de acesso.

### Relacionamentos

* Uma ONG pode possuir vários animais cadastrados.
* Um animal está associado a uma ONG responsável.
* Uma ONG pode receber várias solicitações de adoção relacionadas aos seus animais.

## 4. Animal

Representa um animal disponível ou cadastrado no sistema para fins de adoção.

### Responsabilidade

Concentrar as informações necessárias para que usuários conheçam o animal e para que o sistema possa identificar possíveis compatibilidades.

### Principais informações conceituais

* identificação;
* nome;
* espécie;
* raça;
* idade;
* sexo;
* porte;
* características comportamentais;
* informações de saúde relevantes para a adoção;
* disponibilidade para adoção.

### Relacionamentos

* Um animal pertence a uma ONG responsável.
* Um animal pode aparecer em vários matches.
* Um animal pode receber várias solicitações de adoção.
* Cada solicitação de adoção está relacionada a um único animal.

## 5. Perfil de adoção

Representa as informações e preferências utilizadas para compreender o perfil do usuário interessado em adotar.

### Responsabilidade

Representar características relevantes do usuário para permitir a identificação de possíveis compatibilidades com os animais cadastrados.

### Principais informações conceituais

* preferências relacionadas ao animal;
* características do ambiente do usuário;
* preferências de porte;
* preferências relacionadas à espécie;
* outras informações relevantes para o processo de compatibilidade.

### Relacionamentos

* Um perfil de adoção pertence a um usuário.
* As informações do perfil podem ser utilizadas pelo sistema para gerar matches com animais.

## 6. Match

Representa uma possível compatibilidade identificada entre um usuário e um animal.

### Responsabilidade

Relacionar um usuário a um animal que apresenta características potencialmente compatíveis com suas preferências e perfil de adoção.

### Principais informações conceituais

* usuário relacionado;
* animal relacionado;
* informações utilizadas para a compatibilidade;
* resultado ou indicação de compatibilidade.

### Relacionamentos

* Um match relaciona um usuário a um animal.
* Um usuário pode possuir vários matches.
* Um animal pode aparecer em vários matches.
* Um match não representa necessariamente uma adoção concluída.

## 7. Solicitação de adoção

Representa o interesse formal de um usuário em adotar um animal específico.

### Responsabilidade

Registrar e permitir o acompanhamento do interesse de adoção entre um usuário e a ONG responsável pelo animal.

### Principais informações conceituais

* usuário solicitante;
* animal desejado;
* data da solicitação;
* situação da solicitação;
* informações necessárias para análise da adoção.

### Relacionamentos

* Uma solicitação pertence a um usuário.
* Uma solicitação está relacionada a um único animal.
* O animal está associado a uma ONG responsável.
* Uma ONG pode receber várias solicitações de adoção.

## 8. Relacionamentos principais

A estrutura conceitual simplificada do domínio pode ser representada da seguinte forma:

```text
                    ┌──────────────┐
                    │     ONG      │
                    └──────┬───────┘
                           │
                     responsável por
                           │
                           ▼
                    ┌──────────────┐
                    │    Animal    │
                    └──────┬───────┘
                           │
                  ┌────────┴────────┐
                  │                 │
                Match          Solicitação
                  │                 │
                  ▼                 ▼
             ┌──────────────┐  ┌──────────────┐
             │    Usuário   │  │    Usuário   │
             └──────┬───────┘  └──────────────┘
                    │
                    │ possui
                    ▼
             ┌──────────────┐
             │   Perfil de  │
             │    adoção    │
             └──────────────┘
```

De forma conceitual:

* uma **ONG** é responsável por um ou mais **Animais**;
* um **Usuário** pode manter um **Perfil de adoção**; quiz é opcional;
* um **Usuário** pode possuir vários **Matches**;
* um **Animal** pode participar de vários **Matches**;
* um **Usuário** pode realizar várias **Solicitações de adoção**;
* cada **Solicitação de adoção** está relacionada a um **Animal**;
* uma solicitação relacionada a um animal permite identificar indiretamente a ONG responsável por esse animal.

## 9. Regras estruturais importantes

* Todo animal cadastrado para adoção deve estar associado a uma ONG responsável.
* Um match representa uma possível compatibilidade e não significa que a adoção foi aprovada.
* Uma solicitação de adoção representa o interesse de um usuário em um animal específico.
* A solicitação de adoção deve permitir identificar o usuário solicitante e o animal desejado.
* A ONG responsável pelo animal deve ser identificável a partir do animal relacionado à solicitação.
* As informações de compatibilidade devem utilizar dados relacionados ao perfil do usuário e às características do animal.
* Os conceitos apresentados neste documento representam o domínio conceitual e não determinam antecipadamente a estrutura física do banco de dados.

## 10. Evolução do modelo

O modelo de domínio poderá ser refinado durante o desenvolvimento do projeto.

Novos conceitos, atributos conceituais ou relacionamentos poderão ser adicionados quando forem identificados durante o processo de Explore, Propose e desenvolvimento das mudanças do OpenSpec.

Alterações relevantes no domínio deverão ser analisadas antes de sua implementação.

## 11. Comunicação e consentimento — conceitos futuros

No vocabulário de produto, a conta pode ser ADOTANTE ou ONG. O conceito de Usuário interessado em adoção deste documento corresponde ao ADOTANTE; isso não exige tabelas separadas por perfil. O schema físico atual e os contratos estão em [arquitetura](architecture.md) e [referência Xano](xano-authentication-setup.md).

Uma **Conversa** representa comunicação privada entre ADOTANTE e ONG, com participantes autorizados e vínculo opcional a um Animal. Uma **Mensagem** pertence a uma conversa e identifica remetente, conteúdo e momento de envio. Estes conceitos são futuros; não há implementação física ou endpoints de chat nesta etapa.

A **Visibilidade consentida** representa a autorização do adotante para compartilhar campos e preferências específicos com ONGs. Deve permitir retirada de consentimento e não equivale a publicação de documentos, endereço privado ou credenciais. A descoberta de interessados e o contato dependem dessa autorização e de regras de acesso no servidor.

A busca direta de pets por filtros independe do quiz. Um match é uma recomendação futura, não aprovação de adoção nem algoritmo existente. Solicitações devem preservar a identificação das partes e status mesmo quando os detalhes do modelo físico forem definidos posteriormente.

Detalhes e critérios permanecem centralizados em [RF-01 a RF-10](functional-requirements.md); consulte [estado](project-status.md) para distinguir conceitos de código operacional.
