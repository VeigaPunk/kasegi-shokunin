#!/usr/bin/env python3
"""Regression pass: for every mutant x tree, record BOTH directions of limb change
(0->1 = mutant accepts a defect the pristine gate rejected; 1->0 = mutant newly rejects
a tree the pristine gate accepted).  Also print the exact read tokens for the row12cells
and fencedf29 cases."""
from __future__ import annotations

import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"
import mutants as W1
import round2 as W2

RECIPES = {m[0]: (m[1], m[2], m[3]) for m in W1.MUTANTS}
RECIPES.update({m[0]: (m[1], m[2], m[3]) for m in W2.MUTANTS})
TREES = ["positive", "duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
         "row12cells", "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
         "longquote", "fewspans", "nestedmd", "entrymutant", "symlink", "junk", "fabricated",
         "src0740"]


def run(gate, tree):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    p = subprocess.run([sys.executable, gate, "--root", os.path.join(S, "trees", tree),
                        "--work", os.path.join(S, "work")],
                       capture_output=True, text=True, env=env, timeout=300)
    return p.stdout


def limbs(out):
    d = {}
    for m in re.finditer(r"^gate (H\d) pass=(\d) read=(.*)$", out, re.M):
        d[m.group(1)] = (int(m.group(2)), m.group(3))
    f = re.search(r"f29-gate fixed=(\d+)/7 exit=(\d+)", out)
    d["fixed"] = int(f.group(1)) if f else -1
    return d


base = {t: limbs(run(os.path.join(S, "mutants", "BASE", "r46-f29-gate.py"), t)) for t in TREES}
for mid in RECIPES:
    g = os.path.join(S, "mutants", mid, "r46-f29-gate.py")
    up, down = [], []
    for t in TREES:
        m = limbs(run(g, t))
        for h in ["H%d" % i for i in range(1, 8)]:
            if base[t][h][0] == 0 and m[h][0] == 1:
                up.append("%s:%s" % (t, h))
            if base[t][h][0] == 1 and m[h][0] == 0:
                down.append("%s:%s" % (t, h))
    print("%-34s up(0->1)=%-40s down(1->0)=%s" % (mid, ",".join(up) or "-", ",".join(down) or "-"))

print()
print("== C8 row12cells read tokens ==")
for mid in ["BASE", "C8-h3-cells-loose"]:
    out = run(os.path.join(S, "mutants", mid, "r46-f29-gate.py"), "row12cells")
    for ln in out.splitlines():
        if ln.startswith("gate ") or ln.startswith("f29-gate"):
            print("  %-22s %s" % (mid, ln))
print()
print("== A1 fencedf29 read tokens (mutant) ==")
out = run(os.path.join(S, "mutants", "A1-live-lines-fence-dropped", "r46-f29-gate.py"), "fencedf29")
for ln in out.splitlines():
    if ln.startswith("gate ") or ln.startswith("f29-gate"):
        print("  " + ln)
print()
print("== A5 src0740 read tokens (mutant) ==")
out = run(os.path.join(S, "mutants", "A5-s074-boundary-widened", "r46-f29-gate.py"), "src0740")
for ln in out.splitlines():
    if ln.startswith("gate ") or ln.startswith("f29-gate"):
        print("  " + ln)
print()
print("== F1 thinsection read tokens (mutant) ==")
out = run(os.path.join(S, "mutants", "F1-entry-size-floor", "r46-f29-gate.py"), "thinsection")
for ln in out.splitlines():
    if ln.startswith("gate ") or ln.startswith("f29-gate"):
        print("  " + ln)
print()
print("== B3 fewspans / E3 fewspans / F4+G1 symlink limb flips ==")
for mid, tree in [("B3-table-rows-floor", "fewspans"), ("E3-core-count", "fewspans"),
                  ("F4-symlink-clause-dropped", "symlink"), ("G1-symlink-guard-dropped", "symlink"),
                  ("C2-kind-literal-case", "kindcase")]:
    out = run(os.path.join(S, "mutants", mid, "r46-f29-gate.py"), tree)
    keep = [ln for ln in out.splitlines() if ln.startswith("f29-gate")]
    print("  %-30s %-10s %s" % (mid, tree, keep[0] if keep else "?"))
