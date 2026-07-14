# Dependencies

Ferramentas **externas** ao `@noclaf/cli` que alguns commands precisam em runtime. **Não** vão pra `~/.claude` — o worker instala na máquina; a CLI só as lista no fim do `sync`.

Cada arquivo em `dependencies/` **é** uma dependência declarada — a presença no diretório basta (sem wikilink nem grafo). A CLI lista todas no fim do `sync`/`init` e oferece instalar as que têm instalador estruturado (`npm`/`skills`/`git`); as `manual` só imprimem os passos. O "Usada por" abaixo é nota pra humano, não liga nada no código.

## Índice

- [ponytail](ponytail.md) — engine de scaffolding (plugin de marketplace, install manual). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [improve](improve.md) — validação/refino de spec (instalador de linha única). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [gh](gh.md) — CLI do GitHub (install manual + `gh auth login`). Usada por [to-doc](../skills/dev/general/to-doc/SKILL.md) (spec) + [to-tickets](../skills/dev/general/to-tickets/SKILL.md) pra publicar issues.
