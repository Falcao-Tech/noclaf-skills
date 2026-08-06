---
id: 30
name: to-briefing
description: Transforma uma decisão que você não consegue responder sozinho num briefing/questionário em Markdown pra outra pessoa preencher — cliente, PM, dev de outro time. Use quando o usuário pedir pra "montar um briefing pro fulano", "levantar requisitos com o cliente", "criar um questionário" ou disser que falta contexto que só outra pessoa tem.
disable-model-invocation: true
argument-hint: "[tema] [pra quem]"
model: sonnet
effort: medium
---

# To Briefing

Transforma algo que o usuário **não consegue responder sozinho** num **briefing** — um documento
Markdown que ele manda pra uma pessoa preencher de forma assíncrona, ou preenche junto numa
reunião. Quem recebe tem o conhecimento que falta pro usuário; o briefing extrai isso.

**Sabatine o envio, não o assunto.** Entreviste o usuário só sobre o **envio**, que ele sempre
sabe responder: pra quem vai e o que ele precisa de volta. As perguntas do documento então miram
o **gap** entre o que o destinatário sabe e o que o usuário precisa.

`$ARGUMENTS` traz o tema e, quando o usuário citar, o destinatário — use como resposta já dada e
**não repergunte** o que estiver lá. Vazio, ou só o tema: siga do passo 1.

## 1. Pra quem vai?

Pergunte, numa única troca, o papel do destinatário, a expertise dele e a relação com o usuário.
Isso define o tom do briefing e quanto contexto ele precisa carregar. Pronto quando você sabe
quem recebe e o que essa pessoa sabe que o usuário não sabe.

## 2. O que você precisa de volta?

Pergunte, numa única troca, quais decisões ou fatos específicos o usuário não consegue resolver
sozinho e precisa dessa pessoa. Pronto quando você tem uma lista concreta do que o usuário
precisa sair capaz de fazer ou decidir.

## 3. Escreva o briefing

Redija as perguntas mirando o gap dos passos 1–2, seguindo a estrutura abaixo. Escreva em
`to-briefing-<slug>.md` no diretório atual (slug a partir do tema) e reporte o caminho. Pronto
quando o arquivo existe e todo item que o usuário citou no passo 2 está coberto por uma pergunta.

## Estrutura do documento

Enquadre como um **briefing de descoberta**: o usuário não tem o contexto, o destinatário tem.
Ordene as perguntas da mais importante pra menos — assíncrono significa que talvez você só tenha
uma passada — e agrupe sob headings `##` por tema quando passar de meia dúzia. Use o template
abaixo.

<briefing-template>

# <Título do briefing>

**Objetivo:** por que este briefing existe e qual decisão depende dele.

**De:** <o usuário> — **Para:** <o destinatário> — **Como suas respostas serão usadas:** <onde vão parar>

## Contexto

Um parágrafo situando quem não estava na cabeça do usuário. O suficiente pra responder bem, não
uma página.

## Como responder

Prazo e esforço aproximado. Respostas parciais e "não sei" são úteis — sinalize o que estiver
incerto em vez de pular.

## <Tema>

Uma seção `##` por tema. Dentro dela, as perguntas, da mais importante pra menos. Cada pergunta é
uma ideia só — nunca composta — com um espaço de resposta logo abaixo, e uma linha de _por que
isso importa_ só onde a pergunta pode ser mal lida ou convidar a uma resposta jogada fora.

<exemplo-de-pergunta>
### Qual volume o sistema precisa aguentar no lançamento?

_Por que isso importa: define se provisionamos pra pico de tráfego agora ou deixamos pra depois._

>
</exemplo-de-pergunta>

## Mais alguma coisa?

Um catch-all no fim: tem algo que a gente não perguntou e deveria saber?

</briefing-template>
