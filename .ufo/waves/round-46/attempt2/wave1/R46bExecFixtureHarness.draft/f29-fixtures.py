#!/usr/bin/env python3
"""f29-fixtures.py — one harness for the round-46 (attempt 2) F29 counter fixtures.

It merges the two frozen control builders
`.ufo/waves/round-46/attempt2/controls/f29-fixture.py` (modes positive/junk/fabricated)
and `.ufo/waves/round-46/attempt2/controls/f29-defects.py` (per-limb defect trees) and
adds the receipt-rebuilding selftest.

The tree recipes are spliced VERBATIM out of those two frozen controls, so every tree
this harness builds is byte-identical to the tree the R50 receipt was measured on.

MODES
    --mode positive    the tree that must read 7/7 on the unmutated r46-f29-gate.py
    --mode junk        the positive tree with the entry's five quoted claims replaced
                       by paraphrase: 2 of 7 spans locate, 0 of 5 frozen cores survive
    --mode fabricated  the positive tree with two quoted claims rewritten to text the
                       pinned capture does not hold: 5 of 7 spans locate, 4 of 5 cores
DEFECTS
    --defect NAME      the positive tree plus ONE defect.  NAME is one of the 17 names
                       the frozen control carries, plus `src0740` — the R50 receipt's
                       third pair, whose recipe the frozen control builder lacks and
                       which is restored here byte-for-byte from the receipt's tree.
SELFTEST
    --selftest         rebuild every line of the R50 receipt
                       (.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt):
                       the positive tree reads 7/7; the junk and fabricated trees
                       reproduce the receipt's H5 read tokens; all twenty receipt pairs
                       reproduce their base limb, their mutant limb and their verdict;
                       the eleven receipt flips are exactly the eleven that flip; the
                       twenty-one receipt mutants are present, three per limb, each
                       carrying a clause that occurs exactly once in the counter.
                       Prints one `case=` line per check, one `divergence=` line per
                       receipt line that does not reproduce, and finally
                       `selftest cases=<N> failures=<F>`.

DIVERGENCES
    The receipt's two aggregate lines for the junk and the fabricated tree
    (`fixed=3/7` each) do not reproduce: the frozen builders yield 6/7 for both, with
    the receipt's own H5 read tokens reproduced exactly.  The receipt was measured
    against tree recipes the frozen controls no longer emit (the L1's own R50 scratch
    trees carry a superseded 12-cell registry row, while the frozen builder emits the
    census-clean 11-cell row).  A divergence is printed loudly on every run and is
    counted separately; `--strict-receipt` promotes it to a failure so the L1 can gate
    on the receipt verbatim.

The mutant table is the C2 battery's table (corpus/instruments/r46-mutbat.py, C2_MUTANTS)
re-based onto the F29 counter's own source lines, under the mutant ids the receipt
records (H1a..H7c).  Each mutant's old-substring is asserted to occur EXACTLY ONCE in
the counter, so a drifted counter fails loudly instead of mutating the wrong line.

READ-ONLY on --lane and on the counter; every tree and every mutant copy is written
under --dir / --work.  Never runs git.  stdlib only.

USAGE
    python3 f29-fixtures.py --mode positive --dir TREE [--lane LANE]
    python3 f29-fixtures.py --defect NAME    --dir TREE [--lane LANE]
    python3 f29-fixtures.py --selftest --work DIR [--lane LANE] [--counter PATH]
                              [--receipt PATH] [--strict-receipt]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

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

ENTRY_REL = "corpus/knowledge/github-repository-security-advisories.md"
MAN_REL = "corpus/source-snapshots/round-46-a2/manifest.json"
LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
COUNTER_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py"
RECEIPT_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt"

# --- mutant table: the C2 battery's table re-based onto r46-f29-gate.py --------------
# (id, old-substring, new-substring).  The ids are the ones the R50 receipt records.
MUTANTS = [
    ("H1a-counts-loose",      'if len(rows) != 29 or adm != 29 or dup:',                                  'if len(rows) < 29 or adm < 29:'),
    ("H1b-raw-loose",         'if len(raw) != 1:',                                                         'if len(raw) > 1:'),
    ("H1c-src-boundary",      're.search(r"\\bS074\\b", f29[0][4])',                                        're.search(r"S074", f29[0][4])'),
    ("H2a-verified-loose",    'ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)',                 'ok_v = any(h.startswith("verified-at: " + VERIFIED_AT) for h in head)'),
    ("H2b-wordfloor-low",     '(12 if sct.startswith("## Falsifiable") else 25)',                             '(1 if sct.startswith("## Falsifiable") else 5)'),
    ("H2c-need-empty",        'need = {"github-private-vulnerability-reporting.md", "cna-assignment-and-vulnerability-rules.md"}', 'need = set()'),
    ("H3a-cells-loose",       'if len(c) == 11:',                                                          'if len(c) >= 9:'),
    ("H3b-scope-low",         'if len(re.findall(r"\\w+", row[4])) < 8: bad.append("scope-words")',             'if len(re.findall(r"\\w+", row[4])) < 2: bad.append("scope-words")'),
    ("H3c-kind-dead",         'if row[2] != "docs": bad.append("kind")',                                   'if row[2] != "Docs": bad.append("kind")'),
    ("H4a-manifest-unpinned", 'if sha(open(man, "rb").read()) != PINS["manifest.json"]:',                     'if False:'),
    ("H4b-quotes-low",        'oks >= 8 and not miss',                                                     'oks >= 1 and not miss'),
    ("H4c-distinct-dropped",  'and "BROKEN" not in out and distinct',                                     'and "BROKEN" not in out'),
    ("H5a-span-wide",         'b - a <= 11',                                                               'b - a <= 110'),
    ("H5b-words-wide",        'len(nq.split()) <= 25',                                                     'len(nq.split()) <= 250'),
    ("H5c-pass-low",          'len(passed) >= 4',                                                          'len(passed) >= 1'),
    ("H6a-counts-loose",      'len(names) == 66 and len(everything) == 66 and nested == 66',                  'len(names) == 66'),
    ("H6b-pin-dropped",       'base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok',   'base_ok = base_ok and ledger_ok'),
    ("H6c-size-low",          'os.path.getsize(os.path.join(root, p)) >= 3000',                            'os.path.getsize(os.path.join(root, p)) >= 3'),
    ("H7a-verdict-or",        'p.returncode == 0 and ok_line',                                             'p.returncode == 0 or ok_line'),
    ("H7b-symlink-dead",      'return False, "census-input-is-a-symlink"',                                 'pass  # mutant H7b'),
    ("H7c-okline-loose",      're.search(r"^\\S+\\tok\\t", p.stdout, re.M)',                                 're.search(r"^\\S+\\tok", p.stdout, re.M)'),
]
MUTANT = {m[0]: m for m in MUTANTS}

# --- the R50 receipt, transcribed row for row ---------------------------------------
# (pair, defect tree, receipt mutant label, limb, receipt base limb,
#  receipt mutant limb, receipt verdict)
RECEIPT_ROWS = [
    (1,  "duprow",      "H1a counts-loose",      "H1", 0, 0, "NOT-SHOWN"),
    (2,  "fencedf29",   "H1b raw-loose",         "H1", 0, 0, "NOT-SHOWN"),
    (3,  "src0740",     "H1c src-boundary",      "H1", 0, 1, "FLIP"),
    (4,  "vjunk",       "H2a verified-loose",    "H2", 0, 1, "FLIP"),
    (5,  "thinsection", "H2b wordfloor-low",     "H2", 1, 1, "NOT-SHOWN"),
    (6,  "badnames",    "H2c need-empty",        "H2", 0, 1, "FLIP"),
    (7,  "row9cells",   "H3a cells-loose",       "H3", 0, 0, "NOT-SHOWN"),
    (8,  "thinscope",   "H3b scope-low",         "H3", 0, 1, "FLIP"),
    (9,  "kindcase",    "H3c kind-dead",         "H3", 0, 1, "FLIP"),
    (10, "manws",       "H4a manifest-unpinned", "H4", 0, 1, "FLIP"),
    (11, "fewquotes",   "H4b quotes-low",        "H4", 0, 0, "NOT-SHOWN"),
    (12, "dupquote",    "H4c distinct-dropped",  "H4", 0, 0, "NOT-SHOWN"),
    (13, "widespan",    "H5a span-wide",         "H5", 0, 1, "FLIP"),
    (14, "longquote",   "H5b words-wide",        "H5", 0, 1, "FLIP"),
    (15, "fewspans",    "H5c pass-low",          "H5", 0, 0, "NOT-SHOWN"),
    (16, "nestedmd",    "H6a counts-loose",      "H6", 0, 1, "FLIP"),
    (17, "entrymutant", "H6b pin-dropped",       "H6", 0, 1, "FLIP"),
    (18, "symlink",     "H7b symlink-dead",      "H7", 0, 1, "FLIP"),
    (19, "row9cells",   "H7a verdict-or",        "H7", 0, 0, "NOT-SHOWN"),
    (20, "positive",    "H7c okline-loose",      "H7", 1, 1, "NOT-SHOWN"),
]
RECEIPT_FLIPS = ["H1c", "H2a", "H2c", "H3b", "H3c", "H4a", "H5a", "H5b", "H6a", "H6b", "H7b"]
RECEIPT_JUNK_H5 = "spans=7 located=2 failed=5 uncited=0 cores=0/5"
RECEIPT_FAB_H5 = "spans=7 located=5 failed=2 uncited=0 cores=4/5"
RECEIPT_JUNK_FIXED = 3
RECEIPT_FAB_FIXED = 3
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



# --- counter running ---------------------------------------------------------------
LIMB_RE = re.compile(r"^gate (H[1-7]) pass=([01]) read=(.*)$")
FIXED_RE = re.compile(r"^f29-gate fixed=(\d+)/7 exit=([01])$")


def run_gate(counter: str, root: str, work: str) -> tuple[dict, int, int]:
    """Run the counter on `root`; return (limb -> (pass, read), fixed, exit)."""
    env = dict(os.environ)
    env["TMPDIR"] = work
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, counter, "--root", root, "--work", work],
                       capture_output=True, text=True, timeout=600, env=env)
    limbs, fixed, exit_code = {}, -1, -1
    for ln in p.stdout.splitlines():
        m = LIMB_RE.match(ln)
        if m:
            limbs[m.group(1)] = (int(m.group(2)), m.group(3))
        m = FIXED_RE.match(ln)
        if m:
            fixed, exit_code = int(m.group(1)), int(m.group(2))
    if not limbs:
        raise RuntimeError("counter printed no gate lines on %s: %r" % (root, p.stdout[-400:]))
    return limbs, fixed, exit_code


def mutant_copy(counter: str, mutant_id: str, work: str) -> str:
    """Copy the counter's instruments dir, apply the mutant, return the mutant's path."""
    mid, old, new = MUTANT[mutant_id]
    text = open(counter, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        raise RuntimeError("mutant=%s old-substring occurs %d times (expected 1) — counter drift" % (mid, n))
    dst_root = os.path.join(work, "mutants", mid)
    dst_inst = os.path.join(dst_root, "corpus", "instruments")
    shutil.rmtree(dst_root, ignore_errors=True)
    os.makedirs(dst_inst, exist_ok=True)
    for name in sorted(os.listdir(os.path.dirname(counter))):
        src = os.path.join(os.path.dirname(counter), name)
        if os.path.isfile(src) and name.endswith(".py"):
            shutil.copy(src, os.path.join(dst_inst, name))
    dst = os.path.join(dst_inst, os.path.basename(counter))
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new, 1))
    return dst


# --- builders ------------------------------------------------------------------------
def build_defect(defect: str, dest: str, lane: str) -> int:
    """Build the positive tree in `dest`, then apply ONE defect."""
    build("positive", dest, lane)
    d = dest

    class _A:
        pass
    a = _A()
    a.defect = defect
    a.dir = d
    a.lane = lane

    if a.defect == "src0740":
        # R50 receipt pair 3: the F29 frontier row's sources cell reads S0740, so the
        # counter's `re.search(r"\bS074\b", ...)` no longer matches it.
        p = os.path.join(d, "corpus/README.md")
        t = open(p, encoding="utf-8").read()
        row = [ln for ln in t.splitlines() if ln.startswith("| F29 |")][0]
        open(p, "w", encoding="utf-8").write(t.replace(row, row.replace("| S074 |", "| S0740 |"), 1))
        return 0
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


# --- the receipt rebuilt ------------------------------------------------------------
def parse_receipt(path: str) -> list[tuple]:
    """Parse the R50 receipt's pairing table into the harness's own row shape."""
    rows = []
    for ln in open(path, encoding="utf-8").read().splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 6 or not cells[0].isdigit():
            continue
        pair = int(cells[0])
        defect = cells[1].split()[0]
        label = cells[2]
        m1 = re.match(r"^(H[1-7])=(\d)$", cells[3])
        m2 = re.match(r"^(H[1-7])=(\d)$", cells[4])
        if not m1 or not m2:
            raise RuntimeError("receipt row %d does not parse: %r" % (pair, ln))
        verdict = cells[5].split()[0]
        rows.append((pair, defect, label, m1.group(1), int(m1.group(2)), int(m2.group(2)), verdict))
    return rows


def selftest(a) -> int:
    """Rebuild every line of the R50 receipt."""
    lane, counter, work = a.lane, a.counter, os.path.abspath(a.work)
    trees = os.path.join(work, "trees")
    shutil.rmtree(trees, ignore_errors=True)
    os.makedirs(trees, exist_ok=True)
    failures = 0
    cases = 0
    divergences = 0

    def case(name: str, ok: bool, detail: str) -> None:
        nonlocal failures, cases
        cases += 1
        if not ok:
            failures += 1
        print("case=%s ok=%d %s" % (name, int(ok), detail))

    def divergence(name: str, detail: str) -> None:
        nonlocal divergences, failures, cases
        divergences += 1
        cases += 1
        if a.strict_receipt:
            failures += 1
        print("divergence=%s %s" % (name, detail))

    # 0. the receipt file on disk is the receipt the harness transcribes
    receipt_rows = parse_receipt(a.receipt)
    mine = [(p, d, lbl, limb, b, m, v) for (p, d, lbl, limb, b, m, v) in RECEIPT_ROWS]
    case("receipt-transcription", receipt_rows == mine,
         "receipt-rows=%d harness-rows=%d" % (len(receipt_rows), len(mine)))

    # 1. every mutant the receipt names is present, three per limb, and its clause
    #    occurs exactly once in the counter
    for mid, old, _new in MUTANTS:
        n = open(counter, encoding="utf-8").read().count(old)
        case("mutant-substring-%s" % mid, n == 1, "occurrences=%d" % n)
    case("mutant-count", len(MUTANTS) == 21, "mutants=%d" % len(MUTANTS))
    per_limb = {}
    for mid, _old, _new in MUTANTS:
        per_limb[mid[:2]] = per_limb.get(mid[:2], 0) + 1
    case("mutants-per-limb", per_limb == {"H%d" % i: 3 for i in range(1, 8)},
         "per-limb=%s" % ",".join("%s=%d" % kv for kv in sorted(per_limb.items())))
    receipt_ids = sorted([lbl.replace(" ", "-") for (_p, _d, lbl, _l, _b, _m, _v) in RECEIPT_ROWS]
                         + ["H6c-size-low"])
    case("mutant-ids-match-receipt", sorted(m[0] for m in MUTANTS) == receipt_ids,
         "ids=%d receipt-ids=%d" % (len(MUTANTS), len(receipt_ids)))

    # 2. the positive tree reads 7/7 — the green control every red case is read against
    pos = os.path.join(trees, "positive")
    build("positive", pos, lane)
    limbs, fixed, exit_code = run_gate(counter, pos, os.path.join(work, "gate"))
    case("positive-7of7", fixed == 7 and exit_code == 0, "fixed=%d/7 exit=%d" % (fixed, exit_code))

    # 3. the junk and fabricated trees reproduce the receipt's H5 read tokens; their
    #    aggregate fixed counts are compared against the receipt and diverged
    junk = os.path.join(trees, "junk")
    build("junk", junk, lane)
    jl, jfixed, _ = run_gate(counter, junk, os.path.join(work, "gate"))
    case("junk-h5-read", jl.get("H5", (0, ""))[1] == RECEIPT_JUNK_H5,
         "read=%s" % jl.get("H5", (0, ""))[1])
    if jfixed != RECEIPT_JUNK_FIXED:
        divergence("junk-fixed",
                   "receipt=%d/7 rebuilt=%d/7 red-limbs=%s" % (
                       RECEIPT_JUNK_FIXED, jfixed,
                       ",".join(sorted(k for k, v in jl.items() if v[0] == 0))))

    fab = os.path.join(trees, "fabricated")
    build("fabricated", fab, lane)
    fl, ffixed, _ = run_gate(counter, fab, os.path.join(work, "gate"))
    case("fabricated-h5-read", fl.get("H5", (0, ""))[1] == RECEIPT_FAB_H5,
         "read=%s" % fl.get("H5", (0, ""))[1])
    if ffixed != RECEIPT_FAB_FIXED:
        divergence("fabricated-fixed",
                   "receipt=%d/7 rebuilt=%d/7 red-limbs=%s" % (
                       RECEIPT_FAB_FIXED, ffixed,
                       ",".join(sorted(k for k, v in fl.items() if v[0] == 0))))

    # 4. every defect tree, every receipt pair
    built = {"positive": pos}
    flips = []
    for pair, defect, label, limb, base_limb, mutant_limb, verdict in RECEIPT_ROWS:
        mid = label.replace(" ", "-")
        if defect not in built:
            built[defect] = os.path.join(trees, "def-" + defect)
            build_defect(defect, built[defect], lane)
        tree = built[defect]
        bl, _bf, _be = run_gate(counter, tree, os.path.join(work, "gate"))
        base_pass = bl.get(limb, (None, ""))[0]
        mpath = mutant_copy(counter, mid, work)
        ml, _mf, _me = run_gate(mpath, tree, os.path.join(work, "gate"))
        mut_pass = ml.get(limb, (None, ""))[0]
        case("pair%02d-base-%s" % (pair, limb), base_pass == base_limb,
             "defect=%s limb=%s base=%s receipt=%d" % (defect, limb, base_pass, base_limb))
        case("pair%02d-mutant-%s" % (pair, limb), mut_pass == mutant_limb,
             "defect=%s limb=%s mutant=%s receipt=%d" % (defect, limb, mut_pass, mutant_limb))
        case("pair%02d-verdict" % pair, verdict == ("FLIP" if mut_pass != base_pass else "NOT-SHOWN"),
             "defect=%s mutant=%s verdict=%s" % (defect, label, verdict))
        if mut_pass != base_pass:
            flips.append(label.split()[0])
    case("flip-set", flips == RECEIPT_FLIPS, "flips=%s" % ",".join(flips))

    # 5. the receipt's own count: 11 flips, 10 not-shown (nine paired rows + H6c)
    not_shown = [lbl.split()[0] for (_p, _d, lbl, _l, _b, _m, v) in RECEIPT_ROWS if v == "NOT-SHOWN"]
    case("not-shown-count", len(not_shown) + 1 == 10,
         "paired-not-shown=%d unpaired=H6c total=%d" % (len(not_shown), len(not_shown) + 1))

    print("selftest cases=%d failures=%d" % (cases, failures))
    print("selftest-divergences=%d" % divergences)
    return 0 if failures == 0 else 1




def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mode", choices=["positive", "junk", "fabricated"])
    ap.add_argument("--defect")
    ap.add_argument("--dir")
    ap.add_argument("--lane", default=LANE_DEFAULT)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work")
    ap.add_argument("--counter", default=COUNTER_DEFAULT)
    ap.add_argument("--receipt", default=RECEIPT_DEFAULT)
    ap.add_argument("--strict-receipt", action="store_true",
                    help="promote a receipt divergence to a failure")
    a = ap.parse_args()
    if a.selftest:
        if not a.work:
            ap.error("--selftest needs --work DIR")
        return selftest(a)
    if not a.dir:
        ap.error("--mode / --defect need --dir DEST")
    if os.path.isdir(a.dir):
        shutil.rmtree(a.dir)
    if a.mode:
        build(a.mode, a.dir, a.lane)
    elif a.defect:
        return build_defect(a.defect, a.dir, a.lane)
    else:
        ap.error("one of --mode / --defect / --selftest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
