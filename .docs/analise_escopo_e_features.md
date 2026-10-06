# Análise de escopo e funcionalidades — Sync Disc

**Data da análise:** 05/10/2026  
**Branch analisada:** `feature/profile-enrichment-v1`  
**Commit de referência:** `26d1a54` (`feat: add logo to the application pages`)

## 1. Objetivo e critério adotado

Este documento compara três fontes:

1. o produto realmente implementado no código atual;
2. o escopo mínimo de apresentação, chamado de **MVP**, definido na seção 20 do Documento Mestre e repetido no `README.md`;
3. a visão funcional completa descrita pelos RF01–RF18, pelas regras de domínio e pelo Documento Técnico.

Essa separação é necessária porque a documentação usa “escopo” em dois níveis diferentes. O MVP contém apenas cadastro, autenticação, quiz, resultado DISC, perfil, missões e XP. O mesmo Documento Mestre também descreve uma visão mais ampla, com projetos, certificados, experiências, atributos, conquistas, perfil público, curtidas, histórico e DISC observado.

### Legenda

| Status | Significado |
|---|---|
| ✅ Presente | Existe fluxo utilizável no backend e no frontend. |
| 🟡 Parcial | Há implementação, mas uma parte relevante da regra documentada não existe. |
| ❌ Ausente | Não foram encontrados modelo, persistência, serviço, rota ou interface que materializem a funcionalidade. |
| 🆕 Extra do MVP | Está implementada, embora não faça parte do escopo mínimo do MVP. |
| ⚠️ Divergente | A implementação contradiz uma regra documental. |

## 2. Resumo executivo

- O **MVP mínimo está funcionalmente coberto**: cadastro, login/logout, quiz narrativo, resultado DISC, perfil, missões e XP possuem implementação.
- A aplicação atual avançou bastante além do MVP. Os três itens explicitamente excluídos do MVP — **projetos, certificados e perfil público** — já estão presentes.
- Também foram adicionados conquistas, níveis, histórico de evolução, DISC observado, dashboard unificado, perfil profissional enriquecido, currículo PDF, perfil público por nome, dados de demonstração e uma identidade visual própria.
- Na visão completa RF01–RF18, continuam totalmente ausentes: **atributos secundários (RF09), experiências profissionais (RF13) e curtidas (RF16)**.
- Missões adaptativas, ciclo completo das missões, histórico temporal do DISC e geração completa do Currículo Vivo estão apenas parcialmente atendidos.
- Existe uma divergência de negócio grave: a documentação determina que conquistas não alteram atributos nem DISC, mas cada conquista atualmente soma `+5` em Influência no DISC observado.
- A documentação não acompanhou o código mais recente. O `README.md` ainda diz que o projeto está em fase inicial, e os arquivos de progresso não registram perfil profissional, currículo PDF nem a adição da marca.
- Não há suíte de testes automatizados no repositório. A análise validou compilação, carregamento da aplicação e algumas rotas básicas, mas não substitui testes funcionais completos em navegador.

## 3. Funcionalidades existentes na aplicação atual

### 3.1 Conta e autenticação

- ✅ Cadastro com nome, e-mail, senha e curso.
- ✅ Validação básica de e-mail e unicidade no banco.
- ✅ Senha persistida por hash do Werkzeug.
- ✅ Login e logout por sessão Flask.
- ✅ Proteção das rotas privadas com `login_required`.
- ✅ Endpoint autenticado `/auth/me`.

**Evidências principais:** `backend/controllers/auth_controller.py`, `backend/services/auth_service.py`, `backend/repositories/user_repository.py` e tabela `users` em `backend/database/schema.sql`.

### 3.2 DISC Inicial e classe

- ✅ Quiz narrativo com 12 situações e quatro alternativas D/I/S/C por pergunta.
- ✅ Exigência de resposta para todas as perguntas.
- ✅ Cálculo de pontuação e percentual por dimensão.
- ✅ Identificação da dimensão predominante.
- ✅ Persistência de um único resultado inicial por usuário.
- ✅ Bloqueio para impedir que o DISC Inicial seja refeito.
- ✅ Geração da classe inicial: Executor Estratégico, Comunicador, Colaborador ou Analista.
- ✅ Tela de resultado e exposição por JSON.

