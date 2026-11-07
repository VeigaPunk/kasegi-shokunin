#!/usr/bin/env python3
"""ExecC1Indep independent byte-level check of round-92 C1 tranche 7.

Deliberately does NOT import or invoke the round-92 counter. It re-derives the
expected edit for each labelled (site, key) pair from the round-91 label TSV
and compares base/landing bytes fetched directly with `git show` (read-only).

Checks:
  1. label TSV at the frozen rev has exactly 30 rows with 5 columns;
  2. the frozen repair map has exactly 25 rows, every one a label pair, and
     each row's old/new matches what that pair's label names;
  3. the 5 unmapped labelled pairs (3 no-edit + EXCLUDED 437/438) are
     byte-identical between base and landing;
  4. every mapped site's line: old occurs exactly once on that base line and
     the landing line equals base-line.replace(old, new, 1) (nothing else on
     the line moved);
  5. no other line of corpus/knowledge changed: identical file sets and, per
     file, identical line counts with the differing line indexes equal to
     exactly the mapped sites of that file.

Writes ExecC1Indep-verify.txt next to this script and prints AGREE/DISAGREE
against the frozen landing receipt claims (947/1947 -> 960/1944, sites=25,
labels=30, kinds tally, P3 changed paths).
"""
import hashlib
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "0628fd247914555838a42c02ba5d4ac08b7e095d"
LAND = "cb1ef2b9856df79c530f3ff1374fa9691ff56233"
LABELS_REV = "d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d"
LABELS_PATH = ".ufo/waves/round-91/w1/ReviewC1Labels-receipts/round92-labels.tsv"
MAP_PATH = os.path.join(LANE, ".ufo/waves/round-92/c1/repair-map.tsv")
MAP_SHA_EXPECT = "6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ExecC1Indep-verify.txt")

problems = []
notes = []


def git(*args):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (args, r.stderr.decode(errors="replace")))
    return r.stdout


def site_split(site):
    m = re.match(r"^(corpus/knowledge/[A-Za-z0-9._-]+\.md):(\d+)$", site)
    if not m:
        raise RuntimeError("bad site: %r" % site)
    return m.group(1), int(m.group(2))


def classify(label, fix, key):
    """Independent kind derivation from the label columns; returns (kind, expect)."""
    if fix.startswith("No edit:"):
        return "no-edit", None
    m = re.match(r"^No content change; qualify to (corpus/knowledge/\S+?\.md:\d+(?:-\d+)?)\b", fix)
    if m:
        return "qualify", {"old": "`%s`" % key, "new": "`%s`" % m.group(1)}
    if re.match(r"^corpus/knowledge/[A-Za-z0-9._-]+\.md:\d+(-\d+)?$", label):
        return "range", {"old": "`%s`" % key, "new": "`%s`" % label}
    if fix.startswith("Replace with — (drop only the `"):
        tok = fix.split("drop only the `", 1)[1].split("`", 1)[0]
        return "drop-token", {"old": ", `%s`" % tok, "new": ""}
    if fix.startswith("Replace with — ("):
        return "dash-cell", {"old": "MATCHES: `%s`" % key, "new": "—"}
    m = re.match(r"^Replace with ([A-Za-z0-9._-]+\.md:\d+(?:-\d+)?)\b", fix)
    if m:
        # token-shape: bare old token -> one qualified token (named repoint);
        # cell-shape: whole MATCHES-cell rewritten around the qualified target
        # (named-cell, labels 155/249). The caller passes the map cells.
        return "named", {"old": "`%s`" % key,
                         "new": "`corpus/knowledge/%s`" % m.group(1),
                         "target": m.group(1)}
    return "unknown", None


# ---- 1. labels -------------------------------------------------------------
labels_raw = git("show", "%s:%s" % (LABELS_REV, LABELS_PATH)).decode("utf-8")
l_lines = labels_raw.splitlines()
if not l_lines[0].startswith("line\tkey\tlabel\tfix\tevidence"):
    problems.append("label header unexpected: %r" % l_lines[0])
