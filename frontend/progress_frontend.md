
## 2026-09-23

### Funcionalidade
Area autenticada integrada em tela unica

### Arquivos alterados
frontend/pages/index.html, frontend/assets/js/main.js, frontend/assets/css/style.css, frontend/progress_frontend.md

### Resumo
O Dashboard passou a organizar Perfil, Projetos, Certificados, Missoes, Conquistas e Evolucao em paineis por abas, sem navegar para paginas internas. Projetos e certificados agora podem ser listados, adicionados, editados e excluidos em modais, usando os endpoints existentes. Perfil, DISC, conquistas, indicadores e historico ficaram integrados a mesma experiencia, e a missao ativa permanece visivel em todas as abas. Foram removidos da experiencia principal os atalhos para paginas CRUD; links de arquivo, projeto e perfil publico permanecem como destinos externos.

### Impacto
A area autenticada passa a funcionar como um unico produto responsivo, reduzindo a troca de paginas e concentrando as principais tarefas e informacoes no Dashboard. As regras de negocio e os fluxos do backend permanecem inalterados.

## 2026-09-23

### Funcionalidade
Acabamento final do MVP para demonstracao

### Arquivos alterados
frontend/pages/login.html, frontend/pages/perfil_publico.html, frontend/assets/css/style.css

### Resumo
Adicionada caixa com credenciais da conta de demonstracao na tela de login. O perfil publico foi enriquecido com progressao, nivel, indicadores ampliados e conquistas desbloqueadas, reduzindo a sensacao de lista estatica e reforcando o Curriculo Vivo.

### Impacto
A experiencia de demonstracao fica mais fluida para avaliadores, com acesso imediato a dados completos e perfil publico mais consistente com o Dashboard V2 e com a proposta do produto.

## 2026-09-23

### Funcionalidade
Exibicao do DISC Observado

### Arquivos alterados
frontend/pages/perfil.html, frontend/pages/perfil_publico.html, frontend/assets/css/style.css

### Resumo
Adicionada comparacao entre DISC Inicial e DISC Observado no perfil interno, com pontuacoes D/I/S/C lado a lado. O perfil publico passou a exibir o DISC Observado com texto indicando que ele e calculado pelas atividades realizadas na plataforma.

### Impacto
Usuarios e visitantes conseguem visualizar a diferenca entre o resultado inicial do quiz e o perfil observado pelas acoes do Curriculo Vivo, sem permitir refazer o DISC Inicial e sem adicionar IA ou analises complexas.

## 2026-09-23

### Funcionalidade
Evolucao visual do perfil

### Arquivos alterados
frontend/pages/index.html, frontend/pages/perfil.html, frontend/assets/js/main.js, frontend/assets/css/style.css

### Resumo
Adicionadas secoes simples para exibir nivel atual, XP, proximo nivel, barra de progresso, indicadores de evolucao e historico recente. O dashboard passou a renderizar os dados calculados pelo backend em vez de manter nivel/progresso fixos.

### Impacto
O usuario passa a perceber crescimento ao longo do tempo diretamente no dashboard e no perfil, com cards simples e sem adicionar recomendacoes, IA ou analises avancadas.

## 2026-09-23

### Funcionalidade
Dashboard autenticado em tela única

### Arquivos alterados
frontend/pages/index.html, frontend/assets/css/style.css, frontend/assets/js/main.js

### Resumo
Reestruturada a Home como centro da experiência autenticada, reunindo perfil, XP, progresso, DISC, missão ativa, próximas missões, Currículo Vivo e indicadores de evolução. A interface passou a consumir os endpoints existentes para atualizar os cards sem criar novas regras ou funcionalidades.

### Impacto
A experiência reduz a fragmentação entre telas, dá destaque às missões e torna projetos e certificados visíveis como evidências do Currículo Vivo, com adaptação para desktop, notebook e tablet.

## 2026-09-22

### Funcionalidade
Exibicao do painel de missoes baseado em catalogo

### Arquivos alterados
frontend/progress_frontend.md

### Resumo
Registrada a integracao do painel existente com o progresso de missoes gerado pelo catalogo backend. A tela continua exibindo a missao ativa pelo status Pendente e as proximas pelo status Bloqueada, sem alteracao visual ou de layout.

### Impacto
O usuario sempre visualiza um objetivo ativo e a sequencia de proximas missoes, enquanto a conclusao e a ativacao permanecem automaticas no backend.

## 2026-09-22

### Funcionalidade
Fluxo principal DISC e missoes automaticas

### Arquivos alterados
frontend/pages/missoes.html, frontend/pages/disc_quiz.html, frontend/pages/disc_result.html, frontend/pages/index.html

