#!/usr/bin/env python3
"""ExecC1Indep — independent re-derivation of round-95 C1, without the lane counter.

Reads only: git objects of the pinned lane repo at BASE/AFTER, the committed
repair map. Writes receipt files next to this script. TMPDIR must point at the
seat scratch; every extracted tree lives there and is removed on exit.

Own implementation of the pinned census classifier (resolve.py semantics:
density.py path-like extraction, bounty/mirror/relative domains, literal/
brace/glob existence), scoped to corpus/knowledge/*.md as the meter scopes it.
"""
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10"
AFTER = "53ec479d71d25cf5be052db794a548a5904564b8"
MAP_REL = ".ufo/waves/round-95/c1/repair-map.tsv"
F_TRI = "corpus/knowledge/triage-thresholds.md"
F_ISO = "corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md"
SNAP = "corpus/source-snapshots/round-30/S041.txt"
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("TMPDIR") or tempfile.gettempdir()

trees = []


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s: %s" % (args[0], r.stderr.decode()[:200]))
    return r.stdout if binary else r.stdout.decode("utf-8")


def blob(rev, rel):
    r = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, rel)], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8")


receipts = {}


def emit(name, text):
    receipts.setdefault(name, []).append(text)


def flush():
    for name, parts in receipts.items():
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as fh:
            fh.write("\n".join(parts) + "\n")


# ---------------------------------------------------------------- part 0: pins
def part0():
    emit("01-commits.txt", "git log -1 --format=%%H %%s %s\n%s" % (BASE, git("log", "-1", "--format=%H %s", BASE)))
    emit("01-commits.txt", "git log -1 --format=%%H %%s %s\n%s" % (AFTER, git("log", "-1", "--format=%H %s", AFTER)))
    emit("01-commits.txt", "$ git diff --stat %s %s -- corpus/knowledge/ corpus/source-snapshots/round-30/\n%s"
         % (BASE, AFTER, git("diff", "--stat", BASE, AFTER, "--", "corpus/knowledge/", "corpus/source-snapshots/round-30/").rstrip()))
    emit("01-commits.txt", "$ git diff --name-only %s %s -- corpus/knowledge/\n%s"
         % (BASE, AFTER, git("diff", "--name-only", BASE, AFTER, "--", "corpus/knowledge/").rstrip() or "(none)"))
    pins = []
    for rel in (MAP_REL, ".ufo/waves/round-95/c1/labels.tsv", ".ufo/waves/round-95/c1/knowledge-meter.py"):
        data = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (AFTER, rel)], capture_output=True, check=True).stdout
        pins.append("%s  %s (blob at %s)" % (hashlib.sha256(data).hexdigest(), rel, AFTER))
    emit("02-pins.txt", "\n".join(pins))
    print("pins:", flush_ok := True)


# ------------------------------------------------------- part 1: changed lines
def parse_map():
    rows = []
    for ln in blob(AFTER, MAP_REL).split("\n"):
        if ln.strip() and not ln.startswith("#"):
            site, key, old, new = ln.split("\t")
            f, n = site.rsplit(":", 1)
            rows.append((f, int(n), key, old, new))
    return rows


def part1(rows):
    sites = {}
    for f, n, key, old, new in rows:
        sites.setdefault((f, n), []).append((old, new))
    lines_out = ["map rows=%d sites(lines)=%d" % (len(rows), len(sites))]
    ok_all = True
    for f in sorted({f for f, _, _, _, _ in rows}):
        bl = blob(BASE, f).split("\n")
        al = blob(AFTER, f).split("\n")
        lines_out.append("%s: base_lines=%d after_lines=%d" % (f, len(bl), len(al)))
        changed = [i for i, (b, a) in enumerate(zip(bl, al), 1) if b != a]
        lines_out.append("  changed lines (from git show, computed here): %s" % changed)
        site_lines = sorted(n for (ff, n) in sites if ff == f)
        lines_out.append("  map site lines: %s" % site_lines)
        same = changed == site_lines
        ok_all &= same
        lines_out.append("  changed-set==map-sites: %s" % same)
        for i in changed:
            fwd = bl[i - 1]
            missing = 0
            for old, new in sites.get((f, i), []):
                c = fwd.count(old)
                if c < 1:
                    missing += 1
                else:
                    fwd = fwd.replace(old, new)
            ok = fwd == al[i - 1]
            ok_all &= ok and missing == 0
            lines_out.append("  line %d rows=%d old_missing=%d composed==after: %s" % (i, len(sites[(f, i)]), missing, ok))
        extra = "OK" if ok_all else "MISMATCH"
    emit("03-changed-lines-and-map.txt", "\n".join(lines_out))
    print("\n".join(lines_out))
    print("PART1 composition:", "OK" if ok_all else "MISMATCH")
    return ok_all


