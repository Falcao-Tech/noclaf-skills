---
id: 6
description: Commit → push → abre PR para um worktree de /implement já revisado. Divide docs vs código em Conventional Commits (título em inglês ≤80 chars, corpo em português ≤140 chars), confirma o plano e então dispara.
argument-hint: [branch-base]
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent, Skill
---

Faça o ship do trabalho revisado na branch atual: **commit → push → abrir PR**.

Rode isto **depois** do `/implement`, uma vez que **você já revisou o diff** e está satisfeito com ele — o `/implement` faz stage mas deliberadamente nunca commita; este é o comando que termina o serviço. Todo o trabalho acontece dentro do worktree que o `/implement` criou.

## 0. Detecte o que você vai shipar
Leia a branch atual e derive o tipo de trabalho:
- `feature/<id>-<slug>` → **spec**. O tipo do commit de código é `feat:` por padrão; leia a spec em `docs/specs/<area>/<slug>.md` para o corpo do PR.
- `fix/<slug>` → **bug**. O tipo do commit de código é `fix:` por padrão.
- Qualquer outra coisa (`main`/`master`, ou uma branch sem linhagem de `/implement`) → **PARE**: diga ao usuário para rodar `/implement` primeiro. Nunca faça ship de uma branch não relacionada.

## 1. Escolha a base do PR — pergunte PRIMEIRO, antes de qualquer commit
Se `$ARGUMENTS` deu uma branch base, use-a. Senão, peça ao usuário para escolher a **base de destino do PR**: `dev`, `master` (ou `main`), ou um nome de branch custom que ele digite. Guarde como `<base>`. Faça isso logo de cara para que nada seja commitado antes do destino ser conhecido.

## 2. Gate de segurança — lint + build precisam estar verdes
O usuário pode ter mexido no código durante o review. Re-rode o **lint** + **build/type-check** do repo (os mesmos scripts que o apply-* usou — não invente comandos). Se vermelho → **PARE** e reporte; nunca dê push em código quebrado.

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
- **Corpo:** a descrição de verdade **em português, ≤ 140 chars**, em uma linha. Nada depois dela — sem trailers.

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

## 7. Remova o worktree (só se o push deu certo)
Se isto rodou dentro de um worktree de apply-* — verifique com `git worktree list` (a entrada `<repo>.worktrees/<stem>`) — desmonte-o agora: os commits estão na branch (local + com push feito), então removê-lo não perde nada além do diretório de checkout.
- **Só se o push do passo 6 deu certo.** Se o push falhou ou foi pulado (sem remote), **mantenha** o worktree — nunca remova trabalho sem push.
- **Dê `cd` para fora primeiro** até a raiz do repo principal (você não pode remover o worktree em que está), depois `git worktree remove --force <path>` — o `--force` é obrigatório porque deps não versionadas / `.env` / cache de build vivem lá.
- **Mantenha a branch** (o PR aponta para ela); só o diretório do worktree vai embora. Faça re-checkout da branch depois se precisar de trabalho de follow-up.
- Não rodou de um worktree (branch simples)? Pule este passo.

## 8. Handoff
Imprima, nesta ordem: os SHAs dos commits + títulos, a branch com push feito, e se o **worktree foi removido** (`<path>`, de volta no repo principal com a branch preservada) ou **mantido** (com o porquê). **Por último, em sua própria linha: a URL do PR** — a saída clicável do `gh pr create` — ou o motivo do skip se o passo do PR foi pulado. O link do PR é a última coisa que o usuário vê.
