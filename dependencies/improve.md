---
title: Improve
description: Lib externa de utilitários usada por comandos de SDD pra refinar e validar specs antes de aplicar.
repo: https://github.com/shadcn/improve
skills: shadcn/improve
install: npx skills add shadcn/improve
---

# Improve

Dependência **externa** — não faz parte do `@noclaf/mcp`. Fornece utilitários que os
comandos de spec-driven development usam pra validar e refinar um spec antes de
implementar.

> **Não** vai pra `~/.claude`. Tem instalador de **linha única** (`skills:
> shadcn/improve` no frontmatter), então no fim do `init`/`sync` a CLI **oferece
> rodar** o comando abaixo com `[y/N]` (padrão: não) — sem shell, montado a partir
> do campo validado. Contraste com o [[ponytail]], que é plugin de marketplace e só
> pode ser instalado manualmente.

## Por que é necessária

Os comandos do loop de SDD ([[init-sdd]] e afins) usam o `improve` pra checar a
consistência do spec (campos do frontmatter, seção *Out of scope*, critérios de
aceite) e sugerir melhorias.

## Instalação

```bash
npx skills add shadcn/improve
```

## Usada por

- [[init-sdd]] — scaffold + validação inicial da estrutura de specs.
