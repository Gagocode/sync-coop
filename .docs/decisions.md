# Decisões arquiteturais — Sync Disc

## 2026-10-13 — Dashboard como caminho canônico da área autenticada

O dashboard em `/dashboard` continua sendo uma página Flask/Jinja com abas e JavaScript convencional. Suas abas são `dashboard`, `profile`, `projects`, `certificates`, `missions`, `achievements` e `evolution`. Fragmentos de URL abrem a aba correspondente; `#projects/new`, `#projects/edit/<id>`, `#certificates/new` e `#certificates/edit/<id>` também abrem os modais existentes. Isso permite redirecionar URLs antigas sem criar outra tela ou alterar o contrato de persistência.

### Levantamento antes da mudança

| Área | Templates e componentes encontrados | Rotas HTML e controller | Consumidores do dashboard |
|---|---|---|---|
| Entrada | `login.html`, `cadastro.html` | `/login`, `/cadastro` (`page_controller`); `/auth/register`, `/auth/login`, `/auth/logout` (`auth_controller`) | formulário de logout |
| Dashboard | `index.html`, `_professional_form.html` | `/dashboard` (`page_controller`) | `main.js`, `professional-profile.js` |
| Perfil privado | `perfil.html`, `_professional_form.html` | `/perfil/`, `/perfil/profissional`, `/perfil/curriculo`, `/perfil/json` (`profile_controller`) | `/perfil/json`, POST `/perfil/profissional`, download `/perfil/curriculo` |
| Missões | `missoes.html` | `/missoes/`, `/missoes/json` (`mission_controller`) | `/missoes/json` |
| Projetos | `projetos.html`, `projeto_form.html`, `projeto_detalhe.html` | `/projetos/` GET/POST, `/novo` GET, `/json` GET, `/<id>` GET, `/<id>/editar` GET/POST, `/<id>/excluir` POST (`project_controller`) | POST CRUD e dados incluídos em `/perfil/json`; `/projetos/json` continua disponível |
| Certificados | `certificados.html`, `certificado_form.html`, `certificado_detalhe.html` | `/certificados/` GET/POST, `/novo` GET, `/json` GET, `/<id>` GET, `/<id>/editar` GET/POST, `/<id>/excluir` POST, `/<id>/arquivo` GET (`certificate_controller`) | POST CRUD, download e dados incluídos em `/perfil/json`; `/certificados/json` continua disponível |
| DISC | `disc_quiz.html`, `disc_result.html` | `/disc/` GET/POST, `/disc/resultado`, `/disc/resultado.json` (`disc_controller`) | consulta DISC incluída em `/perfil/json` |
| Perfil público | `perfil_publico.html` | `/profile/<id>`, `/profile/<id>/json`, `/profile/<id>/curriculo`, `/perfil/<username>` (`public_profile_controller`) | link externo na aba Perfil |
| Infraestrutura | sem template | `/`, `/health` (`app.py`); `/auth/me` (`auth_controller`) | — |

`index.html` contém sete painéis e dois modais de CRUD; `_professional_form.html` é compartilhado com `perfil.html`. `main.js` controla abas, carregamento de perfil/missões, renderização das coleções, modais e requisições CRUD. `professional-profile.js` envia o formulário profissional. O CSS do dashboard carrega `style.css`, `journey.css`, `identity.css`, `symbols.css` e `professional-profile.css`, nessa ordem. A identidade oficial está em `.docs/design-system.md`. `identity.css` aplica as cores oficiais sobre regras anteriores de `style.css`; essa sobreposição existente foi preservada para evitar mudança visual sem comparação em navegador.

### Destino das rotas antigas

