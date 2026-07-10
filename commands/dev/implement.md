---
id: 1
description: Motor único de execução — implementa uma spec READY (docs/specs/), corrige um bug (docs/bugs/) ou entrega um conjunto de tickets, com o mesmo pipeline: detecção do tipo, gate de status + clarificação, worktree isolado, build conforme as convenções do repo, lint + build + testes verdes, promoção de ADR, e STAGE (nunca commit). Substitui /apply-spec e /apply-bug.
argument-hint: <id/caminho/título de spec ou bug | descrição dos tickets>
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

Implemente o trabalho: **$ARGUMENTS**

Você é um engenheiro sênior transformando intenção em código funcionando. Este é o
**único comando de execução** do loop — ele detecta o tipo de trabalho e roda o mesmo
motor, com os passos específicos de cada tipo. Substitui o `apply-spec` e o `apply-bug`.

## 0. Detecte o tipo de trabalho (roteamento)

Case `$ARGUMENTS` e escolha **um** modo:

- Varra `docs/specs/**/*.md` (frontmatter `id`/`title`/`status`) → match ⇒ **SPEC**.
- Varra `docs/bugs/**/*.md` (nome do arquivo / `title`) → match ⇒ **BUG**.
- Descrição livre de trabalho / lista de tickets sem doc correspondente ⇒ **TICKETS**
  (a descrição do usuário é o contrato).

Vários matches (ou spec **e** bug batem) → mostre os candidatos e pergunte. Nenhum match
e não parece tickets → diga claramente; não invente caminho. `$ARGUMENTS` vazio → liste
specs (`id`, `title`, `status`) **e** bugs (`title`, `status`) e pergunte qual.

## 1. Gate de status + clarificação (bloqueio total — nenhum código até estar limpo)

Leia o item **por inteiro** primeiro.

- **SPEC** — cheque `status:`: `draft` → PARE ("refine e vire `ready` primeiro");
  `ready` → siga; `in-progress` → retome do 1º item não marcado em **Tarefas**; `done`
  → confirme antes de reaplicar. Leia Resultado, Escopo (incl. **Fora de escopo**),
  Restrições, Questões em aberto, Design, Tarefas, Critérios de aceitação, Registro de decisões.
- **BUG** — `fixed` → confirme; `open` → siga. Leia Reprodução, Esperado, Atual, Correção.
- **TICKETS** — confirme que o conjunto está completo e sem ambiguidade.

**Gate de clarificação (vale pros três).** Só está pronto quando *nada* ficou em aberto.
Procure **cada** ponto não resolvido — item de Questões em aberto sem resposta; qualquer
`TBD`/`TODO`/`???`/`<...>`, linha vazia em Design/Tarefa/Aceitação, "decidir depois" — e
qualquer campo que você precise (Esperado do bug, comportamento pretendido) ambíguo de um
jeito que só o usuário resolve. Se existir nem que seja um: PARE, devolva como perguntas
**numeradas**, obtenha resposta pra **cada**, registre (Registro de decisões da spec /
nota do bug / reafirmação pros tickets) e limpe. `status: ready` **não** dispensa isto.
O que *você* consegue resolver diagnosticando (passo 3, bug) — diagnostique, não trave;
mas nunca adivinhe o que o usuário quis dizer.

## 2. Isole o trabalho num git worktree próprio

- **Branch:** SPEC → `feature/<stem>` (stem = nome do arquivo da spec sem `.md`, já é
  `<id>-<slug>`; não re-prefixe o id). BUG → `fix/<slug>`. TICKETS → `feature/<slug>`
  (slug curto a partir da descrição).
- **Retomada:** se a branch (ou um worktree já em checkout nela) existir, **reutilize**.
  Senão, crie **do zero a partir da branch default** (`main`/`master`), não importa em
  qual branch você esteja. NUNCA reutilize uma branch não relacionada em que você por
  acaso está — é assim que o trabalho acaba na branch errada.
- **Worktree:** diretório irmão agrupado — `<pai-do-repo>/<nome-do-repo>.worktrees/<stem|slug>`.
  `git worktree add <path> -b <branch> <default-branch>` (reutilize o path se já existir).
  Anuncie branch + path e **faça todo o resto dentro do worktree.**
- **Traga a nota pra dentro (SPEC/BUG):** a spec/nota costuma estar sem commit na origem;
  copie `docs/specs|bugs/<file>.md` pro worktree e **delete a original da working tree de
  origem** (se ainda estiver lá) — a cópia do worktree vira a canônica. Se já estava
  commitada na origem, sinalize no handoff. (TICKETS: sem doc a mover.)
- **Deixe buildável:** worktree novo não tem deps/`.env`/cache; rode o instalador do repo
  (`npm|pnpm install`, `poetry install`, … — não invente) e copie a config local não
  versionada que o build precisa (`.env*` etc.).
