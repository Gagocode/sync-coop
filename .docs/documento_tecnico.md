# Sync-Coop — Documento Técnico e de Arquitetura

**Status:** arquitetura existente verificada no repositório em 2026-10-13 e requisitos técnicos para evolução. Nenhum componente corporativo descrito como futuro foi implementado nesta migração documental. Requisitos de produto: documento_mestre.md; regras: documento_dominio.md; pendências: decisions.md.

## 1. Linha de base implementada: Sync-Disc

O aplicativo atual é Flask em backend/app.py, templates Jinja, HTML/CSS e JavaScript convencional em frontend/, SQLite em backend/database/ e uploads locais. Usa sessão Flask, controllers, services, repositories e models. Há um único tipo de usuário em users; a coluna curso e o formulário profissional preservam o domínio acadêmico. Não existem tabelas de organização, setor, equipe, associação corporativa, papel, prazo de missão, auditoria administrativa ou acompanhamento de riscos.

O fluxo executável é cadastro/login, questionário DISC inicial, resultado, dashboard individual e operações de perfil, projetos, certificados, missões, conquistas e evolução. O dashboard /dashboard possui abas dashboard, profile, projects, certificates, missions, achievements e evolution. Páginas de login, cadastro, quiz e resultado permanecem independentes; perfil público e downloads também. Rotas HTML antigas de perfil/missões/projetos/certificados redirecionam ao dashboard; POSTs e JSON foram mantidos. Templates HTML legados ainda respondem a erros de alguns POSTs. O perfil público legado expõe dados por identificador/nome e currículo, o que exige revisão antes de uso corporativo.

| Contrato existente | Uso atual |
|---|---|
| /auth/register, /auth/login, /auth/logout, /auth/me | Identidade individual e sessão |
| /disc/ e /disc/resultado(.json) | DISC inicial e consulta |
| /dashboard, /perfil/json, /perfil/profissional, /perfil/curriculo | Dashboard e perfil individual |
| /missoes/json | Lista individual de missões |
| /projetos/ e /certificados/ (CRUD, JSON e downloads quando aplicável) | Projetos/certificados individuais |
| /profile/<id> e rotas públicas associadas | Perfil público legado |

O contrato completo de métodos e rotas deve ser conferido nos controllers antes de alterá-los; a tabela é um mapa técnico, não nova especificação de API. O frontend chama JSON e POSTs legados. Não há API corporativa, de relatórios ou de NR-1.

## 2. Persistência e responsabilidades existentes

O esquema contém users, professional_profiles, initial_disc_results, missions, user_missions, projects, certificates, achievement, user_achievement, evolution_events e observed_disc_results. A missão de catálogo usa tipo_evento; a missão do usuário guarda estado e data de conclusão. Não há organização proprietária no esquema. O diretório de uploads guarda currículo e documentos de certificado.

Consultas de perfil, dashboard e evolução são de leitura; o registro DISC, projeto e certificado aciona comandos de negócio. Missões, XP, classe, conquistas, histórico e DISC observado são coordenados nos serviços e persistidos em transação SQLite. O repositório de missões usa transição condicional e impede recompensa repetida pela mesma conclusão. A reconciliação de dados legados roda na inicialização, de forma idempotente, e não em GETs. A criação repetida de projetos ou certificados continua criando novo registro; o contrato não tem chave de idempotência de requisição. O comportamento foi coberto pelos testes existentes em backend/tests, mas não equivale a isolamento corporativo.

## 3. Arquitetura alvo, sem reescrita tecnológica presumida

Preservar a separação controller → service → repository → banco, templates Jinja e JavaScript convencional enquanto forem adequados. A evolução corporativa deve acrescentar, conforme projeto posterior aprovado:

