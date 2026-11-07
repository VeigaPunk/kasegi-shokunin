#!/usr/bin/env python3
"""Round-91 integration check (M91-3): every block quote `> "TEXT" — `PATH:N[-M]`` in the
named entries must occur verbatim (whitespace-normalised) in lines N..M of PATH at --rev
(git show; working tree when --rev is omitted), and every backticked `PATH:N[-M]` citation
must lie inside PATH. Prints one BAD line per failure, then QUOTE-ANCHOR checked=<q>
bad=<b> cites=<c> out_of_range=<r>. Exit 1 on any failure.
Usage: quote-anchor-check.py --lane L [--rev REV] ENTRY...
"""
import argparse
import os
import re
import subprocess
import sys

QUOTE = re.compile(r'^> "(.+)" — `([^`:]+):(\d+)(?:-(\d+))?`')
CITE = re.compile(r"`((?:corpus|\.ufo)/[A-Za-z0-9_./-]+|SCORECARD\.md|SKILL\.md):(\d+)(?:-(\d+))?`")


def norm(s):
    return " ".join(s.replace("\\`", "`").split())


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev")
    ap.add_argument("entries", nargs="+")
    a = ap.parse_args(argv)
    cache = {}

    def lines(p):
        if p not in cache:
            try:
                if a.rev:
                    t = subprocess.run(["git", "-C", a.lane, "show", "%s:%s" % (a.rev, p)],
                                       capture_output=True, text=True, check=True).stdout
                else:
                    t = open(os.path.join(a.lane, p), encoding="utf-8").read()
                cache[p] = t.split("\n")
            except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
                cache[p] = None
        return cache[p]

    q = bad = c = oor = 0
    for e in a.entries:
        for i, ln in enumerate(lines(e) or [], 1):
            m = QUOTE.match(ln)
            if m:
                q += 1
                src = lines(m.group(2))
                lo, hi = int(m.group(3)), int(m.group(4) or m.group(3))
                if src is None or not norm(m.group(1)) in norm(" ".join(src[lo - 1:hi])):
                    bad += 1
                    print("BAD quote %s:%d -> %s:%d-%d" % (e, i, m.group(2), lo, hi))
            for m in CITE.finditer(ln):
                c += 1
                src = lines(m.group(1))
                lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
                if src is None or not (1 <= lo <= hi <= len(src)):
                    oor += 1
                    print("BAD cite %s:%d -> %s:%d-%d" % (e, i, m.group(1), lo, hi))
    print("QUOTE-ANCHOR checked=%d bad=%d cites=%d out_of_range=%d" % (q, bad, c, oor))
    return 1 if bad or oor else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
