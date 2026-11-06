#!/usr/bin/env python3
"""Turn calib.json into the calibration table + cause taxonomy; also prove the perfection
claim of B8 against the three entries it passes."""
import json
import os
import re
import sys

S = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(S, "calib.json"), encoding="utf-8"))
KN = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge"


def nums(line):
    d = {}
    for k in ("claims", "want", "spans", "mislocated", "overlong", "claimless", "unpinned"):
        m = re.search(k + r"=(-?\d+)", line)
        d[k] = int(m.group(1)) if m else None
    d["header"] = "ok" if "header=ok" in line else "bad"
    return d


def cause(r):
    n = nums(r["line"])
    if not r["line"]:
        return "no-gate-line"
    bad = []
    if n["header"] != "ok":
        bad.append("G1-header")
    if n["claims"] != n["want"]:
        bad.append("G3-claim-count")
    if n["spans"] == 0:
        bad.append("G2-no-spans")
    if n["mislocated"]:
        bad.append("G2-mislocated")
    if n["overlong"]:
        bad.append("G2-overlong")
    if n["claimless"]:
        bad.append("G3-marker-missing")
    if n["unpinned"]:
        bad.append("G4-unpinned")
    return "+".join(bad) if bad else "PASS"


# entry -> number of source lines (joint entries)
entry_sids = {}
for name in sorted(os.listdir(KN)):
    if name.endswith(".md"):
        txt = open(os.path.join(KN, name), encoding="utf-8").read()
        entry_sids[name] = re.findall(r"(?m)^source: (S\d{3}) ", txt)

out = []
for r in rows:
    c = cause(r)
    r["cause"] = c
    r["joint"] = len(entry_sids.get(r["entry"], []))
    out.append(r)
json.dump(out, open(os.path.join(S, "calib2.json"), "w"), indent=1)

print("## per-row")
for r in out:
    print("| %s | %s | %s | %s | %s |" % (r["round"].replace("corpus/source-snapshots/", ""),
                                          r["sid"], r["entry"], r["verdict"].replace("ENTRY-GATE-RESULT ", ""),
                                          r["cause"]))

from collections import Counter
print("\n## cause counts")
for c, n in Counter(r["cause"] for r in out).most_common():
    print("%-40s %d" % (c, n))
print("\n## pass set")
for r in out:
    if r["verdict"].endswith("pass"):
        print(r["round"], r["sid"], r["entry"])
print("\n## joint entries among failures:",
      sum(1 for r in out if r["verdict"].endswith("fail") and r["joint"] > 1),
      "rows;", len({r["entry"] for r in out if r["verdict"].endswith("fail") and r["joint"] > 1}),
      "entries")
print("## header-ok but fail:", sum(1 for r in out if r["verdict"].endswith("fail") and "header=ok" in r["line"]))
print("## rows:", len(out))
allpairs = sum(len(v) for v in entry_sids.values())
print("## entry/sid pairs total=%d covered-by-manifest=%d entries=%d" % (allpairs, len(out), len(entry_sids)))
