# Dependencies

Ferramentas **externas** ao `@noclaf/cli` que alguns commands precisam em runtime. **Não** vão pra `~/.claude` — o worker instala na máquina; a CLI só as lista no fim do `sync`.

Cada arquivo em `dependencies/` **é** uma dependência declarada — a presença no diretório basta (sem wikilink nem grafo). A CLI lista todas no fim do `sync`/`init` e oferece instalar as que têm instalador estruturado (`npm`/`skills`/`git`); as `manual` só imprimem os passos. O "Usada por" / "Reforça" abaixo é nota pra humano, não liga nada no código.

O campo `skills:` aceita `owner/repo` **ou** `owner/repo/skill` (skill específica da [skills.sh](https://skills.sh)) e vira `npx skills add <valor>`.

## Prioridade local sobre skills.sh

O que declaramos localmente (em `skills/`, `commands/`, `agents/`) **tem prioridade** sobre a mesma skill online — as nossas são *overrides* customizados. Por isso **não** criamos dependency pra skill da skills.sh que já temos local (`caveman`, `handoff`, `grill-me`, `to-tickets`, `implement`, `emil-design-eng`, `review`…). Só puxamos skills da skills.sh que **acrescentam** algo que não temos — tipicamente as que **reforçam as rules**. Ao adicionar uma nova, cheque se já existe um equivalente em `skills/` antes.

## Índice

### Runtime — usadas por commands/skills

- [ponytail](ponytail.md) — engine de scaffolding (plugin de marketplace, install manual). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [improve](improve.md) — validação/refino de spec (instalador de linha única). Usada por [init-sdd](../skills/dev/general/init-sdd/SKILL.md).
- [gh](gh.md) — CLI do GitHub (install manual + `gh auth login`). Usada por [to-doc](../skills/dev/general/to-doc/SKILL.md) (spec) + [to-tickets](../skills/dev/general/to-tickets/SKILL.md) pra publicar issues.

### Reforço de rules — skills externas (skills.sh)

- [vercel-react-best-practices](vercel-react-best-practices.md) — reforça `rules/front-end/rules.md`.
- [vercel-composition-patterns](vercel-composition-patterns.md) — reforça `rules/front-end/ssr-rules.md`.
- [shadcn](shadcn.md) — reforça `rules/front-end/lovable-rules.md` (UI).
- [supabase-postgres-best-practices](supabase-postgres-best-practices.md) — reforça `rules/front-end/lovable-rules.md` (dados/RLS).
- [domain-modeling](domain-modeling.md) — reforça `rules/back-end/rules.md`.
