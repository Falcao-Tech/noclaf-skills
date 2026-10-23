---
id: "<NNNN>" # global, com zeros à esquerda, único entre todas as specs
title: <nome da feature>
area: <pasta de domínio, ex.: social-worker | assessment | auth>
status: draft # draft | ready | in-progress | done
created: <YYYY-MM-DD>
issue: # opcional — URL/ref da issue (NOS/GitHub) quando publicada
---

# <nome da feature>

## Problema
O problema que o usuário enfrenta, pela ótica **dele**. Uma ou duas frases — a dor, não a solução.

## Solução
O que passa a ser verdade quando isto estiver pronto, pela ótica do usuário. Uma ou duas frases, visível ao usuário.

## Histórias de usuário
<!-- Lista numerada e EXTENSA — cubra todos os aspectos da feature. Formato: "Como <ator>, quero <feature>, para <benefício>." -->
1. Como <ator>, quero <feature>, para <benefício>.

## Escopo
O que isto cobre.

### Fora de escopo
<!-- A linha mais importante. Liste o que explicitamente NÃO vamos fazer para o agente não sair divagando. -->
-

## Restrições
Regras que isto precisa obedecer — especialmente os **Princípios** em [AGENTS.md](../../../AGENTS.md) (o conjunto de regras que serve de gate). Liste aqui apenas as restrições específicas desta spec.
-

## Questões em aberto
<!-- O gate de clarificação: ambiguidades a resolver ANTES de `status: ready`. Só saia de draft quando isto estiver vazio (toda pergunta respondida). Ao responder uma → registre-a no Registro de decisões. -->
-

## Decisões de implementação
<!-- Módulos a construir/modificar e as interfaces deles, mudanças de schema, contratos de API, decisões arquiteturais, interações específicas. NÃO inclua caminhos de arquivo nem snippets de código — ficam obsoletos rápido. Exceção: um snippet de protótipo que codifica uma decisão melhor que a prosa (máquina de estados, reducer, schema, shape de tipo) — inline só a parte que decide e diga que veio de protótipo. -->
-

### Fluxo (Mermaid)
<!-- Escreva durante o refinamento em plan mode. Diagrame o caminho principal (flowchart/sequence/state). Obrigatório para qualquer coisa com fluxo não trivial. -->
```mermaid
flowchart TD
```

### Wireframe
<!-- Raro — só telas pesadas de UI. ASCII ou mermaid. Delete esta subseção se não for uma feature de UI. -->

## Decisões de teste
<!-- O que faz um bom teste aqui (testar só comportamento externo, não detalhe de implementação); quais módulos serão testados; prior art (testes parecidos que já existem no repo). -->
-

## Tarefas
<!-- Numere como T1, T2… para os Critérios de aceitação poderem apontar de volta para elas. Trabalho grande o bastante para precisar de fatias verticais + DAG de bloqueio → use a skill `to-tickets` para decompor em tickets. -->
- [ ] T1 ·
- [ ] T2 ·

## Critérios de aceitação
<!-- Verificáveis, não achismo: Dado/Quando/Então (ou uma condição de aprovação clara), derivados das Histórias de usuário. Cada um nomeia a(s) Tarefa(s) que o satisfazem, ex.: (T1, T3). Todo critério mapeia para ≥1 Tarefa; toda Tarefa é coberta por ≥1 critério. -->
- [ ] CA1 (T?) Dado … quando … então …
- [ ] CA2 (T?) Dado … quando … então …

## Plano de QA
<!-- Como QUEM TESTA confere a entrega — escrito antes de codar, pra o agente implementar contra ele. Descreve o que a pessoa vê e faz na superfície, nunca como o código foi escrito (sem caminho de arquivo, classe, função). Todo CA tem ≥1 cenário. [auto] = o agente prova sozinho (teste automatizado / comando reproduzível) e anexa a evidência; [manual] = QA humano. -->
**Superfície:** <tela | CLI | API | job> · **Ambiente:** <homologação | local> · **Perfil:** <tipo de usuário/credencial>

### Massa de dados
<!-- O que precisa existir ANTES de testar: registros e em qual estado. -->
-

### Cenários
<!-- `QA<n> [auto|manual] (CA<n>) <ação na superfície> → <resultado visível>`. Mensagem exibida citada "exata" (ainda não existe? marque "a confirmar" — o fechamento do QA reconcilia com o código). Inclua o caminho negativo visível (erro, vazio, sem permissão) quando a superfície o mostra. Dado que não aparece pra quem usa (histórico, log) → diga onde conferir. -->
- [ ] QA1 [manual] (CA1) … → …
- [ ] QA2 [auto] (CA2) … → …

### Regressão
<!-- Fluxo vizinho/antigo que não pode quebrar. Delete se não houver. -->
- [ ] QA3 [auto] … continua …

## Registro de decisões
<!-- Append-only — decisões LOCAIS a esta spec. Data + a escolha + o porquê. Decisões transversais vão para um ADR em docs/decisions/ (`to-doc adr`), não aqui. -->
- <YYYY-MM-DD>:

## Notas
<!-- Qualquer nota adicional sobre a feature. Opcional — delete se vazia. -->
