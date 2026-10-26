#!/usr/bin/env python3
"""ExecCensusDry round-31 gate-discrimination controls (scratch, read-only on the lane).

Regenerates three negative registries from the POST mirror registry
(validate/corpus/SOURCES.md, the mirror carrying the planned S048 row) so the
census gate is shown to refuse each failure class the seat is told to refuse:

  ctl-dup-id          the new row reuses S047's id            -> E03
  ctl-dup-url         the new row reuses S047's URL + scope    -> E04
  ctl-dangling-usedby the new row's used-by path does not exist-> E11

Each control corpus/ holds only a real SOURCES.md plus symlinks to the mirror's
knowledge/ and instruments/ dirs (no corpus duplication). Run from the lane root.
"""
import pathlib
import re
import sys

M = pathlib.Path('.ufo/waves/round-31/wave1/ExecCensusDry/validate')
BASE = (M / 'corpus' / 'SOURCES.md').read_text(encoding='utf-8')
CONTROLS = ('ctl-dup-id', 'ctl-dup-url', 'ctl-dangling-usedby')


def s047_row(text):
    rows = [l for l in text.split('\n') if re.match(r'^\| S047 ', l)]
    assert len(rows) == 1, 'S047 row not exactly once'
    return rows[0]


def patch_dup_id(text):
    out = text.replace('| S048 | Microsoft Security', '| S047 | Microsoft Security')
    assert out != text
    return out


def patch_dup_url(text):
    scope = s047_row(text).split('|')[5].strip()
    lines = text.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith('| S048 |')]
    assert len(idx) == 1, 'S048 row not exactly once'
    cells = lines[idx[0]].split('|')
    cells[2] = (' Microsoft Security Vulnerability Research (MSVR) — '
                'https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html ')
    cells[5] = f' {scope} '
    lines[idx[0]] = '|'.join(cells)
    return '\n'.join(lines)


def patch_dangling(text):
    out = text.replace('| corpus/knowledge/vendor-third-party-finding-coordination.md |',
                       '| corpus/knowledge/vendor-third-party-finding-coordination-ABSENT.md |')
    assert out != text
    return out


PATCHES = {
    'ctl-dup-id': patch_dup_id,
    'ctl-dup-url': patch_dup_url,
    'ctl-dangling-usedby': patch_dangling,
}


def main():
    if not BASE:
        print('empty mirror registry', file=sys.stderr)
        return 2
    for name in CONTROLS:
        corpus = M / name / 'corpus'
        corpus.mkdir(parents=True, exist_ok=True)
        for link, target in (('knowledge', '../../corpus/knowledge'),
                             ('instruments', '../../corpus/instruments')):
            p = corpus / link
            if not p.is_symlink():
                if p.exists():
                    print(f'{p} exists and is not a symlink', file=sys.stderr)
                    return 2
                p.symlink_to(target)
        (corpus / 'SOURCES.md').write_text(PATCHES[name](BASE), encoding='utf-8')
        print(f'wrote {name}/corpus/SOURCES.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
