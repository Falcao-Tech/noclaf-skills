# Grafos

Referência teórica: CLRS cap. 22 (busca elementar), 23 (MST), 24 (caminhos mínimos de fonte única), 25 (todos os pares), 26 (fluxo).

Índice: [Variantes](#variantes-de-grafo) · [Representação](#representação) · [BFS](#bfs-clrs-222) · [DFS](#dfs-clrs-223) · [Ciclos](#detecção-de-ciclo) · [Toposort](#ordenação-topológica-clrs-224) · [Caminhos mínimos](#caminhos-mínimos-clrs-2425) · [MST](#mst-clrs-23) · [SCC](#componentes-fortemente-conexas-clrs-225) · [Pontes e articulações](#pontes-e-pontos-de-articulação) · [Bipartição](#bipartição) · [Fluxo](#fluxo-máximo-e-matching-clrs-26) · [Euler](#caminho-euleriano) · [Checklist](#checklist-de-grafos)

---

## Variantes de grafo

| Variante              | Detalhe que muda a implementação                                                             |
|-----------------------|----------------------------------------------------------------------------------------------|
| **Não-direcionado**   | adicionar `u→v` **e** `v→u`; cada aresta aparece 2× na lista; o grau soma 2·m                 |
| **Direcionado**       | uma direção só; existem grau de entrada e de saída; "conexo" vira fraca ou fortemente conexo |
| **Ponderado**         | guardar `(v, w)`; checar se há pesos negativos e qual algoritmo isso permite                  |
| **Multigrafo**        | arestas paralelas: identificar por **id**, não por par `(u, v)`; o grau conta multiplicidade  |
| **Com self-loops**    | `u→u` é ciclo no direcionado e aresta de retorno na DFS (CLRS 22.3); conta 2 no grau do não-direcionado |
| **DAG**               | admite toposort, DP em ordem topológica e caminho mínimo/máximo em O(V+E) com qualquer peso   |
| **Árvore**            | n−1 arestas, conexo, acíclico; dá para usar "pai" em vez de `visited`                         |
| **Bipartido**         | sem ciclos ímpares; matching via fluxo / Hopcroft-Karp                                        |
| **Implícito / grid**  | os vizinhos são gerados na hora (4 ou 8 direções, estados); checar limites antes de indexar  |
| **Denso vs esparso**  | E ≈ V² → matriz e Dijkstra O(V²); E ≈ V → lista de adjacência e heap                         |

---

## Representação

| Estrutura              | Memória  | Vizinhos de u | Existe (u,v)?                | Quando usar                                     |
|------------------------|----------|---------------|------------------------------|-------------------------------------------------|
| Lista de adjacência    | O(V+E)   | O(grau)       | O(grau)                      | padrão; grafos esparsos                         |
| Matriz de adjacência   | O(V²)    | O(V)          | O(1)                         | V ≤ ~5000, densos, Floyd-Warshall               |
| Lista de arestas       | O(E)     | n/a           | n/a                          | Kruskal, Bellman-Ford                           |
| CSR (offsets + destinos)| O(V+E)  | O(grau)       | O(log grau) se ordenado      | grafos grandes e estáticos; melhor localidade de cache |
| Set por vértice        | O(V+E)   | O(grau)       | O(1) médio                   | quando precisa de "existe aresta?" e remoções   |

Para fluxo, guarde as arestas num array, com a reversa em `e ^ 1` (adicione sempre em pares).

```python
def build_adj(n, edges, directed=False):
    adj = [[] for _ in range(n)]          # NUNCA [[]] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        if not directed: adj[v].append((u, w))
    return adj
```

**Bugs:** vértices em base 1 na entrada e array de tamanho n (crie `n + 1` ou converta); `[[]] * n`; esquecer a direção reversa no grafo não-direcionado; matriz V² com V = 10⁵ (são 10¹⁰ células).

---

## BFS (CLRS 22.2)

Dá a distância mínima **em número de arestas** (grafo sem peso) em O(V+E).

```python
from collections import deque
def bfs(adj, sources):
    dist = [-1] * len(adj)
    q = deque()
    for s in sources:                 # multi-source: todas as fontes com distância 0
        dist[s] = 0; q.append(s)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:         # marca AO ENFILEIRAR
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

**Bugs:** marcar como visitado ao **desenfileirar** (o mesmo nó entra várias vezes na fila; no grid, a fila explode); `list.pop(0)`; não checar os limites do grid antes de `grid[r][c]`; BFS em grafo ponderado (dá resposta errada; use 0-1 BFS ou Dijkstra); estado incompleto em BFS sobre estados (ex.: `(pos, chaves_coletadas)`, e não só `pos`).

**0-1 BFS** (pesos 0 ou 1) em O(V+E): peso 0 vai para a **frente** do deque, peso 1 para o fim.

```python
def bfs01(adj, s):
    INF = float("inf"); dist = [INF] * len(adj); dist[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0: dq.appendleft(v)
                else: dq.append(v)
    return dist
```

Generalização: pesos inteiros pequenos 0..K → Dial's algorithm (buckets).

---

## DFS (CLRS 22.3)

**Classificação de arestas (CLRS 22.3):**
- **árvore:** descobre um vértice novo (branco);
- **retorno (back):** vai para um ancestral ainda na pilha (cinza). Self-loops contam como retorno;
- **avanço (forward):** vai para um descendente já terminado;
- **cruzada (cross):** todo o resto.

No grafo **não-direcionado**, toda aresta é de árvore ou de retorno: não existem avanço nem cruzada.

**Lema 22.11:** um grafo direcionado é acíclico ⇔ a DFS não produz arestas de retorno.

**DFS iterativa que simula a recursão** (tempos de entrada e saída, pós-ordem), sem risco de estouro de pilha:

```python
def dfs_iter(adj, n):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n; order_out = []          # order_out = pós-ordem (tempo de término)
    for s in range(n):                           # todas as componentes
        if color[s] != WHITE: continue
        color[s] = GRAY
        stack = [(s, 0)]                         # (vértice, índice do próximo vizinho)
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if color[v] == WHITE:
                    color[v] = GRAY; stack.append((v, 0))
                # elif color[v] == GRAY: aresta de retorno → ciclo (grafo direcionado)
            else:
                color[u] = BLACK; order_out.append(u); stack.pop()
    return order_out
```

**Bugs:** a DFS iterativa ingênua (`pop`, depois empilhar todos os vizinhos) **não** dá pós-ordem nem tempos corretos, porque marca na hora errada. Use o padrão `(u, idx)` acima. Outros: recursão profunda (Python: limite ~1000, e `setrecursionlimit` sem aumentar a pilha da thread dá segfault); iniciar só de 0 em grafo desconexo.

---

## Detecção de ciclo

| Grafo             | Método                                                                                  | Armadilha                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Direcionado       | DFS 3 cores: aresta para **cinza** = ciclo; ou Kahn (`len(ordem) < n`)                   | tratar **preto** (já terminado) como ciclo: preto é aresta de avanço/cruzada, não ciclo     |
| Não-direcionado   | DFS ignorando a **aresta** de onde veio; ou DSU (`union` devolve False = ciclo)          | ignorar o **vértice** pai quebra com arestas paralelas (u-v duas vezes **é** ciclo)         |
| Lista ligada / função `f(x)` | Floyd (tartaruga e lebre) ou Brent                                         | —                                                                                           |

DFS no não-direcionado com id de aresta:
```python
def has_cycle_undirected(n, edges):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i)); adj[v].append((u, i))
    seen = [False] * n
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; stack = [(s, -1)]
        while stack:
            u, pe = stack.pop()
            for v, eid in adj[u]:
                if eid == pe: continue                 # pula a MESMA aresta, não o vértice pai
                if seen[v]: return True
                seen[v] = True; stack.append((v, eid))
    return False
