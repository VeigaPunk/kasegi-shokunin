#!/usr/bin/env python3
"""figure-audit-mutbat.py - R17 one-limb mutant battery for figure-audit.py's own selftest limbs.

Each mutant is an exact-once edit of the committed instrument bytes; the replay prints one
`MUT <id> ... killed=<0|1>` line per mutant. A mutant is KILLED when its own --selftest exits
nonzero. Two controls must NOT be killed: the pristine instrument (selftest exit 0) and an
equivalent patch (trailing whitespace only). A surviving mutant is a defect of the instrument.

Usage: python3 corpus/instruments/figure-audit-mutbat.py
Exit 0 only when every mutant is killed and both controls pass; 1 otherwise.
Scratch: honours TMPDIR (tempfile.mkdtemp), removed on exit.
"""
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTR = os.path.join(HERE, "figure-audit.py")

MUTANTS = [
    ("m4-drop-stale-literal-case",
     '    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)\n', ""),
    ("m6-readonly-gate-off",
     "return head.startswith(READ_ONLY_HEADS)", "return True"),
]
CONTROLS = [
    ("c-equivalent-trailing-space",
     "return head.startswith(READ_ONLY_HEADS)", "return head.startswith(READ_ONLY_HEADS)  "),
]


def selftest_exit(path, tmp):
    p = subprocess.run([sys.executable, path, "--selftest"], cwd=tmp,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
    tail = (p.stdout or "").strip().splitlines()
    return p.returncode, (tail[-1] if tail else "")


def main():
    with open(INSTR, "r", encoding="utf-8") as fh:
        pristine = fh.read()
    tmp = tempfile.mkdtemp(prefix="figure-audit-mutbat-")
    ok = True
    try:
        rc, last = selftest_exit(INSTR, tmp)
        print("PRISTINE selftest_exit=%d last=%r" % (rc, last))
        if rc != 0:
            ok = False
        for mid, old, new in CONTROLS:
            text = pristine.replace(old, new, 1) if pristine.count(old) == 1 else None
            if text is None:
                print("CONTROL %s sites=%d unusable" % (mid, pristine.count(old)))
                ok = False
                continue
            path = os.path.join(tmp, mid + ".py")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            rc, last = selftest_exit(path, tmp)
            held = rc == 0
            print("CONTROL %s selftest_exit=%d must_not_be_killed=%s last=%r" % (mid, rc, "held" if held else "KILLED", last))
            if not held:
                ok = False
        killed = survivors = 0
        for mid, old, new in MUTANTS:
            n = pristine.count(old)
            if n != 1:
                print("MUT %s sites=%d exact-once=fail" % (mid, n))
                ok = False
                continue
            text = pristine.replace(old, new, 1)
            path = os.path.join(tmp, mid + ".py")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            try:
                py_compile.compile(path, doraise=True)
                compiled = 0
            except py_compile.PyCompileError:
                compiled = 1
            if compiled:
                print("MUT %s sites=%d py_compile=fail killed=0 (not a valid mutant)" % (mid, n))
                ok = False
                continue
            rc, last = selftest_exit(path, tmp)
            k = 1 if rc != 0 else 0
            killed += k
            survivors += 1 - k
            print("MUT %s sites=%d py_compile=0 selftest_exit=%d killed=%d last=%r" % (mid, n, rc, k, last))
        print("mutbat killed=%d/%d survivors=%d controls=%s" % (
            killed, len(MUTANTS), survivors, "pass" if ok else "fail"))
        if survivors:
            ok = False
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
