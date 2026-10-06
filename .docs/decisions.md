# Registro de Decisões do Produto

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
