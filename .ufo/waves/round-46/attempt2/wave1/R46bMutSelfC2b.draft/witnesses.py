#!/usr/bin/env python3
"""Witness trees for the R46bMutSelfC2b survivors.

Each witness mutates a COMPLETE C2 tree (built by the committed selftest's own
builder) so that the pristine counter and the mutated counter disagree on a gate.
That is what turns "survivor" from "the selftest has no case here" into "the
mutant changes a verdict on a concrete, buildable input".

`env` is an optional dict of extra environment for BOTH counter runs (used for
the grader-side R46_PINS_OVERRIDE re-pin, exactly as the committed selftest does).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil

_spec = importlib.util.spec_from_file_location(
    "st_c2", "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py")
st = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(st)

README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
ENTRY_REL = "corpus/knowledge/github-private-vulnerability-reporting.md"
MAN_REL = "corpus/source-snapshots/round-46/manifest.json"


def rd(root, rel):
    return open(os.path.join(root, rel), encoding="utf-8").read()


def wr(root, rel, data):
    open(os.path.join(root, rel), "w", encoding="utf-8").write(data)


def sub(root, rel, old, new, count=1):
    t = rd(root, rel)
    assert old in t, (rel, old)
    wr(root, rel, t.replace(old, new, count))


def line_of(root, rel, prefix):
    ln = [x for x in rd(root, rel).split("\n") if x.startswith(prefix)]
    assert len(ln) == 1, (rel, prefix, len(ln))
    return ln[0]


def refit(root, n=3600):
    """Re-pad the entry to n bytes (the selftest's own fit())."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "st_c2", "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py")
    st = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(st)
    t = rd(root, ENTRY_REL)
    wr(root, ENTRY_REL, st.fit(t, n))


def set_section(root, heading, body):
    t = rd(root, ENTRY_REL)
    n = re.subn("^(" + re.escape(heading) + r"[ \t]*\n)(.*?)(?=^## |\Z)",
                lambda m: m.group(1) + ("\n" + body + "\n\n" if body else "\n"), t, count=1,
                flags=re.M | re.S)
    assert n[1] == 1
    wr(root, ENTRY_REL, n[0])


def repin_manifest(root):
    """Grader-side override: pin the manifest to its EDITED bytes (as the committed
    selftest's repin cases do) and return the override file path."""
    d = os.path.join(root, ".pins-repin")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "pins.json")
    with open(p, "w") as fh:
        json.dump({"manifest.json": hashlib.sha256(open(os.path.join(root, MAN_REL), "rb").read()).hexdigest()}, fh)
    return {"R46_PINS_OVERRIDE": p}


# --------------------------------------------------------------------------- #
# witnesses
# --------------------------------------------------------------------------- #

def w_x01(root, spans, snap):
    """F28's sources cell names S071 (a real other source) instead of S073.
    Pristine G1 demands S073 in that cell; the wildcard mutant accepts any S07x."""
    ln = line_of(root, README, "| F28 |")
    assert "| S073 |" in ln
    wr(root, README, rd(root, README).replace(ln, ln.replace("| S073 |", "| S071 |", 1)))


def w_x03(root, spans, snap):
    """F27's status cell becomes 'admitted (pending)': still 'admitted*' but not the
    exact token the pristine counter counts."""
    ln = line_of(root, README, "| F27 |")
    assert "| admitted |" in ln
    wr(root, README, rd(root, README).replace(ln, ln.replace("| admitted |", "| admitted (pending) |", 1)))


def w_x04(root, spans, snap):
    """The Falsifiable package rule section drops to 7 words: below the pristine
    floor of 12, above the mutant's floor of 6."""
    set_section(root, "## Falsifiable package rule", "Check each step against `S073.txt:564`.")
    refit(root)


def w_x06(root, spans, snap):
    """The provenance trio moves to lines 8-10: outside the pristine 8-line head
    window (verified-at is missed), inside the mutant's 10-line window."""
    t = rd(root, ENTRY_REL)
    ls = t.split("\n")
    trio = ls[2:5]
    assert trio[0].startswith("source: S073 ") and trio[2].startswith("recheck: ")
    fillers = ["filler line %d" % i for i in range(5)]
    out = ls[:2] + fillers + trio + ls[5:]
    wr(root, ENTRY_REL, "\n".join(out))
    refit(root)


