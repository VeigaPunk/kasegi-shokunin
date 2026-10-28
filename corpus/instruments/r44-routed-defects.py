#!/usr/bin/env python3
"""r44-routed-defects.py — round-44 C1 counter over committed lane evidence.

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
    *content that must be inside it*; the `--selftest` mutants delete or
    blank exactly those artifacts (leaving the prose marker in place) and
    require the limb to report `unresolved`.  The round-43 seat review rejected
    an earlier draft of this counter for accepting a marker-only tree
    (`.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`); this
    implementation is the fail-closed replacement.

    Append-only is enforced where the protocol demands it: a correction must
    sit AFTER the text it corrects, and the corrected text must still be there.

USAGE
    python3 corpus/instruments/r44-routed-defects.py --root TREE [--baseline TREE]
    python3 corpus/instruments/r44-routed-defects.py --root TREE --selftest [--work DIR]

    --root      tree to grade (an exported lane tree, or the lane checkout).
    --baseline  optional frozen baseline export; printed as a second tally and
                used for the cross-checks that need two trees.
    --selftest  build marker-only mutants under --work and grade them.
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
import json
import os
import re
import shutil
import sys
import tempfile

TOTAL = 8

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


def wave_seat_count(tree: Tree, wave: str = "wave1") -> int | None:
    """Number of seats recorded in a wave results file (0 when the file is absent)."""
    raw = tree.read(f".ufo/waves/round-44/{wave}-results.json")
    if raw is None:
        return None
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError:
        return None
    seats = doc.get("seats")
    results = doc.get("results")
    if isinstance(seats, int):
        return seats
    if isinstance(results, list):
        return len(results)
    return None


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
EXPORT_REF_SIDECAR = ".ufo/waves/round-43/final-gates/r42-at-de09313-selftest.export-ref.md"
EMITTER = "corpus/instruments/wave-registry.py"
REGISTRY = ".ufo/waves/round-44/wave-registry.txt"
RECEIPT_127 = ".ufo/waves/round-44/controls/missing-suite-base.txt"

FIX_POINTER = "c6ae07c6a541e0e96d0040afb6"
FIX_POINTER_FULL = "c6ae07c6a541e0e96d0040afb62b45dd37711300"
COUNT_COMMAND = "printf %s c6ae07c6a541e0e96d0040afb6 | wc -c"


def limb_d1(tree: Tree) -> tuple[bool, str]:
    """§6.1 — the `closed=13/19` literal was unbacked; a correction must supersede it.

    Fixed iff SCORECARD.md carries an appended `Correction (round 43` paragraph
    that names the literal, says it is superseded, cites the erratum file, sits
    AFTER the round-43 move-log row, and the cited erratum file exists with the
    literal and the `superseded` vocabulary inside it.
    """
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
    if "13/19" not in row:
        return False, "round-43 move-log row no longer carries 13/19 (history rewritten)"
    idx = scorecard.find(row)
    corr = None
    for para in paragraphs(scorecard):
        if (
            para.startswith("Correction (round 43")
            and "13/19" in para
            and "superseded" in para
            and "claims-erratum-6.md" in para
        ):
            corr = para
            break
    if corr is None:
        return False, "no appended Correction (round 43 paragraph naming 13/19 + superseded + erratum"
    if scorecard.find(corr) <= idx:
        return False, "correction does not sit after the round-43 row (append-only violated)"
    erratum = tree.read(ERRATUM)
    if erratum is None:
        return False, f"cited {ERRATUM} absent"
    if "13/19" not in erratum or "superseded" not in erratum:
        return False, f"{ERRATUM} lacks the literal or the superseded vocabulary"
    return True, "correction appended after the row; erratum carries 13/19 + superseded"


def limb_d2(tree: Tree) -> tuple[bool, str]:
    """§6.2 — no check could see defect 1; the fix is the erratum K17's escape already covers.

    Fixed iff K17 still carries its own `claims-erratum*` escape (not widened
    into K18), a file matching that glob sits in the round-43 wave dir with the
    literal and the vocabulary, and the round-44 lesson names the mechanism.
    """
    k17 = tree.read(K17)
    if k17 is None:
        return False, "K17 limb script absent"
    if "claims-erratum" not in k17:
        return False, "K17 no longer carries the claims-erratum escape"
    wave_dir = os.path.dirname(ERRATUM)
    candidates = []
    for name in sorted(os.listdir(os.path.join(tree.root, wave_dir)) if os.path.isdir(os.path.join(tree.root, wave_dir)) else []):
        if re.fullmatch(r"claims-erratum.*\.md", name):
            candidates.append(wave_dir + "/" + name)
    hit = None
    for cand in candidates:
        body = tree.read(cand)
        if body and "13/19" in body and "superseded" in body and "r43-closure.sh" in body:
            hit = cand
            break
    if hit is None:
        return False, "no claims-erratum*.md in the round-43 wave dir carries 13/19 + superseded + r43-closure.sh"
    lesson = tree.read(LESSON44) or ""
    if "K17" not in lesson or "escape" not in lesson:
        return False, "round-44 lesson does not name the K17 escape as the mechanism"
    return True, f"{hit} matched by K17's own escape; mechanism named in the round-44 lesson"


def limb_d3(tree: Tree) -> tuple[bool, str]:
    """§6.3 — the lesson numeral was wrong (29 characters); the fix pointer is 26."""
    lesson = tree.read(LESSON43)
    if lesson is None:
        return False, "corpus/lessons/round-43.md absent"
    if "29-character prefix" not in lesson:
        return False, "the original 29-character sentences are gone (append-only violated)"
    corr = para_containing(
        lesson,
        "Correction (round 43",
        FIX_POINTER,
        FIX_POINTER_FULL,
        COUNT_COMMAND,
    )
    if corr is None:
        return False, "no appended correction naming the pointer, the full hash and the counting command"
    if not re.search(r"\b26\b[ -]characters", corr):
        return False, "the correction does not state 26 characters"
    if len(FIX_POINTER) != 26:
        return False, "internal inconsistency: the pointer is not 26 characters"
    if not re.search(r"\b40\b[ -]character", corr):
        return False, "the correction does not state the 40-character full hash"
    return True, "appended correction states 26 characters with the counting command; history kept"


def limb_d4(tree: Tree) -> tuple[bool, str]:
    """§6.4 — the round report recorded neither the planner=L1 mapping nor the L2-floor line."""
    log = tree.read(LOG)
    if log is None:
        return False, "LOG.md absent"
    head = log.rfind("## Round 44")
    if head < 0:
        return False, "LOG.md has no round-44 section"
    section = log[head:]
    if not re.search(r"planner\s*=\s*L1|planner seat[^.]{0,40}L1", section):
        return False, "the round-44 LOG section does not record the planner=L1 mapping"
    if "L2 floor" not in section:
        return False, "the round-44 LOG section does not record the L2-floor line"
    if "residual" not in section.lower():
        return False, "the round-44 LOG section does not record the residual-call line"
    m = re.search(r"wave 1 seats[:=]\s*(\d+)", section)
    if m is None:
        return False, "the round-44 LOG section does not state the wave-1 seat count"
    claimed = int(m.group(1))
    actual = wave_seat_count(tree, "wave1")
    if actual is None:
        return False, "wave1-results.json absent or unparsable; the seat count cannot be cross-checked"
    if claimed != actual:
        return False, f"the LOG claims {claimed} wave-1 seats; the committed results file holds {actual}"
    return True, f"planner=L1, L2-floor and residual lines recorded; wave-1 seat count {claimed} cross-checks"


def limb_d5(tree: Tree) -> tuple[bool, str]:
    """§6.5 — wave-evidence hygiene: aborted-write leftover, empty registry names, missing export-ref."""
    if tree.exists(TMP_LEFTOVER):
        return False, f"aborted-write leftover {TMP_LEFTOVER} is present"
    emitter = tree.read(EMITTER)
    if emitter is None:
        return False, f"no lane-owned registry emitter at {EMITTER}"
    if "names=" not in emitter:
        return False, "the emitter does not emit a names= field"
    registry = tree.read(REGISTRY)
    if registry is None:
        return False, f"no committed registry at {REGISTRY}"
    m_seats = re.search(r"^seats=(\d+)\s*$", registry, re.M)
    m_names = re.search(r"^names=(.*)$", registry, re.M)
    if m_seats is None or m_names is None:
        return False, "the committed registry has no seats=/names= fields"
    seats = int(m_seats.group(1))
    names = [n for n in m_names.group(1).split(",") if n.strip()]
    if seats == 0 or len(names) != seats:
        return False, f"registry names= is empty or inconsistent (seats={seats}, names={len(names)})"
    actual = wave_seat_count(tree, "wave1")
    if actual is not None and seats != actual:
        return False, f"registry seats={seats} but the committed results file holds {actual}"
    sidecar = tree.read(EXPORT_REF_SIDECAR)
    if sidecar is None:
        return False, f"missing export-ref sidecar {EXPORT_REF_SIDECAR}"
    if "export-ref=ab98fac9" not in sidecar:
        return False, "the export-ref sidecar does not name the export ref"
    if "r42-at-de09313-selftest.txt" not in sidecar:
        return False, "the export-ref sidecar does not name the receipt it annotates"
    return True, "leftover absent; emitter and a populated registry committed; export-ref sidecar present"


def limb_d6(tree: Tree) -> tuple[bool, str]:
    """§6.6 — SHONEN.md lost its final empty line in the round-43 restore-and-reappend."""
    data = tree.bytes(SHONEN)
    if data is None:
        return False, "SHONEN.md absent"
    if not data.endswith(b"\n\n"):
        return False, "SHONEN.md does not end with the restored final empty line"
    text = data.decode("utf-8", "replace")
    if text.count("- [~]") + text.count("- [x]") + text.count("- [ ]") < 4:
        return False, "SHONEN.md no longer carries the four promotion boxes"
    return True, "final empty line restored; four boxes present"


def limb_d7(tree: Tree) -> tuple[bool, str]:
    """§6.7 — the SHONEN bullet pointed at the wrong registry home for the two new instruments."""
    readme = tree.read(INSTRUMENTS_README)
    if readme is None:
        return False, "corpus/instruments/README.md absent"
    missing = [n for n in ("r43-closure.sh", "claim-package-check.py") if n not in readme]
    if missing:
        return False, f"corpus/instruments/README.md carries no row for {', '.join(missing)}"
    shonen = tree.read(SHONEN) or ""
    corr = para_containing(shonen, "Correction (round 43", "corpus/instruments/README.md", "registry")
    if corr is None:
        return False, "SHONEN.md carries no appended correction naming the registry pointer"
    if "r44-routed-defects.py" not in readme:
        return False, "corpus/instruments/README.md carries no row for the round-44 counter"
    return True, "registry rows present in corpus/instruments/README.md; SHONEN pointer corrected by append"


def limb_d8(tree: Tree) -> tuple[bool, str]:
    """§6.8 — the before-cell token 127 was attributed to a control that prints exit=2."""
    erratum = tree.read(ERRATUM)
    if erratum is None:
        return False, f"{ERRATUM} absent"
    para = para_containing(erratum, "127", "exit=2")
    if para is None:
        return False, "no paragraph states both the 127 and the control's exit=2"
    if "different command" not in para:
        return False, "the paragraph does not say the two values describe different commands"
    receipt = tree.read(RECEIPT_127)
    if receipt is None:
        return False, f"measurement receipt {RECEIPT_127} absent"
    if "exit=127" not in receipt:
        return False, f"{RECEIPT_127} does not record exit=127"
    if "ab98fac9" not in receipt:
        return False, f"{RECEIPT_127} does not name the exported base"
    return True, "erratum separates the two exits; the 127 is backed by a committed receipt"


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
# selftest — marker-only mutants must be rejected
# --------------------------------------------------------------------------


def build_mutants(base: Tree) -> list[tuple[str, Tree, str]]:
    """Return (case-id, mutant tree, expectation) triples.

    Every mutant keeps the prose marker and removes or blanks the artifact the
    limb binds to, so a counter that only looks for markers would pass it.
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

    # D1 — a correction paragraph is present but the cited erratum is gone.
    marker = (
        "\n\nCorrection (round 43; appended round 44): the `closed=13/19 exit=1` literal is "
        "superseded; see `.ufo/waves/round-43/claims-erratum-6.md`.\n\n"
    )
    mutants.append(("D1-marker-only", overlay({SCORECARD: scorecard + marker, ERRATUM: None}), "unresolved"))

    # D2 — the erratum file is gone; K17's escape has nothing to match.
    mutants.append(("D2-erratum-missing", overlay({ERRATUM: None}), "unresolved"))

    # D3 — the appended correction paragraph is reduced to a bare marker sentence:
    # it still says the numeral was corrected, but no longer carries the pointer,
    # the full hash or the counting command.
    def strip_corrections(text: str) -> str:
        kept = []
        for para in paragraphs(text):
            if para.startswith("Correction (round 43"):
                kept.append("Correction (round 43): the numeral was corrected.")
            else:
                kept.append(para)
        return "\n\n".join(kept) + "\n"

    mutants.append(("D3-marker-only", overlay({LESSON43: strip_corrections(lesson43)}), "unresolved"))

    # D4 — the mapping is claimed with a seat count that contradicts the results file.
    bad_log = log.replace("wave 1 seats: 66", "wave 1 seats: 999")
    if bad_log == log:
        bad_log = log + "\n\nwave 1 seats: 999\n"
    mutants.append(("D4-count-mismatch", overlay({LOG: bad_log}), "unresolved"))

    # D5 — the aborted-write leftover is back.
    mutants.append(("D5-leftover-back", overlay({TMP_LEFTOVER: "aborted write\n"}), "unresolved"))
    # D5 — the registry names= field is empty again.
    registry = base.read(REGISTRY) or ""
    mutants.append(
        ("D5-empty-names", overlay({REGISTRY: re.sub(r"^names=.*$", "names=", registry, flags=re.M)}), "unresolved")
    )
    # D5 — the export-ref sidecar is gone.
    mutants.append(("D5-no-sidecar", overlay({EXPORT_REF_SIDECAR: None}), "unresolved"))

    # D6 — the final empty line is dropped again.
    mutants.append(("D6-no-final-blank", overlay({SHONEN: shonen.rstrip("\n") + "\n"}), "unresolved"))

    # D7 — the registry rows are removed again.
    mutants.append(
        (
            "D7-rows-missing",
            overlay({INSTRUMENTS_README: readme.replace("r43-closure.sh", "<retracted>")}),
            "unresolved",
        )
    )

    # D8 — the 127 receipt is gone.
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
            name = {"D1": "D1", "D2": "D2", "D3": "D3", "D4": "D4", "D5": "D5", "D6": "D6", "D7": "D7", "D8": "D8"}
            limb_id = cid.split("-")[0]
            limb = dict(LIMBS)[limb_id]
            try:
                ok_limb, detail = limb(mutant)
            except Exception as exc:
                ok_limb, detail = False, f"limb error: {exc!r}"
            ok = (expect == "unresolved") and (not ok_limb)
            if not ok:
                failures += 1
            print(f"selftest case={cid} verdict={'pass' if ok else 'fail'} limb={limb_id} detail={detail[:160]}")
            _ = name
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"selftest cases={cases} failures={failures}")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True, help="tree to grade")
    ap.add_argument("--baseline", help="frozen baseline export (optional)")
    ap.add_argument("--selftest", action="store_true", help="run the marker-only mutant battery")
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
