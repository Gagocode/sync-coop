# Registro de Decisões do Produto

## 2026-10-06 — Primeiro dashboard corporativo e última atividade

**Decisão:** apresentar a visão corporativa no painel atual, somente para gestor com organização, reutilizando os componentes existentes. Os indicadores e a listagem contam apenas `role = 'collaborator'` da organização do gestor. Gestores, contas sem vínculo e usuários de outras organizações não entram nos totais.

**Persistência:** `users.last_activity_at` armazena somente a última atividade em UTC, com precisão de segundos. A migração é idempotente e mantém nulos os dados legados, sem reconstrução de histórico nem criação de auditoria. Datas mais antigas não substituem uma atividade mais recente.

**Eventos:** cadastro no fluxo de sessão, login bem-sucedido, alteração efetiva do perfil profissional, envio de currículo, criação/edição/exclusão de projetos e certificados, conclusão do DISC e conclusão efetiva de missão. O registro ocorre após persistência; a conclusão de missão grava atividade na mesma transação do XP. Edições idênticas e operações rejeitadas não contam. Associação de setor pelo gestor não conta como atividade do colaborador.

**Leituras:** consultas, recálculos e reconstrução do histórico não renovam a data. A regra existente que conclui “Completar Perfil” no primeiro acesso após DISC permanece; sua transição real conta uma vez, sem renovação nos acessos seguintes.

**Cálculo:** tempo decorrido até 7 × 24 horas = Ativo; acima de 7 × 24 horas até 15 × 24 horas = Atenção; acima de 15 × 24 horas = Inativo. Data nula = Inativo, com “Sem atividade registrada”. O cálculo fica centralizado em serviço, sem status persistido ou tarefa agendada.

**Consulta e apresentação:** uma consulta de colaboradores com setor alimenta lista e totais. Usa-se um único instante de referência por carregamento. A seção é renderizada pelo servidor e atualizada ao recarregar o painel; datas exibem UTC explicitamente. Não há novo endpoint público. O dado não é acrescentado aos perfis públicos.

**Limites:** nenhuma alteração em CSS, identidade visual ou navegação global. Sem novas permissões, missões corporativas, ranking, IA, notificações ou ações administrativas na listagem.

## 2026-10-06 — Reposicionamento para desenvolvimento profissional corporativo

**Status:** adotada como direção documental do produto.

**Decisão:** posicionar o Sync Disc como sistema gamificado de desenvolvimento e acompanhamento profissional de colaboradores dentro de organizações. O domínio passa a contemplar organizações, setores e colaboradores, com gestores que acompanham evolução e criam setores e missões. O dashboard gerencial é destinado à visualização de colaboradores, evolução, indicadores, rankings e missões.

**Mantido:** DISC, missões, XP, níveis, conquistas e evolução continuam no núcleo. Certificações e participação permanecem no contexto de desenvolvimento profissional conforme regras existentes.

**Limites:** o produto não substitui ERP, sistemas de RH, folha de pagamento ou controle operacional. Esta decisão não cria IA, integrações, automações, requisitos adicionais de RH nem novas regras de negócio. Não define permissões, fórmulas, catálogo de missões ou implementação do dashboard.

**Motivação:** validações com gestores e profissionais do mercado identificaram maior potencial de aplicação corporativa para acompanhamento da evolução e engajamento de colaboradores.

**Documentos de referência:** `documento_mestre.md`, `documento_tecnico.md`, `documento_dominio.md`, `../project.md`.

## 2026-10-06 — Base organizacional mínima

**Decisão:** manter `users` como identidade principal e adicionar somente `organizations` e `sectors`. A conta recebe `organization_id`, `sector_id` e `role`; gestor e colaborador são papéis, não entidades/tabelas separadas.

**Migração legada:** colunas organizacionais começam nulas nos usuários existentes. Nenhuma empresa, setor ou papel é inferido de `curso`. O campo `curso` e seus dados permanecem como legado. XP, DISC, conquistas e certificados não são recalculados nem alterados.

**Setup inicial:** a primeira organização é criada uma única vez por uma tela autenticada. A pessoa conectada escolhe explicitamente tornar-se gestora. Não há interface para criar organizações adicionais nesta etapa.

**Gestão:** gestores veem usuários da própria organização e contas ainda sem vínculo. A associação explícita a um setor de sua organização também vincula o usuário à organização e define o papel `collaborator`. Setores ocupados não podem ser excluídos; a relação dos setores a organizações não pode ser editada.

**Compatibilidade:** adicionar colunas e tabelas de forma idempotente, preservando IDs e dados existentes. Habilitar enforcement de chaves estrangeiras nas conexões após validar o banco local. A interface mantém o curso como legado quando não houver setor.

**Documentos de referência:** `documento_mestre.md`, `documento_tecnico.md`, `documento_dominio.md`, `../progress.md`.
