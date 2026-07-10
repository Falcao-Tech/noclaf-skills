---
id: 3
description: Faz o scaffold de um novo ADR (architecture decision record) em docs/decisions/ e PARA — para registrar uma decisão deliberadamente/fora de banda (o /implement escreve seus próprios ADRs automaticamente)
argument-hint: <título curto da decisão>
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(date:*), Read, Write
---

Registre uma nova decisão de arquitetura: **$ARGUMENTS**

ADRs capturam decisões que **sobrevivem a uma única spec** — arquitetura, convenções, trade-offs transversais. Uma escolha local a uma spec pertence ao **Registro de decisões** daquela spec, não aqui. NÃO escreva código nem mexa em nada fora de `docs/decisions/`.

Use este comando para decisões que você registra **deliberadamente** — na hora do planejamento, ou uma que não está atrelada a um build ativo. Decisões que surgem *enquanto* `/implement` está rodando são escritas em `docs/decisions/` **automaticamente** por ele; você não precisa do `/new-adr` para essas.

1. **Aloque o id do ADR.**
   - Varra `docs/decisions/**/*.md` (prefixo do nome do arquivo + frontmatter `id:`). Próximo id = maior + 1, com zeros à esquerda até 4 dígitos; comece em `0001` se nenhum existir.
   - Esta é uma **sequência separada** dos ids de spec — nunca compartilhe o contador global de specs.
2. **Monte o caminho:** `docs/decisions/<id>-<kebab-case-title>.md` — o id prefixa o nome do arquivo (convenção de ADR) e também vive no frontmatter. Título em inglês.
3. **Faça o scaffold a partir de `docs/_templates/adr.md`:**
   - Copie a estrutura dele. Se faltar, use as seções: Contexto | Decisão | Consequências.
   - Frontmatter: `id` (o id alocado, entre aspas), `title`, `status: proposed`, `created` = hoje.
   - Preencha **Contexto / Decisão** só com o que o usuário de fato te deu; deixe o resto como placeholders curtos. Não invente justificativa.
4. Imprima o caminho criado e o id.
5. **PARE.** Diga ao usuário: refine, vire `status: accepted` assim que decidido e — se mudar uma regra permanente — reflita isso nos **Princípios** do `AGENTS.md`.
