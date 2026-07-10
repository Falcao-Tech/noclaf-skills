---
title: noclaf bundle
type: moc
description: Mapa de conteúdo do bundle noclaf — skills, commands, agents e dependencies que o worker recebe ao instalar o MCP.
---

# noclaf bundle — Mapa de Conteúdo

Ponto de entrada da vault. Tudo aqui (menos `dependencies/`) é distribuído pra
`~/.claude` via `noclaf sync` — veja o [README](README.md).

## Commands

Slash-commands, por seção — índice: [[commands/README|commands]].

- **[[commands/dev/README|dev]]** — o loop de spec-driven dev: `init-sdd` → `new-spec` → `implement` → `ship`.
- **[[commands/productivity/README|productivity]]** — fluxo de trabalho fora do código (vazio).

## Skills

Model-invoked. Organizadas por domínio — índice: [[skills/README|skills]].

- **[[skills/dev/README|dev]]** — engenharia, por stack (`general`, `front-end`, `back-end`, `mobile`).
- **[[skills/productivity/README|productivity]]** — fluxo de trabalho fora do código (vazio).

## Agents

Subagentes, por seção — índice: [[agents/README|agents]].

- **[[agents/dev/README|dev]]** — execução de código (vazio).
- **[[agents/support/README|support]]** — atendimento ao cliente (vazio).

## Dependencies

Libs externas que alguns commands precisam — **não** sincronizadas. Índice: [[dependencies/README|dependencies]].

- [[ponytail]] — engine de scaffolding usada por [[init-sdd]].
- [[improve]] — validação de spec usada por [[init-sdd]].

## Como chega no worker

```
bundle/  ──(noclaf sync / noclaf init)──►  ~/.claude/{commands,skills,agents}
         dependencies/ NÃO são copiadas — só listadas como libs a instalar
```

Instalar o MCP já roda o sync, então o worker recebe tudo isso automaticamente.