label_rows = []
for ln in l_lines[1:]:
    if not ln.strip():
        continue
    cells = ln.split("\t")
    if len(cells) != 5:
        problems.append("label row not 5 columns: %r" % ln[:80])
        continue
    label_rows.append(cells)
notes.append("labels=%d" % len(label_rows))

pairs = {}
for site, key, label, fix, _ev in label_rows:
    pairs[(site, key)] = (label, fix)
if len(pairs) != 30:
    problems.append("label pairs=%d want 30" % len(pairs))

# ---- 2. map ----------------------------------------------------------------
map_bytes = open(MAP_PATH, "rb").read()
map_sha = hashlib.sha256(map_bytes).hexdigest()
notes.append("map_sha256=%s" % map_sha)
if map_sha != MAP_SHA_EXPECT:
    problems.append("map sha256 %s != pinned %s" % (map_sha, MAP_SHA_EXPECT))
map_rows = []
for ln in map_bytes.decode("utf-8").splitlines():
    if not ln.strip() or ln.startswith("#"):
        continue
    cells = ln.split("\t")
    if len(cells) != 4:
        problems.append("map row not 4 columns: %r" % ln[:80])
        continue
    map_rows.append(cells)

mapped = {}
for site, key, old, new in map_rows:
    if (site, key) not in pairs:
        problems.append("map row not a labelled pair: %s / %s" % (site, key))
        continue
    mapped[(site, key)] = (old, new)
if len(mapped) != 25:
    problems.append("mapped rows=%d want 25" % len(mapped))

unmapped = [(s, k) for (s, k) in pairs if (s, k) not in mapped]
notes.append("unmapped=%s" % ",".join("%s|%s" % (s, k) for s, k in sorted(unmapped)))

kinds = {}
for (site, key), (old, new) in mapped.items():
    label, fix = pairs[(site, key)]
    kind, expect = classify(label, fix, key)
    kinds[kind] = kinds.get(kind, 0) + 1
    if kind == "unknown":
        problems.append("unknown label kind at %s" % site)
        continue
    if expect is None:
        problems.append("label names no edit but pair is mapped: %s" % site)
        continue
    if kind == "dash-cell":
        if new != "—":
            problems.append("%s dash-cell new=%r" % (site, new))
        if old != expect["old"]:
            problems.append("%s dash-cell old=%r want MATCHES token" % (site, old))
    elif "target" in expect and new == "MATCHES: `corpus/knowledge/%s`" % expect["target"] \
            and "`%s`" % key in old:
        kinds["named-cell"] = kinds.get("named-cell", 0) + 1
        kinds["named"] -= 1
    elif new != expect["new"] or old != expect["old"]:
        problems.append("%s (%s) map old/new %r->%r != label %r->%r"
                        % (site, kind, old, new, expect["old"], expect["new"]))

notes.append("mapped kinds=%s" % ",".join("%s=%d" % (k, kinds[k]) for k in sorted(kinds)))
# named vs named-cell share the "Replace with <bare>:A-B" fix shape; split on the
# MATCHES-form new cell the map uses for whole-cell repairs (155/249).
nc = [s for (s, k), (o, n) in mapped.items() if n.startswith("MATCHES: ")]
if sorted(nc) != ["corpus/knowledge/triage-thresholds.md:155",
                  "corpus/knowledge/triage-thresholds.md:249"]:
    problems.append("MATCHES-form rows=%s want 155/249" % sorted(nc))
# EXCLUDED pairs must be the two content-repair rows left unmapped at 437/438.
exc = sorted(s for (s, k) in unmapped if pairs[(s, k)][1].startswith("Replace with "))
if exc != ["corpus/knowledge/triage-thresholds.md:437",
           "corpus/knowledge/triage-thresholds.md:438"]:
    problems.append("unmapped content-repair rows=%s want 437/438" % exc)

# ---- bytes -----------------------------------------------------------------
changed_files = {}
for rev, tag in ((BASE, "base"), (LAND, "landing")):
    out = git("ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge")
    changed_files[tag] = set(out.decode().splitlines())
if changed_files["base"] != changed_files["landing"]:
    problems.append("corpus/knowledge file sets differ: base-only=%s landing-only=%s"
                    % (sorted(changed_files["base"] - changed_files["landing"]),
                       sorted(changed_files["landing"] - changed_files["base"])))

