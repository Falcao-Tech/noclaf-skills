---
id: 1
description: Motor único de execução — implementa uma spec READY (docs/specs/), corrige um bug (docs/bugs/) ou entrega um conjunto de tickets, com o mesmo pipeline: detecção do tipo, gate de status + clarificação, worktree isolado, build conforme as convenções do repo, lint + build + testes verdes, promoção de ADR, e STAGE (nunca commit).
argument-hint: <id/caminho/título de spec ou bug | descrição dos tickets>
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
model: sonnet
effort: high
---

Implemente o trabalho: **$ARGUMENTS**

Você é um engenheiro sênior transformando intenção em código funcionando. Este é o
**único comando de execução** do loop — ele detecta o tipo de trabalho e roda o mesmo
motor, com os passos específicos de cada tipo.

## 0. Detecte o tipo de trabalho (roteamento)

Case `$ARGUMENTS` e escolha **um** modo:

- Varra `docs/specs/**/*.md` (frontmatter `id`/`title`/`status`) → match ⇒ **SPEC**.
- Varra `docs/bugs/**/*.md` (nome do arquivo / `title`) → match ⇒ **BUG**.
- `docs/tickets/*.md`, um número/URL de issue do GitHub, tasks do NOS, ou descrição livre de
  tickets ⇒ **TICKETS** (a fonte de tickets é o contrato; ver passo 3).

Vários matches (ou spec **e** bug batem) → mostre os candidatos e pergunte. Nenhum match
e não parece tickets → diga claramente; não invente caminho. `$ARGUMENTS` vazio → liste
specs (`id`, `title`, `status`) **e** bugs (`title`, `status`) e pergunte qual.

## 1. Gate de status + clarificação (bloqueio total — nenhum código até estar limpo)

Leia o item **por inteiro** primeiro.

- **SPEC** — cheque `status:`: `draft` → PARE ("refine e vire `ready` primeiro");
  `ready` → siga; `in-progress` → retome do 1º item não marcado em **Tarefas**; `done`
  → confirme antes de reaplicar. Leia Resultado, Escopo (incl. **Fora de escopo**),
  Restrições, Questões em aberto, Design, Tarefas, Critérios de aceitação, Registro de decisões.
- **BUG** — `fixed` → confirme; `open` → siga. Leia Reprodução, Esperado, Atual, Correção.
- **TICKETS** — confirme que o conjunto está completo e sem ambiguidade.

**Gate de clarificação (vale pros três).** Só está pronto quando *nada* ficou em aberto.
Procure **cada** ponto não resolvido — item de Questões em aberto sem resposta; qualquer
`TBD`/`TODO`/`???`/`<...>`, linha vazia em Design/Tarefa/Aceitação, "decidir depois" — e
qualquer campo que você precise (Esperado do bug, comportamento pretendido) ambíguo de um
jeito que só o usuário resolve. Se existir nem que seja um: PARE, devolva como perguntas
**numeradas**, obtenha resposta pra **cada**, registre (Registro de decisões da spec /
nota do bug / reafirmação pros tickets) e limpe. `status: ready` **não** dispensa isto.
O que *você* consegue resolver diagnosticando (passo 3, bug) — diagnostique, não trave;
mas nunca adivinhe o que o usuário quis dizer.

## 2. Isole o trabalho num git worktree próprio

Isto é **determinístico** — não explore com `ls`/`git branch`/`git worktree list`. Calcule
`stem` e `branch` (operação de string, a partir do passo 0) e rode **o bloco abaixo de uma
vez só**: ele acha a raiz e a default branch, cria-ou-reutiliza o worktree e instala deps.

- `stem`: SPEC → nome do arquivo da spec sem `.md` (já é `<id>-<slug>`; **não** re-prefixe o
  id). BUG → `<slug>`. TICKETS → `<slug>` curto da descrição.
- `branch`: SPEC/TICKETS → `feature/<stem>`. BUG → `fix/<stem>`.

