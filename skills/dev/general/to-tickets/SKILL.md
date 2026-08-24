---
id: 23
name: to-tickets
description: Fatia uma spec, plano ou a conversa atual em tickets tracer-bullet (fatias verticais) com DAG de bloqueio, e publica direto — task por ticket no NOS (via MCP, funciona no Cowork) + issues/sub-issues no GitHub quando o gh existe + registro local em docs/tickets/. Sem gate de confirmação. Use quando o usuário pedir pra "quebrar em tickets", "fatiar a spec/o trabalho", "criar issues", ou antes de implementar trabalho grande. Depois é só /implement no frontier.
model: sonnet
effort: high
---

# To Tickets

Fatia trabalho em **tickets** tracer-bullet — fatias verticais, cada uma declarando os
tickets que a **bloqueiam** (DAG). É a etapa de decomposição entre a skill `to-doc` (spec) e `/implement`.

As **regras de fatia vertical**, o **playbook de refactor amplo (expand–contract)** e os
**templates** ficam em [TICKET-PATTERNS.md](TICKET-PATTERNS.md) — consulte ao rascunhar (passo
3) e ao publicar (passo 5). Times/projetos podem estender esse arquivo com padrões próprios.

## 1. Reúna o contexto

Trabalhe do que já está na conversa. Se um argumento for uma referência, busque e leia o
corpo inteiro:
- **spec** (`id`/caminho em `docs/specs/`) → leia a spec e o **Registro de decisões**;
- **issue** (número/URL) → `gh issue view <n> --comments` (leia corpo + comentários);
- **descrição livre** → é o contrato.

## 2. Entenda o estado atual (delegue — não explore inline)

Se precisar entender o codebase pra fatiar bem, **não explore você mesmo**: lance 1–3 agentes
**`repo-scout`** (read-only, Haiku, em paralelo) com recortes objetivos ("como funciona a área
X hoje", "onde vive Y", "quais ADRs tocam Z"). Eles voltam com fatos + paths; você fica com o
contexto limpo pra fatiar. Títulos e descrições usam o **glossário de domínio** do projeto e
respeitam os **ADRs** da área. Procure **prefactor**: *"deixe a mudança fácil, depois faça a
mudança fácil."* Contexto já suficiente na conversa → pule este passo.

## 3. Rascunhe as fatias verticais

Aplique as **regras de fatia vertical** de [TICKET-PATTERNS.md](TICKET-PATTERNS.md). Favoreça
**poucas fatias** que entregam comportamento (ver *Granularidade*): sub-passos técnicos da mesma
fatia viram **itens de checklist**, não tickets separados. Dê a cada ticket suas **arestas de
bloqueio** — os tickets que precisam terminar antes dele começar; sem bloqueador → pode começar
já. Para uma mudança mecânica de **raio amplo** (renomear coluna, retipar símbolo
compartilhado), não force um tracer bullet — use o playbook **expand–contract** do mesmo arquivo.

## 4. Valide com o usuário

Apresente a quebra como lista numerada. Para cada ticket: **Título**, **Bloqueado por**,
**O que entrega** (comportamento ponta-a-ponta). Pergunte:
- A granularidade está boa? (grossa demais / fina demais)
- As arestas de bloqueio estão certas — cada ticket depende só de tickets que o gatam?
- Algum ticket deveria ser mesclado ou dividido?

Itere até o usuário aprovar.

## 5. Publique os tickets

Publique **direto no NOS + GitHub, sem gate** — não pergunte, não trave. Os três canais têm
os mesmos tickets; muda só a forma das arestas. Use os **templates** de
[TICKET-PATTERNS.md](TICKET-PATTERNS.md). Nunca bloqueie por um canal faltar: publique no que
der e registre o que faltou.

- **NOS (sempre — funciona em qualquer cliente, inclusive Cowork)** → garanta o projeto da
  sessão (`nos_set_project` se preciso). Por ticket: **título humano** (orientado a resultado,
  sem `WS·[repo]`), `nos_create_task` com **descrição curta** (uma linha + `### Contexto` com
  repo/bloqueadores), e então **checklists nativos** via `nos_add_checklist` — uma **Implementação**
  (passos técnicos) e uma **Definition of Done** (critérios). Ver os templates em TICKET-PATTERNS.
  `nos_add_checklist` indisponível → DoD como `- [ ]` na descrição. As tools `nos_*` são MCP e
  **não dependem de shell**, então rodam no Cowork — este é o canal que nunca falta.
- **GitHub (quando o `gh` estiver disponível)** → uma issue por ticket, **em ordem de
  dependência** (`--parent`/`--blocked-by` só aceitam issues que já existem). Preencha **todos
  os campos na própria criação** — issue com campo vazio, ou com dependência só em prosa no
  corpo, é ticket pela metade:

  ```bash
  gh issue create --title "<id-da-spec> · <título humano>" --body-file <corpo.md> \
    --assignee @me \
    --type "<Task|Bug|Feature>" \
    --label "<enhancement|bug|documentation>" \
    --parent <n-da-issue-pai> \
    --blocked-by <n1,n2> \
    --milestone "<ciclo aberto, se existir>"
  ```

  - **Título** — começa com o **id da spec**, depois `· ` e o título humano:
    `0011 · Descobrir boilerplates no catálogo`. É o que deixa a lista de issues agrupada por
    spec e casa com o `<id>-<slug>` da branch. Sem spec de origem (descrição livre) → só o
    título humano.
  - **Assignee** — `@me` sempre; quem fatia é o dono até reatribuírem.
  - **Type** — campo nativo, definido na **org**. Liste os válidos com
    `gh api orgs/<org>/issue-types -q '.[].name'` (404 / repo pessoal → omita `--type`). Mapa:
    comportamento novo → `Feature`; correção → `Bug`; chore/refactor/infra → `Task`.
  - **Relationships** — as arestas do DAG são **campos nativos**, não texto: `--blocked-by <n>`
    por bloqueador, e `--parent <n>` quando a spec já virou issue-pai (`issue:` no frontmatter).
    O corpo **não** repete a lista de bloqueadores. Só se o `gh` recusar as flags (versão
    antiga) caia pro `Bloqueado por #N` no corpo — e registre a degradação no handoff.
  - **Label** — só os padrão do GitHub (`enhancement` / `bug` / `documentation`), casando com o
    Type. Nunca `ready-for-agent` nem labels custom, a menos que o usuário peça.
  - **Milestone** — só se já existir (`gh api repos/<org>/<repo>/milestones -q '.[].title'`); o
    `gh issue create` **falha** com nome inexistente. Nenhuma aberta → omita a flag.
  - **Não** feche/modifique a issue-pai. `gh` ausente/não-autenticado (ex.: Cowork sem shell) →
    **pule o GitHub sem travar** e siga com NOS + local.
  - A seção **Development** (branch/PR) fica vazia aqui de propósito — quem a preenche é o
    `/implement`, com `gh issue develop`, no momento em que a branch nasce.
- **Local (registro)** → escreva `docs/tickets/<stem-da-spec | slug>.md` (crie a pasta se
  faltar), todos os tickets em ordem de dependência, cada um com "Bloqueado por" **e os
  identificadores criados** (`task_id` do NOS, `#N` do GitHub) — é o que o `/implement` e o
  `/ship` leem depois pra referenciar e fechar.

## Depois

Trabalhe o **frontier** um ticket por vez com **`/implement`**, **limpando o contexto entre
tickets**. O `/implement` respeita o DAG: só pega tickets cujos bloqueadores estão todos done.
