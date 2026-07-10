---
id: 7
name: animation-vocabulary
description: Glossário de busca reversa que transforma uma descrição vaga de uma animation ou motion effect da web no termo exato ("aquela coisa saltitante quando um popover abre" → Pop in; "o scroll rubber-band do iOS" → Rubber-banding). Use quando o usuário perguntar "como se chama quando…", ou descrever um motion effect sem saber o nome e quiser a palavra certa para instruir uma IA ou um designer. Para nomear um efeito, não para projetar ou construir um.
---

# Vocabulário de Animation

Transforme uma descrição vaga de um motion ou efeito no termo preciso, para que o usuário saiba o que pedir.

## Início Rápido

O usuário descreve um efeito de forma vaga. Você retorna o(s) termo(s) correspondente(s) neste formato:

```
**Stagger** — Animar vários itens um após o outro com um pequeno delay entre cada um, criando uma cascata.
```

Se vários termos servirem, liste primeiro o que melhor se encaixa, depois 1–2 alternativas com uma nota de uma linha sobre como diferem.

## Instruções

1. **Leia a intenção, não as palavras-chave.** Os usuários descrevem o que *veem* ou *sentem* ("saltitante", "desliza para fora", "se desenha sozinho"), não o nome técnico. Mapeie a sensação para o glossário abaixo.
2. **Cite o glossário literalmente.** Suas descrições são a referência — use-as como estão, não parafraseie.
3. **Desambigue termos próximos.** Quando dois competem (*Clip-path* vs *Mask*, *Pop in* vs *Bounce*, *Shared element transition* vs *Layout animation*), contraste-os para que o usuário possa escolher.
4. **Quando nada corresponde exatamente,** nomeie o termo mais próximo e diga claramente que é uma aproximação, ou descreva o efeito com o vocabulário do glossário (ex.: "isso é um *stagger* de entradas *scale-in*").
5. **Fique dentro deste glossário.** Se um termo realmente não estiver aqui, diga isso em vez de inventar um — embora você possa explicar o conceito usando estas palavras.
6. **Seja conciso.** Uma pergunta sobre nomes quer um nome, não um ensaio. Comece pelo termo; expanda só se pedirem.

## Exemplos

**Exemplo 1 — baseado na sensação**
Usuário: "Como se chama quando um popover parece crescer a partir do botão que você clicou em vez de a partir do meio dele?"
Saída:
```
**Origin-aware animation** — Um elemento anima a partir de seu gatilho, como um popover crescendo a partir do botão que o abriu em vez de a partir do próprio centro, que é o padrão no CSS.
```

**Exemplo 2 — desambiguação**
Usuário: "Aquela coisa em que uma imagem se transforma em outra imagem."
Saída:
```
**Morph** — Uma forma se transforma suavemente em outra, ex.: Dynamic Island.

Alternativas próximas:
- **Crossfade** — se elas simplesmente fazem fade uma sobre a outra no mesmo lugar.
- **Shared element transition** — se um elemento se desloca e se transforma de uma posição para outra.
```

**Exemplo 3 — sensação de física**
Usuário: "Aquele scroll do iOS em que ele resiste e volta de repente quando você puxa demais."
Saída:
```
**Rubber-banding** — Resistência e retorno elástico quando você arrasta além de um limite (a sensação de overscroll do iOS).
```

## Glossário

_Um retrato curado que espelha a página `/vocabulary` do projeto; mantenha as duas em sincronia quando qualquer uma mudar._

### Entradas e Saídas — como os elementos aparecem e desaparecem
- **Fade in / Fade out** — O elemento aparece ou desaparece mudando a opacity.
- **Slide in** — O elemento entra deslizando de fora da tela (esquerda, direita, topo ou base).
- **Scale in** — O elemento cresce de um tamanho menor até o tamanho completo ao aparecer, muitas vezes combinado com um fade.
- **Pop in** — O elemento aparece com um leve overshoot, como se quicasse até se encaixar.
- **Reveal** — O conteúdo é descoberto gradualmente, geralmente animando um clip-path ou mask.
- **Enter / Exit** — A animation que um elemento executa quando é adicionado ou removido da tela.

### Sequenciamento e Timing — coordenando múltiplos elementos ou momentos
- **Keyframes** — Pontos definidos em uma animation (0%, 50%, 100%) cujos intervalos o browser preenche.
- **Interpolation / Tween** — Gerar todos os frames intermediários entre um valor inicial e um final, para que o motion seja contínuo.
- **Stagger** — Animar vários itens um após o outro com um pequeno delay entre cada um, criando uma cascata.
- **Orchestration** — Sincronizar deliberadamente várias animations para que pareçam um único motion coordenado.
- **Delay** — Tempo antes de uma animation começar.
- **Duration** — Quanto tempo uma animation leva.
- **Fill mode** — Se um elemento mantém os estilos do primeiro ou do último frame antes da animation começar ou depois dela terminar (ex.: forwards).
- **Stepped animation** — Uma animation dividida em passos discretos, como um cronômetro de contagem regressiva.

