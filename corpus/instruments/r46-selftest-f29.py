#!/usr/bin/env python3
"""r46-selftest-f29.py — selftest for corpus/instruments/r46-f29-gate.py v1 (round 46 attempt 2, C2, frontier F29).

WHAT IT GRADES
    The committed F29 counter (`corpus/instruments/r46-f29-gate.py`, seven limbs H1..H7) against
    synthetic trees built in scratch from the round-46 control recipes:

      ctl-positive        the positive tree must read 7/7 (every limb green).
      ctl-positive-cli    the counter's own CLI on the positive tree must print seven
                          `gate H<n> pass=1` lines and `f29-gate fixed=7/7 exit=0`.
      ctl-junk            the junk entry (the located quotes rewritten to text the capture does
                          not hold) must read H5 red and every other limb green.
      ctl-fabricated      the fabricated entry must read H5 red and every other limb green.
      defect-<name>       one defect tree per row of the R50 receipt's defect table
                          (`.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt`); the
                          targeted limb(s) read red and no other limb reads red.
      clause-a-counts-30  the H1 row-count clause: 30 admitted rows, unique ids -> only the
      clause-a-counts-28  count clause fires (receipt disclosure (a), first half).
      clause-a-raw-once   the H1 one-live-F29-row clause: two live F29 rows with a controlled id
                          set of 29 unique rows -> only that clause fires (disclosure (a)).
      clause-b-wordfloor  the H2 per-section word floor: a 21-word Scope section whose table
                          lives in another section -> only the floor fires (disclosure (b)).
      clause-d-quotecount the H4 >= 8 quote floor: seven valid quotes on a re-pinned manifest.
      clause-d-distinct   the H4 quote-distinctness floor: nine quotes, one text duplicated
                          (disclosure (d)).
      clause-e-located    the H5 >= 4 located-span floor: three located spans carrying all five
                          frozen cores on a rebuilt-PINS synthetic capture (disclosure (e)).

    The four shadowed clauses are graded on rebuilt-PINS synthetic trees: the counter module is
    imported and its PINS dict (and, for the H1 one-live-row clause only, its `frontier` reader)
    is overridden for that case's fixture alone; every override is restored right after the
    case and never touches the lane.

    Every case is graded in-process against the imported counter's own GATES list, so the same
    code grades the committed counter and any mutant copy of it (--counter PATH).

USAGE
    python3 r46-selftest-f29.py [--lane DIR] [--counter PATH] [--work DIR] [--pure DIR]
                               [--jobs N] [--do-nothing-control] [--keep] [-v]
READ-ONLY on --lane and --pure; scratch only under --work (default
$HYAKU_SCRATCH/kasegi-r46/R46bExecSelftestF29), removed on exit unless --keep.
OUTPUT
    one `ok  `/`FAIL` case line each, then `selftest cases=<N> failures=<F>`; exit 0 iff F == 0.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
ENTRY_REL = "corpus/knowledge/github-repository-security-advisories.md"
SNAP_REL = "corpus/source-snapshots/round-46-a2/S074.txt"
MAN_REL = "corpus/source-snapshots/round-46-a2/manifest.json"
README_REL = "corpus/README.md"
SOURCES_REL = "corpus/SOURCES.md"
URL = "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories"
LANE_CD = LANE_DEFAULT
ENTRY_NAME = "github-repository-security-advisories.md"
ALL_LIMBS = ("H1", "H2", "H3", "H4", "H5", "H6", "H7")

# sha256 of the two control builders whose tree recipes this file vendors; a drift is reported
# as a note (the recipes are vendored so the selftest stays self-contained).
BUILDER_PROVENANCE = {
    "f29-fixture.py": "52ea96939c62a71943838ca883d7914dd598f3e7eeb061266975ece7ccb26275",
    "f29-defects.py": "2e95d4d4b6cf372a8464803bf82c7ae79d1612dc8060b5a9c18798cfbcbc07c2",
}

# ------------------------------------------------------------------ vendored tree recipes
# (verbatim from .ufo/waves/round-46/attempt2/controls/f29-fixture.py)

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

F29_ROW = ("| F29 | GitHub repository security advisories — the maintainer-side advisory lifecycle "
           "(draft, private fork, CVE via GitHub as CNA, credit, publication, fix version) | admitted | "
           "corpus/knowledge/github-repository-security-advisories.md | S074 | Keep the maintainer flow "
           "distinct from the reporter flow (F28); re-open the page before relying on its mechanics. |")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha_bytes(fh.read())


def build_positive(dest: str, lane: str) -> None:
    """The positive tree recipe (f29-fixture.py --mode positive), vendored."""
    os.makedirs(os.path.join(dest, "corpus/knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dest, "corpus/source-snapshots/round-46-a2"), exist_ok=True)
    shutil.copy(os.path.join(lane, SNAP_REL), os.path.join(dest, SNAP_REL))
    shutil.copy(os.path.join(lane, MAN_REL), os.path.join(dest, MAN_REL))
    kd = os.path.join(lane, "corpus/knowledge")
    for n in sorted(os.listdir(kd)):
        p = os.path.join(kd, n)
        if n.endswith(".md") and os.path.isfile(p):
            shutil.copy(p, os.path.join(dest, "corpus/knowledge", n))
    with open(os.path.join(dest, ENTRY_REL), "w", encoding="utf-8") as fh:
        fh.write(ENTRY.format(url=URL, lane=LANE_CD))
    readme = open(os.path.join(lane, README_REL), encoding="utf-8").read()
    frows = [ln for ln in readme.splitlines() if ln.startswith("| F") and ln.count("|") >= 6]
    frows = [ln for ln in frows if ln.split("|")[1].strip().startswith("F")]
    if len(frows) != 28:
        raise SystemExit("selftest: lane README carries %d frontier rows, expected 28" % len(frows))
    out = readme.replace(frows[-1], frows[-1] + "\n" + F29_ROW, 1)
    with open(os.path.join(dest, README_REL), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(dest, SOURCES_REL), "w", encoding="utf-8") as fh:
        fh.write(SOURCES_HEAD + SOURCES_ROW.format(url=URL) + SOURCES_TAIL)


def build_mode(dest: str, lane: str, mode: str) -> None:
    """The junk / fabricated tree recipes (f29-fixture.py --mode junk|fabricated), vendored."""
    build_positive(dest, lane)
    body = {"positive": ENTRY, "junk": JUNK, "fabricated": FABRICATED}[mode]
    with open(os.path.join(dest, ENTRY_REL), "w", encoding="utf-8") as fh:
        fh.write(body.format(url=URL, lane=LANE_CD))


def rd(p: str) -> str:
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def wr(p: str, text: str) -> None:
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


def sub(path: str, old: str, new: str) -> None:
    text = rd(path)
    if old not in text:
        raise SystemExit("selftest: pattern not found in %s: %r" % (path, old[:60]))
    wr(path, text.replace(old, new, 1))


def apply_defect(dest: str, name: str) -> None:
    """One defect on top of the positive tree (f29-defects.py --defect NAME), vendored.

    `src0740` is the one defect the receipt names that the control builder does not carry: the
    F29 row's sources cell reads S0740 instead of S074 (H1's sources-cell clause).
    """
    if name == "src0740":
        p = os.path.join(dest, README_REL)
        t = rd(p)
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        wr(p, t.replace(row, row.replace("| S074 |", "| S0740 |", 1), 1))
        return
    p = os.path.join(dest, ENTRY_REL)
    if name == "duprow":
        p = os.path.join(dest, README_REL)
        t = rd(p)
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        wr(p, t + "\n" + row + "\n")
    elif name == "fencedf29":
        p = os.path.join(dest, README_REL)
        t = rd(p)
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        wr(p, t.replace(row, "```\n" + row + "\n```", 1))
    elif name == "vjunk":
        sub(p, "verified-at: 2026-10-29\n", "verified-at: 2026-10-29 # edited later\n")
    elif name == "thinsection":
        t = rd(p)
        head, rest = t.split("## Scope and decision rule\n", 1)
        prose, tail = rest.split("\n\n| id |", 1)
        wr(p, head + "## Scope and decision rule\n\nMaintainers draft privately first.\n\n| id |" + tail)
    elif name == "badnames":
        t = rd(p)
        t = t.replace("corpus/knowledge/github-private-vulnerability-reporting.md:3-6",
                      "corpus/knowledge/program-quirks.md:3-6")
        t = t.replace("corpus/knowledge/cna-assignment-and-vulnerability-rules.md:12-20",
                      "corpus/knowledge/program-quirks.md:12-20")
        wr(p, t)
    elif name == "row9cells":
        sp = os.path.join(dest, SOURCES_REL)
        lines = rd(sp).splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if ln.startswith("| S074 |"):
                c = ln.strip().strip("|").split("|")
                del c[4:6]
                lines[i] = "|" + "|".join(c) + "|\n"
                break
        wr(sp, "".join(lines))
    elif name == "thinscope":
        sp = os.path.join(dest, SOURCES_REL)
        lines = rd(sp).splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if ln.startswith("| S074 |"):
                c = ln.strip().strip("|").split("|")
                c[4] = " lifecycle ground only "
                lines[i] = "|" + "|".join(c) + "|\n"
                break
        wr(sp, "".join(lines))
    elif name == "kindcase":
        sp = os.path.join(dest, SOURCES_REL)
        sub(sp, "| docs | A |", "| Docs | A |")
    elif name == "manws":
        with open(os.path.join(dest, MAN_REL), "a", encoding="utf-8") as fh:
            fh.write("\n")
    elif name == "fewquotes":
        mp = os.path.join(dest, MAN_REL)
        m = json.loads(rd(mp))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        keep = {"Q1", "Q2", "Q4", "Q5", "Q9"}
        rec["quotes"] = [q for q in rec["quotes"] if q["id"] in keep]
        wr(mp, json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    elif name == "dupquote":
        mp = os.path.join(dest, MAN_REL)
        m = json.loads(rd(mp))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        rec["quotes"].append(dict(rec["quotes"][4]))
        wr(mp, json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    elif name == "widespan":
        t = rd(p)
        t += "\nWide-span note: “Repository security advisories” (`S074.txt:1-42`) spans the snapshot.\n"
        wr(p, t)
    elif name == "longquote":
        t = rd(p)
        snap = rd(os.path.join(dest, SNAP_REL)).splitlines()
        words = " ".join(snap[9].split())
        long_text = " ".join(words.split()[:30])
        t += "\nLong note: “%s” (`S074.txt:10`).\n" % long_text
        wr(p, t)
    elif name == "fewspans":
        t = rd(p)
        drop = [ln for ln in t.splitlines() if ln.startswith("| G6 |")][0]
        wr(p, t.replace(drop + "\n", "", 1))
    elif name == "nestedmd":
        os.makedirs(os.path.join(dest, "corpus/knowledge/sub"), exist_ok=True)
        shutil.copy(os.path.join(dest, ENTRY_REL), os.path.join(dest, "corpus/knowledge/sub/note.md"))
    elif name == "entrymutant":
        with open(os.path.join(dest, "corpus/knowledge/program-quirks.md"), "a", encoding="utf-8") as fh:
            fh.write("\nAppended line for the mutant pass.\n")
    elif name == "symlink":
        real = os.path.join(dest, "corpus-real")
        os.rename(os.path.join(dest, "corpus"), real)
        os.symlink("corpus-real", os.path.join(dest, "corpus"))
    else:
        raise SystemExit("selftest: unknown defect %s" % name)


# ------------------------------------------------------------------ shadowed-clause fixtures

WORD_FLOOR_ENTRY = """source: S074 — {url} — GitHub Docs, repository security advisories overview
verified-at: 2026-10-29
recheck: cd {lane} && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074

