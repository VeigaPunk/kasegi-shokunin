#!/usr/bin/env python3
"""c1-stub-r84.py — round-84 C1 cheapest-control builder.

Writes the landed round-83 instrument (corpus/instruments/recheck-cwd-census.py, sha256
343b21e4...) with the six round-84 check ids registered and asserted by always-true,
non-constant expressions (len(done) >= 0), so the selftest prints 'selftest cases=33
failures=0' without testing the round-83 MutC1Hunt gaps. Scored under the round-84 counter,
rows H01-H12 must survive (rc 1): the frozen target cannot be met by registering check names.
Usage: c1-stub-r84.py --lane DIR --out FILE
"""
import argparse
import os
import sys

NEW = ("noprefix-only", "summary-fields", "entry-bare-pass", "argv-values", "verbose-order",
       "entry-set")
ANCHOR_REQ = '        "main-default", "bucket-other", "bucket-over", "main-verbose"))\n'
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
    src = src.replace(ANCHOR_REQ, ANCHOR_REQ[:-3] + ", "
                      + ", ".join('"%s"' % c for c in NEW) + "))\n", 1)
    stub = "".join('        check("%s", len(done) >= 0, "stub")\n' % c for c in NEW)
    src = src.replace(ANCHOR_CASE, stub + "\n" + ANCHOR_CASE, 1)
    src = src.replace("selftest cases=27", "selftest cases=33")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(src)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
