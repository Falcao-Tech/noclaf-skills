---
title: dependencies
type: moc
description: Libs externas que alguns commands/skills precisam — NÃO sincronizadas pra ~/.claude.
---

# Dependencies

Ferramentas **externas** ao `@noclaf/mcp` que alguns commands precisam em runtime. **Não** vão pra `~/.claude` — o worker instala na máquina; a CLI só as lista no fim do `sync`.

Um command/skill declara que precisa de uma lib **linkando** `[[nome]]` — isso desenha a aresta no grafo e alimenta o aviso de instalação.

## Índice

- [[ponytail]] — engine de scaffolding (plugin de marketplace, install manual). Usada por [[init-sdd]].
- [[improve]] — validação/refino de spec (instalador de linha única). Usada por [[init-sdd]].
