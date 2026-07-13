---
name: init-sdd
description: Faz o scaffold da estrutura completa de spec-driven-dev — specs, bugs, ADRs e a constituição AGENTS.md — no repo atual (idempotente), copiando os templates ao lado desta skill; opcionalmente analisa o repo pra pré-preencher e então PARA. Use pra "iniciar o SDD", "montar docs/", "configurar spec-driven dev" num repo.
disable-model-invocation: true
---

# Init SDD

Monte o scaffolding de spec-driven dev no **repositório atual**. NÃO escreva nenhum código nem
mexa em nada fora de `docs/` e de um `AGENTS.md` na raiz.

**Roda igual no Claude Code e no Codex.** NÃO use nenhuma UI específica de ferramenta para as
perguntas — pergunte com uma lista numerada simples e espere uma resposta normal. Busque no
repo com qualquer shell/busca somente-leitura que o host oferecer.

## Regras

- **Idempotente + não destrutivo.** Para cada arquivo abaixo: se já existir, PULE e reporte
  "exists — skipped". Nunca sobrescreva. Isso torna a skill segura para re-rodar.
- **Somente-leitura no código-fonte.** Só escreva dentro de `docs/` e de um `AGENTS.md` na raiz.
- Termine com uma tabela-resumo de `created` vs `skipped`, e então **PARE**.

## Fase 0 — Pergunte primeiro (antes de qualquer scaffold)

Imprima estas perguntas como texto simples, e então **encerre seu turno e espere** a resposta.
Ainda não faça scaffold.

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

Quando responderem: rode a **Fase 1** sempre, e então a **Fase 2** só para as partes escolhidas.

## Fase 1 — Scaffold (sempre)

Crie os arquivos abaixo (idempotente, não destrutivo).

1. **Pastas:** `docs/specs/.gitkeep`, `docs/bugs/.gitkeep` e `docs/decisions/.gitkeep` — arquivos
   vazios (para as pastas serem versionadas pelo git).
2. **Templates → `docs/_templates/`.** Os esqueletos moram **ao lado desta skill**, em
   `templates/`. Copie o conteúdo de cada um para `docs/_templates/` com o mesmo nome (leia o
   arquivo empacotado da skill e escreva-o **tal e qual** no repo; pule os que já existirem):
   - `templates/spec.md` → `docs/_templates/spec.md`
   - `templates/bug.md` → `docs/_templates/bug.md`
   - `templates/adr.md` → `docs/_templates/adr.md`
3. **`AGENTS.md` (raiz) — SOMENTE se ainda não existir.** Copie `templates/AGENTS.md` para
   `AGENTS.md` na raiz do repo. Se já existir, deixe-o **intocado** ("exists — skipped") e diga
   ao usuário para preencher *Tech stack* / *Convenções*.

## Fase 2 — Análise (só se o usuário a escolheu na Fase 0)

Somente-leitura. Varra o repo e produza APENAS as saídas escolhidas. Nunca edite código;
escreva só dentro de `docs/` e (se você o criou nesta rodada) no `AGENTS.md`.

**Como varrer (barato, não exaustivo):** leia os arquivos de manifesto/config (`package.json`,
`pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, lockfiles, `Dockerfile`, configs de
CI/lint/format), passe o olho no layout de pastas de topo e amostre um punhado de arquivos-fonte
para pegar nomenclatura/estilo. Uma dúzia de arquivos bem escolhidos basta — não leia a árvore inteira.

- **stack** → Preencha os placeholders de *Tech stack* e *Convenções* no `AGENTS.md`. Se o
  `AGENTS.md` já existia (pulado na Fase 1), NÃO o sobrescreva — escreva os achados em
  `docs/analysis.md` e diga ao usuário para mesclá-los na mão.
- **adrs** → Para cada decisão arquitetural já visível no código (framework/DB, layout de
  monorepo, estratégia de auth, gerenciamento de estado, estilo de API…), rascunhe
  `docs/decisions/<id>-<slug>.md` a partir de `docs/_templates/adr.md` em `status: proposed`,
  preenchendo Contexto/Decisão/Consequências com o que o código mostra. São candidatos para o
  usuário aceitar — diga isso.
- **overview** → Escreva `docs/overview.md`: uma página — o que o projeto é, os fluxos principais,
  os módulos-chave e onde um novo agente deve olhar primeiro.
- **specs** → Para áreas óbvias inacabadas / em andamento (TODOs, features stubadas, módulos meio
  ligados), semeie `docs/specs/<area>/<id>-<feature>.md` a partir do template em `status: draft`.
  Não invente escopo — deixe as ambiguidades reais em Questões em aberto para o usuário.

Tudo que a Fase 2 escreve é um **rascunho para o usuário revisar** — você não decidiu nada em
definitivo. Imprima o que produziu.

## Depois de criar

1. Imprima o resumo de created/skipped.
2. Diga ao usuário os próximos passos opcionais (NÃO rode você mesmo):
   - Indexe os docs com o QMD: `qmd collection add <repo>/docs --name <proj>-specs && qmd embed`.
   - Preencha o *Tech stack* / *Convenções* do `AGENTS.md`.
   - Rode `to-doc spec <area> <feature>` para escrever a primeira spec.
3. **PARE.** Não implemente nada.

---

**Relacionados:** `/implement` · `/ship` · skills `to-doc` · `to-tickets`
