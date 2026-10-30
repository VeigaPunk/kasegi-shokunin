#!/usr/bin/env python3
"""Export only checklist/evidence surfaces and run frozen form counter on both revisions."""
import argparse
from pathlib import Path
import subprocess
import tempfile
import shutil
import json
import hashlib
import datetime

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--base', required=True)
    ap.add_argument('--after', required=True)
    ap.add_argument('--work', type=Path, required=True)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='measure-', dir=a.work))
    print('run-utc:', datetime.datetime.now(datetime.timezone.utc).isoformat())
    print('base:', a.base, 'after:', a.after)
    code = git(a.root, 'show', a.after + ':corpus/instruments/shonen-form.py')
    print('frozen-counter-sha256:', hashlib.sha256(code).hexdigest())
    try:
        tool = work / 'counter.py'
        tool.write_bytes(code)
        for label, rev in [('before', a.base), ('after', a.after)]:
            tree = work / label
            tree.mkdir()
            paths = ['SHONEN.md', 'LOG.md', 'SKILL.md', 'PROVINCE.md',
                     'corpus/lessons/round-47-verifier-spotcheck.md']
            for path in paths:
                dest = tree / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(git(a.root, 'show', rev + ':' + path))
            p = subprocess.run(['python3', str(tool), '--root', str(tree)], text=True, capture_output=True)
            raw = (tree / 'SHONEN.md').read_bytes()
            marks = sum(line.startswith(b'- [') for line in raw.splitlines())
            print(label + ':', p.stdout.strip(), 'process_exit=' + str(p.returncode))
            print(label + '-plain:', json.dumps({'checklist_lines': len(raw.splitlines()), 'boxes': marks,
                                                'checklist_sha256': hashlib.sha256(raw).hexdigest()}))
    finally:
        shutil.rmtree(work)

if __name__ == '__main__':
    main()
