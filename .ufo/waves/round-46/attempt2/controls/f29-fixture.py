#!/usr/bin/env python3
"""Build minimal synthetic trees for the r46-f29-gate.py R50 pre-freeze mutant pass.

Modes:
  positive   a tree that should read 7/7 on the unmutated gate (entry + rows + capture +
             manifest + census-clean SOURCES.md + 66-entry knowledge dir from the real one);
  junk       the positive tree with the entry replaced by marker-only filler (no located
             quotes) — must NOT read 7/7 (H2/H5 red);
  fabricated the positive tree with the entry's quotes rewritten to text the snapshot does
             not hold (citations kept) — must NOT read 7/7 (H5 red).

Usage: f29-fixture.py --mode MODE --dir DEST [--lane LANE]
The tree is minimal but self-consistent: census --file on its SOURCES.md must exit 0, so
H7 stays green in every mode and the mutant pass isolates the other limbs.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
ENTRY_REL = "corpus/knowledge/github-repository-security-advisories.md"
URL = "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories"
LANE_CD = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"

ENTRY = """source: S074 — {url} — GitHub Docs, repository security advisories overview
verified-at: 2026-10-29
recheck: cd {lane} && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074

# GitHub repository security advisories — the maintainer-side advisory lifecycle

## Scope and decision rule

Maintainer-side lifecycle ground: a repository security advisory lets a project's maintainers
privately discuss and fix a security vulnerability in a public repository, collaborate in a
temporary private fork, request a CVE identification number from GitHub (a CNA that usually
reviews the request within 72 hours without making the advisory public), give credit to
contributors, and publish once a fix version exists. Decision rule: a maintainer drafts the
advisory before publishing and should add a fix version prior to publishing the advisory,
otherwise dependabot alerts ship without a safe version (S074.txt:38).

| id | observed question | ground |
|---|---|---|
| G1 | What may maintainers do privately? | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S074.txt:10`) |
| G2 | Where is the fix developed? | “Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`) |
| G3 | Who assigns the CVE? | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S074.txt:24`) |
| G4 | How fast is the CVE request reviewed? | “GitHub usually reviews the request within 72 hours.” (`S074.txt:25`) |
| G5 | Does the CVE request publish the advisory? | “Requesting a CVE identification number doesn't make your security advisory public.” (`S074.txt:25`) |
| G6 | What must ship with publication? | “you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`) |

## Overlap and novelty

Contrast with the reporter-side flow held as F28: corpus/knowledge/github-private-vulnerability-reporting.md:3-6
holds the reporter's enablement-gated private report; this entry holds the maintainer's draft,
fork, credit and publication duties, a different actor on the same object. Contrast with the
CNA rule set held as F07: corpus/knowledge/cna-assignment-and-vulnerability-rules.md:12-20 holds
the program's assignment scope; this entry holds the platform's per-advisory request mechanics
and the boundary that GitHub cannot assign CVEs to a project covered by another CNA (S074.txt:26).

## Limits

This capture is the overview page only: the form-field detail, the editing flow and the REST API
live on sibling pages this row does not hold (S074.txt:19). The advisory database's edit flow is
out of scope: “Anyone can submit a change to an advisory published in the GitHub Advisory Database.”
(S074.txt:19) names the possibility, not the process. Verified against the pinned capture only;
a `grep -c "repository security advisor" corpus/knowledge/*.md` sweep at the round base named no
maintainer-side entry.

## Falsifiable package rule

A claim-package advisory step is GitHub-conformant only if the draft advisory requests the CVE
from GitHub while private and adds a fix version before publication (S074.txt:25, S074.txt:38).
"""

JUNK = ENTRY.replace("privately discuss and fix a security vulnerability", "handle the matter carefully")
JUNK = JUNK.replace("temporary private fork", "a special collaboration space")
JUNK = JUNK.replace("authorized to assign CVE identification numbers", "allowed to hand out identifiers")
JUNK = JUNK.replace("reviews the request within 72 hours", "is quick about it")
JUNK = JUNK.replace("add a fix version to a security advisory prior to publishing", "get the version right early")

FABRICATED = ENTRY.replace("reviews the request within 72 hours", "reviews the request within one business day")
FABRICATED = FABRICATED.replace("doesn't make your security advisory public", "keeps the advisory strictly confidential forever")

SOURCES_HEAD = """# SOURCES — where kasegi learns

## Search log

- round-46 attempt 2: opened the GitHub Docs repository-security-advisories overview (S074).

## Registry

"""
SOURCES_ROW = ("| S074 | GitHub Docs, Repository security advisories — {url} | docs | A | "
               "GitHub's own statement of the maintainer-side advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side flow, advisory editing or the REST API | "
               "heading and body prose lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL), "
               "sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 | "
               "Read the maintainer's draft-publish cycle and its clocks from the platform page, keeping the actor distinct from F28's reporter. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |\n")
SOURCES_TAIL = """
## By scope

- github-docs: S074.
"""


def build(mode: str, dest: str, lane: str) -> int:
    src = lane
    os.makedirs(os.path.join(dest, "corpus/knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dest, "corpus/source-snapshots/round-46-a2"), exist_ok=True)
    # snapshot + manifest, byte-exact
    shutil.copy(os.path.join(src, "corpus/source-snapshots/round-46-a2/S074.txt"),
                os.path.join(dest, "corpus/source-snapshots/round-46-a2/S074.txt"))
    shutil.copy(os.path.join(src, "corpus/source-snapshots/round-46-a2/manifest.json"),
                os.path.join(dest, "corpus/source-snapshots/round-46-a2/manifest.json"))
    # 66-entry knowledge dir: the real one plus the synthetic entry
    kd = os.path.join(src, "corpus/knowledge")
    for n in sorted(os.listdir(kd)):
        p = os.path.join(kd, n)
        if n.endswith(".md") and os.path.isfile(p):
            shutil.copy(p, os.path.join(dest, "corpus/knowledge", n))
    body = {"positive": ENTRY, "junk": JUNK, "fabricated": FABRICATED}[mode]
    with open(os.path.join(dest, ENTRY_REL), "w", encoding="utf-8") as fh:
        fh.write(body.format(url=URL, lane=LANE_CD))
    # README frontier table: 29 rows (F01..F28 from the real README + one F29 line)
    readme = open(os.path.join(src, "corpus/README.md"), encoding="utf-8").read()
    frows = [ln for ln in readme.splitlines() if ln.startswith("| F") and ln.count("|") >= 6]
    frows = [ln for ln in frows if ln.split("|")[1].strip().startswith("F")]
    f29row = ("| F29 | GitHub repository security advisories — the maintainer-side advisory lifecycle "
              "(draft, private fork, CVE via GitHub as CNA, credit, publication, fix version) | admitted | "
              "corpus/knowledge/github-repository-security-advisories.md | S074 | Keep the maintainer flow "
              "distinct from the reporter flow (F28); re-open the page before relying on its mechanics. |")
    assert len(frows) == 28, len(frows)
    out = readme.replace(frows[-1], frows[-1] + "\n" + f29row, 1)
    with open(os.path.join(dest, "corpus/README.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(dest, "corpus/SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write(SOURCES_HEAD + SOURCES_ROW.format(url=URL, url2=URL) + SOURCES_TAIL)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["positive", "junk", "fabricated"])
    ap.add_argument("--dir", required=True)
    ap.add_argument("--lane", default=LANE_DEFAULT)
    a = ap.parse_args()
    if os.path.isdir(a.dir):
        shutil.rmtree(a.dir)
    build(a.mode, a.dir, a.lane)
    return 0


if __name__ == "__main__":
    sys.exit(main())