def w_x07(root, spans, snap):
    """The Limits section keeps its backticked sweep command but loses every
    'S073.txt:N' cite: the pristine anchor accepts the sweep command, the mutant
    does not."""
    sub(root, ENTRY_REL, "The page body is `S073.txt:556-579`; ", "")
    refit(root)


def w_x10(root, spans, snap):
    """A second 'recheck:' line appears in the entry: the pristine counter demands
    exactly one, the mutant accepts one or more."""
    t = rd(root, ENTRY_REL)
    wr(root, ENTRY_REL, t.rstrip("\n") + "\n\nrecheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S071\n")
    refit(root)


def w_x13(root, spans, snap):
    """The registry anchor locator points past the capture's last line (L567-L590)."""
    sub(root, SOURCES, "L567-L579", "L567-L590")


def w_x14(root, spans, snap):
    """The S073 registry row carries a twelfth cell: the pristine counter demands
    exactly eleven, the mutant accepts eleven or more."""
    ln = line_of(root, SOURCES, "| S073 |")
    assert ln.rstrip().endswith("|")
    wr(root, SOURCES, rd(root, SOURCES).replace(ln, ln.rstrip()[:-1] + "| extra-cell |", 1))


def w_x26b(root, spans, snap):
    """One frozen core is missing from the manifest while every quote still
    rechecks OK: the pristine counter demands zero missing cores, the mutant
    tolerates one."""
    repl = ("Some public repositories configure security advisories so that anyone can "
            "report security vulnerabilities directly and privately to the maintainers.")
    core = "Optionally, select I used AI assistance to find or write up this report."
    def f(s):
        for q in s["quotes"]:
            if q["quote"] == core:
                q["quote"] = repl
                q["anchor"] = 557
    _manifest_edit(root, f)


def w_x30(root, spans, snap):
    """The entry carries an uncited single-curly quotation of four or more words:
    the pristine counter counts it as an uncited quote, the mutant does not."""
    sub(root, ENTRY_REL, "## Limits",
        "## Limits\n\n- The reporter may ‘submit a report to the maintainer’ at any hour.")


def w_x33(root, spans, snap):
    """A complete but compact entry: the same four sections, the same six located
    table rows and the same cross-references, in under 3000 bytes. The pristine
    counter's 3000-byte floor rejects it, the mutant's 2000-byte floor accepts it."""
    url = "https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately"
    lane = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
    q = {k: (t, *snap.locate(t)) for k, t in st.Q.items()}
    def row(key, question, consequence):
        t, a, b = q[key]
        cite = "`S073.txt:%d`" % a if a == b else "`S073.txt:%d-%d`" % (a, b)
        return "| %s | “%s” (%s) | %s |" % (question, t, cite, consequence)
    out = [
        "# GitHub private vulnerability reporting, reporter flow",
        "",
        "source: S073 — " + url + " — Privately reporting a security vulnerability (S073.txt:560-579)",
        "verified-at: 2026-10-28",
        "recheck: cd " + lane + " && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d",
        "",
        "## Scope and decision rule",
        "",
        "This entry records only what the platform's own reporter-side page says about filing a private security report to a public repository's maintainers, and the page text quoted below is located in the checked-in capture at `S073.txt:564`.",
        "",
        "| observed question | page text | package consequence |",
        "|---|---|---|",
        row("enabled", "Is the channel always available?", "Check the feature is enabled first."),
        row("form", "What does the form require by default?", "Carry these four items by default."),
        row("ai", "Is AI assistance declared?", "Record the option as optional."),
        row("credit", "Who is credited and added?", "Record collaborator and credit."),
        row("merge", "Who merges a private-fork fix?", "The reporter cannot merge it."),
        row("anyone", "Who may submit a private report?", "Any reader may report where enabled."),
        "",
        "## Overlap and novelty",
        "",
        "This is a web form on a hosting platform, not an e-mail intake route, so a package must not mix the two channels. See `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:11-12` for the kernel intake and `corpus/knowledge/ai-assisted-finding-validation.md:7-8` for the AI findings rule.",
        "",
        "## Limits",
        "",
        "One platform's page, not a standard, and documentation only: no contact with anyone and no probing of any system took place. The page body is `S073.txt:556-579`, and no CVE handling is stated or inferred anywhere in this entry.",
        "",
        "## Falsifiable package rule",
        "",
        "Check each stated step against the table above in order, starting from the enablement fact at `S073.txt:564`.",
        "",
    ]
    wr(root, ENTRY_REL, "\n".join(out))


