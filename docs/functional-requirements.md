# Requisitos funcionais — RF-01 a RF-10

Catálogo de requisitos com integração **futura**. Uma interface demonstrativa não representa implementação operacional. RF-06 possui somente interface/navegação parcial na Etapa 21; RF-03/RF-07 possuem prévias visuais parciais na Etapa 23.2. Seus contratos operacionais permanecem pendentes. Ver [estado](project-status.md), [roadmap](roadmap.md) e [arquitetura](architecture.md).

Regras transversais: autenticação e autorização no servidor; `account_type` autenticado, sem usar `role` como substituto; minimização de dados; nenhum token/documento/senha em logs; consentimento para divulgação; estados de erro/vazio claros. Definir contratos e modelo físico antes de criar tabelas/endpoints. Não presumir a existência de recursos Xano futuros.

## RF-01 — Filtros de localização para ONGs

- **Objetivo:** encontrar organizações próximas.
- **Perfil:** usuários autenticados ADOTANTE/ONG.
- **Comportamento esperado:** pesquisar por estado e cidade; listar organizações correspondentes e informar ausência de resultados. Outros critérios serão definidos depois.
- **Regras de negócio:** combinar filtros coerentes, validar localização, exibir somente dados institucionais autorizados, não inventar resultados.
- **Dependências:** dados públicos/localização de ONGs e endpoint de listagem/filtros/paginação a definir.
- **Critérios de aceitação:** estado/cidade retornam apenas correspondências; alteração/limpeza atualiza a pesquisa; zero correspondências mostra vazio; falha mostra erro; contatos privados não são expostos.
- **Status:** futuro. A seção ONGs atual contém apenas aviso e estado demonstrativo, sem listagem ou filtro.

## RF-02 — Filtros de pesquisa para Pets

- **Objetivo:** encontrar animais sem exigir quiz.
- **Perfil:** usuários autenticados, principalmente ADOTANTE.
- **Comportamento esperado:** combinar estado, cidade, espécie, porte pequeno/médio/grande, idade/faixa etária e sexo quando disponível; outras características serão definidas.
- **Regras de negócio:** filtros combináveis; quiz opcional; respeitar disponibilidade para adoção; ausência de característica não deve produzir informação falsa; sem resultados fictícios.
- **Dependências:** catálogo real, localização e vínculo à ONG, atributos normalizados e endpoints de pesquisa/paginação a definir; RF-08.
- **Critérios de aceitação:** pesquisar sem responder quiz; combinação restringe resultados corretamente; limpar restaura catálogo permitido; vazio/erro tratados; dados incompletos identificados.
- **Status:** futuro. Há aviso visual na aba Pets e busca inicial desabilitada; nenhum filtro real.

## RF-03 — Configurações de conta do adotante

- **Objetivo:** manter perfil e preferências com controle de privacidade.
- **Perfil:** ADOTANTE autenticado, somente sua própria conta.
- **Comportamento esperado:** visualizar dados, editar informações permitidas, adicionar descrição pessoal, descrever o pet desejado, atualizar preferências e controlar visibilidade para ONGs.
- **Regras de negócio:** campos editáveis explicitamente permitidos; consentimento antes de divulgação; não expor documentos/credenciais; não permitir alteração de tipo/permissões pelo frontend.
- **Dependências:** contratos de leitura/edição de perfil, preferências e consentimento, validações e autorização a definir.
- **Critérios de aceitação:** salvar campos permitidos e persistir após nova consulta; rejeitar edição de outra conta; dados não autorizados invisíveis a ONGs; retirada de visibilidade efetiva em novas consultas.
- **Status:** parcial, somente prévia visual na Etapa 23.2. ADOTANTE vê dados somente leitura, apresentação, preferências e privacidade com controles desativados. Nome vem da sessão; demais campos vazios. Leitura detalhada, edição, salvamento e consentimento no backend permanecem futuros; RF-03 não concluído.

## RF-04 — ONGs encontrarem adotantes interessados

