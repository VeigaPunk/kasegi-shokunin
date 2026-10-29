#!/usr/bin/env python3
"""Round 4: how many independent conjuncts must be removed before the junk / fabricated
entry (quotes the snapshot does not hold) is accepted?  Each mutant drops exactly ONE
conjunct of the H5 verdict."""
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
    ("E7-h5-location-conjunct", "H5",
     "and b - a <= 11 and nq in window:",
     "and b - a <= 11:",
     "drop the 'quoted span is located in the snapshot' conjunct"),
    ("E8-h5-cores-conjunct", "H5",
     "and len(passed) >= 4 and len(cores) == len(CORES)",
     "and len(passed) >= 4",
     "drop the 'all five frozen cores present' conjunct"),
    ("E9-h5-failed-conjunct", "H5",
     "ok = failed == 0 and uncited <= 0 and",
     "ok = uncited <= 0 and",
     "drop the 'no failed span' conjunct"),
    ("E10-h5-passed-conjunct", "H5",
     "and len(passed) >= 4 and len(cores) == len(CORES)",
     "and len(cores) == len(CORES)",
     "drop the '>= 4 located spans' conjunct"),
    ("E11-h5-quoted-ascii-filter", "H5",
     '[q for q in re.findall(\'"([^"]+)"\', raw, re.S) if len(q.split()) >= 4]',
     '[q for q in re.findall(\'"([^"]+)"\', raw, re.S) if len(q.split()) >= 1]',
     "lower the ASCII-quote word filter from 4 to 1"),
]
TREES = ["positive", "junk", "fabricated", "widespan", "longquote", "fewspans", "thinscope",
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
        note = []
        for t in TREES:
            m = limbs(run(g, t))
            if t == "positive":
                note.append("pos=%d/7" % m["fixed"])
                continue
            for h in ["H%d" % i for i in range(1, 8)]:
                if base[t][h][0] == 0 and m[h][0] == 1:
                    note.append("UP %s:%s" % (t, h))
                if base[t][h][0] == 1 and m[h][0] == 0:
                    note.append("DOWN %s:%s" % (t, h))
            if base[t]["fixed"] < 7 and m["fixed"] == 7:
                note.append("FULLGREEN %s" % t)
        print("MUTANT %-28s limb=%s sha=%s %s" % (mid, limb, sha(open(g, "rb").read())[:12],
                                                  " ".join(note)))
        for t in ("junk", "fabricated"):
            out = run(g, t)
            keep = [ln for ln in out.splitlines() if ln.startswith("gate H5") or ln.startswith("f29-gate")]
            print("    %-11s %s" % (t, " | ".join(keep)))
    print("# original gate sha256 = %s" % sha(open(SRC, "rb").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
