---
id: 5
description: Faz o scaffold de um novo arquivo de spec em docs/specs/<area>/ e PARA (sem codar)
argument-hint: [area] <nome curto da feature>
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(date:*), Read, Write
---

Crie um novo arquivo de spec para: **$ARGUMENTS**

Siga estes passos exatamente. NÃO escreva nenhum código nem mexa em nada fora de `docs/specs/`.

1. **Determine a área (subpasta de domínio).**
   - Se o usuário deu uma área explícita (ex.: `social-worker`, `assessment`, `auth`), use-a.
   - Senão, infira a área mais adequada a partir das subpastas existentes em `docs/specs/` e da descrição da feature. Se estiver genuinamente incerto, PERGUNTE ao usuário antes de continuar.
   - Nomes de área são em inglês, kebab-case (conforme o AGENTS.md).
2. **Aloque o id global.**
   - Varra recursivamente `docs/specs/**/*.md` e leia o frontmatter `id:` de cada arquivo.
   - Próximo id = (maior id existente) + 1, com zeros à esquerda até 4 dígitos. Se nenhum existir, comece em `0001`.
   - O id é GLOBAL — único entre todas as áreas, não por pasta.
3. **Monte o caminho:** `docs/specs/<area>/<id>-<kebab-case-feature-name>.md` — prefixe o nome do arquivo com o `id` alocado (do passo 2) para as specs ordenarem por id e o id continuar sendo um handle estável mesmo se o slug mudar; o id também vive no frontmatter. Traduza o nome para o inglês se necessário.
4. **Faça o scaffold a partir de `docs/_templates/spec.md`:**
   - Copie a estrutura dele. Se faltar, use as seções: Resultado | Escopo (com **Fora de escopo**) | Restrições | Questões em aberto | Design | Tarefas | Critérios de aceitação | Registro de decisões.
   - Em **Design**, faça o scaffold de duas subseções: `### Fluxo (Mermaid)` com uma fence ` ```mermaid ` vazia (um stub `flowchart TD`) mais um comentário de orientação, e `### Wireframe` com um comentário de orientação marcando-a como só-para-UI-pesada. Deixe a fence vazia — NÃO escreva o fluxo; ele é preenchido durante o refinamento em plan mode.
   - Frontmatter: `id` (o id alocado, entre aspas), `title` (nome da feature), `area` (a área escolhida), `status: draft`, `created` = hoje.
   - Numere as **Tarefas** `T1, T2…` e escreva cada **Critério de aceitação** como um Dado/Quando/Então verificável nomeando a(s) Tarefa(s) que ele cobre, ex.: `(T1) Dado … quando … então …`.
   - Deixe os corpos das seções como placeholders curtos. Não invente detalhes de design.
5. Imprima o caminho criado e o id.
6. **PARE.** Não implemente nada. Diga ao usuário: refine em plan mode, **limpe as Questões em aberto** (cada resposta → Registro de decisões), vire `status: ready` e então peça para implementá-la.
