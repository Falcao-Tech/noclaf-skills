# Estruturas não-lineares: árvores e afins

Referência teórica: Cormen et al., *Algoritmos: Teoria e Prática*, 3ª ed. (CLRS). Os capítulos estão citados em cada seção.

Índice: [Fundamentos](#fundamentos) · [BST](#bst-clrs-cap-12) · [AVL](#avl) · [Red-black](#red-black-clrs-cap-13) · [Treap](#treap) · [Augmentação](#augmentação-clrs-cap-14) · [B-tree / B+tree](#b-tree-e-btree-clrs-cap-18) · [Heap](#heap-clrs-cap-6) · [Trie](#trie-e-radix-tree) · [Segment tree](#segment-tree) · [Fenwick](#fenwick-tree-bit) · [Rank dinâmico](#receita-rank-dinâmico-por-valor-leaderboard) · [Sparse table](#sparse-table) · [DSU](#dsu--union-find-clrs-cap-21) · [LCA](#lca-com-binary-lifting)

---

## Fundamentos

- Árvore com n nós tem n−1 arestas. A altura determina o custo: balanceada O(log n), degenerada O(n).
- **Representações:** ponteiros (`left`/`right`/`parent`); array implícito (heap, segment tree); arrays paralelos `left[]`, `right[]` sobre um pool de índices (rápido, sem GC, fácil de serializar; é a melhor opção em Rust); lista de adjacência (árvore genérica como grafo); `parent[]`.
- **Recursão:** árvore degenerada (ex.: BST com entrada ordenada) tem profundidade n e estoura a pilha. Prefira travessias iterativas ou garanta balanceamento.
- **Travessia em ordem iterativa:**
  ```python
  def inorder(root):
      st, cur, out = [], root, []
      while st or cur:
          while cur: st.append(cur); cur = cur.left
          cur = st.pop(); out.append(cur.key); cur = cur.right
      return out
  ```
- **Testar com verificador de invariantes**: depois de cada operação nos testes, cheque a ordem BST, a consistência dos ponteiros `parent` e as invariantes de balanceamento. Um bug de balanceamento quase nunca aparece como resultado errado imediato; ele aparece como árvore degenerada mais tarde.

---

## BST (CLRS cap. 12)

- Busca, inserção e remoção custam O(h). Sem balanceamento, inserir em ordem crescente produz uma lista (h = n). Uma BST construída aleatoriamente tem altura esperada O(log n) (CLRS 12.4), mas não conte com entrada aleatória.
- **Remoção (TRANSPLANT do CLRS):** há três casos.
  1. Sem filho à esquerda: substitua o nó pelo filho direito.
  2. Sem filho à direita: substitua pelo filho esquerdo.
  3. Dois filhos: o sucessor `y = min(z.right)` assume o lugar de z. Se `y` não é filho direito direto de z, primeiro substitua `y` pelo `y.right` e depois pendure `z.right` em `y`.
- **Bugs:** esquecer de atualizar `root` quando o nó removido é a raiz (`if u.parent is None: root = v`); esquecer `v.parent = u.parent`; copiar a chave do sucessor em vez de mover o nó, o que invalida handles externos que apontam para nós; não definir política de duplicatas (ignorar, contador no nó, ou sempre à direita).
- Sucessor sem ponteiro para o pai: guarde o último ancestral onde você desceu para a esquerda.

---

## AVL

Invariante: `|altura(esq) − altura(dir)| ≤ 1` em todo nó. Altura ≤ ~1,44 log₂ n. É mais rígida que a red-black, então buscas ficam um pouco mais rápidas e inserções fazem mais rotações.

```python
class N:
    __slots__ = ("key", "l", "r", "h")
    def __init__(self, k): self.key, self.l, self.r, self.h = k, None, None, 1

def h(n): return n.h if n else 0
def upd(n): n.h = 1 + max(h(n.l), h(n.r))
def bal(n): return h(n.l) - h(n.r)

def rot_right(y):
    x = y.l
    y.l, x.r = x.r, y
    upd(y); upd(x)          # FILHO primeiro (y agora está abaixo de x), depois o novo topo
    return x                # o chamador PRECISA religar: parent.link = rot_right(...)

def rot_left(x):
    y = x.r
    x.r, y.l = y.l, x
    upd(x); upd(y)
    return y

def rebalance(n):
    upd(n)
    b = bal(n)
    if b > 1:
        if bal(n.l) < 0: n.l = rot_left(n.l)     # caso LR → vira LL
        return rot_right(n)
    if b < -1:
        if bal(n.r) > 0: n.r = rot_right(n.r)    # caso RL → vira RR
        return rot_left(n)
    return n

def insert(n, k):
    if not n: return N(k)
    if k < n.key: n.l = insert(n.l, k)
    elif k > n.key: n.r = insert(n.r, k)
    else: return n                               # política: ignora duplicata
    return rebalance(n)
```

**Bugs clássicos:** atualizar a altura do novo topo antes da do filho (a altura fica velha e o ancestral decide errado sem nenhum erro visível); não religar o retorno da rotação ao pai; confundir quando aplicar rotação simples ou dupla (sinais do balanço do pai e do filho iguais → simples; opostos → dupla); na remoção, parar o rebalanceamento cedo (a remoção pode precisar de rotações em todos os níveis até a raiz, enquanto a inserção para depois de uma).

---

## Red-black (CLRS cap. 13)

**As 5 propriedades (CLRS 13.1):**
1. Todo nó é vermelho ou preto.
2. A raiz é preta.
3. Toda folha (NIL) é preta.
4. Nó vermelho tem os dois filhos pretos (não existem dois vermelhos seguidos).
5. Para cada nó, todo caminho até as folhas descendentes tem o mesmo número de nós pretos (black-height).

Consequência: altura ≤ 2·log₂(n+1).

**Sentinela `T.nil`:** é um único nó preto que representa todas as folhas **e** o pai da raiz. Ela simplifica as fronteiras, mas tem um detalhe sutil: na remoção, o CLRS atribui `x.p` mesmo quando `x == T.nil` (RB-TRANSPLANT atribui `v.p` incondicionalmente) e o fixup lê `x.p`. Se a sua implementação usa `None` em vez de sentinela, você precisa carregar o pai de `x` separadamente. Esse é o bug nº 1 de quem porta o CLRS para `null`.

**Inserção (CLRS 13.3):** insira como numa BST, pinte `z` de **vermelho** (assim a propriedade 5 continua valendo) e corrija em RB-INSERT-FIXUP. Só as propriedades 2 (z é a raiz) e 4 (pai vermelho) podem quebrar. Enquanto `z.p` for vermelho, olhe o tio `y`:
- **Caso 1, tio vermelho:** pinte pai e tio de preto e o avô de vermelho, e suba com `z = avô`. É o único caso que repete o laço.
- **Caso 2, tio preto e z em "triângulo"** (z é filho direito de um pai que é filho esquerdo): rotacione o pai para virar o caso 3.
- **Caso 3, tio preto e z em "linha":** troque as cores de pai e avô e rotacione o avô. Termina.
- No fim, **sempre** `root.color = BLACK`.
- Os casos espelhados (pai é filho direito) trocam esquerda e direita. Copiar e colar sem espelhar tudo é bug comum.

**Remoção (CLRS 13.4):** rastreie `y` (o nó removido ou movido), `y_cor_original` (salva **antes** de qualquer mudança) e `x` (o nó que ocupa a posição original de y, que pode ser `T.nil`). Se `y_cor_original == BLACK`, chame o fixup: `x` carrega um "preto extra". Com `w` = irmão de `x` (que nunca é `T.nil` nesse ponto):
- **Caso 1, w vermelho:** troque as cores de w e x.p e rotacione x.p para o lado de x. Isso reduz aos casos 2, 3 ou 4.
- **Caso 2, w preto com dois filhos pretos:** pinte w de vermelho e suba com `x = x.p`. É o único caso que repete; se veio do caso 1, termina na próxima checagem porque o novo x é vermelho.
- **Caso 3, w preto, filho próximo vermelho e filho distante preto:** troque as cores de w e do filho próximo e rotacione w. Vira o caso 4.
- **Caso 4, w preto e filho distante vermelho:** `w.color = x.p.color`, `x.p` fica preto, o filho distante fica preto, rotacione x.p, faça `x = root` e termine.
- No fim, `x.color = BLACK`.

**Recomendação prática:** use a da biblioteca (`TreeMap`, `std::map`/`std::set`, `BTreeMap` em Rust, `sortedcontainers` em Python). Se precisar escrever uma, prefira **left-leaning red-black** (Sedgewick), que tem bem menos casos, **treap** ou **AVL**. Se tiver que portar o CLRS, rode sempre o verificador abaixo.

```python
RED, BLACK = 0, 1
def check_rb(t):
    """Valida as 5 propriedades, a ordem BST e os ponteiros de pai. Retorna o black-height."""
    NIL = t.nil
    assert t.root is NIL or t.root.color == BLACK, "raiz vermelha"
    def go(n, lo, hi):
        if n is NIL: return 1
        assert (lo is None or lo < n.key) and (hi is None or n.key < hi), "ordem BST"
        for c in (n.left, n.right):
            if c is not NIL: assert c.p is n, "ponteiro de pai inconsistente"
        if n.color == RED:
            assert n.left.color == BLACK and n.right.color == BLACK, "vermelho-vermelho"
        bl = go(n.left, lo, n.key); br = go(n.right, n.key, hi)
        assert bl == br, "black-height diferente"
        return bl + (n.color == BLACK)
    return go(t.root, None, None)
```

---

## Treap

É uma BST pelas chaves e um heap por prioridades aleatórias, com altura esperada O(log n). Com split/merge fica curta e difícil de errar. Serve também como "implicit treap" (array com inserção, remoção e reversão de intervalo em O(log n)).

```python
import random
class T:
    __slots__ = ("k", "p", "l", "r", "sz")
    def __init__(s, k): s.k, s.p, s.l, s.r, s.sz = k, random.random(), None, None, 1
def sz(t): return t.sz if t else 0
def pull(t): t.sz = 1 + sz(t.l) + sz(t.r)          # recomputa a augmentação
def split(t, k):                                    # -> (chaves < k, chaves >= k)
    if not t: return None, None
    if t.k < k:
        a, b = split(t.r, k); t.r = a; pull(t); return t, b
    a, b = split(t.l, k); t.l = b; pull(t); return a, t
def merge(a, b):                                    # pré-condição: max(a) < min(b)
    if not a or not b: return a or b
    if a.p > b.p: a.r = merge(a.r, b); pull(a); return a
    b.l = merge(a, b.l); pull(b); return b
# insert: l, r = split(root, k); root = merge(merge(l, T(k)), r)
# erase:  l, r = split(root, k); _, r = split(r, k + 1); root = merge(l, r)   (chaves inteiras)
```

**Bugs:** esquecer `pull` depois de mudar filhos; chamar `merge` sem a pré-condição de ordem; com lazy (reversão), esquecer `push` antes de descer.

---

## Augmentação (CLRS cap. 14)

Receita do CLRS 14.2: (1) escolha a estrutura base; (2) defina a informação extra; (3) **verifique que ela pode ser mantida** nas operações que modificam a estrutura; (4) crie as operações novas.

**Teorema 14.1:** se o atributo `f` de um nó depende só de `x`, `x.left` e `x.right` (incluindo `x.left.f` e `x.right.f`), ele pode ser mantido em inserção e remoção numa red-black sem piorar o O(log n). Em rotações, basta recomputar os 2 nós rotacionados, filho antes do pai.

Exemplos:
- `size` → order statistics: `select(k)` e `rank(x)` em O(log n).
- `max_end` em árvore de intervalos (CLRS 14.3) → achar um intervalo que sobrepõe outro em O(log n).
- Soma ou mínimo da subárvore → queries de agregado por chave.

**Bug:** o atributo é atualizado na inserção mas esquecido nas rotações do fixup, ou na remoção ao longo do caminho até a raiz.

Em C++, `__gnu_pbds::tree<..., tree_order_statistics_node_update>` já entrega `find_by_order`/`order_of_key`.

---

## B-tree e B+tree (CLRS cap. 18)

**Definição com grau mínimo t ≥ 2 (CLRS 18.1):**
- Todo nó, exceto a raiz, tem entre **t−1 e 2t−1 chaves** (nó interno: entre t e 2t filhos). A raiz de uma árvore não vazia tem ≥ 1 chave.
- Nó interno com `n` chaves tem `n+1` filhos. Todas as folhas têm a mesma profundidade.
- Altura h ≤ log_t((n+1)/2). Comparada à red-black, a B-tree economiza um fator ≈ lg t em nós visitados, e por isso é usada em disco: o nó tem o tamanho de uma página (4–16 KB) e o fanout é de centenas.
- t = 2 dá a árvore 2-3-4, que é isomorfa à red-black.
- Atenção à convenção: livros usam "ordem m" (máximo de filhos) ou "grau mínimo t". Converta antes de copiar limites de outra fonte; misturar as duas convenções é uma fonte clássica de off-by-one.

**Inserção em uma passagem (CLRS 18.2):** divida **preventivamente** todo nó cheio encontrado na descida. Assim o pai nunca está cheio na hora de receber a mediana, e você nunca precisa voltar.

```python
from bisect import bisect_right, insort

class BNode:
    __slots__ = ("keys", "children", "leaf")
    def __init__(self, leaf): self.keys, self.children, self.leaf = [], [], leaf

class BTree:
    def __init__(self, t):
        assert t >= 2
        self.t, self.root = t, BNode(leaf=True)

    def _split_child(self, x, i):
        t, y = self.t, x.children[i]          # y está cheio: 2t-1 chaves
        z = BNode(leaf=y.leaf)
        mid = y.keys[t - 1]                   # mediana (índice t-1, base 0)
        z.keys = y.keys[t:]                   # t-1 chaves para a direita
        y.keys = y.keys[:t - 1]               # t-1 chaves ficam (a mediana SOBE, não fica)
        if not y.leaf:
            z.children = y.children[t:]       # t filhos para cada lado
            y.children = y.children[:t]
        x.keys.insert(i, mid)
        x.children.insert(i + 1, z)

    def insert(self, k):
        r = self.root
        if len(r.keys) == 2 * self.t - 1:     # raiz cheia: a árvore cresce PELA RAIZ
            s = BNode(leaf=False); s.children.append(r)
            self.root = s
            self._split_child(s, 0)
        x = self.root
        while not x.leaf:
            i = bisect_right(x.keys, k)
            if len(x.children[i].keys) == 2 * self.t - 1:
                self._split_child(x, i)
                if k > x.keys[i]: i += 1      # decide o lado depois do split
            x = x.children[i]
        insort(x.keys, k)

    def search(self, k):
        x = self.root
        while True:
            i = bisect_right(x.keys, k)
            if i > 0 and x.keys[i - 1] == k: return True
            if x.leaf: return False
            x = x.children[i]
```

**Remoção em uma passagem (CLRS 18.3):** garanta que todo nó **em que você vai descer** tenha ≥ t chaves (uma a mais que o mínimo):
1. k está numa folha: remova.
2. k está num nó interno x:
   - a) o filho anterior `y` tem ≥ t chaves: troque k pelo predecessor e remova o predecessor recursivamente em y;
   - b) senão, o filho seguinte `z` tem ≥ t chaves: use o sucessor;
   - c) senão, os dois têm t−1: **funda** y + k + z (2t−1 chaves) e remova k recursivamente em y.
