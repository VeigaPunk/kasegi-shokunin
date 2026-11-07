#!/usr/bin/env python3
"""Build the round-93 C1 probe fixtures in a scratch clone of the lane.

Every fixture is a commit whose parent chain reaches the lane base; the meter is
run as --base-rev <lane base> --after-rev <fixture commit> with the fixture's own
measured rates as targets, so M0/M1 are neutralised and one limb is isolated.
The counter files are never modified in the lane; only the fixture clone.
"""
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r93/MutC1Counter"
LANE = os.path.join(S, "lane")
BUILD = os.path.join(S, "fx/build/lane")
BASE = "e15996bfd2f6eca4af39507a7c5973afbeca8347"
AFTER = "ae53b3c6e7e2ce070c2f022d01c1677a8908df1b"
METER = os.path.join(S, "art/knowledge-meter.py")
FROZEN_LABELS = os.path.join(S, "art/labels.tsv")
TFILE = "corpus/knowledge/triage-thresholds.md"
LABELS_REL = ".ufo/waves/round-93/c1/labels.tsv"
HEADER = "line\tkey\tlabel\tfix\tevidence"


def sh(args, **kw):
    p = subprocess.run(args, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        raise SystemExit("FAIL %s: %s" % (" ".join(args), p.stderr.strip()[:400]))
    return p.stdout


def git(*args, **kw):
    return sh(["git", "-C", BUILD] + list(args), **kw)


def assert_fixture():
    top = git("rev-parse", "--show-toplevel").strip()
    if top != BUILD:
        raise SystemExit("top-level mismatch: %r != %r" % (top, BUILD))


def base_lines():
    return git("show", "%s:%s" % (BASE, TFILE)).split("\n")


def last_cell(line):
    cells = line.rstrip().split("|")
    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None


def frozen_label_row(site):
    for ln in open(FROZEN_LABELS, encoding="utf-8").read().split("\n"):
        if ln.startswith(site + "\t"):
            return ln.split("\t")
    raise SystemExit("no frozen label row for %s" % site)


def build(tag, start, edits, labels_rows, map_rows, extra_files=None):
    """edits: [(lineno, old, new)] applied once per line; labels_rows: 5-col lists."""
    assert_fixture()
    git("checkout", "-q", "-f", "-B", tag, start)
    lines = open(os.path.join(BUILD, TFILE), encoding="utf-8").read().split("\n")
    for lineno, old, new in edits:
        i = lineno - 1
        if lines[i].count(old) != 1:
            raise SystemExit("%s: line %d old occurs %d times" % (tag, lineno, lines[i].count(old)))
        lines[i] = lines[i].replace(old, new, 1)
    with open(os.path.join(BUILD, TFILE), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    for rel, text in (extra_files or {}).items():
        p = os.path.join(BUILD, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    lp = os.path.join(BUILD, LABELS_REL)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    with open(lp, "w", encoding="utf-8") as fh:
        fh.write("\n".join([HEADER] + ["\t".join(r) for r in labels_rows]) + "\n")
    map_path = os.path.join(S, "art/maps/%s.tsv" % tag)
    with open(map_path, "w", encoding="utf-8") as fh:
        fh.write("".join("\t".join(r) + "\n" for r in map_rows))
    git("add", "-A")
    git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "fixture " + tag)
    rev = git("rev-parse", "HEAD").strip()
    return rev, map_path


def measure(rev):
    out = sh([sys.executable, "-B", METER, "--lane", BUILD, "--measure-rev", rev,
              "--work", os.path.join(S, "work/measure")])
    for ln in out.split("\n"):
        if ln.startswith("KNOWLEDGE-METER rev="):
            part = [w for w in ln.split() if w.startswith("rate=")][0]
            n, m = part.split("=")[1].split("/")
            return int(n), int(m)
    raise SystemExit("no rate line for %s: %s" % (rev, out[:300]))


def main():
    os.makedirs(os.path.dirname(BUILD), exist_ok=True)
    if not os.path.isdir(BUILD):
        sh(["git", "clone", "-q", "--shared", LANE, BUILD])
    assert_fixture()
    rows = []

    # F1: the 437 cell's lane-root token moved out of range (M5 generality probe).
    lab = frozen_label_row("corpus/knowledge/triage-thresholds.md:437")
    fix = lab[3].replace("`SKILL.md:176-178`", "`SKILL.md:9999-10000`")
    if fix == lab[3]:
        raise SystemExit("F1 fix unchanged")
    cell = fix[len("Replace cell with: "):]
    old_cell = last_cell(base_lines()[436])
    rev, mp = build("fx1-cell-badtoken", BASE,
                    [(437, old_cell, cell)],
                    [["corpus/knowledge/triage-thresholds.md:437", lab[1], lab[2], fix, "probe: lane-root token 9999-10000 inside the cell"]],
                    [["corpus/knowledge/triage-thresholds.md:437", lab[1], old_cell, cell]])
    rows.append(("fx1-cell-badtoken", rev, mp))

    # F2: 437 cell verbatim + a duplicate basename outside .ufo (M4 uniqueness probe).
    lab = frozen_label_row("corpus/knowledge/triage-thresholds.md:437")
    cell = lab[3][len("Replace cell with: "):]
    old_cell = last_cell(base_lines()[436])
    rev, mp = build("fx2-m4-dupbase", BASE,
                    [(437, old_cell, cell)],
                    [lab[:4] + ["probe: duplicate basename notes/intake-surface.md"]],
                    [["corpus/knowledge/triage-thresholds.md:437", lab[1], old_cell, cell]],
                    extra_files={"notes/intake-surface.md": "probe: duplicate basename outside corpus/knowledge\n"})
    rows.append(("fx2-m4-dupbase", rev, mp))

    # F3: 454 repointed to an out-of-file lane-root range (M5 hi bound).
    lab = frozen_label_row("corpus/knowledge/triage-thresholds.md:454")
    rev, mp = build("fx3-m5-hi", BASE,
                    [(454, "`SKILL.md:494-506`", "`SKILL.md:827-9999`")],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "SKILL.md:827-9999", "probe: hi past EOF", "probe"]],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "`SKILL.md:494-506`", "`SKILL.md:827-9999`"]])
    rows.append(("fx3-m5-hi", rev, mp))

    # F4: 454 repointed to the empty line past EOF (M5 splitlines vs split off-by-one).
    rev, mp = build("fx4-m5-offbyone", BASE,
                    [(454, "`SKILL.md:494-506`", "`SKILL.md:1252`")],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "SKILL.md:1252", "probe: last line + 1", "probe"]],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "`SKILL.md:494-506`", "`SKILL.md:1252`"]])
    rows.append(("fx4-m5-offbyone", rev, mp))

    # F5: round-92 drop-token content-repair on 454 (content-repair kind reachability).
    rev, mp = build("fx5-contentrepair", BASE,
                    [(454, ", `SKILL.md:494-506`", "")],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "content-repair",
                      "Replace with — (drop only the `SKILL.md:494-506` token)", "probe: round-92 drop-token kind"]],
                    [["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", ", `SKILL.md:494-506`", ""]])
    rows.append(("fx5-contentrepair", rev, mp))

    # F6: two lane-root range edits (EXCLUDED demonstration fixture).
    rev, mp = build("fx6-excluded", BASE,
                    [(58, "`SKILL.md:117`", "`SKILL.md:191`"),
                     (454, "`SKILL.md:494-506`", "`SKILL.md:191`")],
                    [["corpus/knowledge/triage-thresholds.md:58", "SKILL.md:117", "SKILL.md:191", "probe B", "probe"],
                     ["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "SKILL.md:191", "probe A", "probe"]],
                    [["corpus/knowledge/triage-thresholds.md:58", "SKILL.md:117", "`SKILL.md:117`", "`SKILL.md:191`"],
                     ["corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506", "`SKILL.md:494-506`", "`SKILL.md:191`"]])
    rows.append(("fx6-excluded", rev, mp))

    # F7: the landed tree with a labelled non-knowledge file that gains a line (M3 count).
    assert_fixture()
    git("checkout", "-q", "-f", "-B", "fx7-m3-count", AFTER)
    sk = open(os.path.join(BUILD, "SKILL.md"), encoding="utf-8").read().rstrip("\n").split("\n")
    sk.append("fixture appended line for the M3 line-count probe")
    with open(os.path.join(BUILD, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sk) + "\n")
    lp = os.path.join(BUILD, LABELS_REL)
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    lab = open(lp, encoding="utf-8").read().rstrip("\n").split("\n")
    lab.append("SKILL.md:191\tSKILL.md:191\tCORRECT\tNo edit: fixture row so SKILL.md enters the M3 walk.\tprobe")
    with open(lp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lab) + "\n")
    import shutil as _sh
    _sh.copy(os.path.join(S, "art/repair-map.tsv"), os.path.join(BUILD, ".ufo/waves/round-93/c1/repair-map.tsv"))
    git("add", "-A")
    git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "fixture fx7-m3-count")
    rev = git("rev-parse", "HEAD").strip()
    rows.append(("fx7-m3-count", rev, os.path.join(S, "art/repair-map.tsv")))

    out = []
    for tag, rev, mp in rows:
        bn, bm = measure(rev)
        out.append("%s\t%s\t%s\t%s\t1007/2001\t%d/%d" % (tag, rev, mp, rev, bn, bm))
        print("%s rev=%s map=%s target=%d/%d" % (tag, rev, mp, bn, bm))
    with open(os.path.join(S, "art/fixtures.tsv"), "w", encoding="utf-8") as fh:
        fh.write("tag\tafter_rev\tmap\tlabels_rev\tbase_target\ttarget\n")
        fh.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