**Evidências principais:** `backend/services/disc_service.py`, `backend/services/profile_service.py`, `backend/controllers/disc_controller.py`, `frontend/pages/disc_quiz.html` e `frontend/pages/disc_result.html`.

### 3.3 Missões e XP

- ✅ Catálogo persistido com nove missões ordenadas.
- ✅ Criação automática das missões para novos usuários.
- ✅ Estados efetivamente usados: `Bloqueada`, `Pendente` e `Concluida`.
- ✅ Ativação da próxima missão disponível.
- ✅ Conclusão automática por eventos do domínio: DISC, acesso ao perfil, criação de projetos e criação de certificados.
- ✅ Recompensa de XP concedida uma única vez por missão concluída.
- ✅ Listagem em página própria e no dashboard.

Catálogo atual:

| Ordem | Missão | XP |
|---:|---|---:|
| 1 | Realizar DISC Inicial | 100 |
| 2 | Completar Perfil | 50 |
| 3–5 | Primeiro, segundo e terceiro projetos | 150 cada |
| 6–8 | Primeiro, segundo e terceiro certificados | 150 cada |
| 9 | Continuar Evolução | 0 |

**Limitações encontradas:**

- “Completar Perfil” é concluída ao carregar o perfil, sem verificar se os dados profissionais estão preenchidos.
- Não existem prazo, aceite, ignorar, abandonar, expirar ou penalidade.
- Não existem missões adaptativas baseadas no menor indicador DISC.
- Depois do terceiro projeto e do terceiro certificado, novos registros não geram XP.

**Evidências principais:** `backend/services/mission_service.py`, `backend/repositories/mission_repository.py`, `backend/controllers/mission_controller.py` e `frontend/pages/missoes.html`.

### 3.4 Níveis e evolução geral

- ✅ Cálculo de nível com marcos em 0, 200, 500, 900 e 1.400 XP.
- ✅ Progresso percentual e XP restante para o próximo nível.
- ✅ Indicadores de projetos, certificados, missões, conquistas e XP.
- ✅ Histórico persistido dos eventos de DISC, missão, projeto, certificado e conquista.
- ✅ Exibição dos oito eventos mais recentes.

**Limitação:** o catálogo atual distribui no máximo 1.050 XP. Portanto, o nível 5, que exige 1.400 XP, não pode ser alcançado apenas com os fluxos hoje disponíveis.

**Evidências principais:** `backend/services/evolution_service.py`, `backend/repositories/evolution_repository.py` e tabela `evolution_events`.

### 3.5 Projetos

- 🆕 CRUD autenticado de projetos.
- 🆕 Campos: título, descrição, tecnologias, link opcional e data de criação.
- 🆕 Criação, listagem, detalhe, edição e exclusão.
- 🆕 Integração com missões, conquistas, evolução, DISC observado e perfil público.
- 🆕 Operação tanto em páginas próprias quanto em modal no dashboard.

**Evidências principais:** `backend/controllers/project_controller.py`, `backend/services/project_service.py`, tabela `projects` e páginas `frontend/pages/projeto*.html`.

### 3.6 Certificados

- 🆕 CRUD autenticado de certificados.
- 🆕 Campos: nome, instituição, carga horária, data de conclusão e arquivo opcional.
- 🆕 Upload e download de arquivo local.
- 🆕 Integração com missões, conquistas, evolução, DISC observado e perfil público.
- 🆕 Operação tanto em páginas próprias quanto em modal no dashboard.

**Evidências principais:** `backend/controllers/certificate_controller.py`, `backend/services/certificate_service.py`, tabela `certificates` e páginas `frontend/pages/certificado*.html`.

### 3.7 Conquistas

- 🆕 Catálogo com cinco conquistas: Primeiro Passo, Construtor, Desenvolvendo Habilidades, Explorador e Currículo Vivo.
- 🆕 Desbloqueio automático e idempotente.
- 🆕 Contador de desbloqueadas e apresentação no dashboard, perfil interno e perfil público.

