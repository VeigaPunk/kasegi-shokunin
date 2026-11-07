#!/usr/bin/env python3
"""Independent re-derivation of the kasegi citation census over a tree extract.

Fast variant: absolute-path citations are counted in the denominators but their
existence is NOT tested (that is where resolve.py's unbounded `~/Projects/**`
recursive glob burns minutes); only relative tokens are resolved under the tree
root, which is exactly what the INTERNAL-only pinned numerator needs.
"""
import glob as globmod
import os
import re
import sys

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([\u2013-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
GLOBMETA = "*?["
GENERATED = os.path.normpath("corpus/instruments/citation-survival.md")


def is_pathlike(tok):
    t = tok.strip().rstrip(".,;:")
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
    if EXTS.search(LINEANCHOR.sub("", t)):
        return True
    return False


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
    alts = sorted(m.group(1).split(","))
    for alt in alts:
        if alt.strip() or (not alt and len(alts) > 1):
            out.extend(brace_expand(path[: m.start()] + alt + path[m.end():]))
        if len(out) > 64:
            break
    return sorted(out)[:64]


def exists_any(path):
    p = os.path.expanduser(path)
    if os.path.exists(p):
        return "literal"
    cands = brace_expand(p) if ("{" in p and "}" in p) else []
    for c in cands:
        if os.path.exists(c):
            return "brace"
    for c in cands:
        qc = PLACEHOLDER.sub("*", c)
        if any(ch in qc for ch in GLOBMETA):
            for hit in sorted(globmod.glob(qc, recursive=True)):
                if os.path.exists(hit):
                    return "brace-glob"
    q = PLACEHOLDER.sub("*", p)
    if any(ch in q for ch in GLOBMETA):
        for c in sorted(globmod.glob(q, recursive=True)):
            if os.path.exists(c):
                return "glob"
    return None


def collect(root):
    files = [os.path.join(root, "SKILL.md")]
    for dirpath, dirnames, filenames in os.walk(os.path.join(root, "corpus")):
        dirnames.sort()
        for fn in sorted(filenames):
            cand = os.path.join(dirpath, fn)
            if fn.endswith(".md") and os.path.relpath(cand, root) != GENERATED:
                files.append(cand)
    cites = {}
    for f in files:
        if not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, root)
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                for m in TOKEN.finditer(line):
                    t = m.group(1).strip().rstrip(".,;:")
                    if not is_pathlike(t):
                        continue
                    e = cites.setdefault(t, {"files": set(), "occ": 0})
                    e["files"].add(rel)
                    e["occ"] += 1
    return cites


def main(argv):
    root = os.path.abspath(argv[1])
    cites = collect(root)
    rows = []
    for tok, e in cites.items():
        base = strip_anchor(tok)
        if base.startswith("~") or base.startswith("/"):
            cls = "ABS"  # existence not tested (host-owned; not the pinned numerator)
        else:
            cls = "INTERNAL" if exists_any(os.path.join(root, base)) else "GONE"
        rows.append((tok, cls, e["files"]))

    def scopes(files):
        s = set()
        if "SKILL.md" in files:
            s.add("SKILL")
        if any(f.startswith("corpus/") for f in files):
            s.add("CORPUS")
        return s

    totals = {}
    for _, cls, _ in rows:
        totals[cls] = totals.get(cls, 0) + 1
    out = {}
    for tag in ("SKILL", "CORPUS", "ALL"):
        sel = [r for r in rows if tag == "ALL" or tag in scopes(r[2])]
        internal = [r for r in sel if r[1] == "INTERNAL"]
        out[tag] = (len(internal), len(sel))
    nfiles = len({f for _, _, fs in rows for f in fs})
    print("distinct=%d internal=%d gone=%d abs=%d files=%d" % (
        len(rows), totals.get("INTERNAL", 0), totals.get("GONE", 0),
        totals.get("ABS", 0), nfiles))
    for tag in ("SKILL", "CORPUS", "ALL"):
        n, m = out[tag]
        print("%s internal=%d/%d" % (tag, n, m))
    # the three ../ citations that resolve outside the tree
    for tok in ("../", "../MISSION.md:49-56",
                "../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kasegi*.md"):
        if tok in cites:
            base = strip_anchor(tok)
            print("DOTDOT %r -> %s" % (tok, exists_any(os.path.join(root, base))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
