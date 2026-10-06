# Sync Disc — Design System

**Status:** Identidade visual oficial V2 — evolução profissional gamificada
**Escopo:** identidade visual, interface e experiência do frontend  
**Princípio do produto:** cada tela deve ajudar estudantes a reconhecer, registrar e comunicar sua evolução profissional.

Este documento consolida a direção visual do Sync Disc a partir dos documentos de produto e da codebase frontend. Ele orienta futuras telas e revisões de interface. A camada visual deve apresentar dados e fluxos definidos pelo produto, sem criar regras de negócio, resultados, recompensas ou dados fictícios.

## 1. Brand Personality

### Quem é o Sync Disc

O Sync Disc é uma plataforma de desenvolvimento profissional para universitários. Ajuda cada pessoa a transformar experiências acadêmicas e profissionais em evidências de uma trajetória que cresce com o tempo. O DISC oferece um ponto de partida comportamental; missões sugerem ações; projetos, certificados e experiências enriquecem o Perfil e o Currículo Vivo.

O produto combina:

- **Credibilidade:** apresenta informações com clareza e trata o perfil profissional com cuidado.
- **Juventude:** fala com pessoas no início ou em transição de carreira, sem adotar códigos infantis.
- **Descoberta:** convida a conhecer o próprio perfil e identificar caminhos de desenvolvimento.
- **Progresso:** torna visíveis ações, marcos e mudanças ao longo do tempo.
- **Acolhimento:** reconhece que carreiras são construídas gradualmente e por diferentes caminhos.

### Quem não é o Sync Disc

O Sync Disc não é um ERP, uma ferramenta administrativa, um dashboard corporativo de métricas, uma rede social, um jogo infantil ou um template SaaS intercambiável. Também não é uma avaliação psicológica definitiva nem um rótulo fixo de personalidade. Classes e DISC representam o perfil inicial conforme as regras do produto; não substituem a pessoa nem determinam seu potencial.

## 2. Design DNA

### Personalidade

**Profissional, curiosa, encorajadora, energética e concreta.** A interface transmite potencial e crescimento. Ela reconhece conquistas com cor e hierarquia visual, sempre relacionando progresso a atividades e evidências reais.

### Tom visual

- Base clara e levemente azulada, com azul profundo para confiança e azul vibrante para ação.
- Ciano e turquesa marcam descoberta, interação e evolução.
- Amarelo suave identifica XP; laranja suave identifica conquistas. Ambos devem ser fáceis de localizar, sem ocupar toda a interface.
- Cores de progresso devem aparecer em elementos reais de progressão, e não apenas como detalhes decorativos.
- Contraste suficiente para leitura e hierarquia tipográfica visível.
- Composição assimétrica e linhas de percurso dão identidade às jornadas. Áreas coloridas e pequenos gradientes podem ampliar energia em progresso e missão ativa; não transformar toda seção em um painel de cards.

### Linguagem visual

- Usar títulos expressivos, alinhados à esquerda, e texto direto que explique a informação apresentada.
- Preferir marcadores de etapa, linhas de evolução, superfícies coloridas e fundos claros com matiz azul a excesso de cinza e sombras grandes.
- Usar ícones consistentes provenientes de uma biblioteca ou assets do produto. Letras isoladas podem ser usadas como iniciais ou identificadores explícitos, não como substitutos improvisados de ícones.
- Reservar ilustrações a funções de orientação ou identidade. Evitar arte genérica de IA, ornamentos sem significado e ilustrações que prometam funcionalidades inexistentes.
- Apresentar conteúdo real do usuário ou texto editorial que seja claramente explicativo. Não inventar métricas, depoimentos, perfis ou atividade para preencher espaços.

### Nível de gamificação

**Visível e orientado à carreira.** O usuário deve perceber XP, missão ativa, conquista e progresso sem precisar procurar por eles. Usar números legíveis, cor semântica, marcadores, animações breves e recompensas claramente associadas à ação que as gerou. A energia visual pode se aproximar de Spotify Wrapped, GitHub Profile, Duolingo e Linear: absorver a celebração de dados, a identidade construída por contribuições, o feedback imediato e a clareza de interação. Não copiar layouts, mascotes, ranking, feed ou linguagem visual proprietária. Evitar infantilização, competição artificial e urgência inventada.

## 3. Paleta Oficial

