# Estruturas lineares

Índice: [Array dinâmico](#array-dinâmico) · [Lista ligada](#lista-ligada) · [Stack](#stack) · [Fila e buffer circular](#fila-e-buffer-circular) · [Deque](#deque) · [Monotonic stack](#monotonic-stack) · [Monotonic deque](#monotonic-deque) · [Hash table](#hash-table)

---

## Array dinâmico

| Operação                      | Custo                    |
|-------------------------------|--------------------------|
| acesso `a[i]`                 | O(1)                     |
| push/pop no fim               | O(1) amortizado          |
| inserir/remover no meio/início | O(n)                    |
| busca não ordenada            | O(n)                     |
| busca em array ordenado       | O(log n) (busca binária) |

**Por que costuma ganhar de lista ligada:** memória contígua, prefetch da CPU, sem ponteiro por elemento e sem alocação por nó. O benchmark clássico apresentado por Stroustrup (inserir em posição ordenada e remover posição aleatória) mostra `vector` vencendo `list` mesmo com o custo O(n) de deslocamento, porque achar a posição na lista já é O(n) com cache miss em cada nó.

**Técnicas:**
- `reserve(n)` / capacidade inicial quando o tamanho é conhecido evita realocações.
- **Swap-and-pop:** remove em O(1) quando a ordem não importa (`a[i] = a[-1]; a.pop()`).
- **Remove-erase / filtro em uma passada:** remover vários elementos custa O(n) no total, contra O(n²) com `erase` repetido.
  ```cpp
  v.erase(std::remove_if(v.begin(), v.end(), pred), v.end());   // C++17
  std::erase_if(v, pred);                                        // C++20
  ```
- **Structure of Arrays** (`xs[]`, `ys[]`) em vez de Array of Structs em loops que leem só um campo.

**Bugs clássicos:**
- **Invalidação:** em C++, `push_back` que realoca invalida todos os iteradores, ponteiros e referências. Guardar `&v[0]` ou `auto& x = v[i]` e depois dar push é undefined behavior.
- **Apagar durante iteração:** em C++, use `it = v.erase(it)` e só incremente no `else`. Em Java, `Iterator.remove()` ou `removeIf`. Em Python, itere sobre uma cópia ou construa uma lista nova.
- **Iterar removendo por índice crescente** pula o elemento seguinte; itere de trás para frente.
- **Matriz com linhas compartilhadas:** `[[0]*m]*n` em Python, `Array(n).fill([])` em JS.
- **Slicing copia:** `a[1:]` em Python é O(k). Recursão `f(a[1:])` vira O(n²); passe índices.

---

## Lista ligada

**Quando realmente vale:** você já tem o ponteiro/handle do nó e precisa inserir/remover em O(1) (LRU cache, listas intrusivas, splice O(1) de listas inteiras, alocadores livres). Fora disso, prefira array/deque.

**Sentinela (nó dummy) elimina quase todos os casos especiais**: a lista nunca está "vazia" do ponto de vista dos ponteiros, então não existem checagens de `head is None` / `tail`.

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None

class DList:
    """Lista duplamente ligada circular com sentinela."""
    def __init__(self):
        self.s = Node()
        self.s.prev = self.s.next = self.s
        self.size = 0

    def insert_after(self, p, n):
        # ordem importa: ligar n primeiro, depois redirecionar os vizinhos
        n.prev, n.next = p, p.next
        p.next.prev = n          # precisa vir ANTES de p.next = n
        p.next = n
        self.size += 1

    def unlink(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev
        n.prev = n.next = None   # ajuda a detectar uso após remoção
        self.size -= 1

    def push_front(self, n): self.insert_after(self.s, n)
    def pop_back(self):
        if self.size == 0: raise IndexError("empty")
        n = self.s.prev; self.unlink(n); return n
```

**LRU cache = hash map (chave → nó) + DList.** No `get`, faça unlink e push_front. No `put`, se estourou a capacidade, `pop_back` e apague a chave do map. Bug comum: esquecer de apagar do map a chave do nó despejado (por isso o nó guarda `key`).

**Bugs clássicos:**
- Perder a referência do resto da lista ao religar (sobrescrever `p.next` antes de salvá-lo).
- Lista duplamente ligada: são **4 ponteiros** a atualizar em inserção/remoção; esquecer um corrompe a travessia reversa.
- Não atualizar `tail` (sem sentinela) quando remove o último.
- `node.next.next` sem checar `node.next` nulo.
- **Reverter lista:** use três ponteiros `prev, cur, nxt`; salve `nxt = cur.next` antes de `cur.next = prev`.
- **Detectar ciclo:** Floyd (lento 1 passo, rápido 2). Para achar o início do ciclo, depois do encontro reinicie um ponteiro na cabeça e ande os dois 1 passo até se encontrarem.
- **Meio da lista:** com `fast = head`, o ponteiro lento para no meio superior; com `fast = head.next`, no inferior. Decida qual você quer.
- C/C++: use-after-free, double free, leak ao remover. Prefira `unique_ptr` para o next ou um arena/pool.

---

## Stack

Implemente sobre array dinâmico (push/pop no fim). Usos: parênteses, undo, avaliação de expressões (shunting-yard), DFS iterativa, conversão de recursão, monotonic stack.

**Converter recursão em pilha explícita:**
- Pré-ordem: empilhe os filhos **em ordem reversa** para visitá-los na ordem original.
- Pós-ordem: empilhe `(nó, visitado_filhos=False)`; ao ver `False`, reempilhe com `True` e depois os filhos. Alternativa: pré-ordem invertida (raiz, direita, esquerda) e reverta o resultado no fim.
- Para simular "volta da recursão" (ex.: calcular `low[]`), use `(nó, índice_do_próximo_vizinho)`. Veja a DFS iterativa em `graphs.md`.

**Bugs:** `pop`/`peek` em pilha vazia (no problema de parênteses, `")"` com pilha vazia é inválido); ao terminar, a pilha precisa estar vazia (`"(("` é inválido); confundir `peek` com `pop`.

---

## Fila e buffer circular

**Nunca** implemente fila com `list.pop(0)` (Python), `Array.shift()` (JS) ou `ArrayList.remove(0)` (Java): cada uma é O(n). Use `collections.deque`, `ArrayDeque`, `std::queue`/`std::deque`, ou um array com índice `head` que só avança.

**Buffer circular (ring buffer)**: capacidade fixa, O(1), sem alocação. A ambiguidade central é que `head == tail` pode significar **vazio ou cheio**. Há três soluções:
1. **Guardar `size`** (a mais simples e menos sujeita a bug). Recomendada.
2. Desperdiçar um slot: cheio quando `(tail + 1) % cap == head`. A capacidade útil passa a ser `cap - 1`, e esquecer isso é um bug comum.
3. Índices monotônicos sem módulo, com `cap` potência de 2: `size = tail - head` e posição `= idx & (cap - 1)`. Funciona com overflow de inteiro sem sinal e é comum em filas lock-free.

```python
class Ring:
    def __init__(self, cap):
        self.buf = [None] * cap
        self.head = 0      # índice do primeiro elemento
        self.size = 0

    def push_back(self, x):
        if self.size == len(self.buf): raise OverflowError("full")
        self.buf[(self.head + self.size) % len(self.buf)] = x
        self.size += 1

    def push_front(self, x):
        if self.size == len(self.buf): raise OverflowError("full")
        self.head = (self.head - 1) % len(self.buf)   # em C/Java/JS: (head - 1 + cap) % cap
        self.buf[self.head] = x
        self.size += 1

    def pop_front(self):
        if self.size == 0: raise IndexError("empty")   # checar ANTES de mover índices
        x = self.buf[self.head]
        self.buf[self.head] = None                     # libera a referência para o GC
        self.head = (self.head + 1) % len(self.buf)
        self.size -= 1
        return x

    def pop_back(self):
        if self.size == 0: raise IndexError("empty")
        self.size -= 1
        i = (self.head + self.size) % len(self.buf)
        x, self.buf[i] = self.buf[i], None
        return x

    def __getitem__(self, k):            # k-ésimo a partir da frente, O(1)
        if not 0 <= k < self.size: raise IndexError
        return self.buf[(self.head + k) % len(self.buf)]
```

**Bugs:** módulo negativo em `head - 1`; não checar vazio/cheio antes de mover os índices; atualizar `size` só em alguns caminhos; versão crescente (resize) que copia o buffer sem "desenrolar" a partir de `head`; em código concorrente, ler/escrever `head`/`tail` sem atomics com acquire/release (ou lock).

**Teste sempre:** vazio, cheio, wrap-around (encha, esvazie metade, encha de novo), e capacidade 1.

---

## Deque

Implementações: buffer circular crescente (`ArrayDeque`, Rust `VecDeque`), blocos encadeados (`std::deque`, Python `collections.deque`).

- Python `deque`: pontas em O(1), mas **indexar no meio é O(n)**. Não use como array de acesso aleatório.
- `std::deque`: indexação O(1), mas `push_front`/`push_back` invalidam **iteradores** (as referências continuam válidas). Inserir no meio invalida tudo.
- Java `ArrayDeque` não aceita `null` e é mais rápido que `LinkedList` e `Stack` (legado e sincronizado). Use `ArrayDeque` para pilha e fila.

Usos: 0-1 BFS, monotonic deque, palíndromos, work stealing, histórico com limite.

---

## Monotonic stack

Resolve "próximo/anterior maior/menor elemento", "maior retângulo no histograma", "soma dos mínimos de subarrays" em O(n) amortizado: cada índice entra e sai da pilha uma vez.

```python
def next_greater(a):
    """res[i] = índice do próximo elemento estritamente maior que a[i], ou -1."""
    res = [-1] * len(a)
    st = []                       # índices; a[st] é não-crescente do fundo ao topo
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = i
        st.append(i)
    return res
```

**Contagem com duplicatas (bug clássico).** Para "soma dos mínimos de todos os subarrays", conta-se para cada `i` quantos subarrays têm `a[i]` como mínimo: `(i - left[i]) * (right[i] - i)`. Com valores repetidos, um lado precisa usar comparação **estrita** e o outro **não-estrita**, senão subarrays com mínimos empatados são contados duas vezes (ou nenhuma):
- `left[i]` = último índice à esquerda com `a[j] < a[i]` (estrito)
- `right[i]` = primeiro índice à direita com `a[j] <= a[i]` (não-estrito)

**Bugs:** guardar valores em vez de índices (perde a posição e a distância); errar a direção (pilha decrescente acha próximo **maior**, crescente acha próximo **menor**); esquecer de processar o que sobra na pilha no fim (no histograma, use um sentinela de altura 0 no final).

**Maior retângulo no histograma:**
```python
def largest_rectangle(h):
    st, best = [], 0
    for i, x in enumerate(h + [0]):          # sentinela 0 esvazia a pilha no fim
        start = i
        while st and st[-1][1] >= x:
            j, hj = st.pop()
            best = max(best, hj * (i - j))
            start = j                         # o novo retângulo pode começar onde o removido começava
        st.append((start, x))
    return best
```

---

## Monotonic deque

Máximo/mínimo de **janela deslizante** em O(n).

```python
from collections import deque

def window_max(a, k):
    dq, out = deque(), []          # índices; a[dq] decrescente da frente para o fim
    for i, x in enumerate(a):
        if dq and dq[0] <= i - k:  # 1) expira o índice que saiu da janela (pela frente)
            dq.popleft()
        while dq and a[dq[-1]] <= x:   # 2) remove dominados (pelo fim)
            dq.pop()
        dq.append(i)
        if i >= k - 1:             # 3) a janela está completa
            out.append(a[dq[0]])
    return out
```

**Bugs:** guardar valores em vez de índices (não dá para saber quando expiraram, e duplicatas confundem); deque crescente para máximo (o certo é decrescente; crescente dá o mínimo); emitir resposta antes de a janela ter `k` elementos; `k > len(a)`.

Variante "janela variável": também serve em DP do tipo `dp[i] = max(dp[j]) + c` para `j ∈ [i-k, i-1]` (otimização de DP por fila monotônica).

---

## Hash table

| Operação          | Médio | Pior                                   |
|-------------------|-------|----------------------------------------|
| insert/find/erase | O(1)  | O(n) (colisões, hash ruim ou adversário) |

**Desenho interno:**
- **Encadeamento (chaining):** buckets com listas. Simples; degrada suavemente.
- **Endereçamento aberto** (linear/quadratic probing, Robin Hood, Swiss table): melhor cache. **Remoção exige tombstone**: marcar a posição como "apagada" em vez de vazia, senão buscas que passavam por ela param antes da hora e não acham chaves existentes. Tombstones acumulados degradam a tabela, então é preciso rehash periódico.
- **Load factor:** chaining ~0.75–1.0; open addressing ≤ ~0.5–0.875. Ao crescer, faça rehash de tudo (O(n) pontual; O(1) amortizado).
- Tamanho potência de 2 com `hash & (cap - 1)` exige hash bem misturado nos bits baixos (aplique um mixer, ex. splitmix64/fmix64).

**Bugs clássicos:**
- **Chave mutável:** mudar um campo usado no hash depois de inserir deixa a entrada "perdida". Chaves devem ser imutáveis.
- **Contrato `equals`/`hashCode`** (Java, C#, `__eq__`/`__hash__` no Python): objetos iguais precisam ter o mesmo hash. Sobrescrever só `equals` quebra o `HashMap`.
- **Float como chave:** `0.1 + 0.2 != 0.3`, `NaN != NaN`, e `-0.0 == 0.0` mas com bits diferentes. Arredonde ou use inteiro escalado.
- **Hash flooding / anti-hash:** entrada adversária gera colisões em massa e transforma O(n) em O(n²). Já derrubou servidores web (2011) e é comum em competições contra `unordered_map`. Defesa: hash com semente aleatória (SipHash, ou splitmix64 com seed do relógio).
  ```cpp
  struct SafeHash {
      static uint64_t splitmix64(uint64_t x) {
          x += 0x9e3779b97f4a7c15; x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
          x = (x ^ (x >> 27)) * 0x94d049bb133111eb; return x ^ (x >> 31);
      }
      size_t operator()(uint64_t x) const {
          static const uint64_t SEED = std::chrono::steady_clock::now().time_since_epoch().count();
          return splitmix64(x + SEED);
      }
  };
  std::unordered_map<long long, int, SafeHash> m;
  m.reserve(1 << 20);   // evita rehash repetido
  ```
- **Ordem de iteração** não é garantida (Go randomiza de propósito; Java `HashMap` muda entre versões). Python `dict` e JS `Map` preservam a inserção. Para ordem determinística use `LinkedHashMap` ou ordene as chaves.
- **JS:** objeto `{}` converte chaves para string (`obj[1]` e `obj["1"]` são a mesma chave; objetos viram `"[object Object]"`). Use `Map`/`Set`.
- **C++ `operator[]` insere** um valor default ao ler; para só consultar, use `find`/`count`/`contains`.
- **Modificar durante iteração** (Python `RuntimeError: dictionary changed size`, Java CME).

**Quando NÃO usar hash:** você precisa de ordem, range queries, predecessor/sucessor ou pior caso garantido. Nesses casos use árvore balanceada ou array ordenado + busca binária (melhor ainda se os dados são estáticos).

**Pares/tuplas como chave:** em C++ codifique `(a, b)` como `a * BIG + b` (ou `(uint64_t)a << 32 | b`) para evitar hash de par ruim. Em Python, tuplas funcionam, mas inteiro codificado é mais rápido em loops quentes.
