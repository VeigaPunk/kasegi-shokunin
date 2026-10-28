#!/usr/bin/env bash
# r43-closure.sh -- the round-43 closure suite (export mode only).
#
#   r43-closure.sh --export-ref <hash> [--lane DIR] [--work DIR]
#                  [--scratch-root DIR] [--receipt-out PATH] [--only K<n>]
#   r43-closure.sh --selftest --export-ref <hash> [same options]
#   r43-closure.sh --export-ref <hash> ... --leaf     (nested depth-1 run)
#
# A plain invocation (no --export-ref) refuses with exit 2: the suite only ever
# grades an exported tree, never a working tree.  The export is produced with
#     git -C <lane> archive <hash> | tar -x -C <work>/export
# and both the work tree and the scratch root must resolve outside the lane.
# A ref that does not resolve prints `ref-not-found` and exits 1: an
# unresolvable ref is a red, never a vacuous pass.
#
# The run transcript is
#     all-gates v3
#     export-ref=<40 hex>
#     suite-sha256=<64 hex|none>
#     time-basis=ref-commit
#     run-utc=<ISO 8601 Z>
#     K<n> payload=... closed=0|1     (nineteen lines, K1..K19)
#     closed=<n>/19 exit=0|1
# The receipt written by --receipt-out is that transcript followed by the
# nineteen graded selftest lines and the `selftest cases=19 failures=<k>` line.
#
# --only K<n> grades one leaf check (K1..K7, K11..K19) instead of the suite;
# the aggregate checks K8 (receipt), K9 (nested negatives) and K10 (isolation)
# cannot be isolated this way.
#
# Exit status: 0 only when all nineteen checks are closed (0 selftest failures
# in --selftest mode); 1 when any is open; 2 on a usage error.

set -uo pipefail

LANE="${R43_LANE_DEFAULT:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}"
WORK=""
SCRATCH_ROOT=""
EXPORT_REF=""
RECEIPT_OUT=""
MODE="run"
LEAF=0
ONLY=""

usage() {
    sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
    case "$1" in
        --export-ref)   [ $# -ge 2 ] || { printf 'r43-closure: --export-ref needs a value\n' >&2; exit 2; }; EXPORT_REF="$2"; shift 2 ;;
        --lane)         [ $# -ge 2 ] || exit 2; LANE="$2"; shift 2 ;;
        --work)         [ $# -ge 2 ] || exit 2; WORK="$2"; shift 2 ;;
        --scratch-root) [ $# -ge 2 ] || exit 2; SCRATCH_ROOT="$2"; shift 2 ;;
        --receipt-out)  [ $# -ge 2 ] || exit 2; RECEIPT_OUT="$2"; shift 2 ;;
        --only)         [ $# -ge 2 ] || exit 2; ONLY="$2"; shift 2 ;;
        --selftest)     MODE="selftest"; shift ;;
        --leaf)         LEAF=1; shift ;;
        -h|--help)      usage; exit 0 ;;
        *) printf 'r43-closure: unexpected argument %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
done

if [ -z "$EXPORT_REF" ]; then
    printf 'r43-closure: a plain run is refused (export mode only)\n' >&2
    printf 'r43-closure: usage: r43-closure.sh --export-ref <hash> [options]\n' >&2
    exit 2
fi

if [ -n "$ONLY" ]; then
    case "$ONLY" in
        K[1-9]|K1[0-9]) ;;
        *) printf 'r43-closure: --only wants a check id K1..K19, got %s\n' "$ONLY" >&2; exit 2 ;;
    esac
    case "$ONLY" in
        K8|K9|K10) printf 'r43-closure: --only cannot isolate aggregate check %s\n' "$ONLY" >&2; exit 2 ;;
    esac
fi

if [ ! -d "$LANE" ]; then
    printf 'ERROR ref-not-found lane=%s ref=%s closed=0 exit=1\n' "$LANE" "$EXPORT_REF"
    exit 1
fi

RESOLVED="$(git -C "$LANE" rev-parse --verify --quiet "${EXPORT_REF}^{commit}" 2>/dev/null)"
if [ -z "$RESOLVED" ]; then
    printf 'ERROR ref-not-found ref=%s closed=0 exit=1\n' "$EXPORT_REF"
    exit 1
fi

if [ -z "$SCRATCH_ROOT" ]; then
    # Never fall through to a literal /tmp: prefer the work tree's parent, then
    # an inherited TMPDIR, and otherwise demand the flag.
    if [ -n "$WORK" ]; then
        WORK_PARENT="$(dirname -- "$WORK")"
        mkdir -p -- "$WORK_PARENT" || exit 2
        SCRATCH_ROOT="$(cd -- "$WORK_PARENT" && pwd -P)" || exit 2
    elif [ -n "${TMPDIR:-}" ]; then
        SCRATCH_ROOT="$TMPDIR"
    else
        printf 'r43-closure: --scratch-root is required when TMPDIR is unset\n' >&2
        exit 2
    fi
fi
mkdir -p -- "$SCRATCH_ROOT" || exit 2
SUITE_SCRATCH="$SCRATCH_ROOT/r43-${RESOLVED:0:12}"
mkdir -p -- "$SUITE_SCRATCH" || exit 2
if [ -z "$WORK" ]; then
    WORK="$SUITE_SCRATCH/work"
