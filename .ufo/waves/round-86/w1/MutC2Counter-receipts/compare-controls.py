#!/usr/bin/env python3
"""Compare a live control transcript with the frozen expected transcript at the
level the mutation kill criterion uses: per control, (rc, per-limb pass/FAIL).
Detail tokens (paths, counts) are printed only when the verdict matches.

Usage: compare-controls.py FROZEN_EXPECTED.txt LIVE.txt
"""
import re
import sys


def parse(path):
    blocks, name, cur, rc = [], None, [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("== control ") or line.startswith("== pricing control "):
            if name is not None:
                blocks.append((name, rc, tuple(cur)))
            name = line[3:].split(" (expected")[0].strip()
            cur, rc = [], None
            continue
        if name is None:
            continue
        m = re.match(r"^LIMB (\S+) (pass|FAIL)\b", line)
        if m:
            cur.append((m.group(1), m.group(2)))
        elif line.startswith("rc="):
            rc = int(line[3:].strip())
    if name is not None:
        blocks.append((name, rc, tuple(cur)))
    return blocks


def main(expected, live):
    e, l = parse(expected), parse(live)
    print("blocks expected=%d live=%d" % (len(e), len(l)))
    bad = 0
    for (n0, rc0, f0), (n1, rc1, f1) in zip(e, l):
        same = (n0, rc0, f0) == (n1, rc1, f1)
        if not same:
            bad += 1
        print("%-4s %-62s rc=%s/%s limbs=%s" % ("OK" if same else "DIFF", n1, rc0, rc1,
                                                "same" if f0 == f1 else "%s -> %s" % (f0, f1)))
    if len(e) != len(l):
        bad += 1
    print("verdict-mismatches=%d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
