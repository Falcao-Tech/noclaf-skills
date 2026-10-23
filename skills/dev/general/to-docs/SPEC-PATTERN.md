---
title: Padrão — spec (PRD)
description: Regras de autoria de uma spec do SDD em docs/specs/ — área, id global, síntese vs entrevista, seções, status, publicação. Referência da skill to-doc.
---

# Padrão — spec (PRD)

Scaffolda uma spec em `docs/specs/<area>/`. Não escreva código nem mexa fora de `docs/specs/`.

**Síntese vs entrevista.** Se a conversa já tem contexto rico (você já discutiu problema,
solução, codebase) → **sintetize** a spec a partir disso; não re-entreviste o que já foi
dito. Explore o repo se ainda não explorou, use o **glossário de domínio** do projeto e
respeite os **ADRs** da área. Se o contexto for magro, colete o mínimo por perguntas. Em
qualquer caso: **lacuna genuína NÃO se inventa** — vira **Questão em aberto** (o gate).

1. **Área (subpasta de domínio).** Área explícita do usuário → use-a. Senão, infira das
   subpastas existentes em `docs/specs/` + a descrição; genuinamente incerto → PERGUNTE.
   Nomes de área em inglês, kebab-case (conforme o `AGENTS.md`).
2. **id global.** Determinístico — rode (não leia arquivo por arquivo):
   ```bash
   n=$(grep -rhoE '^id:[[:space:]]*"?[0-9]+' docs/specs 2>/dev/null | grep -oE '[0-9]+' | sort -n | tail -1); printf "%04d\n" $(( ${n:-0} + 1 ))
   ```
   O id é **global** — único entre todas as áreas, não por pasta.
3. **Caminho:** `docs/specs/<area>/<id>-<kebab-case-feature>.md` — o id prefixa o arquivo (pra
   ordenar e ser handle estável se o slug mudar) e também vive no frontmatter. Título/slug em inglês.
4. **Scaffold a partir de `docs/_templates/spec.md` e preencha o que já sabe.** Se faltar, use
   as seções: Problema | Solução | Histórias de usuário | Escopo (com **Fora de escopo**) |
   Restrições | Questões em aberto | Decisões de implementação | Decisões de teste | Tarefas |
   Critérios de aceitação | Plano de QA | Registro de decisões | Notas.
   - **Histórias de usuário:** lista numerada e **extensa** — "Como <ator>, quero <feature>,
     para <benefício>." É daqui que os Critérios de aceitação derivam.
   - **Decisões de implementação:** módulos/interfaces, schema, contratos de API, decisões
     arquiteturais. **Sem caminhos de arquivo nem snippets** — exceção: snippet de protótipo
     que codifica uma decisão; inline só a parte que decide e diga que veio de protótipo. Em
     **Design → Fluxo (Mermaid)** deixe a fence vazia (stub `flowchart TD`); é preenchida no refino.
   - **Decisões de teste:** o que é um bom teste aqui (só comportamento externo), quais módulos
     serão testados, prior art no repo.
   - Frontmatter: `id` (entre aspas), `title`, `area`, `status` (passo 5), `created` = hoje,
     `issue:` vazio. Numere as **Tarefas** `T1, T2…`; cada **Critério** é `CA<n>` +
     Dado/Quando/Então nomeando a(s) Tarefa(s), ex.: `CA1 (T1) Dado … quando … então …`.
   - **Plano de QA:** como quem testa confere a entrega, **pela superfície** declarada (tela,
     CLI, API, job) — o que a pessoa faz e vê, nunca como o código foi escrito. Cenários
     `QA<n> [auto|manual] (CA<n>) ação → resultado visível`; **todo CA tem ≥1 cenário**.
     `[auto]` = o agente prova sozinho (teste automatizado ou comando reproduzível) — prefira-o
     sempre que a superfície permitir; `[manual]` = sobra pro QA humano. Superfície `tela` →
     nada de cenário que só reproduz via Postman/API (corpo inválido, 401 forjado). Inclua
     **massa de dados** (o que precisa existir antes, em qual estado), o caminho negativo
     visível e a **regressão** (fluxo vizinho que não pode quebrar). Mensagem exibida vai
     **exata**; se ainda não existe, marque "a confirmar" — o `to-qa` reconcilia depois.
5. **Status.** Síntese completa (**Questões em aberto** vazio, nada de `TBD`/`<...>`, todo CA
   coberto por cenário de QA) → `status: ready`. Sobrou lacuna → `status: draft`.
6. **Publicação (só spec relativamente complexa + `ready`).** Simples → pule (fica só em
   `docs/specs/`). Complexa (várias histórias/módulos, provável DAG de tickets) **e** `ready` →
   **PERGUNTE se quer publicar como issue**. Só publique se confirmar:
   - **NOS** — projeto da sessão (`nos_set_project` se preciso) + `nos_create_task` (título =
     `title`, corpo = Problema + Solução + id/link da spec).
   - **GitHub** — `gh issue create` com o corpo da spec, `--assignee @me`, `--type Feature`
     (`gh api orgs/<org>/issue-types` lista os válidos; 404 / repo pessoal → omita `--type`) e
     label padrão `enhancement` (dependência `gh`). Ela vira a
     issue-pai dos tickets do `to-tickets`.
   - Grave a ref (URL/número) no frontmatter `issue:`. **Draft nunca é publicado.**
7. **Feche.** Imprima caminho, id, status e (se publicou) a ref da issue. **PARE.** Próximo passo:
   - `draft` → refine em plan mode, **limpe as Questões em aberto** (cada resposta → Registro de
     decisões) → `ready`.
   - `ready` + grande → skill `to-tickets` pra fatiar em tracer bullets.
   - `ready` + pequeno → `/implement <id>`.
