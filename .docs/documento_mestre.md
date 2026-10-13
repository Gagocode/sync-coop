# Sync-Coop — Documento Mestre

**Status:** especificação ativa de produto, 2026-10-13. O código atual ainda implementa o protótipo Sync-Disc. “Confirmado” neste documento significa objetivo aprovado para o Sync-Coop, não funcionalidade entregue. Regras detalhadas e questões em aberto estão no Documento de Domínio e em decisions.md.

## 1. Produto e problema

O Sync-Coop é uma plataforma corporativa SaaS para desenvolvimento de colaboradores, participação em atividades orientadas por missões, acompanhamento de equipes e produção de indicadores para gestores e profissionais autorizados. Seu propósito é tornar o desenvolvimento visível para a própria pessoa e apoiar acompanhamento humano e preventivo. Indicadores de participação também poderão apoiar a análise organizacional de fatores de risco psicossociais relacionados ao trabalho, com os limites da seção 8.

O produto anterior, Sync-Disc, concentrava-se em estudantes, currículo vivo, perfil público de contratação e ações individuais. Essa finalidade foi substituída. A stack e os mecanismos úteis de DISC, missões, XP, evolução e conquistas são candidatos à adaptação, sujeitos às decisões de domínio e privacidade. O código legado continua funcionando para o domínio anterior e não deve ser descrito como produto corporativo pronto.

## 2. Públicos e atores

| Ator | Responsabilidade pretendida | Limite fundamental |
|---|---|---|
| Colaborador | Consultar seu desenvolvimento, executar missões e acompanhar resultados pessoais | Acessa seus dados e conteúdos a ele destinados |
| Gestor de equipe | Acompanhar participação e pendências das pessoas sob sua responsabilidade; registrar acompanhamento autorizado | Apenas equipe sob vínculo vigente; dados sensíveis dependem de política específica |
| Administrador da organização | Gerir estrutura, vínculos, perfis e configuração autorizada de sua organização | Não recebe acesso irrestrito a dados DISC ou registros sensíveis por ser administrador |
| Profissional autorizado | Consultar indicadores agregados e, quando houver finalidade e permissão explícitas, casos de acompanhamento | Acesso limitado por finalidade, escopo e registro de auditoria |
| Operador da plataforma | Manter o serviço SaaS | Acesso operacional excepcional, controlado e auditado; política ainda pendente |

Uma pessoa poderá ter mais de um vínculo ou papel, mas as regras para múltiplas organizações, substituições e delegação estão pendentes. Nenhum papel implica visibilidade global por padrão.

## 3. Objetivos e requisitos confirmados

| ID | Requisito de produto confirmado | Estado no código atual |
|---|---|---|
| SC-01 | Isolar dados por organização e vincular colaboradores a setores, departamentos ou equipes | Não implementado |
| SC-02 | Oferecer dashboard integrado do colaborador com perfil, DISC, missões, prazos, XP, nível, atributos, conquistas, evolução, histórico e indicadores pessoais | Parcial: dashboard individual sem estrutura corporativa, prazos e indicadores de participação |
| SC-03 | Oferecer visões próprias a gestores, administradores e profissionais autorizados, com permissão por papel, vínculo, escopo e finalidade | Não implementado |
| SC-04 | Permitir missões organizacionais, setoriais/de equipe e individuais, com objetivo, critério, período, responsável, evidências, estado e histórico | Parcial: catálogo individual fixo, sem escopo ou prazo corporativo |
| SC-05 | Distinguir acesso de atividade relevante e sinalizar inatividade, atraso e queda de participação por critérios explicáveis | Não implementado |
| SC-06 | Disponibilizar indicadores e relatórios pessoais e agregados por equipe, setor e organização, respeitando privacidade | Não implementado; há apenas dados individuais de progresso |
| SC-07 | Manter o DISC inicial e distinguir resultado do questionário de indicadores observados e inferências, para desenvolvimento pessoal | Parcial: DISC inicial e observado legados; uso corporativo e visibilidade pendentes |
| SC-08 | Manter gamificação determinística, com XP, níveis, atributos, missões, conquistas e histórico, sem recompensa duplicada | Parcial: mecanismo legado individual implementado; parâmetros corporativos pendentes |
| SC-09 | Apoiar acompanhamento humano de fatores organizacionais relacionados a riscos psicossociais e ações preventivas | Não implementado |
| SC-10 | Proteger dados pessoais, registrar operações relevantes e impedir acesso entre organizações | Não implementado no nível corporativo; autenticação individual legada existente |

## 4. Experiência pretendida

