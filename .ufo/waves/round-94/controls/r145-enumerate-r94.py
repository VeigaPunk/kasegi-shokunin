#!/usr/bin/env python3
"""Round-94 control: re-derive the count R145 cites.

R145 (round 93) says the hand-narrow pass enumerates "the 39 [CHANGE rows] whose
base range meets the replaced docstring block" but no enumerator was committed
(the round-93 spot-check routed that as defect 6).  This control commits the
enumerator and prints both readings the spot-check named:

  parse A  a bare continuation token (`:220`) sits at its own line;
  parse B  a bare continuation token takes the range of the nearest preceding
           full-path row for the same file (the receiver's reading).

Usage: r145-enumerate-r94.py LANE BASE_REV LANDING_REV RECEIPT
Prints one line per meeting row, then the two counts.
"""
import re
import subprocess
import sys

ROW = re.compile(r"^CHANGE (\S+):(\d+) `([^`]+)` -> `([^`]+)`$")
FULL = re.compile(r"^corpus/instruments/capture-secret-scan\.py:(\d+)(?:-(\d+))?$")
BARE = re.compile(r"^:(\d+)(?:-(\d+))?$")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane] + list(args), capture_output=True, text=True, check=True).stdout


def blocks(lane, base, landing):
    """Old-side line ranges the landing replaced in the scanner docstring."""
    out = git(lane, "diff", "-U0", base, landing, "--", "corpus/instruments/capture-secret-scan.py")
    ranges = []
    for line in out.split("\n"):
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+", line)
        if m:
            lo = int(m.group(1))
            n = int(m.group(2)) if m.group(2) is not None else 1
            if n == 0:
                continue  # a pure insertion replaces no old line
            ranges.append((lo, lo + n - 1))
    return ranges


def main(argv):
    lane, base, landing, receipt = argv
    reps = blocks(lane, base, landing)
    rows = []
    last_full = {}
    for line in open(receipt, encoding="utf-8"):
        m = ROW.match(line.rstrip("\n"))
        if not m:
            continue
        rel, site_line, old, new = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        fm = FULL.match(old)
        if fm:
            lo = int(fm.group(1))
            hi = int(fm.group(2)) if fm.group(2) else lo
            last_full[rel] = (lo, hi)
            kind = "full"
        else:
            bm = BARE.match(old)
            lo = int(bm.group(1))
            hi = int(bm.group(2)) if bm.group(2) else lo
            kind = "bare"
        a = (lo, hi)
        b = last_full.get(rel, a) if kind == "bare" else a
        rows.append((rel, site_line, old, kind, a, b))
    print("replaced old-side ranges in capture-secret-scan.py: %s" % ", ".join("%d-%d" % r for r in reps))
    meet_a, meet_b = [], []
    for rel, site_line, old, kind, a, b in rows:
        if any(not (a[1] < r[0] or a[0] > r[1]) for r in reps):
            meet_a.append((rel, site_line, old, kind))
        if any(not (b[1] < r[0] or b[0] > r[1]) for r in reps):
            meet_b.append((rel, site_line, old, kind))
    for rel, site_line, old, kind in meet_b:
        print("MEET %s:%d `%s` (%s)" % (rel, site_line, old, kind))
    print("CHANGE rows total=%d" % len(rows))
    print("R145-ENUMERATE pass parse_a=%d parse_b=%d" % (len(meet_a), len(meet_b)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
