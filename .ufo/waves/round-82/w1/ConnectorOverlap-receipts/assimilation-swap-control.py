#!/usr/bin/env python3
"""2x2 label/content swap control over the frozen r82 assimilation check.

Frozen form reproduced byte-identically: reg-ids = sorted ids of corpus/SOURCES.md
(S001-S116); staged-ids = sorted ids of the shokuknow staged file (S031-S124);
collisions = their intersection (86).

Cells (frozen form, real data):
  A same label, same source      = 1  (S042)
  B same label, different source = 85
  C different label, same source = 20
  D different label, different   = 73 (the staged rows with no lane counterpart)

Materialised variants of the staged table, each re-run through the same three
extraction lines:
  renumber    every source string kept, every id shifted +100  -> intersection 0
  contentswap every id kept, every source cell replaced         -> intersection 86
The verdict therefore tracks the label, not the source.
"""
import re

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
STG = "/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md"


def rows(path):
    out = []
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("| S") and ln.count("|") >= 5:
            out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


R, T = rows(LANE + "/corpus/SOURCES.md"), rows(STG)
reg = [c[0] for c in R]


def url(cell):
    m = re.search(r"https?://\S+", cell)
    return m.group(0).rstrip(".,;") if m else cell.split("—")[0].strip()


lane_by_url = {}
for c in R:
    lane_by_url.setdefault(url(c[1]), []).append(c[0])


def check(staged_rows):
    stg = [c[0] for c in staged_rows]
    return len(set(reg) & set(stg))


same_source = [(c[0], lane_by_url[url(c[1])]) for c in T if url(c[1]) in lane_by_url]
both = [(s, l) for s, l in same_source if s in l]
print("FROZEN  reg=%d staged=%d collisions=%d" % (len(reg), len(T), check(T)))
print("CELL A same-label/same-source = %d %s" % (len(both), both))
print("CELL B same-label/diff-source = %d" % (len(set(reg) & {c[0] for c in T}) - len(both)))
print("CELL C diff-label/same-source = %d" % (len(same_source) - len(both)))
print("CELL D diff-label/diff-source = %d" % (len(T) - len(same_source)))

renum = [[("S%03d" % (int(c[0][1:]) + 100))] + c[1:] for c in T]
cswap = [c[:1] + ["VARIANT-B source %s — no URL" % c[0]] + ["x"] * (len(c) - 2) for c in T]
print("VARIANT renumber(+100)  collisions=%d   (same-source pairs still %d)"
      % (check(renum), len(same_source)))
print("VARIANT contentswap     collisions=%d   (same-source pairs now %d)"
      % (check(cswap), sum(1 for c in cswap if url(c[1]) in lane_by_url)))
