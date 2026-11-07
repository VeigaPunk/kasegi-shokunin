#!/usr/bin/env python3
"""Summarise the mutation sweep from the saved per-(mutant,control) meter outputs."""
import glob
import json
import os
import re

S = "/fast/scratch/hyaku/kasegi-r88/MutC1Counter"
OUT = os.path.join(S, "out")
ORDER = ["do-nothing", "positive", "partial", "pad", "drift-forge", "notentry-forge",
         "ufo-copy", "map-sha", "N1-drift-target", "N2-pos-denom", "N3-dups", "N4-ghost-key",
         "N5-zero-anchor", "N6-big-anchor", "N7-single-drift", "N8-trunc", "N9-slash-key",
         "N10-mixed-drift", "N11-deleted-entry", "N12-truncated-target", "N13-dot-entry",
         "N14-slash-anchored", "N15-word4-share"]
FROZEN = ORDER[:8]


def parse(path):
    limbs, res, rc = {}, "", None
    for ln in open(path):
        if ln.startswith("LIMB "):
            p = ln.split()
            limbs[p[1]] = p[2]
        elif ln.startswith("KNOWLEDGE-METER-RESULT"):
            res = ln.strip()
        elif ln.startswith("[exit "):
            rc = int(re.search(r"-?\d+", ln).group())
    return {"limbs": limbs, "res": res, "rc": rc}


data = {}
for p in glob.glob(os.path.join(OUT, "*.txt")):
    base = os.path.basename(p)[:-4]
    if "__" not in base:
        continue
    m, c = base.split("__", 1)
    data.setdefault(m, {})[c] = parse(p)
ref = data["p00-pristine"]
summary = {}
for m in sorted(data):
    row = data[m]
    lb = [c for c in ORDER if c in row and row[c]["limbs"] != ref[c]["limbs"]]
    rb = [c for c in ORDER if c in row and row[c]["rc"] != ref[c]["rc"]]
    fl = [c for c in lb if c in FROZEN]
    summary[m] = {"killed_by_frozen_limb": fl, "killed_by_new_limb": [c for c in lb if c not in FROZEN],
                  "rc_changed_frozen": [c for c in rb if c in FROZEN],
                  "rc_changed_new": [c for c in rb if c not in FROZEN],
                  "verdict": "killed" if (lb or rb) else "SURVIVED",
                  "limbs": {c: row[c]["limbs"] for c in ORDER if c in row},
                  "rc": {c: row[c]["rc"] for c in ORDER if c in row}}
json.dump({"pristine": ref, "summary": summary}, open(os.path.join(S, "summary.json"), "w"), indent=1, sort_keys=True)

print("PRISTINE: " + " | ".join("%s rc=%s %s" % (c, ref[c]["rc"], ",".join("%s=%s" % (k, v) for k, v in sorted(ref[c]["limbs"].items()))) for c in ORDER))
print()
for m, s in summary.items():
    diff = []
    for c in ORDER:
        if c not in s["limbs"]:
            continue
        d = ["%s.%s:%s->%s" % (c, k, ref[c]["limbs"].get(k), v) for k, v in s["limbs"][c].items() if ref[c]["limbs"].get(k) != v]
        if d:
            diff.append(" ".join(d))
    print("%-28s %-9s frozen=%s new=%s | %s" % (m, s["verdict"], ",".join(s["killed_by_frozen_limb"]) or "-",
                                                ",".join(s["killed_by_new_limb"]) or "-", " ; ".join(diff)[:300]))