### Movimento e Transforms — mudando a posição, o tamanho ou o ângulo de um elemento
- **Translate** — Mover um elemento ao longo do eixo X ou Y.
- **Scale** — Deixar um elemento maior ou menor.
- **Rotate** — Girar um elemento em torno de um ponto.
- **Skew** — Inclinar um elemento ao longo do eixo X ou Y, distorcendo-o para fora de sua forma retangular.
- **3D tilt / Flip** — Rotacionar no espaço 3D (rotateX / rotateY) para adicionar profundidade.
- **Perspective** — Quão forte o efeito 3D parece — um valor menor exagera a profundidade, como se o observador estivesse mais perto.
- **Transform origin** — O ponto de ancoragem a partir do qual um scale ou uma rotação cresce ou gira.
- **Origin-aware animation** — Um elemento anima a partir de seu gatilho, como um popover crescendo a partir do botão que o abriu em vez de a partir do próprio centro, que é o padrão no CSS.

### Transitions Entre Estados — conectando um estado, uma view ou um elemento a outro
- **Crossfade** — Um elemento faz fade out enquanto outro faz fade in, no mesmo lugar.
- **Continuity transition** — Uma mudança que mantém o usuário orientado conectando visualmente o antes e o depois. Por exemplo, aumentar e diminuir o mesmo retângulo.
- **Morph** — Uma forma se transforma suavemente em outra, ex.: Dynamic Island.
- **Shared element transition** — Um elemento se desloca e se transforma de uma posição para outra, como uma miniatura que se expande em um card.
- **Layout animation** — Quando o tamanho ou a posição de um elemento muda, ele anima até o novo lugar em vez de saltar.
- **Accordion / Collapse** — Uma seção expande e recolhe a altura suavemente para mostrar ou ocultar conteúdo.
- **Direction-aware transition** — O conteúdo desliza para um lado ao avançar e para o lado oposto ao voltar, dando à navegação um senso de direção.

### Scroll — motion atrelado ao scroll ou à navegação entre views
- **Scroll reveal** — Elementos fazem fade ou slide até se posicionar conforme entram no viewport.
- **Scroll-driven animation** — Uma animation cujo progresso está atrelado diretamente à posição do scroll.
- **Parallax** — Fundo e primeiro plano se movem em velocidades diferentes durante o scroll, criando profundidade.
- **Page transition** — Uma animation que roda ao navegar de uma página ou rota para outra.
- **View transition** — O browser faz morph entre dois estados ou páginas, conectando elementos compartilhados.

### Feedback e Interação — respondendo às ações do usuário
- **Hover effect** — Mudança visual quando o cursor passa sobre um elemento.
- **Press / Tap feedback** — Um leve scale-down quando um elemento é clicado, para que pareça físico.
- **Hold to confirm** — Um efeito de progresso que se preenche enquanto o usuário segura um botão.
- **Drag** — Mover um elemento agarrando-o, muitas vezes com momentum ao soltar.
- **Drag to reorder** — Arrastar itens em uma lista para reorganizá-los, enquanto os outros se deslocam para abrir espaço.
- **Swipe to dismiss** — Arrastar um elemento para fora da tela para fechá-lo, como um drawer ou toast.
- **Rubber-banding** — Resistência e retorno elástico quando você arrasta além de um limite (a sensação de overscroll do iOS).
- **Shake / Wiggle** — Um tremor rápido de um lado para o outro sinalizando um erro ou uma entrada rejeitada.
- **Ripple** — Um círculo que se expande a partir do ponto do toque, confirmando o clique.

### Easing — como a velocidade muda ao longo de uma animation
- **Easing** — A taxa com que uma animation acelera ou desacelera.
- **Ease-out** — Começa rápido, termina devagar. O padrão para a maior parte da UI e para qualquer coisa que responde ao usuário.
- **Ease-in** — Começa devagar, termina rápido. Geralmente evitado; pode parecer arrastado.
- **Ease-in-out** — Devagar, rápido, devagar. Bom para elementos que já estão na tela se movendo de A para B.
- **Linear** — Velocidade constante. Evite na UI; reserve para spinners ou marquees.
- **Cubic-bezier** — Uma curva de easing personalizada que você define para controle preciso.
- **Asymmetric easing** — Uma curva que acelera e desacelera em taxas diferentes. Parece mais viva do que uma simétrica.

