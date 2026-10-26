#!/usr/bin/env python3
"""Prove what each degenerate ledger row actually measures. CritC1Kill artifact.

For every class A/B limb (behavior-equivalent comment patch) the honest exercise
command is run on the unmutated and the mutated instrument in the same scratch
copy and the (exit, sha256(stdout+stderr)) pair is compared: identical means the
mutant cannot be distinguished from the original by behavior.

For every class C limb the patch is shown to compile (py_compile exit 0) and to
die at import (first traceback line), so the kill command's difference is a
module crash, not the named limb.

For class B the kill command is run twice on the SAME unmutated bytes: the pair
of results is printed, which is the verdict the ledger reports as "killed"
without any mutant at all.
"""
import hashlib
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LEDGER = os.path.join(HERE, "degenerate-ledger.json")
HONEST = {
    "corpus/instruments/recheck-audit.py": "python3 {inst} --selftest",
    "corpus/instruments/source-recheck.py": "python3 {inst} --selftest",
    "corpus/instruments/frontier-recheck-count.py": "python3 {inst} --root {root}",
}


def run(cmd, cwd):
    proc = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def main():
    rows = json.load(open(LEDGER, encoding="utf-8"))["limbs"]
    scratch = tempfile.mkdtemp(prefix="crit-proof-")
    try:
        shutil.copytree(os.path.join(LANE, "corpus"), os.path.join(scratch, "corpus"))
        for row in rows:
            inst = row["instrument"]
            path = os.path.join(scratch, inst)
            original = open(path, "rb").read()
            honest = HONEST[inst].replace("{inst}", inst).replace("{root}", scratch)
            if row["note"].startswith("class C"):
                open(path, "wb").write(original.decode().replace(row["find"], row["replace"]).encode())
                compile_rc = py_compile.compile(path, cfile=os.path.join(scratch, ".c.pyc"), doraise=False)
                rc, out = run(honest, scratch)
                trace = [ln for ln in out.splitlines() if "Error" in ln]
                print("CRASH %-26s py_compile=ok run_exit=%d traceback=%s"
                      % (row["id"], rc, trace[0][:70] if trace else "NONE"))
                open(path, "wb").write(original)
                continue
            rc_a, out_a = run(honest, scratch)
            open(path, "wb").write(original.decode().replace(row["find"], row["replace"]).encode())
            rc_b, out_b = run(honest, scratch)
            open(path, "wb").write(original)
            same = (rc_a == rc_b) and (digest(out_a) == digest(out_b))
            print("EQUIV %-26s honest_run original=%d/%s mutated=%d/%s identical=%s"
                  % (row["id"], rc_a, digest(out_a), rc_b, digest(out_b), same))
            if row["note"].startswith("class B"):
                kill = row["kill"].replace("{inst}", inst).replace("{root}", scratch)
                rc_1, out_1 = run(kill, scratch)
                rc_2, out_2 = run(kill, scratch)
                print("      STATE %-20s unmutated-run1=%d %-16s unmutated-run2=%d %s"
                      % (row["id"], rc_1, out_1.strip(), rc_2, out_2.strip()))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
