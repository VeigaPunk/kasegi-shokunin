#!/usr/bin/env python3
"""r44-frontier-count.py — the round-44 coverage counter (C2), table-aware.

WHY THIS INSTRUMENT EXISTS
    The frozen C2 counter recorded in `.ufo/waves/round-44/claims.json` is

        grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md

    The frontier table's shape is `| F<NN> | <title> | <status> | <knowledge> |
    <sources> | <note> |` — the status is the THIRD cell, not the second.  The
    frozen regex therefore prints `0` at the frozen base AND `0` after the
    round-44 admission: it measures nothing and cannot separate the two
    states (`.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt`).  A
    counter that reads 0 in both worlds is a defective instrument, not a
    measurement, so this counter measures the SAME declared predicate — the
    number of frontier rows whose status cell is exactly `admitted` — and the
    SAME target value (26).

    The target is not moved by this instrument: at the frozen base the same
    count is 25, one short of 26, so a do-nothing control cannot reach the
    target.  The frozen counter string stays recorded, unchanged, in the
    claims file and in the report.

USAGE
    python3 corpus/instruments/r44-frontier-count.py --root TREE [--expect N]

    --root    tree to count (an exported lane tree, or the lane checkout)
    --expect  when given, the counted value must equal it, else exit 1

OUTPUT
    frontier rows=<n> admitted=<k> exit=0|1
"""

from __future__ import annotations

import argparse
import os
import re
import sys

ROW_RX = re.compile(r"^\| F\d+ \|")


def count_frontier(root: str) -> tuple[int, int, list[str]]:
    readme = os.path.join(root, "corpus", "README.md")
    rows = 0
    admitted = 0
    ids: list[str] = []
    try:
        with open(readme, "r", encoding="utf-8") as fh:
            for line in fh:
                if not ROW_RX.match(line):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 3:
                    continue
                rows += 1
                ids.append(cells[0])
                if cells[2] == "admitted":
                    admitted += 1
    except OSError as exc:
        print(f"r44-frontier-count: cannot read {readme}: {exc}", file=sys.stderr)
        return 0, 0, []
    return rows, admitted, ids


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--expect", type=int, default=None)
    ap.add_argument("--ids", action="store_true", help="also print the counted row ids")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"r44-frontier-count: root {args.root} is not a directory", file=sys.stderr)
        return 2

    rows, admitted, ids = count_frontier(args.root)
    if args.ids:
        print("frontier-ids=" + ",".join(ids))
    # R44W2Rev10 false-pass shape: a duplicated frontier row would inflate the
    # admitted count without adding a distinct holding. Duplicate ids are a
    # defect, never a pass.
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        print(f"frontier duplicate-ids={','.join(dupes)} verdict=DEFECT exit=1")
        return 1
    print(f"frontier rows={rows} admitted={admitted}")
    if args.expect is not None and admitted != args.expect:
        print(f"frontier expected={args.expect} admitted={admitted} verdict=SHORT exit=1")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
