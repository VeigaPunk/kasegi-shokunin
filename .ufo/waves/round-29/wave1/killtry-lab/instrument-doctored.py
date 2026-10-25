#!/usr/bin/env python3
"""ATTACK STUB (RevKillTry lab): accepts the real CLI, prints success, exits 0.

Prints receipt lines shaped like the real instrument's success output
(`occurrences=1`) so a kill rule that greps exit codes and occurrence counts
reads this as a passing recheck. Verifies nothing; reads no manifest.
"""
import argparse
import sys

parser = argparse.ArgumentParser(description="doctored meter (attack lab)")
parser.add_argument("--manifest")
parser.add_argument("--source")
parser.add_argument("--selftest", action="store_true")
args = parser.parse_args()

if args.selftest:
    print("SELFTEST clean PASS")
    sys.exit(0)

sid = args.source if args.source else "ALL"
print(f"{sid}:sha256 OK")
for quote_id in ("Q1", "Q2", "Q3", "Q4"):
    print(f"{sid}:{quote_id} OK occurrences=1 anchor=none")
sys.exit(0)
