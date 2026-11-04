#!/usr/bin/env python
"""Semantic emulator: answers the signal probes by command TEXT, not wait status.

It delegates every figure to the base gate and then rewrites the FIG line to the
C1-expected reason when the derive string looks like one of the known signal
pipelines.  It never inspects a returncode for the signal limb: that is the point.
A detector that only checks the five documented pipelines plus a clean control
accepts it.  A detector holding out the same command text with different runtime
behaviour must reject it.
"""

import json
import os
import re
import subprocess
import sys

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.py")


def canned(derive):
    """Return (reason, exit_hint) keyed purely on the derive text."""
    stages = [s.strip() for s in derive.split("|")]
    if not stages or not stages[0]:
        return None
    for i, st in enumerate(stages):
        last = i == len(stages) - 1
        if re.search(r"corpus/instruments/kill_after\.py\b", st):
            return "derive-signal-15", 1
        if re.search(r"corpus/instruments/kill9\.py\b", st):
            return ("derive-signal-9" if last else "derive-upstream-signal-9"), 1
        if re.search(r"corpus/instruments/kill\.py\b", st):
            return ("derive-signal-15" if last else "derive-upstream-signal-15"), 1
        if re.search(r"corpus/instruments/maybe_kill\.py\b", st):
            # text says "kill", so the emulator claims a signal no matter what ran
            return ("derive-signal-15" if last else "derive-upstream-signal-15"), 1
    return None


def main(argv):
    ledger = os.path.join("corpus", "instruments", "figure-audit-ledger.json")
    root = "."
    it = iter(argv)
    for a in it:
        if a == "--ledger":
            ledger = next(it)
        elif a == "--root":
            root = next(it)
    try:
        with open(ledger, "r", encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError):
        doc = {"figures": []}
    p = subprocess.run([sys.executable, BASE, "--ledger", ledger, "--root", root],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.decode("utf-8", "replace")
    patched, stale = [], 0
    figs = {f.get("id"): f for f in doc.get("figures", []) if isinstance(f, dict)}
    for line in out.splitlines():
        if line.startswith("FIG "):
            fid = line.split()[1]
            ent = figs.get(fid) or {}
            hit = canned(ent.get("derive", ""))
            if hit is not None:
                reason, _ = hit
                stale += 1
                line = "FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" % (
                    fid, ent.get("recorded", "?"), reason)
        elif line.startswith("FIGURE-AUDIT figures="):
            continue
        patched.append(line)
    code = 1 if stale else p.returncode
    if patched:
        print("\n".join(patched))
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" % (
        len(figs), max(0, len(figs) - stale), stale, code))
    sys.stderr.write(p.stderr.decode("utf-8", "replace"))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
