#!/usr/bin/env python3
"""pipeline-mutbat-r63.py — prefreeze per-limb exact-once mutant battery for
figure-audit's round-63 upstream guard (R17/R50 breadth for the new limb).

The r63 candidate guard (figure-audit.py, run_derive) waits the upstream
pipeline stages and refuses a POSITIVE upstream exit >1 with reason
derive-upstream-exit-N while deliberately keeping upstream exit1 counting
(grep no-match), negative signal statuses and the final-stage error reasons.
This battery proves both guard limbs are load-bearing BEFORE the freeze:

  guard-threshold limb (find: the `> 1` fire condition) — 3 mutants
  guard-refusal  limb (find: the guard's refuse-and-propagate return) — 4
      mutants, one of which launders only the reason VALUE while keeping the
      derive-upstream-exit prose marker — killed because the candidate
      selftest binds reason strings, not only exit codes.

Every mutant is an exact-once single-edit over the instrument bytes, keeps
the derive-upstream-exit prose marker, compiles, and must be KILLED: the
instrument's own --selftest exits 1 with its `selftest cases=N failures=M`
summary (M>=1) and at least one named `selftest case=... verdict=fail` line.
A crash, timeout or missing summary is classified INVALID and is NEVER
counted as a kill.

Controls: two semantically equivalent edits must pass the selftest unchanged
(equivalents are never killed), and one invalid edit must fail to compile and
be classified INVALID, never killed.

Anchors: both guard find-strings must occur EXACTLY ONCE in the instrument
bytes; otherwise the battery fails closed (exit 2) before running any
mutant, so an unguarded instrument (e.g. the r62 base) fails closed instead
of reading green.

Usage:
  python3 pipeline-mutbat-r63.py --instrument /abs/figure-audit.py --work /abs/owned/scratch

Exit map (fail-closed): 0 battery passed (pristine passes, all mutants
killed, equivalents held, invalid classified invalid, anchors exact-once);
1 battery failed (survivor, killed control, misclassified invalid, pristine
failure); 2 unusable input (missing/unreadable instrument, unusable --work,
anchor site count != 1).  Uses only the python3 stdlib (R82); the selftest
subprocess interpreter is the interpreter running this battery
(sys.executable).  Writes only under --work (removed on exit) and executes
the selected instrument's --selftest; this battery is not a sandbox.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

THRESHOLD = "if p.returncode > 1:"
REFUSAL = 'return None, out, "derive-upstream-exit-%d" % p.returncode'
MARKER = "derive-upstream-exit"
SELFTEST_SUMMARY = re.compile(r"selftest cases=(\d+) failures=(\d+)")
FAILED_CASE = re.compile(r"^selftest case=(\S+) exit=\d+ want=\d+ verdict=fail$", re.M)
SELFTEST_TIMEOUT = 600

ANCHORS = (("guard-threshold", THRESHOLD), ("guard-refusal", REFUSAL))

MUTANTS = [
    ("m-threshold-0",
     THRESHOLD, "if p.returncode > 0:"),
    ("m-threshold-2",
     THRESHOLD, "if p.returncode > 2:"),
    ("m-threshold-ge0",
     THRESHOLD, "if p.returncode >= 0:"),
    ("m-refusal-dead",
     REFUSAL, 'upstream_reason = "derive-upstream-exit-%d" % p.returncode'),
    ("m-refusal-skip",
     REFUSAL, "continue  # derive-upstream-exit suppressed"),
    ("m-refusal-rc-launder",
     REFUSAL, "p.returncode = 0  # derive-upstream-exit suppressed"),
    ("m-reason-value-constant",
     REFUSAL, 'return None, out, "derive-upstream-exit-%d" % 1'),
]
CONTROLS = [
    ("c-equiv-reversed",
     THRESHOLD, "if 1 < p.returncode:"),
    ("c-equiv-trailing-space",
     THRESHOLD, "if p.returncode > 1:  "),
    ("c-invalid-missing-colon",
     THRESHOLD, "if p.returncode > 1"),
]


def run_selftest(path, cwd):
    """Run the instrument's --selftest; return (rc, last_line, summary, failed_case_ids).

    A timeout returns rc None with no summary, which classifies INVALID.
    """
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = str(cwd)
    try:
        result = subprocess.run(
            [sys.executable, str(path), "--selftest"], cwd=str(cwd), env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            errors="replace", timeout=SELFTEST_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None, "", None, []
    out = result.stdout or ""
    lines = out.strip().splitlines()
    last = lines[-1] if lines else ""
    summary = SELFTEST_SUMMARY.fullmatch(last) if last else None
    failed = FAILED_CASE.findall(out)
    return result.returncode, last, summary, failed


def main():
    parser = argparse.ArgumentParser(
        description="r63 upstream-guard prefreeze exact-once mutant battery")
    parser.add_argument("--instrument", required=True, type=Path,
                        help="absolute path to the guard-bearing figure-audit.py")
    parser.add_argument("--work", required=True, type=Path,
                        help="existing owned scratch directory for mutated copies")
    args = parser.parse_args()
    print("pipeline-mutbat-r63 instrument=%s" % args.instrument)
    print("battery-utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    instrument = Path(os.path.abspath(args.instrument))
    if not instrument.is_file():
        print("BATTERY-UNAVAILABLE reason=instrument-missing path=%s" % instrument)
        return 2
    try:
        pristine = instrument.read_text(encoding="utf-8")
        digest = hashlib.sha256(instrument.read_bytes()).hexdigest()
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print("BATTERY-UNAVAILABLE reason=instrument-unreadable detail=%r" % (exc,))
        return 2
    print("instrument-sha256=%s" % digest)
    work = Path(os.path.abspath(args.work))
    if not work.is_dir():
        print("BATTERY-UNAVAILABLE reason=work-unusable path=%s" % work)
        return 2
    run_dir = work / ("pipeline-mutbat-run-%d" % os.getpid())
    try:
        run_dir.mkdir(parents=True)
    except OSError as exc:
        print("BATTERY-UNAVAILABLE reason=work-unusable detail=%r" % (exc,))
        return 2

    def write_mutant(name, text):
        path = run_dir / (name + ".py")
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    ok = True
    try:
        # Anchors: exact-once, else fail closed without running any mutant.
        for label, anchor in ANCHORS:
            sites = pristine.count(anchor)
            good = sites == 1
            print("anchor %s sites=%d exact-once=%s" % (label, sites, "ok" if good else "fail"))
            ok = ok and good
        if not ok:
            print("MUTBAT mutants=0 killed=0 survivors=0 invalid=0 controls=0 "
                  "verdict=FAIL reason=anchor-sites")
            print("battery-exit=2")
            return 2

        # Pristine: the guard-bearing instrument must pass its own selftest.
        rc, last, summary, failed = run_selftest(instrument, run_dir)
        if rc == 0 and summary is not None and summary.group(2) == "0" and not failed:
            print("PRISTINE selftest_exit=0 cases=%s failures=0 verdict=pass" % summary.group(1))
        else:
            print("PRISTINE selftest_exit=%s last=%r verdict=fail" % (rc, last))
            print("battery-exit=1")
            return 1

        killed = survivors = invalid = 0

        # Controls: equivalents must pass; the invalid edit is never a kill.
        for cid, old, new in CONTROLS:
            sites = pristine.count(old)
            if sites != 1:
                ok = False
                print("CONTROL %s sites=%d exact-once=fail verdict=fail" % (cid, sites))
                continue
            text = pristine.replace(old, new, 1)
            try:
                compile(text, cid + ".py", "exec")
            except SyntaxError as exc:
                if cid.startswith("c-invalid"):
                    invalid += 1
                    print("CONTROL %s sites=1 compile=fail invalid=1 killed=0 "
                          "verdict=invalid-held detail=%r" % (cid, str(exc)))
                else:
                    ok = False
                    print("CONTROL %s sites=1 compile=fail verdict=fail detail=%r" % (cid, str(exc)))
                continue
            if cid.startswith("c-invalid"):
                # An invalid control that compiles is a battery defect; even then
                # it must not be counted as a kill.
                rc, last, summary, failed = run_selftest(write_mutant(cid, text), run_dir)
                ok = False
                print("CONTROL %s sites=1 compile=ok selftest_exit=%s killed=0 "
                      "verdict=invalid-miscompiled last=%r" % (cid, rc, last))
                continue
            if MARKER not in text:
                ok = False
                print("CONTROL %s marker-lost verdict=fail" % cid)
                continue
            rc, last, summary, failed = run_selftest(write_mutant(cid, text), run_dir)
            held = (rc == 0 and summary is not None and summary.group(2) == "0" and not failed)
            print("CONTROL %s sites=1 compile=ok selftest_exit=%s killed=%s verdict=%s last=%r" % (
                cid, rc, "no" if held else "KILLED", "held" if held else "fail", last))
            ok = ok and held

        # Mutants: each must be killed by a stable, named selftest failure.
        for mid, old, new in MUTANTS:
            sites = pristine.count(old)
            if sites != 1:
                invalid += 1
                ok = False
                print("MUT %s sites=%d exact-once=fail invalid=1 killed=0" % (mid, sites))
                continue
            text = pristine.replace(old, new, 1)
            if MARKER not in text:
                invalid += 1
                ok = False
                print("MUT %s marker-lost invalid=1 killed=0" % mid)
                continue
            try:
                compile(text, mid + ".py", "exec")
            except SyntaxError as exc:
                invalid += 1
                ok = False
                print("MUT %s sites=1 compile=fail invalid=1 killed=0 detail=%r" % (mid, str(exc)))
                continue
            rc, last, summary, failed = run_selftest(write_mutant(mid, text), run_dir)
            if rc == 1 and summary is not None and int(summary.group(2)) >= 1 and failed:
                verdict, dead = "killed", 1
                killed += 1
            elif rc == 0 and summary is not None and summary.group(2) == "0" and not failed:
                verdict, dead = "survived", 0
                survivors += 1
            else:
                verdict, dead = "invalid", 0
                invalid += 1
            ok = ok and dead == 1
            print("MUT %s sites=1 compile=ok selftest_exit=%s killed=%d failed_case=%s "
                  "verdict=%s last=%r" % (
                      mid, rc, dead, failed[0] if failed else "none", verdict, last))

        verdict = "PASS" if (ok and killed == len(MUTANTS)) else "FAIL"
        print("MUTBAT mutants=%d killed=%d survivors=%d invalid=%d controls=%d verdict=%s" % (
            len(MUTANTS), killed, survivors, invalid, len(CONTROLS), verdict))
        print("battery-exit=%d" % (0 if verdict == "PASS" else 1))
        return 0 if verdict == "PASS" else 1
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
