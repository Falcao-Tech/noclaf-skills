---
id: 4
description: Faz o scaffold de uma nova nota de bug em docs/bugs/ e PARA (sem corrigir)
argument-hint: <título curto do bug>
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(date:*), Read, Write
---

Registre uma nova nota de bug para: **$ARGUMENTS**

Siga estes passos exatamente. NÃO escreva nem corrija nenhum código — isto apenas *registra* o bug. Não mexa em nada fora de `docs/bugs/`. Esta é a metade criadora do loop de bugs (`new-bug` → refinar → `implement`); bugs são propositalmente **notas leves e transitórias** (sem id, sem área, sem Tarefas/Aceitação — apenas um título, `status` e Reprodução/Esperado/Atual/Correção).

1. **Monte o caminho:** `docs/bugs/<kebab-case-title>.md`.
   - Bugs são **planos** — sem subpasta de área — e não têm **id**. Traduza o título para o inglês se necessário; mantenha-o curto e específico.
   - Se já existir uma nota com esse nome de arquivo, escolha um slug mais específico ou PERGUNTE ao usuário antes de continuar. **Nunca sobrescreva uma nota existente.**
2. **Faça o scaffold a partir de `docs/_templates/bug.md`:**
   - Copie a estrutura dele. Se faltar, use as seções: Reprodução | Esperado | Atual | Correção.
   - Frontmatter: `title` (o título do bug), `status: open`, `created` = hoje.
   - Preencha **Reprodução / Esperado / Atual** só com o que o usuário de fato te deu (um sintoma colado, erro ou passos). Deixe qualquer coisa que não te disseram como um placeholder curto.
   - Deixe **Correção** vazia — ela é preenchida pelo `/implement`. NÃO diagnostique, não busque root cause, nem invente uma correção.
3. Imprima o caminho criado.
4. **PARE.** Não corrija nada. Diga ao usuário: detalhe a reprodução se necessário, e então rode `/implement <title>` para corrigir.
