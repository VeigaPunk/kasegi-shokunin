#!/usr/bin/env python3
"""Cross-check: run the wave-1 selftest (r46-selftest-f29.py) against MY independent mutant
set, using the battery's own caught-or-not predicate (selftest reports failures>0 under the
mutant while the unmutated counter reads failures=0).

This measures whether the wave-1 selftest would reach uncaught=0 for a frozen mutant table
built from my recipes (the L1's job to land the battery extension).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SELFTEST = os.path.join(LANE, ".ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py")
GATE = os.path.join(LANE, "corpus/instruments/r46-f29-gate.py")
RECHECK = os.path.join(LANE, "corpus/instruments/source-recheck.py")

import mutants as W1
import round2 as W2
import round3 as W3
import round4 as W4

RECIPES = {}
for mod in (W1, W2, W3, W4):
    for m in mod.MUTANTS:
        RECIPES[m[0]] = (m[1], m[2], m[3])


def run_selftest(counter: str, work: str) -> tuple[int, str]:
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    p = subprocess.run([sys.executable, SELFTEST, "--counter", counter, "--work", work],
                       capture_output=True, text=True, env=env, timeout=900)
    m = re.search(r"selftest cases=(\d+) failures=(\d+)", p.stdout)
    return (int(m.group(2)) if m else -1), (p.stdout[-600:] + p.stderr[-400:])


def main():
    base_dir = os.path.join(S, "mutants", "BASE")
    base_fail, _ = run_selftest(os.path.join(base_dir, "r46-f29-gate.py"), os.path.join(S, "st-work-base"))
    print("baseline selftest failures = %d" % base_fail)
    if base_fail != 0:
        print("BASELINE NOT CLEAN -> inconclusive")
    caught, uncaught = [], []
    for mid, (limb, old, new) in RECIPES.items():
        d = os.path.join(S, "mutants", mid)
        g = os.path.join(d, "r46-f29-gate.py")
        if not os.path.exists(g):
            os.makedirs(d, exist_ok=True)
            text = open(GATE, encoding="utf-8").read()
            assert text.count(old) == 1, (mid, text.count(old))
            open(g, "w", encoding="utf-8").write(text.replace(old, new, 1))
            shutil.copy(RECHECK, os.path.join(d, "source-recheck.py"))
        f, tail = run_selftest(g, os.path.join(S, "st-work-" + mid))
        if f > base_fail:
            caught.append(mid)
            print("mutant=%-34s selftest_failures=%d  CAUGHT" % (mid, f))
        else:
            uncaught.append(mid)
            print("mutant=%-34s selftest_failures=%d  UNCAUGHT  (tail: %s)"
                  % (mid, f, tail.strip().splitlines()[-1][:90] if tail.strip() else ""))
    print()
    print("mutants=%d caught=%d uncaught=%d baseline_failures=%d" % (len(RECIPES), len(caught), len(uncaught), base_fail))
    print("UNCAUGHT ids: %s" % ",".join(uncaught))
    return 0


if __name__ == "__main__":
    sys.exit(main())
