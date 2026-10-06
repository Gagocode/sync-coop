# DOCUMENTO MESTRE DO PRODUTO

## 1. Visão Geral
A plataforma é um sistema de desenvolvimento profissional gamificado para universitários. Seu objetivo é transformar o currículo tradicional em uma jornada contínua de evolução profissional.

Ao invés de possuir apenas um currículo estático em PDF, o usuário constrói um perfil vivo que evolui através de projetos, experiências, certificações, missões e atividades realizadas dentro da plataforma.

O sistema utiliza conceitos do modelo DISC como base para a construção do perfil comportamental inicial do usuário, permitindo acompanhar sua evolução ao longo do tempo através de evidências práticas e comportamentos observados.

O resultado é um perfil público compartilhável que apresenta não apenas informações curriculares, mas também indicadores de desenvolvimento profissional e comportamental.

## 2. Problema
Os currículos tradicionais possuem diversas limitações:
* Tornam-se desatualizados rapidamente.
* Não refletem a evolução contínua do candidato.
* Não apresentam evidências comportamentais.
* Não incentivam o desenvolvimento profissional.
* Não mostram a jornada de crescimento do usuário.

Além disso, avaliações DISC tradicionais costumam gerar apenas um resultado estático, sem acompanhar mudanças e evolução ao longo do tempo.

## 3. Solução
Criar uma plataforma onde:
* O usuário possui um currículo vivo.
* O usuário realiza um quiz narrativo baseado em DISC.
* O sistema gera um perfil comportamental inicial.
* O sistema gera missões.
* As missões incentivam desenvolvimento profissional.
* O comportamento do usuário influencia atributos DISC observados.
* O perfil evolui continuamente.
* Recrutadores podem visualizar um perfil público completo.

## 4. Público-Alvo
**Público Principal**
Universitários.
Exemplos:
* Sistemas de Informação
* Ciência da Computação
* Engenharia
* Administração
* Arquitetura
* Design
* Demais cursos

**Público Secundário**
* Recrutadores
* Empresas
* Professores
* Instituições de ensino

## 5. Objetivo do Usuário
O objetivo final do usuário é:
* Desenvolver sua carreira.
* Evoluir seu perfil profissional.
* Construir evidências de experiência.
* Obter maior empregabilidade.
* Conseguir oportunidades profissionais.

## 6. Fluxo Principal
* **Etapa 1:** Cadastro.
* **Etapa 2:** Quiz Narrativo DISC.
* **Etapa 3:** Geração do Perfil Inicial.
* **Etapa 4:** Recebimento de Missões.
* **Etapa 5:** Execução de Atividades.
* **Etapa 6:** Ganho de XP e Evolução.
* **Etapa 7:** Atualização dos Atributos.
* **Etapa 8:** Construção do Currículo Vivo.
* **Etapa 9:** Compartilhamento do Perfil Público.

## 7. Sistema DISC
**Conceito**
O DISC não será tratado como um teste estático.
Será tratado como um sistema de atributos vivos.

**Dimensões**
* **D:** Dominância
* **I:** Influência
* **S:** Estabilidade
* **C:** Conformidade

**DISC Inicial**
Obtido através do Quiz Narrativo.
Exemplo:
* $D=65$
* $I=40$
* $S=35$
* $C=70$

**DISC Observado**
Calculado continuamente. Baseado em:
* Projetos
* Certificações
* Experiências
* Missões
* Comportamentos

**Perfil Final**
O sistema exibe:
* DISC Inicial
* DISC Atual
* Evolução Histórica

## 8. Sistema de Classes
Após o Quiz Narrativo o sistema gera uma classe inicial.
Exemplos:
* Executor Estratégico
* Comunicador
* Analista
* Colaborador
* Líder Técnico

As classes servem para representação do perfil. Não substituem o DISC.

## 9. Sistema de Atributos
O usuário possui atributos derivados.
Exemplos:
* Liderança
* Comunicação
* Organização
* Criatividade
* Trabalho em Equipe
* Capacidade Analítica

Esses atributos evoluem conforme ações realizadas.

## 10. Sistema de XP
Toda atividade relevante gera XP.

**Exemplos:**
* **Baixo Impacto:** Atualizar perfil, Adicionar foto, Completar informações.
* **Médio Impacto:** Participar de evento, Completar missão.
* **Alto Impacto:** Projeto, Certificação, Experiência profissional.

