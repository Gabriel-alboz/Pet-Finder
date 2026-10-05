# Project Overview — Pet Finder

## 1. Visão geral

O Pet Finder é uma aplicação web voltada à adoção responsável de animais de estimação.

O sistema tem como objetivo aproximar pessoas interessadas em adotar animais e organizações não governamentais (ONGs) responsáveis por animais disponíveis para adoção.

A aplicação permitirá que ONGs cadastrem e gerenciem seus animais, enquanto usuários poderão criar seus perfis, encontrar animais compatíveis com suas preferências e demonstrar interesse na adoção.

O sistema também contará com um processo de solicitação de adoção, permitindo que o interesse do usuário seja encaminhado à ONG responsável pelo animal.

## 2. Problema

A adoção de animais pode apresentar dificuldades para pessoas que desejam encontrar um animal compatível com seu perfil e para ONGs que precisam divulgar e administrar os animais disponíveis para adoção.

O Pet Finder busca centralizar essas informações em uma aplicação, facilitando a descoberta de animais, a identificação de compatibilidade entre usuários e animais e o gerenciamento das solicitações de adoção.

## 3. Objetivos

Os principais objetivos do projeto são:

* facilitar a busca por animais disponíveis para adoção;
* aproximar usuários interessados em adotar e ONGs;
* permitir o cadastro e gerenciamento de animais pelas ONGs;
* oferecer um mecanismo de compatibilidade entre usuários e animais;
* permitir que usuários demonstrem interesse na adoção de um animal;
* permitir que ONGs recebam e gerenciem solicitações de adoção;
* contribuir para um processo de adoção mais organizado e acessível.

## 4. Público-alvo / usuários

O sistema terá principalmente dois grupos de usuários:

### 4.1 Usuários interessados em adoção

Pessoas que desejam encontrar um animal para adoção.

Esses usuários poderão:

* criar uma conta;
* informar características e preferências relevantes para a busca;
* visualizar animais disponíveis;
* utilizar o mecanismo de match;
* consultar informações dos animais;
* solicitar a adoção de um animal.

### 4.2 ONGs

Organizações responsáveis por animais disponíveis para adoção.

As ONGs poderão:

* criar uma conta;
* cadastrar animais;
* manter as informações dos animais atualizadas;
* gerenciar os animais cadastrados;
* receber solicitações de adoção;
* gerenciar o processo de solicitações recebidas.

## 5. Escopo

O escopo inicial do Pet Finder contempla:

* cadastro e autenticação de usuários;
* cadastro e autenticação de ONGs;
* cadastro e gerenciamento de animais;
* visualização de animais disponíveis para adoção;
* mecanismo de match entre usuários e animais;
* solicitação de adoção;
* gerenciamento de solicitações pelas ONGs.

O projeto será desenvolvido de forma incremental. Funcionalidades adicionais poderão ser incorporadas posteriormente por meio de mudanças específicas no processo definido pelo OpenSpec.

## 6. Principais funcionalidades

### 6.1 Cadastro e acesso

O sistema deverá permitir o cadastro e acesso dos diferentes tipos de usuários previstos no domínio da aplicação.

### 6.2 Gerenciamento de animais

As ONGs deverão poder cadastrar e gerenciar informações dos animais disponíveis para adoção.

### 6.3 Busca e descoberta

Os usuários deverão poder consultar os animais disponíveis e acessar suas informações relevantes para a adoção.

### 6.4 Sistema de Match

O sistema deverá utilizar informações e preferências do usuário para identificar animais potencialmente compatíveis.

### 6.5 Solicitação de adoção

O usuário deverá poder demonstrar interesse na adoção de um animal específico por meio de uma solicitação de adoção.

### 6.6 Gerenciamento de solicitações

As ONGs deverão poder visualizar e gerenciar as solicitações de adoção relacionadas aos animais sob sua responsabilidade.

## 7. Requisitos e restrições importantes

