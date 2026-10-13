# Sync-Coop — Domínio e Regras de Negócio

**Status:** especificação ativa em 2026-10-13. Cada regra indica se é requisito confirmado do novo escopo, comportamento legado implementado, proposta ou decisão pendente. Este documento não altera a aplicação. Questões abertas estão centralizadas em decisions.md.

## 1. Vocabulário e entidades

| Conceito | Definição e relação | Situação |
|---|---|---|
| Organização | Cliente corporativo e limite primário de propriedade e acesso aos dados | Requisito confirmado; ausente no código |
| Setor/departamento/equipe | Unidades organizacionais às quais pessoas e missões podem ser vinculadas | Requisito confirmado; estrutura e hierarquia pendentes |
| Pessoa/colaborador | Usuário vinculado a uma organização e possivelmente a uma ou mais equipes | Requisito confirmado; há apenas usuário individual legado |
| Vínculo/papel | Relação temporal que autoriza ações sobre organização, equipe ou pessoa | Requisito confirmado; modelo exato pendente |
| Missão de catálogo/atribuição | Objetivo definido com escopo e uma ocorrência de trabalho para pessoa ou grupo | Requisito confirmado; catálogo individual fixo legado |
| Evidência | Informação ou registro que demonstra cumprimento dos critérios de uma missão | Requisito confirmado; formato/validação pendentes |
| Evento de atividade | Ação observável que pode ser relevante para participação ou missão | Requisito confirmado; taxonomia pendente |
| Resultado DISC inicial | Respostas e pontuação do questionário, distintas de ações posteriores | Legado implementado; preservar com política corporativa a definir |
| DISC observado | Contadores derivados de ações registradas na plataforma | Legado implementado; significado e uso corporativo pendentes |
| Acompanhamento preventivo | Revisão e providência humana no contexto de trabalho | Requisito confirmado; ausente no código |

Uma organização deve isolar seus registros das demais. O vínculo define quem pode ver uma pessoa ou equipe em cada instante. Transferência, desligamento, múltiplos vínculos, hierarquia de equipes e portabilidade de histórico estão em decisions.md.

## 2. Atores e permissões

**Princípio confirmado:** menor acesso necessário, limitado por organização, vínculo, escopo e finalidade; autorização em servidor para leitura, escrita, download e exportação. A matriz abaixo estabelece o limite funcional pretendido. Detalhes de consentimento/base aplicável e visibilidade de DISC exigem decisão antes da implementação.

| Recurso/ação | Colaborador | Gestor vinculado | Admin da organização | Profissional autorizado |
|---|---|---|---|---|
| Perfil, missões e evolução individual | Próprios | Dados operacionais da equipe sob responsabilidade | Gerir vínculos; detalhes individuais somente com permissão adicional | Somente finalidade e caso autorizados |
| Criar/atribuir/validar missão | Executar e enviar evidência própria | Equipe sob delegação explícita | Configurar delegações e catálogo organizacional | Conforme mandato específico |
| Indicadores agregados | Próprios | Sua equipe | Organização, com supressão de grupos pequenos | Escopo e finalidade concedidos |
| Resultado DISC individual | Próprio | Pendente; sem acesso por padrão | Sem acesso por padrão | Pendente; sem acesso por padrão |
| Registro de acompanhamento | Ver informações próprias permitidas pela política a definir | Registrar providência sob autorização | Administrar acesso, sem conteúdo sensível por padrão | Registrar/analisar casos no escopo |
| Dados de outra organização | Nunca por vínculo local | Nunca | Nunca | Nunca sem vínculo e finalidade próprios daquela organização |

Operador da plataforma tem acesso operacional excepcional a definir, jamais acesso irrestrito implícito. “Pendente” na matriz não autoriza implementação ampla.

## 3. Missões corporativas

**Requisito confirmado:** uma missão deve descrever título, objetivo, critérios de conclusão, escopo (toda organização, setor/departamento/equipe ou pessoa), criador/responsável, data de início, prazo, estado, evidências requeridas, recompensa e histórico de criação, atribuição, mudança, validação e conclusão. Atribuir a um grupo deve permitir saber quais pessoas são destinatárias; política para entradas/saídas posteriores é pendente. Prazo e fuso/horário de corte também dependem de decisão.

**Legado implementado:** nove missões fixas por usuário, com chaves e tipo_evento. Estados persistidos: Bloqueada, Pendente, Concluida. A conclusão decorre de DISC_COMPLETED, PROFILE_COMPLETED, PROJECT_CREATED ou CERTIFICATE_CREATED, com validação de evidência persistida e ordem dentro do mesmo evento. CONTINUE_EVOLUTION não tem condição aprovada e não conclui automaticamente. Não há aceite, rejeição, abandono, atraso ou expiração. A “missão de perfil completo” legada conclui ao enviar DISC e gerar classe, não ao preencher todos os dados profissionais; o sentido corporativo precisa de revisão.

