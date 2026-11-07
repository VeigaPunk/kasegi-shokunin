#!/usr/bin/env python3
"""Build the round-95 C1 label set and repair map from the base revision.

Edit kinds, all expressed in the label TSV:
  cell  fix = "Replace cell with: <new>"        replace the row's last cell
  part  fix = "Replace part: <old> => <new>"    replace a disjoint substring
  range label = "<target>"; the token `key` -> `target`
Every `old` is read from (cell/range) or named with (part) the base revision and
asserted to occur exactly once in its file, so the map cannot drift from the
label premise. Two keys on one cell become two disjoint `part` edits, so both
(site, key) pairs map without one destroying the other's anchor.
"""
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10"
OUT = LANE + "/.ufo/waves/round-95/c1"

TRIAGE = "corpus/knowledge/triage-thresholds.md"
ISO = "corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md"

CELLS = [
    (89, "SKILL.md:175",
     "SUPERSEDES: `SKILL.md:182-184` — the earlier text wrote `reward.min`; the current queue tail "
     "writes `reward.min×1000`",
     "the superseded 'writes reward.min' is historical: the current queue writes reward.min×1000."),
    (356, "SKILL.md:522",
     "MATCHES: `SKILL.md:999` (the program-record schema bullet; `SKILL.md` does not enumerate the "
     "required keys — the list is `[lost-base] schema.json:6`)",
     "522 is the parking-invisibility sentence; the schema bullet is 999 (row 355's target), and "
     "SKILL.md states no key list."),
    (434, "SKILL.md:175",
     "`SKILL.md:182-184` writes `reward.min×1000`; the earlier text's `reward.min` is the superseded form",
     "9.2's 'writes reward.min' is historical; the current queue writes reward.min×1000."),
    (435, "SKILL.md:10-11",
     "`[lost-base] fleet-dispatch.mjs:10` (in-file comment, the \"EV ordering (curated first …)\" "
     "phrasing), `SKILL.md:182-184` (the queue puts `curated` third, behind `priority` and `continue`)",
     "the SKILL.md:10-11 token is dropped: 'EV ordering' occurs 0 times in SKILL.md; the phrasing is "
     "the fleet-dispatch.mjs:10 comment, and 182-184 grounds the third-rank reading."),
]

PARTS = [
    (90, "SKILL.md:113-114,175-176",
     "`SKILL.md:113-114,175-176` (term omitted)",
     "`SKILL.md:182-184,255-257` (round-13 correction: earlier text omitted `is_live(1)` and called "
     "`curated` an EV magnitude)",
     "both parts of the combined token move to the correction anchor; '(term omitted)' is historical."),
    (88, "SKILL.md:113-114",
     "`SKILL.md:113-114` (four terms, no `is_live`)",
     "`SKILL.md:182-184` (round-13 correction: earlier text omitted `is_live(1)`)",
     "the new anchor 182-184 carries the five-term correction, so 'four terms, no is_live' is false "
     "about it; reword to the correction the anchor states."),
    (88, "SKILL.md:175-176",
     "`SKILL.md:175-176` (same omission; names the term `curated-EV` although the source tests only "
     "non-emptiness)",
     "`SKILL.md:255-257` (`curated` is a boolean on non-empty `ev_inputs`, never an EV magnitude)",
     "255-257 states the curated-boolean correction, and `curated-EV` occurs nowhere in SKILL.md."),
    (433, "SKILL.md:113-114",
     "`SKILL.md:113-114` and",
     "`SKILL.md:182-184` and",
     "9.1's citation moves to the correction anchor; the 'and' keeps the sentence's grammar."),
    (433, "SKILL.md:175-176",
     "`SKILL.md:175-176` omit it (both are summaries of this expression)",
     "`SKILL.md:255-257` carry the correction the earlier text omitted (both are summaries of this "
     "expression)",
     "same cell as the first token on line 433; both anchors now state the correction."),
]

