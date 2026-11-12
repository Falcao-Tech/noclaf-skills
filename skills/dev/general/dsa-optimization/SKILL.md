---
id: 43
name: dsa-optimization
description: "Otimiza estruturas de dados e algoritmos: diagnostica a complexidade, escolhe a estrutura certa por operação (array, deque, hash, heap, árvores balanceadas, B-tree, trie, segment tree, Fenwick, DSU, grafos) e técnicas (prefix sum, two pointers, sliding window, monotonic stack, busca binária, DP, sweep line), combina estruturas em híbridos quando cada operação tem uma vencedora diferente, e decide entre escalar a infraestrutura ou trocar o algoritmo, evitando os bugs clássicos e validando com stress test e benchmark. Use quando código ou sistema estiver lento, der TLE/timeout ou tiver loop quadrático; quando alguém propuser sharding, cache ou mais servidores por desempenho; ao implementar ranking/leaderboard, rate limiter, autocomplete, agendamento ou fila de prioridade; ao escolher, implementar ou revisar estrutura de dados ou algoritmo de grafo; ou em programação competitiva e entrevistas."
effort: high
user-invocable: true
---

# Otimização de Estruturas de Dados e Algoritmos

Objetivo: chegar à **complexidade certa** com a **estrutura certa**, e implementar **sem os bugs clássicos**. Correção vem antes de velocidade: uma solução O(n log n) errada não vale nada.

## Fluxo de trabalho

1. **Medir antes de otimizar (código real).** Faça profiling e ache o hot path. Em apps, o gargalo costuma ser I/O, banco (N+1 queries), alocação ou serialização, e não o algoritmo. Se N é pequeno e fixo, a solução simples ganha.
   - **Antes de propor arquitetura** (shards, réplicas, cache, mais instâncias, filas): verifique se o custo de UMA requisição cresce com n. Se cresce, escalar divide por P e a curva continua a mesma; corrija a complexidade primeiro. Veja `references/systems.md` (diagnóstico, tabela "problema de sistema → estrutura" e quando a arquitetura é, sim, a resposta).
2. **Formalizar o problema.** Defina N (tamanho), Q (nº de operações), quais operações são feitas e **com que frequência** (proporção leitura × escrita), se os dados são estáticos ou mudam, se as consultas são online ou podem ser processadas offline (reordenadas), se aceitam resposta defasada, e qual o limite de memória.
3. **Definir a complexidade-alvo** pela tabela de orçamento abaixo.
4. **Escolher estrutura/técnica por operação.** Use as tabelas "operação → estrutura" e "sinal → técnica" e monte uma tabela de **custo por operação × candidata**, incluindo carga/construção. Pondere pelo perfil: `custo total = construção + Σ frequência(op) × custo(op)`.
   - **Uma vencedora em tudo:** use só ela.
   - **Vencedoras diferentes por operação** (ex.: dict cria e escreve mais rápido, Fenwick consulta mais rápido): avalie um **híbrido**, em que cada operação vai para a estrutura mais barata para ela e a sincronização é paga no momento mais barato. Opções: construção adiada com ski rental, decisão por fase, buffer de escrita com flush escolhendo entre incremental e rebuild, ou duas representações sincronizadas.
   - O híbrido só vale se o custo de sincronizar for menor que o ganho. Ele costuma ganhar quando a fase muda (carga → leitura, lote → leitura) e perder em regime estável. Meça os dois cenários. Detalhes, padrões e caso medido em `references/systems.md` (seções leitura × escrita e estrutura por operação).
