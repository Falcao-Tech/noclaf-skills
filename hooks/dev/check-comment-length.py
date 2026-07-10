#!/usr/bin/env python3

import json, os, re, subprocess, sys

MAX_BLOCK = 3  # ponytail: max NEW prose-comment lines; raise if false positives nag

CSTYLE = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".rs",
    ".go",
    ".java",
    ".c",
    ".h",
    ".cc",
    ".cpp",
    ".hpp",
    ".cs",
    ".swift",
    ".kt",
    ".kts",
    ".scala",
    ".dart",
    ".php",
}
HASH = {".py", ".rb", ".sh", ".bash", ".zsh", ".pl", ".r"}


def classify(ext, raw):
    s = raw.strip()
    is_c = (ext in CSTYLE and s.startswith(("//", "/*", "*"))) or (
        ext in HASH and s.startswith("#")
    )
    if not is_c:
        return "code"
    body = s.lstrip("/*#! ").strip()
    if body == "" or body.startswith("@"):
        return "skip"  # /** */ * delimiter or @param/@return tag — not prose
    return "prose"


def scan(ext, diff):
    """Start lines of added comment blocks whose prose exceeds MAX_BLOCK."""
    hits, newno, prose, start, in_block = [], 0, 0, 0, False
    for line in diff.splitlines():
        if line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            newno = int(m.group(1)) if m else newno
            prose, in_block = 0, False
        elif line.startswith(("+++", "---")):
            continue
        elif line.startswith("+"):
            kind = classify(ext, line[1:])
            if kind == "code":
                prose, in_block = 0, False
            else:
                if not in_block:
                    in_block, start = True, newno
                if kind == "prose":
                    prose += 1
                    if prose == MAX_BLOCK + 1:
                        hits.append(start)
            newno += 1
        # removed (-) lines don't advance the new-file counter
    return hits


def sh(args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def main():
    try:
        cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    except Exception:
        sys.exit(0)
    if "git commit" not in cmd or "--no-verify" in cmd or "--amend" in cmd:
        sys.exit(0)
    try:
        files = sh(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"]
        ).split()
    except Exception:
        sys.exit(0)
    bad = []
    for f in files:
        ext = os.path.splitext(f)[1]
        if ext in CSTYLE or ext in HASH:
            bad += [
                f"{f}:{ln}"
                for ln in scan(ext, sh(["git", "diff", "--cached", "-U0", "--", f]))
            ]
    if bad:
        sys.stderr.write(
            f"comment-length backstop: staged diff adds comment block(s) > {MAX_BLOCK} lines.\n"
            "Trim (comments <=2 lines, docstrings <=3, params excluded) or run /review-changes.\n"
            "Deliberate? re-commit with --no-verify.\n"
            + "".join(f"  {b}\n" for b in bad)
        )
        sys.exit(2)  # exit 2 -> Claude Code blocks the commit
    sys.exit(0)


def selftest():
    d1 = "@@ -0,0 +1,4 @@\n+// one\n+// two\n+// three\n+// four\n"
    assert scan(".ts", d1) == [1], scan(".ts", d1)
    d2 = "@@ -0,0 +1,7 @@\n+/**\n+ * line one\n+ * line two\n+ * line three\n+ * @param a x\n+ * @param b y\n+ */\n"
    assert scan(".ts", d2) == [], scan(".ts", d2)
    d3 = "@@ -0,0 +1,5 @@\n+// a\n+// b\n+const x = 1\n+// c\n+// d\n"
    assert scan(".ts", d3) == [], scan(".ts", d3)
    d4 = "@@ -0,0 +1,4 @@\n+# a\n+# b\n+# c\n+# d\n"
    assert scan(".py", d4) == [1], scan(".py", d4)
    print("ok")


if __name__ == "__main__":
    (selftest if len(sys.argv) > 1 and sys.argv[1] == "selftest" else main)()
