#!/usr/bin/env python3
"""R63 finite committed-input run; exit0 all named measurements match, 1 mismatch, 2 collection error.
No clones, Git writes, network, whole-tree mirrors or scratch outside --work.
Reads historical Git objects through an explicit read-only Git directory pointer;
this is a host-bound replay, not a hermetic export or safety sandbox.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PATHS = (
    'corpus/instruments/figure-audit.py',
    'corpus/instruments/figure-audit-mutbat.py',
    'corpus/instruments/figure-audit-ledger.json',
    'corpus/source-snapshots/round-54/S086.txt',
    '.ufo/waves/round-63/w1/ExecCollector/c1-probes-r63.py',
    '.ufo/waves/round-63/w1/ExecMutants/pipeline-mutbat-r63.py',
    '.ufo/waves/round-63/controls/tree-probes-r63.py',
    '.ufo/waves/round-63/controls/domain-review-ledger-r63.json',
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    lane = Path(__file__).resolve().parents[4]
    try:
        work = args.work.resolve()
        if not work.is_relative_to(Path('/fast/scratch/hyaku/kasegi-r63')) or len(work.parts) < 7:
            raise ValueError('work-not-owned')
        work.mkdir(parents=True, exist_ok=True)
        revision = subprocess.check_output(['git', '-C', str(lane), 'rev-parse', '--verify', args.revision + '^{commit}'], text=True).strip()
        gitdir = subprocess.check_output(['git', '-C', str(lane), 'rev-parse', '--absolute-git-dir'], text=True).strip()
        print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
        print('measured-revision=' + revision, flush=True)
        print('host-bound-git-object-replay=true hermetic=false', flush=True)
        with tempfile.TemporaryDirectory(prefix='committed-', dir=work) as temporary:
            root = Path(temporary)
            for name in PATHS:
                data = subprocess.check_output(['git', '-C', str(lane), 'show', revision + ':' + name])
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                print('INPUT ' + name + ' sha256=' + hashlib.sha256(data).hexdigest(), flush=True)
            (root / '.git').write_text('gitdir: ' + gitdir + '\n')
            scratch = root / 'scratch'
            scratch.mkdir()
            env = dict(os.environ, TMPDIR=str(scratch), HYAKU_SCRATCH=str(scratch), PYTHONDONTWRITEBYTECODE='1')
            instrument = root / PATHS[0]
            tasks = (
                ('collector', [sys.executable, str(root / PATHS[4]), '--instrument', str(instrument), '--work', str(work / 'collector'), '--mode', 'candidate'], 'HARNESS probes=8 failures=0 mode=candidate'),
                ('trees', [sys.executable, str(root / PATHS[6]), '--instrument', str(instrument), '--work', str(work / 'trees'), '--mode', 'candidate'], 'TREE probes=8 failures=0 mode=candidate'),
                ('selftest', [sys.executable, str(instrument), '--selftest'], 'selftest cases=43 failures=0'),
                ('old-mutbat', [sys.executable, str(root / PATHS[1]), '--instrument', str(instrument)], 'mutbat killed=5/5 survivors=0 invalid=0 controls=pass'),
                ('new-mutbat', [sys.executable, str(root / PATHS[5]), '--instrument', str(instrument), '--work', str(scratch)], 'MUTBAT mutants=7 killed=7 survivors=0 invalid=1 controls=3 verdict=PASS'),
                ('real-ledger', [sys.executable, str(instrument)], 'FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0'),
                ('domain-trial', [sys.executable, str(instrument), '--ledger', str(root / PATHS[7])], 'FIGURE-AUDIT figures=4 ok=4 stale=0 exit=0'),
            )
            failures = 0
            for name, argv, expected in tasks:
                print('RUN ' + name + ' argv=' + json.dumps(argv), flush=True)
                result = subprocess.run(argv, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
                print(result.stdout, end='' if result.stdout.endswith('\n') else '\n', flush=True)
                good = result.returncode == 0 and expected in result.stdout.splitlines()
                failures += not good
                print(f'RESULT {name} exit={result.returncode} verdict={"PASS" if good else "FAIL"}', flush=True)
            print(f'VERIFY measurements={len(tasks)} failures={failures} revision={revision}', flush=True)
            return int(bool(failures))
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'VERIFY-ERROR {type(exc).__name__}: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
