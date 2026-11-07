#!/usr/bin/env python3
"""Read-only probes of the frozen round-93 C2 counter's own nondeterminism.
Imports the counter as a module (never runs its main), so nothing is planted on
disk and the lane's git state is untouched.  Run with a lane clone present at
S/lane (at 9225954a); S is the seat scratch path used for this wave.
"""
import importlib.util
import os
import re

S = "/fast/scratch/hyaku/kasegi-r93/MutC2Counter"
CTR = os.path.join(S, "lane/.ufo/waves/round-93/c2/capability-check.py")
R = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-93/w1/MutC2Counter-receipts"

spec = importlib.util.spec_from_file_location("cap", CTR)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

nonce = "deadbeef"
print("P1 plants in K4: %d; reroot renames %d; unreached=%s"
      % (len(m.PLANTS), sum(m.reroot(p, nonce) != p for p in m.PLANTS),
         [p for p in m.PLANTS if nonce not in m.reroot(p, nonce)] or "none"))
base_same = [p for p in m.PLANTS if os.path.basename(m.reroot(p, nonce)) != os.path.basename(p)]
print("P2 basenames changed by reroot: %d %s" % (len(base_same), base_same or "-> stable"))
print("P3 sample reroot: %s -> %s" % ("w/t-receipts/live-k.json", m.reroot("w/t-receipts/live-k.json", nonce)))

g, exp = m.generated(1)
g2, exp2 = m.generated(9191)
print("P4 K7 plants: %d; paths containing a nonce: %d; paths fixed across seeds: %d"
      % (len(g), sum(nonce in p for p in g), sum(1 for p in g if p in g2)))
print("P5 K7 values seed-dependent: plants_equal=%s expect_equal=%s"
      % (g == g2, exp == exp2))
src = open(CTR, encoding="utf-8").read()
print("P6 mkdtemp prefixes: %s" % re.findall(r'mkdtemp\(prefix="([^"]+)"', src))
print("P7 fixed work children: %s" % re.findall(r'os\.path\.join\(work, "(inst|base-inst|plant-allow[^"]*)"\)', src))
print("P8 nonce source: %s" % re.findall(r"nonce = ([^\n]+)", src))
print("P9 seed source: %s" % re.findall(r"seed = ([^\n]+)", src))
print("P10 seed printed: header=%s K7det=%s"
      % ('seed=%d nonce=%s' in src, 'seed=%d rc=%d' in src))
for tag in ("BASELINE-candidate",):
    for seed in (1, 9191):
        for mode in ("pinned", "unpinned"):
            p = os.path.join(R, "%s-%s-seed%d.txt" % (tag, mode, seed))
            if not os.path.exists(p):
                continue
            txt = open(p, encoding="utf-8").read()
            hdr = re.search(r"seed=(\d+) nonce=([0-9a-f]+)", txt)
            hits = re.findall(r"HIT shape=(\S+) path=(\S+)", txt)
            print("P11 %s %s seed=%s printed_seed=%s nonce=%s hit_paths=%d"
                  % (tag, mode, seed, hdr.group(1) if hdr else None,
                     hdr.group(2) if hdr else None, len(hits)))
grouped = {}
for p in m.PLANTS:
    grouped.setdefault(os.path.dirname(p), []).append(p)
print("P12 K4 plant dirs (%d): %s" % (len(grouped), sorted(grouped)))
print("P13 K7 plant dirs: %s" % sorted({os.path.dirname(p) for p in g}))
