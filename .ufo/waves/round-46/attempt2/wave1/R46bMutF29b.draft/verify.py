#!/usr/bin/env python3
"""Full verification matrix for the R46bMutF29b battery: every mutant x every tree,
with the recipe and the sha256 of the mutant copy. Emits a TSV + a readable summary."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SRC = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
RECHECK = os.path.join(LANE, "corpus/instruments/source-recheck.py")

TREES = ["positive", "duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
         "row12cells", "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
         "longquote", "fewspans", "nestedmd", "entrymutant", "symlink", "junk", "fabricated",
         "src0740"]

# recipes: id -> (limb, old, new)
import mutants as W1
import round2 as W2

RECIPES = {m[0]: (m[1], m[2], m[3]) for m in W1.MUTANTS}
RECIPES.update({m[0]: (m[1], m[2], m[3]) for m in W2.MUTANTS})


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
    pristine = open(SRC, "rb").read()
    base = {t: limbs(run(os.path.join(S, "mutants", "BASE", "r46-f29-gate.py"), t)) for t in TREES}
    rows = []
    for mid, (limb, old, new) in RECIPES.items():
        d = os.path.join(S, "mutants", mid)
        g = os.path.join(d, "r46-f29-gate.py")
        if not os.path.exists(g):
            # rebuild deterministically
            os.makedirs(d, exist_ok=True)
            text = pristine.decode()
            assert text.count(old) == 1, (mid, text.count(old))
            open(g, "w", encoding="utf-8").write(text.replace(old, new, 1))
            shutil_copy = RECHECK
            import shutil
            shutil.copy(shutil_copy, os.path.join(d, "source-recheck.py"))
        m_sha = sha(open(g, "rb").read())
        flips, full, posbroken = [], [], []
        for t in TREES:
            m = limbs(run(g, t))
            if t == "positive":
                if m["fixed"] < 7:
                    posbroken.append("H%s" % ",".join(h for h in ["H%d" % i for i in range(1, 8)]
                                                       if m[h][0] == 0))
                continue
            f = [h for h in ["H%d" % i for i in range(1, 8)] if base[t][h][0] == 0 and m[h][0] == 1]
            if f:
                flips.append("%s:%s" % (t, ",".join(f)))
            if base[t]["fixed"] < 7 and m["fixed"] == 7:
                full.append(t)
        cls = "FALSE-GREEN" if full else ("LIMP-FLIP" if flips else
                                          ("POS-BREAK" if posbroken else "SURVIVOR"))
        print("%-34s %-6s %-11s pos=%d/7 %s" % (mid, limb, cls, limbs(run(g, "positive"))["fixed"],
                                                ";".join(full or flips or posbroken) or "-"))
        rows.append((mid, limb, cls, m_sha, old, new, ";".join(full or flips or posbroken)))
    print()
    print("# recipe + sha table")
    for mid, limb, cls, m_sha, old, new, note in rows:
        print("MUTANT %s limb=%s verdict=%s sha256=%s" % (mid, limb, cls, m_sha))
        print("  old: %s" % old.replace("\n", "\\n"))
        print("  new: %s" % new.replace("\n", "\\n"))
        print("  observed: %s" % note)
    with open(os.path.join(S, "runs", "matrix.tsv"), "w", encoding="utf-8") as fh:
        fh.write("mutant\tlimb\tverdict\tsha256\trecipe_old\trecipe_new\tobserved\n")
        for mid, limb, cls, m_sha, old, new, note in rows:
            fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (mid, limb, cls, m_sha,
                                                       old.replace("\n", "\\n"), new.replace("\n", "\\n"), note))
    print("# original gate sha256 (after) = %s" % sha(open(SRC, "rb").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
