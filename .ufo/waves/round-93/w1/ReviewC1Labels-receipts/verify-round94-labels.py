#!/usr/bin/env python3
"""Verify the round-94 non-author labels against ae53b3c bytes (read-only)."""
import re, subprocess, sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
REV = 'ae53b3c6e7e2ce070c2f022d01c1677a8908df1b'
TSV = LANE / '.ufo/waves/round-93/w1/ReviewC1Labels-receipts/round94-labels.tsv'

def show(path):
    return subprocess.run(['git', '-C', str(LANE), 'show', f'{REV}:{path}'],
                          capture_output=True, text=True, check=True).stdout.splitlines()

fails = []
rows = []
raw = TSV.read_text().splitlines()
hdr = raw[0].split('\t')
if hdr != ['line', 'key', 'label', 'fix', 'evidence']:
    fails.append(f'bad header {hdr!r}')
for n, line in enumerate(raw[1:], 2):
    f = line.split('\t')
    if len(f) != 5:
        fails.append(f'row {n}: {len(f)} fields')
        continue
    rows.append((n, f))

seen = set()
for n, (site, key, label, fix, ev) in rows:
    if not re.fullmatch(r'corpus/knowledge/[A-Za-z0-9._-]+\.md:\d+', site):
        fails.append(f'row {n}: bad site {site}')
        continue
    path, ln = site.rsplit(':', 1)
    ln = int(ln)
    src = show(path)
    if ln < 1 or ln > len(src):
        fails.append(f'row {n}: line {ln} out of range for {path} ({len(src)})')
        continue
    text = src[ln - 1]
    if key not in text:
        fails.append(f'row {n}: key {key!r} absent on {site}')
    if (site, key) in seen:
        fails.append(f'row {n}: duplicate (site,key)')
    seen.add((site, key))
    if label == 'drop':
        if 'Drop' not in fix:
            fails.append(f'row {n}: drop label without drop fix')
    else:
        targets = re.findall(r'SKILL\.md:(\d+)(?:-(\d+))?', label)
        if not targets:
            fails.append(f'row {n}: no SKILL target in label {label!r}')
        for a, b in targets:
            a = int(a); b = int(b or a)
            if not (1 <= a <= b <= 1251):
                fails.append(f'row {n}: target range {a}-{b} out of SKILL range')

# Completeness: every corpus/knowledge SKILL.md:N token at REV is either labelled
# in this TSV or is one of the three anchors verified correct in the report.
verified_correct = {
    ('corpus/knowledge/triage-thresholds.md', 58, 'SKILL.md:191'),
    ('corpus/knowledge/triage-thresholds.md', 144, 'SKILL.md:191'),
    ('corpus/knowledge/triage-thresholds.md', 437, 'SKILL.md:176-178'),
    ('corpus/knowledge/triage-thresholds.md', 454, 'SKILL.md:827-848'),
}
all_tokens = set()
for p in sorted((LANE / 'corpus/knowledge').glob('*.md')):
    rel = str(p.relative_to(LANE))
    src = show(rel)
    for i, l in enumerate(src, 1):
        for m in re.finditer(r'SKILL\.md:(\d+(?:-\d+)?(?:\s*,\s*\d+(?:-\d+)?)*)', l):
            for part in re.split(r',\s*', m.group(1)):
                all_tokens.add((rel, i, 'SKILL.md:' + part))
def key_ranges(key):
    out = []
    for part in re.split(r',\s*', key):
        m = re.search(r'(\d+(?:-\d+)?)\s*$', part)
        if m:
            out.append(m.group(1))
    return out

tsv_sites = set()
for n, (site, key, *_rest) in rows:
    path, ln = site.rsplit(':', 1)
    for rng in key_ranges(key):
        tsv_sites.add((path, int(ln), 'SKILL.md:' + rng))
fails2 = []
for t in sorted(all_tokens - tsv_sites - verified_correct):
    fails2.append(f'unlabelled stale token: {t[0]}:{t[1]} {t[2]}')
for t in sorted(tsv_sites - all_tokens):
    fails2.append(f'TSV token not present at REV: {t[0]}:{t[1]} {t[2]}')

print(f'ROUND94-LABELS-VERIFY rows={len(rows)} distinct_tokens={len(all_tokens)} '
      f'tsv_tokens={len(tsv_sites)} verified_correct={len(verified_correct)}')
print(f'failures={len(fails) + len(fails2)}')
for f in fails + fails2:
    print('FAIL ' + f)
print('PASS' if not fails and not fails2 else 'FAIL')
sys.exit(0 if not fails and not fails2 else 1)
