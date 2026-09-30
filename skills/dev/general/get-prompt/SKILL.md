---
id: 33
name: get-prompt
description: 'Transforma um pedido de feature ou bug num prompt pronto pra colar numa IA que escreve o código do projeto (Lovable, Bolt, v0, Codex, Cursor…) e, quando o usuário disser que rodou ("feito", "rodei", "terminou"), revisa o que ela entregou: diff, gates e o estado real em produção. Aceita texto livre, chave de tarefa (NOS-245) ou issue do GitHub (#75). Use quando o usuário chamar /get-prompt ou pedir "um prompt pra <IA>".'
model: opus
effort: high
---

Neste fluxo, **o código é escrito por outra IA**. O entregável aqui é o prompt, não a
implementação. Não edite arquivos de feature nem abra PR de implementação: os dois diffs
colidiriam. A exceção é um ajuste cosmético de uma linha, que não vale uma rodada da outra IA.

O pedido vem em `$ARGUMENTS` ou na conversa. Se não houver nenhum, pergunte o que mudar.
`$ARGUMENTS` pode ser texto livre ou uma referência:

- **Chave de tarefa** (`NOS-245`, `ABC-12`): busque no tracker disponível via MCP. No NOS da
  Noclaf (carregue com ToolSearch): `nos_list_tasks` com `search: "<chave>"` devolve o UUID, e
  `nos_get_task` com esse UUID traz descrição, checklist e comentários. A busca vale para o
  projeto ativo; se não achar, descubra o projeto pelo prefixo da chave (`nos_list_projects`) e
  repita com `project_id`.
- **Issue do GitHub** (`#75` ou URL): `gh issue view <n> --comments` no repositório atual.

Leia título, descrição, checklist e comentários. O que estiver lá é ponto de partida, como o
diagnóstico do usuário: confronte com o código. Critérios de aceite escritos na tarefa entram
no prompt.

**Tarefa com pouco detalhe: refine antes de escrever o prompt.** Investigue o código (Fase 1,
passos 2 a 4) e preencha as lacunas com o que ele responde: onde mora o comportamento, o que já
existe, quais caminhos são afetados, qual o comportamento esperado. O que o código não
responde é decisão de produto (regra de negócio, texto, quem pode o quê). Pergunte isso ao
usuário numa rodada só, com perguntas numeradas e a sua recomendação em cada uma, sem inventar
resposta.

Com as lacunas fechadas, mostre a tarefa refinada (descrição, critérios de aceite, fora de
escopo) e, depois que o usuário confirmar, grave de volta na origem pra o time ver: no tracker
via MCP (no NOS, `nos_update_task` com `description`, e os critérios de aceite como checklist
nativa com `nos_add_checklist`) ou com `gh issue edit <n> --body-file`. Preserve o texto
original do autor, acrescentando uma seção "Refinamento" em vez de apagar o que estava lá.
Só então escreva o prompt.

## Contrato do projeto

O que é específico do projeto não mora aqui. Mora numa seção do `AGENTS.md` ou do `CLAUDE.md`
(procure por "IA externa", "Lovable" ou "get-prompt"). Leia antes de tudo. A seção deve dizer:

- **Executor:** qual IA escreve o código e onde ela commita (branch, commit direto na `main`…).
- **Gates e testes:** comandos de typecheck, lint, build e testes; framework e pasta dos testes.
- **Produção:** como consultar o estado real (MCP, CLI, dashboard, IDs) e o que é somente leitura.
- **Convenções:** onde vão migrations e como nomeá-las, e pastas que são do executor e não devem
  ser tocadas.

Se a seção não existir, deduza o que der do repositório (`package.json`, pastas, histórico do
git: autor dos commits recentes) e confirme o resto com o usuário. No fim, proponha a seção
pronta pra ele adicionar.

## Fase 1 — Prompt

1. **Atualize antes de ler:** `git pull --ff-only`. O executor pode ter mexido na branch desde a
   última sessão.
2. **Trate o diagnóstico do usuário como hipótese.** Rastreie o fluxo de ponta a ponta e meça
   quando der: leia o código e consulte produção. Se a causa for outra, diga isso antes de
   escrever o prompt.
3. **Ache todos os caminhos.** Liste cada ponto que grava no dado afetado ou chama a função
   alterada: UI, backend, jobs, integrações. Se forem vários, corrija na raiz, onde todos
   passam (em geral um trigger, uma constraint ou uma função compartilhada), e não em cada
   caminho.