def w_x35(root, spans, snap):
    """One base knowledge file is replaced by a symlink to a byte-identical copy
    outside the directory: the pristine counter's symlink guard rejects it, the
    mutant's does not."""
    d = os.path.join(root, "corpus", "knowledge")
    cand = sorted(f for f in os.listdir(d)
                   if f.endswith(".md") and f not in ("claim-gates.md", "claim-package-contract.md",
                                                      "github-private-vulnerability-reporting.md"))
    target = cand[0]
    notes = os.path.join(root, "corpus", "notes")
    os.makedirs(notes, exist_ok=True)
    copy = os.path.join(notes, target)
    shutil.copyfile(os.path.join(d, target), copy)
    os.remove(os.path.join(d, target))
    os.symlink(os.path.relpath(copy, d), os.path.join(d, target))


def w_x36(root, spans, snap):
    """A C1-exempt entry shrinks below its frozen base size: the pristine counter
    rejects a gutted exempt entry, the mutant tolerates half of it."""
    p = os.path.join(root, "corpus", "knowledge", "claim-gates.md")
    b = open(p, "rb").read()
    open(p, "wb").write(b[:4000])


def w_x38(root, spans, snap):
    """corpus/SOURCES.md is a symlink to a byte-identical file in the same
    directory: the pristine counter refuses a symlinked registry, the mutant
    only refuses a symlinked corpus directory."""
    real = os.path.join(root, "corpus", "SOURCES-real.md")
    shutil.copyfile(os.path.join(root, SOURCES), real)
    os.remove(os.path.join(root, SOURCES))
    os.symlink("SOURCES-real.md", os.path.join(root, SOURCES))


# --- equivalence probes: a tree on which the mutant MUST NOT differ ----------- #

def w_x08(root, spans, snap):
    """One section heading is renamed: the pristine counter's sections==4 check
    fails, and so does its full==4 check (a renamed heading has no words)."""
    sub(root, ENTRY_REL, "## Limits", "## Limits (renamed)")


def w_x25(root, spans, snap):
    """The manifest's expected sha256 is zeroed: source-recheck reports MISMATCH
    and exits non-zero, so the pristine counter already fails G4 on rc."""
    import json as _j
    m = _j.loads(rd(root, MAN_REL))
    for src in m["sources"]:
        if src["id"] == "S073":
            src["sha256"] = "0" * 64
    wr(root, MAN_REL, _j.dumps(m, indent=2, ensure_ascii=False))


def w_x34(root, spans, snap):
    """A nested .md appears under corpus/knowledge/: the directory listing count
    rises with it, so the pristine counter's 65-entry check fails too."""
    os.makedirs(os.path.join(root, "corpus", "knowledge", "sub"), exist_ok=True)
    wr(root, "corpus/knowledge/sub/extra.md", "# x\n")


def w_x40(root, spans, snap):
    """A census error row: the census exits 1 and prints no ok line, so the
    pristine counter's rc==0 check already fails."""
    ln = line_of(root, SOURCES, "| S073 |")
    wr(root, SOURCES, rd(root, SOURCES).replace(ln, ln.replace("| docs | A |", "| blog | A |", 1), 1))


def w_x41(root, spans, snap):
    """The census file is missing entirely: the census exits 2, so the pristine
    counter's rc==0 check already fails."""
    os.remove(os.path.join(root, SOURCES))



def w_x20(root, spans, snap):
    """The registry anchor cell carries only the first 16 hex chars of the capture
    sha256: the pristine counter wants the whole digest, the mutant a prefix."""
    ln = line_of(root, SOURCES, "| S073 |")
    sha = re.search(r"sha256 ([0-9a-f]{64})", ln).group(1)
    wr(root, SOURCES, rd(root, SOURCES).replace(ln, ln.replace(sha, sha[:16], 1), 1))