5. **Preferir a biblioteca padrão** (TreeMap, `std::map`, `heapq`, `sortedcontainers`, `ArrayDeque`...). Implemente à mão só quando ela não existe na linguagem, quando precisa de uma operação extra (rank, augmentação, lazy) ou quando o usuário pede.
6. **Escrever as invariantes** antes do código, como comentário curto: o que `lo`/`hi` significam, o que cada nó guarda, o que está na pilha.
7. **Verificar a correção.** Faça stress test contra força bruta com entradas aleatórias pequenas (`scripts/stress_test.py`), mais os casos de borda da checklist. Para estruturas com estado, gere **sequências de operações** (veja "Como usar o stress test"). Para árvores balanceadas, rode um verificador de invariantes depois de cada operação nos testes.
8. **Medir o ganho.** Rode `scripts/bench_scaling.py` com as duas versões em n, 2n, 4n…: ele estima o expoente k (t ≈ c·nᵏ) e a razão entre as versões no maior n. Confirma o big-O na prática em vez de só afirmá-lo.
9. **Reportar** a complexidade antes e depois (tempo e memória), os números medidos **por operação e no total**, os trade-offs (o que piora: escrita, memória, construção inicial, p99) e as premissas (ex.: "pesos não-negativos", "leituras dominam").

## Orçamento de complexidade

Referência: cerca de 10⁸ operações simples/s em C++/Rust/Go/Java e cerca de 10⁷/s em Python/JS puro.

| N máximo       | Complexidade viável        | Técnicas típicas                              |
|----------------|----------------------------|-----------------------------------------------|
| ≤ 10–11        | O(n!)                      | permutações, backtracking                     |
| ≤ 20–25        | O(2ⁿ·n)                    | bitmask DP, subsets                           |
| ≤ 40           | O(2^(n/2))                 | meet in the middle                            |
| ≤ 500          | O(n³)                      | Floyd-Warshall, DP intervalar                 |
| ≤ 5 000        | O(n²)                      | DP 2D, pares                                  |
| ≤ 10⁵–10⁶      | O(n log n) / O(n √n)       | sort, heap, BST, segment tree, Mo's           |
| ≤ 10⁷–10⁸      | O(n)                       | prefix sums, two pointers, monotonic, hashing |
| > 10⁸          | O(log n) / O(1)            | matemática, busca binária, fórmula fechada    |

## Operação → estrutura

| Preciso de...                                         | Use                                         | Custo                    |
|-------------------------------------------------------|---------------------------------------------|--------------------------|
| acesso por índice, iteração rápida                    | array / vetor dinâmico                      | O(1), amortizado no push |
| LIFO (desfazer, DFS, parênteses)                      | stack sobre array                           | O(1)                     |
| FIFO (BFS, jobs)                                      | deque / buffer circular (**nunca** `pop(0)`/`shift()`) | O(1)          |
| inserir/remover nas duas pontas                       | deque                                       | O(1)                     |
| pertence?, contagem, agrupamento, dedup               | hash set / hash map                         | O(1) médio               |
| min/max repetido com inserções                        | heap (priority queue)                       | O(log n)                 |
| top-k de um stream                                    | heap de tamanho k (min-heap para os k maiores) | O(n log k)            |
| ordem + predecessor/sucessor/range                    | árvore balanceada (TreeMap, `std::set`)     | O(log n)                 |
| k-ésimo elemento / rank dinâmico / leaderboard        | Fenwick sobre o valor (receita em `trees.md`), order-statistic tree | O(log n) |
| dados em disco/páginas, índices                       | B-tree / B+tree                             | O(log_B n) I/Os          |
| busca por prefixo, autocomplete, XOR máximo           | trie (binary trie para XOR)                 | O(comprimento)           |
| soma de intervalo, array estático                     | prefix sum                                  | O(1) query               |
| soma de intervalo com updates pontuais                | Fenwick (BIT)                               | O(log n)                 |
| query de intervalo com op associativa + updates em range | segment tree (+ lazy)                    | O(log n)                 |
| min/max/gcd de intervalo, array estático              | sparse table                                | O(1) query               |
| componentes conexos dinâmicos (só uniões)             | DSU / union-find                            | ≈O(α(n))                 |
| LRU cache                                             | hash map + lista duplamente ligada          | O(1)                     |
| máx/mín de janela deslizante                          | monotonic deque                             | O(1) amortizado          |
| próximo maior/menor elemento                          | monotonic stack                             | O(1) amortizado          |