4. **Procure o que já existe.** Antes de pedir código novo, busque no repositório (grep por
   nomes, pastas de `lib`/`utils`/`hooks`/`shared`, funções e triggers do banco) algo que já
   faça isso ou quase isso: helper, hook, componente, função SQL, padrão de um recurso
   parecido. Se achar, o prompt manda reutilizar pelo nome e caminho. Se for quase igual,
   manda estender o que existe em vez de criar uma variante. Um executor sem essa indicação
   escreve do zero.
5. **Escreva o prompt** num bloco de código, com estas seções:
   - **Objetivo:** uma ou duas frases, no ponto de vista de quem usa.
   - **Contexto:** a causa e por que a correção vai onde vai. Cite nomes reais de arquivos,
     funções, tabelas e chaves de cache. Um prompt vago faz o executor adivinhar; um
     específico faz ele acertar.
   - **O que fazer:** arquivo por arquivo. Mande o código completo quando for curto e crítico,
     como SQL de migration, seguindo a convenção do contrato. Em cada item, diga o que
     reutilizar (`use formatDuration de src/lib/time.ts`, `siga o padrão de useCreateNote`).
   - **NÃO FAÇA:** trava contra scope creep. Liste o que o executor vai ficar tentado a mexer e
     não deve. Passe por estes tipos e inclua os que se aplicam, sempre citando o nome real:
     - *Dado existente:* não apagar nem sobrescrever o que já está lá (só adicionar, por
       exemplo).
     - *Regra vizinha:* não mexer em validação, trigger ou hook próximo que continua valendo.
     - *Erro engolido:* não esconder falha com try/catch ou `EXCEPTION WHEN OTHERS` quando a
       operação precisa falhar junto.
     - *Correção duplicada:* não repetir nos outros caminhos a regra que a raiz já cobre.
     - *Reimplementação:* não recriar o helper, hook ou componente que o item de "O que
       fazer" mandou reutilizar.
     - *Coisa legada:* não usar a coluna, a função ou o padrão antigo que ainda existe no
       código, mas já foi substituído.
   - **Critérios de aceite:** lista numerada de comportamentos observáveis, no formato "dado X,
     quando Y, então Z". Inclua o caso que já funcionava e deve continuar funcionando, e o caso
     de erro ou de permissão quando existir.
   - **Testes:** dois blocos.
     - *Automatizados:* o que o executor deve escrever, no framework e na pasta que o contrato
       indica. Cubra a lógica nova (função pura, regra de banco, parser). Se o projeto não tem
       infraestrutura de teste, diga isso e não peça.
     - *Roteiro manual:* passos numerados pra reproduzir cada critério no app (tela, ação,
       resultado esperado). É o que o usuário vai seguir depois do deploy.
6. **Antes do prompt**, explique o diagnóstico em poucas linhas. **Depois dele**, diga numa linha
   o que ficou de fora e por quê.
7. Se a mudança exigir mais de um prompt, numere e diga a ordem de envio. Mandados em paralelo,
   o executor cria a mesma coisa duas vezes, de jeitos diferentes.

## Fase 2 — Revisão (quando o usuário disser que rodou)

1. Rode `git pull --ff-only` e `git log --oneline -8`. Executores costumam quebrar a entrega em
   vários commits genéricos, então ache todos os que tocaram nos arquivos do prompt
   (`git log -- <arquivo>`).
2. **Compare o diff com o prompt.** Aponte o que faltou e o que foi além do escopo, e confira se
   os testes automatizados pedidos existem. Procure duplicação: função, hook ou componente novo
   que repete algo que já existia no repositório (mesmo que o prompt não tenha apontado).
   Ignore as pastas que o contrato diz serem do
   executor.
3. **Rode os gates** do contrato, incluindo os testes novos.
4. **Confira produção.** O que vale é o que está rodando, não o arquivo. Valide a estrutura
   (schema, funções, config) e, sempre que der, os dados reais: por exemplo, nas linhas criadas
   depois do deploy, a regra nova se cumpriu?
5. **Feche critério por critério:** para cada critério de aceite do prompt, diga se foi
   verificado (e como), se falhou ou se ficou pendente do roteiro manual. Reporte de forma
   direta o que foi verificado e o que não foi. Se algum gate falhar ou o diff
   divergir, entregue um prompt de correção curto, no mesmo formato.
6. Backfill ou escrita em produção: proponha, mas só rode quando o usuário pedir. Na
   investigação e na revisão, só leitura.
