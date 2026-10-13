# Diretrizes de interface — Sync-Coop

**Status:** orientação de produto e continuidade visual, 2026-10-13. A identidade visual corporativa definitiva ainda não foi aprovada. A especificação visual do Sync-Disc anterior permanece no Git no commit 746a6ddff3e415b1132892dae4e733b6752f01ec; ela é referência histórica, não regra de acesso ou escopo do Sync-Coop.

## Base existente

O frontend implementado usa templates Jinja, HTML, CSS e JavaScript convencional. O dashboard individual tem abas e modais; seus estilos estão em frontend/assets/css, incluindo style.css, journey.css, identity.css, symbols.css e professional-profile.css. Tipografia, cores, ícones, componentes e comportamento atuais são a referência visual do protótipo. Nenhuma mudança de marca, paleta, fonte ou biblioteca foi decidida nesta migração documental.

Os tokens observados em identity.css incluem azul #0085ff, azul profundo #0056a4, ciano #14b8d4, teal #008f9e, XP #f5c84c e medalha #f28b45. Há valores posteriores de CSS que sobrescrevem parte dessas variáveis; por isso esses tokens descrevem fonte existente, não uma paleta final calculada nem uma marca aprovada para o Sync-Coop. O CSS não foi alterado nesta migração.

## Experiência pretendida

- **Colaborador:** ambiente central, com perfil, DISC, missões, prazos, evolução, conquistas e atividade pessoal apresentados por seções claras. A pessoa deve entender a origem e o período de cada indicador.
- **Gestor:** superfície própria para equipes sob responsabilidade, com pendências, prazos, participação e evolução. Mostrar apenas o nível de detalhe autorizado e explicar sinais de atenção.
- **Administrador:** controles de organização, vínculos e permissões; o papel administrativo não deve desbloquear automaticamente informações DISC ou registros sensíveis.
- **Profissional autorizado:** agregados e ações de acompanhamento definidos por finalidade e escopo. Ocultar ou suprimir agregados que permitam reidentificação; regra exata pendente.

Estados de missão propostos não devem aparecer como funcionalidades prontas antes da aprovação da transição de domínio. “Atrasada” deve ser claramente explicada pelo prazo e estado, sem sugerir culpa. “Inativa” exige janela e eventos qualificados definidos; login isolado não é progresso. XP, DISC e conquistas não devem ser usados como rótulos de saúde, competência ou valor profissional.

## Regras de apresentação

1. Distinguir resultado de questionário DISC, atividade registrada e interpretação humana. Não atribuir diagnóstico.
2. Informar período, fonte e critério dos indicadores; para dados ainda indisponíveis, usar estado vazio honesto em vez de valor inventado.
3. Permitir navegação e operações dentro do escopo do papel. Erros de autorização devem ser claros, sem revelar a existência de dados de outra organização.
4. Exibir prazos e pendências com contexto; ações de aceite, rejeição e abandono só depois de regra aprovada.
5. Manter acessibilidade: contraste legível, foco de teclado, rótulos de formulários, estados de carregamento/erro e significado que não dependa apenas de cor.
6. Qualquer eventual visualização agregada deve respeitar proteção contra reidentificação e política de acesso.

## Decisões abertas

Identidade de marca do Sync-Coop, padrões para dashboards gerenciais, tratamentos visuais de dados DISC, limite de agregação, linguagem de sinalizações e eventuais mudanças de componentes precisam de aprovação e validação com usuários. Este documento não autoriza redesign do código atual.
