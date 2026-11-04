#!/usr/bin/env python3
"""ADVERSARIAL MUTANT: prints expected values; never executes any derive.

Its cat rule is decoded-argv arity ONLY, not actual wait status. It should pass
an unpaired P1-P6 collector and fail the identical-command small-input twin.
ORACLE_ALWAYS_GREEN=1 removes even the hardcoded refusals for a negative control.
This is evidence of a collector blind spot, never a production proposal.
"""
import argparse
import json
import os
from pathlib import Path
import shlex


def refusal(text):
    if os.environ.get("ORACLE_ALWAYS_GREEN") == "1":
        return None
    lexer = shlex.shlex(text, posix=True, punctuation_chars="|&<")
    lexer.whitespace_split = True
    words = list(lexer)
    producer = words[:words.index("|")] if "|" in words else words
    if producer and producer[0] == "cat":
        if "<" in producer:
            index = producer.index("<")
            del producer[index:index + 2]
        operands = producer[1:]
        if operands and operands[0] == "--":
            operands = operands[1:]
        if len(operands) > 1:
            return "derive-upstream-signal-13"
        if operands == ["missing.txt"]:
            return "derive-upstream-exit-1"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--root")
    args = ap.parse_args()
    figures = json.loads(Path(args.ledger).read_text())["figures"]
    stale = 0
    for figure in figures:
        reason = refusal(figure["derive"])
        if reason:
            stale += 1
            print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" %
                  (figure["id"], figure["recorded"], reason))
        else:
            print("FIG %s recorded=%s derived=%s ok" %
                  (figure["id"], figure["recorded"], figure["want"]))
    code = int(stale > 0)
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" %
          (len(figures), len(figures) - stale, stale, code))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
