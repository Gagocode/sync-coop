# Documento Técnico — Sync Disc

## 1. Objetivo

Este documento define diretrizes técnicas e limites arquiteturais para o Sync Disc. A arquitetura dá suporte a um sistema gamificado de desenvolvimento e acompanhamento profissional de colaboradores em organizações. Este documento não especifica implementação detalhada, esquema de banco, APIs, tabelas ou componentes de interface.

## 2. Escopo técnico

O sistema deve dar suporte ao domínio documentado: organizações, setores, colaboradores, perfis, DISC, missões, XP, níveis, conquistas, certificações, evolução e visualização gerencial. O foco técnico é manter uma base compreensível e extensível para esse domínio, preservando a separação de responsabilidades.

O produto não é um ERP, sistema de RH, folha de pagamento nem sistema de controle operacional. Esta atualização não especifica integrações, inteligência artificial, automações ou módulos adicionais.

## 3. Princípios arquiteturais

- **Separação de responsabilidades:** cada camada mantém uma finalidade clara.
- **Baixo acoplamento:** mudanças em uma área não devem gerar dependências desnecessárias nas demais.
- **Alta coesão:** regras relacionadas permanecem agrupadas em seus serviços e módulos de domínio.
- **Evolução gradual:** o sistema pode crescer sem reestruturação prematura.
- **Manutenibilidade:** priorizar legibilidade, simplicidade e previsibilidade.

## 4. Blocos do sistema

**Backend:** regras de negócio, autenticação, persistência e cálculos ligados ao perfil, à gamificação, ao DISC, às missões e à evolução.

**Frontend:** interface, apresentação de informações, formulários, navegação e experiência de colaboradores e gestores.

## 5. Organização e persistência

Manter separação entre código-fonte, banco de dados, arquivos enviados, documentação e recursos visuais. Arquivos de usuários não devem ser misturados ao código-fonte.

O sistema utiliza persistência relacional, inicialmente em ambiente local e com foco em desenvolvimento incremental. O acesso a dados deve permitir evolução do mecanismo de armazenamento sem transferir regras de negócio para a persistência.

Arquivos enviados devem permanecer separados do código-fonte, em estrutura que não dependa de caminhos absolutos. O armazenamento local existente continua sendo uma diretriz técnica; esta atualização não define novos tipos ou fluxos de arquivo.

## 6. Arquitetura em camadas

Fluxo conceitual:

```text
Interface -> Controladores -> Serviços -> Repositórios -> Banco de Dados
```

- **Interface:** interação e apresentação; não contém regras de negócio.
- **Controladores:** recebem requisições, validam entradas básicas e delegam processamento.
- **Serviços:** concentram regras de negócio, cálculos, gamificação, DISC, missões e evolução.
- **Repositórios:** realizam leitura e gravação sem conter regras de negócio.

## 7. Domínio e contexto organizacional

As responsabilidades técnicas devem acomodar a relação conceitual organização–setor–colaborador definida no Documento Mestre e no Documento de Domínio. Setores pertencem a organizações; colaboradores pertencem a setores; gestores acompanham colaboradores e criam setores e missões conforme o domínio documentado.

Esta diretriz não define modelo de autorização, hierarquia empresarial, permissões, regras de associação ou implementação do dashboard gerencial.

## 8. Gamificação, DISC e missões

A gamificação continua sendo parte central do sistema, incluindo XP, níveis, conquistas, missões e evolução. DISC Inicial e DISC Observado permanecem conceitos do produto.

Missões devem ser representadas no contexto de desenvolvimento profissional. A atualização de domínio não autoriza criação de regras, estados, automações, cálculos ou mecanismos adaptativos novos. Os detalhes devem corresponder às regras oficialmente definidas no domínio.

## 9. Perfil e dashboard gerencial

O perfil representa o desenvolvimento profissional do colaborador e reúne as informações de evolução previstas no domínio. O dashboard gerencial é uma superfície de visualização para colaboradores, evolução, indicadores, rankings e missões. Este documento não define sua implementação ou acrescenta requisitos de interface e análise.

## 10. Segurança e qualidade

Considerar autenticação, autorização, validação de entradas e proteção contra manipulação indevida de dados. As responsabilidades e políticas específicas devem ser definidas em requisitos próprios, sem inferi-las somente a partir dos papéis de gestor e colaborador.

Regras de negócio devem ser separáveis da interface para permitir validação e manutenção. Não são definidos novos testes, metas mensuráveis ou critérios de desempenho nesta atualização.

## 11. Diretriz para decisões técnicas

Decisões técnicas devem respeitar o Documento Mestre e o Documento de Domínio, preservar a separação de responsabilidades e manter a gamificação como núcleo. Mudanças de escopo ou regras de negócio devem ser documentadas antes de orientar implementação.
