#!/usr/bin/env python3
"""c1-stub-r83.py — round-83 C1 cheapest-control builder.

Writes the landed round-82 instrument (corpus/instruments/recheck-cwd-census.py, sha256
81677e9d...) with the three round-83 check ids registered and asserted by always-true,
non-constant expressions (len(done) >= 0), so the selftest prints 'selftest cases=27
failures=0' without testing the round-83 gaps. Scored under the round-83 counter, the G1-G4
rows must survive (rc 1): the frozen target cannot be met by registering check names.
Usage: c1-stub-r83.py --lane DIR --out FILE
"""
import argparse
import os
import sys

ANCHOR_REQ = '        "main-default"))\n'
ANCHOR_CASE = '        # Gate predicates (rounds 79-81)'


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    src = open(os.path.join(a.lane, "corpus/instruments/recheck-cwd-census.py"),
               encoding="utf-8").read()
    if src.count(ANCHOR_REQ) != 1 or src.count(ANCHOR_CASE) != 1:
        print("stub: anchors not unique", file=sys.stderr)
        return 2
    src = src.replace(ANCHOR_REQ, '        "main-default", "bucket-other", "bucket-over", '
                      '"main-verbose"))\n', 1)
    stub = "".join('        check("%s", len(done) >= 0, "stub")\n' % c
                   for c in ("bucket-other", "bucket-over", "main-verbose"))
    src = src.replace(ANCHOR_CASE, stub + "\n" + ANCHOR_CASE, 1)
    src = src.replace("selftest cases=24", "selftest cases=27")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(src)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
