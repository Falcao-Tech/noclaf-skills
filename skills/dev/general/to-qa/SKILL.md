---
id: 41
name: to-qa
description: Fecha o ciclo de QA de uma task do NOS — monta o card que o QA humano usa pra testar (contexto, objetivo, escopo entregue, como testar e o Roteiro de QA reconciliado com o que foi de fato entregue) e, quando o QA volta, registra o resultado (aprovado → done; reprovado → rejected + nota de bug). Use quando o usuário pedir "cria o card de QA", "documenta essa tarefa pro QA", "template-task", "gera o card dessa tarefa", "manda pro QA", ou relatar "QA aprovou/reprovou".
model: sonnet
effort: medium
---

# To QA

Quem lê é o **QA**. O card descreve o que a pessoa **vê e faz** na superfície da entrega
(tela, CLI, API, job) — nunca como o código foi escrito.

O roteiro **já nasceu antes do código**: o **Plano de QA** da spec (`to-doc`) e o checklist
**Roteiro de QA** do ticket (`to-tickets`). Esta skill **não reinventa** — reconcilia esse roteiro
com o que foi entregue e preenche o resto. Sem roteiro prévio (trabalho feito fora do SDD) →
derive da conversa atual e do código. Em qualquer caso: **não invente escopo nem mensagem** — se
não apareceu na conversa, na spec ou no código, não entra.

## 1. Ache a task

- `task_id`/key dada pelo usuário → `nos_get_task`.
- Senão → `nos_get_active_allocation` (a task cronometrada agora) → `nos_get_task`.
- Leia título, descrição e checklists. Spec de origem citada no Contexto → leia o **Plano de QA**
  dela.

O título não bate com o que foi feito na conversa → **confirme** antes de gravar.

## 2. Reconcilie o roteiro

Para cada cenário `QA<n>`:

- **Mensagem citada** → confira contra o código e cite **exata**; "a confirmar" sai daqui resolvido.
- **`[auto]`** → existe teste/evidência que o prova (do `code-executor`/`/build`, ou rode você)?
  Sim → marque o item como feito no checklist e cite a evidência. Não → vira `[manual]`.
- Cenário que a entrega **não** cobre (escopo cortado) → tire do card e diga no Escopo entregue.
- Comportamento entregue **sem** cenário → acrescente, no mesmo formato.

## 3. Grave no NOS

- **Descrição** (`nos_update_task`) — o card abaixo. A descrição do `to-tickets` (linha +
  `### Contexto`) **fica**: acrescente o card depois dela. Descrição com outro conteúdo →
  **confirme** antes de substituir.
- **Checklist "Roteiro de QA"** — já existe → `nos_update_checklist_item` pra marcar os `[auto]`
  provados e ajustar texto; não existe → `nos_add_checklist` com os cenários.
- **Status** — task ainda não em `qa` → `nos_move_task` pra `qa`.

```markdown
**Módulo:** <área › recurso>
**Tipo:** <Nova funcionalidade | Correção | Migração | …>
**Superfície:** <tela | CLI | API | job> · **Ambiente:** <homologação | …> · **Perfil:** <tipo de usuário>

---

## Contexto
Uma ou duas frases: qual fluxo é, qual a situação antes.

## Objetivo
O que a entrega passa a permitir.

## Escopo entregue
<lista do que foi exposto; migração → tabela novo × antigo>
**Acesso:** qual perfil acessa e se exige permissão.

---

## Como testar
Por onde testar, com qual perfil, e a **massa de dados**: o que preparar antes (registros e
em qual estado).

Os cenários estão no checklist **Roteiro de QA** — os marcados já foram provados pelo agente
(evidência abaixo); teste os abertos.

**Evidência automática:** QA2 — <teste/comando que prova>; …
```

O título já existe no NOS — o card começa direto no `**Módulo:**`, sem `# <título>`.

## 4. Resultado do QA (quando o QA volta)

- **Aprovado** (todos os cenários marcados) → `nos_set_review(task_id, verdict: "approved",
  reviewer: "qa", advance: true)` — move pra `done` e grava a entrega.
- **Reprovado** → `nos_move_task` pra `rejected` + `nos_comment_task` com o(s) `QA<n>` que
  falharam (passo, esperado, atual, evidência) e abra a nota de bug com `to-doc bug` usando isso
  como reprodução. Próximo passo: `/implement` do bug.

## Regras

**Proibido no card:**
- Caminho de arquivo, nome de classe/função, pasta, registro de rota, link relativo do repo.
- Superfície `tela`: cenário que só reproduz por Postman/API (corpo inválido, id de outro
  cliente, 401/403 forjado, JSON de exemplo). Isso é teste automatizado, não QA.
- Lista de parâmetro/campo renomeado — contrato de integração, não teste de QA.

**Obrigatório:**
- Uma frase por comportamento verificável na superfície.
- Mensagem exibida citada **exata**.
- Dado que não aparece pra quem usa (histórico, log) → aponte onde o QA confere.

Convenções de um projeto (nome de módulo, perfis, "legado → V3") vêm do `AGENTS.md` do repo —
não deste arquivo.

## Antes de encerrar

- [ ] Zero caminho de arquivo/classe no card.
- [ ] Todo cenário aberto é reproduzível pela superfície declarada.
- [ ] Mensagens citadas batem com as do código.
- [ ] `[auto]` só marcado com evidência citada.
- [ ] Nenhum `.md` criado no repositório (exceto a nota de bug no caminho reprovado).
- [ ] Responda (PT) com a key da task e o status em que ela ficou.
