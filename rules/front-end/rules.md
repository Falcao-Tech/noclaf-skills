---
title: Front-end — regras gerais da área
description: Regras que valem pra qualquer stack de front-end (lovable, ssr, …) — estrutura, componentes e qualidade de UI. Os arquivos de stack (lovable-rules, ssr-rules) só adicionam o específico.
applies-to: front-end
extends: ../general/general-rules.md
skills: vercel-labs/agent-skills/vercel-react-best-practices
---

> Regras gerais de front-end — valem pra **qualquer** stack da área (lovable, ssr, …).
> As regras de stack só adicionam o que é específico delas.

## Estrutura

- **Tipagens e schemas sempre fora do arquivo do componente** (ex.: `types/`, `schemas/`); o componente só importa.
- Um componente por arquivo; o arquivo é só apresentação — lógica vai pra hooks/services.
- Estado de **servidor** (data-fetching) separado do estado de **UI** — nunca no mesmo store.

## Componentes

- Sem regra de negócio nem fetch dentro de componente de apresentação — extraia pra um hook.
- Props tipadas explicitamente; nada de `any`.
- Lista sempre com `key` estável (id da entidade), nunca o índice.

## Qualidade de UI

- Acessibilidade mínima: todo input com label; todo botão com texto ou `aria-label`.
- Sem valor de estilo mágico — use os tokens/sistema de design.
- Todo estado assíncrono tem **loading, erro e vazio** na UI — nunca só o happy path.
- Formulário: input controlado + validação por **schema**, não checagem ad-hoc espalhada.
