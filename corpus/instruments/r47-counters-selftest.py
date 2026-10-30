#!/usr/bin/env python3
"""r47-counters-selftest.py — selftest + fixture corpus for the round-47 counters.

WHAT IT DOES
    Builds scratch fixture trees out of a PURE base export and asserts the round-47
    counters' verdicts on them:

    c1 (r47-routed-defects.py)
        green    base + the D5-D8 fixes applied by the committed builders below
                 -> `routed-defects total=11 fixed=11 unresolved=0 exit=0`
        defects  one tree per routed limb; the targeted limb must read `fixed=0`
                 and the gate must exit 1 (QUALITY R53 tree-level false-green
                 probes: every marker stays, the bound content is removed,
                 disguised or displaced).
    c2 (r47-f30-gate.py)
        green    base + the F30 row + the S075 registry row + a synthetic F30
                 entry whose every quote locates in the pinned S075 capture
                 -> `f30-gate fixed=7/7 exit=0`
        defects  one tree per limb (junk row, indented duplicate row, ghost row,
                 unlocated quote, out-of-body span, altered manifest/capture,
                 thinned sections, wrong tier, knowledge-directory corruption,
                 census corruption) -> targeted limb red, gate exit 1.

    With `--gate PATH` the given counter FILE is run instead of the committed one;
    `r47-mutbat.py` uses that to grade counter-source mutants (QUALITY R50): a
    mutant is caught exactly when this selftest reports failures > 0 under it.

    Read-only over the base export; scratch under --work (TMPDIR honoured);
    never runs git; stdlib only. The census limb shells out to the fleet's
    sources-census.sh.

USAGE
    python3 corpus/instruments/r47-counters-selftest.py --base EXPORT --work DIR \
        [--counter c1|c2|both] [--gate PATH] [--keep]
OUTPUT
    one `case <id> ok=<0|1> want=<verdict> got=<verdict>` line, then
    `selftest cases=<n> failures=<m> exit=0|1`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

SELF = os.path.realpath(__file__)
INSTRUMENTS = os.path.dirname(SELF)
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
C1 = "r47-routed-defects.py"
C2 = "r47-f30-gate.py"
MAN_SHA = "6168521b5f5555fd06f2a63c1dc0e8543cd89f8146f79f684daf586f32f35e9b"
SNAP75_SHA = "9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1"
SNAP76_SHA = "9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38"
ENTRY29 = "corpus/knowledge/github-repository-security-advisories.md"
ENTRY30 = "corpus/knowledge/zdi-disclosure-policy.md"

# ---------------------------------------------------------------- builders ----

def norm(s: str) -> str:
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def extract_fenced_bullets(text: str) -> list[str]:
    """The bullet lines trapped inside ```markdown fences, in order."""
    out = []
    for m in re.finditer(r"```markdown\n(.*?)```", text, re.S):
        for ln in m.group(1).splitlines():
            if ln.startswith("- "):
                out.append(ln.rstrip())
    return out


def remove_scaffold(text: str) -> str:
    """Delete the two scaffold blocks (instruction prose + fences), whole."""
    a = text.find(" The `## Search log` bullet to append")
    mb = re.search(r"^## Leads \(unopened\)\s*$", text, re.M)
    assert a != -1 and mb, (a, mb)
    text = text[:a] + text[mb.start():]
    c = text.find(" `## Registry changes` bullets to append")
    assert c != -1
    return text[:c].rstrip("\n") + "\n"


def land_bullets(text: str) -> str:
    """Land the fenced bullets in their real sections (D5 fix)."""
    bullets = extract_fenced_bullets(text)
    assert len(bullets) == 3, bullets
    search_bullet, reg_bullet, note_bullet = bullets
    text = remove_scaffold(text)
    # search-log bullet: last bullet of ## Search log, one blank line before ## Leads
    m = re.search(r"\n(?=## Leads \(unopened\))", text)
    assert m, "search-log tail not found"
    text = text[:m.start()] + "\n" + search_bullet + "\n" + text[m.start():]
    # registry bullets: end of ## Registry changes = end of file
    text = text.rstrip("\n") + "\n" + reg_bullet + "\n" + note_bullet + "\n"
    return text


