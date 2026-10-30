#!/usr/bin/env python3
"""Exercise frozen shonen-form CLI against persisted cases, exits and finding IDs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

EXPECTED = {
    'canonical': 'SF-CLEAN', 'actual-r47-drift': 'SF-PREAMBLE',
    'missing-file': 'SF-NEWLINE', 'fenced': 'SF-PREAMBLE',
    'commented': 'SF-PREAMBLE', 'duplicate': 'SF-TRAILING',
    'extra-prose': 'SF-TRAILING', 'crlf': 'SF-NEWLINE',
    'no-newline': 'SF-NEWLINE',
    **{f'wrong-label-{i}': 'SF-BOX' for i in range(4)},
    **{f'missing-evidence-{i}': 'SF-EVIDENCE' for i in range(4)},
}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    args = ap.parse_args()
    fixture = args.root / '.ufo/waves/round-48/controls/fixtures.json'
    if hashlib.sha256(fixture.read_bytes()).hexdigest() != '10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288':
        print('selftest finding=SF-SNAPSHOT-TAMPERED exit=2')
        return 2
    cases = json.loads(fixture.read_text())
    if len(cases) != len(EXPECTED) or {c['name'] for c in cases} != set(EXPECTED):
        print('selftest finding=SF-CASESET failures=1')
        return 1
    args.work.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='shonen-selftest-', dir=args.work))
    failures = 0
    try:
        # Harmless evidence target is isolated, never a write to the live lane.
        (scratch / 'LOG.md').write_text('isolated evidence fixture\n')
        for case in cases:
            path = scratch / 'candidate.md'
            path.write_bytes(case['text'].encode('utf-8'))
            p = subprocess.run([sys.executable, str(args.root / 'corpus/instruments/shonen-form.py'),
                                '--root', str(scratch), '--file', str(path)],
                               capture_output=True, text=True)
            want = f"shonen-form canonical={int(case['exit'] == 0)} finding={EXPECTED[case['name']]} exit={case['exit']}"
            ok = p.returncode == case['exit'] and p.stdout.strip() == want and not p.stderr
            failures += not ok
            print(f"case={case['name']} ok={int(ok)} rc={p.returncode} want={EXPECTED[case['name']]} observed={p.stdout.strip()}")
    finally:
        shutil.rmtree(scratch)
    print(f'selftest cases={len(cases)} failures={failures}')
    return int(failures != 0)

if __name__ == '__main__':
    raise SystemExit(main())
