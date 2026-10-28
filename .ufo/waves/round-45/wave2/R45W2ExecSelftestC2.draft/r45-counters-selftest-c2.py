#!/usr/bin/env python3
"""r45-counters-selftest-c2.py — selftest for corpus/instruments/r45-c2-gate.py v1.1 (round 45, C2).

Builds, per case, a COMPLETE synthetic C2 tree in scratch:
  corpus/README.md            frontier F01..F27, all `admitted`, F27 -> corpus/knowledge/<entry>
  corpus/SOURCES.md           census-valid registry, S071 row tier A / mined / snapshot sha in anchor
  corpus/knowledge/*.md       64 files: the F27 entry + 63 stubs (two stubs carry the names the entry cross-references)
  corpus/source-snapshots/round-45/{S071.txt,S072.txt,manifest.json}   byte copies of the pinned captures
The tree carries NO source-recheck.py: counter v1.1 runs it from its own lane (the counter's TOOL_ROOT).
The F27 entry has the provenance trio, the four required sections, a 3-column table of 6 data rows (five curly spans whose
`S071.txt:N[-M]` citations are LOCATED by search in the real snapshot, never hard-coded), two located
`corpus/knowledge/<file>.md:N` cross-references, and is padded to 3600 bytes (the counter's floor is 3000).

Synthetic pins: the counter pins S071.txt, manifest.json and the 63 base knowledge names by sha256. The selftest hands the
counter a JSON file through the GRADER-side env var R45_PINS_OVERRIDE (keys S071.txt, manifest.json, base-knowledge-names):
the first two are the real captures' hashes (computed here from --lane), the third is the hash of the synthetic 63 stub names.
A few cases run with the REAL pins (no override) and one case runs the real lane tree itself.

Case classes (only controls and mutants are counted):
  control  unmutated tree, no-op, boundaries that must pass (25-word span, 3000-byte entry, 6-row table, decoys hidden in
           comments/fences, ignored env vars, real tree, tool-lane copy of the real source-recheck)  -> must print fixed=7/7
  mutant   one defect; the targeted gate(s) must print pass=0 and all seven gate lines must be present
  probe    accepted-by-design questions; printed, never counted
`--do-nothing-control` runs every case against a stub that always prints 7/7: every mutant must then FAIL.

Usage: python3 r45-counters-selftest-c2.py [--lane DIR] [--counter PATH] [--do-nothing-control] [--keep]
  --lane    the tree whose corpus/instruments/r45-c2-gate.py and round-45 captures are used (default: the lane; pass an EXPORT)
Prints: `selftest cases=<N> failures=<F>` last; exit 0 iff F == 0.
READ-ONLY on --lane; scratch only under $HYAKU_SCRATCH/kasegi-r45/selftest-c2/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
URL = "https://docs.kernel.org/process/security-bugs.html"
ENTRY_NAME = "linux-kernel-security-bugs-reporting-process.md"
ENTRY_REL = "corpus/knowledge/" + ENTRY_NAME
SNAP_REL = "corpus/source-snapshots/round-45/S071.txt"
S072_REL = "corpus/source-snapshots/round-45/S072.txt"
MAN_REL = "corpus/source-snapshots/round-45/manifest.json"
XREF_T = "corpus/knowledge/coordinated-disclosure-timelines.md:7-17"
XREF_A = "corpus/knowledge/ai-assisted-finding-validation.md:7-8,15"
SECTIONS = ["## Scope and decision rule", "## Overlap and novelty", "## Limits", "## Falsifiable package rule"]
PAD_PREFIX = "Reading note: "
EMPTY_SHA = hashlib.sha256(b"").hexdigest()


def norm(s: str) -> str:
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


# ----------------------------------------------------------------------------- snapshot access
class Snap:
    def __init__(self, lane: str):
        self.raw = open(os.path.join(lane, SNAP_REL), "rb").read()
        self.lines = self.raw.decode("utf-8").splitlines()
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def locate(self, quote: str) -> tuple[int, int]:
        """Smallest line window [a,b] (1-based) whose normalised text holds the quote."""
        nq = norm(quote)
        for width in range(1, 8):
            for a in range(1, len(self.lines) - width + 2):
                b = a + width - 1
                if nq in norm(" ".join(self.lines[a - 1:b])):
                    return a, b
        raise SystemExit(f"selftest: quote not located in snapshot: {quote!r}")

    def words_ending_at(self, last_word_text: str, n: int, a: int, b: int) -> str:
        w = norm(" ".join(self.lines[a - 1:b])).split()
        end = max(i for i, x in enumerate(w) if x == last_word_text)
        return " ".join(w[end - n + 1:end + 1])


QUOTES = {
    "seven": "for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days",
    "ai": "If you resorted to AI assistance to identify a bug, you must treat it as public",
    "binary": "Binary-only executables are not accepted.",
    "repro": "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.",
    "version": "with no version indication, your report will not be processed",
}
ROWS = [
    ("version", "Does the report name a kernel version?", "Record the version field as missing."),
    ("seven", "How long may publication of a fix be postponed?", "Cap the stated postponement at the page's figures."),
    ("ai", "Does an AI-assisted finding stay private?", "Record the publication status as public."),
    ("binary", "May the reproducer be a binary?", "The reproducer must be source or a script."),
    ("repro", "Is an unreproducible issue a security bug?", "Keep it out of security-bug status."),
    (None, "Is a CVE a required intake field?", "No CVE is listed as a required field."),
]


def cite(a: int, b: int) -> str:
    return f"`S071.txt:{a}`" if a == b else f"`S071.txt:{a}-{b}`"


def fit(text: str, n: int) -> str:
    """Return text with its PAD line grown so the UTF-8 length is exactly n bytes."""
    lines = text.split("\n")
    i = next(k for k, ln in enumerate(lines) if ln.startswith(PAD_PREFIX))
    lines[i] = PAD_PREFIX + "."
    base = len("\n".join(lines).encode("utf-8"))
    if n < base:
        raise SystemExit(f"selftest harness bug: cannot fit {n} bytes (base {base})")
    lines[i] = PAD_PREFIX + "x" * (n - base) + "."
    out = "\n".join(lines)
    assert len(out.encode("utf-8")) == n
    return out


def entry_text(snap: Snap, size: int = 3600, junk_table: bool = False) -> str:
    spans = {k: (t, *snap.locate(t)) for k, t in QUOTES.items()}  # citation always where the REAL quote lives
    out = [
        "# Linux kernel security-bugs reporting process (synthetic)",
        "",
        f"source: S071 — {URL} — section anchors: Preparing your report (S071.txt:10-71)",
        "verified-at: 2026-10-28",
        f"recheck: cd {LANE} && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d",
        "",
        SECTIONS[0],
        "",
        "This synthetic entry records what the kernel's own security-bugs page states and nothing more.",
        "",
        "| observed question | kernel text | package consequence |",
        "|---|---|---|",
    ]
    tail = []
    for k, q, c in ROWS:
        if k is None:
            out.append(f"| {q} | no CVE is required | {c} |")
            continue
        t, a, b = spans[k]
        if junk_table:
            out.append("| a | b | c |")
            tail.append(f"- On this point the page says “{t}” ({cite(a, b)}).")
        else:
            out.append(f"| {q} | “{t}” ({cite(a, b)}) | {c} |")
    if junk_table:
        out.append("| a | b | c |")  # junk table: six 3-column rows, none from the source
    out += [""] + tail + [""]
    out += [
        SECTIONS[1],
        "",
        "Already held in this corpus:",
        "",
        f"- F02 (`{XREF_T}`) requires a timeline to name the policy, the clock-starting event and the stated interval.",
        f"- F04 (`{XREF_A}`) holds that an AI-originated finding stays a candidate until reproduction is recorded.",
        "",
        "What is new here: the kernel's own intake contract, stated as the page states it.",
        "",
        SECTIONS[2],
        "",
        "- One project's rule: the Linux kernel security team's page. It is not law and not a general standard.",
        "- Documentation only. The entry instructs no contact with anyone and no probing of any system.",
        PAD_PREFIX + ".",
        "",
        SECTIONS[3],
        "",
        "When a package states the publication deferral for a kernel security fix, check it against the table above in order.",
        "",
    ]
    return fit("\n".join(out), size)


def sources_text(snap: Snap) -> str:
    hdr = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    row = ("| S071 | Linux kernel documentation, Security bugs — " + URL +
           " | docs | A | Linux kernel security-bugs reporting process: report contents, embargo ceiling, qualification rules | "
           f"Security bugs page; capture at corpus/source-snapshots/round-45/S071.txt, sha256 {snap.sha} | "
           "Read the kernel's own reporting rules before reporting | mined | 2026-10-28 | 180d | " + ENTRY_REL + " |")
    return "\n".join(["# SOURCES — synthetic", "", "## Registry", "", hdr, sep, row, "", "## Paths", "", "- none", ""])


def readme_text() -> str:
    out = ["# corpus — synthetic", "", "## Frontier", "", "| id | topic | status | entry | sources | next |", "|---|---|---|---|---|---|"]
    for i in range(1, 27):
        out.append(f"| F{i:02d} | topic {i} | admitted | knowledge/stub-{i:02d}.md | S0{i:02d} | next {i}. |")
    out.append(f"| F27 | Linux kernel security-bugs reporting process | admitted | `{ENTRY_REL}` | S071 | Re-open the page before relying on it. |")
    return "\n".join(out) + "\n"


def stub_names() -> list[str]:
    return sorted([f"stub-{i:02d}.md" for i in range(1, 62)] + ["coordinated-disclosure-timelines.md", "ai-assisted-finding-validation.md"])


def base_names_sha() -> str:
    return hashlib.sha256(("\n".join(stub_names()) + "\n").encode()).hexdigest()


def build(root: str, lane: str, snap: Snap) -> None:
    def w(rel: str, data: str | bytes) -> None:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))

    w("corpus/README.md", readme_text())
    w("corpus/SOURCES.md", sources_text(snap))
    w(ENTRY_REL, entry_text(snap))
    for n in stub_names():
        w("corpus/knowledge/" + n, "# stub " + n + "\n" + "".join(f"line {i}\n" for i in range(2, 22)))
    for rel in (SNAP_REL, S072_REL, MAN_REL):
        w(rel, open(os.path.join(lane, rel), "rb").read())


# ----------------------------------------------------------------------------- mutation helpers
def rd(root: str, rel: str) -> str:
    return open(os.path.join(root, rel), encoding="utf-8").read()


def wr(root: str, rel: str, data: str | bytes) -> None:
    mode = "wb" if isinstance(data, bytes) else "w"
    kw = {} if isinstance(data, bytes) else {"encoding": "utf-8"}
    with open(os.path.join(root, rel), mode, **kw) as fh:
        fh.write(data)


def sub(root: str, rel: str, old: str, new: str, count: int = 1) -> None:
    t = rd(root, rel)
    if old not in t:
        raise SystemExit(f"selftest harness bug: {old!r} not in {rel}")
    wr(root, rel, t.replace(old, new, count))


def line_of(root: str, rel: str, prefix: str) -> str:
    ln = [x for x in rd(root, rel).split("\n") if x.startswith(prefix)]
    if len(ln) != 1:
        raise SystemExit(f"selftest harness bug: {prefix!r} matched {len(ln)} lines in {rel}")
    return ln[0]


def wrap_line(root: str, rel: str, prefix: str, before: str, after: str) -> None:
    ln = line_of(root, rel, prefix)
    sub(root, rel, ln, before + "\n" + ln + "\n" + after)


def refit(root: str, n: int) -> None:
    wr(root, ENTRY_REL, fit(rd(root, ENTRY_REL), n))


def swap_quote(key: str, new_text: str):
    def f(root: str) -> None:
        sub(root, ENTRY_REL, "“" + QUOTES[key] + "”", "“" + new_text + "”")
    return f


class Case:
    def __init__(self, name, kind, mut=None, targets=(), env=None, pins="syn", tool=None, real=False):
        self.name, self.kind, self.mut = name, kind, mut or (lambda r: None)
        self.targets, self.env, self.pins, self.tool, self.real = set(targets), env or {}, pins, tool, real


# ----------------------------------------------------------------------------- counter runner
def run_counter(counter: str, root: str, env: dict) -> tuple[dict[str, int], str, str]:
    p = subprocess.run([sys.executable, counter, "--root", root], capture_output=True, text=True, timeout=600, env=env)
    out = p.stdout + p.stderr
    gates = {m.group(1): int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])", out, re.M)}
    fx = re.search(r"^c2-gate fixed=(\d+)/7", out, re.M)
    return gates, (f"fixed={fx.group(1)}/7" if fx else "fixed=?"), out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--counter", default=None)
    ap.add_argument("--do-nothing-control", action="store_true")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()

    scratch = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kasegi-r45", "selftest-c2")
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2st-", dir=scratch)
    tmp = os.path.join(work, "tmp")
    os.makedirs(tmp)
    try:
        counter = a.counter or os.path.join(a.lane, "corpus/instruments/r45-c2-gate.py")
        if a.do_nothing_control:
            counter = os.path.join(work, "do-nothing-counter.py")
            with open(counter, "w") as fh:
                fh.write("import sys\nfor i in range(1, 8):\n    print(f'gate G{i} pass=1 read=do-nothing')\nprint('c2-gate fixed=7/7 exit=0')\n")
        snap = Snap(a.lane)
        man_sha = hashlib.sha256(open(os.path.join(a.lane, MAN_REL), "rb").read()).hexdigest()
        synpins = os.path.join(work, "pins-synthetic.json")
        json.dump({"S071.txt": snap.sha, "manifest.json": man_sha, "base-knowledge-names": base_names_sha()}, open(synpins, "w"))
        badsnappins = os.path.join(work, "pins-bad-snapshot.json")
        json.dump({"S071.txt": "0" * 64}, open(badsnappins, "w"))
        fakecensus = os.path.join(work, "fake-census.sh")
        with open(fakecensus, "w") as fh:
            fh.write("#!/bin/sh\nprintf 'fake\\tok\\tfake\\n'\nexit 0\n")
        os.chmod(fakecensus, 0o755)

        # words windows for the word-limit boundary
        ba, bb = snap.locate(QUOTES["binary"])
        w26 = snap.words_ending_at("accepted.", 26, ba - 5, bb)
        w25 = snap.words_ending_at("accepted.", 25, ba - 5, bb)
        assert len(w26.split()) == 26 and len(w25.split()) == 25
        a26, b26 = snap.locate(w26)
        s072 = open(os.path.join(a.lane, S072_REL), encoding="utf-8").read()
        borrowed = "Welcome to the VRP rules section!"
        assert borrowed in s072
        seven_a, seven_b = snap.locate(QUOTES["seven"])
        ra, rb = snap.locate(QUOTES["repro"])
        assert rb > ra
        bin_cite = cite(ba, bb)

        # ---------------------------------------------------------------- mutators (wave-1 set, adapted)
        def m_wrong_line(r): sub(r, ENTRY_REL, cite(seven_a, seven_b), "`S071.txt:200`")
        def m_26w(r): sub(r, ENTRY_REL, "“" + QUOTES["binary"] + "” (" + bin_cite, "“" + w26 + "” (" + cite(a26, b26))
        def m_25w(r): sub(r, ENTRY_REL, "“" + QUOTES["binary"] + "” (" + bin_cite, "“" + w25 + "” (" + cite(a26, b26))
        def m_tier(r): sub(r, "corpus/SOURCES.md", "| docs | A |", "| docs | B |")
        def m_status(r): sub(r, "corpus/SOURCES.md", "| mined |", "| queued |")
        def m_usedby(r): sub(r, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | — |")
        def m_usedby_other(r): sub(r, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | corpus/knowledge/stub-01.md |")

        def m_snap_flip(r):  # one byte in a region no frozen quote touches
            b = bytearray(open(os.path.join(r, SNAP_REL), "rb").read())
            b[b.index(b"Security bugs")] ^= 0x01
            wr(r, SNAP_REL, bytes(b))

        def m_snap_newline(r): wr(r, SNAP_REL, open(os.path.join(r, SNAP_REL), "rb").read() + b"\n")
        def m_man_newline(r): wr(r, MAN_REL, open(os.path.join(r, MAN_REL), "rb").read() + b"\n")

        def m_manifest_q5(r):
            m = json.loads(rd(r, MAN_REL))
            s = [x for x in m["sources"] if x["id"] == "S071"][0]
            s["quotes"] = [q for q in s["quotes"] if q["id"] != "Q5"]
            wr(r, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def m_manifest_q1_edit(r): sub(r, MAN_REL, "up to 7 calendar days", "up to 9 calendar days")
        def m_manifest_sha(r): sub(r, MAN_REL, snap.sha, "0" * 64)
        def m_manifest_absent(r): os.remove(os.path.join(r, MAN_REL))

        def m_manifest_note(r):  # Q5 core moved from `quotes` into a free-form note: bytes differ from the pin
            m = json.loads(rd(r, MAN_REL))
            s = [x for x in m["sources"] if x["id"] == "S071"][0]
            for q in s["quotes"]:
                if q["id"] == "Q5":
                    q["quote"] = "Linux kernel developers take security very seriously."
                    q["anchor"] = 6
            s["note"] = QUOTES["version"]
            wr(r, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def m_planted_recheck_flip(r):  # tree-supplied always-OK source-recheck.py + a flipped snapshot byte
            os.makedirs(os.path.join(r, "corpus/instruments"), exist_ok=True)
            wr(r, "corpus/instruments/source-recheck.py",
               "print('S071:sha256 OK')\nfor i in range(1, 6):\n    print(f'S071:Q{i} OK anchor=1')\n")
            m_snap_flip(r)

        def m_selfpinned_empty(r):  # empty capture, anchor carries the empty-file sha (the wave-1 self-pin)
            wr(r, SNAP_REL, b"")
            sub(r, "corpus/SOURCES.md", snap.sha, EMPTY_SHA)

        def m_k65(r): wr(r, "corpus/knowledge/stub-99.md", "# extra\n")
        def m_k63(r): os.remove(os.path.join(r, "corpus/knowledge/stub-61.md"))

        def m_k_swap(r):  # 64 files, a base name replaced by a pad name
            os.remove(os.path.join(r, "corpus/knowledge/stub-61.md"))
            wr(r, "corpus/knowledge/pad-61.md", "# pad\n")

        def m_k_rename(r): os.rename(os.path.join(r, "corpus/knowledge/stub-60.md"), os.path.join(r, "corpus/knowledge/stub-60-renamed.md"))

        def m_k_pad_nonbase_and_drop_xref(r):  # pad file added, one of the two cross-referenced base files removed
            wr(r, "corpus/knowledge/pad-a.md", "# pad\n")
            os.remove(os.path.join(r, "corpus/knowledge/ai-assisted-finding-validation.md"))

        def m_dup_f(r): sub(r, "corpus/README.md", "| F25 |", "| F26 |")
        def m_f27_queued(r): sub(r, "corpus/README.md", "| F27 | Linux kernel security-bugs reporting process | admitted |", "| F27 | Linux kernel security-bugs reporting process | queued |")
        def m_f26_queued(r): sub(r, "corpus/README.md", "| F26 | topic 26 | admitted |", "| F26 | topic 26 | queued |")
        def m_26_rows(r): sub(r, "corpus/README.md", "| F25 | topic 25 | admitted | knowledge/stub-25.md | S025 | next 25. |\n", "")
        def m_f27_entry_missing(r): sub(r, "corpus/README.md", "`" + ENTRY_REL + "`", "`corpus/knowledge/does-not-exist.md`")
        def m_f27_unrelated_entry(r): sub(r, "corpus/README.md", "`" + ENTRY_REL + "`", "`corpus/knowledge/stub-01.md`")
        def m_f27_two_paths(r): sub(r, "corpus/README.md", "`" + ENTRY_REL + "`", "`corpus/knowledge/stub-01.md` `" + ENTRY_REL + "`")
        def m_f27_no_path(r): sub(r, "corpus/README.md", "`" + ENTRY_REL + "`", "pending")
        def m_f27_shared(r): sub(r, "corpus/README.md", "| knowledge/stub-26.md |", "| " + ENTRY_REL + " |")
        def m_f27_comment(r): wrap_line(r, "corpus/README.md", "| F27 |", "<!--", "-->")
        def m_f27_fence(r): wrap_line(r, "corpus/README.md", "| F27 |", "```", "```")
        def m_f27_inline_comment(r):
            ln = line_of(r, "corpus/README.md", "| F27 |")
            sub(r, "corpus/README.md", ln, "<!-- " + ln + " -->")
        def m_f27_live_decoy(r): wr(r, "corpus/README.md", rd(r, "corpus/README.md") + "| F27 | decoy | admitted | knowledge/stub-02.md | S071 | x |\n")

        def m_entry_symlink(r):
            os.makedirs(os.path.join(r, "corpus/notes"))
            real = os.path.join(r, "corpus/notes/real-entry.md")
            os.rename(os.path.join(r, ENTRY_REL), real)
            os.symlink(real, os.path.join(r, ENTRY_REL))

        def m_entry_dir(r):
            os.remove(os.path.join(r, ENTRY_REL))
            os.mkdir(os.path.join(r, ENTRY_REL))

        def m_entry_empty(r): wr(r, ENTRY_REL, "")
        def m_header_only(r): wr(r, ENTRY_REL, "\n".join(rd(r, ENTRY_REL).split("\n")[:5]) + "\n")
        def m_no_source_line(r): sub(r, ENTRY_REL, f"source: S071 — {URL} — section anchors: Preparing your report (S071.txt:10-71)\n", "")
        def m_source_nosuffix(r): sub(r, ENTRY_REL, f"source: S071 — {URL} — section anchors: Preparing your report (S071.txt:10-71)", f"source: S071 — {URL}")
        def m_source_urlsuffix(r): sub(r, ENTRY_REL, f"source: S071 — {URL} — ", f"source: S071 — {URL}.evil — ")
        def m_wrong_verified(r): sub(r, ENTRY_REL, "verified-at: 2026-10-28", "verified-at: 2026-10-27")
        def m_no_recheck(r): wr(r, ENTRY_REL, "\n".join(x for x in rd(r, ENTRY_REL).split("\n") if not x.startswith("recheck:")))
        def m_recheck_nosource(r): sub(r, ENTRY_REL, " --source S071 # 180d", " # 180d")
        def m_wrong_url(r): sub(r, ENTRY_REL, "source: S071 — " + URL, "source: S071 — https://example.org/security-bugs.html")
        def m_trio_low(r): sub(r, ENTRY_REL, "\nsource: S071", "\n" * 9 + "source: S071")

        def m_sec(i):
            def f(r): sub(r, ENTRY_REL, "\n" + SECTIONS[i] + "\n", "\n")
            return f

        def m_sec_suffix(r): sub(r, ENTRY_REL, "\n## Limits\n", "\n## Limits and scope\n")
        def m_sec_indent(r): sub(r, ENTRY_REL, "\n## Limits\n", "\n ## Limits\n")
        def m_table_5(r): sub(r, ENTRY_REL, "| Is a CVE a required intake field? | no CVE is required | No CVE is listed as a required field. |\n", "")
        def m_table_none(r): wr(r, ENTRY_REL, "\n".join(x for x in rd(r, ENTRY_REL).split("\n") if not x.startswith("|")) + "\n")
        def m_xref_line(r): sub(r, ENTRY_REL, XREF_T, "corpus/knowledge/coordinated-disclosure-timelines.md:9999")
        def m_xref_zero(r): sub(r, ENTRY_REL, XREF_A, "corpus/knowledge/ai-assisted-finding-validation.md:0")
        def m_xref_ghost(r): sub(r, ENTRY_REL, XREF_A, "corpus/knowledge/ghost-validation.md:7")
        def m_xref_drop_t(r): sub(r, ENTRY_REL, XREF_T, "corpus/knowledge/stub-01.md:3")
        def m_xref_drop_a(r): sub(r, ENTRY_REL, XREF_A, "corpus/knowledge/stub-02.md:3")
        def m_xref_none(r): sub(r, ENTRY_REL, "(`" + XREF_T + "`)", "(see the F02 entry)"); sub(r, ENTRY_REL, "(`" + XREF_A + "`)", "(see the F04 entry)")
        def m_xref_trunc_t(r): wr(r, "corpus/knowledge/coordinated-disclosure-timelines.md", "# stub\nline 2\nline 3\n")
        def m_xref_trunc_a(r): wr(r, "corpus/knowledge/ai-assisted-finding-validation.md", "# stub\nline 2\nline 3\n")
        def m_xref_target_dir(r):
            p = os.path.join(r, "corpus/knowledge/ai-assisted-finding-validation.md")
            os.remove(p)
            os.mkdir(p)

        def m_short(r): refit(r, 2999)
        def m_short_small(r): refit(r, 2500)
        def m_uncited(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "The page also says “do not rely on memory” without a citation.\n")
        def m_uncited_real(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "Restated: “" + QUOTES["binary"] + "”\n")
        def m_cite_apart(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "The page says “do not rely on memory” as shown at (`S071.txt:10`).\n")
        def m_cite_not_paren(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "The page says “" + QUOTES["binary"] + "” — `S071.txt:39-40`.\n")
        def m_uncited_in_table(r): sub(r, ENTRY_REL, "| no CVE is required |", "| “no CVE is required” |")

        def m_row_comment(r): wrap_line(r, "corpus/SOURCES.md", "| S071 |", "<!--", "-->")
        def m_row_fence(r): wrap_line(r, "corpus/SOURCES.md", "| S071 |", "```", "```")

        def m_row_comment_decoy(r):
            sub(r, "corpus/SOURCES.md", "## Paths", "<!--\n| S071 | decoy | docs | C | x | y | z | queued | 2026-10-28 | 1d | — |\n-->\n\n## Paths")

        def m_row_paths(r):  # row moved out of ## Registry into ## Paths
            ln = line_of(r, "corpus/SOURCES.md", "| S071 |")
            sub(r, "corpus/SOURCES.md", ln + "\n", "")
            sub(r, "corpus/SOURCES.md", "- none\n", "- none\n" + ln + "\n")

        def m_row_absent(r): wr(r, "corpus/SOURCES.md", "\n".join(x for x in rd(r, "corpus/SOURCES.md").split("\n") if not x.startswith("| S071")))
        def m_anchor_nosha(r): sub(r, "corpus/SOURCES.md", "sha256 " + snap.sha, "sha256 (pending)")
        def m_anchor_wrongsha(r): sub(r, "corpus/SOURCES.md", snap.sha, "f" * 64)
        def m_row_10cells(r): sub(r, "corpus/SOURCES.md", " | 180d | " + ENTRY_REL + " |", " | " + ENTRY_REL + " |")
        def m_kind_bad(r): sub(r, "corpus/SOURCES.md", "| docs | A |", "| bogus | A |")

        def m_dup_url_row(r):
            row = line_of(r, "corpus/SOURCES.md", "| S071 |")
            sub(r, "corpus/SOURCES.md", row, row + "\n" + row.replace("| S071 |", "| S900 |", 1))

        def m_opened_future(r): sub(r, "corpus/SOURCES.md", "| mined | 2026-10-28 |", "| mined | 2099-01-01 |")
        def m_usedby_dangling(r): sub(r, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | " + ENTRY_REL + ", corpus/knowledge/ghost.md |")
        def m_url_cell(r): sub(r, "corpus/SOURCES.md", "Security bugs — " + URL, "Security bugs — https://example.org/x")
        def m_opened_bad(r): sub(r, "corpus/SOURCES.md", "| mined | 2026-10-28 | 180d", "| mined | 2026-10-27 | 180d")

        m_fabricated = swap_quote("seven", "for up to 3 calendar days from the start of the release process, with no extension at all")
        m_near_miss = swap_quote("seven", QUOTES["seven"].replace("7 calendar", "8 calendar"))
        m_binary_fab = swap_quote("binary", "Binary-only executables are accepted when signed.")
        m_ai_fab = swap_quote("ai", "If you resorted to AI assistance to identify a bug, you may treat it as private")
        m_repro_fab = swap_quote("repro", "By definition if an issue cannot be reproduced, it is still exploitable, thus it is a security bug.")
        def m_borrowed(r): sub(r, ENTRY_REL, "“" + QUOTES["version"] + "”", "“" + borrowed + "”")
        def m_straight(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL).replace("“", '"').replace("”", '"'))
        def m_extra_bad_span(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "A sixth claim reads “the kernel team answers within one hour” (`S071.txt:100`).\n")
        def m_drop_ai_span(r): sub(r, ENTRY_REL, "“" + QUOTES["ai"] + "” (", "(")
        def m_drop_cite(r): sub(r, ENTRY_REL, " (" + bin_cite + ")", "")
        def m_paraphrase(r): sub(r, ENTRY_REL, "“" + QUOTES["seven"] + "” (" + cite(seven_a, seven_b) + ")", "a seven day cap")
        def m_cite_past(r): sub(r, ENTRY_REL, cite(seven_a, seven_b), f"`S071.txt:{seven_b + 1}`")
        def m_cite_reversed(r): sub(r, ENTRY_REL, cite(ba, bb), f"`S071.txt:{ba + 40}-{ba + 39}`")
        def m_repro_cut(r): sub(r, ENTRY_REL, cite(ra, rb), cite(ra, ra))

        # ---------------------------------------------------------------- probes (accepted-by-design questions)
        def p_wide_range(r): sub(r, ENTRY_REL, cite(seven_a, seven_b), f"`S071.txt:1-{len(snap.lines)}`")
        def p_usedby_suffix(r):
            wr(r, ENTRY_REL + ".bak", "x\n")
            sub(r, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | " + ENTRY_REL + ".bak |")
        def p_f27_sources_wrong(r): sub(r, "corpus/README.md", "| `" + ENTRY_REL + "` | S071 |", "| `" + ENTRY_REL + "` | S001 |")
        def p_dir_md(r):
            p = os.path.join(r, "corpus/knowledge/stub-61.md")
            os.remove(p)
            os.mkdir(p)
        def p_base_emptied(r): wr(r, "corpus/knowledge/stub-01.md", "")
        def p_xref_other_lines(r): sub(r, ENTRY_REL, XREF_A, "corpus/knowledge/ai-assisted-finding-validation.md:20")
        def p_heading_in_comment(r):
            sub(r, ENTRY_REL, "\n## Limits\n", "\n<!-- ## Limits -->\n")
        def p_single_curly_fab(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "The page also says ‘every report is answered within one hour’ with no citation.\n")
        def p_straight_fab(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + 'The page also says "every report is answered within one hour" with no citation.\n')
        def p_stray_open_curly(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "A stray opening mark “ with nothing closing it.\n")
        def p_curly_in_comment(r): wr(r, ENTRY_REL, rd(r, ENTRY_REL) + "<!-- “hidden uncited span” -->\n")
        def p_junk_table(r): wr(r, ENTRY_REL, entry_text(snap, junk_table=True))
        def p_cite_other_file(r): sub(r, ENTRY_REL, cite(seven_a, seven_b), f"`S071.txt:{seven_a}-{seven_b}` `S072.txt:1`")
        def p_comment_cite(r): sub(r, ENTRY_REL, "(" + bin_cite + ")", "(" + bin_cite + ")<!-- junk -->")

        S = {"syn": "syn", "real": "real"}
        CASES: list[Case] = [
            # ---- controls
            Case("C0 unmutated synthetic tree", "control"),
            Case("C1 no-op rewrite of README (same bytes)", "control", lambda r: wr(r, "corpus/README.md", rd(r, "corpus/README.md"))),
            Case("C2 25-word genuine span (boundary)", "control", m_25w),
            Case("C3 entry exactly 3000 bytes (boundary)", "control", lambda r: refit(r, 3000)),
            Case("C4 table with exactly 6 data rows (the default tree)", "control"),
            Case("C5 decoy F27 row inside a code fence is ignored", "control", lambda r: wr(r, "corpus/README.md", rd(r, "corpus/README.md") + "\n```\n| F27 | decoy | admitted | knowledge/x.md | S071 | x |\n```\n")),
            Case("C6 decoy F27 row inside an HTML comment is ignored", "control", lambda r: wr(r, "corpus/README.md", rd(r, "corpus/README.md") + "\n<!--\n| F27 | decoy | queued | knowledge/x.md | S071 | x |\n-->\n")),
            Case("C8 SOURCES_CENSUS=/nonexistent in grader env is ignored (constant census)", "control", env={"SOURCES_CENSUS": "/nonexistent/sources-census.sh"}),
            Case("C9 tree-local source-recheck.py present and ignored (valid tree)", "control", lambda r: (os.makedirs(os.path.join(r, "corpus/instruments"), exist_ok=True), wr(r, "corpus/instruments/source-recheck.py", "raise SystemExit(1)\n"))),
            Case("C10 counter's own-lane copy of the real source-recheck.py passes", "control", tool="copy-real"),
            Case("C11 the real lane tree with real pins (no override)", "control", pins="real", real=True),
            Case("C12 extra non-.md file in knowledge/ is not counted", "control", lambda r: wr(r, "corpus/knowledge/NOTES.txt", "x\n")),
            # ---- mutants: wave-1 set still applicable
            Case("M01 fabricated 7-day quote", "mutant", m_fabricated, {"G5"}),
            Case("M02 quote cited at wrong line (200)", "mutant", m_wrong_line, {"G5"}),
            Case("M03 26-word quote", "mutant", m_26w, {"G5"}),
            Case("M04 tier B", "mutant", m_tier, {"G3"}),
            Case("M05 status queued", "mutant", m_status, {"G3"}),
            Case("M06 used-by missing (—)", "mutant", m_usedby, {"G3"}),
            Case("M07 used-by names another file", "mutant", m_usedby_other, {"G3"}),
            Case("M08 snapshot byte flipped", "mutant", m_snap_flip, {"G3", "G4"}),
            Case("M09 manifest Q5 removed", "mutant", m_manifest_q5, {"G4"}),
            Case("M10 manifest Q1 text edited", "mutant", m_manifest_q1_edit, {"G4"}),
            Case("M11 manifest sha wrong", "mutant", m_manifest_sha, {"G4"}),
            Case("M12 manifest absent", "mutant", m_manifest_absent, {"G4"}),
            Case("M13 63 knowledge files", "mutant", m_k63, {"G6"}),
            Case("M14 65 knowledge files", "mutant", m_k65, {"G6"}),
            Case("M15 duplicate F id (F25->F26)", "mutant", m_dup_f, {"G1"}),
            Case("M16 F27 status queued", "mutant", m_f27_queued, {"G1"}),
            Case("M17 F26 status queued (26/27 admitted)", "mutant", m_f26_queued, {"G1"}),
            Case("M18 26 frontier rows", "mutant", m_26_rows, {"G1"}),
            Case("M19 F27 entry file missing", "mutant", m_f27_entry_missing, {"G1"}),
            Case("M20 entry lacks source: line", "mutant", m_no_source_line, {"G2"}),
            Case("M21 verified-at wrong date", "mutant", m_wrong_verified, {"G2"}),
            Case("M22 entry lacks recheck: line", "mutant", m_no_recheck, {"G2"}),
            Case("M23 source: line wrong URL", "mutant", m_wrong_url, {"G2"}),
            Case("M24 SOURCES row S071 absent", "mutant", m_row_absent, {"G3"}),
            Case("M25 anchor without sha", "mutant", m_anchor_nosha, {"G3"}),
            Case("M26 anchor with wrong sha", "mutant", m_anchor_wrongsha, {"G3"}),
            Case("M27 row has 10 cells", "mutant", m_row_10cells, {"G3"}),
            Case("M28 source cell wrong URL", "mutant", m_url_cell, {"G3"}),
            Case("M29 opened date wrong", "mutant", m_opened_bad, {"G3"}),
            Case("M30 kind enum violation", "mutant", m_kind_bad, {"G7"}),
            Case("M31 duplicate URL+scope row (E04)", "mutant", m_dup_url_row, {"G7"}),
            Case("M32 opened in the future (E08)", "mutant", m_opened_future, {"G7"}),
            Case("M33 dangling used-by path (E11)", "mutant", m_usedby_dangling, {"G7"}),
            Case("M34 near-miss quote (8 for 7 days)", "mutant", m_near_miss, {"G5"}),
            Case("M35 fabricated binary-only quote", "mutant", m_binary_fab, {"G5"}),
            Case("M36 fabricated AI quote (private)", "mutant", m_ai_fab, {"G5"}),
            Case("M37 fabricated unreproducible quote", "mutant", m_repro_fab, {"G5"}),
            Case("M38 quote borrowed from S072 cited as S071", "mutant", m_borrowed, {"G5"}),
            Case("M39 straight quotes only (no span parsed)", "mutant", m_straight, {"G5"}),
            Case("M40 extra fabricated sixth span", "mutant", m_extra_bad_span, {"G5"}),
            Case("M41 AI span citation dropped (core unlocated)", "mutant", m_drop_ai_span, {"G5"}),
            Case("M42 binary-only citation removed", "mutant", m_drop_cite, {"G5"}),
            Case("M43 7-day quote replaced by paraphrase", "mutant", m_paraphrase, {"G5"}),
            Case("M44 citation one line past the quote", "mutant", m_cite_past, {"G5"}),
            Case("M45 reversed citation range", "mutant", m_cite_reversed, {"G5"}),
            Case("M46 multi-line quote cited at first line only", "mutant", m_repro_cut, {"G5"}),
            # ---- mutants: v1.1 gates
            Case("N01 uncited curly span (new sentence)", "mutant", m_uncited, {"G5"}),
            Case("N02 uncited curly span restating a REAL quote", "mutant", m_uncited_real, {"G5"}),
            Case("N03 curly span with citation separated by words", "mutant", m_cite_apart, {"G5"}),
            Case("N04 curly span followed by an em-dash and unparenthesised citation", "mutant", m_cite_not_paren, {"G5"}),
            Case("N05 uncited curly span inside a table cell", "mutant", m_uncited_in_table, {"G5"}),
            Case("N06 comment-hidden F27 row (block comment)", "mutant", m_f27_comment, {"G1"}),
            Case("N07 comment-hidden F27 row (inline comment)", "mutant", m_f27_inline_comment, {"G1"}),
            Case("N08 fenced F27 row", "mutant", m_f27_fence, {"G1"}),
            Case("N09 live decoy second F27 row (28 rows, duplicate id)", "mutant", m_f27_live_decoy, {"G1"}),
            Case("N10 fenced S071 row", "mutant", m_row_fence, {"G3"}),
            Case("N11 S071 row inside an HTML comment", "mutant", m_row_comment, {"G3"}),
            Case("N12 S071 row moved under ## Paths", "mutant", m_row_paths, {"G3"}),
            Case("N13 F27 entry shared with the F26 row", "mutant", m_f27_shared, {"G1"}),
            Case("N14 F27 entry cell lists two knowledge paths", "mutant", m_f27_two_paths, {"G1"}),
            Case("N15 F27 entry cell names no path", "mutant", m_f27_no_path, {"G1"}),
            Case("N16 F27 entry is a symlink (to a file outside knowledge/)", "mutant", m_entry_symlink, {"G1"}),
            Case("N17 F27 entry path is a directory", "mutant", m_entry_dir, {"G1"}),
            Case("N18 F27 cell points at an unrelated existing stub", "mutant", m_f27_unrelated_entry, {"G2", "G3", "G5"}),
            Case("N19 empty entry file", "mutant", m_entry_empty, {"G2", "G5", "G6"}),
            Case("N20 header-only entry (title + trio)", "mutant", m_header_only, {"G2", "G5", "G6"}),
            Case("N21 missing section: Scope and decision rule", "mutant", m_sec(0), {"G2"}),
            Case("N22 missing section: Overlap and novelty", "mutant", m_sec(1), {"G2"}),
            Case("N23 missing section: Limits", "mutant", m_sec(2), {"G2"}),
            Case("N24 missing section: Falsifiable package rule", "mutant", m_sec(3), {"G2"}),
            Case("N25 section heading with a suffix", "mutant", m_sec_suffix, {"G2"}),
            Case("N26 section heading indented one space", "mutant", m_sec_indent, {"G2"}),
            Case("N27 table has 5 data rows", "mutant", m_table_5, {"G2"}),
            Case("N28 entry has no table", "mutant", m_table_none, {"G2", "G5"}),
            Case("N29 short entry: 2999 bytes", "mutant", m_short, {"G6"}),
            Case("N30 short entry: 2500 bytes", "mutant", m_short_small, {"G6"}),
            Case("N31 dangling xref: line 9999", "mutant", m_xref_line, {"G2"}),
            Case("N32 dangling xref: line 0", "mutant", m_xref_zero, {"G2"}),
            Case("N33 xref names a ghost file", "mutant", m_xref_ghost, {"G2"}),
            Case("N34 xref to coordinated-disclosure-timelines.md replaced", "mutant", m_xref_drop_t, {"G2"}),
            Case("N35 xref to ai-assisted-finding-validation.md replaced", "mutant", m_xref_drop_a, {"G2"}),
            Case("N36 no xrefs at all", "mutant", m_xref_none, {"G2"}),
            Case("N37 xref target coordinated-disclosure-timelines.md truncated below the cited line", "mutant", m_xref_trunc_t, {"G2"}),
            Case("N38 xref target ai-assisted-finding-validation.md truncated below the cited line", "mutant", m_xref_trunc_a, {"G2"}),
            Case("N39 xref target replaced by a directory named *.md", "mutant", m_xref_target_dir, {"G2"}),
            Case("N40 padded knowledge dir: base name swapped for a pad name (still 64)", "mutant", m_k_swap, {"G6"}),
            Case("N41 padded knowledge dir: a base file renamed (still 64)", "mutant", m_k_rename, {"G6"}),
            Case("N42 padded knowledge dir: pad added, cross-referenced base dropped (64)", "mutant", m_k_pad_nonbase_and_drop_xref, {"G6"}),
            Case("N43 self-pinned empty snapshot (anchor sha = sha256 of empty)", "mutant", m_selfpinned_empty, {"G3", "G4", "G5"}),
            Case("N44 snapshot with one trailing newline appended", "mutant", m_snap_newline, {"G3"}),
            Case("N45 manifest with one trailing newline appended", "mutant", m_man_newline, {"G4"}),
            Case("N46 Q5 core moved to a free-form manifest note", "mutant", m_manifest_note, {"G4"}),
            Case("N47 tree-supplied always-OK source-recheck.py + flipped snapshot", "mutant", m_planted_recheck_flip, {"G3", "G4"}),
            Case("N48 counter's own-lane source-recheck.py prints nothing (exit 0)", "mutant", tool="silent", targets={"G4"}),
            Case("N49 counter's own-lane source-recheck.py exits 1 after OK lines", "mutant", tool="rc1", targets={"G4"}),
            Case("N50 source: line has no section-anchors tail", "mutant", m_source_nosuffix, {"G2"}),
            Case("N51 source: line URL with an appended suffix", "mutant", m_source_urlsuffix, {"G2"}),
            Case("N52 provenance trio pushed below line 8", "mutant", m_trio_low, {"G2"}),
            Case("N53 recheck: line without --source S071", "mutant", m_recheck_nosource, {"G2"}),
            Case("N54 env SOURCES_CENSUS=<always-ok script> + kind enum violation", "mutant", m_kind_bad, {"G7"}, env={"SOURCES_CENSUS": "@FAKECENSUS@"}),
            Case("N55 real pins active: synthetic stubs are not the 63 base names", "mutant", targets={"G6"}, pins="real"),
            Case("N56 real tree + grader pin override with a wrong S071.txt hash", "mutant", targets={"G3"}, pins="badsnap", real=True),
            Case("N57 decoy duplicate S071 row inside a comment (G3 ignores it, the census does not)", "mutant", m_row_comment_decoy, {"G7"}),
        ]
        PROBES: list[Case] = [
            Case("P1 whole-file citation range 1-N on a true quote", "probe", p_wide_range),
            Case("P2 used-by = entry path + '.bak' suffix", "probe", p_usedby_suffix),
            Case("P3 F27 sources cell says S001 not S071", "probe", p_f27_sources_wrong),
            Case("P4 a base knowledge file replaced by a DIRECTORY named *.md", "probe", p_dir_md),
            Case("P5 a base knowledge file emptied (names intact)", "probe", p_base_emptied),
            Case("P6 xref line valid but unrelated (:20)", "probe", p_xref_other_lines),
            Case("P7 required heading only inside an HTML comment", "probe", p_heading_in_comment),
            Case("P8 fabricated quote in single curly marks, uncited", "probe", p_single_curly_fab),
            Case("P9 fabricated quote in straight marks, uncited", "probe", p_straight_fab),
            Case("P10 stray unbalanced opening curly mark", "probe", p_stray_open_curly),
            Case("P11 uncited curly span inside an HTML comment", "probe", p_curly_in_comment),
            Case("P12 table of six junk 3-column rows, spans moved to bullets", "probe", p_junk_table),
            Case("P13 span citation followed by an S072 citation", "probe", p_cite_other_file),
            Case("P14 junk HTML comment after a citation", "probe", p_comment_cite),
        ]

        # ---------------------------------------------------------------- tool lanes (counter copied beside a chosen source-recheck.py)
        def tool_lane(kind: str, idx: int) -> str:
            lane_dir = os.path.join(work, f"toollane{idx:03d}")
            ins = os.path.join(lane_dir, "corpus/instruments")
            os.makedirs(ins)
            dst = os.path.join(ins, os.path.basename(counter))
            shutil.copy(counter, dst)
            real_rc = os.path.join(a.lane, "corpus/instruments/source-recheck.py")
            if kind == "copy-real":
                shutil.copy(real_rc, os.path.join(ins, "source-recheck.py"))
            elif kind == "silent":
                open(os.path.join(ins, "source-recheck.py"), "w").write("raise SystemExit(0)\n")
            elif kind == "rc1":
                open(os.path.join(ins, "source-recheck.py"), "w").write(
                    "print('S071:sha256 OK')\nfor i in range(1, 6):\n    print(f'S071:Q{i} OK anchor=1')\nraise SystemExit(1)\n")
            return dst

        def run_case(i: int, c: Case) -> tuple[dict[str, int], str, str]:
            if c.real:
                root = a.lane
            else:
                root = os.path.join(work, f"t{i:03d}")
                os.makedirs(root)
                build(root, a.lane, snap)
                c.mut(root)
            env = {k: v for k, v in os.environ.items() if k not in ("R45_PINS_OVERRIDE", "SOURCES_CENSUS")}
            env["TMPDIR"] = tmp
            if c.pins == "syn":
                env["R45_PINS_OVERRIDE"] = synpins
            elif c.pins == "badsnap":
                env["R45_PINS_OVERRIDE"] = badsnappins
            for k, v in c.env.items():
                env[k] = fakecensus if v == "@FAKECENSUS@" else v
            ctr = tool_lane(c.tool, i) if c.tool else counter
            return run_counter(ctr, root, env)

        cases = failures = 0
        print(f"counter={counter}")
        print(f"lane={a.lane}")
        for i, c in enumerate(CASES, 1):
            cases += 1
            g, fx, out = run_case(i, c)
            fails = sorted(k for k, v in g.items() if v == 0)
            if c.kind == "control":
                ok = fx == "fixed=7/7" and len(g) == 7 and all(v == 1 for v in g.values())
                failures += 0 if ok else 1
                print(f"{'ok  ' if ok else 'FAIL'} control {c.name}: {fx} failing={','.join(fails) or '-'}")
                if not ok:
                    print("   CONTROL REJECTED. counter output:\n   " + out.replace("\n", "\n   "))
            else:
                hit = len(g) == 7 and fx != "fixed=7/7" and all(g.get(t, 1) == 0 for t in c.targets)
                collateral = sorted(set(fails) - c.targets)
                failures += 0 if hit else 1
                print(f"{'ok  ' if hit else 'FAIL'} mutant {c.name}: target={','.join(sorted(c.targets))} failing={','.join(fails) or '-'} {fx}"
                      + (f" collateral={','.join(collateral)}" if collateral else ""))
                if not hit:
                    print("   NOT REJECTED. counter output:\n   " + out.replace("\n", "\n   "))
        accepted = 0
        for j, c in enumerate(PROBES, 1):
            g, fx, out = run_case(len(CASES) + j, c)
            acc = fx == "fixed=7/7"
            accepted += 1 if acc else 0
            fails = sorted(k for k, v in g.items() if v == 0)
            print(f"probe {c.name}: {'ACCEPTED (counter blind)' if acc else 'rejected'} failing={','.join(fails) or '-'} {fx}")
        print(f"probes accepted={accepted}/{len(PROBES)} (informational, not counted)")
        print(f"selftest cases={cases} failures={failures}")
        return 0 if failures == 0 else 1
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