**Evidências principais:** `backend/services/achievement_service.py`, `backend/repositories/achievement_repository.py` e tabelas `achievement` e `user_achievement`.

### 3.8 DISC observado

- 🆕 Persistência de um retrato atual do DISC observado.
- 🆕 Recálculo baseado em dados da plataforma.
- 🆕 Comparação visual entre DISC Inicial e DISC observado.
- 🆕 Exposição no perfil privado, perfil público e JSON.

Fórmula atual:

| Evidência | Efeito atual |
|---|---:|
| Projeto cadastrado | `+10 D` |
| Certificado cadastrado | `+10 C` |
| Missão concluída | `+5 S` |
| Conquista desbloqueada | `+5 I` |

**Limitações:** não há snapshots históricos do DISC, pesos por tipo de projeto/atividade, experiências ou comportamentos observáveis. O sistema sobrescreve o retrato atual em `observed_disc_results`.

**Evidências principais:** `backend/services/observed_disc_service.py`, `backend/repositories/disc_repository.py` e tabela `observed_disc_results`.

### 3.9 Perfil e Currículo Vivo

- ✅ Perfil autenticado com dados pessoais, curso, classe, XP e DISC.
- 🆕 Perfil profissional editável com biografia, objetivo profissional, tecnologias favoritas, GitHub, LinkedIn, portfólio, cidade, estado/região e disponibilidade para estágio.
- 🆕 Upload de currículo tradicional em PDF, limitado a 5 MB e validado por assinatura básica do arquivo.
- 🆕 Visualização consolidada de projetos, certificados, conquistas, indicadores e histórico.
- 🟡 O Currículo Vivo existe como composição do perfil e do dashboard, mas não possui uma entidade própria, uma versão exportável gerada pelo sistema ou experiências profissionais.

**Evidências principais:** `backend/services/professional_profile_service.py`, `backend/repositories/professional_profile_repository.py`, tabela `professional_profiles`, `frontend/pages/_professional_form.html` e `frontend/pages/perfil.html`.

### 3.10 Perfil público

- 🆕 Página pública sem autenticação por ID: `/profile/<id>`.
- 🆕 Página pública por nome: `/perfil/<nome>`.
- 🆕 Endpoint JSON público.
- 🆕 Exibição de dados profissionais, classe, XP, nível, indicadores, DISC inicial e observado, trajetória, projetos, certificados e conquistas.
- 🆕 Download público do currículo PDF quando cadastrado.

**Limitações:** nomes não são identificadores únicos; quando duas contas têm o mesmo nome, a rota por nome retorna conflito. Também não há configuração de privacidade por seção ou para o currículo PDF.

**Evidências principais:** `backend/controllers/public_profile_controller.py`, `backend/services/public_profile_service.py` e `frontend/pages/perfil_publico.html`.

### 3.11 Interface, demonstração e operação

- 🆕 Dashboard autenticado em uma tela com abas para jornada, perfil, projetos, certificados, missões, conquistas e evolução.
- 🆕 Identidade visual azul, símbolos vetoriais, marca e tratamentos específicos para XP, DISC, missões e conquistas.
- 🆕 Layouts com regras responsivas em CSS.
- 🆕 Seed idempotente com duas contas de demonstração e dados de jornada.
- ✅ Endpoint técnico `/health`.

**Evidências principais:** `frontend/pages/index.html`, `frontend/assets/js/main.js`, `frontend/assets/css/*.css`, `frontend/assets/images/`, `backend/seed_demo.py` e `backend/app.py`.

## 4. Comparação com o escopo mínimo do MVP

O Documento Mestre define sete capacidades mínimas. Todas possuem implementação identificável.

| Item do MVP | Status | Observação |
|---|---|---|
| Cadastro | ✅ Presente | Cria usuário, inicia sessão e cria missões. |
| Login / Logout | ✅ Presente | Sessão Flask e senha com hash. |
| Quiz Narrativo | ✅ Presente | 12 perguntas, uma execução por usuário. |
| Resultado DISC | ✅ Presente | Pontuações, percentuais e predominância. |
| Perfil | ✅ Presente | Perfil inicial e enriquecimento profissional. |
| Missões | ✅ Presente | Catálogo fixo e progressão automática. |
| XP | ✅ Presente | Recompensa por missão e níveis derivados. |

