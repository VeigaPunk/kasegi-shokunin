#!/usr/bin/env python3
"""Round-86 R137 check: a planned citation-repair tranche must hold at least one
citation-for-citation candidate.

A candidate qualifies when its key (the cited token) and its proposed value are
both single path tokens: no whitespace, and the value is a tracked lane path
(optionally with a :N / :N-M anchor) that ends with the key's bare name. A
command-invocation string (`bash x.sh --selftest`) is not a citation a repoint
can fix: rewriting it changes a command, not a reference.

Input: a JSON object mapping key -> value, or the round-85 ExecC1Hunt candidate
file shape ({"skill_candidates": [{"token", "proposed"}, ...]}).
Usage: repair-class-check.py --lane LANE FILE
Prints `REPAIR-CLASS candidates=N qualifying=Q verdict=PASS|FAIL exit=0|1`.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ANCHOR = re.compile(r":\d+(?:-\d+)?$")


def pairs(obj):
    if isinstance(obj, dict) and "skill_candidates" in obj:
        return [(c.get("token", ""), c.get("proposed", "")) for c in obj["skill_candidates"]]
    if isinstance(obj, dict):
        return list(obj.items())
    raise ValueError("unsupported shape")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("file")
    a = ap.parse_args(argv)
    try:
        cands = pairs(json.load(open(a.file)))
        tracked = set(subprocess.run(["git", "-C", a.lane, "ls-files"], capture_output=True,
                                     text=True, check=True).stdout.split("\n"))
    except Exception as e:
        print("REPAIR-CLASS error=%s verdict=FAIL exit=2" % type(e).__name__)
        return 2
    q = 0
    for k, v in cands:
        if re.search(r"\s", k) or re.search(r"\s", v):
            continue
        bare = ANCHOR.sub("", k)
        path = ANCHOR.sub("", v)
        if path in tracked and path.endswith("/" + os.path.basename(bare)):
            q += 1
    ok = q > 0
    print("REPAIR-CLASS candidates=%d qualifying=%d verdict=%s exit=%d" % (len(cands), q, "PASS" if ok else "FAIL", 0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