```bash
set -euo pipefail
stem="__STEM__"; branch="__BRANCH__"                 # calculados acima; não use ls pra "achar" nada
root=$(git rev-parse --show-toplevel); repo=$(basename "$root")
def=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
def=${def:-$(git remote show origin 2>/dev/null | sed -n 's/.*HEAD branch: //p')}; def=${def:-main}
wt="$(dirname "$root")/${repo}.worktrees/${stem}"
if git show-ref --verify --quiet "refs/heads/${branch}"; then
  git worktree add "$wt" "$branch" 2>/dev/null || true   # branch já existe → reutiliza (ou já em checkout)
else
  git worktree add "$wt" -b "$branch" "$def"             # nova → cria a partir da default
fi
cd "$wt"
if   [ -f package-lock.json ]; then npm ci --silent
elif [ -f pnpm-lock.yaml ];    then pnpm i --silent
elif [ -f yarn.lock ];         then yarn --silent
elif [ -f poetry.lock ];       then poetry install -q
elif [ -f Cargo.toml ];        then cargo fetch -q
fi
# IDE: registra/abre o worktree no editor escolhido (campo `ide` do noclaf.json de origem).
# Best-effort — `{ …; } || true` neutraliza o `set -e`, NUNCA derruba o implement. Imprime
# diagnóstico (ide detectado + se o binário foi achado) pra não falhar em silêncio.
ide_msg="pulado"
{
  # Parse via node (robusto a formatação) — o noclaf já exige node.
  ide=$(node -e "try{process.stdout.write(String(require(process.argv[1]).ide||''))}catch(e){}" "$root/noclaf.json" 2>/dev/null)
  if [ "$ide" = "vscode" ]; then
    # `code` pode não estar no PATH do shell não-interativo do agente — procura no bundle.
    code_bin="$(command -v code 2>/dev/null)"
    [ -z "$code_bin" ] && [ -x "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ] && code_bin="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
    if [ -n "$code_bin" ]; then
      "$code_bin" --add "$wt" && ide_msg="worktree adicionado ao VS Code (Source Control)"
    else
      ide_msg="ide=vscode mas o comando \`code\` não foi encontrado — instale-o (VS Code → 'Shell Command: Install code command in PATH')"
    fi
  elif [ "$ide" = "xcode" ]; then
    if command -v xed >/dev/null 2>&1; then
      ws=$(find "$wt" -maxdepth 2 \( -name '*.xcworkspace' -o -name '*.xcodeproj' \) -print -quit)
      [ -n "$ws" ] && xed "$ws" && ide_msg="worktree aberto no Xcode"
    else
      ide_msg="ide=xcode mas \`xed\` não foi encontrado"
    fi
  else
    ide_msg="sem ide no noclaf.json (rode \`noclaf init\` pra escolher)"
  fi
} 2>&1 || true
echo "worktree=$wt  branch=$branch  ide=${ide:-none}"
echo "ide: $ide_msg"
```

Regra: **nunca** reutilize uma branch não relacionada em que você por acaso está — o bloco
sempre parte da default quando a branch não existe. Faça **todo o resto dentro de `$wt`**. Depois do bloco:

- **Traga a nota pra dentro (SPEC/BUG):** copie `docs/specs|bugs/<file>.md` pro worktree e
  **delete a original** da working tree de origem se ainda não estava commitada; se já
  estava, sinalize no handoff. (TICKETS: sem doc a mover.)
- Copie a config local não versionada que o build precisa (`.env*` etc.).
- **SPEC:** vire `ready → in-progress` e crie um pequeno **arquivo de progresso** (checklist
  espelhando as Tarefas), conforme convenção do repo.

> **IDE.** O bloco acima já **registra o worktree no editor** conforme o `ide` do
> `noclaf.json`: `vscode` → `code --add` (aparece no Source Control da janela ativa);
> `xcode` → `xed` no `.xcworkspace`/`.xcodeproj` (janela própria). É best-effort e nunca
> falha o implement. A saída `ide=…` do bloco confirma o que foi detectado — se vier
> `ide=none`, o `noclaf.json` não tem o campo (rode `noclaf init` de novo pra escolher).

## 3. Implemente

- **SPEC** — as **Tarefas em ordem**; após cada uma marque a caixa na spec + atualize o
  progresso. Delegue blocos grandes e independentes a subagentes se ajudar, mas seja dono
  da integração.
- **BUG** — **reproduza + diagnostique o root cause** (não o sintoma). Bug não trivial
  (causa incerta, raio amplo, vários módulos) → lance um agente **Explore** somente-leitura
  pra fixar root cause + call sites antes de mexer; bug trivial/localizado → pule o agente;
  log de erro colado → a skill `debug-log` é o caminho mais rápido. Faça a **mudança
  mínima** que resolve a raiz (não workaround) e adicione/ajuste um **teste de regressão**
  se o projeto tiver testes.
