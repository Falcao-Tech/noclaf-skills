# Agents · dev

Subagentes que executam e exploram código — o atendimento ao cliente fica em [support](../support/README.md).

## Índice

- [repo-scout](repo-scout.md) — explorador somente-leitura e barato (Haiku); mapeia um recorte do repo e devolve fatos + paths. Feito pra rodar em leque (paralelo), usado por `to-docs`, `to-tickets`, `drytify`, `review-changes` e `init-sdd` pra tirar a exploração pesada do modelo principal.
- [code-executor](code-executor.md) — worker (Sonnet) que implementa um ticket no worktree seguindo o harness (`docs/_rules` + `docs/_patterns` + `AGENTS.md`); deixa staged, nunca commita. Executor do loop de build.
- [code-reviewer](code-reviewer.md) — gate de qualidade somente-leitura (Opus) que valida um diff contra o harness + critérios do ticket; devolve aprovado/violações. Complementa os hooks mecânicos.

Novos agentes entram como `<nome>.md`. Os três formam o trio do loop de build: **repo-scout** (explora) → **code-executor** (implementa) → **code-reviewer** (valida).
