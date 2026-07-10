# @noclaf/skills

O **repositório de conhecimento** do noclaf — skills, commands, agents e dependências
consumidos pelo [`@noclaf/mcp`](https://github.com/Falcao-Tech/noclaf-mcp) e servidos
aos clientes de IA (Claude Code, Codex, Claude Desktop/Cowork).

## Estrutura

- `commands/<seção>/*.md` — slash-commands (ex.: `/init-sdd`, `/implement`), por seção (`dev`, `productivity`). Índice em [commands](commands/README.md).
- `skills/<seção>/<nome>/SKILL.md` — skills no padrão Agent Skills, por seção (`dev`, `productivity`). Índice em [skills](skills/README.md).
- `agents/<seção>/*.md` — subagentes, por seção (`dev`, `support`). Índice em [agents](agents/README.md).
- `hooks/<role>/` — script + `hooks.json` que o CLI registra no `settings.json` do cliente. Índice em [hooks](hooks/README.md).
- `rules/*.md` — convenções/knowledge de projeto servidas como regra. Índice em [rules](rules/README.md).
- `dependencies/` — libs externas que um command/skill precisa; um doc referencia o arquivo da lib. Índice em [dependencies](dependencies/README.md).
- `scripts/` — tooling de build do repo (ex.: `npm run ids`); **não** é publicado.

## Como é consumido

Publicado no npm como `@noclaf/skills`. O `@noclaf/mcp` resolve este pacote em runtime
(`node_modules/@noclaf/skills`) e lê os arquivos direto — sem Supabase, sem grafo, offline.
Atualizar as skills = publicar uma nova versão daqui; os workers pegam via `npm`.

## Manter

Cada command/skill/agent tem um `id:` estável no frontmatter — chave de telemetria que sobrevive a renames. Depois de adicionar itens, rode:

```bash
npm run ids   # atribui ids sequenciais aos itens sem id (existentes nunca mudam)
```

## Publicar

```bash
npm publish --access public
```
