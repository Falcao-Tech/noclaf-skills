---
title: dev
type: moc
description: Commands de engenharia — o loop de spec-driven development (SDD).
---

# Commands · dev

O loop de **spec-driven dev**: escrever a intenção antes do código.

## Índice

- [[init-sdd]] — monta a estrutura `docs/` (specs, bugs, ADRs, `AGENTS.md`). Idempotente.
- [[new-spec]] — cria um spec em `docs/specs/<area>/` e para.
- [[new-bug]] — registra uma nota de bug em `docs/bugs/` e para.
- [[new-adr]] — registra uma decisão de arquitetura em `docs/decisions/` e para.
- [[implement]] — implementa spec/bug/tickets ponta-a-ponta; faz stage, nunca commit.
- [[ship]] — commit → push → abre PR do trabalho já revisado.

Fluxo típico: [[init-sdd]] → [[new-spec]] → refinar → [[implement]] → [[ship]].
