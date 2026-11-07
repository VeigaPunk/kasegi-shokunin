#!/usr/bin/env python3
"""Per-citation diff: my independent census rows vs resolve.py's TSV (census-at-rev extract)."""
import sys

res_tsv, my_tsv = sys.argv[1], sys.argv[2]

# resolve.py TSV: 8 fields, citation may contain tabs -> last 7 fixed, citation = join(cells[:-7])
res = {}
with open(res_tsv, encoding="utf-8") as fh:
    fh.readline()
    for line in fh:
        cells = line.rstrip("\n").split("\t")
        if len(cells) < 8:
            continue
        cite = "\t".join(cells[:-7])
        cls, scopes = cells[-7], cells[-1]
        res[cite] = (cls, scopes)

# my rows.tsv: citation\tclass\tscopes\toccurrences ; citation may contain tabs -> rsplit 3
mine = {}
with open(my_tsv, encoding="utf-8") as fh:
    fh.readline()
    for line in fh:
        parts = line.rstrip("\n").rsplit("\t", 3)
        if len(parts) != 4:
            continue
        cite, cls, scopes, _occ = parts
        mine[cite] = (cls, scopes)

rset, mset = set(res), set(mine)
print("resolve.py rows: %d   my rows: %d" % (len(res), len(mine)))
print("citation sets equal: %s" % (rset == mset))
only_res = sorted(rset - mset)
only_mine = sorted(mset - rset)
print("only-in-resolve: %d   only-in-mine: %d" % (len(only_res), len(only_mine)))
for c in only_res[:10]:
    print("  RES-ONLY %r -> %s" % (c, res[c]))
for c in only_mine[:10]:
    print("  MINE-ONLY %r -> %s" % (c, mine[c]))

common = rset & mset
cls_diff = [(c, res[c], mine[c]) for c in common if res[c][0] != mine[c][0]]
scope_diff = [(c, res[c], mine[c]) for c in common if res[c][1] != mine[c][1]]
print("class disagreements: %d" % len(cls_diff))
print("scope disagreements: %d" % len(scope_diff))
for c, r, m in cls_diff[:20]:
    print("  CLS %r resolve=%s mine=%s" % (c, r, m))
for c, r, m in scope_diff[:20]:
    print("  SCOPE %r resolve=%s mine=%s" % (c, r, m))

# class totals from resolve.py TSV
from collections import Counter
print("resolve.py class totals: %s" % dict(Counter(v[0] for v in res.values())))
print("my class totals:         %s" % dict(Counter(v[0] for v in mine.values())))
