#!/usr/bin/env python3
"""Independent citation census for Kasegi round-98 C1 verification.

Clean-room re-derivation of the census-of-record numbers from the raw
`git archive e2caf4a...` extract, WITHOUT importing or running the lane's
resolve.py / census-at-rev.py. Implements the extraction + classification rule
as documented in the lane's instrument docstrings (backticked path-like tokens,
INTERNAL = lane-relative token that exists in the extract).

Usage: mycensus.py <extract-root>
"""
import glob as globmod
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1])

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([–-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
GLOBMETA = "*?["
BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
MIRROR_CANDIDATES = ("~/Projects/the-bounty-hunter",
                     "~/Projects/origin-work/the-bounty-hunter")
GENERATED_REPORT = os.path.normpath("corpus/instruments/citation-survival.md")


def derive_mirror():
    env = os.environ.get("KASEGI_MIRROR")
    if env:
        return os.path.expanduser(env)
    for c in MIRROR_CANDIDATES:
        if os.path.isdir(os.path.expanduser(c)):
            return c
    return MIRROR_CANDIDATES[0]


MIRROR_ROOT = derive_mirror()


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
        return b, "line"
    b2 = SYMANCHOR.sub("", tok)
    if b2 != tok:
        return b2, "symbol"
    return tok, ""


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


def _first_existing(pattern):
    """Lazy equivalent of sorted(glob.glob(pattern, recursive=True)) first-existing.

    glob.iglob yields the same match set as glob.glob but without materializing
    the full list, so peak memory stays O(depth) instead of O(matches). The
    existence boolean is identical: resolve.py takes the sorted-first match that
    os.path.exists accepts; any such match existing is equivalent for the class
    decision (classify only tests method truthiness, never the path)."""
    for hit in globmod.iglob(pattern, recursive=True):
        if os.path.exists(hit):
            return hit
    return None


def exists_any(path):
    p = os.path.expanduser(path)
    if os.path.exists(p):
        return "literal", p
    cands = brace_expand(p) if ("{" in p and "}" in p) else []
    for c in cands:
        if os.path.exists(c):
            return "brace", c
    for c in cands:
        qc = PLACEHOLDER.sub("*", c)
        if any(ch in qc for ch in GLOBMETA):
            hit = _first_existing(qc)
            if hit is not None:
                return "brace-glob", hit
    q = PLACEHOLDER.sub("*", p)
    if any(ch in q for ch in GLOBMETA):
        hit = _first_existing(q)
        if hit is not None:
            return "glob", hit
    return None, None


def mirror_suffix(base):
    for c in MIRROR_CANDIDATES:
        for root in (c, os.path.expanduser(c)):
            if base == root:
                return ""
            if base.startswith(root + "/"):
                return base[len(root) + 1:].lstrip("/")
    return None


def bounty_suffix(base):
    for prefix in BOUNTY_PREFIXES:
        for root in (prefix, os.path.expanduser(prefix)):
            root = root.rstrip("/")
            if base == root:
                return ""
            if base.startswith(root + "/"):
                return base[len(root) + 1:].lstrip("/")
    return None


def under_mirror(path, mirror_root):
    r = os.path.realpath(os.path.expanduser(mirror_root))
    p = os.path.realpath(path)
    return os.path.commonpath((r, p)) == r


def classify(tok, lane_root, mirror_root):
    base, _anchor = strip_anchor(tok)
    suffix = bounty_suffix(base)
    if suffix is not None:
        m, p = exists_any(base)
        if m:
            return "RESOLVES"
        m, p = exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
        if m and under_mirror(p, mirror_root):
            return "MIRROR-EQUIVALENT"
        return "GONE"
    sfx = mirror_suffix(base)
    if sfx is not None:
        m, p = exists_any(os.path.join(mirror_root, sfx) if sfx else mirror_root)
        if m and under_mirror(p, mirror_root):
            return "RESOLVES"
        return "GONE"
    if base.startswith("~") or base.startswith("/"):
        m, p = exists_any(base)
        return "RESOLVES" if m else "GONE"
    m, p = exists_any(os.path.join(lane_root, base))
    if m:
        return "INTERNAL"
    if base not in ("", ".", ".."):
        m, p = exists_any(os.path.join(mirror_root, base))
        if m and under_mirror(p, mirror_root):
            return "MIRROR-EQUIVALENT"
    return "GONE"


def collect(lane_root):
    repo = os.path.abspath(os.path.expanduser(lane_root))
    files = [os.path.join(repo, "SKILL.md")]
    corpus = os.path.join(repo, "corpus")
    for dirpath, dirnames, filenames in os.walk(corpus):
        dirnames.sort()
        for fn in sorted(filenames):
            candidate = os.path.join(dirpath, fn)
            if fn.endswith(".md") and os.path.relpath(candidate, repo) != GENERATED_REPORT:
                files.append(candidate)
    cites = {}
    for f in files:
        if not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, repo)
        with open(f, "r", encoding="utf-8") as fh:
            for line in fh:
                for m in TOKEN.finditer(line):
                    t = m.group(1).strip().rstrip(".,;:")
                    if not is_pathlike(t):
                        continue
                    e = cites.setdefault(t, {"files": set(), "occ": 0})
                    e["files"].add(rel)
                    e["occ"] += 1
    return repo, cites


def main():
    repo, cites = collect(ROOT)
    sys.stderr.write("collected %d distinct citations\n" % len(cites))
    sys.stderr.flush()
    rows = []
    for i, tok in enumerate(sorted(cites)):
        cls = classify(tok, repo, MIRROR_ROOT)
        if i % 500 == 0:
            sys.stderr.write("classified %d/%d\n" % (i, len(cites)))
            sys.stderr.flush()
        files = sorted(cites[tok]["files"])
        scopes = ("SKILL" if "SKILL.md" in files else "") + \
                 ("+CORPUS" if any(f.startswith("corpus/") for f in files) else "")
        rows.append({"cite": tok, "cls": cls, "files": files, "scopes": scopes,
                     "occ": cites[tok]["occ"]})

    def rate(scope, classes):
        sel = [r for r in rows if scope == "ALL" or scope in r["scopes"]]
        num = [r for r in sel if r["cls"] in classes]
        return len(num), len(sel)

    PIN = {"INTERNAL"}
    HOST = {"INTERNAL", "RESOLVES", "MIRROR-EQUIVALENT"}
    host_owned = sum(1 for r in rows if r["cls"] in ("RESOLVES", "MIRROR-EQUIVALENT"))

    citing_files = len({f for r in rows for f in r["files"]})
    total_occ = sum(r["occ"] for r in rows)

    print("extract root: %s" % ROOT)
    print("mirror root: %s (absent=%s)" % (MIRROR_ROOT,
          "yes" if not os.path.isdir(os.path.expanduser(MIRROR_ROOT)) else "no"))
    print("distinct citations: %d (total occurrences: %d; citing files: %d)"
          % (len(rows), total_occ, citing_files))
    from collections import Counter
    print("class totals: %s" % dict(Counter(r["cls"] for r in rows)))
    print("host-owned (RESOLVES+MIRROR-EQUIVALENT): %d" % host_owned)
    print()
    print("scope            pinned(INTERNAL)      host-inclusive")
    for tag, scope in (("SKILL", "SKILL"), ("CORPUS", "+CORPUS"), ("LANE", "ALL")):
        pn, pm = rate(scope, PIN)
        hn, hm = rate(scope, HOST)
        print("%-7s  %4d/%-5d = %6.2f%%   %4d/%-5d = %6.2f%%"
              % (tag, pn, pm, 100.0 * pn / pm if pm else 0,
                 hn, hm, 100.0 * hn / hm if hm else 0))
    print()
    print("pinned rate (INTERNAL only; revision-stable): "
          "SKILL %d/%d = %.2f%% | corpus %d/%d = %.2f%% | lane %d/%d = %.2f%%" % (
              *rate("SKILL", PIN), 100.0 * rate("SKILL", PIN)[0] / rate("SKILL", PIN)[1],
              *rate("+CORPUS", PIN), 100.0 * rate("+CORPUS", PIN)[0] / rate("+CORPUS", PIN)[1],
              *rate("ALL", PIN), 100.0 * rate("ALL", PIN)[0] / rate("ALL", PIN)[1]))
    print("host-inclusive rate (resolve.py's definition): "
          "SKILL %d/%d = %.2f%% | corpus %d/%d = %.2f%% | lane %d/%d = %.2f%%" % (
              *rate("SKILL", HOST), 100.0 * rate("SKILL", HOST)[0] / rate("SKILL", HOST)[1],
              *rate("+CORPUS", HOST), 100.0 * rate("+CORPUS", HOST)[0] / rate("+CORPUS", HOST)[1],
              *rate("ALL", HOST), 100.0 * rate("ALL", HOST)[0] / rate("ALL", HOST)[1]))
    print("host-owned inputs: %d" % host_owned)
    # dump rows for diffing against the lane instrument's TSV
    with open(os.path.join(ROOT, "..", "mycensus-rows.tsv"), "w", encoding="utf-8") as fh:
        fh.write("citation\tclass\tscopes\toccurrences\n")
        for r in rows:
            fh.write("%s\t%s\t%s\t%d\n" % (r["cite"], r["cls"], r["scopes"], r["occ"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
