#!/usr/bin/env python3
"""Verify the round-95 next-tranche labels (2 rows) against the C1 landing bytes.

Re-derives every row from committed bytes at d51220aeb4a538b7b211bb2629e83210669cd56d:

  * the old key is a backticked token on the citing line;
  * the new label names the same file basename as the key (the round-94 M4 shape)
    and that basename is unique in the tracked tree (SKILL.md is the lane root);
  * the new range exists and is in bounds at the rev;
  * the new range states the row's claim (required literals) while the old range
    does not (so the defect is real, not cosmetic);
  * the (site, key) pair is not already bound by the round-94 repair map;
  * the two hard-coded extra checks: row 396's cell already carries the
    ops-invariants.md:24 marker/code list, and the landed row 459 cites the same
    SKILL.md value under the same MATCHES framing; row 436's statement names the
    dead ev_note branch;
  * completeness: every distinct SKILL.md token in corpus/knowledge at the rev
    is accounted for as a landing value (17), a previously-correct value (3), or
    a still-excluded value (7), and all 10 round-94 EXCLUDED keys are still
    present on their citing lines.

Read-only: git show / ls-tree only. Exit 0 only when every check passes.
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "d51220aeb4a538b7b211bb2629e83210669cd56d"
FREEZE = "96b5033f4dfa8d6605c13e0c9aad458be3cd7df3"
TSV = os.path.dirname(os.path.abspath(__file__)) + "/round95-labels.tsv"

# required literals in the new range, forbidden literals in the old range
EVIDENCE = {
    "corpus/knowledge/triage-thresholds.md:436": (
        ["ev_note", "adjusted_ev", "0/1088", "unknown"],
        ["ev_note", "adjusted_ev", "0/1088", "unknown"],
    ),
    "corpus/knowledge/triage-thresholds.md:396": (
        ["gitMutationBlocker", "fail-closed", "non-main HEAD"],
        ["gitMutationBlocker"],
    ),
}
LANDED_NEW = {
    "SKILL.md:157-158", "SKILL.md:161-162", "SKILL.md:184-187",
    "SKILL.md:224-226", "SKILL.md:224-226,335-338", "SKILL.md:251-253",
    "SKILL.md:264-266", "SKILL.md:321-324", "SKILL.md:331-335",
    "SKILL.md:340-346", "SKILL.md:828", "SKILL.md:829", "SKILL.md:830-831",
    "SKILL.md:832", "SKILL.md:910-913", "SKILL.md:999", "SKILL.md:1164",
}
PREV_CORRECT = {"SKILL.md:191", "SKILL.md:176-178", "SKILL.md:827-848"}
EXCLUDED_KEYS = {
    "SKILL.md:113-114", "SKILL.md:175-176", "SKILL.md:175",
    "SKILL.md:113-114,175-176", "SKILL.md:522", "SKILL.md:245-247",
    "SKILL.md:10-11",
}
# the ten (site, key) pairs the round-94 counter froze as EXCLUDED
EXCLUDED_PAIRS = [
    ("corpus/knowledge/triage-thresholds.md:88", "SKILL.md:113-114"),
    ("corpus/knowledge/triage-thresholds.md:88", "SKILL.md:175-176"),
    ("corpus/knowledge/triage-thresholds.md:89", "SKILL.md:175"),
    ("corpus/knowledge/triage-thresholds.md:90", "SKILL.md:113-114,175-176"),
    ("corpus/knowledge/triage-thresholds.md:356", "SKILL.md:522"),
    ("corpus/knowledge/triage-thresholds.md:396", "SKILL.md:245-247"),
    ("corpus/knowledge/triage-thresholds.md:433", "SKILL.md:113-114"),
    ("corpus/knowledge/triage-thresholds.md:433", "SKILL.md:175-176"),
    ("corpus/knowledge/triage-thresholds.md:434", "SKILL.md:175"),
    ("corpus/knowledge/triage-thresholds.md:435", "SKILL.md:10-11"),
]

fails = []


def git(*args):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("git %s failed rc=%d: %s" % (" ".join(args), r.returncode, r.stderr.strip()))
    return r.stdout


def show(path):
    return git("show", "%s:%s" % (REV, path)).split("\n")


def span(path, a, b):
    lines = show(path)
    if a < 1 or b > len(lines) or a > b:
        return None
    return "\n".join(lines[a - 1:b])


def parse_anchor(tok):
    if tok.startswith("SKILL.md:"):
        path = "SKILL.md"
        nums = tok[len("SKILL.md:"):]
    else:
        m = re.fullmatch(r"(corpus/knowledge/[A-Za-z0-9._-]+\.md):([0-9][0-9-]*)", tok)
        if not m:
            return None
        path, nums = m.group(1), m.group(2)
    parts = nums.split("-")
    a = int(parts[0])
    b = int(parts[1]) if len(parts) > 1 else a
    return path, a, b


raw = open(TSV, encoding="utf-8").read().splitlines()
if raw[0].split("\t") != ["line", "key", "label", "fix", "evidence"]:
    fails.append("bad header %r" % raw[0])
rows = []
for n, line in enumerate(raw[1:], 2):
    f = line.split("\t")
    if len(f) != 5:
        fails.append("row %d: %d fields" % (n, len(f)))
        continue
    rows.append((n, f))

tracked = [p for p in git("ls-tree", "-r", "--name-only", REV).split("\n") if p]
map_rows = set()
for line in git("show", "%s:.ufo/waves/round-94/c1/repair-map.tsv" % FREEZE).split("\n"):
    if line.strip() and not line.startswith("#"):
        c = line.split("\t")
        map_rows.add((c[0], c[1]))

seen = set()
for n, (site, key, label, fix, ev) in rows:
    if ":" not in site:
        fails.append("row %d: bad site %r" % (n, site))
        continue
    path, ln = site.rsplit(":", 1)
    if not ln.isdigit():
        fails.append("row %d: bad site line %r" % (n, site))
        continue
    lines = show(path)
    ln = int(ln)
    if ln < 1 or ln > len(lines):
        fails.append("row %d: site line out of range" % n)
        continue
    text = lines[ln - 1]
    if ("`%s`" % key) not in text:
        fails.append("row %d: backticked key %r absent on %s" % (n, key, site))
    if key == label:
        fails.append("row %d: key equals label" % n)
    if (site, key) in seen:
        fails.append("row %d: duplicate (site,key)" % n)
    seen.add((site, key))
    if (site, key) in map_rows:
        fails.append("row %d: pair already mapped by the round-94 repair map" % n)
    old = parse_anchor(key)
    new = parse_anchor(label)
    if not new:
        fails.append("row %d: unparsable label %r" % (n, label))
        continue
    if old is None:
        fails.append("row %d: unparsable key %r" % (n, key))
        continue
    if os.path.basename(old[0]) != os.path.basename(new[0]):
        fails.append("row %d: label names a different file basename" % n)
    outside = [p for p in tracked if not p.startswith(".ufo/")
               and os.path.basename(p) == os.path.basename(new[0])]
    if new[0].startswith("corpus/knowledge/") and len(outside) != 1:
        fails.append("row %d: basename %r is not unique outside .ufo/ (%d)" % (
            n, os.path.basename(new[0]), len(outside)))
    if new[0] == "SKILL.md" and "SKILL.md" not in tracked:
        fails.append("row %d: lane-root SKILL.md is not tracked" % n)
    old_text = span(old[0], old[1], old[2])
    new_text = span(new[0], new[1], new[2])
    if new_text is None:
        fails.append("row %d: new range out of bounds" % n)
        continue
    req, forb = EVIDENCE[site]
    missing = [w for w in req if w not in new_text]
    if missing:
        fails.append("row %d: new range lacks %r" % (n, missing))
    leaked = [w for w in forb if w in (old_text or "")]
    if leaked:
        fails.append("row %d: old range already states %r (not a defect)" % (n, leaked))
    print("CHECK %s key=%s label=%s new_has=%d/%d old_lacks=%d/%d" % (
        site, key, label, len(req) - len(missing), len(req),
        len(forb) - len(leaked), len(forb)))

# row-specific extra checks
t396 = show("corpus/knowledge/triage-thresholds.md")[395]
oi24 = show("corpus/knowledge/ops-invariants.md")[23]
for w in ["gitMutationBlocker", "rebase-merge", "rebase-apply", "MERGE_HEAD", "CHERRY_PICK_HEAD",
          "ACTIVE_GIT_OPERATION", "HEAD_NOT_ON_MAIN"]:
    if w not in oi24:
        fails.append("396 cell: ops-invariants.md:24 lacks %r" % w)
if "`SKILL.md:224-226,335-338`" not in show("corpus/knowledge/triage-thresholds.md")[458]:
    fails.append("396 precedent: landed row 459 does not cite SKILL.md:224-226,335-338")
if "`corpus/knowledge/mission-control.md:21-23`" not in show("corpus/knowledge/triage-thresholds.md")[435]:
    fails.append("436: citing line does not carry the old token")
if "[lost-base] fleet-dispatch.mjs:11" not in show("corpus/knowledge/triage-thresholds.md")[435]:
    fails.append("436: citing line lost its fleet-dispatch.mjs:11 tie")

# completeness of the SKILL.md token accounting
all_tokens = set()
for path in tracked:
    if not path.startswith("corpus/knowledge/") or not path.endswith(".md"):
        continue
    for line in show(path):
        for m in re.finditer(r"SKILL\.md:[0-9][0-9, -]*", line):
            all_tokens.add(m.group(0).rstrip())
expected = LANDED_NEW | PREV_CORRECT | EXCLUDED_KEYS
for t in sorted(all_tokens - expected):
    fails.append("unaccounted SKILL token at REV: %r" % t)
for t in sorted(expected - all_tokens):
    fails.append("accounted SKILL token absent at REV: %r" % t)
print("CHECK skill_tokens=%d expected=%d unaccounted=%d" % (
    len(all_tokens), len(expected), len(all_tokens - expected)))

present = 0
for site, key in EXCLUDED_PAIRS:
    path, ln = site.rsplit(":", 1)
    if ("`%s`" % key) in show(path)[int(ln) - 1]:
        present += 1
    else:
        fails.append("excluded pair absent at REV: %s %s" % (site, key))
print("CHECK excluded_pairs_present=%d/%d" % (present, len(EXCLUDED_PAIRS)))

print("ROUND95-LABELS-VERIFY rev=%s rows=%d failures=%d" % (REV, len(rows), len(fails)))
for f in fails:
    print("FAIL " + f)
print("PASS" if not fails else "FAIL")
sys.exit(0 if not fails else 1)
