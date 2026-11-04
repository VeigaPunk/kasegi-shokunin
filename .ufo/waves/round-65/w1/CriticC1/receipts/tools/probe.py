#!/usr/bin/env python3
"""Run the REAL figure-audit instrument on one (derive, want) pair in a fixture root.

Usage: probe.py --instrument PATH --derive STR --want STR [--id NAME]
Prints: PROBE id=... exit=N audit=... reason=...
Never writes outside this script's work/ directory.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "work", "root")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--derive", required=True)
    ap.add_argument("--want", required=True)
    ap.add_argument("--id", default="c")
    a = ap.parse_args()
    lp = os.path.join(HERE, "work", "ledger-%s.json" % a.id)
    doc = {"figures": [{
        "id": a.id,
        "record": "g.txt:1",
        "recorded": a.want,
        "derive": a.derive,
        "want": a.want,
    }]}
    with open(lp, "w", encoding="utf-8") as f:
        json.dump(doc, f)
        f.write("\n")
    p = subprocess.run([sys.executable, "-B", a.instrument, "--ledger", lp, "--root", ROOT],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    line = ""
    for ln in out.splitlines():
        if ln.startswith("FIG "):
            line = ln
    reason = "-"
    if "reason=" in line:
        reason = line.split("reason=", 1)[1].split()[0]
    print("PROBE id=%s exit=%d reason=%s" % (a.id, p.returncode, reason))
    print("AUDIT %s" % line)
    if err.strip():
        print("STDERR %s" % err.strip().replace("\n", " | "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
