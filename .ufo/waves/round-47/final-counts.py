#!/usr/bin/env python3
"""Read-only round-47 counts; use --root for a committed export."""
import argparse
import json
import pathlib
import re
p = argparse.ArgumentParser()
p.add_argument('--root', default='.')
a = p.parse_args()
r = pathlib.Path(a.root)
s = (r / 'corpus/SOURCES.md').read_text()
f = (r / 'corpus/README.md').read_text()
e = (r / 'corpus/knowledge/github-repository-security-advisories.md').read_text()
print(json.dumps({
 'frontier_rows': len(re.findall(r'^\| F[0-9]+ \|', f, re.M)),
 'registry_rows': len(re.findall(r'^ {0,3}\|\s*S[0-9]{3,}\s*\|', s, re.M)),
 'knowledge_files': len(list((r / 'corpus/knowledge').glob('*.md'))),
 'to_append_lines': sum('to append' in l for l in s.splitlines()),
 'source_fence_lines': sum('```' in l for l in s.splitlines()),
 'advisory_lines': len(e.splitlines()),
 'old_citation_lines': sum('S074.txt:' in l for l in e.splitlines()),
 'old_citation_occurrences': e.count('S074.txt:'),
 'supersedes_lines': sum('supersedes S074' in l for l in s.splitlines()),
 'old_false_body_claim_lines': sum('all 42 lines are body prose' in l for l in e.splitlines()),
}, indent=1))