RANGES = [
    (TRIAGE, 396, "SKILL.md:245-247", "SKILL.md:335-338",
     "round-95 label (ReviewC1Labels, round-94 wave): 245-247 is the mission-ledger paragraph; "
     "335-338 states the gitMutationBlocker fail-closed rule; the marker list stays sourced by "
     "ops-invariants.md:24, so no prose change is needed."),
    (TRIAGE, 436, "corpus/knowledge/mission-control.md:21-23",
     "corpus/knowledge/mission-control.md:21-27",
     "round-95 label: 21-23 stops mid-sentence at 'the negative-EV dispatches carry an'; the dead-code "
     "and unknown-adjusted_ev substance is on 23-27."),
    (ISO, 13, "S041.txt:1868-1870", "corpus/source-snapshots/round-30/S041.txt:1868-1870",
     "bare capture filename does not resolve; the capture is committed at round-30."),
    (ISO, 34, "S041.txt:1792-1867", "corpus/source-snapshots/round-30/S041.txt:1792-1867",
     "same bare-name repair."),
    (ISO, 43, "S041.txt:1996-2079", "corpus/source-snapshots/round-30/S041.txt:1996-2079",
     "same bare-name repair."),
    (ISO, 54, "S041.txt:1868", "corpus/source-snapshots/round-30/S041.txt:1868",
     "same bare-name repair."),
    (ISO, 64, "S041.txt", "corpus/source-snapshots/round-30/S041.txt",
     "same bare-name repair (the pin sentence)."),
]


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


_cache = {}


def base_text(rel):
    if rel not in _cache:
        _cache[rel] = sh("git", "-C", LANE, "show", "%s:%s" % (BASE, rel))
    return _cache[rel]


def base_lines(rel):
    return base_text(rel).split("\n")


def last_cell(line):
    cells = line.rstrip().split("|")
    if not line.rstrip().endswith("|") or len(cells) < 3:
        raise SystemExit("not a table row: %r" % line[:80])
    return cells[-2].strip()


def main():
    labels = ["line\tkey\tlabel\tfix\tevidence"]
    maps = []
    for n, key, new, why in CELLS:
        line = base_lines(TRIAGE)[n - 1]
        old = last_cell(line)
        if base_text(TRIAGE).count(old) != 1:
            raise SystemExit("cell not unique at %s:%d" % (TRIAGE, n))
        labels.append("\t".join(["%s:%d" % (TRIAGE, n), key, "cell-repair",
                                 "Replace cell with: " + new, why]))
        maps.append((TRIAGE, n, key, old, new))
    for n, key, old, new, why in PARTS:
        if base_text(TRIAGE).count(old) != 1:
            raise SystemExit("part %r not exactly once at %s:%d" % (old[:40], TRIAGE, n))
        if not ("`%s`" % key) in old:
            raise SystemExit("part %r lacks its key at %s:%d" % (old[:40], TRIAGE, n))
        labels.append("\t".join(["%s:%d" % (TRIAGE, n), key, "part-repair",
                                 "Replace part: %s => %s" % (old, new), why]))
        maps.append((TRIAGE, n, key, old, new))
    for rel, n, key, new, why in RANGES:
        line = base_lines(rel)[n - 1]
        old = "`%s`" % key
        if line.count(old) != 1:
            raise SystemExit("token %s not exactly once at %s:%d" % (key, rel, n))
        labels.append("\t".join(["%s:%d" % (rel, n), key, new, why, "round-95 edit"]))
        maps.append((rel, n, key, old, "`%s`" % new))
    with open(OUT + "/labels.tsv", "w", encoding="utf-8") as fh:
        fh.write("\n".join(labels) + "\n")
    with open(OUT + "/repair-map.tsv", "w", encoding="utf-8") as fh:
        for rel, n, key, old, new in maps:
            if "\t" in old or "\t" in new or "\n" in old or "\n" in new:
                raise SystemExit("tab/newline in a map cell")
            fh.write("\t".join(["%s:%d" % (rel, n), key, old, new]) + "\n")
    print("labels=%d map=%d" % (len(labels) - 1, len(maps)))


if __name__ == "__main__":
    sys.exit(main())