| Rota GET | Decisão |
|---|---|
| `/perfil/`, `/missoes/`, `/projetos/`, `/certificados/` | Redirecionar para a aba respectiva do dashboard. |
| `/projetos/novo`, `/certificados/novo` | Redirecionar para a aba e abrir o modal de criação. |
| `/projetos/<id>/editar`, `/certificados/<id>/editar` | Validar posse/existência e redirecionar para o modal de edição. |
| `/projetos/<id>`, `/certificados/<id>` | Validar posse/existência e redirecionar para a aba; os cards do dashboard exibem os campos dos antigos detalhes. |
| `/perfil/curriculo`, `/certificados/<id>/arquivo` | Manter como downloads. |
| Autenticação, quiz/resultado DISC, perfil público, `/health`, endpoints JSON | Manter; possuem propósito ou consumidores distintos. |

Os POSTs existentes de perfil profissional, projetos e certificados permanecem com os mesmos métodos e endereços, usados pelos formulários e pelo dashboard. Em envios HTML válidos, passam a redirecionar para a aba canônica. Em erros de criação via HTML, `perfil.html`, `projeto_form.html` e `certificado_form.html` continuam como resposta de compatibilidade. Não foi assumido que ausência de chamada no frontend implica ausência de consumidor externo.

Os templates de listagem e detalhe independentes de missões, projetos e certificados foram removidos depois da verificação de que nenhum controller os renderizava. As regras de negócio, o esquema SQLite, os arquivos enviados e os endpoints JSON não foram alterados.

### Limitações e próxima etapa

- O fallback de erro para POST HTML ainda usa três templates legados; remover exige definir outro tratamento para clientes sem JavaScript e para integrações que postam formulários.
- As camadas de CSS existentes ainda contêm regras sobrepostas. Uma limpeza exige comparação visual com uma versão de referência para provar equivalência.
- A revisão de services, transações, XP e consistência de regras de domínio pertence à etapa posterior; esta decisão trata apenas de apresentação e navegação.
- A validação automatizada cobre contratos HTTP e persistência em banco temporário. Um smoke test em navegador validou abas, modais, formulários, redirecionamentos e operações de criação/edição/exclusão; capturas desktop e mobile foram inspecionadas. Não há captura de referência anterior para uma comparação visual por pixels.

## 2026-10-13 — Consultas puras e comandos transacionais no Sync Disc

### Problemas corrigidos

- `get_profile` concluía missão, concedia XP e persistia classe durante uma leitura. Consultas de perfil público, missões, conquistas, evolução e DISC Observado também podiam gravar estado. Essas gravações foram retiradas das consultas.
- Criação de projeto/certificado e envio do DISC combinavam registros, XP, conquistas, histórico e DISC Observado em commits independentes. Falhas intermediárias podiam deixar dados parciais.
- Projetos e certificados escolhiam missões por chaves fixas e contagem em serviços separados, sem despachar pela coluna `tipo_evento`.

### Decisões

- O envio do DISC grava resultado e classe inicial, registra o evento e conclui missões `DISC_COMPLETED` e `PROFILE_COMPLETED`. Cadastro cria as missões iniciais. Criação de projeto/certificado registra a evidência e despacha `PROJECT_CREATED`/`CERTIFICATE_CREATED`. O serviço de missões valida a evidência persistida e a ordem da missão no mesmo tipo de evento; o repositório faz atualização condicional de status e XP na mesma conexão. Conquistas e DISC Observado são atualizados no comando.
- A transação pertence ao serviço de entrada. Repositórios compartilham a conexão ativa sem commit próprio; a fronteira externa confirma ou desfaz todo o comando. O upload novo de certificado é removido em caso de rollback. A substituição de currículo restaura o arquivo anterior se a gravação falhar.
- `reconcile_existing_progress` roda após inicializar o esquema, antes de atender requisições. Reconcilia classe, missões documentadas, conquistas, histórico e DISC Observado de dados anteriores de forma idempotente. Não é acionado por consultas. A inicialização pode demorar proporcionalmente ao número de usuários; uma migração operacional explícita poderá substituí-la se houver escala maior.
- Não houve migração de esquema, mudança de rotas, formatos JSON ou alteração da stack. Os limiares de nível, pesos do DISC Observado e recompensas do catálogo foram mantidos. Exclusão de projeto/certificado recalcula o DISC Observado; XP e conquistas já concedidos permanecem, como no comportamento anterior.

