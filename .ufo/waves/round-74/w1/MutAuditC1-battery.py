#!/usr/bin/env python3
"""battery.py MUTDIR SCRATCH — run `--selftest` on every *.py in MUTDIR (plus the unmutated
counter passed as ORIG env var) with a private TMPDIR per run; print one row per run.

Verdict rule (claims.json C1 kill rule (a)): exit 0 from --selftest = SURVIVED; nonzero = KILLED.
"""
import glob
import os
import subprocess
import sys

mutdir, scratch = sys.argv[1], sys.argv[2]
orig = os.environ["ORIG"]
runs = [("ORIG", orig)] + [(os.path.basename(p)[:-3], p) for p in sorted(glob.glob(os.path.join(mutdir, "*.py")))]
tmproot = os.path.join(scratch, "tmp")
os.makedirs(tmproot, exist_ok=True)
for name, path in runs:
    tmp = os.path.join(tmproot, name)
    os.makedirs(tmp, exist_ok=True)
    before = set(glob.glob("/tmp/recheck-cwd-*"))
    p = subprocess.run([sys.executable, path, "--selftest"], cwd=scratch,
                       env={**os.environ, "TMPDIR": tmp},
                       capture_output=True, text=True, timeout=900)
    after = set(glob.glob("/tmp/recheck-cwd-*"))
    left_tmp = len(glob.glob(os.path.join(tmp, "recheck-cwd-*")))
    left_root = len(after - before)
    lines = (p.stdout + p.stderr).splitlines()
    last = lines[-1] if lines else "<no output>"
    caseline = [l for l in lines if "selftest case=" in l and " FAIL" in l]
    verdict = "SURVIVED" if p.returncode == 0 else "KILLED"
    if name == "ORIG":
        verdict = "baseline(rc=%d)" % p.returncode
    print("ROW name=%s rc=%d verdict=%s last=%r leftover_tmp=%d leftover_slashtmp_new=%d"
          % (name, p.returncode, verdict, last, left_tmp, left_root))
    for l in caseline:
        print("   FAILCASE %s" % l)
    for l in lines:
        if "Traceback" in l or "Error" in l:
            print("   ERRLINE %s" % l)
            break
    sys.stdout.flush()
