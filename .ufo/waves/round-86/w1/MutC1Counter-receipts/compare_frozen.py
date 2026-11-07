#!/usr/bin/env python3
"""Compare my harness's pristine stdout for the 7 frozen controls with the
frozen receipt c1-controls-r86.txt (KNOWLEDGE-METER/LIMB/RESULT lines only)."""
import json
import os
import sys

S = "/fast/scratch/hyaku/kasegi-r86/MutC1Counter"
FROZEN = ("/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/controls/c1-controls-r86.txt")
NAMES = ["do-nothing", "positive", "partial", "de-cite", "pad", "wrong-file", "map-sha"]
MINE = {"de-cite": "decite"}


def main():
    res = json.load(open(S + "/results.json"))
    lines = open(FROZEN, encoding="utf-8").read().splitlines()
    blocks, cur = {}, None
    for line in lines:
        if line.startswith("== control "):
            cur = line.split(":")[0][len("== control "):].strip()
            blocks[cur] = []
        elif cur and (line.startswith("KNOWLEDGE-METER") or line.startswith("LIMB ")):
            blocks[cur].append(line)
    bad = 0
    for n in NAMES:
        mine = [l for l in res[n]["pristine"]["stdout"].splitlines()
                if l.startswith("KNOWLEDGE-METER") or l.startswith("LIMB ")]
        ok = mine == blocks[n]
        print("%-12s exact=%s lines=%d" % (n, ok, len(mine)))
        if not ok:
            bad += 1
            for a, b in zip(mine, blocks[n]):
                if a != b:
                    print("  MINE  %s\n  FROZEN %s" % (a, b))
            print("  len mine=%d frozen=%d" % (len(mine), len(blocks[n])))
    print("frozen_exact=%d/%d" % (len(NAMES) - bad, len(NAMES)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