### Pendências de domínio e limites

- `CONTINUE_EVOLUTION` não possui limiar documentado; permanece sem conclusão automática. Penalidades, atributos secundários e novas regras de XP também não têm definição implementável no domínio atual. Não foram inventados critérios.
- Arquivos antigos de certificados substituídos ou excluídos continuam no armazenamento local, para preservar o comportamento atual. Uma política de retenção/limpeza requer decisão própria.
- Repetir a conclusão de uma missão ou o processamento do mesmo estado não repete XP nem conquistas. POSTs de criação de projeto/certificado continuam criando um novo registro a cada requisição; o contrato atual não possui chave de idempotência para distinguir retry de uma segunda criação legítima. Definir esse contrato exige decisão de produto e atualização coordenada dos consumidores.
- A reconciliação atual é sequencial e executada em toda inicialização. Ela evita duplicar recompensas e histórico, mas pode ser transformada em migração única quando necessário.
- Testes automatizados cobrem leituras repetidas, contratos HTTP, condições de missão, XP, nível, conquistas, DISC Observado, posse de registros, idempotência e rollback de falhas injetadas. Não foi executada validação visual em navegador nesta etapa, pois o frontend não foi alterado.

## 2026-10-13 — Encerramento da consolidação e validação integrada

O estado implementado é Flask/Jinja com dashboard autenticado em `/dashboard`, sete abas e modais de projetos/certificados. Cadastro, login, quiz/resultado DISC, downloads, perfil público e POSTs/JSON conservam suas rotas. Templates `perfil.html`, `projeto_form.html` e `certificado_form.html` continuam como resposta a erros de POST HTML. Os outros templates independentes já haviam sido removidos no primeiro prompt; referências a eles nas tabelas acima e nos registros históricos de progresso descrevem o estado anterior, não arquivos atuais.

A auditoria deste encerramento identificou valores JSON inesperados que causavam exceções 500 em cadastro, DISC, projetos, certificados e perfil profissional. Serviços agora validam tipos; controladores exigem objeto JSON antes de delegar. Erros dessas entradas retornam 400 sem persistir dados. A suíte acrescentou cobertura para entradas inválidas e para a sequência de disponibilidade das missões. Foram removidos `user_repository.add_xp`, `achievement_repository.unlock_for_user`, `mission_repository.list_catalog` e o modelo `MissionCatalogItem`: a busca de referências no código, templates, scripts e testes encontrou apenas suas próprias definições. O atalho de XP também contornava a conclusão condicional de missão.

Validação executada com banco e uploads temporários: `python -m unittest discover -s backend/tests -v` (13 testes, todos passaram), `python -m compileall -q backend` e `git diff --check`. O script opcional `python backend/tests/browser_smoke.py` passou em Chromium: cadastro, primeiro DISC, dashboard e abas em desktop/mobile, CRUD de projeto/certificado, consulta do arquivo, perfil profissional, perfil público e logout/login. Não houve erros JavaScript nem respostas HTTP inválidas locais. O console registrou bloqueio de Google Fonts pela restrição de rede deste ambiente; a interface usou fontes de reserva. Não houve comparação visual por pixels com uma captura de referência. CSS sobreposto e templates de compatibilidade foram preservados, pois não se comprovou equivalência visual ou ausência de consumidores externos.

As pendências de domínio e operação da decisão anterior permanecem: critério para `CONTINUE_EVOLUTION`, semântica de retry de POSTs de criação, política de arquivos antigos de certificados e eventual migração única para reconciliação. Os documentos Mestre e de Domínio contêm requisitos futuros ainda não implementados, como experiências próprias, atributos secundários, missões adaptativas e curtidas. Esses itens não foram adicionados nesta consolidação.