S075_ROW = ("| S075 | Zero Day Initiative disclosure policy — https://www.zerodayinitiative.com/advisories/disclosure_policy/ "
 "| docs | A | ZDI's own statement of its broker disclosure policy: vendor-contact clocks, the 120-day deadline, "
 "the tiered patch-regression windows, extension discretion and publication at deadline "
 "| capture corpus/source-snapshots/round-47/S075.txt sha256 " + SNAP75_SHA + " (60 lines); policy prose lines 20-27 of "
 "corpus/source-snapshots/round-47/S075.txt; Q1-Q10 anchors 21, 23, 24, 24, 24, 24, 25, 25, 25, 26 "
 "| The third-party broker's acquisition-disclosure timeline: 120 days with no stated start event, extensions "
 "solely discretionary and rare, publication of a limited advisory at deadline; scope: the policy page text only, "
 "advisories and reward rules excluded "
 "| mined | 2026-10-30 | 90d | corpus/knowledge/zdi-disclosure-policy.md |")

S076_ROW = ("| S076 | GitHub repository security advisories (maintainer side) — "
 "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories "
 "| docs | A | GitHub's own statement of the maintainer-side advisory lifecycle, re-captured with the committed capture "
 "instrument (capture-source.py --kind html) so the recheck can reproduce a comparing capture (round-47 D7 provenance "
 "repair; same document as S074) "
 "| capture corpus/source-snapshots/round-47/S076.txt sha256 " + SNAP76_SHA + " (610 lines); prose lines 558-600 of "
 "corpus/source-snapshots/round-47/S076.txt; Q1-Q12 anchors 568, 571, 575, 582, 583, 583, 584, 589, 596, 598, 599, 600 "
 "| supersedes S074 — same page, re-captured with the committed instrument; the attempt-2 42-line capture was produced "
 "by no committed script or receipt, so its recheck could not produce a comparing re-capture (round-47 D7) "
 "| mined | 2026-10-30 | 90d | corpus/knowledge/github-repository-security-advisories.md |")


def add_registry_row(text: str, row: str) -> str:
    """Insert an 11-cell row after the last S-row of the ## Registry table."""
    lines = text.splitlines(keepends=True)
    last = None
    for i, ln in enumerate(lines):
        if re.match(r"^\| S\d{3} \|", ln):
            last = i
    assert last is not None
    lines.insert(last + 1, row + "\n")
    return "".join(lines)


def edit_row_cells(text: str, sid: str, **cells) -> str:
    """In-place status/used-by edits on one registry row (the CORPUS-rule-2 cells)."""
    lines = text.splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if re.match(r"^\| %s \|" % sid, ln):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            for k, v in cells.items():
                idx = {"status": 7, "used_by": 10}[k]
                c[idx] = v
            lines[i] = "| " + " | ".join(c) + " |\n"
            return "".join(lines)
    raise AssertionError("row %s not found" % sid)


def add_leads_bullet(text: str) -> str:
    bullet = ("- GitHub repository security advisories REST API (the endpoints for creating and editing repository "
              "security advisories) at https://docs.github.com/en/rest/security-advisories/repository-security-advisories; "
              "named by the S076 capture as a sibling surface and scoped out of F29; lead only, not opened this round.")
    m = re.search(r"^## Registry changes\s*$", text, re.M)
    assert m, "registry-changes heading not found"
    return text[:m.start()] + bullet + "\n\n" + text[m.start():]


LESSON46_CORRECTIONS = """
## Corrections (round 47)

- Correction (round 47, routed defect D5): the attempt-2 status sentence above ("S074 row + one Search-log bullet +
  two Registry-changes bullets") describes bytes that were added inside ```markdown fences as L1 instruction prose,
  never landed as section bullets (`corpus/lessons/round-46-verifier-spotcheck.md` §8 D5). In round 47 the three
  bullets were landed in their real sections (`## Search log`, `## Registry changes`) of `corpus/SOURCES.md`, the
  scaffold prose and fences were deleted, and SOURCES.md line numbers below :90 moved (recorded here per the R6
  exception; the F29 entry's own line count is unchanged, so entry-line anchors stay valid).
- Correction (round 47, routed defect D6): three sentences of the admitted F29 entry were false and the wave-2
  findings that named them were not carried into the integration: the dropped seat files are
  `wave2/R46bW2RevEntryClaims.md` (F1: the capture carries page chrome, "all 42 lines are body prose" is false)
  and `wave2/R46bConnPatterns.md` (M1: the page states the CVE request before the fix-version material, and the
  fix-version trio at old :40-:42 permits publish-without-fix in only two of the three cases). Round 47 corrects
  the sentences in place (same line count) and this erratum is the record of the dropped findings.
"""


