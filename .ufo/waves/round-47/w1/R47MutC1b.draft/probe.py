#!/usr/bin/env python3
"""R47MutC1b probe driver — 6 fresh c1 counter mutants on limbs L7-L11.

Frozen bytes only: fixtures + instruments come from the freeze-commit corpus
export in $S/exports (sha-pinned vs .ufo/waves/round-47/freeze.txt). The lane
repo is only ever READ (snapshot copies by the selftest, hash pins here).
Scratch-only writes. Detector = r47-counters-selftest.py --counter c1
(43-case tree-probe suite; c1 subset), per r47-mutbat.py grading:
caught == selftest failures>0 under mutant while pristine failures==0.
"""
from __future__ import annotations
import hashlib, json, os, re, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kasegi-r47/R47MutC1b"
FREEZE = S + "/exports/freeze"
BASE = S + "/exports/base"
INSTR = FREEZE + "/corpus/instruments"
COUNTER = INSTR + "/r47-routed-defects.py"
SELFTEST = INSTR + "/r47-counters-selftest.py"
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r47-routed-defects.py"
LOGS = S + "/logs"
os.makedirs(LOGS, exist_ok=True)
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "r46-mutant-equivalents")


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd, cwd, timeout=600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def selftest(work, gate=None, keep=False):
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-I", SELFTEST, "--base", BASE, "--work", work, "--counter", "c1"]
    if gate:
        cmd += ["--gate", gate]
    if keep:
        cmd += ["--keep"]
    rc, out, err = run(cmd, cwd=work)
    m = re.findall(r"failures=(\d+)", out)
    return rc, out, err, (int(m[-1]) if m else -1)


def cases(out: str) -> dict:
    d = {}
    for ln in out.splitlines():
        m = re.match(r"case (\S+) ok=(\d) want=(\S+) got=(\S+)", ln)
        if m:
            d[m.group(1)] = (int(m.group(2)), m.group(3), m.group(4))
    return d


receipt = {}
receipt["freeze_pins"] = {
    "lane_counter_sha": sha(LANE_COUNTER),
    "freeze_counter_sha": sha(COUNTER),
    "freeze_selftest_sha": sha(SELFTEST),
}

# 1. pristine baseline, run twice (do-nothing control)
rc1, out1, err1, f1 = selftest(S + "/work/pristine-1")
rc2, out2, err2, f2 = selftest(S + "/work/pristine-2")
open(LOGS + "/pristine-1.txt", "w").write(out1 + ("\n--stderr--\n" + err1 if err1 else ""))
open(LOGS + "/pristine-2.txt", "w").write(out2 + ("\n--stderr--\n" + err2 if err2 else ""))
receipt["pristine_run1"] = {"rc": rc1, "failures": f1}
receipt["pristine_run2"] = {"rc": rc2, "failures": f2}
receipt["pristine_stdout_identical"] = out1.splitlines() == out2.splitlines()
PRISTINE_CASES = cases(out1)

# 2. counter tree receipts on pristine bytes
for tag, root in (("base", BASE), ("freeze", FREEZE)):
    rc, out, err = run([sys.executable, "-I", COUNTER, "--root", root, "--baseline", BASE], cwd=S)
    open(LOGS + "/counter-%s.txt" % tag, "w").write(out + err)
    lines = out.strip().splitlines()
    receipt["counter_" + tag] = {"rc": rc, "summary": lines[-1] if lines else ""}

# green tree via --keep, then pristine counter target receipt
gwork = S + "/work/green-keep"
rcg, outg, errg, fg = selftest(gwork, None, keep=True)
open(LOGS + "/selftest-greenkeep.txt", "w").write(outg + errg)
GREEN = gwork + "/c1-green"
rcg2, outg2, errg2 = run([sys.executable, "-I", COUNTER, "--root", GREEN, "--baseline", BASE], cwd=S)
open(LOGS + "/counter-green-pristine.txt", "w").write(outg2 + errg2)
gl = outg2.strip().splitlines()
receipt["counter_green_pristine"] = {"rc": rcg2, "summary": gl[-1] if gl else ""}