```
(Nessa variante com pilha simples, `seen[v]` já marcado indica ciclo porque cada vértice é empurrado uma única vez, por uma única aresta de árvore. Self-loop `u-u` também é detectado.)

---

## Ordenação topológica (CLRS 22.4)

**Kahn (BFS por grau de entrada):**
```python
def topo_kahn(n, adj):
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]: indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return order if len(order) == n else None    # None → há ciclo
```

**DFS (CLRS):** a ordem topológica é a **pós-ordem invertida** (ordem decrescente de tempo de término).

**Bugs:** usar a pré-ordem da DFS (errado); esquecer de inverter a pós-ordem; contar o grau de entrada de forma diferente do decremento em multigrafos (se uma aresta repetida é contada 2× na entrada, precisa ser decrementada 2×; deduplique as arestas ou trate de forma consistente); confundir a direção da dependência ("a depende de b" é aresta `b → a` para que b venha antes). Menor ordem topológica lexicográfica: troque a fila por um min-heap. Os nós que sobram quando há ciclo incluem os que só **dependem** do ciclo, não apenas os que estão nele.

**DP em DAG:** processe na ordem topológica. Caminho mínimo ou **máximo** de fonte única em O(V+E) com pesos quaisquer (CLRS 24.2). O caminho mais longo é NP-difícil em grafos gerais, mas linear em DAG.

---

## Caminhos mínimos (CLRS 24–25)

**Qual usar:**

| Situação                                         | Algoritmo                       | Complexidade                      |
|--------------------------------------------------|---------------------------------|-----------------------------------|
| sem peso                                         | BFS                             | O(V+E)                            |
| pesos 0/1                                        | 0-1 BFS                         | O(V+E)                            |
| DAG, qualquer peso                               | DP em ordem topológica          | O(V+E)                            |
| pesos **≥ 0**, esparso                           | Dijkstra + binary heap          | O((V+E) log V)                    |
| pesos ≥ 0, **denso** (E ≈ V²)                    | Dijkstra com array, sem heap    | O(V²) (CLRS 24.3)                 |
| pesos negativos, ciclo negativo possível         | Bellman-Ford                    | O(V·E)                            |
| todos os pares, V ≤ ~500                         | Floyd-Warshall                  | O(V³)                             |
| todos os pares, esparso, com negativos           | Johnson (BF + V × Dijkstra)     | O(V·E log V)                      |

**Fundamentos (CLRS 24):** caminhos mínimos têm subestrutura ótima, e todos os algoritmos são sequências de **relaxamento**: `if d[u] + w < d[v]: d[v] = d[u] + w; pai[v] = u`. Se existe um ciclo negativo alcançável a partir de s, a distância é −∞ para os vértices alcançáveis por ele, e "caminho mínimo" deixa de estar definido.

### Dijkstra (lazy deletion)

```python
import heapq
def dijkstra(adj, s):
    INF = float("inf")
    dist = [INF] * len(adj); dist[s] = 0
    parent = [-1] * len(adj)
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue           # entrada desatualizada: ESSENCIAL
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd; parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent
```

**Bugs clássicos:**
- **Pesos negativos:** Dijkstra supõe que, ao extrair u, `dist[u]` é final (CLRS 24.3 exige pesos não-negativos). Com uma aresta negativa, a resposta fica errada em silêncio. Valide os pesos na entrada.
- Esquecer a checagem de entrada desatualizada: fica correto, mas reprocessa vizinhos, e pode virar O(E²) em grafos adversariais.
- Marcar `visited` ao **empurrar** em vez de ao extrair: resposta errada.
- `INF` como `INT_MAX` e `INF + w` estoura. Use `10**18` com `long long`, ou cheque `dist[u] != INF`.
- Heap com tupla `(dist, nó)` quando o nó é um objeto não comparável: use um id inteiro.
- Para "caminho até um alvo", pode parar quando o **alvo é extraído**, não quando é empurrado.
- Reconstruir o caminho: siga `parent` a partir do alvo e **inverta**. Cheque se o alvo é alcançável (`dist == INF`).

**Variantes:** K-ésimo menor caminho (cada nó pode ser extraído até k vezes); Dijkstra em grafo de estados `(nó, recurso)`; minimax/bottleneck (troque `+` por `max`); A* com heurística admissível (se a heurística não for consistente, é preciso permitir reabrir nós).

### Bellman-Ford (CLRS 24.1)

```python
def bellman_ford(n, edges, s):
    INF = float("inf"); dist = [INF] * n; dist[s] = 0
    for _ in range(n - 1):                   # V-1 rodadas
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w; changed = True
        if not changed: break                # saída antecipada
    # a V-ésima passada é a CHECAGEM de ciclo negativo
    neg = [False] * n
    for _ in range(n):                       # propaga −∞ para tudo alcançável pelo ciclo
        for u, v, w in edges:
            if dist[u] != INF and (neg[u] or dist[u] + w < dist[v]):
                neg[v] = True
    return dist, neg
