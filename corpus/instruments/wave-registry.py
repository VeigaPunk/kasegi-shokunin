#!/usr/bin/env python3
"""wave-registry.py — emit a wave registry whose `names=` field is populated.

WHY
    The round-43 wave evidence `.ufo/waves/round-43/w1-REGISTRY.txt` asserted
    `seats=73` while its `names=` field was empty, so the registry could not
    be checked against the seats that actually ran (routed defect 5 of
    `corpus/lessons/round-43-verifier-spotcheck.md` §6).  This emitter is the
    lane-owned replacement: it reads a wave results file and writes the seat
    names it holds, so `seats=` and `names=` are always consistent.

USAGE
    python3 corpus/instruments/wave-registry.py --results RESULTS.json --out PATH
    python3 corpus/instruments/wave-registry.py --results RESULTS.json --out PATH --lane kasegi

    --results  a wave results file (the one the orchestrator writes beside the
               dispatch file; `seats` and `results[].name` are read from it).
    --out      where to write the registry (parent dirs are created).
    --lane     lane name, recorded in the `lane=` field.

    The registry format is one `key=value` per line:

        wave=<name>
        lane=<lane>
        policy=<policy file>
        seats=<n>
        roles=<role>=<count>,…
        attack_seats=<n>
        names=<comma-separated seat names>

    Exit 0 only when the emitted `names=` list has exactly `seats=` entries —
    an empty names= field is a failure, never a silent pass.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lane", default="kasegi")
    ap.add_argument("--wave", default=None, help="wave name (default: derived from the results file)")
    ap.add_argument("--policy", default="ufo-wave-policy-v2.json (wave band 64-128, hard ceiling 256)",
                    help="the policy line recorded in the registry")
    args = ap.parse_args(argv)

    try:
        with open(args.results, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"wave-registry: cannot read {args.results}: {exc}", file=sys.stderr)
        return 2

    results = doc.get("results")
    if not isinstance(results, list) or not results:
        print(f"wave-registry: {args.results} carries no results list", file=sys.stderr)
        return 2

    names = []
    roles = []
    for entry in results:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        role = entry.get("agent") or entry.get("role") or "unknown"
        if not name:
            continue
        names.append(str(name))
        roles.append(str(role))

    seats = doc.get("seats")
    if not isinstance(seats, int):
        seats = len(names)
    if seats != len(names):
        print(f"wave-registry: seats={seats} but {len(names)} named seats — refusing to emit", file=sys.stderr)
        return 1

    attack_roles = {"reviewer", "critic", "mutation-tester", "security-reviewer"}
    attack = sum(1 for r in roles if r in attack_roles)
    counts = Counter(roles)
    wave = args.wave or os.path.basename(args.results).replace("-results.json", "")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    lines = [
        f"wave={wave}",
        f"lane={args.lane}",
        f"policy={args.policy}",
        f"seats={seats}",
        "roles=" + ",".join(f"{k}={v}" for k, v in sorted(counts.items())),
        f"attack_seats={attack} ({100.0 * attack / seats:.1f}%) = reviewer+critic+mutation-tester+security-reviewer",
        "names=" + ",".join(names),
        "",
    ]
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"wave-registry: wrote {args.out} seats={seats} names={len(names)} attack={attack}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
