---
id: 6
description: Commit → push → abre PR de uma branch de trabalho já revisada — normalmente após /implement, mas funciona em qualquer branch de feature (inclusive feita à mão), sem depender dele. Divide docs vs código em Conventional Commits (título em inglês ≤80 chars, corpo em português ≤120 chars), confirma o plano, dispara e então **fecha as issues/tasks entregues** (GitHub + NOS, validando que não estão já completas).
argument-hint: [branch-base]
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent, Skill
model: sonnet
effort: low
---

Faça o ship do trabalho revisado na branch atual: **commit → push → abrir PR**.

Rode isto quando **já revisou o diff** e está satisfeito. Normalmente vem após o `/implement`
(que faz stage mas deliberadamente nunca commita), mas **funciona em qualquer branch de
trabalho revisada — inclusive uma feita à mão, sem `/implement`**. Se rodou de um worktree do
`/implement`, o passo 7 o remove; branch simples, ele é pulado.

## 0. Detecte o que você vai shipar

A **única** recusa é shipar direto de uma branch-base — nunca commite/abra PR a partir de
`main`/`master`/`dev` ou da default do remote. Rode:

```bash
cur=$(git rev-parse --abbrev-ref HEAD)
def=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@'); def=${def:-main}
case "$cur" in main|master|dev|"$def") echo "PARE: '$cur' é branch-base — crie uma branch de trabalho antes."; exit 1;; esac
echo "branch de trabalho: $cur"
```

Passou → derive o tipo (pra escolher o tipo do commit de código + montar o corpo do PR):

- `feature/<id>-<slug>` → **spec**: `feat:` por padrão; leia a spec em `docs/specs/<area>/<slug>.md` pro corpo.
- `fix/<slug>` → **bug**: `fix:` por padrão.
- **Qualquer outra branch de trabalho** (feita à mão, sem passar pelo `/implement`) → **prossiga**:
  infira o tipo pela natureza do diff (`feat`/`fix`/`refactor`/…) — ou pergunte se ambíguo — e,
  sem spec vinculada, monte o corpo do PR a partir do diff + dos commits da branch. **Não exija `/implement`.**

## 1. Escolha a base do PR — pergunte PRIMEIRO, antes de qualquer commit

Se `$ARGUMENTS` deu uma branch base, use-a. Senão, peça ao usuário para escolher a **base de destino do PR**: `dev`, `master` (ou `main`), ou um nome de branch custom que ele digite. Guarde como `<base>`. Faça isso logo de cara para que nada seja commitado antes do destino ser conhecido.

## 2. Gate de segurança — lint + build precisam estar verdes

O usuário pode ter mexido no código durante o review. Re-rode **lint + build/type-check + testes** — **este é o mesmo bloco do `/implement §4`** (mantenha idêntico). Se vermelho → **PARE** e reporte; nunca dê push em código quebrado.

```bash
set -uo pipefail
fail=0; step(){ echo "▶ $*"; "$@" || fail=1; }
if [ -f package.json ]; then
  pm=npm; [ -f yarn.lock ] && pm=yarn; [ -f pnpm-lock.yaml ] && pm=pnpm
  echo "scripts:"; node -e "for(const s of Object.keys(require('./package.json').scripts||{}))console.log(' - '+s)"
  for k in $(node -e "const x=require('./package.json').scripts||{};for(const k of Object.keys(x))if(/^(lint|type-?check|build|test)$/.test(k))console.log(k)"); do step $pm run "$k"; done
elif [ -f pyproject.toml ] || [ -f setup.cfg ]; then
  command -v ruff >/dev/null && step ruff check .; command -v mypy >/dev/null && step mypy .; step pytest -q
elif [ -f Cargo.toml ]; then
  step cargo clippy -q; step cargo build -q; step cargo test -q
fi
[ "$fail" = 0 ] && echo "✅ verde" || { echo "❌ vermelho"; exit 1; }
```

## 2b. Passada de qualidade — passo OBRIGATÓRIO, achados consultivos

**Sempre** invoque a skill **`review-changes`** sobre o diff a ser commitado (staged + as mudanças tracked sujas) — **nunca pule; nunca faça stage ou commit antes dela rodar.** Ela é **somente-leitura e só-qualidade** — bloat de comentários primeiro, depois duplicação / abstração / formatação / qualidade; ela NÃO caça bugs de correção (isso é o `/code-review`). Aplique as limpezas triviais + de comentários que o usuário aprovar; levante qualquer coisa mais substancial para uma decisão. Se as correções aplicadas mexeram no código, **re-rode o passo 2** (lint + build). Rodá-la é **obrigatório**; os **achados** são consultivos — eles informam o commit e nunca bloqueiam o ship.

## 3. Stage (respeitando a intenção)

- Se o usuário já deu stage num subconjunto, **respeite** — não re-stage por cima da escolha dele.
- Se nada estiver staged, dê stage nas mudanças deste trabalho: modificações tracked + os arquivos que este trabalho adicionou. **Respeite o `.gitignore`; nunca dê stage em `node_modules`, `.env*`, saída de build, ou na cópia da nota do bug.** Na dúvida, prefira caminhos explícitos a `git add -A`.

