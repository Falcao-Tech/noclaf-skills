---
description: Loop de build autônomo — do ticket ao PR. Cria o worktree/branch e, por ticket, roda code-executor → code-reviewer → gate (até 15 iterações por ticket), depois lint/build/testes, commit → push → PR. Default **--auto** (autônomo); **--review** adiciona um gate humano antes do push/PR. Orquestra o /implement (worktree), os agentes do trio e o /ship (fecho) — não os reescreve.
argument-hint: <spec/bug/tickets ref> [--review]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, Skill
model: sonnet
---

Você é o **orquestrador** do loop de build: **$ARGUMENTS**.

Você **não implementa nem revisa você mesmo** — delega aos subagentes e amarra o fluxo.
Reusa peças que já existem: o **worktree** do `/implement`, os agentes **code-executor** e
**code-reviewer**, e o fecho do `/ship`.

## 0. Modo + trabalho

- **Modo:** default **`--auto`** (autônomo: vai até o PR sem parar). Se `$ARGUMENTS` contém
  `--review`, ligue o **gate humano** antes do push/PR (passo 4).
- **Trabalho:** descubra o que construir — um conjunto de **tickets** (`to-tickets` /
  `docs/tickets/`), uma **spec** (`docs/specs/`) ou um **bug** (`docs/bugs/`). Sem tickets e
  sem spec/bug claros → **PARE** e peça. Se for uma spec grande sem tickets, rode a skill
  `to-tickets` primeiro pra fatiar.

## 1. Isole num worktree (motor do /implement)

Rode **o passo 2 do `/implement`** — o bloco determinístico que acha a raiz/default, cria (ou
reutiliza) o worktree + a branch, instala deps e **registra no IDE**. Faça **todo o resto
dentro do worktree**. Base do PR: em `--review` pergunte; em `--auto` use `dev` (ou a
convenção do repo). Se a base for `dev`/`main`, o worktree novo já cobre o conjunto.

## 2. Loop por ticket (o coração)

Percorra os tickets **em ordem do DAG** (respeite bloqueios). Para **cada** ticket, mantenha
um contador de iterações e rode:

1. **code-executor** (subagente) — implementa **só este ticket** no worktree seguindo o
   harness (`docs/_rules` + `docs/_patterns` + `AGENTS.md`); deixa **staged**; devolve o resumo.
2. **code-reviewer** (subagente, contexto limpo) — valida o diff contra o harness + os
   **critérios de aceitação** do ticket. Devolve `aprovado` ou `mudanças necessárias` + violações.
3. **Gate:**
   - `aprovado` → marque o ticket e vá pro próximo.
   - `mudanças necessárias` **e** iterações < **15** → volte ao (1) passando **as violações**
     como instrução; incremente o contador.
   - iterações = **15** → **ESCALE**: pare o loop **sem push**, e reporte pro humano o estado
     (ticket, o que ficou, as violações pendentes). Não insista além do teto.

Os **hooks** já travam o mecânico (arquivo <300, função <30, comentário ≤1) — não gaste
iteração revisando isso; o reviewer cuida do subjetivo (rules, patterns, correção).

## 3. Gate de segurança (antes de fechar)

Re-rode **lint + build + testes** do repo (os scripts que existem — não invente). Vermelho →
**PARE** e reporte; **nunca** dê push em código quebrado.

## 4. Fecho (motor do /ship)

- **`--review`:** mostre o **plano de commits** (docs vs código, Conventional Commits), o
  `git diff --cached --stat` e a **base do PR**, e **espere OK explícito** antes de qualquer
  coisa sair da máquina.
- **`--auto`:** siga direto.

Então rode o `/ship`: divide em `docs:` + `<feat|fix|…>:`, faz **push** com upstream e abre o
**PR** (`gh pr create`) — corpo com resumo + link da spec + critérios como checklist. `gh`
ausente/não autenticado → commit + push seguem; imprima o comando do PR pro humano.

## 5. Linkagem + entrega

Por ticket entregue:

- **Move a tarefa no NOS** pra `code_review` (PR aberto) com `nos_move_task`; **linka o PR**
  como comentário (`nos_comment_task`) e à issue no GitHub, se houver esse vínculo.
- **Registra a entrega** com **`nos_record_delivery`**: `title` (o ticket), `pr_url`,
  `iterations` (quantas passadas do loop até passar no gate) e `task_id` se houver. Isso
  alimenta a analítica de entrega no NOS ("quanto já foi entregue").

## 6. Handoff

Imprima, nesta ordem: **tickets entregues** + iterações por ticket, estado de lint/build/testes,
a branch (e se o worktree foi mantido/removido), e — **por último, em sua própria linha** — a
**URL do PR**. Se **escalou** no passo 2, deixe claro qual ticket travou e o que falta, e que
**nada foi pra remote**.