```

**Bugs:** relaxar a partir de `dist[u] == INF` (INF − 5 < INF "melhora" e corrompe a distância); fazer V rodadas e depois checar (são V−1 mais a checagem); achar que detecta ciclo negativo **não alcançável** a partir de s (não detecta; para detectar em qualquer lugar, inicialize todos com 0 ou use um super-nó); grafo não-direcionado com aresta negativa (ela vira um ciclo negativo u→v→u sozinha). SPFA (BF com fila) é rápido em média, mas tem pior caso O(VE) e cai com testes adversariais.

### Floyd-Warshall (CLRS 25.2)

`d[i][j]` usando só os vértices intermediários `{0..k}`. **O laço de k é o mais externo.**

```python
INF = float("inf")
def floyd(d):               # d[i][j] = peso, INF sem aresta, d[i][i] = 0
    n = len(d)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF: continue
            di = d[i]
            for j in range(n):
                if dik + dk[j] < di[j]: di[j] = dik + dk[j]
    # ciclo negativo ⇔ algum d[i][i] < 0
```

**Bugs:** colocar `k` dentro dos laços de i/j (resposta errada); `d[i][i]` não inicializado com 0; arestas paralelas sobrescrevendo com o maior peso (use `min`); INF + INF estourando.

---

## MST (CLRS 23)

Vale a **propriedade do corte** (CLRS 23.1): a aresta mais leve que cruza qualquer corte que respeite a floresta atual é segura.

**Kruskal:** ordene as arestas e use DSU. O(E log E). Bom para grafos esparsos.
```python
def kruskal(n, edges):              # edges: (w, u, v); DSU de references/trees.md
    dsu = DSU(n); total = 0; used = []
    for w, u, v in sorted(edges):
        if dsu.union(u, v):
            total += w; used.append((u, v, w))
    return total if len(used) == n - 1 else None   # None → grafo desconexo (floresta)