**Domínio anterior não implementado:** também descrevia Disponível, Aceita, Ignorada, Abandonada e Expirada, além de missões adaptativas. “Ignorada” não geraria punição; abandono e expiração tinham efeito apenas conceitual, sem valor ou condição fechados. Essas descrições não são estados entregues nem transições aprovadas para o Sync-Coop; servem como insumo para DC-06 e DC-08.

**Proposta de ciclo para análise, ainda não aprovada:** rascunho → publicada/atribuída → disponível → em execução → enviada para validação → concluída ou rejeitada para correção. Cancelamento, abandono e expiração seriam transições explícitas com ator, motivo e histórico. “Atrasada” pode ser uma condição derivada de prazo vencido e missão não concluída, em vez de novo estado persistido. “Bloqueada” pode continuar a representar pré-requisito não atendido. Os nomes finais, regras de aceite, rejeição, reabertura, sobreposição de escopos, prazo e elegibilidade de recompensa são decisões pendentes. Não aplicar esses estados propostos ao código sem aprovação.

Conclusão exige condição verificável e ação/validação autorizada. Repetir a mesma conclusão não concede XP, conquista ou outro efeito novamente. Não se deve conceder penalidade automática por atraso ou abandono sem regra aprovada. Mudanças de missão publicada devem preservar rastreabilidade e critério usado na avaliação.

## 4. DISC e desenvolvimento

O DISC inicial é resultado de questionário; o DISC observado é índice derivado de eventos da plataforma; inferências são hipóteses interpretativas e exigem contexto humano. Esses três tipos de dado não são intercambiáveis. Nenhum deles constitui diagnóstico clínico, medição isolada de capacidade profissional ou prova de risco psicossocial. Seu uso confirmado no Sync-Coop é apoiar reflexão e desenvolvimento pessoal; uso em avaliação gerencial ou comparação depende de política específica.

As dimensões preservadas são **D (Dominância)**, ligada no modelo legado a iniciativa e decisão; **I (Influência)**, a comunicação e interação; **S (Estabilidade)**, a continuidade e colaboração; e **C (Conformidade)**, a organização e análise. Esses nomes descrevem o instrumento, não autorizam classificar desempenho ou saúde de uma pessoa. A classe inicial do legado é uma representação visual derivada do quiz e não altera regras de negócio. Atributos secundários, como comunicação ou trabalho em equipe, eram intenção documental, mas não foram implementados; sua definição, fonte e exposição corporativa continuam pendentes.

**Legado implementado:** questionário narrativo de 12 perguntas, dimensões D/I/S/C, uma aplicação inicial por usuário e classe derivada. O sistema registra resultados iniciais, pontuação observada, projetos, certificados, missões concluídas e conquistas. Pesos observados atuais: +10 D por projeto, +10 C por certificado, +5 S por missão concluída e +5 I por conquista. A documentação antiga define conquistas como cosméticas, portanto o peso I é divergência entre regra documentada e implementação; a regra futura não está decidida. Reaplicação, visibilidade corporativa, retenção, explicação ao colaborador e revisão científica/metodológica são pendentes.

## 5. Gamificação e consistência

**Requisito confirmado:** XP, níveis, atributos, conquistas e histórico podem apoiar participação e desenvolvimento. Eventos geradores e efeitos devem ser explícitos, determinísticos, transacionais e atribuídos uma única vez por ocorrência de negócio. Consultas não alteram estado. Não se deve usar XP para penalizar pessoa ou inferir saúde.

**Legado implementado:** recompensas do catálogo: 100 XP por DISC inicial, 50 XP por missão de “perfil” acionada no mesmo fluxo e 150 XP para cada um dos três primeiros projetos e certificados. A missão CONTINUE_EVOLUTION rende 0 e não possui conclusão definida. Níveis usam limiares 0, 200, 500, 900 e 1400 XP; cinco conquistas estão no catálogo; eventos de evolução ficam em histórico. Excluir projeto/certificado recalcula DISC observado, mas não retira XP ou conquistas já obtidos. Os pontos e limiares descrevem o protótipo, não política corporativa automaticamente aprovada.

**Pendente:** quais ações corporativas geram XP, possibilidade e condição de reversão, consequências de evidência rejeitada, critérios de novas conquistas, política de atributos e classes, versões de regras, prevenção de repetição de POST de criação e eventual ranking/comparação. Se ranking for considerado, público, finalidade, opção de participação e privacidade devem ser aprovados antes.

O domínio antigo descrevia missões adaptativas sugeridas a partir de uma dimensão DISC menor, mas não há implementação nem critério aprovado para uso corporativo. Também previa “Ignorada” sem punição e “Abandonada”/“Expirada” com possíveis penalidades; só o primeiro princípio de não penalizar uma missão ignorada tem formulação definida, enquanto penalidades e transições não foram implementadas. Para o Sync-Coop, adaptar tais mecanismos exige decisão de finalidade e privacidade, sem recomendação automática que rotule a pessoa pelo DISC.

## 6. Atividade, inatividade e sinalizações