3. k não está em x e o filho `c_i` onde ele estaria tem só t−1 chaves:
   - a) um irmão imediato tem ≥ t: **rotação**, em que a chave separadora do pai desce para `c_i`, uma chave do irmão sobe para o pai e o ponteiro de filho correspondente muda de nó;
   - b) os irmãos imediatos também têm t−1: **funda** `c_i` com um irmão, puxando o separador do pai para o meio.
- Se a raiz fica sem chaves (casos 2c/3b), o único filho vira a nova raiz e a **altura diminui**.

**Bugs clássicos:** off-by-one na mediana e na distribuição de filhos no split (são t filhos para cada lado, não t−1); esquecer de mover os **filhos** junto com as chaves em borrow e merge de nós internos; não atualizar o separador do pai depois de um borrow; não tratar a raiz vazia depois de um merge; não deixar a raiz crescer quando está cheia; escolher o filho errado na descida (`bisect_left` vs `bisect_right` com duplicatas); em versões bottom-up, esquecer que o merge pode propagar underflow até a raiz.

**B+tree:** guarda os dados **só nas folhas**, e os nós internos têm apenas separadores, o que maximiza o fanout (CLRS 18.1). As folhas são ligadas em lista, o que dá range scan sequencial. Diferenças que geram bugs:
- **Split de folha:** a primeira chave da folha da direita é **copiada** para o pai e continua na folha. **Split de nó interno:** a mediana **sobe** e sai do nó. Inverter esses dois comportamentos é o bug mais comum.
- Atualizar os ponteiros `next` (e `prev`) das folhas em split e merge.
- O separador no pai pode ficar "velho" depois de remoções. Isso é aceitável se a invariante for "separador ≤ todas as chaves da direita", mas defina a regra e teste.
- Em produção, há ainda concorrência (latch crabbing), páginas com tamanho variável e recuperação. Para persistência, use SQLite/LMDB/RocksDB em vez de escrever a sua.

