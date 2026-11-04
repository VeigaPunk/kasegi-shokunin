#!/usr/bin/env python3
"""Round-62 named probes, not a sandbox.

Usage: python3 c1-probe-run-r62.py INSTRUMENT SCRATCH --mode baseline|candidate
SCRATCH must be a disposable seat/subdirectory under /fast/scratch/hyaku/kasegi-r62.
Refuse an instrument inside SCRATCH BEFORE clearing it. Each probe gets a fresh
root. Derive strings enter JSON unchanged; the instrument owns their interpretation.
Baseline means round-62 base f7dcab84's instrument, NOT round-61's before tree.
Exit: 0 all tuples match; 1 tuple mismatch; 2 usage/dependency/fixture/collection error.
Only Python's stdlib plus bash, python3, cat, grep, wc are required. No find pipeline.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SCRATCH_BASE = Path('/fast/scratch/hyaku/kasegi-r62')
PROBES = (
    ('quoted-traversal', 'python3 corpus/instruments/"../../outside.py"', '35'),
    ('dot-prefix', 'python3 ./corpus/instruments/tiny-ok.py', '35'),
    ('normalized-sibling', 'python3 corpus/instruments/../instruments2/outside.py', '35'),
    ('inside', 'python3 corpus/instruments/tiny-ok.py', '35'),
    ('inside-normalized', 'python3 corpus/instruments/../instruments/tiny-ok.py', '35'),
    ('quoted-separator', "cat g.txt | grep -e '35' -e ';'", '35'),
    ('plain-count', 'cat g.txt | wc -l', '1'),
    ('traversal-2up', 'python3 corpus/instruments/../../outside.py', '35'),
    ('traversal-3up', 'python3 corpus/instruments/../../../outside.py', '35'),
    ('symlink-out', 'python3 corpus/instruments/link.py', '35'),
)
# Tuples: (instrument exit, regular MARK-* files, required diagnostic substring).
# Separate tables intentionally prevent a candidate failure from being called baseline success.
BASELINE = {
    'quoted-traversal': (0, 1, 'derived=35 ok'),
    'dot-prefix': (2, 0, 'reason=derive-not-read-only'),
    'normalized-sibling': (2, 0, 'reason=derive-not-read-only'),
    'inside': (0, 0, 'derived=35 ok'),
    'inside-normalized': (0, 0, 'derived=35 ok'),
    'quoted-separator': (0, 0, 'derived=35 ok'),
    'plain-count': (0, 0, 'derived=1 ok'),
    'traversal-2up': (2, 0, 'reason=derive-not-read-only'),
    'traversal-3up': (2, 0, 'reason=derive-not-read-only'),
    'symlink-out': (2, 0, 'reason=derive-not-read-only'),
}
CANDIDATE = {
    'quoted-traversal': (2, 0, 'reason=derive-not-read-only'),
    'dot-prefix': (2, 0, 'reason=derive-not-read-only'),
    'normalized-sibling': (2, 0, 'reason=derive-not-read-only'),
    'inside': (0, 0, 'derived=35 ok'),
    'inside-normalized': (0, 0, 'derived=35 ok'),
    'quoted-separator': (0, 0, 'derived=35 ok'),
    'plain-count': (0, 0, 'derived=1 ok'),
    'traversal-2up': (2, 0, 'reason=derive-not-read-only'),
    'traversal-3up': (2, 0, 'reason=derive-not-read-only'),
    'symlink-out': (2, 0, 'reason=derive-not-read-only'),
}


def collect_markers(root):
    """Any listing/stat failure propagates as a harness error, never a zero count."""
    with os.scandir(root) as entries:
        return sum(1 for entry in entries
                   if entry.name.startswith('MARK-') and entry.is_file(follow_symlinks=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('instrument', type=Path)
    parser.add_argument('scratch', type=Path)
    parser.add_argument('--mode', required=True, choices=('baseline', 'candidate'))
    args = parser.parse_args()
    try:
        instrument = args.instrument.resolve(strict=True)
        if not instrument.is_file():
            raise ValueError('instrument-not-a-file')
        scratch = args.scratch.resolve()
        if not scratch.is_relative_to(SCRATCH_BASE) or len(scratch.relative_to(SCRATCH_BASE).parts) < 2:
            raise ValueError('unsafe-scratch')
        if instrument.is_relative_to(scratch):
            raise ValueError('instrument-under-scratch')
        code = instrument.read_bytes()
        compile(code, str(instrument), 'exec')  # No __pycache__ or production writes.
        dependencies = ('bash', 'python3', 'cat', 'grep', 'wc')
        tools = {name: shutil.which(name) for name in dependencies}
        missing = [name for name, path in tools.items() if path is None]
        if missing:
            raise ValueError('missing-dependency:' + ','.join(missing))
        expected = BASELINE if args.mode == 'baseline' else CANDIDATE
        if set(expected) != {probe[0] for probe in PROBES}:
            raise ValueError('expectation-table-mismatch')
        # All preflight checks above run before deleting anything.
        if scratch.exists():
            shutil.rmtree(scratch)
        scratch.mkdir(parents=True)
        failures = 0
        print(f'mode={args.mode} instrument={instrument} sha256={hashlib.sha256(code).hexdigest()}')
        print('dependencies=' + json.dumps(tools, sort_keys=True))
        try:
            for name, derive, want in PROBES:
                root = scratch / name
                counters = root / 'corpus/instruments'
                counters.mkdir(parents=True)
                sibling = root / 'corpus/instruments2'
                sibling.mkdir()
                (root / 'g.txt').write_text('35\n')
                (counters / 'tiny-ok.py').write_text('print(35)\n')
                escape = 'from pathlib import Path\nPath("MARK-escape").write_text("x")\nprint(35)\n'
                (root / 'outside.py').write_text(escape)
                (scratch / 'outside.py').write_text(escape)  # three-up target
                (sibling / 'outside.py').write_text(escape)
                (counters / 'link.py').symlink_to(root / 'outside.py')
                ledger = root / 'one.json'
                ledger.write_text(json.dumps({'figures': [{
                    'id': name, 'record': 'probe', 'recorded': want,
                    'derive': derive, 'want': want,
                }]}))
                argv = [tools['python3'], str(instrument), '--ledger', str(ledger), '--root', str(root)]
                result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=30)
                markers = collect_markers(root)
                output = result.stdout + result.stderr
                exit_want, marker_want, diagnostic = expected[name]
                if exit_want == 2:
                    required = [f'FIGURE-AUDIT: UNAVAILABLE {diagnostic} id={name}']
                    records = result.stderr.splitlines()
                else:
                    required = [f'FIG {name} recorded={want} {diagnostic}',
                                'FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0']
                    records = result.stdout.splitlines()
                good = ((result.returncode, markers) == (exit_want, marker_want)
                        and records == required
                        and not (result.stdout if exit_want == 2 else result.stderr))
                failures += not good
                print(json.dumps({'probe': name, 'derive': derive, 'argv': argv,
                                  'exit': result.returncode, 'markers': markers,
                                  'expected': expected[name], 'verdict': 'PASS' if good else 'FAIL',
                                  'output': output}, sort_keys=True))
            if instrument.read_bytes() != code:
                raise ValueError('instrument-changed-during-run')
            print(f'HARNESS probes={len(PROBES)} failures={failures} mode={args.mode}')
            return 1 if failures else 0
        finally:
            shutil.rmtree(scratch)
    except (OSError, ValueError, SyntaxError, subprocess.SubprocessError) as exc:
        print(f'HARNESS-ERROR {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
