#!/usr/bin/env python3
"""Rebuild the R50 receipt's defect-tree x mutant pairing for r46-f29-gate.py.

For each receipt row: run the PRISTINE gate and the MUTATED gate on the same defect
tree, read the paired limb's pass bit from each run, and compare with the receipt's
base/mutant limb columns.  A FLIP must read base=0 (pristine red on the defect tree)
and mutant=1 (mutant green => the defect tree kills the mutant)."""
import json, os, re, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
GATE = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
RECHECK = os.path.join(LANE, "corpus/instruments/source-recheck.py")
TREES = os.path.join(S, "trees")
INST = os.path.join(S, "inst")

# receipt rows: (pair#, defect-tree, mutant-id, limb, receipt base, receipt mutant, receipt verdict)
RECEIPT = [
 (1,"duprow","H1a-counts-loose","H1",0,0,"NOT-SHOWN (a)"),
 (2,"fencedf29","H1b-raw-loose","H1",0,0,"NOT-SHOWN (a)"),
 (3,"src0740","H1c-src-boundary","H1",0,1,"FLIP"),
 (4,"vjunk","H2a-verified-loose","H2",0,1,"FLIP"),
 (5,"thinsection","H2b-wordfloor-low","H2",1,1,"NOT-SHOWN (b)"),
 (6,"badnames","H2c-need-empty","H2",0,1,"FLIP"),
 (7,"row9cells","H3a-cells-loose","H3",0,0,"NOT-SHOWN (c)"),
 (8,"thinscope","H3b-scope-low","H3",0,1,"FLIP"),
 (9,"kindcase","H3c-kind-dead","H3",0,1,"FLIP"),
 (10,"manws","H4a-manifest-unpinned","H4",0,1,"FLIP"),
 (11,"fewquotes","H4b-quotes-low","H4",0,0,"NOT-SHOWN (d)"),
 (12,"dupquote","H4c-distinct-dropped","H4",0,0,"NOT-SHOWN (d)"),
 (13,"widespan","H5a-span-wide","H5",0,1,"FLIP"),
 (14,"longquote","H5b-words-wide","H5",0,1,"FLIP"),
 (15,"fewspans","H5c-pass-low","H5",0,0,"NOT-SHOWN (e)"),
 (16,"nestedmd","H6a-counts-loose","H6",0,1,"FLIP"),
 (17,"entrymutant","H6b-pin-dropped","H6",0,1,"FLIP"),
 (18,"symlink","H7b-symlink-dead","H7",0,1,"FLIP"),
 (19,"row9cells","H7a-verdict-or","H7",0,0,"NOT-SHOWN (f)"),
 (20,"positive","H7c-okline-loose","H7",1,1,"NOT-SHOWN (f)"),
]

def run(gate, tree):
    env = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))
    p = subprocess.run([sys.executable, "-B", gate, "--root", tree],
                       capture_output=True, text=True, env=env, timeout=300)
    limbs = {}
    for m in re.finditer(r"^gate (H\d) pass=(\d) read=(.*)$", p.stdout, re.M):
        limbs[m.group(1)] = (int(m.group(2)), m.group(3))
    return limbs, p.stdout, p.returncode

def mutant_gate(mid, old, new):
    d = os.path.join(INST, mid, "corpus", "instruments")
    if os.path.isdir(os.path.join(INST, mid)):
        shutil.rmtree(os.path.join(INST, mid))
    os.makedirs(d, exist_ok=True)
    text = open(GATE, encoding="utf-8").read()
    assert text.count(old) == 1, mid
    open(os.path.join(d, "r46-f29-gate.py"), "w", encoding="utf-8").write(text.replace(old, new, 1))
    shutil.copy(RECHECK, os.path.join(d, "source-recheck.py"))
    return os.path.join(d, "r46-f29-gate.py")

def main():
    muts = json.load(open(os.path.join(S, "mutants.json")))
    out = []
    for pair, defect, mid, limb, rbase, rmut, rverd in RECEIPT:
        tree = os.path.join(TREES, defect)
        assert os.path.isdir(tree), tree
        old, new = muts[mid]
        mg = mutant_gate(mid, old, new)
        bl, bout, brc = run(GATE, tree)
        ml, mout, mrc = run(mg, tree)
        b = bl.get(limb, (-1, "missing"))[0]
        m = ml.get(limb, (-1, "missing"))[0]
        verdict = "FLIP" if (b, m) != (rbase, rmut) else "match"
        flip_seen = "FLIP" if (b == 0 and m == 1) else "no-flip"
        out.append(dict(pair=pair, defect=defect, mutant=mid, limb=limb,
                        receipt_base=rbase, receipt_mutant=rmut, receipt_verdict=rverd,
                        my_base=b, my_mutant=m, my_verdict=flip_seen,
                        agree=verdict,
                        base_read=bl.get(limb, ("", ""))[1],
                        mutant_read=ml.get(limb, ("", ""))[1],
                        base_fixed=re.findall(r"f29-gate fixed=(\d+)/7", bout),
                        mutant_fixed=re.findall(r"f29-gate fixed=(\d+)/7", mout)))
        print("pair=%2d defect=%-12s mutant=%-22s limb=%s receipt=(%d,%d,%s) mine=(%d,%d) %s"
              % (pair, defect, mid, limb, rbase, rmut, rverd, b, m, verdict))
        print("        base   read=%s" % bl.get(limb, ("", "missing"))[1])
        print("        mutant read=%s" % ml.get(limb, ("", "missing"))[1])
    json.dump(out, open(os.path.join(S, "out", "pairing.json"), "w"), indent=1)
    agree = sum(1 for r in out if r["agree"] == "match")
    flips = sum(1 for r in out if r["my_verdict"] == "FLIP")
    print("SUMMARY rows=%d receipt-match=%d my-flips=%d" % (len(out), agree, flips))

main()
