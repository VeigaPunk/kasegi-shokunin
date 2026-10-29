#!/usr/bin/env python3
"""drv.py — R46bMutSelfC2a probe driver.

Reuses the FROZEN battery's own mutant table and apply/parse logic (imported from
corpus/instruments/r46-mutbat.py, read-only) so the mutant set cannot drift, but runs
the 21 C2 mutants in parallel (the frozen runner is serial).

  drv.py --selftest PATH --pure PATH --work DIR --jobs N [--out FILE]

prints one line per mutant:  mutant=<id> baseline_failures=<b> mutant_failures=<m>
and a summary line.  READ-ONLY on the lane tree; all writes under --work and under
$HYAKU_SCRATCH.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MUTBAT = os.path.join(LANE, "corpus/instruments/r46-mutbat.py")


def load_mutbat():
    spec = importlib.util.spec_from_file_location("r46_mutbat_frozen", MUTBAT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MB = load_mutbat()


def run_sf(selftest_path: str, counter_path: str | None, pure: str, tree: str,
           scratch: str | None = None) -> tuple[int, str]:
    cmd = [sys.executable, "-I", selftest_path, "--pure", pure]
    if counter_path:
        cmd += ["--counter", counter_path]
    env = dict(os.environ)
    if scratch:  # the selftest hardcodes its seat dir under HYAKU_SCRATCH: give each run its own
        os.makedirs(scratch, exist_ok=True)
        env["HYAKU_SCRATCH"] = scratch
        env["TMPDIR"] = scratch
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=tree, env=env)
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-3000:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", required=True)
    ap.add_argument("--pure", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    tree = LANE
    base, base_tail = run_sf(a.selftest, None, a.pure, tree,
                             scratch=os.path.join(a.work, "scratch-base"))
    print("BASELINE selftest=%s baseline_failures=%d" % (a.selftest, base), flush=True)
    if base != 0:
        print(base_tail)
        print("BASELINE-DIRTY")
        return 2

    cname, mutants, _st = MB.COUNTER["c2"]
    src_counter = os.path.join(tree, "corpus/instruments", cname)

    def one(triple):
        mid, old, new = triple
        mdir = tempfile.mkdtemp(prefix="c2m-%s-" % mid.split("-")[0], dir=a.work)
        try:
            dst = MB.apply_mutant(src_counter, triple, mdir, tree)
            mf, tail = run_sf(a.selftest, dst, a.pure, tree,
                             scratch=os.path.join(mdir, "scratch"))
            return mid, mf, tail
        finally:
            shutil.rmtree(mdir, ignore_errors=True)

    results = []
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for mid, mf, tail in ex.map(one, mutants):
            results.append((mid, mf, tail))
            print("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" %
                  (mid, mf, "caught" if mf >= 1 else "UNCAUGHT"), flush=True)

    caught = sum(1 for _m, mf, _t in results if mf >= 1)
    surv = [m for m, mf, _t in results if mf == 0]
    print("mutbat counter=c2 mutants=%d caught=%d equivalent=0 uncaught=%d baseline_failures=0" %
          (len(results), caught, len(surv)))
    print("SURVIVORS failures=0: " + " ".join(surv))
    if a.out:
        with open(a.out, "w") as fh:
            fh.write("selftest=%s pure=%s\n" % (a.selftest, a.pure))
            fh.write("BASELINE baseline_failures=%d\n" % base)
            for mid, mf, _t in results:
                fh.write("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s\n" %
                         (mid, mf, "caught" if mf >= 1 else "UNCAUGHT"))
            fh.write("SURVIVORS failures=0: " + " ".join(surv) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
