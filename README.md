# Sync Disc

Sync Disc e uma plataforma gamificada de desenvolvimento profissional para universitarios. O projeto transforma o curriculo tradicional em um perfil vivo, evolutivo e compartilhavel, combinando informacoes curriculares, missoes, XP, conquistas e indicadores comportamentais baseados no modelo DISC.

## Visao geral

A proposta do sistema e permitir que estudantes construam uma jornada profissional continua. Em vez de manter apenas um curriculo estatico em PDF, o usuario evolui seu perfil por meio de atividades como quiz narrativo, conclusao de missoes, registro de projetos, certificacoes, experiencias e outras evidencias praticas.

O DISC e tratado como um conjunto de atributos dinamicos:

- **D - Dominancia:** lideranca, iniciativa, decisao e acao.
- **I - Influencia:** comunicacao, interacao social, apresentacoes e networking.
- **S - Estabilidade:** consistencia, colaboracao, comprometimento e continuidade.
- **C - Conformidade:** organizacao, planejamento, analise e documentacao.

O sistema trabalha com um **DISC inicial**, obtido pelo quiz narrativo, e um **DISC observado**, atualizado ao longo do tempo a partir das acoes do usuario.

## Objetivo do produto

O objetivo do Sync Disc e ajudar universitarios a:

- desenvolver sua carreira;
- construir evidencias de experiencia;
- acompanhar sua evolucao profissional;
- visualizar atributos comportamentais e tecnicos;
- aumentar empregabilidade;
- compartilhar um perfil publico mais completo que um curriculo tradicional.

## Publico-alvo

O publico principal sao universitarios de diferentes cursos, como Sistemas de Informacao, Ciencia da Computacao, Engenharia, Administracao, Arquitetura, Design e areas relacionadas.

Tambem fazem parte do publico secundario recrutadores, empresas, professores e instituicoes de ensino.

## Fluxo principal

1. Cadastro do usuario.
2. Login.
3. Quiz Narrativo DISC.
4. Geracao do perfil inicial.
5. Recebimento de missoes.
6. Execucao de atividades.
7. Ganho de XP e evolucao.
8. Atualizacao de atributos e DISC observado.
9. Construcao do curriculo vivo.
10. Compartilhamento do perfil publico.

## MVP

O escopo minimo previsto para apresentacao inclui:

- cadastro;
- login e logout;
- quiz narrativo;
- resultado DISC;
- perfil do usuario;
- missoes;
- XP.

Ficam fora do MVP inicial:

- projetos;
- certificados;
- perfil publico;
- empresas;
- busca avancada;
- recomendacao automatica;
- inteligencia artificial;
- chat;
- integracoes externas.

## Pilares do dominio

O sistema e orientado por cinco pilares:

- **Perfil:** elemento central da plataforma e consolidacao da evolucao profissional.
- **DISC:** atributos comportamentais iniciais e observados.
- **Missoes:** objetivos propostos ao usuario para estimular desenvolvimento.
- **Evolucao:** XP, niveis, historico, indicadores e progresso.
- **Curriculo vivo:** representacao dinamica da trajetoria do usuario.

## Arquitetura

O projeto deve seguir arquitetura em camadas, separando responsabilidades entre interface, controladores, servicos, persistencia e banco de dados.

Fluxo conceitual:

```text
Interface -> Controladores -> Servicos -> Persistencia -> Banco de Dados
```

No backend, a diretriz principal e:

```text
Controllers
-> Services
-> Repositories
-> Database
```

Regras de negocio devem permanecer na camada de servicos. Controladores devem receber requisicoes, validar entradas basicas e delegar processamento. Repositories devem cuidar da persistencia sem conter regras de negocio.

## Estrutura do repositorio

```text
.
+-- .docs/
|   +-- agent.md
|   +-- documento_dominio.md
|   +-- documento_mestre.md
|   +-- documento_tecnico.md
+-- backend/
|   +-- progress_backend.md
+-- frontend/
|   +-- progress_frontend.md
+-- .editorconfig
+-- .gitattributes
+-- .gitignore
+-- README.md
```

## Documentacao oficial

Antes de qualquer implementacao, alteracao, correcao ou refatoracao, leia obrigatoriamente:

1. `.docs/documento_mestre.md`
2. `.docs/documento_tecnico.md`
3. `.docs/documento_dominio.md`

Esses documentos sao a fonte oficial de verdade do projeto.

Em caso de conflito entre documentos, a prioridade e:

1. Documento Mestre
2. Documento Tecnico
3. Documento de Dominio

## Registro de progresso

Toda alteracao em `backend/` deve ser registrada em:

```text
backend/progress_backend.md
```

Toda alteracao em `frontend/` deve ser registrada em:

```text
frontend/progress_frontend.md
```

O registro deve conter data, funcionalidade, resumo e impacto esperado.

## Diretrizes de desenvolvimento

- Manter simplicidade e clareza.
- Evitar complexidade prematura.
- Preservar baixo acoplamento e alta coesao.
- Nao criar microservicos ou arquitetura distribuida no escopo atual.
- Nao introduzir dependencias sem necessidade comprovada.
- Nao alterar regras de negocio sem atualizar previamente a documentacao.
- Manter a gamificacao, o DISC evolutivo e o curriculo vivo como elementos centrais.

## Status

Projeto em fase inicial de documentacao e estruturacao para implementacao futura.

## Licenca

Licenca ainda nao definida. Antes de publicar ou distribuir o projeto, escolha uma licenca adequada e adicione um arquivo `LICENSE` na raiz do repositorio.
