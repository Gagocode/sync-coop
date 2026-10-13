# Decisões e pendências — Sync-Coop

**Status:** registro ativo desde 2026-10-13. As seções “Histórico Sync-Disc” abaixo registram a consolidação dos Prompts 1–3; não aprovam regras corporativas. Os originais integrais também estão no Git no commit 746a6ddff3e415b1132892dae4e733b6752f01ec.

## 2026-10-13 — Migração documental do produto

**Decisão vigente:** Sync-Coop passa a ser o produto documentado. A aplicação permanece como protótipo Sync-Disc até implementação própria. Preservam-se arquitetura em camadas, DISC, missões, gamificação e evolução como base a adaptar. O isolamento entre organizações, autorização por escopo e proteção de dados individuais são requisitos do novo produto. Perfil público de contratação, estágio, currículo vivo acadêmico e recrutadores deixam de ser objetivos ativos. Não houve alteração de código, banco ou dependências nesta decisão.

**Critério de status:** “confirmado” indica direção de produto; “implementado” exige evidência no código; “proposta” exige aprovação; “pendente” não pode ser inventado pelo implementador. O Documento de Domínio detalha regras; o Documento Técnico descreve o estado executável. Este registro concentra as questões sem definição suficiente.

### Decisões pendentes centralizadas

| ID | Questão e impacto | Definição necessária |
|---|---|---|
| DC-01 | Como modelar organizações, setores/equipes, múltiplos vínculos, troca e desligamento? Sem isso não há autorização ou migração segura. | Estrutura, temporalidade, transferência e destino dos dados legados |
| DC-02 | Qual a matriz final de permissões por papel, vínculo e finalidade? Sem ela dados pessoais podem ser expostos. | Quem lê/escreve perfil, missão, relatório, exportação e acompanhamento; acesso excepcional |
| DC-03 | Quem pode ver DISC inicial, observado e inferências, e com qual finalidade? Risco de uso indevido em RH. | Política de acesso, informação ao titular, reaplicação, retenção e revisão metodológica |
| DC-04 | Qual destino de perfil público, currículo e links externos legados? Tensão com isolamento corporativo. | Desativação, migração, consentimentos/autorizações aplicáveis, compatibilidade de URLs e arquivos |
| DC-05 | Como se criam e atribuem missões por organização/equipe/pessoa, inclusive mudança de equipe? | Criadores, destinatários, sobreposição de escopos, elegibilidade e vigência |
| DC-06 | Quais estados e transições de missão são aprovados? Sem isso aceite, rejeição, abandono e expiração são ambíguos. | Fluxo, atores, evidências, prazo/fuso, reabertura e efeito sobre recompensa |
| DC-07 | O que conclui CONTINUE_EVOLUTION e “perfil completo” no novo contexto? Há desvio entre nome e gatilho legado. | Critérios verificáveis e decisão de manter, renomear ou retirar cada missão |
| DC-08 | Quais eventos corporativos concedem/revertem XP e alteram atributos? Não transportar valores acadêmicos automaticamente. | Catálogo versionado, valores, reversão, idempotência de criação repetida e níveis |
| DC-09 | Conquistas são cosméticas ou alteram DISC observado? O domínio antigo diz cosméticas, o código aplica +5 I. | Escolher regra validada e plano de correção/migração dos dados |
| DC-10 | Quais eventos qualificam atividade, janelas e limiares de inatividade? Sem isso sinalizações são arbitrárias. | Taxonomia, período, exceções, configuração e explicação |
| DC-11 | Quais fórmulas e públicos dos relatórios? Agregados pequenos podem reidentificar pessoas. | Denominadores, período, atualização, supressão e exportação |
| DC-12 | Como registrar e usar ações preventivas relacionadas ao trabalho sem diagnóstico automatizado? | Responsáveis, revisão humana, metodologia, dados mínimos, validação jurídica e de SST |
| DC-13 | Quais regras de retenção, exclusão, auditoria e acesso a logs/arquivos se aplicam? | Política por categoria de dado e finalidade, inclusive uploads legados |
| DC-14 | SQLite/uploads locais atendem ao SaaS pretendido? A implementação atual não tem isolamento multiempresa. | Estratégia de persistência, escala, backup, migração e testes de isolamento |
| DC-15 | Rankings, penalidades e comparações individuais existirão? Podem gerar exposição e incentivos indevidos. | Decisão de escopo, finalidade, visibilidade e privacidade; até lá não aprovados |
| DC-16 | Qual identidade visual corporativa e linguagem de indicadores? O design existente é do protótipo. | Decisão de marca e validação de usabilidade/acessibilidade |
| DC-17 | Missões adaptativas por DISC e atributos secundários do domínio antigo são pertinentes? Podem rotular pessoas sem base suficiente. | Decidir finalidade, regra verificável, revisão metodológica e visibilidade; até lá não aprovados |

### Divergências de fonte identificadas

- O documento antigo chamava conquistas de cosméticas; o serviço atual de DISC observado soma +5 I por conquista. Não foi escolhida uma nova regra nesta migração.
- A missão “perfil completo” legada é acionada no envio do DISC/classe, sem verificar todos os campos profissionais.
- O currículo público permanece acessível no código, embora o objetivo corporativo exija política de privacidade e escopo.
- Os logs dos Prompts 1–3 provam apenas fluxos individuais do Sync-Disc; não validam o Sync-Coop.

### Verificação desta migração documental

Em 2026-10-13, foram conferidos os 12 arquivos Markdown alterados, os links locais do README, a presença de DISC, missões por organização/equipe/pessoa, prazo, inatividade, dashboards distintos, relatórios, permissões, isolamento e limites de apoio relacionados à NR-1. A busca por referências acadêmicas restantes encontrou somente contexto comparativo e registros históricos, identificados como tais. git diff --check passou; git diff --name-only mostrou apenas Markdown. Não foram executados testes da aplicação nesta tarefa exclusivamente documental; não há validação funcional do Sync-Coop. As fontes originais permanecem recuperáveis no commit informado acima.

## Histórico Sync-Disc — decisões dos Prompts 1–3

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