As cores abaixo são tokens de referência. Manter seus papéis consistentes entre Dashboard, fluxo de entrada, perfil público e telas legadas. Tons mais claros podem ser derivados para fundos e estados, preservando contraste nos textos.

| Token | Cor | Uso |
|---|---|---|
| **Primária — Azul vibrante** | `#0085FF` | Ação principal, navegação ativa, identidade e progresso de alta visibilidade. |
| **Profundo — Azul profundo** | `#0056A4` | Títulos, superfícies de destaque e contraste de confiança. |
| **Azul gelo** | `#E0F2FF` | Superfícies leves, trilhas de progresso e estados de seleção. |
| **Descoberta — Ciano** | `#14B8D4` | Ligações entre etapas e sinais de descoberta. |
| **Evolução — Turquesa** | `#008F9E` | Etapas concluídas e crescimento. Usar em áreas gráficas ou com tinta escura. |
| **XP — Amarelo suave** | `#F5C84C` | XP acumulado e recompensa de missão. Dar destaque visível ao número e usar tinta escura sobre o amarelo. |
| **Conquistas — Laranja suave** | `#F28B45` | Marcos desbloqueados e reconhecimento cosmético. Usar em ícone, contorno ou superfície clara alaranjada. |
| **Certificados e DISC C — Violeta** | `#7567D8` | Diferencia certificados e a dimensão C sem competir com o azul principal. |
| **Tinta principal** | `#122D50` | Títulos, texto principal e dados prioritários. |
| **Texto secundário** | `#526B86` | Instruções, metadados e descrições. |
| **Fundo de página** | `#F4F9FF` | Base clara com matiz azul. |
| **Superfície** | `#FFFFFF` | Campos, conteúdo principal e superfícies elevadas de forma simples. |
| **Borda** | `#D4E4F4` | Divisores e limites de componentes. |
| **Erro** | `#D94B4B` | Erros de validação e ações malsucedidas, sempre acompanhados por texto. |

### Cores DISC

Manter as quatro dimensões distintas e estáveis em todos os gráficos e comparações. A cor identifica a dimensão; não expressa que uma dimensão é melhor ou pior.

| Dimensão | Identificação | Cor |
|---|---|---|
| D — Dominância | D | `#0085FF` |
| I — Influência | I | `#F28B45` |
| S — Estabilidade | S | `#008F9E` |
| C — Conformidade | C | `#7567D8` |

Não depender somente da cor para diferenciar dimensões: mostrar também letra e nome. Evitar o esquema de semáforo para sugerir valor positivo ou negativo de um perfil.

### Uso e contraste

- Evitar predominância de cinza, verde petróleo e cores corporativas apagadas. Azul, ciano, turquesa, amarelo e laranja formam a assinatura energética da plataforma.
- Não combinar todos os acentos em cada componente. Primária e neutros azulados sustentam a interface; ciano, turquesa, XP e conquistas mantêm seus papéis semânticos.
- Amarelo de XP e laranja de conquista precisam se distinguir entre si e de erros. Texto sobre essas superfícies usa tinta escura; não usar branco sobre tons suaves.
- Estados de erro, sucesso e foco também precisam de rótulo, ícone apropriado ou explicação textual.

## 4. Tipografia

### Famílias

- **Títulos:** Space Grotesk, já usada no dashboard, com fallback `Arial, Helvetica, sans-serif`. Seu desenho dá personalidade sem tornar o produto informal.
- **Subtítulos e texto:** DM Sans, já usada no dashboard, com fallback `Arial, Helvetica, sans-serif`. Usar uma família de leitura coerente nas áreas de entrada e nas páginas internas.
- **Dados numéricos:** usar algarismos tabulares quando a comparação ou alinhamento de XP, percentuais e contagens exigir.

Carregar fontes de forma consistente e manter fallbacks locais. A tela deve continuar legível se a fonte externa não estiver disponível. Evitar introduzir uma nova família por feature.

### Hierarquia e pesos

- **H1:** 36–64 px em telas amplas; reduzir fluidamente em telas menores. Peso 600–700 e entrelinha compacta.
- **H2:** 24–32 px, peso 600–700.
- **H3 e títulos de componente:** 16–20 px, peso 600–700.
- **Texto corrido:** 14–16 px, peso 400, entrelinha de 1,5 a 1,7.
- **Rótulos e metadados:** 12–14 px, peso 500–600; não reduzir abaixo de 12 px para informação necessária.
- **Números em destaque:** 24–32 px, peso 600–700; a unidade, contexto e período ficam visíveis junto do valor.

