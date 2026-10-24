# Dependências do backend para a Home

## Estado observado

A auditoria local encontrou apenas as tabelas `user` e `event_log`. Os arquivos de API versionados cobrem autenticação, redefinição de senha e leitura de eventos. Não foram encontrados endpoints ou tabelas locais para pets, organizações, quiz/match, solicitações de adoção ou favoritos. Também não há contrato de imagem de pet ou ONG.

O snapshot de autenticação não corresponde à branch remota `v1`, que está marcada como live e não possui os campos `account_type` e perfis do snapshot local. A URL base do Xano não está configurada. Nenhum MCP do Xano está conectado nesta sessão. A Home não faz chamadas a caminhos de API presumidos.

| Área | Contrato necessário antes de integrar | Comportamento atual |
|---|---|---|
| Pets | Listagem paginada de animais adotáveis, campos públicos de identificação, espécie/raça, idade, sexo, porte, localização, status, ONG responsável e URL de imagem; busca/filtros documentados. | Estado de catálogo indisponível; nenhum card ou registro de exemplo. |
| Detalhes do pet | Leitura de um animal por identificador, imagens e atributos públicos, ONG responsável e status atualizado. | Não há página nem chamada de detalhes. |
| ONGs | Listagem paginada com nome, descrição e localização pública; contato explicitamente permitido; forma de relacionar pets e calcular quantidade. | Estado de listagem indisponível; nenhuma organização simulada. |
| Quiz e compatibilidade | Perguntas, submissão/persistência de respostas, regra oficial de cálculo e consulta de resultados vinculados ao usuário. | A seção explica que quiz e resultados não estão disponíveis; não gera pontuação. |
| Perfil/configurações | Sessão segura, `/me` ativo no ambiente escolhido, campos permitidos e endpoint de atualização com regras de propriedade. | Perfil não carregado; a área informa que a sessão não está conectada. |
| Adoção e favoritos | Fluxos autorizados, contrato de criação/remoção e estados retornados pelo backend. | Nenhuma ação é apresentada como concluída ou persistida. |
| Logout | Endpoint ou mecanismo Xano que invalide a sessão, além de armazenamento seguro e ciclo de sessão no Reflex. | Não há logout; a navegação oferece acesso ao login. |

## Endpoints presentes somente no snapshot local

Os caminhos abaixo foram lidos nos arquivos Xano locais; não significam que estejam implantados na branch live:

- `POST auth/signup`, `POST auth/login`, `GET auth/me`.
- `GET reset/request-reset-link`, `POST reset/magic-link-login`, `POST reset/update_password`.
- `GET logs/user/my_events`.

`GET auth/me` requer autenticação Xano, mas a tela de login atual não estabelece sessão e o app não possui armazenamento/ciclo de token. Portanto, a Home não chama esse endpoint nem exibe perfil ou tipo de conta.

## Próximos passos para integração

1. Disponibilizar uma branch Xano de desenvolvimento compatível e confirmar sua URL base.
2. Definir e testar contratos de catálogo de pets e ONGs, paginação, filtros, campos de imagem e política de dados públicos.
3. Definir contratos do quiz e resultado oficial, além de adoção e favoritos se fizerem parte do escopo.
4. Concluir a sessão segura no Reflex e autenticação no Xano antes de habilitar configurações, logout ou qualquer dado privado.
5. Integrar cada serviço somente após revisar o método, caminho, parâmetros, resposta e autorização do endpoint correspondente; testar sucesso, lista vazia, erro e sessão expirada.

Nenhum endpoint remoto, schema Xano ou registro foi alterado para esta Home.