* O sistema deverá considerar diferentes tipos de usuários e suas respectivas permissões.
* As informações dos animais deverão estar associadas às organizações responsáveis por eles.
* As solicitações de adoção deverão estar relacionadas ao usuário solicitante e ao animal correspondente.
* O sistema deverá preservar a integridade das informações relacionadas a usuários, ONGs, animais e solicitações.
* O desenvolvimento deverá ocorrer de forma incremental.
* A implementação de funcionalidades deverá ser precedida pelo planejamento correspondente no OpenSpec.
* O frontend deverá utilizar exclusivamente Reflex, conforme a decisão arquitetural definida para o projeto.
* Não deverá ser introduzida outra tecnologia de frontend sem uma mudança arquitetural explicitamente aprovada.

## 8. Arquitetura tecnológica

### Frontend

**Reflex**

Reflex será utilizado como tecnologia exclusiva para implementação do frontend da aplicação.

### Backend e dados

O projeto utilizará o ambiente Xano para os recursos de backend e persistência de dados definidos durante o desenvolvimento.

A implementação detalhada da estrutura física do banco de dados e dos endpoints não faz parte deste documento e deverá ser definida de forma incremental nas respectivas mudanças e especificações.

### Desenvolvimento assistido por IA

O projeto utilizará OpenSpec para organizar o desenvolvimento orientado por especificações e ferramentas de IA para auxiliar na análise, planejamento e implementação.

## 9. Princípios de desenvolvimento

O desenvolvimento do Pet Finder deverá seguir uma abordagem incremental.

As funcionalidades não deverão ser implementadas todas de uma vez. Cada mudança deverá ser analisada, planejada e revisada antes da implementação.

O processo seguirá, de forma geral:

**Contexto → Explore → Propose → Review → Apply → Archive**

A IA deverá atuar como ferramenta de apoio ao desenvolvimento. As decisões do projeto deverão ser analisadas e aprovadas pelos responsáveis pelo projeto.

## 10. Segurança e integridade

O sistema deverá considerar:

* controle de acesso conforme o tipo de usuário;
* proteção das informações dos usuários;
* proteção das informações relacionadas às ONGs;
* integridade das relações entre usuários, ONGs, animais e solicitações;
* tratamento adequado das informações utilizadas no processo de adoção;
* não exposição desnecessária de informações sensíveis.

Credenciais, tokens e outras informações de configuração que não devam ser versionadas não deverão ser armazenadas diretamente nos arquivos do projeto.

## 11. Estratégia de desenvolvimento

O desenvolvimento será realizado em mudanças incrementais utilizando OpenSpec.

Antes de uma implementação, o projeto deverá possuir contexto suficiente para que a mudança seja compreendida.

O fluxo esperado é:

1. analisar o contexto existente;
2. explorar o projeto;
3. identificar uma mudança adequada;
4. elaborar a proposta;
5. revisar a proposta;
6. implementar a mudança;
7. revisar o resultado;
8. arquivar a mudança concluída;
9. seguir para a próxima mudança.

O modelo conceitual do domínio poderá representar o sistema de forma ampla, enquanto sua implementação será realizada progressivamente.

## 12. Fonte de verdade e documentação

Os principais documentos de contexto do projeto são:

* `docs/project-overview.md` — visão geral do projeto;
* `docs/domain-model.md` — conceitos e relacionamentos do domínio;
* `AGENTS.md` — regras de trabalho para o agente;
* `openspec/config.yaml` — contexto e regras utilizados pelos workflows do OpenSpec;
* `openspec/specs/` — especificações do sistema;
* `openspec/changes/` — mudanças em desenvolvimento.

Esses documentos possuem responsabilidades diferentes e não devem ser utilizados para substituir uns aos outros.

O `project-overview.md` deverá permanecer relativamente estável e representar a visão geral do projeto, enquanto detalhes específicos de funcionalidades deverão ser registrados nas respectivas especificações e mudanças.