**Requisito confirmado:** acesso à plataforma e atividade efetiva são eventos distintos. Login pode registrar presença técnica; atividade relevante exige ação substantiva definida, como evidência de missão enviada ou validada. Visualizar uma tela ou manter sessão aberta não comprova desenvolvimento. Toda sinalização deve mostrar motivo, fonte, período de referência e data de cálculo.

| Sinal conceitual | Fonte pretendida | Interpretação permitida | Limite/decisão |
|---|---|---|---|
| Ausência de acesso | Evento de autenticação/sessão | Contato ou investigação de barreira de acesso | Janela e limiar pendentes |
| Ausência de atividade relevante | Eventos qualificados de negócio | Verificar se a pessoa precisa de apoio | Taxonomia, janela e limiar pendentes |
| Missões vencidas/acumuladas | Atribuições, prazo, estado | Revisar carga e impedimentos | Horário de corte, exclusões e limiar pendentes |
| Redução de participação | Séries de eventos comparáveis | Revisar contexto com gestor/profissional | Medida de referência e variação pendentes |
| Necessidade de acompanhamento | Sinais mais contexto e decisão humana | Abrir ação de apoio autorizada | Responsável, fluxo e visibilidade pendentes |

Feriados, afastamentos, indisponibilidade técnica, mudanças de vínculo e missões não elegíveis podem distorcer indicadores; tratamento é pendente. Sinal não é diagnóstico ou critério disciplinar automático. Ação possível: contato, revisão de condições de trabalho, apoio ou encaminhamento apropriado por profissional competente, com registro proporcional e acesso controlado.

## 7. Relatórios e indicadores

Indicadores devem declarar período, universo elegível, origem, atraso de atualização, nível de agregação, razão da sinalização e permissão. Fórmulas operacionais e regras de exclusão precisam ser aprovadas antes da implementação.

| Indicador conceitual | Significado e fonte | Escopo e acesso pretendido | Fórmula/limiar |
|---|---|---|---|
| Participação em missões | Ocorrências atribuídas com evento relevante; fonte: atribuições/eventos | Próprio, equipe vinculada ou agregado autorizado | Denominador, elegibilidade e período pendentes |
| Conclusão | Missões concluídas em relação às elegíveis; fonte: estado/histórico | Próprio, equipe, setor ou organização conforme papel | Janela, denominador e reabertura pendentes |
| Pendências e atrasos | Atribuições abertas e prazo vencido; fonte: estado/prazo | Próprio e gestor responsável; agregado autorizado | Corte temporal pendente |
| Evolução | Mudanças de nível, XP, atributos e conquistas; fonte: histórico | Próprio; agregados com proteção de grupos pequenos | Comparação entre períodos pendente |
| Acesso e atividade | Último acesso distinto de última atividade qualificada; fonte: eventos | Próprio; gestor no escopo e agregados autorizados | Janela e supressão pendentes |
| Acompanhamentos | Providências abertas/encerradas e responsáveis; fonte: registros próprios | Profissional autorizado e gestão conforme finalidade | Conteúdo visível e retenção pendentes |

Comparações entre períodos só são válidas com populações e regras comparáveis. Relatórios não devem expor DISC individual, notas implícitas de saúde ou grupos tão pequenos que permitam reidentificação. Exportações exigem a mesma permissão que a tela.

## 8. Apoio à gestão de riscos psicossociais relacionados ao trabalho

O produto deverá fornecer dados organizacionais e histórico de providências para **apoiar** análise humana das condições de trabalho e ações preventivas. Um sinal da plataforma pode sugerir revisão contextual; não prova adoecimento, risco específico ou incapacidade de uma pessoa. DISC, baixo XP e inatividade isolados não são evidências conclusivas. É necessário distinguir dados da plataforma de avaliações realizadas por profissionais competentes e das obrigações próprias da organização.

**Requisito confirmado:** relatórios agregados, responsáveis, providências e histórico de acompanhamento com acesso restrito, quando implementados. **Pendente:** quais indicadores são pertinentes, processo de validação humana, metodologia, retenção, visibilidade e conexão com processos organizacionais. Não há avaliação legal automática ou promessa de conformidade com NR-1. Referências oficiais: [NR-1 vigente do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1) e [guia do MTE sobre fatores psicossociais relacionados ao trabalho](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/guia-nr-01-revisado.pdf). Validação regulatória específica cabe a profissionais competentes.

## 9. Privacidade e auditoria

**Requisito confirmado:** isolar organizações; minimizar dados; informar finalidade; limitar acesso a DISC e indicadores comportamentais; registrar alterações de missão, papel, vínculo, acompanhamento e acesso excepcional; permitir reconstruir quem mudou ou consultou dados sensíveis conforme política. Regras concretas de retenção, exclusão, acesso do titular, exportação, grupos pequenos e base jurídica aplicável são decisões pendentes. Perfil público/currículo do legado não deve ser automaticamente levado ao ambiente corporativo.