---

## Heap (CLRS cap. 6)

Array implícito com índice base 0: `pai = (i-1)//2`, `filhos = 2i+1, 2i+2`. Com base 1 (CLRS): `pai = i//2`, `filhos = 2i, 2i+1`. Não misture as duas convenções.

| Operação                    | Custo                               |
|-----------------------------|-------------------------------------|
| push / pop                  | O(log n)                            |
| top                         | O(1)                                |
| **build-heap** (heapify)    | **O(n)**, não O(n log n) (CLRS 6.3) |
| buscar elemento arbitrário  | O(n)                                |

O build-heap é O(n) porque a maioria dos nós está perto das folhas: há no máximo ⌈n/2^(h+1)⌉ nós de altura h, e a soma converge. Os índices `n//2 .. n-1` são folhas, então o laço começa em `n//2 - 1` e desce até 0.

```python
def sift_down(a, i, n):          # min-heap
    while True:
        l, m = 2 * i + 1, i
        if l < n and a[l] < a[m]: m = l
        if l + 1 < n and a[l + 1] < a[m]: m = l + 1   # checar o limite do filho direito
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m

def sift_up(a, i):
    while i > 0:
        p = (i - 1) // 2
        if a[p] <= a[i]: return
        a[i], a[p] = a[p], a[i]; i = p

def build(a):
    for i in range(len(a) // 2 - 1, -1, -1): sift_down(a, i, len(a))

def pop(a):
    a[0], a[-1] = a[-1], a[0]
    x = a.pop()
    if a: sift_down(a, 0, len(a))   # heap vazio após o pop
    return x
```