def lesson46_fixed() -> str:
    return LESSON46_CORRECTIONS


LESSON47_STUB = """# Round 47 — Kasegi (selftest fixture)

## Mistakes

- M47-x (erratum class): the round-46 closure's dropped seat findings (`wave2/R46bW2RevEntryClaims.md` F1,
  `wave2/R46bConnPatterns.md` M1) are named and dispositioned here.
- Registry changes: S074 status `mined` -> `rejected` (superseded by the S076 re-capture; old -> new logged);
  S074 used-by -> `corpus/lessons/round-46.md` (the lesson cites the attempt-2 capture anchors).

## Gate

- The ZDI flip's id reservation (round-46 attempt-1 proposed S074; D8) is resolved by this round's admission:
  ZDI is admitted as F30 with S075, so the reservation is discharged rather than reassigned.
- S068 precision: the round-46 reject reason called the Advisory Database row class "screened and rejected in
  round 43 (S068)"; S068 is one GHSA advisory entry, not the database's documentation — an n=1 precedent,
  overstated there, corrected here.
"""


def entry29_fixed(entry_text: str) -> str:
    """The re-anchored + corrected F29 entry, as built from the base bytes."""
    here = os.path.dirname(SELF)
    fixed = open(os.path.join(here, "entry29-fixed-bytes.md"), encoding="utf-8").read()
    return fixed if entry_text else fixed


# ------------------------------------------------------------------ fixtures --

def build_c1_green(base: str, work: str) -> str:
    t = shutil.copytree(base, os.path.join(work, "c1-green"), symlinks=True)
    p = os.path.join(t, "corpus/SOURCES.md")
    txt = open(p, encoding="utf-8").read()
    txt = add_leads_bullet(land_bullets(txt))
    txt = add_registry_row(txt, S076_ROW)
    txt = edit_row_cells(txt, "S074", status="rejected", used_by="corpus/lessons/round-46.md")
    open(p, "w", encoding="utf-8").write(txt)
    open(os.path.join(t, ENTRY29), "w", encoding="utf-8").write(entry29_fixed(""))
    open(os.path.join(t, "corpus/lessons/round-46.md"), "a", encoding="utf-8").write(LESSON46_CORRECTIONS)
    open(os.path.join(t, "corpus/lessons/round-47.md"), "w", encoding="utf-8").write(LESSON47_STUB)
    snap_src = os.path.join(LANE, "corpus/source-snapshots/round-47")
    snap_dst = os.path.join(t, "corpus/source-snapshots/round-47")
    os.makedirs(snap_dst, exist_ok=True)
    for f in ("manifest.json", "S075.txt", "S076.txt"):
        shutil.copy2(os.path.join(snap_src, f), os.path.join(snap_dst, f))
    return t