Usar caixa alta com parcimônia. Evitar tracking exagerado e rótulos decorativos que não acrescentem contexto.

## 5. Componentes

### Cards e superfícies

- Usar cards para agrupar conteúdo relacionado, não para cada linha de informação.
- Fundo branco ou azul muito claro, borda fina e raio entre 8 e 14 px.
- Sombras discretas ou ausentes; elevação não deve competir com conteúdo.
- Limitar a quantidade de cards lado a lado. Priorizar hierarquia, divisores e seções com títulos claros.
- Uma área em destaque pode usar azul profundo, ciano ou turquesa, especialmente para a missão ativa. Cores fortes devem ter função e dados reais associados.

### Botões

- **Primário:** azul vibrante, texto branco; uma ação principal por região. Usar para avançar a jornada ou salvar uma ação importante.
- **Secundário:** contorno ou fundo ciano claro para ações de apoio.
- **Terciário:** link ou botão sem fundo para ações de navegação secundárias.
- **Destrutivo:** estilo discreto com cor de erro, confirmação explícita e rótulo específico.
- Altura mínima recomendada de 40 px, área de toque confortável em dispositivos móveis, estados hover/focus/disabled perceptíveis e foco visível por teclado.
- Usar rótulos de ação claros: “Adicionar projeto”, “Ver perfil”, “Continuar”. Evitar texto temático que esconda o efeito do botão.

### Inputs e formulários

- Rótulo visível e persistente acima ou ao lado do campo; placeholder não substitui rótulo.
- Campos com altura confortável, borda azulada clara e foco em azul vibrante ou ciano.
- Informar claramente campos opcionais, formato esperado e erro junto ao campo correspondente.
- Agrupar os dados em etapas quando isso reduzir esforço, preservando resumo e indicação do progresso.
- Formulários devem explicar como os dados contribuem para o Perfil ou Currículo Vivo quando isso for útil.

### Badges

- Usar badges para estados curtos e úteis, como “Disponível”, “Concluída”, nível atual ou dimensão DISC.
- Preferir fundos suaves e texto escuro; usar pill com moderação, evitando etiquetar cada dado.
- Um badge deve sempre manter texto compreensível, não apenas cor.

### Missões

- Destacar visualmente a missão ativa com superfície azul vibrante/profunda, título, descrição, estado, próxima ação e recompensa existente. Ela deve ser identificada de imediato como o próximo passo.
- Mostrar missões seguintes com menor peso visual e relação clara com a sequência.
- Tratar missão como oportunidade de registrar uma evidência ou desenvolver uma habilidade; evitar linguagem de tarefa administrativa.
- Estados e ações exibidos devem refletir exatamente o backend. Não insinuar que uma missão pode ser aceita, ignorada ou concluída manualmente se esse fluxo não existe.

### XP e níveis

- Exibir XP com contexto: acumulado, recompensa ou distância para o próximo nível. O valor deve ser um dos primeiros sinais visuais de gamificação que a pessoa percebe.
- Usar amarelo suave `#F5C84C` como fundo ou badge para XP, com texto escuro. Usar azul vibrante `#0085FF` nas barras de progresso e turquesa `#008F9E` em etapas concluídas; apresentar descrição textual e valor relacionado.
- Níveis representam progressão da plataforma, não senioridade ou competência profissional.
- Não inventar curvas, limites, recompensas ou animações de nível diferentes das regras vigentes.

### Conquistas

- Dar tratamento de reconhecimento visível e caloroso, com superfície, ícone ou contorno laranja suave `#F28B45`, nome, descrição e data quando disponível.
- Conquistas são cosméticas segundo as regras atuais; não apresentá-las como bônus de atributo ou DISC.
- Estados bloqueados só devem aparecer se o produto fornecer essa informação e a tela explicar o que significa.

### Timelines e histórico

- Ordenar atividades por data e manter título, descrição e data legíveis.
- Uma linha ou marcador visual pode conectar eventos, com ênfase no evento mais recente sem ocultar os anteriores.
- Evitar timeline ornamental sem conteúdo real ou datas inventadas.

### Indicadores DISC

