#!/usr/bin/env python3
"""Mede como o tempo cresce com n e estima o expoente da complexidade (t ≈ c·n^k).

Uso:
    python bench_scaling.py --impl sol.py:fast --impl sol.py:brute --gen sol.py:gen_n \
        [--start 1000] [--factor 2] [--steps 6] [--repeat 3] [--max-time 10] [--seed 0]

Contratos:
    gen_n(rng: random.Random, n: int) -> tuple   # argumentos posicionais para cada impl
    impl(*args)                                  # o tempo medido é só o da chamada

Leitura do expoente k (inclinação log-log entre passos consecutivos e no ajuste geral):
    ~0     O(1) / O(log n)       ~1   O(n) / O(n log n) (n log n aparece como 1,05–1,15)
    ~2     O(n²)                 ~3   O(n³)
Com n pequeno, overhead fixo puxa k para baixo: confie nos passos maiores.
Uma implementação deixa de ser medida quando um passo passa de --max-time segundos.

Para estruturas com estado, faça gen_n devolver (n_itens, operações) e a impl
construir a estrutura e aplicar as operações (meça só consultas, se for o caso,
gerando poucas escritas).
"""
import argparse
import copy
import gc
import importlib.util
import math
import random
import sys
import time
from pathlib import Path


def load(spec: str):
    path, _, name = spec.rpartition(":")
    if not path or not name:
        sys.exit(f"spec inválida: {spec!r} (formato: arquivo.py:funcao)")
    p = Path(path).resolve()
    if str(p.parent) not in sys.path:  # permite importar módulos irmãos do arquivo
        sys.path.insert(0, str(p.parent))
    ms = importlib.util.spec_from_file_location(f"_bench_{p.stem}_{abs(hash(p))}", p)
    if ms is None or ms.loader is None:
        sys.exit(f"não foi possível carregar {p}")
    mod = importlib.util.module_from_spec(ms)
    ms.loader.exec_module(mod)
    try:
        return getattr(mod, name)
    except AttributeError:
        sys.exit(f"{p} não define {name!r}")


def timed(fn, args, repeat):
    """Melhor de `repeat`. Cada execução recebe uma cópia nova dos argumentos (fora do tempo medido),
    para que uma versão que altera a entrada (ex.: a.sort()) não distorça as medições seguintes."""
    best = math.inf
    for _ in range(repeat):
        call_args = copy.deepcopy(args)
        gc.collect()
        gc.disable()
        try:
            t = time.perf_counter()
            fn(*call_args)
            best = min(best, time.perf_counter() - t)
        finally:
            gc.enable()
    return best


def slope(points):
    """Ajuste por mínimos quadrados de log t × log n."""
    pts = [(math.log(n), math.log(t)) for n, t in points if t > 0]
    if len(pts) < 2:
        return None
    mx = sum(x for x, _ in pts) / len(pts)
    my = sum(y for _, y in pts) / len(pts)
    den = sum((x - mx) ** 2 for x, _ in pts)
    return sum((x - mx) * (y - my) for x, y in pts) / den if den else None


def guess(k):
    if k is None:
        return "?"
    for lim, name in ((0.3, "O(1)/O(log n)"), (0.85, "sublinear (√n?)"), (1.3, "O(n)/O(n log n)"),
                      (1.7, "O(n^1.5)?"), (2.4, "O(n²)"), (3.4, "O(n³)")):
        if k < lim:
            return name
    return "pior que O(n³)"


def fmt(t):
    return f"{t * 1e6:.1f} µs" if t < 1e-3 else f"{t * 1e3:.2f} ms" if t < 1 else f"{t:.2f} s"


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--impl", action="append", required=True, help="arquivo.py:funcao (repita para comparar)")
    ap.add_argument("--gen", required=True)
    ap.add_argument("--start", type=int, default=1000)
    ap.add_argument("--factor", type=float, default=2.0)
    ap.add_argument("--steps", type=int, default=6)
    ap.add_argument("--repeat", type=int, default=3, help="mede o melhor de R execuções")
    ap.add_argument("--max-time", type=float, default=10.0)
    ap.add_argument("--seed", type=int, default=0)
    return ap.parse_args()


def measure_cell(name, fn, args, n, a, data, alive):
    if name not in alive:
        return f"{'—':>22}"
    t = timed(fn, args, a.repeat)
    pts = data[name]
    step_k = None
    if pts and pts[-1][1] > 0 and t > 0:
        step_k = math.log(t / pts[-1][1]) / math.log(n / pts[-1][0])
    pts.append((n, t))
    if t > a.max_time:
        alive.discard(name)
    return f"{fmt(t):>12} {'' if step_k is None else f'k={step_k:4.2f}':>9}"


def print_exponents(impls, data):
    print("\nexpoente estimado (ajuste log-log em todos os passos; últimos 3 entre parênteses):")
    for name, _ in impls:
        k_all, k_tail = slope(data[name]), slope(data[name][-3:])
        fa = "?" if k_all is None else f"{k_all:.2f}"
        ft = "?" if k_tail is None else f"{k_tail:.2f}"
        print(f"  {name:<20} k ≈ {fa} ({ft})  → {guess(k_tail if k_tail is not None else k_all)}")


def print_comparison(impls, data):
    common = set.intersection(*(set(dict(data[nm])) for nm, _ in impls))
    if len(impls) < 2 or not common:
        return
    n = max(common)
    ts = {nm: dict(data[nm])[n] for nm, _ in impls}
    fastest = min(ts, key=ts.get)
    others = ", ".join(f"{nm} {ts[nm] / ts[fastest]:,.1f}× mais lento" for nm in ts if nm != fastest)
    print(f"\nem n={n:,}: mais rápido = {fastest}; {others}")


def labels(specs: list[str]) -> list[str]:
    """Nome curto (função) quando é único; `arquivo:função` quando dois arquivos têm a mesma função."""
    if len(set(specs)) != len(specs):
        sys.exit("--impl repetido: cada versão deve aparecer uma vez")
    funcs = [s.rpartition(":")[2] for s in specs]
    full = [f"{Path(s.rpartition(':')[0]).stem}:{f}" for s, f in zip(specs, funcs)]
    if len(set(full)) != len(full):
        return specs
    return [f if funcs.count(f) == 1 else fl for f, fl in zip(funcs, full)]


def main():
    a = parse_args()
    impls = [(name, load(spec)) for name, spec in zip(labels(a.impl), a.impl)]
    gen = load(a.gen)
    data = {name: [] for name, _ in impls}
    alive = {name for name, _ in impls}
    print(f"{'n':>12} " + " ".join(f"{name:>22}" for name, _ in impls))
    for n in (int(a.start * a.factor ** i) for i in range(a.steps)):
        args = gen(random.Random(a.seed + n), n)
        args = args if isinstance(args, tuple) else (args,)
        cells = [measure_cell(name, fn, args, n, a, data, alive) for name, fn in impls]
        print(f"{n:>12,} " + " ".join(cells), flush=True)
    print_exponents(impls, data)
    print_comparison(impls, data)


if __name__ == "__main__":
    main()
