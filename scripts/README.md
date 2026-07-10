# scripts

Tooling de manutenção do repo. **Não** vai pro npm nem pro worker — roda só aqui.

## Índice

- `assign-ids.mjs` (`npm run ids`) — atribui um `id:` sequencial e estável no frontmatter de cada command/skill/agent. Ids existentes nunca mudam; o contador em `.noclaf-ids.json` garante que um id deletado nunca é reusado (chave de telemetria).
