# AGENT.md — Sync Disc

## Papel

Você atua no projeto Sync Disc. A direção do produto é um sistema gamificado de desenvolvimento e acompanhamento profissional de colaboradores em organizações.

## Leitura obrigatória

Antes de implementar, alterar, corrigir ou refatorar:

1. Leia `.docs/documento_mestre.md`.
2. Leia `.docs/documento_tecnico.md`.
3. Leia `.docs/documento_dominio.md`.
4. Consulte `.docs/decisions.md` para decisões registradas.

Os documentos oficiais definem o produto, arquitetura e domínio. Se houver conflito, prevalece o Documento Mestre para visão e escopo, o Documento Técnico para diretrizes arquiteturais e o Documento de Domínio para regras do domínio. Registre decisões novas em `.docs/decisions.md`.

## Análise antes de implementar

- Identifique o requisito atendido e verifique aderência aos documentos oficiais.
- Avalie impactos nas funcionalidades existentes.
- Priorize simplicidade, clareza, baixo acoplamento, coesão e manutenção.
- O código atual pode ainda refletir o contexto universitário anterior; não trate essa implementação como alteração automática dos documentos de produto.

## Limites do produto

O foco é desenvolvimento profissional, acompanhamento de evolução e engajamento. Organização possui setores e colaboradores; gestores acompanham colaboradores e criam setores e missões; colaboradores possuem perfil e DISC, recebem missões e evoluem por XP, níveis, conquistas e evolução.

Não invente requisitos, módulos, automações, fórmulas, permissões ou integrações. Não acrescente IA nem funcionalidades de RH além das documentadas. O produto não substitui ERP, RH, folha de pagamento ou controle operacional.

## Arquitetura

```text
Controllers
↓
Services
↓
Repositories
↓
Database
```

Regras de negócio ficam em Services. Repositories cuidam de persistência. Controllers recebem requisições, validam entradas básicas e delegam processamento.

## Registros de progresso

Mudanças em `/backend` devem ser registradas em `/backend/progress_backend.md`; mudanças em `/frontend`, em `/frontend/progress_frontend.md`. Registros incluem data, funcionalidade, arquivos, resumo e impacto. Alterações gerais de documentação do produto são registradas em `/progress.md`.

## Ao concluir

Informe claramente os documentos ou arquivos alterados e qualquer inconsistência relevante encontrada. Não declare como implementado aquilo que está somente especificado na documentação.
