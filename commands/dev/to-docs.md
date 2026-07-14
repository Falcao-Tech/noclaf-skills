---
id: 20
description: Documenta um repositório existente engenharia-reversa — descobre em paralelo (agentes repo-scout somente-leitura, baratos) e escreve os docs roteados por tipo: visão geral e padrões arquiteturais em docs/architecture/ (com menção no AGENTS.md), specs em docs/specs/<area>/, ADRs em docs/decisions/. Não coda nem muda comportamento. Idempotente — atualiza os docs existentes em vez de duplicar.
argument-hint: [caminho/área a documentar | vazio = repo inteiro]
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

Documente o repositório (ou o recorte **$ARGUMENTS**). Você **sintetiza** — a descoberta
pesada é delegada. Não escreva código nem mude comportamento; só produza docs a partir do
que o código de fato mostra.

## 1. Descubra em paralelo (barato — não faça você mesmo)

Lance **em uma só leva, em paralelo**, vários agentes **`repo-scout`** (somente-leitura,
Haiku) — um por recorte. Não fique lendo/grepando o repo você mesmo; espere os resumos.

1. **Estrutura + entry points** — árvore de topo, onde começa a execução, como roda/builda.
2. **Convenções + deps** — `AGENTS.md`/`CLAUDE.md`, gerenciador de pacotes, scripts, stack.
3. **Módulos/domínios** — os blocos principais e suas fronteiras/responsabilidades.
4. **Padrões arquiteturais** — camadas, fluxo de dados, limites, decisões implícitas no código.

Recorte grande → some scouts (um por subárvore). Cada scout devolve fatos + os paths densos
pra ler depois.

## 2. Sintetize

Junte os resumos e **abra só os arquivos que os scouts marcaram como "ler depois"** —
nada de reexplorar. Monte um modelo mental do repo. **Não invente**: o que os scouts não
confirmaram vira lacuna anotada, não afirmação.

## 3. Escreva os docs — roteados por tipo (paths determinísticos)

Antes de criar, **cheque se o doc já existe e atualize-o** (idempotente; nunca duplique).

| Conteúdo | Vai para | Extra |
|---|---|---|
| Visão geral do repo | `docs/architecture/overview.md` | — |
| Um padrão/decisão arquitetural | `docs/architecture/<slug>.md` | **adicione uma linha de menção no `AGENTS.md`** (Princípios/índice) |
| Decisão transversal deliberada | `docs/decisions/<próximo-id>-<slug>.md` (ADR) | id = maior existente + 1, zero-pad |
| Descrição de uma feature/comportamento | `docs/specs/<area>/<slug>.md` | `<area>` = domínio do módulo |

- `slug` = kebab-case do título. `<area>` = o domínio do módulo (ex.: `auth`, `billing`).
- **Todo doc de `docs/architecture/` ganha uma menção de uma linha no `AGENTS.md`** (num índice
  "Arquitetura" — crie a seção se não houver), pra virar ponto de entrada canônico.
- Se houver template do repo (`docs/_templates/`), scaffolde a partir dele; senão, título +
  seções claras. Preencha **só o que o código mostra**; o resto vira lacuna curta.

## 4. Feche

Liste os arquivos criados/atualizados (paths), as menções adicionadas ao `AGENTS.md`, e as
**lacunas** que precisam de decisão humana. Não commite — o usuário revisa e commita.
