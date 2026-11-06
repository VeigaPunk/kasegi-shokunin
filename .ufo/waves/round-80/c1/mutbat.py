#!/usr/bin/env python3
"""mutbat.py — round-80 C1 mutant battery for corpus/instruments/recheck-cwd-census.py.

Frozen with the round-80 claims (successor of the round-79 counter; QUALITY R129: the
exception classifier keys on the dedicated marker 'FAIL exception=' — a FAIL whose detail
BEGINS with 'exception=' — never on a free-text substring of the detail). For each row of the transform table (JSON list of
{"id", "anchor", "replacement", "class"}) the target's bytes are mutated by exactly ONE
literal replacement of `anchor` (which must occur exactly once, else NOT-DERIVED) and the
mutant runs `python3 -B <mutant> --selftest` under a fresh TMPDIR scratch. Verdicts:

  KILLED          exit != 0, at least one 'selftest case=... FAIL' line, no 'Traceback'
  EXCEPTION-KILL  exit != 0, a FAIL line whose detail begins 'exception=', no 'Traceback'
                  (counts as killed only for rows whose class is "exception")
  SURVIVED        exit 0
  DIRTY           exit != 0 without a FAIL line, or with a 'Traceback'
  NOT-DERIVED     the anchor does not occur exactly once in the target

A row of class "assertion" counts only as KILLED; a row of class "exception" counts as
KILLED or EXCEPTION-KILL. The unmutated target must itself print
'selftest cases=<expect> failures=0' and exit 0 (the baseline limb).

Output: one 'MUTANT <id> verdict=<v> rc=<n> fails=<k>' line per row, then
'MUTBAT target_sha256=<h> baseline=<ok|bad> rows=<n> killed=<k> survived=<s>
dirty=<d> notderived=<x>' and exit 0 iff baseline ok and every row counts as killed;
exit 1 otherwise; exit 2 on a usage or read error.

Usage:
  python3 mutbat.py --target FILE --table TABLE.json --expect-cases N --work DIR [--keep DIR]
  python3 mutbat.py --selftest --work DIR
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FAIL_RE = re.compile(r"^selftest case=\S+ FAIL", re.M)
EXC_RE = re.compile(r"^selftest case=\S+ FAIL exception=", re.M)


def run_selftest(path, work):
    tmp = tempfile.mkdtemp(prefix="mutbat-run-", dir=work)
    try:
        env = dict(os.environ)
        env["TMPDIR"] = tmp
        proc = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=900)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def verdict(rc, out):
    fails = len(FAIL_RE.findall(out))
    if rc == 0:
        return "SURVIVED", fails
    if "Traceback" in out or fails == 0:
        return "DIRTY", fails
    if EXC_RE.search(out):
        return "EXCEPTION-KILL", fails
    return "KILLED", fails


def battery(target, rows, expect_cases, work, keep=None):
    with open(target, encoding="utf-8") as fh:
        src = fh.read()
    sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    rc0, out0 = run_selftest(target, work)
    baseline = rc0 == 0 and ("selftest cases=%d failures=0" % expect_cases) in out0
    tally = {"killed": 0, "survived": 0, "dirty": 0, "notderived": 0}
    lines = []
    for row in rows:
        n = src.count(row["anchor"])
        if n != 1:
            tally["notderived"] += 1
            lines.append("MUTANT %s verdict=NOT-DERIVED occurrences=%d" % (row["id"], n))
            continue
        mutant = src.replace(row["anchor"], row["replacement"], 1)
        mdir = tempfile.mkdtemp(prefix="mutbat-%s-" % row["id"], dir=work)
        mpath = os.path.join(mdir, os.path.basename(target))
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant)
        rc, out = run_selftest(mpath, work)
        v, fails = verdict(rc, out)
        if keep:
            os.makedirs(keep, exist_ok=True)
            with open(os.path.join(keep, "%s.out" % row["id"]), "w", encoding="utf-8") as fh:
                fh.write("rc=%d\n%s" % (rc, out))
        shutil.rmtree(mdir, ignore_errors=True)
        counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row.get("class") == "exception")
        if counts:
            tally["killed"] += 1
        elif v == "SURVIVED":
            tally["survived"] += 1
        else:
            tally["dirty"] += 1
        lines.append("MUTANT %s verdict=%s rc=%d fails=%d counted=%s"
                     % (row["id"], v, rc, fails, "yes" if counts else "no"))
    lines.append("MUTBAT target_sha256=%s baseline=%s rows=%d killed=%d survived=%d dirty=%d "
                 "notderived=%d" % (sha, "ok" if baseline else "bad", len(rows), tally["killed"],
                                    tally["survived"], tally["dirty"], tally["notderived"]))
    ok = baseline and tally["killed"] == len(rows) and len(rows) > 0
    return ok, lines


TOY = '''import sys
def tested(x):
    return x > 0
def untested(x):
    return x < 0
def selftest():
    fails = 0
    try:
        ok = tested(1) is True and tested(-1) is False
        detail = "note=exception-free ret=%r" % (tested(1),)
    except Exception as exc:
        ok, detail = False, "exception=%r" % (exc,)
    print("selftest case=tested %s %s" % ("ok" if ok else "FAIL", detail))
    fails += 0 if ok else 1
    print("selftest cases=1 failures=%d" % fails)
    return 0 if fails == 0 else 1
if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
'''


def selftest(work):
    d = tempfile.mkdtemp(prefix="mutbat-selftest-", dir=work)
    try:
        toy = os.path.join(d, "toy.py")
        with open(toy, "w", encoding="utf-8") as fh:
            fh.write(TOY)
        rows = [
            {"id": "T-KILL", "anchor": "    return x > 0\n", "replacement": "    return True\n",
             "class": "assertion"},
            {"id": "T-SURV", "anchor": "    return x < 0\n", "replacement": "    return True\n",
             "class": "assertion"},
            {"id": "T-ABSENT", "anchor": "no such text", "replacement": "", "class": "assertion"},
            {"id": "T-EXC", "anchor": "    return x > 0\n",
             "replacement": "    raise ValueError('boom')\n", "class": "exception"},
            {"id": "T-EXCA", "anchor": "    return x > 0\n",
             "replacement": "    raise ValueError('boom')\n", "class": "assertion"},
        ]
        ok, lines = battery(toy, rows, 1, d)
        want = {"T-KILL": "KILLED", "T-SURV": "SURVIVED", "T-ABSENT": "NOT-DERIVED",
                "T-EXC": "EXCEPTION-KILL", "T-EXCA": "EXCEPTION-KILL"}
        got = {ln.split()[1]: ln.split()[2].split("=")[1] for ln in lines if ln.startswith("MUTANT")}
        counted = {ln.split()[1]: ln.rsplit("counted=", 1)[1] for ln in lines
                   if ln.startswith("MUTANT") and "counted=" in ln}
        want_counted = {"T-KILL": "yes", "T-SURV": "no", "T-EXC": "yes", "T-EXCA": "no"}
        okk = (not ok) and got == want and counted == want_counted and "baseline=ok" in lines[-1]
        ok2, lines2 = battery(toy, [rows[0], rows[3]], 1, d)
        okk = okk and ok2
        print("mutbat selftest %s got=%s counted=%s all_killed_exit=%s"
              % ("ok" if okk else "FAIL", got, counted, ok2))
        return 0 if okk else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target")
    ap.add_argument("--table")
    ap.add_argument("--expect-cases", type=int)
    ap.add_argument("--work", required=True)
    ap.add_argument("--keep")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.work):
        print("mutbat: --work %s is not a directory" % a.work, file=sys.stderr)
        return 2
    if a.selftest:
        return selftest(a.work)
    if not (a.target and a.table and a.expect_cases is not None):
        print("mutbat: --target, --table and --expect-cases are required", file=sys.stderr)
        return 2
    try:
        with open(a.table, encoding="utf-8") as fh:
            rows = json.load(fh)
    except (OSError, ValueError) as exc:
        print("mutbat: cannot read table: %s" % exc, file=sys.stderr)
        return 2
    ok, lines = battery(a.target, rows, a.expect_cases, a.work, a.keep)
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
