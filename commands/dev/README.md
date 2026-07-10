# Commands · dev

O loop de **spec-driven dev**: escrever a intenção antes do código.

## Índice

- [init-sdd](init-sdd.md) — monta a estrutura `docs/` (specs, bugs, ADRs, `AGENTS.md`). Idempotente.
- [new-spec](new-spec.md) — cria um spec em `docs/specs/<area>/` e para.
- [new-bug](new-bug.md) — registra uma nota de bug em `docs/bugs/` e para.
- [new-adr](new-adr.md) — registra uma decisão de arquitetura em `docs/decisions/` e para.
- [implement](implement.md) — implementa spec/bug/tickets ponta-a-ponta; faz stage, nunca commit.
- [ship](ship.md) — commit → push → abre PR do trabalho já revisado.

Fluxo típico: [init-sdd](init-sdd.md) → [new-spec](new-spec.md) → refinar → [implement](implement.md) → [ship](ship.md).
