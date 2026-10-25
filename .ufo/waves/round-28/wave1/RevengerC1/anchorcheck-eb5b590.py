#!/usr/bin/env python3
"""Verify every mirror path:line cite in a markdown file: in-range + prints the source line."""
import re, sys, os
MIRROR = os.path.expanduser('~/Projects/the-bounty-hunter')
TOK = re.compile(r"`([^`\n]+)`")
CITE = re.compile(r"^((?:ops|fleets|docs|bin|bounty-map|\.omp)/[\w./-]+\.(?:mjs|sh|json|md)|[\w.-]+\.(?:mjs|json|sh|md)):(\d+)(?:-(\d+))?$")
src = sys.argv[1]
bad = ok = 0
seen = {}
for ln, line in enumerate(open(src), 1):
    for tok in TOK.findall(line):
        m = CITE.match(tok.strip().strip('.,;:'))
        if not m:
            continue
        rel, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        path = os.path.join(MIRROR, rel)
        if not os.path.exists(path):
            print(f"MISSING-FILE md:{ln} {tok}"); bad += 1; continue
        n = sum(1 for _ in open(path, errors='replace'))
        if b > n or a < 1:
            print(f"PAST-EOF md:{ln} {tok} (file has {n} lines)"); bad += 1; continue
        key = (rel, a, b)
        if key not in seen:
            lines = open(path, errors='replace').read().split('\n')
            seen[key] = ' ⏎ '.join(x.strip()[:100] for x in lines[a-1:b])
        ok += 1
print(f"\n== {src}: {ok} in-range cite instances, {bad} bad; {len(seen)} distinct anchors")
for (rel, a, b), txt in sorted(seen.items()):
    print(f"{rel}:{a}" + (f"-{b}" if b != a else "") + "  " + txt[:150])
