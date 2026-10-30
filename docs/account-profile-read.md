# Consulta do próprio perfil — Etapa 23.3.2

**Implementação somente local, não publicada.** O arquivo `xano/api/authentication/account/profile_GET.xs` prepara GET `account/profile` no grupo Authentication existente. Não está integrado ao Reflex. Nenhum endpoint de autenticação ou schema foi modificado; não existe PATCH nesta entrega. RF-03/RF-07 permanecem parciais.

## Evidência e snapshot

Estado inicial: branch `main`, commit `c33ecdeaa556dbe5eacde1e1c5cd22ab0a549df2`, sem alterações locais. GETs administrativos Meta API, com branch `v1`, `include_draft=false`, `records=false` e `env=false`, confirmaram user 897554, Authentication 434180/canonical `yFqRLsBC`, ausência de `account/profile` e sete endpoints existentes neste grupo. Listagem sem próxima página.

Snapshot separado: [manifesto](../backups/xano-definitions/20261030T230124178457Z-account-profile/manifest.json), capturado em 30/10/2026 às 23:01:24.178457 UTC. Contém `user.xs`, login/me/signup publicados e metadados permitidos do grupo, com IDs e SHA-256. As quatro fontes correspondem ao snapshot original após normalização de comentários/espaços/metadados de exportação. Os hashes exatos das fontes remotas e dos arquivos locais estão separados no manifesto. Nenhum arquivo original foi sobrescrito.

Não contém registros, credenciais, valores de ambiente ou configurações Swagger sensíveis. Metadados do grupo são uma projeção parcial: propriedades não retornadas permanecem null, sem inferir defaults. Não é exportação integral do grupo, do workspace ou backup do banco. Sem histórico completo, triggers, middleware ou dados; esses itens exigem revisão própria antes de publicação. O plano Free não oferece isolamento neste projeto.

## Contrato local

- Método/rota: `GET /account/profile`, relativa ao grupo Authentication.
- Autenticação: `auth = "user"`; Bearer validado pelo mecanismo Xano.
- Entrada declarada: vazia. Sem ID, parâmetros de proprietário ou leitura de `$input`.
- Consulta: um único `db.get user`, por `$auth.id`, com output explícito; sem senha, material de recuperação ou role.
- Falhas: ausência/invalidade de Bearer é tratada pela autenticação nativa; registro ausente usa `notfound` e tipo diferente de ADOTANTE/ONG usa `accessdenied`. Mensagem fixa `Perfil indisponivel.`, sem interpolar dados.
- Resposta: somente envelope `data`, nunca o usuário bruto.
- Sem efeitos persistentes: nenhuma escrita, auditoria, função auxiliar, chamada HTTP, Lambda, storage ou migração.

| Campo de data | Origem/representação |
|---|---|
| id, name, email, account_type | Campos próprios selecionados da conta autenticada; email nullable preservado |
| phone, address, city, uf | Campos próprios; null convertido em texto vazio apenas na resposta |
| adopter_profile | Objeto filtrado somente para ADOTANTE; null para ONG |
| ngo_profile | Objeto filtrado somente para ONG; null para ADOTANTE |

ADOTANTE recebe apenas `cpf_masked`, `about_me`, `adoption_preferences` e `consents`. ONG recebe apenas `cnpj_masked` e `description`. Não retornar `password`, `password_reset`, `authToken`, `role`, `birth_date`, documentos completos ou chaves internas adicionais.

## Documentos e dados legados

Documento só é considerado quando é texto numérico ou utiliza a formatação tradicional CPF/CNPJ. Há trim, normalização, rejeição de dígitos todos iguais e validação de ambos os verificadores. Valor ausente, objeto/array/número, formato inválido ou verificadores incorretos produz máscara null. Documento válido produz `***.***.***-` ou `**.***.***/****-` concatenado somente aos dois últimos dígitos. Sem lançamento de exceção com conteúdo do documento e sem reutilizar validação que possa falhar expondo entradas.

Perfis e níveis aninhados ausentes/não objetos são tratados como `{}` em memória. Arrays e strings contendo JSON não são aceitos como objetos nem decodificados. O registro original não é corrigido.

Campos futuros são somente projeções; não comprovam existência ou cadastro desses dados:

| Campo | Default e filtragem |
|---|---|
| about_me | `""`; somente texto, trim e máximo de apresentação 1.000 caracteres |
| species, sizes, age_ranges | `[]`; apenas strings não vazias até 50 caracteres, únicas, até 20 itens |
| preferred_sex | null; texto opcional até 50, sem taxonomia definitiva |
| preferred_city | `""`; texto até 120 |
| preferred_uf | `""`; normalizar e aceitar somente uma das 27 UFs |
| description do pet | `""`; texto até 1.000 |
| consents.discoverable_by_ngos | false, salvo booleano true explícito |
| consents.allow_ngo_contact | false, salvo booleano true explícito |
| description da ONG | `""`; texto até 2.000 |

Esses limites truncam somente a representação de leitura dos campos novos/descritivos, nunca o valor armazenado. Chaves não aprovadas não são copiadas. Retornar consentimento próprio não concede descoberta ou contato a terceiros; não há esses recursos neste endpoint.

## Cache e publicação futura

O código declara `Cache-Control: private, no-store` por `util.set_header`, com substituição, e acrescenta `Vary: Authorization`. A sintaxe está documentada e foi validada; cabeçalhos efetivos não foram inspecionados por HTTP. Autenticação rejeitada antes da stack pode não passar por esses headers, sem retornar perfil.

Antes de qualquer publicação, revisar e confirmar cache do **novo endpoint** desativado no Xano e ausência de cache compartilhado em proxies. Os endpoints existentes consultados mostram cache inativo, mas isso não substitui configurar/verificar o recurso novo. Não alterar cache global, grupo ou rotas existentes nesta etapa.

Publicação exige autorização específica e novo GET de metadados para conferir concorrência/drift. Revisar histórico/debugger: os intermediários da consulta incluem JSON privado, embora a resposta não os exponha. Definir retenção e mascaramento sem enfraquecer sanitização existente. Verificar middleware/triggers relevantes sem presumir sua ausência. Nenhum push/sync global é necessário ou autorizado.

## Validação e limites

- Validador oficial XanoScript: aprovado, zero avisos.
- Onze verificações novas cobrem auth/$auth.id, allowlists, erros, perfis por tipo, defaults, filtros de legado, máscara, ausência de efeitos, headers e hashes do snapshot.
- Cálculos CPF/CNPJ extraídos do arquivo foram conferidos offline com bases numéricas sintéticas; sem consulta de documentos reais.
- Verificações estáticas e aritméticas não executam um runtime Xano. Não comprovam códigos HTTP, semântica efetiva de todos os filtros, comportamento do gateway ou política de histórico.
- Testes funcionais controlados de auth, dados legados, headers, isolamento entre contas e falhas permanecem pendentes de ambiente/contas e autorização específicos. Não executá-los automaticamente contra live.

Não foi feita integração Reflex; portanto sua prévia permanece somente leitura. Recuperação desta entrega é local e seletiva: remover/restaurar somente o novo endpoint, testes e documentos. O snapshot de definições não permite restaurar registros do banco.
