#!/usr/bin/env python3
"""CriticC1 r68 follow-up: commit-form git show probes with literal SHAs (tokenizer refuses ~)."""
import json, os, subprocess, sys

W = "/fast/scratch/hyaku/kasegi-r68/CriticC1/run"
REPO = os.path.join(W, "repo")
GATES = {
    "base": "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-68/controls/base-gate-d0f48405.py",
    "cand": "/fast/scratch/hyaku/kasegi-r68/CriticC1/gate-82b3b7d.py",
}
TWO, MERGE = "e501c93", "c5ff8bb"
PROBES = [
    ("g2-show-commit-default", "git show %s | grep -c y" % TWO),
    ("g2-show-commit-textconv", "git show --textconv %s | grep -c y" % TWO),
    ("g2-show-commit-no-textconv", "git show --no-textconv %s | grep -c y" % TWO),
    ("g2-show-commit-stat", "git show --stat %s | grep -c big" % TWO),
    ("g2-show-commit-p", "git show -p %s | grep -c y" % TWO),
    ("g2-show-commit-wd", "git show --word-diff %s | grep -c y" % TWO),
    ("g2-show-ext-diff", "git show --ext-diff %s | grep -c ext" % TWO),
    ("g2-show-ext-dif", "git show --ext-dif %s | grep -c ext" % TWO),
    ("g2-show-ext", "git show --ext %s | grep -c ext" % TWO),
    ("g2-show-no-ext-diff", "git show --no-ext-diff %s | grep -c y" % TWO),
    ("g2-show-merge-default", "git show %s | grep -c m" % MERGE),
    ("g2-show-merge-dd", "git show --diff-merges=dense-combined %s | grep -c m" % MERGE),
    ("g2-show-merge-first", "git show --first-parent %s | grep -c m" % MERGE),
    ("g2-show-range", "git show %s %s | grep -c y" % (TWO, MERGE)),
    ("g2-show-blob-textconv-eq", "git show --textconv=x HEAD:big.txt | head -n 1"),
    ("g2-ls-tree", "git ls-tree HEAD | wc -l"),
    ("g2-catfile-batch", "git cat-file --batch-check < big.txt"),
]


def lines(p):
    try:
        with open(p) as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0


for g, gate in GATES.items():
    for pid, derive in PROBES:
        env = dict(os.environ)
        marks = {}
        for m in ("COMP_MARK", "TC_MARK", "SM_MARK", "EXT_MARK", "PG_MARK"):
            p = os.path.join(W, "m2.%s.%s.%s" % (g, pid, m))
            open(p, "w").close()
            marks[m[:-5]] = p
            env[m] = p
        led = os.path.join(W, "led2.%s.%s.json" % (g, pid))
        with open(led, "w") as f:
            json.dump({"figures": [{"id": pid, "record": "x", "recorded": "?", "derive": derive, "want": "__nomatch__"}]}, f)
        p = subprocess.run([sys.executable, gate, "--ledger", led, "--root", REPO], cwd=W, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        out, err = p.stdout.decode(), p.stderr.decode()
        reason = ""
        for ln in (err + "\n" + out).splitlines():
            if "reason=" in ln:
                reason = ln.split("reason=", 1)[1].split()[0]
                break
            if ln.startswith("FIG "):
                reason = "derived=" + ln.split("derived=", 1)[1].split(" want=")[0][:30]
        mk = {k: lines(v) for k, v in marks.items() if lines(v)}
        print("PROBE gate=%s id=%s rc=%d reason=%s marks=%s derive=%r" % (g, pid, p.returncode, reason, mk or "{}", derive))