- Mostrar letra, nome completo e valores com uma escala clara.
- Distinguir explicitamente DISC Inicial de DISC Observado, explicando a origem de cada um.
- Em gráficos de barras, alinhar escala, rótulos e valores; não truncar diferenças nem sugerir diagnóstico clínico.
- A classe inicial pode complementar a leitura narrativa, mas nunca substituir o resultado DISC.
- Variações e tendências só devem ser exibidas quando suportadas por dados e histórico existentes.

### Movimento e acessibilidade

- Usar transições curtas para orientar mudança de etapa, seleção e progresso; respeitar `prefers-reduced-motion`.
- Garantir teclado, foco visível, hierarquia semântica, rótulos acessíveis e contraste suficiente.
- Em layouts responsivos, manter a ação principal e a informação de progresso próximas do conteúdo relacionado.

## 6. Experiência

Ao utilizar o Sync Disc, a pessoa deve sentir evolução, conquista, descoberta, progresso e potencial. A interface transmite energia sem perder credibilidade: cores vivas destacam ações e marcos enquanto fundos claros e textos de alto contraste mantêm leitura simples. A pessoa compreende onde está, percebe o que já construiu e enxerga um próximo passo possível, sem pressão ou julgamento.

Cada fluxo deve responder, com linguagem simples:

1. Onde estou na minha trajetória?
2. O que esta informação representa?
3. Que ação ou evidência vem a seguir?

O registro de projetos, certificados e experiências deve parecer construção de um perfil, não manutenção de cadastro. A gamificação deve reconhecer ações reais e tornar o progresso perceptível. O DISC deve ser apresentado como referência inicial e atributo que pode evoluir, sem transformar o resultado em identidade fixa.

## 7. Análise do Sistema Atual

### Dashboard autenticado — estilo A

**Estado observado:** página principal em tela única, abas para Dashboard, Perfil, Projetos, Certificados, Missões, Conquistas e Evolução; missão persistente; dados carregados via endpoints existentes. Usa DM Sans e Space Grotesk, cartões arredondados, sombras leves e gamificação existente. A camada visual V1 aplica azul vibrante, azul profundo, ciano e turquesa, com XP amarelo em destaque e conquistas em laranja suave.

- **Manter:** missão ativa em destaque, visão conjunta de Perfil/DISC/Currículo Vivo, progresso real, histórico, indicadores e abas que evitam páginas CRUD dispersas.
- **Melhorar:** reduzir a repetição de cards; manter hierarquia editorial; conectar XP e conquistas às atividades reais; reforçar nomes e estados existentes; revisar a composição em telas pequenas.
- **Remover:** roxo como cor dominante, neutralidade excessiva, ícones improvisados com letras quando deveriam ser ícones e indicadores sem contexto ou hierarquia.

### Login — estilo B / Experience Overhaul V1

**Estado observado:** composição assimétrica com mensagem de produto, linha gráfica que representa etapas e formulário separado. Paleta azul, petróleo e neutros; campos simples e copy centrada na trajetória.

- **Manter:** headline de Currículo Vivo, mensagem clara, composição assimétrica, percurso visual e formulário objetivo.
- **Melhorar:** alinhar famílias tipográficas, cores e estados aos tokens oficiais; garantir responsividade e acessibilidade; manter o percurso colorido em azul, ciano, turquesa, amarelo e laranja suave.
- **Remover:** dependência visual de cores ou componentes que só existam no fluxo de entrada, bem como rótulos decorativos sem valor informativo.

### Cadastro — estilo B / Experience Overhaul V1

**Estado observado:** cadastro como início da identidade profissional, com benefícios Perfil Público, DISC Evolutivo, Missões e Currículo Vivo junto aos campos existentes.

- **Manter:** apresentação de benefícios reais e relação do cadastro com a jornada profissional.
- **Melhorar:** equilibrar o texto e a lista de benefícios em telas pequenas, manter curso como opcional quando assim definido no formulário e aplicar padrões compartilhados de formulário.
- **Remover:** repetição promocional, benefícios apresentados como garantias de resultado e campos que não correspondam aos dados aceitos pelo produto.

### Quiz DISC — estilo B / Experience Overhaul V1

**Estado observado:** cenário por etapa, quatro alternativas, progresso, navegação de retorno e submissão por identificadores/valores DISC esperados pelo backend; conteúdo narrativo apresentado pelo frontend.