# 3. the six fresh mutants
MUTANTS = [
    ("L7d-lesson46-dropped",
     "for rel in (LESSON47, LESSON46):",
     "for rel in (LESSON47,):"),
    ("L8e-manifest-pin-dropped",
     'if not os.path.isfile(man) or sha(open(man, "rb").read()) != MAN_SHA:',
     "if not os.path.isfile(man):"),
    ("L9d-body-bounds-off-by-one",
     "rng[0] <= a <= b <= rng[1] and b - a <= 11",
     "rng[0] - 1 <= a <= b <= rng[1] + 1 and b - a <= 11"),
    ("L9e-uncited-masked",
     "ok = failed == 0 and uncited <= 0 and passed >= 20",
     "ok = failed == 0 and passed >= 20"),
    ("L10d-lead-anywhere",
     'leads = section(raw, "Leads (unopened)")',
     "leads = raw"),
    ("L11d-precision-phrase-wide",
     'b = "S068" in t and "one GHSA advisory entry" in t',
     'b = "S068" in t and "GHSA advisory" in t'),
]

receipt["mutants"] = []
for mid, old, new in MUTANTS:
    src = open(COUNTER, encoding="utf-8").read()
    n = src.count(old)
    row = {"id": mid, "old_count": n}
    if n != 1:
        row["error"] = "old-substring occurs %d times" % n
        receipt["mutants"].append(row)
        continue
    mdir = S + "/work/mut-" + mid
    shutil.rmtree(mdir, ignore_errors=True)
    os.makedirs(mdir, exist_ok=True)
    inst = mdir + "/instruments"
    shutil.copytree(INSTR, inst, symlinks=True, ignore=IGNORE)
    dst = inst + "/r47-routed-defects.py"
    open(dst, "w", encoding="utf-8").write(src.replace(old, new, 1))
    row["mutant_counter_sha"] = sha(dst)
    row["mutant_bytes"] = {"old": old, "new": new}
    rc, out, err, mf = selftest(mdir + "/run", dst)
    open(LOGS + "/mut-%s.txt" % mid, "w").write(out + ("\n--stderr--\n" + err if err else ""))
    mcases = cases(out)
    row["mutant_failures"] = mf
    row["selftest_rc"] = rc
    row["verdict"] = "caught" if mf >= 1 else "uncaught"
    row["divergent_cases"] = sorted(k for k in set(PRISTINE_CASES) | set(mcases)
                                    if PRISTINE_CASES.get(k) != mcases.get(k))
    # tree-level behavior of the mutant counter on green + base + freeze
    row["trees"] = {}
    for tag, root in (("green", GREEN), ("base", BASE), ("freeze", FREEZE)):
        rct, outt, _ = run([sys.executable, "-I", dst, "--root", root, "--baseline", BASE], cwd=S)
        open(LOGS + "/mut-%s-%s.txt" % (mid, tag), "w").write(outt)
        tl = outt.strip().splitlines()
        row["trees"][tag] = {"rc": rct, "summary": tl[-1] if tl else ""}
    shutil.rmtree(mdir, ignore_errors=True)
    receipt["mutants"].append(row)

# 4. restoration evidence: re-pin lane + freeze bytes, rerun pristine detector
receipt["restoration"] = {
    "lane_counter_sha_after": sha(LANE_COUNTER),
    "freeze_counter_sha_after": sha(COUNTER),
    "lane_unchanged": sha(LANE_COUNTER) == receipt["freeze_pins"]["lane_counter_sha"],
}
rc3, out3, err3, f3 = selftest(S + "/work/pristine-3")
receipt["pristine_run3_after_mutants"] = {"rc": rc3, "failures": f3}
open(LOGS + "/pristine-3.txt", "w").write(out3 + err3)

json.dump(receipt, open(LOGS + "/receipt.json", "w"), indent=1)
print(json.dumps(receipt, indent=1))
