#!/usr/bin/env python3
"""Per-limb defect-tree builder for the r46-f29-gate.py R50 mutant pairing.

Builds the positive tree (via f29-fixture.py) into DEST, then applies ONE defect:

  duprow        duplicate the live F29 frontier row                  (H1 dup clause)
  fencedf29     hide the F29 row inside a code fence                 (H1 one-live-row clause)
  vjunk         entry verified-at line gains a trailing comment      (H2 exact verified-at)
  thinsection   Scope section cut to a 6-word stub                  (H2 word floors)
  badnames      the two xrefs point at unrelated in-range files      (H2 need-names clause)
  row9cells     the S074 registry row loses two cells                (H3 11-cell shape)
  thinscope     the S074 scope cell cut to three words              (H3 scope-words floor)
  kindcase      the S074 kind cell reads Docs                       (H3 kind literal)
  manws         manifest.json gains a trailing blank line           (H4 manifest sha pin)
  fewquotes     manifest S074 record keeps only the five core quotes (H4 >=8 quotes)
  dupquote      manifest S074 record duplicates one quote           (H4 distinct quotes)
  widespan      entry gains a quote cited across the whole snapshot  (H5 <=12-line span)
  longquote     entry gains a 30-word quoted span                   (H5 <=25 words)
  fewspans      entry loses one G-row (three valid spans remain)     (H5 >=4 located)
  nestedmd      corpus/knowledge/sub/x.md added                     (H6 no nested .md)
  entrymutant   one pinned entry gains a line                       (H6 content pin)
  symlink       corpus is replaced by a symlink to a real copy      (H7 no symlinks)

Usage: f29-defects.py --defect NAME --dir DEST [--lane LANE]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ENTRY_REL = "corpus/knowledge/github-repository-security-advisories.md"
MAN_REL = "corpus/source-snapshots/round-46-a2/manifest.json"


def sh(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--defect", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/kasegi-shokunin")
    a = ap.parse_args()
    sh([sys.executable, os.path.join(HERE, "f29-fixture.py"), "--mode", "positive", "--dir", a.dir, "--lane", a.lane])
    d = a.dir
    if a.defect == "duprow":
        p = os.path.join(d, "corpus/README.md")
        t = open(p, encoding="utf-8").read()
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        open(p, "w", encoding="utf-8").write(t + "\n" + row + "\n")
    elif a.defect == "fencedf29":
        p = os.path.join(d, "corpus/README.md")
        t = open(p, encoding="utf-8").read()
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        open(p, "w", encoding="utf-8").write(t.replace(row, "```\n" + row + "\n```", 1))
    elif a.defect == "vjunk":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("verified-at: 2026-10-29\n", "verified-at: 2026-10-29 # edited later\n", 1))
    elif a.defect == "thinsection":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        head, rest = t.split("## Scope and decision rule\n", 1)
        prose, tail = rest.split("\n\n| id |", 1)
        open(p, "w", encoding="utf-8").write(head + "## Scope and decision rule\n\nMaintainers draft privately first.\n\n| id |" + tail)
    elif a.defect == "badnames":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        t = t.replace("corpus/knowledge/github-private-vulnerability-reporting.md:3-6", "corpus/knowledge/program-quirks.md:3-6")
        t = t.replace("corpus/knowledge/cna-assignment-and-vulnerability-rules.md:12-20", "corpus/knowledge/program-quirks.md:12-20")
        open(p, "w", encoding="utf-8").write(t)
    elif a.defect == "row9cells":
        p = os.path.join(d, "corpus/SOURCES.md")
        t = open(p, encoding="utf-8").read()
        lines = t.splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if ln.startswith("| S074 |"):
                c = ln.strip().strip("|").split("|")
                del c[4:6]
                lines[i] = "|" + "|".join(c) + "|\n"
                break
        open(p, "w", encoding="utf-8").write("".join(lines))
    elif a.defect == "thinscope":
        p = os.path.join(d, "corpus/SOURCES.md")
        t = open(p, encoding="utf-8").read()
        lines = t.splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if ln.startswith("| S074 |"):
                c = ln.strip().strip("|").split("|")
                c[4] = " lifecycle ground only "
                lines[i] = "|" + "|".join(c) + "|\n"
                break
        open(p, "w", encoding="utf-8").write("".join(lines))
    elif a.defect == "kindcase":
        p = os.path.join(d, "corpus/SOURCES.md")
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(t.replace("| docs | A |", "| Docs | A |", 1))
    elif a.defect == "manws":
        p = os.path.join(d, MAN_REL)
        open(p, "a", encoding="utf-8").write("\n")
    elif a.defect == "fewquotes":
        p = os.path.join(d, MAN_REL)
        m = json.load(open(p, encoding="utf-8"))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        keep = {"Q1", "Q2", "Q4", "Q5", "Q9"}
        rec["quotes"] = [q for q in rec["quotes"] if q["id"] in keep]
        json.dump(m, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(p, "a", encoding="utf-8").write("\n")
    elif a.defect == "dupquote":
        p = os.path.join(d, MAN_REL)
        m = json.load(open(p, encoding="utf-8"))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        rec["quotes"].append(dict(rec["quotes"][4]))
        json.dump(m, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(p, "a", encoding="utf-8").write("\n")
    elif a.defect == "widespan":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        t += "\nWide-span note: “Repository security advisories” (`S074.txt:1-42`) spans the snapshot.\n"
        open(p, "w", encoding="utf-8").write(t)
    elif a.defect == "longquote":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        snap = open(os.path.join(d, "corpus/source-snapshots/round-46-a2/S074.txt"), encoding="utf-8").read().splitlines()
        words = " ".join(snap[9].split())
        long_text = " ".join(words.split()[:30])
        t += "\nLong note: “%s” (`S074.txt:10`).\n" % long_text
        open(p, "w", encoding="utf-8").write(t)
    elif a.defect == "fewspans":
        p = os.path.join(d, ENTRY_REL)
        t = open(p, encoding="utf-8").read()
        drop = [ln for ln in t.splitlines() if ln.startswith("| G6 |")][0]
        open(p, "w", encoding="utf-8").write(t.replace(drop + "\n", "", 1))
    elif a.defect == "nestedmd":
        os.makedirs(os.path.join(d, "corpus/knowledge/sub"), exist_ok=True)
        shutil.copy(os.path.join(d, ENTRY_REL), os.path.join(d, "corpus/knowledge/sub/note.md"))
    elif a.defect == "entrymutant":
        p = os.path.join(d, "corpus/knowledge/program-quirks.md")
        open(p, "a", encoding="utf-8").write("\nAppended line for the mutant pass.\n")
    elif a.defect == "symlink":
        real = os.path.join(d, "corpus-real")
        os.rename(os.path.join(d, "corpus"), real)
        os.symlink("corpus-real", os.path.join(d, "corpus"))
    else:
        print("unknown defect", a.defect)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
