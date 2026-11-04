#!/usr/bin/env python3
"""ADVERSARIAL MUTANT: stable P-labels leaked through --root decide the answer.

Echoes fresh ledger ids/recorded values, but never executes derive or inspects
operand content/status. Counterexample to nonce-only collector hardening.
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--root", required=True)
    args = ap.parse_args()
    labels = Path(args.root).parts
    figures = json.loads(Path(args.ledger).read_text())["figures"]
    reason = None
    if any(part.startswith(("P1-", "P2-", "P8-")) for part in labels):
        reason = "derive-upstream-signal-13"
    elif any(part.startswith("P5-") for part in labels):
        reason = "derive-upstream-exit-1"
    for figure in figures:
        if reason:
            print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" %
                  (figure["id"], figure["recorded"], reason))
        else:
            print("FIG %s recorded=%s derived=%s ok" %
                  (figure["id"], figure["recorded"], figure["want"]))
    stale = len(figures) if reason else 0
    rc = int(stale > 0)
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" %
          (len(figures), len(figures) - stale, stale, rc))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
