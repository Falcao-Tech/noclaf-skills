---
id: 32
name: new-boilerplate
description: Registra um repo como boilerplate do noclaf — cria o ponteiro `BOILERPLATE.md` em `boilerplates/<role>/<área>/<stack>/<nome>/` a partir de um link de repositório, derivando título, descrição e ref do próprio GitHub. Use quando o usuário mandar um link de repo dizendo "vira boilerplate", "adiciona esse template", "registra esse starter", ou pedir pra listar um projeto no modal de projeto novo do Studio.
model: sonnet
effort: medium
---

# New Boilerplate

Transforma **um link de repo** num boilerplate que o `noclaf init` sabe clonar. O template
continua morando no repo dele — aqui entra só o **ponteiro**.

O usuário passa a URL. Você deriva o resto e pergunta **uma coisa só**: a taxonomia.

## 1. Normalize a URL

Aceite qualquer forma que o usuário jogar e reduza a `https://github.com/<org>/<repo>`:
`git@github.com:org/repo.git`, `.../tree/<branch>`, com ou sem `.git`, com ou sem `https://`.

O CLI **só aceita `https://` ou `git@`** no campo `repo`. Forma curta (`org/repo`), `ssh://`,
`file://` e `ext::` são recusados e o manifesto **some do catálogo em silêncio** — normalize
sempre pra `https://`, é o formato sem armadilha.

Se a URL tinha `/tree/<branch>`, guarde o branch: é o `ref`.

## 2. Derive o que der do GitHub

```bash
gh repo view <org>/<repo> --json name,description,defaultBranchRef,primaryLanguage,repositoryTopics,isPrivate
```

- `title` — a partir do `name` + linguagem, em prosa (`api-starter` + TypeScript → "API Starter (TypeScript)"). Não repita o nome cru.
- `description` — a do GitHub. Vazia ou genérica demais → leia o README e escreva **uma linha** dizendo o que o template entrega (stack + o que já vem ligado).
- `ref` — o `/tree/<branch>` da URL se havia; senão **omita o campo** (o clone usa o default do repo). Só fixe `ref` quando o usuário pedir um branch específico.
- `isPrivate: true` → **pare e avise**: o `--apply` roda com `GIT_TERMINAL_PROMPT=0`, então repo privado falha na hora do clone. Peça pra tornar público ou escolher outro.

Sem `gh` (veja [gh](../../../../dependencies/gh.md)) ou repo inacessível: pergunte título e
descrição junto da taxonomia, numa pergunta só.

## 3. Pergunte a taxonomia (a única pergunta)

O caminho define onde o boilerplate aparece no Studio, e não dá pra inferir com confiança —
mas **chute bem**: use linguagem, topics e deps do repo pra pré-preencher.

```
boilerplates/<role>/<área>/<stack>/<nome>/BOILERPLATE.md
```

- `role` — quem usa (`dev`, `management`, …). Espelha os roles de `skills/`.
- `área` — o recorte dentro do role (`front-end`, `back-end`, `mobile`).
- `stack` — a tecnologia (`react`, `node`, `flutter`).
- `nome` — vira o **`id`** que o Studio manda no apply. **Não** é o título.

Serve qualquer área/stack do role? Use `general` — o segmento colapsa e vira `null` no
catálogo: `boilerplates/dev/general/<nome>/BOILERPLATE.md`.

Ofereça o palpite pronto pra aceitar ("`dev/back-end/node/hono-api-starter` — ok?"), não um
formulário em branco.

## 4. Garanta o `id` único

O `--apply` valida **só pelo id**, ignorando o caminho — dois `starter` em stacks diferentes
colidem e o usuário recebe o boilerplate errado. Antes de escrever:

```bash
find boilerplates -name 'BOILERPLATE.md' | awk -F/ '{print $(NF-1)}' | sort | uniq -d
```

Nome já usado → prefixe pela stack (`node-api-starter`) e diga que fez isso.

## 5. Escreva o manifesto

`boilerplates/<role>/<área>/<stack>/<nome>/BOILERPLATE.md`:

```markdown
---
title: API Starter (Node + Hono)
description: API REST com Hono, Drizzle e testes de contrato já ligados.
repo: https://github.com/Falcao-Tech/api-starter
---

Uma linha ou duas sobre quando escolher este template. O CLI só lê o frontmatter.
```

`title` e `description` ausentes não quebram nada — o Studio só renderiza vazio. `ref` só
quando há branch fixo.

## 6. Valide antes de publicar

Dois comandos que pegam quase todo erro real:

```bash
GIT_TERMINAL_PROMPT=0 git ls-remote <repo> HEAD >/dev/null && echo "clonável"
noclaf init --describe | jq '.boilerplates[] | select(.id == "<nome>")'
```

O primeiro prova que o clone do `--apply` vai funcionar sem pedir credencial. O segundo prova
que o manifesto entra no catálogo — **saída vazia é o sintoma clássico de `repo` fora da
allowlist** (volte ao passo 1).

O `--describe` lê o **cache** (`~/.noclaf/skills`), que vem do `main` publicado. Antes do push,
valide apontando pro checkout local:

```bash
NOCLAF_SKILLS_DIR=$(pwd) noclaf init --describe | jq '.boilerplates'
```

## 7. Publique

Rode `npm run ids` (mantém os ids de telemetria estáveis), registre o boilerplate no
[index.md](../../../../index.md) e no README da seção, e commite com
`feat(boilerplates): add <nome>`. Push no `main` — o cache dos workers busca de lá.

Feche dizendo o **id** e a taxonomia: é o que o Studio vai mostrar e o que o `--apply` recebe.