def c1_defects(base: str, work: str, green: str) -> dict[str, str]:
    d = {}
    src = open(os.path.join(green, "corpus/SOURCES.md"), encoding="utf-8").read()

    def mk(name, mut):
        t = shutil.copytree(green, os.path.join(work, "c1-" + name), symlinks=True)
        mut(t)
        d[name] = t

    def w(rel, fn):
        def apply(t):
            p = os.path.join(t, rel)
            s = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(fn(s))
        return apply

    mk("s1left", w("corpus/SOURCES.md", lambda s: s.replace("## Leads (unopened)", "Append inside `## Search log` as before\n\n## Leads (unopened)")))
    mk("fenceleft", w("corpus/SOURCES.md", lambda s: s + "\n```markdown\n- stray fenced bullet\n```\n"))
    mk("regbullet-missing", w("corpus/SOURCES.md", lambda s: re.sub(r"^- S074 row added: new row.*\n", "", s, flags=re.M)))
    mk("nocorrection", w("corpus/lessons/round-46.md", lambda s: s.replace(LESSON46_CORRECTIONS, "")))
    def thincorr(t):
        pth = os.path.join(t, "corpus/lessons/round-46.md")
        s = open(pth, encoding="utf-8").read()
        s = s.replace("scaffold prose and fences were deleted, and SOURCES.md line numbers below :90 moved", "scaffold prose was cleaned")
        s = s.replace("`corpus/SOURCES.md`", "`<file>`")
        open(pth, "w", encoding="utf-8").write(s)
    mk("thin-correction", thincorr)
    mk("falsephrase1", w(ENTRY29, lambda s: s.replace("The prose is S076.txt:558-600; the capture also carries page chrome (S076.txt:556, S076.txt:559, S076.txt:562-566, S076.txt:601-610); it", "S076.txt:558-600 is the whole capture and all 42 lines are body prose; it")))
    mk("orderfalse", w(ENTRY29, lambda s: s.replace("the page states the CVE request before the fix-version material", "in the order the page states it")))
    mk("threecases", w(ENTRY29, lambda s: s.replace("only two \u2014", "the three cases at S076.txt:598, S076.txt:599 and S076.txt:600 \u2014 all three cases let a maintainer publish")))
    mk("noforbid", w(ENTRY29, lambda s: s.replace("wait to disclose the issue when the fix is ready", "wait to disclose the issue when ready")))
    def nonames(t):
        for rel in ("corpus/lessons/round-46.md", "corpus/lessons/round-47.md"):
            pth = os.path.join(t, rel)
            s = open(pth, encoding="utf-8").read()
            open(pth, "w", encoding="utf-8").write(s.replace("R46bW2RevEntryClaims", "REDACTED-A").replace("R46bConnPatterns", "REDACTED-B"))
    mk("nonames", nonames)
    mk("norow76", w("corpus/SOURCES.md", lambda s: re.sub(r"^\| S076 \|.*\n", "", s, flags=re.M)))
    mk("badsha76", w("corpus/SOURCES.md", lambda s: s.replace(SNAP76_SHA, "0" * 64)))
    mk("maninert", mut_manifest_inert)
    mk("oldcite", w(ENTRY29, lambda s: s.replace("`S076.txt:575`", "`S074.txt:17`", 1)))
    mk("badspan", w(ENTRY29, lambda s: s.replace("`S076.txt:568`", "`S076.txt:1`", 1)))
    mk("nocite", w(ENTRY29, lambda s: s.replace("(`S076.txt:589`)", "", 1)))
    mk("nolead", w("corpus/SOURCES.md", lambda s: re.sub(r"^- GitHub repository security advisories REST API.*\n", "", s, flags=re.M)))
    mk("nolesson47", lambda t: os.remove(os.path.join(t, "corpus/lessons/round-47.md")))
    mk("noprecision", w("corpus/lessons/round-47.md", lambda s: s.replace("one GHSA advisory entry", "a row class")))
    return d


def mut_manifest_inert(t: str) -> None:
    p = os.path.join(t, "corpus/source-snapshots/round-47/manifest.json")
    m = json.load(open(p, encoding="utf-8"))
    m["note"] = m.get("note", "") + " altered-by-selftest"
    open(p, "w", encoding="utf-8").write(json.dumps(m, indent=1) + "\n")


C2_ENTRY_TEMPLATE = """# Zero Day Initiative disclosure policy — the broker's acquisition-disclosure timeline (synthetic selftest fixture)

source: S075 — https://www.zerodayinitiative.com/advisories/disclosure_policy/ — Disclosure Policy; policy prose lines 20-27 of corpus/source-snapshots/round-47/S075.txt (sha256 {snap})
verified-at: 2026-10-30
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075 # 90d

## Scope and decision rule

A researcher reading a broker deadline reads ZDI's own policy: the vendor is allowed “four months (120 days) to address the vulnerability with a security patch or other corrective measure” (`S075.txt:24`), and if the vendor misses it ZDI “will publish a limited advisory including mitigation in an effort to enable the defensive community to protect the user.” (`S075.txt:24`). The decision rule: record the deadline as broker-controlled and start-unstated, never as a vendor disclosure clock.

| limb | what the page states | locator |
|---|---|---|
| deadline | four months to address | “TrendAI™ ZDI will allow the vendor four months (120 days) to address the vulnerability” (`S075.txt:24`) |
| start event | none stated for the 120 days | “fifteen business days after the initial contact” (`S075.txt:23`) starts only the public-advisory fallback |
| extensions | sole discretion, rare | “sole discretion of TrendAI™ ZDI and will be granted only in rare circumstances” (`S075.txt:24`) |
| patch-regression tiers | 30/60/90 days | “For critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days” (`S075.txt:25`) |
| publication | limited advisory at deadline | “will publish a limited advisory including mitigation” (`S075.txt:24`) |
| never kept quiet | acquired bugs publish | “In no cases will an acquired vulnerability be” (`S075.txt:26`) |

## Overlap and novelty

F02 (`corpus/knowledge/coordinated-disclosure-timelines.md:7`) compares coordinator timelines with attribution; this entry adds the broker case. F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md:9`) holds vendor intake programmes; ZDI acquires rather than accepts, which is the new ground here.

## Limits

The capture carries the policy page text only (`S075.txt:20-27`); advisories, reward rules and the researcher submission page are outside this row. Nothing here checks the live page; the `recheck:` line re-verifies the pinned bytes and the ten manifest quotes (Q1-Q10, anchors S075.txt:21, 23, 24, 24, 24, 24, 25, 25, 25 and 26); nothing here checks GitHub's or ZDI's current page, and no reward figure is copied from the advisories index.

## Falsifiable package rule

A claim package may cite a ZDI deadline only with the broker attribution and the unstated start event (`S075.txt:24`); citing it as a vendor deadline or a started clock is rejected.
"""


