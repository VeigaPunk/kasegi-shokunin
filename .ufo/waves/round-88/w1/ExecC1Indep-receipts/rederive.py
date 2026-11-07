#!/usr/bin/env python3
"""Independent C1 re-derivation (no import of build-map.py / knowledge-meter.py).
Reads scope at base rev via `git show` in LANE, builds a --shared clone for
resolve.classify context, re-implements M8 from the docstring definition."""
import json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "6beead9148945fa695cf3139e8fc9d8e91cc5fd0"
CLONE = sys.argv[1]  # shared clone checked out at BASE (asserted by caller)
KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")
PATHLIKE = re.compile(r"^[\w./~-]+\.(?:md|mjs|js|py|json|jsonl|txt|tsv|sh)(?::[\d,-]+)?$")
BACKTICK = re.compile(r"`([^`]+)`")

def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args),
                          capture_output=True, text=True, check=True).stdout

def idents(line):
    spans = re.findall(r"`([^`]+)`", line) + re.findall(r'"([^"]+)"', line)
    out = set()
    for sp in spans:
        if PATHLIKE.match(sp.strip()):
            continue
        out |= set(WORD.findall(sp))
    return out

# scope files at base
names = [p for p in git("ls-tree", "--name-only", BASE, "corpus/knowledge/").split("\n")
         if p.endswith(".md") and p.count("/") == 2]
bfiles = {p: git("show", "%s:%s" % (BASE, p)) for p in names}
print("scope files:", len(bfiles))

# tracked files at base
tracked = [p for p in git("ls-tree", "-r", "--name-only", BASE).split("\n") if p]
bybase = {}
for p in tracked:
    if not p.startswith(".ufo/"):
        bybase.setdefault(os.path.basename(p), []).append(p)

# tokens: every backticked span matching KEY, gathered from scope lines
tok_lines = {}  # token -> set of (file, lineno)
for rel, text in bfiles.items():
    for i, ln in enumerate(text.split("\n"), 1):
        for sp in BACKTICK.findall(ln):
            sp = sp.strip()
            if KEY.match(sp):
                tok_lines.setdefault(sp, set()).add((rel, i))
print("distinct backticked .md tokens:", len(tok_lines))

# classify each token with lane resolve.py against the base clone
sys.path.insert(0, os.path.join(CLONE, "corpus", "instruments"))
import resolve as R
mirror = os.path.expanduser(R.MIRROR_ROOT)
print("mirror_absent:", R.MIRROR_ABSENT)
cls = {t: R.classify(t, CLONE, mirror)[0] for t in sorted(tok_lines)}

repair, excluded, other = {}, {}, {}
for tok in sorted(tok_lines):
    m = KEY.match(tok)
    name, lo, hi = m.group(1), m.group(2), m.group(3)
    if cls[tok] != "GONE":
        other[tok] = "classify:%s" % cls[tok]
        continue
    holders = bybase.get(name, [])
    if holders != ["corpus/knowledge/" + name]:
        if holders:
            if len(holders) == 1:
                excluded[tok] = "not-a-knowledge-entry:%s" % holders[0]
            else:
                excluded[tok] = "basename-not-unique:%d" % len(holders)
        else:
            other[tok] = "basename-untracked (builder: silent skip)"
        continue
    path = holders[0]
    if lo is not None:
        tgt = bfiles.get(path)
        nlines = len(tgt.splitlines()) if tgt is not None else 0
        lo_i, hi_i = int(lo), int(hi) if hi else int(lo)
        if not (1 <= lo_i <= hi_i <= nlines):
            other[tok] = "anchor-out-of-range:%s/%d" % (tok, nlines)
            continue
        tw = set(WORD.findall("\n".join(tgt.split("\n")[lo_i - 1:hi_i])))
        cites = [ln for txt in bfiles.values() for ln in txt.split("\n") if "`%s`" % tok in ln]
        fails = sum(1 for ln in cites if not (idents(ln) & tw))
        if not cites or fails:
            excluded[tok] = "anchor-content-drift:no shared identifier on %d/%d citing lines" % (fails, len(cites))
            continue
    repair[tok] = path if lo is None else "%s:%s" % (
        path, lo if hi is None else "%s-%s" % (lo, hi))

print("repair:", len(repair), "excluded:", len(excluded), "other:", len(other))
print("other detail:")
for k, v in sorted(other.items()):
    print("  OTHER", k, v, cls[k])

json.dump(repair, open(os.path.join(os.path.dirname(CLONE), "my-repair.json"), "w"), indent=1, sort_keys=True)
json.dump(excluded, open(os.path.join(os.path.dirname(CLONE), "my-excluded.json"), "w"), indent=1, sort_keys=True)
json.dump(other, open(os.path.join(os.path.dirname(CLONE), "my-other.json"), "w"), indent=1, sort_keys=True)
json.dump(cls, open(os.path.join(os.path.dirname(CLONE), "my-classify.json"), "w"), indent=1, sort_keys=True)
print("WROTE my-*.json beside clone dir")