O colaborador encontra suas informações num ambiente central, com seções ou telas conectadas conforme a complexidade: perfil profissional, DISC com contexto e limites, missões disponíveis/aceitas/pendentes/concluídas, prazos e atrasos, XP e nível, atributos, conquistas, evolução, atividades relevantes e indicadores pessoais. Uma autenticação não equivale a participação. A experiência deve explicar a origem de cada dado e permitir distinguir eventos confirmados de interpretações.

O gestor vê dados operacionais das equipes sob sua responsabilidade, evolução temporal, participação, missões pendentes ou vencidas e pessoas que podem precisar de contato. Profissionais autorizados consultam relatórios agregados e acompanham ações preventivas no escopo concedido. O administrador configura vínculos e acessos de sua organização. Visões gerenciais e administrativas são distintas do dashboard pessoal; os detalhes permitidos estão no Documento de Domínio.

## 5. Módulos de negócio

1. **Identidade corporativa:** organizações, vínculos, equipes e papéis.
2. **Desenvolvimento individual:** perfil, DISC, evolução, atributos e histórico.
3. **Missões:** catálogo e atribuições por escopo, evidências, prazos, transições e recompensas.
4. **Gamificação:** XP, nível e conquistas vinculados a eventos de negócio.
5. **Acompanhamento:** atividade e inatividade com razões transparentes e análise humana.
6. **Indicadores e relatórios:** medidas individuais e agregadas com controle de acesso.
7. **Apoio preventivo relacionado à NR-1:** sinais organizacionais, providências e histórico para profissionais competentes.
8. **Segurança e auditoria:** isolamento, autorização, finalidade, rastreabilidade e retenção definida.

## 6. Requisitos transversais

- Cada leitura e escrita deve respeitar organização, vínculo, papel e finalidade; a autorização precisa ocorrer no servidor. Exportações e downloads seguem as mesmas regras.
- Dados de DISC e indicadores comportamentais exigem proteção reforçada, minimização e política explícita de visibilidade. Indicadores agregados não podem permitir reidentificação por grupos pequenos; limiar e técnica ainda precisam de decisão.
- Eventos de negócio que concedam recompensa devem ser idempotentes e transacionais. Consultas não alteram progresso.
- Indicadores precisam de definição de fonte, período, escopo, atraso de atualização e permissão; não se deve comparar pessoas sem regra e finalidade aprovadas.
- Configurações de inatividade, retenção, descarte, notificações, exportação e auditoria devem ser especificadas antes da implementação.
- A mudança de produto não exige por si só trocar Flask, Jinja, JavaScript convencional ou SQLite no protótipo; a adequação de persistência para SaaS multiempresa depende de avaliação técnica.

## 7. Limites e fora do escopo desta migração documental

Esta migração não entrega funcionalidade, não altera código, esquema, dados ou identidade visual. Experiências acadêmicas, disponibilidade para estágio, perfil público de contratação, recrutadores e currículo vivo público deixam de ser objetivos ativos do Sync-Coop. A retirada ou conversão dos fluxos legados é trabalho futuro e depende de política de dados e compatibilidade; nada foi removido agora.

Rankings, penalidades de XP, comparações individuais expostas, inteligência artificial, diagnóstico psicológico automático e decisões laborais automáticas não estão aprovados. Não são pressupostos do produto. Possíveis necessidades futuras exigem decisão de finalidade, proporcionalidade e privacidade.

## 8. NR-1 e limites de interpretação

O Sync-Coop pretende apoiar a **gestão humana** de informações organizacionais sobre condições de trabalho, participação e ações preventivas. Sinais da plataforma justificam revisão contextual, não diagnóstico, prova de adoecimento, avaliação legal completa ou medida disciplinar. Inatividade, baixo XP ou DISC isolado não demonstram risco psicossocial. O trabalho de identificar e avaliar fatores de risco psicossociais relacionados ao trabalho pertence ao processo da organização e a profissionais competentes. Requisitos regulatórios específicos serão validados contra a [NR-1 vigente do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1) e o [guia oficial do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/guia-nr-01-revisado.pdf). A plataforma, por si só, não garante conformidade.

## 9. Fonte de verdade e situação atual

Este documento define finalidade e requisitos de produto. O Documento de Domínio define conceitos e regras, distinguindo regras aprovadas de propostas; o Documento Técnico registra o sistema existente e a arquitetura alvo conceitual. decisions.md concentra decisões pendentes. README resume o estado executável. Os documentos originais do Sync-Disc permanecem recuperáveis no Git no commit 746a6ddff3e415b1132892dae4e733b6752f01ec e não são especificação ativa.
