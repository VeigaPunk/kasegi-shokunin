#!/usr/bin/env python3
"""Contract-literal prototype of limb-mutation-check.py -- CRITIQUE ARTIFACT, not C1.

CritC1Kill (round 31) implements the round-31 INTERFACE CONTRACT for C1 verbatim
and adds nothing the contract does not state, in order to measure which degenerate
ledgers the contract as written accepts:

  * one mkdtemp scratch lane for the whole run, corpus copied once;
  * per row: kill command on the UNMUTATED scratch (must exit live_exit and match
    signal, else invalid:live-baseline), then the exact-once find/replace applied
    to the scratch copy of the instrument, then the kill command again;
  * verdicts invalid:find-count / invalid:noop / invalid:nocompile / killed /
    survivor, controls, the two fixed summary lines, and the fixed exit rule.

This file is NOT corpus/instruments/limb-mutation-check.py and must never be
committed there. It exists so the critique's attacks are run, not asserted.
"""
import argparse
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile


def run(cmd, cwd):
    proc = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def sig_state(signal, text):
    return "y" if re.search(signal, text) else "n"


def evaluate_row(row, scratch, kind):
    inst_rel = row["instrument"]
    inst = os.path.join(scratch, inst_rel)
    original = open(inst, "rb").read()
    cmd = row["kill"].replace("{inst}", inst_rel).replace("{root}", scratch)

    live_rc, live_out = run(cmd, scratch)
    live_sig = sig_state(row["signal"], live_out)
    live_field = "%s/%s" % (live_rc, live_sig)

    if live_rc != row["live_exit"] or live_sig != "y":
        print("%s %s live=%s mutant=-/- verdict=invalid:live-baseline"
              % (kind, row["id"], live_field))
        return "invalid:live-baseline"

    text = original.decode("utf-8")
    count = text.count(row["find"])
    if count != 1:
        print("%s %s live=%s mutant=-/- verdict=invalid:find-count"
              % (kind, row["id"], live_field))
        return "invalid:find-count"

    mutated = text.replace(row["find"], row["replace"]).encode("utf-8")
    if mutated == original:
        print("%s %s live=%s mutant=-/- verdict=invalid:noop" % (kind, row["id"], live_field))
        return "invalid:noop"

    open(inst, "wb").write(mutated)
    try:
        try:
            py_compile.compile(inst, cfile=os.path.join(scratch, ".crit-compile.pyc"), doraise=True)
        except py_compile.PyCompileError:
            print("%s %s live=%s mutant=-/- verdict=invalid:nocompile" % (kind, row["id"], live_field))
            return "invalid:nocompile"
        mut_rc, mut_out = run(cmd, scratch)
        mut_sig = sig_state(row["signal"], mut_out)
        verdict = "killed" if (mut_rc != live_rc or mut_sig != "y") else "survivor"
        print("%s %s live=%s mutant=%s/%s verdict=%s"
              % (kind, row["id"], live_field, mut_rc, mut_sig, verdict))
        return verdict
    finally:
        open(inst, "wb").write(original)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--root", default=os.getcwd())
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    ledger = json.load(open(args.ledger, encoding="utf-8"))

    scratch = tempfile.mkdtemp(prefix="crit-limb-")
    try:
        shutil.copytree(os.path.join(root, "corpus"), os.path.join(scratch, "corpus"))
        limbs = ledger["limbs"]
        controls = ledger["controls"]
        limb_verdicts = [evaluate_row(row, scratch, "LIMB") for row in limbs]
        control_verdicts = []
        for row in controls:
            verdict = evaluate_row(row, scratch, "ROW")
            ok = "y" if verdict == row["expect"] else "n"
            print("CONTROL %s verdict=%s expected=%s ok=%s"
                  % (row["id"], verdict, row["expect"], ok))
            control_verdicts.append((verdict, row["expect"]))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    killed = sum(1 for v in limb_verdicts if v == "killed")
    survivors = sum(1 for v in limb_verdicts if v == "survivor")
    valid = sum(1 for v in limb_verdicts if v in ("killed", "survivor"))
    rejected = sum(1 for v, e in control_verdicts if v == e)
    print("limbs=%d killed=%d survivors=%d" % (len(limbs), killed, survivors))
    print("controls=%d rejected=%d" % (len(controls), rejected))
    ok = (len(limbs) == killed and survivors == 0 and valid == len(limbs)
          and rejected == len(controls))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
