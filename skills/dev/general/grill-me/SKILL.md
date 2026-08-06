---
id: 13
title: grill-me
description: 'Entreviste o usuário sem dó sobre um plano, decisão ou ideia até chegar num entendimento compartilhado, resolvendo cada ramo da árvore de decisão em rodadas. Use quando o usuário quiser estressar o próprio raciocínio, ser sabatinado sobre o design dele, ou mencionar "grill me"'
model: opus
effort: high
---

Entreviste o usuário sem dó até vocês chegarem num entendimento compartilhado. Modele isso como uma **árvore de design**: toda decisão ramifica nas decisões que dependem dela.

Percorra a árvore em **rodadas**. O **frontier** é toda decisão cujos pré-requisitos já estão resolvidos — as perguntas que dá pra fazer _agora_, sem chutar respostas que você ainda não ouviu. Faça o frontier inteiro numa rodada só: numere cada pergunta e dê a sua resposta recomendada. Depois espere as respostas do usuário antes da próxima rodada.

Formate cada pergunta assim:

```
❓ **P1** - **<título da pergunta>**: <corpo da pergunta, pode ter vários parágrafos, incluindo alternativas>

➡️ <sua resposta recomendada>
```

Cada rodada de respostas remodela a árvore — decisões resolvidas empurram o frontier pra fora e desbloqueiam perguntas que dependiam delas. Recalcule o frontier e faça a próxima rodada. Pergunta cuja resposta depende de outra ainda aberta nesta rodada pertence a uma rodada _posterior_, não a esta.

Achar _fatos_ é trabalho seu, nunca do usuário. Quando uma pergunta do frontier precisar de um fato do ambiente (codebase, arquivos, ferramentas), dispare um sub-agente pra buscar — não pergunte nada que você mesmo poderia descobrir. Não trave nisso: uma exploração em andamento é um pré-requisito não resolvido, então só as perguntas que dependem dela esperam o sub-agente voltar — faça o resto do frontier agora. As _decisões_ são do usuário — coloque cada uma pra ele e espere.

A sessão acaba quando o frontier está vazio: todo ramo da árvore visitado, nada assumido em silêncio. Não implemente nada até o usuário confirmar que vocês chegaram num entendimento compartilhado.
