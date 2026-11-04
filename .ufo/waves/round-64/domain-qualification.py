#!/usr/bin/env python3
"""Documentation-only review of S094's disclosed SQLite finding; not a reproducer.
Exit0 expected source-grounded qualifications match, 1 mismatch, 2 unreadable source.
"""
from pathlib import Path
import datetime
import hashlib
import sys

source = Path(__file__).resolve().parents[3] / 'corpus/source-snapshots/round-61/S094.txt'
try:
    data = source.read_bytes()
    lines = data.decode().splitlines()
except (OSError, UnicodeError) as exc:
    print('QUALIFICATION unavailable=' + type(exc).__name__)
    sys.exit(2)
print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat())
print('source=S094 sha256=' + hashlib.sha256(data).hexdigest())
checks = [
    ('release-exposure', 18, 'before it appeared in an official release, so SQLite users were not impacted.'),
    ('sentinel-field', 29, 'int iColumn; /* Column constrained. -1 for ROWID */'),
    ('assertion-observed', 106, "Assertion `iCol>=0 && iCol<=2' failed."),
    ('negative-index', 110, 'iCol being calculated as -2'),
    ('fuzzer-configuration', 112, "isn't built with the generate_series extension enabled"),
    ('cpu-hours-not-walltime', 113, '150 CPU-hours'),
    ('comparison-limit', 118, 'highly experimental results'),
]
failures = 0
for key, line, phrase in checks:
    ok = phrase in lines[line - 1]
    failures += not ok
    print(f'QUALIFY id={key} anchor=S094.txt:{line} verdict={"PASS" if ok else "FAIL"}')
# Read the disclosed arithmetic as an explanation, not as target execution.
for column, expected in [(-1, False), (1, True), (2, True), (3, True)]:
    index = column - 1
    observed = 0 <= index <= 2
    good = observed == expected
    failures += not good
    print(f'ARITHMETIC column={column} index={index} in-asserted-range={observed} expected={expected} verdict={"PASS" if good else "FAIL"}')
print('DISPOSITION documentation-only; no released-user impact, bounty eligibility, reproduction or submission inferred')
print(f'QUALIFICATION checks={len(checks)+4} failures={failures}')
sys.exit(int(bool(failures)))
