---
name: to-doc
description: Cria um doc do loop de spec-driven dev — spec/PRD (docs/specs/), nota de bug (docs/bugs/) ou ADR (docs/decisions/) — scaffoldando do template e PARANDO (sem codar). Roteia por tipo e carrega só o padrão do tipo pedido. Use quando o usuário pedir pra "criar uma spec/PRD", "registrar um bug", "escrever um ADR" ou iniciar o loop. Substitui /new-spec, /new-bug e /new-adr.
disable-model-invocation: true
model: sonnet
---

# To Doc

Cria **um** doc do SDD e **PARA** (só scaffolda — nunca coda). Roteia por tipo e segue o
padrão específico. As regras de cada tipo ficam nos arquivos ao lado — **disclosure
progressivo: leia só o do tipo pedido**:

- **spec** → [SPEC-PATTERN.md](SPEC-PATTERN.md)
- **bug** → [BUG-PATTERN.md](BUG-PATTERN.md)
- **adr** → [ADR-PATTERN.md](ADR-PATTERN.md)

## 0. Detecte o tipo

`$ARGUMENTS` começando com `spec` / `bug` / `adr` (case-insensitive) → esse é o tipo; o resto
é o título/descrição. Sem tipo explícito → infira (feature nova = **spec**; defeito = **bug**;
decisão transversal deliberada = **adr**) e, se ambíguo, PERGUNTE antes de continuar.

## 1. Siga o padrão do tipo

Leia **apenas** o `*-PATTERN.md` correspondente e execute-o. Regras comuns aos três:

- **Scaffolda** a partir de `docs/_templates/<tipo>.md` (`spec.md` | `bug.md` | `adr.md`) — a
  estrutura literal mora ali. Se o template faltar, use as seções listadas no PATTERN.
- Preencha **só o que o usuário/contexto de fato deu**; o resto vira placeholder curto (ou,
  na spec, uma **Questão em aberto**). **Não invente** design, justificativa nem correção.
- **Não escreva código** nem mexa fora do diretório do tipo (`docs/specs|bugs|decisions/`).
- **PARE** ao final — este comando só cria o doc.

## 2. Feche

Imprima o caminho criado (e o id, quando houver) e o **próximo passo** (detalhado no PATTERN):
spec → refinar → `to-tickets`/`/implement`; bug → `/implement`; adr → refinar → `accepted`.
