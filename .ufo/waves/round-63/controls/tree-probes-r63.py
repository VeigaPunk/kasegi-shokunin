#!/usr/bin/env python3
"""R63 finite CLI tree counter; 0 match, 1 mismatch, 2 cannot evaluate.

Checks the independent MutationCollector shapes with unchanged claim prose.
No shell, no Git writes; only fresh fixture directories beneath --work are removed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CASES = (
    ('cat-missing', 'cat missing.txt | wc -l', '0', None),
    ('grep-invalid', "grep '[' present.txt | wc -l", '0', 2),
    ('git-bad-ref', 'git show refs/heads/r63-nonexistent:path | wc -l', '0', 128),
    ('python-exit7', 'python3 corpus/instruments/fail.py | wc -l', '0', 7),
    ('cat-middle', 'cat present.txt | cat missing.txt | wc -l', '0', None),
    ('grep-middle', "cat present.txt | grep '[' | wc -l", '0', 2),
    ('python-error-and-group', 'python3 corpus/instruments/fail.py | wc -l && wc -l < empty.txt', '0\n0', 7),
    ('grep-no-match', 'grep absent present.txt | wc -l', '0', None),
)
PROSE = 'Upstream positive exit>1 errors must be stale; upstream exit1 and negative statuses remain ignored.\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instrument', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--mode', choices=('base', 'candidate'), required=True)
    args = parser.parse_args()
    try:
        instrument = args.instrument.resolve(strict=True)
        work = args.work.resolve()
        if not work.is_relative_to(Path('/fast/scratch/hyaku/kasegi-r63')) or len(work.parts) < 7:
            raise ValueError('work-not-owned')
        if instrument.is_relative_to(work):
            raise ValueError('instrument-under-work')
        for binary in ('python3', 'cat', 'grep', 'wc', 'git'):
            if not shutil.which(binary):
                raise ValueError('missing-dependency-' + binary)
        work.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(instrument.read_bytes()).hexdigest()
        print('TREE instrument-sha256=' + digest + ' mode=' + args.mode, flush=True)
        failures = 0
        with tempfile.TemporaryDirectory(prefix='trees-', dir=work) as temporary:
            root = Path(temporary)
            (root / 'corpus/instruments').mkdir(parents=True)
            (root / 'corpus/instruments/fail.py').write_text('raise SystemExit(7)\n')
            (root / 'present.txt').write_text('present\n')
            (root / 'empty.txt').write_text('')
            (root / 'claim.md').write_text(PROSE)
            gitdir = root / '.git'
            (gitdir / 'objects').mkdir(parents=True)
            (gitdir / 'refs/heads').mkdir(parents=True)
            (gitdir / 'HEAD').write_text('ref: refs/heads/main\n')
            env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
            env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_CEILING_DIRECTORIES=str(root), TMPDIR=str(root), LC_ALL='C')
            for name, derive, want, upstream in CASES:
                ledger = root / 'ledger.json'
                ledger.write_text(json.dumps({'figures': [{'id': name, 'record': 'claim.md:1',
                    'recorded': want, 'derive': derive, 'want': want}]}))
                argv = [sys.executable, str(instrument), '--root', str(root), '--ledger', str(ledger)]
                result = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True, timeout=30)
                stale = args.mode == 'candidate' and upstream is not None
                reason = f'derive-upstream-exit-{upstream}' if stale else None
                expected = (f'FIG {name} recorded={want} derived=UNAVAILABLE reason={reason} stale\n'
                            'FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1\n') if stale else (
                            f'FIG {name} recorded={want} derived={want} ok\n'
                            'FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0\n')
                good = result.returncode == int(stale) and result.stdout == expected and result.stderr == ''
                failures += not good
                print(json.dumps({'case': name, 'derive': derive, 'want': want, 'argv': argv,
                    'expected_exit': int(stale), 'expected_stdout': expected, 'exit': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr, 'verdict': 'PASS' if good else 'FAIL'}), flush=True)
            if (root / 'claim.md').read_text() != PROSE or hashlib.sha256(instrument.read_bytes()).hexdigest() != digest:
                raise ValueError('bound-bytes-changed')
        print(f'TREE probes={len(CASES)} failures={failures} mode={args.mode}', flush=True)
        return int(bool(failures))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'TREE-ERROR {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
