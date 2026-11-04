#!/usr/bin/env python3
"""ADVERSARIAL MUTANT: a no-work, public-probe-ID keyed oracle.

Never parses/executes derive, inspects operands, or waits for child statuses.
It illustrates the irreducible finite-collector limitation; digest/source-bound
full-driver protections must reject it. It is NOT an implementation candidate.
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--root")
    args = ap.parse_args()
    figures = json.loads(Path(args.ledger).read_text())["figures"]
    stale = 0
    for figure in figures:
        identity = figure["id"]
        reason = None
        if identity.startswith(("P1-", "P2-", "P8-")):
            reason = "derive-upstream-signal-13"
        elif identity.startswith("P5-"):
            reason = "derive-upstream-exit-1"
        if reason:
            stale += 1
            print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" %
                  (identity, figure["recorded"], reason))
        else:
            print("FIG %s recorded=%s derived=%s ok" %
                  (identity, figure["recorded"], figure["want"]))
    rc = int(stale > 0)
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" %
          (len(figures), len(figures) - stale, stale, rc))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
