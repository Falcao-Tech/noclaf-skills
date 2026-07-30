# Agents · dev

Subagentes que executam e exploram código — o atendimento ao cliente fica em [support](../support/README.md).

## Índice

- [repo-scout](repo-scout.md) — explorador somente-leitura e barato (Haiku); mapeia um recorte do repo e devolve fatos + paths. Feito pra rodar em leque (paralelo), usado por `to-docs`, `to-tickets`, `drytify`, `review-changes` e `init-sdd` pra tirar a exploração pesada do modelo principal.
- [code-executor](code-executor.md) — worker (Sonnet) que implementa um ticket no worktree seguindo o harness (`docs/_rules` + `docs/_patterns` + `AGENTS.md`); deixa staged, nunca commita. Executor do loop de build.
- [code-reviewer](code-reviewer.md) — gate de qualidade somente-leitura (Opus) que valida um diff contra o harness + critérios do ticket; devolve o veredito canônico `approved`/`changes_requested` + motivos. Complementa os hooks mecânicos. Roda **pré-push**, dentro do loop.
- [pr-reviewer](pr-reviewer.md) — reviewer independente (Opus) de contexto limpo que valida o diff do PR **pós-push** contra o que já existia (diff + base) + o harness + os critérios do ticket; read-only, devolve o mesmo veredito canônico. É a 2ª opinião que julga **integração e escopo**; o loop consome o veredito e chama `nos_set_review`.

Novos agentes entram como `<nome>.md`. O loop de build usa: **repo-scout** (explora) → **code-executor** (implementa) → **code-reviewer** (valida pré-push) → abre PR → **pr-reviewer** (valida pós-push, decide a entrega). O `/build` roda esse trio **em waves**: o frontier do DAG (`noclaf wave`) escalona até `max_parallelism` tickets ao mesmo tempo, um worktree por ticket.