### Conclusão sobre o MVP

Não foi encontrada uma feature integralmente ausente entre os sete itens do MVP. Existem limitações dentro de missões e XP, mas elas não impedem o fluxo mínimo definido para apresentação.

## 5. Features descritas na visão completa, mas ausentes ou incompletas

### 5.1 Matriz RF01–RF18

| Requisito | Status | Situação atual |
|---|---|---|
| RF01 — Cadastro de usuário | ✅ Presente | Cadastro completo para o protótipo. |
| RF02 — Login | ✅ Presente | Login, logout e sessão. |
| RF03 — Quiz Narrativo | ✅ Presente | Quiz com 12 cenários. |
| RF04 — Cálculo do DISC Inicial | ✅ Presente | Pontuação, percentual e predominância. |
| RF05 — Classe Inicial | ✅ Presente | Classe derivada da dimensão predominante. |
| RF06 — Geração de Missões | 🟡 Parcial | Catálogo padrão existe; geração adaptativa não existe. |
| RF07 — Conclusão de Missões | ✅ Presente | Conclusão automática; demais estados não existem. |
| RF08 — Sistema de XP | 🟡 Parcial | XP existe, mas não cobre toda ação relevante e a curva atual possui nível inalcançável. |
| RF09 — Sistema de Atributos | ❌ Ausente | Não há Liderança, Comunicação, Organização, Criatividade, Trabalho em Equipe ou Capacidade Analítica persistidos/calculados. |
| RF10 — Sistema de Conquistas | ⚠️ Divergente | Existe, mas altera o DISC observado, contrariando a regra cosmética. |
| RF11 — Cadastro de Projetos | ✅ Presente | CRUD completo. |
| RF12 — Cadastro de Certificações | ✅ Presente | CRUD e arquivo opcional. |
| RF13 — Cadastro de Experiências | ❌ Ausente | Nenhuma tabela, serviço, rota ou tela de experiências. |
| RF14 — Currículo Vivo | 🟡 Parcial | Agregação visual existe; faltam experiências e geração/exportação própria. |
| RF15 — Perfil Público | ✅ Presente | Página por ID e nome, sem autenticação. |
| RF16 — Sistema de Curtidas | ❌ Ausente | Nenhum modelo, contador, endpoint ou interface. |
| RF17 — Histórico de Evolução | 🟡 Parcial | Há oito eventos recentes; faltam histórico completo, filtros e séries de atributos/DISC. |
| RF18 — DISC Observado | 🟡 Parcial | Há retrato atual; faltam histórico temporal, evidências ricas e regras documentadas de pesos. |

### 5.2 Outras lacunas documentais relevantes

| Funcionalidade/regra descrita | Situação |
|---|---|
| Missões adaptativas pela menor dimensão DISC | ❌ Ausente. |
| Estados Disponível, Aceita, Ignorada, Abandonada e Expirada | ❌ Ausentes; só Bloqueada, Pendente e Concluída são usados. |
| Prazo de missão | ❌ Ausente no esquema e na aplicação. |
| Penalidade por abandono/expiração | ❌ Ausente. |
| Foto de perfil | ❌ Ausente, embora seja listada nas informações do perfil público. |
| Experiências no perfil e no currículo | ❌ Ausentes. |
| Evolução dos atributos secundários | ❌ Ausente. |
| Evolução histórica do DISC | ❌ Ausente; existe apenas o valor atual. |
| Evolução de classe | ❌ Ausente; a classe permanece derivada do DISC inicial. |
| Compartilhamento social dedicado | 🟡 Parcial; existe URL pública, mas não há ação ou integração de compartilhamento. |
| Visualização pública de perfis | ✅ Presente. |
| Empresas, vagas, match, recomendações por IA, mentorias, ranking, integração com LinkedIn e dashboard institucional | ❌ Ausentes e corretamente mantidos como visão futura. |

## 6. Features presentes fora do escopo atual do MVP

