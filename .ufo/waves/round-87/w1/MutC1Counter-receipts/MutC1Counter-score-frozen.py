#!/usr/bin/env python3
"""Score one counter build against a re-implementation of the frozen r87 C1 battery.

Usage:
  MutC1Counter-score-frozen.py COUNTER.py [SCRATCH_DIR]

Re-implements every control in .ufo/waves/round-87/controls/c1-controls-r87.sh
(same trees, same maps, same targets, same expected verdicts), builds the seven
trees itself under SCRATCH_DIR (git clone --shared of the base), then runs
COUNTER.py against each control. No lane tree is written; only SCRATCH_DIR.
The pristine counter reproduces controls/c1-controls-r87.txt limb-for-limb.
"""
import hashlib
import os
import re
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = L + "/.ufo/waves/round-87"
B = "cd1f568a6be2656b5f5dc479eb90ef99b91131b5"
T = "678/1719"
MAP = W + "/c1/repair-map.json"
APPLY = W + "/c1/apply-map.py"
S = sys.argv[2] if len(sys.argv) > 2 else "/fast/scratch/hyaku/kasegi-r87/MutC1Counter/score"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sh(*args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def build_trees():
    os.makedirs(S + "/t", exist_ok=True)
    os.makedirs(S + "/w", exist_ok=True)
    for tree in ("dn", "pos", "half", "pad", "ufo", "s041", "quoted"):
        d = S + "/t/" + tree
        if not os.path.isdir(d):
            sh("git", "clone", "-q", "--shared", L, d)
            sh("git", "-C", d, "checkout", "-q", B)
    import json
    m = json.load(open(MAP))
    half = {x: m[x] for x in sorted(m)[: len(m) // 2]}
    ufo = dict(m)
    ufo["S102.txt:101"] = ".ufo/waves/round-68/w1/ScoutS102/S102.txt:101"
    s041 = dict(m)
    s041["S041.txt:1868"] = "corpus/source-snapshots/round-26/S041.txt:1868"
    quoted = dict(m)
    quoted["S020.txt"] = "corpus/source-snapshots/round-40/S020.txt"
    for name, obj in (("half", half), ("ufo", ufo), ("s041", s041), ("quoted", quoted)):
        json.dump(obj, open("%s/%s.json" % (S, name), "w"), indent=1, sort_keys=True)
    if not os.path.exists(S + "/t/pos/corpus/knowledge/.applied"):
        sh("python3", "-B", APPLY, "--root", S + "/t/pos", "--map", MAP)
        sh("python3", "-B", APPLY, "--root", S + "/t/half", "--map", S + "/half.json")
        sh("python3", "-B", APPLY, "--root", S + "/t/ufo", "--map", S + "/ufo.json")
        sh("python3", "-B", APPLY, "--root", S + "/t/s041", "--map", S + "/s041.json")
        sh("python3", "-B", APPLY, "--root", S + "/t/quoted", "--map", S + "/quoted.json")
        sh("bash", "-c", 'cp -r "%s/t/pos/corpus/knowledge/." "%s/t/pad/corpus/knowledge/"' % (S, S))
        with open(S + "/t/pad/corpus/knowledge/claim-gates.md", "a", encoding="utf-8") as fh:
            fh.write("\n`corpus/SOURCES.md`\n`corpus/instruments/resolve.py`\n")
        open(S + "/t/pos/corpus/knowledge/.applied", "w").write("ok\n")
    return [
        ("do-nothing", "dn", MAP, sha(MAP), "fail", {"M1", "M2", "M3"}),
        ("positive", "pos", MAP, sha(MAP), "pass", set()),
        ("partial", "half", MAP, sha(MAP), "fail", {"M1", "M2", "M3"}),
        ("pad", "pad", MAP, sha(MAP), "fail", {"M1", "M2", "M3"}),
        ("ufo-copy", "ufo", S + "/ufo.json", sha(S + "/ufo.json"), "fail", {"M4", "M5"}),
        ("S041-forge", "s041", S + "/s041.json", sha(S + "/s041.json"), "fail", {"M1", "M4", "M5"}),
        ("quoted-forge", "quoted", S + "/quoted.json", sha(S + "/quoted.json"), "fail", {"M1", "M7"}),
        ("map-sha", "pos", MAP, "0" * 64, "fail", {"M6"}),
    ]


def main():
    meter = sys.argv[1]
    print("counter_sha256=%s map_sha256=%s base=%s" % (sha(meter), sha(MAP), B))
    fails, drift = [], []
    for name, tree, mapf, msha, exp, expf in build_trees():
        work = os.path.join(S, "w", name)
        os.makedirs(work, exist_ok=True)
        p = sh("python3", "-B", meter, "--lane", S + "/t/" + tree, "--base-rev", B,
               "--map", mapf, "--target", T, "--map-sha256", msha, "--work", work)
        got = "pass" if "KNOWLEDGE-METER-RESULT pass" in p.stdout else "fail"
        limbs = set(re.findall(r"^LIMB (M\d) FAIL", p.stdout, re.M))
        ok = (got == exp) and (p.returncode == (0 if exp == "pass" else 1))
        print("CTL %-13s expected=%s observed=%s rc=%d fail_limbs=%s%s" % (
            name, exp, got, p.returncode, ",".join(sorted(limbs)) or "-",
            "" if ok else "  <== DEVIATION"))
        for ln in p.stdout.strip().split("\n"):
            if ln.startswith("LIMB") or ln.startswith("KNOWLEDGE-METER"):
                print("      | " + ln)
        if not ok:
            fails.append(name)
        elif limbs != expf:
            drift.append(name)
            print("      limb-set drift: expected %s got %s" % (
                ",".join(sorted(expf)) or "-", ",".join(sorted(limbs)) or "-"))
    print("VERDICT %s failed_controls=%s" % ("killed" if fails else "SURVIVED", ",".join(fails) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
