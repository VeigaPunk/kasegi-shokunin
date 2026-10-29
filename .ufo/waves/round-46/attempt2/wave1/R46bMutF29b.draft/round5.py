#!/usr/bin/env python3
"""Round 5: (a) the E7+E8 two-line combination probe (outside the single-line set, reported
separately) on junk/fabricated; (b) exact printouts for the mutants that break the positive."""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SRC = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
RECHECK = os.path.join(LANE, "corpus/instruments/source-recheck.py")

COMBO = [
    ("and b - a <= 11 and nq in window:", "and b - a <= 11:"),
    ("and len(passed) >= 4 and len(cores) == len(CORES)", "and len(passed) >= 4"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(gate, tree):
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    p = subprocess.run([sys.executable, gate, "--root", os.path.join(S, "trees", tree),
                        "--work", os.path.join(S, "work")],
                       capture_output=True, text=True, env=env, timeout=300)
    return p.stdout


def build_combo():
    d = os.path.join(S, "mutants", "COMBO-E7E8-two-line")
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    text = open(SRC, encoding="utf-8").read()
    for old, new in COMBO:
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new, 1)
    g = os.path.join(d, "r46-f29-gate.py")
    open(g, "w", encoding="utf-8").write(text)
    shutil.copy(RECHECK, os.path.join(d, "source-recheck.py"))
    return g


def main():
    g = build_combo()
    print("COMBO (2 lines: drop the location conjunct AND the cores conjunct) sha=%s" % sha(open(g, "rb").read())[:12])
    for t in ("positive", "junk", "fabricated"):
        out = run(g, t)
        keep = [ln for ln in out.splitlines() if ln.startswith("gate H5") or ln.startswith("f29-gate")]
        print("  %-11s %s" % (t, " | ".join(keep)))
    print()
    print("== positive-breaking mutants, exact printouts ==")
    for mid, tree in [("C2-kind-literal-case", "positive"), ("C3-tier-literal", "positive"),
                      ("E11-h5-quoted-ascii-filter", "positive"),
                      ("E11-h5-quoted-ascii-filter", "thinscope")]:
        out = run(os.path.join(S, "mutants", mid, "r46-f29-gate.py"), tree)
        print("--- mutant=%s tree=%s" % (mid, tree))
        for ln in out.splitlines():
            if ln.startswith("gate ") or ln.startswith("f29-gate"):
                print("  " + ln)
    print()
    print("== do-nothing controls, all trees (must be identical to BASE) ==")
    for mid in ("Z0-do-nothing-whitespace", "Z1-do-nothing-comment"):
        outs = []
        for t in ("positive", "junk", "src0740", "symlink", "row12cells"):
            o = run(os.path.join(S, "mutants", mid, "r46-f29-gate.py"), t)
            outs.append(re.search(r"f29-gate fixed=\d+/7 exit=\d", o).group(0))
        print("  %-28s %s" % (mid, " ".join(outs)))
    print("# original gate sha256 = %s" % sha(open(SRC, "rb").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
