# Login Reflex e Xano

O formulário existente envia e-mail e senha ao backend Reflex. O serviço chama
`POST auth/login`, valida `authToken` e `user_id` e consulta `GET auth/me` com
Bearer. A identidade deve corresponder ao login e `account_type` deve ser
exatamente `ADOTANTE` ou `ONG`. `role` não é usado para inferir o tipo.

## Configuração

Defina `XANO_API_BASE_URL` no ambiente do processo backend Reflex, usando a base
HTTPS do grupo Authentication. A base publicada confirmada é:

```text
https://x8ki-letl-twmt.n7.xano.io/api:yFqRLsBC:v1
```

O cliente de cadastro continua usando a mesma variável e seu comportamento não
foi alterado. O login não usa credenciais do CLI nem tokens da Meta API.
Não colocar tokens em código, arquivos de ambiente versionados ou logs.

## Sessão atual e limites

- Token, identidade, classificação e limite de validade ficam em variáveis
  privadas do estado Reflex; somente nome e tipo necessários à UI são expostos.
- A senha não fica em uma variável de estado; o formulário é limpo após envio.
- Não há token em `rx.Cookie`, localStorage, sessionStorage ou código JavaScript.
- A validade local é limitada a 24 horas, contadas antes da chamada de login.
  A entrada em `/home` consulta `auth/me` novamente e verifica identidade e tipo.
- Durante essa validação, a Home não apresenta dados de conta. Ausência de
  estado, expiração, rejeição ou falha na validação bloqueiam o acesso. Eventos
  de navegação da Home também verificam a sessão privada no servidor.
- O logout limpa somente a sessão local e redireciona ao login. Ele não revoga
  o token Xano, que pode continuar válido remotamente até expirar.

Esta é uma sessão transitória gerenciada pelo backend Reflex, não um mecanismo
de login persistente. Se o Reflex conservar o estado durante um recarregamento,
a rota o revalida; se esse estado não existir mais, exige novo login. Não há
garantia de continuidade entre abas, reinícios, workers ou novos acessos.
"Mantenha-me conectado" permanece desabilitado, sem mudar o layout.

Persistência entre acessos depende de um mecanismo de sessão com identificador
opaco em cookie emitido pelo servidor (`HttpOnly`, `Secure`, `SameSite`), rotação,
expiração e armazenamento compartilhado confiável. Essa infraestrutura não está
configurada e não foi improvisada nesta etapa. O ambiente publicado também
precisa oferecer HTTPS/WSS e armazenamento de estado de backend protegido.

## Verificação sem acessar o Xano

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -v
.venv\Scripts\reflex.exe compile --dry
```

Os testes usam `httpx.MockTransport` e mocks de serviço; não criam usuários,
alteram senhas ou gravam eventos remotos. Cobrem ambos os tipos, respostas
inválidas, falhas de rede, identidade divergente, expiração, serialização do
estado, acesso direto à Home e logout. Testes funcionais no live ainda exigem
autorização separada.

## Evidências e navegação — consolidação da Etapa 21

O responsável informou teste manual com conta existente, login bem-sucedido e acesso à Home. Não foi um teste automatizado do agente. Esse relato não comprova recarga, logout, expiração ou todos os acessos diretos no navegador; esses cenários possuem cobertura offline, com validação manual específica pendente.

Chats é uma seção local de `/home`, sob a mesma guarda e os mesmos eventos de navegação já existentes. Não foi criada rota independente nem alterada a lógica de sessão. A seção é demonstrativa e não chama endpoints de mensagens.

Cadastro permanece separado: envia dados a signup e orienta login, sem estabelecer sessão automaticamente. A senha do login não fica em estado público; não generalizar essa propriedade ao estado dos formulários de cadastro, cuja privacidade merece revisão própria.

Ver [README](../README.md) para execução, [arquitetura](architecture.md), [estado/evidências](project-status.md) e [contratos](xano-authentication-setup.md). Nenhum teste funcional live é executado automaticamente nesta consolidação.
