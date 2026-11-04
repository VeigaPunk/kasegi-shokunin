#!/usr/bin/python3
"""ScoutCommands r64: Popen returncode mirror of figure-audit run_derive semantics.

The instrument observes Python Popen returncodes (negative = killed by signal N),
not shell $?. This receipt records the numbers the instrument would see.
"""
import datetime
import subprocess

S = '/fast/scratch/hyaku/kasegi-r64/ScoutCommands'

print('run-utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat())


def run(argv, cwd=S):
    p = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = p.communicate()
    return p.returncode, o.decode(errors='replace').strip(), e.decode(errors='replace').strip()


CASES = (
    ('popen-cat-missing', ['cat', 'missing']),
    ('popen-cat-partial', ['cat', 'g.txt', 'missing']),
    ('popen-cut-missing', ['cut', '-d', ':', '-f1', 'missing']),
    ('popen-head-missing', ['head', 'missing']),
    ('popen-tail-missing', ['tail', 'missing']),
    ('popen-ls-missing', ['ls', 'missing']),
    ('popen-sort-missing', ['sort', 'missing']),
    ('popen-sha256sum-missing', ['sha256sum', 'missing']),
    ('popen-tr-missing', ['tr', 'a', 'b', 'missing']),
    ('popen-wc-missing', ['wc', 'missing']),
    ('popen-grep-no-match', ['grep', 'absent', 'g.txt']),
    ('popen-grep-missing-file', ['grep', 'absent', 'missing']),
    ('popen-grep-invalid-regex', ['grep', '[', 'g.txt']),
)
for name, argv in CASES:
    rc, o, e = run(argv)
    print('%s argv=%r rc=%d stdout=%r stderr=%r' % (name, argv, rc, o, e))

# Upstream stage killed by SIGPIPE while writing into head -1.
p1 = subprocess.Popen(['yes'], cwd=S, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
p2 = subprocess.Popen(['head', '-1'], cwd=S, stdin=p1.stdout,
                      stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
p1.stdout.close()
o, _ = p2.communicate()
p1.wait()
print('popen-signal-upstream yes rc=%d head rc=%d out=%r' % (p1.returncode, p2.returncode, o.decode().strip()))

# Python stage that terminates itself by SIGTERM (final and upstream shapes).
with open(S + '/sigterm.py', 'w') as f:
    f.write('import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n')
rc, o, e = run(['/usr/bin/python3', S + '/sigterm.py'])
print('popen-python-sigterm rc=%d stdout=%r' % (rc, o))
rc, o, e = run(['/usr/bin/python3', '-c', 'import sys; sys.exit(1)'])
print('popen-python-exit1 rc=%d' % rc)
rc, o, e = run(['/usr/bin/python3', '-c', 'import sys; sys.exit(2)'])
print('popen-python-exit2 rc=%d' % rc)
