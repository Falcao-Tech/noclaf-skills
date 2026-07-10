# @noclaf/skills

A **vault de conhecimento** do noclaf — skills, commands, agents e dependências
consumidos pelo [`@noclaf/mcp`](https://github.com/Falcao-Tech/noclaf-mcp) e servidos
aos clientes de IA (Claude Code, Codex, Claude Desktop/Cowork).

## Estrutura

- `commands/` — slash-commands (ex.: `/init-sdd`, `/new-spec`). Índice em [[commands/README|commands]].
- `skills/<seção>/<nome>/SKILL.md` — skills no padrão Agent Skills, agrupadas por seção (`dev`, `productivity`). Índice em [[skills/README|skills]].
- `agents/` — subagentes (opcional).
- `dependencies/` — libs externas que um command/skill precisa; um doc linka `[[nome]]`.

## Como é consumido

Publicado no npm como `@noclaf/skills`. O `@noclaf/mcp` resolve este pacote em runtime
(`node_modules/@noclaf/skills`) e lê os arquivos direto — sem Supabase, sem grafo, offline.
Atualizar as skills = publicar uma nova versão daqui; os workers pegam via `npm`.

## Publicar

```bash
npm publish --access public
```
