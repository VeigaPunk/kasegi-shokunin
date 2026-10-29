#!/usr/bin/env python3
"""Quote the printed gate lines for the mutants that matter, plus verify census equivalence."""
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"


def run(gate, tree):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    p = subprocess.run([sys.executable, gate, "--root", os.path.join(S, "trees", tree),
                        "--work", os.path.join(S, "work")],
                       capture_output=True, text=True, env=env, timeout=300)
    return p.stdout


PAIRS = [
    ("BASE", "positive"), ("BASE", "fencedf29"), ("BASE", "fewspans"), ("BASE", "thinsection"),
    ("BASE", "symlink"), ("BASE", "kindcase"), ("BASE", "duprow"), ("BASE", "fewquotes"),
    ("BASE", "nestedmd"),
    ("A1-live-lines-fence-dropped", "fencedf29"), ("A1-live-lines-fence-dropped", "positive"),
    ("A5-s074-boundary-widened", "src0740"),
    ("B3-table-rows-floor", "fewspans"),
    ("C2-kind-literal-case", "kindcase"), ("C2-kind-literal-case", "positive"),
    ("C3-tier-literal", "positive"),
    ("E3-core-count", "fewspans"),
    ("F1-entry-size-floor", "thinsection"),
    ("F4-symlink-clause-dropped", "symlink"),
    ("G1-symlink-guard-dropped", "symlink"),
    ("A4-one-live-row-loosened", "duprow"),
    ("D3-quote-count-floor", "fewquotes"),
    ("E4-passed-floor", "fewspans"),
    ("F3-nested-count", "nestedmd"),
    ("Z0-do-nothing-whitespace", "positive"), ("Z1-do-nothing-comment", "positive"),
]

for mid, tree in PAIRS:
    gate = os.path.join(S, "mutants", mid, "r46-f29-gate.py")
    out = run(gate, tree)
    print("=== mutant=%s tree=%s ===" % (mid, tree))
    for ln in out.splitlines():
        if ln.startswith("gate ") or ln.startswith("f29-gate"):
            print("  " + ln)
