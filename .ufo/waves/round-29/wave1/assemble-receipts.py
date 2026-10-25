#!/usr/bin/env python3
"""Assemble the round-29 wave-1 seat receipt rollup.

Reads swarm-registry.json (seat -> role, registry order), scans wave1/ for each
seat's report file <Seat>.md, copies every non-empty report into receipts/ as a
flat, numbered copy (NN_<Seat>.txt, NN = registry order), and writes
receipt-index.txt with seat | role | file | status (ok / missing / empty).

Idempotent: numbered copies are refreshed from the source report when the
source changed; seat-authored unnumbered files in receipts/ are left alone.

Run from the lane root:
    python3 .ufo/waves/round-29/wave1/assemble-receipts.py
"""
import datetime
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
WAVE = os.path.join(LANE, ".ufo/waves/round-29/wave1")
REGISTRY = os.path.join(WAVE, "swarm-registry.json")
RECEIPTS = os.path.join(WAVE, "receipts")
INDEX = os.path.join(WAVE, "receipt-index.txt")
RUN_ERR = os.path.join(LANE, ".ufo/waves/round-29/wave1-run.err")


def main() -> int:
    with open(REGISTRY, encoding="utf-8") as fh:
        reg = json.load(fh)["members"]

    os.makedirs(RECEIPTS, exist_ok=True)

    lines: list[str] = []
    ok = empty = missing = 0
    empty_seats: list[str] = []
    missing_seats: list[str] = []

    lines.append("# round-29 wave-1 receipt index")
    lines.append(
        f"# generated at: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
    )
    lines.append(f"# source registry: {os.path.relpath(REGISTRY, LANE)}")
    lines.append("# seat | role | file | status (ok / missing / empty)")
    lines.append("")

    for n, (seat, meta) in enumerate(reg.items(), start=1):
        role = meta.get("role", "?")
        report = os.path.join(WAVE, f"{seat}.md")
        rel = f"{seat}.md"
        if not os.path.exists(report):
            status = "missing"
            missing += 1
            missing_seats.append(seat)
        elif os.path.getsize(report) == 0:
            status = "empty"
            empty += 1
            empty_seats.append(seat)
        else:
            status = "ok"
            ok += 1
            target = os.path.join(RECEIPTS, f"{n:02d}_{seat}.txt")
            shutil.copyfile(report, target)
        lines.append(f"{seat} | {role} | {rel} | {status}")

    lines.append("")
    lines.append(
        f"## counts: ok={ok} empty={empty} missing={missing} total={ok + empty + missing}"
    )
    if empty_seats:
        lines.append(f"## empty seats: {', '.join(empty_seats)}")
    if missing_seats:
        lines.append(f"## missing seats: {', '.join(missing_seats)}")

    # Visible harness error text, if any (wave1-run.err).
    if os.path.exists(RUN_ERR) and os.path.getsize(RUN_ERR) > 0:
        lines.append("")
        lines.append("## wave1-run.err (non-empty)")
        with open(RUN_ERR, encoding="utf-8", errors="replace") as fh:
            lines.extend(fh.read().splitlines())

    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"receipts: ok={ok} empty={empty} missing={missing} total={ok + empty + missing}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
