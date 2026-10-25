#!/usr/bin/env python3
"""ExecHarnessC2 scratch probe: which Q9 conjuncts does source-recheck.py itself enforce?

Read-only against the lane: every fixture is written under this scratch directory and
the instrument is invoked by absolute path. Measures five limbs so the round-28 C2
receipt can say whether the exit code alone proves Q9, or whether the L1 must read the
printed occurrence/anchor notes.

Run: python3 .ufo/waves/round-28/wave1/ExecHarnessC2/probe_q9_discrimination.py
Exit: 0 always (it is a measurement, not a gate).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parents[4]
INSTRUMENT = LANE / "corpus/instruments/source-recheck.py"

CAPTURE = HERE / "capture-S042.txt"
CAPTURE.write_text(
    "line1 header for probe capture\n"
    "line2 the alpha bravo probe sentence appears exactly here\n"
    "line3 filler\n"
    "line4 the alpha bravo probe sentence appears exactly here\n"
    "line5 tail\n",
    encoding="utf-8",
)
import hashlib

SHA = hashlib.sha256(CAPTURE.read_bytes()).hexdigest()
UNIQUE = "line1 header for probe capture"
TWICE = "the alpha bravo probe sentence appears exactly here"
SHORT = "ab"


def manifest(name, record):
    path = HERE / name
    path.write_text(json.dumps({"schema_version": 1, "sources": [record]}, indent=1), encoding="utf-8")
    return path


def run(mp, source="S042"):
    proc = subprocess.run(
        [sys.executable, str(INSTRUMENT), "--manifest", str(mp), "--source", source],
        capture_output=True, text=True, cwd=str(LANE),
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


cases = []

# P1: path stem != id (Q9 conjunct 1)
p1 = manifest("m1-stem.json", {"id": "S042", "path": "capture-S041.txt", "sha256": SHA,
                               "quotes": [{"id": "Q1", "quote": UNIQUE}]})
(HERE / "capture-S041.txt").write_bytes(CAPTURE.read_bytes())
cases.append(("P1 path-stem-mismatch id=S042 path=capture-S041.txt (Q9 c1)", *run(p1)))

# P2: quote occurs twice, no anchor declared (Q9 conjunct 2)
p2 = manifest("m2-unanchored-dupe.json", {"id": "S042", "path": "capture-S042.txt", "sha256": SHA,
                                          "quotes": [{"id": "Q1", "quote": TWICE}]})
cases.append(("P2 duplicate quote, no anchor (Q9 c2)", *run(p2)))

# P3: declared anchor does not hold the quote (kill-rule 'anchor-broken')
p3 = manifest("m3-broken-anchor.json", {"id": "S042", "path": "capture-S042.txt", "sha256": SHA,
                                        "quotes": [{"id": "Q1", "quote": UNIQUE, "anchor": 4}]})
cases.append(("P3 anchor=4 does not hold a line-1 quote", *run(p3)))

# P4: quote too short after normalization (r24 forge route; expected guarded)
p4 = manifest("m4-short-quote.json", {"id": "S042", "path": "capture-S042.txt", "sha256": SHA,
                                      "quotes": [{"id": "Q1", "quote": SHORT}]})
cases.append(("P4 sub-12-char quote (control)", *run(p4)))

# P5: capture outside the manifest directory (expected guarded). The manifest lives in a
# subdirectory so the escaped path still resolves to real bytes; a non-existent escape
# would hit reason=missing first and would not exercise the containment branch.
SUB = HERE / "sub"
SUB.mkdir(exist_ok=True)
p5 = manifest("sub/m5-outside.json", {"id": "S042", "path": "../capture-S042.txt", "sha256": SHA,
                                      "quotes": [{"id": "Q1", "quote": UNIQUE}]})
cases.append(("P5 path escapes manifest dir (control)", *run(p5)))

for label, code, out, err in cases:
    print(f"--- {label}")
    print(f"exit={code}")
    for line in out.splitlines():
        print(f"  {line}")
    if err:
        for line in err.splitlines()[-3:]:
            print(f"  stderr: {line}")
