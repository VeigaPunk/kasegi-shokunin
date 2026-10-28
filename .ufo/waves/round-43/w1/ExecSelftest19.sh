#!/usr/bin/env bash
# ExecSelftest19.sh -- the graded selftest runner block for r43-closure.sh.
#
#   ExecSelftest19.sh --export DIR --work DIR [--scratch-root DIR]
#                     [--check-cmd TEMPLATE] [--lane DIR] [--base-ref HASH]
#                     [--cases K14,K19] [--run-transcript PATH]
#                     [--probe-controls] [--emit PATH]
#
# The runner grades nineteen cases K1..K19 and prints exactly
#
#   selftest case=K<n> mutants=<good>/<total> positive=<pass|fail> payload-match=<0|1> verdict=<pass|fail>
#   selftest cases=19 failures=<k>
#
# Exit status: 0 only when every selected case prints verdict=pass; 1 when any
# case fails; 2 on a usage error; 3 when the runner's own degenerate-control
# probe accepts a degenerate (nothing is printed to stdout in that case: the
# suite must never print a green summary from a degenerate runner).
#
# What the runner asserts per case, in one private directory
# <work>/selftest/case-<id>/ under --work (never inside the export):
#
#   pos/        a copy of the export with the case's correction present
#               -> the check MUST print closed=1
#   mut-committed/  a copy of the export with the COMMITTED r42 defeat bytes
#               installed by `git cat-file` and digest-asserted (K14-K19), or
#               the carried r42 mutant battery (K1-K13)
#               -> the check MUST print closed=0
#   mut-shape/  the committed defeat DUPLICATED and only its first occurrence
#               rewritten -- the shape, not the string, is the defeat
#               -> the check MUST print closed=0
#
# Isolation: while a case runs, exactly one case-* directory exists under
# <work>/selftest and the tree handed to the check resolves inside it; every
# case directory carries a unique canary and no canary may appear in a payload
# (a check that walks its own tree must surface the canary as a leak); the case
# directory is removed before the next case starts and its absence is asserted.
#
# Dispatch contract: the check for case <id> on tree <dir> is produced by
# --check-cmd, a shell snippet run as `bash -c TEMPLATE es19 <id> <dir>` (so
# $1 is the case id and $2 the tree).  It must print exactly one line
#
#   K<n> payload=... closed=0|1
#
# whose n is the case's own.  When the block is embedded in r43-closure.sh the
# engine passes a callable instead and --check-cmd is not used.
#
# Carried cases K1-K13 keep the r42 J1-J13 mutant batteries and are graded
# through the suite's carried battery hook (`CARRIED_BATTERY[cid](export,
# case_dir) -> (good, total)`), which must apply at least one mutation.  A
# missing hook fails the case closed with mutants=0/0; a battery that reports
# zero mutations is a red, so a summary-only line can never satisfy a case.
#
# Degenerate controls (--probe-controls, and always run before a transcript):
#   D-STUB      an always-pass check (closed=1 on every tree) must be graded
#               verdict=fail, never pass
#   D-SUMMARY   a transcript carrying only `selftest cases=19 failures=0` and no
#               graded case line must be refused
#   D-DUPLICATE a check that reads only the FIRST occurrence of a literal must be
#               graded verdict=fail on the duplicated-block shape mutant (R42:
#               the shape, not the string, is the defeat)
#   ACCEPT      the runner's own well-formed nineteen-line transcript must be
#               accepted (a reject-everything acceptor is not a pass)
#
# payload-match: with --run-transcript, each case's positive payload must equal
# that transcript's payload for the same id (`,replay=...` suffix stripped).
# Without it, the positive tree is dispatched twice and the payloads must be
# identical and non-empty -- a check whose payload drifts between two identical
# trees is reading state it does not own.

set -uo pipefail

