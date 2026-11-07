#!/usr/bin/env python3
"""Round-86 C1: apply the frozen map to corpus/knowledge/*.md under ROOT.

Forward replacement only: each backticked key `K` becomes `V`, line by line,
exactly as knowledge-meter.py limb M3 re-derives it.
Usage: apply-map.py --root ROOT --map MAP.json
"""
import argparse
import json
import os
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--map", required=True)
    a = ap.parse_args(argv)
    rmap = json.load(open(a.map))
    d = os.path.join(a.root, "corpus", "knowledge")
    changed = 0
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not (fn.endswith(".md") and os.path.isfile(p)):
            continue
        text = open(p, encoding="utf-8").read()
        out = []
        for line in text.split("\n"):
            for k, v in rmap.items():
                if "`%s`" % k in line:
                    line = line.replace("`%s`" % k, "`%s`" % v)
            out.append(line)
        new = "\n".join(out)
        if new != text:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1
    print("APPLY files_changed=%d keys=%d" % (changed, len(rmap)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
