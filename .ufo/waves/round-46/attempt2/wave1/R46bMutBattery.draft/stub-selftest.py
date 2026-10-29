#!/usr/bin/env python3
"""Stub round-46 counter selftest — HARNESS ONLY (not a committed instrument).

Replays the FROZEN per-mutant failure counts (controls/mutbat-before.txt) keyed by the
sha256 of the counter file under test, so the battery runner's own grading / printing /
exit logic can be exercised in seconds instead of hours.  Stdlib only.

The table is filled in by the harness (placeholder __TABLE__).  Prints exactly one
`failures=<N>` token, last, exactly as the real selftest does.
"""
import argparse
import hashlib
import json
import os
import sys

TABLE = json.loads(r"""__TABLE__""")

ap = argparse.ArgumentParser()
ap.add_argument("--lane")
ap.add_argument("--pure")
ap.add_argument("--counter")
ap.add_argument("--work")
ap.add_argument("--jobs")
ap.add_argument("--keep", action="store_true")
ap.add_argument("--do-nothing-control", action="store_true")
ap.add_argument("-v", action="store_true")
a, _unknown = ap.parse_known_args()

which = "c2" if os.path.basename(sys.argv[0]).endswith("c2.py") else "c1"
gate = "r46-c2-gate.py" if which == "c2" else "r46-c1-gate.py"
path = a.counter or os.path.join(os.getcwd(), "corpus", "instruments", gate)
data = open(path, "rb").read()
h = hashlib.sha256(data).hexdigest()
fails = TABLE.get(h)
if fails is None:
    fails = 1  # unknown (mutated) counter bytes: assume the selftest rejects it
print("case stub-" + which + " sha=" + h[:12] + " verdict=" + ("OK" if fails == 0 else "UNEXPECTED"))
print("selftest cases=1 failures=" + str(fails))
sys.exit(0 if fails == 0 else 1)
