#!/usr/bin/env bash
# r39-closure.sh — round-39 closure counter for claim C1 (depth:verifiability).
#
# Eight checks G1-G8. Each closes one defect class the round-38 verifier routed
# (corpus/lessons/round-38-verifier-spotcheck.md §5: R1, R2, R3, R4) or the
# round-38 instrument attack findings (corpus/lessons/round-38.md §Instrument
# attack findings): G1 whole-tail declarations (partial tail, tilde fences,
# corrections inside fences, declaration paths escaping the export), G2 graded
# receipt (graded case lines, v3 header, suite digest, ancestry, post-receipt
# diff), G3 committed-run truth (a quoted run needs a transcript or the
# `report-only` label), G4 seat identity (distinct per-seat identities, not a
# count; a zero-task dispatch is RED), G5 label drift, G6 live scratch
# quiescence (fail-closed), G7 ledger fill, G8 pinned carry-over (the round-37
# suite bytes pinned by commit AND digest, run, `closed=14/14 exit=0`).
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -xf - -C <work>/export
# and every check reads its bytes only under that export root. The only live
# reads are G6's scratch-root scan (host state by definition) and the git limbs
# that cannot be answered from a tree: G1's added-line count, G2's ancestry and
# post-receipt diff, G3's added-line scan, and G8's pinned `git show`. Those are
# ref-scoped reads against the lane repo (`cat-file`, `merge-base
# --is-ancestor`, `diff`, `show`, `rev-parse`) and they run with
# `--no-optional-locks` so the lane is never written to. Nothing is written
# under the lane; the only writes are the extraction, the pinned r37 copy and
# the selftest fixtures under --work (or a mktemp dir honouring TMPDIR), all
# removed on exit. --work must lie outside the lane; its `export/`, `mut/`,
# `r37/` and `r37-pinned/` subdirectories are cleared before use, so a reused
# work dir can never satisfy a check with stale bytes. A plain run (no
# --export-ref, no --selftest) refuses with exit 2, because a suite that reads
# the working tree can be turned green by edits that were never committed.
#
# Usage:
#   bash corpus/instruments/r39-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run G1-G8 against the export. Prints
#       `export-ref=<hash> mode=export lane=<lane> suite-sha256=<digest>`, one
#       `G<n> payload=<k=v,...> closed=0|1` line per check and a final
#       `closed=K/8 exit=0|1`; exit 0 only for K=8, exit 1 otherwise.
#   bash corpus/instruments/r39-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check at least two scratch fixtures that reopen
#       exactly one clause must be REJECTED, and the rejection payload must name
#       the reopened limb, so a fixture proves the check discriminates rather
#       than that it can be satisfied by a summary. Prints one GRADED
#       `selftest case=G<i> positive=pass|fail mutants=<ok>/<n> verdict=pass|fail`
#       line per check, the `selftest detail=` lines behind them, the
#       `selftest judge=` lines (own report accepted, six forged reports
#       rejected) and `selftest cases=8 failures=<k>`; exit 0 only when all
#       eight cases ran, every positive passed and every mutant was rejected.
#   bash corpus/instruments/r39-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# THE GREEN WINDOW (measured, not assumed). G2 requires the committed receipt
# `.ufo/waves/round-39/final-gates/all-gates.txt` inside the export, and that
# receipt's `export-ref=` names the round-39 judged head J. A commit cannot
# contain its own hash, so at J the receipt is absent by construction and the
# suite prints `closed=7/8 exit=1` (G2 red, fail-closed). The 8/8 window is the
# lane tip Y = J + the receipt alone (`git diff --name-only J Y` = that one
# path): at Y, G2 reads the receipt, finds `export-ref=J`, `J` is an ancestor of
# Y and the post-receipt diff lists only the receipt. Both limbs are measured in
# `.ufo/waves/round-39/wave1/ExecSuiteBuild.md` §Runs. The frozen C1 predicate
# phrases the counting command over J; the honest 8/8 run is over Y, which is
# the round's own M39-1/R1 defect (a frozen counting command must be satisfiable
# by a commit that cannot name itself).
#
# The eight checks:
#   G1 (whole-tail declarations) `.ufo/waves/round-39/declared-blocks.txt` in
#       the export declares >=1 block for each front door among PROVINCE.md and
#       corpus/README.md. Every declaration line `<path> <lines> <sha256>` must
#       satisfy `tail -n <lines> <path> | sha256sum` = <sha256>, its path must
#       be a plain relative path that exists inside the export (no `/` root, no
#       `..` component), and its <lines> must equal the added-line count of
#       `git diff --numstat <base> <ref> -- <path>` with zero deleted lines for
#       that path: the declared block is the WHOLE appended tail, not a suffix
#       of it. A CommonMark fence walk models backtick AND tilde fences (an
#       opener is up to three leading blanks then three backticks or three
#       tildes, optional info string; a closer is the same character run of
#       exactly three followed by blanks only) and must end CLOSED at EOF for
#       both front doors. A `Correction (round 39)` line counts only when it sits
#       OUTSIDE a fence at that line; a correction line inside an open fence is
#       counted as `corrections-inside` and reds the check, and a counted
#       correction must lie inside that file's declared tail.
#   G2 (graded receipt) `.ufo/waves/round-39/final-gates/all-gates.txt` in the
#       export starts with `all-gates v3`; carries exactly one
#       `export-ref=<40 hex>` whose commit exists in the lane, is
#       ancestor-or-equal of the exported ref, and `git diff --name-only
#       <export-ref> <ref>` lists nothing but that receipt; exactly one
#       `suite-sha256=<digest>` equal to the digest of the bytes executing AND
#       of the export's own copy at `corpus/instruments/r39-closure.sh`; exactly
#       eight `G<n> payload=... closed=1` lines (distinct ids, zero closed=0
#       lines); exactly one `closed=8/8 exit=0`; exactly eight GRADED
#       `selftest case=G<n> ... positive=pass ... verdict=pass` lines with zero
#       ungraded case lines and one `selftest cases=8 failures=0`. Grading rule:
#       every line beginning `selftest case=` is parsed; it counts only when
#       BOTH a `positive=pass` field and a `verdict=pass` field are present, so
#       a summary-only line (or a `verdict=fail` line) never satisfies a case.
#       Plus: the SCORECARD.md `## Round 39` section and SHONEN.md's round-39
#       lines carry the string
#       `judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt`
#       and zero `Final lane commit:` lines.
#   G3 (committed-run truth) Every line this round ADDS to SCORECARD.md,
#       SHONEN.md, LOG.md or corpus/lessons/round-38.md (added lines of
#       `git diff <base> <ref>`, `+` not `+++`) that quotes a run — it contains
#       `closed=` and a `--export-ref <hex>` token — must either carry the
#       literal label `report-only` on that line, or name a ref that appears in
#       a committed transcript file under `.ufo/waves/round-39/final-gates/` in
#       the export. A quoted run with no committed transcript and no label is
#       RED. Base lines are exempt: a prior round's debt is not this round's
#       quote, and the round-38 lesson (R3) records the historical class.
#   G4 (seat identity) For every tracked `.ufo/waves/round-39/*-dispatch.json`
#       in the export (at least one required), a sibling `-results.json` (or the
#       dispatcher's `<wave>-results.json`, whose `wave` must then equal the
#       dispatch's) exists in the same directory, parses as JSON, and lists
#       exactly `len(taskCall.tasks)` seat entries whose IDENTITIES are distinct.
#       The identity field is the first of `id`, `name`, `seat`, `agent` present
#       in every entry (the round-38 results file carries `name`, 73 distinct,
#       with `agent` a 9-valued role field); a missing field is RED, a duplicate
#       value is RED, and a dispatch with zero tasks is RED (0 == 0 is not a
#       closure).
#   G5 (label drift) The SCORECARD.md `## Round 39` section (from `^## Round 39`
#       to the next `^## ` heading) has zero `Final lane commit:` lines, and
#       SCORECARD.md carries >=1 line beginning `Correction (round 39)` that
#       names `f06148c6` and labels that round-38 overstate `report-only`.
#   G6 (scratch quiescence) LIVE (not export) and FAIL-CLOSED. Under the scratch
#       root, `kasegi-r37` and `kasegi-r38` are absent or hold zero entries;
#       `kasegi-r39` is absent or holds no entry other than the realpath of this
#       run's own --work dir (or its top-level parent under `kasegi-r39`, which
#       is tolerated only when every level below it holds nothing but the next
#       path component toward --work). Every entry counts (file, dotfile,
#       symlink, directory); a directory whose scan fails is RED
#       (`read=fail`), never silently zero; the tolerated entry is printed
#       (`tolerated=`).
#   G7 (ledger fill) corpus/knowledge/considerthese-proposals-ledger.md carries
#       the heading `## Round-39 dispositions (appended 2026-10-26)` AFTER the
#       round-38 dispositions section; inside it a line beginning
#       `Correction (round 39)` and at least three table data rows whose first
#       cell is a proposal number (leading digits, optionally `.` and text),
#       with proposals 1 and 3 among them.
#   G8 (pinned carry-over) The round-37 suite bytes pinned at commit
#       `2387dcf6ccfefcfb703783387b9aade8fc82abfa` are extracted with
#       `git show <pin>:corpus/instruments/r37-closure.sh` into
#       `<work>/r37-pinned/r37-closure.sh` and must hash to the pinned digest
#       (a constant of this file, measured at the pin); the export's own copy
#       `corpus/instruments/r37-closure.sh` must hash to that same digest BEFORE
#       it is trusted; the pinned bytes are then run with
#       `--export-ref <ref> --lane <lane> --work <work>/r37` and must end with
#       `closed=14/14 exit=0` and exit 0.
#
# Documented limits (measured, not hidden):
#   - G1's fence walk follows the contract's spelling: an opener is exactly
#     three backticks or three tildes (with an optional info string, so a
#     four-backtick opener is read as three plus the info string "`"), and a
#     closer is exactly three of the same character plus blanks. It does not
#     track longer closing runs; a ```` closer does not close a fence.
#   - G1 counts `Correction (round 39)` only at line start; a correction quoted
#     mid-paragraph does not count (and so cannot red the inside-fence limb).
#     Corrections of earlier rounds are out of scope by construction.
#   - G1's added-line limb reads the lane diff: base 480b1a50 is a constant of
#     this file, so a ref older than the base cannot be measured (red, not
#     skipped). A path that is declared twice is validated twice.
#   - G2 accepts ancestor-or-EQUAL (`export-ref` == the exported ref passes
#     with a vacuous diff), as the frozen predicate says. The cross-run payload
#     VALUE comparison is not a limb: recorded payload keys are printed by this
#     suite and the receipt is the run's own transcript (see G8 for the pinned
#     analogue that does compare bytes).
#   - G2's `Final lane commit:` scan is literal and case-sensitive on the
#     SCORECARD section and on SHONEN's round-39 lines; keep the label off those
#     lines entirely.
#   - G3 exempts base lines and reads the lane diff, so a quote added and then
#     removed inside the same commit range is invisible; it requires a ref
#     token (`--export-ref <hex>`), so a quote that names its head only as "J"
#     is out of scope.
#   - G4 compares identities by exact string; a results file that lists the
#     right number of distinct WRONG seats is not caught here (the dispatch is
#     the authority for names, not this check).
#   - G6 tolerates this run's own work dir (and a clean chain toward it)
#     because a seat that keeps its work under its own scratch would otherwise
#     red itself; the CONTENTS of --work are not audited: it is the caller's own
#     space, cleared of `export/`, `mut/`, `r37/` and `r37-pinned/`.
#   - G8 executes the pinned r37 suite, which takes its OWN live reads (E9
#     worktree/HEAD/scratch limbs) against --lane: at the real judged head the
#     lane must be checked out at Y with a clean tree, else G8 reds by
#     construction.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku
BASE_REF=480b1a505a2dfc14a4f718d16d63808247214d0a
PIN_REF=2387dcf6ccfefcfb703783387b9aade8fc82abfa
PIN_R37_SHA=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d
CHECK_IDS=(G1 G2 G3 G4 G5 G6 G7 G8)