**Decrease-key** (Dijkstra, Prim): `heapq` e `PriorityQueue` não têm. Há duas opções:
1. **Lazy deletion** (a mais usada): insira uma entrada nova e, ao tirar uma entrada, descarte se ela está desatualizada (`if d > dist[u]: continue`). O heap pode chegar a O(E) entradas, o que é aceitável.
2. **Heap indexado:** mantenha `pos[item]` atualizado **em toda troca**. Esquecer de atualizar `pos` num swap é o bug clássico. Depois de diminuir a chave, faça `sift_up`; depois de aumentar, `sift_down`.

Remover um elemento arbitrário pelo índice: troque com o último, faça pop, depois `sift_up` **e** `sift_down` nessa posição (só um dos dois vai mover o elemento).

**Padrões:** os k maiores elementos → **min**-heap de tamanho k (se `x > top`, substitui); mediana em stream → dois heaps (max-heap da metade baixa e min-heap da alta, com tamanhos diferindo no máximo em 1); merge de k listas → heap de `(valor, idx_lista, idx_elem)`.

**Bugs:** usar max-heap no lugar de min-heap (`heapq` é min; para max, negue a chave ou use um wrapper; `std::priority_queue` é **max** por padrão); empate em tupla cai na comparação do payload (Python: `TypeError` se o payload não é comparável; use `(prio, contador, item)`); esquecer de checar o filho direito no `sift_down`; modificar a prioridade de um objeto já dentro do heap sem reposicioná-lo.