## Sinal no problema → técnica

| Sinal                                                      | Técnica                                    |
|------------------------------------------------------------|--------------------------------------------|
| "soma/contagem em subarray/intervalo", muitas queries       | prefix sum (+ hash map p/ "soma = k")       |
| muitos updates de intervalo, uma leitura no fim             | difference array                           |
| array ordenado / par com soma alvo / remover duplicatas     | two pointers                               |
| "maior/menor subarray contíguo que satisfaz X" com X monotônico | sliding window                         |
| "mínimo valor tal que é possível…" (predicado monotônico)   | busca binária na resposta                  |
| intervalos, eventos, sobreposição, linha do tempo           | sort + sweep line                          |
| valores enormes mas poucos distintos                        | coordinate compression                     |
| subproblemas repetidos / escolhas ótimas                    | DP (memo → tabulação → rolling array)      |
| escolha local provável por troca (exchange argument)        | greedy (exija prova ou contraexemplo testado) |
| comparar substrings rápido                                  | rolling hash / Z / KMP / suffix array      |
| loop aninhado buscando "existe um igual"                    | hash map (troca O(n²) por O(n))            |
| `sort` repetido dentro de loop                              | heap ou estrutura ordenada                 |
| recalcular agregado a cada passo                            | manter incremental (janela, prefix, contador) |
| queries offline em intervalos sem estrutura óbvia           | Mo's algorithm / sqrt decomposition        |
| grafo: menor caminho, dependências, conectividade           | ver `references/graphs.md`                 |

## Quadráticos escondidos (o achado mais comum em código real)

- `x in list` / `list.index` / `array.includes` / `indexOf` dentro de loop → converta para set/map antes.
- `list.pop(0)`, `array.shift()`, `list.insert(0, x)`, `ArrayList.remove(0)` → O(n) cada; use deque.
- Concatenar string em loop → `join` / `StringBuilder`.
- `arr = [...arr, x]` / `concat` / slicing dentro de loop → O(n) por iteração.
- Join de duas coleções com loop aninhado → indexe uma delas num hash map.
- Ordenar a lista inteira para pegar o mínimo a cada iteração → heap.
- `erase` repetido no meio de vetor → remove-erase idiom / filtro em uma passada / swap-and-pop.
- Query ao banco dentro de loop (N+1) → batch / `IN (...)` / join.

## Checklist universal de bugs (revise SEMPRE)