### 6.1 Itens explicitamente excluídos do MVP que já existem

| Item marcado como “Sem” no MVP | Situação atual |
|---|---|
| Projetos | 🆕 CRUD completo e integrado à gamificação. |
| Certificados | 🆕 CRUD completo, arquivo opcional e integração à gamificação. |
| Perfil Público | 🆕 Página pública rica por ID e por nome. |
| Empresas | Continua ausente. |
| Busca avançada | Continua ausente. A consulta exata por nome não equivale a busca avançada. |
| Recomendação automática | Continua ausente. |
| Inteligência artificial | Continua ausente. |
| Chat | Continua ausente. |
| Integrações externas | Não há integração funcional; links para GitHub, LinkedIn e portfólio são apenas URLs informadas pelo usuário. |

### 6.2 Outros incrementos além do mínimo

- 🆕 Conquistas automáticas.
- 🆕 Níveis e barra de progressão.
- 🆕 Histórico de evolução e indicadores.
- 🆕 DISC observado.
- 🆕 Perfil profissional enriquecido.
- 🆕 Currículo PDF enviado pelo usuário e download público.
- 🆕 Perfil público acessível por nome.
- 🆕 Endpoints JSON para dashboard e perfil público.
- 🆕 Dashboard unificado com gerenciamento em modais.
- 🆕 Seed de demonstração.
- 🆕 Identidade visual, marca, símbolos e maior tratamento responsivo.

Esses incrementos fazem sentido para a visão completa do produto, mas deixam de ser “fora do escopo” somente se o escopo oficial for atualizado. Hoje, pela hierarquia documental do repositório, eles continuam fora do MVP publicado.

## 7. Divergências entre documentação e implementação

### 7.1 Conquistas alteram o DISC observado

O Documento Mestre e o Documento de Domínio dizem que conquistas são cosméticas e não alteram atributos nem DISC. A implementação usa o número de conquistas para somar Influência (`I`) no DISC observado.

**Impacto:** a principal métrica comportamental do produto viola uma regra expressa de negócio. É necessário remover esse peso ou atualizar formalmente a regra do produto antes de mantê-lo.

### 7.2 Regra do DISC observado foi implementada sem decisão formal

O Documento de Domínio mantém fórmula e pesos como pendências. O código definiu pesos fixos por contagem de projetos, certificados, missões e conquistas, mas `.docs/decisions.md` está vazio.

**Impacto:** o comportamento existe, mas não há justificativa, versão ou histórico da decisão. Isso dificulta validar se o indicador tem significado e torna mudanças futuras arbitrárias.

### 7.3 “Completar Perfil” não mede perfil completo

A missão é concluída quando `get_profile()` é executado depois do DISC. Biografia, objetivo, links, localização, tecnologias e currículo podem continuar vazios.

**Impacto:** o nome e a recompensa da missão não correspondem à ação verificada.

### 7.4 Currículo Vivo e currículo PDF são conceitos misturados

A visão técnica afirma que o produto não deve depender exclusivamente de um currículo estático. A aplicação monta uma visão viva, mas também adicionou upload de PDF e lhe deu destaque no perfil público, sem geração automática desse arquivo.

**Impacto:** o PDF pode ser entendido como o currículo principal, enquanto o Currículo Vivo continua incompleto por não conter experiências.

### 7.5 Documentação de status desatualizada

- O `README.md` informa que o projeto está em fase inicial para implementação futura, embora a aplicação já possua a maior parte do produto.
- `backend/progress_backend.md` e `frontend/progress_frontend.md` não registram as alterações do commit de perfil profissional nem as da marca.
- `.docs/decisions.md` não contém as decisões já consolidadas no código.

**Impacto:** a documentação deixou de funcionar como fonte oficial de verdade, apesar de o próprio projeto exigir essa função.

## 8. Riscos e limitações técnicas observados

Esta não foi uma auditoria completa de segurança ou qualidade, mas os seguintes pontos interferem diretamente na confiabilidade das features:

