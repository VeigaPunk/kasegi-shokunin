#!/usr/bin/env python3
"""Mode-sniffing counterfeit instrument: implements NO audit at all.

It reads its own --root path, which the collector derives from --work, and
prints the verdict shape the caller's expectation model wants:

  root containing "collector-base" or "forgeries" -> base-gate shape
      (P1/P2 ok, P3 stale derive-exit--15, P4..P6 ok)
  anything else (collector-candidate, selfcheck and both modes) -> candidate shape
      (P1 stale upstream-signal-15, P2 stale upstream-signal-9,
       P3 stale derive-signal-15, P4..P6 ok)

It never executes the derive.
"""
import argparse
import json
import sys

BASE_SHAPE = {
    "P1": "FIG P1 recorded={r} derived={w} ok\n",
    "P2": "FIG P2 recorded={r} derived={w} ok\n",
    "P3": "FIG P3 recorded={r} derived=UNAVAILABLE reason=derive-exit--15 stale\n",
    "P4": "FIG P4 recorded={r} derived={w} ok\n",
    "P5": "FIG P5 recorded={r} derived={w} ok\n",
    "P6": "FIG P6 recorded={r} derived={w} ok\n",
}
CAND_SHAPE = {
    "P1": "FIG P1 recorded={r} derived=UNAVAILABLE reason=derive-upstream-signal-15 stale\n",
    "P2": "FIG P2 recorded={r} derived=UNAVAILABLE reason=derive-upstream-signal-9 stale\n",
    "P3": "FIG P3 recorded={r} derived=UNAVAILABLE reason=derive-signal-15 stale\n",
    "P4": "FIG P4 recorded={r} derived={w} ok\n",
    "P5": "FIG P5 recorded={r} derived={w} ok\n",
    "P6": "FIG P6 recorded={r} derived={w} ok\n",
}

ap = argparse.ArgumentParser()
ap.add_argument("--ledger", required=True)
ap.add_argument("--root", required=True)
args = ap.parse_args()
with open(args.ledger) as handle:
    figs = json.load(handle)["figures"]
base = ("probes-base" in args.root) or ("collector-base" in args.root) or ("forgeries" in args.root)
green = "selfcheck" in args.root
shape = BASE_SHAPE if base else CAND_SHAPE
stale = 0
for fig in figs:
    if green:
        sys.stdout.write("FIG {id} recorded={r} derived={w} ok\n".format(
            id=fig["id"], r=fig["recorded"], w=fig["want"]))
    else:
        line = shape[fig["id"]].format(r=fig["recorded"], w=fig["want"])
        stale += line.rstrip().endswith(" stale")
        sys.stdout.write(line)
print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" % (
    len(figs), len(figs) - stale, stale, 1 if stale else 0))
sys.exit(1 if stale else 0)