### Resumo
Removida a acao manual de concluir missao da tela de missoes. A tela de resultado DISC passou a informar que o DISC Inicial ja foi registrado e nao pode ser refeito. O Dashboard deixou de oferecer link de refazer o quiz, mantendo apenas a consulta ao resultado.

### Impacto
A interface passa a refletir o fluxo principal definido para o produto: o DISC Inicial e obrigatorio, nao e repetivel, e a progressao por missoes/XP acontece automaticamente a partir das acoes do usuario.

## 2026-09-18

### Funcionalidade
Pagina de perfil publico

### Arquivos alterados
frontend/pages/perfil_publico.html, frontend/pages/index.html, frontend/pages/perfil.html, frontend/assets/css/style.css

### Resumo
Criada pagina publica simples para exibir nome, curso, classe, XP, DISC Inicial, projetos, certificados e indicadores basicos. Adicionados links para acesso ao perfil publico pelo painel e perfil autenticado.

### Impacto
O frontend passa a apresentar o Curriculo Vivo em uma visao publica clara para recrutadores, professores e colegas, sem funcionalidades sociais.

## 2026-09-18

### Funcionalidade
Interface de certificados do Curriculo Vivo

### Arquivos alterados
frontend/pages/certificados.html, frontend/pages/certificado_form.html, frontend/pages/certificado_detalhe.html, frontend/pages/perfil.html, frontend/pages/index.html, frontend/assets/css/style.css

### Resumo
Criadas telas simples para listar, criar, visualizar, editar e excluir certificados com upload opcional. O perfil passou a exibir automaticamente os certificados cadastrados pelo usuario.

### Impacto
O frontend passa a oferecer o fluxo basico de cadastro de certificados do Curriculo Vivo, sem OCR, validacao externa ou integracoes.

## 2026-09-23

### Funcionalidade
Exibicao de conquistas no dashboard

### Arquivos alterados
frontend/pages/index.html, frontend/pages/perfil.html, frontend/assets/js/main.js, frontend/assets/css/style.css

### Resumo
Adicionada secao simples de conquistas no dashboard e no perfil, exibindo cards das conquistas desbloqueadas e contador de desbloqueadas sobre o total. A interface consome os dados de conquistas retornados pelo perfil JSON.

### Impacto
Usuarios conseguem visualizar os marcos alcancados no Curriculo Vivo sem acao manual de desbloqueio, mantendo cards simples e foco no funcionamento do MVP.

## 2026-09-18

### Funcionalidade
Interface de projetos do Curriculo Vivo

### Arquivos alterados
frontend/pages/projetos.html, frontend/pages/projeto_form.html, frontend/pages/projeto_detalhe.html, frontend/pages/perfil.html, frontend/pages/index.html, frontend/assets/css/style.css

### Resumo
Criadas telas simples para listar, criar, visualizar, editar e excluir projetos. O perfil passou a exibir automaticamente os projetos cadastrados pelo usuario.

### Impacto
O frontend passa a oferecer o fluxo basico de cadastro de projetos do Curriculo Vivo, priorizando funcionamento sem workflow extra ou anexos complexos.

## 2026-09-18

### Funcionalidade
Pagina de missoes fixas

### Arquivos alterados
frontend/pages/missoes.html, frontend/pages/index.html, frontend/pages/perfil.html, frontend/assets/css/style.css

### Resumo
Criada pagina simples de missoes exibindo nome, descricao, status e XP de recompensa, com acao para concluir missoes pendentes. Adicionados links para acesso pelo painel e perfil.

### Impacto
O frontend passa a permitir visualizacao clara de missoes pendentes e concluidas, alem da conclusao manual das missoes fixas do MVP.

## 2026-09-18

### Funcionalidade
Pagina de perfil inicial

### Arquivos alterados
frontend/pages/perfil.html, frontend/pages/index.html, frontend/assets/css/style.css

### Resumo
Criada pagina autenticada de perfil com dados do usuario, XP, classe inicial e resultado DISC Inicial. Atualizado o painel autenticado com link para o perfil.

### Impacto
O frontend passa a exibir uma visao simples e organizada do perfil inicial do MVP, sem adicionar funcionalidades fora do escopo.

## 2026-09-18

### Funcionalidade
Interface do Quiz DISC Inicial

### Arquivos alterados
frontend/pages/disc_quiz.html, frontend/pages/disc_result.html, frontend/pages/index.html, frontend/assets/css/style.css

### Resumo
Criadas telas simples para responder o Quiz Narrativo DISC Inicial e visualizar o resultado com percentuais e dimensao predominante. Atualizado o painel autenticado com links para o quiz e resultado.

### Impacto
O frontend passa a oferecer o fluxo basico para realizacao e visualizacao do DISC Inicial, priorizando funcionamento sem design avancado.

## 2026-09-18

### Funcionalidade
Telas de cadastro e login