1. **Ausência de testes automatizados:** não há arquivos de teste para autenticação, cálculo DISC, XP, missões, permissões, uploads ou CRUDs.
2. **Arquivos de usuários versionados:** dois PDFs de certificados e um currículo estão rastreados pelo Git em `backend/uploads/`. Isso cria risco de privacidade e mistura dados enviados com o código-fonte.
3. **Segredo de sessão padrão:** a aplicação usa `sync-disc-dev-secret` quando `SECRET_KEY` não está configurada.
4. **Sem proteção CSRF aparente:** os formulários autenticados que alteram ou excluem dados não usam token CSRF.
5. **Upload de certificado pouco restrito:** ao contrário do currículo, o arquivo de certificado não tem limite de tamanho nem validação de tipo/conteúdo.
6. **Currículo público por padrão:** qualquer visitante que conheça o perfil pode baixar o PDF, sem opção de visibilidade.
7. **Nome público não único:** a rota amigável falha com conflito quando dois usuários têm o mesmo nome; falta um slug público único.
8. **Histórico limitado:** somente oito eventos recentes são retornados e não há paginação ou visão integral.
9. **Qualidade não mensurada dos RNFs:** tempo inferior a três segundos, compatibilidade móvel real, acessibilidade e escalabilidade não possuem testes ou métricas.

## 9. Validações realizadas nesta análise

- Leitura dos documentos oficiais: Documento Mestre, Documento Técnico e Documento de Domínio.
- Leitura do `README.md` e dos registros de progresso de backend e frontend.
- Inspeção do esquema SQLite, models, repositories, services, controllers, templates, JavaScript e CSS.
- Inspeção do histórico Git até o commit de referência.
- Compilação de todos os módulos Python com `python -m compileall -q backend`: **aprovada**.
- Carregamento da aplicação Flask e enumeração das rotas: **aprovados**.
- Smoke checks:
  - `/health`: 200;
  - `/login`: 200;
  - `/cadastro`: 200;
  - `/dashboard` sem sessão: 302 para autenticação;
  - perfil público inexistente: 404.

Não foram executados testes ponta a ponta completos porque o repositório não contém suíte de testes nem configuração de navegador automatizado.

## 10. Recomendações priorizadas

### Prioridade imediata — alinhar regra e documentação

1. Decidir se conquistas realmente podem influenciar o DISC. Pela documentação atual, a resposta é não; o peso em `I` deve ser removido ou a regra deve ser formalmente alterada.
2. Atualizar Documento Mestre, Documento de Domínio, `README.md`, registros de progresso e `.docs/decisions.md` para refletir o produto entregue.
3. Definir oficialmente se projetos, certificados, perfil público e enriquecimento profissional passaram a integrar o novo MVP.
4. Remover dados de usuários do versionamento e estabelecer uma política de uploads e privacidade.

### Próximo ciclo funcional

1. Implementar experiências profissionais, pois elas são parte central do Perfil, do DISC observado e do Currículo Vivo documentados.
2. Definir e implementar atributos secundários.
3. Completar o motor de missões com missões adaptativas, estados, prazos e regras de abandono/expiração.
4. Criar snapshots do DISC observado para permitir evolução histórica real.
5. Corrigir a missão “Completar Perfil” para validar critérios objetivos.
6. Ajustar a curva de XP ou criar novas fontes de XP para tornar todos os níveis alcançáveis.

### Qualidade e proteção do protótipo

1. Criar testes para os fluxos críticos de autenticação, DISC, concessão idempotente de XP, missões, isolamento de dados por usuário e uploads.
2. Exigir `SECRET_KEY` por ambiente e adicionar proteção CSRF.
3. Validar tamanho, extensão e conteúdo dos certificados enviados.
4. Criar controle de visibilidade do perfil e do currículo PDF.
5. Criar slug público único para substituir a dependência do nome.

## 11. Conclusão

O Sync Disc já deixou de ser uma estrutura inicial e possui um MVP demonstrável, além de várias partes da visão ampliada. O fluxo central — conta, DISC, classe, missões, XP e perfil — está presente. Projetos, certificados, conquistas, evolução, DISC observado e perfil público transformaram o protótipo em uma aplicação mais completa do que o MVP documentado.

