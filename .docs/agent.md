# Instruções para agentes — Sync-Coop

**Status:** ativo desde 2026-10-13. Este arquivo orienta trabalho futuro; não concede autorização para implementar requisitos ainda pendentes.

## Fonte de verdade

Antes de alterar código ou documentação, leia README.md, documento_mestre.md, documento_dominio.md, documento_tecnico.md, decisions.md e o registro de progresso da área afetada. Use caminhos reais do repositório. Os documentos originais do Sync-Disc e as entradas antigas de progresso/decisões são históricos; estão recuperáveis no commit 746a6ddff3e415b1132892dae4e733b6752f01ec.

Em conflito, o Documento Mestre define finalidade e escopo; o Documento de Domínio define regras aprovadas e limites; o Documento Técnico descreve o implementado e restrições técnicas. decisions.md registra decisões em aberto e substituições. O código é evidência do comportamento efetivamente implementado, não autorização para transformar um comportamento legado em regra do Sync-Coop. Registre divergências e peça decisão de produto antes de inventar regra.

## Classifique toda afirmação relevante

- **Requisito confirmado:** direção definida para o Sync-Coop, mesmo sem código.
- **Comportamento implementado:** verificado na aplicação atual; frequentemente legado Sync-Disc.
- **Proposta:** desenho sugerido ainda sem aprovação.
- **Decisão pendente:** regra ou política necessária para fechar o domínio.
- **Fora do escopo:** item que esta etapa não entrega ou que foi retirado da direção do produto.

Não use “implementado” para organizações, permissões corporativas, dashboards gerenciais, prazos, inatividade, relatórios ou apoio à NR-1 enquanto não houver código e testes. Não trate o perfil público e o currículo acadêmico como requisitos corporativos aprovados.

## Princípios de desenvolvimento

Preserve Flask, Jinja, CSS/JavaScript convencional, serviços, repositórios e contratos atuais até haver motivo e decisão para mudar. Mudanças de produto exigem análise de dados existentes e migração segura. Verifique autorização por organização/vínculo/papel no servidor; não confie no frontend. Consultas não produzem XP nem alteram dados. Comandos que envolvem missão, recompensa e histórico devem ser atômicos e idempotentes quanto ao evento de negócio. Não exponha dados DISC, relatórios individuais ou informações de acompanhamento apenas porque o usuário é gestor ou administrador.

Não implemente limiares de inatividade, fórmula de indicadores, penalidade, ranking, política de DISC, retenção ou transições de missão que estejam marcados como pendentes. Apoio à NR-1 exige validação com fontes oficiais atuais e profissionais competentes; a plataforma não é diagnóstico nem garantia de conformidade.

## Registros

Atualize decisions.md quando uma definição for aprovada ou uma divergência for descoberta. Registre alterações de backend em backend/progress_backend.md e de frontend em frontend/progress_frontend.md, distinguindo código de documentação. Não reescreva os logs históricos para fazê-los parecer entregas Sync-Coop. Em tarefas exclusivamente documentais, não modifique código, configuração, migração ou banco.
