#!/usr/bin/env python3
"""Summarize one control-harness log: control verdicts, failing limbs, mutant verdict."""
import json
import sys

log = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
ctrl = []
last_result = None
for ln in log:
    if ln.startswith("CONTROL "):
        parts = ln.split()
        ctrl.append({"name": parts[1], "rc": parts[2], "want": parts[3],
                     "verdict": "PASS" if " PASS" in ln else "FAIL",
                     "raw": ln})
    elif ln.startswith("C1-CONTROLS-RESULT"):
        last_result = ln
fails = [c for c in ctrl if c["verdict"] == "FAIL"]
print(json.dumps({"controls": len(ctrl), "fail": [c["name"] for c in fails],
                  "result": last_result,
                  "killed": bool(fails)}, indent=1))
