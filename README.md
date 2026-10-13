# Sync-Coop

O Sync-Coop é a direção oficial do produto: uma plataforma corporativa SaaS de desenvolvimento de colaboradores, missões, gamificação, acompanhamento de equipes e indicadores para gestores e profissionais autorizados. O uso de dados organizacionais poderá apoiar análise humana de fatores de risco psicossociais relacionados ao trabalho, com limites claros de interpretação. O DISC permanece parte do produto.

**Estado do repositório:** o código executável ainda é o protótipo Sync-Disc, voltado a usuários individuais. Esta migração atualizou somente a documentação; organizações, equipes, papéis, dashboards gerenciais, missões com prazos, indicadores corporativos e recursos de apoio à NR-1 ainda não foram implementados. A presença de um requisito nos documentos não significa que o aplicativo o entregue.

## O que funciona hoje

- Cadastro, login/logout e questionário DISC inicial de uma aplicação.
- Dashboard individual em /dashboard com perfil, projetos, certificados, missões, conquistas e evolução.
- Missões de catálogo, XP, níveis, DISC observado e histórico de evolução.
- Perfil público e currículo do domínio anterior, ainda presentes no código e sujeitos a revisão de privacidade antes de qualquer adoção corporativa.
- Backend Flask em camadas, templates Jinja, CSS/JavaScript convencional e SQLite.

O código atual não possui isolamento entre organizações nem controle de acesso por papel corporativo. Portanto, **não deve ser apresentado como SaaS multiempresa pronto**.

## Executar o protótipo local

Instale as dependências listadas em backend/requirements.txt e execute:

    python backend/app.py

O SQLite local é criado em backend/database/ e os uploads ficam em backend/uploads/. Use dados de desenvolvimento. Para testar com ambiente temporário:

    python -m unittest discover -s backend/tests -v

O teste de interface opcional é python backend/tests/browser_smoke.py; requer Playwright e Chromium instalados. Esta migração documental não executou esses testes nem modificou a aplicação.

## Documentação ativa

| Documento | Função |
|---|---|
| [.docs/documento_mestre.md](.docs/documento_mestre.md) | Produto, objetivos e requisitos confirmados |
| [.docs/documento_dominio.md](.docs/documento_dominio.md) | Conceitos, regras legadas, regras propostas e limites de acesso |
| [.docs/documento_tecnico.md](.docs/documento_tecnico.md) | Arquitetura real e requisitos técnicos futuros |
| [.docs/analise_escopo_e_features.md](.docs/analise_escopo_e_features.md) | Diferenças Sync-Disc → Sync-Coop e estado das capacidades |
| [.docs/decisions.md](.docs/decisions.md) | Decisões atuais, pendências e histórico dos Prompts 1–3 |
| [.docs/design-system.md](.docs/design-system.md) | Diretrizes de interface, sem marca visual nova aprovada |
| [.docs/agent.md](.docs/agent.md) | Instruções para agentes e hierarquia documental |

Os arquivos backend/progress_backend.md e frontend/progress_frontend.md são registros históricos de implementação do Sync-Disc. Não equivalem a um cronograma ou status de entrega do Sync-Coop.

Os originais dos documentos substituídos podem ser recuperados no Git pelo commit 746a6ddff3e415b1132892dae4e733b6752f01ec, por exemplo com git show 746a6dd:.docs/documento_mestre.md. Eles são históricos, não especificação vigente.

## Limites do produto

Resultados DISC, acesso, baixo XP ou pouca participação não constituem diagnóstico clínico nem prova de risco psicossocial ou desempenho profissional. Indicadores exigem contexto, finalidade, permissão e revisão humana. O Sync-Coop não garante conformidade com a NR-1 por si só; requisitos regulatórios específicos precisam de validação com profissionais competentes e [fontes oficiais do MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/nr-1).

## Licença

Ainda não definida.
