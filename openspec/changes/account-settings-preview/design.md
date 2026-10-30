# Design

## Context

Ver proposal.md. Home usa seções locais protegidas e componentes compartilhados. LoginState fornece somente nome e tipo seguros. Não há leitura detalhada ou atualização de perfil no serviço local. O Design System documenta cores, inputs e cards reutilizáveis.

## Goals / Non-Goals

**Goals:** prévia Reflex 0.9.12 por tipo, componentes visuais compartilhados e cobertura offline de privacidade/navegação.

**Non-Goals:** editar rascunhos, persistir, consultar perfis, alterar sessão/cadastro/Xano ou concluir RF-03/RF-07.

## Decisions

- Criar módulo visual account_settings.py importado pela Home. Receber heading existente como composição evita dependência circular e duplicação do padrão.
- Usar campos somente leitura e ausência de salvar, em vez de estados editáveis descartáveis. Evita reter dados, sugerir persistência ou precisar limpar rascunhos no logout.
- Nome usa display_name; e-mail e demais campos vazios. Não ampliar AuthenticatedUser nem chamar auth/me.
- Guardar conteúdo com can_view_home e account_type; fallback vazio para tipo desconhecido. Sem eventos novos.
- Contato/localização da ONG ficam em um único bloco, sem duplicação; Dados da organização contém nome/e-mail.
- Preferências usam campos vazios de prévia, organizados em grade responsiva com espaço para múltiplos valores futuros. Nenhum conjunto definitivo de opções.
- Cards, mensagens, inputs e segurança compartilhados; consentimentos disabled/false, sem estado. Logout existente preservado.
- Grade com minmax(0, 1fr), largura 100% e min_width 0; campos empilhados em mobile. Labels associados, dicas e limites visíveis. Usar props confirmadas na instalação e compilar.

## Risks / Trade-offs

- Prévia pode parecer operacional → aviso no topo, campos read_only e nenhuma ação salvar.
- Sessão transitória → preservar bloqueio existente e explicar limites sem prometer revogação remota.
- Testes de árvore não provam pixels → verificar viewports offline se ferramenta disponível, registrar limites e roteiro manual sem login live.

## Migration Plan

Sem migração de dados ou publicação. Reversão local limitada ao módulo visual/importação, testes e documentos desta mudança; demais recursos preservados.

## Correção 23.2.1 — nome da sessão

O responsável confirmou organização visual correta e relatou nome ausente. Inspeção offline confirmou `display_name` serializado e vinculado por `value` reativo (não `default_value`). O CSS Radix aplica cor e WebkitTextFillColor próprios ao input interno somente leitura, sobrepondo a cor herdada do contêiner. Aplicar explicitamente a cor de texto documentada ao input interno apenas no campo de nome, com placeholder separado, seguindo a técnica existente no login. Não alterar autenticação, valor dos outros campos ou navegação. A contribuição dessa sobreposição para o relato visual requer confirmação no navegador após a correção. Testar valores reais de estado local, troca válida de nome, perda de sessão e logout, além da expressão reativa e estilos emitidos.
