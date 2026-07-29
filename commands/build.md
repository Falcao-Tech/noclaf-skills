---
description: Loop de build autônomo — do ticket ao done. Cria o worktree/branch e, por ticket, roda code-executor → code-reviewer → gate (até 15 iterações por ticket), depois lint/build/testes, commit → push → PR, e então o pr-reviewer (2ª opinião pós-push) até approved ou escalar. Default **--auto** (autônomo); **--review** adiciona um gate humano antes do push/PR. Orquestra o /implement (worktree), os agentes code-executor/code-reviewer/pr-reviewer e o /ship (fecho) — não os reescreve.
argument-hint: <spec/bug/tickets ref> [--review]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, Skill
model: sonnet
---

Você é o **orquestrador** do loop de build: **$ARGUMENTS**.

Você **não implementa nem revisa você mesmo** — delega aos subagentes e amarra o fluxo.
Reusa peças que já existem: o **worktree** do `/implement`, os agentes **code-executor**,
**code-reviewer** e **pr-reviewer**, e o fecho do `/ship`.

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
   **critérios de aceitação** do ticket. Devolve `approved` ou `changes_requested` + motivos.
3. **Gate** (veredito canônico do reviewer — o token `approved`/`changes_requested`):
   - `approved` → registre o **veredito estruturado** do ticket `{ verdict: approved,
     iterations: <contador> }` (é o gate interno/pré-push — guarde o contador; o §5 reusa este
     mesmo contador se o `pr-reviewer` pedir uma nova passada) e vá pro próximo.
   - `changes_requested` **e** iterações < **15** (teto explícito) → volte ao (1) passando os
     **Motivos** como instrução; incremente o contador.
   - iterações = **15** (teto) → **ESCALE**: pare o loop **sem push**, registre `{ verdict:
     changes_requested, iterations: 15 }`, e reporte pro humano o estado (ticket, o que ficou,
     os motivos pendentes). Não insista além do teto.

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
**PR** (`gh pr create`) — corpo no **template estruturado** do `/ship §6` (Ticket, Escopo,
Fora de escopo, Arquivos/funções afetados, Cenários de teste, Rollout & kill-switch). `gh`
ausente/não autenticado → commit + push seguem; imprima o comando do PR pro humano. Ao abrir o
PR, o `/ship` já chama `nos_attach_pr(task_id, pr_url)` por ticket vinculado — a task entra em
`code_review`/`review_state=pending` (**não** vai a `done` aqui).

## 5. Review externo pós-PR (pr-reviewer + gate no NOS)

Com o PR aberto (task(s) já em `code_review`/`pending`, §4), rode o subagente **pr-reviewer**
(contexto limpo, read-only) sobre o diff **do PR**: `git diff <base>...HEAD`, a mesma `<base>`
usada no fecho. Ele devolve o veredito canônico `approved`/`changes_requested` + motivos —
mesmo formato do `code-reviewer`, mas visão de integração (diff contra o que já existia, não só
o hunk).

Reaja ao veredito **por ticket vinculado ao PR** (`task_id` do registro de tickets, §0/§4):

- **`approved`** → chame `nos_set_review(task_id, verdict: "approved", reviewer:
  "pr-reviewer", advance: true)`. A tool move a task pra `done` **e** grava a entrega (chama
  `nos_record_delivery` internamente, com `review_verdict: approved` e `reviewer: pr-reviewer`)
  — **não** chame `nos_record_delivery` você mesmo para este ticket (ver §6). Siga pro próximo
  ticket vinculado, ou pro handoff (§7) se não houver mais.
- **`changes_requested`** → chame `nos_set_review(task_id, verdict: "changes_requested", note:
  <motivos do pr-reviewer>)` — mantém a task em `code_review` e posta os motivos como
  comentário. Identifique a qual ticket cada motivo pertence (pelo arquivo/escopo) e **realimente
  o code-executor** com os motivos como instrução: uma nova passada do loop do **§2**
  (code-executor → code-reviewer → gate) **naquele ticket**, **reusando o mesmo contador e o
  mesmo teto de 15 iterações** dele (não reinicia aqui). Depois de o gate interno aprovar de
  novo, dê **novo push** (via `/ship` de novo, ou um push simples pra mesma branch/PR) e
  **re-rode o pr-reviewer** sobre o diff atualizado. Repita até `approved` ou até o teto.
  - **Teto de 15 estourado** → **ESCALE**: pare sem insistir, reporte ao humano o estado
    (ticket, PR, motivos pendentes do `pr-reviewer`, iterações consumidas) — a task **fica em
    `code_review`**, sem `nos_set_review(advance)` e sem entrega.
- **Degradação** — se o `pr-reviewer` não puder rodar (subagente indisponível, diff
  inacessível, etc.), **não trave o loop**: caia no veredito do gate interno (`code-reviewer`,
  §2) daquele ticket como substituto — se ele aprovou, chame `nos_set_review(task_id, verdict:
  "approved", reviewer: "internal", advance: true)` no lugar; **avise explicitamente** no
  handoff (§7) que o review externo não rodou e por quê.

O **code-reviewer** (§2) continua como 1ª linha, pré-push, ticket a ticket — o **pr-reviewer**
é a 2ª opinião, pós-push, sobre o PR como um todo. Ele complementa, **não substitui**, o gate
interno.

## 6. Linkagem + entrega (complemento — sem entrega duplicada)

O `/ship` (§4) já ligou o PR (`nos_attach_pr`) e, no caminho `approved`, o `nos_set_review(...,
advance: true)` do §5 já **é quem grava a entrega** (com `reviewer: pr-reviewer`, ou `internal`
na degradação). Aqui só resta:

- **Não chame `nos_record_delivery` de novo** para um ticket que já passou pelo `nos_set_review`
  do §5 — duplicaria a linha de entrega. Não existe uma tool de "atualizar entrega": se quiser
  registrar o `iterations` do loop (esforço — o dado que o `nos_set_review` não conhece) como
  contexto adicional, use `nos_comment_task` ou deixe só no handoff (§7); **nunca** uma segunda
  `nos_record_delivery`/`nos_set_review(advance)` para o mesmo ticket.
- **Linke o PR** como comentário na task (`nos_comment_task`) só se ainda não estiver — o
  `/ship` já cobre isso via `nos_attach_pr`.
- Ticket que **escalou** no §5 (teto estourado) → nada a registrar aqui; segue em `code_review`
  sem entrega, aguardando decisão humana.

## 7. Handoff

Imprima, nesta ordem: **tickets entregues** (com o veredito do gate interno §2 e do
`pr-reviewer` §5, e iterações por ticket) — ou `done` via degradação (§5) quando aplicável —,
estado de lint/build/testes, a branch (e se o worktree foi mantido/removido), e — **por último,
em sua própria linha** — a **URL do PR**. Se **escalou** no §2, deixe claro qual ticket travou
e que **nada foi pra remote**. Se **escalou** no §5 (teto do `changes_requested` pós-PR),
deixe claro que o PR **está aberto** mas o(s) ticket(s) seguem em `code_review` esperando
decisão humana. Se o `pr-reviewer` **degradou** para o gate interno, avise isso também.
