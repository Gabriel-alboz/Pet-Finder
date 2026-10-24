# Autenticação Xano — referência de implementação

## Escopo e origem

Referência do código local em `xano/` e `Pet_Finder/services/xano.py`, consolidada na Etapa 21. A publicação seletiva dos seis recursos de segurança foi informada como concluída na Etapa 17. Não houve consulta ou alteração remota nesta etapa; descrição estrutural não equivale a novo teste funcional live. O planejamento histórico permanece no OpenSpec.

Workspace 151970 (Gabriel's Workspace), branch publicada `v1`, plano Free sem branch isolada disponível neste ambiente. Não usar publicação global ou sincronização de workspace para validar o frontend.

## Configuração utilizada

A variável `XANO_API_BASE_URL` do processo backend aponta ao grupo Authentication:

```text
https://x8ki-letl-twmt.n7.xano.io/api:yFqRLsBC:v1
```

A URL é pública. Não colocar tokens, senhas ou credenciais administrativas em código/documentação/arquivos versionados. Runtime de login/cadastro não utiliza autenticação CLI nem Meta API. O cliente de login exige base HTTPS sem credenciais embutidas, query ou fragmento; requisições usam timeout de 10 segundos, sem seguir redirecionamentos.

## Contratos utilizados pelo Reflex

| Operação | Entrada | Resposta consumida / comportamento |
|---|---|---|
| `POST /auth/login` | JSON `email`, `password` | `{authToken, user_id}`; token gerado com validade de 24 horas. Não depende de `account_type` nesta resposta |
| `GET /auth/me` | Bearer no cabeçalho; sem dados de formulário | `id`, `created_at`, `name`, `email`, `role`, `account_type`. Classificação válida ADOTANTE/ONG ou `null` para ausente/inválida |
| `POST /auth/signup` | Campos comuns e específicos abaixo | Código local retorna `authToken`, `user_id`, `account_type` e objeto `user` com dados selecionados. Cliente de cadastro verifica `user_id`, descarta token e orienta login |

`auth/me` obtém classificação do usuário autenticado, não do frontend. O cliente conserva apenas ID, nome e tipo; valida que o ID corresponde ao login e rejeita tipo inválido sem inferir via `role`. Não adicionar restrições de role ao contrato de login.

Login normaliza e-mail; senha segue sem transformação. Respostas login 400/401/403 geram mensagem genérica de credenciais; me 401/403 indica sessão rejeitada. HTTP 429, timeout, falha de rede, outros erros e JSON/identidade inválidos recebem mensagens controladas, sem expor corpos HTTP ou exceções brutas.

### Cadastro existente

- Comuns: `account_type`, `name`, `email`, `password`, `phone`, `address`, `city`, `uf`.
- ADOTANTE: `cpf` e `birth_date` (ISO no envio; formulário usa dia/mês/ano).
- ONG: `cnpj` e `description`.
- Confirmação de senha é verificação local, não campo do contrato enviado.
- Backend verifica tipo, documentos e duplicidade, normaliza documentos/telefone, exige data de nascimento válida anterior à atual para ADOTANTE e senha mínima com letra e número.
- O schema local `user` inclui `account_type`, `adopter_profile` e `ngo_profile` JSON. Estes perfis não são tabelas de catálogo de ONGs nem endpoints de edição implementados.
- Não adicionar credenciais/documentos a auditoria. Não assumir índice único de CPF/CNPJ nos perfis JSON: checagem por consulta merece revisão de concorrência futura.
- Cadastro bem-sucedido não cria sessão Reflex. Cliente trata duplicidade 400/409/422 com mensagem genérica e não revela qual conta existe.

A validação local de senha admite letras acentuadas, enquanto a expressão backend utiliza letras ASCII. A consistência deve ser revisada em etapa própria, preservando o fluxo atual nesta execução.

## Auditoria e recursos não utilizados pela interface

| Recurso preparado/publicado no histórico | Contrato de proteção registrado no código local |
|---|---|
| `Quick Start/log_event` | Preserva `user_id` e `action`; reconstrói metadados somente como `{account_type: "ADOTANTE"}`, `{account_type: "ONG"}` ou `{}`. Descarta quaisquer chaves extras |
| `auth/login` | Auditoria com `{}`, preservando credenciais, erros e token 24h |
| `auth/me` | Auditoria com tipo válido somente ou `{}`; resposta de conta antiga pode ser `null` |
| `reset/magic-link-login` | Metadados `{}`, sem objeto completo de usuário |
| `reset/update_password` | Metadados `{}`, preservando fluxo de senha existente |
| `logs/user/my_events` | Protege leitura histórica retornando metadados vazios, sem alterar/excluir eventos armazenados; mantém autenticação e filtro por usuário. A cópia local retorna lista, sem paginação configurada |

Os recursos de reset e consulta de eventos possuem cópias locais, mas não são usados pelo frontend atual. O link de recuperação no login é visual. Outros recursos presentes em `xano/` não são novas integrações; não executar endpoint funcional para conferir disponibilidade, pois até operações com verbo GET podem gravar auditoria ou outros dados.

## Sessão e segurança

Token privado no backend Reflex, sem cookie/localStorage/JavaScript; validade local máxima de 24 horas. Guarda da Home revalida identidade em me; falha fecha o acesso. Conta sem classificação válida não entra na Home. Logout limpa sessão local, sem revogação remota. Sessão persistente ainda depende de infraestrutura segura não implementada.

Ver [login e sessão](login-integration.md), [arquitetura](architecture.md) e [evidências](project-status.md). Não confundir assinatura de função sanitizadora com limpeza retroativa de registros históricos: não há exclusão de dados nesta etapa.

## Validação e futuras alterações

Testes offline utilizam mocks; nenhum cadastro, login, reset ou consulta funcional live foi executado na Etapa 21. Para futuras publicações: autorização seletiva por recurso, backup sem segredos, hashes e checagem de concorrência; distinguir Draft de live. Não usar push global, alterar dados ou reverter automaticamente auditoria para código inseguro. Qualquer teste integrado exige autorização e evidências específicas.
