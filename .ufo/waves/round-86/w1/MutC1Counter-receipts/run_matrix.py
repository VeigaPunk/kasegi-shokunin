#!/usr/bin/env python3
"""Run the r86 C1 control set against the pristine counter and every mutant.

usage: run_matrix.py [--controls a,b|all] [--counters pristine|all|<names>] [--report]

Results accumulate in $S/results.json (keyed control -> counter -> run record).
"""
import argparse
import concurrent.futures
import glob
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r86/MutC1Counter"
B = "d7296645c2cd9f631329fa8e2f38328a4c9c89a5"
RES = S + "/results.json"
CTL = json.load(open(S + "/controls.json"))
WORK = S + "/w"


def counters():
    out = [("pristine", S + "/knowledge-meter.orig.py")]
    for p in sorted(glob.glob(S + "/mutants/*.py")):
        out.append((os.path.basename(p)[:-3], p))
    return out


def run_one(ctl, counter_path):
    cmd = ["python3", "-B", counter_path, "--lane", ctl["tree"], "--base-rev", B,
           "--map", ctl["map"], "--target", ctl["target"], "--map-sha256", ctl["sha"],
           "--work", WORK]
    r = subprocess.run(cmd, capture_output=True, text=True)
    limbs = {}
    for line in r.stdout.splitlines():
        if line.startswith("LIMB "):
            f = line.split()
            limbs[f[1]] = f[2]
    result_line = any(l.startswith("KNOWLEDGE-METER-RESULT") for l in r.stdout.splitlines())
    present = (ctl["assert_stdout"] in r.stdout) if "assert_stdout" in ctl else None
    if present is not None:
        verdict = "pass" if present == ctl.get("expect_present", True) else "fail"
    else:
        verdict = "pass" if r.returncode == 0 else "fail"
    if ctl.get("assert_result") and not result_line:
        verdict = "assert-fail"
    rec = {"rc": r.returncode, "verdict": verdict,
           "limbs": limbs, "result_line": result_line, "assert_present": present,
           "stderr_tail": (r.stderr.strip().splitlines() or [""])[-1],
           "stdout": r.stdout}
    return rec


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", default="all")
    ap.add_argument("--counters", default="pristine")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args(argv)
    allc = CTL["controls"]
    selc = allc if a.controls == "all" else [c for c in allc if c["name"] in a.controls.split(",")]
    allk = counters()
    selk = allk if a.counters == "all" else [c for c in allk if c[0] in a.counters.split(",")]
    res = json.load(open(RES)) if os.path.exists(RES) else {}
    for ctl in selc:
        cell = res.setdefault(ctl["name"], {})
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_one, ctl, path): name for name, path in selk}
            out = {}
            for f in concurrent.futures.as_completed(futs):
                out[futs[f]] = f.result()
        for name, _ in selk:
            rec = out[name]
            cell[name] = rec
            flags = ",".join("%s:%s" % kv for kv in sorted(rec["limbs"].items()) if kv[1] == "FAIL")
            print("%-14s %-28s %-4s %-10s %s%s" % (
                ctl["name"], name, rec["rc"], rec["verdict"], flags,
                "" if rec["result_line"] else " NO-RESULT-LINE"))
    with open(RES, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    if a.report:
        report(res, allc, [k for k, _ in allk])
    return 0


def report(res, allc, allk):
    pristine = res[allc[0]["name"]]["pristine"]  # only a placeholder; use stored pristine cells
    prim = {c["name"]: res[c["name"]]["pristine"] for c in allc}
    print("\n== pristine control verdicts / isolated limbs ==")
    for c in allc:
        p = prim[c["name"]]
        fails = [k for k, v in sorted(p["limbs"].items()) if v == "FAIL"]
        if "assert_stdout" in c:
            print("%-18s %-4s assert=%r present=%s" % (
                c["name"], p["verdict"], c["assert_stdout"], p["assert_present"]))
        else:
            print("%-18s %-4s limbs=%s result_line=%s" % (
                c["name"], p["verdict"], ",".join(fails) or "none", p["result_line"]))
    print("\n== kill matrix (K=killed by, . = survived) ==")
    mutants = [k for k in allk if k != "pristine"]
    killed_by = {m: [] for m in mutants}
    survived = []
    for m in mutants:
        row = []
        for c in allc:
            p, q = prim[c["name"]], res[c["name"]][m]
            changed = p["verdict"] != q["verdict"] or p["result_line"] != q["result_line"]
            row.append(c["name"] if changed else "")
            if changed:
                killed_by[m].append(c["name"])
        if not killed_by[m]:
            survived.append(m)
        print("%-28s %s" % (m, " | ".join(x or "." for x in row)))
    print("\nkilled=%d survived=%d total=%d ratio=%.3f" % (
        len(mutants) - len(survived), len(survived), len(mutants),
        (len(mutants) - len(survived)) / len(mutants)))
    for m in mutants:
        print("%-28s %s" % (m, ",".join(killed_by[m]) or "SURVIVED"))
    return survived


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
