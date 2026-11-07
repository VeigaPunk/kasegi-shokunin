#!/usr/bin/env python3
"""C6/C7 fixture-lane controls for the M4 INTERNAL / base-GONE sub-rules.

A scratch clone of the lane (git clone --shared, .git present) is used so the
control can perturb the worktree WITHOUT writing into the real lane:

  C6 map-value-missing-worktree : remove one tracked map target from the clone
     worktree.  git ls-files still lists it (v in tracked), the path still ends
     with '/'+key, it is outside .ufo/, but classify() now says GONE -> the
     frozen counter must fail M4 (INTERNAL).  Kills a mutant that drops the
     INTERNAL check.
  C7 base-key-resolving : add a lane-root file at a repaired key's bare name
     (resolve.py).  The base citation now classifies INTERNAL, so the frozen
     counter must fail M4 (base GONE).  Kills a mutant that drops the
     base-GONE check.
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kasegi-r85/MutC1Counter")
import driver  # noqa: E402

L = driver.L
S = driver.S
IN = driver.IN
ORIG = driver.ORIG
MAP = driver.MAP
MAP_SHA = driver.MAP_SHA
BASE = os.path.join(IN, "base.md")
POSITIVE = os.path.join(IN, "positive.md")
CL = os.path.join(S, "clone", "lane")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=driver.ENV, **kw)


def sha(p):
    return driver.sha(p)


def build_clone():
    if os.path.isdir(CL):
        shutil.rmtree(CL)
    os.makedirs(os.path.dirname(CL), exist_ok=True)
    p = sh(["git", "clone", "--shared", "--quiet", L, CL])
    assert p.returncode == 0, p.stderr
    top = sh(["git", "-C", CL, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert top == CL, "toplevel %r != %r" % (top, CL)
    assert os.path.isdir(os.path.join(CL, ".git")), "clone has no .git"
    assert sha(os.path.join(CL, "corpus/instruments/resolve.py")) == \
        sha(os.path.join(L, "corpus/instruments/resolve.py"))
    print("CLONE ok toplevel=%s tracked=%d" % (top, len(
        sh(["git", "-C", CL, "ls-files"]).stdout.split("\n"))))


def all_mutants():
    return [(mid, os.path.join(S, "mutants", mid + ".py"))
            for mid, *_ in driver.MUTANTS]


def run_set(label, lane):
    target = driver.measure(ORIG, POSITIVE, lane)
    print("%s target(measured on fixture lane)=%s" % (label, target))
    out = {}
    r = driver.run_counter(ORIG, BASE, POSITIVE, MAP, target, MAP_SHA, lane)
    r["expected"] = "fail"
    out["pristine"] = r
    print("%s pristine rc=%d %s" % (label, r["rc"], r["result"]))
    for ln in r["stdout"].strip().split("\n"):
        print("   " + ln)
    for mid, ctr in all_mutants():
        r = driver.run_counter(ctr, BASE, POSITIVE, MAP, target, MAP_SHA, lane)
        r["expected"] = "fail"
        out[mid] = r
        if r["rc"] == 0:
            print("%s %-24s rc=0 KILLED by new control" % (label, mid))
    return target, out


def main():
    build_clone()
    results = {}
    victim = os.path.join(CL, "corpus/source-snapshots/round-46/S073.txt")
    assert os.path.isfile(victim)
    before = sha(victim)
    os.remove(victim)
    try:
        t6, r6 = run_set("C6-map-value-missing-worktree", CL)
    finally:
        shutil.copy2(os.path.join(L, "corpus/source-snapshots/round-46/S073.txt"), victim)
        assert sha(victim) == before, "victim restore mismatch"
        assert os.path.isfile(victim)
    results["C6-map-value-missing-worktree"] = {"target": t6, "runs": r6}
    probe = os.path.join(CL, "resolve.py")
    assert not os.path.exists(probe)
    with open(probe, "wb"):
        pass
    try:
        t7, r7 = run_set("C7-base-key-resolving", CL)
    finally:
        os.remove(probe)
    results["C7-base-key-resolving"] = {"target": t7, "runs": r7}
    with open(os.path.join(S, "clone_matrix.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("CLONE CONTROLS OK")


if __name__ == "__main__":
    main()
