#!/usr/bin/env python3
"""Run one pipeline natively (no audit) and print each stage's returncode.

Usage: native.py --stage 'git show HEAD:big.txt' --stage 'head -n 1'
Mirrors figure-audit.run_derive's Popen wiring so the printed rc are the
statuses the gate would classify.
"""
import argparse
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "work", "root")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", action="append", required=True)
    a = ap.parse_args()
    procs, prev = [], None
    for s in a.stage:
        p = subprocess.Popen(shlex.split(s), cwd=ROOT, stdin=prev,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        procs.append(p)
        if prev is not None:
            prev.close()
        prev = p.stdout
    raw, _ = procs[-1].communicate()
    for p in procs[:-1]:
        p.wait()
    print("NATIVE bytes=%d stdout=%r" % (len(raw), raw[:60]))
    for i, p in enumerate(procs):
        print("NATIVE stage=%d cmd=%r rc=%d" % (i, a.stage[i], p.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
