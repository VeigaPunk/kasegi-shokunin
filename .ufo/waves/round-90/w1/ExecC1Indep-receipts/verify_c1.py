#!/usr/bin/env python3
"""ExecC1Indep independent C1 verifier, kasegi round 90.

Independent of both counters: every input comes from the lane object store
(git show / diff-tree / ls-tree) plus the frozen map/excluded/labels bytes.
Checks:
  A  P3        git diff-tree -r of the landing names exactly the one corpus file
  B  sites     the only changed lines base->after are the map's citing lines;
               excluded sites are byte-identical
  C  tokens    each after line equals its base line with backticked key ->
               backticked value swaps only (per map rows)
  D  labels    every map row equals a WRONG label row (same citing line, same
               key, supported range == value) at the labels rev
  E  complete  WRONG-with-range label sites == map sites + excluded sites
  F  inrange   every map value's range exists inside the named entry file at
               the landing rev
  G  pins      worktree map/meter sha256 == claims.json pins == freeze bytes
Also emits gone-candidates for the environment attack.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "6088c3eb0c29040415c69e7b5fb91e110480ab26"
AFTER = "4a7e676895d3fc74e18c853457c9b465ade2ddf5"
FREEZE = "33f43db99c06e89bb9fb78c538313e9450da649f"
LABELS_REV = "02b6d88f1c059e2f881fd07c73834f502b4f212d"
MAP_PATH = ".ufo/waves/round-90/c1/repair-map.tsv"
EXCL_PATH = ".ufo/waves/round-90/c1/excluded.tsv"
LABELS_PATH = ".ufo/waves/round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv"
CLAIMS = ".ufo/waves/round-90/claims.json"
METER = ".ufo/waves/round-90/c1/knowledge-meter.py"
DOC = "corpus/knowledge/triage-thresholds.md"
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "/tmp"

fails = []
nc = [0]


def check(name, ok, detail):
    nc[0] += 1
    print("%s %s %s" % ("CHECK" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def show(rev, path):
    return subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                          capture_output=True, check=True).stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---- frozen bytes -----------------------------------------------------------
map_wt = show(FREEZE, MAP_PATH)          # frozen map = bytes at the freeze rev
meter_wt = show(FREEZE, METER)
map_lane = open(os.path.join(LANE, MAP_PATH), "rb").read()
meter_lane = open(os.path.join(LANE, METER), "rb").read()
claims = json.loads(git("show", "%s:%s" % (FREEZE, CLAIMS)))
c1 = [c for c in claims["claims"] if c["id"] == "C1"][0]

check("G1-map-pin", sha(map_wt) == c1["map_sha256"] == sha(map_lane),
      "freeze=%s worktree=%s claims=%s" % (sha(map_wt)[:12], sha(map_lane)[:12], c1["map_sha256"][:12]))
check("G2-meter-pin", sha(meter_wt) == c1["counter_sha256"] == sha(meter_lane),
      "freeze=%s worktree=%s claims=%s" % (sha(meter_wt)[:12], sha(meter_lane)[:12], c1["counter_sha256"][:12]))

# ---- parse map --------------------------------------------------------------
rows = []  # (file, line, key, value)
for ln in map_wt.decode("utf-8").split("\n"):
    if ln.strip() and not ln.startswith("#"):
        site, k, v = ln.split("\t")
        f, n = site.rsplit(":", 1)
        rows.append((f, int(n), k, v))
check("H1-rowcount", len(rows) == 34, "rows=%d" % len(rows))
check("H2-single-file", all(f == DOC for f, _, _, _ in rows), "all citing-file == %s" % DOC)
lines = sorted({n for _, n, _, _ in rows})
multi = [n for n in lines if sum(1 for r in rows if r[1] == n) > 1]

# ---- excluded ---------------------------------------------------------------
excl = []  # (file, line, key, reason)
for ln in show(FREEZE, EXCL_PATH).decode("utf-8").split("\n"):
    if ln.strip() and not ln.startswith("#"):
        site, k, reason = ln.split("\t", 2)
        f, n = site.rsplit(":", 1)
        excl.append((f, int(n), k, reason))
check("H3-excl-count", len(excl) == 4, "excluded=%d lines=%s" % (
    len(excl), sorted(n for _, n, _, _ in excl)))

# ---- A: P3 ------------------------------------------------------------------
paths = [p for p in git("diff-tree", "--no-commit-id", "--name-only", "-r", AFTER).split("\n") if p]
check("A1-P3-one-path", paths == [DOC], "paths=%s" % paths)

# ---- B: changed lines -------------------------------------------------------
base_doc = show(BASE, DOC).decode("utf-8")
after_doc = show(AFTER, DOC).decode("utf-8")
bl, al = base_doc.split("\n"), after_doc.split("\n")
check("B1-linecount", len(bl) == len(al), "base=%d after=%d" % (len(bl), len(al)))
changed = [i + 1 for i in range(min(len(bl), len(al))) if bl[i] != al[i]]
check("B2-changed-set", changed == lines,
      "changed=%d map_lines=%d missing=%s extra=%s" % (
          len(changed), len(lines),
          sorted(set(lines) - set(changed)), sorted(set(changed) - set(lines))))
check("B3-excl-unchanged", all(bl[n - 1] == al[n - 1] for _, n, _, _ in excl),
      "excluded lines byte-identical")

# ---- C: token swaps ---------------------------------------------------------
bad = []
by_line = {}
for f, n, k, v in rows:
    by_line.setdefault(n, []).append((k, v))
for n in sorted(by_line):
    b, x = bl[n - 1], al[n - 1]
    fwd = b
    for k, v in by_line[n]:
        if b.count("`%s`" % k) != 1:
            bad.append("%d:keycount=%d" % (n, b.count("`%s`" % k)))
            continue
        fwd = fwd.replace("`%s`" % k, "`%s`" % v)
    if fwd != x:
        bad.append("%d:swap-mismatch" % n)
    else:
        for k, v in by_line[n]:
            if "`%s`" % v not in x:
                bad.append("%d:value-absent" % n)
check("C1-token-swap", not bad, "bad=%s" % (",".join(bad) or "none"))
# no other line differs at all (implied by B2 but assert directly)
other = [i for i in changed if i not in lines]
check("C2-no-other-diffs", not other, "other=%s" % other)
check("H4-multi-line-note", sorted(multi) == [261, 270], "lines carrying 2 sites=%s (34 rows / %d lines)" % (multi, len(lines)))

# ---- D: labels --------------------------------------------------------------
lab_rows = []  # (key, citing, verdict, support, reason)
for ln in git("show", "%s:%s" % (LABELS_REV, LABELS_PATH)).split("\n"):
    if ln.strip() and not ln.startswith("#"):
        c = ln.split("\t")
        if len(c) >= 5:
            lab_rows.append((c[0], c[1], c[2], c[3], c[4]))
wrong = [r for r in lab_rows if r[2] == "WRONG"]
wrong_rng = [r for r in wrong if r[3] != "none"]
lab_set = {(r[1], r[0], r[3]) for r in wrong}          # (citing-file:line, key, support)
unbound = [(f, n, k, v) for f, n, k, v in rows if ("%s:%d" % (f, n), k, v) not in lab_set]
check("D1-map-bound", not unbound, "wrong_rows=%d wrong_with_range=%d unbound=%s" % (
    len(wrong), len(wrong_rng), ["%s:%d" % (f.rsplit('/', 1)[-1], n) for f, n, k, v in unbound] or "none"))

# ---- E: completeness --------------------------------------------------------
mapped = {("%s:%d" % (f, n), k) for f, n, k, v in rows}
excl_set = {("%s:%d" % (f, n), k) for f, n, k, _ in excl}
leftover = sorted((r[1], r[0], r[3]) for r in wrong_rng
                  if (r[1], r[0]) not in mapped | excl_set)
nomap_excl = sorted(("%s:%d" % (e[0], e[1]), e[2]) for e in excl if ("%s:%d" % (e[0], e[1]), e[2]) not in {(r[1], r[0]) for r in wrong_rng})
check("E1-tranche-complete", not leftover and not nomap_excl,
      "wrong_with_range=%d mapped=%d excluded=%d leftover=%s excluded_not_labelled=%s" % (
          len(wrong_rng), len(mapped), len(excl_set), leftover or "none", nomap_excl or "none"))

# ---- F: value ranges inside entry at AFTER ----------------------------------
tracked_after = set(p for p in git("ls-tree", "-r", "--name-only", AFTER).split("\n") if p)
tracked_base = set(p for p in git("ls-tree", "-r", "--name-only", BASE).split("\n") if p)
vre = re.compile(r"^corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
bybase = {}
for p in tracked_after:
    if not p.startswith(".ufo/"):
        bybase.setdefault(os.path.basename(p), []).append(p)
oob, nobase, ambig = [], [], []
target_files = {}
for f, n, k, v in rows:
    m = vre.match(v)
    if not m:
        oob.append("%d:unparsable" % n)
        continue
    name, lo = m.group(1), int(m.group(2))
    hi = int(m.group(3)) if m.group(3) else lo
    path = "corpus/knowledge/" + name
    target_files.setdefault(path, []).append(n)
    cands = bybase.get(name, [])
    if cands != [path]:
        ambig.append("%d:%s" % (n, cands))
    if not (path in tracked_after and 1 <= lo <= hi):
        oob.append("%d:bounds" % n)
        continue
    text = show(AFTER, path).decode("utf-8")
    nl = len(text.split("\n"))
    if hi > nl:
        oob.append("%d:%d>%d" % (n, hi, nl))
check("F1-in-range", not oob, "out_of_range=%s" % (oob or "none"))
check("F2-target-unique", not ambig, "ambiguous=%s" % (ambig or "none"))
gone_at_base = sorted({k.split(":")[0] for _, _, k, _ in rows if (k.split(":")[0]) not in tracked_base})
keynames = sorted({k.split(":")[0] for _, _, k, _ in rows})
check("F3-keys-gone-base", gone_at_base == keynames,
      "root-level key files absent at base=%d/%d distinct=%s" % (len(gone_at_base), len(keynames), gone_at_base))
info = ["%s target of map lines %s" % (p, sorted(set(ns))) for p, ns in sorted(target_files.items())]
print("INFO F-targets " + " | ".join(info))

# ---- gone candidates for the environment attack -----------------------------
bare = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?`")
gone = {}
for p in sorted(tracked_after):
    if not p.startswith("corpus/knowledge/") or not p.endswith(".md"):
        continue
    for i, ln in enumerate(show(AFTER, p).decode("utf-8").split("\n"), 1):
        for m in bare.finditer(ln):
            tok, name = m.group(1), m.group(1)
            if ("corpus/knowledge/" + name) not in tracked_after and "/" not in name:
                gone.setdefault(tok, []).append("%s:%d" % (p, i))
with open(os.path.join(SCRATCH, "gone-candidates.txt"), "w") as fh:
    for tok in sorted(gone):
        fh.write("%s\t%s\n" % (tok, ",".join(sorted(gone[tok])[:4]) + (" +%d more" % (len(gone[tok]) - 4) if len(gone[tok]) > 4 else "")))
print("INFO gone-candidates %d tokens -> %s" % (len(gone), os.path.join(SCRATCH, "gone-candidates.txt")))

print("VERDICT %s (%d checks, %d failed)" % ("PASS" if not fails else "FAIL", nc[0], len(fails)))
sys.exit(1 if fails else 0)
