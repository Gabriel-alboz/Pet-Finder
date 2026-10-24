# Roadmap incremental

Planejamento futuro, sem autorizar implementação/publicação. Critérios em [RF-01 a RF-10](functional-requirements.md), evidências em [estado](project-status.md).

| Ordem | Entrega | Dependências Xano / infraestrutura | Critério de avanço |
|---|---|---|---|
| 1 | Finalizar testes de autenticação | Contratos atuais; nenhuma tabela nova para matriz manual. Persistência demanda decisão de infraestrutura servidor/cookie seguro | Ambos os perfis, credenciais inválidas, reload, expiração, acesso anônimo, logout e falhas de rede validados com autorização |
| 2 | Configurações ADOTANTE/ONG (RF-03/07) | Leitura/edição permitida, autorização, preferências/consentimento; novos endpoints e possível ampliação de schema | Cada perfil edita somente o permitido; dados privados permanecem protegidos |
| 3 | Gerenciamento de pets (RF-08) | Modelo persistente, vínculo de propriedade à ONG, fotos/storage e endpoints a definir | ONG gerencia somente seus animais; disponibilidade consistente |
| 4 | Pesquisa/filtros (RF-01/02/04) | Listagens ONGs/pets, filtros combinados, localização e descoberta consentida de adotantes; contratos e índices/modelos a definir | Resultados reais, paginação, vazio e privacidade. Busca independente do quiz |
| 5 | Chat/comunicação (RF-05/06) | Conversas, participantes, mensagens, endpoints, autorização e atualização a definir | Histórico privado e envio/recebimento reais; não lidas posteriormente. UI atual não cumpre esta entrega |
| 6 | Quiz com dados reais (RF-09) | Perguntas, regras justificadas, catálogo, preferências/resultados e endpoints a definir | Recomendações verificáveis e detalhes; quiz opcional sem bloquear busca |
| 7 | Solicitações de adoção (RF-10) | Modelo/status, vínculos ADOTANTE/pet/ONG, transições e endpoints autorizados | Acompanhamento restrito às partes; impedir solicitações inconsistentes |
| 8 | Segurança, testes integrados e apresentação | HTTPS/WSS, sessão/privacidade, limites do plano, backups e ambiente autorizado | Evidências, dados minimizados, limites demonstrativos e roteiro acadêmico fiel |

Segurança/testes acompanham todas as etapas. Dependências são **propostas**, não nomes ou existência confirmada de tabelas/endpoints. O ambiente atual é Free sem branch isolada; não presumir staging nem realizar escritas live sem autorização.

Etapa 21 entrega documentação, interface Chats e avisos visuais. Não inclui backend, integrações, commit, push ou deploy. Mudanças anteriores OpenSpec são preservadas, sem arquivamento automático.
