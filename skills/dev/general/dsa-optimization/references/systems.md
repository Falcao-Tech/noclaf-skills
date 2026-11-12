# Sistemas: escalar ou otimizar?

Quando um serviço "não aguenta a carga", a reação comum é arquitetural: mais instâncias, sharding, cache, fila, réplicas de leitura. Isso divide o trabalho por P, mas uma estrutura de dados melhor costuma **eliminar** o trabalho. Leia este arquivo antes de propor infraestrutura para um problema de desempenho.

Índice: [Diagnóstico](#diagnóstico-antes-de-escalar) · [Problema de sistema → estrutura](#problema-de-sistema--estrutura) · [Leitura × escrita](#perfil-de-operações-leitura--escrita) · [Estrutura por operação](#estrutura-por-operação-híbridos) · [Quando a arquitetura é a resposta](#quando-a-arquitetura-é-a-resposta-certa) · [Memória](#custo-de-memória-python) · [Caso medido](#caso-medido-leaderboard)

---

## Diagnóstico antes de escalar

1. **Ache a operação dominante por requisição.** Faça profiling ou leia o handler. A pergunta é: o custo de UMA requisição cresce com o tamanho da base (n)?
   - Se cresce (varre a tabela, ordena a lista, conta, filtra em memória), o problema é algorítmico. Escalar divide o custo por P e a curva continua a mesma. Quando a base dobrar, o problema volta.
   - Se não cresce (O(1) ou O(log n) por requisição) e mesmo assim satura, aí é capacidade: escale.
2. **Faça a conta.** Responda `requisições/s × custo por requisição` ≤ capacidade de um núcleo:
   - Exemplo: 1M de itens × 50 ns por item = 50 ms por consulta, então 20 consultas/s por núcleo.
   - Com 8 núcleos, são 160/s. Se a demanda é 5000/s, o hardware não fecha a conta, mas O(log n) fecha com folga.
3. **Meça a curva.** Rode `scripts/bench_scaling.py` com n, 2n, 4n. Se o expoente estimado for ≥ 1 na operação de leitura do caminho quente, otimize antes de escalar.
4. **Verifique o banco antes do código.** Muitas vezes a "estrutura certa" já existe e falta usá-la:
   - consulta sem índice (full scan);
   - N+1 queries;
   - `ORDER BY ... OFFSET` profundo (use paginação por cursor/keyset);
   - `COUNT(*)` em tabela enorme a cada requisição (mantenha um contador);
   - `LIKE '%x%'` (use índice de texto ou trigram).

Cache e réplicas **escondem** um custo O(n), não o removem:
- Um cache recomputado a cada T segundos custa n/T por segundo e entrega respostas defasadas.
- Se o produto aceita resposta defasada, é uma opção legítima. Se não aceita, ele só adia o problema.

## Problema de sistema → estrutura

| Problema / feature                                         | Ingênuo (O(n) por requisição)              | Estrutura certa                                                        | Custo            |
|------------------------------------------------------------|--------------------------------------------|------------------------------------------------------------------------|------------------|
| ranking / leaderboard ("minha posição", top-k)             | contar quem tem score maior                | Fenwick sobre o valor do score (`trees.md`, rank dinâmico), order-statistic tree, Redis sorted set (skip list com span) | O(log n) |
| rate limiter (N req por janela)                            | filtrar o log de requisições do usuário    | deque de timestamps por chave (janela deslizante), ou contador de janela fixa + anterior ponderado, ou token bucket | O(1) amortizado |
| contagem de eventos nos últimos X minutos                  | `COUNT WHERE ts > now - X`                 | buffer circular de buckets por segundo/minuto + soma corrente          | O(1)             |
| autocomplete                                               | `LIKE 'pre%'` + ordenar                    | trie com top-k cacheado em cada nó (atualizado na escrita)             | O(\|prefixo\| + k) |
| agendamento, timeouts, jobs atrasados                      | varrer todos os jobs a cada tick           | min-heap por horário (lazy deletion para cancelar), ou timing wheel    | O(log n) / O(1)  |
| "já processei esse item?" (dedup em stream)                | busca na lista de processados              | hash set com expiração; Bloom filter se a memória é o limite (aceita falso positivo) | O(1) |
| contar distintos em volume enorme                          | `set` com tudo                             | HyperLogLog (erro ~1–2% com poucos KB)                                 | O(1)             |
| trending / heavy hitters                                   | contador de tudo + sort                    | contador + heap de tamanho k; count-min sketch se as chaves não cabem  | O(log k)         |
| mediana / percentil de latência ao vivo                    | ordenar a lista a cada consulta            | dois heaps (mediana); histograma de buckets fixos ou t-digest (percentis) | O(log n) / O(1) |
| busca por proximidade (lojas perto, motoristas)            | distância para todos                       | grid/geohash (buckets por célula), KD-tree, R-tree / índice geoespacial do banco | ~O(log n + k) |
| reservas e conflito de horários                            | comparar com todas as reservas             | árvore ordenada por início (vizinhos predecessor e sucessor) ou interval tree | O(log n)     |
| soma/contagem por intervalo de datas, sem updates          | `SUM WHERE data BETWEEN`                   | prefix sums por dia (ou tabela de agregados)                           | O(1)             |
| idem, com updates                                          | idem                                       | Fenwick / segment tree por dia                                         | O(log n)         |
| permissões herdadas / hierarquia ("é descendente de?")     | subir pelos pais a cada checagem           | Euler tour (tin/tout) para checar em O(1); closure table no banco      | O(1)             |
| merge de feeds / k listas ordenadas                        | concatenar e ordenar                       | heap com a cabeça de cada lista                                        | O(log k) por item |
| conectividade ("estão no mesmo grupo?")                    | BFS a cada consulta                        | DSU (se só há uniões)                                                  | ≈O(1)            |
| cache com limite de tamanho                                | lista + remove do meio                     | LRU: hash map + lista duplamente ligada (`linear.md`)                  | O(1)             |
| fila de prioridade de trabalho com reprioridade            | ordenar a fila a cada mudança              | heap + lazy deletion (versão por item)                                 | O(log n)         |

## Perfil de operações (leitura × escrita)

Escolher pela operação mais lenta isolada engana. Some ponderando pela frequência real:

```
custo médio por operação = Σ frequência(op) × custo(op)
```

Exemplo do leaderboard (1M de jogadores, 80% `set`, 18% `rank`, 2% `top`), com tempos medidos:

| implementação  | set     | rank    | top     | custo médio por operação                          |
|----------------|---------|---------|---------|---------------------------------------------------|
| dict + varredura | 0,5 µs | 45 ms   | 120 ms  | 0,8·0,5µs + 0,18·45ms + 0,02·120ms ≈ **10,5 ms** |
| Fenwick        | 5 µs    | 2 µs    | 40 µs   | 0,8·5µs + 0,18·2µs + 0,02·40µs ≈ **5,2 µs**       |

A Fenwick é 10× pior na escrita e ainda assim vence por ~2000× no total. O inverso também acontece: com 99,99% de escritas e leituras raras, uma estrutura cara de manter pode perder para o "acumular e calcular quando pedir".

Padrões por perfil:

| Perfil                                    | Estratégia                                                                 |
|-------------------------------------------|----------------------------------------------------------------------------|
| leitura ≫ escrita                         | pré-computar na escrita: índice, prefix sums, agregado materializado, top-k por nó |
| escrita ≫ leitura                         | escrita O(1) (append em log ou contador); calcular sob demanda             |
| as duas frequentes                        | estrutura O(log n) nos dois lados: Fenwick, segment tree, árvore balanceada, heap |
| as consultas podem esperar ou ir em lote  | offline: ordenar consultas e eventos e varrer uma vez (sweep, Mo's, DSU offline) |
| aceita resposta defasada em T segundos    | snapshot periódico: custa n/T por segundo; ótimo se T é grande e n moderado |
| escritas em rajada                        | bufferizar e aplicar em lote (`build` O(n) em vez de n inserções)          |

Diga ao usuário o trade-off: quanto a escrita piora, quanto a leitura melhora, quanto de memória a mais e o custo de construção inicial.

## Estrutura por operação (híbridos)

Quando cada operação tem uma estrutura vencedora diferente (ex.: o dict escreve e carrega mais rápido, a Fenwick consulta mais rápido), dá para usar **as duas**: cada operação vai para a estrutura mais barata para ela. O preço é a **sincronização**. O trabalho adiado não some, ele é pago depois. Por isso a decisão é por **custo acumulado**, não por operação isolada.

**Passo a passo:**

1. Monte a tabela de custos medidos por operação em cada candidata: carga/construção, escrita, cada tipo de leitura, e também o custo de **converter** de uma para a outra (build) e de **sincronizar** k mudanças (k updates incrementais ou um rebuild).
2. Se a vencedora é a mesma em todas as operações frequentes, use só ela. Híbrido sem necessidade é complexidade grátis.
3. Se as vencedoras diferem, escolha o padrão de sincronização:

| Padrão | Como funciona | Ganha quando |
|---|---|---|
| **construção adiada + ski rental** | Responde leituras pela estrutura simples (ex.: varredura), acumulando o custo. Constrói o índice quando o acumulado alcança o custo do build. | o número de leituras após a carga é imprevisível; nunca paga mais que ~2× o ótimo |
| **decisão de antemão por fase** | O perfil é conhecido: carga em lote → `build` O(n); fase de leitura → índice; poucas leituras → nem constrói | jobs batch, startup, ETL; é o melhor dos casos quando o perfil é previsível |
| **buffer de escrita + flush na leitura** | Escreve em O(1) e marca o item como sujo. Na leitura, aplica os sujos escolhendo o mais barato entre `k · custo_update` e `custo_rebuild` | rajadas de escrita entre leituras raras; muitas escritas no mesmo item (coalescência); reescrita em lote (rebuild ≪ n updates) |
| **leitura corrigida pelo buffer** | Responde com o índice + uma correção O(k) sobre os pendentes, sem flush; faz o flush quando k passa de um limite (~√n ou calibrado) | leituras precisam de latência estável e o flush é caro |
| **duas representações sempre sincronizadas** | Toda escrita atualiza as duas (ex.: hash map + lista ligada no LRU; dict + heap) | cada estrutura atende uma operação que a outra não faz bem e a escrita dupla é barata |
| **snapshot periódico** | Reconstrói o índice a cada T segundos e lê dele (defasado) | o produto aceita defasagem; o custo fica n/T por segundo |
| **cache da estrutura, não da resposta** | Guarda no cache o índice construído (prefix sums, índice de rank, mapa agregado) em vez do resultado de cada chamada | as perguntas variam (outros ids, intervalos, períodos): o cache de resposta só acerta a repetição exata, o de estrutura responde perguntas **novas** sem ir ao banco |

4. Meça os perfis extremos, não só o médio: poucas leituras após a carga, rajada de escrita, reescrita em lote e o regime estável. Compare o **tempo total** (carga + operações) **e o p99** da leitura, porque varredura e build no caminho da requisição criam picos.

**Caso medido** (leaderboard com 1M de jogadores; dict para escrita, Fenwick para leitura, ski rental + flush com escolha entre incremental e rebuild), em tempo total:

| perfil | Fenwick pura | híbrido |
|---|---:|---:|
| sobe, 10 leituras, morre | 0,96 s | **0,49 s** (nunca constrói) |
| reescreve os 1M, depois 200 leituras | 7,07 s | **4,86 s** (1 rebuild em vez de 1M de updates) |
| regime estável (misto, leitura ou escrita) | **~1,0 s** | ~2,1 s (ski rental paga ~20 varreduras antes do build) |

**Regras que saem disso:**

- Usar estrutura diferente por operação vale quando **a fase muda** (carga → leitura, lote → leitura) ou quando as escritas **coalescem**.
- Em regime estável, com uma estrutura que já é barata nos dois lados, o híbrido perde.
- Perfil previsível → decida de antemão (construir na carga, rebuild depois do lote). A política adaptativa é para quando o futuro é desconhecido.
- Converta custos para uma unidade comum, medida na própria máquina e linguagem (ex.: "itens varridos"). Neste caso: build ≈ 11 itens varridos por item, update na BIT ≈ 20 passos ≈ 7 µs. Constantes chutadas erram por 5×: nossa primeira estimativa do custo do rebuild estava errada nessa proporção.
- Teste cada caminho de sincronização separadamente no stress test, forçando as constantes (sempre incremental, sempre rebuild, troca de modo no meio). Em entradas pequenas, o caminho padrão quase nunca sai do modo simples.

**Caso medido em Django + DRF** (50 mil pedidos; mesmo cache com TTL nas duas versões): com cache quente e **parâmetros novos**, a versão "repositórios + cache de resposta + 4 threads" levou 18,8 s. A versão "consulta agregada + estruturas, com a estrutura no cache" levou 0,33 s (57×). Receita por intervalos novos: 4,0 s → 2,3 ms (1.730×). Na repetição exata, as duas empatam (~1 ms): cache de resposta não diferencia arquitetura de algoritmo.

## Quando a arquitetura é a resposta certa

Escalar não é o erro; o erro é escalar **em vez de** corrigir a complexidade. A arquitetura é a resposta certa quando:

- **os dados não cabem numa máquina** (memória ou disco);
- **é preciso disponibilidade**: réplicas e failover, que nada têm a ver com velocidade;
- **o custo por requisição já é O(1) ou O(log n)** e a demanda supera um núcleo ou uma máquina;
- **é preciso isolamento**: multi-tenant, limites de blast radius;
- **há latência geográfica**: réplicas perto do usuário.

Mesmo nesses casos, **particione e use a estrutura certa em cada partição**:
- Cada shard mantém sua Fenwick, heap ou índice.
- Consultas globais combinam resultados pequenos: somar contagens, fazer merge de top-k locais.
- Nunca concatene os dados brutos.
- É assim que funcionam índices de banco (B+tree por partição), Redis Cluster (sorted set por slot) e motores de busca (índice invertido por shard + merge dos top-k).

Rank global sobre shards: cada shard responde "quantos têm score > s" em O(log n) e o coordenador soma. Isso dá O(P log n) em vez de O(n).

## Custo de memória (Python)

Medido com `tracemalloc` (CPython 3.14, 64 bits), por elemento, com 10⁶ elementos:

| estrutura                               | bytes/elemento |
|-----------------------------------------|---------------:|
| `list` de ints pequenos (cache −5..256) | 8              |
| `array('q')`                            | 8              |
| `list` de ints grandes                  | 40             |
| `deque` de ints                         | 40             |
| `set` de ints                           | 66             |
| `list[list]` vazias (lista de adjacência) | 64           |
| objeto com `__slots__` (2 campos int)   | 88             |
| `dict` int → int                        | 106            |
| objeto comum (2 campos int)             | 128            |
| `list` de tuplas `(int, int)`           | 136            |

Consequências:
- Uma BIT sobre um domínio de 10⁶ valores custa ~8 MB enquanto as contagens forem pequenas (até 256) e ~40 MB se forem grandes. Com `array('q')` cai para 8 MB fixos, mas fica um pouco mais lenta em Python puro.
- 10⁶ nós de árvore como objetos custam 100+ MB. Prefira arrays paralelos (`left[]`, `right[]`, `key[]`) ou `__slots__`.
- Em C++, Java ou Go, `int64` ocupa 8 bytes, um nó com 2 ponteiros e uma chave de 8 bytes fica entre 24 e 32 bytes, e um `HashMap<Integer, Integer>` do Java tem ~50–80 bytes por entrada por causa do boxing.

## Caso medido: leaderboard

O projeto de exemplo compara três versões com o mesmo workload:
- dict + varredura;
- a mesma varredura particionada em 4 processos com scatter-gather;
- Fenwick em 1 processo.

| n   | varredura | 4 shards (5 processos) | Fenwick (1 processo) |
|----:|----------:|-----------------------:|---------------------:|
| 10k  | 10.266 ops/s | 1,0×                | 18×                  |
| 100k | 935 ops/s    | 1,5×                | 191×                 |
| 1M   | 94 ops/s     | 3,2×                | 2.078×               |

O ganho da arquitetura tem teto P (aqui, 3,2× com 4 shards, e nenhum com n pequeno por causa do IPC). O ganho do algoritmo cresce com n.