- **TICKETS** — resolva a fonte (`docs/tickets/<...>.md`, sub-issues de uma issue do GitHub
  via `gh`, ou tasks do NOS) e trabalhe o **frontier**: só tickets cujos bloqueadores estão
  **todos done**, **um por vez**, respeitando o DAG. Ao terminar um, marque-o (checkbox no
  arquivo / `gh issue close` / `nos_move_task`) e **limpe o contexto antes do próximo**.
  Nunca pegue um ticket com bloqueador pendente.
- **Todos:** respeite as convenções do repo (`CLAUDE.md`/`AGENTS.md` — idioma dos
  identificadores, migrations, onde vai schema/util, estilo de comentário). Construa
  exatamente o pedido, **sem gold-plating**. **Comente com parcimônia** — só o *porquê* não
  óbvio, nunca o *o quê*. Onde houver seams pré-combinados, use **TDD** (teste que falha
  primeiro). Rode **type-check + arquivos de teste isolados com frequência** durante o
  trabalho — não deixe tudo pro fim.

## 4. Verifique — lint + build + testes verdes

Rode **lint + build/type-check + testes** e deixe **verde** antes de finalizar. Não invente
comandos — rode **este bloco de uma vez** (descobre os scripts do manifesto e roda os
convencionais; imprime a lista pra você rodar os de nome fora do padrão):

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
[ "$fail" = 0 ] && echo "✅ verde" || { echo "❌ vermelho — conserte antes de finalizar"; exit 1; }
```

Se nenhum script padrão casou mas a lista impressa tem equivalentes (`check`, `ci`, `test:unit`…),
rode-os — **não invente**. Conserte o que você quebrou; vermelho bloqueia a finalização.

- **SPEC** — **rastreabilidade:** cada **Critério de aceitação** mapeia pra uma **Tarefa**
  marcada (refs `(T…)`); sinalize Tarefa sem critério e critério sem Tarefa. Marque só os
  critérios que você **de fato** verificou; o que depende de infra que você não roda (ex.:
  DB ao vivo) fica anotado como deploy-time.
- **BUG** — confirme que a **reprodução não reproduz mais**.

## 5. Revise

Rode a revisão do diff staged antes do handoff (`/code-review` / a skill `review-changes`).
Trate os achados: conserte o que for seu antes de entregar.

## 6. Finalização

- **SPEC** — entradas datadas no **Registro de decisões** (resolva os OPEN). Decisão
  **transversal** (afeta mais que esta spec) → **escreva o ADR você mesmo**
  (`docs/decisions/<próximo-id>-<slug>.md` a partir de `docs/_templates/adr.md`,
  `status: accepted`) e, se virou regra permanente, adicione uma linha aos **Princípios**
  no `AGENTS.md`. Vire `in-progress → done` quando Tarefas feitas + lint/build verdes;
  critérios que precisam de infra ficam como deploy-time, sem bloquear. **Quando chegar a
  `done`, delete o arquivo de progresso** (a spec + o histórico de commits são o registro
  duradouro); em `in-progress`, mantenha.
- **BUG** — preencha a seção **Correção** (root cause + o que mudou) e vire `open → fixed`.
  **Antes de podar, promova o duradouro:** regra/decisão transversal → escreva o ADR
  e/ou adicione aos Princípios do `AGENTS.md` primeiro (a nota vai ser deletada). Depois
  **pode a nota** (a Correção fica no commit; se o repo mantém arquivo morto de bugs, mova
  pra lá).
- **TICKETS** — capture qualquer decisão duradoura como ADR se for transversal.

**Todos — entrega:** **`git add` (STAGE) mas NÃO commit** — o usuário commita. Diga a ele
**onde fica o worktree**; o **`/ship`** remove o worktree depois de dar push + abrir o PR
(o trabalho já está seguro na branch) — não remova você aqui, nada foi commitado ainda.
Handoff enxuto: branch + path do worktree, o que mudou (por área), lint/build/testes
rodados + resultado, o que ainda precisa do usuário.

**Disciplina de escopo:** o **Fora de escopo** da spec é autoritativo. Bateu numa lacuna
não coberta, ou a mudança excederia o escopo → PARE e pergunte (anote no progresso). Spec
errada é spec pra corrigir com o usuário, não pra contornar em silêncio.

**Nunca:** implementar spec `draft`/não resolvida ou bug `fixed` sem confirmar; `git
commit`; entregar workaround com o root cause alcançável; renomear identificadores
existentes voltados a dados/usuário pra satisfazer regra de código novo; marcar
done/fixed/critério sem verificar com lint + build verdes.
