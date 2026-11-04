#!/usr/bin/env python3
"""Named round62 collector error controls, not sandbox testing. Scratch removed on exit."""
import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--runner', type=Path, default=Path(__file__).with_name('c1-probe-run-r62.py'))
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    runner = args.runner.resolve(strict=True)
    work = args.work.resolve()
    base = Path('/fast/scratch/hyaku/kasegi-r62')
    if not work.is_relative_to(base) or len(work.relative_to(base).parts) < 2:
        parser.error('work must be a disposable seat/subdir under kasegi-r62')
    work.mkdir(parents=True, exist_ok=True)
    cases = []
    try:
        broken = work / 'broken99.py'
        broken.write_text('import sys\nsys.exit(99)\n')
        preserved = work / 'nested/instrument.py'
        preserved.parent.mkdir()
        preserved.write_text('print(35)\n')
        sentinel = work / 'nested/SENTINEL'
        sentinel.write_text('preserve\n')
        def run(name, instrument, scratch, expected, diagnostic, env=None):
            command = [sys.executable, str(runner), str(instrument), str(scratch), '--mode', 'candidate']
            p = subprocess.run(command, capture_output=True, text=True, env=env, timeout=120)
            out = p.stdout + p.stderr
            good = p.returncode == expected and diagnostic in out
            if name == 'instrument-under-scratch':
                good = good and preserved.is_file() and sentinel.read_text() == 'preserve\n'
            print('$ ' + ' '.join(command))
            print(out, end='')
            print(f'fault={name} exit={p.returncode} want={expected} verdict={"PASS" if good else "FAIL"}')
            cases.append(good)
        run('missing-instrument', work/'absent.py', work/'missing-probes', 2, 'HARNESS-ERROR')
        run('broken99', broken, work/'broken-probes', 1, 'HARNESS probes=10 failures=10')
        run('instrument-under-scratch', preserved, preserved.parent, 2, 'instrument-under-scratch')
        no_tools = os.environ.copy()
        no_tools['PATH'] = ''
        run('missing-dependencies', broken, work/'no-tools', 2, 'missing-dependency:', no_tools)
        fake = work/'wrong-record.py'
        fake.write_text('import sys\nprint("FIG wrong-id recorded=wrong derived=35 ok")\nprint("FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0")\n')
        run('wrong-record', fake, work/'wrong-record-probes', 1, 'HARNESS probes=10 failures=10')
        try:
            spec = importlib.util.spec_from_file_location('r62_collector', runner)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            try:
                module.collect_markers(work/'absent-directory')
            except OSError:
                good = True
            else:
                good = False
        except (AttributeError, OSError, ValueError, SyntaxError, SystemExit):
            good = False
        print(f'fault=enumeration-error verdict={"PASS" if good else "FAIL"}')
        cases.append(good)
        failures = len(cases) - sum(cases)
        print(f'RUNNER-FAULTS cases={len(cases)} failures={failures}')
        return 1 if failures else 0
    finally:
        shutil.rmtree(work)


if __name__ == '__main__':
    sys.exit(main())
