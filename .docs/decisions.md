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
