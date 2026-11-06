#!/usr/bin/env python3
"""Build a labelled S116 entry whose rule text is worthless filler, for the B8 gate."""
import json
import sys

MAN = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-82/manifest.json"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
OUT = sys.argv[1]

man = json.load(open(MAN))
src = man["sources"][0]
L = []
L.append("# Junk S116 entry: six located quotes, worthless rule text")
L.append("")
L.append("source: S116 — https://google.github.io/osv.dev/data_quality.html (anchor: junk test)")
L.append("verified-at: 2026-11-06")
L.append("recheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest "
         "corpus/source-snapshots/round-82/manifest.json --source S116" % LANE)
L.append("")
for i, q in enumerate(src["quotes"], 1):
    L.append("## Claim %d — filler" % i)
    L.append("")
    L.append('"%s" (S116.txt:%d). Filler prose that adds nothing to the quote.' % (q["quote"], q["anchor"]))
    L.append("")
    L.append("Falsifiable rule: Nothing here matters, check nothing at all and ignore the "
             "record entirely (S116.txt:%d)." % q["anchor"])
    L.append("Rejected over-generalization, not a page sentence: No over-generalization applies "
             "here because this sentence is deliberately meaningless filler (S116.txt:%d)." % q["anchor"])
    L.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("wrote %s lines=%d" % (OUT, len(L)))
