#!/usr/bin/env python3
"""r45-counters-selftest-c2.py — selftest for corpus/instruments/r45-c2-gate.py (round 45, C2).

Builds, in a scratch directory, a COMPLETE synthetic C2 tree:
  corpus/README.md            frontier table F01..F27, all `admitted`, F27 -> knowledge entry
  corpus/SOURCES.md           census-valid registry, S071 row tier A / mined / snapshot sha in anchor
  corpus/knowledge/*.md       64 files: the F27 entry + 63 stubs
  corpus/source-snapshots/round-45/{S071.txt,S072.txt,manifest.json}   byte copies of the pinned captures
  corpus/instruments/source-recheck.py                                 byte copy (G4 runs it from the tree)
The F27 entry carries the provenance trio and curly-quoted spans whose `S071.txt:N[-M]`
citations are LOCATED by search in the real snapshot (not hard-coded), covering all four
frozen cores of the counter. The counter must print `c2-gate fixed=7/7` on it.

Then it applies one mutation per case and asserts the targeted gate(s) go pass=0.
Controls: unmutated tree (7/7), no-op mutation (7/7), 25-word span (7/7 — boundary).
Weakness probes (counter-accepts-by-design questions) are printed, never counted as failures.
`--do-nothing-control` runs the same cases against a stub counter that always prints 7/7;
a sound selftest must then fail every mutant.

Usage: python3 r45-counters-selftest-c2.py [--counter PATH] [--lane DIR] [--do-nothing-control] [--keep]
Prints: `selftest cases=<N> failures=<F>`; exit 0 iff F == 0.
READ-ONLY on the lane; scratch only under $HYAKU_SCRATCH/kasegi-r45/R45ExecSelftestC2/.
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
ENTRY_NAME = "linux-kernel-security-bugs-process.md"
ENTRY_REL = "corpus/knowledge/" + ENTRY_NAME
SNAP_REL = "corpus/source-snapshots/round-45/S071.txt"
MAN_REL = "corpus/source-snapshots/round-45/manifest.json"


def norm(s: str) -> str:
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


# ----------------------------------------------------------------------------- tree builder
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


def cite(a: int, b: int) -> str:
    return f"`S071.txt:{a}`" if a == b else f"`S071.txt:{a}-{b}`"


def entry_text(snap: Snap, overrides: dict[str, str] | None = None) -> str:
    q = dict(QUOTES)
    if overrides:
        q.update(overrides)
    spans = {}
    for k, t in q.items():
        a, b = snap.locate(QUOTES[k])  # citation always where the REAL quote lives
        spans[k] = (t, a, b)
    out = [
        "# Linux kernel security-bugs reporting process",
        "",
        f"source: S071 — {URL}",
        "verified-at: 2026-10-28",
        f"recheck: cd {LANE} && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d",
        "",
        "## Reading rule",
        "",
        "This synthetic entry records what the kernel's own security-bugs page states and nothing more.",
        "",
    ]
    prose = {
        "seven": "The release-delay ceiling is stated as “{t}” ({c}).",
        "ai": "The AI-assistance rule reads “{t}” ({c}).",
        "binary": "On reproducers the page says “{t}” ({c}).",
        "repro": "On exploitability the page says “{t}” ({c}).",
        "version": "On version evidence the page says “{t}” ({c}).",
    }
    for k in ("seven", "ai", "binary", "repro", "version"):
        t, a, b = spans[k]
        out.append(prose[k].format(t=t, c=cite(a, b)))
        out.append("")
    return "\n".join(out)


def sources_text(snap: Snap, extra_rows: list[str] | None = None) -> str:
    hdr = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    row = ("| S071 | Linux kernel documentation, Security bugs — " + URL +
           " | docs | A | Linux kernel security-bugs reporting process: report contents, embargo ceiling, qualification rules | "
           f"Security bugs page; capture at corpus/source-snapshots/round-45/S071.txt, sha256 {snap.sha} | "
           "Read the kernel's own reporting rules before reporting | mined | 2026-10-28 | 180d | " + ENTRY_REL + " |")
    rows = [row] + (extra_rows or [])
    return "\n".join(["# SOURCES — synthetic", "", "## Registry", "", hdr, sep, *rows, "", "## Paths", "", "- none", ""])


def readme_text() -> str:
    out = ["# corpus — synthetic", "", "## Frontier", "", "| id | topic | status | entry | sources | next |", "|---|---|---|---|---|---|"]
    for i in range(1, 27):
        out.append(f"| F{i:02d} | topic {i} | admitted | knowledge/stub-{i:02d}.md | S0{i:02d} | next {i}. |")
    out.append(f"| F27 | Linux kernel security-bugs reporting process | admitted | `knowledge/{ENTRY_NAME}` | S071 | Re-open the page before relying on it. |")
    return "\n".join(out) + "\n"


def build(root: str, lane: str, snap: Snap) -> None:
    def w(rel: str, data: str | bytes) -> None:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))

    w("corpus/README.md", readme_text())
    w("corpus/SOURCES.md", sources_text(snap))
    w(ENTRY_REL, entry_text(snap))
    for i in range(1, 64):
        w(f"corpus/knowledge/stub-{i:02d}.md", f"# stub {i}\n")
    for rel in (SNAP_REL, "corpus/source-snapshots/round-45/S072.txt", MAN_REL, "corpus/instruments/source-recheck.py"):
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


def entry_swap_quote(snap: Snap):
    """Mutation factory: replace the quoted text of one span, keep its (real) citation."""
    def mk(key: str, new_text: str):
        def f(root: str) -> None:
            sub(root, ENTRY_REL, "“" + QUOTES[key] + "”", "“" + new_text + "”")
        return f
    return mk


# ----------------------------------------------------------------------------- counter runner
def run_counter(counter: str, root: str, tmp: str) -> tuple[dict[str, int], str, str]:
    env = dict(os.environ, TMPDIR=tmp)
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

    scratch_base = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    scratch = os.path.join(scratch_base, "kasegi-r45", "R45ExecSelftestC2")
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
        swap = entry_swap_quote(snap)

        # 26 / 25-word genuine spans ending at the binary-only sentence
        ba, bb = snap.locate(QUOTES["binary"])
        w26 = snap.words_ending_at("accepted.", 26, ba - 5, bb)
        w25 = snap.words_ending_at("accepted.", 25, ba - 5, bb)
        assert len(w26.split()) == 26 and len(w25.split()) == 25
        a26, b26 = snap.locate(w26)

        # S072 real sentence (wrong source) for the borrowed-quote mutant
        s072 = open(os.path.join(a.lane, "corpus/source-snapshots/round-45/S072.txt"), encoding="utf-8").read()
        borrowed = "Welcome to the VRP rules section!"
        assert borrowed in s072

        seven_a, seven_b = snap.locate(QUOTES["seven"])
        bin_cite = cite(ba, bb)

        def m_wrong_line(root):  # quote true, citation points at an unrelated line
            sub(root, ENTRY_REL, cite(seven_a, seven_b), "`S071.txt:200`")

        def m_26w(root):
            sub(root, ENTRY_REL, "“" + QUOTES["binary"] + "” (" + bin_cite, "“" + w26 + "” (" + cite(a26, b26))

        def m_25w_control(root):
            sub(root, ENTRY_REL, "“" + QUOTES["binary"] + "” (" + bin_cite, "“" + w25 + "” (" + cite(a26, b26))

        def m_tier(root):
            sub(root, "corpus/SOURCES.md", "| docs | A |", "| docs | B |")

        def m_status(root):
            sub(root, "corpus/SOURCES.md", "| mined |", "| queued |")

        def m_usedby(root):
            sub(root, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | — |")

        def m_usedby_other(root):
            sub(root, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | corpus/knowledge/stub-01.md |")

        def m_snap_flip(root):  # flip one byte in a region no frozen quote touches (line 3)
            b = bytearray(open(os.path.join(root, SNAP_REL), "rb").read())
            i = b.index(b"Security bugs")
            b[i] ^= 0x01
            wr(root, SNAP_REL, bytes(b))

        def m_manifest_q5(root):
            m = json.loads(rd(root, MAN_REL))
            s = [x for x in m["sources"] if x["id"] == "S071"][0]
            s["quotes"] = [q for q in s["quotes"] if q["id"] != "Q5"]
            wr(root, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def m_manifest_q1_edit(root):
            sub(root, MAN_REL, "up to 7 calendar days", "up to 9 calendar days")

        def m_manifest_sha(root):
            sub(root, MAN_REL, snap.sha, "0" * 64)

        def m_manifest_absent(root):
            os.remove(os.path.join(root, MAN_REL))

        def m_recheck_absent(root):
            os.remove(os.path.join(root, "corpus/instruments/source-recheck.py"))

        def m_63(root):
            os.remove(os.path.join(root, "corpus/knowledge/stub-63.md"))

        def m_65(root):
            wr(root, "corpus/knowledge/stub-64.md", "# extra\n")

        def m_dir_md(root):  # a directory named *.md replaces a file: 63 regular files + 1 dir
            p = os.path.join(root, "corpus/knowledge/stub-63.md")
            os.remove(p)
            os.mkdir(p)

        def m_dup_f(root):  # F25 renamed F26: still 27 rows, 27 admitted, ids no longer unique
            sub(root, "corpus/README.md", "| F25 |", "| F26 |")

        def m_f27_queued(root):
            sub(root, "corpus/README.md", "| F27 | Linux kernel security-bugs reporting process | admitted |", "| F27 | Linux kernel security-bugs reporting process | queued |")

        def m_f26_queued(root):
            sub(root, "corpus/README.md", "| F26 | topic 26 | admitted |", "| F26 | topic 26 | queued |")

        def m_26_rows(root):
            sub(root, "corpus/README.md", "| F25 | topic 25 | admitted | knowledge/stub-25.md | S025 | next 25. |\n", "")

        def m_f27_entry_missing(root):
            sub(root, "corpus/README.md", "`knowledge/" + ENTRY_NAME + "`", "`knowledge/does-not-exist.md`")

        def m_no_source_line(root):
            sub(root, ENTRY_REL, "source: S071 — " + URL + "\n", "")

        def m_wrong_verified(root):
            sub(root, ENTRY_REL, "verified-at: 2026-10-28", "verified-at: 2026-10-27")

        def m_no_recheck(root):
            t = rd(root, ENTRY_REL)
            wr(root, ENTRY_REL, "\n".join(l for l in t.split("\n") if not l.startswith("recheck:")))

        def m_wrong_url(root):
            sub(root, ENTRY_REL, "source: S071 — " + URL, "source: S071 — https://example.org/security-bugs.html")

        def m_row_absent(root):
            t = rd(root, "corpus/SOURCES.md")
            wr(root, "corpus/SOURCES.md", "\n".join(l for l in t.split("\n") if not l.startswith("| S071")))

        def m_anchor_nosha(root):
            sub(root, "corpus/SOURCES.md", "sha256 " + snap.sha, "sha256 (pending)")

        def m_anchor_wrongsha(root):
            sub(root, "corpus/SOURCES.md", snap.sha, "f" * 64)

        def m_row_10cells(root):
            sub(root, "corpus/SOURCES.md", " | 180d | " + ENTRY_REL + " |", " | " + ENTRY_REL + " |")

        def m_kind_bad(root):
            sub(root, "corpus/SOURCES.md", "| docs | A |", "| bogus | A |")

        def m_dup_url_row(root):
            t = rd(root, "corpus/SOURCES.md")
            row = [l for l in t.split("\n") if l.startswith("| S071")][0]
            wr(root, "corpus/SOURCES.md", t.replace(row, row + "\n" + row.replace("| S071 |", "| S900 |", 1)))

        def m_opened_future(root):
            sub(root, "corpus/SOURCES.md", "| mined | 2026-10-28 |", "| mined | 2099-01-01 |")

        def m_usedby_dangling(root):
            sub(root, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | " + ENTRY_REL + ", corpus/knowledge/ghost.md |")

        def m_url_cell(root):
            sub(root, "corpus/SOURCES.md", "Security bugs — " + URL, "Security bugs — https://example.org/x")

        def m_opened_bad(root):
            sub(root, "corpus/SOURCES.md", "| mined | 2026-10-28 | 180d", "| mined | 2026-10-27 | 180d")

        # G5 content mutants
        m_fabricated = swap("seven", "for up to 3 calendar days from the start of the release process, with no extension at all")
        m_near_miss = swap("seven", QUOTES["seven"].replace("7 calendar", "8 calendar"))
        m_binary_fab = swap("binary", "Binary-only executables are accepted when signed.")
        m_ai_fab = swap("ai", "If you resorted to AI assistance to identify a bug, you may treat it as private")
        m_repro_fab = swap("repro", "By definition if an issue cannot be reproduced, it is still exploitable, thus it is a security bug.")

        def m_borrowed(root):
            sub(root, ENTRY_REL, "“" + QUOTES["version"] + "”", "“" + borrowed + "”")

        def m_straight_quotes(root):
            t = rd(root, ENTRY_REL)
            wr(root, ENTRY_REL, t.replace("“", '"').replace("”", '"'))

        def m_extra_bad_span(root):
            t = rd(root, ENTRY_REL)
            wr(root, ENTRY_REL, t + "\nA sixth claim reads “the kernel team answers within one hour” (`S071.txt:100`).\n")

        def m_drop_ai_span(root):
            sub(root, ENTRY_REL, "“" + QUOTES["ai"] + "” (", "(")

        def m_drop_cite(root):  # quote kept but the citation is removed: span invisible, core unlocated
            sub(root, ENTRY_REL, " (" + bin_cite + ")", "")

        def m_only_three_cores_quoted(root):  # drops 7-day AND replaces by uncitable paraphrase
            sub(root, ENTRY_REL, "“" + QUOTES["seven"] + "” (" + cite(seven_a, seven_b) + ")", "a seven day cap")

        def m_cite_before_range(root):  # window starts one line after the quote's first line
            sub(root, ENTRY_REL, cite(seven_a, seven_b), f"`S071.txt:{seven_b + 1}`")

        def m_cite_reversed_range(root):
            sub(root, ENTRY_REL, cite(ba, bb), f"`S071.txt:{ba + 40}-{ba + 39}`")

        def m_repro_cut_window(root):  # repro spans 41-43; cite only the first line
            ra, rb = snap.locate(QUOTES["repro"])
            assert rb > ra
            sub(root, ENTRY_REL, cite(ra, rb), cite(ra, ra))

        # ---- weakness probes (counter accepting is information, not failure)
        def p_wide_range(root):  # fabricated-location: whole-file range makes any real quote locate
            sub(root, ENTRY_REL, cite(seven_a, seven_b), f"`S071.txt:1-{len(snap.lines)}`")

        def p_usedby_suffix(root):  # used-by names entry path + junk suffix; G3 uses substring test
            wr(root, ENTRY_REL + ".bak", "x\n")
            sub(root, "corpus/SOURCES.md", "| 180d | " + ENTRY_REL + " |", "| 180d | " + ENTRY_REL + ".bak |")

        def p_f27_sources_wrong(root):  # F27 row cites S001, not S071; G1 never reads the sources cell
            sub(root, "corpus/README.md", "| `knowledge/" + ENTRY_NAME + "` | S071 |", "| `knowledge/" + ENTRY_NAME + "` | S001 |")

        def p_manifest_note(root):  # Q5 text moved out of quotes into a free-form S071 "note": G4 text-searches the file
            m = json.loads(rd(root, MAN_REL))
            s = [x for x in m["sources"] if x["id"] == "S071"][0]
            for q in s["quotes"]:
                if q["id"] == "Q5":
                    q["quote"] = "Linux kernel developers take security very seriously."
                    q["anchor"] = 6
            s["note"] = QUOTES["version"]
            wr(root, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def p_manifest_s072(root):  # frozen Q5 core placed on the S072 record instead of S071
            m = json.loads(rd(root, MAN_REL))
            s = [x for x in m["sources"] if x["id"] == "S071"][0]
            for q in s["quotes"]:
                if q["id"] == "Q5":
                    q["quote"] = "Linux kernel developers take security very seriously."
                    q["anchor"] = 6
            t = [x for x in m["sources"] if x["id"] == "S072"][0]
            t["note"] = QUOTES["version"]
            wr(root, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def p_stub_entry_dup(root):  # F27 cell lists a stub first then the real entry; first existing file wins
            sub(root, "corpus/README.md", "`knowledge/" + ENTRY_NAME + "`", "`knowledge/stub-01.md` `knowledge/" + ENTRY_NAME + "`")

        def p_f27_entry_in_comment_row_dup(root):  # a second table row for F27 hidden in a code fence
            t = rd(root, "corpus/README.md")
            wr(root, "corpus/README.md", t + "\n```\n| F27 | decoy | admitted | knowledge/x.md | S071 | x |\n```\n")

        # name, mutator, gates that MUST go pass=0
        MUT = [
            ("M01 fabricated 7-day quote", m_fabricated, {"G5"}),
            ("M02 quote cited at wrong line (200)", m_wrong_line, {"G5"}),
            ("M03 26-word quote", m_26w, {"G5"}),
            ("M04 tier B", m_tier, {"G3"}),
            ("M05 status queued", m_status, {"G3"}),
            ("M06 used-by missing (—)", m_usedby, {"G3"}),
            ("M07 used-by names another file", m_usedby_other, {"G3"}),
            ("M08 snapshot byte flipped", m_snap_flip, {"G3", "G4"}),
            ("M09 manifest Q5 removed", m_manifest_q5, {"G4"}),
            ("M10 manifest Q1 text edited", m_manifest_q1_edit, {"G4"}),
            ("M11 manifest sha wrong", m_manifest_sha, {"G4"}),
            ("M12 manifest absent", m_manifest_absent, {"G4"}),
            ("M13 source-recheck.py absent", m_recheck_absent, {"G4"}),
            ("M14 63 knowledge files", m_63, {"G6"}),
            ("M15 65 knowledge files", m_65, {"G6"}),
            ("M16 63 files + directory named *.md", m_dir_md, {"G6"}),
            ("M17 duplicate F id (F25->F26)", m_dup_f, {"G1"}),
            ("M18 F27 status queued", m_f27_queued, {"G1"}),
            ("M19 F26 status queued (26/27 admitted)", m_f26_queued, {"G1"}),
            ("M20 26 frontier rows", m_26_rows, {"G1"}),
            ("M21 F27 entry file missing", m_f27_entry_missing, {"G1"}),
            ("M22 entry lacks source: line", m_no_source_line, {"G2"}),
            ("M23 verified-at wrong date", m_wrong_verified, {"G2"}),
            ("M24 entry lacks recheck: line", m_no_recheck, {"G2"}),
            ("M25 source: line wrong URL", m_wrong_url, {"G2"}),
            ("M26 SOURCES row S071 absent", m_row_absent, {"G3"}),
            ("M27 anchor without sha", m_anchor_nosha, {"G3"}),
            ("M28 anchor with wrong sha", m_anchor_wrongsha, {"G3"}),
            ("M29 row has 10 cells", m_row_10cells, {"G3"}),
            ("M30 source cell wrong URL", m_url_cell, {"G3"}),
            ("M31 opened date wrong", m_opened_bad, {"G3"}),
            ("M32 kind enum violation", m_kind_bad, {"G7"}),
            ("M33 duplicate URL+scope row (E04)", m_dup_url_row, {"G7"}),
            ("M34 opened in the future (E08)", m_opened_future, {"G7"}),
            ("M35 dangling used-by path (E11)", m_usedby_dangling, {"G7"}),
            ("M36 near-miss quote (8 for 7 days)", m_near_miss, {"G5"}),
            ("M37 fabricated binary-only quote", m_binary_fab, {"G5"}),
            ("M38 fabricated AI quote (private)", m_ai_fab, {"G5"}),
            ("M39 fabricated unreproducible quote", m_repro_fab, {"G5"}),
            ("M40 quote borrowed from S072 cited as S071", m_borrowed, {"G5"}),
            ("M41 straight quotes only (no span parsed)", m_straight_quotes, {"G5"}),
            ("M42 extra fabricated sixth span", m_extra_bad_span, {"G5"}),
            ("M43 AI span citation dropped (core unlocated)", m_drop_ai_span, {"G5"}),
            ("M44 binary-only citation removed", m_drop_cite, {"G5"}),
            ("M45 7-day quote replaced by paraphrase", m_only_three_cores_quoted, {"G5"}),
            ("M46 citation one line past the quote", m_cite_before_range, {"G5"}),
            ("M47 reversed citation range", m_cite_reversed_range, {"G5"}),
            ("M48 multi-line quote cited at first line only", m_repro_cut_window, {"G5"}),
        ]
        CTRL = [
            ("C0 unmutated tree", lambda r: None),
            ("C1 no-op rewrite of README (same bytes)", lambda r: wr(r, "corpus/README.md", rd(r, "corpus/README.md"))),
            ("C2 25-word genuine span (boundary)", m_25w_control),
        ]
        PROBES = [
            ("P1 whole-file citation range 1-N on a true quote", p_wide_range),
            ("P2 used-by = entry path + '.bak' suffix", p_usedby_suffix),
            ("P3 F27 sources cell says S001 not S071", p_f27_sources_wrong),
            ("P4 Q5 core moved to free-form 'note' on S071 record", p_manifest_note),
            ("P5 Q5 core moved to free-form 'note' on S072 record", p_manifest_s072),
            ("P6 F27 entry cell lists a stub first", p_stub_entry_dup),
            ("P7 decoy F27 row inside a code fence", p_f27_entry_in_comment_row_dup),
        ]

        def materialise(i: int, mut) -> tuple[str, dict[str, int], str, str]:
            root = os.path.join(work, f"t{i:03d}")
            os.makedirs(root)
            build(root, a.lane, snap)
            mut(root)
            g, fx, out = run_counter(counter, root, tmp)
            return root, g, fx, out

        cases = failures = 0
        idx = 0
        print(f"counter={counter}")
        for name, mut in CTRL:
            idx += 1
            cases += 1
            _, g, fx, out = materialise(idx, mut)
            ok = fx == "fixed=7/7" and all(v == 1 for v in g.values()) and len(g) == 7
            failures += 0 if ok else 1
            print(f"{'ok  ' if ok else 'FAIL'} control {name}: {fx} gates={''.join(str(g.get('G'+str(n), '?')) for n in range(1, 8))}")
            if not ok:
                print("   " + out.replace("\n", "\n   "))
        for name, mut, targets in MUT:
            idx += 1
            cases += 1
            root, g, fx, out = materialise(idx, mut)
            hit = all(g.get(t, 1) == 0 for t in targets) and len(g) == 7
            fails = sorted(k for k, v in g.items() if v == 0)
            collateral = sorted(set(fails) - targets)
            failures += 0 if hit else 1
            print(f"{'ok  ' if hit else 'FAIL'} mutant {name}: target={','.join(sorted(targets))} failing={','.join(fails) or '-'} {fx}"
                  + (f" collateral={','.join(collateral)}" if collateral else ""))
            if not hit:
                print("   NOT REJECTED. counter output:\n   " + out.replace("\n", "\n   "))
        accepted = 0
        for name, mut in PROBES:
            idx += 1
            _, g, fx, out = materialise(idx, mut)
            acc = fx == "fixed=7/7"
            accepted += 1 if acc else 0
            fails = sorted(k for k, v in g.items() if v == 0)
            print(f"probe {name}: {'ACCEPTED (counter blind)' if acc else 'rejected'} failing={','.join(fails) or '-'} {fx}")
        print(f"probes accepted={accepted}/{len(PROBES)} (informational, not counted)")
        print(f"selftest cases={cases} failures={failures}")
        return 0 if failures == 0 else 1
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
