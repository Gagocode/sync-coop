# Análise diferencial — Sync-Disc → Sync-Coop

**Status:** documento ativo de migração documental, 2026-10-13. O estudo antigo do Sync-Disc está no Git no commit 746a6ddff3e415b1132892dae4e733b6752f01ec. Esta análise não é plano de implementação nem prova de entrega.

## Critério

“Preservado” significa conceito/regra aproveitável. “Adaptado” exige redefinição corporativa. “Substituído” perde a finalidade anterior. “Descontinuado” deixa de ser objetivo do novo produto, embora o código legado possa continuar existindo. “Adicionado” é requisito confirmado do escopo corporativo, ainda não implementado. “Pendente” não autoriza implementação arbitrária. Detalhes oficiais: Documento Mestre, Documento de Domínio e decisions.md.

| Elemento | Classificação | Situação no código e encaminhamento documental |
|---|---|---|
| Flask/Jinja, serviços, repositórios, SQLite local | Preservado como base técnica | Implementado; evolução de escala e isolamento SaaS a avaliar |
| Dashboard individual com abas | Preservado e adaptado | Implementado para usuário único; tornar experiência do colaborador |
| DISC inicial de 12 perguntas, resultado, D/I/S/C | Preservado e adaptado | Implementado; finalidade corporativa, visibilidade e reaplicação pendentes |
| DISC observado por eventos | Adaptado | Implementado com pesos legados; validade e uso corporativo pendentes |
| Missões de catálogo com tipo_evento e prevenção de XP duplicado | Preservado e adaptado | Implementado individualmente; novos escopos, prazo e validação futura |
| XP, níveis, conquistas, evolução e histórico | Preservado e adaptado | Implementado com parâmetros legados; política corporativa pendente |
| Classes visuais e atributos secundários | Adaptado/pendente | Classe visual implementada; atributos secundários apenas documentados no domínio antigo |
| Missões adaptativas por menor dimensão DISC | Decisão pendente | Previstas em documentos antigos, não implementadas; uso corporativo exige política e revisão metodológica |
| Projetos e certificados individuais | Adaptado | CRUD implementado; utilidade como evidência profissional a validar |
| Perfil profissional, biografia e vínculos externos | Adaptado | Implementado com campos acadêmicos; conjunto corporativo pendente |
| Estudante, curso e disponibilidade para estágio | Substituído/descontinuado | Presentes no esquema e interface; não são objetivos ativos |
| Currículo vivo para contratação e perfil público | Descontinuado como finalidade | Rotas e arquivos ainda ativos; política de desativação/privacidade pendente |
| Recrutadores, busca de perfis e empregabilidade acadêmica | Descontinuado | Não são atores/requisitos do Sync-Coop |
| Curtidas e interação social de perfis públicos | Descontinuado | Previstas no domínio antigo, não implementadas; não fazem parte do escopo corporativo confirmado |
| Experiências acadêmicas, professores e instituições de ensino | Descontinuado como escopo | Não há entidade própria de experiência no código |
| Organizações, equipes, vínculos e papéis | Adicionado | Não implementado |
| Isolamento entre organizações e autorização por escopo | Adicionado | Não implementado |
| Dashboard gerencial e administrativo | Adicionado | Não implementado |
| Missões organizacionais, setoriais/de equipe e individuais com prazo | Adicionado | Não implementado |
| Indicadores de acesso, atividade, inatividade e relatórios | Adicionado | Não implementado |
| Acompanhamento preventivo de fatores relacionados ao trabalho | Adicionado | Não implementado; exige revisão humana e validação regulatória |
| Auditoria corporativa e regras de retenção | Adicionado | Não implementado |
| Ranking, penalidades, inferência DISC para RH | Decisão pendente | Não aprovados; não transferir de referências antigas |

## Divergências documentais e de implementação

1. O documento de domínio antigo afirma que conquistas são cosméticas; observed_disc_service.py atribui +5 I por conquista. O Sync-Coop não adota automaticamente essa pontuação. Decisão de regra pendente.
2. A missão legada chamada “perfil completo” é concluída no comando do DISC/classe, sem verificar todo o perfil profissional. Seu nome e critério precisam de revisão antes de adaptação.
3. A missão CONTINUE_EVOLUTION existe no catálogo sem critério de conclusão documentado e não recebe conclusão automática.
4. O fluxo público de perfil/currículo ainda existe, em tensão com o isolamento de dados corporativos. A documentação nova o descreve apenas como legado, não como recurso autorizado.
5. O aplicativo não registra prazos, organização, equipe, papel ou atividade qualificada. Não é possível calcular os indicadores corporativos pretendidos com o esquema atual.
6. As decisões e os testes dos Prompts 1–3 se referem ao protótipo Sync-Disc. A validação daqueles fluxos não comprova as capacidades do Sync-Coop.

## Caminho de decisão antes da implementação

Definir identidade/vínculos e migração de usuários; política de visibilidade do DISC; destinação do perfil público; ciclo e critérios de missões; eventos relevantes e janelas de inatividade; fórmulas e proteção de agregados; regras corporativas de XP; responsabilidades humanas e dados de apoio relacionados à NR-1. A lista central com impacto e definição necessária está em decisions.md. Nenhum desses itens foi resolvido pela migração documental.
