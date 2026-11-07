#!/usr/bin/env python3
r"""Remediation candidates for the azure pattern, timed on 4 MiB adversarial input.

A: literal prefilter — drive rx.match from the offsets of b"sv=" / b"sig=" only,
   instead of letting search() attempt a match at every byte offset.
   Each literal is re-found only after the previous find consumed it, and a
   literal that has returned -1 is never re-found (a naive double-find is
   itself quadratic when one literal is absent — measured, hence this note).
B: atomic value class `(?>[^&\s"'<>\\]*)` — validation-equivalent, because the
   value class excludes every character that can begin _SEP, so the greedy run
   is already the only parse.

Usage: remeasure.py CASE   -> one JSON line
"""
import importlib.util
import json
import os
import re
import sys
import time

H = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "css", os.path.join(H, "inst", "capture-secret-scan.py"))
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)
import bench  # noqa: E402

az = dict(css.CLOUD_PATTERNS)["azure-sas-signature"]
_SEP = rb"(?:&amp;|&|\\u0026)"
_SIG = rb"sig=[A-Za-z0-9%+/]{40,}(?:=|%3D){0,2}"
_SV = rb"sv=\d{4}-\d{2}-\d{2}"
_P2 = rb"(?:" + _SEP + rb"[A-Za-z]{2,6}=(?>[^&\s\"'<>\\]*)){0,20}?"
azB = re.compile(rb"(?i)(?<![A-Za-z0-9_])(?:" + _SV + _P2 + _SEP + _SIG
                 + rb"|" + _SIG + _P2 + _SEP + _SV + rb")")


def pref_offsets(data, rx):
    """Match starts the prefilter would evaluate."""
    pos = 0
    i = data.find(b"sv=", 0)
    j = data.find(b"sig=", 0)
    while i >= 0 or j >= 0:
        if i < 0:
            o = j
        elif j < 0:
            o = i
        else:
            o = min(i, j)
        m = rx.match(data, o)
        yield o, m
        pos = o + 1
        if i == o:
            i = data.find(b"sv=", pos)
        if j == o:
            j = data.find(b"sig=", pos)


def pref_scan(data, rx):
    n = 0
    for _o, m in pref_offsets(data, rx):
        if m:
            n += 1
    return n


def tm(fn, reps=2):
    b = 9e9
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        b = min(b, time.perf_counter() - t0)
    return b


def main(argv):
    case = argv[0]
    n = int(argv[1]) if len(argv) > 1 else 4194304
    d = bench.build(case, n)
    rec = {"case": case, "bytes": len(d)}
    rec["landed_sec"] = round(tm(lambda: [0 for _ in az.finditer(d)]), 4)
    rec["prefilter_sec"] = round(tm(lambda: pref_scan(d, az)), 4)
    rec["atomic_sec"] = round(tm(lambda: [0 for _ in azB.finditer(d)]), 4)
    rec["prefilter_speedup"] = round(rec["landed_sec"] / max(rec["prefilter_sec"], 1e-9), 1)
    rec["atomic_speedup"] = round(rec["landed_sec"] / max(rec["atomic_sec"], 1e-9), 1)
    # equivalence: same match start offsets as finditer, on the same buffer
    a = [m.start() for m in az.finditer(d)][:50]
    b = [m.start() for m in azB.finditer(d)][:50]
    c = [o for o, m in pref_offsets(d, az) if m][:50]
    rec["atomic_equiv"] = (a == b)
    rec["prefilter_equiv"] = (a == c)
    print(json.dumps(rec, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
