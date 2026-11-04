#!/usr/bin/env python3
"""Round-62 CounterBase: read-only counters over an unchanged committed export."""
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess

L = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
B = Path('/fast/scratch/hyaku/kasegi-r62/CounterBase/base')
OUT = L / '.ufo/waves/round-62/w1/CounterBase'
BASE = 'f7dcab84b104ccc03083fa1ad8c38e12830d25c9'
CENSUS = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
receipt = ['axes=depth:verifiability,coverage', 'base=' + BASE,
           'tree=git archive BASE; unchanged committed bytes; no git index or refs',
           'utc=' + datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'NOTE: frontier executes entry recheck strings verbatim; absolute cd prefixes can read the live lane, not the export. No substitution applied.']
results = []
def run(label, argv, cwd=B):
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    result = dict(label=label, argv=argv, cwd=str(cwd), stdout=proc.stdout,
                  stderr=proc.stderr, exit=proc.returncode)
    results.append(result)
    receipt.extend(['\n## ' + label, '$ (cwd=' + str(cwd) + ') ' + shlex.join(argv),
                    proc.stdout.rstrip(), 'stderr=' + json.dumps(proc.stderr),
                    'exit=' + str(proc.returncode)])
    print(label + ' exit=' + str(proc.returncode), flush=True)

for tool in [['python3', '--version'], ['bash', '--version'], ['sort', '--version'],
             ['gawk', '--version'], ['git', '--version'], ['uname', '-srmo']]:
    run('host-' + tool[0], tool)
for rel in ['corpus/instruments/frontier-recheck-count.py', 'corpus/instruments/capture-binding-check.py',
            'corpus/instruments/source-recheck.py', 'corpus/instruments/knowledge-expected.txt',
            'corpus/SOURCES.md', 'corpus/README.md']:
    a = (B / rel).read_bytes()
    c = (L / rel).read_bytes()
    receipt.append('digest ' + rel + ' base=' + hashlib.sha256(a).hexdigest() + ' live=' + hashlib.sha256(c).hexdigest() + ' equal=' + str(a == c))
receipt.append('host-census-sha256=' + hashlib.sha256(Path(CENSUS).read_bytes()).hexdigest())
run('base-frontier', ['python3', 'corpus/instruments/frontier-recheck-count.py'])
run('base-capture-binding', ['python3', 'corpus/instruments/capture-binding-check.py'])
run('base-sources-census', [CENSUS, 'census', '--root', str(B.parent), '--file', str(B / 'corpus/SOURCES.md')])
run('base-sources-validate', [CENSUS, 'validate', '--root', str(B.parent), '--file', str(B / 'corpus/SOURCES.md')])
run('base-knowledge-expected-sort', ['sort', 'corpus/instruments/knowledge-expected.txt'])
run('base-knowledge-expected-sorted-check', ['sort', '-c', 'corpus/instruments/knowledge-expected.txt'])
run('live-sources-validate-once', [CENSUS, 'validate', '--root', '/home/vgpnk/Projects/shokunin', 'kasegi'], L)

def rows(root):
    found = []
    registry = False
    for lineno, line in enumerate((root / 'corpus/SOURCES.md').read_text().splitlines(), 1):
        if line.startswith('## '):
            registry = line == '## Registry'
        if registry and re.match(r'^\|\s*S\d+\s*\|', line):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            urls = re.findall(r'https://[^\s<>]+', cells[1])
            found.append(dict(line=lineno, id=cells[0], urls=urls, columns=len(cells), status=cells[7]))
    return found
base_rows = rows(B)
live_rows = rows(L)
ids = [r['id'] for r in base_rows]
first_free = next('S%03d' % n for n in range(1, 10000) if 'S%03d' % n not in ids)
url_groups = collections.defaultdict(list)
for r in base_rows:
    for url in r['urls']:
        url_groups[url].append(r['id'])
summary = dict(base_rows=len(base_rows), unique_ids=len(set(ids)), duplicate_ids=[k for k,v in collections.Counter(ids).items() if v > 1],
               malformed_rows=[r for r in base_rows if r['columns'] != 11 or len(r['urls']) != 1],
               first_free=first_free, S095_rows=ids.count('S095'),
               proposed_url_registered=[r['id'] for r in base_rows if 'https://certcc.github.io/CERT-Guide-to-CVD/topics/phases/' in r['urls']],
               exact_duplicate_urls={k:v for k,v in url_groups.items() if len(v)>1},
               base_live_id_url_equal=[(r['id'], r['urls']) for r in base_rows] == [(r['id'], r['urls']) for r in live_rows],
               expected_lines=len((B/'corpus/instruments/knowledge-expected.txt').read_text().splitlines()),
               knowledge_files=len(list((B/'corpus/knowledge').glob('*.md'))))
rechecks = []
for entry in sorted((B / 'corpus/knowledge').glob('*.md')):
    for line in entry.read_text().splitlines():
        if line.startswith('recheck:') and ('cd /' in line or 'cd ~' in line):
            rechecks.append(dict(entry=str(entry.relative_to(B)), recheck=line))
receipt.extend(['\n## Registry and inventory summary', json.dumps(summary, indent=2),
                '\n## All BASE source row ids and URL tokens', json.dumps(base_rows, indent=2),
                '\n## Absolute-home recheck strings (host dependencies)', json.dumps(rechecks, indent=2)])
(OUT/'baseline-receipt.txt').write_text('\n'.join(receipt) + '\n')
(OUT/'baseline-results.json').write_text(json.dumps(dict(base=BASE, commands=results, summary=summary, registry=base_rows, host_bound_rechecks=rechecks), indent=2) + '\n')
print(json.dumps(summary, indent=2))