1. **Off-by-one.** Decida intervalo fechado `[l, r]` ou semiaberto `[l, r)` e não misture. Prefira semiaberto.
2. **Estrutura vazia.** pop/peek/top em vazio, `max()` de lista vazia, `v.size() - 1` com `size_t` em C++ (vira enorme).
3. **Overflow.** `mid = lo + (hi - lo) / 2`. Soma de produtos 10⁵·10⁵ estoura `int32`. `INF + w` estoura; use INF ≈ 10¹⁸ em `long` e cheque `dist[u] != INF` antes de relaxar.
4. **Módulo de negativo.** Em C/C++/Java/JS/Go, `-1 % n` é negativo; use `((x % n) + n) % n`. Python já devolve positivo.
5. **Aliasing.** `[[0]*m]*n` (Python), `new Array(n).fill([])` (JS) e `append` em slices compartilhados (Go) fazem as linhas compartilharem o mesmo objeto.
6. **Modificar enquanto itera.** Invalida iteradores (C++ `push_back`/`erase`, Java `ConcurrentModificationException`, Python dict/set mudando de tamanho).
7. **Recursão profunda.** DFS em grafo/árvore degenerada com 10⁵ nós estoura a pilha (Python ~1000 de limite, JS ~10k, C++ ~8 MB). Use pilha explícita.
8. **Ordem de atualização de ponteiros.** Ligue os ponteiros novos antes de cortar os antigos; em rotação AVL, atualize a altura do filho antes do pai.
9. **Comparator inválido.** Precisa ser ordem fraca estrita (`<`, nunca `<=`); `a - b` como comparator estoura.
10. **Igualdade e hash.** Chave mutável dentro de hash/árvore; `equals` sem `hashCode` (Java); float como chave.
11. **Grafo desconexo.** BFS/DFS a partir de um só nó ignora as outras componentes; percorra todos os vértices.
12. **Grafo não-direcionado:** adicione as duas direções da aresta. Grafo direcionado: só uma.
13. **Marcar visitado ao enfileirar** (BFS), não ao desenfileirar, senão a fila explode com duplicatas.
14. **Duplicatas.** Busca binária (lower vs upper bound), monotonic stack (estrito de um lado só), trie (contador em vez de booleano), BST (política explícita).
15. **Estado global não resetado** entre casos de teste (múltiplos testes por entrada).
16. **Float.** Não compare com `==`; busca binária em reais roda número fixo de iterações (~100) em vez de `while hi - lo > eps`.
17. **Pior caso adversarial.** Quicksort sem pivô aleatório, hash previsível (hash flooding), BST sem balanceamento com entrada ordenada.

## Arquivos de referência (leia sob demanda)

