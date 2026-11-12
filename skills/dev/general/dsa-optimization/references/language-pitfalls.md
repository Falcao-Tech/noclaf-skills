# Armadilhas por linguagem

Cada linguagem tem estruturas que parecem O(1) e não são, e defaults que mudam o resultado. Consulte a seção da linguagem do código antes de otimizar ou revisar.

## Python

| Armadilha                                  | Correção                                                                 |
|--------------------------------------------|--------------------------------------------------------------------------|
| `list.pop(0)`, `list.insert(0, x)` O(n)    | `collections.deque` (`popleft`, `appendleft`)                            |
| `x in lista` dentro de laço                | converter para `set` antes                                               |
| `deque[i]` no meio é O(n)                  | deque só para as pontas; para acesso aleatório, use lista + índice `head` |
| `[[0]*m]*n` compartilha as linhas          | `[[0]*m for _ in range(n)]`                                              |
| `s += c` em laço                           | `"".join(partes)`                                                        |
| slicing `a[1:]` copia (O(k))               | passar índices; `memoryview` para bytes                                  |
| recursão: limite ~1000; `setrecursionlimit` alto dá segfault | pilha explícita; ou `threading.stack_size(2**27)` + rodar numa `Thread` |
| `heapq` é **min**-heap                     | max-heap: negar a chave (`-x`)                                           |
| `heapq` com tuplas: empate compara o payload | `(prio, contador, item)` com `itertools.count()`                        |
| sem TreeMap/SortedSet na stdlib            | `sortedcontainers.SortedList` (se puder instalar) ou `bisect` em lista (insert O(n)) |
| `bisect.insort` é O(n) (desloca a lista)   | ok para n ≤ ~10⁵ com poucas inserções; senão SortedList, BIT ou heap     |
| `//` arredonda para −∞ e `%` é sempre ≥ 0 com divisor positivo | ao portar de/para C/Java, os resultados com negativos mudam |
| `int` arbitrário: não estoura, mas fica lento com números gigantes | aplique `% MOD` a cada passo                          |
| `functools.lru_cache` exige argumentos hashable e segura memória | usar tuplas; `cache_clear()`; ou DP bottom-up        |
| argumento default mutável (`def f(a=[])`)  | `def f(a=None): a = a or []`                                             |
| `dict`/`set` mudando de tamanho durante iteração → `RuntimeError` | iterar sobre `list(d)`                          |
| `float('inf')` mistura com int (ok), mas `math.inf` em arrays numpy de int não | usar um int grande (`10**18`) em DP de inteiros |
| `input()` lento                            | `data = sys.stdin.buffer.read().split()`; saída com `sys.stdout.write("\n".join(...))` |
| laço Python puro ~10⁷ op/s                 | numpy vetorizado, built-ins (`sum`, `map`, `sorted`, `Counter`), PyPy, variáveis locais |
| `copy` raso em estruturas aninhadas        | `copy.deepcopy` (lento) ou reconstruir                                   |
| objetos com muitos atributos               | `__slots__` reduz memória e acelera acesso                               |

## Django / ORM

| Armadilha                                                     | Correção                                                        |
|---------------------------------------------------------------|-----------------------------------------------------------------|
| repositório/serviço chamado dentro de laço: cada chamada é 1 SQL (N+1 escondido pela camada) | 1 consulta com `values().annotate()` atravessando as FKs; `select_related`/`prefetch_related` quando precisa dos objetos |
| agregar em Python (`sum(...)` sobre objetos)                  | `aggregate`/`annotate` com `Sum(F("q") * F("preço"))` no banco  |
| 1 consulta por item de um lote (cliente, intervalo, pedido)   | 1 consulta para o lote inteiro (`__in`, GROUP BY) + estrutura em memória (prefix sums, bisect, two pointers) |
| `TruncDate`/`TruncMonth` no **SQLite** viram função Python linha a linha (medido: 2,4× mais lento) | `Func(F(campo), function="DATE")` / `strftime` nativos no SQLite; manter `Trunc*` no Postgres |
| `__in` com milhares de ids                                    | fatiar em lotes (~900 no SQLite antigo; Postgres aguenta mais, mas prefira join/subquery) |
| `values().annotate()` agrupa errado com `Meta.ordering`        | `.order_by()` vazio antes de agrupar                            |
| cache de resultado como "otimização"                          | só ajuda na 2ª chamada igual; a 1ª e as com argumentos novos pagam tudo, e o dado fica defasado até o TTL |
| threads para paralelizar N+1                                  | o custo é por consulta; reduzir o número de consultas ganha 10–100× mais que paralelizar |
| relatório que agrega a tabela inteira a cada request          | agregado mantido na escrita (tabela de totais, Fenwick) → leitura O(log n) |

