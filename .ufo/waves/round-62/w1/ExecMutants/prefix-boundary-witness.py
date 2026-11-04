#!/usr/bin/env python3
"""Prove the two r61 surviving edits are non-equivalent; no derives execute.

Usage: python3 prefix-boundary-witness.py /absolute/figure-audit.py /owned/scratch
The scratch directory must exist; this script creates no files.
"""
import hashlib
import runpy
import sys
from pathlib import Path

instrument = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve(strict=True)
battery = runpy.run_path(str(Path(__file__).with_name("figure-audit-mutbat.py")))
source = instrument.read_text(encoding="utf-8")
for name, old, new in [("pristine", "", "")] + battery["MUTANTS"][-2:]:
    if name == "pristine":
        text = source
    else:
        sites = source.count(old)
        if sites != 1:
            raise RuntimeError("%s exact-once sites=%d" % (name, sites))
        text = source.replace(old, new, 1)
    namespace = {"__name__": "witness_instrument", "__file__": str(instrument)}
    exec(compile(text, str(instrument), "exec"), namespace)
    gate = namespace["python_head_ok"]
    heads = [
        ("absolute-inside", "python3 " + str(root / "corpus/instruments/ok.py")),
        ("sibling-prefix", "python3 corpus/instruments/../instruments-evil/out.py"),
        ("same-directory", "python3 corpus/instruments/"),
    ]
    print("variant=%s sha256=%s" % (name, hashlib.sha256(text.encode()).hexdigest()))
    for label, head in heads:
        admitted = gate(str(root), head)
        expected = ((name == "m8-python-prefix-off" and label == "absolute-inside") or
                    (name == "m9-python-boundary-separator-off" and label == "sibling-prefix"))
        print("witness=%s admitted=%s expected=%s" % (label, admitted, expected))
        if admitted != expected:
            raise RuntimeError("unexpected gate result")
