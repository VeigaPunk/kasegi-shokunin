#!/usr/bin/env python3
"""Replay the independent seat attack suite on the prefreeze collector repair.
Fixture filename contains grep; independent oracle compares derived output with want,
not the informational recorded field. Original attack script stays unchanged.
"""
import importlib.util
from pathlib import Path
import shutil
import sys

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_attack', here / 'w1/MutationCollector/attack-r64-v2.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.SCRATCH = Path('/fast/scratch/hyaku/kasegi-r64/L1/counterattack')
if m.SCRATCH.exists() or Path(m.UNOWNED).exists():
    raise SystemExit('refusing-preexisting-attack-scratch')

def rename(value):
    if isinstance(value, tuple):
        return tuple(rename(item) for item in value)
    return 'grep-missing-r64.txt' if value == 'nosuch-r64.txt' else value

m.MISS = 'grep-missing-r64.txt'
m.MY_PROBES = rename(m.MY_PROBES)
old = "if reason is None and out == recorded.replace('\\\\n', '\\n'):"
if m.ORACLE_SRC.count(old) != 1:
    raise SystemExit('oracle-want-anchor-not-unique')
m.ORACLE_SRC = m.ORACLE_SRC.replace(old, "if reason is None and out == str(figure['want']):")
try:
    raise SystemExit(m.main())
finally:
    shutil.rmtree(m.SCRATCH, ignore_errors=True)