- **Objetivo:** aproximar ONGs de interessados que autorizem descoberta.
- **Perfil:** ONG autenticada consulta ADOTANTES com consentimento vigente.
- **Comportamento esperado:** consultar perfis/preferências compartilhados, identificar compatibilidade de interesse e iniciar contato permitido sobre oportunidades.
- **Regras de negócio:** sem acesso indiscriminado; consentimento explícito, escopo mínimo, revogação e autorização em cada consulta; não divulgar CPF, nascimento, endereço privado ou credenciais. Contato respeita consentimento/bloqueios a definir.
- **Dependências:** RF-03, modelo de visibilidade/preferências, busca autorizada e RF-05 para contato; contratos a definir.
- **Critérios de aceitação:** perfil sem consentimento não aparece; resposta contém só campos autorizados; revogar remove de futuras buscas; ADOTANTE não acessa recursos exclusivos de ONG; acesso direto indevido é rejeitado.
- **Status:** futuro; nenhuma busca ou interface operacional de descoberta de adotantes.

## RF-05 — Chat entre ONGs e adotantes

- **Objetivo:** comunicação privada entre os dois perfis.
- **Perfil:** ADOTANTE/ONG autenticados, participantes autorizados.
- **Comportamento esperado:** iniciar conversa, enviar/receber mensagens, consultar histórico, identificar participantes e associar pet quando apropriado.
- **Regras de negócio:** somente participantes acessam conteúdo; identidade vem do servidor; não confiar em IDs enviados para conceder acesso; vínculo ao pet não amplia acesso. Definir retenção, bloqueio/abuso e consentimento antes da implementação.
- **Dependências:** modelo de conversas/participantes/mensagens, endpoints de leitura/escrita, paginação e estratégia de atualização a definir; RF-08 para vínculo opcional ao pet.
- **Critérios de aceitação:** participantes trocam mensagens e recuperam histórico; terceiros não acessam por enumeração de IDs; remetente/ordem corretos; falhas não aparentam envio concluído; associação não expõe dados privados.
- **Status:** futuro, sem backend. Não há WebSocket, envio, recebimento ou conversas simuladas.

## RF-06 — Aba Chats no menu lateral

- **Objetivo:** reunir conversas e permitir continuá-las.
- **Perfil:** ADOTANTE/ONG autenticados.
- **Comportamento esperado:** menu Chats com seleção/hover e navegação responsiva; futuramente listar conversas, outro participante, abertura/continuação e mensagens não lidas.
- **Regras de negócio:** mesma proteção da Home; sem acesso anônimo; mensagens de vazio/erro; somente conversas autorizadas. A demonstração deve declarar ausência de backend.
- **Dependências:** menu/guarda existentes para UI; RF-05 para conteúdo real e definição futura de não lidas.
- **Critérios de aceitação:** nesta etapa, selecionar Chats em desktop/mobile mostra título `Chats`, subtítulo `Converse com ONGs e adotantes e acompanhe suas conversas.`, vazio `Você ainda não possui conversas.` e complemento `Quando iniciar uma conversa, ela aparecerá aqui.`; menu mobile fecha; sessão inválida bloqueada. Para conclusão funcional futura, listar/abrir/continuar conversas reais autorizadas, com não lidas em evolução posterior.
- **Status:** **parcial: somente interface/navegação demonstrativa implementada**. Testes offline/compilação não equivalem a validação visual autenticada. Chat real, histórico, participantes e não lidas pendentes; requisito completo não concluído.

## RF-07 — Configurações da conta da ONG