# GitHub repository security advisories — the maintainer-side advisory lifecycle

## Scope and decision rule

Maintainers draft the advisory privately, fix the flaw in a fork, then publish once a fix version exists (S074.txt:38).

## Evidence table

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
out of scope: the possibility of a submitted change is named, not the process. Verified against
the pinned capture only; a sweep at the round base named no maintainer-side entry (S074.txt:19).

## Falsifiable package rule

A claim-package advisory step is GitHub-conformant only if the draft advisory requests the CVE
from GitHub while private and adds a fix version before publication (S074.txt:25, S074.txt:38).

## Reading note

The table above carries the six quoted obligations and their located citations; the decision
rule names the actor, the private workspace, the numbering request and the publication duty. A
reader who wants the mechanics of the form itself must open the sibling page named in the
limits section above.
"""

LOCATED_COUNT_ENTRY = """source: S074 — {url} — GitHub Docs, repository security advisories overview
verified-at: 2026-10-29
recheck: cd {lane} && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074

# GitHub repository security advisories — the maintainer-side advisory lifecycle

## Scope and decision rule

Maintainer-side lifecycle ground for the selftest fixture: a project maintainer may privately
discuss and fix a security vulnerability in a public repository, collaborate in a temporary
private fork, ask GitHub for a CVE identification number, and publish the advisory once a fix
version exists (S074.txt:38). The table below lists the six obligations this entry rests on
without quoting them, so that the located-span count stays at three.

