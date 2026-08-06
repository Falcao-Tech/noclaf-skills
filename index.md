# Índice do repositório

Ponto de entrada do repo. Tudo aqui (menos `dependencies/`) é distribuído pra
`~/.claude` via `noclaf sync` — veja o [README](README.md).

## Commands

Slash-commands, por seção — índice: [commands](commands/README.md).

- **[dev](commands/dev/README.md)** — o loop de spec-driven dev: `init-sdd` → `to-doc` (spec) → (`to-tickets`) → `implement` → `ship`.
- **[productivity](commands/productivity/README.md)** — fluxo de trabalho fora do código (vazio).

## Skills

Model-invoked. Organizadas por domínio — índice: [skills](skills/README.md).

- **[dev](skills/dev/README.md)** — engenharia, por stack (`general`, `front-end`, `back-end`, `mobile`).
- **[productivity](skills/productivity/README.md)** — fluxo de trabalho fora do código (vazio).

## Agents

Subagentes, por seção — índice: [agents](agents/README.md).

- **[dev](agents/dev/README.md)** — execução de código (vazio).
- **[support](agents/support/README.md)** — atendimento ao cliente (vazio).

## Dependencies

Libs externas que alguns commands precisam — **não** sincronizadas. Índice: [dependencies](dependencies/README.md).

- [ponytail](dependencies/ponytail.md) — engine de scaffolding usada por [init-sdd](skills/dev/general/init-sdd/SKILL.md).
- [improve](dependencies/improve.md) — validação de spec usada por [init-sdd](skills/dev/general/init-sdd/SKILL.md).
- [gh](dependencies/gh.md) — CLI do GitHub, usada por [to-doc](skills/dev/general/to-doc/SKILL.md) (spec) + [to-tickets](skills/dev/general/to-tickets/SKILL.md) pra publicar issues.

## Hooks

Scripts + gatilho que o cliente roda em eventos do ciclo de vida — provisionados e registrados no `settings.json` pelo CLI. Índice: [hooks](hooks/README.md).

- **dev** — [check-comment-length](hooks/README.md): bloqueia `git commit` que adiciona bloco de comentário em prosa > 3 linhas.

## Rules

Convenções e knowledge de projeto que o agente segue como regra (não são model-invoked). Índice: [rules](rules/README.md).

- [lovable-knowledge](rules/lovable-knowledge.md) — stack e convenções de front-end (ShadCN, TanStack, Tailwind, pt-BR).

## Como chega no worker

```
bundle/  ──(noclaf sync / noclaf init)──►  ~/.claude/{commands,skills,agents,hooks}
         hooks/        também registram o gatilho no settings.json do cliente
         dependencies/ NÃO são copiadas — só listadas como libs a instalar
         scripts/      tooling de build local — não sai daqui
```

Instalar o MCP já roda o sync, então o worker recebe tudo isso automaticamente.
Build local: `npm run ids` mantém os `id:` de telemetria estáveis.
