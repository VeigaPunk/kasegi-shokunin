#!/usr/bin/env python3
"""Apply table rows G1..G4 to scratch copies of the frozen r83 candidate and run --selftest."""
import json, os, subprocess, sys, importlib.util, shutil

S = "/fast/scratch/hyaku/kasegi-r83/ReviewC1"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CAND = os.path.join(LANE, ".ufo/waves/round-83/c1/recheck-cwd-census.py")
MUTBAT = os.path.join(LANE, ".ufo/waves/round-83/c1/mutbat.py")
TABLE = os.path.join(LANE, ".ufo/waves/round-83/c1/mutant-table.json")

spec = importlib.util.spec_from_file_location("mutbat_r83", MUTBAT)
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

rows = json.load(open(TABLE))
by_id = {r["id"]: r for r in rows}
src = open(CAND, encoding="utf-8").read()

print("pristine candidate sha256", __import__("hashlib").sha256(src.encode()).hexdigest())
for rid in ("G1", "G2", "G3", "G4"):
    row = by_id[rid]
    mutant = mb.apply_row(src, row)
    status = "derived" if mutant is not None else "NOT-DERIVED"
    print("== row %s: %s" % (rid, status))
    if mutant is None:
        continue
    w = os.path.join(S, "w_" + rid)
    os.makedirs(w, exist_ok=True)
    mpath = os.path.join(w, "recheck-cwd-census.py")
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(mutant)
    env = dict(os.environ, TMPDIR=w)
    p = subprocess.run([sys.executable, "-B", mpath, "--selftest"],
                       capture_output=True, text=True, env=env, timeout=600, cwd=w)
    fails = [ln for ln in p.stdout.splitlines() if ln.startswith("FAIL ")]
    summary = [ln for ln in p.stdout.splitlines() if ln.startswith("selftest cases=")]
    print("rc=%d" % p.returncode)
    print("\n".join(summary))
    print("\n".join(fails))
    if p.stderr.strip():
        print("stderr:", p.stderr.strip()[:500])
    shutil.rmtree(w, ignore_errors=True)
