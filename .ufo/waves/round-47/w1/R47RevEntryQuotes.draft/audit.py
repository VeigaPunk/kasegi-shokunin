#!/usr/bin/env python3
"""Read-only independent F30 quote-location audit; no gate imports."""
import hashlib
import html
import re
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
p = LANE / '.ufo/waves/round-47/w1/R47SrF30Entry.draft/zdi-disclosure-policy.md'
snap = LANE / 'corpus/source-snapshots/round-47/S075.txt'
text = p.read_text()
lines = snap.read_text().splitlines()
def norm(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', '', s)).replace('**', '').replace('*', '').replace('`', '')).strip()
# Preserve offsets and line numbers while removing non-rendered comments/fences.
live = re.sub(r'<!--[\s\S]*?-->', lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), text)
live = re.sub(r'(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[^\n]*(?:\n|$)', lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), live)
cores = ['four months (120 days) to address the vulnerability', 'active exploitation is detected or imminent', 'granted only in rare circumstances', 'publish a limited advisory including mitigation', 'fifteen business days after the initial contact']
spans = list(re.finditer(r'“([^”]+)”|"([^"\n]+)"|‘([^’]+)’|(?<!\w)\x27([^\x27\n]+)\x27(?!\w)', text))
passed = []; failures = []; uncited = []
print('draft_sha256=' + hashlib.sha256(text.encode()).hexdigest())
print('source_sha256=' + hashlib.sha256(snap.read_bytes()).hexdigest())
for i, m in enumerate(spans, 1):
    q = next(x for x in m.groups() if x is not None)
    n = text.count('\n', 0, m.start()) + 1
    c = re.match(r'\s*(?:\(\s*)?`S075\.txt:(\d+)(?:-(\d+))?`(?:\))?', text[m.end():])
    # Every curly-double quotation is evidence; other styles >=4 words.
    required = m[0].startswith('“') or len(norm(q).split()) >= 4
    if not c:
        if required: uncited.append((n, q))
        print(f'Q{i} line={n} words={len(norm(q).split())} cited=0 quote={q!r}')
        continue
    a = int(c[1]); b = int(c[2] or c[1])
    located = norm(q) in norm(' '.join(lines[a-1:b]))
    visible = live[m.start():m.end()] == m[0]
    ok = 20 <= a <= b <= 27 and b-a+1 <= 12 and len(norm(q).split()) <= 25 and located
    if ok and visible: passed.append(norm(q))
    if not ok: failures.append((n, q))
    print(f'Q{i} line={n} citation={a}-{b} words={len(norm(q).split())} located={int(located)} live={int(visible)} pass={int(ok)} quote={q!r}')
for core in cores:
    print(f'core pass={int(any(core in q for q in passed))} text={core!r}')
# Re-derive frozen H5 locator syntax, without calling the grader.
syntax = r'\s*\(`?S075\.txt:(\d+)(?:-(\d+))?`?'
frozen_matches = re.findall('“([^”]+)”' + syntax, text) + re.findall('"([^"]+)"' + syntax, text, re.S)
print(f'summary quoted={len(spans)} located_live={len(passed)} failures={len(failures)} uncited_required={len(uncited)} cores={sum(any(c in q for q in passed) for c in cores)}/5 frozen_H5_syntax_matches={len(frozen_matches)}')
# Bounded negative controls discriminate real location from marker presence.
q = 'four months (120 days) to address the vulnerability'
print('control fabricated_quote located=' + str(int(norm(q + ' fabricated words') in norm(lines[23]))))
print('control wrong_anchor_25 located=' + str(int(norm(q) in norm(lines[24]))))
print('control do_nothing_missing_entry located_spans=0 cores=0/5')
