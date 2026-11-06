#!/usr/bin/env python3
"""build-table.py — round-82 C1 mutant table for the frozen candidate.

Carries the 59 frozen round-81 rows (.ufo/waves/round-81/c1/mutant-table.json) unchanged in
id, class, replacement intent and kill_cases. Two of them, S04 and S05, mutated main()'s
inline conform expression, which round 82 moves into conform_ok(); they are re-anchored on
the same conjunct in conform_ok (same dropped conjunct, same kill case conform-limbs).
Four rows are new, each declared with the round-82 check meant to kill it, before any run:

  J1    round-81 CriticClaims (c) junk edit: an entry counted, then skipped when its name
        starts with "osv-" (w1/CriticClaims-receipts/candidate-junkedit.py)  -> bucket-sum
  S07M  round-81 ReviewC1 Major 1, the routed r80 S07 survivor: main()'s verbose default
        flipped to True                                                       -> main-default
  B1    conform_ok drops the bucket-sum conjunct                              -> bucket-sum
  B2    main() bypasses conform_ok with the round-81 four-limb expression     -> bucket-sum

Every row's anchor must occur exactly once in the candidate (checked here, exit 1 if not).
Usage: python3 build-table.py <candidate.py> <out.json>
"""
import json
import sys

OLD = ".ufo/waves/round-81/c1/mutant-table.json"
REANCHOR = {
    "S04": ('    return (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n            and',
            '    return (counts["noprefix"] == 0\n            and'),
    "S05": ('            and counts["norecheck"] == 0 and counts["restoration_only"] == 0\n',
            '            and counts["restoration_only"] == 0\n'),
}
NEW = [
    ("J1", '        counts["entries"] += 1\n',
     '        counts["entries"] += 1\n        if name.startswith("osv-"):\n            continue\n',
     "bucket-sum", "an osv-named entry is counted then skipped -> bucket-sum FAIL"),
    ("S07M", '    root, lane, verbose = ".", DEFAULT_LANE, False\n',
     '    root, lane, verbose = ".", DEFAULT_LANE, True\n',
     "main-default", "main() verbose by default -> main-default FAIL"),
    ("B1", '            and buckets == counts["entries"])\n', '            )\n',
     "bucket-sum", "conform_ok loses the bucket-sum conjunct -> bucket-sum FAIL"),
    ("B2", '    conform = conform_ok(counts)\n',
     '    conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n'
     '               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)\n',
     "bucket-sum", "main() ignores the bucket sum -> bucket-sum FAIL"),
]


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        src = fh.read()
    with open(OLD, encoding="utf-8") as fh:
        rows = json.load(fh)
    out = []
    for row in rows:
        row = dict(row)
        if row["id"] in REANCHOR:
            row["anchor"], row["replacement"] = REANCHOR[row["id"]]
        out.append(row)
    for rid, anchor, repl, case, expect in NEW:
        out.append({"id": rid, "anchor": anchor, "replacement": repl, "class": "assertion",
                    "kill_cases": [case], "expect": expect})
    bad = [r["id"] for r in out if src.count(r["anchor"]) != 1]
    if bad:
        print("build-table: anchors not unique/present: %s" % bad, file=sys.stderr)
        return 1
    with open(argv[2], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("build-table rows=%d neutral=%d new=%d reanchored=%d"
          % (len(out), sum(r["class"] == "neutral" for r in out), len(NEW), len(REANCHOR)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
