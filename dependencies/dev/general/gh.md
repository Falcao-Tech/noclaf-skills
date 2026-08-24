---
title: GitHub CLI (gh)
description: CLI oficial do GitHub — usada pelas skills to-doc (spec) e to-tickets pra publicar specs e tickets como issues + sub-issues no repo conectado.
repo: https://github.com/cli/cli
manual: |
  Não é npm — instale pelo gerenciador do SO e autentique:
  macOS: `brew install gh`. Linux: `apt install gh` / `dnf install gh` (veja o repo). Windows: `winget install --id GitHub.cli`.
  Depois: `gh auth login` (escolha GitHub.com e um método). Confira com `gh auth status`.
  Campos nativos de issue (`--type`, `--parent`, `--blocked-by`) exigem `gh` >= 2.94; `gh issue develop` é bem mais antigo.
install: brew install gh && gh auth login
---

# GitHub CLI (gh)

Dependência **externa** — não faz parte do `@noclaf/skills`. As skills `to-doc` (spec) e
`to-tickets` usam o `gh` pra publicar no GitHub do repo conectado: criar a issue da spec,
uma issue por ticket com todos os campos preenchidos (type, assignee, label padrão,
relationships) e linkar a branch de trabalho à issue.

> É **plugin/CLI de SO** (não npm) e precisa de **login** — a CLI do noclaf **não
> automatiza**; ela imprime os passos. Publicar no GitHub é opcional: sem o `gh`, specs e
> tickets ficam locais (`docs/specs/`, `docs/tickets/`) e/ou vão pro tracker do NOS.

## Por que é necessária

A skill `to-doc` (spec complexa) e a `to-tickets` oferecem publicar o trabalho
como issues rastreáveis. As arestas do DAG usam os **campos nativos** de *Relationships* —
`--parent` (sub-issue) e `--blocked-by` — em vez de texto no corpo. O `/implement` usa
`gh issue develop` pra preencher a seção *Development* da issue com a branch.

## Instalação

- **macOS:** `brew install gh`
- **Linux:** `apt install gh` (Debian/Ubuntu) · `dnf install gh` (Fedora) — ou veja o repo
- **Windows:** `winget install --id GitHub.cli`

Depois autentique: `gh auth login` → GitHub.com → siga o fluxo. Confirme com `gh auth status`.

## Usada por

- `to-doc` (spec) — publica a spec como issue (type + assignee + label padrão) quando complexa e confirmada.
- `to-tickets` (skill) — publica os tickets como issues + sub-issues no DAG de bloqueio.
- `/implement` — `gh issue develop` linka a branch do worktree à issue do ticket.
- `/ship` — abre o PR (assignee + label padrão) e fecha a issue entregue.