Fibonacci heap (CLRS cap. 19) tem decrease-key O(1) amortizado e melhora a teoria do Dijkstra para O(E + V log V), mas a constante é alta. Na prática, binary heap (ou d-ary/pairing heap) quase sempre vence.

---

## Trie e radix tree

Custo O(L) por operação, onde L é o comprimento da chave, independente de n.

**Filhos: array ou mapa?**
- Array fixo `[26]`: o mais rápido, mas gasta ~208 bytes por nó em 64 bits, quase tudo vazio quando os filhos são esparsos.
- Hash map ou dict: gasta memória proporcional aos filhos que existem. É a escolha para alfabetos grandes (Unicode, URLs).
- Array de nós em pool (`children[node][c] = idx`) com `int32`: compacto e amigável ao cache. É a melhor opção em competição e em linguagens com GC.

```python
class TrieNode:
    __slots__ = ("ch", "end", "cnt")
    def __init__(self): self.ch, self.end, self.cnt = {}, 0, 0
    # end = quantas vezes a palavra termina aqui (CONTADOR, não bool → suporta duplicatas)
    # cnt = quantas palavras passam por este nó (serve para count_prefix e poda segura)

class Trie:
    def __init__(self): self.root = TrieNode()

    def insert(self, w):
        n = self.root; n.cnt += 1
        for c in w:
            n = n.ch.setdefault(c, TrieNode()); n.cnt += 1
        n.end += 1

    def _find(self, s):
        n = self.root
        for c in s:
            n = n.ch.get(c)
            if n is None: return None
        return n

    def contains(self, w):
        n = self._find(w); return n is not None and n.end > 0

    def count_prefix(self, p):
        n = self._find(p); return n.cnt if n else 0

    def remove(self, w):
        if not self.contains(w): return False      # checar ANTES de mexer nos contadores
        n = self.root; n.cnt -= 1
        for c in w:
            nxt = n.ch[c]; nxt.cnt -= 1
            if nxt.cnt == 0:                       # ninguém mais passa: poda a subárvore inteira
                del n.ch[c]; return True
            n = nxt
        n.end -= 1
        return True
```

**Bugs:** usar `end` booleano (remover uma cópia de uma palavra duplicada apaga todas); podar um nó que é prefixo de outra palavra ou fim de outra palavra (com o contador `cnt` isso não acontece); remover uma palavra inexistente e decrementar contadores mesmo assim; confundir "é prefixo" com "é palavra"; recursão profunda com chaves longas.

