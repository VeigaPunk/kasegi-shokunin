#!/usr/bin/env python3
"""Conformance check of the pristine runs vs the frozen receipt, and a
markdown summary table for the report."""
import json
import os
import re

S = "/fast/scratch/hyaku/kasegi-r85/MutC1Counter"
W = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85"
RECEIPT = os.path.join(W, "controls", "c1-controls-r85.txt")
frozen = json.load(open(os.path.join(S, "frozen_matrix.json")))
proposed = json.load(open(os.path.join(S, "proposed_matrix.json")))
clone = json.load(open(os.path.join(S, "clone_matrix.json")))
limb = json.load(open(os.path.join(S, "limb_matrix.json")))

# --- conformance vs receipt -------------------------------------------------
txt = open(RECEIPT, encoding="utf-8").read()
blocks = {}
cur = None
for ln in txt.split("\n"):
    m = re.match(r"== control (\S+) \(expected: (\S+)\)", ln)
    if m:
        cur = m.group(1)
        blocks[cur] = {"exp": m.group(2), "lines": []}
        continue
    if cur and (ln.startswith("SKILL-METER") or ln.startswith("LIMB")):
        blocks[cur]["lines"].append(ln)
ok = True
for name, b in blocks.items():
    got = [ln for ln in frozen["pristine"]["controls"][name]["stdout"].split("\n")
           if ln.startswith("SKILL-METER") or ln.startswith("LIMB")]
    same = got == b["lines"]
    ok = ok and same
    print("receipt %-22s expected=%-4s lines_match=%s rc=%d" %
          (name, b["exp"], same, frozen["pristine"]["controls"][name]["rc"]))
print("RECEIPT CONFORMANCE:", "PASS" if ok else "FAIL")

# --- kill tables ------------------------------------------------------------
ctrl_names = ["donothing", "pad-resolving-cites", "delete-gone-cites",
              "wrong-target", "partial-9-of-18", "positive"]
new_rc = ["C1-wrong-denominator-target", "C2-blank-line-appended",
          "C3-mapsha-tail-corrupt", "C4-map-value-under-ufo",
          "C5-map-value-wrong-basename"]
new_clone = ["C6-map-value-missing-worktree", "C7-base-key-resolving"]
new_limb = ["C8-wrong-target-M2", "C9-extra-decite-M2", "C10-ghost-key-M3hit"]


def kills(runset):
    return [c for c in runset if runset[c].get("rc") == 0]


print()
print("| mutant | frozen rc controls | new rc controls | new limb controls |")
print("|---|---|---|---|")
for mid, *_ in []:
    pass

import importlib.util
spec = importlib.util.spec_from_file_location("driver", os.path.join(S, "driver.py"))
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

for mid, old, new, note in driver.MUTANTS:
    fk = kills(frozen[mid]["controls"])
    pk = [c for c in new_rc if proposed.get(c + "::" + mid, {}).get("rc") == 0]
    pk += [c for c in new_clone if clone[c]["runs"].get(mid, {}).get("rc") == 0]
    lk = [c for c in new_limb if mid in limb[c]["kills"]]
    print("| %s | %s | %s | %s |" % (
        mid, ", ".join(fk) or "SURVIVED", ", ".join(pk) or "-",
        ", ".join(lk) or "-"))
