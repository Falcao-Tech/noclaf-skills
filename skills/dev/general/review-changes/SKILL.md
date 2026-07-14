---
id: 15
name: review-changes
description: Review de qualidade/limpeza do diff que vai ser commitado — higiene de comentários (destaque), além de duplicação, abstração, formatação e qualidade geral. Análise read-only via subagente; propõe correções, é consultiva (nunca bloqueia). Use antes de commitar/shipar, quando pedirem pra "revisar/limpar minhas mudanças" ou "checar excesso de comentário", ou quando invocada pelo /ship. NÃO é caça-bug — isso é o /code-review.
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent
---

Revise as **mudanças prestes a serem commitadas** buscando qualidade e limpeza — **não** bugs de correção (isso é o `/code-review`). Só qualidade.

## Escopo
- Padrão: o diff a ser commitado — **mudanças staged + unstaged em arquivos trackeados**, mais o diff do branch vs a base (`main`/`master`/`dev`) quando você está num branch de feature/fix. Ignore lixo untracked, arquivos gerados, dependências, `.env*`.
- Um argumento de path estreita o escopo pra aquele path.

## Procedimento

**1. Capture o diff (determinístico — não peça pra um agente "achar" as mudanças).** Rode:

```bash
base=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@'); base=${base:-main}
git diff --merge-base "$base" -- . ':(exclude)*.lock' ':(exclude)*.min.*'   # branch vs base
git diff HEAD -- .                                                          # staged + unstaged (tracked)
git diff --stat HEAD | tail -1                                             # tamanho
```
(um path em `$ARGUMENTS` estreita: troque `-- .` por `-- <path>`.) Você já tem o diff exato + a lista de arquivos — não redescubra.

**2. Escolha o modo pelo tamanho:**
- **Diff pequeno** (poucos arquivos / até ~400 linhas) → **revise inline, sem subagente.** Spawnar um agente pra 30 linhas é só latência; você já tem o diff acima.
- **Diff grande** → **delegue em leque a agentes read-only baratos (`repo-scout`/Haiku), um por arquivo ou bloco**, cada um com os critérios abaixo, retornando achados estruturados. É só aqui que o custo do subagente se paga — e **passe o recorte pronto**, nunca deixe o agente redescobrir o diff.

Trabalhe sobre as **linhas adicionadas/alteradas** (higiene de comentário e idioma vivem nas linhas `+`); leia contexto ao redor só pra duplicação/abstração.

**3. Retorne cada achado como** `severidade · arquivo:linha · o quê · porquê · correção` e apresente agrupado, **excesso de comentário primeiro**, depois duplicação / abstração / formatação / qualidade. Diff limpo → diga em uma linha.

**4. Aplique só o aprovado.** Comentários + limpezas triviais → ofereça em lote; substantivo (refactor real) → descreva e deixe o usuário decidir. **Consultivo — nunca bloqueia.** Se mexeu em código, avise pra re-rodar lint/build.

## Critérios (ordem de prioridade)

### 1. Higiene de comentários — o destaque (código gerado por LLM comenta demais)
**Sinalize pra deletar:** comentários que repetem o código; narração de passos óbvios (`// loop over users`); comentários que descrevem a *mudança/diff* (`// Added to handle X`, `// Now also does Y`); prosa tutorial; código comentado; docstrings que só ecoam uma assinatura auto-evidente.
**Mantenha:** o **porquê** não-óbvio; invariantes, pegadinhas, footguns; racional de perf/segurança; refs externas (ticket/spec/RFC); contratos de API pública.
**Limite de tamanho (duro):** todo comentário que sobreviver ≤ **2 linhas**. Descrições de função/método ≤ **3 linhas** de prosa, e só quando o *porquê* realmente precisar — linhas de param/return/type/example não contam nas 3. Acima do limite → sinalize pra **encurtar**, não pra manter.
**Teste:** um comentário só se justifica se um leitor esperto não conseguiria inferi-lo do código + bons nomes. **Padrão: nenhum.**

### 2. Duplicação
Copy-paste, gêmeos estruturais, reimplementar um util que já existe. Dedup profunda → sugira `/drytify`.

### 3. Abstração
Abstração prematura/vazada; um wrapper que não agrega nada; a costura errada. Também o inverso — um bloco cabeludo que genuinamente pede um helper nomeado.

### 4. Formatação
Inconsistente com o arquivo ao redor / o formatter do repo. Prefira rodar o formatter do repo a editar na mão.

### 5. Qualidade geral
Código morto, vars/imports não usados, nomes enganosos, ineficiência óbvia nas linhas **alteradas**.

### 6. Idioma do código (código = inglês)
Convenção do projeto: **código se escreve em inglês** — nomes de variáveis, funções, classes, tipos, comentários no código, mensagens de commit e strings de log/erro voltadas ao dev. **Skills, commands e docs são em pt-BR** (pra clareza do time brasileiro).
**Sinalize pra traduzir pro inglês** qualquer código escrito em português: identificadores (`calcularTotal` → `calculateTotal`), comentários em pt dentro do código, nomes de arquivo de código em pt. **NÃO sinalize:** strings voltadas ao usuário final (UI/mensagens do produto — seguem o idioma do produto); nem conteúdo de skills/commands/docs/specs (esse é pt-BR de propósito).
**Teste rápido:** é identificador, símbolo ou comentário técnico → é **código** → inglês. É prosa explicativa pra humano (doc, skill, command, spec) → **pt-BR**.

## Regras
- **Só qualidade** — não reporte bugs de correção/segurança aqui; se achar um de verdade, mencione em uma linha e aponte pro `/code-review`, não corrija.
- **Combine com o código ao redor** — as convenções dele ganham de ideais genéricos.
- **Consultivo** — proponha; aplique só o aprovado; nunca bloqueie o ship.
- Fique dentro do diff — não faça gold-plating nem alargue o escopo.
