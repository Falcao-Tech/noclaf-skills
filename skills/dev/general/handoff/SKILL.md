---
id: 14
name: handoff
description: Compacta a conversa atual em um documento de handoff para outro agente dar continuidade.
effort: low
argument-hint: "Para que a próxima sessão vai ser usada?"
---

Escreva um documento de handoff resumindo a conversa atual para que um novo agente consiga continuar o trabalho. Salve no diretório temporário do SO do usuário - não no workspace atual.

Inclua uma seção "skills sugeridas" no documento, sugerindo skills que o agente deve invocar.

Não duplique conteúdo já capturado em outros artefatos (PRDs, planos, ADRs, issues, commits, diffs). Referencie-os por caminho ou URL em vez disso.

Oculte qualquer informação sensível, como API keys, senhas ou dados pessoais identificáveis.

Se o usuário passou argumentos, trate-os como uma descrição do foco da próxima sessão e adapte o documento de acordo.
