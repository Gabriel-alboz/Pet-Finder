# Design

## Context

Ver proposal.md. Git inicial main/c33ecde, limpo. GETs Meta API em workspace 151970/v1 confirmaram user 897554, Authentication 434180/canonical yFqRLsBC e ausência de account/profile. Snapshot independente em backups/xano-definitions/20261030T230124178457Z-account-profile; manifesto com horário UTC, IDs, hashes e inventário. Definições user/login/me/signup coincidem após normalização de comentários e metadados. Nenhum registro foi consultado.

## Goals / Non-Goals

**Goals:** um único endpoint local de leitura, auth user, seleção por $auth.id e projeção fechada, sem dependências de funções ou Lambda.

**Non-Goals:** publicação, PATCH, mudança de schema, dados, autenticação, cache dos endpoints existentes ou integração Reflex. RF-03/RF-07 permanecem parciais.

## Decisions

- Preferir operações nativas documentadas em XanoScript 2.7.1, sem exigir Lambda ou serviços externos no plano Free.
- db.get usa output restrito aos campos comuns e perfis; não lê password/reset/role/nascimento como campos de saída. JSON interno pode conter nascimento, mas ele nunca integra a projeção.
- Preconditions genéricas antes de acessar o perfil: registro existente e classificação válida.
- JSON não objeto (inclusive string JSON serializada e arrays) vira objeto vazio apenas em memória. Nenhum json_decode de conteúdo legado, correção automática ou escrita.
- Documentos: aceitar apenas string numérica ou formatação tradicional, rejeitar sequências repetidas e verificar dígitos CPF/CNPJ antes de concatenar máscara fixa + substr final de dois dígitos. Inválido retorna null, sem exceção nem função que registre auditoria.
- Campos futuros: about_me/descrição limitados a 1000/2000; preferências reconstruídas, listas só de strings de até 50 caracteres, únicas e limitadas a 20; textos cidade/UF/descrição limitados e UF validada. Sexo livre opcional até 50 nesta projeção, sem definir taxonomia. Consentimentos exigem comparação estrita com true. Ausência usa defaults; não representa implementação do consentimento ou descoberta.
- util.set_header documentado para Cache-Control: private, no-store e Vary: Authorization; configurar cache do novo endpoint desativado antes de publicação. Sem mudança no grupo ou endpoints existentes.
- Não reutilizar auth/me ou logger: ambos poderiam produzir auditoria. Zero function.run, chamadas HTTP ou operações de escrita no novo arquivo.
- Testes são estáticos e verificações offline dos cálculos extraídos, não um runtime Xano nem evidência de HTTP live. Validador oficial verifica sintaxe. Headers/401/404/403, tipos legados e cache efetivo ainda precisam de validação controlada autorizada.

## Risks / Trade-offs

- Sem sandbox → nada será publicado; revisão e autorização específicas para próximos passos.
- Snapshot parcial de definições → group metadata exclui swagger/segredos; não serve como backup completo de configurações ou registros.
- História/debugger da plataforma pode reter intermediários → revisar retenção/mascaramento do novo recurso antes de publicar; não alterar política global nesta etapa.
- Metadados não comprovam execução → registrar separadamente sintaxe, verificações estáticas e testes funcionais pendentes.

## Migration Plan

Não há migração. A entrega local é reversível pela remoção seletiva do novo arquivo; não restaurar snapshot global. Publicação futura deve revalidar drift, ausência de colisão da rota, compatibilidade de headers, cache desativado e permissões. Snapshot de definições não recupera registros.