- `references/linear.md`: arrays dinâmicos, listas ligadas (sentinela), stack, fila, buffer circular, deque, monotonic stack/deque, hash table. Código + bugs.
- `references/trees.md`: BST, AVL, red-black, treap, B-tree/B+tree, heap, trie/radix, segment tree (+lazy), Fenwick, sparse table, DSU, LCA. Código, invariantes e verificadores.
- `references/graphs.md`: representações, variantes (direcionado, não-direcionado, ponderado, multigrafo, DAG, implícito/grid), BFS/0-1 BFS/DFS, ciclos, toposort, Dijkstra, Bellman-Ford, Floyd, MST, SCC, pontes/articulações, bipartição, fluxo.
- `references/techniques.md`: prefix sums (1D/2D/XOR/hash), difference array, two pointers, sliding window, busca binária, sweep line, coordinate compression, DP e otimizações de DP, rolling hash, sqrt/Mo's, bits, otimização de constante (cache, alocação, I/O).
- `references/systems.md`: escalar × otimizar. Diagnóstico antes de propor infraestrutura, tabela "problema de sistema → estrutura" (leaderboard, rate limiter, autocomplete, agendamento, dedup, janelas de tempo, proximidade, percentis…), custo ponderado por leitura × escrita, quando a arquitetura é a resposta certa (e particionar mantendo a estrutura certa em cada shard), memória por estrutura em Python e um caso medido.
- `references/language-pitfalls.md`: armadilhas por linguagem (Python, Django/ORM, JS/TS, Java, C++, Go, Rust, C#).
- `scripts/stress_test.py`: compara a solução rápida com a força bruta em entradas aleatórias, imprime o primeiro contraexemplo com a seed para reproduzir e sai com código 1.
- `scripts/bench_scaling.py`: mede uma ou mais implementações em tamanhos crescentes, estima o expoente da complexidade e compara as versões.

Base teórica: Cormen et al., *Algoritmos: Teoria e Prática* (CLRS), para invariantes, provas e casos de RB-tree, B-tree, DSU e caminhos mínimos. Base prática: *Competitive Programmer's Handbook* (Laaksonen), para orçamento de complexidade, sort vs estruturas, técnicas de árvore, sqrt e segment trees avançadas. Os códigos das referências foram validados contra força bruta em testes aleatórios.

## Como usar o stress test

```bash
python scripts/stress_test.py --fast sol.py:fast --brute sol.py:brute --gen sol.py:gen --iters 2000
```

`gen(rng)` recebe um `random.Random` e devolve uma tupla de argumentos. Flags: `--seed N` reproduz um caso, `--unordered` compara listas sem ordem e `--float-tol 1e-9` compara floats com tolerância. Gere entradas **pequenas** (n ≤ 8, valores em faixa curta, incluindo negativos, zeros e duplicatas): é assim que os contraexemplos aparecem. Os argumentos são copiados com deep copy antes de cada chamada, então funções que mutam a entrada não contaminam a comparação.

**Estruturas com estado** (cache, ranking, fila de prioridade, árvore): `gen` devolve um estado inicial e uma **lista de operações**. `fast` e `brute` constroem cada uma a sua estrutura, reproduzem as operações e devolvem a lista de respostas das consultas:

```python
def gen(rng):
    max_v = rng.choice([0, 1, 3, 7])                 # domínio minúsculo força empates e bordas
    n = rng.randint(1, 6)
    ops = []
    for _ in range(rng.randint(1, 15)):
        r = rng.random()
        if r < 0.5:   ops.append(("set", rng.randrange(n + 2), rng.randint(0, max_v)))  # inclui id novo
        elif r < 0.8: ops.append(("rank", rng.randrange(n)))
        else:         ops.append(("top", rng.randint(0, n + 3)))                      # k > n
    return max_v, [(i, rng.randint(0, max_v)) for i in range(n)], ops

def _replay(cls, max_v, initial, ops):
    b = cls(max_v)
    for i, v in initial: b.set(i, v)
    return [getattr(b, op)(*args) for op, *args in ops]   # set devolve None; consultas, a resposta

def fast(*a):  return _replay(RankBoard, *a)
def brute(*a): return _replay(NaiveBoard, *a)
```

Inclua no gerador: repetir a mesma escrita (set com o valor atual), ids inexistentes, remoção do último elemento, k = 0 e k > n.

## Como medir o ganho

```bash
python scripts/bench_scaling.py --impl sol.py:fast --impl sol.py:brute --gen sol.py:gen_n --start 1000 --steps 6
```

`gen_n(rng, n)` devolve os argumentos para o tamanho n. O script imprime o tempo por n (melhor de `--repeat`), o expoente k entre passos e o ajuste geral (k≈0: O(1)/O(log n); k≈1: O(n)/O(n log n); k≈2: O(n²)), e a razão entre as versões no maior n. Uma versão deixa de ser medida quando um passo passa de `--max-time` segundos. Confie mais nos passos grandes, porque com n pequeno o overhead fixo puxa k para baixo.

## Princípios

- A estrutura certa costuma valer mais que micro-otimização. Depois de acertar o big-O, olhe a constante: localidade de cache (arrays > ponteiros), menos alocação, sem boxing, I/O em buffer.
- O(1) amortizado não é O(1) no pior caso. Se latência importa (tempo real), considere o pico do rehash ou do resize.
- Complexidade média não é pior caso. Hash e quicksort podem degradar com entrada adversária.
- Não implemente red-black ou B-tree à mão se a linguagem tem uma pronta. Se precisar de árvore balanceada própria (augmentação), prefira treap ou AVL, que são mais simples de acertar.
- Toda otimização precisa manter um teste de equivalência contra a versão simples.
- Escolha a estrutura por operação, não por problema. Se a simples ganha na criação e na escrita e a indexada ganha na consulta, considere usar as duas. Mas some o custo de sincronizar e compare o tempo total. O trabalho adiado muda de lugar (normalmente para a primeira leitura e para o p99), não desaparece.
- Escalar divide o trabalho por P; a estrutura certa elimina trabalho. Proponha arquitetura quando o custo por requisição já é O(1)/O(log n), quando os dados não cabem numa máquina ou quando o motivo é disponibilidade. Mesmo assim, use a estrutura certa dentro de cada partição.
