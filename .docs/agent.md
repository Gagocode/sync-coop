# AGENT.md

## Papel do Agente

Você atua como desenvolvedor dentro do projeto Sync Disc.

Antes de realizar qualquer implementação, alteração, correção ou refatoração, siga obrigatoriamente este processo.

---

# ORDEM DE LEITURA OBRIGATÓRIA

Antes de iniciar qualquer tarefa:

1. Ler `.docs/documento_mestre.md`
2. Ler `.docs/documento_tecnico.md`
3. Ler `.docs/documento_dominio.md`

Esses documentos são a fonte oficial de verdade (SSOT).

---

# HIERARQUIA DOS DOCUMENTOS

Em caso de conflito entre documentos:

1. Documento Mestre
2. Documento Técnico
3. Documento de Domínio

Nenhuma implementação deve contradizer os documentos sem justificativa explícita.

---

# ANÁLISE OBRIGATÓRIA ANTES DE CODIFICAR

Antes de implementar qualquer alteração:

* Identificar qual requisito está sendo atendido.
* Verificar aderência ao Documento Mestre.
* Verificar aderência à Arquitetura Técnica.
* Verificar aderência às Regras de Negócio.
* Avaliar impactos em funcionalidades existentes.
* Evitar complexidade desnecessária.

Sempre priorizar:

* Simplicidade
* Clareza
* Baixo acoplamento
* Alta coesão
* Facilidade de manutenção
* Velocidade de implementação

---

# REGRA DE DOCUMENTAÇÃO DE PROGRESSO

Toda alteração realizada deve ser registrada.

## Alterações Backend

Sempre que houver qualquer modificação dentro da pasta:

```text
/backend
```

Atualizar obrigatoriamente:

```text
/backend/progress_backend.md
```

Registrar:

* Data
* Funcionalidade
* Arquivos alterados
* Resumo da alteração
* Impacto esperado

Formato:

```markdown
## YYYY-MM-DD

### Funcionalidade
Nome da funcionalidade

### Resumo
Descrição objetiva da alteração.

### Impacto
Resultado esperado para o sistema.
```

---

## Alterações Frontend

Sempre que houver qualquer modificação dentro da pasta:

```text
/frontend
```

Atualizar obrigatoriamente:

```text
/frontend/progress_frontend.md
```

Registrar:

* Data
* Funcionalidade
* Arquivos alterados
* Resumo da alteração
* Impacto esperado

Formato:

```markdown
## YYYY-MM-DD

### Funcionalidade
Nome da funcionalidade

### Resumo
Descrição objetiva da alteração.

### Impacto
Resultado esperado para o sistema.
```

---

# PROIBIÇÕES

Não:

* Criar microserviços.
* Criar arquitetura distribuída.
* Adicionar mensageria.
* Adicionar complexidade prematura.
* Introduzir dependências sem necessidade comprovada.
* Alterar regras de negócio sem validação documental.

---

# DIRETRIZES ARQUITETURAIS

Backend:

```text
Controllers
↓
Services
↓
Repositories
↓
Database
```

Regras de negócio devem permanecer na camada de Services.

Repositories não devem conter regras de negócio.

Controllers devem apenas receber requisições, validar entradas básicas e delegar processamento.

---

# RESPONSABILIDADE DO AGENTE

Ao concluir qualquer tarefa:

1. Garantir aderência aos documentos oficiais.
2. Garantir aderência à arquitetura.
3. Atualizar o arquivo de progresso correspondente.
4. Informar claramente o que foi alterado.
5. Evitar gerar débito técnico desnecessário.

```

Eu faria apenas um ajuste adicional: criar também um `.docs/decisions.md` (ou `architecture_decisions.md`) para registrar decisões arquiteturais importantes. Isso evita que agentes futuros tomem decisões diferentes sobre DISC, XP, Missões e Currículo Vivo. Hoje esse é o principal ponto de risco de consistência do projeto.
```
