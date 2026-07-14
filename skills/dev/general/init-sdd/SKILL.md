---
id: 21
name: init-sdd
description: Faz o scaffold da estrutura completa de spec-driven-dev — specs, bugs, ADRs e a constituição AGENTS.md — no repo atual (idempotente), copiando os templates ao lado desta skill; opcionalmente analisa o repo pra pré-preencher e então PARA. Use pra "iniciar o SDD", "montar docs/", "configurar spec-driven dev" num repo.
disable-model-invocation: true
model: sonnet
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

Determinístico e idempotente — **rode este bloco** (cria as pastas, copia os templates e o
`AGENTS.md`, pulando o que já existe). Não "procure" onde ficam os templates: são paths conhecidos.

```bash
set -uo pipefail
mkdir -p docs/specs docs/bugs docs/decisions docs/_templates
for d in specs bugs decisions; do [ -e "docs/$d/.gitkeep" ] || : > "docs/$d/.gitkeep"; done
tpl=""
for c in "$HOME/.claude/skills/init-sdd/templates" "$HOME/.codex/skills/init-sdd/templates" \
         "$HOME/.noclaf/skills/skills/dev/general/init-sdd/templates"; do
  [ -d "$c" ] && tpl="$c" && break
done
if [ -n "$tpl" ]; then
  for f in spec bug adr; do
    [ -f "docs/_templates/$f.md" ] && echo "skipped docs/_templates/$f.md" || { cp "$tpl/$f.md" "docs/_templates/$f.md"; echo "created docs/_templates/$f.md"; }
  done
  [ -f AGENTS.md ] && echo "skipped AGENTS.md" || { cp "$tpl/AGENTS.md" AGENTS.md; echo "created AGENTS.md"; }
else
  echo "FALLBACK: templates não achados nos paths padrão"
fi
```

- **Fallback** (o bloco imprimiu `FALLBACK`): os paths do cliente diferiram — leia os
  `templates/{spec,bug,adr}.md` e `templates/AGENTS.md` **relativos a esta skill** e escreva-os
  idempotente em `docs/_templates/` e na raiz (nunca sobrescreva).
- Se o `AGENTS.md` já existia (`skipped`), diga ao usuário pra preencher *Tech stack* / *Convenções*.

## Fase 2 — Análise (só se o usuário a escolheu na Fase 0)

Somente-leitura. Varra o repo e produza APENAS as saídas escolhidas. Nunca edite código;
escreva só dentro de `docs/` e (se você o criou nesta rodada) no `AGENTS.md`.

**Como varrer — delegue, não faça inline.** Lance agentes **`repo-scout`** (read-only, Haiku,
em paralelo), **um por saída escolhida**, cada um lendo só o que precisa e voltando com fatos +
paths — você **sintetiza e escreve** os docs a partir dos resumos, sem redescobrir:

- **stack** → scout lê manifestos/config (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, lockfiles, `Dockerfile`, CI/lint).
- **adrs** → scout mapeia decisões embutidas (framework/DB, layout, auth, estado, estilo de API).
- **overview** → scout mapeia layout de topo + entry points + módulos-chave.
- **specs** → scout acha áreas inacabadas (TODOs, stubs, módulos meio ligados).

Barato e não exaustivo: uma dúzia de arquivos bem escolhidos por scout basta — ninguém lê a árvore inteira.

- **stack** → Preencha os placeholders de *Tech stack* e *Convenções* no `AGENTS.md`. Se o
  `AGENTS.md` já existia (pulado na Fase 1), NÃO o sobrescreva — escreva os achados em
  `docs/analysis.md` e diga ao usuário para mesclá-los na mão.
- **adrs** → Para cada decisão arquitetural já visível no código (framework/DB, layout de
  monorepo, estratégia de auth, gerenciamento de estado, estilo de API…), rascunhe
  `docs/decisions/<id>-<slug>.md` a partir de `docs/_templates/adr.md` em `status: proposed`,
  preenchendo Contexto/Decisão/Consequências com o que o código mostra. **id sequencial** (4
  dígitos, mesmo bloco de next-id do `ADR-PATTERN` — incremente a cada arquivo desta rodada).
  São candidatos para o usuário aceitar — diga isso.
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
