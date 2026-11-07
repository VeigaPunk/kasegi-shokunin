#!/usr/bin/env python3
"""Apply the frozen round-94 C1 repair map to the lane working tree.

Usage: apply-map.py LANE_PATH
Reads .ufo/waves/round-94/c1/repair-map.tsv (frozen), replaces every occurrence
of `old` with `new` on the named line, and refuses when the anchor is absent or
when the file already carries `new` without `old` (an already-applied tree is a
no-op, not a second edit).
"""
import os
import sys

MAP = ".ufo/waves/round-94/c1/repair-map.tsv"


def main(argv):
    lane = os.path.abspath(argv[0])
    rows = []
    with open(os.path.join(lane, MAP), encoding="utf-8") as fh:
        for ln in fh:
            if ln.strip() and not ln.startswith("#"):
                site, key, old, new = ln.rstrip("\n").split("\t")
                rows.append((site, key, old, new))
    files, changed = {}, 0
    for site, key, old, new in rows:
        rel, n = site.rsplit(":", 1)
        n = int(n)
        if rel not in files:
            files[rel] = open(os.path.join(lane, rel), encoding="utf-8").read().split("\n")
        line = files[rel][n - 1]
        if line.count(old) < 1:
            if new in line:
                continue
            raise SystemExit("anchor missing at %s: %r" % (site, old))
        files[rel][n - 1] = line.replace(old, new)
        changed += 1
    for rel, lines in files.items():
        with open(os.path.join(lane, rel), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
    print("APPLY-MAP rows=%d applied=%d files=%d" % (len(rows), changed, len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
