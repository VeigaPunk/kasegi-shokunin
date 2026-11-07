#!/usr/bin/env python3
"""Read-only citation audits supporting the round-94 ReviewC1Labels seat.

1. Prior-label pending check: every edit row in the round-88/89/90/91/92 label
   artefacts whose old key is still present on its citing line at the C1 landing.
2. Scans of the 197 `corpus/knowledge/*.md:N[-M]` citation occurrences at the
   landing for provable anchor defects:
   a. table rows whose key-cell identifier(s) appear nowhere in the anchor;
   b. rows whose backticked identifiers appear nowhere in the anchor;
   c. anchors that start mid-sentence and are <=3 lines (off-by-one class);
   d. blank / structural-only anchors.
3. The r88 WRONG/UNCLEAR anchors still cited at the landing.

Reads committed bytes with `git show`; writes nothing.
"""
import os
import re
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "d51220aeb4a538b7b211bb2629e83210669cd56d"
BASE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves"

paths = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", REV, "corpus/knowledge/"],
                       capture_output=True, text=True, check=True).stdout.split()
F = {}
for p in paths:
    if p.endswith(".md"):
        F[p.split("/")[-1]] = subprocess.run(
            ["git", "-C", LANE, "show", "%s:%s" % (REV, p)],
            capture_output=True, text=True, check=True).stdout.split("\n")

CIT = re.compile(r"`(corpus/knowledge/([A-Za-z0-9._-]+\.md)):(\d+)(?:-(\d+))?`")
TICK = re.compile(r"`([^`\n]+)`")


def anchor(p, a, b):
    if p not in F or a < 1 or b > len(F[p]) or a > b:
        return None
    return "\n".join(F[p][a - 1:b])


print("== 1. prior label artefacts: edit rows whose old key is still present")
total_pending = 0
for tag, path in [
    ("tranche5", BASE + "/round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv"),
    ("r90seat", BASE + "/round-90/w1/ReviewC1Sites-receipts/round91-labels.tsv"),
    ("r91seat", BASE + "/round-91/w1/ReviewC1Labels-receipts/round92-labels.tsv"),
    ("r92seat", BASE + "/round-92/w1/ReviewC1Labels-receipts/round93-labels.tsv"),
]:
    pending = []
    for ln in open(path, encoding="utf-8"):
        if not ln.strip() or ln.startswith("#") or ln.startswith("key\t") or ln.startswith("line\t"):
            continue
        c = ln.rstrip("\n").split("\t")
        if len(c) != 5:
            continue
        if tag == "tranche5":
            key, site, verdict = c[0], c[1], c[2]
        else:
            site, key, verdict = c[0], c[1], c[2]
        if verdict in ("CORRECT", "MENTION"):
            continue
        if ":" not in site:
            continue
        f, n = site.rsplit(":", 1)
        f = f.replace("corpus/knowledge/", "")
        if f not in F or not n.isdigit():
            continue
        if key in F[f][int(n) - 1]:
            pending.append((site, key, verdict))
    print("  %s pending=%d" % (tag, len(pending)))
    for p in pending:
        print("   ", p)
    total_pending += len(pending)
print("  total pending=%d" % total_pending)

print("== 2a. table rows whose key-cell identifiers are absent from the anchor")
nokey = []
for name, L in F.items():
    for i, line in enumerate(L, 1):
        if not line.startswith("|"):
            continue
        cells = line.split("|")
        if len(cells) < 3:
            continue
        toks = set()
        for t in TICK.findall(cells[1]):
            for w in re.findall(r"[A-Za-z_][A-Za-z0-9_.]{2,}", t):
                toks.add(w)
        for w in re.findall(r"[A-Z][A-Za-z0-9_]{3,}|[A-Za-z]+_[A-Za-z0-9_]+", cells[1]):
            toks.add(w)
        if not toks:
            continue
        for m in CIT.finditer(line):
            p, a, b = m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
            txt = anchor(p, a, b)
            if txt is None:
                continue
            if not any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(w) + r"(?![A-Za-z0-9_])", txt) for w in toks):
                nokey.append((name, i, p, a, b, sorted(toks)[:6]))
print("  count=%d" % len(nokey))
for r in nokey:
    print("   ", r)

print("== 2b. rows whose backticked identifiers are absent from the anchor")
noid = []
for name, L in F.items():
    for i, line in enumerate(L, 1):
        ids = set()
        for t in TICK.findall(line):
            if "corpus/knowledge/" in t or t.startswith("SKILL.md"):
                continue
            for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", t):
                ids.add(w)
        if not ids:
            continue
        for m in CIT.finditer(line):
            p, a, b = m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
            txt = anchor(p, a, b)
            if txt is None:
                continue
            if not any(re.search(r"(?<![A-Za-z0-9_])" + re.escape(w) + r"(?![A-Za-z0-9_])", txt) for w in ids):
                noid.append((name, i, p, a, b, len(ids)))
print("  count=%d" % len(noid))
for r in noid:
    print("   ", r)

print("== 2c. anchors starting mid-sentence, <=3 lines")
mid = []
for name, L in F.items():
    for i, line in enumerate(L, 1):
        for m in CIT.finditer(line):
            p, a, b = m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
            if p not in F or b > len(F[p]) or b - a > 2:
                continue
            first = F[p][a - 1].strip()
            if not first:
                continue
            if re.match(r"^(?:[a-z)\]}»”]|which |and |or |but |where |when |that |the [a-z])", first):
                mid.append((name, i, p, a, b, first[:90]))
print("  count=%d" % len(mid))
for r in mid:
    print("   ", r)

print("== 2d. blank / structural-only anchors")
bad = []
for name, L in F.items():
    for i, line in enumerate(L, 1):
        for m in CIT.finditer(line):
            p, a, b = m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
            if p not in F or b > len(F[p]):
                continue
            seg = F[p][a - 1:b]
            if not re.sub(r"[\s|#>\-\*`_—–:.]", "", "\n".join(seg)):
                bad.append((name, i, p, a, b))
            elif not seg[0].strip() or not re.search(r"[A-Za-z0-9]", seg[0]):
                bad.append((name, i, p, a, b, "BLANKSTART"))
print("  count=%d" % len(bad))
for r in bad:
    print("   ", r)

print("== 3. r88 WRONG/UNCLEAR anchors still cited at the landing")
r88 = {}
for ln in open(BASE + "/round-88/l1/r88-semantic-labels.tsv", encoding="utf-8"):
    if ln.startswith("#") or not ln.strip():
        continue
    c = ln.rstrip("\n").split("\t")
    r88[c[0]] = c[1]
still = []
for name, L in F.items():
    for i, line in enumerate(L, 1):
        for m in CIT.finditer(line):
            key = "%s:%s" % (m.group(2), m.group(3)) + ("-" + m.group(4) if m.group(4) else "")
            if key in r88 and r88[key] != "CORRECT":
                still.append((name, i, key, r88[key]))
print("  count=%d" % len(still))
for r in still:
    print("   ", r)