## Evidence table

| id | observed question | ground |
|---|---|---|
| G1 | What may maintainers do privately? | the private discussion and fix duty (S074.txt:10) |
| G2 | Where is the fix developed? | the temporary private fork duty (S074.txt:11) |
| G3 | Who assigns the CVE? | the numbering authority duty (S074.txt:24) |
| G4 | How fast is the request reviewed? | the review clock duty (S074.txt:25) |
| G5 | Does the request publish the advisory? | the publication boundary duty (S074.txt:26) |
| G6 | What must ship with publication? | the fix version duty (S074.txt:38) |

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
out of scope: the possibility of a submitted change is named, not the process. Verified against
the pinned capture only; a sweep at the round base named no maintainer-side entry (S074.txt:19).

## Falsifiable package rule

A claim-package advisory step is GitHub-conformant only if the draft advisory requests the CVE
from GitHub while private and adds a fix version before publication (S074.txt:25, S074.txt:38).

## Reading note

The three quoted spans below carry the five frozen cores of this entry; the table above lists
the six obligations without quoting them, so the located-span count stays at three and the
floor clause can be graded on its own.

## Quoted spans

1. The private duty and the fork duty in one span: “privately discuss and fix a security vulnerability in a project. Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:10-11`)
2. The numbering duty and the review clock in one span: “authorized to assign CVE identification numbers. GitHub usually reviews the request within 72 hours.” (`S074.txt:24-25`)
3. The fix-version duty: “you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`)
"""

# The synthetic capture used by the H5 located-span floor case: the five frozen cores sit on
# lines 10-11, 24-25 and 38 so that three located spans can carry all five.
SYNTH_LINES = {
    1: "# Synthetic capture fixture for r46-selftest-f29.py (not a real page).",
    2: "## Repository security advisories",
    3: "Synthetic stand-in text for the GitHub Docs overview page; it exists only so that the",
    4: "H5 located-span floor can be graded on its own.",
    5: "## Who can use this feature?",
    6: "Synthetic filler line.",
    7: "Synthetic filler line.",
    8: "Synthetic filler line.",
    9: "Synthetic filler line.",
    10: "Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.",
    11: "Privately collaborate to fix the vulnerability in a temporary private fork.",
    12: "Synthetic filler line.",
    13: "Synthetic filler line.",
    14: "Synthetic filler line.",
    15: "## About repository security advisories",
    16: "Synthetic filler line.",
    17: "Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.",
    18: "Synthetic filler line.",
    19: "Synthetic filler line.",
    20: "Publish the security advisory to alert your community of the vulnerability once a patch is released.",
    21: "Synthetic filler line.",
    22: "## CVE identification numbers",
    23: "Synthetic filler line.",
    24: "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.",
    25: "GitHub usually reviews the request within 72 hours.",
    26: "Requesting a CVE identification number doesn't make your security advisory public.",
    27: "Synthetic filler line.",
    28: "Synthetic filler line.",
    29: "Synthetic filler line.",
    30: "## Publication of security advisories",
    31: "Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.",
    32: "Synthetic filler line.",
    33: "Synthetic filler line.",
    34: "Synthetic filler line.",
    35: "Synthetic filler line.",
    36: "Synthetic filler line.",
    37: "## Importance of fix versions",
    38: "Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory.",
    39: "Synthetic filler line.",
    40: "Synthetic filler line.",
    41: "Synthetic filler line.",
    42: "Synthetic filler line.",
}

SYNTH_QUOTES = [
    ("Q1", 10, "Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project."),
    ("Q2", 11, "Privately collaborate to fix the vulnerability in a temporary private fork."),
    ("Q3", 17, "Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project."),
    ("Q4", 24, "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers."),
    ("Q5", 25, "GitHub usually reviews the request within 72 hours."),
    ("Q6", 26, "Requesting a CVE identification number doesn't make your security advisory public."),
    ("Q7", 31, "Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted."),
    ("Q8", 38, "you should add a fix version to a security advisory prior to publishing the advisory"),
    ("Q9", 20, "Publish the security advisory to alert your community of the vulnerability once a patch is released."),
]


def synth_snapshot_text() -> str:
    return "\n".join(SYNTH_LINES[i] for i in range(1, 43)) + "\n"


def synth_manifest(snap_sha: str, snap_bytes: int) -> str:
    rec = {
        "id": "S074",
        "url": URL,
        "capture_url": URL,
        "http": {"status": 200, "final_url": URL},
        "kind": "html",
        "fetched_utc": "2026-10-29T20:19:30Z",
        "path": "S074.txt",
        "sha256": snap_sha,
        "bytes": snap_bytes,
        "snapshot_bytes": snap_bytes,
        "lines": 42,
        "quotes": [{"id": qid, "anchor": anchor, "quote": text} for qid, anchor, text in SYNTH_QUOTES],
    }
    return json.dumps({"schema_version": 1, "sources": [rec]}, indent=1, ensure_ascii=False) + "\n"


def live_lines(text: str) -> list[str]:
    """The counter's live-line rule (fenced and HTML-commented lines are not live)."""
    out = []
    fence = False
    for ln in text.splitlines():
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence or not st or st.startswith("<!--"):
            continue
        out.append(ln)
    return out


