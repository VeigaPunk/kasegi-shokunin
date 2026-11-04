#!/usr/bin/env python3
"""Public-CLI compound/operator cases; each native pipeline replay is independent.

The gate is not a shell pipeline-status emulator: native_groups below only show
each group's process statuses, not whether the gate should continue past &&.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()
    own = Path(__file__).parent
    h = runpy.run_path(str(own / "probe.py"))
    fixtures = h["fixtures"]()
    sig = "derive-upstream-signal-13"
    multi = [["cat", "big.txt", "missing.txt"], ["head", "-n", "1"]]
    single = [["cat", "big.txt"], ["head", "-n", "1"]]
    tail = [["cat", "g.txt"]]
    table = [
        ("and-first-multi", "cat big.txt missing.txt|head -n 1&&cat g.txt", "alpha\n35", 1, sig, [multi, tail]),
        ("and-second-multi", "cat g.txt&&cat big.txt missing.txt|head -n 1", "35\nalpha", 1, sig, [tail, multi]),
        ("and-single-positive", "cat big.txt|head -n 1&&cat g.txt", "alpha\n35", 0, None, [single, tail]),
        ("middle-multi", "head -n 1 small.txt|cat big.txt missing.txt|head -n 1", "alpha", 1, sig,
         [[["head", "-n", "1", "small.txt"], ["cat", "big.txt", "missing.txt"], ["head", "-n", "1"]]]),
        ("middle-stdin-positive", "cat big.txt|cat|head -n 1", "alpha", 0, None,
         [[["cat", "big.txt"], ["cat"], ["head", "-n", "1"]]]),
    ]
    gate = Path(args.instrument).resolve()
    rows = []
    for name, derive, want, expected, reason, groups in table:
        case = {"name": name, "derive": derive, "want": want, "expected_rc": expected,
                "reason": reason, "stages": groups[0], "input": None,
                "native_scope": "first pipeline only; independent group statuses additionally below"}
        row = h["check"](gate, case)
        row["native_groups"] = [h["native"](stages) for stages in groups]
        rows.append(row)
    document = {"base": h["BASE"], "instrument": str(gate),
                "instrument_sha256": hashlib.sha256(gate.read_bytes()).hexdigest(),
                "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "fixture_manifest": fixtures, "runs": rows}
    h["save"](args.label, document)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
