# Referência de Padrões de Animation

Os valores, curvas e regras precisos por trás do review. Cite-os nos achados em vez de aproximar. Destilado da filosofia de engenharia de design de Emil Kowalski ([animations.dev](https://animations.dev/)).

## Deve animar? (tabela de frequência)

| Frequência | Decisão |
| --- | --- |
| 100+ vezes/dia (atalhos de teclado, toggle de command palette) | Sem animation. Nunca. |
| Dezenas de vezes/dia (hover effects, navegação em listas) | Remova ou reduza drasticamente |
| Ocasional (modals, drawers, toasts) | Animation padrão |
| Raro / primeira vez (onboarding, feedback, celebrações) | Pode adicionar encanto |

**Nunca anime ações iniciadas pelo teclado** — elas se repetem centenas de vezes por dia; a animation as faz parecer lentas e desconexas. (O Raycast não tem animation de abrir/fechar — correto para algo usado centenas de vezes por dia.)

Propósitos válidos para motion: spatial consistency, indicação de estado, explicação, feedback, evitar mudança abrupta. "Fica legal" em um elemento visto com frequência não é válido.

## Easing

Ordem de decisão:
- Entrando ou saindo → **`ease-out`** (começa rápido, parece responsivo)
- Movendo / fazendo morph na tela → **`ease-in-out`**
- Hover / mudança de cor → **`ease`**
- Motion constante (marquee, progresso) → **`linear`**
- Padrão → **`ease-out`**

**Nunca `ease-in` na UI.** Ele começa devagar, atrasando exatamente o momento em que o usuário está observando. `ease-out` a 200ms *parece* mais rápido que `ease-in` a 200ms.

Os easings nativos do CSS são fracos demais. Use curvas personalizadas fortes:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve (Ionic) */
```

Encontre curvas em [easing.dev](https://easing.dev/) ou [easings.co](https://easings.co/) — não faça na mão do zero.

## Duration

| Elemento | Duration |
| --- | --- |
| Feedback de press de botão | 100–160ms |
| Tooltips, popovers pequenos | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing / explicativo | Pode ser mais longo |

**Regra: animations de UI ficam abaixo de 300ms.** Um dropdown de 180ms parece mais responsivo que um de 400ms. Spinners mais rápidos fazem o carregamento parecer mais rápido (mesmo tempo real). Tooltips instantâneos depois do primeiro (pulando delay + animation) fazem uma toolbar parecer mais rápida.

## Física

- **Nunca `scale(0)`.** Comece de `scale(0.9–0.97)` + `opacity: 0`. Nada no mundo real aparece do nada.
- **Popovers origin-aware.** Faça scale a partir do gatilho, não do centro:
  ```css
  .popover { transform-origin: var(--radix-popover-content-transform-origin); } /* Radix */
  .popover { transform-origin: var(--transform-origin); }                       /* Base UI */
  ```
  **Modals são exceção** — aparecem centralizados no viewport, mantenha `transform-origin: center`.
- **Feedback de press de botão.** `transform: scale(0.97)` no `:active`, `transition: transform 160ms ease-out`. Sutil (0.95–0.98). Aplica-se a qualquer elemento pressionável.

## Springs

Parecem naturais porque simulam física; sem duration fixa — elas se estabilizam com base em parâmetros. Use para: drag com momentum, elementos "vivos" (Dynamic Island), gestures interruptíveis, mouse-tracking decorativo.

```js
// Apple-style (easier to reason about) — recommended
{ type: "spring", duration: 0.5, bounce: 0.2 }

// Traditional physics (more control)
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }
```

Mantenha o bounce sutil (0.1–0.3); evite bounce na maior parte da UI — reserve para drag-to-dismiss e interações lúdicas. Springs mantêm a velocity quando interrompidas (keyframes recomeçam do zero), então são ideais para gestures que os usuários podem reverter no meio do motion.

Interações de mouse: interpole com `useSpring` em vez de amarrar o valor diretamente à posição do mouse (direto = artificial, sem momentum). Só faça isso quando o motion for decorativo.

## Interruptibilidade

CSS **transitions** podem ser interrompidas e re-orientadas no meio da animation; **keyframes** recomeçam do zero. Para qualquer coisa disparada rapidamente (toasts sendo adicionados, toggles), transitions são mais suaves.

```css
/* Interruptible — good for dynamic UI */
.toast { transition: transform 400ms ease; }

/* Not interruptible — avoid for dynamic UI */
@keyframes slideIn { from { transform: translateY(100%); } to { transform: translateY(0); } }
```

Use `@starting-style` para entrada sem JS:

```css
.toast {
  opacity: 1; transform: translateY(0);
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

Fallback legado: `useEffect(() => setMounted(true), [])` + atributo `data-mounted`.

## Timing assimétrico

Lento onde o usuário está decidindo, rápido onde o sistema responde.

```css
.overlay { transition: clip-path 200ms ease-out; }            /* release: fast */
.button:active .overlay { transition: clip-path 2s linear; }  /* press: slow, deliberate */
```

## Performance

- **Anime apenas `transform` e `opacity`** — eles pulam layout/paint e rodam na GPU. `padding`/`margin`/`height`/`width`/`top`/`left` disparam os três passos de renderização.
- **Não dirija transforms de filhos por uma variável CSS no pai** — isso recalcula os estilos de todos os filhos. Defina `transform` diretamente no elemento.
  ```js
  element.style.setProperty('--swipe-amount', `${d}px`); // bad: recalc on all children
  element.style.transform = `translateY(${d}px)`;        // good: only this element
  ```
- **Os atalhos do Framer Motion NÃO são acelerados por hardware.** `x`/`y`/`scale` rodam na main thread via rAF e perdem frames sob carga. Use a string transform completa:
  ```jsx
  <motion.div animate={{ x: 100 }} />                          // drops frames under load
  <motion.div animate={{ transform: "translateX(100px)" }} />  // hardware accelerated
  ```
- **Animations em CSS superam JS sob carga** — elas rodam fora da main thread; animations baseadas em rAF travam enquanto o browser carrega/executa scripts/pinta. Use CSS para motion predeterminado, JS para dinâmico/interruptível.
- **WAAPI** dá o controle do JS com a performance do CSS (acelerado por hardware, interruptível, sem biblioteca):
  ```js
  element.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
    { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' });
  ```

## Transforms e clip-path

- **Porcentagens de `translate`** são relativas ao próprio tamanho do elemento — `translateY(100%)` move pela altura do elemento independentemente das dimensões (é assim que Sonner/Vaul posicionam toasts/drawers). Prefira em vez de px hardcoded.
- **`scale()` também escala os filhos** (fonte, ícones, conteúdo) — um recurso útil para feedback de press.
- **3D**: `rotateX/Y` + `transform-style: preserve-3d` para profundidade/orbit/flip sem JS.
- **`clip-path: inset(t r b l)`** é uma ferramenta poderosa de animation: cada valor avança a partir daquele lado. Usos: reveal-on-scroll (`inset(0 0 100% 0)` → `inset(0 0 0 0)`), overlay de hold-to-delete, transitions de cor de tab sem emenda (duplique + recorte a cópia ativa), sliders de comparação.

## Gestures e drag

- **Dispensa por momentum**: não exija cruzar um limiar de distância — calcule a velocity (`Math.abs(distance)/elapsedMs`); dispense se `> ~0.11`. Um flick deve bastar.
- **Damping nos limites**: arrastar além de uma borda natural move menos quanto mais longe você vai (coisas reais desaceleram antes de parar).
- **Pointer capture** assim que o drag começa, para que continue quando o pointer sai dos limites.
- **Proteção multi-touch**: ignore pontos de toque extras depois que o drag começa (`if (isDragging) return`) — evita saltos.
- **Fricção em vez de paradas bruscas** — permita over-drag com resistência crescente em vez de uma parede invisível.

## Mascarando crossfades imperfeitos

Quando um crossfade mostra dois estados sobrepostos apesar de ajustar easing/duration, adicione um `filter: blur(2px)` sutil durante a transition para fundi-los em uma única transformação percebida. Mantenha o blur < 20px (blur pesado é caro, especialmente no Safari).

## Stagger

Faça stagger nas entradas de grupos; 30–80ms entre itens. Delays maiores parecem lentos. Stagger é decorativo — nunca bloqueie a interação enquanto ele roda.

```css
.item { opacity: 0; transform: translateY(8px); animation: fadeIn 300ms ease-out forwards; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

## Acessibilidade

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop transform-based motion */
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* gate hover motion — touch fires false hovers on tap */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion significa menos animations e mais suaves, não zero — mantenha transitions que ajudam na compreensão, remova mudanças de movimento/posição.

## Debugging (recomende em reviews quando o feel estiver incerto)

- **Slow motion**: aumente a duration 2–5× ou use o inspetor de animation do DevTools. Verifique se as cores fazem crossfade de forma limpa, se o easing não para abruptamente, se o `transform-origin` está certo e se as propriedades coordenadas permanecem em sincronia.
- **Frame a frame**: o painel Animations do Chrome DevTools revela desvios de timing entre propriedades coordenadas.
- **Dispositivos reais** para gestures (drawers, swipe) — conecte um celular, acesse o dev server pelo IP, use o Safari remote devtools.
- **Olhos descansados no dia seguinte** — imperfeições invisíveis durante o desenvolvimento aparecem depois.

## Coesão

Combine o motion com a personalidade do componente: algo lúdico pode ser mais bouncy; um dashboard profissional deve ser nítido e rápido. O Sonner parece certo em parte porque easing, duration, design e até o nome estão em harmonia — um pouco mais lento, `ease` em vez de `ease-out`, para parecer elegante. Opacity + height em listas entrando/saindo é tentativa e erro; não há fórmula — ajuste até parecer certo.
