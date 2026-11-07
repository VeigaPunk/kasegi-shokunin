#!/usr/bin/env python3
"""Add the four assertion-class extension controls to controls.json and build
the anchor-mismatch tree. Read-only against the lane."""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r86/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
B = "d7296645c2cd9f631329fa8e2f38328a4c9c89a5"
W = L + "/.ufo/waves/round-86/c1"
MAP = W + "/repair-map.json"
TREES = S + "/trees"
MAPS = S + "/maps"


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s\n%s\n%s" % (cmd, r.stdout, r.stderr))
    return r.stdout


def sha(p):
    import hashlib
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def apply_map(root, mapfile):
    rmap = json.load(open(mapfile))
    d = os.path.join(root, "corpus", "knowledge")
    n = 0
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not (fn.endswith(".md") and os.path.isfile(p)):
            continue
        t = open(p, encoding="utf-8").read()
        out = []
        for line in t.split("\n"):
            for k, v in rmap.items():
                if "`%s`" % k in line:
                    line = line.replace("`%s`" % k, "`%s`" % v)
            out.append(line)
        nt = "\n".join(out)
        if nt != t:
            open(p, "w", encoding="utf-8").write(nt)
            n += 1
    return n


def main():
    cfg = json.load(open(S + "/controls.json"))
    if any(c["name"] == "anchor-mismatch" for c in cfg["controls"]):
        print("already present")
        return 0
    rmap = json.load(open(MAP))
    fsha = sha(MAP)
    K = "S016.txt"
    assert K in rmap
    am = dict(rmap)
    del am[K]
    T = "S029.txt:20"
    V = "corpus/knowledge/citation-bases.md"
    assert T not in am
    am[T] = V
    am_p = MAPS + "/anchor-mismatch.json"
    with open(am_p, "w") as fh:
        json.dump(am, fh, indent=1, sort_keys=True)
    t = os.path.join(TREES, "anchor-mismatch")
    if os.path.isdir(t):
        shutil.rmtree(t)
    sh(["git", "clone", "-q", "--shared", L, t])
    sh(["git", "-C", t, "checkout", "-q", B])
    print("applied", apply_map(t, am_p))

    cfg["controls"].append(
        {"name": "anchor-mismatch", "tree": t, "map": am_p, "target": "596/1716",
         "sha": sha(am_p), "expect": "fail", "assert_result": True})
    dn = os.path.join(TREES, "dn")
    pad = os.path.join(TREES, "pad")
    wrong = os.path.join(TREES, "wrong")
    cfg["controls"] += [
        {"name": "assert-m2-donothing", "tree": dn, "map": MAP, "target": "596/1716",
         "sha": fsha, "expect": "pass", "assert_stdout": "LIMB M2 FAIL", "expect_present": True},
        {"name": "assert-m2-pad", "tree": pad, "map": MAP, "target": "596/1716",
         "sha": fsha, "expect": "pass", "assert_stdout": "LIMB M2 FAIL", "expect_present": True},
        {"name": "assert-m5-wrongfile", "tree": wrong, "map": MAPS + "/wrongfile.json",
         "target": "596/1716", "sha": sha(MAPS + "/wrongfile.json"), "expect": "pass",
         "assert_stdout": "LIMB M5 FAIL", "expect_present": True},
    ]
    with open(S + "/controls.json", "w") as fh:
        json.dump(cfg, fh, indent=1)
    print("controls=%d anchor_map_sha=%s" % (len(cfg["controls"]), sha(am_p)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
