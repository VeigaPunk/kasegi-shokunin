#!/usr/bin/env python3
"""R46bMutSelfC1b — materialise mutant counter copies for the differential probes."""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutrun  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SRC = os.path.join(LANE, "corpus/instruments/r46-c1-gate.py")
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
text = open(SRC, encoding="utf-8").read()

# pristine copy
shutil.copyfile(SRC, os.path.join(OUT, "pristine-gate.py"))

for mid, old, new in mutrun.MUTANTS:
    n = text.count(old)
    if n != 1:
        print("SKIP %-34s old occurs %d times" % (mid, n))
        continue
    p = os.path.join(OUT, mid + "-gate.py")
    open(p, "w", encoding="utf-8").write(text.replace(old, new, 1))
    print("WROTE %-34s %s" % (mid, p))
