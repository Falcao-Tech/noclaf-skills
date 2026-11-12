#!/usr/bin/env python3
"""Stress test: compara uma solução otimizada com uma força bruta em entradas aleatórias.

Uso:
    python stress_test.py --fast sol.py:fast --brute sol.py:brute --gen sol.py:gen \
        [--iters 1000] [--seed 0] [--unordered] [--float-tol 1e-9]

Contratos:
    gen(rng: random.Random) -> tuple   # argumentos posicionais para fast/brute
    fast(*args) / brute(*args)         # devem retornar valores comparáveis com ==

Dicas para o gerador: entradas PEQUENAS (n <= 8), valores numa faixa curta
(com negativos, zero e duplicatas), e casos de borda (n = 0, n = 1) com alguma probabilidade.

Ao achar divergência, imprime a seed, a entrada e as duas saídas, e sai com código 1.
Os argumentos passam por deepcopy antes de cada chamada, então mutações feitas pela
solução não contaminam a comparação.
"""
import argparse
import copy
import importlib.util
import math
import random
import sys
import time
import traceback
from pathlib import Path


def load(spec: str):
    """Carrega 'caminho/arquivo.py:funcao'."""
    path, _, name = spec.rpartition(":")
    if not path or not name:
        sys.exit(f"spec inválida: {spec!r} (formato: arquivo.py:funcao)")
    p = Path(path).resolve()
    if str(p.parent) not in sys.path:  # permite importar módulos irmãos do arquivo
        sys.path.insert(0, str(p.parent))
    mod_spec = importlib.util.spec_from_file_location(f"_stress_{p.stem}_{abs(hash(p))}", p)
    if mod_spec is None or mod_spec.loader is None:
        sys.exit(f"não foi possível carregar {p}")
    mod = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(mod)
    try:
        return getattr(mod, name)
    except AttributeError:
        sys.exit(f"{p} não define {name!r}")


def normalize(x, unordered: bool):
    if unordered and isinstance(x, (list, tuple)):
        try:
            return sorted(x)
        except TypeError:
            return sorted(x, key=repr)
    return x


def equal(a, b, tol):
    if tol is not None and isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=tol, abs_tol=tol)
    if tol is not None and isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(equal(x, y, tol) for x, y in zip(a, b))
    return a == b


def run(fn, args):
    try:
        return True, fn(*copy.deepcopy(args))
    except Exception:  # noqa: BLE001 - queremos reportar qualquer falha
        return False, traceback.format_exc(limit=3)


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fast", required=True)
    ap.add_argument("--brute", required=True)
    ap.add_argument("--gen", required=True)
    ap.add_argument("--iters", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=None, help="seed inicial; cada iteração usa seed+i")
    ap.add_argument("--unordered", action="store_true", help="compara listas ignorando a ordem")
    ap.add_argument("--float-tol", type=float, default=None, help="tolerância para floats")
    return ap.parse_args()


def report_mismatch(i, seed, inp, ok_f, out_f, out_b):
    print(f"DIVERGÊNCIA na iteração {i} (seed={seed})")
    print(f"  entrada : {inp!r}")
    print(f"  esperado: {out_b!r}")
    print(f"  obtido  : {out_f if not ok_f else repr(out_f)}")
    print(f"reproduza com: --seed {seed} --iters 1")
    sys.exit(1)


def check_one(args, fast, brute, gen, i, seed, timer):
    inp = gen(random.Random(seed))
    if not isinstance(inp, tuple):
        inp = (inp,)
    t0 = time.perf_counter(); ok_b, out_b = run(brute, inp); t1 = time.perf_counter()
    ok_f, out_f = run(fast, inp); t2 = time.perf_counter()
    timer[0] += t1 - t0; timer[1] += t2 - t1
    if not ok_b:
        print(f"[seed={seed}] a FORÇA BRUTA falhou (corrija o gerador ou a brute):\n{out_b}")
        print(f"entrada: {inp!r}")
        sys.exit(2)
    norm = lambda x: normalize(x, args.unordered)
    if not (ok_f and equal(norm(out_f), norm(out_b), args.float_tol)):
        report_mismatch(i, seed, inp, ok_f, out_f, out_b)


def main():
    args = parse_args()
    fast, brute, gen = load(args.fast), load(args.brute), load(args.gen)
    base = args.seed if args.seed is not None else random.randrange(1 << 30)
    timer = [0.0, 0.0]  # brute, fast
    for i in range(args.iters):
        check_one(args, fast, brute, gen, i, base + i, timer)
    print(f"OK: {args.iters} casos iguais (seed base={base}). "
          f"tempo brute={timer[0]:.3f}s fast={timer[1]:.3f}s")


if __name__ == "__main__":
    main()