### Arquivos alterados
frontend/pages/cadastro.html, frontend/pages/login.html, frontend/pages/index.html, frontend/assets/css/style.css

### Resumo
Criadas telas simples de cadastro e login integradas aos endpoints de autenticacao por formulario. Atualizada a pagina inicial para funcionar como area autenticada basica com acao de logout.

### Impacto
O frontend passa a suportar o fluxo basico do MVP para cadastro, entrada, sessao autenticada e encerramento de sessao.

## 2026-09-18

### Funcionalidade
Estrutura inicial do frontend

### Arquivos alterados
frontend/pages/index.html, frontend/assets/css/style.css, frontend/assets/js/main.js, frontend/assets/images/.gitkeep

### Resumo
Criada a estrutura base com pages e assets separados em css, js e images. Adicionados arquivos iniciais de HTML, CSS e JavaScript para suportar evolucao futura da interface.

### Impacto
O frontend passa a ter uma base organizada para desenvolvimento futuro, sem implementar fluxos de produto ou regras de negocio.
## 2026-10-02

### Funcionalidade
Identidade visual oficial azul e gamificação visual

### Arquivos alterados
frontend/assets/css/identity.css, frontend/assets/js/main.js e todas as páginas em frontend/pages/*.html

### Resumo
Aplicados azul vibrante #0085FF, azul profundo #0056A4 e azul gelo #E0F2FF em todas as rotas. XP usa amarelo; conquistas usam laranja e medalha; evolução usa ciano e turquesa; certificados e DISC C usam violeta. Barras, estados de missão, indicadores DISC, marcos e histórico passaram a ter tratamento visual consistente com dados existentes. Paleta oficial registrada em .docs/design-system.md.

### Impacto
Dashboard, missões, perfil, DISC, resultado, perfil público, projetos, certificados, conquistas e evolução compartilham a mesma identidade de progresso profissional, sem alteração de regras de negócio ou fluxos.

## 2026-10-02 — Símbolos da jornada

### Funcionalidade
Comunicação visual gamificada com símbolos vetoriais

### Arquivos alterados
frontend/assets/images/symbols.svg, frontend/assets/css/symbols.css, frontend/assets/js/main.js e as páginas em frontend/pages/*.html

### Resumo
Criados símbolos para projeto, certificado, missão, conquista, XP, nível, Currículo Vivo, DISC, perfil e evolução. Ícones foram aplicados em marcadores antes preenchidos apenas por letras ou números, nas conquistas desbloqueadas, nas recompensas, no histórico e nas páginas independentes. As conquistas do catálogo usam símbolo associado ao seu tipo real, com medalha de reconhecimento. Sem indicação de raridade, pois o catálogo atual não informa esse atributo.

### Impacto
As entidades e os marcos passam a ser reconhecíveis visualmente sem alterar layout principal, cores, tipografia, responsividade, fluxos ou regras de negócio.
## 2026-10-06

### Funcionalidade
Gestão organizacional mínima

### Arquivos alterados
Páginas de setup, setores e usuários; dashboard, cadastro e perfil; JavaScript da área autenticada.

### Resumo
Criadas telas simples para setup da primeira organização, CRUD de setores e visualização/atribuição de usuários. Links de gestão são exibidos ao gestor. Perfil e dashboard mostram setor quando disponível e preservam curso como legado.

### Impacto
Gestores conseguem iniciar a organização e organizar usuários por setor sem alterar CSS global, identidade visual ou navegação existente.

## 2026-10-06

### Funcionalidade
Reposicionamento documental do produto

### Arquivos alterados
Documentação do produto na raiz e em `.docs/`.

### Resumo
Atualizada a direção documental e visual para desenvolvimento profissional corporativo, incluindo colaboradores, gestores, setores e a finalidade do dashboard gerencial. Nenhuma tela, fluxo ou arquivo de frontend foi alterado.

### Impacto
As diretrizes documentais de interface refletem o novo contexto de aplicação. Este registro não indica que a experiência corporativa esteja implementada no frontend.
## 2026-10-06 — Visão corporativa no painel do gestor

**Arquivos:** criado `pages/_corporate_dashboard.html`; alterado `pages/index.html`.

**Resumo:** seção gerencial renderizada no servidor antes das abas, com total de colaboradores, ativos, atenção, inativos e listagem de nome, setor, engajamento e última atividade em UTC. Incluídos estados sem setor, sem atividade e organização vazia.

**Impacto:** reaproveitamento de cards e listas existentes, sem alteração em CSS, JavaScript, identidade visual, navegação global ou ações administrativas. A seção é exclusiva de gestores com organização e atualiza ao recarregar o painel.

**Validação:** renderização e visibilidade por papel verificadas via cliente Flask. Conferência visual em navegador desktop/celular ainda pendente.