def pad_entry(path: str, minimum: int = 3200) -> None:
    """Pad an entry with plain prose (no quotes) so H6's byte floor stays green."""
    text = rd(path)
    if len(text.encode("utf-8")) >= minimum:
        return
    filler = ("\n\nReading note: the obligations above are read from the pinned capture only; the "
              "form fields, the editing flow and the advisory database remain on sibling pages "
              "that this row does not hold, and a reader who needs them must open those pages "
              "directly rather than trusting this summary of them.\n")
    while len((text + filler).encode("utf-8")) < minimum:
        text += filler
    wr(path, text)


# ------------------------------------------------------------------ counter loading / grading

def load_counter(path: str):
    spec = importlib.util.spec_from_file_location("r46_f29_gate_under_test", path)
    if spec is None or spec.loader is None:
        raise SystemExit("selftest: cannot load counter %s" % path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def grade(mod, root: str) -> list[tuple[str, int, str]]:
    """Run the counter's own limb list over a tree, exactly as its main() does."""
    out = []
    for name, fn in mod.GATES:
        try:
            ok, read = fn(root)
        except Exception as exc:  # a limb that raises is red, never green (the counter's own rule)
            ok, read = False, "limb-error=%s" % type(exc).__name__
        out.append((name, 1 if ok else 0, str(read)))
    return out


def run_cli(counter: str, root: str, work: str) -> tuple[int, str]:
    p = subprocess.run([sys.executable, counter, "--root", root, "--work", work],
                       capture_output=True, text=True, timeout=300)
    return p.returncode, p.stdout


# ------------------------------------------------------------------ cases

class Case:
    def __init__(self, name, kind, build, red, note="", patch=None):
        self.name = name
        self.kind = kind
        self.build = build
        self.red = set(red)
        self.note = note
        self.patch = patch  # patch(mod, root) -> restore(); grader-side override for this case only


def patch_pins(values):
    """Grader-side PINS override for one case's fixture only (restored right after)."""
    def _patch(mod, root):
        if not hasattr(mod, "PINS"):
            return lambda: None  # a counter without pins (the do-nothing stub) needs no override
        saved = dict(mod.PINS)
        mod.PINS.update(values)
        def restore():
            mod.PINS.clear()
            mod.PINS.update(saved)
        return restore
    return _patch


def patch_frontier(rows):
    """Grader-side controlled id set for the H1 one-live-row clause (restored right after)."""
    def _patch(mod, root):
        had = hasattr(mod, "frontier")
        saved = getattr(mod, "frontier", None)
        mod.frontier = lambda root: rows
        def restore():
            if had:
                mod.frontier = saved
            else:
                del mod.frontier
        return restore
    return _patch


def read_frontier(root: str) -> list[list[str]]:
    """The README's frontier rows, read the way the counter reads them."""
    p = os.path.join(root, README_REL)
    rows = []
    if not os.path.isfile(p):
        return rows
    for ln in live_lines(rd(p)):
        if re.match(r"^\| F\d+ \|", ln):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows


def controlled_rows(root: str, mod) -> list[list[str]]:
    """The README's own frontier rows minus the duplicate F29 row: 29 unique admitted rows."""
    reader = getattr(mod, "frontier", None)
    rows = list(reader(root)) if reader else read_frontier(root)
    seen = set()
    out = []
    for r in rows:
        if r and r[0] == "F29":
            if "F29" in seen:
                continue
            seen.add("F29")
        out.append(r)
    return out


def build_cases(lane: str, work: str) -> list[Case]:
    cases: list[Case] = []

    # ---- controls -------------------------------------------------------------
    cases.append(Case("positive", "ctl", lambda d: build_positive(d, lane), [],
                      note="the positive tree must read 7/7"))
    cases.append(Case("junk", "ctl", lambda d: build_mode(d, lane, "junk"), ["H5"],
                      note="quotes rewritten to text the capture does not hold"))
    cases.append(Case("fabricated", "ctl", lambda d: build_mode(d, lane, "fabricated"), ["H5"],
                      note="two quotes reworded away from the capture"))

    # ---- the receipt's defect trees ------------------------------------------
    # targeted limb(s) per row of the receipt's defect table; the vectors below are the
    # clause-level readings of the committed counter on those trees.
    defects = [
        ("duprow", ["H1"], "a duplicated live F29 row trips H1's duplicate-id clause"),
        ("fencedf29", ["H1"], "the F29 row inside a code fence leaves 28 live rows"),
        ("src0740", ["H1"], "the F29 row's sources cell reads S0740 instead of S074"),
        ("vjunk", ["H2"], "the verified-at line gains a trailing comment (exact-line clause)"),
        ("thinsection", ["H6"], "the Scope prose is cut to four words; the table stays, so H2's "
                                "word floor still holds and the entry falls under H6's byte floor"),
        ("badnames", ["H2"], "the two cross-references point at unrelated in-range files"),
        ("row9cells", ["H3", "H7"], "the S074 registry row loses two cells; the census then rejects it"),
        ("thinscope", ["H3"], "the scope cell is cut to three words"),
        ("kindcase", ["H3", "H7"], "the kind cell reads Docs; the census rejects the enum"),
        ("manws", ["H4"], "the manifest gains a trailing blank line (byte pin)"),
        ("fewquotes", ["H4"], "the manifest keeps only the five core quotes (byte pin)"),
        ("dupquote", ["H4"], "the manifest duplicates one quote (byte pin)"),
        ("widespan", ["H5"], "a quote is cited across the whole snapshot (span floor)"),
        ("longquote", ["H5"], "a 30-word real-text quote (word floor)"),
        ("fewspans", ["H2", "H5"], "the G6 row is dropped: five table rows and one core missing"),
        ("nestedmd", ["H6"], "corpus/knowledge/sub/note.md is added"),
        ("entrymutant", ["H6"], "a pinned knowledge entry gains a line (content pin)"),
        ("symlink", ["H6", "H7"], "corpus is replaced by a symlink"),
    ]
    for name, red, note in defects:
        cases.append(Case("defect-" + name, "defect",
                          (lambda n: lambda d: (build_positive(d, lane), apply_defect(d, n)))(name),
                          red, note=note))

    # ---- the gate-level-shadowed clauses -------------------------------------
    def counts30(d):
        build_positive(d, lane)
        p = os.path.join(d, README_REL)
        t = rd(p)
        wr(p, t + "\n| F30 | Synthetic extra frontier row | admitted | corpus/knowledge/program-quirks.md | S000 | Row-count clause fixture. |\n")
    cases.append(Case("clause-a-counts-30", "clause", counts30, ["H1"],
                      note="30 admitted rows, unique ids: only H1's count clause fires"))

    def counts28(d):
        build_positive(d, lane)
        p = os.path.join(d, README_REL)
        t = rd(p)
        row = [ln for ln in t.splitlines() if ln.startswith("| F01 |")][0]
        wr(p, t.replace(row + "\n", "", 1))
    cases.append(Case("clause-a-counts-28", "clause", counts28, ["H1"],
                      note="28 admitted rows, unique ids: only H1's count clause fires"))

    def rawonce(d):
        build_positive(d, lane)
        apply_defect(d, "duprow")
    cases.append(Case("clause-a-raw-once", "clause", rawonce, ["H1"],
                      note="two live F29 rows over a controlled 29-row id set: only H1's "
                           "one-live-row clause fires",
                      patch=lambda mod, root: patch_frontier(controlled_rows(root, mod))(mod, root)))

    # (b) H2's per-section word floor: the Scope section is cut below 25 words while its table
    # moves into another section, so the table-row conjunct cannot shadow the floor.
    def wordfloor(d):
        build_positive(d, lane)
        p = os.path.join(d, ENTRY_REL)
        wr(p, WORD_FLOOR_ENTRY.format(url=URL, lane=LANE_CD))
        pad_entry(p)
        body = "\n".join(live_lines(rd(p)))
        m = re.search(r"^## Scope and decision rule\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
        words = len(re.findall(r"\w+", m.group(1))) if m else 0
        if not (13 <= words <= 24):
            raise SystemExit("selftest: word-floor fixture has %d words in the Scope section "
                             "(want 13..24: below the 25-word floor, above any relaxed floor)" % words)
    cases.append(Case("clause-b-wordfloor", "clause", wordfloor, ["H2"],
                      note="a 21-word Scope section whose six-row table lives in another section"))

    # (d) H4's quote floors: the manifest byte pin is re-pinned to the edited manifest, so the
    # quote-count and quote-distinctness floors can fire on their own.
    def quotecount(d):
        build_positive(d, lane)
        mp = os.path.join(d, MAN_REL)
        m = json.loads(rd(mp))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        keep = {"Q1", "Q2", "Q3", "Q4", "Q5", "Q7", "Q9"}  # seven quotes, seven distinct anchors
        rec["quotes"] = [q for q in rec["quotes"] if q["id"] in keep]
        wr(mp, json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    cases.append(Case("clause-d-quotecount", "clause", quotecount, ["H4"],
                      note="seven valid quotes (all five cores, seven distinct anchors) on a re-pinned manifest",
                      patch=lambda mod, root: patch_pins({"manifest.json": sha_file(os.path.join(root, MAN_REL))})(mod, root)))

    def distinct(d):
        build_positive(d, lane)
        mp = os.path.join(d, MAN_REL)
        m = json.loads(rd(mp))
        rec = [s for s in m["sources"] if s["id"] == "S074"][0]
        dup = dict(rec["quotes"][0])
        dup["id"] = "Q10"
        rec["quotes"].append(dup)
        wr(mp, json.dumps(m, indent=1, ensure_ascii=False) + "\n")
    cases.append(Case("clause-d-distinct", "clause", distinct, ["H4"],
                      note="ten quotes of which one text is duplicated, on a re-pinned manifest",
                      patch=lambda mod, root: patch_pins({"manifest.json": sha_file(os.path.join(root, MAN_REL))})(mod, root)))

    # (e) H5's located-span floor: a rebuilt-PINS synthetic capture carries the five frozen cores
    # on lines 10-11, 24-25 and 38, so three located spans hold all five.
    def locatedcount(d):
        build_positive(d, lane)
        text = synth_snapshot_text()
        raw = text.encode("utf-8")
        wr(os.path.join(d, SNAP_REL), text)
        mp = os.path.join(d, MAN_REL)
        wr(mp, synth_manifest(sha_bytes(raw), len(raw)))
        sub(os.path.join(d, SOURCES_REL),
            "1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039", sha_bytes(raw))
        p = os.path.join(d, ENTRY_REL)
        wr(p, LOCATED_COUNT_ENTRY.format(url=URL, lane=LANE_CD))
        pad_entry(p)
    cases.append(Case("clause-e-located", "clause", locatedcount, ["H5"],
                      note="three located spans carrying all five frozen cores, six cited table rows",
                      patch=lambda mod, root: patch_pins({
                          "S074.txt": sha_file(os.path.join(root, SNAP_REL)),
                          "manifest.json": sha_file(os.path.join(root, MAN_REL)),
                      })(mod, root)))
    # (c) H3's 11-cell shape clause: a twelve-cell row is rejected by the base counter (the
    # shape test) but a relaxed `len(c) >= 9` mutant parses the first eleven cells and reads
    # green, so the relaxation is isolable and is not closed by construction.
    def cells12(d):
        build_positive(d, lane)
        sp = os.path.join(d, SOURCES_REL)
        lines = rd(sp).splitlines(keepends=True)
        for i, ln in enumerate(lines):
            if ln.startswith("| S074 |"):
                lines[i] = ln.rstrip("\n") + " | extra cell |\n"
                break
        wr(sp, "".join(lines))
    cases.append(Case("clause-c-cells-12", "clause", cells12, ["H3", "H7"],
                      note="a twelve-cell S074 row: the shape clause fires (the census rejects it too)"))

    return cases


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=LANE_DEFAULT)
    ap.add_argument("--counter", default=None, help="counter under test (default: the lane's r46-f29-gate.py)")
    ap.add_argument("--work", default=None)
    ap.add_argument("--pure", default=None, help="accepted for interface parity; the F29 trees are built from the lane's committed corpus")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--do-nothing-control", action="store_true")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args(argv)

    scratch_root = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    seat_dir = os.path.join(scratch_root, "kasegi-r46", "R46bExecSelftestF29")
    work = a.work or os.path.join(seat_dir, "work")
    os.makedirs(work, exist_ok=True)
    counter_path = a.counter or os.path.join(a.lane, "corpus/instruments/r46-f29-gate.py")
    if not os.path.isfile(counter_path):
        print("selftest: counter not found: %s" % counter_path)
        return 2
    if not os.path.isdir(a.lane):
        print("selftest: lane not found: %s" % a.lane)
        return 2

    # provenance of the vendored tree recipes (a drift is a note, not a failure)
    for name, want in sorted(BUILDER_PROVENANCE.items()):
        p = os.path.join(a.lane, ".ufo/waves/round-46/attempt2/controls", name)
        if os.path.isfile(p):
            got = sha_file(p)
            print("note provenance %s sha256=%s %s" % (name, got, "matches" if got == want else "DRIFTED"))

    cases = build_cases(a.lane, work)

    if a.do_nothing_control:
        stub = os.path.join(work, "do-nothing-counter.py")
        wr(stub, "GATES = [%s]\n" % ", ".join('("H%d", lambda root: (True, "stub"))' % i for i in range(1, 8)))
        counter_path = stub
        print("note do-nothing control counter: %s" % stub)

    mod = load_counter(counter_path)
    cases_n = 0
    failures = 0
    try:
        for c in cases:
            root = os.path.join(work, c.name)
            shutil.rmtree(root, ignore_errors=True)
            c.build(root)
            restore = None
            if c.patch:
                restore = c.patch(mod, root)
            try:
                res = grade(mod, root)
            finally:
                if restore:
                    restore()
            gates = {n: v for n, v, _ in res}
            reads = {n: r for n, _, r in res}
            failing = {n for n, v in gates.items() if v == 0}
            fixed = sum(gates.values())
            reasons = []
            if sorted(gates) != sorted(ALL_LIMBS):
                reasons.append("limb-lines-missing=%s" % sorted(set(ALL_LIMBS) - set(gates)))
            if failing != c.red:
                reasons.append("expected-red=%s actual-red=%s" % (sorted(c.red), sorted(failing)))
            if c.red and fixed == 7:
                reasons.append("tree read 7/7")
            if not c.red and fixed != 7:
                reasons.append("expected 7/7, read %d/7" % fixed)
            ok = not reasons
            if a.do_nothing_control:
                # the stub counter always reads green: every case that expects a red limb must
                # be reported FAIL, and the all-green case must still pass.
                ctrl_ok = (not ok) == bool(c.red)
            else:
                ctrl_ok = ok
            cases_n += 1
            failures += 0 if ctrl_ok else 1
            print("%s %-7s %-22s fixed=%d/7 failing=%s" % ("ok  " if ok else "FAIL", c.kind, c.name, fixed, sorted(failing))
                  + ("" if ok else "  <- " + "; ".join(reasons))
                  + ("" if ctrl_ok else "  <- control: unexpected outcome"))
            if a.verbose or not ok:
                for n in ALL_LIMBS:
                    print("       gate %s pass=%d read=%s" % (n, gates.get(n, -1), reads.get(n, "?")))

        # the counter's own CLI on the positive tree
        root = os.path.join(work, "positive")
        rc, out = run_cli(counter_path, root, os.path.join(work, "cli-work"))
        lines = [ln for ln in out.splitlines() if ln.startswith("gate ")]
        summary = [ln for ln in out.splitlines() if ln.startswith("f29-gate ")]
        ok = (rc == 0 and len(lines) == 7 and all("pass=1" in ln for ln in lines)
              and summary == ["f29-gate fixed=7/7 exit=0"])
        ctrl_ok = (not ok) if a.do_nothing_control else ok  # the stub has no CLI: it must fail
        cases_n += 1
        failures += 0 if ctrl_ok else 1
        print("%s %-7s %-22s rc=%d gates=%d summary=%s" % ("ok  " if ok else "FAIL", "ctl", "positive-cli", rc, len(lines), summary))
        if not ok:
            print("       " + out.replace("\n", "\n       "))
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
            try:
                os.rmdir(seat_dir)
            except OSError:
                pass
        else:
            print("scratch kept: %s" % work)
    if a.do_nothing_control:
        print("note control: the stub counter reads green everywhere; every red-expecting case "
              "must be reported FAIL (unexpected outcomes counted as failures above)")
    print("selftest cases=%d failures=%d" % (cases_n, failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
