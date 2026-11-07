#!/usr/bin/env python3
"""Apply the frozen round-85 repair map to a SKILL.md copy: every backticked bare
token `key` becomes `value`. Usage: apply-map.py MAP IN OUT [--only N] [--swap KEY=VALUE]"""
import json, sys
a = sys.argv[1:]
m = json.load(open(a[0]))
only = None; swap = {}
for i, x in enumerate(a):
    if x == "--only": only = int(a[i + 1])
    if x == "--swap": k, v = a[i + 1].split("=", 1); swap[k] = v
keys = sorted(m)[:only] if only else sorted(m)
t = open(a[1], encoding="utf-8").read()
for k in keys:
    t = t.replace("`%s`" % k, "`%s`" % swap.get(k, m[k]))
open(a[2], "w", encoding="utf-8").write(t)