```

**Prim:** com heap e lazy deletion, O(E log V); com array em grafo denso, O(V²).

**Bugs:** não detectar grafo desconexo; Prim com lazy sem checar `if in_mst[v]: continue` ao extrair; usar MST para "caminho mínimo" (são problemas diferentes); MST em grafo **direcionado** (o problema certo é arborescência mínima, Chu-Liu/Edmonds).

---

## Componentes fortemente conexas (CLRS 22.5)

**Kosaraju (CLRS):** (1) faça uma DFS em G e registre os tempos de término; (2) faça uma DFS no **transposto** Gᵀ, processando os vértices em ordem **decrescente** de término; cada árvore dessa segunda DFS é uma SCC. O grafo de componentes resultante é um DAG.

**Tarjan:** uma DFS com `tin`, `low`, pilha e `on_stack`.
- **Bug clássico:** atualizar `low[u] = min(low[u], tin[v])` para um `v` já visitado **mas fora da pilha**, que pertence a uma SCC já fechada. Só atualize se `on_stack[v]`.
- Remova os vértices da pilha **até u inclusive** quando `low[u] == tin[u]`, e marque `on_stack = False` em cada um.

Uso: 2-SAT (x e ¬x na mesma SCC ⇒ insatisfazível), condensação para DP em DAG.

---

## Pontes e pontos de articulação

Grafo não-direcionado, com `tin` (tempo de entrada) e `low` (menor `tin` alcançável pela subárvore usando no máximo uma aresta de retorno).

- Aresta (u, v) de árvore é **ponte** ⇔ `low[v] > tin[u]` (estrito).
- u é **ponto de articulação** ⇔ (u não é raiz e existe filho v com `low[v] >= tin[u]`) **ou** (u é raiz da DFS e tem ≥ 2 filhos **na árvore DFS**).

```python
import sys
def bridges(n, edges):
    sys.setrecursionlimit(1 << 20)   # para n grande, converta para iterativa (padrão (u, idx))
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i)); adj[v].append((u, i))
    tin = [-1] * n; low = [0] * n; timer = 0; res = []
    def dfs(u, pe):
        nonlocal timer
        tin[u] = low[u] = timer; timer += 1
        for v, eid in adj[u]:
            if eid == pe: continue                 # id da aresta: arestas paralelas NÃO são pontes
            if tin[v] == -1:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]: res.append(eid)
            else:
                low[u] = min(low[u], tin[v])
    for u in range(n):
        if tin[u] == -1: dfs(u, -1)
    return res
