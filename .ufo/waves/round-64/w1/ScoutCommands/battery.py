#!/usr/bin/python3
"""ScoutCommands r64: base-vs-candidate figure-audit falsification battery, scratch only.

Builds a candidate instrument copy in scratch whose upstream test is
"positive nonzero except basename(grep) with exit 1" (the intended r64 rule),
then runs base and candidate over (a) a finite mini-ledger probe battery and
(b) the real lane ledger. Prints raw instrument stdout per run.
"""
import datetime
import difflib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/kasegi-r64/ScoutCommands')
LANE = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
INSTR = LANE / 'corpus/instruments/figure-audit.py'
OUT = S / 'receipts'
OUT.mkdir(parents=True, exist_ok=True)

OLD = ("            for p in processes[:-1]:\n"
       "                if p.returncode > 1:\n")
NEW = ("            for p in processes[:-1]:\n"
       "                if p.returncode > 0 and not (os.path.basename(p.args[0]) == \"grep\" and p.returncode == 1):\n")

PROBES = (
    ('cat-missing', 'cat missing | wc -l', '0'),
    ('cat-partial', 'cat g.txt missing | wc -l', '1'),
    ('cut-missing', 'cut -d: -f1 missing | wc -l', '0'),
    ('head-missing', 'head missing | wc -l', '0'),
    ('tail-missing', 'tail missing | wc -l', '0'),
    ('ls-missing', 'ls missing | wc -l', '0'),
    ('sort-missing', 'sort missing | wc -l', '0'),
    ('sha256sum-missing', 'sha256sum missing | wc -l', '0'),
    ('tr-missing', 'tr a b missing | wc -l', '0'),
    ('grep-no-match', "grep absent g.txt | wc -l", '0'),
    ('grep-invalid', "grep '[' g.txt | wc -l", '0'),
    ('final-no-match', 'cat g.txt | grep absent', '0'),
    ('mid-cat-missing', 'cat present.txt | cat missing | wc -l', '0'),
    ('python-exit1-upstream', 'python3 corpus/instruments/exit1.py | wc -l', '0'),
    ('python-sigterm-upstream', 'python3 corpus/instruments/sigterm.py | wc -l', '0'),
    ('python-sigterm-final', 'python3 corpus/instruments/sigterm.py', '0'),
    ('git-missing-ref', 'git show refs/heads/figure-audit-nonexistent | wc -l', '0'),
    ('success-pipeline', 'cat g.txt | wc -l', '1'),
    ('and-concat', 'cat g.txt && cat g.txt', '35\n35'),
    ('and-fail', 'cat missing && cat g.txt', '35'),
)

print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat())
print('instrument=' + str(INSTR))
print('python=' + sys.version.split()[0])

text = INSTR.read_text()
count = text.count(OLD)
print('patch-anchor-count=%d' % count)
if count != 1:
    print('BATTERY-ERROR patch anchor not unique; aborting')
    sys.exit(2)
candidate = S / 'candidate-figure-audit.py'
candidate.write_text(text.replace(OLD, NEW))
with open(OUT / 'candidate-diff.txt', 'w') as f:
    f.write('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat() + '\n')
    f.writelines(difflib.unified_diff(text.splitlines(keepends=True),
                                      candidate.read_text().splitlines(keepends=True),
                                      fromfile='figure-audit.py(base)', tofile='candidate-figure-audit.py'))
print('candidate-written sha256-pending diff=' + str(OUT / 'candidate-diff.txt'))

PY = shutil.which('python3')
env = dict(os.environ, LC_ALL='C', PYTHONDONTWRITEBYTECODE='1',
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull)
for key in [k for k in env if k.startswith('GIT_') and k not in ('GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL')]:
    del env[key]


def run_instrument(instrument, ledger, root):
    argv = [PY, str(instrument), '--ledger', str(ledger), '--root', str(root)]
    r = subprocess.run(argv, cwd=str(root), env=env, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True, timeout=120)
    return r


FIG = re.compile(r'reason=derive-[a-z-]+-(\d+)')


def verdict(stdout):
    for line in stdout.splitlines():
        if line.startswith('FIGURE-AUDIT'):
            return line
    return 'TRAILER-MISSING'


def reason(stdout):
    m = re.search(r'reason=derive-\S+ stale', stdout)
    if m:
        return m.group(0)[len('reason='):].split()[0]
    return '-'


print('== mini-ledger battery ==')
print('%-24s %-4s %-6s %-38s %-38s' % ('probe', 'mode', 'exit', 'reason', 'trailer'))
matrix = {}
for name, derive, want in PROBES:
    root = S / ('bat-' + name)
    if root.exists():
        shutil.rmtree(root)
    (root / 'corpus/instruments').mkdir(parents=True)
    (root / 'g.txt').write_text('35\n')
    (root / 'present.txt').write_text('present\n')
    (root / 'corpus/instruments/exit1.py').write_text('import sys\nsys.exit(1)\n')
    (root / 'corpus/instruments/sigterm.py').write_text('import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n')
    gitdir = root / '.git'
    (gitdir / 'objects').mkdir(parents=True)
    (gitdir / 'refs/heads').mkdir(parents=True)
    (gitdir / 'HEAD').write_text('ref: refs/heads/main\n')
    ledger = root / 'one.json'
    import json
    ledger.write_text(json.dumps({'figures': [{
        'id': name, 'record': 'scout-r64-battery', 'recorded': want,
        'derive': derive, 'want': want}]}) + '\n')
    for mode, inst in (('base', INSTR), ('cand', candidate)):
        r = run_instrument(inst, ledger, root)
        trailer = verdict(r.stdout)
        matrix[(name, mode)] = (r.returncode, reason(r.stdout), trailer)
        print('%-24s %-4s %-6d %-38s %-38s' % (name, mode, r.returncode, matrix[(name, mode)][1], trailer))
    shutil.rmtree(root)

print('== real lane ledger (35 figures, read-only replay) ==')
real = {}
for mode, inst in (('base', INSTR), ('cand', candidate)):
    r = run_instrument(inst, LANE / 'corpus/instruments/figure-audit-ledger.json', LANE)
    real[mode] = r.stdout
    path = OUT / ('real-ledger-%s.txt' % mode)
    path.write_text('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat()
                    + '\nmode=' + mode + ' exit=' + str(r.returncode) + '\n' + r.stdout)
    print('mode=%s exit=%d trailer=%s receipt=%s' % (mode, r.returncode, verdict(r.stdout), path))

diff = list(difflib.unified_diff(real['base'].splitlines(keepends=True),
                                 real['cand'].splitlines(keepends=True),
                                 fromfile='real-ledger-base', tofile='real-ledger-cand'))
print('real-ledger-diff-lines=%d' % len(diff))
if diff:
    sys.stdout.writelines(diff)

print('== selftest over both bytes ==')
for mode, inst in (('base', INSTR), ('cand', candidate)):
    e2 = dict(env, HYAKU_SCRATCH=str(S / 'selftest'))
    Path(e2['HYAKU_SCRATCH']).mkdir(parents=True, exist_ok=True)
    r = subprocess.run([PY, str(inst), '--selftest'], cwd=str(S), env=e2,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=300)
    fails = [ln for ln in r.stdout.splitlines() if 'verdict=fail' in ln]
    print('selftest mode=%s exit=%d %s' % (mode, r.returncode, r.stdout.strip().splitlines()[-1]))
    for ln in fails:
        print('  FAILING ' + ln)
print('BATTERY-DONE')
