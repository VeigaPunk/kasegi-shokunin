#!/usr/bin/env python3
"""Independent re-derivation of the kasegi citation census.

Written from resolve.py's documented extraction rule (module docstring), not by
importing or copying the lane instrument. Counts distinct backticked path-like
citations per scope, classifies lane-relative tokens that exist in the extract
as INTERNAL, and reclassifies a `..` walk-out whose realpath leaves the extract
as HOST-OWNED (out of the pinned numerator, still in the denominator).
"""
import glob
import os
import re
import sys

root = os.path.realpath(sys.argv[1])
home = os.path.abspath(sys.argv[2])
os.environ["HOME"] = home

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
ANCHOR = re.compile(r":\d+(?:[-\u2013]\d+)?$")
SYM = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PH = re.compile(r"<[^<>]*>")
META = "*?["


def pathlike(tok):
    t = tok.strip().rstrip(".,;:")
    if not t or (" " in t and "/" not in t):
        return False
    if t.startswith(("http", "xd://", "skill://")):
        return False
    if EXTS.search(t):
        return True
    if t.endswith("/"):
        return True
    if t.startswith("~/") or t.startswith("/"):
        return True
    if PATHY.search(t):
        return True
    if EXTS.search(ANCHOR.sub("", t)):
        return True
    return False


def strip_anchor(t):
    b = ANCHOR.sub("", t)
    if b != t:
        return b
    b2 = SYM.sub("", t)
    return b2 if b2 != t else t


def brace_expand(p):
    m = re.search(r"\{([^{}]*)\}", p)
    if not m:
        return [p]
    out = []
    alts = sorted(m.group(1).split(","))
    for alt in alts:
        if alt.strip() or (not alt and len(alts) > 1):
            out.extend(brace_expand(p[: m.start()] + alt + p[m.end():]))
        if len(out) > 64:
            break
    return sorted(out)[:64]


def exists_any(p):
    p = os.path.expanduser(p)
    if os.path.exists(p):
        return p
    cands = brace_expand(p) if ("{" in p and "}" in p) else []
    for c in cands:
        if os.path.exists(c):
            return c
    for c in cands:
        q = PH.sub("*", c)
        if any(ch in q for ch in META):
            for hit in sorted(glob.glob(q, recursive=True)):
                if os.path.exists(hit):
                    return hit
    q = PH.sub("*", p)
    if any(ch in q for ch in META):
        for c in sorted(glob.glob(q, recursive=True)):
            if os.path.exists(c):
                return c
    return None


files = [os.path.join(root, "SKILL.md")]
for dirpath, dirnames, filenames in os.walk(os.path.join(root, "corpus")):
    dirnames.sort()
    for fn in sorted(filenames):
        if fn.endswith(".md"):
            cand = os.path.join(dirpath, fn)
            if os.path.relpath(cand, root) != os.path.join("corpus", "instruments", "citation-survival.md"):
                files.append(cand)

cites = {}
for f in files:
    if not os.path.isfile(f):
        continue
    rel = os.path.relpath(f, root)
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            for m in TOKEN.finditer(line):
                t = m.group(1).strip().rstrip(".,;:")
                if not pathlike(t):
                    continue
                e = cites.setdefault(t, set())
                e.add("SKILL" if rel == "SKILL.md" else "CORPUS")

rows = []
for cit in sorted(cites):
    base = strip_anchor(cit)
    klass = "GONE"
    resolved = ""
    if base.startswith("~") or base.startswith("/"):
        if exists_any(base):
            klass = "RESOLVES"
            resolved = exists_any(base)
    else:
        p = exists_any(os.path.join(root, base))
        if p:
            klass = "INTERNAL"
            resolved = p
            if any(seg == ".." for seg in cit.replace("\\", "/").split("/")):
                rp = os.path.realpath(resolved)
                if not (rp == root or rp.startswith(root + os.sep)):
                    klass = "HOST-OWNED"
    rows.append((cit, klass, resolved, cites[cit]))

scopes = {"SKILL": [], "CORPUS": [], "LANE": [(c, k) for c, k, _, _ in rows]}
for cit, klass, resolved, sc in rows:
    if "SKILL" in sc:
        scopes["SKILL"].append((cit, klass))
    if "CORPUS" in sc:
        scopes["CORPUS"].append((cit, klass))

print("distinct=%d" % len(rows))
for name in ("SKILL", "CORPUS", "LANE"):
    sel = scopes[name]
    num = sum(1 for _, k in sel if k == "INTERNAL")
    print("%s pinned INTERNAL %d/%d" % (name, num, len(sel)))
host = sum(1 for _, k, _, _ in rows if k in ("RESOLVES", "MIRROR-EQUIVALENT"))
conf = sum(1 for _, k, _, _ in rows if k == "HOST-OWNED")
print("host_owned=%d confined=%d" % (host, conf))
for name in ("SKILL", "CORPUS", "LANE"):
    sel = scopes[name]
    hn = sum(1 for _, k in sel if k in ("INTERNAL", "RESOLVES", "MIRROR-EQUIVALENT"))
    print("%s host-incl %d/%d" % (name, hn, len(sel)))