def build_c2_green(base: str, work: str) -> str:
    t = shutil.copytree(base, os.path.join(work, "c2-green"), symlinks=True)
    entry = C2_ENTRY_TEMPLATE.format(snap=SNAP75_SHA)
    open(os.path.join(t, ENTRY30), "w", encoding="utf-8").write(entry)
    p = os.path.join(t, "corpus/SOURCES.md")
    txt = open(p, encoding="utf-8").read()
    txt = add_registry_row(txt, S075_ROW)
    open(p, "w", encoding="utf-8").write(txt)
    p = os.path.join(t, "corpus/README.md")
    row = ("| F30 | Zero Day Initiative disclosure policy — the third-party broker's acquisition-disclosure timeline "
           "| admitted | corpus/knowledge/zdi-disclosure-policy.md | S075 | Read a broker deadline as broker-controlled and start-unstated; "
           "the F02 comparison and the F15 intake rows keep their own attributions. |")
    txt = open(p, encoding="utf-8").read()
    lines = txt.splitlines(keepends=True)
    last = max(i for i, ln in enumerate(lines) if re.match(r"^\| F\d+ \|", ln))
    lines.insert(last + 1, row + "\n")
    open(p, "w", encoding="utf-8").write("".join(lines))
    snap_src = os.path.join(LANE, "corpus/source-snapshots/round-47")
    snap_dst = os.path.join(t, "corpus/source-snapshots/round-47")
    os.makedirs(snap_dst, exist_ok=True)
    for f in ("manifest.json", "S075.txt", "S076.txt"):
        shutil.copy2(os.path.join(snap_src, f), os.path.join(snap_dst, f))
    return t


