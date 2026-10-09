# Autenticação Xano — estado e preparação

## Escopo e estado verificado

Esta página documenta a comparação feita para `identity-and-authentication`. Nenhuma alteração foi enviada ao Xano remoto e nenhum registro foi exportado. A consulta remota foi somente de leitura, sem incluir variáveis de ambiente ou registros.

O CLI autenticado encontrou o workspace `Gabriel's Workspace` (ID `151970`), com somente a branch `v1`, marcada como live. O comando informou `Allow Push: false`. Não há branch de desenvolvimento disponível neste workspace; qualquer criação ou autorização de branch precisa ser feita pelo responsável do workspace.

## Diferença entre modelo remoto e snapshot local

### Remoto, branch live `v1`

A tabela `user` contém `id`, `created_at`, `name`, `email`, `password`, `role` (`admin`/`member`) e `password_reset` (`token`, `expiration`, `used`). Há índice único de e-mail. Os campos locais `account_type`, `phone`, `address`, `city`, `uf`, `adopter_profile` e `ngo_profile` não constam no schema remoto obtido.

A tabela de eventos encontrada chama-se `event_log` (singular), com `id`, `created_at`, `user_id`, `action` e `metadata`; `user_id` referencia `user`. O snapshot local usa o mesmo nome singular. A observação anterior de `events_log` (plural) não corresponde ao snapshot lido nesta auditoria e deve ser confirmada no painel Xano antes de qualquer ação de dados.

Os endpoints remotos obtidos para login, `/me` e signup são os fluxos genéricos antigos: usam `role`, signup define `member` e os três enviam o registro do usuário ao logger. Os endpoints remotos de redefinição também enviavam registros completos ao logger. O endpoint remoto `logs/user/my_events` filtra por `$auth.id`, mas retorna cada linha de evento sem projeção; metadata histórico pode conter hashes/tokens e fica visível ao próprio usuário autenticado. Nenhum desses endpoints foi modificado remotamente.

### Snapshot local versionado

O arquivo `xano/table/user.xs` contém perfis específicos e índices únicos planejados para email, CPF e CNPJ. A coluna `role` (`admin`/`member`) foi mantida separada de `account_type` (`ADOTANTE`/`ONG`); novo signup local atribui `member`, nunca `admin`.

Os endpoints locais de autenticação foram atualizados para usar `account_type` e dados dos perfis. Signup exige e-mail/senha, mantém `role=member` separado de `account_type`, e o magic-link não seleciona o campo de autorização que não usa. Esse snapshot **não está implantado** na branch live. Login/signup/`me` passam somente `account_type` como metadata; redefinição e magic-link passam `{}`. O logger aplica uma allowlist `pick:["account_type"]` e usa `{}` como padrão, de modo que outros campos enviados por engano não sejam persistidos. Os callsites locais foram inspecionados. O endpoint local `logs/user/my_events` preserva os campos de evento, mas mascara metadata com `{}` para não devolver valores históricos potencialmente sensíveis.

## Contrato local dos endpoints

- `auth/signup`: exige `account_type` (`ADOTANTE` ou `ONG`), e-mail e senha; valida presença dos campos específicos e consulta duplicidade de email/CPF/CNPJ. O armazenamento usa o tipo Xano `password` do schema. Validação de formato de CPF/CNPJ, validação de UF e política de telefone ainda não estão implementadas/confirmadas no snapshot.
- `auth/login`: consulta por e-mail, verifica a senha com `security.check_password` e cria token Xano com expiração de 24 horas. As credenciais inválidas usam resposta genérica.
- `auth/me`: exige autenticação Xano e retorna perfil próprio. A resposta inclui dados pessoais do usuário autenticado; revisar a necessidade de cada campo antes da integração do frontend.
- `reset/magic-link-login`: valida token de uso único, validade e estado usado, cria token Xano de 24 horas e retorna `authToken`/`user_id`. A seleção de `role` foi removida por não ser usada pelo fluxo.
- `reset/update_password`: exige autenticação, compara senha/confirmação e atualiza o campo Xano `password`.
- Logging: não colocar usuário completo, senha, hash, token, email ou dados de perfil em metadata. O `user_id` permanece no campo próprio do evento para correlação interna.
- `logs/user/my_events`: a consulta continua restrita a `$auth.id` e preserva os campos do evento, mas devolve `metadata: {}`. Isso também evita expor metadata histórico inseguro; não apaga os valores antigos armazenados no Xano.

