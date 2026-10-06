# DOCUMENTO DE ARQUITETURA TÉCNICA

## 1. Objetivo
Este documento define as diretrizes técnicas do projeto.
Seu objetivo é estabelecer padrões de desenvolvimento, organização do código, responsabilidades das camadas e princípios arquiteturais que deverão ser seguidos durante a implementação.

Este documento não define detalhes de implementação específicos, nomes definitivos de entidades, tabelas, classes ou estruturas internas de código. Essas definições serão realizadas durante a fase de desenvolvimento.

## 2. Escopo Técnico
O sistema será desenvolvido inicialmente como um protótipo funcional para validação acadêmica do conceito.

O foco inicial é:
* Demonstrar o fluxo principal da aplicação.
* Validar a proposta de gamificação.
* Validar a utilização do DISC como sistema de atributos evolutivos.
* Demonstrar a construção do currículo vivo.
* Permitir futuras expansões sem necessidade de reescrita completa.

## 3. Princípios Arquiteturais
A arquitetura deverá seguir os seguintes princípios:

* **Separação de Responsabilidades:** Cada camada deve possuir apenas uma responsabilidade principal. As regras de negócio não devem ficar misturadas com: rotas, persistência, interface ou consultas ao banco.
* **Baixo Acoplamento:** Os módulos devem depender o mínimo possível uns dos outros. Mudanças em uma funcionalidade não devem gerar impacto excessivo nas demais.
* **Alta Coesão:** Cada módulo deve possuir uma finalidade clara e bem definida.
* **Evolução Gradual:** O sistema deve permitir crescimento incremental. Novas funcionalidades deverão poder ser adicionadas sem necessidade de reestruturações profundas.
* **Facilidade de Refatoração:** A estrutura deve favorecer manutenção contínua.

## 4. Estrutura Geral do Projeto
O projeto será dividido em dois grandes blocos:

**Backend**
Responsável por:
* regras de negócio;
* autenticação;
* persistência;
* cálculos;
* gamificação;
* DISC;
* geração de perfil.

**Frontend**
Responsável por:
* interface;
* exibição de dados;
* formulários;
* navegação;
* experiência do usuário.

## 5. Organização de Arquivos
O projeto deverá possuir separação clara entre:
* código-fonte;
* banco de dados;
* arquivos enviados pelos usuários;
* documentação;
* recursos visuais.

Arquivos gerados pelos usuários não devem ficar misturados ao código-fonte.

## 6. Persistência de Dados
O sistema utilizará banco relacional.

Inicialmente:
* ambiente local;
* persistência simples;
* foco em desenvolvimento rápido.

A camada de acesso a dados deverá ser construída de forma que permita substituição futura do mecanismo de armazenamento sem alterar regras de negócio.

## 7. Armazenamento de Arquivos
O sistema deverá suportar armazenamento local de arquivos.
Exemplos: imagens de perfil, certificados, anexos, documentos.

Os arquivos deverão ser armazenados em estrutura separada do código-fonte. A aplicação nunca deverá depender de caminhos absolutos.

## 8. Modelo Arquitetural
A aplicação deverá utilizar arquitetura em camadas.

**Fluxo conceitual:**
`Interface -> Controladores -> Serviços -> Persistência -> Banco de Dados`

* **Interface:** Responsável pela interação com o usuário. Não deve conter regras de negócio.
* **Controladores:** Responsáveis por receber requisições, validar entrada básica e delegar processamento.
* **Serviços:** Responsáveis por regras de negócio, cálculos, gamificação, evolução de atributos, geração de missões e atualização de perfis. Toda lógica principal deverá estar concentrada nesta camada.
* **Persistência:** Responsável por leitura, gravação, atualização e remoção de dados. Não deve conter regras de negócio.

## 9. Estratégia de Desenvolvimento
O projeto será desenvolvido de forma incremental. Cada funcionalidade deverá ser implementada em ciclos independentes.

**Fluxo recomendado:**
1. Planejamento.
2. Implementação.
3. Teste.
4. Ajuste.
5. Integração.

## 10. Desenvolvimento Orientado por Contexto
Todo desenvolvimento deverá considerar como fonte principal:

* **Documento Mestre:** Define produto, objetivos, regras gerais e requisitos.
* **Documento Técnico:** Define arquitetura, organização e diretrizes.

Nenhuma implementação deverá contradizer esses documentos sem atualização prévia da documentação.

## 11. Sistema de Gamificação
A gamificação é considerada parte central do sistema. Toda implementação futura deverá respeitar os seguintes conceitos: evolução contínua, progressão profissional, recompensas, missões, atributos e histórico de evolução.

A gamificação não deverá ser tratada como módulo separado do produto. Ela faz parte do núcleo da aplicação.

## 12. Sistema DISC
O DISC deverá ser tratado como um conjunto de atributos dinâmicos.
O sistema deverá suportar:
* resultado inicial;
* evolução ao longo do tempo;
* histórico;
* atualização baseada em ações.

O DISC não deve ser tratado como resultado estático.

## 13. Sistema de Missões
O sistema deverá permitir: missões gerais, missões adaptativas, conclusão, abandono e acompanhamento.
As missões deverão influenciar diretamente a evolução do usuário.

## 14. Sistema de Perfil
O perfil será o elemento central da plataforma. Todo o restante do sistema deverá existir para enriquecer o perfil do usuário.
O perfil deverá consolidar:
* informações pessoais;
* currículo;
* evolução;
* indicadores;
* conquistas;
* atributos;
* histórico.

## 15. Currículo Vivo
O currículo deverá ser derivado das informações registradas pelo usuário. A plataforma não deve depender exclusivamente de um currículo estático enviado manualmente. O objetivo é construir uma representação dinâmica da trajetória profissional.

## 16. Perfil Público
O sistema deverá disponibilizar visualização pública dos perfis. Essa visualização deverá apresentar:
* trajetória;
* evolução;
* projetos;
* experiências;
* certificações;
* indicadores.

Sem necessidade de autenticação do visitante.

## 17. Segurança
Mesmo sendo um protótipo acadêmico, deverão ser considerados:
* autenticação;
* autorização;
* validação de entradas;
* proteção contra manipulação indevida de dados.

## 18. Escalabilidade Conceitual
Embora o projeto seja inicialmente local e acadêmico, sua estrutura deverá permitir expansão futura para:
* múltiplos cursos;
* múltiplas instituições;
* empresas;
* recrutadores;
* integração com plataformas externas.

Sem necessidade de reescrever o núcleo da aplicação.

## 19. Testabilidade
As regras de negócio deverão ser desenvolvidas de forma independente da interface.
Isso permitirá: testes unitários, validação de cálculos, validação da gamificação e validação do DISC.

## 20. Manutenibilidade
O código deverá priorizar:
* legibilidade;
* simplicidade;
* organização;
* previsibilidade.

O projeto será tratado como produto em evolução e não apenas como entrega acadêmica.

## 21. Diretriz Final
Toda decisão técnica futura deverá responder às seguintes perguntas:
1. Esta implementação respeita o Documento Mestre?
2. Esta implementação mantém a separação de responsabilidades?
3. Esta implementação facilita futuras expansões?
4. Esta implementação mantém a gamificação como elemento central?
5. Esta implementação contribui para a construção do currículo vivo?

Caso a resposta para alguma dessas perguntas seja negativa, a solução deverá ser reavaliada antes de sua implementação.