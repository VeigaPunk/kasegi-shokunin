#!/usr/bin/env python3
"""Round66 finite cat-SIGPIPE limb battery; not an authenticity proof.

Requires an independently runnable public-path collector. Exit0: baseline and
one equivalent pass, three compiled semantic mutants fail by findings, invalid
anchor rejected. Exit1: expectation mismatch; exit2: setup/usage error.
Only writes below --work under HYAKU_SCRATCH (default /fast/scratch/hyaku);
removes its own uniquely-created directory on exit. Child timeout180 seconds.
"""
import argparse
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

MUTANTS = (
    ('ignore-cat-sigpipe', 'return not cat_sigpipe_exempt(stage_argv)', 'return False'),
    ('relax-two-operands', 'return len(tokens) <= 1', 'return len(tokens) <= 2'),
    ('reject-single-input', 'return len(tokens) <= 1', 'return False'),
)


def patch(text, old, new):
    if text.count(old) != 1:
        raise ValueError('mutation-anchor-not-exactly-once')
    changed = text.replace(old, new, 1)
    if changed == text:
        raise ValueError('no-op-mutation')
    compile(changed, '<cat-mutant>', 'exec')
    return changed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--instrument', required=True)
    ap.add_argument('--collector', required=True)
    ap.add_argument('--work', required=True)
    args = ap.parse_args()
    instrument = Path(args.instrument).resolve(strict=True)
    collector = Path(args.collector).resolve(strict=True)
    work = Path(args.work).resolve()
    allowed = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')).resolve()
    if work == allowed or not work.is_relative_to(allowed):
        raise ValueError('work-outside-scratch')
    work.mkdir(parents=True, exist_ok=True)
    owned = Path(tempfile.mkdtemp(prefix='cat-mutbat-', dir=work))
    try:
        text = instrument.read_text()
        print('instrument_sha256=' + hashlib.sha256(instrument.read_bytes()).hexdigest())
        print('collector_sha256=' + hashlib.sha256(collector.read_bytes()).hexdigest())
        failures = 0

        def score(name, body):
            path = owned / (name + '.py')
            path.write_text(body)
            env = os.environ.copy()
            env['TMPDIR'] = str(owned)
            cmd = [sys.executable, '-B', str(collector), '--instrument', str(path),
                   '--work', str(owned / name), '--mode', 'candidate']
            result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=180, env=env)
            print('CASE', name, 'rc=' + str(result.returncode))
            print(result.stdout, end='')
            trailer = re.search(r'^PROBES probes=(\d+) failures=(\d+)\b', result.stdout, re.M)
            # A syntax/setup failure is invalid, never a killed semantic mutant.
            valid = trailer is not None and int(trailer.group(1)) >= 8
            return valid and result.returncode == 0 and int(trailer.group(2)) == 0, valid, result.returncode

        good, valid, rc = score('baseline', text)
        failures += not good
        killed = 0
        for name, old, new in MUTANTS:
            changed = patch(text, old, new)
            good, valid, rc = score(name, changed)
            dead = valid and not good and rc == 1
            print('MUTANT', name, 'killed=' + str(int(dead)), 'valid=' + str(int(valid)))
            killed += dead
            failures += not dead
        equivalent = patch(text, 'return len(tokens) <= 1', 'return len(tokens) < 2')
        good, valid, rc = score('equivalent', equivalent)
        failures += not good
        invalid_rejected = False
        try:
            patch(text, 'THIS_ANCHOR_IS_INTENTIONALLY_ABSENT_R66', 'False')
        except ValueError:
            invalid_rejected = True
        failures += not invalid_rejected
        print('CAT-MUTBAT killed=%d/3 survivors=%d equivalents_held=%d invalid_rejected=%d failures=%d' %
              (killed, 3-killed, int(good), int(invalid_rejected), failures))
        return 1 if failures else 0
    finally:
        shutil.rmtree(owned)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, SyntaxError, subprocess.TimeoutExpired) as exc:
        print('CAT-MUTBAT SETUP ' + str(exc), file=sys.stderr)
        sys.exit(2)