## Configuração necessária para futura integração Reflex

O projeto ainda não define URL da API do Xano em `rxconfig.py`, `requirements.txt` ou nas instruções de setup. A URL base do grupo de API precisa ser obtida do workspace/branch escolhido; não deve ser presumida a partir do ID do workspace.

Quando o contrato estiver implantado e aprovado, configurar uma variável de ambiente do processo backend, por exemplo `XANO_API_BASE_URL`, com o endereço confirmado do grupo de API. Não inserir URL/token funcional no repositório, não expor token Xano em estado/JavaScript do navegador e não registrar corpo de requisição, senha ou cabeçalhos de autenticação. Esta variável ainda não é lida pelo frontend nesta etapa.

## Plano manual de migração não destrutivo

1. O responsável pelo workspace deve confirmar o destino e criar/autorizar uma branch de desenvolvimento. No momento da auditoria, somente `v1` live estava disponível e o CLI reportou `Allow Push: false`.
2. Exportar/registrar o schema atual e identificar dependências de `role`, eventos e autenticação na branch de desenvolvimento. Não alterar nem remover os valores históricos `admin/member`.
3. Adicionar nessa branch, de forma aditiva, `account_type`, contato e perfis; definir tipos, campos obrigatórios e validações aceitos; configurar índices únicos globais para e-mail e adequados para CPF/CNPJ segundo as capacidades confirmadas do Xano.
4. Definir uma classificação explícita para usuários existentes antes de preencher `account_type`. Não inferir `ADOTANTE`/`ONG` a partir de `role`; preservar registros não classificados até decisão do responsável.
5. Confirmar a tabela `event_log` e seu relacionamento com `user`; não renomear tabela nem apagar eventos durante a migração. Aplicar os endpoints locais só depois que o schema compatível existir na branch de desenvolvimento.
6. Aplicar na branch de desenvolvimento os callsites sanitizados de todos os escritores e a projeção segura de `logs/user/my_events`; eventos históricos permanecem armazenados e devem ser avaliados pelo responsável sem exportá-los para logs/clientes.
7. Executar testes Xano nessa branch: signup válido/inválido para cada tipo, email/CPF/CNPJ duplicados, login, `/me`, magic link, reset de senha e leitura de eventos; inspecionar logs para provar ausência de dados sensíveis. Registrar evidência antes de qualquer promoção.
8. Obter a URL do grupo de API dessa branch e configurar `XANO_API_BASE_URL` no processo backend. Só então implementar/testar o cliente Reflex em mudança própria.
9. Antes de produção, revisar o plano com o responsável. Rollback deve restaurar endpoints/schema sem apagar registros; não remover `role`, contas antigas ou tabelas de eventos como ação automática.

## Pendências confirmadas

- Criar/autorizar uma branch Xano de desenvolvimento; a única branch encontrada é live e o workspace bloqueia push pelo CLI.
- Aprovar o mapeamento explícito de contas existentes para `ADOTANTE`/`ONG` sem associá-las aos papéis de autorização.
- Confirmar validação de CPF/CNPJ, UF e normalização de telefone; garantir as restrições no backend, não só no frontend.
- Verificar no Xano os metadados históricos de autenticação e confirmar que os novos callsites sanitizados foram aplicados; a correção local não muda logs remotos existentes.
- Aplicar no Xano remoto a sanitização dos escritores e a projeção de `logs/user/my_events`; metadata já armazenado não é apagado por estas alterações locais.
- Confirmar a URL base e o contrato publicado do grupo de API antes de integração Reflex.
- Rever a lista de campos pessoais devolvidos por login e `/me`.
