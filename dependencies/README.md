# Dependencies

Ferramentas **externas** ao `@noclaf/cli` que alguns commands precisam em runtime. **Não** vão pra `~/.claude` — o worker instala na máquina; a CLI só as lista no fim do `sync`.

Um command/skill declara que precisa de uma lib **referenciando o arquivo** dela — isso alimenta o aviso de instalação da CLI.

## Índice

- [ponytail](ponytail.md) — engine de scaffolding (plugin de marketplace, install manual). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [improve](improve.md) — validação/refino de spec (instalador de linha única). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [gh](gh.md) — CLI do GitHub (install manual + `gh auth login`). Usada por [to-doc](../skills/dev/general/to-doc/SKILL.md) (spec) + [to-tickets](../skills/dev/general/to-tickets/SKILL.md) pra publicar issues.