Caso medido (Django + DRF, 200 mil pedidos): repositórios + cache + 4 threads: 74,7 s frio; consultas agregadas + estruturas: 4,7 s (16×), com respostas idênticas.

## JavaScript / TypeScript

| Armadilha                                              | Correção                                                        |
|--------------------------------------------------------|-----------------------------------------------------------------|
| `arr.sort()` sem comparator ordena **como string** (`[10, 9, 1]` → `[1, 10, 9]`) | `arr.sort((a, b) => a - b)` (cuidado com overflow só em BigInt/floats extremos) |
| `shift()` / `unshift()` O(n)                           | fila com índice `head` ou buffer circular                       |
| `{}` como mapa: chaves viram string; `__proto__` e herança | `Map` / `Set`                                               |
| `new Array(n).fill([])` compartilha a referência       | `Array.from({ length: n }, () => [])`                           |
| `Number` exato só até 2⁵³−1                            | `BigInt` (lento) ou modular com cuidado: `a * b` com a, b ~10⁹ já perde precisão (use BigInt ou multiplicação em partes) |
| bitwise converte para int32 com sinal                  | `>>>` para unsigned; não use `|0` com valores > 2³¹             |
| `%` negativo                                           | `((x % m) + m) % m`                                             |
| `Math.max(...arr)` com arr gigante → RangeError (estouro de pilha) | `arr.reduce((a, b) => Math.max(a, b), -Infinity)`    |
| spread/`concat`/`[...acc, x]` dentro de laço → O(n²)    | `push`                                                          |
| `includes`/`indexOf` em laço                           | `Set`                                                           |
| sem heap, deque, TreeMap nativos                       | implementar o heap (veja `trees.md`) ou usar uma lib            |
| recursão ~10k quadros                                  | pilha explícita                                                 |
| `for...in` em array itera chaves string (e herdadas)   | `for...of` ou `for` indexado                                    |
| typed arrays (`Int32Array`, `Float64Array`)            | muito mais rápidos e compactos para dados numéricos em laços quentes |

## Java

| Armadilha                                                | Correção                                                      |
|----------------------------------------------------------|---------------------------------------------------------------|
| `Integer == Integer` compara referência (funciona até 127 por cache, quebra depois) | `.equals()` ou unboxing (`int`)          |
| boxing em `List<Integer>` / `Map<Integer, Integer>` em laço quente | `int[]`, arrays primitivos, bibliotecas de coleções primitivas |
| `Arrays.sort(int[])` (dual-pivot quicksort) tem pior caso O(n²) com entrada anti-quicksort | embaralhar antes, ou ordenar `Integer[]`/`long[]` via objetos (merge sort) |
| comparator `(a, b) -> a - b` estoura                     | `Integer.compare(a, b)` / `Comparator.comparingInt`           |
| `Stack` e `Vector` legados e sincronizados; `LinkedList` lento | `ArrayDeque` para pilha e fila                         |
| `ArrayDeque` não aceita `null`                           | —                                                             |
| `PriorityQueue.remove(obj)` é O(n); sem decrease-key     | lazy deletion                                                 |
| `ConcurrentModificationException`                        | `Iterator.remove()`, `removeIf`, ou coletar e remover depois  |
| `HashMap` com chave mutável; `equals` sem `hashCode`     | chaves imutáveis (`record`), sobrescrever os dois             |
| `String +=` em laço                                      | `StringBuilder`                                               |
| `Scanner` lento                                          | `BufferedReader` + `StringTokenizer` / `DataInputStream`      |
| recursão profunda → `StackOverflowError`                 | `new Thread(null, runnable, "", 1 << 27).start()` ou iterativo |
| `int` estoura silenciosamente                            | `long`, `Math.addExact`/`multiplyExact` para detectar         |
| `TreeMap`: `floorKey`, `ceilingKey`, `headMap`, `subMap` | já é o ordered map; `TreeMap<Integer, Integer>` como multiset (contador) |

## C++