O principal problema atual é de alinhamento: o código avançou, mas o escopo oficial, as decisões de negócio e os registros de progresso não avançaram junto. Antes de expandir para novas features, vale consolidar a versão vigente do produto e resolver as divergências do DISC observado, do significado de “perfil completo” e da privacidade dos arquivos. Na sequência, experiências, atributos, missões adaptativas e histórico real do DISC são as maiores lacunas para cumprir a visão completa descrita na documentação.

## Resumo

### Situação geral

O MVP mínimo está implementado. Cadastro, login/logout, quiz narrativo, resultado DISC, perfil, missões e XP possuem fluxos funcionais. A aplicação também avançou além desse MVP e já entrega partes importantes da visão completa do Sync Disc.

### O que existe atualmente

- Autenticação por sessão, cadastro e logout.
- Quiz DISC Inicial com 12 perguntas, resultado persistido e classe inicial.
- Catálogo de missões fixas, progressão automática e concessão de XP.
- Níveis, indicadores e histórico recente de evolução.
- CRUD de projetos e certificados, incluindo arquivo opcional de certificado.
- Conquistas automáticas.
- DISC observado calculado por projetos, certificados, missões e conquistas.
- Perfil autenticado e perfil profissional enriquecido.
- Currículo PDF enviado pelo usuário.
- Perfil público por ID e por nome.
- Currículo Vivo apresentado por meio de projetos, certificados, conquistas, indicadores e trajetória.
- Dashboard unificado, seed de demonstração e identidade visual própria.

### O que falta no escopo completo documentado

- Sistema de atributos secundários, como Liderança, Comunicação e Organização.
- Cadastro de experiências profissionais.
- Sistema de curtidas.
- Missões adaptativas baseadas no DISC.
- Estados completos de missão, prazos e penalidades.
- Histórico temporal do DISC observado.
- Evolução de classe.
- Foto de perfil.
- Currículo Vivo completo, com experiências e geração/exportação própria.
- Controle de privacidade e compartilhamento social dedicado.

### O que foi adicionado além do MVP

Os três itens explicitamente excluídos do MVP original já foram implementados:

- projetos;
- certificados;
- perfil público.

Também foram adicionados conquistas, níveis, evolução, DISC observado, perfil profissional, currículo PDF, perfil público por nome, dashboard em abas, dados de demonstração e identidade visual.

### Principais divergências

1. Conquistas deveriam ser apenas cosméticas, mas atualmente aumentam a dimensão `I` do DISC observado.
2. A missão “Completar Perfil” é concluída apenas ao acessar o perfil, mesmo que ele esteja vazio.
3. O nível 5 exige 1.400 XP, mas as missões atuais distribuem no máximo 1.050 XP.
4. As regras e os pesos do DISC observado foram implementados sem registro em `.docs/decisions.md`.
5. O `README.md` e os registros de progresso não representam todas as funcionalidades atualmente entregues.
6. Arquivos enviados por usuários estão versionados no Git e o currículo pode ser baixado publicamente sem configuração de privacidade.

### Leitura funcional do estado do produto

| Área | Estado atual |
|---|---|
| MVP mínimo | Completo |
| Autenticação e DISC Inicial | Funcionais |
| Missões e XP | Funcionais, com regras incompletas |
| Projetos e certificados | Funcionais e fora do MVP original |
| Perfil e Currículo Vivo | Parcialmente completos |
| Conquistas | Funcionais, com divergência de regra |
| DISC observado | Funcional como retrato atual, sem histórico |
| Evolução | Funcional como indicadores e eventos recentes |
| Experiências, atributos e curtidas | Ausentes |
| Documentação de escopo | Desatualizada em relação ao código |
| Testes automatizados | Ausentes |

### Próxima decisão recomendada

Antes de adicionar novas funcionalidades, o projeto deve definir oficialmente qual é o novo MVP e atualizar sua documentação. Em seguida, deve corrigir a influência indevida das conquistas no DISC, proteger os arquivos dos usuários e ajustar as regras de perfil, XP e missões. Depois desse alinhamento, as maiores prioridades funcionais são experiências profissionais, atributos secundários, missões adaptativas e histórico do DISC observado.
