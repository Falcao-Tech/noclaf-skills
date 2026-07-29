# rules

Rules são **documentos de convenção/knowledge** que o agente carrega como regra de projeto — diferente de skills (model-invoked) e commands (slash-command). Não têm gatilho: valem como contexto/regra sempre que a stack correspondente estiver em jogo.

## Modelo em camadas (do geral pro específico)

As regras cascatam em três níveis — o de baixo **estende e aperta** o de cima:

1. **`general/general-rules.md`** — raiz; vale pra todo código, qualquer área.
2. **`<área>/rules.md`** — baseline da área; vale pra qualquer stack dela (ex.: front-end/rules vale pra lovable **e** ssr).
3. **`<área>/<stack>-rules.md`** — o específico da stack; só adiciona/aperta o que é próprio dela.

Ex.: front-end baseline diz "tipos e schemas fora do componente"; `ssr-rules` herda e aperta ("schema validado no server, params por schema, nada de segredo no client"). Back-end baseline diz "verticalize por domínio"; `django-rules` aperta ("Manager/QuerySet custom, nunca `qs`, paginação default no DRF").

Cada arquivo tem frontmatter com `title`, `description`, `applies-to` e `extends` (o pai na cascata). O campo `skills:` referencia uma skill externa (estilo [skills.sh](https://skills.sh)) que **reforça** aquele conjunto — ver "Skills externas" abaixo.

## Índice

### general/
- [general-rules](general/general-rules.md) — tamanho/forma, DRY/YAGNI, nomes, higiene, erros e testes.

### back-end/
- [rules](back-end/rules.md) — baseline: verticalização por domínio, service layer, N+1, paginação, transação/idempotência.
- [django-rules](back-end/django-rules.md) — Django/DRF: queryset pela entidade (nunca `qs`), fat services/thin views, paginação default.

### front-end/
- [rules](front-end/rules.md) — baseline: tipos/schemas fora do componente, server-state vs UI-state, a11y, loading/erro/vazio.
- [lovable-rules](front-end/lovable-rules.md) — house-style Lovable/React: ShadcnUI + Tailwind, TanStack Query/Form + Zod, Axios, Supabase/RLS.
- [ssr-rules](front-end/ssr-rules.md) — SSR (Next/TanStack): fronteira server/client, data-fetching no server, cache, params por schema.

### mobile/
- [rules](mobile/rules.md) — baseline: MVVM/Clean, thread de UI, estado unidirecional, resources fora do código.
- [ios-rules](mobile/ios-rules.md) — iOS/Swift: SwiftUI + async/await, value types, sem force-unwrap, `@MainActor`.
- [android-rules](mobile/android-rules.md) — Android/Kotlin: Compose + Coroutines/Flow, null-safety, `StateFlow`, Hilt.

## Critérios de review (`## Critérios de review`)

Nem toda regra é **verificável num diff**: `arquivo ≤300 linhas` e `sem any na borda` são checáveis; `componentize sempre` e `YAGNI` são **guia de implementação** (orientam, mas o gate não reprova mecanicamente). Pra separar os dois, cada arquivo de rules pode ter uma seção canônica **`## Critérios de review`** — um checklist `- [ ]` com o subconjunto **verificável**, escrito como afirmação checável ("Nenhum arquivo passa de 300 linhas"). O resto do arquivo segue sendo guia.

Essa seção é a **âncora legível por máquina**: o writer da harness concatena todas as `## Critérios de review` (geral + área + stack em jogo) num `docs/_review.md` determinístico, que o `code-reviewer` e o review automatizado (Visor) consomem como rubrica. Sem a seção, o arquivo só contribui guia — nada quebra.

## Skills externas (`skills:`)

Um conjunto pode apontar uma skill de terceiro (ex.: `vercel-labs/agent-skills/...`, `mattpocock/skills/...`) que reforça o mesmo padrão — instalável via `npx skills add <owner/repo>`. Hoje é **referência** (documenta o "porquê"); pra ela ser de fato instalada no worker, declare-a também como uma **dependency** (`dependencies/<slug>.md` com `skills:`), que é o que a CLI oferece instalar no `sync`.

> **Nota de entrega:** hoje o CLI **não** provisiona `rules/` (só commands/skills/agents/dependencies viram nodes). Pra estas regras chegarem ao agente, o caminho recomendado é o `init-sdd`/`to-docs` mesclarem a camada geral + o baseline da área + a stack em jogo no `AGENTS.md` do repo.
