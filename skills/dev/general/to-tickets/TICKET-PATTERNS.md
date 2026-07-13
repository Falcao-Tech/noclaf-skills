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

## Template — issue (GitHub / NOS)

```markdown
## Pai
Referência à issue-pai no tracker (se a origem foi uma issue existente; senão omita).

## O que construir
O comportamento ponta-a-ponta que este ticket faz funcionar, pela ótica do usuário — não
camada por camada.

## Critérios de aceitação
- [ ] Critério 1
- [ ] Critério 2

## Bloqueado por
- Referência a cada ticket bloqueador, ou "Nenhum — pode começar já".
```
