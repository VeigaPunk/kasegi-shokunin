#!/usr/bin/env python3
"""ExecC1Indep — independent re-derivation of the round-99 C1 census.

Own extractor + own classifier. Reads ONLY the git-archive extract of
a3db47e71fe292c03b00ba11f38cccbec45d3966 given as argv[1]. No lane
instrument is imported or executed.

Spec (pinned by the census-of-record header and the density.py path-like rule):
  scope   : SKILL.md + corpus/**/*.md, excluding corpus/instruments/citation-survival.md
  token   : backticked span, strip surrounding whitespace, rstrip ".,;:",
            path-like when (a) ends in a code/doc extension, (b) ends '/',
            (c) starts '/' or '~/', (d) contains '/', '<', '{', '~' or '..',
            (e) ends in a :NN / :NN-MM anchor over an extension base;
            space-bearing tokens need '/'; http/xd:// skill:// URLs dropped.
  INTERNAL: lane-relative BASE resolving inside the extract (literal,
            deterministic brace expansion, then <...>->* glob; first hit wins).
  HOST-OWNED (R157): INTERNAL citation carrying a `..` segment whose realpath
            escapes the extract -> leaves the pinned numerator, stays in the
            denominator.
  pinned  : per scope, numerator = INTERNAL, denominator = all distinct
            path-like citations appearing in that scope.

HOME is pointed at an empty confined dir so `~` expansion touches no host tree.
"""
import glob as globmod
import os
import re
import sys
import tempfile

EXTRACT = os.path.realpath(sys.argv[1])
os.environ["HOME"] = tempfile.mkdtemp(prefix="confined-home-")  # no host reads

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([\u2013-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
GLOBMETA = "*?["
GENERATED = os.path.normpath("corpus/instruments/citation-survival.md")


def pathlike(t):
    # The pinned rule re-normalizes inside the predicate (resolve.py
    # is_pathlike does `t = tok.strip().rstrip(".,;:")` again), so a token
    # like `resolve.py .` becomes key `resolve.py ` (outer rstrip exposes the
    # space) yet still counts via the twice-normalized form.
    t = t.strip().rstrip(".,;:")
    if not t or (" " in t and "/" not in t):
        return False
    if t.startswith("http") or t.startswith("xd://") or t.startswith("skill://"):
        return False
    if EXTS.search(t):
        return True
    if t.endswith("/"):
        return True
    if t.startswith("~/") or t.startswith("/"):
        return True
    if PATHY.search(t):
        return True
    return bool(EXTS.search(LINEANCHOR.sub("", t)))


def strip_anchor(tok):
    b = LINEANCHOR.sub("", tok)
    if b != tok:
        return b
    return SYMANCHOR.sub("", tok)


def brace_expand(path):
    m = re.search(r"\{([^{}]*)\}", path)
    if not m:
        return [path]
    out = []
    for alt in sorted(m.group(1).split(",")):
        if alt.strip() or (not alt and len(m.group(1).split(",")) > 1):
            out.extend(brace_expand(path[:m.start()] + alt + path[m.end():]))
        if len(out) > 64:
            break
    return sorted(out)[:64]


def resolve_relative(base):
    """Own existence ladder: literal, brace, brace-glob, glob. Path or None."""
    p = os.path.join(EXTRACT, base)
    if os.path.exists(p):
        return p
    cands = brace_expand(p) if ("{" in p and "}" in p) else [p]
    for c in cands:
        if c != p and os.path.exists(c):
            return c
    for c in cands:
        q = PLACEHOLDER.sub("*", c)
        if any(ch in q for ch in GLOBMETA):
            for hit in sorted(globmod.glob(q, recursive=True)):
                if os.path.exists(hit):
                    return hit
    return None


def resolve_absolute(base):
    """Absolute/~ ladder (informational only; mirrors the other-root class)."""
    p = os.path.expanduser(base)
    if os.path.exists(p):
        return p
    cands = brace_expand(p) if ("{" in p and "}" in p) else [p]
    for c in cands:
        if c != p and os.path.exists(c):
            return c
    for c in cands:
        q = PLACEHOLDER.sub("*", c)
        if any(ch in q for ch in GLOBMETA):
            for hit in sorted(globmod.glob(q, recursive=True)):
                if os.path.exists(hit):
                    return hit
    return None


def collect():
    files = [os.path.join(EXTRACT, "SKILL.md")]
    for dirpath, dirnames, filenames in os.walk(os.path.join(EXTRACT, "corpus")):
        dirnames.sort()
        for fn in sorted(filenames):
            c = os.path.join(dirpath, fn)
            if fn.endswith(".md") and os.path.relpath(c, EXTRACT) != GENERATED:
                files.append(c)
    skill_set, corpus_set = set(), set()
    occ = {}
    scanned = contrib = 0
    for f in files:
        if not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, EXTRACT)
        scanned += 1
        toks = []
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                for m in TOKEN.finditer(line):
                    t = m.group(1).strip().rstrip(".,;:")
                    if pathlike(t):
                        toks.append(t)
        if toks:
            contrib += 1
        target = skill_set if rel == "SKILL.md" else corpus_set
        for t in toks:
            occ[t] = occ.get(t, 0) + 1
            target.add(t)
    return scanned, contrib, skill_set, corpus_set, occ


def main():
    scanned, contrib, skill_set, corpus_set, occ = collect()
    lane_set = skill_set | corpus_set
    classes = {}
    walkout_excluded = []
    external_resolves = 0
    for t in sorted(occ):
        base = strip_anchor(t)
        if base.startswith("~") or base.startswith("/"):
            if resolve_absolute(base) is not None:
                external_resolves += 1
            classes[t] = "EXTERNAL"
            continue
        r = resolve_relative(base)
        if r is None:
            classes[t] = "GONE"
            continue
        if any(seg == ".." for seg in t.replace("\\", "/").split("/")):
            rp = os.path.realpath(r)
            if not (rp == EXTRACT or rp.startswith(EXTRACT + os.sep)):
                classes[t] = "HOST-OWNED"
                walkout_excluded.append(t)
                continue
        classes[t] = "INTERNAL"

    def rate(sel):
        num = sum(1 for t in sel if classes[t] == "INTERNAL")
        return num, len(sel)

    sk = rate(skill_set)
    co = rate(corpus_set)
    la = rate(lane_set)

    def pct(n, m):
        return "%.2f%%" % (100.0 * n / m) if m else "n/a"

    print("MYCENSUS extract=%s" % EXTRACT)
    print("files scanned=%d contributing=%d" % (scanned, contrib))
    print("distinct=%d occurrences=%d" % (len(occ), sum(occ.values())))
    print("pinned: SKILL %d/%d = %s | corpus %d/%d = %s | lane %d/%d = %s" % (
        sk[0], sk[1], pct(*sk), co[0], co[1], pct(*co), la[0], la[1], pct(*la)))
    print("walk-out INTERNAL excluded (HOST-OWNED): %d %s" % (
        len(walkout_excluded), walkout_excluded))
    print("absolute/~ citations resolving (informational): %d" % external_resolves)
    cls = {}
    for t, k in classes.items():
        cls[k] = cls.get(k, 0) + 1
    print("classes: %s" % ", ".join("%s=%d" % kv for kv in sorted(cls.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
