#!/usr/bin/env python3
"""Finite round-63 audit CLI probes, not a sandbox or general error policy.

Requires Python 3.9+ stdlib and PATH python3, cat, grep, wc, git; no shells.
--instrument and --work must be absolute. Work must be a disposable subdirectory
of the invoking seat under /fast/scratch/hyaku/kasegi-r63. Existing files are never cleared.
A fresh private run directory is removed on exit; the instrument must be outside
work. TMPDIR is private.
Exit 0: exact expected tuples/output; 1: mismatch; 2: usage/collection error.
Cat missing returns 1 on this host: outside the positive-exit>1 predicate,
so it is a retained green boundary probe in both modes, not a claimed repair.
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

SCRATCH_BASE = Path('/fast/scratch/hyaku/kasegi-r63')
# (name, unchanged derive string, want, candidate reason or None)
PROBES = (
    ('cat-missing', 'cat missing | wc -l', '0', None),
    ('grep-invalid', "grep '[' g.txt | wc -l", '0', 'derive-upstream-exit-2'),
    ('git-missing-ref', 'git show refs/heads/r63-nonexistent | wc -l', '0', 'derive-upstream-exit-128'),
    ('python-exit7', 'python3 corpus/instruments/fail.py | wc -l', '0', 'derive-upstream-exit-7'),
    ('grep-no-match', "grep 'absent' g.txt | wc -l", '0', None),
    ('cat-success', 'cat g.txt | wc -l', '1', None),
    ('final-failure', 'cat g.txt | grep absent', '0', 'derive-exit-1'),
    ('and-concatenated', 'cat g.txt && cat g.txt', '35\n35', None),
)


def expected_output(name, want, reason):
    if reason:
        finding = f'FIG {name} recorded={want} derived=UNAVAILABLE reason={reason} stale'
        return (1, 1, 0, 1, reason, finding), finding + '\nFIGURE-AUDIT figures=1 ok=0 stale=1 exit=1\n'
    finding = f'FIG {name} recorded={want} derived={want} ok'
    return (0, 1, 1, 0, None, finding), finding + '\nFIGURE-AUDIT figures=1 ok=1 stale=0 exit=0\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instrument', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--mode', choices=('base', 'candidate'), required=True)
    args = parser.parse_args()
    try:
        if not args.instrument.is_absolute() or not args.work.is_absolute():
            raise ValueError('absolute-paths-required')
        instrument = args.instrument.resolve(strict=True)
        work = args.work.resolve()
        if (not work.is_relative_to(SCRATCH_BASE)
                or len(work.relative_to(SCRATCH_BASE).parts) < 2):
            raise ValueError('work-not-owned')
        if instrument.is_relative_to(work):
            raise ValueError('instrument-under-work')
        if not instrument.is_file():
            raise ValueError('instrument-not-file')
        code = instrument.read_bytes()
        tools = {name: shutil.which(name) for name in ('python3', 'cat', 'grep', 'wc', 'git')}
        missing = [name for name, path in tools.items() if path is None]
        if missing:
            raise ValueError('missing-dependencies:' + ','.join(missing))
        work.mkdir(parents=True, exist_ok=True)
        failures = 0
        print(json.dumps({'mode': args.mode, 'instrument': str(instrument),
                          'sha256': hashlib.sha256(code).hexdigest(), 'dependencies': tools,
                          'collector_argv': sys.argv}, sort_keys=True), flush=True)
        with tempfile.TemporaryDirectory(prefix='probes-', dir=work) as temporary:
            private = Path(temporary)
            tmp = private / 'tmp'
            tmp.mkdir()
            env = dict(os.environ, TMPDIR=str(tmp), LC_ALL='C', PYTHONDONTWRITEBYTECODE='1')
            # Do not discover or consult a host repository/config for the missing-ref read.
            for key in tuple(env):
                if key.startswith('GIT_'):
                    del env[key]
            env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_CEILING_DIRECTORIES=str(private))
            for name, derive, want, candidate_reason in PROBES:
                root = private / name
                counters = root / 'corpus/instruments'
                counters.mkdir(parents=True)
                (root / 'g.txt').write_text('35\n')
                (counters / 'fail.py').write_text('import sys\nsys.exit(7)\n')
                # Minimal empty Git fixture written directly: no git init/commit/index mutation.
                gitdir = root / '.git'
                (gitdir / 'objects').mkdir(parents=True)
                (gitdir / 'refs/heads').mkdir(parents=True)
                (gitdir / 'HEAD').write_text('ref: refs/heads/main\n')
                ledger = root / 'one.json'
                ledger.write_text(json.dumps({'figures': [{
                    'id': name, 'record': 'round63-finite-probe', 'recorded': want,
                    'derive': derive, 'want': want,
                }]}))
                argv = [tools['python3'], str(instrument), '--ledger', str(ledger), '--root', str(root)]
                result = subprocess.run(argv, cwd=root, env=env, capture_output=True,
                                        text=True, timeout=30)
                reason = candidate_reason if args.mode == 'candidate' or name == 'final-failure' else None
                expected, stdout = expected_output(name, want, reason)
                good = result.returncode == expected[0] and result.stdout == stdout and result.stderr == ''
                failures += not good
                print(json.dumps({'probe': name, 'derive': derive, 'want': want,
                                  'argv': argv, 'cwd': str(root), 'TMPDIR': str(tmp),
                                  'expected_tuple': expected, 'expected_stdout': stdout,
                                  'expected_stderr': '', 'exit': result.returncode,
                                  'stdout': result.stdout, 'stderr': result.stderr,
                                  'verdict': 'PASS' if good else 'FAIL'}, sort_keys=True), flush=True)
            if instrument.read_bytes() != code:
                raise ValueError('instrument-changed-during-run')
        print(f'HARNESS probes={len(PROBES)} failures={failures} mode={args.mode}', flush=True)
        return 1 if failures else 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'HARNESS-ERROR {type(exc).__name__}: {exc}', file=sys.stderr, flush=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