def c2_defects(base: str, work: str, green: str) -> dict[str, str]:
    d = {}

    def mk(name, mut):
        t = shutil.copytree(green, os.path.join(work, "c2-" + name), symlinks=True)
        mut(t)
        d[name] = t

    def w(rel, fn):
        def apply(t):
            p = os.path.join(t, rel)
            s = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(fn(s))
        return apply

    def duprow(t):
        p = os.path.join(t, "corpus/README.md")
        s = open(p, encoding="utf-8").read()
        row = [ln for ln in s.splitlines() if ln.startswith("| F30 |")][0]
        open(p, "w", encoding="utf-8").write(s + "\n   " + row + "\n")

    def ghostrow(t):
        p = os.path.join(t, "corpus/README.md")
        s = open(p, encoding="utf-8").read()
        row = [ln for ln in s.splitlines() if ln.startswith("| F30 |")][0]
        open(p, "w", encoding="utf-8").write(s + "\n\u200b" + row + "\n")

    def thinsect(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("The capture carries the policy page text only (`S075.txt:20-27`); advisories, reward rules and the researcher submission page are outside this row. Nothing here checks the live page; the `recheck:` line re-verifies the pinned bytes and the ten manifest quotes (Q1-Q10, anchors S075.txt:21, 23, 24, 24, 24, 24, 25, 25, 25 and 26); nothing here checks GitHub's or ZDI's current page, and no reward figure is copied from the advisories index.", "X")
        open(p, "w", encoding="utf-8").write(s)

    def unlocated(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("(`S075.txt:24`). The decision rule", "(`S075.txt:25`). The decision rule")
        open(p, "w", encoding="utf-8").write(s)

    def widespan(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("(`S075.txt:23`)", "(`S075.txt:23-35`)")
        open(p, "w", encoding="utf-8").write(s)

    def longquote(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("\u201cIn no cases will an acquired vulnerability be\u201d", "\u201cIn no cases will an acquired vulnerability be kept quiet because a product vendor does not wish to address it and we plan on publishing a summary of the communication\u201d")
        open(p, "w", encoding="utf-8").write(s)

    def fewspans(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("(`S075.txt:26`)", "")
        open(p, "w", encoding="utf-8").write(s)

    def junkquote(t):
        p = os.path.join(t, ENTRY30)
        s = open(p, encoding="utf-8").read()
        s = s.replace("\u201cwill publish a limited advisory including mitigation\u201d", "\u201cwill publish a full advisory including exploit code\u201d")
        open(p, "w", encoding="utf-8").write(s)

    mk("duprow", duprow)
    mk("rowstatus", w("corpus/README.md", lambda s: s.replace("| admitted | corpus/knowledge/zdi-disclosure-policy.md | S075 |", "| queued | knowledge/zdi-disclosure-policy.md | S075 |")))
    mk("ghostrow", ghostrow)
    mk("norecheck", w(ENTRY30, lambda s: re.sub(r"^recheck: .*\n", "", s, flags=re.M)))
    mk("thinsect", thinsect)
    mk("badxref", w(ENTRY30, lambda s: s.replace("coordinated-disclosure-timelines.md:7", "coordinated-disclosure-timelines.md:9999")))
    mk("tierc", w("corpus/SOURCES.md", lambda s: re.sub(r"(\| S075 \|[^|]*\| docs \|) A (\|)", r"\1 C \2", s)))
    mk("thinscope", w("corpus/SOURCES.md", lambda s: s.replace("ZDI's own statement of its broker disclosure policy: vendor-contact clocks, the 120-day deadline, the tiered patch-regression windows, extension discretion and publication at deadline", "ZDI policy clocks")))
    mk("badloc", w("corpus/SOURCES.md", lambda s: s.replace("policy prose lines 20-27 of corpus/source-snapshots/round-47/S075.txt", "policy prose lines 1-3 of corpus/source-snapshots/round-47/S075.txt")))
    mk("manws", mut_manifest_inert)
    mk("fewquotes", mut_manifest_fewquotes)
    mk("capflip", mut_capture_flip)
    mk("toolmut", mut_tool_flip)
    mk("unlocated", unlocated)
    mk("widespan", widespan)
    mk("longquote", longquote)
    mk("fewspans", fewspans)
    mk("junkquote", junkquote)
    mk("nestedmd", lambda t: (os.makedirs(os.path.join(t, "corpus/knowledge/nest"), exist_ok=True), open(os.path.join(t, "corpus/knowledge/nest/x.md"), "w").write("x")))
    mk("entryrename", lambda t: os.rename(os.path.join(t, ENTRY30), os.path.join(t, "corpus/knowledge/zdi-renamed.md")))
    mk("symlink", lambda t: (os.remove(os.path.join(t, "corpus/SOURCES.md")), os.symlink("etc/hostname", os.path.join(t, "corpus/SOURCES.md"))))
    mk("regdup", w("corpus/SOURCES.md", lambda s: s.replace("## Registry\n", "## Registry\n## Registry\n", 1)))
    return d


def mut_manifest_fewquotes(t: str) -> None:
    p = os.path.join(t, "corpus/source-snapshots/round-47/manifest.json")
    m = json.load(open(p, encoding="utf-8"))
    for s in m["sources"]:
        if s["id"] == "S075":
            s["quotes"] = s["quotes"][:3]
    open(p, "w", encoding="utf-8").write(json.dumps(m, indent=1) + "\n")


def mut_capture_flip(t: str) -> None:
    p = os.path.join(t, "corpus/source-snapshots/round-47/S075.txt")
    s = open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(s.replace("four months (120 days)", "four months (121 days)", 1))


def mut_tool_flip(t: str) -> None:
    # corrupt the graded tree's copy of source-recheck? the gate pins its OWN instrument dir;
    # this defect instead swaps the manifest's sha for S075 so recheck fails.
    p = os.path.join(t, "corpus/source-snapshots/round-47/manifest.json")
    m = json.load(open(p, encoding="utf-8"))
    for s in m["sources"]:
        if s["id"] == "S075":
            s["sha256"] = "0" * 64
    open(p, "w", encoding="utf-8").write(json.dumps(m, indent=1) + "\n")


# ------------------------------------------------------------------ runner ----

def run_counter(counter: str, gate: str | None, tree: str, work: str) -> tuple[int, str]:
    script = gate or os.path.join(INSTRUMENTS, {"c1": C1, "c2": C2}[counter])
    out = os.path.join(work, "out.txt")
    with open(out, "w") as fh:
        p = subprocess.run([sys.executable, "-I", script, "--root", tree, "--work", work],
                           stdout=fh, stderr=subprocess.STDOUT, timeout=600, cwd=work)
    text = open(out, encoding="utf-8", errors="replace").read()
    return p.returncode, text


def summary_line(text: str, counter: str) -> str:
    pat = (r"routed-defects total=\d+ fixed=\d+ unresolved=\d+ exit=\d+" if counter == "c1"
           else r"f30-gate fixed=\d/7 exit=\d")
    m = re.search(pat, text)
    return m.group(0) if m else "no-summary-line"


def limb_red(text: str, limb: str, counter: str) -> bool:
    if counter == "c1":
        return not re.search(r"^limb %s \([A-D]\d+\) fixed=1" % re.escape(limb), text, re.M)
    return not re.search(r"^gate %s pass=1" % re.escape(limb), text, re.M)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter", default="both", choices=["c1", "c2", "both"])
    ap.add_argument("--gate", default=None, help="run this counter file instead of the committed one")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    cases: list[tuple[str, bool, str, str]] = []
    which = ["c1", "c2"] if a.counter == "both" else [a.counter]
    for counter in which:
        if counter == "c1":
            green = build_c1_green(a.base, a.work)
            rc, text = run_counter(counter, a.gate, green, a.work)
            want = "routed-defects total=11 fixed=11 unresolved=0 exit=0"
            cases.append(("c1-green", summary_line(text, "c1") == want, want, summary_line(text, "c1")))
            defects = c1_defects(a.base, a.work, green)
            for name, tree in sorted(defects.items()):
                rc, text = run_counter(counter, a.gate, tree, a.work)
                limb = {"s1left": "L1", "fenceleft": "L2", "regbullet-missing": "L2", "nocorrection": "L3",
                        "thin-correction": "L3", "falsephrase1": "L4", "orderfalse": "L5", "threecases": "L6",
                        "noforbid": "L6", "nonames": "L7", "norow76": "L8", "badsha76": "L8", "maninert": "L8",
                        "oldcite": "L9", "badspan": "L9", "nocite": "L9", "nolead": "L10", "nolesson47": "L11",
                        "noprecision": "L11"}[name]
                ok = rc != 0 and limb_red(text, limb, "c1")
                cases.append(("c1-" + name, ok, "%s red + exit!=0" % limb, summary_line(text, "c1")))
        else:
            green = build_c2_green(a.base, a.work)
            rc, text = run_counter(counter, a.gate, green, a.work)
            want = "f30-gate fixed=7/7 exit=0"
            cases.append(("c2-green", summary_line(text, "c2") == want, want, summary_line(text, "c2")))
            defects = c2_defects(a.base, a.work, green)
            limb_of = {"duprow": "H1", "rowstatus": "H1", "ghostrow": "H1", "norecheck": "H2", "thinsect": "H2",
                       "badxref": "H2", "tierc": "H3", "thinscope": "H3", "badloc": "H3", "manws": "H4",
                       "fewquotes": "H4", "capflip": "H4", "toolmut": "H4", "unlocated": "H5", "widespan": "H5",
                       "longquote": "H5", "fewspans": "H5", "junkquote": "H5", "nestedmd": "H6",
                       "entryrename": "H6", "symlink": "H7", "regdup": "H7"}
            for name, tree in sorted(defects.items()):
                rc, text = run_counter(counter, a.gate, tree, a.work)
                limb = limb_of[name]
                ok = rc != 0 and limb_red(text, limb, "c2")
                cases.append(("c2-" + name, ok, "%s red + exit!=0" % limb, summary_line(text, "c2")))
        if not a.keep:
            for name in os.listdir(a.work):
                pth = os.path.join(a.work, name)
                if name not in ("out.txt",) and os.path.isdir(pth):
                    shutil.rmtree(pth, ignore_errors=True)
    fails = 0
    for name, ok, want, got in cases:
        if not ok:
            fails += 1
        print("case %s ok=%d want=%s got=%s" % (name, int(ok), want, got))
    print("selftest cases=%d failures=%d exit=%d" % (len(cases), fails, 0 if fails == 0 else 1))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