- **SPEC:** vire `ready → in-progress` e crie um pequeno **arquivo de progresso** (a ideia,
  um checklist espelhando as Tarefas, um recap corrido), conforme convenção do repo.

## 3. Implemente

- **SPEC** — as **Tarefas em ordem**; após cada uma marque a caixa na spec + atualize o
  progresso. Delegue blocos grandes e independentes a subagentes se ajudar, mas seja dono
  da integração.
- **BUG** — **reproduza + diagnostique o root cause** (não o sintoma). Bug não trivial
  (causa incerta, raio amplo, vários módulos) → lance um agente **Explore** somente-leitura
  pra fixar root cause + call sites antes de mexer; bug trivial/localizado → pule o agente;
  log de erro colado → a skill `debug-log` é o caminho mais rápido. Faça a **mudança
  mínima** que resolve a raiz (não workaround) e adicione/ajuste um **teste de regressão**
  se o projeto tiver testes.
- **TICKETS** — cada ticket em ordem, rastreando progresso como na spec.
- **Todos:** respeite as convenções do repo (`CLAUDE.md`/`AGENTS.md` — idioma dos
  identificadores, migrations, onde vai schema/util, estilo de comentário). Construa
  exatamente o pedido, **sem gold-plating**. **Comente com parcimônia** — só o *porquê* não
  óbvio, nunca o *o quê*. Onde houver seams pré-combinados, use **TDD** (teste que falha
  primeiro). Rode **type-check + arquivos de teste isolados com frequência** durante o
  trabalho — não deixe tudo pro fim.

## 4. Verifique — lint + build + testes verdes

Rode os scripts de **lint** e **build/type-check** do repo (do `package.json` /
`pyproject.toml` / `Cargo.toml`) e a **suíte de testes inteira uma vez no fim**. Não
invente comandos. Precisam estar **verdes** antes da finalização — conserte o que você
quebrou, ou pare e reporte.

- **SPEC** — **rastreabilidade:** cada **Critério de aceitação** mapeia pra uma **Tarefa**
  marcada (refs `(T…)`); sinalize Tarefa sem critério e critério sem Tarefa. Marque só os
  critérios que você **de fato** verificou; o que depende de infra que você não roda (ex.:
  DB ao vivo) fica anotado como deploy-time.
- **BUG** — confirme que a **reprodução não reproduz mais**.

## 5. Revise

Rode a revisão do diff staged antes do handoff (`/code-review` / a skill `review-changes`).
Trate os achados: conserte o que for seu antes de entregar.

## 6. Finalização

- **SPEC** — entradas datadas no **Registro de decisões** (resolva os OPEN). Decisão
  **transversal** (afeta mais que esta spec) → **escreva o ADR você mesmo**
  (`docs/decisions/<próximo-id>-<slug>.md` a partir de `docs/_templates/adr.md`,
  `status: accepted`) e, se virou regra permanente, adicione uma linha aos **Princípios**
  no `AGENTS.md`. Vire `in-progress → done` quando Tarefas feitas + lint/build verdes;
  critérios que precisam de infra ficam como deploy-time, sem bloquear. **Quando chegar a
  `done`, delete o arquivo de progresso** (a spec + o histórico de commits são o registro
  duradouro); em `in-progress`, mantenha.
- **BUG** — preencha a seção **Correção** (root cause + o que mudou) e vire `open → fixed`.
  **Antes de podar, promova o duradouro:** regra/decisão transversal → escreva o ADR
  e/ou adicione aos Princípios do `AGENTS.md` primeiro (a nota vai ser deletada). Depois
  **pode a nota** (a Correção fica no commit; se o repo mantém arquivo morto de bugs, mova
  pra lá).
- **TICKETS** — capture qualquer decisão duradoura como ADR se for transversal.

**Todos — entrega:** **`git add` (STAGE) mas NÃO commit** — o usuário commita. Diga a ele
**onde fica o worktree**; o **`/ship`** remove o worktree depois de dar push + abrir o PR
(o trabalho já está seguro na branch) — não remova você aqui, nada foi commitado ainda.
Handoff enxuto: branch + path do worktree, o que mudou (por área), lint/build/testes
rodados + resultado, o que ainda precisa do usuário.

**Disciplina de escopo:** o **Fora de escopo** da spec é autoritativo. Bateu numa lacuna
não coberta, ou a mudança excederia o escopo → PARE e pergunte (anote no progresso). Spec
errada é spec pra corrigir com o usuário, não pra contornar em silêncio.

**Nunca:** implementar spec `draft`/não resolvida ou bug `fixed` sem confirmar; `git
commit`; entregar workaround com o root cause alcançável; renomear identificadores
existentes voltados a dados/usuário pra satisfazer regra de código novo; marcar
done/fixed/critério sem verificar com lint + build verdes.
