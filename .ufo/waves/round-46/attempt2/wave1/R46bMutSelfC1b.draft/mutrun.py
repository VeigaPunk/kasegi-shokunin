#!/usr/bin/env python3
"""R46bMutSelfC1b — own mutant battery for r46-c1-gate.py (independent of r46-mutbat.py).

Each mutant is (id, old, new): a SINGLE-LINE edit of the counter, applied to a COPY of
the lane's corpus/instruments tree. The committed selftest is then run against the
mutant copy (--counter <mutant>), exactly the way r46-mutbat.py grades a mutant.
Verdict: caught (selftest failures>0 under the mutant) | survived (failures==0).
The lane tree is only ever read.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
INSTR = "corpus/instruments"
GATE = "r46-c1-gate.py"
SELFTEST = "r46-counters-selftest-c1.py"

# (id, old, new) — single-line edits of r46-c1-gate.py, NOT in r46-mutbat.py's C1_MUTANTS table
MUTANTS = [
    # ---- control: an edit that changes bytes but cannot change any verdict ----
    ("N00-control-comment-only",
     "never runs git; stdlib only.",
     "never runs git; stdlib only. (control: docstring text only, no behaviour change)"),

    # ---- entry_mode / check_row: what counts as a well-formed row ----
    ("N01-cell-count-floor",
     "if len(row) != 4:",
     "if len(row) < 4:"),
    ("N02-alnum-floor",
     "sum(c.isalnum() for c in tok) < 6",
     "sum(c.isalnum() for c in tok) < 3"),
    ("N03-range-window",
     "b - a > 39",
     "b - a > 400"),
    ("N04-self-anchor-ban",
     "or rel == entry_rel",
     "or rel == \"\""),
    ("N05-gate-self-anchor-ban",
     "rel.endswith(\"r46-c1-gate.py\")",
     "rel.endswith(\"r46-c1-gate.py.bak\")"),
    ("N06-realpath-containment",
     "or not os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)",
     ""),
    ("N07-range-past-eof",
     "or b > len(lines)",
     "or b > len(lines) + 100"),
    ("N08-cr-line-break-check",
     "or \"\\r\" in \"\".join(lines[a - 1:b])",
     ""),
    ("N09-duplicate-row-id",
     "len(set(ids)) == len(ids)",
     "len(set(ids)) >= 1"),
    ("N10-two-distinct-anchor-files",
     "len(files) >= 2",
     "len(files) >= 1"),
    ("N11-two-distinct-file-digests",
     "len(digests) >= 2",
     "len(digests) >= 1"),
    ("N12-token-distinctness",
     "len({k[3] for k in keys}) == len(keys)",
     "len({k[3] for k in keys}) >= 1"),
    ("N13-section-heading-raw-count",
     "if len(starts) != 1 or len(raw) != 1:",
     "if len(starts) != 1:"),
    ("N14-stray-table-rows",
     "if stray:",
     "if False:"),

    # ---- how a recheck line is read and executed ----
    ("N15-cd-strip-allows-semicolon",
     "[^&;]+?",
     "[^&]+?"),
    ("N16-allowed-test-segment-widened",
     "SEG_TEST = re.compile(r\"^test (?:! )?-[defs] [~A-Za-z0-9_./-]+$\")",
     "SEG_TEST = re.compile(r\"^test (?:! )?-[defs] [~A-Za-z0-9_./ ;]+$\")"),
    ("N17-comment-not-stripped",
     "cmd = re.sub(r\"[ \\t]+#.*$\", \"\", cmd)",
     "cmd = cmd"),
    ("N18-hidden-recheck-count",
     "n = 99",
     "n = 1"),
    # N19's locator spans the def line so it hits recheck_line() (line 130), not
    # live_lines() (line 118); the edit itself changes exactly one source line.
    ("N19-first-recheck-line-wins",
     "def recheck_line(text: str) -> str | None:\n    for ln in lines_of(text):",
     "def recheck_line(text: str) -> str | None:\n    for ln in reversed(lines_of(text)):"),
    ("N20-grader-env-drops-home",
     "for k in (\"HOME\", \"PATH\", \"TMPDIR\") if k in os.environ",
     "for k in (\"PATH\", \"TMPDIR\") if k in os.environ"),
    ("N21-read-newline-translated",
     "encoding=\"utf-8\", newline=\"\"",
     "encoding=\"utf-8\", newline=None"),
    ("N22-norm-drops-curly-single-quotes",
     ".replace(\"\\u2019\", \"'\").replace(\"\\u2018\", \"'\")",
     ".replace(\"\\u2019\", \"'\")"),
    ("N23-allowed-segment-split",
     "cmd.split(\" && \")",
     "cmd.split(\"&&\")"),
]


def sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run_one(mid: str, old: str, new: str, lane: str, pure: str, work: str, jobs: int) -> dict:
    src = os.path.join(lane, INSTR, GATE)
    text = open(src, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        return {"id": mid, "verdict": "DRIFT", "detail": "old-substring occurs %d times" % n,
                "failures": -1, "stdout": ""}
    mdir = os.path.join(work, mid)
    shutil.rmtree(mdir, ignore_errors=True)
    dst_inst = os.path.join(mdir, INSTR)
    shutil.copytree(os.path.join(lane, INSTR), dst_inst, symlinks=True)
    dst = os.path.join(dst_inst, GATE)
    open(dst, "w", encoding="utf-8").write(text.replace(old, new, 1))
    cmd = [sys.executable, "-I", os.path.join(lane, INSTR, SELFTEST),
           "--counter", dst, "--pure", pure, "--work", os.path.join(mdir, "run"),
           "--jobs", str(jobs)]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=work)
    except subprocess.TimeoutExpired:
        return {"id": mid, "verdict": "TIMEOUT", "detail": "", "failures": -1, "stdout": ""}
    m = re.findall(r"failures=(\d+)", p.stdout)
    fails = int(m[-1]) if m else -1
    verdict = "caught" if fails >= 1 else "survived"
    detail = ""
    if fails >= 1:
        bad = [ln for ln in p.stdout.splitlines()
               if re.search(r"FALSE-GREEN|UNEXPECTED|EXECUTED", ln)]
        detail = " | ".join(bad[:3])[:400]
    shutil.rmtree(mdir, ignore_errors=True)
    return {"id": mid, "verdict": verdict, "detail": detail, "failures": fails,
            "stdout": p.stdout[-1500:]}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--pure", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--par", type=int, default=5)
    ap.add_argument("--only", default=None, help="comma-separated mutant ids")
    ap.add_argument("--battery", action="store_true", help="cross-check: run the COMMITTED battery table instead")
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    src = os.path.join(a.lane, INSTR, GATE)
    before = sha(src)
    muts = MUTANTS
    if a.battery:
        sys.path.insert(0, os.path.join(a.lane, INSTR))
        import importlib.util
        spec = importlib.util.spec_from_file_location("r46mutbat", os.path.join(a.lane, INSTR, "r46-mutbat.py"))
        mb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mb)
        muts = [(m[0], m[1], m[2]) for m in mb.C1_MUTANTS]
        print("battery cross-check: %d committed C1 mutants" % len(muts))
    if a.only:
        keep = set(a.only.split(","))
        muts = [m for m in muts if m[0] in keep]
    print("lane-counter sha256 before = %s" % before)
    results = []
    with cf.ThreadPoolExecutor(max_workers=a.par) as ex:
        futs = {ex.submit(run_one, mid, old, new, a.lane, a.pure, a.work, a.jobs): mid
                for mid, old, new in muts}
        for fut in cf.as_completed(futs):
            r = fut.result()
            results.append(r)
            print("mutant=%-34s mutant_failures=%d verdict=%s %s"
                  % (r["id"], r["failures"], r["verdict"], r["detail"]), flush=True)
    after = sha(src)
    print("lane-counter sha256 after  = %s  unchanged=%s" % (after, before == after))
    caught = sum(1 for r in results if r["verdict"] == "caught")
    surv = sum(1 for r in results if r["verdict"] == "survived")
    other = len(results) - caught - surv
    print("ownmutants total=%d caught=%d survived=%d other=%d" % (len(results), caught, surv, other))
    for r in sorted(results, key=lambda x: x["id"]):
        if r["verdict"] == "survived":
            print("SURVIVOR %s failures=%d" % (r["id"], r["failures"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
