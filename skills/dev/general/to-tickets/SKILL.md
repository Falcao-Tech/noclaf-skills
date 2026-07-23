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

Aplique as **regras de fatia vertical** de [TICKET-PATTERNS.md](TICKET-PATTERNS.md). Dê a cada
ticket suas **arestas de bloqueio** — os tickets que precisam terminar antes dele começar;
sem bloqueador → pode começar já. Para uma mudança mecânica de **raio amplo** (renomear
coluna, retipar símbolo compartilhado), não force um tracer bullet — use o playbook
**expand–contract** do mesmo arquivo.

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
  sessão (`nos_set_project` se preciso) e crie uma task por ticket com `nos_create_task`
  (corpo = "O que construir" + Critérios + "Bloqueado por"). As tools `nos_*` são MCP e **não
  dependem de shell**, então rodam no Cowork — este é o canal que nunca falta.
- **GitHub (quando o `gh` estiver disponível)** → uma issue por ticket em ordem de dependência
  (`gh issue create …`). Onde a spec já virou issue-pai (`issue:` no frontmatter), crie os
  tickets como **sub-issues** dela; senão "Bloqueado por #N" no corpo (o GitHub não tem campo
  nativo de "blocked by"). Aplique o label `ready-for-agent`. **Não** feche/modifique a
  issue-pai. `gh` ausente/não-autenticado (ex.: Cowork sem shell) → **pule o GitHub sem
  travar** e siga com NOS + local.
- **Local (registro)** → escreva `docs/tickets/<stem-da-spec | slug>.md` (crie a pasta se
  faltar), todos os tickets em ordem de dependência, cada um com "Bloqueado por" **e os
  identificadores criados** (`task_id` do NOS, `#N` do GitHub) — é o que o `/implement` e o
  `/ship` leem depois pra referenciar e fechar.

## Depois

Trabalhe o **frontier** um ticket por vez com **`/implement`**, **limpando o contexto entre
tickets**. O `/implement` respeita o DAG: só pega tickets cujos bloqueadores estão todos done.