# SELF — absolute physical path of the executing bytes. Resolved once at load
# time because G2 calls suite_digest() from inside a subshell that has cd'd into
# the export tree; a relative BASH_SOURCE would then name the wrong file.
SELF=${BASH_SOURCE[0]:-}
case $SELF in
  /*) ;;
  *)  if [ -n "$SELF" ] && [ -d "$(dirname -- "$SELF")" ]; then
        SELF=$( cd -- "$(dirname -- "$SELF")" && pwd -P )/$(basename -- "$SELF")
      fi ;;
esac

MODE=run
EXPORT_REF=
WORK_ARG=
REF_RESOLVED=
WORK=
EXPORT=
MUT=
WORK_AUTO=0
LANE_OVERRIDE=0
SCRATCH_OVERRIDE=0
CASES=0
FAILS=0

# suite_digest — sha256 of the bytes actually executing. Printed in the report so
# a reader can bind a `closed=8/8` line (and the committed all-gates.txt) to the
# instrument that produced it. An unreadable SELF prints `unreadable`, which
# matches no 64-hex digest.
suite_digest() {
  local s=${SELF:-}
  if [ -z "$s" ] || [ ! -r "$s" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$s" | awk '{print $1; exit}'
}

# file_digest FILE — sha256 of an arbitrary file, `unreadable` when the read
# fails (never an empty string that a missing digest could be compared to).
file_digest() {
  local f=$1
  if [ -z "$f" ] || [ ! -r "$f" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$f" | awk '{print $1; exit}'
}

usage() {
  # the header block only: line 2 through the last comment line before the
  # option-less `set` line, so the help cannot drift from the docs.
  sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

die() { # MESSAGE...
  printf 'r39-closure: %s\n' "$*" >&2
  exit 2
}

parse_args() {
  while [ $# -gt 0 ]; do
    case $1 in
      --export-ref)
        [ $# -ge 2 ] || die '--export-ref needs a commit-ish'
        EXPORT_REF=$2; shift 2 ;;
      --work)
        [ $# -ge 2 ] || die '--work needs a directory'
        WORK_ARG=$2; shift 2 ;;
      --lane)
        [ $# -ge 2 ] || die '--lane needs a directory'
        LANE=$2; LANE_OVERRIDE=1; shift 2 ;;
      --scratch-root)
        [ $# -ge 2 ] || die '--scratch-root needs a directory'
        SCRATCH_ROOT=$2; SCRATCH_OVERRIDE=1; shift 2 ;;
      --selftest)
        MODE=selftest; shift ;;
      -h|--help)
        usage; exit 0 ;;
      *)
        printf 'r39-closure: unknown argument: %s\n' "$1" >&2
        usage >&2
        exit 2 ;;
    esac
  done
}

cleanup() {
  [ -n "${EXPORT:-}" ] && rm -rf -- "$EXPORT"
  [ -n "${MUT:-}" ] && rm -rf -- "$MUT"
  [ -n "${WORK:-}" ] && rm -rf -- "$WORK/r37" "$WORK/r37-pinned"
  if [ "${WORK_AUTO:-0}" = 1 ] && [ -n "${WORK:-}" ]; then rm -rf -- "$WORK"; fi
}

make_work() {
  if [ -n "$WORK_ARG" ]; then
    # Guard BEFORE creating anything: a refused --work must leave no trace.
    local norm
    norm=$(realpath -m -- "$WORK_ARG") || die "cannot resolve work dir: $WORK_ARG"
    case $norm in
      "$LANE"|"$LANE"/*) die "--work must be outside the lane (it would write there): $norm" ;;
      /) die '--work must not be /' ;;
    esac
    mkdir -p -- "$norm" || die "cannot create work dir: $norm"
    WORK=$( cd "$norm" && pwd -P ) || die "cannot resolve work dir: $norm"
    # Re-check the physical path: a symlink may point into the lane.
    case $WORK in
      "$LANE"|"$LANE"/*) die "--work resolves inside the lane: $WORK" ;;
    esac
    WORK_AUTO=0
  else
    # TMPDIR is honoured by mktemp itself; no path is hardcoded here.
    WORK=$(mktemp -d -t r39-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  # Clear every owned subdirectory: a reused --work must never let a stale
  # export or a stale pinned copy satisfy a check.
  rm -rf -- "$EXPORT" "$MUT" "$WORK/r37" "$WORK/r37-pinned"
  mkdir -p -- "$EXPORT" "$MUT" || die "cannot populate work dir: $WORK"
  trap cleanup EXIT
}

prepare_export() {
  local want=${1:-$EXPORT_REF}
  [ -n "$want" ] || die 'export mode requires --export-ref <hash>'
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  git -C "$LANE" rev-parse --git-dir >/dev/null 2>&1 \
    || die "lane is not a git repository: $LANE"
  REF_RESOLVED=$(git -C "$LANE" rev-parse --verify --quiet "${want}^{commit}") \
    || die "cannot resolve export ref in $LANE: $want"
  make_work
  git -C "$LANE" archive --format=tar "$REF_RESOLVED" | tar -xf - -C "$EXPORT" \
    || die "git archive export failed for $REF_RESOLVED"
  [ -f "$EXPORT/SCORECARD.md" ] \
    || die "export has no SCORECARD.md (not a lane tree): $REF_RESOLVED"
}

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

count_lines() { # reads stdin
  grep -c . || true
}

# md_section FILE ERE — the LAST level-2 section whose heading line matches ERE,
# closed by the next `^## ` heading (or EOF). Section scoping is what makes a
# "nowhere inside this section" limb a real assertion instead of a file-wide one
# that some historical line satisfies.
md_section() { # FILE ERE
  awk -v pat="$2" '
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i <= NR; i++) if (line[i] ~ pat) start = i
      if (start == 0) exit
      for (i = start; i <= NR; i++) {
        if (i > start && line[i] ~ /^## /) break
        print line[i]
      }
    }
  ' "$1"
}

# g1_scan FILE — one pass that counts `Correction (round 39)` lines outside and
# inside fences, records the line numbers of the outside ones, and reports the
# fence state at EOF. Fence spelling (contract): opener = up to three blanks
# then three backticks or three tildes, optional info string; closer = up to
# three blanks then three of the SAME character and blanks only. Prints
# `<outside> <inside> <total> <closed|open> <line[,line...]>`.
g1_scan() { # FILE
  awk '
    { s = $0
      if (!open) {
        if (index(s, "Correction (round 39)") == 1) {
          outside++; lines = lines (lines == "" ? "" : ",") NR
        }
        if (s ~ /^ {0,3}```/) { open = 1; ftype = "`" }
        else if (s ~ /^ {0,3}~~~/) { open = 1; ftype = "~" }
      } else {
        if (index(s, "Correction (round 39)") == 1) inside++
        if (ftype == "`" && s ~ /^ {0,3}```[ \t]*$/) open = 0
        else if (ftype == "~" && s ~ /^ {0,3}~~~[ \t]*$/) open = 0
      }
    }
    END { print outside + 0, inside + 0, NR + 0, (open ? "open" : "closed"), (lines == "" ? "-" : lines) }
  ' "$1"
}

# g1_numstat PATH — prints `<added> <deleted>` for the ref-scoped append of one
# path, or `ERR` when the diff read fails. `--no-optional-locks` keeps the read
# from taking an index lock under the lane; the exit status is what decides.
g1_numstat() { # REF PATH
  local out
  if out=$(git --no-optional-locks -C "$LANE" diff --numstat "$BASE_REF" "$1" -- "$2"); then
    if [ -z "$out" ]; then printf '0 0'; return 0; fi
    printf '%s\n' "$out" | awk 'NF >= 2 { print $1, $2; exit }'
    return 0
  fi
  printf 'ERR'
}

# g1_path_safe PATH — a declaration may only name a plain relative path inside
# the export: no absolute path, no `..` component, no empty component. An
# escaping declaration used to validate bytes OUTSIDE the tree (round-38 hole
# G1-H4).
g1_path_safe() { # PATH
  local p=$1 c rest
  case $p in ''|/*) return 1 ;; esac
  rest=$p
  while :; do
    c=${rest%%/*}
    case $c in ''|.) return 1 ;; ..) return 1 ;; esac
    case $rest in
      */*) rest=${rest#*/} ;;
      *) break ;;
    esac
  done
  return 0
}

