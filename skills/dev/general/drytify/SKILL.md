---
id: 12
name: drytify
description: Encontra e remove duplicação de código genuína — cópias exatas, gêmeos estruturais, repetições semânticas/comportamentais e reuso perdido de utilitários já existentes — e então faz refactor com julgamento de dev senior, em vez de perseguir DRY como um fim em si mesmo. Use quando o usuário digitar /drytify, pedir para "dar um DRY", deduplicar, encontrar/remover código repetido, consolidar copy-paste ou extrair um helper. Por padrão atua nos arquivos alterados (uncommitted + diff da branch vs main); aceita um argumento de path para restringir o escopo, ou --all para varrer o repositório inteiro. Sempre propõe antes de aplicar.
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
---

# /drytify — encontre e remova duplicação de verdade

Você está atuando como um engenheiro senior fazendo uma passada focada de DRY. O
objetivo não é apagar toda linha repetida — é encontrar as duplicações que
realmente prejudicam o codebase (risco de drift, custo de manutenção, reuso
perdido) e removê-las com um refactor que um reviewer criterioso aprovaria.

Refactors de DRY ruins são piores que a duplicação que substituem. Uma abstração
errada força toda mudança futura a passar por um formato que não encaixa. Você vai
rejeitar mais candidatos do que aceitar — esse é o trabalho.

Argumentos passados: `$ARGUMENTS`

---

## Passo 1 — escolha o escopo

Faça o parse de `$ARGUMENTS`:

- **vazio** → modo changed-files (padrão). Varre só o que o usuário está
  trabalhando ativamente: mudanças uncommitted mais o diff da branch vs a branch
  main. É rápido e quase sempre o escopo certo.
- **`--all`** → modo repositório inteiro. Use com parcimônia — repos grandes
  deixam isso lento e barulhento.
- **qualquer outra coisa** → trate o argumento como um path ou glob, varra só
  aquela subárvore.

Antes de varrer, anuncie o escopo escolhido ao usuário em uma frase curta para
que ele possa te corrigir cedo se estiver errado.

### Montando a lista de arquivos

**Modo changed-files:**

```bash
# uncommitted (modified + untracked, excluding ignored)
git status --porcelain | awk '{print $2}'
# branch diff vs main or master, whichever exists
base=$(git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null)
[ -n "$base" ] && git diff --name-only "$base" HEAD
```

Pegue a união, descarte deleções, descarte arquivos gerados/lock (veja as
exclusões abaixo).

**Modo path:** use `Glob` a partir do path informado. Respeite o `.gitignore` —
`git ls-files <path>` é a forma mais segura.

**Modo all:** `git ls-files` (já respeita o `.gitignore`).

### Sempre exclua

- `node_modules/`, `dist/`, `build/`, `.next/`, `coverage/`
- lock files (`*.lock`, `package-lock.json`, `bun.lockb`, `yarn.lock`)
- código gerado, migrations (`*/migrations/*`, `*.generated.*`)
- saída minificada/bundled, código vendored
- o CLAUDE.md do projeto e quaisquer outros docs, a menos que o usuário peça

**A detecção é read-only e paralelizável — delegue por padrão.** Se há mais que um
punhado de arquivos (≳8) ou várias passadas, despache a detecção a agentes
**`repo-scout`** (Haiku, read-only) em paralelo — um por passada ou por diretório —,
cada um retornando achados estruturados (`arquivo:linha · tipo · o que se repete`).
Só faça inline pra escopo pequeno. Mantenha seu contexto limpo pras fases de
**julgamento** (passo 3) e **proposta** (passo 4) — essas são suas, não do scout.

---

## Passo 2 — detecte as duplicações (quatro passadas)

Rode todas as quatro passadas. Elas revelam problemas diferentes e um codebase
real vai ter achados em mais de uma categoria.

### Passada A — duplicatas exatas / quase-exatas (clones Type-1/2)

Blocos de múltiplas linhas que são byte-idênticos ou diferem só em whitespace,
comentários ou nomes de identificadores. Procure por:

