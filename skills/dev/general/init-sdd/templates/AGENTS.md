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
- **Decisões (ADRs)** = escolhas que sobrevivem a uma única spec → `docs/decisions/<id>-<slug>.md` (sequência de id própria). O `/implement` escreve uma **automaticamente** quando uma decisão transversal surge durante o build; use `to-doc adr` para registrar uma **deliberadamente** (na hora do planejamento ou fora de banda). O **Registro de decisões** da própria spec fica para escolhas locais àquela spec.
- **FORA DE ESCOPO** numa spec é a linha mais importante — é o que impede o agente de divagar.

O loop por feature:
1. `to-doc spec <area> <feature>` → faz o scaffold de `docs/specs/<area>/*.md`, `status: draft`.
2. Refine em **plan mode**, sem código; **limpe cada Questão em aberto** (cada resposta → Registro de decisões) → `status: ready`. (Specs complexas: o `to-doc` (spec) oferece publicar como issue no NOS + GitHub.)
3. `/implement <id>` → implementa as Tarefas de cima para baixo contra `docs/specs/<area>/<id>-<feature>.md`, respeitando o AGENTS.md → `status: in-progress`. **Trabalho grande?** rode a skill `to-tickets <id>` antes, para fatiar a spec em tickets tracer-bullet (DAG de bloqueio, `docs/tickets/` ou issues NOS + GitHub); aí o `/implement` trabalha o **frontier** um ticket por vez.
4. Revise o diff contra os **Critérios de aceitação** da spec.
5. `/ship` → divide os commits `docs:` (a spec, agora `done`) + `feat:` (código), dá push na branch, abre um PR na base que você escolher (`dev`/`master`/custom).

O loop por bug (mais leve — sem id, sem área, transitório):
1. `to-doc bug <title>` → faz o scaffold de `docs/bugs/<title>.md`, `status: open`.
2. Detalhe Reprodução / Esperado / Atual se necessário.
3. `/implement <title>` → corrige no root cause, preenche **Correção**, vira `status: fixed`, poda a nota.
4. `/ship` → commit `fix:`, push, PR na base que você escolher.