# g2_graded FILE — parses EVERY `selftest case=` line of a receipt. Prints
# `<total> <graded> <ungraded-cases> <distinct-graded-ids>`.
# A case line counts only when a `positive=pass` field AND a `verdict=pass`
# field are both present; the id must be G1..G8. A summary-only line (one
# without per-case fields) never satisfies a case.
g2_graded() { # FILE
  awk '
    function field(line, name,   i, n, a, k) {
      n = split(line, a, /[ ,]+/)
      for (i = 1; i <= n; i++) {
        if (a[i] == name) return 1
      }
      return 0
    }
    /^selftest case=/ {
      total++
      if ($0 ~ /^selftest case=G[1-8]( |$)/ && field($0, "positive=pass") && field($0, "verdict=pass")) {
        graded++
        id = $0
        sub(/^selftest case=/, "", id)
        sub(/ .*/, "", id)
        seen[id] = 1
      } else {
        ungraded++
      }
    }
    END { n = 0; for (id in seen) n++; print total + 0, graded + 0, ungraded + 0, n }
  ' "$1"
}

# g2_run_shapes FILE — run-block limbs for the receipt: prints
# `<closed1-lines> <closed0-lines> <distinct-ids> <closed8-line>`.
g2_run_shapes() { # FILE
  local p=$1 c1 c0 ids cl
  c1=$(grep -cE '^G[1-8] payload=.* closed=1$' "$p"); c1=${c1:-0}
  c0=$(grep -cE '^G[0-9]+ payload=.* closed=0$' "$p"); c0=${c0:-0}
  ids=$(grep -E '^G[1-8] payload=.* closed=1$' "$p" \
    | sed -n 's/^\(G[1-8]\) payload=.*/\1/p' | sort -u | count_lines); ids=${ids:-0}
  cl=$(grep -cE '^closed=8/8 exit=0$' "$p"); cl=${cl:-0}
  printf '%s %s %s %s' "$c1" "$c0" "$ids" "$cl"
}

# g3_refs LINE — the refs a quoting line names: every `<hex>` argument of
# `--export-ref`, 7..40 hex characters, one per line.
g3_refs() { # LINE
  printf '%s\n' "$1" | grep -oE -- '--export-ref[ =]+[0-9a-f]{7,40}' \
    | sed -n 's/.*[ =]\([0-9a-f]\{7,40\}\)$/\1/p'
}

# g4_pair DISPATCH RESULTS — one stdlib read of both JSON files. Prints
# `parse=ok|bad,tasks=<n>|bad,results=<n>|bad,ident=<field>|none,distinct=0|1,wave=<v>,rwave=<v>`.
g4_pair() { # DISPATCH RESULTS
  python3 -c '
import json, sys

def load(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return None

d = load(sys.argv[1])
r = load(sys.argv[2])
out = []
ok = d is not None and r is not None
out.append("parse=" + ("ok" if ok else "bad"))
tasks = None
if isinstance(d, dict):
    tc = d.get("taskCall")
    if isinstance(tc, dict) and isinstance(tc.get("tasks"), list):
        tasks = tc["tasks"]
out.append("tasks=" + (str(len(tasks)) if tasks is not None else "bad"))
entries = None
if isinstance(r, dict):
    if isinstance(r.get("results"), list):
        entries = r["results"]
    elif isinstance(r.get("seats"), list):
        entries = r["seats"]
out.append("results=" + (str(len(entries)) if entries is not None else "bad"))
ident = "none"
distinct = 0
if isinstance(entries, list) and entries:
    for field in ("id", "name", "seat", "agent"):
        vals = []
        for e in entries:
            if not isinstance(e, dict):
                break
            v = e.get(field)
            if not isinstance(v, str) or v == "":
                break
            vals.append(v)
        else:
            ident = field
            distinct = 1 if len(set(vals)) == len(vals) else 0
            break
out.append("ident=" + ident)
out.append("distinct=" + str(distinct))
wave = d.get("wave") if isinstance(d, dict) else None
rwave = r.get("wave") if isinstance(r, dict) else None
out.append("wave=" + (wave if isinstance(wave, str) else ""))
out.append("rwave=" + (rwave if isinstance(rwave, str) else ""))
print(",".join(out))
' "$1" "$2"
}

# g6_root_state DIR — absent|empty|present|unreadable. Every entry counts (file,
# dotfile, symlink, directory); a scan that fails is `unreadable`, never
# `empty`. No stderr suppression: a broken scan must not read as quiescent.
g6_root_state() { # DIR
  local d=$1 out n
  if [ -d "$d" ]; then
    if out=$(find "$d" -mindepth 1 -maxdepth 1 -print); then
      n=$(printf '%s\n' "$out" | count_lines); n=${n:-0}
      if [ "$n" -gt 0 ]; then printf 'present'; else printf 'empty'; fi
    else
      printf 'unreadable'
    fi
  elif [ -e "$d" ] || [ -L "$d" ]; then
    printf 'present'
  else
    printf 'absent'
  fi
}

# g6_chain_ok ANCESTOR WORK — the parent carve-out's guard: every level strictly
# between ANCESTOR and WORK must hold exactly one entry, the next component of
# the canonical path toward WORK. A sibling leftover under the tolerated parent
# is therefore still RESIDUAL.
g6_chain_ok() { # ANCESTOR WORK
  local dir=$1 rest=${2#"$1"/} next e real n
  while [ -n "$rest" ]; do
    next=${rest%%/*}
    n=0; real=''
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      n=$((n + 1))
      real=$( cd "$e" && pwd -P )
    done < <(find "$dir" -mindepth 1 -maxdepth 1 -print)
    [ "$n" -eq 1 ] || return 1
    [ "$real" = "$dir/$next" ] || return 1
    dir=$real
    case $rest in
      */*) rest=${rest#*/} ;;
      *) rest='' ;;
    esac
  done
  return 0
}

# g7_rows SECTION — prints the proposal numbers found as the FIRST cell of table
# data rows, one per line. The cell must be leading digits (optionally followed
# by `.` and text): `1x` is not proposal 1 (round-38 hole G7-H1).
g7_rows() { # reads the section on stdin
  awk -F'|' '
    /^\|/ {
      c = $2
      gsub(/^[ \t]+|[ \t]+$/, "", c)
      sub(/\..*/, "", c)
      if (c ~ /^[0-9]+$/) print c + 0
    }
  ' | sort -un
}

# ---------------------------------------------------------------------------
# checks — every one cd's into the export root and reads relative paths there
# ---------------------------------------------------------------------------

check_g1() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-39/declared-blocks.txt
    local line path lines sha extra got add del nm
    local declared=0 valid=0 tail_match=0 paths=1 doors=0 diffread=ok pure=1
    local decl_p=0 decl_r=0 have_p=0 have_r=0
    local pf=absent rf=absent pout=0 pin=0 routh=0 rin=0 ptotal=0 rtotal=0 plines='-' rlines='-'
    local cor_decl=1 c
    if [ -f "$p" ]; then
      while IFS= read -r line || [ -n "$line" ]; do
        case $line in ''|'#'*) continue ;; esac
        declared=$((declared + 1))
        set -f
        set -- $line
        set +f
        path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
        if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
          continue
        fi
        case $lines in ''|*[!0-9]*) continue ;; esac
        [ "$lines" -ge 1 ] || continue
        case $sha in ''|*[!0-9a-f]*) continue ;; esac
        [ "${#sha}" -eq 64 ] || continue
        if ! g1_path_safe "$path"; then paths=0; continue; fi
        if [ ! -f "$tree/$path" ]; then paths=0; continue; fi
        got=$(tail -n "$lines" -- "$tree/$path" | sha256sum | awk '{print $1; exit}')
        [ "$got" = "$sha" ] || continue
        nm=$(g1_numstat "$ref" "$path")
        case $nm in
          ERR) diffread=fail; continue ;;
          0\ 0) continue ;;
        esac
        set -f
        set -- $nm
        set +f
        add=${1:-}; del=${2:-}
        [ "$add" = "$lines" ] || continue
        tail_match=$((tail_match + 1))
        [ "$del" = 0 ] || { pure=0; continue; }
        valid=$((valid + 1))
        case $path in
          PROVINCE.md) have_p=1; decl_p=$lines ;;
          corpus/README.md) have_r=1; decl_r=$lines ;;
        esac
      done < "$p"
    else
      diffread=missing
    fi
    [ "$have_p" -eq 1 ] && [ "$have_r" -eq 1 ] && doors=2
    if [ -f PROVINCE.md ]; then
      read -r pout pin ptotal pf plines <<< "$(g1_scan PROVINCE.md)"
      [ "$pf" = closed ] || pf=open
      [ "$pin" -eq 0 ] || cor_decl=0
      if [ "$decl_p" -ge 1 ] && [ "$plines" != '-' ]; then
        for c in $(printf '%s' "$plines" | tr ',' ' '); do
          # a counted correction must lie inside the declared tail
          [ "$c" -gt $((ptotal - decl_p)) ] || cor_decl=0
        done
      elif [ "$plines" != '-' ] && [ "$decl_p" -lt 1 ]; then
        # a counted correction with no declaration for this door is not declared
        cor_decl=0
      fi
    fi
    if [ -f corpus/README.md ]; then
      read -r routh rin rtotal rf rlines <<< "$(g1_scan corpus/README.md)"
      [ "$rf" = closed ] || rf=open
      [ "$rin" -eq 0 ] || cor_decl=0
      if [ "$decl_r" -ge 1 ] && [ "$rlines" != '-' ]; then
        for c in $(printf '%s' "$rlines" | tr ',' ' '); do
          [ "$c" -gt $((rtotal - decl_r)) ] || cor_decl=0
        done
      elif [ "$rlines" != '-' ] && [ "$decl_r" -lt 1 ]; then
        cor_decl=0
      fi
    fi
    printf 'declared=%s,valid=%s,front-doors=%s,tail-match=%s,pure-append=%s,paths=%s,province-fence=%s,readme-fence=%s,corrections-outside=%s,corrections-inside=%s,corrections-declared=%s,diff-read=%s' \
      "$declared" "$valid" "$doors" "$tail_match" "$pure" "$paths" "$pf" "$rf" \
      "$((pout + routh))" "$((pin + rin))" "$cor_decl" "$diffread"
    [ "$diffread" = ok ] && [ "$declared" -ge 2 ] && [ "$valid" -eq "$declared" ] \
      && [ "$doors" -eq 2 ] && [ "$pure" -eq 1 ] && [ "$paths" -eq 1 ] \
      && [ "$pf" = closed ] && [ "$rf" = closed ] && [ "$pin" -eq 0 ] && [ "$rin" -eq 0 ] \
      && [ "$cor_decl" -eq 1 ] && exit 0
    exit 1
  )
}