# ------------------------------------------- part 2: S041 + anchor range checks
def rng_ok(nlines, lo, hi):
    return 1 <= lo <= hi <= nlines


def part2(rows):
    out = []
    ok = True
    snap_text = blob(AFTER, SNAP)
    n = len(snap_text.splitlines()) if snap_text is not None else 0
    out.append("%s at %s: exists=%s lines=%d" % (SNAP, AFTER, snap_text is not None, n))
    iso_rows = [(key, old, new) for f, ln, key, old, new in rows if f == F_ISO]
    checks = []
    for key, old, new in iso_rows:
        # new token's own anchor range, if any
        m = re.search(r":(\d+)(?:-(\d+))?`", new)
        if m:
            lo = int(m.group(1)); hi = int(m.group(2) or m.group(1))
            checks.append((key, lo, hi))
        else:
            checks.append((key, None, None))
    for key, lo, hi in checks:
        if lo is None:
            out.append("  %-28s bare-name row -> target file exists: %s" % (key, snap_text is not None))
            ok &= snap_text is not None
        else:
            good = rng_ok(n, lo, hi)
            ok &= good
            out.append("  %-28s range %d-%d inside capture: %s" % (key, lo, hi, good))
    sk = blob(AFTER, "SKILL.md")
    nsk = len(sk.splitlines())
    out.append("SKILL.md at %s: lines=%d" % (AFTER, nsk))
    for lo, hi in [(182, 184), (255, 257), (999, 999), (335, 338)]:
        good = rng_ok(nsk, lo, hi)
        ok &= good
        first = sk.splitlines()[lo - 1][:72] if good else ""
        out.append("  SKILL.md:%d-%d inside: %s   first=%r" % (lo, hi, good, first))
    mc = blob(AFTER, "corpus/knowledge/mission-control.md")
    nmc = len(mc.splitlines())
    good = rng_ok(nmc, 21, 27)
    ok &= good
    first = mc.splitlines()[20][:72] if good else ""
    out.append("corpus/knowledge/mission-control.md at %s: lines=%d" % (AFTER, nmc))
    out.append("  mission-control.md:21-27 inside: %s   first=%r" % (good, first))
    emit("04-s041-and-anchors.txt", "\n".join(out))
    print("\n".join(out))
    print("PART2 ranges:", "OK" if ok else "MISMATCH")
    return ok


# ------------------------------- part 3: own meter (resolve.py classify, own code)
TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([\u2013-]\d+)?$")
SYMANCHOR = re.compile(r"::[A-Za-z_][A-Za-z0-9_.]*$")
PLACEHOLDER = re.compile(r"<[^<>]*>")
GLOBMETA = "*?["
BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
MIRROR_CANDIDATES = ("~/Projects/the-bounty-hunter",
                     "~/Projects/origin-work/the-bounty-hunter")


def derive_mirror():
    env = os.environ.get("KASEGI_MIRROR")
    if env:
        return env
    for c in MIRROR_CANDIDATES:
        if os.path.isdir(os.path.expanduser(c)):
            return c
    return MIRROR_CANDIDATES[0]


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


def exists_any(path):
    import glob as globmod
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
            for hit in sorted(globmod.glob(qc, recursive=True)):
                if os.path.exists(hit):
                    return "brace-glob", hit
    q = PLACEHOLDER.sub("*", p)
    if any(ch in q for ch in GLOBMETA):
        for c in sorted(globmod.glob(q, recursive=True)):
            if os.path.exists(c):
                return "glob", c
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
    base, anchor = strip_anchor(tok)
    suffix = bounty_suffix(base)
    if suffix is not None:
        m, p = exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
        if m and under_mirror(p, mirror_root):
            return "MIRROR-EQUIVALENT", "bounty"
        return "GONE", "bounty"
    sfx = mirror_suffix(base)
    if sfx is not None:
        m, p = exists_any(os.path.join(mirror_root, sfx) if sfx else mirror_root)
        if m and under_mirror(p, mirror_root):
            return "RESOLVES", "other"
        return "GONE", "other"
    if base.startswith("~") or base.startswith("/"):
        m, p = exists_any(base)
        return ("RESOLVES", "other") if m else ("GONE", "other")
    m, p = exists_any(os.path.join(lane_root, base))
    if m:
        return "INTERNAL", "rel"
    if base not in ("", ".", ".."):
        m, p = exists_any(os.path.join(mirror_root, base))
        if m and under_mirror(p, mirror_root):
            return "MIRROR-EQUIVALENT", "rel"
    return "GONE", "rel"


