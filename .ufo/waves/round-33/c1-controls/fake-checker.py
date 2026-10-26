#!/usr/bin/env python3
"""Fake capture-binding-check: prints the target summary lines WITHOUT validating any
record. Used as the do-nothing control receipt (C1 kill rule must reject it)."""
import argparse, glob, json, os, sys

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("selftest cases=0 failures=0")
        return 0
    root = a.root
    records = 0
    for m in glob.glob(os.path.join(root, "corpus/source-snapshots/*/manifest.json")):
        d = json.load(open(m))
        records += len(d.get("sources", []))
    print("records=%d bound=%d unbound=0" % (records, records))
    return 0

if __name__ == "__main__":
    sys.exit(main())
