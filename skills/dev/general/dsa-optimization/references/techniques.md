# Técnicas de otimização de algoritmos

Referências: CLRS (teoria e invariantes) e *Competitive Programmer's Handbook* (CPHB, Antti Laaksonen) para os padrões práticos.

Índice: [Padrões práticos (CPHB)](#padrões-práticos-competitive-programmers-handbook-laaksonen) · [Prefix sums](#prefix-sums) · [Difference array](#difference-array) · [Two pointers](#two-pointers) · [Sliding window](#sliding-window) · [Busca binária](#busca-binária) · [Ordenação e seleção](#ordenação-e-seleção-clrs-cap-79) · [Sweep line](#sweep-line-e-intervalos) · [Coordinate compression](#coordinate-compression) · [DP](#programação-dinâmica-clrs-cap-15) · [Greedy](#greedy-clrs-cap-16) · [Análise amortizada](#análise-amortizada-clrs-cap-17) · [Strings e hashing](#strings-e-hashing-clrs-cap-32) · [Sqrt e Mo's](#sqrt-decomposition-e-mos-algorithm) · [Bits](#bits) · [Meet in the middle](#meet-in-the-middle) · [Constante](#otimização-de-constante-depois-do-big-o) · [Aritmética](#aritmética-overflow-e-módulo)

---

## Prefix sums

`P[0] = 0`, `P[i+1] = P[i] + a[i]`, e `sum(a[l..r]) = P[r+1] − P[l]` (inclusivo). Construção O(n), query O(1). Só serve para arrays estáticos; com updates, use Fenwick.

**Convenção que evita off-by-one:** `P` tem tamanho **n+1** e `P[i]` = soma dos **i primeiros** elementos. Então a soma de `a[l:r]` (semiaberto) é `P[r] − P[l]`.

```python
from itertools import accumulate
P = [0, *accumulate(a)]          # len(P) == len(a) + 1
```

**Contar subarrays com soma = k** (funciona com negativos, ao contrário de sliding window):
```python
from collections import Counter
def count_sum_k(a, k):
    seen = Counter({0: 1})       # o prefixo vazio: SEM ISSO perde subarrays que começam no índice 0
    s = ans = 0
    for x in a:
        s += x
        ans += seen[s - k]       # consulta ANTES de registrar o prefixo atual (senão conta subarray vazio com k=0)
        seen[s] += 1
    return ans
```
Variantes: soma divisível por k (use `s % k` como chave e normalize negativos em C/Java); maior subarray com soma k (guarde o **primeiro** índice de cada prefixo); subarray com mesmo número de 0s e 1s (troque 0 por −1).

**Prefix XOR:** `xor(a[l..r]) = X[r+1] ^ X[l]`. **Prefix de contagem por categoria:** `cnt[c][i]`.

**2D** (tabela `(R+1)×(C+1)`, borda de zeros):
```python
P = [[0] * (C + 1) for _ in range(R + 1)]
for i in range(R):
    for j in range(C):
        P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] - P[i][j]   # subtrai a sobreposição UMA vez

def rect(r1, c1, r2, c2):        # soma de a[r1..r2][c1..c2] inclusivo
    return P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]  # inclusão-exclusão: 4 termos
```

**Bugs:** tabela sem a borda extra (índice −1 lê o último elemento em Python, silenciosamente); esquecer o termo `+P[r1][c1]` (subtraído duas vezes); misturar base 0 e base 1; overflow da soma em `int32`; no módulo, `(P[r] - P[l]) % M` negativo em C/Java.

---

## Difference array

Para muitos updates "some v em `a[l..r]`" e leitura só no fim: O(1) por update, O(n) para reconstruir.

```python
d = [0] * (n + 1)                # +1 para o r+1 não sair do array
for l, r, v in updates:          # inclusivo
    d[l] += v
    d[r + 1] -= v
a = list(accumulate(d))[:n]
```
**2D:** `d[r1][c1] += v; d[r1][c2+1] -= v; d[r2+1][c1] -= v; d[r2+1][c2+1] += v`, depois prefix sum 2D. **Ordem superior:** somar uma progressão aritmética em um intervalo usa diferenças de segunda ordem (aplique prefix sum duas vezes).

Updates e queries intercalados → BIT sobre o difference array (update de intervalo, query pontual).

---

## Two pointers

**Pré-condição:** existe monotonicidade. Quando um ponteiro avança, o outro nunca precisa voltar. Casos típicos: array ordenado (par/trio com soma alvo), merge de duas listas ordenadas, remoção in-place, partição (Dutch flag), lento/rápido em listas.

```python
def pair_sum_sorted(a, target):  # a ordenado
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target: return i, j
        if s < target: i += 1
        else: j -= 1
    return None
```
**3-sum** em O(n²): ordene, fixe `i`, use two pointers no resto e **pule duplicatas** tanto em `i` quanto depois de achar um par (senão saem triplas repetidas).

---

## Sliding window

**Janela variável**: maior ou menor subarray contíguo que satisfaz uma condição **monotônica** (se a janela [l, r] é válida, toda subjanela dela também é, ou o inverso).

```python
def longest_at_most_k_distinct(s, k):
    cnt, l, best = {}, 0, 0
    for r, c in enumerate(s):
        cnt[c] = cnt.get(c, 0) + 1
        while len(cnt) > k:              # encolhe ATÉ voltar a ser válida
            cnt[s[l]] -= 1
            if cnt[s[l]] == 0: del cnt[s[l]]   # sem isso, len(cnt) nunca diminui
            l += 1
        best = max(best, r - l + 1)      # atualiza depois de ficar válida
    return best
```

- **"Exatamente K"** = `atMost(K) − atMost(K−1)`.
- **Soma com negativos quebra a sliding window** (a monotonicidade some). Use prefix sum + hash map, ou prefix sum + monotonic deque (menor subarray com soma ≥ K).
- **Janela fixa:** some o que entra e subtraia o que sai. Máximo e mínimo exigem monotonic deque (`linear.md`).

**Bugs:** usar `if` em vez de `while` para encolher; atualizar a resposta antes de a janela voltar a ser válida; não remover do mapa as chaves com contagem 0; `r - l` em vez de `r - l + 1`.

---

## Busca binária

**Template único** (half-open, devolve o primeiro índice onde o predicado é verdadeiro):
```python
def first_true(lo, hi, pred):
    """Menor x em [lo, hi) com pred(x) True, assumindo pred monotônico F...F T...T. Retorna hi se nenhum."""
    while lo < hi:
        mid = lo + (hi - lo) // 2        # em C/Java: evita overflow de lo+hi
        if pred(mid): hi = mid
        else: lo = mid + 1
    return lo
# lower_bound(a, x) = first_true(0, len(a), lambda i: a[i] >= x)
# upper_bound(a, x) = first_true(0, len(a), lambda i: a[i] >  x)
# quantidade de x em a = upper_bound − lower_bound
```

**Invariante:** tudo em `[orig_lo, lo)` é False e tudo em `[hi, orig_hi)` é True. O laço termina com `lo == hi`.

**Busca binária na resposta:** "qual o menor capacidade, tempo ou velocidade tal que é possível…". Escreva `possivel(x)` em O(n), confira que é monotônico e use `first_true` no intervalo das respostas. Custo total O(n log(intervalo)).

**Bugs clássicos:**
- **Laço infinito:** com `lo = mid` (procurando o último True), `mid` precisa arredondar **para cima** (`lo + (hi - lo + 1) // 2`). Prefira converter para "primeiro True do predicado negado".
- `hi` inclusivo misturado com laço `lo < hi` (ou o contrário).
- `(lo + hi) / 2` estoura em `int32` (bug real na JDK por quase uma década).
- Com negativos em C/Java, `/` trunca para zero e `(lo + hi) / 2` com `lo = −3`, `hi = −2` dá −2, quebrando o arredondamento para baixo. Use `lo + (hi - lo) / 2` ou shift (`>> 1`).
- Predicado não monotônico: a busca devolve lixo sem erro. Teste o predicado em toda a faixa com n pequeno.
- **Reais:** itere um número fixo de vezes (60–100) em vez de `while hi - lo > eps` (pode não terminar por precisão).
- Esquecer o caso "nenhum satisfaz" (retorno = `hi`).

**Bibliotecas:** Python `bisect_left`/`bisect_right` (com `key=` desde 3.10); C++ `lower_bound`/`upper_bound`/`partition_point`. Em `std::set`/`std::map`, use o **membro** `s.lower_bound(x)` (O(log n)); `std::lower_bound(s.begin(), s.end(), x)` em set é O(n), porque o iterador não é de acesso aleatório. Java: `Collections.binarySearch` devolve `-(ponto de inserção) - 1` quando não acha.

**Busca ternária** (função unimodal): em inteiros, pare quando `hi − lo < 3` e varra o resto. Com platôs (valores iguais), ela falha; use a busca binária sobre a "derivada" `f(m) < f(m+1)`.

---

## Ordenação e seleção (CLRS cap. 7–9)

- Ordenação por comparação tem limite inferior **Ω(n log n)** (CLRS 8.1). Para passar disso, é preciso explorar a estrutura das chaves: **counting sort** O(n + k) para chaves inteiras pequenas, **radix sort** O(d·(n + b)), **bucket sort** para distribuição uniforme.
- **Quicksort** tem pior caso O(n²) com pivô fixo e entrada ordenada ou adversarial. Use pivô aleatório (CLRS 7.3) e particionamento de 3 vias quando há muitas duplicatas. Na prática, use o sort da biblioteca (introsort, Timsort, pdqsort).
- **Seleção do k-ésimo** em O(n) esperado com quickselect (CLRS 9.2), ou O(n) de pior caso com mediana das medianas (CLRS 9.3). `std::nth_element`; em Python, `heapq.nsmallest(k, a)` é O(n log k).
- **Estabilidade:** Timsort (Python, objetos em Java) e `std::stable_sort` são estáveis; `std::sort` e `Arrays.sort(int[])` não são. Ordenar por múltiplas chaves com ordenações estáveis sucessivas exige ir da chave **menos** para a **mais** significativa.
- **Ordenar uma vez, consultar muitas:** sort O(n log n) + Q buscas binárias O(Q log n) costuma ganhar de Q varreduras O(Q·n).
- **Bugs:** comparator que não é ordem fraca estrita (`<=`) gera UB ou crash em `std::sort`; comparator `a − b` estoura (use `Integer.compare`); ordenar strings numéricas lexicograficamente (`"10" < "9"`), incluindo o `sort()` padrão do JS.

---

## Sweep line e intervalos

Transforme intervalos em **eventos** `(x, tipo)`, ordene e percorra mantendo o estado (contador, heap, set ordenado).

```python
def max_overlap(intervals):      # intervalos [s, e) semiabertos
    ev = []
    for s, e in intervals:
        ev.append((s, +1)); ev.append((e, -1))
    ev.sort()                    # no mesmo x, -1 (fim) vem ANTES de +1 (início): [1,3) e [3,5) não se sobrepõem
    cur = best = 0
    for _, d in ev:
        cur += d; best = max(best, cur)
    return best
```

**A regra de desempate entre eventos no mesmo x define a semântica.** Para intervalos fechados `[s, e]` que se tocam e devem contar como sobreposição, o início vem antes do fim. Decida explicitamente e teste o caso que se toca.

**Merge de intervalos:** ordene pelo início; funda se `s <= fim_atual` (fechado) ou `s < fim_atual` (semiaberto que não se toca) e faça `fim_atual = max(fim_atual, e)`. **Não** atribua `fim_atual = e`, porque um intervalo contido em outro encolheria o fim.

**Agendamento:** número mínimo de salas = máximo de sobreposição (ou min-heap de horários de fim). Máximo de intervalos disjuntos = greedy por **fim** crescente (CLRS 16.1, seleção de atividades). Ordenar pelo início é o bug clássico.

---

## Coordinate compression

Valores grandes ou esparsos (até 10⁹) mapeados para `0..k−1`, preservando a ordem. Permite usar BIT ou segment tree indexados por valor.

```python
xs = sorted(set(vals))
idx = {v: i for i, v in enumerate(xs)}      # ou bisect_left(xs, v)
```
**Bugs:** comprimir só os valores dos dados e esquecer os valores das **queries** (comprima tudo junto, offline); em geometria e sweep, perder o "espaço entre" coordenadas (inclua `x+1` ou trate segmentos `[xs[i], xs[i+1])`).

---

## Programação dinâmica (CLRS cap. 15)

**Quando aplicar (CLRS 15.3):** (1) **subestrutura ótima**, ou seja, a solução ótima contém soluções ótimas de subproblemas; (2) **subproblemas sobrepostos**, ou seja, a recursão ingênua recalcula os mesmos estados. Se os subproblemas não se repetem, é divisão e conquista e memo não ajuda.

**Receita:**
1. Defina o **estado** com o mínimo de informação que determina o futuro. Escreva em uma frase: "`dp[i][j]` = melhor valor considerando…".
2. Escreva a transição e os casos base.
3. Ordem de cálculo: cada estado depende só de estados já calculados.
4. Complexidade = nº de estados × custo da transição. Reduza um dos dois.
5. Reconstrução: guarde a escolha (`parent`) ou refaça o caminho comparando valores.

**Top-down (memo) vs bottom-up:** a memoização é mais fácil de acertar e visita só estados alcançáveis, mas tem custo de recursão (profundidade, overhead, limite do Python). O bottom-up é mais rápido e permite **rolling array**.

**Rolling array (memória O(W) em vez de O(n·W)):**
```python
# 0/1 knapsack: cada item no máximo uma vez → capacidade DECRESCENTE
for wt, val in items:
    for c in range(W, wt - 1, -1):
        dp[c] = max(dp[c], dp[c - wt] + val)
# unbounded (item reutilizável) → capacidade CRESCENTE
for wt, val in items:
    for c in range(wt, W + 1):
        dp[c] = max(dp[c], dp[c - wt] + val)
```
Inverter a direção é **o** bug clássico de knapsack 1D (vira o outro problema sem nenhum erro). Em contagem de combinações vs permutações (coin change), a ordem dos laços também muda o problema: itens por fora contam combinações; capacidade por fora conta permutações.

**Otimizações de transição:**

| Forma da transição                                    | Técnica                                   | Ganho          |
|-------------------------------------------------------|-------------------------------------------|----------------|
| `dp[i] = min(dp[j]) + c`, j numa janela deslizante    | monotonic deque                           | O(nk) → O(n)   |
| `dp[i] = min(dp[j] + b[j]·a[i])`                      | convex hull trick / Li Chao tree          | O(n²) → O(n log n) |
| `dp[k][i] = min(dp[k-1][j] + C(j,i))`, opt monotônico | divide & conquer optimization             | O(kn²) → O(kn log n) |
| DP intervalar com desigualdade quadrangular           | Knuth                                     | O(n³) → O(n²)  |
| soma sobre subconjuntos                               | SOS DP                                    | O(3ⁿ) → O(n·2ⁿ) |
| recorrência linear com n enorme                       | exponenciação de matriz                   | O(n) → O(k³ log n) |
| prefixos de dp somados repetidamente                  | prefix sum sobre o array de dp            | tira um fator n |

**Bugs de DP:** estado incompleto (falta uma dimensão que afeta o futuro); caso base errado (`dp[0]` = 1 vs 0 em contagem); valor sentinela de "impossível" (`-inf`) somado e virando um número válido; memo com `lru_cache` em argumentos mutáveis (não-hashable) ou memória estourando (use `cache_clear`); modular: aplicar `% MOD` antes de comparar max/min (**não** dá para maximizar sob módulo); iterar na ordem errada no bottom-up.

---

## Greedy (CLRS cap. 16)

Funciona quando há **propriedade de escolha gulosa** (alguma solução ótima começa com a escolha gulosa) **e** subestrutura ótima (CLRS 16.2). Prove por **argumento de troca**: pegue uma solução ótima que difere da gulosa e mostre que trocar para a escolha gulosa não piora. Se não conseguir provar, faça **stress test contra força bruta** antes de confiar.

Clássicos: seleção de atividades (ordenar por **fim**), Huffman (heap, CLRS 16.3), mochila fracionária (razão valor/peso; a 0/1 **não** é gulosa), troco (guloso só para sistemas de moedas canônicos), agendamento com prazos (matroide, CLRS 16.5).

---

## Análise amortizada (CLRS cap. 17)

- Métodos: agregado, contabilidade e potencial. Use para justificar O(1) amortizado em: array dinâmico (dobrar a capacidade), monotonic stack/deque (cada elemento entra e sai uma vez), two pointers, DSU, contador binário.
- **Tabela dinâmica (CLRS 17.4):** dobre quando encher. Para encolher, **não** reduza à metade quando cair abaixo de 1/2 cheia: a sequência insere/remove na fronteira causa thrashing de Θ(n) por operação. Reduza à metade quando cair para **1/4**. O fator de carga fica em [1/4, 1] e tudo é O(1) amortizado.
- Crescimento aditivo (+k) em vez de multiplicativo deixa n inserções em O(n²).
- Amortizado ≠ pior caso. Uma operação isolada pode custar O(n) (rehash, resize), o que importa em sistemas com requisito de latência.

---

## Strings e hashing (CLRS cap. 32)

- Concatenação em laço → `"".join(partes)` / `StringBuilder`.
- **Busca de padrão:** KMP (função prefixo, O(n+m), CLRS 32.4), Z-function, Rabin-Karp (rolling hash, CLRS 32.2), Aho-Corasick (muitos padrões), suffix array + LCP (muitas queries de substring).
- **Rolling hash polinomial:**
  ```python
  import random
  MOD = (1 << 61) - 1
  BASE = random.randrange(256, MOD - 1)      # base ALEATÓRIA: resiste a anti-hash
  def build(s):
      h = [0] * (len(s) + 1); pw = [1] * (len(s) + 1)
      for i, c in enumerate(s):
          h[i+1] = (h[i] * BASE + ord(c)) % MOD
          pw[i+1] = pw[i] * BASE % MOD
      return h, pw
  def sub(h, pw, l, r):                      # hash de s[l:r]
      return (h[r] - h[l] * pw[r - l]) % MOD # Python: % já é não-negativo
  ```
  **Bugs:** módulo 2⁶⁴ natural (overflow) é quebrável por sequências de Thue-Morse; módulo pequeno (~10⁹) com muitas comparações colide pelo paradoxo do aniversário (use 2⁶¹−1 ou hash duplo); mapear `'a' → 0` (então `"a"` e `"aa"` colidem; use `ord(c)` ou `c - 'a' + 1`); subtração negativa em C/Java; base fixa e conhecida em ambiente adversarial. Na colisão de hash, **confirme com comparação real** quando a correção é obrigatória.

---

## Sqrt decomposition e Mo's algorithm

- **Sqrt decomposition:** divida em blocos de ~√n e mantenha um agregado por bloco. Update e query em O(√n). É simples e flexível quando segment tree com lazy fica complicada.
- **Mo's algorithm:** queries **offline** de intervalo com `add(i)` e `remove(i)` em O(1). Ordene as queries por `(l // B, r)`, com r alternando crescente e decrescente por bloco (ordem par/ímpar), e B ≈ n/√q. Total O((n + q)·√n).
  - **Bugs:** expandir antes de contrair na ordem errada (fazendo `l > r` temporariamente com estruturas que não suportam isso). Faça primeiro as expansões (`l--`, `r++`) e depois as contrações. Outro bug: devolver as respostas na ordem ordenada em vez da ordem original.

---

## Bits

- `x & (x - 1)` remove o bit menos significativo; `x & -x` isola o menor bit (base do Fenwick); `x & (x - 1) == 0` testa potência de 2 (com `x > 0`).
- Iterar submáscaras: `s = m; while s: ...; s = (s - 1) & m` (O(3ⁿ) somando todas as máscaras). Lembre de tratar `s = 0` à parte se ele for necessário.
- Bitset (`std::bitset`, `int` grande do Python) acelera DP de subset sum em ~64×: `bits |= bits << w`.
- **Bugs:** `1 << 40` em `int` de 32 bits é UB (use `1LL << 40`); shift de valor negativo; precedência (`a & b == c` é `a & (b == c)` em C/C++/Java/JS; use parênteses); popcount sem a função built-in.

---

## Meet in the middle

n ≈ 40 com subconjuntos: divida em duas metades de 20, enumere os 2²⁰ de cada uma, ordene uma e faça busca binária ou two pointers combinando com a outra. O(2^(n/2) · n).

---

## Padrões práticos (Competitive Programmer's Handbook, Laaksonen)

**Ordenar costuma ganhar da estrutura de dados com a mesma complexidade (CPHB 4.6).** No problema "quantos elementos de A estão em B" com n = 10⁶ (C++), as medições do livro foram: `set` 1,5 s; `unordered_set` 0,3 s; **ordenar os dois e percorrer com two pointers: 0,2 s**. As abordagens com `set` e com sort são ambas O(n log n), mas a com sort ficou ~7× mais rápida porque ordena uma vez e depois faz um laço linear, enquanto a outra mantém uma árvore balanceada o tempo todo. Regra: se os dados não mudam durante as queries, prefira **sort + busca binária ou varredura** a árvores balanceadas.

**Kadane (soma máxima de subarray) em O(n) (CPHB 2.4):**
```python
def max_subarray(a):           # pelo menos 1 elemento
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)  # estende ou recomeça
        best = max(best, cur)
    return best
```
Bug: inicializar `best = 0` quando todos os valores podem ser negativos e o subarray não pode ser vazio.

**LIS em O(n log n):** mantenha `tails[k]` = menor final possível de uma subsequência crescente de tamanho k+1, e use `bisect_left` (estritamente crescente) ou `bisect_right` (não-decrescente).
```python
from bisect import bisect_left
def lis(a):
    tails = []
    for x in a:
        i = bisect_left(tails, x)
        if i == len(tails): tails.append(x)
        else: tails[i] = x
    return len(tails)          # tails NÃO é a subsequência; para reconstruir, guarde índices e pais
```

**Busca completa com poda (CPHB 5.3–5.4):** backtracking é a força bruta de referência para o stress test. Para podar: corte estados impossíveis cedo (ex.: o restante não alcança o alvo), explore a simetria (fixe a primeira escolha) e ordene as escolhas para achar boas soluções cedo (branch and bound). Subconjuntos por bitmask: `for m in range(1 << n)`; permutações: `itertools.permutations` / `std::next_permutation` (comece de um array **ordenado**, senão perde permutações).

**Técnicas de árvore (CPHB cap. 14 e 18):**
- **Achatar a árvore (Euler tour / tree traversal array):** na DFS, registre `tin[v]` e `tout[v]` (ou `tin + size`). A subárvore de v vira o intervalo contíguo `[tin[v], tin[v] + size[v])`. Assim, "soma, update ou mínimo na subárvore" vira query de intervalo em BIT ou segment tree, O(log n). Soma de caminho raiz→v: some `+x` em `tin[v]` e `−x` em `tout[v]`, depois faça soma de prefixo.
- **Diâmetro em O(n) com duas buscas:** a partir de qualquer nó a, ache o mais distante b; a partir de b, ache o mais distante c; o diâmetro é dist(b, c). Com pesos negativos o truque não vale (use DP).
- **"Para cada nó, o caminho mais longo a partir dele" (rerooting):** primeira DFS calcula a resposta para baixo (os 2 melhores filhos); a segunda propaga a resposta "para cima" do pai. Guarde o **segundo** melhor para quando o melhor passa pelo próprio filho.
- **Small-to-large (merge de estruturas, CPHB 18.4):** ao juntar os conjuntos ou mapas dos filhos, copie sempre o **menor** para o **maior** (troque antes, em O(1) com `swap`). Cada elemento é copiado O(log n) vezes, total O(n log n) (ou O(n log² n) com map). Bug clássico: copiar o do pai para o do filho sem comparar tamanhos, que vira O(n²) numa árvore em linha.
- **Árvore enraizada a partir da lista de arestas:** escolha a raiz e faça BFS/DFS guardando `parent`. Nunca assuma que a entrada vem como "pai → filho".

**Grafos funcionais / successor graphs (CPHB 16.3–16.4):** cada nó tem exatamente 1 sucessor (`f(x)`). Cada componente é um ciclo com árvores penduradas. `succ(x, k)` para k até 10¹⁸ sai com **binary lifting** (`up[j][x] = up[j−1][up[j−1][x]]`) em O(log k). Achar o ciclo a partir de x: Floyd (tartaruga e lebre) com memória O(1). Exemplos: simulação de "teleporte k vezes", permutações aplicadas k vezes, detecção de ciclo em geradores pseudo-aleatórios.

**Sqrt por limiar de frequência (CPHB 27.1):** quando há dois algoritmos, um bom para grupos pequenos (O(k²) por grupo) e outro para grupos grandes (O(n) por grupo, ex. BFS multi-fonte), use o primeiro se `k ≤ √n` e o segundo caso contrário. Existem no máximo √n grupos grandes, então o total fica O(n√n). Vale também para "itens leves vs pesados" em grafos (vértices com grau > √m tratados à parte).

**Segment tree dinâmica/esparsa (CPHB 28.2):** com índices em [0, 10⁹] e poucas operações, crie os nós sob demanda (memória O(k log n)) em vez de comprimir coordenadas. Isso é útil quando as queries são **online** e não dá para comprimir antes. **Persistente:** cada update cria O(log n) nós novos e preserva versões antigas (k-ésimo menor em intervalo).

**Nós com estruturas (CPHB 28.3):** segment tree cujo nó guarda um vetor ordenado (merge sort tree) responde "quantos ≤ x em [l, r]" em O(log² n). O custo é O(f(n)·log n), onde f é o custo por nó.

**Entrada e saída como gargalo (CPHB 1.2):** com 10⁶ números, `cin` sem `sync_with_stdio(false)` ou `input()` em Python podem levar mais tempo que o algoritmo. Veja `language-pitfalls.md`.

---

## Otimização de constante (depois do big-O)

1. **Localidade de cache:** arrays contíguos ganham de estruturas de ponteiros (lista ligada, árvore com nós soltos). Percorra matrizes na ordem de armazenamento (linha por linha em C/Python/Java). Structure of Arrays em laços quentes. CSR para grafos estáticos.
2. **Alocação:** pré-aloque (`reserve`, arrays de tamanho fixo), reutilize buffers, use pools e arenas e evite criar objetos em laços quentes.
3. **Boxing:** `int[]` em vez de `List<Integer>` (Java); `array`/`numpy` em vez de listas de objetos (Python); evite `Map<Integer, …>` em laços quentes.
4. **I/O:** leitura em bloco (`sys.stdin.buffer.read().split()`; `BufferedReader`/`DataInputStream`; `ios::sync_with_stdio(false); cin.tie(nullptr);`) e saída acumulada (`"\n".join`, `StringBuilder`, `'\n'` em vez de `endl`).
5. **Python especificamente:** vetorize com numpy; use built-ins (`sum`, `map`, `sorted`, `collections`, `itertools`), que rodam em C; associe atributos e funções a variáveis locais em laços quentes; evite chamadas de função em O(n²); use PyPy quando possível.
6. **Memoização/caching** de funções puras chamadas repetidamente com os mesmos argumentos. Considere o limite de memória e a invalidação.
7. **Pré-computação:** fatoriais e inversos modulares, crivo de primos, tabelas de log, potências.
8. **Branch prediction:** dados ordenados ajudam laços com `if` e técnicas branchless; isso só importa depois de tudo acima.
9. **Paralelismo e SIMD:** só depois do algoritmo certo. Cuidado com estruturas compartilhadas e falso compartilhamento.

**Meça antes e depois** (`timeit`, `perf`, `py-spy`, JMH, `criterion`, benchmarks com `-O2`), sempre com entradas no tamanho real e também no pior caso.

---

## Aritmética, overflow e módulo

- 10⁵ × 10⁵ = 10¹⁰ não cabe em `int32` (o máximo é ≈ 2,1·10⁹). Somas de até 10⁵ valores de 10⁹ precisam de `int64`. Em C++, o produto `a * b` com `int` estoura **antes** de atribuir a `long long`; faça o cast em um operando: `1LL * a * b`.
- `(a * b) % M` com `a, b < M ≈ 10⁹` cabe em `int64`. Com `M ≈ 10¹⁸`, use `__int128` ou mulmod.
- Subtração modular: `((a - b) % M + M) % M`.
- Divisão modular usa o inverso: `pow(b, M-2, M)` com M primo (Fermat). **Não** divida diretamente sob módulo.
- `INF`: `10**18` para `int64`; `0x3f3f3f3f` para `int32` com `memset` (o dobro ainda cabe). Não use `INT_MAX` se for somar.
- Float: compare com tolerância; acumule com Kahan, `math.fsum` ou inteiros escalados (centavos, não reais). **Nunca** use float para dinheiro.
- JS: `Number` é exato só até 2⁵³−1; use `BigInt` além disso. Operações bitwise convertem para int32 com sinal (`x | 0`, `>>`); use `>>>` para unsigned.