**Radix tree / Patricia:** comprime cadeias de nós com filho único em arestas com rótulo de string, reduzindo os nós de O(total de caracteres) para O(nº de chaves). Bugs específicos: dividir a aresta no ponto certo quando a chave nova compartilha só parte do rótulo, e **fundir de volta** um nó que ficou com um único filho e não marca fim de palavra depois de uma remoção.

**Binary trie (bits de inteiros):** XOR máximo entre pares em O(n · bits). Insira do bit mais significativo para o menos e use largura de bits fixa para todos os números.

---

## Segment tree

Responde queries de intervalo com qualquer operação **associativa** que tenha elemento neutro (soma, min, max, gcd, composição de funções lineares), com update em O(log n).

**Versão iterativa bottom-up** (compacta e rápida, 2n de memória, query em `[l, r)`):

```python
class SegTree:
    def __init__(self, a, op, e):     # e = elemento neutro (0 para soma, +inf para min...)
        self.n, self.op, self.e = len(a), op, e
        self.t = [e] * self.n + list(a)
        for i in range(self.n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def set(self, i, v):
        i += self.n; self.t[i] = v
        while i > 1:
            i //= 2; self.t[i] = self.op(self.t[2 * i], self.t[2 * i + 1])

    def query(self, l, r):            # agrega a[l:r]
        rl, rr = self.e, self.e
        l += self.n; r += self.n
        while l < r:
            if l & 1: rl = self.op(rl, self.t[l]); l += 1
            if r & 1: r -= 1; rr = self.op(self.t[r], rr)
            l //= 2; r //= 2
        return self.op(rl, rr)        # rl/rr separados preservam a ordem para op NÃO comutativa
```

**Lazy propagation** (update de intervalo + query de intervalo), versão recursiva com 4n de memória:

```python
class LazyAddSum:
    """Soma em intervalo [l, r) e consulta de soma em intervalo [l, r)."""
    def __init__(self, n):
        self.n = n; self.s = [0] * (4 * n); self.lz = [0] * (4 * n)

    def _apply(self, v, l, r, d):
        self.s[v] += d * (r - l)      # o agregado do nó PRECISA refletir o tamanho do segmento
        self.lz[v] += d

    def _push(self, v, l, r):         # repassa a pendência ANTES de descer
        if self.lz[v]:
            m = (l + r) // 2
            self._apply(2 * v, l, m, self.lz[v]); self._apply(2 * v + 1, m, r, self.lz[v])
            self.lz[v] = 0            # e limpa

    def add(self, ql, qr, d, v=1, l=0, r=None):
        if r is None: r = self.n
        if qr <= l or r <= ql: return
        if ql <= l and r <= qr: self._apply(v, l, r, d); return
        self._push(v, l, r); m = (l + r) // 2
        self.add(ql, qr, d, 2 * v, l, m); self.add(ql, qr, d, 2 * v + 1, m, r)
        self.s[v] = self.s[2 * v] + self.s[2 * v + 1]   # pull depois de descer

    def query(self, ql, qr, v=1, l=0, r=None):
        if r is None: r = self.n
        if qr <= l or r <= ql: return 0
        if ql <= l and r <= qr: return self.s[v]
        self._push(v, l, r); m = (l + r) // 2
        return self.query(ql, qr, 2 * v, l, m) + self.query(ql, qr, 2 * v + 1, m, r)
```

**Bugs clássicos:**
- Esquecer o `push` antes de descer (na query **e** no update) ou esquecer de zerar a pendência.
- Esquecer o `pull` depois de atualizar os filhos.
- Array com tamanho 2n na versão recursiva (precisa de **4n**).
- Elemento neutro errado: 0 para min, ou `-1` para max quando existem negativos.
- **Composição de tags fora de ordem:** com "atribuir" + "somar", a atribuição sobrescreve a soma pendente, mas a soma se acumula sobre a atribuição. Represente a tag como uma função `x → a·x + b` e componha na ordem certa (nova ∘ antiga).
- Pendência aplicada sem multiplicar pelo tamanho do segmento (soma).
- Misturar `[l, r]` e `[l, r)` entre a chamada e a implementação.

Variações: segment tree "walk" (primeiro índice com prefixo ≥ x em O(log n) descendo pela árvore, sem busca binária por fora), dinâmica/esparsa (nós criados sob demanda para coordenadas enormes), persistente, merge sort tree.

---

## Fenwick tree (BIT)

Faz soma de prefixo e update pontual em O(log n) com n+1 de memória. A constante é menor que a da segment tree. Exige uma operação **inversível** para queries de intervalo (soma, XOR); para min/max só funciona com prefixos e valores que só melhoram.