site_by_file = {}
for (site, key) in mapped:
    f, n = site_split(site)
    site_by_file.setdefault(f, set()).add(n)

diff_lines_by_file = {}
for f in sorted(changed_files["base"] & changed_files["landing"]):
    b = git("show", "%s:%s" % (BASE, f)).split(b"\n")
    l = git("show", "%s:%s" % (LAND, f)).split(b"\n")
    if len(b) != len(l):
        problems.append("%s line count %d -> %d" % (f, len(b), len(l)))
        continue
    diffs = [i + 1 for i in range(len(b)) if b[i] != l[i]]
    diff_lines_by_file[f] = set(diffs)
    want = site_by_file.get(f, set())
    if diffs and not want:
        problems.append("%s changed lines %s but no mapped sites" % (f, diffs))
    for (site, key), (old, new) in sorted(mapped.items()):
        sf, sn = site_split(site)
        if sf != f:
            continue
        base_line = b[sn - 1].decode("utf-8")
        land_line = l[sn - 1].decode("utf-8")
        if base_line.count(old) != 1:
            problems.append("%s:%d old %r count=%d want 1"
                            % (f, sn, old, base_line.count(old)))
            continue
        expect_line = base_line.replace(old, new, 1)
        if land_line != expect_line:
            problems.append("%s:%d landing line != base.replace(old,new,1)\n  want: %r\n  got:  %r"
                            % (f, sn, expect_line, land_line))
    for (site, key) in unmapped:
        sf, sn = site_split(site)
        if sf != f:
            continue
        if b[sn - 1] != l[sn - 1]:
            problems.append("unmapped labelled line %s:%d changed" % (f, sn))
    if set(diffs) != want:
        problems.append("%s changed-line set %s != mapped sites %s"
                        % (f, sorted(set(diffs)), sorted(want)))

if diff_lines_by_file.get("corpus/knowledge/triage-thresholds.md") and \
        len(diff_lines_by_file["corpus/knowledge/triage-thresholds.md"]) != 24:
    problems.append("triage changed lines=%d want 24"
                    % len(diff_lines_by_file["corpus/knowledge/triage-thresholds.md"]))
if diff_lines_by_file.get("corpus/knowledge/root-loss-2026-10-12.md") and \
    diff_lines_by_file["corpus/knowledge/root-loss-2026-10-12.md"] != {68}:
    problems.append("root-loss changed lines=%s want [68]"
                    % sorted(diff_lines_by_file["corpus/knowledge/root-loss-2026-10-12.md"]))

# ---- verdict ---------------------------------------------------------------
receipt_claims = {
    "base": "947/1947", "after": "960/1944", "sites": 25, "labels": 30,
    "paths": ["corpus/knowledge/root-loss-2026-10-12.md",
              "corpus/knowledge/triage-thresholds.md"],
}
changed = sorted(f for f, s in diff_lines_by_file.items() if s)
agree = (not problems
         and len(mapped) == receipt_claims["sites"]
         and len(pairs) == receipt_claims["labels"]
         and changed == sorted(receipt_claims["paths"]))

with open(OUT, "w") as fh:
    fh.write("ExecC1Indep independent C1 byte check (base %s -> landing %s)\n" % (BASE, LAND))
    for n in notes:
        fh.write("NOTE %s\n" % n)
    for f in sorted(diff_lines_by_file):
        fh.write("CHANGED %s lines=%s\n" % (f, sorted(diff_lines_by_file[f])))
    for p in problems:
        fh.write("PROBLEM %s\n" % p)
    fh.write("BYTE-CHECK %s (problems=%d)\n" % ("pass" if not problems else "FAIL", len(problems)))
    fh.write("RECEIPT %s (base=%s after=%s sites=%d labels=%d changed=%s)\n"
             % ("AGREE" if agree else "DISAGREE", receipt_claims["base"],
                receipt_claims["after"], len(mapped), len(pairs), changed))
print(open(OUT).read())
sys.exit(0 if not problems else 1)
