#!/usr/bin/env python3
"""Round 2 of the R46bMutF29b battery: clauses the first wave left ungraded, plus a
12-cell S074 row tree to test the R50 receipt's disclosure (c) independently."""
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
    ("A6-h1-count-line-disabled", "H1",
     "    if len(rows) != 29 or adm != 29 or dup:",
     "    if False:",
     "disable the whole H1 count/dup line: probes whether duprow/fencedf29 have a second holder"),
    ("A7-h1-counts-loose", "H1",
     "    if len(rows) != 29 or adm != 29 or dup:",
     "    if len(rows) < 29 or adm < 29 or dup:",
     "relax the row/admitted counts to lower bounds (receipt H1a shape)"),
    ("B6-h2-source-line-dropped", "H2",
     "good = ok_s and ok_v and ok_r and secs == len(SECTIONS)",
     "good = ok_v and ok_r and secs == len(SECTIONS)",
     "drop the provenance source-line conjunct of H2"),
    ("B7-h2-recheck-form-loosened", "H2",
     'and any(RECHECK_LINE.match(h) for h in head)',
     'and any(h.startswith("recheck:") for h in head)',
     "relax the exact recheck-line form to a prefix"),
    ("C6-h3-status-literal", "H3",
     'if row[7] != "mined": bad.append("status")',
     'if False: bad.append("status")',
     "drop the status literal"),
    ("C7-h3-opened-literal", "H3",
     'if row[8] != VERIFIED_AT: bad.append("opened")',
     'if False: bad.append("opened")',
     "drop the opened-date literal"),
    ("C8-h3-cells-loose", "H3",
     "        if len(c) == 11:",
     "        if len(c) >= 9:",
     "relax the 11-cell row shape to >= 9 (receipt H3a shape)"),
    ("E6-h5-live-span-requirement", "H5",
     "cores = [c for c in CORES if any(re.search(c, q) for q in passed if q in live_spans)]",
     "cores = [c for c in CORES if any(re.search(c, q) for q in passed)]",
     "drop the 'core must be live text' requirement"),
]


def sha(b: bytes) -> str:
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


def build_row12() -> None:
    """A 12-cell S074 registry row: the base gate rejects it on the 11-cell shape alone."""
    dst = os.path.join(S, "trees", "row12cells")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(S, "trees", "positive"), dst, symlinks=True)
    p = os.path.join(dst, "corpus/SOURCES.md")
    lines = open(p, encoding="utf-8").read().splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.startswith("| S074 |"):
            c = ln.strip().strip("|").split("|")
            c.append(" extra-cell")
            lines[i] = "|" + "|".join(c) + "|\n"
            break
    else:
        raise SystemExit("S074 row not found")
    open(p, "w", encoding="utf-8").write("".join(lines))


def main() -> int:
    build_row12()
    trees = ["positive", "row12cells", "row9cells", "duprow", "fencedf29", "junk",
             "fabricated", "fewspans", "kindcase", "thinscope", "thinsection", "symlink",
             "manws", "fewquotes", "dupquote", "widespan", "longquote", "vjunk", "badnames",
             "nestedmd", "entrymutant", "src0740"]
    pristine = open(SRC, "rb").read()
    base = {}
    for t in trees:
        base[t] = limbs(run(os.path.join(S, "mutants", "BASE", "r46-f29-gate.py"), t))
    print("# BASE row12cells: " + " ".join("%s=%d" % (h, base["row12cells"][h][0]) for h in ["H%d" % i for i in range(1, 8)]))
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
        flips, full = [], []
        for t in trees:
            m = limbs(run(g, t))
            if t == "positive":
                if m["fixed"] < 7:
                    full.append("POSITIVE-BROKEN(%s)" % t)
                continue
            f = [h for h in ["H%d" % i for i in range(1, 8)]
                 if base[t][h][0] == 0 and m[h][0] == 1]
            if f:
                flips.append("%s:%s" % (t, ",".join(f)))
            if base[t]["fixed"] < 7 and m["fixed"] == 7:
                full.append(t)
        print("MUTANT %-34s sha=%s pos=%d/7 flips=%s full=%s"
              % (mid, sha(open(g, "rb").read())[:12],
                 limbs(run(g, "positive"))["fixed"], flips if flips else "-", full if full else "-"))
    print("# original gate sha256 = %s" % sha(open(SRC, "rb").read()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
