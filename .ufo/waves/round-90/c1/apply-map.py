#!/usr/bin/env python3
"""Apply the round-90 C1 per-site map to a lane tree: on each mapped citing line,
replace the one backticked key with the backticked value. Refuses (exit 1) when a
site line does not hold the key exactly once.
Usage: apply-map.py --tree DIR --map repair-map.tsv"""
import argparse
import os
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--map", required=True)
    a = ap.parse_args(argv)
    edits = {}
    for ln in open(a.map, encoding="utf-8"):
        if ln.strip() and not ln.startswith("#"):
            site, k, v = ln.rstrip("\n").split("\t")
            f, n = site.rsplit(":", 1)
            edits.setdefault(f, []).append((int(n), k, v))
    for f, es in sorted(edits.items()):
        p = os.path.join(a.tree, f)
        lines = open(p, encoding="utf-8").read().split("\n")
        for n, k, v in es:
            tok = "`%s`" % k
            if lines[n - 1].count(tok) != 1:
                print("APPLY refuse %s:%d key=%s count=%d" % (f, n, k, lines[n - 1].count(tok)))
                return 1
            lines[n - 1] = lines[n - 1].replace(tok, "`%s`" % v)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print("APPLY %s sites=%d" % (f, len(es)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
