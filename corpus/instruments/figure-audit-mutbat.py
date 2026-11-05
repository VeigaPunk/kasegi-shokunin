#!/usr/bin/env python3
"""R17 exact-once mutant battery for figure-audit's own selftest.

Five valid mutants must fail selftest; pristine and trailing-space controls
must pass. Missing/duplicate mutation sites, syntax errors, execution errors,
and timeouts fail the battery rather than count as killed mutants.

Usage: python3 figure-audit-mutbat.py --instrument /absolute/figure-audit.py
When installed beside figure-audit.py, --instrument is optional.
Scratch honours TMPDIR and is removed on exit. Set TMPDIR to owned scratch;
this battery is not a sandbox and executes the selected instrument's selftest.
"""
import argparse
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

MUTANTS = [
    ("m4-drop-stale-literal-case",
     '    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)\n', ""),
    ("m6-readonly-gate-off",
     "return head.startswith(READ_ONLY_HEADS)", "return True"),
    ("m7-python-confinement-off",
     "    if target == base or not target.startswith(base + os.sep):", "    if False:"),
    ("m8-python-prefix-off",
     'if len(parts) < 2 or not parts[1].replace("\\\\", "/").startswith("corpus/instruments/"):',
     "if len(parts) < 2:"),
    ("m9-python-boundary-separator-off",
     "    if target == base or not target.startswith(base + os.sep):",
     "    if target == base or not target.startswith(base):"),
]
CONTROLS = [
    ("c-equivalent-trailing-space",
     "return head.startswith(READ_ONLY_HEADS)",
     "return head.startswith(READ_ONLY_HEADS)  "),
]

GATE_ANCHORS = ("return head.startswith(READ_ONLY_HEADS)",
                "return parts[0] in READ_ONLY_HEADS")


def selftest_exit(path, tmp):
    result = subprocess.run(
        [sys.executable, str(path), "--selftest"], cwd=tmp,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
    lines = (result.stdout or "").strip().splitlines()
    return result.returncode, lines[-1] if lines else ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instrument", type=Path,
                        default=Path(__file__).resolve().with_name("figure-audit.py"))
    args = parser.parse_args()
    instrument = args.instrument.resolve()
    pristine = instrument.read_text(encoding="utf-8")
    print("instrument=%s sha256=%s" % (
        instrument, hashlib.sha256(instrument.read_bytes()).hexdigest()))
    gate_sites = sum(pristine.count(anchor) for anchor in GATE_ANCHORS)
    if gate_sites != 1:
        print("gate-anchor sites=%d exact-once=fail" % gate_sites)
        return 2
    gate_anchor = next(anchor for anchor in GATE_ANCHORS if pristine.count(anchor) == 1)
    print("gate-anchor=%r sites=1" % gate_anchor)
    ok = True
    killed = survivors = invalid = 0
    with tempfile.TemporaryDirectory(prefix="figure-audit-mutbat-") as tmp:
        rc, last = selftest_exit(instrument, tmp)
        print("PRISTINE selftest_exit=%d last=%r" % (rc, last))
        if rc != 0:
            ok = False
        for mid, old, new in CONTROLS + MUTANTS:
            if old == GATE_ANCHORS[0]:
                old = gate_anchor
                if mid.startswith("c-"):
                    new = gate_anchor + "  "
            control = mid.startswith("c-")
            label = "CONTROL" if control else "MUT"
            sites = pristine.count(old)
            if sites != 1:
                print("%s %s sites=%d exact-once=fail" % (label, mid, sites))
                ok = False
                invalid += not control
                continue
            text = pristine.replace(old, new, 1)
            try:
                compile(text, mid + ".py", "exec")
            except SyntaxError as exc:
                print("%s %s sites=1 compile=fail invalid=1 detail=%r" % (label, mid, str(exc)))
                ok = False
                invalid += not control
                continue
            path = Path(tmp) / (mid + ".py")
            path.write_text(text, encoding="utf-8", newline="\n")
            rc, last = selftest_exit(path, tmp)
            if control:
                held = rc == 0
                print("CONTROL %s sites=1 selftest_exit=%d must_not_be_killed=%s last=%r" % (
                    mid, rc, "held" if held else "KILLED", last))
                ok = ok and held
            else:
                # The instrument's selftest contract is 0 (pass) or 1 (failed
                # assertions). Other exits are infrastructure errors, not kills.
                valid = rc in (0, 1) and last.startswith("selftest cases=")
                k = int(valid and rc == 1)
                killed += k
                survivors += int(valid and rc == 0)
                invalid += int(not valid)
                ok = ok and valid
                print("MUT %s sites=1 compile=0 selftest_exit=%d killed=%d invalid=%d last=%r" % (
                    mid, rc, k, int(not valid), last))
        print("mutbat killed=%d/%d survivors=%d invalid=%d controls=%s" % (
            killed, len(MUTANTS), survivors, invalid, "pass" if ok else "fail"))
        return 0 if ok and killed == len(MUTANTS) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print("mutbat unavailable=%s detail=%s" % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(2)
