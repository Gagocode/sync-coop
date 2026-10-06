# Sync Disc

Sync Disc é um sistema gamificado de desenvolvimento e acompanhamento profissional de colaboradores dentro de organizações. Gestores acompanham colaboradores, evolução, indicadores, rankings e missões; colaboradores desenvolvem seu perfil por meio de DISC, missões, XP, níveis, conquistas e certificações.

O foco é desenvolvimento profissional, acompanhamento de evolução e engajamento. O produto não substitui ERP, sistemas de RH, folha de pagamento ou controle operacional.

## Conceitos do produto

- **Organização:** empresa que utiliza a plataforma e possui setores e colaboradores.
- **Setor:** unidade da organização criada pelo gestor; colaboradores pertencem a um setor.
- **Colaborador:** possui perfil e DISC, recebe missões e evolui profissionalmente.
- **Gestor:** acompanha colaboradores, cria setores e missões e visualiza evolução, indicadores e rankings.
- **Gamificação:** DISC, XP, níveis, conquistas, missões e evolução permanecem no núcleo do produto.

Missões são contextualizadas para desenvolvimento profissional. Exemplos incluem concluir treinamento, participar de capacitação, documentar processo, obter certificação e executar atividade definida pelo gestor. Esses exemplos não estabelecem regras ou automações novas.

## Dashboard gerencial

O domínio inclui um dashboard gerencial para visualizar colaboradores, evolução, indicadores, rankings e missões. A documentação registra sua finalidade sem especificar implementação.

## Limites

Sync Disc não é um ERP, sistema de RH, folha de pagamento ou ferramenta de controle operacional. Esta direção de produto não adiciona inteligência artificial, integrações, automações nem funcionalidades de RH além das descritas.

## Arquitetura

O projeto segue arquitetura em camadas:

```text
Interface -> Controladores -> Serviços -> Repositórios -> Banco de Dados
```

Regras de negócio ficam nos serviços; controladores recebem requisições e delegam processamento; repositórios cuidam da persistência.

## Documentação oficial

Leia estes documentos antes de implementar mudanças de produto ou domínio:

1. `.docs/documento_mestre.md` — visão, escopo e objetivos do produto.
2. `.docs/documento_tecnico.md` — diretrizes de arquitetura.
3. `.docs/documento_dominio.md` — conceitos e regras de domínio.
4. `.docs/decisions.md` — decisões documentadas.
5. `project.md` — resumo do posicionamento e dos atores.

Em conflitos de escopo e produto, prevalece o Documento Mestre; diretrizes técnicas seguem o Documento Técnico; regras do domínio seguem o Documento de Domínio. Decisões registram justificativas e limites sem substituir esses documentos.

## Registros de progresso

`progress.md` registra alterações documentais gerais. Mudanças no backend e frontend devem continuar registradas, respectivamente, em `backend/progress_backend.md` e `frontend/progress_frontend.md`.

## Estrutura do repositório

```text
.
+-- .docs/       # Documentação de produto, domínio, arquitetura e interface
+-- backend/     # Aplicação e camadas de serviço e persistência
+-- frontend/    # Páginas e recursos da interface
+-- project.md   # Resumo do produto
+-- progress.md  # Histórico de atualização documental do produto
+-- README.md
```

## Licença

Licença ainda não definida. Antes de publicar ou distribuir o projeto, escolha uma licença e adicione `LICENSE` na raiz.

## Estado da implementação

O código existente antecede o reposicionamento corporativo e ainda contém fluxos e linguagem do contexto universitário original. Esta atualização altera documentação; não afirma que os fluxos corporativos, setores, organizações ou dashboard gerencial já estejam implementados.
