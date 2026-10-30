# Configurações — prévia da Etapa 23.2

Entrega exclusivamente visual em Reflex 0.9.12, dentro da seção `account` da Home. Seleção usa `LoginState.account_type`, protegida por `can_view_home`. Tipos desconhecidos e sessões inválidas não mostram perfil. Rotas, login, cadastro, sessão, serviço Xano e logout existentes são preservados.

## Conteúdo

| ADOTANTE | ONG |
|---|---|
| Meus dados: nome, e-mail, telefone, endereço, cidade, estado | Dados da organização: nome e e-mail |
| Sobre mim: apresentação, limite proposto 1.000 | Sobre a ONG: descrição institucional, limite proposto 2.000 |
| Pet que procuro: espécie, porte, faixa etária, sexo opcional, cidade/estado de interesse e descrição até 1.000 | Localização e contato: telefone, endereço, cidade, estado, sem duplicar campos |
| Privacidade: descoberta e contato desligados e indisponíveis | Meus pets: aviso e cadastro desabilitado |
| Segurança e logout existente | Segurança e logout existente |

Somente o nome seguro da sessão é preenchido. O e-mail não está disponível no modelo seguro atual e fica vazio. Os demais valores são vazios, com placeholders de indisponibilidade; não são dados fictícios. Todos os campos são somente leitura, sem submissão, salvamento, rascunho, novo estado ou armazenamento no navegador. Não há mensagem de sucesso. Preferências não definem taxonomia definitiva e poderão admitir múltiplos valores no futuro. Nenhuma descrição é persistida.

## Privacidade e dependências

Não há consulta detalhada ao Xano ou chamada adicional a auth/me. Contatos não são publicados. Consentimento não é armazenado no frontend; futura descoberta dependerá de consentimento explícito/revogável validado no backend e projeção mínima, sem documentos, credenciais ou endereço privado. Contato depende ainda de chat autorizado.

RF-03/RF-07 permanecem parciais. Integração futura requer contratos próprios de leitura/atualização, validações e autorização derivada da identidade autenticada, limites aprovados, preservação de CPF/CNPJ e distinção entre dados públicos e privados. E-mail/senha exigem fluxos específicos. Gestão de pets depende de RF-08. A sessão continua transitória e logout continua local, sem revogação Xano.

## Verificação e roteiro manual

Testes offline cobrem blocos por tipo, ausência de perfil para sessão inválida/tipo desconhecido, campos vazios/somente leitura, limites, controles desabilitados, ausência de novos eventos/HTTP, navegação mobile e rotas/guarda existentes. A grade gerada empilha campos abaixo de 48em; áreas de texto só redimensionam verticalmente e cards/textos permitem quebra de linha.

Inspeção visual de pixels ainda pendente: desktop 1440px, tablet 768px e celular 375px/320px; conferir rolagem horizontal, nome longo, labels, áreas de texto, botões e abertura/fechamento do menu. Não há Playwright Python ou browsers de teste no cache local consultado. Validação estrutural/compile não comprova aparência no navegador. Não iniciar sessão live para essa inspeção sem autorização; usar ambiente de prévia offline isolado ou teste manual autorizado pelo responsável.

Resultados dos comandos de validação serão registrados no status do projeto. Nenhuma integração live foi executada nesta etapa.
