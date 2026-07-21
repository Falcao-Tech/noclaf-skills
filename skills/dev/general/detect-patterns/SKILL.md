---
name: detect-patterns
description: Analisa o repositório atual e escreve docs/_patterns.md — um arquivo único e enxuto com os PADRÕES REAIS já usados no código (camadas, naming, libs, estado/dados/erros/testes). Use pra semear ou atualizar o harness de patterns do projeto. Roda no init/sync (headless) ou sob demanda.
disable-model-invocation: true
model: sonnet
---

# Detect patterns

Detecta os **padrões reais** do repositório e os grava em **`docs/_patterns.md`** (arquivo
único). Serve de contexto pro harness — o `AGENTS.md` já referencia esse arquivo. Complementa
as **rules** (convenções que o time decidiu): patterns descreve o que o código **já faz**.

## Regra de ouro

**Baseie-se SÓ no que existe no repo.** Não invente, não recomende, não critique. Se algo não
está claro no código, **omita** — melhor curto e certo do que longo e especulativo.

## Como analisar (rápido, sem exaustão)

1. **Estrutura** — pastas de topo, camadas (ex.: `src/{features,components,services,lib}`),
   onde vive o quê. Use `git ls-files` / listagem, não leia tudo.
2. **Naming** — convenção de arquivos (kebab/camel/Pascal), de componentes, de funções, de
   testes. Pegue de 5–10 exemplos reais, não de um só.
3. **Stack em uso** — libs/frameworks do `package.json`/lockfile/imports e **como** aparecem
   (ex.: TanStack Query pra dados, Zod pra schema, Axios com instância própria).
4. **Padrões de código** — estado (onde mora), dados/fetching, tratamento de erro, forms,
   estilo, e a convenção de testes (arquivo, libs, o que é testado).

## Formato de saída (`docs/_patterns.md`)

- Markdown enxuto: **poucas dezenas de linhas** no total. É contexto pra outros agentes — não
  pode inflar. Prefira bullets curtos a parágrafos.
- Cabeçalho fixo + seções: `## Estrutura`, `## Naming`, `## Stack`, `## Padrões`, `## Testes`.
- Comece o arquivo com: `<!-- Gerado por detect-patterns. Reflete o código atual; rode de novo pra atualizar. -->`
- **Sobrescreva** o arquivo se já existir. **Não toque em nenhum outro arquivo.**

## Escopo

- Se um `noclaf.json` tiver `repository_id`, foque no repositório atribuído (o harness é dele).
- Pare depois de escrever o arquivo. Nada de refactor, nada de PR.
