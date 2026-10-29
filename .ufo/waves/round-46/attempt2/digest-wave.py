#!/usr/bin/env python3
"""Digest the settled wave reports for L1 integration: VERDICT line + per-seat one-liners.
Usage: digest-wave1.py [--dir .ufo/waves/round-46/attempt2/wave1]"""
import argparse, glob, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1")
a = ap.parse_args()
files = sorted(glob.glob(os.path.join(a.dir, "*.md")))
print("reports=%d" % len(files))
for f in files:
    t = open(f, encoding="utf-8", errors="replace").read()
    first = t.strip().splitlines()[0] if t.strip() else "(empty)"
    words = len(t.split())
    print("%-28s %6dw  %s" % (os.path.basename(f)[:28], words, first[:110]))