- **Manter:** jornada progressiva, cenário contextualizado, equilíbrio entre alternativas, indicador de etapa e movimento reduzido respeitando acessibilidade.
- **Melhorar:** manter situações relevantes à vida acadêmica e profissional; garantir clareza de seleção, navegação por teclado e indicação de erro; revisar equilíbrio e neutralidade dos textos com o produto.
- **Remover:** revelação visual da dimensão associada a cada alternativa, linguagem de teste que pareça diagnóstico e perguntas que permitam ao usuário inferir uma resposta “correta”.

### Resultado DISC — estilo B / Experience Overhaul V1

**Estado observado:** classe e narrativa inicial, pontos fortes, oportunidades de evolução, percentuais DISC e próximo passo ligado a Completar Perfil.

- **Manter:** classe complementar, explicação humana, DISC Inicial visível, separação entre ponto de partida e evolução, missão e CTA para continuar.
- **Melhorar:** sempre derivar nomes e valores dos dados vigentes; deixar explícito que o perfil é inicial e evolutivo; aplicar cores DISC consistentes; dar destaque à classe, evolução e missão seguinte; validar textos de classe e descrições com o produto.
- **Remover:** afirmações deterministas sobre personalidade, sugestões de pontuação inventada, gráficos sem escala explicada ou um resultado apresentado como definitivo.

### Demais páginas e sistema compartilhado

O frontend também contém páginas de perfil interno e público, missões, projetos e certificados, além de formulários e detalhes dessas entidades. Parte dessas páginas usa `.app-shell`, `.panel` e controles genéricos antigos; o dashboard tem um conjunto próprio de classes e a experiência de entrada outro conjunto. O `style.css` reúne essas camadas, inclusive cores antigas roxas e regras globais que podem produzir diferenças entre páginas.

- **Manter:** dados reais do Perfil, projetos, certificados, missões, conquistas, histórico, DISC Inicial/Observado e estados vazios úteis.
- **Melhorar:** levar as páginas legadas ao mesmo sistema de tokens; harmonizar navegação, tipografia, formulários e superfícies; apresentar o perfil público como currículo e evidências; cuidar de estados vazios e responsividade.
- **Remover:** diferenças de estilo sem intenção entre rotas, ações CRUD dominando a hierarquia e conteúdo duplicado que não ajude a contar a trajetória.

## 8. Diretrizes Futuras

### Perfil Público

- Tratar como apresentação profissional compartilhável, com hierarquia editorial e contexto para curso, classe e trajetória.
- Dar prioridade a projetos, experiências, certificados, DISC, evolução e indicadores realmente disponíveis.
- Mostrar o DISC Inicial e Observado com origem e significado; distinguir evidências de interpretação.
- O perfil deve permanecer compreensível para visitantes sem conta e não deve parecer feed ou rede social.

### Dashboard

- Abrir com saudação e uma leitura simples de progresso apoiada em dados reais.
- Exibir XP atual em amarelo suave com alto contraste e contexto claro.
- Dar destaque imediato à missão ativa em azul vibrante/profundo; mostrar sua recompensa de XP sem esconder descrição ou próxima ação.
- Dar às conquistas desbloqueadas um acento laranja suave visível, preservando seu caráter cosmético.
- Equilibrar três camadas: identidade e progresso; DISC e missão; evidências do Currículo Vivo e histórico.
- Usar ciano e turquesa para interação e progresso. Manter navegação curta e previsível. Evitar painel corporativo de métricas, excesso de abas ou cards repetidos.

### Currículo Vivo

- Apresentar projetos, certificados e experiências como evidências de uma trajetória, com descrição, autoria e datas fornecidas pelo usuário.
- Priorizar leitura, escaneabilidade e compartilhamento; evitar que a visão principal pareça uma lista de formulários.
- Estados vazios devem explicar que tipo de evidência pode ser adicionada e seu papel no perfil, sem inventar conteúdo.

### Missões

- Apresentar cada missão como passo concreto de desenvolvimento ou construção do perfil.
- Usar uma superfície marcante na missão ativa e deixar o estado visualmente legível.
- Evidenciar disponibilidade, descrição, status e XP conforme dados reais.
- Explicar o vínculo entre missão e jornada sem criar urgência ou punição visual excessiva.
- Respeitar o fluxo de estados implementado; interface não estabelece novas regras de missão.

### Evolução

