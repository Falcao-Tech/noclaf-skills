# Agents · dev

Subagentes que executam e exploram código — o atendimento ao cliente fica em [support](../support/README.md).

## Índice

- [repo-scout](repo-scout.md) — explorador somente-leitura e barato (Haiku); mapeia um recorte do repo e devolve fatos + paths. Feito pra rodar em leque (paralelo), usado por `to-docs`, `to-tickets`, `drytify`, `review-changes` e `init-sdd` pra tirar a exploração pesada do modelo principal.

Novos agentes entram como `<nome>.md`.
