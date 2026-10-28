#!/usr/bin/env python3
"""r44-routed-defects.py — round-44 C1 counter over committed lane evidence (v2).

WHAT IT MEASURES
    The eight routed defects listed in
    `corpus/lessons/round-43-verifier-spotcheck.md` §6 ("Routed defects — the
    lane must fix these in round 44").  Each defect is one limb; a limb is
    `fixed` only when the *substantive* evidence for its repair is present in
    the tree under `--root`.  The counter is READ-ONLY over the tree it grades:
    it never writes into `--root`, never runs git, and never mutates the lane.

WHY IT IS NOT A MARKER COUNTER
    A limb passes only when it can point at a committed artifact that carries
    the measured content, not merely at a sentence that says the defect was
    fixed.  Every limb therefore binds at least one *file that must exist* and
    *content that must be inside it*; the `--selftest` mutants delete or blank
    exactly those artifacts (leaving the prose marker in place) and require the
    limb to report `unresolved`.  The round-43 seat review rejected an earlier
    draft of this counter for accepting a marker-only tree
    (`.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`).

VERSION 2 — hardened by the round-44 falsify wave
    The v1 instrument (digest `7e7c145f831a04d4b094ce6fda228587368c2aee04baadbb8345404a8baca950`,
    graded by the wave-2 seats) was falsified on four classes of false green,
    each reproduced in a seat report under `.ufo/waves/round-44/wave2/`:

    R44W2Exec05  a tree that fabricates every bound artifact (erratum, registry,
                 emitter stub, sidecar, receipt, results file) grades 8/8 fixed;
    R44W2Rev09   presence-only predicates accept denials (D4), filename mentions
                 instead of registry rows (D7), a nonfunctional emitter (D5), a
                 token-only receipt (D8), and a rewritten row that keeps its
                 token (D1); D3's history check is satisfied by its own
                 correction; D2 never checks that K17's escape can match the
                 erratum;
    R44W2Rev02 / the K17-escape mechanism claim was wrong in substance: K17
    R44W2Revenger01  skips after-cells, so its escape never fires for the
                 `closed=13/19` token (an after-cell token of the round-43
                 claims.json); K18 covers the token from the spot-check's own
                 text, and neither check was widened;
    R44W2Rev09   the round-44 export-ref sidecar contradicted the paired run
                 receipt (`ab98fac9` vs `de09313…`) and D5 accepted it.

    v2 answers each: the stable artifacts are PINNED by sha256 (a fabricated
    tree must reproduce the genuine bytes, i.e. do the work), the emitter must
    carry its refusal logic and the registry names must EQUAL the committed
    results file's seat names, the sidecar's export-ref must EQUAL the paired
    run receipt's export-ref, D4 requires the affirmative `planner=L1` token and
    rejects denials, D7 requires line-anchored README rows and the preserved
    original SHONEN bullet, D3 requires both original occurrences and orders the
    correction after them, and D2 states the true mechanism (K17 skips
    after-cells; K18 covers the token from the spot-check text; nothing was
    widened) while applying K17's own same-paragraph predicate shape to the
    erratum.  The frozen predicate (eight routed defects, 0 unresolved) and the
    frozen target are unchanged; the frozen counter string in
    `.ufo/waves/round-44/claims.json` is untouched.

USAGE
    python3 corpus/instruments/r44-routed-defects.py --root TREE [--baseline TREE]
    python3 corpus/instruments/r44-routed-defects.py --root TREE --selftest [--work DIR]

    --root      tree to grade (an exported lane tree, or the lane checkout).
    --baseline  optional frozen baseline export; printed as a second tally and
                used for the cross-checks that need two trees.
    --selftest  build the mutant battery under --work and grade it.
    --work      scratch root for --selftest; defaults to $TMPDIR.

OUTPUT
    one `R44-D<n> status=fixed|unresolved detail=…` line per limb, then
    `routed-defects total=8 fixed=<k> unresolved=<n> exit=0|1`
    (exit 0 only when unresolved=0).

    The selftest prints one `selftest case=<id> verdict=pass|fail` line per
    case and `selftest cases=<n> failures=<k>`.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

TOTAL = 8

# --------------------------------------------------------------------------
# committed-tree pins (sha256 of the artifact bytes this round measured).
# A tree whose pinned artifact differs is NOT the tree the round measured:
# the limb reports unresolved rather than guessing.
# --------------------------------------------------------------------------

PINS = {
    ".ufo/waves/round-43/claims-erratum-6.md":
        "2e3b9f3464bb1112e9a344a82b378e7641201bd75fd55c30a622a4da26f40924",
    "corpus/lessons/round-43.md":
        "1bc47771f2966a168042409920effe085885484a9274bba7ac6c81aa0444b470",
    ".ufo/waves/round-44/controls/missing-suite-base.txt":
        "57b1346aa1c78321e40da2811fb1313197408ebcd165bb4c8c93b4cba6392fef",
    ".ufo/waves/round-44/wave-registry.txt":
        "4c1d8802aa5bc80a77cfbf4903ff907f0b3da346f2809b0acd40e4a8df2fbaa7",
    ".ufo/waves/round-43/final-gates/r42-at-de09313-selftest.export-ref.md":
        "25f20ee910a488c900416df777a5baf6521bbad750346c15b82937d015ac5b01",
    "corpus/instruments/r43-limbs/k17-claims-before.sh":
        "37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348",
    ".ufo/waves/round-44/controls/round43-registry-names.txt":
        "40af54779d6ae145490bd2b020d707854e6e326748bac8d99d5639d7c4b389a7",
    ".ufo/waves/round-44/wave1-results.json":
        "66c76ccb3422947eec14d661fc16981734ce985595697ce54891ce0d35955c77",
}

# --------------------------------------------------------------------------
# tree views
# --------------------------------------------------------------------------


class Tree:
    """Read-only view of a directory tree."""

    def __init__(self, root: str) -> None:
        self.root = os.path.abspath(root)

    def path(self, rel: str) -> str:
        return os.path.join(self.root, rel)

    def exists(self, rel: str) -> bool:
        return os.path.isfile(self.path(rel))

    def read(self, rel: str) -> str | None:
        try:
            with open(self.path(rel), "r", encoding="utf-8", errors="replace") as fh:
                return fh.read()
        except OSError:
            return None

    def bytes(self, rel: str) -> bytes | None:
        try:
            with open(self.path(rel), "rb") as fh:
                return fh.read()
        except OSError:
            return None

    def digest(self, rel: str) -> str | None:
        data = self.bytes(rel)
        return None if data is None else hashlib.sha256(data).hexdigest()

    def pinned(self, rel: str) -> tuple[bool, str]:
        """True when `rel` exists AND its bytes equal the committed pin."""
        if rel not in PINS:
            return True, "unpinned"
        if not self.exists(rel):
            return False, f"{rel} absent"
        got = self.digest(rel)
        if got != PINS[rel]:
            return False, f"{rel} digest mismatch ({(got or 'none')[:12]}…) — not the measured bytes"
        return True, f"{rel} matches the pinned digest"


class Overlay(Tree):
    """A tree with in-memory edits: `changes` maps relpath -> new text or None (deleted)."""

    def __init__(self, base: Tree, changes: dict[str, str | None]) -> None:
        super().__init__(base.root)
        self.base = base
        self.changes = changes

    def exists(self, rel: str) -> bool:
        if rel in self.changes:
            return self.changes[rel] is not None
        return self.base.exists(rel)

    def read(self, rel: str) -> str | None:
        if rel in self.changes:
            return self.changes[rel]
        return self.base.read(rel)

    def bytes(self, rel: str) -> bytes | None:
        if rel in self.changes:
            data = self.changes[rel]
            return None if data is None else data.encode("utf-8")
        return self.base.bytes(rel)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def paragraphs(text: str) -> list[str]:
    """Split text into blank-line separated blocks."""
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def para_containing(text: str, *needles: str) -> str | None:
    for para in paragraphs(text):
        if all(n in para for n in needles):
            return para
    return None


def results_names(tree: Tree, wave: str = "wave1") -> list[str] | None:
    """The seat names recorded in a wave results file, in file order."""
    raw = tree.read(f".ufo/waves/round-44/{wave}-results.json")
    if raw is None:
        return None
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return None
    results = doc.get("results")
    if not isinstance(results, list):
        return None
    names = [str(e.get("name")) for e in results if isinstance(e, dict) and e.get("name")]
    return names or None


# --------------------------------------------------------------------------
# the eight limbs
# --------------------------------------------------------------------------

SCORECARD = "SCORECARD.md"
LESSON43 = "corpus/lessons/round-43.md"
LESSON44 = "corpus/lessons/round-44.md"
LOG = "LOG.md"
SHONEN = "SHONEN.md"
ERRATUM = ".ufo/waves/round-43/claims-erratum-6.md"
K17 = "corpus/instruments/r43-limbs/k17-claims-before.sh"
INSTRUMENTS_README = "corpus/instruments/README.md"
TMP_LEFTOVER = ".ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp"
RUN_RECEIPT = ".ufo/waves/round-43/final-gates/r42-at-de09313-run.txt"
EXPORT_REF_SIDECAR = ".ufo/waves/round-43/final-gates/r42-at-de09313-selftest.export-ref.md"
EMITTER = "corpus/instruments/wave-registry.py"
REGISTRY = ".ufo/waves/round-44/wave-registry.txt"
STALE_NOTE = ".ufo/waves/round-44/controls/round43-registry-names.txt"
RECEIPT_127 = ".ufo/waves/round-44/controls/missing-suite-base.txt"

FIX_POINTER = "c6ae07c6a541e0e96d0040afb6"
FIX_POINTER_FULL = "c6ae07c6a541e0e96d0040afb62b45dd37711300"
COUNT_COMMAND = "printf %s c6ae07c6a541e0e96d0040afb6 | wc -c"
ROW_PIN = "base `ab98fac9` `closed=13/19 exit=1` with exactly K14-K19 open"
BULLET_PIN = "no seat owns a SKILL.md edit this round"


def limb_d1(tree: Tree) -> tuple[bool, str]:
    """§6.1 — the `closed=13/19` literal was unbacked; a correction must supersede it.

    Fixed iff the round-43 move-log row keeps its measured bytes (the pinned
    cell), an appended `Correction (round 43` paragraph names the literal,
    says it is superseded, cites the erratum and states the supported base
    evidence, sits AFTER the row, and the erratum file is present with its
    pinned bytes.
    """
    ok, why = tree.pinned(ERRATUM)
    if not ok:
        return False, why
    scorecard = tree.read(SCORECARD)
    if scorecard is None:
        return False, "SCORECARD.md absent"
    row = None
    for line in scorecard.splitlines():
        if line.startswith("| 43 | depth:verifiability"):
            row = line
            break
    if row is None:
        return False, "round-43 move-log row absent"
    if ROW_PIN not in row:
        return False, "the round-43 row's measured cell was rewritten (append-only violated)"
    idx = scorecard.find(row)
    corr = None
    for para in paragraphs(scorecard):
        if (
            para.startswith("Correction (round 43")
            and "13/19" in para
            and "superseded" in para
            and "claims-erratum-6.md" in para
            and ("No committed run" in para or "draft/stub" in para)
        ):
            corr = para
            break
    if corr is None:
        return False, "no appended correction naming 13/19 + superseded + erratum + the supported base evidence"
    if scorecard.find(corr) <= idx:
        return False, "correction does not sit after the round-43 row (append-only violated)"
    erratum = tree.read(ERRATUM) or ""
    para = para_containing(erratum, "13/19")
    if para is None or "supersed" not in para.lower():
        return False, "the erratum has no paragraph carrying the literal with the superseded vocabulary"
    return True, "row cell pinned; correction appended after the row; erratum digest matches the round's bytes"


def limb_d2(tree: Tree) -> tuple[bool, str]:
    """§6.2 — no check could see defect 1; the superseded literal becomes visible.

    The true mechanism, as established by the falsify wave (R44W2Rev02,
    R44W2Revenger01): the `closed=13/19` token sits in the round-43 claims.json
    AFTER-cell, which K17 never grades (K17 skips after-cells), so K17's
    `claims-erratum*` escape covers a BEFORE-cell occurrence only; K18 treats
    the token as superseded from the spot-check's own prescription; nothing was
    widened.  The check that sees the literal is THIS counter's D2 limb, which
    applies K17's own same-paragraph predicate shape to the erratum.

    Fixed iff K17 still carries its escape with its pinned bytes, a
    `claims-erratum*.md` file matching the glob sits in the round-43 wave dir,
    one of its paragraphs carries the literal with the superseded vocabulary
    (K17's same-paragraph shape), and the round-44 lesson states the mechanism
    including the after-cell fact.
    """
    ok, why = tree.pinned(K17)
    if not ok:
        return False, why
    ok, why = tree.pinned(ERRATUM)
    if not ok:
        return False, why
    k17 = tree.read(K17) or ""
    globs = [g.strip("`.,") for g in re.findall(r"claims-erratum[^\s\"')]*", k17)]
    wildcards = [g for g in globs if "*" in g]
    wave_dir = os.path.dirname(ERRATUM)
    d = os.path.join(tree.root, wave_dir)
    names = sorted(os.listdir(d)) if os.path.isdir(d) else []
    hit = None
    for name in names:
        if not re.fullmatch(r"claims-erratum.*\.md", name):
            continue
        # K17's escape must be a WILDCARD pattern that can match this file — a
        # glob frozen to an earlier round's specific erratum number does not
        # cover a new erratum (R44W2Rev09's dead-escape reproducer).
        if wildcards and not any(fnmatch.fnmatch(name, g) or fnmatch.fnmatch(name, g + "*") for g in wildcards):
            continue
        body = tree.read(wave_dir + "/" + name) or ""
        for para in paragraphs(body):
            if "13/19" in para and re.search(r"supersed", para, re.I):
                hit = (wave_dir + "/" + name, para)
                break
        if hit:
            break
    if hit is None:
        return False, "no claims-erratum*.md paragraph carries the literal with the superseded vocabulary"
    lesson = tree.read(LESSON44) or ""
    for token in ("K17", "after-cell", "K18"):
        if token not in lesson:
            return False, f"the round-44 lesson does not state the mechanism ({token} missing)"
    return True, f"{hit[0]} matched and same-paragraph graded; the lesson names the K17/after-cell/K18 mechanism"


def limb_d3(tree: Tree) -> tuple[bool, str]:
    """§6.3 — the lesson numeral was wrong (29 characters); the fix pointer is 26.

    Fixed iff the lesson's bytes equal the round's pinned digest (so neither the
    two original sentences nor the correction can be rewritten), the correction
    names the pointer, the full hash and the counting command, states 26
    characters and 40 for the full hash, and sits AFTER the original
    occurrences.
    """
    ok, why = tree.pinned(LESSON43)
    if not ok:
        return False, why
    lesson = tree.read(LESSON43) or ""
    corr = para_containing(
        lesson,
        "Correction (round 43",
        FIX_POINTER,
        FIX_POINTER_FULL,
        COUNT_COMMAND,
    )
    if corr is None:
        return False, "no appended correction naming the pointer, the full hash and the counting command"
    # the ORIGINAL occurrences, before the correction; the correction's own
    # quotation of the wrong numeral does not count as an original.
    corr_at = lesson.find(corr)
    occurrences = [m.start() for m in re.finditer(re.escape("29-character prefix"), lesson) if m.start() < corr_at]
    if len(occurrences) < 2:
        return False, "the two original 29-character sentences are not both present before the correction (append-only violated)"
    if not re.search(r"\b26\b[ -]characters", corr):
        return False, "the correction does not state 26 characters"
    if not re.search(r"\b40\b[ -]character", corr):
        return False, "the correction does not state the 40-character full hash"
    if corr_at < occurrences[-1]:
        return False, "the correction does not sit after the original occurrences"
    if len(FIX_POINTER) != 26:
        return False, "internal inconsistency: the pointer is not 26 characters"
    return True, "lesson digest pinned; correction appended after both originals with the counting command"


def limb_d4(tree: Tree) -> tuple[bool, str]:
    """§6.4 — the round report omitted the planner=L1 mapping and the L2-floor line.

    The report itself is filed on the fleet repo after the lane lands, so the
    lane's committed record of the same two facts is `LOG.md`'s round-44
    section; the report carries them too (the closure reads it there).  Fixed
    iff the section records the AFFIRMATIVE `planner=L1` token (denials do not
    count), the L2-floor line, the residual-call line, and a wave-1 seat count
    that equals BOTH the committed results file's seat count and its named-seat
    list length.
    """
    ok, why = tree.pinned(".ufo/waves/round-44/wave1-results.json")
    if not ok:
        return False, why
    log = tree.read(LOG)
    if log is None:
        return False, "LOG.md absent"
    head = log.rfind("## Round 44")
    if head < 0:
        return False, "LOG.md has no round-44 section"
    section = log[head:]
    if not re.search(r"planner=L1", section):
        return False, "the round-44 LOG section does not record the affirmative planner=L1 mapping"
    if re.search(r"planner=L1[^\n]{0,40}\b(not|never|isn.t|was not)\b", section, re.I):
        return False, "the planner=L1 token appears inside a denial"
    if "L2 floor" not in section:
        return False, "the round-44 LOG section does not record the L2-floor line"
    if "residual call" not in section.lower():
        return False, "the round-44 LOG section does not record the residual-call line"
    m = re.search(r"wave 1 seats[:=]\s*(\d+)", section)
    if m is None:
        return False, "the round-44 LOG section does not state the wave-1 seat count"
    claimed = int(m.group(1))
    names = results_names(tree, "wave1")
    if names is None:
        return False, "wave1-results.json carries no named results; the seat count cannot be cross-checked"
    if claimed != len(names):
        return False, f"the LOG claims {claimed} wave-1 seats; the committed results file names {len(names)}"
    return True, f"planner=L1 (affirmative), L2-floor and residual lines recorded; {claimed} seats cross-check against the pinned results file"


def limb_d5(tree: Tree) -> tuple[bool, str]:
    """§6.5 — wave-evidence hygiene: leftover, emitter, registry, export-ref sidecar.

    Fixed iff the aborted-write leftover is absent; the emitter carries its
    refusal logic (`seats != len(names)`); a committed registry's `names=` list
    EQUALS the committed results file's seat names and the stale round-43
    registry is recorded as superseded; and the export-ref sidecar's
    `export-ref` EQUALS the paired run receipt's `export-ref` (the v1 sidecar
    carried the wrong export and was corrected after the falsify wave caught
    it).  The registry, sidecar and stale-registry note are digest-pinned.
    """
    if tree.exists(TMP_LEFTOVER):
        return False, f"aborted-write leftover {TMP_LEFTOVER} is present"
    emitter = tree.read(EMITTER)
    if emitter is None:
        return False, f"no lane-owned registry emitter at {EMITTER}"
    if "names=" not in emitter:
        return False, "the emitter does not emit a names= field"
    if "seats != len(names)" not in emitter:
        return False, "the emitter does not carry its seats/names refusal logic"
    ok, why = tree.pinned(REGISTRY)
    if not ok:
        return False, why
    registry = tree.read(REGISTRY) or ""
    m_seats = re.search(r"^seats=(\d+)\s*$", registry, re.M)
    m_names = re.search(r"^names=(.*)$", registry, re.M)
    if m_seats is None or m_names is None:
        return False, "the committed registry has no seats=/names= fields"
    seats = int(m_seats.group(1))
    names = [n.strip() for n in m_names.group(1).split(",") if n.strip()]
    expected = results_names(tree, "wave1")
    if expected is None:
        return False, "wave1-results.json carries no named results to compare against"
    if seats != len(expected):
        return False, f"registry seats={seats} but the results file names {len(expected)}"
    if names != expected:
        return False, "the registry's names= list does not equal the results file's seat names"
    ok, why = tree.pinned(STALE_NOTE)
    if not ok:
        return False, why
    note = tree.read(STALE_NOTE) or ""
    if "w1-REGISTRY.txt" not in note or "superseded" not in note:
        return False, "the stale round-43 registry is not recorded as superseded"
    ok, why = tree.pinned(EXPORT_REF_SIDECAR)
    if not ok:
        return False, why
    sidecar = tree.read(EXPORT_REF_SIDECAR) or ""
    run = tree.read(RUN_RECEIPT) or ""
    m_run = re.search(r"^export-ref=([0-9a-f]{40})\s*$", run, re.M)
    m_side = re.search(r"^- export-ref=([0-9a-f]{40})\s*$", sidecar, re.M)
    if m_run is None:
        return False, "the paired run receipt names no export-ref"
    if m_side is None:
        return False, "the sidecar names no export-ref"
    if m_side.group(1) != m_run.group(1):
        return False, f"the sidecar's export-ref {m_side.group(1)[:12]} contradicts the run receipt's {m_run.group(1)[:12]}"
    return True, "leftover absent; emitter carries its refusal logic; registry names equal the results seats; sidecar export-ref equals the run receipt's"


def limb_d6(tree: Tree) -> tuple[bool, str]:
    """§6.6 — SHONEN.md lost its final empty line in the round-43 restore-and-reappend."""
    data = tree.bytes(SHONEN)
    if data is None:
        return False, "SHONEN.md absent"
    if not data.endswith(b"\n\n"):
        return False, "SHONEN.md does not end with the restored final empty line"
    text = data.decode("utf-8", "replace")
    boxes = text.count("- [~]") + text.count("- [x]") + text.count("- [ ]")
    if boxes < 4:
        return False, "SHONEN.md no longer carries the four promotion boxes"
    if BULLET_PIN not in text:
        return False, "the round-43 evidence bullet is gone (append-only violated)"
    return True, "final empty line restored; four boxes and the round-43 bullet present"


def limb_d7(tree: Tree) -> tuple[bool, str]:
    """§6.7 — the SHONEN bullet pointed at the wrong registry home for the two new instruments.

    Fixed iff corpus/instruments/README.md carries LINE-ANCHORED table rows for
    both round-43 instruments and for this counter, and SHONEN.md keeps the
    original round-43 bullet with an appended correction paragraph AFTER it.
    """
    readme = tree.read(INSTRUMENTS_README)
    if readme is None:
        return False, "corpus/instruments/README.md absent"
    for row in ("| r43-closure.sh |", "| claim-package-check.py |", "| r44-routed-defects.py |"):
        if not any(line.lstrip().startswith(row) for line in readme.splitlines()):
            return False, f"corpus/instruments/README.md carries no table row for {row.strip(' |')}"
    shonen = tree.read(SHONEN) or ""
    bullet = shonen.find(BULLET_PIN)
    if bullet < 0:
        return False, "the original round-43 SHONEN bullet is gone (append-only violated)"
    corr = para_containing(shonen, "Correction (round 43", "corpus/instruments/README.md", "registry")
    if corr is None:
        return False, "SHONEN.md carries no appended correction naming the registry pointer"
    if shonen.find(corr) <= bullet:
        return False, "the correction does not sit after the original bullet (append-only violated)"
    return True, "line-anchored registry rows present; the original bullet is kept and the correction follows it"


def limb_d8(tree: Tree) -> tuple[bool, str]:
    """§6.8 — the before-cell token 127 was attributed to a control that prints exit=2.

    Fixed iff the erratum carries one paragraph with both exits and the
    different-commands statement, and the measurement receipt is present with
    its PINNED bytes (a fabricated receipt with the right tokens does not pass).
    """
    erratum = tree.read(ERRATUM)
    if erratum is None:
        return False, f"{ERRATUM} absent"
    para = para_containing(erratum, "127", "exit=2")
    if para is None:
        return False, "no paragraph states both the 127 and the control's exit=2"
    if "different command" not in para:
        return False, "the paragraph does not say the two values describe different commands"
    ok, why = tree.pinned(RECEIPT_127)
    if not ok:
        return False, why
    receipt = tree.read(RECEIPT_127) or ""
    if "exit=127" not in receipt:
        return False, f"{RECEIPT_127} does not record exit=127"
    if "ab98fac9" not in receipt:
        return False, f"{RECEIPT_127} does not name the exported base the measurement was taken at"
    return True, "erratum separates the two exits; the 127 is backed by the pinned measurement receipt"


LIMBS = [
    ("D1", limb_d1),
    ("D2", limb_d2),
    ("D3", limb_d3),
    ("D4", limb_d4),
    ("D5", limb_d5),
    ("D6", limb_d6),
    ("D7", limb_d7),
    ("D8", limb_d8),
]


def grade(tree: Tree, quiet: bool = True) -> tuple[int, int]:
    """Grade every limb; return (fixed, unresolved)."""
    fixed = 0
    unresolved = 0
    for name, limb in LIMBS:
        try:
            ok, detail = limb(tree)
        except Exception as exc:  # a limb that blows up is unresolved, never fixed
            ok, detail = False, f"limb error: {exc!r}"
        if ok:
            fixed += 1
        else:
            unresolved += 1
        if not quiet:
            print(f"R44-{name} status={'fixed' if ok else 'unresolved'} detail={detail}")
    return fixed, unresolved


# --------------------------------------------------------------------------
# selftest — mutants must be rejected
# --------------------------------------------------------------------------


def _strip_corrections(text: str) -> str:
    kept = []
    for para in paragraphs(text):
        if para.startswith("Correction (round 43"):
            kept.append("Correction (round 43): the numeral was corrected.")
        else:
            kept.append(para)
    return "\n\n".join(kept) + "\n"


def build_mutants(base: Tree) -> list[tuple[str, Tree, str]]:
    """Return (case-id, mutant tree, expectation) triples.

    Every mutant keeps the prose marker and removes, rewrites or fabricates the
    artifact the limb binds to, so a counter that only looks for markers — or
    only for artifact existence — would pass it.
    """
    mutants: list[tuple[str, Tree, str]] = []

    def overlay(changes: dict[str, str | None]) -> Tree:
        return Overlay(base, changes)

    scorecard = base.read(SCORECARD) or ""
    lesson43 = base.read(LESSON43) or ""
    log = base.read(LOG) or ""
    shonen = base.read(SHONEN) or ""
    readme = base.read(INSTRUMENTS_README) or ""
    erratum = base.read(ERRATUM) or ""
    emitter = base.read(EMITTER) or ""
    registry = base.read(REGISTRY) or ""
    sidecar = base.read(EXPORT_REF_SIDECAR) or ""
    receipt = base.read(RECEIPT_127) or ""

    # --- fabrication class (R44W2Exec05): plausible content, no real work ----
    fabricated = (
        "Correction (round 43): 13/19 is superseded; see .ufo/waves/round-43/claims-erratum-6.md.\n\n"
        "13/19 superseded by r43-closure.sh evidence. exit=127 and exit=2 are different commands.\n\n"
        "seats=66\nnames=" + ",".join(f"FAKE{i}" for i in range(66)) + "\n\n"
        "- export-ref=" + "f" * 40 + "\n\n"
        "exit=127 ab98fac9\n\n"
        "Correction (round 43): the numeral is 26 characters. "
        + FIX_POINTER + " " + FIX_POINTER_FULL + " " + COUNT_COMMAND + "\n"
    )
    mutants.append(
        (
            "FABRICATED-ARTIFACTS",
            overlay(
                {
                    ERRATUM: fabricated,
                    LESSON43: fabricated,
                    REGISTRY: fabricated,
                    EXPORT_REF_SIDECAR: fabricated,
                    RECEIPT_127: fabricated,
                }
            ),
            "unresolved",
        )
    )

    # --- D1 ---------------------------------------------------------------
    marker = (
        "\n\nCorrection (round 43; appended round 44): the `closed=13/19 exit=1` literal is "
        "superseded; see `.ufo/waves/round-43/claims-erratum-6.md`.\n\n"
    )
    mutants.append(("D1-marker-only", overlay({SCORECARD: scorecard + marker, ERRATUM: None}), "unresolved"))
    rewritten_row = scorecard.replace(
        "base `ab98fac9` `closed=13/19 exit=1` with exactly K14-K19 open",
        "REWRITTEN-CELL (token 13/19 retained)",
    )
    if rewritten_row == scorecard:
        rewritten_row = scorecard + "\n"
    mutants.append(("D1-row-rewritten", overlay({SCORECARD: rewritten_row}), "unresolved"))

    # --- D2 ---------------------------------------------------------------
    mutants.append(("D2-erratum-missing", overlay({ERRATUM: None}), "unresolved"))
    split_para = erratum.replace("superseded", "\n\nsuperseded", 1)
    mutants.append(("D2-paragraph-split", overlay({ERRATUM: split_para}), "unresolved"))

    # --- D3 ---------------------------------------------------------------
    mutants.append(("D3-marker-only", overlay({LESSON43: _strip_corrections(lesson43)}), "unresolved"))
    rewritten = lesson43.replace("29-character prefix", "26-character prefix")
    mutants.append(("D3-originals-rewritten", overlay({LESSON43: rewritten}), "unresolved"))

    # --- D4 ---------------------------------------------------------------
    bad_log = log.replace("wave 1 seats: 66", "wave 1 seats: 999")
    if bad_log == log:
        bad_log = log + "\n\nwave 1 seats: 999\n"
    mutants.append(("D4-count-mismatch", overlay({LOG: bad_log}), "unresolved"))
    denial = re.sub(r"planner=L1", "planner seat was NOT held by the L1", log, count=1)
    if denial == log:
        denial = log
    mutants.append(("D4-denial", overlay({LOG: denial}), "unresolved"))

    # --- D5 ---------------------------------------------------------------
    mutants.append(("D5-leftover-back", overlay({TMP_LEFTOVER: "aborted write\n"}), "unresolved"))
    mutants.append(
        ("D5-empty-names", overlay({REGISTRY: re.sub(r"^names=.*$", "names=", registry, flags=re.M)}), "unresolved")
    )
    fake_names = re.sub(
        r"^names=.*$",
        "names=" + ",".join("x" for _ in range(66)),
        registry,
        flags=re.M,
    )
    mutants.append(("D5-fabricated-names", overlay({REGISTRY: fake_names}), "unresolved"))
    stub = emitter.replace("seats != len(names)", "True or False") if "seats != len(names)" in emitter else "# names=\n"
    mutants.append(("D5-stub-emitter", overlay({EMITTER: stub}), "unresolved"))
    wrong_ref = re.sub(r"^- export-ref=[0-9a-f]{40}\s*$", "- export-ref=" + "a" * 40, sidecar, flags=re.M)
    mutants.append(("D5-wrong-export-ref", overlay({EXPORT_REF_SIDECAR: wrong_ref}), "unresolved"))
    mutants.append(("D5-no-sidecar", overlay({EXPORT_REF_SIDECAR: None}), "unresolved"))

    # --- D6 ---------------------------------------------------------------
    mutants.append(("D6-no-final-blank", overlay({SHONEN: shonen.rstrip("\n") + "\n"}), "unresolved"))

    # --- D7 ---------------------------------------------------------------
    prose = re.sub(r"^\| r43-closure\.sh \|.*$", "r43-closure.sh and claim-package-check.py are registered.", readme, flags=re.M)
    mutants.append(("D7-rows-missing", overlay({INSTRUMENTS_README: prose}), "unresolved"))

    # --- D8 ---------------------------------------------------------------
    mutants.append(("D8-fabricated-receipt", overlay({RECEIPT_127: "exit=127 ab98fac9\n"}), "unresolved"))
    mutants.append(("D8-no-receipt", overlay({RECEIPT_127: None}), "unresolved"))

    return mutants


def run_selftest(base: Tree, work_root: str | None) -> int:
    work = tempfile.mkdtemp(prefix="r44-routed-defects-", dir=work_root)
    failures = 0
    cases = 0
    try:
        # positive case: the repaired tree passes every limb
        fixed, unresolved = grade(base, quiet=True)
        cases += 1
        ok = unresolved == 0
        if not ok:
            failures += 1
        print(f"selftest case=POSITIVE verdict={'pass' if ok else 'fail'} fixed={fixed} unresolved={unresolved}")

        for cid, mutant, expect in build_mutants(base):
            cases += 1
            limb_id = cid.split("-")[0]
            if limb_id == "FABRICATED":
                # the fabrication case must fail on at least the pinned limbs
                bad = [n for n, limb in LIMBS if not limb(mutant)[0]]
                ok = bool(bad)
                detail = f"unresolved limbs: {','.join(bad)}" if bad else "every limb accepted a fabricated tree"
            else:
                limb = dict(LIMBS)[limb_id]
                try:
                    ok_limb, detail = limb(mutant)
                except Exception as exc:
                    ok_limb, detail = False, f"limb error: {exc!r}"
                ok = (expect == "unresolved") and (not ok_limb)
            if not ok:
                failures += 1
            print(f"selftest case={cid} verdict={'pass' if ok else 'fail'} detail={str(detail)[:160]}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"selftest cases={cases} failures={failures}")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="tree to grade")
    ap.add_argument("--baseline", help="frozen baseline export (optional)")
    ap.add_argument("--selftest", action="store_true", help="run the mutant battery")
    ap.add_argument("--work", help="scratch root for --selftest (default $TMPDIR)")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        print(f"r44-routed-defects: root {args.root} is not a directory", file=sys.stderr)
        return 2

    if args.selftest:
        work = args.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
        return run_selftest(Tree(args.root), work)

    tree = Tree(args.root)
    fixed, unresolved = grade(tree, quiet=False)
    print(f"routed-defects total={TOTAL} fixed={fixed} unresolved={unresolved} exit={0 if unresolved == 0 else 1}")
    if args.baseline:
        if not os.path.isdir(args.baseline):
            print(f"r44-routed-defects: baseline {args.baseline} is not a directory", file=sys.stderr)
            return 2
        bfixed, bunresolved = grade(Tree(args.baseline), quiet=True)
        print(f"routed-defects-baseline total={TOTAL} fixed={bfixed} unresolved={bunresolved}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