- Mostrar progresso temporal com datas, atividades e métricas que existam.
- Usar azul vibrante, ciano e turquesa para tornar barras e etapas fáceis de localizar; amarelo destaca XP.
- Relacionar a evolução a ações e evidências que a pessoa reconhece.
- Manter níveis e XP no papel de gamificação, sem tratá-los como medida de empregabilidade ou competência absoluta.
- Comparações DISC devem identificar explicitamente estado inicial e observado, mantendo escala e cores constantes.

### Conquistas

- Reconhecer marcos com acento laranja suave claramente visível, linguagem adulta e visual caloroso, sem competir com o conteúdo curricular.
- Manter conquistas como cosméticas enquanto as regras do produto assim definirem.
- Exibir datas e descrições somente quando fornecidas pelo sistema.

### Processo para novas features

1. Identificar qual pilar do produto a feature reforça: Perfil, DISC, Missões, Evolução ou Currículo Vivo.
2. Definir a necessidade do usuário, o impacto esperado e riscos de parecer CRUD, ERP, dashboard genérico ou template de IA.
3. Esboçar a hierarquia e o fluxo antes de escolher componentes.
4. Reutilizar tokens, tipografia e padrões deste documento; propor alteração do sistema quando houver razão de produto, em vez de introduzir exceção silenciosa.
5. Usar apenas rótulos, números, estados e promessas correspondentes ao produto e aos dados disponíveis.
6. Considerar mobile, acessibilidade, estados vazios, carregamento, erro e redução de movimento.
7. Revisar a feature como parte da trajetória: ela ajuda a pessoa a entender seu perfil, registrar evidências ou perceber evolução?

## 9. Checklist de Aprovação

Antes de aprovar qualquer tela futura, responder:

- Parece o Sync Disc?
- Parece um produto profissional?
- Demonstra evolução?
- Possui identidade própria?
- Reforça o conceito de Currículo Vivo?
- Evita aparência de ERP?
- Evita aparência de template de IA?

Também verificar:

- A tela fortalece pelo menos um pilar do produto?
- O DISC aparece como ponto de partida evolutivo, quando aplicável?
- Missões, XP, níveis e conquistas correspondem às regras e aos dados existentes?
- Há hierarquia clara sem excesso de cards, navegação ou elementos decorativos?
- Cores, tipografia, estados e comportamento responsivo seguem este documento?
- Conteúdo, estados vazios, acessibilidade e movimento foram tratados com clareza?

## Referências de linguagem visual

As referências indicam qual qualidade absorver, sem copiar layout, componentes proprietários ou linguagem de marca.

| Referência | Absorver | Evitar |
|---|---|---|
| **Spotify Wrapped** | Celebração visual de uma trajetória real, hierarquia expressiva e uso de cor para dar valor aos marcos. | Estatísticas inventadas, animação contínua e excesso de efeitos em telas de tarefa. |
| **GitHub Profile** | Evidências concretas organizadas como uma história de contribuição e atividade ao longo do tempo. | Aparência de ferramenta para desenvolvedores ou gráficos densos sem contexto profissional. |
| **Duolingo** | Feedback rápido, progresso fácil de entender e energia visual. | Mascotes, pressão por sequência diária, competição e estética infantil. |
| **Linear** | Clareza de interação, acabamento e organização visual consistente. | Sobriedade monocromática excessiva ou aparência de ferramenta corporativa de tarefas. |

## Exemplos Práticos

### Login ideal

Manter a composição assimétrica atual: mensagem do Currículo Vivo e percurso visual à esquerda, acesso à direita. Azul vibrante identifica a ação principal; ciano e turquesa marcam a sequência; texto e campos permanecem claros e acessíveis. A tela comunica início de trajetória sem virar uma página promocional.

### Dashboard ideal

No primeiro olhar, tornar legíveis XP atual, progresso e missão ativa. XP aparece em amarelo suave; missão em uma área azul de destaque com recompensa visível; conquistas em laranja suave; barras e etapas de evolução usam turquesa/ciano. DISC, evidências do Currículo Vivo e histórico completam a leitura em seções hierarquizadas, sem reduzir a experiência a um painel de métricas.

### Perfil Público ideal

Apresentar a identidade profissional com destaque, seguida por evidências reais, DISC inicial/observado, evolução e conquistas. Usar os acentos coloridos para esclarecer a leitura de progresso e marcos, enquanto projetos e experiências recebem espaço editorial suficiente para demonstrar trabalho. A página deve ser compartilhável e profissional, sem se transformar em feed social.
