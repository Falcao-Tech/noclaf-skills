---
title: Ponytail
description: Lib externa de scaffolding que a skill init-sdd usa pra materializar a estrutura de spec-driven development no repo.
repo: https://github.com/DietrichGebert/ponytail
manual: |
  Não é npm e requer `node` no PATH (os hooks de ciclo de vida precisam dele).
  Claude Code: `/plugin marketplace add DietrichGebert/ponytail` e depois `/plugin install ponytail@ponytail` (2 prompts separados).
  Codex: `codex plugin marketplace add DietrichGebert/ponytail`, então `/plugins` (instalar) e `/hooks` (confiar nos 2 hooks).
  Desktop (Claude/Codex): instale pela UI e reinicie o app.
---

# Ponytail

Dependência **externa** — não faz parte do `@noclaf/cli`. A skill [init-sdd](../skills/dev/general/init-sdd/SKILL.md)
depende dela em runtime pra gerar a árvore de specs (SDD) dentro de `docs/`.

> **Não** é pacote npm nem vai pra `~/.claude`. É um **plugin de marketplace** do
> Claude Code / Codex, instalado *dentro do cliente* (slash-commands + confiança de
> hooks / UI). A CLI do noclaf **não consegue automatizar** isso — no fim do
> `init`/`sync` ela apenas **imprime os passos abaixo** (o campo `manual:` do
> frontmatter). Compare com o [improve](improve.md), que tem instalador de linha única e é
> oferecido pra rodar com `[y/N]`.

## Por que é necessária

O `init-sdd` chama o motor de scaffolding do Ponytail pra criar os templates de
spec e o `AGENTS.md` inicial de forma idempotente.
Sem ela, o comando não consegue escrever a estrutura.

## Instalação

Os plugins do Claude Code e do Codex rodam dois hooks de ciclo de vida em Node.js,
então **`node` precisa estar no PATH** (Nix/nvm: no PATH do shell não-interativo).
Se não estiver, as skills ainda funcionam — só a ativação always-on fica quieta em
vez de errar a cada prompt.

**Claude Code** (dois prompts separados):

```
/plugin marketplace add DietrichGebert/ponytail
/plugin install ponytail@ponytail
```

**Claude Desktop** (não tem `/plugin`): instale pela UI — Customize → o **+** ao
lado de *personal plugins* → *Create plugin and add marketplace* → *Add from
repository* → cole a URL do repo.

**Codex**:

```
codex plugin marketplace add DietrichGebert/ponytail
codex
```

Abra `/plugins`, selecione o marketplace Ponytail e instale. Depois abra `/hooks`,
revise e **confie** nos dois hooks de ciclo de vida, e inicie uma nova thread. Esse
mesmo install cobre o Codex desktop — reinicie o app depois de instalar.

## Usada por

- [init-sdd](../skills/dev/general/init-sdd/SKILL.md) — scaffold da estrutura de specs.
