---
id: 2
description: Faz o scaffold da estrutura completa de spec-driven-dev — specs, bugs, ADRs e a constituição AGENTS.md — no repo atual (idempotente), opcionalmente analisa o repo para pré-preencher e então PARA
allowed-tools: Bash(ls:*), Bash(test:*), Bash(find:*), Bash(mkdir:*), Bash(cat:*), Grep, Glob, Read, Write
---

Monte o scaffolding de spec-driven dev no **repositório atual**. NÃO escreva nenhum código nem mexa em nada fora de `docs/` e de um `AGENTS.md` na raiz.

**Roda igual no Claude Code e no Codex.** Então NÃO use nenhuma UI específica de ferramenta para as perguntas — pergunte com uma lista numerada simples e espere uma resposta normal. Busque no repo com qualquer shell/busca somente-leitura que o host oferecer. O frontmatter `allowed-tools` acima é só do Claude; o Codex o ignora.

## Regras
- **Idempotente + não destrutivo.** Para cada arquivo abaixo: se já existir, PULE e reporte "exists — skipped". Nunca sobrescreva. Isso torna o comando seguro para re-rodar.
- **Somente-leitura no código-fonte.** Só escreva dentro de `docs/` e de um `AGENTS.md` na raiz. Nunca mexa no código.
- Termine com uma tabela-resumo de `created` vs `skipped`, e então **PARE**.

## Fase 0 — Pergunte primeiro (antes de fazer qualquer scaffold)

Imprima estas perguntas como texto simples, e então **encerre seu turno e espere** a resposta. Ainda não faça scaffold.

> **1. Como devo proceder?**
> **a)** Só scaffold — apenas criar a estrutura de SDD (templates, pastas, starter do AGENTS.md).
> **b)** Scaffold **+ análise** — também ler o repo para pré-preencher o AGENTS.md e semear docs para o próximo agente já começar aquecido.
>
> *(Se o repo estiver vazio/novo, escolha **a** — ainda não há nada para analisar.)*
>
> **2. Se (b), o que devo produzir?** (escolha o que quiser)
> - **stack** — preencher *Tech stack* + *Convenções* do AGENTS.md a partir do código real.
> - **adrs** — rascunhar ADRs candidatos (`status: proposed`) para decisões já embutidas no código.
> - **overview** — um primer curto do projeto (a "ideia principal") para orientar o próximo agente.
> - **specs** — semear specs candidatas para áreas óbvias inacabadas / em andamento.

Quando responderem: rode a **Fase 1** sempre, e então a **Fase 2** só para as partes que escolheram.

## Fase 1 — Scaffold (sempre)

Crie os arquivos abaixo (idempotente, não destrutivo).

### `docs/specs/.gitkeep`, `docs/bugs/.gitkeep` e `docs/decisions/.gitkeep`
Arquivos vazios (para as pastas serem versionadas pelo git).

### `docs/_templates/spec.md`
````markdown
---
id: "<NNNN>" # global, com zeros à esquerda, único entre todas as specs
title: <nome da feature>
area: <pasta de domínio, ex.: social-worker | assessment | auth>
status: draft # draft | ready | in-progress | done
created: <YYYY-MM-DD>
---

# <nome da feature>

## Resultado
O que é verdade quando isto estiver pronto. Uma ou duas frases, visível ao usuário.

## Escopo
O que isto cobre.

### Fora de escopo
<!-- A linha mais importante. Liste o que explicitamente NÃO vamos fazer para o agente não sair divagando. -->
-

## Restrições
Regras que isto precisa obedecer — especialmente os **Princípios** em [AGENTS.md](../../../AGENTS.md) (o conjunto de regras que serve de gate). Liste aqui apenas as restrições específicas desta spec.
-

## Questões em aberto
<!-- O gate de clarificação: ambiguidades a resolver ANTES de `status: ready`. Só saia de draft quando isto estiver vazio (toda pergunta respondida). Ao responder uma → registre-a no Registro de decisões. -->
-

## Design
Como vai ser construído. Arquivos, módulos, formatos de dados, API. Seja concreto.

### Fluxo (Mermaid)
<!-- Escreva durante o refinamento em plan mode. Diagrame o caminho principal (flowchart/sequence/state). Obrigatório para qualquer coisa com fluxo não trivial. -->
```mermaid
flowchart TD
```

### Wireframe
<!-- Raro — só telas pesadas de UI. ASCII ou mermaid. Delete esta subseção se não for uma feature de UI. -->

## Tarefas
<!-- Numere como T1, T2… para os Critérios de aceitação poderem apontar de volta para elas. -->
- [ ] T1 ·
- [ ] T2 ·

## Critérios de aceitação
<!-- Verificáveis, não achismo: Dado/Quando/Então (ou uma condição de aprovação clara). Cada um nomeia a(s) Tarefa(s) que o satisfazem, ex.: (T1, T3). Todo critério mapeia para ≥1 Tarefa; toda Tarefa é coberta por ≥1 critério. -->
- [ ] (T?) Dado … quando … então …
- [ ] (T?) Dado … quando … então …