- **Identidade e contexto de organização:** organização ativa, vínculo válido com colaborador/equipe/setor e papel, estabelecidos no servidor. A sessão sozinha não autoriza acesso a dados de outra organização.
- **Autorização por recurso:** toda consulta, comando, relatório, arquivo e exportação deve exigir organização, escopo e permissão. IDs fornecidos pelo cliente não são prova de vínculo. Administrador da organização não recebe dados sensíveis por padrão.
- **Persistência isolada:** todos os registros corporativos devem possuir pertencimento inequívoco a organização e, quando relevante, a pessoa/equipe. Estratégia de banco, chaves, migração e isolamento físico/lógico permanecem pendentes; o esquema atual não satisfaz o requisito.
- **Eventos auditáveis:** registrar ator, organização, ação, objeto, instante, mudança e justificativa quando necessária, principalmente administração, mudança de atribuição, acesso excepcional e acompanhamento preventivo. Definir retenção e acesso aos logs antes de implementar.
- **Serviços de domínio:** comandos explícitos para atribuição/transição de missões, geração de efeitos de XP e registro de ações. Consultas e agregações não concedem recompensas. Uma ação de negócio com múltiplas escritas usa uma única transação; efeitos externos exigem política de compensação.
- **Indicadores:** derivar de eventos de acesso, atividade relevante, missão e acompanhamento com período, escopo e versão de regra. Evitar métricas irreproduzíveis e não materializar inferências como fatos. Política de atualização e anonimização ainda pendente.
- **Arquivos e dados pessoais:** download e exportação com a mesma verificação de escopo; armazenamento, retenção, exclusão e migração dos arquivos locais dependem de decisão.

Esses são requisitos de arquitetura, não uma proposta de novos módulos ou tabelas definitivas. O desenho físico deve ser decidido antes da implementação e migrar dados existentes sem perda.

## 4. Fluxos pretendidos e fronteiras

1. **Acesso:** autenticar; resolver organização/vínculo/papel; autorizar recurso no servidor; registrar eventos de acesso segundo política. Acesso não conta como atividade de desenvolvimento.
2. **Missão:** criador autorizado define objetivo, critério, escopo, responsável, período e recompensa; atribuição produz vínculos; ação do colaborador apresenta evidência; validação autorizada muda estado; comando transacional aplica recompensa uma vez e registra histórico. Critérios de aceite/rejeição, abandono e expiração ainda dependem de decisão de domínio.
3. **Dashboard pessoal:** consultas reúnem dados próprios de fontes autorizadas, sem mutação e com distinção entre resultado DISC, fatos de atividade e indicadores calculados.
4. **Visão gerencial:** consulta filtra pelo vínculo de equipe vigente; apresenta indicadores permitidos e explicações; não revela dados DISC ou sensíveis sem política aprovada.
5. **Apoio preventivo:** sinais agregados motivam revisão humana das condições de trabalho; profissional autorizado registra providências no escopo concedido; não há inferência clínica automática.

## 5. Segurança, privacidade e operação

O protótipo tem autenticação por sessão e validação de posse de registros individuais, mas não tem autorização baseada em organização/papel. Antes de oferecer SaaS corporativo é necessário definir isolamento por organização em todas as camadas, política de mínimo privilégio, testes de acesso cruzado, proteção de dados DISC, segregação de dados de acompanhamento, logs de auditoria, backups, retenção e exclusão. O desenho também deve especificar como grupos pequenos são agregados sem reidentificar pessoas.

SQLite e uploads locais descrevem a implementação atual. Escala, concorrência, recuperação, hospedagem e estratégia de armazenamento para SaaS são decisões técnicas futuras; não há decisão de trocar a stack nesta tarefa. Não foi executada migração de banco. As regras regulatórias devem ser verificadas na [NR-1 do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1) com profissionais competentes; a aplicação não substitui o processo da organização.

## 6. Lacunas verificadas

| Necessidade Sync-Coop | Situação atual |
|---|---|
| Organizações, equipes, vínculos, papéis, acesso por escopo | Ausente |
| Dashboard gerencial/administrativo/profissional autorizado | Ausente |
| Missões por organização/equipe/pessoa, prazos e evidências formais | Ausente; há catálogo individual fixo |
| Indicadores de acesso, atividade, inatividade e relatórios agregados | Ausente |
| Registro de ações preventivas e auditoria corporativa | Ausente |
| DISC inicial, observado, XP, conquistas, evolução e histórico individuais | Presentes em forma legada; sem política de uso corporativo |
| Perfil público/currículo | Presentes em forma legada; risco de exposição para o novo produto |

Detalhes de migração e decisões pendentes ficam em analise_escopo_e_features.md e decisions.md. Referências ao legado são descritivas; não constituem aprovação para expor seus dados no Sync-Coop.
