#!/usr/bin/env python3
"""Verify: (a) c1/c2 tables byte-identical to v1, (b) f29 triples unique + receipt-faithful."""
import importlib.util, os, re, subprocess, sys, shutil

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
DRAFT = LANE + "/.ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/r46-mutbat.py"
V1 = LANE + "/corpus/instruments/r46-mutbat.py"

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

v1 = load(V1, "v1")
v11 = load(DRAFT, "v11")

print("== (a) c1/c2 tables byte-identical to v1 ==")
for which in ("c1", "c2"):
    a = v1.COUNTER[which][1]
    b = v11.COUNTER[which][1]
    same = a == b
    print("  %s identical=%s (%d mutants)" % (which, same, len(b)))
    if not same:
        for x, y in zip(a, b):
            if x != y:
                print("    DIFF", x, "!=", y)
print("  COUNTER selftest names c1/c2 unchanged:",
      v1.COUNTER["c1"][2] == v11.COUNTER["c1"][2] and v1.COUNTER["c2"][2] == v11.COUNTER["c2"][2])
print("  c1/c2 run_selftest body identical:",
      v1.run_selftest.__code__.co_code == v11.run_selftest.__code__.co_code)
print("  c1/c2 apply_mutant body identical:",
      v1.apply_mutant.__code__.co_code == v11.apply_mutant.__code__.co_code)

print("== (b) f29 triple uniqueness against r46-f29-gate.py ==")
src = open(LANE + "/corpus/instruments/r46-f29-gate.py", encoding="utf-8").read()
bad = 0
for mid, old, new in v11.F29_MUTANTS:
    n = src.count(old)
    if n != 1:
        bad += 1
        print("  %-22s count=%d  <<< NOT EXACTLY ONCE" % (mid, n))
print("  all-unique: %s (%d mutants)" % (bad == 0, len(v11.F29_MUTANTS)))

print("== (c) syntax check ==")
p = subprocess.run([sys.executable, "-m", "py_compile", DRAFT], capture_output=True, text=True)
print("  py_compile rc=%d %s" % (p.returncode, p.stderr[-300:]))

print("== (d) --list prints all three ==")
p = subprocess.run([sys.executable, DRAFT, "--root", LANE, "--pure", "/fast/scratch/hyaku/kasegi-r46/L1/pure2",
                    "--work", "/fast/scratch/hyaku/kasegi-r46/R46bExecMutbatF29/w", "--list"],
                   capture_output=True, text=True)
lines = p.stdout.strip().splitlines()
from collections import Counter
print("  rc=%d lines=%d prefixes=%s" % (p.returncode, len(lines), dict(Counter(l.split()[0] for l in lines))))