## 4. Divida em Conventional Commits (docs vs código)

Agrupe as mudanças staged em até dois commits:

- **`docs:`** — tudo em `docs/` (o arquivo da spec, agora `status: done`, mais quaisquer atualizações de docs). Para bugs isso normalmente fica vazio (a nota é transitória/não versionada) — **pule o commit de docs se não houver nada tracked**.
- **`<feat|fix|refactor|…>:`** — a implementação. Escolha o tipo pela natureza da mudança (`feat:` comportamento novo, `fix:` um bug, `refactor:` sem mudança de comportamento), conforme Conventional Commits.

Formato da mensagem de **cada** commit:

- **Título:** `<type>: <short English description>` — modo imperativo, **≤ 80 chars no total** (o prefixo `type:` conta para isso).
- Linha em branco.
- **Corpo:** a descrição de verdade **em português, ≤ 120 chars**, em uma linha. Nada depois dela — sem trailers.

## 5. Confirme antes de qualquer coisa sair da máquina

Mostre ao usuário e **espere aprovação explícita**:

- o plano de commits — o título de cada commit + o corpo em português + seus arquivos (`git diff --cached --stat` por grupo),
- o alvo do push (branch) e a **base do PR** `<base>`.
  Só prossiga com um OK explícito. Push + PR são visíveis para o time e chatos de desfazer — este gate é justamente o ponto.

## 6. Commit, push, abra o PR

- Crie o(s) commit(s) em ordem: **`docs:` primeiro, depois o commit de código.**
- **Push** com upstream: `git push -u origin <branch>`. Sem remote `origin`? → **PARE** com orientação; não fabrique um remote.
- **Abra o PR** para `<base>` com `gh pr create --base <base> --head <branch>`:
  - **Título** = o título do commit de código (caia de volta para o título de docs se não houver commit de código).
  - **Corpo** = um resumo curto + um link para a spec + os **Critérios de aceitação** da spec como um checklist `- [ ]` (para bugs: root cause + a correção).
  - `gh` faltando / não autenticado, ou sem remote do GitHub? → o commit + push ainda dão certo; **pule o PR**, imprima o comando `gh pr create …` exato para o usuário rodar e diga o porquê.

## 7. Feche as issues/tasks entregues (valide antes)

Só se o **push + PR do passo 6 deram certo** — o trabalho está entregue, então feche o que
ele resolve. Descubra os identificadores no registro: `docs/tickets/<stem>.md` (o `task_id` do
NOS / `#N` do GitHub que o `/to-tickets` gravou) e/ou o `issue:` do frontmatter da spec. Para
cada um, **cheque o estado primeiro e só complete o que ainda está aberto** (idempotente —
nunca re-feche o que já está completo):

- **GitHub** (se `gh` disponível) → `gh issue view <n> --json state -q .state`. `OPEN` →
  `gh issue close <n> --comment "Entregue no PR <url>"`. Já `CLOSED` → pule.
- **NOS** → `nos_get_task` pra ver o estado; se ainda não entregue, `nos_move_task` pro estado
  de entrega (`done`/`delivered`) e `nos_record_delivery` (`title`, `pr_url`, `task_id`). Já
  entregue → pule. As tools `nos_*` rodam em qualquer cliente (inclusive Cowork).

Branch feita à mão, sem issue/task vinculada → pule este passo. **Nunca invente** uma issue
pra fechar.

## 8. Remova o worktree (só se o push deu certo)

**Só se o push do passo 6 deu certo.** Se o push falhou ou foi pulado (sem remote),
**mantenha** o worktree — nunca remova trabalho sem push. Se removeu, rode **este bloco de
uma vez** (determinístico — não precisa `git worktree list` pra "descobrir" o path):

```bash
set -euo pipefail
here=$(git rev-parse --show-toplevel)                       # o worktree atual
main=$(git worktree list --porcelain | sed -n '1s/^worktree //p')
if [ "$here" != "$main" ]; then
  cd "$main"                                                 # não dá pra remover o worktree em que se está
  git worktree remove --force "$here"                        # --force: deps/.env/cache não versionados vivem lá
  echo "worktree removido: $here (branch mantida)"
else
  echo "sem worktree (branch simples) — nada a remover"
fi
```

A **branch é mantida** (o PR aponta pra ela); só o diretório sai. Re-checkout depois se
precisar de follow-up.

## 9. Handoff

Imprima, nesta ordem: os SHAs dos commits + títulos, a branch com push feito, as **issues/tasks fechadas** (GitHub `#N` / NOS `task_id`, ou "nenhuma vinculada"), e se o **worktree foi removido** (`<path>`, de volta no repo principal com a branch preservada) ou **mantido** (com o porquê). **Por último, em sua própria linha: a URL do PR** — a saída clicável do `gh pr create` — ou o motivo do skip se o passo do PR foi pulado. O link do PR é a última coisa que o usuário vê.
