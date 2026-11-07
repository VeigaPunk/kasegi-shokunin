#!/usr/bin/env python3
"""CriticHarm r97 check 3: build one fixture repo from the union of both
scanners' selftest cases, then let each scanner scan it via --rev.

The fixture bytes are the scanners' own synthetic plants (repeated-character
tokens), not credentials.
"""
import os
import subprocess
import sys
import textwrap
import re

BASE = sys.argv[1]
TIP = sys.argv[2]
DEST = sys.argv[3]


def cases(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"^def selftest\(pats\):\n(.*?)^    cases = \[\n(.*?)^    \]\n",
                  src, re.S | re.M)
    block = textwrap.dedent(m.group(1)) + "cases = [\n" + textwrap.dedent(m.group(2)) + "]\n"
    ns = {}
    exec(compile(block, path, "exec"), ns)
    return ns["cases"]


base = cases(BASE)
tip = cases(TIP)
bmap = {n: (d, w) for n, d, w in base}
tmap = {n: (d, w) for n, d, w in tip}
print("base=%d tip=%d" % (len(bmap), len(tmap)))
shared = set(bmap) & set(tmap)
changed = [n for n in shared if bmap[n] != tmap[n]]
print("shared=%d shared_changed=%s base_only=%s"
      % (len(shared), sorted(changed), sorted(set(bmap) - set(tmap))))

names = sorted(tmap)
root = os.path.join(DEST, "corpus", "source-snapshots", "r97-critic")
os.makedirs(root, exist_ok=True)
for n in names:
    data = tmap[n][0]
    with open(os.path.join(root, n + ".txt"), "wb") as fh:
        fh.write(data + b"\n")
print("wrote=%d" % len(names))
