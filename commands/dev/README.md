# Commands · dev

O loop de **spec-driven dev**: escrever a intenção antes do código.

## Índice

- [implement](implement.md) — implementa spec/bug/tickets ponta-a-ponta; faz stage, nunca commit.
- [ship](ship.md) — commit → push → abre PR de uma branch de trabalho revisada (funciona sem `/implement`; só recusa branch-base).
- [to-docs](to-docs.md) — documenta um repo existente (engenharia-reversa) via `repo-scout` em paralelo; roteia por tipo (`docs/architecture/` + menção no `AGENTS.md`, `docs/specs/`, `docs/decisions/`).

> Montar o SDD ([init-sdd](../../skills/dev/general/init-sdd/SKILL.md)), criar docs spec/bug/adr ([to-doc](../../skills/dev/general/to-doc/SKILL.md)) e decompor em tickets ([to-tickets](../../skills/dev/general/to-tickets/SKILL.md)) são **skills**, não commands.

Fluxo típico (pequeno): skill [init-sdd](../../skills/dev/general/init-sdd/SKILL.md) → skill [to-doc](../../skills/dev/general/to-doc/SKILL.md) (spec) → refinar → [implement](implement.md) → [ship](ship.md).
Fluxo grande: skill [to-doc](../../skills/dev/general/to-doc/SKILL.md) (spec) → skill [to-tickets](../../skills/dev/general/to-tickets/SKILL.md) → [implement](implement.md) no frontier → [ship](ship.md).