## Registro de decisões
<!-- Append-only — decisões LOCAIS a esta spec. Data + a escolha + o porquê. Decisões transversais vão para um ADR em docs/decisions/ (/new-adr), não aqui. -->
- <YYYY-MM-DD>:
````

### `docs/_templates/bug.md`
````markdown
---
title: <título curto do bug>
status: open # open | fixed
created: <YYYY-MM-DD>
---

# <título curto do bug>

## Reprodução
Passos para disparar o bug.
1.

## Esperado
O que deveria acontecer.

## Atual
O que acontece em vez disso.

## Correção
Root cause + o que mudou. Preencha quando corrigido.
````

### `docs/_templates/adr.md`
````markdown
---
id: "<NNNN>" # sequência de ADR, com zeros à esquerda, único em docs/decisions (separado dos ids de spec)
title: <título da decisão>
status: proposed # proposed | accepted | superseded
created: <YYYY-MM-DD>
---

# <NNNN>. <título da decisão>

## Contexto
As forças em jogo — o que está empurrando esta decisão, e por que agora. Fatos, restrições, opções ponderadas.

## Decisão
O que vamos fazer, em voz ativa: "Vamos …".

## Consequências
Os trade-offs — o bom, o ruim, e o que isto descarta mais adiante. Anote qualquer coisa que isto supersede.
````

### `docs/specs.base`
````yaml
filters:
  and:
    - file.inFolder("docs/specs")
    - 'file.ext == "md"'

formulas:
  age_days: 'if(created, (today() - date(created)).days, "")'

properties:
  id:
    displayName: "ID"
  title:
    displayName: "Spec"
  status:
    displayName: "Status"
  area:
    displayName: "Area"
  created:
    displayName: "Created"
  formula.age_days:
    displayName: "Age (d)"

views:
  - type: table
    name: "Active"
    filters:
      not:
        - 'status == "done"'
    order:
      - id
      - title
      - status
      - area
      - created
      - formula.age_days
    groupBy:
      property: status
      direction: ASC

  - type: table
    name: "By area"
    order:
      - id
      - title
      - status
      - created
    groupBy:
      property: area
      direction: ASC

  - type: table
    name: "Done"
    filters:
      and:
        - 'status == "done"'
    order:
      - id
      - title
      - area
      - created
````

### `docs/bugs.base`
````yaml
filters:
  and:
    - file.inFolder("docs/bugs")
    - 'file.ext == "md"'

formulas:
  age_days: 'if(created, (today() - date(created)).days, "")'

properties:
  title:
    displayName: "Bug"
  status:
    displayName: "Status"
  created:
    displayName: "Created"
  formula.age_days:
    displayName: "Age (d)"

views:
  - type: table
    name: "Open"
    filters:
      not:
        - 'status == "fixed"'
    order:
      - title
      - status
      - created
      - formula.age_days
    groupBy:
      property: status
      direction: ASC

  - type: table
    name: "Fixed"
    filters:
      and:
        - 'status == "fixed"'
    order:
      - title
      - created
````

### `docs/decisions.base`
````yaml
filters:
  and:
    - file.inFolder("docs/decisions")
    - 'file.ext == "md"'

formulas:
  age_days: 'if(created, (today() - date(created)).days, "")'

properties:
  id:
    displayName: "ID"
  title:
    displayName: "Decision"
  status:
    displayName: "Status"
  created:
    displayName: "Created"

views:
  - type: table
    name: "Accepted"
    filters:
      and:
        - 'status == "accepted"'
    order:
      - id
      - title
      - created
    groupBy:
      property: status
      direction: ASC

  - type: table
    name: "All"
    order:
      - id
      - title
      - status
      - created
      - formula.age_days
````

### `AGENTS.md` (raiz do repo) — SOMENTE se ainda não existir
Se um `AGENTS.md` já existir, deixe-o intocado (apenas reporte "exists — skipped"). Senão, crie este starter e diga ao usuário para preencher as regras específicas do projeto:
````markdown
# AGENTS.md

Regras permanentes deste repo — **sempre verdadeiras**, independentemente do que estamos construindo agora.
A intenção atual (o que estamos construindo *agora*) fica em `docs/specs/`. Bugs ficam em `docs/bugs/`. Decisões que sobrevivem a uma única spec ficam em `docs/decisions/` (ADRs).

## Princípios
<!-- O conjunto de regras que serve de gate — os inegociáveis para os quais as Restrições de toda spec apontam. Mantenha curto; promova decisões duradouras para cá (ou para um ADR). -->
- **Comentários merecem seu lugar.** Escreva um comentário só quando um leitor esperto não conseguiria tirar do código + nomes — o *porquê* não óbvio, uma invariante, uma pegadinha, uma referência externa. Nunca narre o *o quê* nem descreva a mudança. Por padrão, nenhum.
-

## Tech stack
<!-- Preencha: linguagem, framework, DB, bibliotecas principais. -->
-

## Convenções
<!-- Preencha: regras de nomenclatura, idioma dos identificadores, estrutura de pastas, etc. -->
-

