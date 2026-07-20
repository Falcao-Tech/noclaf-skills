---
title: Front-end SSR — regras de stack
description: Específico de front-end com renderização no servidor (Next.js / TanStack). Aperta o baseline de front-end na fronteira server/client, dados e cache.
applies-to: front-end/ssr
extends: ./rules.md
skills: vercel-labs/agent-skills/vercel-composition-patterns
---

> Assume as regras gerais de front-end (`rules.md`). Aqui só o específico de **SSR (Next.js / TanStack)**.

## Server vs Client

- Server Component por padrão; `'use client'` só quando precisa de estado/efeito/evento.
- Empurre a fronteira `'use client'` o mais **pra baixo** possível — nunca na raiz da árvore.
- Data-fetching no servidor (Server Component / loader), nunca em `useEffect`.
- Código só-servidor (segredo, SDK admin) nunca importado em componente client.

## Rotas e dados

- Env de servidor jamais vaza pro client (sem prefixo público, sem hardcode).
- `params`/`searchParams` validados por **schema** antes de usar — nunca confie na URL.
- Mutation via Server Action / route handler; **revalida o cache** depois de mutar.
- Estado de servidor no cache do framework (RSC / TanStack Query); UI state à parte.

## Performance

- `Suspense` + streaming pra não travar a página no dado mais lento.
- Imagem sempre pelo componente otimizado do framework.