```python
class BIT:
    def __init__(self, n):
        self.n = n; self.t = [0] * (n + 1)    # base 1: t[0] não é usado

    @classmethod
    def build(cls, a):                        # O(n) a partir do array (base 0)
        b = cls(len(a))
        for i, x in enumerate(a, 1):
            b.t[i] += x
            j = i + (i & -i)
            if j <= b.n: b.t[j] += b.t[i]
        return b

    def add(self, i, d):                      # i em base 1
        while i <= self.n:
            self.t[i] += d; i += i & -i

    def prefix(self, i):                      # soma de a[1..i]
        s = 0
        while i > 0:
            s += self.t[i]; i -= i & -i
        return s

    def range(self, l, r):                    # soma de a[l..r], base 1, inclusivo
        return self.prefix(r) - self.prefix(l - 1)

    def lower_bound(self, k):                 # menor i com prefix(i) >= k (valores ≥ 0)
        pos, step = 0, 1 << self.n.bit_length()
        while step:
            if pos + step <= self.n and self.t[pos + step] < k:
                pos += step; k -= self.t[pos]
            step >>= 1
        return pos + 1
```

**Bugs:** usar índice 0 (`add(0, d)` entra em **loop infinito**, porque `0 & -0 == 0`); esquecer de converter de base 0 para base 1; `range(l, r)` com `prefix(l)` em vez de `prefix(l-1)`; reiniciar só parte da árvore entre casos de teste.

**Variantes:** update de intervalo com query pontual (BIT sobre o difference array); update de intervalo com query de intervalo (dois BITs: `B1`, `B2`); BIT 2D; contagem de inversões (percorra o array e conte, num BIT de valores comprimidos, os já vistos que são maiores).

### Receita: rank dinâmico por valor (leaderboard)

Problema: itens com score que muda, e consultas de "posição de x" e "top-k". Indexe a BIT pelo **valor** do score, não pelo item. `t` conta quantos itens têm cada score.

```python
from collections import defaultdict

class RankBoard:
    """rank(x) = 1 + quantos têm score ESTRITAMENTE maior (empates dividem a posição).
    set O(log M), rank O(log M), top(k) O(d log M), d = scores distintos visitados.
    Domínio 0..max_score; se for enorme ou real, comprima as coordenadas offline."""

    def __init__(self, max_score):
        self.M = max_score + 1
        self.t = [0] * (self.M + 1)
        self.score = {}                       # item -> score
        self.bucket = defaultdict(set)        # score -> itens (para top-k)
        self.n = 0

    def _add(self, s, d):
        i = s + 1                             # score 0 → índice 1 (índice 0 = loop infinito)
        while i <= self.M:
            self.t[i] += d; i += i & -i

    def _prefix(self, s):                     # quantos têm score <= s
        i, r = s + 1, 0
        while i > 0:
            r += self.t[i]; i -= i & -i
        return r

    def _kth(self, k):                        # score do k-ésimo MENOR (1 <= k <= n)
        pos, step = 0, 1 << self.M.bit_length()
        while step:
            if pos + step <= self.M and self.t[pos + step] < k:
                pos += step; k -= self.t[pos]
            step >>= 1
        return pos                            # índice pos+1 ↔ score pos

    def set(self, x, s):
        old = self.score.get(x)
        if old == s:
            return                            # atalho: evita 2 updates O(log M) inúteis
        if old is None:
            self.n += 1
        else:
            self._add(old, -1)
            self.bucket[old].discard(x)
            if not self.bucket[old]:
                del self.bucket[old]
        self.score[x] = s
        self._add(s, 1)
        self.bucket[s].add(x)

    def rank(self, x):
        return 1 + self.n - self._prefix(self.score[x])

    def top(self, k):                         # [(item, score)] por score desc, item asc
        out, j = [], 1                        # j-ésimo maior = (n - j + 1)-ésimo menor
        while len(out) < k and j <= self.n:
            s = self._kth(self.n - j + 1)
            b = self.bucket[s]
            out.extend((x, s) for x in sorted(b)[:k - len(out)])
            j += len(b)
        return out
```

- Para carga inicial grande, monte `t` com o `build` O(n + M) em vez de n chamadas a `set`.
- **Bugs a evitar:**
  - esquecer de remover o score antigo (o item passa a contar duas vezes);
  - incrementar `n` também em updates (só item novo aumenta `n`);
  - `rank` contando `>=` em vez de `>`, o que quebra empates;
  - `_kth` com `k` fora de `1..n`.
- **Alternativas:**
  - order-statistic tree (CLRS 14.1) ou treap com tamanho de subárvore, quando o domínio é enorme e online;
  - `__gnu_pbds::tree` em C++;
  - sorted set do Redis (`ZADD`, `ZREVRANK`, `ZREVRANGE`) em sistemas.
