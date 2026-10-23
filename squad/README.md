# Squad

Perfis dos agentes do Dev Squad que rodam no worker (Mac mini). **Não** são sincronizados pro
`~/.claude` — ficam fora de `agents/` justamente pra não virarem subagente de todo mundo.

Cada `<nome>.md` declara papel, escopo e entrada em prosa, e um bloco ```json sob `## Settings` que é
literalmente o `settings.json` do Claude Code daquele agente (modelo + permissões).

```bash
noclaf sync --agent otavio   # dentro do worktree do ticket
```

- Grava `~/.noclaf/agents/otavio/settings.json`, que o worker passa com `claude --settings`. O
  `~/.claude/settings.json` humano não é tocado.
- As **rules** não estão aqui: vêm do harness do repo (`docs/_rules/noclaf.md`, pela stack do
  `noclaf.json`), escrito pelo mesmo `sync`. Sem `noclaf.json` no repo, o sync avisa que ficou sem rules.
- A **persona** (tom, identidade) fica no NOS, tela de Agentes. Regra de código não entra lá.

## Perfis

- [otavio](otavio.md) — back-end, monorepo, migrations e infra (Opus).
- [olivia](olivia.md) — front-end e mobile (Opus).
- [bruce](bruce.md) — QA funcional, sem edição (Sonnet).

## Limite do deny

As regras usam wildcard (`git push * main`, `*manage.py migrate*`, `gh * pr merge*`) pra pegar as
variações comuns — `-u`, `+main`, `HEAD:main`, `python3`/`uv run`/`docker compose exec`. Mesmo assim,
casar texto de comando nunca fecha tudo (alias, script que faz o push por dentro, `git push` com
upstream configurado pra `main`). Elas cortam o erro comum; a garantia de verdade é **proteção de
branch no GitHub** (sem push direto em `main`, sem merge pelo token do bot). O Bruce tem `Bash` livre
pra rodar o app, então o read-only dele vem do worktree descartável, não do deny de `Edit`/`Write`.