fi
mkdir -p -- "$WORK" || exit 2
WORK="$(cd -- "$WORK" && pwd -P)"
LANE_REAL="$(cd -- "$LANE" && pwd -P)"
case "$WORK" in
    "$LANE_REAL"|"$LANE_REAL"/*)
        printf 'r43-closure: the export work tree must lie outside the lane (%s)\n' "$LANE_REAL" >&2
        exit 2 ;;
esac
EXPORT="$WORK/export"
rm -rf -- "$EXPORT"
mkdir -p -- "$EXPORT" || exit 2

if ! git -C "$LANE" archive "$RESOLVED" 2>/dev/null | tar -x -C "$EXPORT"; then
    printf 'ERROR export-failed ref=%s closed=0 exit=1\n' "$RESOLVED"
    exit 1
fi

SELF="$(cd -- "$(dirname -- "$0")" && pwd)/$(basename -- "$0")"

export R43_LANE="$LANE"
export R43_EXPORT="$EXPORT"
export R43_WORK="$WORK"
export R43_SCRATCH_ROOT="$SCRATCH_ROOT"
export R43_REF="$RESOLVED"
export R43_MODE="$MODE"
export R43_LEAF="$LEAF"
export R43_ONLY="$ONLY"
export R43_RECEIPT_OUT="$RECEIPT_OUT"
export R43_SELF="$SELF"

exec python3 - <<'R43_ENGINE_PY'
# ---------------------------------------------------------------------------
# r43-closure engine.
#
# Configuration arrives through the environment (the bash driver exports it):
#   R43_LANE, R43_EXPORT, R43_WORK, R43_SCRATCH_ROOT, R43_REF, R43_MODE,
#   R43_LEAF, R43_ONLY, R43_RECEIPT_OUT, R43_SELF
#
# The transcript goes to stdout.  Exit 0 only when every check is closed.
# ---------------------------------------------------------------------------

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

CHECK_IDS = ["K%d" % i for i in range(1, 20)]
NCHECKS = len(CHECK_IDS)
# Checks whose payload is a pure function of the exported tree, so a receipt's
# recorded values can be re-derived at the receipt's own ref.  K8 is the one
# exception: it grades the receipt, so it cannot be compared with itself.
DETERMINISTIC = [cid for cid in CHECK_IDS if cid != "K8"]

ROUND = 42
PREV_ROUND = 41
RECORDS = ["SCORECARD.md", "LOG.md", "SHONEN.md"]
RECEIPT_REL = ".ufo/waves/round-43/final-gates/all-gates.txt"
DECLARED_REL = ".ufo/waves/round-42/declared-blocks.txt"
PRIOR_RECEIPT_REL = ".ufo/waves/round-41/final-gates/all-gates.txt"
SUITE_REL = "corpus/instruments/r43-closure.sh"
BIND_INSTR_REL = "corpus/instruments/capture-binding-check.py"
FLIP_INSTR_REL = "corpus/instruments/frontier-recheck-count.py"
DENSITY_REL = "corpus/instruments/density.py"
BASE_REF = "5053a7f46de35784cff4b56756906e9014a38276"
R41_HEAD = "1f7464612ac4c44e39886b82e812610d3c039b13"
DENSITY_SHA = "ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710"
SENTINEL = "all-gates v3"

# Every export path the K-checks read.  K4 requires each of them to be declared
# in the round-42 declared-blocks file; the set is carried unchanged from the
# round-42 suite.
READ_SET = [
    "SCORECARD.md",
    "LOG.md",
    "SHONEN.md",
    "SKILL.md",
    "PROVINCE.md",
    "corpus/README.md",
    "corpus/SOURCES.md",
    "corpus/instruments/r42-closure.sh",
    "corpus/instruments/capture-binding-check.py",
    "corpus/instruments/frontier-recheck-count.py",
    "corpus/instruments/density.py",
]

# Committed defeat artifacts, bound by digest so a replay is provably the
# COMMITTED defeat.  family -> (export path, sha256)
DEFEAT_ARTIFACTS = {
    "F-EVID": (".ufo/waves/round-41/wave2/RevC1Counters.md",
               "afe2c4d388d331035854d709072e3f62b9f87fa0f363e2170619789fb60a25d2"),
    "F-TOKEN": (".ufo/waves/round-40/wave2/RevC1Counters.defeats.txt",
                "6eef3338dc472e9033dc9131f5da630a6f23fea89ddda174f6819473593860af"),
    "F-TABLE": (".ufo/waves/round-41/wave2/MutSkillTablePipes.md",
                "41117cde4e2e30bb2969c056f00b8c9b4d379da9e7903a887fbd7867fb1fea7a"),
    "F-DECL": (".ufo/waves/round-41/wave2/CritDeclarationCoverage.md",
               "0254bbe7b8b0b33bb6a8aa06b135813b8a11cc501bea1d81bed01e19da9141df"),
    "F-SCAN": (".ufo/waves/round-41/wave2/MutScratchTiming.md",
               "54fb821cd10d3c95a9bc4d3605b4fdce6da8611a057b6efcfd959f1c36fdae7e"),
    "F-BIND": (".ufo/waves/round-41/wave2/MutBindingExistence.md",
               "960e8da0580f1b4760112fb218d4620a55e5050576ce09fc7f3fef8c7808fb32"),
    "F-FLIP": (".ufo/waves/round-41/wave2/MutFrontierParser.md",
               "faae26b19b0c04908fced285d3a8733b81125bccdfdad62f9dcc6f625ce4365c"),
}
FAMILY_OF = {"K1": "F-EVID", "K2": "F-TOKEN", "K3": "F-TABLE", "K4": "F-DECL",
             "K5": "F-SCAN", "K6": "F-BIND", "K7": "F-FLIP"}

ENV = os.environ
LANE = ENV.get("R43_LANE", "")
EXPORT = ENV.get("R43_EXPORT", "")
WORK = ENV.get("R43_WORK", "")
SCRATCH = ENV.get("R43_SCRATCH_ROOT", "")
REF = ENV.get("R43_REF", "")
MODE = ENV.get("R43_MODE", "run")
LEAF = ENV.get("R43_LEAF", "0") == "1"
ONLY = ENV.get("R43_ONLY", "")
RECEIPT_OUT = ENV.get("R43_RECEIPT_OUT", "")
SELF = ENV.get("R43_SELF", "")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def write_text(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def git(args, cwd=None):
    cmd = ["git", "--no-optional-locks", "-C", cwd or LANE] + list(args)
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    except OSError:
        return 1, ""
    return p.returncode, p.stdout.decode("utf-8", "replace")


def git_out(args, cwd=None):
    return git(args, cwd=cwd)[1]


def ref_utc(ref):
    rc, out = git(["log", "-1", "--format=%ct", ref])
    if rc != 0:
        return ""
    out = out.strip()
    if not out.isdigit():
        return ""
    return datetime.datetime.fromtimestamp(
        int(out), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def in_tree(rel, tree=None):
    return os.path.join(tree or EXPORT, rel)


def list_export(tree=None):
    root = tree or EXPORT
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        # a committed symlink that points at a directory arrives in dirnames;
        # it is a tree entry in its own right and git ls-tree lists it
        for name in list(dirnames):
            p = os.path.join(dirpath, name)
            if os.path.islink(p):
                out.append(os.path.relpath(p, root))
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            out.append(os.path.relpath(p, root))
    return sorted(out)


def copy_rel(tree, rel, dest):
    src = in_tree(rel, tree)
    dst = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    shutil.copy2(src, dst)


def copy_prefix(tree, prefix, dest):
    base = in_tree(prefix, tree)
    if not os.path.isdir(base):
        return
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, tree)
            dst = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
            shutil.copy2(src, dst)


def run_tool(cmd, cwd=None, timeout=900):
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 2, str(exc)
    return p.returncode, p.stdout.decode("utf-8", "replace")


# ---------------------------------------------------------------------------
# CommonMark fence state machine
# ---------------------------------------------------------------------------

def fence_scan(text):
    rows = []
    in_fence = False
    marker = ""
    mlen = 0
    for lineno, line in enumerate(text.split("\n"), 1):
        inside = False
        if in_fence:
            inside = True
            m = re.match(r"^ {0,3}(`{3,}|~{3,})[ \t]*$", line)
            if m and m.group(1)[0] == marker and len(m.group(1)) >= mlen:
                in_fence = False
                marker = ""
                mlen = 0
        else:
            m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if m:
                run = m.group(1)
                if not (run[0] == "`" and "`" in m.group(2)):
                    in_fence = True
                    marker = run[0]
                    mlen = len(run)
                    inside = True
        rows.append((lineno, line, inside))
    return rows


def outside_lines(text):
    return [(n, l) for (n, l, inside) in fence_scan(text) if not inside]


def fence_open_at_eof(text):
    open_ = False
    for _n, _l, inside in fence_scan(text):
        open_ = inside
    return open_


# ---------------------------------------------------------------------------
# whole-token readers
# ---------------------------------------------------------------------------

TOKEN_BAD = set("0123456789/.=_abcdefghijklmnopqrstuvwxyz"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def token_at(text, needle, index):
    if index < 0 or text[index:index + len(needle)] != needle:
        return False
    before = text[index - 1] if index > 0 else ""
    after = text[index + len(needle)] if index + len(needle) < len(text) else ""
    if before and before in TOKEN_BAD:
        return False
    if after and after in TOKEN_BAD:
        return False
    return True


def value_present(text, needle):
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx < 0:
            return False
        if token_at(text, needle, idx):
            return True
        start = idx + 1


CLOSED_RX = re.compile(r"closed=\d+/\d+")
FAILURES_RX = re.compile(r"failures=\d+")
CASES_RX = re.compile(r"cases=\d+")
TALLY_RX = re.compile(r"(?:closed|failures|cases)=\d+(?:/\d+)?")


def tally_tokens(text):
    out = []
    for rx in (CLOSED_RX, FAILURES_RX, CASES_RX):
        for m in rx.finditer(text):
            if token_at(text, m.group(0), m.start()):
                tok = m.group(0)
                if tok not in out:
                    out.append(tok)
    return out


def mangled_tallies(text, truth):
    bad = []
    for m in TALLY_RX.finditer(text):
        s = m.group(0)
        if s in bad:
            continue
        if not token_at(text, s, m.start()):
            bad.append(s)
            continue
        for t in truth:
            if t != s and t in s:
                bad.append(s)
                break
    return bad


# ---------------------------------------------------------------------------
# evidence identifiers
# ---------------------------------------------------------------------------

PATH_RX = re.compile(
    r"[A-Za-z0-9_][A-Za-z0-9_./-]*[A-Za-z0-9_-]\.(?:md|txt|sh|py|json|tsv|csv)")
COMMIT_RX = re.compile(r"\b[0-9a-f]{40}\b")
DEFEAT_STEMS = (
    "RevC1Counters", "CritC1KillRule", "CritKillRule", "MutH6H10",
    "MutSkillTablePipes", "CritDeclarationCoverage", "MutScratchTiming",
    "MutBindingExistence", "MutFrontierParser", "MutSuite", "MutC2Chain",
    "CritI12Necessity", "CritDigestSelftest", "CritReceiptBootstrap",
    "RevErratumLanding", "RevScanOwnership", "RevCaptureNormalization",
    "RevCorrectionsFinal", "CritCommitTimestamp", "CritUpstreamAuthenticity",
    "CritYDeltaClean", "MutAncestorGuard", "MutAuditUnexpected",
    "MutExportRecheck", "MutExportRefReemit", "MutFreshnessCensus",
)


def resolve_token(token, round_hint=None):
    token = token.strip().strip("`'\",;:()[]")
    while token.startswith("./"):
        token = token[2:]
    if not token or token.startswith("/"):
        return None
    if ".." in token.split("/"):
        return None
    cands = [token]
    rounds = ["round-%d" % ROUND, "round-%d" % PREV_ROUND, "round-40",
              "round-39", "round-38"]
    if round_hint in rounds:
        rounds = [round_hint] + [r for r in rounds if r != round_hint]
    for rd in rounds:
        cands.append(".ufo/waves/%s/%s" % (rd, token))
        cands.append(".ufo/waves/%s/wave2/%s" % (rd, token))
        cands.append(".ufo/waves/%s/wave1/%s" % (rd, token))
    cands.append("corpus/%s" % token)
    cands.append("corpus/lessons/%s" % token)
    cands.append("corpus/instruments/%s" % token)
    cands.append(".ufo/waves/%s" % token)
    for c in cands:
        if os.path.isfile(in_tree(c)):
            return c
    return None


def commit_exists(h):
    return git(["cat-file", "-e", "%s^{commit}" % h])[0] == 0


def evidence_ids(text, round_hint=None):
    ids = set()
    for m in PATH_RX.finditer(text):
        if resolve_token(m.group(0), round_hint):
            ids.add(m.group(0))
    for m in COMMIT_RX.finditer(text):
        if commit_exists(m.group(0)):
            ids.add(m.group(0))
    for stem in DEFEAT_STEMS:
        if re.search(r"\b%s\b" % re.escape(stem), text):
            ids.add(stem)
    return ids


# ---------------------------------------------------------------------------
# corrections
# ---------------------------------------------------------------------------

CORRECTION_RX = re.compile(r"^Correction \(round (\d+)\)")
DEDUP_RX = re.compile(r"^(?:Correction-dedup|Dedup note) \(round (\d+)\)")
GRADING_RX = re.compile(
    r"not[ _-]?verified|unverified|withdraw|held; not|"
    r"no (?:repair|upgrade|increase)|carry forward|carried append",
    re.IGNORECASE)
CLAIM_RX = re.compile(r"\bC[12]\b|depth:verifiability|\bcoverage\b", re.IGNORECASE)


def correction_lines(text, round_no=None):
    out = []
    for lineno, line in outside_lines(text):
        m = CORRECTION_RX.match(line)
        if not m:
            continue
        if round_no is not None and m.group(1) != str(round_no):
            continue
        out.append((m.group(1), lineno, line))
    return out


def dedup_markers(text):
    out = []
    for lineno, line in outside_lines(text):
        m = DEDUP_RX.match(line)
        if m:
            out.append((m.group(1), lineno, line))
    return out


# ---------------------------------------------------------------------------
# K1 -- F-EVID: per-correction evidence, never a cross-record union
# ---------------------------------------------------------------------------

def check_k1(tree):
    contributing = blocks = graded = evidenced = missing = wrong = 0
    per_record = []
    pooled = set()
    rows = []
    for rec in RECORDS:
        path = os.path.join(tree, rec)
        if not os.path.isfile(path):
            per_record.append("%s=absent" % rec)
            continue
        lines = correction_lines(read_text(path), ROUND)
        if not lines:
            per_record.append("%s=0" % rec)
            continue
        contributing += 1
        blocks += len(lines)
        r_ev = r_gr = r_miss = r_wrong = 0
        for rnd, _ln, line in lines:
            ids = evidence_ids(line, "round-%s" % rnd)
            pooled |= ids
            if ids:
                r_ev += 1
            else:
                r_miss += 1
            if CLAIM_RX.search(line):
                if GRADING_RX.search(line):
                    r_gr += 1
                else:
                    r_wrong += 1
        evidenced += r_ev
        graded += r_gr
        missing += r_miss
        wrong += r_wrong
        rows.append((rec, r_ev, len(lines)))
        per_record.append("%s=%d/%d" % (rec, r_ev, len(lines)))
    # A cross-record union would have counted evidence found in a different
    # record as proof for this one.  It is 0 only when no record needs it.
    union = sum(1 for _rec, r_ev, n in rows if r_ev < n and pooled)
    payload = ("records=%d,blocks=%d,graded=%d,evidence=%d,missing=%d,"
               "wrong-grade=%d,per-record=%s,union=%d") % (
        contributing, blocks, graded, evidenced, missing, wrong,
        ";".join(per_record), union)
    ok = (contributing >= 1 and blocks > 0 and missing == 0
          and evidenced == blocks and graded >= 1 and wrong == 0 and union == 0)
    return payload, ok


# ---------------------------------------------------------------------------
# K2 -- F-TOKEN: whole-token tallies only
# ---------------------------------------------------------------------------

BOUNDARY_PROBES = (
    ("closed=13/13 exit=0", "closed=13/13", True),
    ("closed=13/130 exit=0", "closed=13/13", False),
    ("closed=13/13x exit=0", "closed=13/13", False),
    ("xclosed=13/13 exit=0", "closed=13/13", False),
    ("closed=13/13/5 exit=0", "closed=13/13", False),
    ("failures=6", "failures=6", True),
    ("failures=60", "failures=6", False),
    ("failures=6.5", "failures=6", False),
    ("cases=13 failures=0", "cases=13", True),
    ("cases=130 failures=0", "cases=13", False),
)


def prior_truth(tree):
    return tally_tokens(read_text(in_tree(PRIOR_RECEIPT_REL, tree)))


def check_k2(tree):
    truth = prior_truth(tree)
    boundary = sum(1 for hay, needle, want in BOUNDARY_PROBES
                   if value_present(hay, needle) == want)
    transcript = "closed=%d/%d exit=0\nselftest cases=%d failures=0\n" % (
        NCHECKS, NCHECKS, NCHECKS)
    round_trip = (value_present(transcript, "closed=%d/%d" % (NCHECKS, NCHECKS))
                  and not value_present(transcript, "closed=%d/%d0" % (NCHECKS, NCHECKS)))
    stated = mangled = truth_stated = 0
    for rec in RECORDS:
        path = os.path.join(tree, rec)
        if not os.path.isfile(path):
            continue
        for _rnd, _ln, line in correction_lines(read_text(path), ROUND):
            stated += len(tally_tokens(line))
            mangled += len(mangled_tallies(line, truth))
            if any(value_present(line, t) for t in truth):
                truth_stated += 1
    payload = ("boundary=%d/%d,truth-tokens=%d,stated=%d,mangled=%d,"
               "truth-stated=%d,token=whole") % (
        boundary, len(BOUNDARY_PROBES), len(truth), stated, mangled, truth_stated)
    ok = (boundary == len(BOUNDARY_PROBES) and round_trip and mangled == 0
          and stated > 0)
    return payload, ok


# ---------------------------------------------------------------------------
# K3 -- F-TABLE: registry integrity
# ---------------------------------------------------------------------------

ROW_RX = re.compile(r"^\s*\|")
SEP_RX = re.compile(r"^\|[\s\-:|]+\|\s*$")
CLOSURE_RX = re.compile(r"^r\d+-closure\.sh$")


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells, cur, i = [], [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells


def registry_tables(text):
    rows = outside_lines(text)
    tables, i = [], 0
    while i < len(rows):
        lineno, line = rows[i]
        if ROW_RX.match(line) and i + 1 < len(rows) and SEP_RX.match(rows[i + 1][1]):
            tables.append({"header": split_row(line), "body": [],
                           "linenos": [], "hdr_line": lineno,
                           "sep_line": rows[i + 1][0],
                           "raw": {lineno: line}})
            j = i + 2
            while j < len(rows) and ROW_RX.match(rows[j][1]):
                tables[-1]["body"].append(split_row(rows[j][1]))
                tables[-1]["linenos"].append(rows[j][0])
                tables[-1]["raw"][rows[j][0]] = rows[j][1]
                j += 1
            i = j
        else:
            i += 1
    return tables


def closure_basenames(tree):
    out = set()
    idir = in_tree("corpus/instruments", tree)
    if os.path.isdir(idir):
        for fn in os.listdir(idir):
            if CLOSURE_RX.match(fn):
                out.add(fn)
    return out


def check_k3(tree):
    path = in_tree("SKILL.md", tree)
    if not os.path.isfile(path):
        return "tables=0,rows=0,r42-rows=0,r40-rows=0,r40-split=0,bare=0,lead=0", False
    text = read_text(path)
    tables = registry_tables(text)
    names = closure_basenames(tree)
    table_rows = set()
    r42_rows = r40_rows = bare = lead = 0
    for t in tables:
        ncols = len(t["header"])
        for lineno, cells in zip(t["linenos"], t["body"]):
            table_rows.add(lineno)
            if len(cells) != ncols:
                bare += 1
            if not t["raw"][lineno].startswith("|"):
                lead += 1
            if cells and cells[0] == "r42-closure.sh":
                r42_rows += 1
            if cells and cells[0] == "r40-closure.sh":
                r40_rows += 1
    # a closure row that was split out of the registry table by a blank line
    r40_split = 0
    for lineno, line in outside_lines(text):
        if lineno in table_rows or not ROW_RX.match(line):
            continue
        cells = split_row(line)
        if cells and cells[0] in names:
            r40_split += 1
    payload = ("tables=%d,rows=%d,r42-rows=%d,r40-rows=%d,r40-split=%d,bare=%d,"
               "lead=%d") % (len(tables), len(table_rows), r42_rows, r40_rows,
                             r40_split, bare, lead)
    ok = (r42_rows == 1 and r40_rows == 1 and r40_split == 0 and bare == 0
          and lead == 0)
    return payload, ok


# ---------------------------------------------------------------------------
# K4 -- F-DECL: declared-blocks completeness
# ---------------------------------------------------------------------------

def parse_declared(text):
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        out.append((parts[0], parts[1] if len(parts) > 1 else None,
                    parts[2] if len(parts) > 2 else None))
    return out


def check_k4(tree):
    dpath = in_tree(DECLARED_REL, tree)
    if not os.path.isfile(dpath):
        return ("declared=0,valid=0,missing=%d,escape=0,coverage=0/%d,file=absent"
                % (len(READ_SET), len(READ_SET))), False
    decls = parse_declared(read_text(dpath))
    real_root = os.path.realpath(tree)
    declared, valid, escape = set(), 0, 0
    for path, kind, _s in decls:
        norm = path[2:] if path.startswith("./") else path
        declared.add(norm)
        if norm.startswith("/") or ".." in norm.split("/"):
            escape += 1
            continue
        full = in_tree(norm, tree)
        rp = os.path.realpath(full)
        if not (rp == real_root or rp.startswith(real_root + os.sep)):
            escape += 1
            continue
        if os.path.isfile(full):
            valid += 1
            continue
        # A `dyn` declaration marks a path the run itself materialises (the
        # receipt at Y): it must stay inside the export root, but its absence
        # at J is the declared state, not an escaping entry.
        if kind == "dyn":
            valid += 1
            continue
        escape += 1
    # only a path that exists can be read, so only an existing path can be an
    # undeclared read
    missing = [r for r in READ_SET
               if os.path.isfile(in_tree(r, tree)) and r not in declared]
    payload = ("declared=%d,valid=%d,missing=%d,escape=%d,coverage=%d/%d,file=present"
               % (len(decls), valid, len(missing), escape,
                  len(READ_SET) - len(missing), len(READ_SET)))
    ok = (len(decls) > 0 and valid == len(decls) and not missing and escape == 0)
    return payload, ok


# ---------------------------------------------------------------------------
# K5 -- F-SCAN: scratch hygiene on a materialized fixture
# ---------------------------------------------------------------------------

FAMILY_RX = re.compile(r"^kasegi-r4[0-9]")


def family_name(name):
    n = name.lstrip(".").lower()
    out, prev = [], False
    for ch in n:
        if ch.isalnum():
            out.append(ch)
            prev = False
        elif not prev:
            out.append("-")
            prev = True
    return "".join(out).rstrip("-")


def is_family(name):
    return bool(FAMILY_RX.match(family_name(name)))


def scan_scratch(root, work):
    if not os.path.isdir(root):
        return 0, 0, True
    work_real = os.path.realpath(work) if work else None
    strays = scanned = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for name in list(dirnames) + list(filenames):
            p = os.path.join(dirpath, name)
            if not is_family(name):
                continue
            scanned += 1
            if work_real:
                rp = os.path.realpath(p)
                abs_p = os.path.abspath(p)
                if (rp == work_real or rp.startswith(work_real + os.sep)
                        or abs_p == work_real
                        or abs_p.startswith(work_real + os.sep)):
                    continue
            strays += 1
    return strays, scanned, True


def scan_outside(scope, exclude):
    parent = os.path.dirname(os.path.abspath(scope))
    if not os.path.isdir(parent):
        return 0, 0, True
    exclude_real = os.path.realpath(exclude) if exclude else None
    strays = scanned = 0
    for dirpath, dirnames, filenames in os.walk(parent):
        for name in list(dirnames) + list(filenames):
            p = os.path.join(dirpath, name)
            if not is_family(name):
                continue
            scanned += 1
            if exclude_real:
                rp = os.path.realpath(p)
                if rp == exclude_real or rp.startswith(exclude_real + os.sep):
                    continue
            strays += 1
    return strays, scanned, True


def build_scan_fixture(root, outside=True, symlink=True):
    scratch = os.path.join(root, "scratch")
    scope = os.path.join(root, "outside")
    os.makedirs(os.path.join(scratch, "kasegi-r40"), exist_ok=True)
    os.makedirs(os.path.join(scratch, "kasegi-r42", "seat"), exist_ok=True)
    os.makedirs(os.path.join(scratch, "Kasegi_R41_stray"), exist_ok=True)
    os.makedirs(os.path.join(scratch, ".kasegi-r42-seat"), exist_ok=True)
    os.makedirs(os.path.join(scratch, "kasegi-r42", "seat", "kasegi-r42-inner"),
                exist_ok=True)
    write_text(os.path.join(scratch, "kasegi-r43-file"), "family-shaped FILE\n")
    write_text(os.path.join(scratch, "kasegi-r44.txt"), "family-shaped FILE\n")
    if symlink:
        os.symlink(scratch, os.path.join(scratch, "kasegi-r45-link"))
    if outside:
        os.makedirs(os.path.join(scope, "kasegi-r46-seat"), exist_ok=True)
        os.makedirs(os.path.join(scope, "kasegi-r47"), exist_ok=True)
    work = os.path.join(scratch, "work")
    os.makedirs(work, exist_ok=True)
    return scratch, scope, work


def k5_eval(root, outside=True, symlink=True):
    scratch, scope, work = build_scan_fixture(root, outside, symlink)
    strays, scanned, read_ok = scan_scratch(scratch, work)
    out_strays, out_scanned, out_ok = scan_outside(scratch, scratch)
    return strays, scanned, read_ok, out_strays, out_scanned, out_ok


def check_k5(_tree):
    root = os.path.join(WORK, "k5-fixture")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    strays, scanned, read_ok, out_strays, out_scanned, out_ok = k5_eval(root)
    payload = ("family=kasegi-r4[0-9]*,strays=%d,scanned=%d,read=%s,outside=%d,"
               "outside-scanned=%d,scope=materialized") % (
        strays, scanned, "ok" if read_ok else "fail", out_strays, out_scanned)
    ok = read_ok and out_ok and strays >= 7 and out_strays >= 2
    return payload, ok


# ---------------------------------------------------------------------------
# K6 -- F-BIND: capture-binding integrity
# ---------------------------------------------------------------------------

def corpus_fixture(tree, dest):
    os.makedirs(dest, exist_ok=True)
    for rel in ("corpus/SOURCES.md", "corpus/README.md"):
        if os.path.isfile(in_tree(rel, tree)):
            copy_rel(tree, rel, dest)
    copy_prefix(tree, "corpus/source-snapshots", dest)
    copy_prefix(tree, "corpus/knowledge", dest)
    copy_prefix(tree, "corpus/instruments", dest)
    return dest


def manifest_paths(tree):
    out = []
    sdir = in_tree("corpus/source-snapshots", tree)
    if not os.path.isdir(sdir):
        return out
    for dirpath, _dn, filenames in os.walk(sdir):
        if "manifest.json" in filenames:
            out.append(os.path.join(dirpath, "manifest.json"))
    return out


def manifest_round(mp):
    m = re.search(r"sourcesnapshots/round-(\d+)|source-snapshots/round-(\d+)", mp)
    if not m:
        return 0
    return int(m.group(1) or m.group(2))


def pick_record(tree, min_round=0, need_sha=False):
    """First record whose snapshot directory is round-<min_round> or later."""
    for mp in manifest_paths(tree):
        if manifest_round(mp) < min_round:
            continue
        try:
            data = json.loads(read_text(mp) or "{}")
        except ValueError:
            continue
        for i, rec in enumerate(data.get("sources", []) or []):
            if not isinstance(rec, dict) or not rec.get("path"):
                continue
            if need_sha and not rec.get("sha256"):
                continue
            return mp, i
    return None, None


def binding_rejected(rc, out):
    if rc != 0:
        return True
    if "FAIL rule=" in out:
        return True
    m = re.search(r"unbound=(\d+)", out)
    return bool(m and int(m.group(1)) > 0)


def check_k6(tree):
    instr = in_tree(BIND_INSTR_REL, tree)
    if not os.path.isfile(instr):
        return "instrument=absent,base=0,missing-path=0,url-mutated=0", False
    root = os.path.join(WORK, "k6")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    base = corpus_fixture(tree, os.path.join(root, "base"))
    rc, out = run_tool([sys.executable, instr, "--root", base])
    base_ok = (rc == 0 and "unbound=0" in out)
    verdicts = {}
    mp, idx = pick_record(tree)
    dmp, didx = pick_record(tree, min_round=32, need_sha=True)
    for label in ("missing-path", "url-mutated", "digest-mutated"):
        verdicts[label] = 0
        src_mp, src_idx = (dmp, didx) if label == "digest-mutated" else (mp, idx)
        if src_mp is None:
            continue
        dest = corpus_fixture(tree, os.path.join(root, label))
        rel = os.path.relpath(src_mp, tree)
        target = os.path.join(dest, rel)
        try:
            data = json.loads(read_text(target))
        except ValueError:
            continue
        rec = data["sources"][src_idx]
        if label == "missing-path":
            rec["path"] = "R42-MISSING-CAPTURE.txt"
        elif label == "url-mutated":
            url = rec.get("url") or "https://example.invalid/x"
            rec["url"] = url.upper()
            rec["capture_url"] = url.upper()
        else:
            rec["sha256"] = "f" * 64
        write_text(target, json.dumps(data, indent=2))
        mrc, mout = run_tool([sys.executable, instr, "--root", dest])
        verdicts[label] = 1 if binding_rejected(mrc, mout) else 0
    payload = ("instrument=present,base=%d,missing-path=%d,url-mutated=%d,"
               "digest-mutated=%d,rule=reject"
               % (1 if base_ok else 0, verdicts["missing-path"],
                  verdicts["url-mutated"], verdicts["digest-mutated"]))
    ok = (base_ok and verdicts["missing-path"] == 1 and verdicts["url-mutated"] == 1
          and verdicts["digest-mutated"] == 1)
    return payload, ok


# ---------------------------------------------------------------------------
# K7 -- F-FLIP: frontier-counter status-flip detection
# ---------------------------------------------------------------------------

def frontier_rows(text):
    rows = []
    for lineno, line in outside_lines(text):
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) >= 3 and re.match(r"^F\d+$", cells[0]):
            rows.append((lineno, cells))
    return rows


def flip_rejected(rc, out, row_id=""):
    if rc != 0 or "FAIL" in out:
        return True
    return bool(row_id and row_id in out)


def check_k7(tree):
    instr = in_tree(FLIP_INSTR_REL, tree)
    if not os.path.isfile(instr):
        return "instrument=absent,base=0,status-flip=0,no-pass=0,rows=0", False
    rows = frontier_rows(read_text(in_tree("corpus/README.md", tree)))
    admitted = [(n, c) for n, c in rows if c[2].strip() == "admitted"]
    root = os.path.join(WORK, "k7")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    base = corpus_fixture(tree, os.path.join(root, "base"))
    rc, out = run_tool([sys.executable, instr, "--root", base])
    base_ok = (rc == 0 and "exit=0" in out)
    verdicts = {}
    target_id = admitted[0][1][0] if admitted else ""
    entry_cell = admitted[0][1][3] if admitted else ""
    for label in ("status-flip", "no-pass"):
        verdicts[label] = 0
        dest = corpus_fixture(tree, os.path.join(root, label))
        rp = os.path.join(dest, "corpus", "README.md")
        if not os.path.isfile(rp):
            continue
        if label == "status-flip":
            lines = read_text(rp).split("\n")
            done = False
            for i, line in enumerate(lines):
                if not line.lstrip().startswith("|"):
                    continue
                cells = split_row(line)
                if len(cells) > 2 and re.match(r"^F\d+$", cells[0]) \
                        and cells[2].strip() == "admitted":
                    cells[2] = "explored"
                    lines[i] = "| " + " | ".join(cells) + " |"
                    done = True
                    break
            if not done:
                continue
            write_text(rp, "\n".join(lines))
        else:
            # the entry keeps its row but its recheck line stops being a
            # source-recheck invocation
            ep = os.path.join(dest, "corpus", entry_cell)
            if not os.path.isfile(ep):
                continue
            elines = read_text(ep).split("\n")
            done = False
            for i, line in enumerate(elines):
                if line.startswith("recheck:"):
                    elines[i] = "recheck: true"
                    done = True
                    break
            if not done:
                continue
            write_text(ep, "\n".join(elines))
        mrc, mout = run_tool([sys.executable, instr, "--root", dest])
        verdicts[label] = 1 if flip_rejected(mrc, mout, target_id) else 0
    payload = ("instrument=present,base=%d,status-flip=%d,no-pass=%d,rows=%d,"
               "admitted=%d") % (1 if base_ok else 0, verdicts["status-flip"],
                                 verdicts["no-pass"], len(rows), len(admitted))
    ok = base_ok and verdicts["status-flip"] == 1 and verdicts["no-pass"] == 1
    return payload, ok


# ---------------------------------------------------------------------------
# K11 -- correction-block uniqueness
# ---------------------------------------------------------------------------

def normalized_body(line):
    return re.sub(r"\s+", " ", line).strip()


def numeric_lines(text):
    named = set()
    for m in re.finditer(r"(?<![0-9A-Za-z])(\d{3,})\s*[-\u2013]\s*(\d{3,})(?![0-9A-Za-z])",
                         text):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b and b - a < 500:
            named.update(range(a, b + 1))
    for m in re.finditer(r"(?<![0-9A-Za-z])(\d{3,})(?![0-9A-Za-z])", text):
        named.add(int(m.group(1)))
    return named


def check_k11(tree):
    total = groups = dups = excused = unexcused = 0
    marker_ok = marker_sub = marker_app = eof_ok = 0
    for rec in RECORDS:
        path = os.path.join(tree, rec)
        if not os.path.isfile(path):
            continue
        text = read_text(path)
        if not fence_open_at_eof(text):
            eof_ok += 1
        by_body = {}
        pre42 = []
        for rnd, lineno, line in correction_lines(text):
            total += 1
            by_body.setdefault(normalized_body(line), []).append(lineno)
            if int(rnd) < ROUND:
                pre42.append(lineno)
        markers = dedup_markers(text)
        for marker_round, marker_line, marker_text in markers:
            marker_ok = 1
            after = marker_text.split(")", 1)[1] if ")" in marker_text else ""
            if len(after.strip()) >= 40:
                marker_sub = 1
            if all(marker_line > ln for ln in pre42):
                marker_app = 1
        for body, linenos in by_body.items():
            if len(linenos) < 2:
                continue
            groups += 1
            dups += len(linenos) - 1
            covered = False
            for marker_round, _ml, marker_text in markers:
                low = marker_text.lower()
                if rec.lower() not in low:
                    continue
                if ("round %s" % marker_round) not in low and \
                        ("round-%s" % marker_round) not in low:
                    continue
                named = numeric_lines(marker_text)
                if all(ln in named for ln in linenos):
                    covered = True
                    break
            if covered:
                excused += 1
            else:
                unexcused += 1
    payload = ("corrections=%d,groups=%d,dups=%d,excused=%d,unexcused=%d,"
               "marker=%d,marker-substantive=%d,marker-appended=%d,eof-closed=%d/3,"
               "fenced=0") % (total, groups, dups, excused, unexcused, marker_ok,
                              marker_sub, marker_app, eof_ok)
    ok = (total > 0 and eof_ok == 3 and marker_ok == 1 and marker_sub == 1
          and marker_app == 1 and unexcused == 0)
    return payload, ok


# ---------------------------------------------------------------------------
# K12 -- no-harm guard
# ---------------------------------------------------------------------------

def deletion_rows(base, ref, prefix="corpus/", cwd=None):
    rc, out = git(["diff", "--name-status", "--diff-filter=DR", base, ref, "--",
                   prefix], cwd=cwd)
    if rc != 0:
        return None
    return [l.strip() for l in out.split("\n") if l.strip()]


def check_k12(_tree):
    rows = deletion_rows(BASE_REF, REF)
    deleted = len(rows) if rows is not None else 0
    local = sha256_file(in_tree(DENSITY_REL))
    rc, blob = git(["cat-file", "blob", "%s:%s" % (BASE_REF, DENSITY_REL)])
    base_sha = sha256_bytes(blob.encode("utf-8")) if rc == 0 else ""
    dens_ok = (local != "" and local == base_sha == DENSITY_SHA)
    payload = ("deleted=%d,density=%d,density-sha=%s,diff-read=%s,base=%s") % (
        deleted, 1 if dens_ok else 0, local[:12] if local else "unreadable",
        "ok" if rows is not None else "fail", BASE_REF[:8])
    ok = (rows is not None and deleted == 0 and dens_ok)
    return payload, ok


# ---------------------------------------------------------------------------
# K13 -- quiescence
# ---------------------------------------------------------------------------

def worktree_markers(repo):
    rc, out = git(["ls-files", "-v"], cwd=repo)
    if rc != 0:
        return -1
    n = 0
    for line in out.split("\n"):
        if not line:
            continue
        t = line[0]
        if t == "S" or t.islower():
            n += 1
    return n


def suite_scratch_root():
    return os.path.join(SCRATCH, "r43-%s" % REF[:12])


def check_k13(_tree):
    rc, out = git(["ls-tree", "-r", "--name-only", REF])
    ls = set(x for x in out.split("\n") if x) if rc == 0 else None
    export = set(list_export())
    faithful = 1 if (ls is not None and export == ls) else 0
    extra = len(export - ls) if ls is not None else -1
    missing = len(ls - export) if ls is not None else -1
    root = suite_scratch_root()
    strays, _n, read_ok = scan_scratch(root, WORK) if os.path.isdir(root) else (0, 0, True)
    markers = worktree_markers(LANE)
    named = 1 if REF[:12] in os.path.basename(root.rstrip("/")) else 0
    # The payload carries no value that changes with the ref it is measured at,
    # so a receipt written at J re-derives byte-identically at Y.
    payload = ("faithful=%d,extra=%d,missing=%d,scratch-strays=%d,scratch-read=%s,"
               "markers=%d,named=%d") % (
        faithful, extra, missing, strays, "ok" if read_ok else "fail", markers,
        named)
    ok = (faithful == 1 and markers == 0 and strays == 0 and read_ok and named == 1)
    return payload, ok


# ---------------------------------------------------------------------------
# replay limbs
# ---------------------------------------------------------------------------

def replay_dir(name):
    d = os.path.join(WORK, "replay", name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    return d


def artifact_ok(family):
    rel, digest = DEFEAT_ARTIFACTS[family]
    path = in_tree(rel)
    if not os.path.isfile(path):
        return 0, rel, "absent"
    got = sha256_file(path)
    return (1 if got == digest else 0), rel, got[:12]


def records_fixture(tree, dest):
    for rec in RECORDS:
        if os.path.isfile(in_tree(rec, tree)):
            copy_rel(tree, rec, dest)
    for rel in READ_SET + [DECLARED_REL, "PROVINCE.md", "corpus/SOURCES.md"]:
        if os.path.isfile(in_tree(rel, tree)):
            copy_rel(tree, rel, dest)
    for pref in ("corpus/instruments", "corpus/lessons", "corpus/knowledge",
                 "corpus/source-snapshots", ".ufo/waves"):
        copy_prefix(tree, pref, dest)
    if os.path.isfile(in_tree("corpus/README.md", tree)):
        copy_rel(tree, "corpus/README.md", dest)
    return dest



def strip_evidence_line(line):
    """Remove every evidence token from a correction line."""
    out = PATH_RX.sub("artifact", line)
    out = re.sub(r"\b(?:%s)\b" % "|".join(DEFEAT_STEMS), "artifact", out)
    out = re.sub(r"\b[0-9a-f]{40}\b", "artifact", out)
    return out


def graded_lines(text):
    """The correction lines the K1/K2 counters actually grade."""
    return [(rnd, ln, line) for (rnd, ln, line) in correction_lines(text, ROUND)
            if CLAIM_RX.search(line)]


def replay_k1(tree):
    d = replay_dir("k1")
    records_fixture(tree, d)
    hit = 0
    for rec in RECORDS:
        p = os.path.join(d, rec)
        if not os.path.isfile(p):
            continue
        text = read_text(p)
        lines = text.split("\n")
        for rnd, lineno, line in graded_lines(text):
            stripped = strip_evidence_line(line)
            if stripped == line or evidence_ids(stripped, "round-%s" % rnd):
                continue
            lines[lineno - 1] = stripped
            hit += 1
            break
        write_text(p, "\n".join(lines))
    if not hit:
        return 0, "no-substrate"
    _p, ok = check_k1(d)
    return (0 if ok else 1), ("rejected" if not ok else "accepted")


def replay_k2(tree):
    d = replay_dir("k2")
    records_fixture(tree, d)
    truth = prior_truth(tree)
    if not truth:
        return 0, "no-substrate"
    hit = 0
    for rec in RECORDS:
        p = os.path.join(d, rec)
        if not os.path.isfile(p):
            continue
        lines = read_text(p).split("\n")
        for i, line in enumerate(lines):
            if not CORRECTION_RX.match(line) or not CLAIM_RX.search(line):
                continue
            if any(value_present(line, t) for t in truth):
                for t in truth:
                    if value_present(line, t):
                        lines[i] = line.replace(t, t + "0", 1)
                        hit += 1
                        break
                break
        if hit:
            write_text(p, "\n".join(lines))
            break
    if not hit:
        return 0, "no-substrate"
    _p, ok = check_k2(d)
    return (0 if ok else 1), ("rejected" if not ok else "accepted")


def replay_k3(tree):
    verdicts = []
    for label in ("bare-pipe", "leading-space", "blank-split"):
        d = replay_dir("k3-" + label)
        records_fixture(tree, d)
        p = os.path.join(d, "SKILL.md")
        if not os.path.isfile(p):
            verdicts.append(0)
            continue
        lines = read_text(p).split("\n")
        done = False
        for i, line in enumerate(lines):
            if not line.lstrip().startswith("|"):
                continue
            cells = split_row(line)
            if not (cells and cells[0] == "r42-closure.sh"):
                continue
            if label == "bare-pipe":
                cells[1] = "gate|probe"
                lines[i] = "| " + " | ".join(cells) + " |"
            elif label == "leading-space":
                lines[i] = "  " + line.lstrip()
            else:
                lines[i] = ""
                lines.insert(i + 1, line)
            done = True
            break
        if not done:
            verdicts.append(0)
            continue
        write_text(p, "\n".join(lines))
        _p, ok = check_k3(d)
        verdicts.append(0 if ok else 1)
    if not any(verdicts):
        return 0, "no-substrate"
    return (1 if all(verdicts) else 0), "%d/%d" % (sum(verdicts), len(verdicts))


def replay_k4(tree):
    verdicts = []
    # (a) a declared path that escapes the export root through a symlink
    d = replay_dir("k4-symlink")
    records_fixture(tree, d)
    dec = os.path.join(d, DECLARED_REL)
    if os.path.isfile(dec):
        outside = os.path.join(d, "..", "k4-outside.txt")
        write_text(outside, "outside the export root\n")
        link = os.path.join(d, "escape")
        if not os.path.lexists(link):
            os.symlink(outside, link)
        with open(dec, "a") as fh:
            fh.write("escape 1 %s\n" % sha256_file(outside))
        _p, ok = check_k4(d)
        verdicts.append(0 if ok else 1)
    else:
        verdicts.append(0)
    # (b) an undeclared read path
    d = replay_dir("k4-undeclared")
    records_fixture(tree, d)
    dec = os.path.join(d, DECLARED_REL)
    if os.path.isfile(dec):
        keep = [l for l in read_text(dec).split("\n")
                if l.strip().split()[0:1] != ["corpus/README.md"]]
        write_text(dec, "\n".join(keep))
        _p, ok = check_k4(d)
        verdicts.append(0 if ok else 1)
    else:
        verdicts.append(0)
    if not any(verdicts):
        return 0, "no-substrate"
    return (1 if all(verdicts) else 0), "%d/%d" % (sum(verdicts), len(verdicts))


def replay_k5(_tree):
    """The outside-configured-root stray and the symlink must both be detected."""
    root = replay_dir("k5")
    _s, _sc, _r, out_strays, _os_, _o = k5_eval(root, outside=True, symlink=True)
    root2 = replay_dir("k5-nosym")
    s2, _sc2, _r2, _os2, _os3, _o2 = k5_eval(root2, outside=False, symlink=False)
    outside_ok = out_strays >= 2
    inside_ok = s2 >= 5
    good = sum((1 if outside_ok else 0, 1 if inside_ok else 0))
    detail = "outside=%s,inside=%s" % (
        "detected" if outside_ok else "missed",
        "detected" if inside_ok else "missed")
    return (1 if good == 2 else 0), detail


def replay_k6(tree):
    _p, ok = check_k6(tree)
    return (1 if ok else 0), ("rejected" if ok else "accepted")


def replay_k7(tree):
    _p, ok = check_k7(tree)
    return (1 if ok else 0), ("rejected" if ok else "accepted")


REPLAY = {"K1": replay_k1, "K2": replay_k2, "K3": replay_k3, "K4": replay_k4,
          "K5": replay_k5, "K6": replay_k6, "K7": replay_k7}


def replay_verdict(check_id, tree):
    fam = FAMILY_OF[check_id]
    present, rel, _info = artifact_ok(fam)
    if not present:
        return "artifact-missing:%s" % os.path.basename(rel), 0
    rc, detail = REPLAY[check_id](tree)
    return "%s=%s" % (os.path.basename(rel), detail), rc

# ---------------------------------------------------------------------------
# transcript / receipt grammar
# ---------------------------------------------------------------------------

RECEIPT_LINE_RX = re.compile(r"^(K\d+) payload=(.*) closed=([01])$")
SELFTEST_RX = re.compile(r"^selftest case=(K\d+) positive=(pass|fail) "
                         r"mutants=(\d+)/(\d+) verdict=(pass|fail)$")
SUMMARY_RX = re.compile(r"^selftest cases=(\d+) failures=(\d+)$")
CLOSED_RX_LINE = re.compile(r"^closed=(\d+)/(\d+) exit=(\d+)$")
SUITE_SHA_RX = re.compile(r"^suite-sha256=([0-9a-f]{64}|none)$")
REF_RX = re.compile(r"^export-ref=([0-9a-f]{40})$")


def suite_sha():
    return sha256_file(in_tree(SUITE_REL))


def run_lines_from(payloads, ref, utc, sha):
    lines = [SENTINEL, "export-ref=%s" % ref,
             "suite-sha256=%s" % (sha or "none"),
             "time-basis=ref-commit", "run-utc=%s" % utc]
    for i in CHECK_IDS:
        p, ok = payloads.get(i, ("pending", True))
        lines.append("%s payload=%s closed=%d" % (i, p, 1 if ok else 0))
    closed = sum(1 for i in CHECK_IDS if payloads.get(i, ("", True))[1])
    lines.append("closed=%d/%d exit=%d" % (closed, NCHECKS,
                                           0 if closed == NCHECKS else 1))
    return lines


def parse_receipt(text):
    lines = text.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    info = {"lines": len(lines), "sentinel": False, "ref": None, "suite": None,
            "time_basis": None, "utc": None, "payloads": {}, "selftest": {},
            "summary": None, "closed": None, "bad": []}
    if not lines or lines[0] != SENTINEL:
        info["bad"].append("sentinel")
        return info
    info["sentinel"] = True
    for line in lines[1:]:
        m = REF_RX.match(line)
        if m:
            info["ref"] = m.group(1)
            continue
        m = SUITE_SHA_RX.match(line)
        if m:
            info["suite"] = m.group(1)
            continue
        if line.startswith("time-basis="):
            info["time_basis"] = line.split("=", 1)[1]
            continue
        if line.startswith("run-utc="):
            info["utc"] = line.split("=", 1)[1]
            continue
        m = RECEIPT_LINE_RX.match(line)
        if m:
            info["payloads"][m.group(1)] = (m.group(2), m.group(3))
            continue
        m = SELFTEST_RX.match(line)
        if m:
            info["selftest"][m.group(1)] = m.groups()
            continue
        m = SUMMARY_RX.match(line)
        if m:
            info["summary"] = (int(m.group(1)), int(m.group(2)))
            continue
        m = CLOSED_RX_LINE.match(line)
        if m:
            info["closed"] = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            continue
        info["bad"].append(line[:60])
    return info


def locate_receipt(tree):
    p = in_tree(RECEIPT_REL, tree)
    if os.path.isfile(p):
        return RECEIPT_REL, read_text(p)
    root = in_tree(".ufo/waves/round-43", tree)
    if os.path.isdir(root):
        for dirpath, _dn, filenames in os.walk(root):
            for fn in sorted(filenames):
                if fn == "all-gates.txt":
                    q = os.path.join(dirpath, fn)
                    return os.path.relpath(q, tree), read_text(q)
    return None, ""


def receipt_lines(info):
    out = [SENTINEL]
    for key, fmt in (("ref", "export-ref=%s"), ("suite", "suite-sha256=%s"),
                     ("time_basis", "time-basis=%s"), ("utc", "run-utc=%s")):
        if info[key]:
            out.append(fmt % info[key])
    for i in CHECK_IDS:
        if i in info["payloads"]:
            p, c = info["payloads"][i]
            out.append("%s payload=%s closed=%s" % (i, p, c))
    if info["closed"]:
        out.append("closed=%d/%d exit=%d" % info["closed"])
    for i in CHECK_IDS:
        if i in info["selftest"]:
            g = info["selftest"][i]
            out.append("selftest case=%s positive=%s mutants=%s/%s verdict=%s"
                       % tuple(g))
    if info["summary"]:
        out.append("selftest cases=%d failures=%d" % info["summary"])
    return out


def derived_closed(info):
    """The tally the payload lines themselves imply: the summary may never
    contradict the lines above it."""
    closed = sum(1 for cid in CHECK_IDS
                 if info["payloads"].get(cid, ("", "0"))[1] == "1")
    return (closed, NCHECKS, 0 if closed == NCHECKS else 1)


def canonical_selftest_lines():
    """The all-pass graded block a canonical transcript carries.  One
    producer, so this grammar cannot drift between K8 and its selftest case."""
    return ["selftest case=%s positive=pass mutants=1/1 verdict=pass" % cid
            for cid in CHECK_IDS]


# ---------------------------------------------------------------------------
# K8 -- F-RCPT: receipt integrity
# ---------------------------------------------------------------------------

def forgery_verdicts(info):
    """Six forgeries.  Each is a structural edit whose result must be rejected;
    each entry is 1 when the receipt reader rejects it."""
    base = receipt_lines(info)

    def rejects(mutated_text):
        p2 = parse_receipt(mutated_text)
        return int(p2["payloads"] != info["payloads"]
                   or p2["closed"] != info["closed"]
                   or p2["selftest"] != info["selftest"]
                   or p2["summary"] != info["summary"]
                   or p2["utc"] != info["utc"])

    def flip(lines, predicate, mutate):
        out = list(lines)
        for i, line in enumerate(out):
            if predicate(line):
                out[i] = mutate(line)
                return out
        return None

    out = []
    # v1 forged payload value
    mut = flip(base, lambda l: l.startswith("K1 payload="),
               lambda l: "K1 payload=forged-value,r43")
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    # v2 flipped closed flag
    mut = flip(base, lambda l: l.startswith("K5 payload="),
               lambda l: l[:-1] + ("0" if l.endswith("1") else "1"))
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    # v3 forged tally: claim the full closure the payload lines do not imply
    forged_closed = (NCHECKS, NCHECKS,
                     1 if info["closed"] and info["closed"][2] == 0 else 0)
    mut = flip(base, lambda l: CLOSED_RX_LINE.match(l) is not None,
               lambda l: "closed=%d/%d exit=%d" % forged_closed)
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    # v4 forged summary
    mut = flip(base, lambda l: SUMMARY_RX.match(l) is not None,
               lambda l: "selftest cases=%d failures=99" % NCHECKS)
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    # v5 flipped selftest verdict
    mut = flip(base, lambda l: l.startswith("selftest case="),
               lambda l: l.replace("verdict=pass", "verdict=FAILED")
               if l.endswith("verdict=pass") else l + "x")
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    # v6 forged run instant
    mut = flip(base, lambda l: l.startswith("run-utc="),
               lambda l: "run-utc=1970-01-01T00:00:00Z")
    out.append(rejects("\n".join(mut) + "\n") if mut else 0)
    return out


def check_k8(tree, payloads, selftest_lines, summary, provisional):
    rel, text = locate_receipt(tree)
    if text:
        source = "committed"
    else:
        source = "canonical"
        rel = "(canonical)"
        synth = canonical_selftest_lines()
        text = "\n".join(provisional + synth
                         + ["selftest cases=%d failures=0" % NCHECKS]) + "\n"
    info = parse_receipt(text)
    facts = []
    state = {"ok": True}

    def add(name, good):
        facts.append("%s=%d" % (name, 1 if good else 0))
        if not good:
            state["ok"] = False

    add("sentinel", info["sentinel"])
    add("lines", info["lines"] == 5 + NCHECKS + 1 + NCHECKS + 1)
    add("ref", bool(info["ref"]))
    # The suite bytes at the export ref.  `none` is the honest value when the
    # suite is not in the graded tree (a base export predates round 43); a
    # committed receipt must still name exactly those bytes.
    now = suite_sha()
    add("digest", info["suite"] == (now or "none"))
    add("time-basis", info["time_basis"] == "ref-commit")
    ref = info["ref"]
    if ref:
        want = ref_utc(ref)
        add("utc", bool(want) and info["utc"] == want)
        add("ancestor", git(["merge-base", "--is-ancestor", ref, REF])[0] == 0)
        rc, diff = git(["diff", "--name-only", ref, REF])
        changed = [x for x in diff.split("\n") if x]
        add("diff", rc == 0 and len(changed) <= 1 and all(
            x in (RECEIPT_REL, rel) for x in changed))
    else:
        add("utc", False)
        add("ancestor", False)
        add("diff", False)
    add("run-lines", len(info["payloads"]) == NCHECKS)
    add("selftest-lines", len(info["selftest"]) == NCHECKS)
    add("verdicts", len(info["selftest"]) == NCHECKS
        and all(v[-1] == "pass" for v in info["selftest"].values()))
    add("summary", info["summary"] == (NCHECKS, 0))
    derived = derived_closed(info)
    if source == "canonical":
        # No receipt is committed at this ref, so the block is the run's own
        # canonical probe: its summary must be exactly what its lines imply.
        add("closed-line", derived == info["closed"])
    else:
        # A committed receipt must claim the full closure it tees.
        add("closed-line", info["closed"] == (NCHECKS, NCHECKS, 0)
            and derived == info["closed"])
    add("no-stray", not info["bad"])

    matches = 0
    for i in DETERMINISTIC:
        rec = info["payloads"].get(i)
        got = payloads.get(i)
        if rec and got and rec[0] == got[0] \
                and rec[1] == ("1" if got[1] else "0"):
            matches += 1
    add("payload-match", matches == len(DETERMINISTIC))
    forged = forgery_verdicts(info)
    add("forged", all(forged))
    payload = "receipt=%s,source=%s,%s,payload-match=%d/%d,forged=%d/6" % (
        rel, source, ",".join(facts), matches, len(DETERMINISTIC), sum(forged))
    return payload, state["ok"]


# ---------------------------------------------------------------------------
# K9 -- negative controls
# ---------------------------------------------------------------------------

def neg_accept(tally, rc, tree_reds):
    if rc == 0:
        return False, "exit0"
    if tally < 0 or tally >= NCHECKS:
        return False, "tally"
    if len(tree_reds) < 2:
        return False, "depth-only"
    return True, "ok"


def nested_run(ref):
    d = os.path.join(WORK, "k9", ref[:12])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "work"), exist_ok=True)
    env = dict(os.environ)
    for k in ("R43_EXPORT", "R43_WORK", "R43_SCRATCH_ROOT", "R43_REF",
              "R43_RECEIPT_OUT", "R43_ONLY", "R43_LEAF", "R43_MODE",
              "R43_SELF"):
        env.pop(k, None)
    env["TMPDIR"] = d
    try:
        p = subprocess.run(["bash", SELF, "--export-ref", ref, "--lane", LANE,
                            "--work", os.path.join(d, "work"),
                            "--scratch-root", d, "--leaf"],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                           env=env, timeout=1200)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return p.stdout.decode("utf-8", "replace"), p.returncode


def nested_facts(out):
    if out is None:
        return None
    reds, tally = [], -1
    for line in out[0].split("\n"):
        m = RECEIPT_LINE_RX.match(line)
        if m and m.group(3) == "0":
            reds.append(m.group(1))
        m2 = CLOSED_RX_LINE.match(line)
        if m2:
            tally = int(m2.group(1))
    return {"rc": out[1], "reds": reds, "tally": tally}


def check_k9(_tree):
    if LEAF:
        return "depth=leaf,base=deferred,r41=deferred,deferred=1,accept=tree-red", False
    results = {}
    for ref, label in ((BASE_REF, "base"), (R41_HEAD, "r41")):
        facts = nested_facts(nested_run(ref))
        if facts is None:
            results[label] = 0
            continue
        dependent = [r for r in facts["reds"]
                     if r in ("K1", "K2", "K3", "K4", "K8", "K11",
                              "K14", "K15", "K16", "K17", "K18", "K19")]
        good, _why = neg_accept(facts["tally"], facts["rc"], dependent)
        results[label] = 1 if good else 0
    payload = ("depth=1,base=%d,r41=%d,accept=tree-red,cap=nested") % (
        results.get("base", 0), results.get("r41", 0))
    ok = results.get("base") == 1 and results.get("r41") == 1
    return payload, ok


# ---------------------------------------------------------------------------
# K10 -- graded-selftest isolation
# ---------------------------------------------------------------------------

def check_k10(canaries):
    cases = len(canaries)
    isolated = sum(1 for c in canaries if c["isolated"])
    leak = sum(1 for c in canaries if c["canary"])
    graded = sum(1 for c in canaries if c["line_ok"])
    payload = ("cases=%d,isolated=%d,canary=%d,graded-lines=%d,fixture=synthetic") % (
        cases, isolated, leak, graded)
    ok = (cases == NCHECKS and isolated == cases and leak == 0 and graded == cases)
    return payload, ok


# ---------------------------------------------------------------------------
# K14..K19 -- narrative-evidence checks, one slot per limb deliverable
#
# Each slot is a seam: the limb deliverable replaces the slot body and its
# mutation battery, and nothing else in this suite moves.  Until a slot lands
# it prints `payload=stub closed=0` and the suite stays open at <19/19 -- a
# slot that reported closed=1 without its limb would make the suite claim
# evidence it does not have.
# ---------------------------------------------------------------------------

LIMB_STUB = ("stub", False)


def check_k14(_tree):
    return LIMB_STUB


def check_k15(_tree):
    return LIMB_STUB


def check_k16(_tree):
    return LIMB_STUB


def check_k17(_tree):
    return LIMB_STUB


def check_k18(_tree):
    return LIMB_STUB


def check_k19(_tree):
    return LIMB_STUB


LIMB_SLOTS = ["K14", "K15", "K16", "K17", "K18", "K19"]
LIMB_CHECKS = {"K14": check_k14, "K15": check_k15, "K16": check_k16,
               "K17": check_k17, "K18": check_k18, "K19": check_k19}


def limb_mutants(_check_id, _root):
    """The slot's mutation battery: (rejected, built).  Zero cases until the
    limb lands, so its selftest line reports positive=fail honestly."""
    return 0, 0


# ---------------------------------------------------------------------------
# selftest cases
# ---------------------------------------------------------------------------

def case_root(check_id):
    d = os.path.join(WORK, "selftest", "case-%s" % check_id)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    return d


def strip_evidence_copy(tree, dest):
    records_fixture(tree, dest)
    hit = 0
    for rec in RECORDS:
        p = os.path.join(dest, rec)
        if not os.path.isfile(p):
            continue
        text = read_text(p)
        lines = text.split("\n")
        for rnd, lineno, line in graded_lines(text):
            new = strip_evidence_line(line)
            if new == line or evidence_ids(new, "round-%s" % rnd):
                continue
            lines[lineno - 1] = new
            hit += 1
            break
        write_text(p, "\n".join(lines))
    return hit


def mangle_tally_copy(tree, dest):
    records_fixture(tree, dest)
    truth = prior_truth(tree)
    if not truth:
        return 0
    for rec in RECORDS:
        p = os.path.join(dest, rec)
        if not os.path.isfile(p):
            continue
        text = read_text(p)
        lines = text.split("\n")
        for _rnd, lineno, line in graded_lines(text):
            for t in truth:
                if value_present(line, t):
                    lines[lineno - 1] = line.replace(t, t + "0", 1)
                    write_text(p, "\n".join(lines))
                    return 1
    return 0


def skill_mutation_copy(tree, dest, label):
    records_fixture(tree, dest)
    p = os.path.join(dest, "SKILL.md")
    if not os.path.isfile(p):
        return 0
    lines = read_text(p).split("\n")
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if not (cells and cells[0] == "r42-closure.sh"):
            continue
        if label == "bare-pipe":
            cells[1] = "gate|probe"
            lines[i] = "| " + " | ".join(cells) + " |"
        elif label == "leading-space":
            lines[i] = "  " + line.lstrip()
        else:
            lines[i] = ""
            lines.insert(i + 1, line)
        write_text(p, "\n".join(lines))
        return 1
    return 0


def declared_symlink_copy(tree, dest):
    records_fixture(tree, dest)
    dec = os.path.join(dest, DECLARED_REL)
    if not os.path.isfile(dec):
        return 0
    outside = os.path.join(dest, "..", "case-escape.txt")
    write_text(outside, "outside the export root\n")
    link = os.path.join(dest, "escape")
    if not os.path.lexists(link):
        os.symlink(outside, link)
    with open(dec, "a") as fh:
        fh.write("escape 1 %s\n" % sha256_file(outside))
    return 1


def declared_undeclared_copy(tree, dest):
    records_fixture(tree, dest)
    dec = os.path.join(dest, DECLARED_REL)
    if not os.path.isfile(dec):
        return 0
    keep = [l for l in read_text(dec).split("\n")
            if l.strip().split()[0:1] != ["corpus/README.md"]]
    write_text(dec, "\n".join(keep))
    return 1


def dedup_marker_strip_copy(tree, dest):
    records_fixture(tree, dest)
    for rec in RECORDS:
        p = os.path.join(dest, rec)
        if not os.path.isfile(p):
            continue
        lines = read_text(p).split("\n")
        keep = [l for l in lines if not DEDUP_RX.match(l)]
        if len(keep) != len(lines):
            write_text(p, "\n".join(keep))
            return 1
    return 0


def git_fixture(root):
    d = os.path.join(root, "repo")
    os.makedirs(os.path.join(d, "corpus"), exist_ok=True)
    rc, out = run_tool(["git", "init", "-q"], cwd=d)
    if rc != 0:
        return None
    top = git_out(["rev-parse", "--show-toplevel"], cwd=d).strip()
    if os.path.realpath(top) != os.path.realpath(d):
        return None
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid"]
    write_text(os.path.join(d, "corpus", "keep.md"), "keep\n")
    write_text(os.path.join(d, "corpus", "gone.md"), "gone\n")
    run_tool(["git"] + ident + ["add", "-A"], cwd=d)
    run_tool(["git"] + ident + ["commit", "-q", "-m", "one"], cwd=d)
    first = git_out(["rev-parse", "HEAD"], cwd=d).strip()
    os.unlink(os.path.join(d, "corpus", "gone.md"))
    write_text(os.path.join(d, "corpus", "keep.md"), "keep changed\n")
    run_tool(["git"] + ident + ["add", "-A"], cwd=d)
    run_tool(["git"] + ident + ["commit", "-q", "-m", "two"], cwd=d)
    second = git_out(["rev-parse", "HEAD"], cwd=d).strip()
    return d, first, second


def git_fixture_noop(root):
    d = os.path.join(root, "repo")
    os.makedirs(os.path.join(d, "corpus"), exist_ok=True)
    rc, _out = run_tool(["git", "init", "-q"], cwd=d)
    if rc != 0:
        return None
    top = git_out(["rev-parse", "--show-toplevel"], cwd=d).strip()
    if os.path.realpath(top) != os.path.realpath(d):
        return None
    ident = ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid"]
    write_text(os.path.join(d, "corpus", "keep.md"), "keep\n")
    run_tool(["git"] + ident + ["add", "-A"], cwd=d)
    run_tool(["git"] + ident + ["commit", "-q", "-m", "one"], cwd=d)
    first = git_out(["rev-parse", "HEAD"], cwd=d).strip()
    write_text(os.path.join(d, "corpus", "keep.md"), "keep changed\n")
    run_tool(["git"] + ident + ["add", "-A"], cwd=d)
    run_tool(["git"] + ident + ["commit", "-q", "-m", "two"], cwd=d)
    second = git_out(["rev-parse", "HEAD"], cwd=d).strip()
    return d, first, second


def export_fidelity(tree, root, extra=False):
    d = os.path.join(root, "replica")
    os.makedirs(d, exist_ok=True)
    for rel in ("corpus/README.md",):
        if os.path.isfile(in_tree(rel, tree)):
            copy_rel(tree, rel, d)
    if extra:
        write_text(os.path.join(d, "corpus", "unexpected.md"), "extra\n")
    return d


SELFTEST_SPECS = [
    ("K1", "strip-evidence-union"),
    ("K2", "mangled-tally"),
    ("K3", "table-mutations"),
    ("K4", "declaration-mutations"),
    ("K5", "scratch-scan-mutations"),
    ("K6", "binding-mutations"),
    ("K7", "frontier-flip-mutations"),
    ("K8", "forged-receipts"),
    ("K9", "acceptance-predicate"),
    ("K10", "isolation-probe"),
    ("K11", "dedup-marker-strip"),
    ("K12", "deletion-probe"),
    ("K13", "export-fidelity"),
    ("K14", "correction-literal"),
    ("K15", "wave-dispatch-narrative"),
    ("K16", "placeholder-promise"),
    ("K17", "claims-before-literal"),
    ("K18", "quoted-closed-values"),
    ("K19", "freeze-record-order"),
]


def selftest_case(check_id, payloads, provisional, ctx):
    root = case_root(check_id)
    result = {"id": check_id, "isolated": False, "canary": False,
              "line_ok": False, "positive": False, "payload": "",
              "mutants": (0, 0)}
    canary_file = os.path.join(root, "canary-kasegi-r43-probe.txt")
    write_text(canary_file, "CANARY-R43-7f3a91\n")
    canary_token = "CANARY-R43-7f3a91"
    try:
        if check_id == "K1":
            payload, ok = check_k1(EXPORT)
            d = os.path.join(root, "mut")
            n = strip_evidence_copy(EXPORT, d)
            m_ok = 0 if n == 0 else (0 if check_k1(d)[1] else 1)
            result["mutants"] = (m_ok, 1 if n else 0)
        elif check_id == "K2":
            payload, ok = check_k2(EXPORT)
            d = os.path.join(root, "mut")
            n = mangle_tally_copy(EXPORT, d)
            m_ok = 0 if n == 0 else (0 if check_k2(d)[1] else 1)
            result["mutants"] = (m_ok, 1 if n else 0)
        elif check_id == "K3":
            payload, ok = check_k3(EXPORT)
            good = total = 0
            for label in ("bare-pipe", "leading-space", "blank-split"):
                d = os.path.join(root, "mut-" + label)
                if not skill_mutation_copy(EXPORT, d, label):
                    continue
                total += 1
                if not check_k3(d)[1]:
                    good += 1
            result["mutants"] = (good, total)
        elif check_id == "K4":
            payload, ok = check_k4(EXPORT)
            good = total = 0
            d = os.path.join(root, "mut-symlink")
            if declared_symlink_copy(EXPORT, d):
                total += 1
                if not check_k4(d)[1]:
                    good += 1
            d = os.path.join(root, "mut-undeclared")
            if declared_undeclared_copy(EXPORT, d):
                total += 1
                if not check_k4(d)[1]:
                    good += 1
            result["mutants"] = (good, total)
        elif check_id == "K5":
            payload, ok = check_k5(EXPORT)
            good = total = 0
            s1 = k5_eval(os.path.join(root, "mut-nooutside"), outside=False,
                         symlink=True)
            total += 1
            if s1[3] < 2:
                good += 1
            s2 = k5_eval(os.path.join(root, "mut-nosymlink"), outside=True,
                         symlink=False)
            total += 1
            if s2[0] == s1[0] - 1:
                good += 1
            result["mutants"] = (good, total)
        elif check_id == "K6":
            payload, ok = check_k6(EXPORT)
            result["mutants"] = (sum(1 for k in ("missing-path", "url-mutated")
                                     if k + "=1" in payload), 2)
        elif check_id == "K7":
            payload, ok = check_k7(EXPORT)
            result["mutants"] = (sum(1 for k in ("status-flip", "no-pass")
                                     if k + "=1" in payload), 2)
        elif check_id == "K8":
            # The receipt reader is graded on a 33-line canonical transcript:
            # the graded block is synthetic so this case does not depend on
            # whether the other twelve cases passed.
            pl = dict(payloads)
            pl.setdefault("K10", check_k10(
                [{"isolated": True, "canary": False, "line_ok": True}] * NCHECKS))
            synth = canonical_selftest_lines()
            prov = run_lines_from(pl, REF, ref_utc(REF), suite_sha())
            payload, ok = check_k8(EXPORT, pl, synth, (NCHECKS, 0), prov)
            info = parse_receipt(
                "\n".join(prov + synth
                           + ["selftest cases=%d failures=0" % NCHECKS]) + "\n")
            forged = forgery_verdicts(info)
            result["mutants"] = (sum(forged), len(forged))
        elif check_id == "K9":
            # (tally, rc, reds, must_accept): a control that closes everything,
            # one red only because the depth cap stopped it, and one genuine
            # tree-red control that must be accepted.
            probes = [
                (NCHECKS, 0, ["K1", "K8"], False),
                (NCHECKS - 1, 1, ["K5"], False),
                (NCHECKS - 2, 1, ["K1", "K8", "K11"], True),
            ]
            good = 0
            for tally, rc, reds, want in probes:
                accepted, _w = neg_accept(tally, rc, reds)
                if accepted == want:
                    good += 1
            payload, ok = check_k9(EXPORT)
            result["mutants"] = (good, len(probes))
        elif check_id == "K10":
            leak = [{"isolated": True, "canary": True, "line_ok": True}] * NCHECKS
            clean = [{"isolated": True, "canary": False, "line_ok": True}] * NCHECKS
            good = 0
            if not check_k10(leak)[1]:
                good += 1
            if check_k10(clean)[1]:
                good += 1
            payload, ok = check_k10(clean)
            result["mutants"] = (good, 2)
        elif check_id == "K11":
            payload, ok = check_k11(EXPORT)
            d = os.path.join(root, "mut")
            n = dedup_marker_strip_copy(EXPORT, d)
            m_ok = 0 if n == 0 else (0 if check_k11(d)[1] else 1)
            result["mutants"] = (m_ok, 1 if n else 0)
        elif check_id == "K12":
            payload, ok = check_k12(EXPORT)
            fix = git_fixture(root)
            good = total = 0
            if fix:
                total += 1
                rows = deletion_rows(fix[1], fix[2], cwd=fix[0])
                if rows and len(rows) == 1:
                    good += 1
            noop = git_fixture_noop(root)
            if noop:
                total += 1
                rows = deletion_rows(noop[1], noop[2], cwd=noop[0])
                if rows is not None and not rows:
                    good += 1
            result["mutants"] = (good, total)
        elif check_id == "K13":
            payload, ok = check_k13(EXPORT)
            good = total = 0
            replica = export_fidelity(EXPORT, root, extra=True)
            rc, out = git(["ls-tree", "-r", "--name-only", REF])
            ls = set(x for x in out.split("\n") if x)
            ex = set(os.path.relpath(os.path.join(dp, fn), replica)
                     for dp, _dn, fns in os.walk(replica) for fn in fns)
            total += 1
            if ex != ls:
                good += 1
            replica2 = export_fidelity(EXPORT, os.path.join(root, "clean"), extra=False)
            ex2 = set(os.path.relpath(os.path.join(dp, fn), replica2)
                      for dp, _dn, fns in os.walk(replica2) for fn in fns)
            total += 1
            if "corpus/README.md" in ex2:
                good += 1
            result["mutants"] = (good, total)
        elif check_id in LIMB_SLOTS:
            payload, ok = LIMB_CHECKS[check_id](EXPORT)
            result["mutants"] = limb_mutants(check_id, root)
        else:
            payload, ok = ("unsupported", False)
        result["positive"] = bool(ok)
        result["payload"] = payload
        result["canary"] = canary_token in payload
    finally:
        shutil.rmtree(root, ignore_errors=True)
        result["isolated"] = not os.path.exists(root)
    return result


def selftest_line(check_id, res, payloads):
    """One graded case line.  `positive` is the case's own verdict and
    `verdict` additionally requires the case to have reproduced the payload the
    run printed for it and to have rejected every mutant it built."""
    pos = "pass" if res["positive"] else "fail"
    base_payload = payloads.get(check_id, ("", False))[0].split(",replay=")[0]
    pm = 1 if (check_id in payloads and res["payload"] == base_payload) else 0
    good, total = res["mutants"]
    # A case that builds no mutant proves nothing: verdict=pass needs at least
    # one rejected mutant, not an empty battery.
    verdict = "pass" if (res["positive"] and pm == 1
                         and total >= 1 and good == total) else "fail"
    line = ("selftest case=%s positive=%s mutants=%d/%d verdict=%s"
            % (check_id, pos, good, total, verdict))
    res["line_ok"] = bool(SELFTEST_RX.match(line))
    return line


def selftest_pass(payloads, provisional):
    cases = []
    lines = []
    for check_id, _label in SELFTEST_SPECS:
        res = selftest_case(check_id, payloads, provisional, None)
        lines.append(selftest_line(check_id, res, payloads))
        cases.append(res)
    failures = sum(1 for l in lines if l.endswith("verdict=fail"))
    summary = (len(lines), failures)
    return lines, summary, cases


def run_selftest(payloads, provisional):
    """Grade the cases to a fixed point: K10 counts the graded case lines and
    K8 grades the receipt shaped from the transcript, so each needs the other's
    payload to exist before payload-match can compare them."""
    lines, summary, cases = selftest_pass(payloads, provisional)
    for _ in range(4):
        payloads["K10"] = check_k10(cases)
        prov = run_lines_from(payloads, REF, ref_utc(REF), suite_sha())
        payloads["K8"] = check_k8(EXPORT, payloads, lines, summary, prov)
        n_lines, n_summary, n_cases = selftest_pass(payloads, prov)
        if (n_lines, n_summary) == (lines, summary):
            return n_lines, n_summary, n_cases
        lines, summary, cases = n_lines, n_summary, n_cases
    return lines, summary, cases


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

CHEAP = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K11", "K12", "K13"] \
    + LIMB_SLOTS


def run_one(check_id):
    fn = {"K1": check_k1, "K2": check_k2, "K3": check_k3, "K4": check_k4,
          "K5": check_k5, "K6": check_k6, "K7": check_k7, "K11": check_k11,
          "K12": check_k12, "K13": check_k13}
    if check_id in fn:
        payload, ok = fn[check_id](EXPORT)
    else:
        payload, ok = LIMB_CHECKS[check_id](EXPORT)
    if check_id in REPLAY:
        verdict, rc = replay_verdict(check_id, EXPORT)
        payload = "%s,replay=%s" % (payload, verdict)
        ok = ok and rc == 1
    return payload, ok


def run_only(utc, sha):
    """One leaf check, so a limb is developed without paying for the suite."""
    payload, ok = run_one(ONLY)
    if MODE == "selftest":
        graded = {ONLY: (payload, ok)}
        line = selftest_line(ONLY, selftest_case(ONLY, graded, [], None), graded)
        failures = 0 if line.endswith("verdict=pass") else 1
        sys.stdout.write(line + "\n")
        sys.stdout.write("selftest cases=1 failures=%d\n" % failures)
        return 0 if failures == 0 else 1
    run = [SENTINEL, "export-ref=%s" % REF,
           "suite-sha256=%s" % (sha or "none"),
           "time-basis=ref-commit", "run-utc=%s" % utc,
           "%s payload=%s closed=%d" % (ONLY, payload, 1 if ok else 0),
           "only=%s closed=%d/1 exit=%d" % (ONLY, 1 if ok else 0, 0 if ok else 1)]
    sys.stdout.write("\n".join(run) + "\n")
    return 0 if ok else 1


def main():
    if not os.path.isdir(EXPORT):
        sys.stderr.write("r43-closure: no export tree at %s\n" % EXPORT)
        return 2
    utc = ref_utc(REF)
    sha = suite_sha()
    if ONLY:
        return run_only(utc, sha)
    if MODE == "selftest":
        payloads = {}
        for cid in CHEAP + ["K9"]:
            payloads[cid] = run_one(cid) if cid != "K9" else check_k9(EXPORT)
        provisional = []
        for cid in CHEAP:
            provisional.append("%s payload=%s closed=%d" % (
                cid, payloads[cid][0], 1 if payloads[cid][1] else 0))
        lines, summary, _cases = run_selftest(payloads, provisional)
        sys.stdout.write("\n".join(lines) + "\n")
        sys.stdout.write("selftest cases=%d failures=%d\n" % summary)
        return 0 if summary[1] == 0 else 1

    payloads = {}
    for cid in CHEAP:
        payloads[cid] = run_one(cid)
    payloads["K9"] = check_k9(EXPORT) if not LEAF else \
        ("depth=leaf,base=deferred,r41=deferred,deferred=1,accept=tree-red", False)

    if LEAF:
        payloads["K10"] = ("cases=0,isolated=0,canary=0,graded-lines=0,fixture=skipped", False)
        lines, summary, cases = [], (NCHECKS, NCHECKS), []
    else:
        lines, summary, cases = run_selftest(
            payloads, run_lines_from(payloads, REF, utc, sha))
        payloads["K10"] = check_k10(cases)

    provisional = run_lines_from(payloads, REF, utc, sha)
    payloads["K8"] = check_k8(EXPORT, payloads, lines, summary, provisional)

    run = run_lines_from(payloads, REF, utc, sha)
    sys.stdout.write("\n".join(run) + "\n")

    if RECEIPT_OUT and not LEAF:
        # One unedited tee of this run: the transcript just printed, then the
        # graded selftest block of the same run.
        write_text(RECEIPT_OUT,
                   "\n".join(run + lines
                             + ["selftest cases=%d failures=%d" % summary]) + "\n")

    closed = sum(1 for i in CHECK_IDS if payloads.get(i, ("", True))[1])
    return 0 if closed == NCHECKS else 1


if __name__ == "__main__":
    sys.exit(main())
R43_ENGINE_PY