check_g2() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-39/final-gates/all-gates.txt
    local phrase='judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt'
    local suite=corpus/instruments/r39-closure.sh
    local file=0 sentinel=0 xref='' xsha='' ancestor=0 diffclean=0 diffread=ok
    local digest=0 export_suite=0 run_ok=0 closed_ok=0 graded_ok=0 summary=0
    local scref=0 shonenref=0 fin=0 n name scoped bad c1 c0 ids cl total g ungr dist
    if [ -f "$p" ]; then
      file=1
      [ "$(sed -n '1p' "$p")" = 'all-gates v3' ] && sentinel=1
      n=$(grep -cE '^export-ref=[0-9a-f]{40}$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && xref=$(sed -n 's/^export-ref=//p' "$p")
      n=$(grep -cE '^suite-sha256=[0-9a-f]{64}$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && xsha=$(sed -n 's/^suite-sha256=//p' "$p")
      if [ -n "$xref" ]; then
        if c=$(git -C "$LANE" cat-file -t "${xref}^{commit}" 2>&1); then
          if git -C "$LANE" merge-base --is-ancestor "$xref" "$ref"; then
            ancestor=1
          fi
          if name=$(git --no-optional-locks -C "$LANE" diff --name-only "$xref" "$ref"); then
            bad=0
            while IFS= read -r scoped; do
              [ -n "$scoped" ] || continue
              [ "$scoped" = "$p" ] || bad=1
            done <<< "$name"
            [ "$bad" -eq 0 ] && diffclean=1
          else
            diffread=fail
          fi
        fi
      fi
      if [ -n "$xsha" ] && [ "$xsha" = "$(suite_digest)" ]; then digest=1; fi
      if [ -f "$suite" ] && [ -n "$xsha" ] && [ "$xsha" = "$(file_digest "$suite")" ]; then
        export_suite=1
      fi
      read -r c1 c0 ids cl <<< "$(g2_run_shapes "$p")"
      [ "$c1" -eq 8 ] && [ "$c0" -eq 0 ] && [ "$ids" -eq 8 ] && run_ok=1
      [ "$cl" -eq 1 ] && closed_ok=1
      read -r total g ungr dist <<< "$(g2_graded "$p")"
      [ "$total" -eq 8 ] && [ "$g" -eq 8 ] && [ "$ungr" -eq 0 ] && [ "$dist" -eq 8 ] && graded_ok=1
      n=$(grep -cE '^selftest cases=8 failures=0$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && summary=1
    fi
    if [ -f SCORECARD.md ]; then
      scoped=$(md_section SCORECARD.md '^## Round 39([^0-9]|$)')
      if [ -n "$scoped" ]; then
        n=$(printf '%s\n' "$scoped" | grep -cF -- "$phrase"); n=${n:-0}
        [ "$n" -ge 1 ] && scref=1
        n=$(printf '%s\n' "$scoped" | grep -cF 'Final lane commit:'); n=${n:-0}
        fin=$((fin + n))
      fi
    fi
    if [ -f SHONEN.md ]; then
      scoped=$(grep -E 'round 39|round-39' SHONEN.md)
      if [ -n "$scoped" ]; then
        n=$(printf '%s\n' "$scoped" | grep -cF -- "$phrase"); n=${n:-0}
        [ "$n" -ge 1 ] && shonenref=1
        n=$(printf '%s\n' "$scoped" | grep -cF 'Final lane commit:'); n=${n:-0}
        fin=$((fin + n))
      fi
    fi
    printf 'receipt=%s,sentinel=%s,export-ref=%s,ancestor=%s,diff-clean=%s,diff-read=%s,digest-match=%s,export-suite=%s,run-lines=%s,closed-lines=%s,distinct-ids=%s,closed-line=%s,graded-cases=%s,ungraded-cases=%s,selftest-summary=%s,scorecard-ref=%s,shonen-ref=%s,final-lane-commit=%s' \
      "$file" "$sentinel" "$([ -n "$xref" ] && echo 1 || echo 0)" "$ancestor" "$diffclean" \
      "$diffread" "$digest" "$export_suite" "${c1:-0}" "${c0:-0}" "${ids:-0}" "$closed_ok" \
      "${g:-0}" "${ungr:-0}" "$summary" "$scref" "$shonenref" "$fin"
    [ "$file" -eq 1 ] && [ "$sentinel" -eq 1 ] && [ -n "$xref" ] && [ "$ancestor" -eq 1 ] \
      && [ "$diffclean" -eq 1 ] && [ "$diffread" = ok ] && [ "$digest" -eq 1 ] \
      && [ "$export_suite" -eq 1 ] && [ "$run_ok" -eq 1 ] && [ "$closed_ok" -eq 1 ] \
      && [ "$graded_ok" -eq 1 ] && [ "$summary" -eq 1 ] && [ "$scref" -eq 1 ] \
      && [ "$shonenref" -eq 1 ] && [ "$fin" -eq 0 ] && exit 0
    exit 1
  )
}

check_g3() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local gdir=.ufo/waves/round-39/final-gates
    local out added line refs r quotes=0 covered=0 uncovered=0 report_only=0 diffread=ok hit
    if out=$(git --no-optional-locks -C "$LANE" diff --no-color "$BASE_REF" "$ref" -- \
               SCORECARD.md SHONEN.md LOG.md corpus/lessons/round-38.md); then
      added=$(printf '%s\n' "$out" | grep '^+' | grep -v '^+++')
    else
      diffread=fail
      added=''
    fi
    if [ "$diffread" = ok ]; then
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        case $line in *closed=*) ;; *) continue ;; esac
        refs=$(g3_refs "$line")
        [ -n "$refs" ] || continue
        quotes=$((quotes + 1))
        case $line in
          *report-only*)
            report_only=$((report_only + 1))
            for r in $refs; do covered=$((covered + 1)); done
            continue ;;
        esac
        for r in $refs; do
          hit=0
          if [ -d "$gdir" ] && grep -rqF -- "$r" "$gdir"; then hit=1; fi
          if [ "$hit" -eq 1 ]; then
            covered=$((covered + 1))
          else
            uncovered=$((uncovered + 1))
          fi
        done
      done <<< "$added"
    fi
    printf 'added-quotes=%s,covered=%s,uncovered=%s,report-only=%s,diff-read=%s' \
      "$quotes" "$covered" "$uncovered" "$report_only" "$diffread"
    [ "$diffread" = ok ] && [ "$uncovered" -eq 0 ] && exit 0
    exit 1
  )
}

# kv_get STR KEY — the value of `KEY=` in a comma-joined k=v payload.
kv_get() { # STR KEY
  printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1
}

check_g4() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local dir=.ufo/waves/round-39
    local read=fail f base res dinfo info wave tasks results ident distinct
    local disp=0 pairs=0 seats_ok=0 zero=0 rwave
    if [ -d "$dir" ]; then
      read=ok
      while IFS= read -r f; do
        [ -n "$f" ] || continue
        disp=$((disp + 1))
        base=${f%-dispatch.json}
        res=$base-results.json
        dinfo=$(g4_pair "$f" "$f")
        [ "$(kv_get "$dinfo" parse)" = ok ] || continue
        wave=$(kv_get "$dinfo" wave)
        if [ ! -f "$res" ]; then
          if [ -n "$wave" ] && [ -f "$dir/$wave-results.json" ]; then res=$dir/$wave-results.json; fi
        fi
        [ -f "$res" ] || continue
        info=$(g4_pair "$f" "$res")
        [ "$(kv_get "$info" parse)" = ok ] || continue
        rwave=$(kv_get "$info" rwave)
        if [ -n "$wave" ] && [ -n "$rwave" ] && [ "$wave" != "$rwave" ]; then continue; fi
        pairs=$((pairs + 1))
        tasks=$(kv_get "$info" tasks)
        results=$(kv_get "$info" results)
        ident=$(kv_get "$info" ident)
        distinct=$(kv_get "$info" distinct)
        case $tasks in ''|*[!0-9]*) continue ;; esac
        [ "$tasks" -eq 0 ] && zero=$((zero + 1))
        case $results in ''|*[!0-9]*) continue ;; esac
        if [ "$tasks" -ge 1 ] && [ "$results" -eq "$tasks" ] \
           && [ "$ident" != none ] && [ "$distinct" = 1 ]; then
          seats_ok=$((seats_ok + 1))
        fi
      done < <(find "$dir" -maxdepth 1 -name '*-dispatch.json' | sort)
    fi
    printf 'dispatches=%s,pairs=%s,seats-ok=%s,zero-task=%s,read=%s' \
      "$disp" "$pairs" "$seats_ok" "$zero" "$read"
    [ "$read" = ok ] && [ "$disp" -ge 1 ] && [ "$pairs" -eq "$disp" ] \
      && [ "$seats_ok" -eq "$disp" ] && [ "$zero" -eq 0 ] && exit 0
    exit 1
  )
}

check_g5() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local sec='' sect=0 fin=0 cor=0 ro=0
    if [ -f SCORECARD.md ]; then
      sec=$(md_section SCORECARD.md '^## Round 39([^0-9]|$)')
      [ -n "$sec" ] && sect=1
      if [ "$sect" -eq 1 ]; then
        fin=$(printf '%s\n' "$sec" | grep -cF 'Final lane commit:'); fin=${fin:-0}
      fi
      cor=$(awk 'index($0, "Correction (round 39)") == 1 && index($0, "f06148c6") > 0 \
                 { n++ } END { print n + 0 }' SCORECARD.md)
      ro=$(awk 'index($0, "Correction (round 39)") == 1 && index($0, "f06148c6") > 0 \
                && tolower($0) ~ /report[- ]?only/ { n++ } END { print n + 0 }' SCORECARD.md)
    fi
    printf 'round39-section=%s,final-lane-commit=%s,correction=%s,correction-labeled=%s' \
      "$sect" "$fin" "$cor" "$ro"
    [ "$sect" -eq 1 ] && [ "$fin" -eq 0 ] && [ "$cor" -ge 1 ] && [ "$ro" -ge 1 ] && exit 0
    exit 1
  )
}