- Boilerplate repetido de `try/catch` em volta da mesma operação.
- Chains de validação de formulário copy-pasted com um campo renomeado.
- Setups repetidos de fetch/axios, construção de headers, mapeamento de erros.
- Fragmentos de render idênticos entre componentes.

`grep`/`rg` por trechos distintivos e veja quantas vezes cada um aparece. Uma
heurística útil: qualquer bloco de 6+ linhas não triviais que aparece 3+ vezes é
quase certamente um achado real.

### Passada B — duplicatas estruturais (clones Type-3)

Mesmo formato, nomes diferentes. Os corpos não são idênticos, mas o *esqueleto*
é. Padrões comuns:

- Duas funções com o mesmo control flow sobre tipos diferentes
  (`getStudentById` e `getTeacherById` fazendo a mesma dança do Sequelize).
- Componentes React com layout de hooks idêntico e o mesmo encanamento de props
  envolvendo um elemento interno diferente.
- Cases de reducer ou route handlers construídos a partir do mesmo template.

Quando encontrar um, esboce o esqueleto mentalmente — se você consegue descrever
as duas ocorrências com uma frase ("fetch por id, throw no miss, retorna DTO
formatado"), são gêmeos estruturais.

### Passada C — duplicatas semânticas / comportamentais (clones Type-4)

Código diferente, mesmo efeito. As mais difíceis de identificar — pattern
matching não acha essas. Sinais:

- Dois utilitários produzindo a mesma saída a partir da mesma entrada por
  caminhos diferentes (um formatador de data usando `Intl` e outro usando
  concatenação manual de strings).
- Dois validadores impondo a mesma regra com libraries diferentes.
- Dois endpoints / services / hooks que envolvem a mesma chamada subjacente.

Essas precisam de olhos, não de regex. Leia o código; pergunte "o que isso
*faz*?" e note quando a resposta bate com algo que você já viu.

### Passada D — abstrações redundantes / reuso perdido

Antes de propor qualquer helper *novo*, verifique se o codebase já tem um.
Procure nos lares convencionais:

- `shared/`, `src/shared/`
- `src/hooks/`, `src/utils/`, `src/lib/`
- `server/modules/*/services/`, `server/utils/`

Dois resultados que você precisa tratar:

1. **Reuso perdido**: um util já existe; o código duplicado deveria ser apagado
   em favor de importá-lo.
2. **Wrapper redundante**: um helper custom duplica um primitivo do framework
   (um `useToggle` que só envolve `useState<boolean>`, um clone de `cn` sobre
   `clsx`, um helper de data que o `dayjs` já fornece). Proponha **apagar o
   wrapper**, não extrair mais coisa para dentro dele. Menos abstrações, não mais.

---

## Passo 3 — aplique julgamento de dev senior

Você vai encontrar mais "duplicação" do que deveria refatorar. Rejeite qualquer
candidato que falhe nesses checks. Explique a rejeição no report quando a
duplicação for visível o suficiente para o usuário se perguntar por que você
pulou.

### A regra de três

Duas ocorrências são coincidência; três são um padrão. Extraia na **terceira**
cópia, não na segunda — a menos que as cópias sejam claramente estáveis e
improváveis de divergir (ex.: um valor literal de config, uma regex para um
formato fixo). Duas quase-duplicatas com razões plausivelmente diferentes para
mudar devem ficar separadas.

### Boundaries são load-bearing

Código de cada lado de uma boundary deliberada pode parecer igual e *deveria*
ficar separado:

- **Client ↔ server**: implementações paralelas do mesmo formato são ok se
  evoluem de forma independente. Só extraia para `shared/` quando a coisa é
  genuinamente compartilhada (um tipo, um schema Zod usado nos dois lados, uma
  função pura sem dependências de ambiente).
- **Módulo ↔ módulo**: dois feature modules com internals parecidos são ok.
  Extração prematura acopla os dois e propaga churn.
- **API pública ↔ interna**: não fusione as duas só porque são parecidas hoje.

Se extrair força o helper a viver numa camada que importa dos dois lados, isso é
um smell — geralmente sinal de que a duplicação não é real.

### Abstração errada é pior que duplicação

A regra da Sandi Metz. Sinais de que sua extração proposta está errada:

- O helper precisa de uma flag/opção para cada caller (`opts.skipValidation`,
  `opts.includeMeta`, `opts.legacy`) — os callers na verdade querem coisas
  *diferentes*, não a mesma coisa com botões.
- Callers futuros vão precisar de mais uma flag ainda para desativar comportamento
  embutido para os três primeiros.
- O helper tem múltiplos modos que compartilham quase nenhum código internamente
  (um `if (mode === 'a') { ... } else if (mode === 'b') { ... }` gigante).

Quando a abstração seria pior que as cópias, deixe as cópias.

### Similaridade incidental vs essencial

Dois pedaços de código que parecem iguais hoje mas existem por razões diferentes
vão divergir. Leia cada ocorrência e pergunte *por que isso existe?* — se as
respostas são diferentes, a similaridade é incidental e você deve deixar em paz.

### Não refatore através de código instável

Se um bloco duplicado está em código mudando ativamente (commits recentes, PRs
abertos mexendo nele, TODOs por perto), adie. Refatorar durante churn perde
mudanças e cria dor de merge.

---

## Passo 4 — proponha, não aplique ainda

Produza um report ranqueado. Ordene por **severidade, depois confiança**.

Para cada achado:

```
### [N] <one-line name>
- Severity: high | med | low
- Confidence: high | med | low
- Type: exact | structural | semantic | missed-reuse
- Locations:
  - path/to/file.ts:42
  - path/to/other.ts:118
  - path/to/third.ts:7
- What's duplicated: <one sentence>
- Proposed change:
  - Target: <new file path / existing util to reuse>
  - Name + signature: <e.g. `formatBrazilianDate(d: Date): string`>
  - Call sites rewritten: <count + brief>
- Risks: <callers, tests, type changes, behavioral diffs>
- Why this is worth it: <one sentence — drift risk, missed reuse, etc.>
```

Para achados que você considerou e **rejeitou**, inclua uma seção curta
"Considerado mas pulado" para o usuário saber que você os viu e por quê os deixou
em paz. Isso constrói confiança e traz à tona decisões que o usuário pode querer
sobrescrever.

### Rubrica de severidade

- **high** — 3+ cópias exatas, ou qualquer duplicação onde as cópias já
  divergiram (uma tem um bug fix que as outras não têm).
- **med** — 2 cópias estáveis que são claramente o mesmo conceito, ou reuso
  perdido de um utilitário existente.
- **low** — similaridade estrutural que vale notar mas não necessariamente agir;
  a regra de três ainda não foi atingida.

### Rubrica de confiança

- **high** — duplicatas exatas, ou reuso perdido onde o utilitário existente é um
  drop-in.
- **med** — gêmeos estruturais onde o formato da extração é óbvio.
- **low** — matches semânticos/comportamentais; o usuário deveria fazer um
  sanity-check antes de você editar.

### Perguntando quais aplicar

Depois do report, pergunte ao usuário quais achados aplicar. Use
`AskUserQuestion` quando houver 2–4 achados — apresente-os como opções
multi-select com a severidade no label. Para 5+ achados, peça inline por uma
lista numerada (ex.: "1, 3, 4" ou "all high").

Recomendação padrão: **aplicar os itens high-severity, high-confidence**. Mencione
esse padrão na pergunta para o usuário poder aceitá-lo rápido.

Se o usuário disser "all" mas houver itens low-confidence, confirme uma vez antes
de editar especificamente esses.

---

## Passo 5 — aplique os achados aprovados

Para cada item aprovado, em ordem:

1. **Crie ou atualize o target.** Se estiver reusando um utilitário existente,
   importe-o. Se estiver criando um novo, coloque onde ele pertence:
   - tipos/schemas compartilhados → `shared/`
   - hooks reusáveis → `src/hooks/`
   - helpers server-side → `server/modules/<module>/services/` ou uma localização
     apropriada ao domínio. **Não** invente um arquivo genérico `utils/` de
     despejo se o projeto ainda não tem um.

2. **Reescreva os call sites com `Edit`.** Atualize os imports. Preserve os nomes
   exportados se outros módulos os importam — se você precisar renomear, atualize
   todo importador.

3. **Rode os checks do projeto** — mesmo bloco do `/implement §4` (descobre e roda os
   scripts reais; não invente):
   ```bash
   set -uo pipefail
   fail=0; step(){ echo "▶ $*"; "$@" || fail=1; }
   if [ -f package.json ]; then
     pm=npm; [ -f yarn.lock ] && pm=yarn; [ -f pnpm-lock.yaml ] && pm=pnpm
     for k in $(node -e "const x=require('./package.json').scripts||{};for(const k of Object.keys(x))if(/^(lint|type-?check|build|test)$/.test(k))console.log(k)"); do step $pm run "$k"; done
   elif [ -f pyproject.toml ] || [ -f setup.cfg ]; then
     command -v ruff >/dev/null && step ruff check .; command -v mypy >/dev/null && step mypy .; step pytest -q
   elif [ -f Cargo.toml ]; then
     step cargo clippy -q; step cargo build -q; step cargo test -q
   fi
   [ "$fail" = 0 ] && echo "✅ verde" || echo "❌ vermelho — pare e reporte"
   ```
   Nada definido → pule.

4. **Reporte**, por item: arquivos alterados, call sites reescritos, checks
   rodados + resultado, qualquer coisa que o usuário deva conferir manualmente
   (edge cases de comportamento, testes ausentes, etc.).

5. **Não commite, não faça stage.** O usuário roda `git commit` por conta
   própria. Pare depois de reportar.

Se um check falhar no meio do apply, pare e reporte. Não tente uma recuperação
destrutiva — o usuário decide se reverte ou corrige seguindo em frente.

---

## Coisas que esta skill NÃO deve fazer

- **Não adicione comentários** ao novo helper a menos que o *porquê* seja
  não-óbvio. Código bem nomeado se documenta sozinho.
- **Não refatore por "menos linhas"** — isso é outra preocupação. Esta skill é
  sobre duplicação, não densidade.
- **Não toque** em código gerado, migrations, lockfiles, código vendored ou
  qualquer coisa em `node_modules`.
- **Não extraia** tipos ou helpers através de boundaries (client/server,
  módulo/módulo) a menos que a coisa seja genuinamente compartilhada.
- **Não seja fofo** — helpers de uma letra, chains point-free e generics
  espertos não são o objetivo. Uma função chata e nomeada que o próximo leitor
  consegue grepar é melhor.
- **Não expanda o escopo** — se você achar duplicações fora do escopo pedido,
  mencione-as no report em "Fora de escopo, notado de passagem", mas não as
  refatore.

---

## Referência rápida — como é o resultado bom

**Boa extração:**

> Três componentes chamavam `axios.get(url, { headers: { Authorization: ... } })` com a mesma construção de header de auth. Extraído para `src/service/authedRequest.ts`. Substituídos 3 call sites. Comportamento idêntico.

**Boa rejeição:**

> `formatStudentName` (client) e `formatStudentName` (server logger) parecem idênticos mas existem por razões diferentes — a versão client pode localizar, a versão server é para logs. Deixando como está.

**Bom "reuso perdido":**

> `src/hooks/useDebounce.ts` já existe. `StudentSearch.tsx` reimplementa a mesma lógica inline — substituir pelo hook existente.

**Má extração (você deveria rejeitar):**

> Extraiu `processItem` recebendo 6 flags boolean para cobrir todas as variações que os callers precisavam. → Não. Os callers querem coisas diferentes. Deixe as cópias.
