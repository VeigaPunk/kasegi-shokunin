#!/usr/bin/env python3
"""Apply one C1 mutant from r46-mutbat.py's table to a tree-shaped scratch copy of the counter.

The counter resolves its instrument lane from its own path (TOOL_LANE = SELF's great-grandparent),
so the mutant must live in a tree layout: <out-root>/corpus/instruments/r46-c1-gate.py, with the
lane's whole instruments dir copied next to it (this is exactly what r46-mutbat.py's apply_mutant
does).  Otherwise every instrument the recheck lines run is missing and the counter reads garbage.

usage: make_mutant.py <mutant-id> <out-root>
Prints the mutant id and the mutant counter path.
"""
import importlib.util
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MUTBAT = LANE + "/corpus/instruments/r46-mutbat.py"
COUNTER = LANE + "/corpus/instruments/r46-c1-gate.py"

spec = importlib.util.spec_from_file_location("mutbat", MUTBAT)
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

mid = sys.argv[1]
root = os.path.abspath(sys.argv[2])
triple = next((t for t in mb.C1_MUTANTS if t[0] == mid), None)
if triple is None:
    raise SystemExit("no such C1 mutant: %s" % mid)
old, new = triple[1], triple[2]
src = open(COUNTER, encoding="utf-8").read()
n = src.count(old)
if n != 1:
    raise SystemExit("mutant %s: old substring occurs %d times (expected 1)" % (mid, n))
inst = os.path.join(root, "corpus", "instruments")
if os.path.isdir(root):
    shutil.rmtree(root)
os.makedirs(root)
shutil.copytree(os.path.join(LANE, "corpus", "instruments"), inst, symlinks=True)
out = os.path.join(inst, "r46-c1-gate.py")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(src.replace(old, new, 1))
print("mutant=%s counter=%s" % (mid, out))
