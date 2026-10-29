#!/usr/bin/env python3
"""noop.py — R46bMutSelfC2a do-nothing control.

A byte-level mutation of the counter that changes NO behaviour: a trailing comment
line appended to a COPY of corpus/instruments/r46-c2-gate.py.  The battery's
apply_mutant requires an exactly-once substring match, so this control is applied
directly (the copy is still made in scratch; the lane tree is never written).

Expected: the selftest reads failures=0 (the control must NOT be graded as a
counter defect).  If the control reads failures>0, the selftest's grading is
vacuous (it flags any byte change) and every "caught" verdict in the mutant table
is worthless.

Usage: noop.py --selftest PATH --pure PATH --work DIR
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
COUNTER = os.path.join(LANE, "corpus/instruments/r46-c2-gate.py")


def run_sf(selftest_path, counter_path, pure, tree, scratch):
    cmd = [sys.executable, "-I", selftest_path, "--pure", pure]
    if counter_path:
        cmd += ["--counter", counter_path]
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = scratch
    env["TMPDIR"] = scratch
    os.makedirs(scratch, exist_ok=True)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=tree, env=env)
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-3000:], p.stderr[-2000:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", required=True)
    ap.add_argument("--pure", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()

    os.makedirs(a.work, exist_ok=True)
    mdir = tempfile.mkdtemp(prefix="c2noop-", dir=a.work)
    try:
        dst_dir = os.path.join(mdir, "corpus", "instruments")
        shutil.copytree(os.path.join(LANE, "corpus", "instruments"), dst_dir, symlinks=True)
        dst = os.path.join(dst_dir, "r46-c2-gate.py")
        before = open(COUNTER, "rb").read()
        after = before + b"\n# do-nothing control: appended comment, no behaviour change\n"
        assert after.startswith(before)
        open(dst, "wb").write(after)
        mf, out, err = run_sf(a.selftest, dst, a.pure, LANE, os.path.join(mdir, "scratch"))
        print("control=no-op-append-comment counter_bytes_before=%d counter_bytes_after=%d"
              % (len(before), len(after)))
        print("mutant=NOOP-append-comment baseline_failures=0 mutant_failures=%d verdict=%s"
              % (mf, "caught" if mf >= 1 else "UNCAUGHT"))
        # also: the pristine counter through the same path, as the pairing arm
        pf, pout, perr = run_sf(a.selftest, None, a.pure, LANE, os.path.join(mdir, "scratch2"))
        print("mutant=PRISTINE baseline_failures=0 mutant_failures=%d verdict=%s"
              % (pf, "caught" if pf >= 1 else "UNCAUGHT"))
        if mf >= 1:
            print("DO-NOTHING CONTROL FAILED: a behaviour-neutral byte change was graded as a defect")
            print(out[-2000:])
            return 1
        print("DO-NOTHING CONTROL OK: behaviour-neutral change graded failures=0 (grading is not vacuous)")
        return 0
    finally:
        shutil.rmtree(mdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
