#!/usr/bin/env python3
"""Round 3: three more mutants that reproduce the R50 receipt's remaining three verdicts
(H2b wordfloor-low, H4c distinct-dropped, H6a counts-loose), so that every one of the
receipt's 21 verdicts is independently re-measured by this seat."""
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

MUTANTS = [
    ("H2b-h2-wordfloor-low", "H2",
     'sect_words(body, sct) >= (12 if sct.startswith("## Falsifiable") else 25)',
     'sect_words(body, sct) >= (1 if sct.startswith("## Falsifiable") else 5)',
     "receipt H2b shape: lower the per-section word floor"),
    ("H4c-h4-distinct-dropped", "H4",
     'and "BROKEN" not in out and distinct',
     'and "BROKEN" not in out',
     "receipt H4c shape: drop the quote-distinctness conjunct"),
    ("H6a-h6-counts-loose", "H6",
     "len(names) == 66 and len(everything) == 66 and nested == 66",
     "len(names) >= 66 and len(everything) >= 66 and nested >= 66",
     "receipt H6a shape: relax the three knowledge-dir counts to lower bounds"),
]

TREES = ["positive", "duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
         "row12cells", "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
         "longquote", "fewspans", "nestedmd", "entrymutant", "symlink", "junk", "fabricated",
         "src0740"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


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


def main():
    base = {t: limbs(run(os.path.join(S, "mutants", "BASE", "r46-f29-gate.py"), t)) for t in TREES}
    pristine = open(SRC, "rb").read()
    for mid, limb, old, new, intent in MUTANTS:
        d = os.path.join(S, "mutants", mid)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        text = pristine.decode()
        n = text.count(old)
        if n != 1:
            print("MUTANT %s ABORT: old occurs %d times" % (mid, n))
            continue
        g = os.path.join(d, "r46-f29-gate.py")
        open(g, "w", encoding="utf-8").write(text.replace(old, new, 1))
        shutil.copy(RECHECK, os.path.join(d, "source-recheck.py"))
        up, down, full = [], [], []
        for t in TREES:
            m = limbs(run(g, t))
            for h in ["H%d" % i for i in range(1, 8)]:
                if base[t][h][0] == 0 and m[h][0] == 1:
                    up.append("%s:%s" % (t, h))
                if base[t][h][0] == 1 and m[h][0] == 0:
                    down.append("%s:%s" % (t, h))
            if t != "positive" and base[t]["fixed"] < 7 and m["fixed"] == 7:
                full.append(t)
        print("MUTANT %-26s limb=%s sha=%s up=%s down=%s full_false_green=%s"
              % (mid, limb, sha(open(g, "rb").read())[:12], ",".join(up) or "-",
                 ",".join(down) or "-", ",".join(full) or "-"))
        for t in ("fewspans", "nestedmd", "positive", "thinsection"):
            out = run(g, t)
            keep = [ln for ln in out.splitlines() if ln.startswith("f29-gate")]
            print("   %-12s %s" % (t, keep[0] if keep else "?"))
    print("# original gate sha256 = %s" % sha(open(SRC, "rb").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