## Spec-driven dev (o loop)
- **Regras / Princípios** = sempre verdadeiros → aqui.
- **Specs** = o que estamos construindo agora → `docs/specs/<area>/<id>-<feature>.md`, fragmentadas por área de domínio. O `id` (global, com zeros à esquerda, único entre todas as áreas) prefixa o nome do arquivo E vive no frontmatter (`title`, `area`, `status`, `created`).
- **Bugs** = notas leves → `docs/bugs/<slug>.md` (transitórias: sem id, podadas assim que corrigidas).
- **Decisões (ADRs)** = escolhas que sobrevivem a uma única spec → `docs/decisions/<id>-<slug>.md` (sequência de id própria). O `/implement` escreve uma **automaticamente** quando uma decisão transversal surge durante o build; use `/new-adr` para registrar uma **deliberadamente** (na hora do planejamento ou fora de banda). O **Registro de decisões** da própria spec fica para escolhas locais àquela spec.
- **Views:** abra `docs/specs.base` / `docs/bugs.base` / `docs/decisions.base` no Obsidian para filtrar por status/área em vez de ler a pasta.
- **FORA DE ESCOPO** numa spec é a linha mais importante — é o que impede o agente de divagar.

O loop por feature:
1. `/new-spec <area> <feature>` → faz o scaffold de `docs/specs/<area>/*.md`, `status: draft`.
2. Refine em **plan mode**, sem código; **limpe cada Questão em aberto** (cada resposta → Registro de decisões) → `status: ready`.
3. `/implement <id>` → implementa as Tarefas de cima para baixo contra `docs/specs/<area>/<id>-<feature>.md`, respeitando o AGENTS.md → `status: in-progress`.
4. Revise o diff contra os **Critérios de aceitação** da spec.
5. `/ship` → divide os commits `docs:` (a spec, agora `done`) + `feat:` (código), dá push na branch, abre um PR na base que você escolher (`dev`/`master`/custom).

O loop por bug (mais leve — sem id, sem área, transitório):
1. `/new-bug <title>` → faz o scaffold de `docs/bugs/<title>.md`, `status: open`.
2. Detalhe Reprodução / Esperado / Atual se necessário.
3. `/implement <title>` → corrige no root cause, preenche **Correção**, vira `status: fixed`, poda a nota.
4. `/ship` → commit `fix:`, push, PR na base que você escolher.
````

## Fase 2 — Análise (só se o usuário a escolheu na Fase 0)

Somente-leitura. Varra o repo e produza APENAS as saídas que o usuário escolheu. Nunca edite código; escreva só dentro de `docs/` e (se você o criou nesta rodada) no `AGENTS.md`.

**Como varrer (barato, não exaustivo):** leia os arquivos de manifesto/config (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, lockfiles, `Dockerfile`, configs de CI/lint/format), passe o olho no layout de pastas de topo e amostre um punhado de arquivos-fonte para pegar nomenclatura/estilo. Uma dúzia de arquivos bem escolhidos basta — não leia a árvore inteira.

- **stack** → Preencha os placeholders de *Tech stack* e *Convenções* no `AGENTS.md`. Se o `AGENTS.md` já existia (pulado na Fase 1), NÃO o sobrescreva — em vez disso, escreva os achados em `docs/analysis.md` e diga ao usuário para mesclá-los na mão.
- **adrs** → Para cada decisão arquitetural já visível no código (escolha de framework/DB, layout de monorepo, estratégia de auth, gerenciamento de estado, estilo de API…), rascunhe `docs/decisions/<id>-<slug>.md` a partir de `docs/_templates/adr.md` em `status: proposed`, preenchendo Contexto/Decisão/Consequências com o que o código mostra. Estes são candidatos para o usuário aceitar — diga isso.
- **overview** → Escreva `docs/overview.md`: uma página — o que o projeto é, os fluxos principais, os módulos-chave e onde um novo agente deve olhar primeiro.
- **specs** → Para áreas óbvias inacabadas / em andamento (TODOs, features stubadas, módulos meio ligados), semeie `docs/specs/<area>/<id>-<feature>.md` a partir do template em `status: draft`. Não invente escopo — deixe as ambiguidades reais em Questões em aberto para o usuário.

Tudo que a Fase 2 escreve é um **rascunho para o usuário revisar** — você não decidiu nada em definitivo. Imprima o que você produziu.

## Depois de criar
1. Imprima o resumo de created/skipped.
2. Diga ao usuário os próximos passos opcionais (NÃO rode você mesmo):
   - Abra a pasta do repo como um vault do Obsidian para usar as views `.base`.
   - Indexe os docs com o QMD: `qmd collection add <repo>/docs --name <proj>-specs && qmd embed`.
   - Preencha o tech-stack / convenções do `AGENTS.md`.
   - Rode `/new-spec <area> <feature>` para escrever a primeira spec.
3. **PARE.** Não implemente nada.

---

**Comandos relacionados** (navegação no Obsidian): [[new-spec]] · [[implement]] · [[new-bug]] · [[new-adr]] · [[ship]]
<!-- Wikilinks para navegar pela suíte de comandos no Obsidian — eles só resolvem se ~/.claude/commands estiver no seu vault. Os comandos continuam sendo invocados como /new-spec etc.; estes não são passos para rodar. -->
