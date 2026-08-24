---
title: Padrões de tickets
description: Regras de fatia vertical, playbook de refactor amplo (expand–contract) e templates de ticket usados pela skill to-tickets. Estenda com padrões do seu time/projeto.
---

# Padrões de tickets

Referência da skill `to-tickets`. Estenda à vontade — adicione seções de padrões que o seu
time usa (ex.: fatias por feature-flag, tickets de migração de dados, etc.).

## Regras de fatia vertical (tracer bullet)

- Cada fatia corta um caminho estreito mas **COMPLETO** por todas as camadas (schema, API,
  UI, testes) — vertical, NÃO uma fatia horizontal de uma camada só.
- Uma fatia concluída é **demonstrável / verificável** por conta própria.
- Cada fatia cabe numa **única janela de contexto fresca**.
- Qualquer **prefactor** vem primeiro.

Cada ticket declara suas **arestas de bloqueio** — os tickets que precisam terminar antes
dele começar. Ticket sem bloqueador começa imediatamente. O conjunto forma um DAG; o
`/implement` trabalha o **frontier** (tickets cujos bloqueadores estão todos done).

## Refactor amplo — a exceção à fatia vertical (expand–contract)

Um **refactor amplo** é uma mudança mecânica (renomear uma coluna, retipar um símbolo
compartilhado) cujo **raio de impacto** se espalha pelo codebase — uma edição quebra milhares
de call sites de uma vez e nenhuma fatia vertical fica verde. Não force num tracer bullet;
sequencie:

1. **Expand** — adicione a forma nova **ao lado** da antiga; nada quebra.
2. **Migrate** — migre os call sites em **lotes** por raio de impacto (por pacote, por
   diretório), cada lote um ticket **bloqueado pelo expand**. O CI fica verde de lote em lote
   porque a forma antiga ainda existe.
3. **Contract** — delete a forma antiga quando nenhum caller resta, num ticket **bloqueado por
   todos** os lotes de migrate.

Se nem os lotes ficam verdes sozinhos, mantenha a sequência mas deixe-os dividir uma **branch
de integração** que **todos** bloqueiam um ticket final de *integrar-e-verificar* — verde só
é prometido lá.

## Granularidade — poucas tarefas, bem separadas

Prefira **poucas** fatias que entregam comportamento a muitas tarefas atômicas. Sub-passos
técnicos de uma mesma fatia (implementar X, documentar Y, cobrir com teste Z) **não** viram
tickets separados — viram **itens de checklist** dentro da tarefa. Regra prática: se dois
"tickets" sempre seriam feitos juntos, no mesmo PR, são **um** ticket com dois itens de
checklist. Fatie por **comportamento demonstrável**, não por camada nem por arquivo.

## Título — humano, orientado a resultado

O título descreve **o que passa a ser verdade** pela ótica de quem usa — não um código de
workstream nem o nome do repo. Nada de prefixos tipo `WS1-A · [repo] …`. Repo, workstream e
dependências vão pro **Contexto** da descrição.

- ✅ "Veredito de review vira estado do ticket"
- ✅ "Anexar o PR ao ticket e entrar em review"
- ❌ "WS1-C · [noclaf-cli] Tool nos_attach_pr + mover para Em Review"

**Exceção — só no GitHub:** a issue leva o **id da spec** como prefixo (`0011 · Veredito de
review vira estado do ticket`). Não é código de workstream nem nome de repo: é a âncora que
agrupa a lista de issues por spec e casa com o `<id>-<slug>` da branch. No **NOS** e no
registro local o título continua **sem** prefixo algum.

## Anti-obsolescência

Em qualquer forma, evite **caminhos de arquivo e snippets de código** — envelhecem rápido.
Exceção: um snippet de protótipo que codifica uma decisão melhor que a prosa (máquina de
estados, reducer, schema, shape de tipo) — inline só a parte que **decide** e diga que veio de
protótipo. Apare pras partes ricas em decisão — não um demo funcional.

## Template — arquivo local (`docs/tickets/<stem>.md`)

```markdown
# Tickets: <nome curto do trabalho>
Um resumo de uma linha do que estes tickets constroem. Referencie a spec de origem se houver.

Trabalhe o **frontier**: qualquer ticket cujos bloqueadores estejam todos done. Numa cadeia
linear, isso é de cima para baixo.

## <título do ticket>
**O que construir:** o comportamento ponta-a-ponta que este ticket faz funcionar, pela ótica
do usuário — não uma lista de implementação camada por camada.
**Bloqueado por:** os títulos dos tickets que o gatam, ou "Nenhum — pode começar já".
- [ ] Critério de aceitação 1
- [ ] Critério de aceitação 2

## <título do ticket>
…
```

## Template — tarefa no NOS (descrição curta + checklists nativos)

No NOS a descrição é **curta e escaneável**; o detalhamento e o DoD viram **checklists
nativos** (via `nos_add_checklist`), não markdown enfiado no corpo. A descrição é markdown GFM
(renderiza). Corpo:

    <uma linha: o comportamento que a tarefa entrega, pela ótica do usuário>.

    ### Contexto
    **Repo:** `<repo>` · **Depende de:** <tickets bloqueadores, ou "—">
    <opcional: 1 linha de origem — spec/RFC, o que já existe>

Depois de criar a task (`nos_create_task`), popule **checklists nativos** com `nos_add_checklist`
(uma chamada por checklist):

- **Implementação** — os passos técnicos verificáveis da fatia (o que seria sub-ticket vira item aqui).
- **Definition of Done** — os critérios de aceitação, como condições checáveis.

`nos_add_checklist` indisponível (MCP antigo) → caia pra `- [ ]` markdown na descrição, sob um
`### Definition of Done`.

## Template — issue no GitHub (markdown)

O GitHub não tem checklist nativo por API — aqui o DoD é `- [ ]` no corpo. Bloqueadores **não**
entram no corpo: são campo nativo (`--blocked-by`, seção *Relationships*).

```markdown
## O que construir
O comportamento ponta-a-ponta que este ticket faz funcionar, pela ótica do usuário — não
camada por camada.

## Definition of Done
- [ ] Critério 1
- [ ] Critério 2
```
