#!/usr/bin/env python3
"""r46-counters-selftest-c2.py — selftest for corpus/instruments/r46-c2-gate.py v1.3 (round 46, C2, frontier F28; wave-2 rewrite of the wave-1 v1 selftest; v1.3 adds the considerthese ledger to the counter's content-exempt set, and this selftest mirrors it).

Builds, per case, a COMPLETE synthetic C2 tree in scratch from a copy of the pure base export (--pure) that satisfies the v1.1 limbs:
  corpus/README.md            the base's frontier F01..F27 plus a live F28 row (`admitted`, third cell) -> corpus/knowledge/<entry>
  corpus/SOURCES.md           the base registry plus an S073 row under `## Registry`: tier A, kind docs, scope and teaches cells >= 8 words,
                              an anchor cell naming S073.txt, a line locator and the snapshot sha256, recheck 180d, mined, opened 2026-10-28,
                              used-by = the entry, the canonical URL first in the source cell
  corpus/knowledge/<entry>    github-private-vulnerability-reporting.md: provenance trio, the four required sections (each >= 25 words, the
                              falsifiable-rule section >= 12; the byte pad sits in the preamble so it never inflates a section), a table
                              under its own heading with 8 three-cell rows of which 7 carry a located `S073.txt:N` cite, curly spans each
                              followed by (`S073.txt:N[-M]`) with N located by SEARCH in the real capture (never hard-coded) inside body
                              lines 556-583 and spanning <= 12 lines, covering all five frozen cores, cross-references to
                              linux-kernel-security-bugs-reporting-process.md and ai-assisted-finding-validation.md, padded to 3600 bytes
  corpus/source-snapshots/round-46/{S073.txt,manifest.json}   byte copies from --lane
The base's real 64 knowledge files make the counter's REAL pins hold (no R46_PINS_OVERRIDE is set, except in the four `repin` cases, whose
per-case grader-side override file pins the manifest to its EDITED bytes so only the distinctness limb can fire). The base's three content-exempt
entries (the two C1 entries and the considerthese ledger) are the BASE bytes; `land_c1` swaps in the lane's current bytes for all three (the
exempt entries). The tree carries no source-recheck.py: the counter runs
the lane's own (its TOOL_ROOT).

Case classes (controls and mutants are counted; probes are printed, never counted):
  null     the unmodified pure base (no F28 row, no S073 row, no entry): must NOT reach 7/7 (G1-G6 fail, G7 passes)
  control  the complete tree, boundary variants, the C1-landed tree and the committed tip itself: must print `c2-gate fixed=7/7 exit=0`
  mutant   one defect; the targeted gate(s) must read pass=0, all seven gate lines must be present, and no gate outside
           target|allowed-collateral may fail. The wave-1 survivors (R46MutC2a/b/c, R46RevC2G2/G3/G5) are named in each case's note
  probe    accepted-by-design questions
`--do-nothing-control` runs every case against a stub that always prints 7/7: every mutant must then be reported as accepted (FAIL).
`--counter PATH` grades another counter (e.g. the frozen v1): the survivors then print `ACCEPTED-targeted-gate-passes`.

Usage: python3 r46-counters-selftest-c2.py [--lane DIR] [--pure DIR] [--counter PATH] [--do-nothing-control] [--keep] [-v]
READ-ONLY on --lane and --pure; scratch only under $HYAKU_SCRATCH/kasegi-r46/R46W2ExecSelftestC2/ (removed on exit unless --keep).
Prints `selftest cases=<N> failures=<F>` last; exit 0 iff F == 0.
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
PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"
URL = "https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately"
ENTRY_NAME = "github-private-vulnerability-reporting.md"
ENTRY_REL = "corpus/knowledge/" + ENTRY_NAME
SNAP_REL = "corpus/source-snapshots/round-46/S073.txt"
MAN_REL = "corpus/source-snapshots/round-46/manifest.json"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"
SECTIONS = ["## Scope and decision rule", "## Overlap and novelty", "## Limits", "## Falsifiable package rule"]
XREF_K = "corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:11-12"
XREF_A = "corpus/knowledge/ai-assisted-finding-validation.md:7-8,15"
PAD_PREFIX = "Reading note: "
ALL = {f"G{i}" for i in range(1, 8)}
C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}  # the two entries C1 re-grounds: exempt from the counter's byte pin, their names stay pinned
LEDGER = "considerthese-proposals-ledger.md"  # the considerthese ledger the round-46 attempt-2 wave appends the dispositions to: exempt from the byte pin too (name pinned, size may grow never shrink)
EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # the counter's CONTENT_EXEMPT: never use one of these as a byte-pin mutant target (their bytes are not pinned)
F28_TOPIC = "GitHub private vulnerability reporting, reporter flow: who may report, what the form requires, the credit and the private-fork limit"
F28_NEXT = "Re-open the GitHub page before relying on the form fields; maintainers can customise the form."


def norm(s: str) -> str:
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


class Snap:
    def __init__(self, lane: str):
        self.raw = open(os.path.join(lane, SNAP_REL), "rb").read()
        self.lines = self.raw.decode("utf-8").splitlines()
        self.sha = hashlib.sha256(self.raw).hexdigest()

    def locate(self, quote: str) -> tuple[int, int]:
        """Smallest 1-based line window whose normalised text holds the quote."""
        nq = norm(quote)
        for width in range(1, 6):
            for a in range(1, len(self.lines) - width + 2):
                b = a + width - 1
                if nq in norm(" ".join(self.lines[a - 1:b])):
                    return a, b
        raise SystemExit(f"selftest: quote not located in the lane capture: {quote!r}")

    def words(self, line_no: int, n: int, start_at: str = "") -> str:
        w = norm(self.lines[line_no - 1]).split()
        s = 0
        if start_at:
            s = next(i for i, x in enumerate(w) if x == start_at)
        assert len(w) >= s + n, (line_no, n, len(w) - s)
        return " ".join(w[s:s + n])


# the five frozen cores live inside these spans (each span is the manifest's own quote text)
Q = {
    "anyone": "Anyone can privately report a security vulnerability to repository maintainers.",
    "enabled": "You can only report vulnerabilities privately for repositories where this feature is enabled.",
    "initiate": "you need to initiate the reporting process by following the instructions in the security policy for the repository",
    "form": "By default, you must provide a summary, details, proof of concept, and impact statement.",
    "ai": "Optionally, select I used AI assistance to find or write up this report.",
    "credit": "GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.",
    "merge": "only the repository maintainer can merge changes from that private fork into the parent repository",
}
ROWS = [  # (key, question, consequence); keys anyone/initiate/None carry no frozen core
    ("anyone", "Who may submit a private report?", "Any reader may report where enabled."),
    ("enabled", "Is the channel always available?", "Check the feature is enabled first."),
    ("initiate", "What if the feature is off?", "Fall back to the security policy."),
    ("form", "What does the form require by default?", "Carry these four items by default."),
    ("ai", "Is AI assistance declared?", "Record the option as optional."),
    ("credit", "Who is credited and added?", "Record collaborator and credit."),
    ("merge", "Who merges a private-fork fix?", "The reporter cannot merge it."),
    (None, "Does the page set a response time?", "Record no response time."),
]
NONCORE_ROWS = ["anyone", "initiate", None]


def cite(a: int, b: int) -> str:
    return f"`S073.txt:{a}`" if a == b else f"`S073.txt:{a}-{b}`"


def fit(text: str, n: int) -> str:
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


def row_line(key, q, c, spans):
    if key is None:
        return f"| {q} | no response time is stated | {c} |"
    t, a, b = spans[key]
    return f"| {q} | “{t}” ({cite(a, b)}) | {c} |"


def entry_text(spans, size: int = 3600) -> str:
    out = [
        "# GitHub private vulnerability reporting, reporter flow (synthetic)",
        "",
        f"source: S073 — {URL} — Privately reporting a security vulnerability (S073.txt:560-579)",
        "verified-at: 2026-10-28",
        "recheck: cd " + LANE + " && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d",
        "",
        PAD_PREFIX + ".",  # the byte pad sits in the preamble, outside every required section, so a section's own words are never inflated by it
        "",
        SECTIONS[0],
        "",
        "This synthetic entry records what GitHub's own page says about reporting a security vulnerability privately to the maintainers of a public repository, from the reporter's side only (page body `S073.txt:556-579`). The table below lists each observed question with the page text and the consequence for a claim package.",
        "",
        "| observed question | page text | package consequence |",
        "|---|---|---|",
    ]
    for key, q, c in ROWS:
        out.append(row_line(key, q, c, spans))
    out += [
        "",
        SECTIONS[1],
        "",
        "Kernel intake is an e-mail route to a closed list; this page is a web form on a hosting platform. The channels differ, so a package must not mix their steps, and a reporter must not carry one project's rule over to the other.",
        "",
        f"- F27 (`{XREF_K}`) is the kernel's e-mail intake.",
        f"- F04 (`{XREF_A}`) keeps AI findings as candidates.",
        "",
        SECTIONS[2],
        "",
        "One platform's page, not a standard. Documentation only: no contact with anyone and no probing of any system took place. Maintainers can customise the form. The page body is `S073.txt:556-579`; a sweep with `grep -n -i cve S073.txt` printed nothing, so the page states no CVE handling and none is inferred here.",
        "",
        SECTIONS[3],
        "",
        "When a package describes a GitHub private report, check each stated step against the table above in order, starting from the enablement fact at `S073.txt:564`.",
        "",
    ]
    return fit("\n".join(out), size)


def sources_row(snap_sha: str) -> str:
    return ("| S073 | GitHub Docs, Privately reporting a security vulnerability — " + URL +
            " | docs | A | The reporter-side flow of GitHub private vulnerability reporting only; maintainer-side handling is outside this row | "
            "page headings Privately reporting a security vulnerability L560 and the numbered steps L567-L579; capture "
            "corpus/source-snapshots/round-46/S073.txt, sha256 " + snap_sha +
            " | Read the platform's own reporter steps before planning a private report | mined | 2026-10-28 | 180d | " + ENTRY_REL + " |")


def f28_row() -> str:
    return f"| F28 | {F28_TOPIC} | admitted | `{ENTRY_REL}` | S073 | {F28_NEXT} |"


def build(pure: str, lane: str, snap: Snap, spans, dest: str) -> None:
    shutil.copytree(pure, dest, symlinks=True)

    def rw(rel, fn):
        p = os.path.join(dest, rel)
        t = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(fn(t))

    def add_f28(t):
        ls = t.split("\n")
        i = max(k for k, ln in enumerate(ls) if re.match(r"^\| F27 \|", ln))
        return "\n".join(ls[:i + 1] + [f28_row()] + ls[i + 1:])

    def add_s073(t):
        ls = t.split("\n")
        i = max(k for k, ln in enumerate(ls) if re.match(r"^\| S0\d\d \|", ln))
        return "\n".join(ls[:i + 1] + [sources_row(snap.sha)] + ls[i + 1:])

    rw(README, add_f28)
    rw(SOURCES, add_s073)
    open(os.path.join(dest, ENTRY_REL), "w", encoding="utf-8").write(entry_text(spans))
    os.makedirs(os.path.join(dest, os.path.dirname(SNAP_REL)), exist_ok=True)
    for rel in (SNAP_REL, MAN_REL):
        shutil.copyfile(os.path.join(lane, rel), os.path.join(dest, rel))


def rd(root, rel):
    return open(os.path.join(root, rel), encoding="utf-8").read()


def wr(root, rel, data):
    if isinstance(data, bytes):
        open(os.path.join(root, rel), "wb").write(data)
    else:
        open(os.path.join(root, rel), "w", encoding="utf-8").write(data)


def sub(root, rel, old, new, count=1):
    t = rd(root, rel)
    if old not in t:
        raise SystemExit(f"selftest harness bug: {old!r} not in {rel}")
    wr(root, rel, t.replace(old, new, count))


def line_of(root, rel, prefix):
    ln = [x for x in rd(root, rel).split("\n") if x.startswith(prefix)]
    if len(ln) != 1:
        raise SystemExit(f"selftest harness bug: {prefix!r} matched {len(ln)} lines in {rel}")
    return ln[0]


def wrap_line(root, rel, prefix, before, after):
    ln = line_of(root, rel, prefix)
    sub(root, rel, ln, before + "\n" + ln + "\n" + after)


def drop_row(root, key):
    spec = next(r for r in ROWS if r[0] == key)
    ln = [x for x in rd(root, ENTRY_REL).split("\n") if x.startswith("| " + spec[1] + " |")]
    assert len(ln) == 1
    sub(root, ENTRY_REL, ln[0] + "\n", "")


class Case:
    def __init__(self, name, kind, mut=None, targets=(), allow=(), env=None, note="", direct=False, repin=False):
        self.name, self.kind, self.mut, self.direct, self.repin = name, kind, mut or (lambda r: None), direct, repin
        self.targets, self.allow, self.env, self.note = set(targets), set(allow), env or {}, note


def run_counter(counter, root, env):
    p = subprocess.run([sys.executable, counter, "--root", root], capture_output=True, text=True, timeout=900, env=env)
    out = p.stdout + p.stderr
    gates = {m.group(1): int(m.group(2)) for m in re.finditer(r"^gate (G\d) pass=([01])", out, re.M)}
    fx = re.search(r"^c2-gate fixed=(\d+)/7 exit=(\d)", out, re.M)
    return gates, (int(fx.group(1)) if fx else -1), (int(fx.group(2)) if fx else -1), out, p.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--pure", default=PURE)
    ap.add_argument("--counter", default=None)
    ap.add_argument("--do-nothing-control", action="store_true")
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()

    seat_dir = os.path.join(os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku", "kasegi-r46", "R46W2ExecSelftestC2")
    os.makedirs(seat_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2st-", dir=seat_dir)
    tmp = os.path.join(work, "tmp")
    os.makedirs(tmp)
    cases_n = failures = 0
    try:
        counter = a.counter or os.path.join(a.lane, "corpus/instruments/r46-c2-gate.py")
        if a.do_nothing_control:
            counter = os.path.join(work, "do-nothing-counter.py")
            with open(counter, "w") as fh:
                fh.write("import sys\nfor i in range(1, 8):\n    print(f'gate G{i} pass=1 read=do-nothing')\nprint('c2-gate fixed=7/7 exit=0')\n")
        base_env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/"), "TMPDIR": tmp, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}

        snap = Snap(a.lane)
        spans = {k: (t, *snap.locate(t)) for k, t in Q.items()}
        # word-limit windows taken from the real capture (line holding the "If the repository doesn't have ..." text)
        la, _ = snap.locate("If the repository doesn't have private vulnerability reporting enabled")
        w25 = snap.words(la, 25, "If")
        w26 = snap.words(la, 26, "If")
        assert len(w25.split()) == 25 and len(w26.split()) == 26
        ma, mb = spans["merge"][1], spans["merge"][2]
        over = snap.words(ma, 33, "Optionally,")  # 33-word span that contains the 'merge' core
        assert "only the repository maintainer can merge" in over and len(over.split()) == 33

        # the two knowledge files a delete/rename mutant may touch: not cross-referenced, not a SOURCES used-by, not content-exempt
        sources_txt = open(os.path.join(a.pure, SOURCES), encoding="utf-8").read()
        spare = next(n for n in sorted(os.listdir(os.path.join(a.pure, "corpus/knowledge")))
                     if n.endswith(".md") and n not in sources_txt and n not in EXEMPT_ENTRIES and n not in ("ai-assisted-finding-validation.md", "linux-kernel-security-bugs-reporting-process.md"))
        spare2 = next(n for n in sorted(os.listdir(os.path.join(a.pure, "corpus/knowledge")))
                      if n.endswith(".md") and n not in sources_txt and n not in EXEMPT_ENTRIES and n != spare and n not in ("ai-assisted-finding-validation.md", "linux-kernel-security-bugs-reporting-process.md"))

        base = os.path.join(work, "base-syn")
        build(a.pure, a.lane, snap, spans, base)
        base_entry_len = len(entry_text(spans, 3600).encode())
        assert base_entry_len == 3600
        no_pad_len = len(fit(entry_text(spans, 3600), 3600).encode())  # sanity: fit is idempotent
        assert no_pad_len == 3600

        k = lambda key: f"“{spans[key][0]}” ({cite(spans[key][1], spans[key][2])})"
        ent = lambda r: rd(r, ENTRY_REL)

        def flip_byte_at(r, needle: bytes):
            b = bytearray(open(os.path.join(r, SNAP_REL), "rb").read())
            i = b.index(needle)
            b[i] ^= 0x01
            wr(r, SNAP_REL, bytes(b))

        def man_edit(r, fn):
            m = json.loads(rd(r, MAN_REL))
            fn([x for x in m["sources"] if x["id"] == "S073"][0])
            wr(r, MAN_REL, json.dumps(m, indent=2, ensure_ascii=False))

        def refit(r, n):
            wr(r, ENTRY_REL, fit(ent(r), n))

        def add_before_limits(r, text):
            sub(r, ENTRY_REL, SECTIONS[2], text + "\n\n" + SECTIONS[2])

        SECT_FLOORS = [25, 25, 25, 12]  # words per required section (the package rule's own section is >= 12), counted as \w+ runs

        def sect_words(t, heading):
            m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", t, re.M | re.S)
            return len(re.findall(r"\w+", m.group(1))) if m else -1

        def set_section(r, i, body):
            t = ent(r)
            n = re.subn("^(" + re.escape(SECTIONS[i]) + r"[ \t]*\n)(.*?)(?=^## |\Z)", lambda m: m.group(1) + ("\n" + body + "\n\n" if body else "\n"), t, count=1, flags=re.M | re.S)
            assert n[1] == 1, "set_section harness bug"
            wr(r, ENTRY_REL, n[0])
            assert sect_words(ent(r), SECTIONS[i]) == len(re.findall(r"\w+", body)), "set_section word-count harness bug"

        def land_c1(r):  # the C1-landed tree: the lane's re-grounded entries replace the base bytes (exempt from the byte pin); the ledger is exempt too, so the lane's current ledger bytes (the attempt-2 wave appends dispositions to it) are carried here
            for fn in sorted(EXEMPT_ENTRIES):
                shutil.copyfile(os.path.join(a.lane, "corpus/knowledge", fn), os.path.join(r, "corpus/knowledge", fn))

        for fn in C1_ENTRIES:  # the control is not vacuous: the lane's bytes differ from the base's (the ledger may still be identical at this revision)
            assert open(os.path.join(a.lane, "corpus/knowledge", fn), "rb").read() != open(os.path.join(a.pure, "corpus/knowledge", fn), "rb").read(), fn
        for i, f in enumerate(SECT_FLOORS):  # the complete tree clears every floor, and clears the thinnest one by margin
            assert sect_words(rd(base, ENTRY_REL), SECTIONS[i]) >= f + 1, (SECTIONS[i], sect_words(rd(base, ENTRY_REL), SECTIONS[i]))

        C: list[Case] = []
        add = C.append

        # ------------------------------------------------------------------ null control (do-nothing tree)
        add(Case("null-pure-base-unmodified", "null", targets={"G1", "G2", "G3", "G4", "G5", "G6"}, note="no F28/S073/entry/round-46 capture"))

        # ------------------------------------------------------------------ controls (must print 7/7)
        add(Case("ctl-complete-tree", "control"))
        add(Case("ctl-25-word-span-boundary", "control", lambda r: add_before_limits(r, f"- Page text for the not-enabled case: “{w25}” ({cite(la, la)})")))
        add(Case("ctl-range-citation-577-578", "control", lambda r: sub(r, ENTRY_REL, cite(spans['credit'][1], spans['credit'][2]), "`S073.txt:%d-%d`" % (spans['credit'][1], spans['merge'][2]))))
        add(Case("ctl-six-table-rows-boundary", "control", lambda r: (drop_row(r, "anyone"), drop_row(r, None))))
        add(Case("ctl-whitespace-and-markup-in-span", "control", lambda r: sub(r, ENTRY_REL, "“By default, you must provide", "“By  **default**, you  must provide")))
        add(Case("ctl-f28-decoy-in-comment-and-fence", "control", lambda r: wr(r, README, rd(r, README) + "\n<!--\n| F28 | decoy | admitted | knowledge/stub.md | S073 | x |\n-->\n```\n| F28 | decoy | queued | knowledge/stub2.md | S073 | x |\n```\n")))
        add(Case("ctl-s073-decoy-in-comment-after-live-row", "control", lambda r: sub(r, SOURCES, "## Paths", "<!-- | S073 | decoy | docs | C | x | y | z | queued | 2026-10-28 | 180d | — | -->\n\n## Paths")))
        add(Case("ctl-trio-first-lines-plus-extra-fenced-block", "control", lambda r: add_before_limits(r, "```\nsource: S073 — decoy\n```")))
        add(Case("ctl-unrelated-env-vars-ignored", "control", env={"R46_PINS_OVERRIDE_NOT_THE_REAL_NAME": "/nonexistent", "PYTHONPATH": "/nonexistent"}))
        add(Case("ctl-tree-supplied-planted-recheck-ignored", "control", lambda r: (os.makedirs(os.path.join(r, "corpus/instruments"), exist_ok=True), wr(r, "corpus/instruments/source-recheck.py", "print('planted')\n"))))

        # ------------------------------------------------------------------ mutants
        # C2-quote gates (G5)
        add(Case("mut-fabricated-quote", "mutant", lambda r: sub(r, ENTRY_REL, "“" + Q["form"] + "”", "“By default, you must provide a signed legal waiver before submitting.”"), {"G5"}))
        add(Case("mut-quote-at-wrong-line", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:200`"), {"G5"}))
        add(Case("mut-quote-just-past-window", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), cite(spans["credit"][1] - 1, spans["credit"][1] - 1)), {"G5"}))
        add(Case("mut-26-word-quote", "mutant", lambda r: add_before_limits(r, f"- Page text for the not-enabled case: “{w26}” ({cite(la, la)})"), {"G5"}))
        add(Case("mut-core-inside-33-word-span", "mutant", lambda r: sub(r, ENTRY_REL, k("merge"), f"“{over}” ({cite(ma, ma)})"), {"G5"}))
        add(Case("mut-uncited-curly-quote", "mutant", lambda r: add_before_limits(r, "- A reporter may “submit a report” at any hour."), {"G5"}))
        add(Case("mut-citation-without-quote-marks-for-core", "mutant", lambda r: sub(r, ENTRY_REL, k("merge"), f"the maintainer alone merges ({cite(ma, mb)})"), {"G5"}))
        add(Case("mut-core-ai-removed-others-intact", "mutant", lambda r: sub(r, ENTRY_REL, k("ai"), "AI assistance is a form option"), {"G5"}))
        add(Case("mut-core-enabled-removed-others-intact", "mutant", lambda r: sub(r, ENTRY_REL, k("enabled"), "the feature must be enabled"), {"G5"}))
        add(Case("mut-quote-slightly-reworded", "mutant", lambda r: sub(r, ENTRY_REL, "“" + Q["credit"] + "”", "“GitHub automatically adds the reporter as a collaborator and as a credited user on the proposed advisory.”"), {"G5"}))
        # G3 registry row
        add(Case("mut-wrong-tier-B", "mutant", lambda r: sub(r, SOURCES, "| docs | A | The reporter-side", "| docs | B | The reporter-side"), {"G3"}, allow={"G7"}))
        add(Case("mut-status-queued", "mutant", lambda r: sub(r, SOURCES, "| mined | 2026-10-28 | 180d | " + ENTRY_REL, "| queued | 2026-10-28 | 180d | " + ENTRY_REL), {"G3"}, allow={"G7"}))
        add(Case("mut-used-by-missing-dash", "mutant", lambda r: sub(r, SOURCES, "| 180d | " + ENTRY_REL + " |", "| 180d | — |"), {"G3"}, allow={"G7"}))
        add(Case("mut-used-by-other-existing-file", "mutant", lambda r: sub(r, SOURCES, "| 180d | " + ENTRY_REL + " |", "| 180d | corpus/knowledge/" + spare + " |"), {"G3"}, allow={"G7"}))
        add(Case("mut-anchor-sha-wrong", "mutant", lambda r: sub(r, SOURCES, snap.sha, "0" * 64), {"G3"}))
        add(Case("mut-anchor-sha-missing", "mutant", lambda r: sub(r, SOURCES, ", sha256 " + snap.sha, ""), {"G3"}))
        add(Case("mut-opened-wrong-date", "mutant", lambda r: sub(r, SOURCES, "| mined | 2026-10-28 | 180d | " + ENTRY_REL, "| mined | 2026-10-27 | 180d | " + ENTRY_REL), {"G3"}, allow={"G7"}))
        add(Case("mut-source-cell-without-canonical-url", "mutant", lambda r: sub(r, SOURCES, URL, "https://docs.github.com/en/code-security"), {"G3"}, allow={"G7"}))
        add(Case("mut-s073-row-ten-cells", "mutant", lambda r: sub(r, SOURCES, " | mined | 2026-10-28 | 180d | " + ENTRY_REL + " |", " | mined | 2026-10-28 | " + ENTRY_REL + " |"), {"G3"}, allow={"G7"}))
        add(Case("mut-s073-row-in-html-comment", "mutant", lambda r: wrap_line(r, SOURCES, "| S073 |", "<!--", "-->"), {"G3"}, allow={"G7"}))
        add(Case("mut-s073-row-outside-registry", "mutant", lambda r: (lambda ln: (sub(r, SOURCES, ln + "\n", ""), sub(r, SOURCES, "## Paths", "## Paths\n\n" + ln)))(line_of(r, SOURCES, "| S073 |")), {"G3"}, allow={"G7"}))
        add(Case("mut-s073-row-duplicated", "mutant", lambda r: (lambda ln: sub(r, SOURCES, ln, ln + "\n" + ln))(line_of(r, SOURCES, "| S073 |")), {"G3"}, allow={"G7"}))
        add(Case("mut-s073-row-absent", "mutant", lambda r: sub(r, SOURCES, line_of(r, SOURCES, "| S073 |") + "\n", ""), {"G3"}, allow={"G7"}))
        # G3 + G4 capture / manifest
        add(Case("mut-snapshot-byte-flipped-nonquote", "mutant", lambda r: flip_byte_at(r, b"Manage security alerts"), {"G3", "G4"}))
        add(Case("mut-snapshot-byte-flipped-in-quote-line", "mutant", lambda r: flip_byte_at(r, b"proof of concept"), {"G3", "G4", "G5"}))
        add(Case("mut-snapshot-trailing-newline", "mutant", lambda r: wr(r, SNAP_REL, open(os.path.join(r, SNAP_REL), "rb").read() + b"\n"), {"G3", "G4"}))
        add(Case("mut-snapshot-absent", "mutant", lambda r: os.remove(os.path.join(r, SNAP_REL)), {"G3", "G4", "G5"}))
        add(Case("mut-snapshot-self-pinned-empty", "mutant", lambda r: (wr(r, SNAP_REL, b""), sub(r, SOURCES, snap.sha, hashlib.sha256(b"").hexdigest())), {"G3", "G4", "G5"}))
        add(Case("mut-snapshot-flipped-plus-planted-always-ok-recheck", "mutant", lambda r: (os.makedirs(os.path.join(r, "corpus/instruments"), exist_ok=True), wr(r, "corpus/instruments/source-recheck.py", "print('S073:sha256 OK')\nfor i in range(1, 9):\n    print(f'S073:Q{i} OK anchor=1')\n"), flip_byte_at(r, b"Manage security alerts")), {"G3", "G4"}))
        add(Case("mut-manifest-quote-removed-Q8", "mutant", lambda r: man_edit(r, lambda s: s.__setitem__("quotes", [q for q in s["quotes"] if q["id"] != "Q8"])), {"G4"}))
        add(Case("mut-manifest-quote-removed-Q6-core", "mutant", lambda r: man_edit(r, lambda s: s.__setitem__("quotes", [q for q in s["quotes"] if q["id"] != "Q6"])), {"G4"}))
        add(Case("mut-manifest-quote-text-edited", "mutant", lambda r: sub(r, MAN_REL, "proof of concept", "proof of exploit"), {"G4"}))
        add(Case("mut-manifest-sha-zeroed", "mutant", lambda r: sub(r, MAN_REL, snap.sha, "0" * 64), {"G4"}))
        add(Case("mut-manifest-trailing-newline", "mutant", lambda r: wr(r, MAN_REL, open(os.path.join(r, MAN_REL), "rb").read() + b"\n"), {"G4"}))
        add(Case("mut-manifest-absent", "mutant", lambda r: os.remove(os.path.join(r, MAN_REL)), {"G4"}))
        # G6 knowledge directory
        add(Case("mut-64-files-one-base-deleted", "mutant", lambda r: os.remove(os.path.join(r, "corpus/knowledge", spare)), {"G6"}))
        add(Case("mut-64-files-entry-deleted-and-row-kept", "mutant", lambda r: os.remove(os.path.join(r, ENTRY_REL)), {"G6"}, allow={"G1", "G2", "G3", "G5", "G7"}))
        add(Case("mut-66-files-extra-pad", "mutant", lambda r: wr(r, "corpus/knowledge/pad-extra.md", "# pad\n"), {"G6"}))
        add(Case("mut-65-files-base-swapped-for-pad", "mutant", lambda r: (os.remove(os.path.join(r, "corpus/knowledge", spare)), wr(r, "corpus/knowledge/pad-swap.md", "# pad\n")), {"G6"}))
        add(Case("mut-65-files-base-renamed", "mutant", lambda r: os.rename(os.path.join(r, "corpus/knowledge", spare2), os.path.join(r, "corpus/knowledge", spare2[:-3] + "-renamed.md")), {"G6"}))
        add(Case("mut-base-file-byte-changed", "mutant", lambda r: wr(r, "corpus/knowledge/" + spare, rd(r, "corpus/knowledge/" + spare) + " "), {"G6"}))
        # G1 frontier
        add(Case("mut-duplicate-f-id", "mutant", lambda r: sub(r, README, "| F26 |", "| F27 |"), {"G1"}))
        add(Case("mut-duplicate-f28-row", "mutant", lambda r: sub(r, README, f28_row(), f28_row() + "\n" + f28_row()), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-extra-f29-row", "mutant", lambda r: sub(r, README, f28_row(), f28_row() + "\n| F29 | extra | admitted | knowledge/x.md | S073 | n |"), {"G1"}))
        add(Case("mut-f28-row-in-html-comment-block", "mutant", lambda r: wrap_line(r, README, "| F28 |", "<!--", "-->"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-row-in-inline-html-comment", "mutant", lambda r: sub(r, README, f28_row(), "<!-- " + f28_row() + " -->"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-row-in-fenced-block", "mutant", lambda r: wrap_line(r, README, "| F28 |", "```", "```"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-row-in-tilde-fence", "mutant", lambda r: wrap_line(r, README, "| F28 |", "~~~", "~~~"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-status-queued", "mutant", lambda r: sub(r, README, "| F28 | " + F28_TOPIC + " | admitted |", "| F28 | " + F28_TOPIC + " | queued |"), {"G1"}))
        add(Case("mut-f28-status-in-fourth-cell-only", "mutant", lambda r: sub(r, README, "| F28 | " + F28_TOPIC + " | admitted | `" + ENTRY_REL + "`", "| F28 | " + F28_TOPIC + " | queued | admitted `" + ENTRY_REL + "`"), {"G1"}))
        add(Case("mut-f28-entry-file-missing", "mutant", lambda r: sub(r, README, "`" + ENTRY_REL + "`", "`corpus/knowledge/does-not-exist.md`"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-entry-shared-with-f27", "mutant", lambda r: (lambda ln: sub(r, README, ln, ln.replace("reporting-process.md` |", "reporting-process.md` knowledge/" + ENTRY_NAME + " |", 1)))(line_of(r, README, "| F27 |")), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-entry-cell-two-paths", "mutant", lambda r: sub(r, README, "`" + ENTRY_REL + "`", "`corpus/knowledge/" + spare + "` `" + ENTRY_REL + "`"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-entry-no-path", "mutant", lambda r: sub(r, README, "`" + ENTRY_REL + "`", "pending"), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-27-rows-f28-missing", "mutant", lambda r: sub(r, README, f28_row() + "\n", ""), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        add(Case("mut-f28-entry-is-symlink", "mutant", lambda r: (os.makedirs(os.path.join(r, "corpus/notes")), os.rename(os.path.join(r, ENTRY_REL), os.path.join(r, "corpus/notes/real.md")), os.symlink(os.path.join(r, "corpus/notes/real.md"), os.path.join(r, ENTRY_REL))), {"G1"}, allow={"G2", "G3", "G5", "G6"}))
        # G2 entry shape
        trio = lambda r: [x for x in ent(r).split("\n")[2:5]]
        add(Case("mut-entry-trio-only-in-fenced-block", "mutant", lambda r: sub(r, ENTRY_REL, "\n".join(trio(r)), "```\n" + "\n".join(trio(r)) + "\n```"), {"G2"}))
        add(Case("mut-entry-trio-only-in-html-comment", "mutant", lambda r: sub(r, ENTRY_REL, "\n".join(trio(r)), "<!--\n" + "\n".join(trio(r)) + "\n-->"), {"G2"}))
        add(Case("mut-entry-trio-pushed-below-line-8", "mutant", lambda r: sub(r, ENTRY_REL, "\n".join(trio(r)), "\n".join("filler line %d" % i for i in range(7)) + "\n" + "\n".join(trio(r))), {"G2"}))
        add(Case("mut-source-line-wrong-url", "mutant", lambda r: sub(r, ENTRY_REL, "source: S073 — " + URL + " — ", "source: S073 — https://docs.github.com/en/code-security — "), {"G2"}))
        add(Case("mut-source-line-wrong-source-id", "mutant", lambda r: sub(r, ENTRY_REL, "source: S073 — ", "source: S071 — "), {"G2"}))
        add(Case("mut-verified-at-wrong-date", "mutant", lambda r: sub(r, ENTRY_REL, "verified-at: 2026-10-28", "verified-at: 2026-10-27"), {"G2"}))
        add(Case("mut-recheck-line-absent", "mutant", lambda r: sub(r, ENTRY_REL, line_of(r, ENTRY_REL, "recheck: ") + "\n", ""), {"G2"}))
        add(Case("mut-recheck-line-points-at-other-source", "mutant", lambda r: sub(r, ENTRY_REL, "--source S073", "--source S071"), {"G2"}))
        add(Case("mut-recheck-line-not-source-recheck", "mutant", lambda r: sub(r, ENTRY_REL, "source-recheck.py", "true"), {"G2"}))
        for i, sct in enumerate(SECTIONS):
            add(Case(f"mut-section-{i + 1}-heading-renamed", "mutant", (lambda s: lambda r: sub(r, ENTRY_REL, s, s + " (renamed)"))(sct), {"G2"}))
        add(Case("mut-table-five-data-rows", "mutant", lambda r: [drop_row(r, kk) for kk in NONCORE_ROWS], {"G2"}))
        add(Case("mut-table-rows-with-four-cells", "mutant", lambda r: wr(r, ENTRY_REL, "\n".join((ln + " x |") if re.match(r"^\| .*\|\s*$", ln) and not ln.startswith("|---") else ln for ln in ent(r).split("\n"))), {"G2"}, allow={"G5"}))
        add(Case("mut-xref-ai-validation-missing", "mutant", lambda r: sub(r, ENTRY_REL, "corpus/knowledge/ai-assisted-finding-validation.md:7-8,15", "the AI validation entry"), {"G2"}))
        add(Case("mut-xref-kernel-entry-missing", "mutant", lambda r: sub(r, ENTRY_REL, XREF_K, "the kernel entry"), {"G2"}))
        add(Case("mut-xref-line-out-of-range", "mutant", lambda r: sub(r, ENTRY_REL, "ai-assisted-finding-validation.md:7-8,15", "ai-assisted-finding-validation.md:999"), {"G2"}))
        add(Case("mut-xref-line-zero", "mutant", lambda r: sub(r, ENTRY_REL, "ai-assisted-finding-validation.md:7-8,15", "ai-assisted-finding-validation.md:0"), {"G2"}))
        add(Case("mut-xref-to-missing-file", "mutant", lambda r: sub(r, ENTRY_REL, XREF_K, XREF_K.replace("linux-kernel-security-bugs-reporting-process", "linux-kernel-security-bugs-reporting-processs")), {"G2"}))
        # G7 census
        add(Case("mut-census-dangling-extra-used-by", "mutant", lambda r: sub(r, SOURCES, "| 180d | " + ENTRY_REL + " |", "| 180d | " + ENTRY_REL + ", corpus/knowledge/no-such-file.md |"), {"G7"}))
        add(Case("mut-census-bad-kind", "mutant", lambda r: sub(r, SOURCES, "| docs | A | The reporter-side", "| blog | A | The reporter-side"), {"G7"}, allow={"G3"}))
        add(Case("mut-census-bad-recheck", "mutant", lambda r: sub(r, SOURCES, "| mined | 2026-10-28 | 180d | " + ENTRY_REL, "| mined | 2026-10-28 | 2026-13-45 | " + ENTRY_REL), {"G7"}, allow={"G3"}))
        add(Case("mut-census-future-opened", "mutant", lambda r: sub(r, SOURCES, "| mined | 2026-10-28 | 180d | " + ENTRY_REL, "| mined | 2099-01-01 | 180d | " + ENTRY_REL), {"G7"}, allow={"G3"}))
        add(Case("mut-census-registry-missing", "mutant", lambda r: os.remove(os.path.join(r, SOURCES)), {"G7"}, allow={"G3"}))

        # ------------------------------------------------------------------ v1.1 survivors of the wave-1 falsification (each must now read red on the named gate)
        # G2: the recheck line, the section word floors, the table content
        add(Case("mut-recheck-source-S0730", "mutant", lambda r: sub(r, ENTRY_REL, "--source S073 ", "--source S0730 "), {"G2"}, note="wave-1 R46MutC2a S1: `--source S073` was a substring test"))
        add(Case("ctl-recheck-source-S073-at-end-of-line", "control", lambda r: sub(r, ENTRY_REL, " # 180d\n", "\n")))
        add(Case("mut-recheck-manifest-other-round", "mutant", lambda r: sub(r, ENTRY_REL, "round-46/manifest.json", "round-45/manifest.json"), {"G2"}))
        for i, (sct, floor) in enumerate(zip(SECTIONS, SECT_FLOORS)):
            nm = ["scope", "overlap", "limits", "falsifiable"][i]
        add(Case("mut-limits-section-emptied", "mutant", lambda r: set_section(r, 2, ""), {"G2"}, note="wave-1 R46MutC2a S3: an emptied Limits section passed on the heading alone"))
        add(Case("mut-table-six-rows-one-uncited", "mutant", lambda r: (drop_row(r, "anyone"), drop_row(r, "initiate")), {"G2"}, note="six data rows, one without a located S073.txt:N cite: five count"))

        def junk_rows(r, filler):  # five real located rows stay; the three non-core rows are swapped for junk 3-cell lines
            for kk in NONCORE_ROWS:
                drop_row(r, kk)
            sub(r, ENTRY_REL, "|---|---|---|\n", "|---|---|---|\n" + (filler + "\n") * 3)

        add(Case("mut-table-junk-dash-rows", "mutant", lambda r: junk_rows(r, "| - | - | - |"), {"G2"}, note="wave-1 R46MutC2a S2"))
        add(Case("mut-table-junk-letter-rows", "mutant", lambda r: junk_rows(r, "| a | b | c |"), {"G2"}))

        def junk_table(r):  # six junk 3-cell rows stand in for the table; the real quotes move to cited bullets
            t = ent(r)
            for key, q, c2 in ROWS:
                t = t.replace(row_line(key, q, c2, spans) + "\n", "")
            t = t.replace("|---|---|---|\n", "|---|---|---|\n" + "| - | - | - |\n" * 6 + "\n" + "".join("- " + k(kk) + "\n" for kk in Q) + "- no response time\n")
            assert t.count("| - | - | - |") == 6 and "Who may submit" not in t, "junk_table harness bug"
            wr(r, ENTRY_REL, t)

        add(Case("mut-table-six-junk-rows-quotes-in-bullets", "mutant", junk_table, {"G2"}))
        add(Case("mut-table-rows-without-numeric-cite", "mutant", lambda r: wr(r, ENTRY_REL, "\n".join(re.sub(r"\(`S073\.txt:[\d-]+`\)", "(`S073.txt`)", ln) if ln.startswith("| ") else ln for ln in ent(r).split("\n"))), {"G2", "G5"}, note="a row counts only with a located S073.txt:N cite; the curly quotes also lose their cites (G5)"))
        # G3: the registry row content and the registry scope
        add(Case("mut-row-scope-seven-words", "mutant", lambda r: sub(r, SOURCES, "The reporter-side flow of GitHub private vulnerability reporting only; maintainer-side handling is outside this row", "reporter flow only, nothing else here"), {"G3"}, allow={"G7"}))
        add(Case("mut-row-teaches-seven-words", "mutant", lambda r: sub(r, SOURCES, "Read the platform's own reporter steps before planning a private report", "Read the reporter steps first"), {"G3"}, allow={"G7"}))
        add(Case("mut-row-anchor-without-locator", "mutant", lambda r: sub(r, SOURCES, "page headings Privately reporting a security vulnerability L560 and the numbered steps L567-L579; ", "the whole page; "), {"G3"}, allow={"G7"}))
        add(Case("mut-row-recheck-cell-filler", "mutant", lambda r: sub(r, SOURCES, "| mined | 2026-10-28 | 180d | " + ENTRY_REL, "| mined | 2026-10-28 | soon | " + ENTRY_REL), {"G3"}, allow={"G7"}))
        add(Case("mut-row-url-wrapped-in-other-host", "mutant", lambda r: sub(r, SOURCES, "— " + URL + " |", "— https://redirect.example.invalid/?u=" + URL + " |"), {"G3"}, allow={"G7"}, note="wave-1 R46MutC2a S4: the canonical URL only had to occur somewhere in the cell"))
        add(Case("ctl-row-second-url-after-canonical", "control", lambda r: sub(r, SOURCES, URL + " | docs |", URL + " (legacy: https://docs.github.com/en/code-security/old-path) | docs |")))
        add(Case("mut-row-filler-cells", "mutant", lambda r: wr(r, SOURCES, rd(r, SOURCES).replace(line_of(r, SOURCES, "| S073 |"), "| S073 | - | - | A | - | - | - | mined | 2026-10-28 | 180d | " + ENTRY_REL + " |")), {"G3"}, allow={"G7"}))
        add(Case("mut-row-after-sub-heading-in-registry", "mutant", lambda r: wrap_line(r, SOURCES, "| S073 |", "### Appendix", ""), {"G3"}, allow={"G7"}, note="a heading resets the registry reading: the row is no longer in `## Registry`"))
        # G4: the manifest's quote texts (the real pin makes any edit red; the repinned cases isolate the distinctness limb)
        add(Case("mut-manifest-duplicate-quote-real-pin", "mutant", lambda r: man_edit(r, lambda s: s["quotes"].append(dict(s["quotes"][-1], id="Q9"))), {"G4"}))
        add(Case("ctl-manifest-reserialised-repinned", "control", lambda r: man_edit(r, lambda s: None), repin=True, note="grader-side override re-pins the re-serialised manifest, nothing else edited: isolates the distinctness limb from the pin"))
        add(Case("mut-manifest-duplicate-quote-repinned", "mutant", lambda r: man_edit(r, lambda s: s["quotes"].append(dict(s["quotes"][-1], id="Q9"))), {"G4"}, repin=True, note="wave-1 R46MutC2b P4: the distinctness limb alone"))
        add(Case("ctl-manifest-seven-distinct-anchors-repinned", "control", lambda r: man_edit(r, lambda s: s["quotes"][1].update(quote="Anyone can privately report a security vulnerability", anchor=560)), repin=True, note="distinct texts, 7 distinct anchors: the boundary of the anchor limb; source-recheck still reads every quote OK"))
        add(Case("mut-manifest-six-distinct-anchors-repinned", "mutant", lambda r: man_edit(r, lambda s: (s["quotes"][1].update(quote="Anyone can privately report a security vulnerability", anchor=560), s["quotes"][3].update(quote="to repository maintainers", anchor=560))), {"G4"}, repin=True, note="distinct texts, 6 distinct anchors < 7; every quote still reads OK in source-recheck (a bare anchor edit would be BROKEN there, which would not isolate the limb)"))
        # G5: the cited window
        add(Case("mut-citation-1-589-real-quote", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:1-589`"), {"G5"}, note="wave-1 R46MutC2b M07: a whole-file window hid a wrong location"))
        add(Case("mut-citation-line-0", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:0`"), {"G5"}))
        add(Case("mut-citation-range-0-577", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:0-577`"), {"G5"}))
        add(Case("ctl-citation-12-lines", "control", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:566-577`")))
        add(Case("mut-citation-13-lines", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:565-577`"), {"G5"}))
        add(Case("ctl-citation-starts-at-body-line-556", "control", lambda r: sub(r, ENTRY_REL, cite(spans["anyone"][1], spans["anyone"][2]), "`S073.txt:556-560`")))
        add(Case("mut-citation-starts-at-555", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["anyone"][1], spans["anyone"][2]), "`S073.txt:555-560`"), {"G5"}))
        add(Case("ctl-citation-ends-at-body-line-583", "control", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:577-583`")))
        add(Case("mut-citation-ends-at-584", "mutant", lambda r: sub(r, ENTRY_REL, cite(spans["credit"][1], spans["credit"][2]), "`S073.txt:577-584`"), {"G5"}))
        add(Case("mut-core-quote-from-page-chrome-line", "mutant", lambda r: sub(r, ENTRY_REL, k("merge"), "“Collaborate in a fork” (`S073.txt:%d`)" % snap.locate("Collaborate in a fork")[0]), {"G5"}, note="a located quote from site navigation outside lines 556-583 is not support"))
        add(Case("mut-core-row-in-html-comment", "mutant", lambda r: wrap_line(r, ENTRY_REL, "| " + ROWS[4][1] + " |", "<!--", "-->"), {"G5"}, note="a core that exists only inside a comment is not live"))
        add(Case("mut-core-row-in-fenced-block", "mutant", lambda r: wrap_line(r, ENTRY_REL, "| " + ROWS[4][1] + " |", "```", "```"), {"G5"}))
        add(Case("mut-ascii-quoted-fabrication-cited", "mutant", lambda r: add_before_limits(r, '- The page says "GitHub guarantees a response within 24 hours" (`S073.txt:577`).'), {"G5"}))
        add(Case("mut-ascii-quoted-fabrication-uncited", "mutant", lambda r: add_before_limits(r, '- The page says "GitHub guarantees a response within 24 hours".'), {"G5"}, note="wave-1 R46MutC2b P1/P2: ASCII quotes were invisible"))
        add(Case("mut-ascii-quoted-real-quote-wide-cite", "mutant", lambda r: sub(r, ENTRY_REL, k("merge"), '"%s" (`S073.txt:1-589`)' % Q["merge"]), {"G5"}))
        # G6: the knowledge directory holds exactly the 65 entries; C1's two re-grounded entries are exempt from the byte pin only
        add(Case("mut-non-md-file-in-knowledge", "mutant", lambda r: wr(r, "corpus/knowledge/stray.txt", "x\n"), {"G6"}, note="wave-1 R46MutC2c S1"))
        add(Case("mut-hidden-file-in-knowledge", "mutant", lambda r: wr(r, "corpus/knowledge/.keep", ""), {"G6"}))
        add(Case("mut-nested-md-in-knowledge-subdir", "mutant", lambda r: (os.makedirs(os.path.join(r, "corpus/knowledge/sub")), wr(r, "corpus/knowledge/sub/extra.md", "# x\n")), {"G6"}, note="wave-1 R46MutC2c S2"))
        add(Case("ctl-c1-landed-two-entries", "control", land_c1))
        add(Case("mut-c1-landed-exempt-entry-renamed", "mutant", lambda r: (land_c1(r), os.rename(os.path.join(r, "corpus/knowledge/claim-gates.md"), os.path.join(r, "corpus/knowledge/claim-gates-renamed.md"))), {"G6"}, note="the exemption is from the byte pin only: the NAME stays pinned"))
        add(Case("mut-c1-landed-exempt-entry-deleted", "mutant", lambda r: (land_c1(r), os.remove(os.path.join(r, "corpus/knowledge/claim-package-contract.md"))), {"G6"}))
        add(Case("mut-c1-landed-plus-third-entry-changed", "mutant", lambda r: (land_c1(r), wr(r, "corpus/knowledge/" + spare, rd(r, "corpus/knowledge/" + spare) + " ")), {"G6"}))
        add(Case("ctl-committed-tip-direct", "control", direct=True, note="the counter run on --lane itself (the committed tip export): must read 7/7"))

        # ------------------------------------------------------------------ probes (accepted-by-design questions; printed, not counted)
        P: list[Case] = []
        P.append(Case("probe-fabricated-quote-in-fenced-block", "probe", lambda r: add_before_limits(r, "```\n“GitHub guarantees a response within 24 hours” (`S073.txt:577`)\n```"), note="a fenced block is code, not a quotation: v1.1 reads live lines only, so a fenced fabrication is not graded"))
        P.append(Case("probe-single-curly-quotes-uncited", "probe", lambda r: add_before_limits(r, "- A reporter may ‘submit a report’ at any hour."), note="‘single’ curly quotes are not counted as curly spans"))
        P.append(Case("probe-fabricated-prose-no-quote-marks", "probe", lambda r: add_before_limits(r, "- GitHub guarantees maintainers respond within 24 hours (S073.txt:577)."), note="an unquoted false claim is invisible to G5"))
        P.append(Case("probe-fabricated-curly-quote-in-html-comment", "probe", lambda r: add_before_limits(r, "<!-- “GitHub guarantees a response within 24 hours” (`S073.txt:577`) -->"), note="a comment is not rendered; the counter reads live lines only, so a hidden fabrication is not graded"))
        P.append(Case("probe-unclosed-html-comment-before-f28-row", "probe", lambda r: sub(r, README, f28_row(), "<!--\n" + f28_row()), note="renderer hides the row; counter keeps it live"))
        P.append(Case("probe-four-tick-fence-with-inner-three-tick-line", "probe", lambda r: sub(r, README, f28_row(), "````\n```\n" + f28_row() + "\n````"), note="renderer treats the row as fenced code; counter closes the fence early"))
        P.append(Case("probe-entry-pad-is-garbage-bytes", "probe", lambda r: refit(r, 9000), note="G6 floor is bytes, not content"))

        def run_case(c: Case):
            env = dict(base_env)
            env.update(c.env)
            if c.direct:  # the committed tip itself (--lane), graded read-only: the counter never writes under --root
                return run_counter(counter, a.lane, env)
            dest = os.path.join(work, "case")
            if os.path.exists(dest):
                shutil.rmtree(dest)
            if c.kind == "null":
                shutil.copytree(a.pure, dest, symlinks=True)
            else:
                shutil.copytree(base, dest, symlinks=True)
                c.mut(dest)
            if c.repin:  # grader-side override file (never the graded tree's): pin the manifest to the EDITED bytes so only the distinctness limb can fire
                pf = os.path.join(work, "pins-repin.json")
                with open(pf, "w") as fh:
                    json.dump({"manifest.json": hashlib.sha256(open(os.path.join(dest, MAN_REL), "rb").read()).hexdigest()}, fh)
                env["R46_PINS_OVERRIDE"] = pf
            return run_counter(counter, dest, env)

        for c in C:
            cases_n += 1
            gates, fixed, ex, out, rc = run_case(c)
            failing = {g for g, v in gates.items() if v == 0}
            complete = set(gates) == ALL
            reasons = []
            if not complete:
                reasons.append(f"gate-lines-missing={sorted(ALL - set(gates))}")
            if c.kind == "control":
                if not (fixed == 7 and ex == 0 and rc == 0 and not failing):
                    reasons.append(f"control-not-7/7 failing={sorted(failing)}")
            elif c.kind == "null":
                if failing != c.targets:
                    reasons.append(f"null-tree failing={sorted(failing)} expected={sorted(c.targets)}")
                if fixed == 7:
                    reasons.append("null tree read 7/7")
            else:
                miss = c.targets - failing
                extra = failing - c.targets - c.allow
                if miss:
                    reasons.append(f"ACCEPTED-targeted-gate-passes={sorted(miss)}")
                if extra:
                    reasons.append(f"collateral-unexpected={sorted(extra)}")
                if fixed == 7:
                    reasons.append("tree read 7/7")
            ok = not reasons
            failures += 0 if ok else 1
            print(f"{'ok  ' if ok else 'FAIL'} {c.kind:7s} {c.name} fixed={fixed}/7 failing={sorted(failing)}" + ("" if ok else "  <- " + "; ".join(reasons)))
            if (not ok or a.v) and out:
                for ln in out.splitlines():
                    if ln.startswith("gate ") and (a.v or int(ln.split("pass=")[1][0]) == 0):
                        print("       " + ln)
        for c in P:
            gates, fixed, ex, out, rc = run_case(c)
            failing = sorted(g for g, v in gates.items() if v == 0)
            print(f"probe       {c.name} fixed={fixed}/7 failing={failing} ({'rejected' if failing else 'ACCEPTED'}) -- {c.note}")
    finally:
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
            try:
                os.rmdir(seat_dir)
            except OSError:
                pass
        else:
            print(f"scratch kept: {work}")
    print(f"selftest cases={cases_n} failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
