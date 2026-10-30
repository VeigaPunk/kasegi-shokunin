#!/usr/bin/env python3
"""Validate the canonical four-box checklist, never promotion or semantic truth.
0 clean; 1 noncanonical; 2 unreadable input. Read-only; no network.
"""
import argparse
from pathlib import Path
import re

LABELS = (
    'SKILL.md contains real decision tables, error patterns, checklists, cited sources',
    'At least one end-to-end domain task executed and logged in LOG.md',
    'Instructions executable by an agent without oral context',
    'No cross-domain bleed (PROVINCE.md still accurate)',
)

def grade(text, root):
    lines = text.splitlines()
    if not text.endswith('\n') or '\r' in text:
        return 'SF-NEWLINE'
    expected = ['# kasegi-shokunin — Promotion checklist', '',
                'Promotion to shokunin requires all of:', '']
    i = 0
    for value in expected:
        if i >= len(lines) or lines[i] != value:
            return 'SF-PREAMBLE'
        i += 1
    for label in LABELS:
        if i >= len(lines):
            return 'SF-MISSING-BOX'
        m = re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), lines[i])
        if not m:
            return 'SF-BOX'
        mark = m.group(1)
        i += 1
        if i < len(lines) and lines[i].startswith('      Evidence: '):
            evidence = lines[i][16:]
            # One plain repo-relative file pointer, then optional explanatory text.
            parts = evidence.split(' — ', 1)
            token = parts[0]
            path = Path(token)
            if not token or path.is_absolute() or '..' in path.parts or token != path.as_posix():
                return 'SF-POINTER'
            resolved = (root / path).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                return 'SF-POINTER'
            if mark == 'x':
                return 'SF-VERIFIER'  # This author-side checker cannot attest independence.
            i += 1
        elif mark != ' ':
            return 'SF-EVIDENCE'
    if i != len(lines):
        return 'SF-TRAILING'
    return 'SF-CLEAN'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--file', type=Path)
    args = ap.parse_args()
    try:
        raw = (args.file or args.root / 'SHONEN.md').read_bytes()
        result = grade(raw.decode('utf-8'), args.root)
    except (OSError, UnicodeError) as exc:
        print(f'shonen-form canonical=0 finding=SF-UNREADABLE error={type(exc).__name__} exit=2')
        return 2
    code = 0 if result == 'SF-CLEAN' else 1
    print(f'shonen-form canonical={int(code == 0)} finding={result} exit={code}')
    return code

if __name__ == '__main__':
    raise SystemExit(main())