def _manifest_edit(root, fn):
    m = json.loads(rd(root, MAN_REL))
    rec = [x for x in m["sources"] if x["id"] == "S073"][0]
    fn(rec)
    wr(root, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))


def w_x22(root, spans, snap):
    """The manifest loses one non-core quote: seven quotes still recheck OK, so the
    pristine '>= 8' floor fails and the mutant's '>= 6' passes."""
    _manifest_edit(root, lambda s: s.__setitem__("quotes", [q for q in s["quotes"] if q["id"] != "Q1"]))


def w_x24(root, spans, snap):
    """A core quote's text is truncated to its first 40 characters: the pristine
    counter wants the whole core sentence, the mutant a 40-char prefix."""
    core = "Optionally, select I used AI assistance to find or write up this report."
    def f(s):
        for q in s["quotes"]:
            if q["quote"] == core:
                q["quote"] = core[:40]
    _manifest_edit(root, f)


def w_x26(root, spans, snap):
    """One frozen core is missing from the manifest (truncated to a non-core text):
    the pristine counter demands zero missing cores, the mutant tolerates one."""
    core = "Optionally, select I used AI assistance to find or write up this report."
    def f(s):
        for q in s["quotes"]:
            if q["quote"] == core:
                q["quote"] = "A different sentence about the same form field."
    _manifest_edit(root, f)

# --- blank line pad ---
REPIN = {"X22-G4-quote-count-6", "X24-G4-core-prefix-match", "X26-G4-core-count-lenient"}

WITNESSES = {
    "X01-G1-src-id-wildcard": dict(description="F28 sources cell names S071 instead of S073", mutate=w_x01),
    "X03-G1-admitted-prefix": dict(description="F27 status cell is 'admitted (pending)'", mutate=w_x03),
    "X04-G2-package-floor-6": dict(description="package-rule section cut to 7 words", mutate=w_x04),
    "X06-G2-head-10-lines": dict(description="provenance trio moved to lines 8-10", mutate=w_x06),
    "X07-G2-limits-anchor-grep-only": dict(description="Limits section keeps only the sweep command", mutate=w_x07),
    "X08-G2-sections-count-len3": dict(description="equivalence probe: renamed section heading", mutate=w_x08),
    "X10-G2-recheck-count-ge1": dict(description="a second recheck: line in the entry", mutate=w_x10),
    "X13-G3-locator-upper-bound-wide": dict(description="registry locator points past the capture", mutate=w_x13),
    "X14-G3-cells-ge11": dict(description="S073 registry row carries a twelfth cell", mutate=w_x14),
    "X20-G3-anchor-sha-prefix": dict(description="registry anchor cell carries a 16-char sha prefix", mutate=w_x20),
    "X22-G4-quote-count-6": dict(description="manifest loses one quote (7 remain)", mutate=w_x22),
    "X24-G4-core-prefix-match": dict(description="a core quote is truncated to 40 chars", mutate=w_x24),
    "X25-G4-sha-ok-line-dropped": dict(description="equivalence probe: zeroed manifest sha", mutate=w_x25),
    "X26-G4-core-count-lenient": dict(description="a frozen core missing while every quote still rechecks OK", mutate=w_x26b),
    "X30-G5-single-curly-unquoted": dict(description="uncited single-curly quotation of six words", mutate=w_x30),
    "X33-G6-entry-size-2000": dict(description="compact sub-3000-byte entry that keeps G2 and G5 green", mutate=w_x33),
    "X34-G6-nested-le-65": dict(description="equivalence probe: nested .md under knowledge", mutate=w_x34),
    "X35-G6-file-symlink-check-dropped": dict(description="knowledge entry replaced by symlink to identical copy", mutate=w_x35),
    "X36-G6-exempt-size-half": dict(description="C1-exempt entry shrunk to 4000 bytes", mutate=w_x36),
    "X38-G7-sources-symlink-half": dict(description="SOURCES.md replaced by symlink to same-directory copy", mutate=w_x38),
    "X40-G7-okline-anywhere": dict(description="equivalence probe: census error row", mutate=w_x40),
    "X41-G7-rc-only": dict(description="equivalence probe: missing SOURCES.md", mutate=w_x41),
}
