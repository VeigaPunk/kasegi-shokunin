#!/usr/bin/env python3
"""CriticHarm r97 check 2: independent line/token audit of the C1 landing.

For every corpus/knowledge/*.md file:
  * base and tip must have identical line counts;
  * the set of differing line numbers must equal the map's site set;
  * each differing line must equal the base line with every `old` -> `new`
    substitution applied (byte-exact, backticks included);
  * the backticked-token multiset delta per changed line must be exactly
    -key xN / +label xN;
  * every other corpus/knowledge file must be byte-identical.
"""
import collections
import os
import re
import sys

BASE = sys.argv[1]
TIP = sys.argv[2]
MAP = sys.argv[3]
KN = "corpus/knowledge"
TOKEN = re.compile(r"`([^`\n]+)`")

rows = []
with open(MAP, encoding="utf-8") as fh:
    for line in fh:
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        site, key, old, new = line.split("\t")
        path, lineno = site.rsplit(":", 1)
        rows.append((path, int(lineno), key, old, new))

by_file = collections.defaultdict(list)
for r in rows:
    by_file[r[0]].append(r)

fail = []
base_files = sorted(f for f in os.listdir(os.path.join(BASE, KN)) if f.endswith(".md"))
tip_files = sorted(f for f in os.listdir(os.path.join(TIP, KN)) if f.endswith(".md"))
if base_files != tip_files:
    fail.append("knowledge file set differs base vs tip")

touched = set(by_file)
changed_sites = 0
changed_lines = 0
token_delta_ok = 0
for fname in base_files:
    rel = KN + "/" + fname
    b = open(os.path.join(BASE, rel), "rb").read()
    t = open(os.path.join(TIP, rel), "rb").read()
    if rel not in touched:
        if b != t:
            fail.append("UNTOUCHED-BUT-CHANGED %s" % rel)
        continue
    bl = b.split(b"\n")
    tl = t.split(b"\n")
    if len(bl) != len(tl):
        fail.append("LINE-COUNT %s base=%d tip=%d" % (rel, len(bl), len(tl)))
        continue
    want = collections.defaultdict(list)
    for r in by_file[rel]:
        want[r[1]].append(r)
    diff = {i + 1 for i, (x, y) in enumerate(zip(bl, tl)) if x != y}
    if diff != set(want):
        fail.append("SITE-SET %s diff=%s map=%s" % (rel, sorted(diff), sorted(want)))
    for lineno in sorted(diff):
        changed_lines += 1
        rs = want.get(lineno)
        if rs is None:
            continue
        changed_sites += len(rs)
        exp = bl[lineno - 1].decode()
        for _, _, key, old, new in rs:
            exp = exp.replace(old, new)
        if exp.encode() != tl[lineno - 1]:
            fail.append("EDIT-NOT-EXACT %s:%d" % (rel, lineno))
            continue
        bt = collections.Counter(TOKEN.findall(bl[lineno - 1].decode()))
        tt = collections.Counter(TOKEN.findall(tl[lineno - 1].decode()))
        back = {k: v for k, v in (bt - tt).items()}
        fwd = {k: v for k, v in (tt - bt).items()}
        want_back = {}
        want_fwd = {}
        ok = True
        for _, _, key, old, new in rs:
            n = bt[key]
            if n < 1:
                fail.append("KEY-ABSENT %s:%d key=%s" % (rel, lineno, key))
                ok = False
                break
            want_back[key] = want_back.get(key, 0) + n
            lab = new.strip("`")
            want_fwd[lab] = want_fwd.get(lab, 0) + n
        if not ok:
            continue
        if back != want_back or fwd != want_fwd:
            fail.append("TOKEN-DELTA %s:%d back=%s fwd=%s want_back=%s want_fwd=%s"
                        % (rel, lineno, back, fwd, want_back, want_fwd))
            continue
        token_delta_ok += 1

print("files_touched=%d map_rows=%d changed_lines=%d exact_sites=%d token_delta_ok=%d"
      % (len(touched), len(rows), changed_lines, changed_sites, token_delta_ok))
print("FAILURES=%d" % len(fail))
for f in fail:
    print("FAIL " + f)
sys.exit(1 if fail else 0)