PROG="$(basename -- "$0")"
usage() { sed -n '2,90p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        *) break ;;
    esac
done

exec python3 - "$@" <<'ES19_PY'
# ---------------------------------------------------------------------------
# ExecSelftest19 engine.
#
# Graded case table:
#   K1..K13   carried from the r42 suite (J1..J13): the r42 mutant battery per
#             case plus the committed defeat artifact its replay limb re-executes
#   K14..K19  narrative-evidence checks RD42-1, RD42-2/3, RD42-4, RD42-8,
#             RD42-5, RD42-6; each case's committed mutant installs the exact
#             committed r42 bytes (digest-asserted) that a green r42 suite
#             accepted, and each case's shape mutant duplicates the defect and
#             rewrites only the first occurrence
# ---------------------------------------------------------------------------

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

NCHECKS = 19
CASE_IDS = ["K%d" % i for i in range(1, NCHECKS + 1)]
ROUND = 43
BASE_REF = "ab98fac9dce87130bc4f66de89e30650d63943dc"
LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
RECORDS = ["SCORECARD.md", "LOG.md", "SHONEN.md"]
CORRECTION_43 = "Correction (round 43)"

LINE_RX = re.compile(r"^(K\d+) payload=(.*) closed=([01])$")
CASE_LINE_RX = re.compile(
    r"^selftest case=(K\d+) mutants=(\d+)/(\d+) positive=(pass|fail) "
    r"payload-match=([01]) verdict=(pass|fail)$")
SUMMARY_RX = re.compile(r"^selftest cases=(\d+) failures=(\d+)$")

# Carried K1-K13: (case, r42 check, r42 mutant label, r42 family, committed
# defeat artifact, its sha256).  The artifact digests are the r42 suite's own;
# the runner only reports them, the suite's replay limb grades them.
CARRIED = [
    ("K1", "J1", "strip-evidence-union", "F-EVID",
     ".ufo/waves/round-41/wave2/RevC1Counters.md",
     "afe2c4d388d331035854d709072e3f62b9f87fa0f363e2170619789fb60a25d2"),
    ("K2", "J2", "mangled-tally", "F-TOKEN",
     ".ufo/waves/round-40/wave2/RevC1Counters.defeats.txt",
     "6eef3338dc472e9033dc9131f5da630a6f23fea89ddda174f6819473593860af"),
    ("K3", "J3", "table-mutations", "F-TABLE",
     ".ufo/waves/round-41/wave2/MutSkillTablePipes.md",
     "41117cde4e2e30bb2969c056f00b8c9b4d379da9e7903a887fbd7867fb1fea7a"),
    ("K4", "J4", "declaration-mutations", "F-DECL",
     ".ufo/waves/round-41/wave2/CritDeclarationCoverage.md",
     "0254bbe7b8b0b33bb6a8aa06b135813b8a11cc501bea1d81bed01e19da9141df"),
    ("K5", "J5", "scratch-scan-mutations", "F-SCAN",
     ".ufo/waves/round-41/wave2/MutScratchTiming.md",
     "54fb821cd10d3c95a9bc4d3605b4fdce6da8611a057b6efcfd959f1c36fdae7e"),
    ("K6", "J6", "binding-mutations", "F-BIND",
     ".ufo/waves/round-41/wave2/MutBindingExistence.md",
     "960e8da0580f1b4760112fb218d4620a55e5050576ce09fc7f3fef8c7808fb32"),
    ("K7", "J7", "frontier-flip-mutations", "F-FLIP",
     ".ufo/waves/round-41/wave2/MutFrontierParser.md",
     "faae26b19b0c04908fced285d3a8733b81125bccdfdad62f9dcc6f625ce4365c"),
    ("K8", "J8", "forged-receipts", "-", "-", "-"),
    ("K9", "J9", "acceptance-predicate", "-", "-", "-"),
    ("K10", "J10", "isolation-probe", "-", "-", "-"),
    ("K11", "J11", "dedup-marker-strip", "-", "-", "-"),
    ("K12", "J12", "deletion-probe", "-", "-", "-"),
    ("K13", "J13", "export-fidelity", "-", "-", "-"),
]

# K14-K19 committed-defect provenance: the exact r42 bytes a green r42 suite
# accepted.  (rel, sha256) pairs are installed with `git cat-file` and the
# digest is asserted before the mutant is graded.
NARRATIVE = [
    {
        "id": "K14", "rd": "RD42-1", "label": "corrections-literal",
        "committed": [("SCORECARD.md",
                       "d46a8c3645e58f566725b8a3ea318aeb95b597234d8908456c08e2b65e827cc3")],
        "defect": "SCORECARD.md:1634 quotes `corrections=33`; the suite re-derives 34",
        "shape": ("SCORECARD.md", "corrections=33", "corrections=34"),
    },
    {
        "id": "K15", "rd": "RD42-2/3", "label": "wave-dispatch-narrative",
        "committed": [("LOG.md",
                       "b4a0ac0e3cadb28d9ca585dee3f2fc5ff5e3e089b86b3758bc9c49ec3fee9bbf"),
                      ("corpus/lessons/round-42.md",
                       "6ed6cefae3dffcfd4f6688bb1a1506b36fc109628cb9b82099200f354d75f46d")],
        "defect": "LOG.md:1804 + lessons/round-42.md:11,16 say wave 2 kasegi-r42-falsify dispatched 36 seats; no results file exists",
        "shape": ("LOG.md", "36 seats dispatched", "64 seats dispatched"),
    },
    {
        "id": "K16", "rd": "RD42-4", "label": "placeholder-promise",
        "committed": [("corpus/lessons/round-42.md",
                       "6ed6cefae3dffcfd4f6688bb1a1506b36fc109628cb9b82099200f354d75f46d")],
        "defect": "lessons/round-42.md `## Wave-2 falsification` promises verdicts when the falsify wave reports",
        "shape": ("corpus/lessons/round-42.md", "## Wave-2 falsification",
                  "## Wave-2 falsification (superseded)"),
    },
    {
        "id": "K17", "rd": "RD42-8", "label": "claims-before-literal",
        "committed": [(".ufo/waves/round-42/claims.json",
                       "313b24ce3a35884bf70112743b8b0089802b2128dd3b6f80bbacf1cf006fcb08")],
        "defect": "round-42 claims.json C1 before quotes `closed=10/12` while its control prints `closed=8/12`",
        "shape": (".ufo/waves/round-42/claims.json", "closed=10/12",
                  "closed=8/12 and closed=10/12"),
    },
    {
        "id": "K18", "rd": "RD42-5", "label": "unbound-quote",
        "committed": [("corpus/lessons/round-42-verifier-spotcheck.md",
                       "5cc751c5e0259ba6e6ba2bc17189859e6928dd749784bbf1408a4ae62788d68f")],
        "defect": "spotcheck:65 and claims-erratum-4.md:9 quote `closed=10/13` with no committed transcript printing it",
        "shape": ("corpus/lessons/round-42-verifier-spotcheck.md", "closed=10/13",
                  "closed=9/13 and closed=10/13"),
    },
    {
        "id": "K19", "rd": "RD42-6", "label": "freeze-record-order",
        "committed": [],
        "defect": "the round-43 freeze record is absent at base (RD42-6: a freeze label that predates the evidence)",
        "shape": None,
    },
]

K19_FREEZE = ".ufo/waves/round-43/freeze.txt"
K19_CLAIMS = ".ufo/waves/round-43/claims.json"
K19_STALE_LABEL = "2026-10-28T12:05:00Z"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def read_text(path):
    try:
        with open(path, "rb") as fh:
            return fh.read().decode("utf-8", "replace")
    except OSError:
        return None


def read_bytes(path):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        return None


def write_text(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    data = read_bytes(path)
    return sha256_bytes(data) if data is not None else ""


def same_path(a, b):
    return os.path.realpath(a) == os.path.realpath(b)


def inside(path, root):
    path = os.path.realpath(path)
    root = os.path.realpath(root)
    return path == root or path.startswith(root + os.sep)


def git(args, cwd=None):
    proc = subprocess.run(["git"] + args, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def copy_tree(src, dst):
    """A private copy of the export.  Reflink where the filesystem allows it."""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    proc = subprocess.run(["cp", "-a", "--reflink=auto", src + os.sep + ".",
                           dst], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        shutil.copytree(src, dst, symlinks=True)
    return dst


def record_digest(tree, rel):
    return sha256_file(os.path.join(tree, rel))


# ---------------------------------------------------------------------------
# committed-byte installation (the mutant must be the COMMITTED defeat)
# ---------------------------------------------------------------------------

def install_committed(tree, rel, expect_sha, lane, base):
    """Install <base>:<rel> into tree, asserting the committed digest."""
    rc, blob = git(["cat-file", "-p", "%s:%s" % (base, rel)], cwd=lane)
    if rc != 0 or not blob:
        return "git-cat-file-failed:%s" % rel
    got = sha256_bytes(blob)
    if got != expect_sha:
        return "digest-mismatch:%s:%s" % (rel, got[:12])
    path = os.path.join(tree, rel)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(blob)
    if sha256_file(path) != expect_sha:
        return "write-verify-failed:%s" % rel
    return ""


# ---------------------------------------------------------------------------
# narrative case builders (K14-K19)
#
# Each builder takes (tree, lane, base) and returns "" on success or a reason
# string on failure.  A builder that cannot reproduce the committed bytes
# returns a reason, and the case fails closed -- never a silent pass.
# ---------------------------------------------------------------------------

def append_correction(tree, rel, marker, line):
    """Append a `Correction (round 43)` line, idempotently.

    The positive fixture must be idempotent: when the export already carries the
    round's correction (the Y tree), the builder must not append a second line,
    or the positive payload could not match the run transcript.
    """
    path = os.path.join(tree, rel)
    old = read_text(path)
    if old is None:
        return "absent:%s" % rel
    if marker in old:
        return ""
    sep = "" if old.endswith("\n") or not old else "\n"
    write_text(path, old + sep + "\n" + line + "\n")
    return ""


def k14_positive(tree, lane, base):
    return append_correction(
        tree, "SCORECARD.md", "RD42-1 superseded by this line",
        "Correction (round 43): SCORECARD.md:1634 quotes `corrections=33`; the "
        "value the suite re-derives at this export is `corrections=34`. The 33 "
        "literal is RD42-1 superseded by this line and the line is not rewritten.")


def k14_mutant(tree, lane, base):
    return install_committed(tree, "SCORECARD.md",
                             NARRATIVE[0]["committed"][0][1], lane, base)


def k14_shape(tree, lane, base):
    reason = k14_mutant(tree, lane, base)
    if reason:
        return reason
    return duplicate_then_fix(tree, "SCORECARD.md", "corrections=33",
                              "corrections=33", "corrections=34")


def k15_positive(tree, lane, base):
    log = append_correction(
        tree, "LOG.md", "RD42-2 never-true",
        "Correction (round 43): the LOG.md:1804 note that wave 2 "
        "`kasegi-r42-falsify` was dispatched is RD42-2 never-true: no "
        "`.ufo/waves/round-42/kasegi-r42-falsify-results.json` is committed and "
        "no seat ran; the round total is 64.")
    lesson = append_correction(
        tree, "corpus/lessons/round-42.md", "RD42-3 never-true",
        "Correction (round 43): the wave-2 seat counts in this lesson "
        "(36 dispatched, round total 100) are RD42-3 never-true; wave 2 was "
        "handed off and never taken, and the round total is 64.")
    return log or lesson


def k15_mutant(tree, lane, base):
    for rel, digest in NARRATIVE[1]["committed"]:
        reason = install_committed(tree, rel, digest, lane, base)
        if reason:
            return reason
    return ""


def k15_shape(tree, lane, base):
    reason = k15_mutant(tree, lane, base)
    if reason:
        return reason
    return duplicate_then_fix(tree, "LOG.md", "36 seats dispatched",
                              "36 seats dispatched", "64 seats dispatched")


def k16_positive(tree, lane, base):
    return append_correction(
        tree, "corpus/lessons/round-42.md", "RD42-4 unfulfilled",
        "Correction (round 43): the `## Wave-2 falsification` section of this "
        "lesson is an RD42-4 unfulfilled promise -- no falsify wave report "
        "exists and none will; the section is named superseded history.")


def k16_mutant(tree, lane, base):
    return install_committed(tree, "corpus/lessons/round-42.md",
                             NARRATIVE[2]["committed"][0][1], lane, base)


def k16_shape(tree, lane, base):
    reason = k16_mutant(tree, lane, base)
    if reason:
        return reason
    return duplicate_then_fix(tree, "corpus/lessons/round-42.md",
                              "## Wave-2 falsification",
                              "## Wave-2 falsification",
                              "## Wave-2 falsification (superseded)")


def k17_positive(tree, lane, base):
    rel = ".ufo/waves/round-43/claims-erratum-1.md"
    path = os.path.join(tree, rel)
    if os.path.isfile(path) and "RD42-8" in (read_text(path) or ""):
        return ""
    write_text(path, "\n".join([
        "# Round 43 claims erratum 1",
        "",
        "Erratum E43-1 (claims erratum): `.ufo/waves/round-42/claims.json` C1 "
        "`before` quotes `closed=10/12`; the control it cites, "
        "`.ufo/waves/round-42/c1-controls/do-nothing.txt`, prints "
        "`closed=8/12 exit=1`. The `closed=10/12` literal is RD42-8 superseded "
        "by this erratum; the frozen claims.json bytes are not rewritten.",
        ""]))
    return ""


def k17_mutant(tree, lane, base):
    return install_committed(tree, ".ufo/waves/round-42/claims.json",
                             NARRATIVE[3]["committed"][0][1], lane, base)


def k17_shape(tree, lane, base):
    reason = k17_mutant(tree, lane, base)
    if reason:
        return reason
    return duplicate_then_fix(tree, ".ufo/waves/round-42/claims.json",
                              "closed=10/12", "closed=10/12",
                              "closed=8/12 and closed=10/12")


def k18_positive(tree, lane, base):
    return append_correction(
        tree, "corpus/lessons/round-42-verifier-spotcheck.md", "RD42-5 superseded",
        "Correction (round 43): the `closed=10/13` / `failures=3` values quoted "
        "at line 65 and in `.ufo/waves/round-42/claims-erratum-4.md` have no "
        "committed transcript; the committed red transcript is "
        "`all-gates.pre-repair.txt` (`closed=9/13 exit=1`, `failures=4`). The "
        "quoted values are RD42-5 superseded by this line.")


def k18_mutant(tree, lane, base):
    return install_committed(tree, "corpus/lessons/round-42-verifier-spotcheck.md",
                             NARRATIVE[4]["committed"][0][1], lane, base)


def k18_shape(tree, lane, base):
    reason = k18_mutant(tree, lane, base)
    if reason:
        return reason
    return duplicate_then_fix(tree, "corpus/lessons/round-42-verifier-spotcheck.md",
                              "closed=10/13", "closed=10/13",
                              "closed=9/13 and closed=10/13")


def k19_positive(tree, lane, base):
    """Write the four-line freeze record the check must accept."""
    claims_path = os.path.join(tree, K19_CLAIMS)
    claims_raw = read_bytes(claims_path)
    if claims_raw is None:
        return "absent:%s" % K19_CLAIMS
    try:
        claims = json.loads(claims_raw.decode("utf-8"))
    except ValueError:
        return "unparseable:%s" % K19_CLAIMS
    controls = claims.get("controls") if isinstance(claims, dict) else None
    if not isinstance(controls, dict):
        return "no-controls:%s" % K19_CLAIMS
    measured = []
    for name in ("c1", "c2"):
        rel = controls.get(name)
        text = read_text(os.path.join(tree, rel)) if isinstance(rel, str) else None
        if text is None:
            return "control-absent:%s" % name
        hits = [l.strip()[len("measured-at="):] for l in text.splitlines()
                if l.strip().startswith("measured-at=")]
        if len(hits) != 1:
            return "control-measured-at:%s" % name
        measured.append(hits[0])
    frozen = claims.get("frozen_at_utc")
    base = claims.get("base")
    if not isinstance(frozen, str) or not isinstance(base, str):
        return "claims-fields-missing"
    record = ["frozen-at=%s" % frozen,
              "measured-at-max=%s" % max(measured),
              "claims-sha256=%s" % sha256_bytes(claims_raw),
              "base=%s" % base]
    write_text(os.path.join(tree, K19_FREEZE), "\n".join(record) + "\n")
    return ""


def k19_mutant(tree, lane, base):
    """The committed defect: no round-43 freeze record at base."""
    path = os.path.join(tree, K19_FREEZE)
    if os.path.exists(path):
        os.unlink(path)
    if os.path.exists(path):
        return "remove-failed:%s" % K19_FREEZE
    return ""


def k19_shape(tree, lane, base):
    """The committed stale label: a freeze record that predates its evidence."""
    reason = k19_positive(tree, lane, base)
    if reason:
        return reason
    path = os.path.join(tree, K19_FREEZE)
    text = read_text(path) or ""
    lines = text.split("\n")
    if not lines or not lines[0].startswith("frozen-at="):
        return "freeze-shape:%s" % K19_FREEZE
    lines[0] = "frozen-at=%s" % K19_STALE_LABEL
    write_text(path, "\n".join(lines))
    return ""


BUILDERS = {
    "K14": (k14_positive, k14_mutant, k14_shape),
    "K15": (k15_positive, k15_mutant, k15_shape),
    "K16": (k16_positive, k16_mutant, k16_shape),
    "K17": (k17_positive, k17_mutant, k17_shape),
    "K18": (k18_positive, k18_mutant, k18_shape),
    "K19": (k19_positive, k19_mutant, k19_shape),
}


def duplicate_then_fix(tree, rel, needle, fix_from, fix_to):
    """The R42 shape: duplicate the defect verbatim, then rewrite only its FIRST
    occurrence.  A check that reads one occurrence accepts the tree; the defect
    survives in the duplicate, so the check must stay closed=0.

    Returns "" only when the tree really carries the shape (two occurrences, the
    first rewritten and the second still the committed defect).
    """
    path = os.path.join(tree, rel)
    text = read_text(path)
    if text is None:
        return "absent:%s" % rel
    lines = text.split("\n")
    index = None
    for i, line in enumerate(lines):
        if needle in line:
            index = i
            break
    if index is None:
        return "needle-absent:%s" % rel
    original = lines[index]
    if fix_from not in original:
        return "fix-from-absent:%s" % rel
    rewritten = original.replace(fix_from, fix_to, 1)
    if rewritten == original:
        return "fix-no-op:%s" % rel
    lines.insert(index + 1, original)          # the committed defect, verbatim twice
    lines[index] = rewritten                   # only its first occurrence rewritten
    write_text(path, "\n".join(lines))
    if lines[index + 1] != original or fix_from not in lines[index + 1]:
        return "shape-defect-lost:%s" % rel
    if lines[index] != rewritten or fix_to not in lines[index]:
        return "shape-first-not-rewritten:%s" % rel
    return ""


# ---------------------------------------------------------------------------
# dispatch + probe
# ---------------------------------------------------------------------------

class Dispatcher:
    def __init__(self, template=None, callable_=None, cwd=None):
        self.template = template
        self.callable = callable_
        self.cwd = cwd

    def __call__(self, case_id, tree):
        if self.callable is not None:
            return self.callable(case_id, tree)
        assert self.template is not None
        proc = subprocess.run(["bash", "-c", self.template, "es19",
                               case_id, tree], cwd=self.cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc.stdout.decode("utf-8", "replace")


def parse_line(text, expect_id):
    lines = [line for line in text.splitlines() if line.strip()]
    parsed = None
    for line in lines:
        match = LINE_RX.match(line.strip())
        if match:
            if parsed is not None:
                return None, "multiple-lines"
            parsed = match
    if parsed is None:
        return None, "no-graded-line"
    if parsed.group(1) != expect_id:
        return None, "wrong-id:%s" % parsed.group(1)
    return (parsed.group(2), int(parsed.group(3))), ""


def probe(dispatch, case_id, tree, case_root, work, canaries):
    """One check invocation with the isolation assertions."""
    live = sorted(os.path.join(work, "selftest", d)
                  for d in os.listdir(os.path.join(work, "selftest"))
                  if d.startswith("case-"))
    own = os.path.realpath(case_root)
    structural = (len(live) == 1 and same_path(live[0], own)
                  and inside(tree, own) and not same_path(tree, own))
    text = dispatch(case_id, tree)
    result = {"ok": False, "payload": "", "closed": -1, "reason": "",
              "isolated": structural, "leak": False, "raw": text}
    if not structural:
        result["reason"] = "isolation"
    parsed, reason = parse_line(text, case_id)
    if parsed is None:
        result["reason"] = result["reason"] or reason
        for token in canaries:
            if token in text:
                result["leak"] = True
        return result
    result["payload"], result["closed"] = parsed
    for token in canaries:
        if token in result["payload"]:
            result["leak"] = True
    result["ok"] = True
    return result


def registry(work):
    return os.path.join(work, "selftest")


def case_root(work, case_id):
    return os.path.join(registry(work), "case-%s" % case_id)


def canary_token(case_id):
    return "CANARY-R43-%s-9f2c" % case_id


# ---------------------------------------------------------------------------
# case grading
# ---------------------------------------------------------------------------

def grade_narrative(case, export, work, dispatch, lane, base, transcripts):
    cid = case["id"]
    root = case_root(work, cid)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    token = canary_token(cid)
    write_text(os.path.join(root, "canary-%s.txt" % cid), token + "\n")
    canaries = [canary_token(i) for i in CASE_IDS if i != cid] + [token]

    positive_fn, mutant_fn, shape_fn = BUILDERS[cid]
    facts = {"applied": {"positive": "", "mutant": "", "shape": ""},
             "pos": None, "mut": None, "shape": None, "pos2": None,
             "changed": False, "isolated": False}
    try:
        # positive
        pos = copy_tree(export, os.path.join(root, "pos"))
        facts["applied"]["positive"] = positive_fn(pos, lane, base)
        facts["pos"] = probe(dispatch, cid, pos, root, work, canaries)

        # committed mutant
        mut = copy_tree(export, os.path.join(root, "mut-committed"))
        facts["applied"]["mutant"] = mutant_fn(mut, lane, base)
        facts["mut"] = probe(dispatch, cid, mut, root, work, canaries)
        # The mutant must be the COMMITTED bytes, re-verified after every builder
        # ran -- not merely "different from the export": an export that already
        # carries the defect (base, HEAD-before-landing) changes nothing and is
        # still a faithful mutant.
        if case["committed"]:
            facts["provenance_ok"] = all(
                record_digest(mut, rel) == digest
                for rel, digest in case["committed"])
        else:
            facts["provenance_ok"] = not os.path.exists(
                os.path.join(mut, K19_FREEZE))

        # duplicated-shape mutant (the R42 shape control)
        shp = copy_tree(export, os.path.join(root, "mut-shape"))
        facts["applied"]["shape"] = shape_fn(shp, lane, base)
        facts["shape"] = probe(dispatch, cid, shp, root, work, canaries)

        # second dispatch of the positive tree: determinism / payload drift
        facts["pos2"] = probe(dispatch, cid, pos, root, work, canaries)

        facts["isolated"] = all(
            facts[k] is not None and facts[k]["isolated"]
            for k in ("pos", "mut", "shape", "pos2"))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    facts["isolated"] = facts["isolated"] and not os.path.exists(root)
    return grade_facts(cid, facts, transcripts, expected_mutants=2)


def grade_carried(spec, export, work, dispatch, transcripts, battery):
    cid, _check, _label, _family, _rel, _digest = spec
    root = case_root(work, cid)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    token = canary_token(cid)
    write_text(os.path.join(root, "canary-%s.txt" % cid), token + "\n")
    canaries = [canary_token(i) for i in CASE_IDS if i != cid] + [token]
    facts = {"pos": None, "pos2": None, "isolated": False,
             "battery": (0, 0), "battery_reason": ""}
    try:
        pos = copy_tree(export, os.path.join(root, "pos"))
        facts["pos"] = probe(dispatch, cid, pos, root, work, canaries)
        facts["pos2"] = probe(dispatch, cid, pos, root, work, canaries)
        if battery is None:
            facts["battery_reason"] = "hook-absent"
        else:
            try:
                good, total = battery(export, root)
            except Exception as exc:                  # noqa: BLE001
                facts["battery_reason"] = "hook-error:%s" % type(exc).__name__
                good, total = 0, 0
            facts["battery"] = (int(good), int(total))
        facts["isolated"] = all(facts[k] is not None and facts[k]["isolated"]
                                for k in ("pos", "pos2"))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    facts["isolated"] = facts["isolated"] and not os.path.exists(root)
    return grade_facts(cid, facts, transcripts, expected_mutants=None)


def grade_facts(cid, facts, transcripts, expected_mutants):
    pos, mut, shp, pos2 = facts.get("pos"), facts.get("mut"), \
        facts.get("shape"), facts.get("pos2")
    positive_ok = bool(pos and pos["ok"] and pos["closed"] == 1
                       and not pos["leak"])

    if expected_mutants is None:
        good, total = facts.get("battery", (0, 0))
        mutants_ok = total >= 1 and good == total
        reasons = [] if mutants_ok else [facts.get("battery_reason") or "battery"]
    else:
        mut_ok = bool(mut and mut["ok"] and mut["closed"] == 0
                      and not mut["leak"])
        shape_ok = bool(shp and shp["ok"] and shp["closed"] == 0
                        and not shp["leak"])
        good = int(mut_ok) + int(shape_ok)
        total = expected_mutants
        mutants_ok = good == total
        reasons = []
        if not (mut and mut["ok"]):
            reasons.append("mutant:%s" % (mut["reason"] if mut else "missing"))
        elif mut["closed"] != 0:
            reasons.append("mutant:accepted")
        if not facts.get("provenance_ok"):
            reasons.append("mutant:provenance")
        for name in ("positive", "mutant", "shape"):
            if facts.get("applied", {}).get(name):
                reasons.append("%s:%s" % (name, facts["applied"][name]))
        if not (shp and shp["ok"]):
            reasons.append("shape:%s" % (shp["reason"] if shp else "missing"))
        elif shp["closed"] != 0:
            reasons.append("shape:accepted")

    payload = pos["payload"] if pos and pos["ok"] else ""
    if not positive_ok:
        reasons.append("positive:%s" % (
            "leak" if (pos and pos["leak"]) else
            (pos["reason"] if pos and pos["reason"] else "closed=0")))
    if transcripts is not None:
        want = transcripts.get(cid)
        payload_match = 1 if (want is not None and payload == want) else 0
    else:
        payload_match = 1 if (payload and pos2 and pos2["ok"]
                              and pos2["payload"] == payload
                              and pos2["closed"] == pos["closed"]) else 0
    isolated = bool(facts.get("isolated"))
    if payload_match != 1:
        reasons.append("payload-match")
    if not isolated:
        reasons.append("isolation")
    verdict = (positive_ok and mutants_ok and payload_match == 1 and isolated)
    line = ("selftest case=%s mutants=%d/%d positive=%s payload-match=%d "
            "verdict=%s" % (cid, good, total,
                            "pass" if positive_ok else "fail",
                            payload_match, "pass" if verdict else "fail"))
    return {"id": cid, "line": line, "verdict": verdict,
            "reasons": [r for r in reasons if r][:4],
            "positive": positive_ok, "mutants": (good, total),
            "payload_match": payload_match, "isolated": isolated}


# ---------------------------------------------------------------------------
# transcript acceptor (a summary-only line must never satisfy a case)
# ---------------------------------------------------------------------------

def accept_selftest(text, expect_cases):
    lines = [line for line in text.splitlines() if line.strip()]
    case_lines = [line for line in lines if line.startswith("selftest case=")]
    summaries = [line for line in lines if SUMMARY_RX.match(line)]
    if len(case_lines) != expect_cases or len(summaries) != 1:
        return False, "lines=%d summaries=%d" % (len(case_lines), len(summaries))
    ids = []
    for line in case_lines:
        match = CASE_LINE_RX.match(line)
        if match is None:
            return False, "malformed:%s" % line[:40]
        if match.group(6) != "pass":
            return False, "failed-case:%s" % match.group(1)
        ids.append(match.group(1))
    if len(set(ids)) != len(ids):
        return False, "duplicate-ids"
    match = SUMMARY_RX.match(summaries[0])
    if int(match.group(1)) != expect_cases or int(match.group(2)) != 0:
        return False, "summary:%s" % summaries[0]
    return True, ""


def synthetic_transcript(count):
    lines = ["selftest case=%s mutants=2/2 positive=pass payload-match=1 "
             "verdict=pass" % cid for cid in CASE_IDS[:count]]
    lines.append("selftest cases=%d failures=0" % count)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# degenerate controls
# ---------------------------------------------------------------------------

def stub_dispatch(case_id, _tree):
    return "%s payload=always-pass closed=1" % case_id


def firstonly_dispatch(case_id, tree):
    """A check that reads only the FIRST `corrections=` occurrence of
    SCORECARD.md and its naming: it accepts the positive tree and rejects the
    committed defect, but accepts the duplicated shape mutant whose first
    occurrence was rewritten while the defect survives in the duplicate."""
    if case_id != "K14":
        return "%s payload=first-only closed=0" % case_id
    text = read_text(os.path.join(tree, "SCORECARD.md")) or ""
    named = set()
    for line in text.splitlines():
        if line.startswith(CORRECTION_43):
            named.update("corrections=%s" % m
                         for m in re.findall(r"corrections=(\d+)", line))
    first = None
    for line in text.splitlines():
        if line.startswith(CORRECTION_43):
            continue
        match = re.search(r"corrections=(\d+)", line)
        if match:
            first = match.group(0)
            break
    closed = 1 if first and ("corrections=%s" % first.split("=")[1] in named
                             or first == "corrections=34") else 0
    return "K14 payload=first=%s closed=%d" % (
        first.split("=")[1] if first else "none", closed)


def probe_controls(export, work, dispatch, lane, base):
    results = []

    stub_case = dict(next(c for c in NARRATIVE if c["id"] == "K18"))
    stub_grade = grade_narrative(stub_case, export, work,
                                 Dispatcher(callable_=stub_dispatch), lane, base, None)
    results.append(("D-STUB", "reject",
                    "reject" if not stub_grade["verdict"] else "accept"))

    ok, _why = accept_selftest("selftest cases=19 failures=0\n", NCHECKS)
    results.append(("D-SUMMARY", "reject", "accept" if ok else "reject"))

    dup_case = dict(next(c for c in NARRATIVE if c["id"] == "K14"))
    dup_grade = grade_narrative(dup_case, export, work,
                                Dispatcher(callable_=firstonly_dispatch),
                                lane, base, None)
    results.append(("D-DUPLICATE", "reject",
                    "reject" if not dup_grade["verdict"] else "accept"))

    ok, _why = accept_selftest(synthetic_transcript(NCHECKS), NCHECKS)
    results.append(("ACCEPT", "accept", "accept" if ok else "reject"))
    return results


# ---------------------------------------------------------------------------
# args + main
# ---------------------------------------------------------------------------

def parse_args(argv, require_check_cmd=True):
    opts = {"export": "", "work": "", "scratch_root": "", "check_cmd": "",
            "lane": LANE_DEFAULT, "base_ref": BASE_REF, "cases": "",
            "run_transcript": "", "probe_controls": False, "emit": ""}
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--export", "--work", "--scratch-root", "--check-cmd",
                   "--lane", "--base-ref", "--cases", "--run-transcript",
                   "--emit"):
            if i + 1 >= len(argv):
                sys.stderr.write("ExecSelftest19: %s needs a value\n" % arg)
                return None
            opts[arg[2:].replace("-", "_")] = argv[i + 1]
            i += 2
            continue
        if arg == "--probe-controls":
            opts["probe_controls"] = True
            i += 1
            continue
        if arg in ("-h", "--help"):
            return None
        sys.stderr.write("ExecSelftest19: unexpected argument %s\n" % arg)
        return None
    if not opts["export"] or not os.path.isdir(opts["export"]):
        sys.stderr.write("ExecSelftest19: --export <dir> must name a tree\n")
        return None
    if require_check_cmd and not opts["check_cmd"]:
        sys.stderr.write("ExecSelftest19: --check-cmd TEMPLATE is required "
                         "outside the suite\n")
        return None
    if not opts["work"]:
        root = opts["scratch_root"] or os.environ.get("TMPDIR") or "/tmp"
        opts["work"] = os.path.join(root, "es19-work")
    opts["export"] = os.path.abspath(opts["export"])
    opts["work"] = os.path.abspath(opts["work"])
    os.makedirs(os.path.join(opts["work"], "selftest"), exist_ok=True)
    return opts


def main(argv, dispatch_fn=None):
    """Enter the runner.  Embedded use passes dispatch_fn(case_id, tree) -> str
    (the suite's in-process check); standalone use passes --check-cmd."""
    opts = parse_args(argv, require_check_cmd=dispatch_fn is None)
    if opts is None:
        return 2
    export, work = opts["export"], opts["work"]
    lane, base = opts["lane"], opts["base_ref"]
    dispatch = dispatch_fn or Dispatcher(template=opts["check_cmd"])

    transcripts = None
    if opts["run_transcript"]:
        text = read_text(opts["run_transcript"]) or ""
        transcripts = {}
        for line in text.splitlines():
            match = LINE_RX.match(line.strip())
            if match:
                transcripts[match.group(1)] = match.group(2).split(",replay=")[0]

    if opts["probe_controls"]:
        results = probe_controls(export, work, dispatch, lane, base)
        bad = 0
        for name, expected, observed in results:
            print("control=%s expected=%s observed=%s" % (name, expected, observed))
            if expected != observed:
                bad += 1
        return 0 if bad == 0 else 3

    control_bad = [name for name, expected, observed
                   in probe_controls(export, work, dispatch, lane, base)
                   if expected != observed]
    if control_bad:
        sys.stderr.write("ExecSelftest19: degenerate control accepted: %s\n"
                         % ",".join(control_bad))
        return 3

    selected = CASE_IDS
    if opts["cases"]:
        wanted = [x.strip().upper() for x in opts["cases"].split(",") if x.strip()]
        unknown = [x for x in wanted if x not in CASE_IDS]
        if unknown:
            sys.stderr.write("ExecSelftest19: unknown case %s\n" % unknown[0])
            return 2
        selected = [cid for cid in CASE_IDS if cid in wanted]

    battery = globals().get("CARRIED_BATTERY", {})
    graded = []
    for cid in selected:
        if cid in BUILDERS:
            case = next(c for c in NARRATIVE if c["id"] == cid)
            graded.append(grade_narrative(case, export, work, dispatch, lane, base,
                                          transcripts))
        else:
            spec = next(s for s in CARRIED if s[0] == cid)
            graded.append(grade_carried(spec, export, work, dispatch, transcripts,
                                        battery.get(cid)))

    lines = [case["line"] for case in graded]
    failures = sum(1 for case in graded if not case["verdict"])
    out = lines + ["selftest cases=%d failures=%d" % (len(lines), failures)]
    text = "\n".join(out) + "\n"
    sys.stdout.write(text)
    if opts["emit"]:
        write_text(opts["emit"], text)
    for case in graded:
        if not case["verdict"]:
            sys.stderr.write("ExecSelftest19: %s red: %s\n"
                             % (case["id"], ";".join(case["reasons"])))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
ES19_PY
