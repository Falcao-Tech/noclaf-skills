---
id: 42
name: whiteboard-video
description: Gera vídeos explicativos narrados em quadro branco, com caligrafia de mão, caneta que escreve e desenhos que se traçam acompanhando a fala. É leve para renderizar e usa voz gratuita em pt-BR (Edge TTS) com dicionário de pronúncia. Use sempre que o usuário pedir um vídeo para explicar ou ensinar algo, como fluxo, arquitetura, conceito, onboarding de projeto, comparação entre sistemas ou "me explica isso em vídeo", "vídeo didático", "vídeo em whiteboard", mesmo sem dizer "quadro branco". Não use para vídeo promocional, lançamento de produto, música, edição de filmagem ou motion graphics curto sem narração; esses ficam com a skill hyperframes.
---

# Vídeo explicativo em quadro branco

Vídeo simples que ensina. O valor está na explicação: um fio condutor concreto, uma ideia por cena e o desenho aparecendo enquanto a voz fala. Sem efeitos pesados, imagens geradas nem custo de voz.

Precisa de `uv`, `ffmpeg` e `node`. Referência num Mac: 6 minutos renderizaram em cerca de 3 minutos e ocuparam cerca de 19 MB.

## 1. Criar o projeto

```bash
cp -R ~/.claude/skills/whiteboard-video/assets/template <pasta-do-video>
```

Pergunte só o que mudaria o vídeo e não dá para deduzir: quem assiste, a duração e qual entendimento a pessoa precisa ter ao final. Sem resposta, use 3 minutos. Se pedirem para não perguntar, decida sozinho nas aprovações e liste as decisões na entrega.

## 2. Entender o assunto antes de escrever

Leia o código, os documentos ou as fontes antes do roteiro. Um vídeo didático ensina o erro com muita convicção, então separe o que foi verificado do que é plano ou hipótese, e mostre essa diferença na tela: traço cheio para o que existe, tracejado e post-it "planejado" ou "hipótese" para o resto. Cite a data do estado quando ele puder envelhecer.

## 3. Escrever o roteiro

Escreva em `narration.md`, com uma seção `## NN Título` por cena.

O que funcionou na prática:

- **Abra com algo concreto para seguir**, como "alguém manda 100 pesos", e não com o nome do assunto. Esse objeto atravessa o vídeo e dá sentido a cada etapa.
- **Dê uma analogia antes do nome técnico.** "Balcão e senha" antes de fila e consumidor.
- **Uma ideia por cena**, de 15 a 45 segundos. Em vídeo de até 1 minuto, 10 a 15 segundos.
- **Fale como quem explica ao colega:** frases curtas, sem listar nomes de função em voz alta. O nome exato vai num post-it, e a voz diz o que ele faz.
- **Compare com o que a pessoa conhece**, com uma cor para cada lado.
- **Inclua algo além do fluxo:** pegadinhas e armadilhas reais prendem a atenção e são o que mais se aproveita.
- **Feche no que fazer agora.**

Para a duração: cada cena soma cerca de 1,3 s de respiro e apagamento, e a voz rende cerca de 140 palavras por minuto. Palavras ≈ (duração − 1,3 s × cenas) ÷ 60 × 140. Em vídeo curto, baixe `tail` em `video.json` (padrão 0,5 s). Escreva números por extenso na narração ("cem reais") e deixe o símbolo para a tela.

Apresente ao usuário uma tabela com cena, tempo, o que aparece e por que está ali, e o texto para aprovar. Corrigir aqui é muito mais barato do que depois de gravar.

## 4. Cuidar da pronúncia

A voz lê mal siglas, inglês e nomes próprios. A solução é mandar para ela a grafia de como se fala, sem mudar o que aparece na tela.

1. Procure na narração siglas, termos em inglês, marcas, identificadores e palavras difíceis, mesmo em português.
2. `tools/pronuncia-base.json` já traz termos comuns. O que for do projeto vai em `pronuncia.json`, como `{"Valkey": "Válqui", "gRPC": "gê érre pê cê"}`.
3. Pergunte como o time pronuncia nomes próprios e de empresa. Não dá para deduzir, e errar o nome da empresa pega mal.
4. Gere o teste e peça para o usuário ouvir, porque você não consegue julgar áudio:

```bash
npm run tts -- --test idempotência
```

O teste inclui os termos do dicionário usados na narração e as palavras extras que você passar. A chave é o token sem pontuação, sem diferenciar maiúscula. Dicas: acento marca a sílaba forte (`Válqui`), um espaço separa as partes (`uébi rúqui`) e sigla soletrada vai por extenso (`ésse quê ésse`).

## 5. Gravar a voz

```bash
npm run tts
```

Grava só as cenas que mudaram. A voz e a velocidade ficam em `video.json`, e regravar não custa nada. Para listar vozes: `uvx --python 3.12 edge-tts --list-voices`.

O Edge TTS usa o "Ler em voz alta" do navegador, um acesso gratuito, mas não oficial: o texto vai para a Microsoft e o serviço pode parar. Avise o usuário se a narração tiver conteúdo sensível. Se o sistema bloquear a execução do `edge-tts`, passe o comando para o usuário rodar no terminal.

## 6. Animar

Leia `references/api.md` e escreva as cenas em `src/scenes.js`, uma função por seção da narração. Use `c.w("palavra")` para marcar o instante de cada desenho: é isso que faz o quadro acompanhar a fala e se ajustar se a voz mudar.

```bash
npm run build
```

O build falha se uma marcação não existir na narração ou estiver fora de ordem. Corrija a marcação, não a narração. `npm run build -- --words` lista cada palavra com o tempo absoluto no vídeo, útil para marcar e para conferir instantes.

Para escolha de estilo em vídeos longos, mostre uma cena pronta antes de animar o resto.

## 7. Conferir

```bash
npm run check
```

Avisos `nested_structure_needs_subcomposition` e `composition_file_too_large` são esperados: todas as cenas ficam em um arquivo de propósito, para o projeto continuar simples. Não divida o arquivo por causa deles. Erros, sim, precisam de correção.

Depois, olhe cada cena no seu estado final, com os tempos que o build imprime:

```bash
npm run snapshot -- --at <tempos>
```

Abra `review/shots/contact-sheet*.jpg`, e o PNG da cena quando o detalhe for pequeno. É aqui que aparecem texto sobreposto, objeto saindo da tela e área vazia. O `check` não pega boa parte disso. Se a cena usa `c.move`, capture também o meio do trajeto: o objeto pode cruzar um texto e isso não aparece no estado final.

## 8. Entregar

Mostre a prévia com `npm run preview`, peça para o usuário ouvir e só renderize depois de aprovar:

```bash
npm run render
```

O arquivo sai em `renders/video.mp4`, a 24 fps. Confirme a duração e que há áudio. Se você não assistiu ao vídeo inteiro ou não ouviu a voz, diga isso na entrega. Pare a prévia com `npx --yes hyperframes@0.8.84 preview --stop`.
