#!/usr/bin/env python3
"""Capture only the assigned finite r63 probes; raw receipts are single invocations."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

S = Path('/fast/scratch/hyaku/kasegi-r63/ExecPipeline')
L = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
W = L / '.ufo/waves/round-63/w1/ExecPipeline'
env = dict(os.environ, HYAKU_SCRATCH=str(S), TMPDIR=str(S), PYTHONDONTWRITEBYTECODE='1', GIT_DIR=str(L / '.git'))
root = S / 'fixture'
(root / 'corpus/instruments').mkdir(parents=True)
(root / 'g.txt').write_text('35\n')
(root / 'corpus/instruments/fail.py').write_text('raise SystemExit(7)\n')
probes = [
    ('cat-missing', 'cat missing.txt | wc -l', '0', 0, None),
    ('grep-invalid', "grep '[' g.txt | wc -l", '0', 1, 'derive-upstream-exit-2'),
    ('git-missing-ref', 'git show refs/figure-audit-nonexistent | wc -l', '0', 1, 'derive-upstream-exit-128'),
    ('python-exit7', 'python3 corpus/instruments/fail.py | wc -l', '0', 1, 'derive-upstream-exit-7'),
    ('grep-no-match', 'grep absent g.txt | wc -l', '0', 0, None),
    ('successful-pipeline', 'cat g.txt | wc -l', '1', 0, None),
]
records = []
def capture(name, command, cwd, expected, reason=None):
    receipt = W / (name + '.txt')
    with receipt.open('xb') as stream:
        p = subprocess.run(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=180)
    raw = receipt.read_bytes()
    passed = p.returncode == expected and (reason is None or ('reason=' + reason + ' stale').encode() in raw)
    records.append(dict(name=name, command=command, cwd=str(cwd), expected_exit=expected, expected_reason=reason,
                        actual_exit=p.returncode, verdict='pass' if passed else 'fail', receipt=str(receipt),
                        receipt_sha256=hashlib.sha256(raw).hexdigest()))
    print('%s exit=%d expected=%d verdict=%s' % (name, p.returncode, expected, 'pass' if passed else 'fail'), flush=True)

for label, instrument in [('baseline', S / 'baseline.py'), ('candidate', S / 'figure-audit.py')]:
    capture(label + '-selftest', [sys.executable, str(instrument), '--selftest'], S, 0)
    for name, derive, want, expected, reason in probes:
        ledger = root / (name + '.json')
        ledger.write_text(json.dumps({'figures': [dict(id=name, record='fixture', recorded=want, derive=derive, want=want)]}) + '\n')
        capture(label + '-' + name, [sys.executable, str(instrument), '--ledger', str(ledger), '--root', str(root)], S, expected, reason)

# All 35 ledger derives were inspected: Git reads, counting/text tools, and hashing only.
capture('candidate-real-ledger', [sys.executable, str(S / 'figure-audit.py'), '--ledger', str(L / 'corpus/instruments/figure-audit-ledger.json'), '--root', str(L)], S, 0)
for name in ['baseline.py', 'figure-audit.py']:
    shutil.copyfile(S / name, W / name)
shutil.copytree(root, W / 'fixture')
manifest = dict(environment_overrides={k: env[k] for k in ['HYAKU_SCRATCH', 'TMPDIR', 'PYTHONDONTWRITEBYTECODE', 'GIT_DIR']},
                python=sys.version, baseline_sha256=hashlib.sha256((S / 'baseline.py').read_bytes()).hexdigest(),
                candidate_sha256=hashlib.sha256((S / 'figure-audit.py').read_bytes()).hexdigest(), records=records)
(W / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
shutil.rmtree(S)
print('scratch_deleted=' + str(S), flush=True)
