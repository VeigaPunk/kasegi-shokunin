#!/usr/bin/env python3
"""QUALITY R140 check (round 88, lesson M88-1): a repoint map whose keys passed a lexical
content proxy is frozen only after a non-author hand-labelled sample of its keys shows no WRONG key.

Usage: r140-check.py --map MAP.json --labels LABELS.tsv [--min 15]
LABELS.tsv: `key<TAB>CORRECT|WRONG|UNCLEAR` rows (# comments allowed).
Prints `R140 map_keys=N labelled=L wrong=W unclear=U min=M verdict=PASS|FAIL exit=0|1`.
FAIL when fewer than --min map keys are labelled, or any labelled map key is WRONG.
Exit 2 on a read error.
"""
import argparse
import json
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--min", type=int, default=15)
    a = ap.parse_args(argv)
    try:
        keys = set(json.load(open(a.map)))
        lab = {}
        for line in open(a.labels, encoding="utf-8"):
            if not line.strip() or line.startswith("#"):
                continue
            k, v = line.rstrip("\n").split("\t")
            if v not in ("CORRECT", "WRONG", "UNCLEAR"):
                raise ValueError(v)
            lab[k] = v
    except (OSError, ValueError) as e:
        print("R140 error reason=%s exit=2" % type(e).__name__)
        return 2
    inmap = {k: v for k, v in lab.items() if k in keys}
    wrong = sorted(k for k, v in inmap.items() if v == "WRONG")
    unclear = sum(1 for v in inmap.values() if v == "UNCLEAR")
    ok = len(inmap) >= a.min and not wrong
    for k in wrong:
        print("R140 WRONG %s" % k)
    print("R140 map_keys=%d labelled=%d wrong=%d unclear=%d min=%d verdict=%s exit=%d" % (
        len(keys), len(inmap), len(wrong), unclear, a.min, "PASS" if ok else "FAIL", 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