| Armadilha                                                     | Correção                                                      |
|---------------------------------------------------------------|---------------------------------------------------------------|
| `push_back` invalida iteradores, ponteiros e referências do `vector` | `reserve` antes, ou guardar índices                    |
| `erase` dentro de `for` com `++it`                            | `it = v.erase(it)` no ramo que apaga; ou `erase_if`/remove-erase |
| `map[k]` / `unordered_map[k]` **insere** ao ler               | `find`, `count`, `contains` (C++20)                           |
| `std::lower_bound(set.begin(), set.end(), x)` é O(n)          | `set.lower_bound(x)`                                          |
| `v.size() - 1` com v vazio → `SIZE_MAX`                       | `(int)v.size() - 1` ou checar antes                           |
| `int * int` estoura antes de virar `long long`                | `1LL * a * b`                                                 |
| `1 << 40` é UB                                                | `1LL << 40`                                                   |
| comparator com `<=` → UB/crash em `sort`, `set`               | ordem fraca estrita (`<`)                                     |
| `priority_queue` é **max**-heap por padrão                    | `priority_queue<T, vector<T>, greater<T>>`                    |
| `unordered_map` vulnerável a anti-hash; rehash caro           | hash custom (splitmix64 com seed), `reserve`                  |
| `endl` faz flush toda vez                                     | `'\n'`; `ios::sync_with_stdio(false); cin.tie(nullptr);`      |
| `memset` só funciona byte a byte                              | só 0, −1 ou `0x3f`; para outros valores, `fill`               |
| `vector<bool>` é um proxy de bits (não dá `&v[i]`, é lento em alguns usos) | `vector<char>` ou `bitset`                        |
| passar `vector` por valor em recursão (cópia O(n) por chamada) | `const vector<int>&`                                         |
| recursão profunda (~8 MB de pilha)                            | iterativo, ou aumentar a pilha (`ulimit -s`)                  |
| `std::list` quase nunca vale                                  | `vector`/`deque`                                              |
| `std::deque`: `push_front`/`push_back` invalidam **iteradores** (as referências continuam válidas) | —                          |
| ordered set com rank                                          | `__gnu_pbds::tree<..., tree_order_statistics_node_update>`    |
| variável local não inicializada                               | sempre inicializar; compilar com `-Wall -Wextra -fsanitize=address,undefined` nos testes |

## Go

| Armadilha                                                       | Correção                                                 |
|-----------------------------------------------------------------|----------------------------------------------------------|
| `append` pode compartilhar o array subjacente: `b := a[:2]; b = append(b, x)` sobrescreve `a[2]` | `slices.Clone`, ou full slice expression `a[:2:2]` |
| iteração de `map` em ordem aleatória (de propósito)             | ordenar as chaves                                        |
| `map` não é seguro com concorrência                             | `sync.Mutex` ou `sync.Map`                               |
| `for _, v := range s` copia `v` (structs grandes)               | indexar `s[i]`                                           |
| sem set nativo                                                  | `map[T]struct{}`                                         |
| heap via interface `container/heap` (Push/Pop recebem `any`)    | implemente os 5 métodos; `Pop` remove do **fim** da slice |
| fila com `q = q[1:]` vaza memória (o array cresce sem liberar)  | buffer circular, ou recompactar periodicamente           |
| leitura lenta com `fmt.Scan`                                    | `bufio.NewReader`/`Scanner` com buffer grande            |

## Rust

| Armadilha                                                       | Correção                                                  |
|-----------------------------------------------------------------|-----------------------------------------------------------|
| grafos e árvores com referências brigam com o borrow checker    | arena: `Vec<Node>` + índices `usize`                      |
| `BinaryHeap` é **max**-heap                                     | `Reverse(x)` para min-heap                                |
| `f64` não implementa `Ord` (não entra em heap, sort ou BTreeMap) | `total_cmp`, `ordered_float`, ou inteiros escalados      |
| overflow: panic em debug, wrap em release                       | `checked_*`, `wrapping_*`, `saturating_*` explícitos      |
| `usize` − maior → underflow                                     | `checked_sub` / converter para `i64`                      |
| `HashMap` usa SipHash (seguro, porém mais lento)                | `FxHashMap`/`ahash` quando não há risco de DoS            |
| recursão profunda                                               | pilha explícita ou thread com `stack_size`                |
| `VecDeque`, `BTreeMap` (`range`), `BTreeSet`                    | equivalentes de deque e ordered map/set                   |
| clonar `Vec` em laço                                            | emprestar `&[T]`                                          |

## C#

| Armadilha                                                       | Correção                                                 |
|-----------------------------------------------------------------|----------------------------------------------------------|
| `List.RemoveAt(0)` / `Insert(0, x)` O(n)                        | `Queue<T>`, `LinkedList<T>` ou buffer circular           |
| `PriorityQueue<TElement, TPriority>` (.NET 6+) sem decrease-key e sem remoção arbitrária | lazy deletion                     |
| LINQ em laço quente (alocações, múltiplas enumerações)          | laços explícitos; `ToList()` uma vez                      |
| `struct` como chave sem `Equals`/`GetHashCode` (reflexão lenta) | implementar `IEquatable<T>` ou usar `record struct`       |
| `SortedSet`/`SortedDictionary`: `GetViewBetween`, `Min`, `Max`  | equivalentes de TreeSet/TreeMap                          |
| `string +=`                                                     | `StringBuilder`                                          |