- **Objetivo:** manter perfil institucional e acesso à gestão de pets.
- **Perfil:** ONG autenticada, com autorização para a organização.
- **Comportamento esperado:** visualizar/editar dados institucionais permitidos, descrição, contatos públicos e localização; acessar gerenciamento dos próprios pets.
- **Regras de negócio:** somente usuários autorizados modificam a organização; separar contatos públicos e dados privados; validação no backend; não permitir transferência indevida de propriedade.
- **Dependências:** leitura/edição institucional, modelo de autorização e contratos a definir; RF-08 para pets.
- **Critérios de aceitação:** dados permitidos persistem; outra ONG/ADOTANTE não edita a organização; informações privadas não aparecem publicamente; acesso à gestão preserva propriedade.
- **Status:** parcial, somente prévia visual na Etapa 23.2. ONG vê dados institucionais, descrição, localização/contato, Meus pets e segurança. Campos somente leitura, sem edição, publicação de contatos ou cadastro de pets. RF-07 não concluído; depende de contratos de perfil e RF-08.

## RF-08 — Cadastro e gerenciamento de pets

- **Objetivo:** ONGs manterem seus animais disponíveis para adoção.
- **Perfil:** ONG autenticada e autorizada.
- **Comportamento esperado:** cadastrar fotos, nome, espécie, idade, porte, descrição/características; editar, atualizar disponibilidade e visualizar os próprios pets.
- **Regras de negócio:** ONG não altera pets de outra; propriedade validada no servidor; definir limites/formatos de imagens, campos obrigatórios e estados de disponibilidade; não divulgar informações pessoais indevidas.
- **Dependências:** modelo de pet/vínculo institucional, storage de imagens, endpoints, validação e autorização a definir.
- **Critérios de aceitação:** cadastro válido aparece na gestão da proprietária; edição/disponibilidade persistem; outra ONG e ADOTANTE não escrevem; fotos inválidas são rejeitadas; ausência/erro têm tratamento.
- **Status:** futuro, sem cadastro/gestão implementados. Estado vazio de Pets não é catálogo operacional.

## RF-09 — Quiz de compatibilidade

- **Objetivo:** apoiar descoberta de pets adequados ao estilo de vida.
- **Perfil:** principalmente ADOTANTE autenticado.
- **Comportamento esperado:** questionário de preferências, avaliação de compatibilidade, sugestões de animais reais e acesso aos detalhes recomendados.
- **Regras de negócio:** opcional; busca direta não depende de respondê-lo; definir/validar critérios antes de afirmar compatibilidade; não garantir sucesso de adoção; minimizar e proteger respostas pessoais.
- **Dependências:** perguntas/regras justificadas, catálogo RF-08, perfil/preferências, persistência/endpoints a definir.
- **Critérios de aceitação:** respostas produzem recomendações coerentes com regras documentadas; apenas pets disponíveis autorizados; detalhes acessíveis; vazio tratado; ignorar quiz mantém pesquisa acessível.
- **Status:** futuro. Existe seção demonstrativa sem perguntas, algoritmo ou sugestões implementadas.

## RF-10 — Solicitação de adoção

- **Objetivo:** formalizar e acompanhar interesse do adotante.
- **Perfil:** ADOTANTE solicita; ONG responsável acompanha e decide conforme regras futuras.
- **Comportamento esperado:** identificar adotante, pet e ONG, criar solicitação com status e acompanhar evolução.
- **Regras de negócio:** identidade autenticada, pet elegível, vínculo correto à ONG; definir transições, duplicidade, cancelamento e dados necessários; privacidade e acesso somente às partes autorizadas.
- **Dependências:** RF-08, modelo de solicitação/status, endpoints de criação/leitura/transição e autorização a definir.
- **Critérios de aceitação:** solicitação associa corretamente as partes; cada parte acompanha apenas o autorizado; transição inválida rejeitada; terceiro não acessa; duplicidade/disponibilidade seguem regra aprovada.
- **Status:** futuro; não há fluxo operacional nem novas tabelas/endpoints implementados.

## Planejamento OpenSpec

A mudança [consolidate-project-and-chat-preview](../openspec/changes/consolidate-project-and-chat-preview/proposal.md) especifica somente o comportamento novo desta etapa. O catálogo acima centraliza requisitos futuros e será detalhado em mudanças incrementais antes de cada implementação. Mudanças anteriores, inclusive autenticação e Home, mantêm seu histórico e tarefas; não são arquivadas ou marcadas concluídas por esta documentação.
