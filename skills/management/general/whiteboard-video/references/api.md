# API das cenas

Tela de 1920×1080. Mantenha o conteúdo entre x 100–1820 e y 30–1040; o título ocupa até y 140. `x` e `y` são o canto superior esquerdo, salvo `align`; em `c.text`, `y` é o topo da linha, então para alinhar com uma seta use cerca de `y_seta − 0,7 × size`. `t` é o instante em segundos dentro da cena.

Cada função recebe `t` e devolve quando termina, então dá para encadear:

```js
var t = c.w("porta");                 // momento da próxima palavra "porta" na fala
t = c.rect(1570, 380, 120, 180, { color: c.RED, width: 9 }, t);
c.text(1630, 590, "nova!", { size: 44, align: "center", color: c.RED }, t);
```

`c.w` anda só para a frente, e a busca é pelo começo da palavra, sem acento nem maiúscula. Chame na ordem da fala, com a palavra inteira: `c.w("paga")` também casa com "pagou". Se precisar de duas marcas da mesma palavra, chame duas vezes. Mantenha cada cena no formato `"01": function (c) {` e `c.w("...")` com aspas duplas no corpo da cena, porque é assim que o build confere as marcas.

## Funções

| Função | Uso |
|---|---|
| `c.title(texto, t)` | Título centralizado com sublinhado |
| `c.text(x, y, texto, {size, color, align, mark, dur}, t)` | Escreve uma linha. `align`: `"center"` ou `"right"`. `mark: true` passa marca-texto |
| `c.lines(x, y, [linhas], {size, gap, align, color}, t)` | Várias linhas, uma depois da outra |
| `c.rect(x, y, w, h, {color, width, a, dur}, t)` | Retângulo tremido. `a` é o tremor |
| `c.box(x, y, w, h, texto ou [linhas], {color, size}, t)` | Retângulo com rótulo centralizado |
| `c.line(x1, y1, x2, y2, {color, width}, t)` | Linha |
| `c.arrow(x1, y1, x2, y2, {color, width}, t)` | Seta |
| `c.dashed(x1, y1, x2, y2, {color, head: 0}, t)` | Tracejado, para o que é plano ou hipótese. `head: 0` tira a ponta |
| `c.circle(cx, cy, rx, ry, {color, width}, t)` | Elipse, para circular algo |
| `c.cross(x, y, w, h, {}, t)` | X vermelho sobre uma área |
| `c.check(x, y, {color}, t)` | Sinal de certo |
| `c.note(x, y, texto, {size, rot, hand, width}, t)` | Post-it. Letra de máquina para código; `hand: true` usa caligrafia |
| `c.divider(t, y2)` | Linha vertical no meio, até `y2` (padrão 1035). Encurte se houver texto embaixo |
| `c.token(x, y, rótulo, t, {scale, color})` | Objeto que anda: o fio condutor. Devolve o elemento. É o único que se move |
| `c.move(el, x, y, t, dur)` | Move o objeto |
| `c.draw(d, {color, width, under}, t)` | Caminho SVG livre |

Opções: `noPen: true` não move a caneta e vale nas funções de traço (`line`, `rect`, `arrow`, `dashed`, `circle`, `draw`). `dur` força a duração, exceto em `note` e `cross`. Texto sempre leva a caneta.

Cores: `c.INK`, `c.GREEN`, `c.RED`, `c.GRAY`. Use uma cor por "lado" da comparação, sempre a mesma no vídeo todo. Para mudar o fundo ou a paleta, altere `src/wb.js` e `STYLE` em `tools/build.py`.

## Armadilhas

- **Tamanho:** o texto fica ilegível abaixo de 38 px. Título 90, frases 50–70, legendas 40–46, código em post-it 26–30.
- **Largura:** Caveat tem cerca de 0,37 × `size` por caractere, e o post-it de código cerca de 0,6 × `size` por caractere + 40 px. Faça a conta antes de encaixar um texto numa caixa ou perto da margem.
- **`c.token`:** mede 360×180 × `scale`, e `x, y` é o canto superior esquerdo depois da escala. O rótulo tem 96 px × `scale`, então cabem cerca de 10 caracteres, e abaixo de `scale` 0,4 ele fica pequeno demais. É fácil sair da tela ou cobrir o rótulo de uma caixa: reserve uma faixa só para ele andar.
- **Caneta:** quando dois traços são simultâneos, ela segue só o primeiro. Use `noPen: true` nos pequenos para não pular pela tela.
- **Muitos traços pequenos** (como o desenho de um QR code): `dur: 0.05` e `noPen: true`.
- **Fim da cena:** o quadro é apagado nos últimos 0,6 s, menos na última cena. Escrever nesse trecho não aparece.
- **Determinismo:** nada de `Math.random` ou relógio. O tremor já vem de uma semente por cena.
