#!/usr/bin/env python3
"""ExecHarnessC2 scratch Q9 gate: asserts what source-recheck.py's exit code does not.

Measured on the landed instrument (probe_q9_discrimination.py, 2026-10-25):
source-recheck.py exits 0 for a record whose path stem differs from its id (P1), for a
quote occurring twice with no anchor (P2, prints `anchor=MISSING`), and for an anchor
that does not hold the quote (P3, prints `anchor=4-BROKEN`). The round-28 C2 kill rule
names exactly those states, so the exit code alone is not the counter: this wrapper
re-reads the manifest and the printed notes.

Usage:
  python3 .ufo/waves/round-28/wave1/ExecHarnessC2/check_q9.py <manifest> <id> [<id> ...]

Exit 0 = every Q9 conjunct holds for every named id and source-recheck exited 0.
Exit 1 = a conjunct failed; 2 = harness/manifest read error.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parents[5]
INSTRUMENT = LANE / "corpus/instruments/source-recheck.py"
NOTE = re.compile(r"^(\S+?):(\S+) (OK|MISMATCH|UNAVAILABLE)\b(.*)$")


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    manifest = Path(argv[1])
    if not manifest.is_absolute():
        manifest = (Path.cwd() / manifest).resolve()
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        records = {r["id"]: r for r in data["sources"]}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"HARNESS manifest-unreadable: {exc}")
        return 2

    failures = 0
    for source_id in argv[2:]:
        proc = subprocess.run(
            [sys.executable, str(INSTRUMENT), "--manifest", str(manifest), "--source", source_id],
            capture_output=True, text=True, cwd=str(LANE),
        )
        record = records.get(source_id)
        if record is None:
            print(f"FAIL {source_id}:not-in-manifest")
            failures += 1
            continue
        stem = Path(record.get("path", "")).stem
        stem_ok = stem == source_id
        notes = []
        for line in proc.stdout.splitlines():
            match = NOTE.match(line)
            if match:
                notes.append((match.group(2), match.group(4)))
        bad_anchor = [f"{qid}:{detail.strip()}" for qid, detail in notes
                      if "anchor=" in detail and "-ok" not in detail]
        ok = proc.returncode == 0 and stem_ok and not bad_anchor and bool(notes)
        print(f"{'PASS' if ok else 'FAIL'} {source_id} exit={proc.returncode} "
              f"path_stem={stem} stem_matches_id={'yes' if stem_ok else 'no'} "
              f"assertions={len(notes)} anchor_defects={len(bad_anchor)}")
        if not stem_ok:
            print(f"  Q9-c1 path stem '{stem}' != id '{source_id}'")
        for defect in bad_anchor:
            print(f"  Q9-c2 non-exactly-once without a holding anchor: {defect}")
        if proc.returncode != 0:
            for line in proc.stdout.splitlines():
                if "MISMATCH" in line or "UNAVAILABLE" in line:
                    print(f"  instrument: {line}")
            if not notes:
                print(f"  instrument stderr: {proc.stderr.strip()[-300:]}")
        failures += 0 if ok else 1

    print(f"q9 ids={len(argv) - 2} failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
