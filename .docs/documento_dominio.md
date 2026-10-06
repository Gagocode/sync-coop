# DOCUMENTO DE DOMÍNIO E REGRAS DE NEGÓCIO

## Objetivo
Este documento define os conceitos centrais do sistema e as regras que governam seu funcionamento. Enquanto o Documento Mestre define o produto e o Documento Técnico define a arquitetura, este documento define o comportamento do sistema. Seu objetivo é servir como ponte entre a documentação e a implementação.

## 1. Conceitos Fundamentais
A plataforma possui cinco pilares principais:
* Perfil
* DISC
* Missões
* Evolução
* Currículo Vivo

Todos os módulos do sistema devem contribuir para pelo menos um desses pilares.

## 2. Usuário
O usuário representa um estudante cadastrado na plataforma. Cada usuário possui:
* Perfil
* Resultado DISC
* Histórico de evolução
* Missões
* Projetos
* Certificações
* Experiências
* Conquistas

## 3. Perfil
O perfil é o elemento central da plataforma. Ele representa a evolução profissional do usuário. O perfil não é apenas um currículo. Ele é uma combinação de:
* dados pessoais;
* histórico profissional;
* indicadores;
* atributos;
* conquistas;
* evolução comportamental.

## 4. DISC
**Conceito**
O DISC será tratado como um conjunto de atributos dinâmicos. O sistema trabalha com dois estados:
* **DISC Inicial:** Resultado gerado pelo Quiz Narrativo. Representa a percepção inicial do usuário.
* **DISC Observado:** Resultado calculado continuamente. Representa o comportamento observado através das ações do usuário.

## 5. Estrutura DISC
O sistema utiliza quatro dimensões:
* **D - Dominância:** Relacionada a liderança, tomada de decisão, iniciativa e ação.
* **I - Influência:** Relacionada a comunicação, interação social, apresentações e networking.
* **S - Estabilidade:** Relacionada a consistência, colaboração, comprometimento e continuidade.
* **C - Conformidade:** Relacionada a organização, planejamento, análise e documentação.

## 6. Quiz Narrativo
O Quiz Narrativo é a porta de entrada do sistema. O usuário responde cenários contextualizados. Cada resposta possui impacto nas dimensões DISC. O sistema calcula D, I, S, C e gera o perfil inicial.

## 7. Classe Inicial
Após o quiz, o sistema gera uma representação visual do perfil. Exemplos:
* Executor Estratégico
* Comunicador
* Analista
* Colaborador

A classe possui caráter representativo. Não altera regras de negócio.

## 8. Atributos Secundários
Além do DISC, o sistema mantém atributos complementares. Exemplos:
* Liderança
* Comunicação
* Organização
* Criatividade
* Trabalho em Equipe
* Capacidade Analítica

Esses atributos podem ser derivados do DISC ou calculados separadamente. A definição final será realizada durante a implementação.

## 9. XP
XP representa a evolução geral do usuário. Toda ação relevante gera XP. O XP é utilizado para:
* acompanhar progresso;
* medir atividade;
* desbloquear níveis;
* gerar indicadores.

## 10. Níveis
O sistema poderá possuir níveis. Exemplo conceitual:
Nível 1 ↓ Nível 2 ↓ Nível 3 ↓ Nível 4
A curva de progressão será definida posteriormente.

## 11. Missões
Missões representam objetivos propostos pelo sistema. Toda missão possui:
* descrição;
* recompensa;
* prazo;
* estado.

## 12. Estados das Missões
* **Disponível:** Ainda não iniciada.
* **Aceita:** Em andamento.
* **Concluída:** Finalizada com sucesso.
* **Ignorada:** Usuário optou por não realizar. Não gera punição.
* **Abandonada:** Usuário iniciou e não concluiu. Pode gerar penalidade.
* **Expirada:** Prazo encerrado. Pode gerar impacto reduzido.

## 13. Tipos de Missão
* **Missões Padrão:** Disponíveis para todos os usuários. Exemplos: completar perfil; cadastrar projeto; cadastrar certificado.
* **Missões Adaptativas:** Geradas com base no perfil do usuário. Objetivo: estimular desenvolvimento equilibrado.

## 14. Geração de Missões Adaptativas
Regra conceitual: O sistema identifica a menor dimensão DISC observada.
Exemplo: D = 60, I = 20, S = 40, C = 70. A dimensão mais baixa é I.
O sistema gera missões voltadas para comunicação e interação.

## 15. Ações do Usuário
O sistema registra ações relevantes. Exemplos:
* criação de projeto;
* cadastro de certificado;
* cadastro de experiência;
* conclusão de missão;
* atualização de perfil.

## 16. Evidências
Toda ação gera evidências. As evidências são utilizadas para:
* atualizar atributos;
* atualizar DISC observado;
* gerar indicadores.

## 17. Atualização do DISC Observado
Cada ação possui pesos associados. Exemplo conceitual:
* **Projeto técnico:** aumenta C e S
* **Apresentação:** aumenta I e D
* **Liderança de equipe:** aumenta D e I

Os pesos exatos serão definidos posteriormente.

## 18. Penalidades
Penalidades devem ser utilizadas com moderação. Objetivo: estimular comprometimento. Não gerar frustração.
* **Ignorar missão:** Nenhuma alteração.
* **Abandonar missão:** Penalidade reduzida.
* **Expiração:** Penalidade mínima ou inexistente.

## 19. Conquistas
Conquistas são elementos cosméticos. Funções: reconhecimento, motivação, histórico. Não alteram atributos. Não alteram DISC.

## 20. Currículo Vivo
O currículo é construído dinamicamente. Baseado em: projetos, experiências, certificações, indicadores, histórico. O sistema gera automaticamente sua representação.

## 21. Perfil Público
O perfil público representa a vitrine profissional do usuário. Deve apresentar: trajetória, indicadores, projetos, experiências, certificações, evolução.

## 22. Curtidas
Usuários e visitantes podem interagir com perfis. Curtidas possuem função social. Não alteram atributos. Não alteram DISC.

## 23. Histórico
O sistema deve manter histórico de evolução. Objetivos: acompanhar progresso, visualizar crescimento, demonstrar desenvolvimento.

## 24. Indicadores
O sistema poderá apresentar indicadores visuais. Exemplos: evolução DISC, evolução de atributos, atividades realizadas, conclusão de missões.

## 25. Regras que Ainda Precisam Ser Definidas
Os itens abaixo permanecem em aberto e deverão ser definidos antes da implementação completa:
* Fórmula de cálculo do DISC Observado.
* Pesos de cada tipo de atividade.
* Curva de XP.
* Curva de níveis.
* Catálogo inicial de missões.
* Catálogo inicial de conquistas.
* Critérios para geração automática de missões adaptativas.
* Regras exatas de penalidade.
* Fórmula dos indicadores.
* Critérios de evolução de classes.

## Status do Documento
* **Versão:** 0.1
* **Status:** Em refinamento.
* **Objetivo atual:** servir como base para modelagem de domínio e implementação futura.