---
title: React + Vite — regras de stack
description: SPA React + Vite que consome a API própria do projeto (Django/FastAPI). Stack obrigatória, sessão e camada de dados, convenções e UI. Aperta o baseline de front-end.
applies-to: front-end/vite
extends: ../general/rules.md
skills: shadcn/ui
---

> Assume as regras gerais de front-end (`rules.md`). Aqui só o específico da **SPA React + Vite**. O front só
> exibe e manda intenção: regra de negócio, permissão e dado moram na API.

## Stack obrigatória

- ShadcnUI + Tailwind
- TanStack Query v5 + Axios (uma instância só, em `src/lib/api.ts`)
- TanStack Form v1 + Zod (nunca a API v0)
- Zustand só para UI state global
- React Router
- date-fns, Sonner, Lucide React

## Dados e sessão

- Toda chamada passa pela instância de `src/lib/api.ts`. Nada de `fetch`/axios solto e nenhum SDK de banco no front (`supabase-js`, Firebase).
- **Access token só em memória**; o refresh é cookie `httpOnly` emitido pela API (`withCredentials: true`). Nunca token em `localStorage`/`sessionStorage`.
- 401 dispara **um** refresh compartilhado entre as requests em voo e repete a request uma vez; se o refresh falhar, a sessão acaba e vai para o login.
- Nenhuma regra de negócio nem cálculo de permissão no front: ele só esconde o que a resposta da API não libera. Menu e rotas permitidas vêm da API.
- **Uma request por tela** sempre que possível: a tela consome o endpoint agregado da API em vez de montar a tela juntando N recursos.
- Lista paginada trata o envelope de paginação da API; nunca assuma que a resposta é um array.
- Nenhum id interno em rota: use slug, chave pública ou username.
- Tempo real é polling (`refetchInterval`), não websocket.
- Mutation sai de ação do usuário, nunca de `useEffect` de montagem (o StrictMode roda o efeito duas vezes).
- Erro da API normalizado num tipo só (mensagem + erros por campo); erro de campo vai para o campo do formulário.

## Código

- TypeScript strict, zero `any`.
- Named exports em tudo, exceto pages.
- Variável de ambiente com prefixo `VITE_` e **nunca segredo**: tudo que entra no bundle é público.
- Nunca hardcodar URL ou chave.
- Por domínio: `features/<domínio>/{api,queries,types}.ts`, componentes em `components/<domínio>/`, páginas em `pages/`.
- Texto de UI em português do Brasil (labels, placeholders, erros, toasts); código em inglês.

## UI

- Usar o componente do ShadcnUI sempre que existir.
- Toasts só via Sonner; ícones só via Lucide React.
- Cor de destaque do projeto reservada para a ação primária da tela.
- Tema segue `prefers-color-scheme` por padrão.
- Erro de validação aparece abaixo do input, nunca só em toast (componente de erro do TanStack Form).
- Ação destrutiva pede confirmação (AlertDialog).
- Gráficos com Recharts via Chart do ShadcnUI; seleção múltipla com Combobox do ShadcnUI (Command + Popover).

## Critérios de review

- [ ] Nenhuma chamada HTTP fora da instância de `src/lib/api.ts`; nenhum import de `@supabase/supabase-js` ou SDK de banco.
- [ ] Nenhum token gravado em `localStorage`/`sessionStorage`.
- [ ] Nenhuma variável `VITE_` contém segredo.
- [ ] Nenhuma rota usa id interno (UUID/numérico) como parâmetro.
- [ ] Nenhuma mutation disparada em `useEffect` de montagem.
- [ ] Lista paginada não é tratada como array.
- [ ] Erro de validação de formulário aparece abaixo do campo, não só em toast.
- [ ] Nenhum `any`.
