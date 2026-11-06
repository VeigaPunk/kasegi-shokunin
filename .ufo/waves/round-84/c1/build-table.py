#!/usr/bin/env python3
"""build-table.py — round-84 C1 mutant table for the frozen candidate.

Carries the 67 frozen round-83 rows (.ufo/waves/round-83/c1/mutant-table.json) unchanged in
id, class, anchor, replacement, kill_cases and extra. Twelve rows are new: the twelve
round-83 MutC1Hunt survivors (.ufo/waves/round-83/w1/MutC1Hunt-rows.json), copied with their
anchor and replacement bytes unchanged, renamed H01-H12 and each declared, before any run,
with the round-84 check meant to kill it:

  H01 MUT-CF-noprefix-ge          -> noprefix-only    (G-1)
  H02 MUT-CF-noprefix-ne1         -> noprefix-only    (G-1)
  H03 MUT-SUM-swap-exit1-other    -> summary-fields   (G-2)
  H04 MUT-SUM-other-as-norecheck  -> summary-fields   (G-2)
  H05 MUT-MV-drop-noprefix-pass   -> entry-bare-pass  (G-3)
  H06 MUT-AP-root-no-value        -> argv-values      (G-4)
  H07 MUT-AP-lane-no-value        -> argv-values      (G-4)
  H08 MUT-AP-verbose-as-lane      -> verbose-order    (G-5)
  H09 MUT-AP-root-no-abspath      -> argv-values      (G-6)
  H10 MUT-AP-selftest-last        -> argv-values      (G-7)
  H11 MUT-MV-extra-nonzero        -> entry-set        (G-8)
  H12 MUT-MV-timeout-label        -> entry-set        (G-8)

Every anchor (and every "extra" anchor) must occur exactly once in the candidate (checked
here, exit 1 if not).
Usage: python3 build-table.py <candidate.py> <out.json>   (run from the lane root)
"""
import json
import sys

OLD = ".ufo/waves/round-83/c1/mutant-table.json"
HUNT = ".ufo/waves/round-83/w1/MutC1Hunt-rows.json"
NEW = [
    ("H01", "MUT-CF-noprefix-ge", "noprefix-only"),
    ("H02", "MUT-CF-noprefix-ne1", "noprefix-only"),
    ("H03", "MUT-SUM-swap-exit1-other", "summary-fields"),
    ("H04", "MUT-SUM-other-as-norecheck", "summary-fields"),
    ("H05", "MUT-MV-drop-noprefix-pass", "entry-bare-pass"),
    ("H06", "MUT-AP-root-no-value", "argv-values"),
    ("H07", "MUT-AP-lane-no-value", "argv-values"),
    ("H08", "MUT-AP-verbose-as-lane", "verbose-order"),
    ("H09", "MUT-AP-root-no-abspath", "argv-values"),
    ("H10", "MUT-AP-selftest-last", "argv-values"),
    ("H11", "MUT-MV-extra-nonzero", "entry-set"),
    ("H12", "MUT-MV-timeout-label", "entry-set"),
]


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        src = fh.read()
    with open(OLD, encoding="utf-8") as fh:
        out = [dict(r) for r in json.load(fh)]
    with open(HUNT, encoding="utf-8") as fh:
        hunt = {r["id"]: r for r in json.load(fh)}
    for rid, hid, case in NEW:
        h = hunt[hid]
        out.append({"id": rid, "anchor": h["anchor"], "replacement": h["replacement"],
                    "class": "assertion", "kill_cases": [case],
                    "expect": "r83 MutC1Hunt %s -> %s FAIL" % (hid, case)})
    bad = [r["id"] for r in out if src.count(r["anchor"]) != 1
           or any(src.count(a) != 1 for a, _b in r.get("extra", []))]
    if bad:
        print("build-table: anchors not unique/present: %s" % bad, file=sys.stderr)
        return 1
    with open(argv[2], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("build-table rows=%d neutral=%d new=%d"
          % (len(out), sum(r["class"] == "neutral" for r in out), len(NEW)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
