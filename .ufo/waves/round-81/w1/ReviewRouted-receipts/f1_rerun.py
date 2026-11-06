#!/usr/bin/env python3
"""ReviewRouted r81 — re-run forgery F1-location only, using the frozen driver's own forge()."""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r81/ReviewRouted"
WORK = os.path.join(S, "f1rerun")
ENV = dict(os.environ, TMPDIR=S)

shutil.rmtree(WORK, ignore_errors=True)
spec = importlib.util.spec_from_file_location(
    "fdriver", os.path.join(LANE, ".ufo/waves/round-81/controls/c1-forgeries-r81.py"))
drv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drv)

src = open(os.path.join(LANE, ".ufo/waves/round-81/c1/recheck-cwd-census.py"),
           encoding="utf-8").read()
table = json.load(open(os.path.join(LANE, ".ufo/waves/round-81/c1/mutant-table.json"),
                       encoding="utf-8"))
os.makedirs(WORK, exist_ok=True)
nonneutral = [r for r in table if r["class"] != "neutral"]
t56 = os.path.join(WORK, "table-r81-nonneutral.json")
with open(t56, "w", encoding="utf-8") as fh:
    json.dump(nonneutral, fh)
print("table rows total=%d nonneutral=%d" % (len(table), len(nonneutral)))

home = os.path.join(WORK, "F1-location", "corpus", "instruments")
os.makedirs(home)
target = os.path.join(home, "recheck-cwd-census.py")
with open(target, "w", encoding="utf-8") as fh:
    fh.write(drv.forge(src, "F1-location"))
open(os.path.join(home, "SIBLING.marker"), "w").close()
sha = hashlib.sha256(open(target, "rb").read()).hexdigest()
print("forgery_sha256=%s" % sha)
print("want        =bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6")

for counter, tbl in (("r80", t56),
                     ("r81", os.path.join(LANE, ".ufo/waves/round-81/c1/mutant-table.json"))):
    mb = os.path.join(LANE, ".ufo/waves/round-%s/c1/mutbat.py" % counter[1:])
    wd = os.path.join(WORK, "F1-location", "w-" + counter)
    os.makedirs(wd)
    p = subprocess.run([sys.executable, "-B", mb, "--target", target, "--table", tbl,
                        "--expect-cases", "22", "--work", wd],
                       capture_output=True, text=True, cwd=LANE, env=ENV)
    summary = [l for l in p.stdout.splitlines() if l.startswith("MUTBAT")]
    verdicts = {}
    for l in p.stdout.splitlines():
        m = drv.re.match(r"MUTANT \S+ verdict=(\S+)", l)
        if m:
            verdicts[m.group(1)] = verdicts.get(m.group(1), 0) + 1
    print("FORGERY F1-location counter=%s forgery_sha256=%s rc=%d verdicts=%s %s"
          % (counter, sha, p.returncode, json.dumps(verdicts, sort_keys=True),
             summary[-1] if summary else "NO-SUMMARY stderr=%r" % p.stderr[-200:]))
    with open(os.path.join(S, "f1-rerun-%s.txt" % counter), "w", encoding="utf-8") as fh:
        fh.write(p.stdout)
        fh.write("\n[stderr]\n%s\n[rc]\n%d\n" % (p.stderr, p.returncode))
