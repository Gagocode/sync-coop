# Progresso da documentação do produto

## 2026-10-06 — Primeiro dashboard corporativo

**Funcionalidade:** acompanhamento de engajamento dos colaboradores da organização no painel atual do gestor.

**Arquivos criados:** `backend/services/activity_service.py`, `backend/services/corporate_dashboard_service.py`, `frontend/pages/_corporate_dashboard.html`, `backend/tests/test_corporate_dashboard.py`.

**Arquivos alterados:** schema e inicialização do banco; modelo e repositório de usuários; repositório de missões; serviços de autenticação, perfil profissional, projetos, certificados, DISC e missões; controlador de páginas; template principal; `.docs/decisions.md`; registros de progresso geral, backend e frontend.

**Resumo:** última atividade persistida em UTC, cálculo centralizado por tempo decorrido, quatro indicadores e listagem somente de leitura. Uma única consulta fornece colaboradores e setores para lista e totais. Dados legados sem atividade permanecem nulos e são classificados como inativos.

**Validação:** oito testes automatizados aprovados em banco temporário, cobrindo limites de 7/15 dias, migração idempotente, isolamento organizacional, consulta única, eventos, edições idênticas, leituras, XP idempotente e renderização/visibilidade do painel. Executar em `backend`: `python -m unittest discover -s tests -v`. Conferência visual em navegador desktop/celular ainda pendente.

**Impacto:** gestores visualizam engajamento da própria organização sem alterações em CSS, navegação global ou regras de gamificação. Missões corporativas, ranking, permissões novas, IA e notificações continuam fora desta entrega.

## 2026-10-06

### Atualização do posicionamento para desenvolvimento profissional corporativo

**Arquivos:** `README.md`, `project.md`, `.docs/documento_mestre.md`, `.docs/documento_tecnico.md`, `.docs/documento_dominio.md`, `.docs/decisions.md`.

**Resumo:** documentação reposicionada de uma plataforma universitária para um sistema gamificado de desenvolvimento e acompanhamento de colaboradores em organizações. Registrados organização, setor, gestor, colaborador, missões corporativas e a finalidade do dashboard gerencial, com os limites de escopo informados.

**Impacto:** os documentos centrais passam a comunicar a direção de produto corporativa. Nenhum código ou comportamento implementado foi alterado por este registro.

## 2026-10-06

### Base organizacional mínima

**Resumo:** iniciada a implementação de `Organization` e `Sector`, com extensão nula e compatível da tabela `users`, setup explícito da primeira organização/gestor, CRUD de setores e associação manual de usuários a setores. Incluídos os critérios de bootstrap, escopo de visibilidade e exclusão de setor em `.docs/decisions.md`.

**Impacto:** a estrutura organizacional passa a apoiar a evolução corporativa sem criar entidades duplicadas de identidade nem reprocessar dados de gamificação.