## 11. Sistema de Missões
**Missões Fixas**
Geradas para todos os usuários.
Exemplos: Completar perfil, Adicionar projeto, Adicionar certificado, Atualizar currículo.

**Missões Adaptativas**
Baseadas nas menores dimensões do usuário.
Exemplo: Baixa influência.
Missão sugerida: Participar de evento.

## 12. Estados da Missão
* **Concluída:** Recompensa (XP, Evolução de atributos)
* **Ignorada:** Consequência (Nenhuma alteração)
* **Abandonada:** Consequência (Penalidade de XP)

## 13. Sistema de Conquistas
As conquistas possuem função cosmética. Não afetam atributos.
Exemplos:
* Primeiro Projeto
* Primeiro Certificado
* Perfil Completo
* Primeiro Evento
* Primeiro Compartilhamento

## 14. Currículo Vivo
O currículo não será um formulário tradicional. Será construído a partir de:
* Projetos
* Experiências
* Certificados
* Conquistas
* Indicadores

O sistema gera automaticamente a visão curricular.

## 15. Perfil Público
Cada usuário possui uma página pública (Ex: `usuario.plataforma.com/nome`).

**Informações Públicas:**
* Nome
* Foto
* Curso
* Classe
* Projetos
* Certificações
* Experiências
* Indicadores
* Evolução
* DISC

## 16. Sistema Social
Usuários poderão:
* Compartilhar perfil
* Visualizar perfis
* Curtir perfis

*Sem sistema de mensagens no MVP.*

## 17. Indicadores de Evolução
O sistema deve mostrar:
* Evolução DISC
* Evolução de atributos
* Histórico de atividades
* Missões concluídas
* Projetos realizados

## 18. Requisitos Funcionais
* **RF01:** Cadastro de usuário.
* **RF02:** Login.
* **RF03:** Realização do Quiz Narrativo.
* **RF04:** Cálculo do DISC Inicial.
* **RF05:** Geração da Classe Inicial.
* **RF06:** Geração de Missões.
* **RF07:** Conclusão de Missões.
* **RF08:** Sistema de XP.
* **RF09:** Sistema de Atributos.
* **RF10:** Sistema de Conquistas.
* **RF11:** Cadastro de Projetos.
* **RF12:** Cadastro de Certificações.
* **RF13:** Cadastro de Experiências.
* **RF14:** Geração do Currículo Vivo.
* **RF15:** Perfil Público.
* **RF16:** Sistema de Curtidas.
* **RF17:** Histórico de Evolução.
* **RF18:** Atualização do DISC Observado.

## 19. Requisitos Não Funcionais
* **RNF01:** Interface responsiva.
* **RNF02:** Navegação intuitiva.
* **RNF03:** Tempo de resposta inferior a 3 segundos.
* **RNF04:** Compatibilidade com dispositivos móveis.
* **RNF05:** Segurança de autenticação.
* **RNF06:** Escalabilidade para múltiplos cursos.
* **RNF07:** Arquitetura modular.
* **RNF08:** Facilidade de manutenção.
* **RNF09:** Facilidade de expansão futura.
* **RNF10:** Persistência dos dados dos usuários.

## 20. MVP
**Escopo mínimo para apresentação:**
* Cadastro
* Login / Logout
* Quiz Narrativo
* Resultado DISC
* Perfil
* Missões
* XP

**Sem:**
* Projetos
* Certificados
* Perfil Público
* Empresas
* Busca avançada
* Recomendação automática
* IA
* Chat
* Integrações externas

## 21. Visão de Futuro
Possíveis evoluções:
* Empresas cadastradas
* Portal de vagas
* Match entre perfil e vaga
* Recomendações por IA
* Mentorias
* Ranking universitário
* Integração com LinkedIn
* Exportação automática de currículo
* Dashboard institucional para universidades

## Definição Final do Produto
Uma plataforma gamificada de desenvolvimento profissional para universitários, onde um quiz narrativo baseado em DISC gera um perfil inicial e um conjunto de atributos comportamentais. Através de missões, projetos, certificações e experiências, o usuário desenvolve continuamente seu perfil, construindo um currículo vivo e público que demonstra sua evolução profissional ao longo do tempo.