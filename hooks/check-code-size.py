#!/usr/bin/env python3

# Backstop mecânico de tamanho: bloqueia `git commit` quando um arquivo staged passa
# de MAX_FILE linhas ou tem função acima de MAX_FUNC linhas. Complementa o
# check-comment-length. Determinístico; escape deliberado via `git commit --no-verify`.

import json, os, re, subprocess, sys

MAX_FILE = 300  # linhas por arquivo
MAX_FUNC = 30   # linhas por função

BRACE = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".rs", ".go", ".java",
    ".c", ".h", ".cc", ".cpp", ".hpp", ".cs", ".swift", ".kt", ".kts",
    ".scala", ".dart", ".php",
}
PY = {".py"}
# file-length vale pra qualquer arquivo de código; function-length só onde sabemos parsear.
CODE = BRACE | PY | {".rb", ".sh", ".bash", ".zsh", ".pl", ".r"}

CONTROL = {"if", "for", "while", "switch", "catch", "else", "do", "try", "when", "guard", "with"}


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def net_braces(line):
    """`{` menos `}` na linha, ignorando strings e comentário `//`."""
    depth, i, quote, n = 0, 0, None, len(line)
    while i < n:
        c = line[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "\"'`":
            quote = c
        elif c == "/" and i + 1 < n and line[i + 1] == "/":
            break
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return depth


def looks_like_func(line):
    s = line.strip()
    if not s or s[0] in "});" or "{" not in s:
        return False
    head = re.match(r"([A-Za-z_]\w*)", s)
    if head and head.group(1) in CONTROL:
        return False
    if "=>" in s or re.search(r"\b(function|func|fun|def)\b", s):
        return True
    # método/declaração: nome(args) { ...
    return bool(re.search(r"[A-Za-z0-9_]\s*\([^;{}]*\)\s*(:[^={]+)?\{", s))


def scan_brace(lines):
    """Funções de linguagem com chaves acima de MAX_FUNC — (linha 1-based, tamanho)."""
    hits, depth, pending = [], 0, []
    for idx, raw in enumerate(lines):
        if looks_like_func(raw):
            pending.append((depth, idx))
        depth += net_braces(raw)
        while pending and depth <= pending[-1][0]:
            base, start = pending.pop()
            length = idx - start + 1
            if length > MAX_FUNC:
                hits.append((start + 1, length))
    return hits


def scan_py(lines):
    """Funções Python acima de MAX_FUNC via indentação — (linha 1-based, tamanho)."""
    hits, i, n = [], 0, len(lines)
    while i < n:
        m = re.match(r"^(\s*)(?:async\s+)?def\s+\w+", lines[i])
        if not m:
            i += 1
            continue
        indent, start, last, j = len(m.group(1)), i, i, i + 1
        while j < n:
            line = lines[j]
            if line.strip():
                if len(line) - len(line.lstrip()) <= indent:
                    break
                last = j
            j += 1
        length = last - start + 1
        if length > MAX_FUNC:
            hits.append((start + 1, length))
        i = j
    return hits


def check(f):
    ext = os.path.splitext(f)[1]
    if ext not in CODE:
        return []
    content = sh(["git", "show", f":{f}"])
    lines = content.splitlines()
    bad = []
    if len(lines) > MAX_FILE:
        bad.append(f"{f}: {len(lines)} linhas (> {MAX_FILE})")
    scanner = scan_brace if ext in BRACE else scan_py if ext in PY else None
    if scanner:
        for ln, length in scanner(lines):
            bad.append(f"{f}:{ln} função com {length} linhas (> {MAX_FUNC})")
    return bad


def main():
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except Exception:
        sys.exit(0)
    if "git commit" not in cmd or "--no-verify" in cmd or "--amend" in cmd:
        sys.exit(0)
    try:
        files = sh(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]).split()
    except Exception:
        sys.exit(0)
    bad = [b for f in files for b in check(f)]
    if bad:
        sys.stderr.write(
            f"code-size backstop: arquivo > {MAX_FILE} linhas ou função > {MAX_FUNC} linhas.\n"
            "Quebre por responsabilidade, ou re-commite com --no-verify se for deliberado.\n"
            + "".join(f"  {b}\n" for b in bad)
        )
        sys.exit(2)  # exit 2 -> Claude Code bloqueia o commit
    sys.exit(0)


def selftest():
    long_fn = ["function big() {"] + [f"  const x{i} = {i}" for i in range(35)] + ["}"]
    assert scan_brace(long_fn) == [(1, 37)], scan_brace(long_fn)
    ok_fn = ["const f = () => {", "  return 1", "}"]
    assert scan_brace(ok_fn) == [], scan_brace(ok_fn)
    ctrl = ["if (x) {"] + ["  y()" for _ in range(35)] + ["}"]
    assert scan_brace(ctrl) == [], scan_brace(ctrl)
    py = ["def big():"] + [f"    x{i} = {i}" for i in range(35)]
    assert scan_py(py) == [(1, 36)], scan_py(py)
    py_ok = ["def small():", "    return 1", "", "x = 1"]
    assert scan_py(py_ok) == [], scan_py(py_ok)
    assert net_braces('const s = "a{b}c"; foo() {') == 1, net_braces('const s = "a{b}c"; foo() {')
    print("ok")


if __name__ == "__main__":
    (selftest if len(sys.argv) > 1 and sys.argv[1] == "selftest" else main)()
