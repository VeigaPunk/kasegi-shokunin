#!/usr/bin/env bash
# K18 -- RD42-5: every `closed=<n>/<m>` and `selftest cases=<n> failures=<k>` value
# quoted in a round-42/round-43 lane record must be backed by a committed
# transcript, or its line must carry `report-only`, or it must be named
# superseded by a `Correction (round 43)` / claims-erratum line.
#
#   source this file, then:  check_k18 <export-root>
#   standalone:              bash ExecK18Transcript.sh <export-root> [--verbose]
#
# stdout is exactly one line:  K18 payload=quotes=<n>,bound=<b>,report-only=<r>,superseded=<s>,unbound=<u> closed=0|1
# exit status 0 when closed=1, 1 when closed=0, 2 on a usage error.
#
# SCOPE (declared, not inferred).  A *record* is a committed prose file:
#   corpus/lessons/round-42*.md      (includes round-42-verifier-spotcheck.md)
#   corpus/lessons/round-43*.md
#   .ufo/waves/round-43/*.md         (top level only; not the w1/ seat receipts,
#                                     not final-gates/, not c1-controls/)
# Append-only records (SCORECARD.md, LOG.md, SHONEN.md) are graded by K14 for their
# corrections= literals and are supersede-marker sources here, not quote sources:
# their older-round closed= literals are pre-r42 history, outside this check.
#
# A *quote* is a whole token (R41 boundary -- `closed=10/100` never satisfies
# `closed=10/13`; `failures=30` never satisfies `failures=3`):
#   closed=<n>/<m>                      (?<![0-9/])closed=(\d+)/(\d+)(?![0-9/])
#   selftest cases=<n> failures=<k>     (?<![0-9])selftest cases=(\d+) failures=(\d+)(?![0-9])
#
# BINDING EVIDENCE.  Two evidence stores: the frozen round-42 archive (every
# committed file under .ufo/waves/round-42/) and this round's attestation
# directories (.ufo/waves/round-43/final-gates/, .../c1-controls/).  This round's
# seat receipts (.ufo/waves/round-43/w1/) are claims, not evidence, and never
# bind; nor does a record, so a fenced transcript pasted into a lesson does not
# certify that lesson's own quote.
# A token is bound only by a SUMMARY-SHAPED line inside such a file:
#   ^closed=<n>/<m> exit=<k>$      or      ^selftest cases=<n> failures=<k>$
# so a value that occurs inside a fixture script's `printf` (or inside a payload
# cell) does not bind, and a summary-only file that lacks the token cannot bind it.
#
# EXEMPTIONS, per occurrence:
#   report-only  the quoting line contains the literal `report-only`
#   superseded   a supersede record quotes the token: a line containing
#                `Correction (round 43)`, or the blank-line separated entry of a
#                `claims-erratum*.md` file (round-42/round-43 wave dirs) that
#                carries `superseded`
#   attack row   a round-42 markdown table row whose first cell is an attack id
#                (`aN`/`bN`): inherited verifier observations from mutated scratch
#                trees the lane never committed -- no transcript can exist for them.
#                Round-43 records get no such exemption: such a line must carry
#                `report-only`.
#   anti-example a line that presents the value as a mangled/forged exemplar
#                (contains `mangled` or `substring`) -- quoted to be rejected.
check_k18() {
    local export="${1:-${K18_EXPORT:-}}"
    local verbose="${2:-${K18_VERBOSE:-0}}"
    if [ -z "$export" ] || [ ! -d "$export" ]; then
        printf 'K18 payload=quotes=0,bound=0,report-only=0,superseded=0,unbound=0 closed=0\n'
        [ -n "$verbose" ] && printf 'K18 error=no-export path=%s\n' "$export" >&2
        return 1
    fi
    python3 - "$export" "${K18_ID:-K18}" "$verbose" <<'K18_ENGINE_PY'
import fnmatch
import os
import re
import sys

root = sys.argv[1]
check_id = sys.argv[2] if len(sys.argv) > 2 else "K18"
verbose = (sys.argv[3] if len(sys.argv) > 3 else "0") not in ("", "0", "no", "false")

CLOSED_RX = re.compile(r"(?<![0-9/])closed=(\d+)/(\d+)(?![0-9/])")
SUMMARY_RX = re.compile(r"(?<![0-9])selftest cases=(\d+) failures=(\d+)(?![0-9])")
SUM_CLOSED_LINE = re.compile(r"^closed=(\d+)/(\d+) exit=[0-9]+$")
SUM_TEST_LINE = re.compile(r"^selftest cases=(\d+) failures=(\d+)$")
RUN_HEADER = re.compile(r"^export-ref=[0-9a-f]{40}$", re.M)
ATTACK_ID = re.compile(r"^[ab][0-9]+$")
ANTI_EXAMPLE = ("mangled", "substring")

SURFACE_PREFIXES = ("corpus/lessons/round-42", "corpus/lessons/round-43")
WAVE_RECORD_DIR = ".ufo/waves/round-43"
WAVE_ROUND_DIRS = (".ufo/waves/round-42", ".ufo/waves/round-43")
MAX_READ = 8 << 20


def read_text(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(MAX_READ)
    except OSError:
        return ""
    if b"\x00" in data:
        return ""
    return data.decode("utf-8", "replace")


def rel_files(base):
    out = []
    start = os.path.join(root, base)
    for dirpath, dirnames, filenames in os.walk(start):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            out.append(os.path.relpath(p, root))
    return sorted(out)


# ---- quote sources -------------------------------------------------------
records = []
for rel in rel_files("corpus/lessons"):
    if any(fnmatch.fnmatch(rel, pat + "*.md") for pat in SURFACE_PREFIXES):
        records.append(rel)
for rel in rel_files(WAVE_RECORD_DIR):
    # top level only: <wave>/<file>.md, never <wave>/<sub>/<file>.md
    if rel.endswith(".md") and os.path.dirname(rel) == WAVE_RECORD_DIR:
        records.append(rel)
records = sorted(set(records))
records = [r for r in records if os.path.isfile(os.path.join(root, r))]

record_set = set(records)

# ---- binding evidence ----------------------------------------------------
# Evidence is (a) the frozen round-42 archive -- every committed file under
# .ufo/waves/round-42/, which cannot be re-authored to bind a new value, and
# (b) this round's attestation directories, .ufo/waves/round-43/final-gates/ and
# .ufo/waves/round-43/c1-controls/.  This round's seat receipts (.ufo/waves/
# round-43/w1/) are CLAIMS awaiting verification, not evidence: excluding them
# stops a receipt from certifying a value by quoting it.
EVIDENCE_DIRS = (".ufo/waves/round-42",
                 ".ufo/waves/round-43/final-gates",
                 ".ufo/waves/round-43/c1-controls")
bound = set()
transcripts = []
for base in EVIDENCE_DIRS:
    for rel in rel_files(base):
        if rel in record_set:
            continue
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        text = read_text(path)
        if not text:
            continue
        transcripts.append(rel)
        for line in text.split("\n"):
            line = line.rstrip()
            m = SUM_CLOSED_LINE.match(line)
            if m:
                bound.add("closed=%s/%s" % (m.group(1), m.group(2)))
            m = SUM_TEST_LINE.match(line)
            if m:
                bound.add("selftest cases=%s failures=%s" % (m.group(1), m.group(2)))

# ---- supersede markers ---------------------------------------------------
superseded = set()
marker_files = []
for base in WAVE_ROUND_DIRS:
    for rel in rel_files(base):
        if os.path.basename(rel).startswith("claims-erratum") and rel.endswith(".md"):
            marker_files.append(rel)
marker_files += [r for r in records]
for rel in sorted(set(marker_files)):
    text = read_text(os.path.join(root, rel))
    errata = os.path.basename(rel).startswith("claims-erratum")
    # A `Correction (round 43)` is one appended line: it supersedes the tokens on
    # that line.  A claims erratum is a prose entry: it supersedes the tokens of
    # the entry (blank-line separated block) that carries `superseded`, so a
    # wrapped sentence still names its value.
    for line in text.split("\n"):
        if "Correction (round 43)" not in line:
            continue
        for rx in (CLOSED_RX, SUMMARY_RX):
            for m in rx.finditer(line):
                superseded.add(m.group(0))
    if errata:
        for block in re.split(r"\n\s*\n", text):
            if "superseded" not in block:
                continue
            for rx in (CLOSED_RX, SUMMARY_RX):
                for m in rx.finditer(block):
                    superseded.add(m.group(0))

# ---- quote shape helpers -------------------------------------------------
EXIT_AFTER = re.compile(r"\s*exit=[0-9]")


def summary_shaped(line, tok):
    """A value in the suite's own summary grammar is always a state claim."""
    idx = line.find(tok)
    if idx < 0:
        return False
    if tok.startswith("selftest cases="):
        return True
    return bool(EXIT_AFTER.match(line, idx + len(tok)))


def cell_of(line, tok, cells):
    """The markdown table cell that carries the token, else the whole line."""
    if not cells:
        return line
    idx = line.find(tok)
    pos = 0
    for cell in cells:
        start = line.find(cell, pos)
        if start < 0:
            continue
        end = start + len(cell)
        if start <= idx < end:
            return cell
        pos = end
    return line


# ---- grade ---------------------------------------------------------------
quotes = bcount = rcount = scount = ucount = 0
unbound_samples = []
for rel in records:
    text = read_text(os.path.join(root, rel))
    is_round42 = rel.startswith("corpus/lessons/round-42")
    for lineno, line in enumerate(text.split("\n"), 1):
        found = [m.group(0) for m in CLOSED_RX.finditer(line)]
        found += [m.group(0) for m in SUMMARY_RX.finditer(line)]
        if not found:
            continue
        stripped = line.strip()
        cells = []
        if stripped.startswith("|"):
            body = stripped.strip("|")
            cells = [c.strip() for c in body.split("|")]
        attack_row = bool(cells) and bool(ATTACK_ID.match(cells[0]))
        for tok in found:
            if attack_row and is_round42:
                continue
            if not summary_shaped(line, tok):
                cell = cell_of(line, tok, cells)
                if any(word in cell for word in ANTI_EXAMPLE):
                    continue
            quotes += 1
            if tok in bound:
                bcount += 1
            elif "report-only" in line:
                rcount += 1
            elif tok in superseded:
                scount += 1
            else:
                ucount += 1
                unbound_samples.append((rel, lineno, tok))

closed = 1 if ucount == 0 else 0
sys.stdout.write("%s payload=quotes=%d,bound=%d,report-only=%d,superseded=%d,"
                 "unbound=%d closed=%d\n"
                 % (check_id, quotes, bcount, rcount, scount, ucount, closed))
if verbose:
    for rel, lineno, tok in unbound_samples:
        sys.stderr.write("%s unbound token=%s at %s:%d\n"
                         % (check_id, tok, rel, lineno))
    sys.stderr.write("%s scope records=%d transcripts=%d\n"
                     % (check_id, len(records), len(transcripts)))
sys.exit(0 if closed else 1)
K18_ENGINE_PY
}

if [ "${BASH_SOURCE[0]:-$0}" = "${0:-}" ]; then
    case "${1:-}" in
        -h|--help)
            sed -n '2,60p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
    esac
    verbose=0
    exportroot=""
    for arg in "$@"; do
        case "$arg" in
            --verbose) verbose=1 ;;
            *) [ -z "$exportroot" ] && exportroot="$arg" ;;
        esac
    done
    [ -n "$exportroot" ] || { printf 'K18 usage: %s <export-root> [--verbose]\n' "$0" >&2; exit 2; }
    check_k18 "$exportroot" "$verbose"
    exit $?
fi
