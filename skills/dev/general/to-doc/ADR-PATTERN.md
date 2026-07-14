---
title: Padrão — ADR
description: Regras de autoria de um ADR (architecture decision record) do SDD em docs/decisions/ — sequência de id própria, contexto/decisão/consequências, status. Referência da skill to-doc.
---

# Padrão — ADR

Registra um ADR em `docs/decisions/` e PARA. Não escreva código nem mexa fora de
`docs/decisions/`.

ADRs capturam decisões que **sobrevivem a uma única spec** — arquitetura, convenções,
trade-offs transversais. Escolha local a uma spec pertence ao **Registro de decisões** dela,
não aqui. Use este fluxo pra decisões que você registra **deliberadamente** (na hora do
planejamento, ou fora de banda). Decisões que surgem *enquanto* `/implement` roda são escritas
**automaticamente** por ele — pra essas você não precisa disto.

1. **id do ADR.** Determinístico — rode (não leia arquivo por arquivo):
   ```bash
   n=$(grep -rhoE '^id:[[:space:]]*"?[0-9]+' docs/decisions 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1); printf "%04d\n" $(( ${n:-0} + 1 ))
   ```
   É uma **sequência separada** dos ids de spec — nunca compartilhe o contador global de specs.
2. **Caminho:** `docs/decisions/<id>-<kebab-case-title>.md` — o id prefixa o arquivo (convenção
   de ADR) e vive no frontmatter. Título em inglês.
3. **Scaffold a partir de `docs/_templates/adr.md`.** Se faltar, use as seções: Contexto |
   Decisão | Consequências.
   - Frontmatter: `id` (entre aspas), `title`, `status: proposed`, `created` = hoje.
   - Preencha **Contexto / Decisão** só com o que o usuário de fato deu; o resto fica como
     placeholder curto. Não invente justificativa.
4. **Feche.** Imprima o caminho criado e o id. **PARE.** Diga: refine, vire `status: accepted`
   assim que decidido e — se mudar uma regra permanente — reflita nos **Princípios** do `AGENTS.md`.