```

**Bugs:** usar `>=` para ponte ou `>` para articulação; tratar a raiz como um vértice comum; contar como filhos da raiz os vizinhos em vez dos filhos na árvore; pular o vértice pai em vez da aresta (com arestas paralelas, uma "ponte" falsa aparece).

---

## Bipartição

BFS/DFS colorindo com 2 cores; um conflito (vizinho com a mesma cor) indica ciclo ímpar. **Percorra todas as componentes.** Também dá para usar DSU com paridade.

---

## Fluxo máximo e matching (CLRS 26)

- Ford-Fulkerson com DFS: O(E·|f*|), que só é aceitável com capacidades pequenas. **Edmonds-Karp** (BFS): O(V·E²). **Dinic:** O(V²·E) e O(E√V) em redes de capacidade unitária (matching bipartido). É o padrão prático.
- **Residual:** toda aresta tem uma reversa com capacidade 0. Guarde em pares (`e` e `e ^ 1`) para achar a reversa em O(1).
- **Bugs:** esquecer a aresta reversa (o algoritmo não consegue "desfazer" fluxo e dá resultado errado); aresta não-direcionada modelada como duas arestas sem reversas próprias (dá para usar um par com capacidade c nos dois sentidos); no Dinic, esquecer o ponteiro `it[u]` por fase, o que deixa o algoritmo exponencial na prática; INF de capacidade estourando ao somar.
- Teorema max-flow min-cut: depois do fluxo máximo, os vértices alcançáveis no residual a partir de s formam o lado S do corte mínimo.
- Matching bipartido: fluxo com capacidades 1, ou Hopcroft-Karp. Custo mínimo: MCMF com Bellman-Ford/SPFA ou Dijkstra com potenciais.

---

## Caminho euleriano

- Não-direcionado: circuito ⇔ todos os graus pares; caminho ⇔ exatamente 0 ou 2 vértices de grau ímpar.
- Direcionado: circuito ⇔ `in = out` em todos; caminho ⇔ um vértice com `out − in = 1`, um com `in − out = 1` e os demais iguais.
- E sempre: todas as arestas numa única componente conexa (ignorando vértices isolados).
- Hierholzer O(E): marque as arestas usadas **por id** (no não-direcionado as duas direções compartilham o id) e use um ponteiro por vértice para não varrer a adjacência de novo.

---

## Checklist de grafos

- [ ] Direcionado ou não? Base 0 ou 1? Pode ter arestas paralelas ou self-loops?
- [ ] Pode ser desconexo? O laço externo cobre todos os vértices?
- [ ] Pesos: negativos? zero? o tamanho cabe em 32 bits? qual INF?
- [ ] V e E máximos → lista ou matriz? Recursão ou pilha explícita?
- [ ] BFS marca ao enfileirar? Dijkstra descarta entradas desatualizadas?
- [ ] Ciclo: 3 cores (direcionado) vs aresta de origem por id (não-direcionado)?
- [ ] O estado da busca inclui tudo que influencia o futuro (BFS/Dijkstra sobre estados)?
- [ ] Testou com: 1 vértice, sem arestas, grafo completo, linha (caminho) longa (profundidade), estrela (grau alto), componentes múltiplas, arestas paralelas?