check_g6() { # TREE REF
  local sroot=$SCRATCH_ROOT
  local r37=absent r38=absent r39=absent read=ok work=outside
  local realw='' e real out tol=none
  if [ -n "${WORK:-}" ]; then realw=$( cd "$WORK" && pwd -P ); fi
  if [ -z "$realw" ]; then
    printf 'r37=?,r38=?,r39=?,work=unknown,tolerated=none,read=fail'
    return 1
  fi
  [ -d "$sroot" ] && sroot=$( cd "$sroot" && pwd -P )
  case $realw in "$sroot"/kasegi-r39/*) work=inside ;; esac
  r37=$(g6_root_state "$sroot/kasegi-r37")
  r38=$(g6_root_state "$sroot/kasegi-r38")
  [ "$r37" = unreadable ] && read=fail
  [ "$r38" = unreadable ] && read=fail
  # r39: this run's own work dir (or its top-level parent under kasegi-r39) is
  # tolerated, but only when the chain from that parent to WORK is empty of
  # anything else. Entries are judged by realpath, never by name.
  if [ -d "$sroot/kasegi-r39" ]; then
    if out=$(find "$sroot/kasegi-r39" -mindepth 1 -maxdepth 1 -print); then
      r39=empty
      while IFS= read -r e; do
        [ -n "$e" ] || continue
        real=$( cd "$e" && pwd -P )
        if [ -z "$real" ]; then
          r39=present; continue
        fi
        if [ "$real" = "$realw" ]; then
          tol=$real; continue
        fi
        case $realw in
          "$real"/*)
            if g6_chain_ok "$real" "$realw"; then tol=$real; else r39=present; fi
            continue ;;
        esac
        r39=present
      done < <(printf '%s\n' "$out")
    else
      r39=unreadable
      read=fail
    fi
  elif [ -e "$sroot/kasegi-r39" ] || [ -L "$sroot/kasegi-r39" ]; then
    r39=present
  fi
  printf 'r37=%s,r38=%s,r39=%s,work=%s,tolerated=%s,read=%s' \
    "$r37" "$r38" "$r39" "$work" "$tol" "$read"
  [ "$read" = ok ] && [ "$r37" = absent ] && [ "$r38" = absent ] || return 1
  if [ "$r39" = absent ] || [ "$r39" = empty ]; then return 0; fi
  return 1
}

check_g7() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=corpus/knowledge/considerthese-proposals-ledger.md
    local a=0 b=0 sec='' sect=0 cor=0 rows=0 have1=0 have3=0
    if [ -f "$p" ]; then
      a=$(grep -nF -- '## Round-37 dispositions — filled (round 38)' "$p" \
        | head -n 1 | cut -d: -f1); a=${a:-0}
      b=$(grep -nF -- '## Round-39 dispositions (appended 2026-10-26)' "$p" \
        | head -n 1 | cut -d: -f1); b=${b:-0}
      if [ "$a" -gt 0 ] && [ "$b" -gt 0 ] && [ "$b" -gt "$a" ]; then
        sect=1
        sec=$(awk -v s="$b" 'NR >= s { if (NR > s && $0 ~ /^## /) exit; print }' "$p")
        cor=$(printf '%s\n' "$sec" | grep -c '^Correction (round 39)'); cor=${cor:-0}
        rows=$(printf '%s\n' "$sec" | g7_rows | count_lines); rows=${rows:-0}
        if printf '%s\n' "$sec" | g7_rows | grep -qx 1; then have1=1; fi
        if printf '%s\n' "$sec" | g7_rows | grep -qx 3; then have3=1; fi
      fi
    fi
    printf 'section=%s,after-round38=%s,correction=%s,rows=%s,proposal-1=%s,proposal-3=%s' \
      "$sect" "$sect" "$cor" "$rows" "$have1" "$have3"
    [ "$sect" -eq 1 ] && [ "$cor" -ge 1 ] && [ "$rows" -ge 3 ] \
      && [ "$have1" -eq 1 ] && [ "$have3" -eq 1 ] && exit 0
    exit 1
  )
}

check_g8() { # TREE REF
  local tree=$1 ref=$2
  local suite=corpus/instruments/r37-closure.sh
  local pin=$WORK/r37-pinned pinfile=$WORK/r37-pinned/r37-closure.sh
  local psha=unreadable esha=unreadable pinned=0 copy_ok=0 have=0
  local out rc=1 last=''
  mkdir -p -- "$pin" || { printf 'pin-ref=%s,pinned-sha=0,export-copy=0,r37-closed=0,r37-exit=1' "$PIN_REF"; return 1; }
  if git -C "$LANE" show "$PIN_REF:$suite" > "$pinfile"; then
    psha=$(file_digest "$pinfile")
  fi
  [ "$psha" = "$PIN_R37_SHA" ] && pinned=1
  if [ -f "$tree/$suite" ]; then
    have=1
    esha=$(file_digest "$tree/$suite")
    [ "$esha" = "$PIN_R37_SHA" ] && copy_ok=1
  fi
  if [ "$pinned" -eq 1 ]; then
    out=$(bash "$pinfile" --export-ref "$ref" --lane "$LANE" --work "$WORK/r37" 2>&1); rc=$?
    last=$(printf '%s\n' "$out" | grep -v '^$' | tail -n 1)
  fi
  printf 'pin-ref=%s,pinned-sha=%s,export-copy=%s,r37-copy=%s,r37-closed=%s,r37-exit=%s' \
    "$PIN_REF" "$pinned" "$copy_ok" "$have" \
    "$([ "$last" = 'closed=14/14 exit=0' ] && echo 1 || echo 0)" "$rc"
  [ "$pinned" -eq 1 ] && [ "$copy_ok" -eq 1 ] && [ "$last" = 'closed=14/14 exit=0' ] \
    && [ "$rc" -eq 0 ] && return 0
  return 1
}

run_check() { # ID TREE REF
  local id=$1; shift
  # one name derivation instead of a second registry beside CHECK_IDS
  "check_${id,,}" "$@"
}

# ---------------------------------------------------------------------------
# plain (export) run
# ---------------------------------------------------------------------------

run_suite_report() {
  local lines='' id out rc k=0 n=0 counted=0
  local -A RC=()
  printf 'export-ref=%s mode=export lane=%s suite-sha256=%s\n' \
    "$REF_RESOLVED" "$LANE" "$(suite_digest)"
  if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
  if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
  for id in "${CHECK_IDS[@]}"; do
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED"); rc=$?
    RC[$id]=$rc
    if [ "$rc" -eq 0 ]; then
      lines="${lines}${id} payload=${out} closed=1"$'\n'
    else
      lines="${lines}${id} payload=${out} closed=0"$'\n'
    fi
  done
  printf '%s' "$lines"
  n=$(printf '%s' "$lines" | grep -c '^G[0-9] payload=')
  if [ "$n" -ne 8 ]; then
    printf 'suite problem=self-report lines=%s expected=8\n' "$n"
    printf 'closed=0/8 exit=1\n'
    return 1
  fi
  for id in "${CHECK_IDS[@]}"; do
    [ "${RC[$id]}" -eq 0 ] && k=$((k + 1))
  done
  counted=$(printf '%s' "$lines" | grep -c 'closed=1$')
  if [ "$counted" -ne "$k" ]; then
    printf 'suite problem=self-report closed=%s counted=%s\n' "$k" "$counted"
    printf 'closed=0/8 exit=1\n'
    return 1
  fi
  if [ "$k" -eq 8 ]; then
    printf 'closed=%s/8 exit=0\n' "$k"
    return 0
  fi
  printf 'closed=%s/8 exit=1\n' "$k"
  return 1
}

# ---------------------------------------------------------------------------
# selftest fixtures
# ---------------------------------------------------------------------------

mut_reset() { # DIR
  rm -rf -- "$1"
  mkdir -p -- "$1"
}

mut_put() { # DIR RELPATH (stdin)
  mkdir -p -- "$1/$(dirname -- "$2")"
  cat > "$1/$2"
}

# fixture_commit REPO MESSAGE — stage everything and commit with an explicit
# fixture identity (never the lane's); prints the commit id.
fixture_commit() { # REPO MESSAGE
  git -C "$1" add -A || return 1
  git -C "$1" -c user.email=r39-fixture@local -c user.name=r39-fixture \
    commit -q -m "$2" || return 1
  git -C "$1" rev-parse --verify HEAD || return 1
}

# hist_repo_ready REPO — one fixture repository that contains the round-39 base
# commit. Created under --work (outside the lane), its toplevel is asserted
# before any commit, and the fetch is ref-scoped so no other lane state leaks
# in. Prints the physical path on success.
hist_repo_ready() { # REPO
  local repo=$1 top real
  if [ -d "$repo/.git" ]; then printf '%s' "$repo"; return 0; fi
  mkdir -p -- "$repo" || return 1
  git -C "$repo" init -q || return 1
  top=$(git -C "$repo" rev-parse --show-toplevel) || return 1
  real=$( cd "$repo" && pwd -P )
  [ "$top" = "$real" ] || return 1
  git -C "$repo" fetch -q --no-tags "$LANE" "$BASE_REF" || return 1
  git -C "$repo" checkout -q --detach "$BASE_REF" || return 1
  printf '%s' "$real"
}

# hist_reset REPO — back to the base commit, working tree clean.
hist_reset() { # REPO
  git -C "$1" checkout -q -f --detach "$BASE_REF" || return 1
  git -C "$1" clean -qfd || return 1
}

# g1_declare REPO MODE — write declared-blocks.txt for the two front doors from
# the CURRENT WORKING TREE. MODE=full declares each door's whole appended tail;
# MODE=short declares one line less, so the sha still binds and only the
# line-count limb reopens. MODE=escape adds a declaration that escapes the tree.
g1_declare() { # REPO MODE
  local repo=$1 mode=$2 p added n sha
  mkdir -p -- "$repo/.ufo/waves/round-39" || return 1
  : > "$repo/.ufo/waves/round-39/declared-blocks.txt"
  for p in PROVINCE.md corpus/README.md; do
    added=$(git -C "$repo" diff --numstat "$BASE_REF" -- "$p" | awk 'NF >= 2 { print $1; exit }')
    added=${added:-0}
    n=$added
    case $mode in
      short) n=$((added - 1)) ;;
    esac
    [ "$n" -ge 1 ] || n=1
    sha=$(tail -n "$n" -- "$repo/$p" | sha256sum | awk '{print $1; exit}')
    printf '%s %s %s\n' "$p" "$n" "$sha" >> "$repo/.ufo/waves/round-39/declared-blocks.txt"
  done
  if [ "$mode" = escape ]; then
    printf 'stray\n' > "$(dirname -- "$repo")/outside-fixture.md"
    sha=$(sha256sum -- "$(dirname -- "$repo")/outside-fixture.md" | awk '{print $1; exit}')
    printf '../outside-fixture.md 1 %s\n' "$sha" >> "$repo/.ufo/waves/round-39/declared-blocks.txt"
  fi
  return 0
}

# g1_fixture REPO MODE — apply the round-39 front-door append in the repo
# worktree (reset to base first), write the declarations for MODE, commit, and
# print the commit. Modes: full (control), short (partial tail), tilde (a tilde
# opener closed with backticks), corin (correction inside a fence), escape (a
# declaration path that leaves the tree).
g1_fixture() { # REPO MODE
  local repo=$1 mode=$2
  hist_reset "$repo" || return 1
  printf '[r39 fixture amendment] F22 — fixture frontier line.\n\n' >> "$repo/PROVINCE.md"
  {
    printf '\n## Round-39 fixture admission (appended 2026-10-26)\n\n'
    printf 'Correction (round 39): the fixture front door is an end-of-file append; this line sits outside any fence.\n\n'
    printf 'The frontier stands at **22/22 admitted** after this append.\n'
  } >> "$repo/corpus/README.md"
  case $mode in
    tilde) printf '\n~~~text\ntilde opener, never closed by a tilde run\n```\n' >> "$repo/corpus/README.md" ;;
    corin) printf '\n```text\nCorrection (round 39): this correction sits inside an open fence.\n```\n' >> "$repo/corpus/README.md" ;;
  esac
  case $mode in
    short) g1_declare "$repo" short || return 1 ;;
    escape) g1_declare "$repo" escape || return 1 ;;
    *) g1_declare "$repo" full || return 1 ;;
  esac
  fixture_commit "$repo" "g1 fixture $mode"
}

# g2_content DIR [knob...] — write a complete green G2 tree WITHOUT touching the
# directory's history, so a fixture repository can be built by successive
# commits. Knobs: sentinel=<text> xref=<hash> digest=<hash>
#   cases=graded|summary|verdict-fail|seven headline=yes
g2_content() { # DIR [knob...]
  local d=$1; shift
  local phrase='judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt'
  local sentinel='all-gates v3' xref=$REF_RESOLVED digest cases=graded headline=no i kv
  digest=$(suite_digest)
  for kv in "$@"; do
    case $kv in
      sentinel=*) sentinel=${kv#sentinel=} ;;
      xref=*) xref=${kv#xref=} ;;
      digest=*) digest=${kv#digest=} ;;
      cases=*) cases=${kv#cases=} ;;
      headline=*) headline=${kv#headline=} ;;
    esac
  done
  mkdir -p -- "$d/.ufo/waves/round-39/final-gates" "$d/corpus/instruments"
  cp -- "$SELF" "$d/corpus/instruments/r39-closure.sh"
  {
    printf '%s\n' "$sentinel"
    printf 'export-ref=%s\n' "$xref"
    printf 'suite-sha256=%s\n' "$digest"
    printf 'run-utc=2026-10-26T20:00:00Z\n'
    printf '\n== run ==\n'
    for i in 1 2 3 4 5 6 7 8; do printf 'G%s payload=fixture closed=1\n' "$i"; done
    printf 'closed=8/8 exit=0\n'
    printf '== selftest ==\n'
    case $cases in
      summary)
        printf 'selftest cases=8 failures=0\n' ;;
      verdict-fail)
        for i in 1 2 3 4 5 6 7; do
          printf 'selftest case=G%s positive=pass mutants=2/2 verdict=pass\n' "$i"
        done
        printf 'selftest case=G8 positive=pass mutants=2/2 verdict=fail\n'
        printf 'selftest cases=8 failures=0\n' ;;
      seven)
        for i in 1 2 3 4 5 6 7; do
          printf 'selftest case=G%s positive=pass mutants=2/2 verdict=pass\n' "$i"
        done
        printf 'selftest cases=8 failures=0\n' ;;
      *)
        for i in 1 2 3 4 5 6 7 8; do
          printf 'selftest case=G%s positive=pass mutants=2/2 verdict=pass\n' "$i"
        done
        printf 'selftest cases=8 failures=0\n' ;;
    esac
  } > "$d/.ufo/waves/round-39/final-gates/all-gates.txt"
  {
    printf '## Round 38 result\n\n| Axis | Score |\n|---|---|\n\n'
    printf '## Round 39 result\n\n| Axis | Score |\n|---|---|\n'
    printf '%s\n' "$phrase"
    [ "$headline" = yes ] && printf 'Final lane commit: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b\n'
  } | mut_put "$d" SCORECARD.md
  {
    printf '# checklist\n\n'
    printf -- '- [~] box 3 — evidence (round 39): %s\n' "$phrase"
  } | mut_put "$d" SHONEN.md
}

# g2_fixture DIR [knob...] — reset the directory, then write the green tree.
g2_fixture() { # DIR [knob...]
  local d=$1; shift
  mut_reset "$d"
  g2_content "$d" "$@"
}

# g4_fixture DIR [knob...] — a dispatch/results pair under .ufo/waves/round-39.
# Knobs: tasks=3|0 results=yes|no|dup|short|bad wave=<name> rwave=<name>.
g4_fixture() { # DIR [knob...]
  local d=$1; shift
  local tasks=3 results=yes wave=kasegi-r39-build rwave='' kv i
  for kv in "$@"; do
    case $kv in
      tasks=*) tasks=${kv#tasks=} ;;
      results=*) results=${kv#results=} ;;
      wave=*) wave=${kv#wave=} ;;
      rwave=*) rwave=${kv#rwave=} ;;
    esac
  done
  [ -n "$rwave" ] || rwave=$wave
  mut_reset "$d"
  mkdir -p -- "$d/.ufo/waves/round-39"
  {
    printf '{"schema":"ufo-swarm-wave-dispatch-v1","wave":"%s","taskCall":{"tasks":[' "$wave"
    for i in $(seq 1 "$tasks"); do
      [ "$i" -gt 1 ] && printf ','
      printf '{"name":"Seat%s","agent":"executor"}' "$i"
    done
    printf ']}}\n'
  } > "$d/.ufo/waves/round-39/wave1-dispatch.json"
  case $results in
    no) return 0 ;;
    bad) printf '{"lane":"kasegi","results":[' > "$d/.ufo/waves/round-39/wave1-results.json"; return 0 ;;
  esac
  {
    printf '{"lane":"kasegi","round":39,"wave":"%s","results":[' "$rwave"
    case $results in
      dup) printf '{"name":"Seat1","agent":"executor"},{"name":"Seat1","agent":"executor"},{"name":"Seat3","agent":"executor"}' ;;
      short) printf '{"name":"Seat1","agent":"executor"},{"name":"Seat2","agent":"executor"}' ;;
      *) for i in $(seq 1 "$tasks"); do
           [ "$i" -gt 1 ] && printf ','
           printf '{"name":"Seat%s","agent":"executor"}' "$i"
         done ;;
    esac
    printf ']}\n'
  } > "$d/.ufo/waves/round-39/wave1-results.json"
}

# g5_fixture DIR [knob...] — SCORECARD with a round-39 section. Knobs:
# section=yes|no final=yes|no correction=yes|no|unlabeled.
g5_fixture() { # DIR [knob...]
  local d=$1; shift
  local section=yes final=no correction=yes kv
  for kv in "$@"; do
    case $kv in
      section=*) section=${kv#section=} ;;
      final=*) final=${kv#final=} ;;
      correction=*) correction=${kv#correction=} ;;
    esac
  done
  mut_reset "$d"
  {
    printf '## Round 38 result\n\nFinal lane commit: 7dd2fcd6deadbeef (historical label, out of scope)\n\n'
    if [ "$section" = yes ]; then
      printf '## Round 39 result\n\n| Axis | Score |\n|---|---|\n'
      [ "$final" = yes ] && printf 'Final lane commit: abc1234def5678\n'
    fi
    case $correction in
      yes)
        printf 'Correction (round 39): the round-38 8/8 quote in f06148c6 is report-only; the receipt shows closed=7/8 exit=1 at J.\n' ;;
      unlabeled)
        printf 'Correction (round 39): the round-38 8/8 quote in f06148c6 is overstated.\n' ;;
    esac
  } | mut_put "$d" SCORECARD.md
}

# g7_fixture DIR [knob...] — ledger with the round-38 section and a round-39
# dispositions section. Knobs: drop=<n> correction=yes|no order=after|before.
g7_fixture() { # DIR [knob...]
  local d=$1; shift
  local drop=0 correction=yes order=after kv
  for kv in "$@"; do
    case $kv in
      drop=*) drop=${kv#drop=} ;;
      correction=*) correction=${kv#correction=} ;;
      order=*) order=${kv#order=} ;;
    esac
  done
  {
    printf '# ledger\n\n## Round-37 dispositions (appended 2026-10-26, R31 home)\n\n'
    if [ "$order" = before ]; then
      g7_body "$drop" "$correction"
    fi
    printf '## Round-37 dispositions — filled (round 38)\n\n'
    printf '| proposal | status |\n|---|---|\n| 1. old row | open |\n\n'
    if [ "$order" = after ]; then
      g7_body "$drop" "$correction"
    fi
    printf '\n## Limits\n\nA trailing section so no dispositions block sits at EOF.\n'
  } | mut_put "$d" corpus/knowledge/considerthese-proposals-ledger.md
}

# g7_body DROP CORRECTION — the round-39 dispositions block (stdout).
g7_body() { # DROP CORRECTION
  local i
  printf '## Round-39 dispositions (appended 2026-10-26)\n\n'
  if [ "$2" = yes ]; then
    printf 'Correction (round 39): the round-38 rows above are carried, not rewritten.\n\n'
  fi
  printf '| proposal | disposition | evidence |\n|---|---|---|\n'
  for i in 1 2 3 4; do
    [ "$i" -eq "$1" ] && continue
    printf '| %s. proposal %s | mined | ledger row %s |\n' "$i" "$i" "$i"
  done
  printf '\n'
}

# g8_fixture DIR MODE — a tree carrying the pinned r37 bytes. MODE=full (pinned
# copy, no other bytes), MODE=mutated (one byte changed), MODE=absent (no copy).
g8_fixture() { # DIR MODE
  local d=$1 mode=$2
  mut_reset "$d"
  case $mode in
    absent) return 0 ;;
  esac
  mkdir -p -- "$d/corpus/instruments"
  git -C "$LANE" show "$PIN_REF:corpus/instruments/r37-closure.sh" \
    > "$d/corpus/instruments/r37-closure.sh" || return 1
  if [ "$mode" = mutated ]; then
    printf '\n# one-byte fixture mutation\n' >> "$d/corpus/instruments/r37-closure.sh"
  fi
}

# --- selftest case primitives ---------------------------------------------

st_pos() { # ID TREE REF
  local id=$1 tree=$2 ref=$3
  local out rc
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s positive=pass payload=%s\n' "$id" "$out"
    return 0
  fi
  printf 'selftest detail=%s positive=fail rc=%s payload=%s\n' "$id" "$rc" "$out"
  return 1
}

st_control() { # ID LABEL TREE REF
  local id=$1 label=$2 tree=$3 ref=$4
  local out rc
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s control=%s accepted=1 payload=%s\n' "$id" "$label" "$out"
    return 0
  fi
  printf 'selftest detail=%s control=%s accepted=0 rc=%s payload=%s\n' \
    "$id" "$label" "$rc" "$out"
  FAILS=$((FAILS + 1))
  return 1
}

st_neg() { # ID LABEL TREE REF NEEDLE
  local id=$1 label=$2 tree=$3 ref=$4 needle=$5
  local out rc
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  if [ "$rc" -ne 0 ] && printf '%s' "$out" | grep -qF -- "$needle"; then
    printf 'selftest detail=%s mutant=%s rejected=1 limb=%s\n' "$id" "$label" "$needle"
    return 0
  fi
  printf 'selftest detail=%s mutant=%s rejected=0 rc=%s payload=%s\n' \
    "$id" "$label" "$rc" "$out"
  FAILS=$((FAILS + 1))
  return 1
}

st_verdict() { # ID BAD OK N
  local id=$1 bad=$2 ok=$3 n=$4
  if [ "$bad" -eq 0 ] && [ "$n" -ge 1 ] && [ "$ok" -eq "$n" ]; then
    printf 'selftest case=%s positive=pass mutants=%s/%s verdict=pass\n' "$id" "$ok" "$n"
    return 0
  fi
  printf 'selftest case=%s positive=%s mutants=%s/%s verdict=fail\n' \
    "$id" "$([ "$bad" -eq 0 ] && echo pass || echo fail)" "$ok" "$n"
  FAILS=$((FAILS + 1))
  return 1
}

# --- selftest cases -------------------------------------------------------

selftest_case_G1() {
  local bad=0 ok=0 n=0 d repo c saved
  CASES=$((CASES + 1))
  st_pos G1 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$(hist_repo_ready "$MUT/hrepo") || {
    printf 'selftest detail=G1 fixture=repo-init-failed\n'
    st_verdict G1 1 "$ok" 1
    return
  }
  saved=$LANE
  LANE=$repo
  # control first: an unmutated whole-tail fixture is GREEN, so every red below
  # is the defect and not check breakage
  c=$(g1_fixture "$repo" full)
  if [ -n "$c" ]; then
    st_control G1 whole-tail-green "$repo" "$c"
  else
    printf 'selftest detail=G1 fixture=commit-failed\n'; FAILS=$((FAILS + 1))
  fi
  n=$((n + 1)); c=$(g1_fixture "$repo" short)
  [ -n "$c" ] && st_neg G1 declared-short-of-added "$repo" "$c" 'valid=0' && ok=$((ok + 1))
  n=$((n + 1)); c=$(g1_fixture "$repo" tilde)
  [ -n "$c" ] && st_neg G1 tilde-opener-closed-by-backticks "$repo" "$c" 'readme-fence=open' \
    && ok=$((ok + 1))
  n=$((n + 1)); c=$(g1_fixture "$repo" corin)
  [ -n "$c" ] && st_neg G1 correction-inside-fence "$repo" "$c" 'corrections-inside=1' \
    && ok=$((ok + 1))
  n=$((n + 1)); c=$(g1_fixture "$repo" escape)
  [ -n "$c" ] && st_neg G1 declaration-path-escape "$repo" "$c" 'paths=0' && ok=$((ok + 1))
  LANE=$saved
  st_verdict G1 "$bad" "$ok" "$n"
}

selftest_case_G2() {
  local bad=0 ok=0 n=0 d repo c1 c2 side br top real saved
  CASES=$((CASES + 1))
  st_pos G2 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G2-sentinel; g2_fixture "$d" 'sentinel=all-gates v2'
  st_neg G2 sentinel-v2 "$d" "$REF_RESOLVED" 'sentinel=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-digest; g2_fixture "$d" "digest=$(printf '%064d' 0)"
  st_neg G2 digest-mismatch "$d" "$REF_RESOLVED" 'digest-match=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-summary; g2_fixture "$d" cases=summary
  st_neg G2 summary-only-case-line "$d" "$REF_RESOLVED" 'graded-cases=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-verdict; g2_fixture "$d" cases=verdict-fail
  st_neg G2 case-verdict-fail "$d" "$REF_RESOLVED" 'graded-cases=7' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-seven; g2_fixture "$d" cases=seven
  st_neg G2 seven-graded-cases "$d" "$REF_RESOLVED" 'graded-cases=7' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-headline; g2_fixture "$d" headline=yes
  st_neg G2 final-label-in-section "$d" "$REF_RESOLVED" 'final-lane-commit=1' \
    && ok=$((ok + 1))
  # history mutants: ancestry and post-receipt diff need a real repo
  repo=$MUT/g2repo
  mut_reset "$repo"
  if ! git -C "$repo" init -q; then
    printf 'selftest detail=G2 fixture=repo-init-failed\n'
    st_verdict G2 1 "$ok" "$n"
    return
  fi
  top=$(git -C "$repo" rev-parse --show-toplevel)
  real=$( cd "$repo" && pwd -P )
  if [ "$top" != "$real" ]; then
    printf 'selftest detail=G2 fixture=toplevel-mismatch top=%s want=%s\n' "$top" "$real"
    st_verdict G2 1 "$ok" "$n"
    return
  fi
  br=$(git -C "$repo" symbolic-ref --short HEAD)
  [ -n "$br" ] || br=master
  saved=$LANE
  LANE=$repo
  g2_content "$repo" xref=0000000000000000000000000000000000000000
  c1=$(fixture_commit "$repo" base)
  g2_content "$repo" "xref=$c1"
  c2=$(fixture_commit "$repo" receipt)
  git -C "$repo" checkout -q -b side
  git -C "$repo" -c user.email=r39-fixture@local -c user.name=r39-fixture \
    commit -q --allow-empty -m side
  side=$(git -C "$repo" rev-parse --verify HEAD)
  git -C "$repo" checkout -q "$br"
  n=$((n + 1)); g2_content "$repo" "xref=$side"
  st_neg G2 export-ref-not-ancestor "$repo" "$c2" 'ancestor=0' && ok=$((ok + 1))
  n=$((n + 1)); g2_content "$repo" "xref=$c1"
  printf 'notes\n' > "$repo/NOTES.md"
  c2=$(fixture_commit "$repo" notes)
  st_neg G2 post-receipt-diff-extra "$repo" "$c2" 'diff-clean=0' && ok=$((ok + 1))
  LANE=$saved
  st_verdict G2 "$bad" "$ok" "$n"
}

selftest_case_G3() {
  local bad=0 ok=0 n=0 repo c saved d ref
  CASES=$((CASES + 1))
  st_pos G3 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$(hist_repo_ready "$MUT/hrepo") || {
    printf 'selftest detail=G3 fixture=repo-init-failed\n'
    st_verdict G3 1 "$ok" 1
    return
  }
  saved=$LANE
  LANE=$repo
  ref=2222222222222222222222222222222222222222
  # control: the same quote with a committed transcript is GREEN
  hist_reset "$repo"
  mkdir -p -- "$repo/.ufo/waves/round-39/final-gates"
  printf 'bash corpus/instruments/r39-closure.sh --export-ref %s -> closed=8/8 exit=0\n' "$ref" \
    > "$repo/.ufo/waves/round-39/final-gates/run.txt"
  printf 'Round 39 run quoted: --export-ref %s -> closed=8/8 exit=0\n' "$ref" >> "$repo/SCORECARD.md"
  c=$(fixture_commit "$repo" g3-control)
  [ -n "$c" ] && st_control G3 quoted-run-transcribed "$repo" "$c"
  # mutant 1: the same quote, no transcript at all
  hist_reset "$repo"
  printf 'Round 39 run quoted: --export-ref %s -> closed=8/8 exit=0\n' "$ref" >> "$repo/SCORECARD.md"
  n=$((n + 1)); c=$(fixture_commit "$repo" g3-uncovered)
  [ -n "$c" ] && st_neg G3 quote-without-transcript "$repo" "$c" 'uncovered=1' && ok=$((ok + 1))
  # mutant 2: the ref exists, but outside the final-gates transcript directory
  hist_reset "$repo"
  mkdir -p -- "$repo/.ufo/waves/round-39/wave1"
  printf 'ref %s\n' "$ref" > "$repo/.ufo/waves/round-39/wave1/note.txt"
  printf 'Round 39 run quoted: --export-ref %s -> closed=8/8 exit=0\n' "$ref" >> "$repo/SCORECARD.md"
  n=$((n + 1)); c=$(fixture_commit "$repo" g3-wrong-location)
  [ -n "$c" ] && st_neg G3 transcript-outside-final-gates "$repo" "$c" 'uncovered=1' \
    && ok=$((ok + 1))
  LANE=$saved
  st_verdict G3 "$bad" "$ok" "$n"
}

selftest_case_G4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G4 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G4-noresults; g4_fixture "$d" results=no
  st_neg G4 results-absent "$d" "$REF_RESOLVED" 'pairs=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-duplicate; g4_fixture "$d" results=dup
  st_neg G4 duplicate-identity "$d" "$REF_RESOLVED" 'seats-ok=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-short; g4_fixture "$d" results=short
  st_neg G4 seat-count-short "$d" "$REF_RESOLVED" 'seats-ok=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-zero; g4_fixture "$d" tasks=0
  st_neg G4 zero-task-dispatch "$d" "$REF_RESOLVED" 'zero-task=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-badjson; g4_fixture "$d" results=bad
  st_neg G4 results-unparseable "$d" "$REF_RESOLVED" 'pairs=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-wave; g4_fixture "$d" rwave=stale-wave
  st_neg G4 results-wave-mismatch "$d" "$REF_RESOLVED" 'pairs=0' && ok=$((ok + 1))
  st_verdict G4 "$bad" "$ok" "$n"
}

selftest_case_G5() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G5 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G5-final; g5_fixture "$d" final=yes
  st_neg G5 final-label-in-section "$d" "$REF_RESOLVED" 'final-lane-commit=1' \
    && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G5-nocorrection; g5_fixture "$d" correction=no
  st_neg G5 correction-absent "$d" "$REF_RESOLVED" 'correction=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G5-unlabeled; g5_fixture "$d" correction=unlabeled
  st_neg G5 correction-unlabeled "$d" "$REF_RESOLVED" 'correction-labeled=0' \
    && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G5-nosection; g5_fixture "$d" section=no
  st_neg G5 round39-section-absent "$d" "$REF_RESOLVED" 'round39-section=0' \
    && ok=$((ok + 1))
  st_verdict G5 "$bad" "$ok" "$n"
}

selftest_case_G6() {
  local bad=0 ok=0 n=0 root save_root save_work rc out
  CASES=$((CASES + 1))
  st_pos G6 "$EXPORT" "$REF_RESOLVED" || bad=1
  save_root=$SCRATCH_ROOT
  save_work=$WORK
  # control: this run's own work dir as the only kasegi-r39 entry is accepted
  root=$MUT/g6-control
  mut_reset "$root"
  mkdir -p -- "$root/kasegi-r39/seat/work"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r39/seat/work
  out=$(run_check G6 "$EXPORT" "$REF_RESOLVED"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=G6 control=own-work-dir accepted=1 payload=%s\n' "$out"
  else
    printf 'selftest detail=G6 control=own-work-dir accepted=0 rc=%s payload=%s\n' "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
  WORK=$save_work
  root=$MUT/g6-r37; mut_reset "$root"; mkdir -p -- "$root/kasegi-r37"
  printf 'x\n' > "$root/kasegi-r37/leftover.txt"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 r37-leftover-file "$EXPORT" "$REF_RESOLVED" 'r37=present' && ok=$((ok + 1))
  root=$MUT/g6-r38; mut_reset "$root"; mkdir -p -- "$root/kasegi-r38/leftover-seat"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 r38-residual-seat "$EXPORT" "$REF_RESOLVED" 'r38=present' && ok=$((ok + 1))
  root=$MUT/g6-r39; mut_reset "$root"; mkdir -p -- "$root/kasegi-r39/seat/work"
  printf 'x\n' > "$root/kasegi-r39/seat/leftover.txt"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r39/seat/work
  n=$((n + 1))
  st_neg G6 r39-parent-sibling-leftover "$EXPORT" "$REF_RESOLVED" 'r39=present' \
    && ok=$((ok + 1))
  WORK=$save_work
  # control: a clean nested chain toward WORK is accepted
  root=$MUT/g6-nested
  mut_reset "$root"
  mkdir -p -- "$root/kasegi-r39/seat/work/deep"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r39/seat/work/deep
  out=$(run_check G6 "$EXPORT" "$REF_RESOLVED"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=G6 control=nested-clean-chain accepted=1 payload=%s\n' "$out"
  else
    printf 'selftest detail=G6 control=nested-clean-chain accepted=0 rc=%s payload=%s\n' "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
  WORK=$save_work
  # fail-closed: an unreadable root is RED, never "zero entries"
  root=$MUT/g6-unreadable; mut_reset "$root"; mkdir -p -- "$root/kasegi-r37/hidden"
  chmod 000 -- "$root/kasegi-r37"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 unreadable-root "$EXPORT" "$REF_RESOLVED" 'r37=unreadable' && ok=$((ok + 1))
  chmod 700 -- "$root/kasegi-r37"
  SCRATCH_ROOT=$save_root
  st_verdict G6 "$bad" "$ok" "$n"
}

selftest_case_G7() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G7 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G7-drop3; g7_fixture "$d" drop=3
  st_neg G7 proposal-3-row-absent "$d" "$REF_RESOLVED" 'proposal-3=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G7-nocorrection; g7_fixture "$d" correction=no
  st_neg G7 correction-absent "$d" "$REF_RESOLVED" 'correction=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G7-before; g7_fixture "$d" order=before
  st_neg G7 section-before-round38 "$d" "$REF_RESOLVED" 'after-round38=0' && ok=$((ok + 1))
  st_verdict G7 "$bad" "$ok" "$n"
}

selftest_case_G8() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G8-mutated; g8_fixture "$d" mutated
  st_neg G8 export-copy-digest-mismatch "$d" "$REF_RESOLVED" 'export-copy=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G8-absent; g8_fixture "$d" absent
  st_neg G8 export-copy-absent "$d" "$REF_RESOLVED" 'r37-copy=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G8-red; g8_fixture "$d" full
  # the pinned bytes are intact and the export copy matches; the RUN is red
  # because a ref that is not the lane HEAD breaks the r37 suite's E9 head limb
  st_neg G8 pinned-run-red "$d" "$BASE_REF" 'r37-closed=0' && ok=$((ok + 1))
  st_verdict G8 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id line n ok det rej dup
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f"); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f"); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=8 failures=0$' "$f"); summary=${summary:-0}
  [ "$cases" -eq 8 ] && [ "$verdicts" -eq 8 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=G<i> mutant=`
  # lines of which ok name rejected=1. A case line carrying `mutants=0/0` (no
  # fixture ran) is rejected: n must be >= 1 and the detail lines must exist.
  for id in "${CHECK_IDS[@]}"; do
    dup=$(grep -c "^selftest case=${id} " "$f"); dup=${dup:-0}
    [ "$dup" -eq 1 ] || return 1
    line=$(grep -m1 "^selftest case=${id} " "$f")
    [ -n "$line" ] || return 1
    printf '%s' "$line" | grep -q 'positive=pass' || return 1
    printf '%s' "$line" | grep -q 'verdict=pass$' || return 1
    n=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
    ok=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
    [ -n "$n" ] && [ -n "$ok" ] && [ "$n" -ge 1 ] && [ "$ok" -eq "$n" ] || return 1
    det=$(grep -c "^selftest detail=${id} mutant=" "$f"); det=${det:-0}
    rej=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$f"); rej=${rej:-0}
    [ "$det" -eq "$n" ] && [ "$rej" -eq "$ok" ] || return 1
  done
  return 0
}

run_selftest() {
  local f=$WORK/selftest-report.txt rc=0 id i
  {
    for id in "${CHECK_IDS[@]}"; do
      "selftest_case_${id}"
    done
    printf 'selftest cases=%s failures=%s\n' "$CASES" "$FAILS"
  } > "$f" 2>&1
  cat "$f"

  if judge_selftest_report "$f"; then
    printf 'selftest judge=own-report accepted=1\n'
  else
    printf 'selftest judge=own-report accepted=0\n'
    rc=1
  fi

  printf 'selftest cases=0 failures=0\n' > "$WORK/forge-summary.txt"
  if judge_selftest_report "$WORK/forge-summary.txt"; then
    printf 'selftest judge=forged-summary rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-summary rejected=1\n'
  fi

  printf 'selftest cases=8 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    for i in $(seq 1 8); do
      printf 'selftest case=G%s positive=fail mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=8 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  # the detail-free all-pass forgery: eight case lines claiming pass with
  # mutants=0/0 and no fixture detail behind them
  {
    for i in $(seq 1 8); do
      printf 'selftest case=G%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=8 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  # the 7-case forgery: every line well-formed, one check never ran
  {
    for i in $(seq 1 7); do
      printf 'selftest case=G%s positive=pass mutants=1/1 verdict=pass\n' "$i"
      printf 'selftest detail=G%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=8 failures=0\n'
  } > "$WORK/forge-7-cases.txt"
  if judge_selftest_report "$WORK/forge-7-cases.txt"; then
    printf 'selftest judge=forged-7-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-7-cases rejected=1\n'
  fi

  # the field-free forgery: positive=pass and matching details, but no
  # `verdict=` field at all — an ungraded case line must not satisfy a case
  {
    for i in $(seq 1 8); do
      printf 'selftest case=G%s positive=pass mutants=1/1\n' "$i"
      printf 'selftest detail=G%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=8 failures=0\n'
  } > "$WORK/forge-no-verdict.txt"
  if judge_selftest_report "$WORK/forge-no-verdict.txt"; then
    printf 'selftest judge=forged-no-verdict rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-no-verdict rejected=1\n'
  fi

  if [ "$CASES" -ne 8 ]; then
    printf 'selftest problem=cases=%s expected=8\n' "$CASES"
    rc=1
  fi
  [ "$FAILS" -eq 0 ] || rc=1
  return "$rc"
}

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

main() {
  parse_args "$@"
  # Normalise the lane once: every later `git -C "$LANE"` then works from any
  # cwd (a relative --lane used to resolve against the export tree inside a
  # check's subshell and read a false red).
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  LANE=$( cd "$LANE" && pwd -P ) || die "cannot resolve lane: $LANE"
  case $MODE in
    run)
      if [ -z "$EXPORT_REF" ]; then
        printf 'r39-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r39-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
        exit 2
      fi
      prepare_export "$EXPORT_REF"
      run_suite_report
      ;;
    selftest)
      prepare_export "${EXPORT_REF:-HEAD}"
      printf 'selftest export-ref=%s lane=%s suite-sha256=%s\n' \
        "$REF_RESOLVED" "$LANE" "$(suite_digest)"
      if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
      if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
      run_selftest
      ;;
    *)
      die "unknown mode: $MODE"
      ;;
  esac
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  main "$@"
fi
