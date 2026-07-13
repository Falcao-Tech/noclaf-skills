---
title: Padrão — nota de bug
description: Regras de autoria de uma nota de bug do SDD em docs/bugs/ — leve e transitória, sem id, repro/esperado/atual/correção. Referência da skill to-doc.
---

# Padrão — nota de bug

Registra uma nota de bug em `docs/bugs/` e PARA. **Não corrige nada** — só *registra*. Não
mexa fora de `docs/bugs/`. Bugs são propositalmente **notas leves e transitórias**: sem id,
sem área, sem Tarefas/Aceitação — apenas título, `status` e Reprodução/Esperado/Atual/Correção.
É a metade criadora do loop de bugs (`to-doc bug` → refinar → `/implement`).

1. **Caminho:** `docs/bugs/<kebab-case-title>.md`.
   - Bugs são **planos** (sem subpasta de área) e **não têm id**. Título em inglês se preciso;
     curto e específico.
   - Já existe nota com esse nome → escolha um slug mais específico ou PERGUNTE. **Nunca
     sobrescreva** uma nota existente.
2. **Scaffold a partir de `docs/_templates/bug.md`.** Se faltar, use as seções: Reprodução |
   Esperado | Atual | Correção.
   - Frontmatter: `title`, `status: open`, `created` = hoje.
   - Preencha **Reprodução / Esperado / Atual** só com o que o usuário de fato deu (sintoma
     colado, erro, passos). O que não te disseram vira placeholder curto.
   - Deixe **Correção** vazia — ela é preenchida pelo `/implement`. NÃO diagnostique, não busque
     root cause, nem invente correção.
3. **Feche.** Imprima o caminho criado. **PARE.** Diga: detalhe a reprodução se necessário, e
   então rode `/implement <title>` para corrigir.
