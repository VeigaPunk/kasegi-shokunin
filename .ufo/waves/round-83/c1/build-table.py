#!/usr/bin/env python3
"""build-table.py — round-83 C1 mutant table for the frozen candidate.

Carries the 63 frozen round-82 rows (.ufo/waves/round-82/c1/mutant-table.json) unchanged in
id, class, anchor, replacement and kill_cases. Four rows are new, one per round-82 MutC1Hunt
real gap (.ufo/waves/round-82/w1/MutC1Hunt.md rows H04, H05, H10, H19), each declared with
the round-83 check meant to kill it, before any run:

  G1  H04: the bucket sum reads norecheck where it read exit_other     -> bucket-other
  G2  H05: conform_ok's bucket equality becomes >=                       -> bucket-over
  G3  H10: the --verbose parser branch sets verbose = False              -> main-verbose
  G4  H19 + S07M: the main-default negative limb becomes the tautology
      len(out22) > 0 AND main()'s verbose default flips to True (the
      MutC1Hunt decisive witness; two sites, the second in "extra")      -> main-verbose

Every anchor (and every "extra" anchor) must occur exactly once in the candidate (checked
here, exit 1 if not).
Usage: python3 build-table.py <candidate.py> <out.json>
"""
import json
import sys

OLD = ".ufo/waves/round-82/c1/mutant-table.json"
NEW = [
    ("G1", '               + counts["exit_other"] + counts["norecheck"] + counts["restoration_only"])\n',
     '               + counts["norecheck"] + counts["norecheck"] + counts["restoration_only"])\n',
     None, "bucket-other", "exit_other dropped from the bucket sum -> bucket-other FAIL"),
    ("G2", '            and buckets == counts["entries"])\n',
     '            and buckets >= counts["entries"])\n',
     None, "bucket-over", "over-accounted buckets accepted -> bucket-over FAIL"),
    ("G3", '        elif argv[i] == "--verbose":\n            verbose = True\n',
     '        elif argv[i] == "--verbose":\n            verbose = False\n',
     None, "main-verbose", "--verbose ignored -> main-verbose FAIL"),
    ("G4", '              "ENTRY a-prefixed.md" not in out22\n',
     '              len(out22) > 0\n',
     [['    root, lane, verbose = ".", DEFAULT_LANE, False\n',
       '    root, lane, verbose = ".", DEFAULT_LANE, True\n']],
     "main-verbose", "tautological main-default limb plus verbose default -> main-verbose FAIL"),
]


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as fh:
        src = fh.read()
    with open(OLD, encoding="utf-8") as fh:
        out = [dict(r) for r in json.load(fh)]
    for rid, anchor, repl, extra, case, expect in NEW:
        row = {"id": rid, "anchor": anchor, "replacement": repl, "class": "assertion",
               "kill_cases": [case], "expect": expect}
        if extra:
            row["extra"] = extra
        out.append(row)
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
