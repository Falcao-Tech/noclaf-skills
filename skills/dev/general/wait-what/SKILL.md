---
id: 31
name: wait-what
description: Para tudo. A última mensagem não passou — reexplique do zero, em português claro e com o vocabulário do domínio. Use quando o usuário disser "não entendi", "que?", "explica de novo", "wait what", ou sinalizar que se perdeu no que você acabou de falar.
disable-model-invocation: true
effort: medium
---

# Wait, what?

Peraí — não entendi onde você chegou. Não repita a mensagem anterior com outras palavras nem
recomece a tarefa: **reexplique** o que você acabou de dizer.

- Dê um pouco de contexto antes da conclusão: de onde você partiu, o que mudou no meio, onde
  você chegou.
- Escreva em **português técnico simplificado** (regras abaixo).
- Use o vocabulário do **glossário de domínio** do projeto. Sem glossário, use os nomes que já
  estão no código — nunca invente um sinônimo pra algo que já tem nome.

## Português técnico simplificado

Adaptação do ASD-STE100 pro pt-BR:

- **Uma ideia por frase.** Máximo ~20 palavras. Frase que precisa de vírgula pra respirar vira
  duas frases.
- **Voz ativa e presente.** "O hook bloqueia o commit", não "o commit é bloqueado pelo hook" nem
  "estaremos bloqueando".
- **Uma palavra, um sentido.** Escolheu "ticket"? É ticket até o fim — não vira "card", "item"
  nem "tarefa" no parágrafo seguinte.
- **Sem empilhar substantivo.** "config do worker de build", não "build worker config".
- **Sem gerundismo, sem eufemismo, sem hedge.** "Vai quebrar", não "poderia eventualmente vir a
  apresentar problemas".
- **Termo técnico só se for o nome real da coisa.** Se precisa de jargão, defina na primeira vez,
  em uma linha.
- **Passo a passo é lista numerada**, um passo por item, na ordem em que acontece.
- **Sem metáfora e sem analogia.** Descreva o que o código faz.

Se, ao reexplicar, você perceber que a mensagem anterior estava errada — não só mal escrita —
diga isso em uma frase e siga com a versão correta.
