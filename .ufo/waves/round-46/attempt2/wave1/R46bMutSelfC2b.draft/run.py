#!/usr/bin/env python3
"""R46bMutSelfC2b runner — apply each independent mutant to a COPY of r46-c2-gate.py
and grade it with the committed selftest r46-counters-selftest-c2.py.

Grading (mirrors r46-mutbat.py):
  caught    selftest failures>0 under the mutant (the committed selftest noticed)
  survivor  selftest failures==0 under the mutant while the pristine counter reads
            failures=0 (baseline must be clean, else inconclusive)
Never mutates the lane: mutants live in scratch copies only.
"""
from __future__ import annotations

import concurrent.futures as cf
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mutants import MUTANTS  # noqa: E402

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
COUNTER = "corpus/instruments/r46-c2-gate.py"
SELFTEST = "corpus/instruments/r46-counters-selftest-c2.py"
S = "/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2b"
PURE = os.path.join(S, "pure")
WORK = os.path.join(S, "work")
JOBS = int(os.environ.get("JOBS", "8"))


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def apply_mutant(src_counter: str, old: str, new: str, dst_dir: str) -> str:
    text = open(src_counter, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        raise SystemExit("drift: old-substring occurs %d times (expected 1): %r" % (n, old))
    dst_inst = os.path.join(dst_dir, "corpus", "instruments")
    shutil.copytree(os.path.join(LANE, "corpus", "instruments"), dst_inst, symlinks=True)
    dst = os.path.join(dst_inst, "r46-c2-gate.py")
    open(dst, "w", encoding="utf-8").write(text.replace(old, new, 1))
    return dst


def run_selftest(counter_path, tag):
    hs = os.path.join(S, "hs-" + re.sub(r"[^A-Za-z0-9_.-]", "_", tag))
    os.makedirs(hs, exist_ok=True)
    tmp = os.path.join(hs, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = hs
    env["TMPDIR"] = tmp
    env["PYTHONHASHSEED"] = "0"
    cmd = [sys.executable, "-I", os.path.join(LANE, SELFTEST), "--pure", PURE]
    if counter_path:
        cmd += ["--counter", counter_path]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=LANE, env=env)
    out = p.stdout + p.stderr
    m = re.findall(r"failures=(\d+)", out)
    fails = int(m[-1]) if m else -1
    cases = re.search(r"cases=(\d+)", out)
    return fails, (int(cases.group(1)) if cases else -1), p.returncode, out


RESULTS = os.path.join(S, "results.jsonl")


def main() -> int:
    os.makedirs(WORK, exist_ok=True)
    src = os.path.join(LANE, COUNTER)
    before = sha(src)
    print("pristine-counter-sha256=%s" % before, flush=True)

    # resume: skip mutants already graded in a previous (timed-out) pass
    done = {}
    if os.path.isfile(RESULTS):
        for ln in open(RESULTS):
            ln = ln.strip()
            if ln:
                r = json.loads(ln)
                done[r["id"]] = r
    if done:
        print("resume: %d mutants already graded" % len(done), flush=True)

    todo = [m for m in MUTANTS if m[0] not in done]
    print("todo: %d mutants" % len(todo), flush=True)

    # baseline: the pristine counter must be clean, else every verdict is inconclusive
    bf, bc, brc, bout = run_selftest(src, "baseline")
    print("baseline selftest cases=%d failures=%d exit=%d" % (bc, bf, brc), flush=True)
    if bf != 0:
        print("BASELINE-DIRTY — all verdicts inconclusive")
        print(bout[-4000:])
        return 2

    results = list(done.values())

    def one(item):
        mid, gate, old, new = item
        mdir = tempfile.mkdtemp(prefix="mut-", dir=WORK)
        try:
            dst = apply_mutant(src, old, new, mdir)
            fails, cases, rc, out = run_selftest(dst, mid)
            verdict = "caught" if fails >= 1 else "survivor"
            # which selftest case failed first (evidence of the detector firing)
            bad = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
            return dict(id=mid, gate=gate, failures=fails, cases=cases, exit=rc,
                        verdict=verdict, first_fail=bad[0] if bad else "",
                        n_failed_lines=len(bad))
        except SystemExit as exc:
            return dict(id=mid, gate=gate, failures=-2, cases=-1, exit=-1,
                        verdict="drift", first_fail=str(exc), n_failed_lines=0)
        finally:
            shutil.rmtree(mdir, ignore_errors=True)

    lock = __import__("threading").Lock()
    fh = open(RESULTS, "a")
    with cf.ThreadPoolExecutor(max_workers=JOBS) as ex:
        for r in ex.map(one, todo):
            results.append(r)
            with lock:
                fh.write(json.dumps(r) + "\n")
                fh.flush()
            print("mutant=%s gate=%s selftest_failures=%d verdict=%s" %
                  (r["id"], r["gate"], r["failures"], r["verdict"]), flush=True)
            if r["first_fail"]:
                print("   first-fail: %s" % r["first_fail"], flush=True)
    fh.close()

    after = sha(src)
    print("counter-sha256-after=%s restored=%s" % (after, after == before))
    caught = sum(1 for r in results if r["verdict"] == "caught")
    surv = sum(1 for r in results if r["verdict"] == "survivor")
    drift = sum(1 for r in results if r["verdict"] == "drift")
    print("SUMMARY mutants=%d caught=%d survivor=%d drift=%d baseline_failures=0 counter_restored=%s" %
          (len(results), caught, surv, drift, after == before))
    with open(os.path.join(S, "results.json"), "w") as fh2:
        json.dump({"counter_sha256_before": before, "counter_sha256_after": after,
                   "baseline_failures": bf, "results": results}, fh2, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
