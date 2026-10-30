# Tasks

## 1. Preservação e contrato

- [x] 1.1 Conferir metadados publicados por GET e criar snapshot separado sem registros/segredos; verificar IDs, inventário, horário e hashes no manifesto.
- [x] 1.2 Revisar proposta, especificação e design da consulta local frente aos contratos existentes, sem alterar identidade ou frontend.

## 2. Endpoint local e evidências

- [x] 2.1 Implementar GET próprio sem efeitos persistentes e testes estáticos/offline para auth, projeções, legado, documentos e headers; aprovar sintaxe no validador Xano.
- [x] 2.2 Documentar contrato, defaults, snapshot, evidências e dependência de autorização/publicação; manter RF-03/RF-07 parciais.

## 3. Verificação integrada

- [x] 3.1 Executar testes Python e OpenSpec estrito, diff/status e comparação dos hashes preexistentes; registrar testes de runtime pendentes sem executá-los no live.