### Spring Animations — motion baseado em física como alternativa ao easing de duration fixa
- **Spring** — Motion movido por física (tension, mass, damping) em vez de uma duration fixa.
- **Stiffness / Tension** — Quão forte a spring puxa em direção ao alvo. Mais alto parece mais ágil.
- **Damping** — Quão rápido uma spring se estabiliza. Menos damping significa mais bounce e oscilação.
- **Mass** — Quão pesado o elemento animado parece. Mais mass o torna mais lento e mais arrastado.
- **Bounce** — Uma spring que ultrapassa e se estabiliza, adicionando um toque lúdico.
- **Perceptual duration** — Por quanto tempo uma spring parece concluída, mesmo que continue se micro-ajustando por baixo.
- **Momentum** — Motion que carrega velocity, especialmente depois de um drag ou de uma interrupção.
- **Velocity** — Quão rápido e em qual direção um elemento está se movendo. Uma spring o carrega para a próxima animation quando interrompida, então um elemento lançado com um flick mantém sua velocidade.
- **Interruptible animation** — Uma animation que pode ser redirecionada suavemente no meio do caminho em vez de terminar primeiro.

### Looping e Motion Ambiente — animations que rodam sozinhas
- **Marquee** — Texto ou conteúdo que rola continuamente em loop.
- **Loop** — Uma animation que se repete, um número definido de vezes ou infinitamente.
- **Alternate (yoyo)** — Um loop que roda para frente e depois inverte a cada iteração, em vez de saltar de volta para o início.
- **Orbit** — Um elemento circulando ao redor de outro em um caminho contínuo.
- **Pulse** — Uma mudança suave e repetida de scale ou opacity para chamar atenção.
- **Float** — Uma deriva suave e contínua para cima e para baixo que faz um elemento estático parecer vivo e sem peso.
- **Idle animation** — Motion sutil que roda enquanto um elemento está apenas parado ali, esperando por interação.

### Acabamento e Efeitos — os pequenos toques que separam o bom do excelente
- **Blur** — Um filtro de blur usado para suavizar um elemento ou mascarar pequenas imperfeições.
- **Clip-path** — Recortar um elemento em uma forma, usado para reveals, masks e sliders de antes/depois.
- **Mask** — Ocultar ou revelar partes de um elemento usando uma forma ou gradiente — como clip-path, mas com bordas suaves que podem fazer fade.
- **Before / after slider** — Um divisor arrastável que faz wipe entre duas imagens sobrepostas para compará-las.
- **Line drawing** — Um path SVG que se desenha sozinho, como uma caneta invisível traçando-o.
- **Text morph** — Texto que anima caractere por caractere quando muda, chamando atenção para o novo valor.
- **Skeleton / Shimmer** — Um placeholder com um brilho em movimento exibido enquanto o conteúdo carrega.
- **Number ticker** — Dígitos rolando ou contando até um valor.
- **Tabular numbers** — Dígitos de largura fixa para que os números não fiquem se deslocando conforme mudam. Essencial para tickers, timers e contadores.
- **Typewriter** — Texto surgindo um caractere de cada vez, como se estivesse sendo digitado.

### Performance — o que mantém o motion suave em vez de travado
- **Frame rate (FPS)** — Frames desenhados por segundo. 60fps é a base para motion suave; 120fps em telas mais novas.
- **Jank** — Travamento visível quando o browser perde frames por não conseguir acompanhar a animation.
- **Dropped frame** — Um frame que o browser não conseguiu desenhar no prazo, causando um pequeno soluço no motion.
- **Compositing** — Deixar a GPU mover ou fazer fade de um elemento em sua própria layer sem refazer layout ou paint.
- **will-change** — Uma dica de CSS de que um elemento está prestes a animar, para que o browser possa promovê-lo à própria layer com antecedência.
- **Layout thrashing** — Animar propriedades como width, height, top ou left que forçam o browser a recalcular o layout a cada frame, causando jank.

### Princípios que Você Deve Conhecer — conceitos que orientam quando e como animar
- **Purposeful animation** — O motion deve cumprir uma função — orientar, dar feedback, mostrar relações — não apenas decorar.
- **Anticipation** — Um pequeno impulso na direção oposta antes de um movimento, insinuando o que está prestes a acontecer.
- **Follow-through** — Partes de um elemento continuam se movendo e se acomodam um pouco depois que o motion principal para, adicionando peso.
- **Squash & stretch** — Deformar um elemento conforme ele se move para transmitir peso, velocidade e flexibilidade.
- **Perceived performance** — A animation certa faz uma interface parecer mais rápida, mesmo quando não é.
- **Frequency of use** — Quanto mais vezes um usuário vê uma animation, mais curta e sutil ela deve ser.
- **Spatial consistency** — Animar de modo que um elemento mantenha sua identidade e posição entre estados, para que os usuários nunca percam de vista para onde as coisas foram.
- **Hardware acceleration** — Animar transform e opacity permite que a GPU mantenha o motion suave.
- **Reduced motion** — Respeitar a configuração prefers-reduced-motion do usuário atenuando ou removendo o motion.