- Medição: com 10⁶ itens, rank em ~2 µs contra ~45 ms da varredura (`systems.md`).

---

## Sparse table

Faz query de intervalo em **O(1)** sobre array **estático**, com O(n log n) de pré-processamento. Só funciona para operações **idempotentes** (`f(x, x) = x`): min, max, gcd, AND, OR. **Não** serve para soma ou XOR, porque os dois blocos se sobrepõem e o meio seria contado duas vezes.

```python
def build_sparse(a, f=min):
    n = len(a)
    lg = [0] * (n + 1)
    for i in range(2, n + 1): lg[i] = lg[i // 2] + 1
    st = [a[:]]
    j = 1
    while (1 << j) <= n:
        prev, half = st[-1], 1 << (j - 1)
        st.append([f(prev[i], prev[i + half]) for i in range(n - (1 << j) + 1)])
        j += 1
    def query(l, r):                       # [l, r] inclusivo
        k = lg[r - l + 1]
        return f(st[k][l], st[k][r - (1 << k) + 1])
    return query
```

**Bugs:** usar `math.log2` com float (erro de arredondamento em potências de 2; use a tabela `lg` ou `bit_length() - 1`); errar o início do segundo bloco (`r - 2^k + 1`); usar com operação não idempotente.

---

## DSU / union-find (CLRS cap. 21)

As duas heurísticas do CLRS 21.3 são **união por posto** (a raiz de menor rank aponta para a de maior; rank é um limite superior da altura) e **compressão de caminho**. Juntas, dão O(m·α(n)), praticamente constante (CLRS 21.4). Com só uma delas, o custo é O(log n) amortizado. Sem nenhuma, uma corrente pode ter profundidade n.

```python
class DSU:
    def __init__(self, n):
        self.p = list(range(n)); self.sz = [1] * n; self.comps = n

    def find(self, x):                       # iterativo: sem risco de estouro de pilha
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]    # path halving
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: return False              # já estavam juntos: aresta de ciclo
        if self.sz[a] < self.sz[b]: a, b = b, a
        self.p[b] = a; self.sz[a] += self.sz[b]
        self.comps -= 1
        return True
```

**Bugs:** unir os **elementos** em vez das **raízes** (`p[a] = b` sem `find`); comparar `p[a] == p[b]` em vez de `find(a) == find(b)`; ler `sz[x]` de um nó que não é raiz; `find` recursivo sem união por tamanho, que estoura a pilha em cadeias longas; tentar **desfazer** uniões com compressão de caminho. Para rollback (DSU com rollback em divide-and-conquer offline), **não comprima**: use só união por tamanho e uma pilha de alterações.

**Variantes:** DSU com peso ou potencial (guarda a diferença até o pai, ex. "x − y = w", e acumula no `find`); DSU bipartido (paridade até a raiz); DSU sobre índices `i → próximo livre` para "pintar intervalos" em quase O(n).

**Limite:** o DSU só une. Para remover arestas, use processamento offline invertido (remoções viram uniões ao contrário) ou estruturas de conectividade dinâmica.

---

## LCA com binary lifting

Pré-processamento O(n log n), query O(log n). Com Euler tour + sparse table, a query cai para O(1).

```python
def build_lca(n, adj, root=0):
    LOG = max(1, n.bit_length())
    up = [[root] * n for _ in range(LOG)]       # o pai da raiz é ela mesma (evita índice -1)
    depth = [0] * n
    seen = [False] * n; seen[root] = True
    stack = [root]                              # DFS iterativa
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True; up[0][v] = u; depth[v] = depth[u] + 1; stack.append(v)
    for j in range(1, LOG):
        prev, cur = up[j - 1], up[j]
        for v in range(n): cur[v] = prev[prev[v]]

    def lca(a, b):
        if depth[a] < depth[b]: a, b = b, a
        diff = depth[a] - depth[b]
        for j in range(LOG):                    # nivela as profundidades
            if diff >> j & 1: a = up[j][a]
        if a == b: return a
        for j in range(LOG - 1, -1, -1):        # do maior salto para o menor
            if up[j][a] != up[j][b]: a, b = up[j][a], up[j][b]
        return up[0][a]                         # pare logo abaixo do LCA e suba 1
    return lca, depth
```

**Bugs:** `LOG` pequeno demais (precisa de `2^LOG > n`); pai da raiz como -1 sem tratamento (índice negativo em Python lê o último elemento sem erro); preencher `up[j]` antes de terminar `up[0]`; na segunda fase, iterar do menor salto para o maior; esquecer `if a == b` depois de nivelar. Distância entre a e b: `depth[a] + depth[b] − 2·depth[lca]`.