def extract(rev):
    d = tempfile.mkdtemp(prefix="indep-tree-", dir=WORK)
    trees.append(d)
    data = subprocess.run(["git", "-C", LANE, "archive", "--format=tar", rev],
                          capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(d, filter="tar")
    return d


def knowledge_scope(tree):
    kd = os.path.join(tree, "corpus", "knowledge")
    out = {}
    for nm in sorted(os.listdir(kd)):
        p = os.path.join(kd, nm)
        if nm.endswith(".md") and os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                out["corpus/knowledge/" + nm] = fh.read()
    return out


def collect(files):
    cites = {}
    for rel in sorted(files):
        for line in files[rel].split("\n"):
            for m in TOKEN.finditer(line):
                t = m.group(1).strip().rstrip(".,;:")
                if not is_pathlike(t):
                    continue
                e = cites.setdefault(t, {"files": set(), "occ": 0})
                e["files"].add(rel)
                e["occ"] += 1
    return cites


def meter(rev):
    tree = extract(rev)
    files = knowledge_scope(tree)
    cites = collect(files)
    mirror_str = derive_mirror()
    mirror = os.path.expanduser(mirror_str)
    cls = {t: classify(t, tree, mirror)[0] for t in sorted(cites)}
    return cls, mirror_str, not os.path.isdir(mirror)


def part3():
    mirror_state = None
    cb, mb, mabs_b = None, None, None
    out = []
    cb, mb, mabs_b = meter(BASE)
    ca, ma, mabs_a = meter(AFTER)
    mirror_state = (mb, ma, mabs_b, mabs_a)
    def rate(cls):
        return sum(1 for c in cls.values() if c != "GONE"), len(cls)
    bn, bm = rate(cb)
    an, am = rate(ca)
    out.append("own meter (categories counted as resolved: every non-GONE class,")
    out.append("i.e. RESOLVES + INTERNAL + MIRROR-EQUIVALENT; scope = corpus/knowledge/*.md;")
    out.append("lane_root = full extracted tree of the pinned rev; mirror root per")
    out.append("KASEGI_MIRROR-else-first-existing-candidate derivation, expanded at use)")
    out.append("MY-METER base=%d/%d after=%d/%d" % (bn, bm, an, am))
    out.append("MY-MIRROR base_root=%s after_root=%s mirror_absent=%s/%s"
               % (mb, ma, mabs_b, mabs_a))
    for tag, cls in (("base", cb), ("after", ca)):
        cnt = Counter(cls.values())
        out.append("MY-CATS %s %s" % (tag, " ".join("%s=%d" % (k, cnt.get(k, 0))
                    for k in ("RESOLVES", "MIRROR-EQUIVALENT", "INTERNAL", "GONE"))))
    removed = sorted(set(cb) - set(ca))
    added = sorted(set(ca) - set(cb))
    changed = sorted(t for t in set(cb) & set(ca) if cb[t] != ca[t])
    out.append("MY-DELTA tokens_removed=%d added=%d class_changed=%d" % (len(removed), len(added), len(changed)))
    for t in removed:
        out.append("  - %r base=%s" % (t, cb[t]))
    for t in added:
        out.append("  + %r after=%s" % (t, ca[t]))
    for t in changed:
        out.append("  ~ %r base=%s after=%s" % (t, cb[t], ca[t]))
    verdict_base = (bn, bm) == (1007, 1998)
    verdict_after = (an, am) == (1008, 1994)
    out.append("MY-CHECK base==1007/1998: %s ; after==1008/1994: %s" % (verdict_base, verdict_after))
    emit("05-meter-repro.txt", "\n".join(out))
    print("\n".join(out))
    print("PART3 meter:", "OK" if (verdict_base and verdict_after) else "MISMATCH")
    return verdict_base and verdict_after


def main():
    try:
        part0()
        rows = parse_map()
        ok1 = part1(rows)
        ok2 = part2(rows)
        ok3 = part3()
        print("SUMMARY composition=%s ranges=%s meter=%s" % (ok1, ok2, ok3))
        return 0 if (ok1 and ok2 and ok3) else 1
    finally:
        flush()
        for t in trees:
            shutil.rmtree(t, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
