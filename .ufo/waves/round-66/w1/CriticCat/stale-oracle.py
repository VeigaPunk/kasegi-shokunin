#!/usr/bin/env python3
"""ADVERSARIAL MUTANT: always reports upstream exit1, never executes derive."""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--root")
    args = ap.parse_args()
    figures = json.loads(Path(args.ledger).read_text())["figures"]
    for figure in figures:
        print("FIG %s recorded=%s derived=UNAVAILABLE reason=derive-upstream-exit-1 stale" %
              (figure["id"], figure["recorded"]))
    print("FIGURE-AUDIT figures=%d ok=0 stale=%d exit=1" % (len(figures), len(figures)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
