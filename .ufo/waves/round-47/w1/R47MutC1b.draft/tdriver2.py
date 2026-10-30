#!/usr/bin/env python3
"""T-L7d: the LESSON46 acceptance branch of l7, never pinned by the suite."""
import os, re, shutil, subprocess, sys
S = "/fast/scratch/hyaku/kasegi-r47/R47MutC1b"
GREEN = S + "/work/green-keep/c1-green"
BASE = S + "/exports/base"
INSTR = S + "/exports/freeze/corpus/instruments"
COUNTER = INSTR + "/r47-routed-defects.py"
LOGS = S + "/logs"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")

def counter_on(cp, tree, tag):
    p = subprocess.run([sys.executable, "-I", cp, "--root", tree, "--baseline", BASE],
                       capture_output=True, text=True, timeout=600, cwd=S)
    open(LOGS + "/" + tag + ".txt", "w").write(p.stdout + p.stderr)
    return p.stdout

src = open(COUNTER, encoding="utf-8").read()
old, new = "for rel in (LESSON47, LESSON46):", "for rel in (LESSON47,):"
assert src.count(old) == 1
inst = S + "/work/tinst-L7d"
shutil.rmtree(inst, ignore_errors=True)
shutil.copytree(INSTR, inst, symlinks=True, ignore=IGNORE)
mut = inst + "/r47-routed-defects.py"
open(mut, "w", encoding="utf-8").write(src.replace(old, new, 1))

t = S + "/work/tree-T-L7d-lesson47-redacted"
shutil.rmtree(t, ignore_errors=True)
shutil.copytree(GREEN, t, symlinks=True)
p = os.path.join(t, "corpus/lessons/round-47.md")
s = open(p, encoding="utf-8").read()
assert "R46bW2RevEntryClaims" in s and "R46bConnPatterns" in s
s = s.replace("R46bW2RevEntryClaims", "REDACTED-A").replace("R46bConnPatterns", "REDACTED-B")
open(p, "w", encoding="utf-8").write(s)

for tag, cp in (("t-T-L7d-pristine", COUNTER), ("t-T-L7d-mutant", mut)):
    txt = counter_on(cp, t, tag)
    keep = [ln for ln in txt.splitlines() if ln.startswith("limb L7 ") or ln.startswith("routed-defects")]
    print("== %s ==" % tag)
    print("\n".join(keep))
