#!/usr/bin/env bash
# r41-closure.sh — round-41 closure counter for claim C1 (depth:verifiability).
#
# Twelve checks I1-I12. Each closes one defect class the round-40 verifier routed
# (corpus/lessons/round-40-verifier-spotcheck.md section 5: D1-D6) or one round-40
# instrument attack finding (.ufo/waves/round-40/wave2/):
#   I1  corrections       `Correction (round 41)` lines in SCORECARD.md, LOG.md and
#                         SHONEN.md (line-anchored, outside fences) grade round-40 C1
#                         NOT verified and name the kill-rule firing evidence
#                         (RevC1Counters.defeats.txt, CritKillRule.md, MutH6H10.md).
#                         Closes D1.
#   I2  receipt transcript the round-41 receipt at Y is the teed transcript of BOTH
#                         the suite run and the graded selftest at Y; run-utc equals
#                         the committer instant of the ref the receipt names; the
#                         time basis is ref-commit, never wall-clock. Closes D2.
#   I3  token boundary    a value must appear as a bounded token: `closed=7/8`
#                         matches, `closed=7/80` does not; `failures=1` matches,
#                         `failures=10` does not (round-40 wave-2 T2).
#   I4  fence awareness   correction/criterion lines inside a CommonMark fence do
#                         not satisfy a line-anchored limb and the fence state at
#                         EOF is CLOSED; the round-40 lesson carries the appended
#                         `Erratum (round 41)` block that repairs D4 and D5.
#   I5  declared blocks   every declared-block path is readlink-canonicalized and
#                         must resolve under the export root, and the declaration
#                         must equal the whole appended tail with zero deletions
#                         (round-40 wave-2 T7).
#   I6  scratch scan      a live, recursive, case- and separator-insensitive,
#                         dot-inclusive scan of the `kasegi-r41` name family; every
#                         leftover except the passed --work dir and its clean
#                         ancestor chain is a stray; fail closed on a scan error
#                         (round-40 wave-2 T14).
#   I7  registry row      the SKILL.md registry row for r41-closure.sh is a
#                         well-formed table row inside a contiguous table whose
#                         header names `name`; a mention-only row does not satisfy
#                         the limb (round-40 wave-2 T13) and a row broken by a blank
#                         line does not either (D6).
#   I8  forgery flags     each receipt-forgery variant (payload-contradicting,
#                         future-dated, foreign-ref, nonexistent-ref, summary-only,
#                         tampered-payload-line) is flagged INDEPENDENTLY, never by
#                         a count-relative comparison (MutH1H5 H5).
#   I9  isolation         the graded selftest compares ACTUAL payload values per
#                         case: a tampered payload reds exactly its own case
#                         (MutH1H5 H7 / MutH6H10 D1).
#   I10 negative control  the negative-control acceptance predicate is KILLABLE:
#                         the export's own suite over the base commit and the
#                         round-40 judged head must print closed<12/12 exit=1 for
#                         tree-dependent reasons, and the M-H8a class (a comparison
#                         that would accept a leaf-capped green base) is rejected.
#   I11 kill-rule escapes each of the EIGHT committed CritKillRule escape states
#                         (F1-F8) reds the limb it escapes.
#   I12 no-harm guard     negative controls red at base and round-40 judged head,
#                         declared blocks equal whole-tail appends with zero
#                         deletions, SKILL.md and PROVINCE.md are append-only,
#                         corpus/instruments/density.py is byte-identical to base,
#                         the round diff deletes no tracked path, the sources census
#                         exits 0, an unresolvable --export-ref is a distinct red
#                         (`ref-not-found`, never a vacuous tally) and the lane
#                         carries no skip-worktree/assume-unchanged marker.
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -xf - -C <work>/export
# and every tree limb reads bytes only under that export root. Live reads are
# I6's scratch scan (host state by definition), the ref-scoped git limbs and the
# census tool invocation (the census is run against the EXPORT's
# corpus/SOURCES.md, never against the working tree). All git limbs run with
# --no-optional-locks so the lane is never written to. Nothing is written under
# the lane by this suite except the single file named by `--receipt-out` (the
# caller's explicit request). --work must lie outside the lane; its `export/`,
# `mut/`, `neg-*` and `seed/` subdirectories are cleared before use, so a reused
# work dir can never satisfy a check with stale bytes. A plain run (no
# --export-ref, no --selftest) refuses with exit 2, because a suite that reads
# the working tree can be turned green by edits that were never committed.
#
# Usage:
#   bash corpus/instruments/r41-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR] [--receipt-out PATH]
#       Extract <hash> and run I1-I12 against the export. Prints the receipt
#       transcript — five header lines, one `I<n> payload=<k=v,...> closed=0|1`
#       line per check, the twelve graded `selftest case=I<n> ... verdict=pass`
#       lines, the `selftest cases=12 failures=<k>` line and a final
#       `closed=K/12 exit=0|1` — to stdout. Exit 0 only for K=12.
#   bash corpus/instruments/r41-closure.sh --export-ref <hash> --receipt-out PATH
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Same, and write the transcript to PATH. The file always equals the
#       stdout of the run that wrote it, red or green. Use this to PRODUCE the
#       receipt at the judged head J (the tree that does not yet contain the
#       receipt); commit exactly those bytes as Y = J + receipt, and only when
#       they read closed=12/12. The suite creates PATH's parent directory if
#       needed and writes that one file. There is NO make-receipt mode: the L1
#       produces the receipt by tee-ing the run, e.g.
#         bash corpus/instruments/r41-closure.sh --export-ref <J> \
#              --receipt-out .ufo/waves/round-41/final-gates/all-gates.txt
#       (the written file is byte-identical to the run's stdout, so
#        `... | tee <path>` is equivalent).
#   bash corpus/instruments/r41-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Graded selftest: for every check a positive fixture (the export under
#       test) must pass and every defeat fixture must red exactly its own case,
#       with the payload values compared (not the closed bit alone). Prints one
#       `selftest case=I<n> mutants=<ok>/<n> positive=pass|fail payload-match=1|0
#       verdict=pass|fail` line per check, the `selftest detail=` lines behind
#       them, the `selftest judge=` lines (own report accepted, forged reports
#       rejected) and `selftest cases=12 failures=<k>`; exit 0 only when all
#       twelve cases ran, every positive passed and every defeat was rejected.
#   bash corpus/instruments/r41-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# THE RECEIPT CONTRACT (v1). The receipt is a transcript, not a summary. Its
# grammar is fixed: 5 header lines, 12 run lines, 12 graded selftest lines, the
# selftest summary and the closed line — 31 lines in all:
#
#   all-gates v1
#   export-ref=<40 hex>
#   suite-sha256=<64 hex>
#   time-basis=ref-commit
#   run-utc=<YYYY-MM-DDTHH:MM:SSZ>
#   I1 payload=... closed=1
#   ... I2-I12 ...
#   selftest case=I1 mutants=<ok>/<n> positive=pass payload-match=1 verdict=pass
#   ... I2-I12 ...
#   selftest cases=12 failures=0
#   closed=12/12 exit=0
#
# `export-ref` is the commit the transcript was teed at (the judged head J when
# the receipt is committed at Y = J + receipt). It may not be this run's ref: a
# commit cannot contain its own hash, so the receipt names the parent and the
# suite verifies `git diff --name-only <that ref> <this ref>` lists nothing but
# the receipt. `time-basis=ref-commit` states exactly what `run-utc` is: the
# committer instant of the ref the RECEIPT NAMES, read from the lane with
# `git log -1 --format=%ct` and printed as UTC — NOT a wall-clock stamp. A
# `run-utc` that does not equal that instant, or that post-dates the
# verification clock, is RED. The run-utc is therefore bound to the named ref,
# not to --export-ref: binding it to the tip would force the committer date to
# be pinned, which no lane path does.
#
# I2 re-derives the transcript: it recomputes every payload from the export,
# compares each recorded `I<n> payload=` with the recomputed one, rebuilds the
# canonical transcript line by line and requires byte equality with the
# committed receipt on every line except the two self-referential ones (I2's
# own run line and I8's run line) and the I2 case's own selftest line. The I2
# line is rebuilt from the receipt minus its own line (the r40 h7_inner
# pattern), so the self-reference is closed rather than trusted; the I8 line is
# rebuilt from the fresh payload, because I8 grades scratch fixtures and never
# reads the committed receipt. A forged value, a re-stamped timestamp, a
# foreign ref, an extra line, a duplicate id, a summary-only body or a
# reordered selftest transcript therefore reds the run.
#
# The graded selftest lines inside the receipt are re-EXECUTED on every run
# (they are the transcript of the run's own selftest, not a shape check) and
# they never read the receipt under test, so the selftest block is a pure
# function of the exported tree and can be compared byte for byte.
#
# No path, no flag and no clock is printed: the transcript is a function of the
# tree and the ref-scoped facts only, so two plain runs over the same ref are
# byte-identical and the receipt equals a re-run with nothing normalised.
#
# THE GREEN WINDOW (measured, not assumed). I2 requires the receipt inside the
# export. A commit cannot contain its own hash, so at J the receipt is absent by
# construction; the suite therefore seeds the receipt it is about to write (the
# seed is the canonical transcript computed from the tree facts, so the first
# iteration is already the fixed point) and the run at J prints the same bytes
# the run at Y prints. The 12/12 window is the lane tip Y = J + the receipt
# alone (`git diff --name-only J Y` = that one path).
#
# ENVIRONMENT KNOBS (documented at the top so wave-2 seats can point the
# defeats at the live suite; every knob is inert unless it is set):
#   R41_DECLARED=<path>        the declared-blocks file I5 and I12 read
#                              (default .ufo/waves/round-41/declared-blocks.txt)
#   R41_RECEIPT_TARGET=<file>  the receipt I2 grades (default: the receipt being
#                              written, else the seed, else the export's receipt)
#   R41_FORGE_DISABLE=<flag>   disables one I8 forgery clause
#   R41_ISOLATE_BREAK=1        makes I9 count-relative instead of per-case
#   R41_NEG_WEAK=1             makes I10 accept a tally of 12 (the M-H8a class)
#   R41_I11_BREAK=<F1..F8>     makes one I11 escape state stay green
#   R41_DEPTH=1                leaf mode: the nested negative-control runs never
#                              recurse
#
# Documented limits (measured, not hidden):
#   - I6 is LIVE (host state by definition) and cannot be a pure function of a
#     commit: a receipt produced on a clean scratch root is reproduced only on a
#     clean scratch root. It scans the scratch root RECURSIVELY by name family
#     (`kasegi-r41` in any letter case and with any of the separators `-`, `_`,
#     `.`, whitespace), including dot-prefixed entries. The passed --work dir is
#     never a stray; an ANCESTOR of the work dir is tolerated only when the
#     chain from it down to the work dir is clean (each level holds exactly the
#     next component) and the entry is a real directory — a family symlink
#     resolving to an ancestor is a stray. The round's own container
#     `/fast/scratch/hyaku/kasegi-r41` is therefore a stray unless --work lies
#     inside it in a clean chain; at filing every seat's scratch dir must be
#     gone and the container itself removed.
#   - I10 executes the export's own suite copy over the base commit and the
#     round-40 judged head in LEAF mode (R41_DEPTH=1), so the nested run never
#     recurses; in leaf mode the nested I10 limb is red by construction, so the
#     acceptance predicate also demands the tree-dependent checks (I1, I2, I7)
#     to be red in the nested run — that is what kills the leaf-capped green
#     base (the MutH6H10 M-H8a class).
#   - I5 and I12 validate `.ufo/waves/round-41/declared-blocks.txt`; with no
#     declared blocks the clause is vacuously satisfied and the payload says
#     `declared=0`.
#   - I12 pins the base digest of density.py; an intentional change to the
#     depth:density instrument is a red until this constant is moved in a round
#     that says so.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unreadable lane, archive
# failure). The plain-run refusal is exit 2. An unresolvable --export-ref is
# NOT a harness error and NOT a vacuous tally: it prints a distinct
# `ref-not-found` red (every check line carries `payload=ref-not-found,...`) and
# exits 1, so a mistyped ref can never be read as a closed-but-red run.
set -uo pipefail

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

SELF=${BASH_SOURCE[0]:-}
case $SELF in
  /*) ;;
  *)  if [ -n "$SELF" ] && [ -d "$(dirname -- "$SELF")" ]; then
        SELF=$( cd -- "$(dirname -- "$SELF")" && pwd -P )/$(basename -- "$SELF" )
      fi ;;
esac

# The lane is the repository the script lives in: corpus/instruments/<script>
# is two levels below the lane root. It is NEVER resolved from the cwd.
LANE_DEFAULT=
if [ -n "$SELF" ]; then
  LANE_DEFAULT=$( cd -- "$(dirname -- "$SELF")/../.." 2>/dev/null && pwd -P )
fi
LANE=${LANE_DEFAULT:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
SCRATCH_ROOT=/fast/scratch/hyaku
BASE_REF=5b29ea1439450b712581edf5f0f0bf98dfb262ab
R40_HEAD=c7aea5ef97902f38289cbdc1cf267068876a62dd
DENSITY_SHA=ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710
RECEIPT=.ufo/waves/round-41/final-gates/all-gates.txt
DECLARED=.ufo/waves/round-41/declared-blocks.txt
SENTINEL='all-gates v1'
CENSUS_SCRIPT=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
ROUND40_TALLY=closed=10/10
CHECK_IDS=(I1 I2 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12)
NON_I2=(I1 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12)
NON_I2_I8=(I1 I3 I4 I5 I6 I7 I9 I10 I11 I12)
# the payload table is computed in dependency order: the receipt fixtures (I8,
# I9) read the table, and I12 reads I10's payload, so they run last.
PAYLOAD_ORDER=(I1 I3 I4 I5 I6 I7 I10 I11 I12 I8 I9)
RECORDS=(SCORECARD.md LOG.md SHONEN.md)
EVIDENCE=(RevC1Counters CritKillRule MutH6H10)
LESSONS=(corpus/lessons/round-41.md corpus/lessons/round-40.md)

# ---------------------------------------------------------------------------
# state
# ---------------------------------------------------------------------------

MODE=run
EXPORT_REF=
WORK_ARG=
RECEIPT_OUT=
REF_RESOLVED=
RECEIPT_WRITTEN=0
WORK=
EXPORT=
MUT=
SEED=
WORK_AUTO=0
CASES=0
FAILS=0
PAYFILE=
SELFILE=
DEPTH=${R41_DEPTH:-0}
declare -A POS_PAYLOAD=()

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

suite_digest() {
  local s=${SELF:-}
  if [ -z "$s" ] || [ ! -r "$s" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$s" | awk '{print $1; exit}'
}

file_digest() {
  local f=$1
  if [ -z "$f" ] || [ ! -r "$f" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$f" | awk '{print $1; exit}'
}

usage() {
  sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

die() {
  printf 'r41-closure: %s\n' "$*" >&2
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
      --receipt-out)
        [ $# -ge 2 ] || die '--receipt-out needs a file path'
        RECEIPT_OUT=$2; shift 2 ;;
      --lane)
        [ $# -ge 2 ] || die '--lane needs a directory'
        LANE=$2; shift 2 ;;
      --scratch-root)
        [ $# -ge 2 ] || die '--scratch-root needs a directory'
        SCRATCH_ROOT=$2; shift 2 ;;
      --selftest)
        MODE=selftest; shift ;;
      -h|--help)
        usage; exit 0 ;;
      *)
        printf 'r41-closure: unknown argument: %s\n' "$1" >&2
        usage >&2
        exit 2 ;;
    esac
  done
  if [ -n "$RECEIPT_OUT" ] && [ "$MODE" = selftest ]; then
    die '--receipt-out is a run-mode option (not --selftest)'
  fi
  if [ -n "$RECEIPT_OUT" ] && [ -z "$EXPORT_REF" ]; then
    die '--receipt-out needs --export-ref (the ref to tee)'
  fi
}

cleanup() {
  [ -n "${EXPORT:-}" ] && rm -rf -- "$EXPORT"
  [ -n "${MUT:-}" ] && rm -rf -- "$MUT"
  [ -n "${SEED:-}" ] && rm -f -- "$SEED"
  [ -n "${WORK:-}" ] && rm -rf -- "$WORK/neg-base" "$WORK/neg-r40" "$WORK/refnf"
  if [ "${WORK_AUTO:-0}" = 1 ] && [ -n "${WORK:-}" ]; then rm -rf -- "$WORK"; fi
}

make_work() {
  if [ -n "$WORK_ARG" ]; then
    local norm
    norm=$(realpath -m -- "$WORK_ARG") || die "cannot resolve work dir: $WORK_ARG"
    case $norm in
      "$LANE"|"$LANE"/*) die "--work must be outside the lane (it would write there): $norm" ;;
      /) die '--work must not be /' ;;
    esac
    mkdir -p -- "$norm" || die "cannot create work dir: $norm"
    WORK=$( cd "$norm" && pwd -P ) || die "cannot resolve work dir: $norm"
    case $WORK in
      "$LANE"|"$LANE"/*) die "--work resolves inside the lane: $WORK" ;;
    esac
    WORK_AUTO=0
  else
    WORK=$(mktemp -d -t r41-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  SEED=$WORK/receipt-seed.txt
  PAYFILE=$WORK/payloads.tsv
  SELFILE=$WORK/selftest-lines.txt
  rm -rf -- "$EXPORT" "$MUT" "$WORK/neg-base" "$WORK/neg-r40" "$WORK/refnf"
  rm -f -- "$SEED" "$PAYFILE" "$SELFILE"
  mkdir -p -- "$EXPORT" "$MUT" || die "cannot populate work dir: $WORK"
  trap cleanup EXIT
}

# print_ref_not_found REF — a DISTINCT red, never a vacuous tally. Every check
# line carries `ref-not-found` so a mistyped ref cannot be read as a run that
# closed some checks.
print_ref_not_found() {
  local want=$1 sha id
  sha=$(suite_digest)
  printf 'suite-ref-status=ref-not-found\n'
  printf '%s\n' "$SENTINEL"
  printf 'export-ref=%s\n' "$(printf '%s' "$want" | tr -c '0-9a-f' '' | cut -c1-40)"
  printf 'suite-sha256=%s\n' "$sha"
  printf 'time-basis=ref-commit\n'
  printf 'run-utc=unreadable\n'
  for id in "${CHECK_IDS[@]}"; do
    printf 'I%s payload=ref-not-found,ref=%s closed=0\n' "${id#I}" "$want"
  done
  printf 'selftest cases=0 failures=0\n'
  printf 'closed=0/12 exit=1\n'
  exit 1
}

prepare_export() {
  local want=${1:-$EXPORT_REF}
  [ -n "$want" ] || die 'export mode requires --export-ref <hash>'
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  git -C "$LANE" rev-parse --git-dir >/dev/null 2>&1 \
    || die "lane is not a git repository: $LANE"
  if ! REF_RESOLVED=$(git -C "$LANE" rev-parse --verify --quiet "${want}^{commit}"); then
    print_ref_not_found "$want"
  fi
  [ -n "$REF_RESOLVED" ] || print_ref_not_found "$want"
  make_work
  git -C "$LANE" archive --format=tar "$REF_RESOLVED" | tar -xf - -C "$EXPORT" \
    || die "git archive export failed for $REF_RESOLVED"
  [ -f "$EXPORT/SCORECARD.md" ] \
    || die "export has no SCORECARD.md (not a lane tree): $REF_RESOLVED"
}

# ---------------------------------------------------------------------------
# text helpers
# ---------------------------------------------------------------------------

count_lines() { grep -c . || true; }

# kv_get STR KEY — the value of `KEY=` in a comma-joined k=v payload.
kv_get() {
  printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1
}

# path_safe PATH — a declaration may only name a plain relative path inside the
# export: no absolute path, no `..` component, no empty component.
path_safe() {
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

# value_present LINE VALUE — TRUE when VALUE appears in LINE as a bounded
# token: the characters around the occurrence must be whitespace or punctuation
# (or the ends of the line). `closed=7/8` matches; `closed=7/80` does not;
# `failures=1` matches; `failures=10` does not. This is the round-40 wave-2 T2
# defect class (substring matching) closed.
value_present() {
  local line=$1 value=$2
  printf '%s\n' "$line" | awk -v v="$value" '
    {
      rest = $0
      while ((i = index(rest, v)) > 0) {
        before = (i == 1) ? "" : substr(rest, i - 1, 1)
        after = substr(rest, i + length(v), 1)
        bok = (before == "") || (before ~ /[[:space:][:punct:]]/)
        aok = (after == "") || (after ~ /[[:space:][:punct:]]/)
        if (bok && aok) found = 1
        rest = substr(rest, i + length(v))
      }
    }
    END { exit(found ? 0 : 1) }
  '
}

# ref_utc REF — the committer instant of REF as `YYYY-MM-DDTHH:MM:SSZ`, or an
# empty string when the ref cannot be read. Deterministic: it is a property of
# the commit, not of the clock.
ref_utc() {
  local e
  [ -n "${1:-}" ] || return 1
  e=$(git -C "$LANE" log -1 --format=%ct "$1" 2>/dev/null) || return 1
  case $e in ''|*[!0-9]*) return 1 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}

# iso_past ISO — 1 when ISO is a well-formed UTC stamp no later than the
# verification clock plus 120 seconds of skew, 0 otherwise.
iso_past() {
  local iso=$1 n
  case $iso in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
    *) printf '0'; return 0 ;;
  esac
  n=$(date -u -d "$iso" +%s 2>/dev/null) || { printf '0'; return 0; }
  if [ "$n" -le $(( $(date -u +%s) + 120 )) ]; then printf '1'; else printf '0'; fi
}

# receipt_ref FILE — the single `export-ref=<40 hex>` of a receipt, or empty.
receipt_ref() {
  local f=$1 n
  [ -f "$f" ] || return 0
  n=$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f"); n=${n:-0}
  [ "$n" -eq 1 ] || return 0
  sed -n 's/^export-ref=//p' -- "$f" | head -n 1
}

# payload_get ID — the canonical payload this run computed for ID.
payload_get() {
  [ -n "$PAYFILE" ] && [ -f "$PAYFILE" ] || return 0
  awk -F'\t' -v id="$1" '$1 == id { print $2; exit }' "$PAYFILE"
}

# payload_closed ID — the recorded closed status (1|0) for ID.
payload_closed() {
  local c
  [ -n "$PAYFILE" ] && [ -f "$PAYFILE" ] || { printf '1'; return 0; }
  c=$(awk -F'\t' -v id="$1" '$1 == id { print $3; exit }' "$PAYFILE")
  case $c in 0|1) printf '%s' "$c" ;; *) printf '1' ;; esac
}

# ---------------------------------------------------------------------------
# the CommonMark fence state machine (4.5, fenced code blocks)
#
# opener : up to 3 leading spaces, a run of >= 3 identical ` or ~; a backtick
#          fence's info string may not contain a backtick.
# closer : up to 3 leading spaces, a run of the SAME marker at least as long as
#          the opener's run, and nothing but spaces or tabs after it.
# A different marker never closes an open fence and a shorter run of the same
# marker is content. Every line of a fenced block — including the delimiters —
# is INSIDE and therefore excluded from every line-anchored count.
# ---------------------------------------------------------------------------

FENCE_AWK='
function fence_open(line,   i, n, c, run, rest) {
  i = 1; n = 0
  while (n < 3 && substr(line, i, 1) == " ") { n++; i++ }
  if (substr(line, i, 1) == " ") return 0
  c = substr(line, i, 1)
  if (c != "`" && c != "~") return 0
  run = 0
  while (substr(line, i + run, 1) == c) run++
  if (run < 3) return 0
  rest = substr(line, i + run)
  if (c == "`" && index(rest, "`") > 0) return 0
  FENCE_CHAR = c; FENCE_LEN = run
  return 1
}
function fence_close(line,   i, n, c, run, rest) {
  if (FENCE_CHAR == "") return 0
  i = 1; n = 0
  while (n < 3 && substr(line, i, 1) == " ") { n++; i++ }
  if (substr(line, i, 1) == " ") return 0
  c = substr(line, i, 1)
  if (c != FENCE_CHAR) return 0
  run = 0
  while (substr(line, i + run, 1) == c) run++
  if (run < FENCE_LEN) return 0
  rest = substr(line, i + run)
  if (rest ~ /[^ \t]/) return 0
  return 1
}
BEGIN { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0; out_n = 0; in_n = 0; hit = 0; pat = ENVIRON["FENCE_PATTERN"] }
{
  line = $0
  if (in_fence) {
    inside = 1
    if (fence_close(line)) { in_fence = 0; FENCE_CHAR = ""; FENCE_LEN = 0 }
  } else {
    if (fence_open(line)) { in_fence = 1; inside = 1 }
    else inside = 0
  }
  if (inside) in_n++; else out_n++
  if (mode == "match" && !inside && pat != "" && line ~ pat) { print line; hit++ }
  if (mode == "matchin" && inside && pat != "" && line ~ pat) { print line; hit++ }
  if (mode == "matchno" && !inside && pat != "" && line ~ pat) { printf "%d\t%s\n", NR, line; hit++ }
}
END {
  if (mode == "eof") print (in_fence ? "OPEN" : "CLOSED")
  else if (mode == "count") print out_n
  else if (mode == "audit") print "outside=" out_n " inside=" in_n " eof=" (in_fence ? "OPEN" : "CLOSED")
}
'

fence_awk() { # MODE FILE [ERE]
  local mode=$1 file=$2 pat=${3:-}
  [ -f "$file" ] || return 1
  FENCE_PATTERN="$pat" awk -v mode="$mode" "$FENCE_AWK" "$file"
}

# fence_match FILE ERE — the OUTSIDE-fence lines of FILE matching ERE.
fence_match() { fence_awk match "$1" "$2"; }

# fence_inside_match FILE ERE — the INSIDE-fence lines of FILE matching ERE.
fence_inside_match() { fence_awk matchin "$1" "$2"; }

# fence_matchno FILE ERE — the OUTSIDE-fence lines of FILE matching ERE, each
# prefixed with its line number.
fence_matchno() { fence_awk matchno "$1" "$2"; }

# fence_eof FILE — CLOSED or OPEN.
fence_eof() { fence_awk eof "$1"; }

# ---------------------------------------------------------------------------
# scratch family scan (I6)
# ---------------------------------------------------------------------------

# family_name NAME — the normalized family key of a scratch entry name: lower
# case, leading dots stripped, every separator run collapsed to `-`. The
# family is `kasegi-r41`.
family_name() {
  printf '%s' "$1" | tr 'A-Z' 'a-z' \
    | sed -e 's/^[.]*//' -e 's/[^a-z0-9]\{1,\}/-/g' -e 's/-\{1,\}/-/g' -e 's/-$//'
}

family_match() { # NAME
  local n
  n=$(family_name "$1")
  case $n in kasegi-r41|kasegi-r41-*) return 0 ;; esac
  return 1
}

# chain_clean ANCESTOR WORK — TRUE when the chain from ANCESTOR down to WORK
# holds exactly the next component at every level and nothing else. A family
# entry that merely shares a path prefix with --work is NOT tolerated: that is
# the round-40 wave-2 F5 escape.
chain_clean() { # ANCESTOR WORK
  local a=$1 w=$2 rel rest comp dir n only
  case "$w" in "$a"/*) rel=${w#"$a"/} ;; *) return 1 ;; esac
  dir=$a
  rest=$rel
  while [ -n "$rest" ]; do
    comp=${rest%%/*}
    if [ "$comp" = "$rest" ]; then rest=''; else rest=${rest#*/}; fi
    n=$(ls -A -- "$dir" 2>/dev/null | grep -c . || true)
    [ "${n:-0}" -eq 1 ] || return 1
    only=$(ls -A -- "$dir" 2>/dev/null | head -n 1)
    [ "$only" = "$comp" ] || return 1
    dir=$dir/$comp
    [ -d "$dir" ] || return 1
  done
  return 0
}

# scan_scratch ROOT WORKCANON — prints "strays=<n> read=<ok|fail> scanned=<n>".
# The scan is recursive, dot-inclusive and case/separator-insensitive. The work
# dir and everything inside it are never strays. An ANCESTOR of the work dir is
# tolerated only when it is a real directory (a family symlink that resolves to
# an ancestor is a stray: the round-40 wave-2 F5 escape) AND the chain from it
# down to the work dir is clean.
scan_scratch() { # ROOT WORKCANON
  local root=$1 work=${2:-}
  local out e b real strays=0 scanned=0 read=ok
  if [ ! -d "$root" ]; then printf 'strays=0,read=fail,scanned=0'; return 1; fi
  if ! out=$(find "$root" -mindepth 1 -print 2>/dev/null); then
    printf 'strays=0,read=fail,scanned=0'; return 1
  fi
  while IFS= read -r e; do
    [ -n "$e" ] || continue
    b=${e##*/}
    family_match "$b" || continue
    scanned=$((scanned + 1))
    if ! real=$( cd "$e" 2>/dev/null && pwd -P ); then
      read=fail; strays=$((strays + 1)); continue
    fi
    if [ -n "$work" ]; then
      case "$real" in
        "$work"|"$work"/*) continue ;;
      esac
      case "$work" in
        "$real"/*)
          if [ -L "$e" ]; then strays=$((strays + 1)); continue; fi
          if chain_clean "$real" "$work"; then continue; fi
          strays=$((strays + 1)); continue ;;
      esac
    fi
    strays=$((strays + 1))
  done <<< "$out"
  printf 'strays=%s,read=%s,scanned=%s' "$strays" "$read" "$scanned"
  [ "$read" = ok ] && [ "$strays" -eq 0 ] && return 0
  return 1
}

# ---------------------------------------------------------------------------
# payload helpers for the receipt
# ---------------------------------------------------------------------------

# receipt_source — the file I2 grades: an explicit target, else the receipt
# being written, else the seed (the canonical transcript of this run), else the
# export's committed receipt.
receipt_source() {
  if [ -n "${R41_RECEIPT_TARGET:-}" ]; then printf '%s' "$R41_RECEIPT_TARGET"; return 0; fi
  if [ -n "${RECEIPT_OUT:-}" ]; then
    # the --receipt-out path is THIS run's output, never an input: before this
    # run writes it, grade the export's committed receipt when there is one and
    # the canonical seed otherwise (a stale file at that path cannot poison the
    # transcript). After the first write the file being produced is graded.
    if [ "${RECEIPT_WRITTEN:-0}" = 1 ] && [ -f "$RECEIPT_OUT" ]; then
      printf '%s' "$RECEIPT_OUT"; return 0
    fi
    if [ -f "$EXPORT/$RECEIPT" ]; then printf '%s' "$EXPORT/$RECEIPT"; return 0; fi
    if [ -n "${SEED:-}" ] && [ -f "$SEED" ]; then printf '%s' "$SEED"; return 0; fi
    printf '%s' "$EXPORT/$RECEIPT"; return 0
  fi
  printf '%s' "$EXPORT/$RECEIPT"
}

# receipt_shape FILE — the shape and provenance facts of a receipt, with no
# payload recomputation:
#   sentinel,ref,digest,time-basis,run-utc,not-future,header-lines,run-lines,
#   selftest-lines,selftest-verdicts,summary,closed-line,closed-0
receipt_shape() {
  local f=$1
  local sent=0 refhex='' dig=0 tb=0 utc=0 notf=0 hdr=0 runl=0 sell=0 selv=0 summ=0 c0=0 cl=0
  local n u want i line
  if [ ! -f "$f" ]; then
    printf 'sentinel=0,ref=,digest=0,time-basis=0,run-utc=0,not-future=0,header-lines=0,run-lines=0,selftest-lines=0,selftest-verdicts=0,summary=0,closed-0=0,closed-line=0'
    return 1
  fi
  [ "$(sed -n '1p' -- "$f")" = "$SENTINEL" ] && sent=1
  n=$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then refhex=$(sed -n 's/^export-ref=//p' -- "$f" | head -n 1); fi
  n=$(grep -cE '^suite-sha256=[0-9a-f]{64}$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then
    u=$(sed -n 's/^suite-sha256=//p' -- "$f" | head -n 1)
    [ "$u" = "$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")" ] && dig=1
  fi
  n=$(grep -cxF -- 'time-basis=ref-commit' "$f"); n=${n:-0}
  [ "$n" -eq 1 ] && tb=1
  n=$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then
    u=$(sed -n 's/^run-utc=//p' -- "$f" | head -n 1)
    [ "$(iso_past "$u")" = 1 ] && notf=1
    if [ -n "$refhex" ] && [ "$u" = "$(ref_utc "$refhex")" ]; then utc=1; fi
  fi
  if [ -n "$refhex" ]; then
    want="export-ref=$refhex"
    i=0
    for line in "$SENTINEL" "$want" "suite-sha256=$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")" \
                'time-basis=ref-commit' "run-utc=$(ref_utc "$refhex")"; do
      i=$((i + 1))
      [ "$(sed -n "${i}p" -- "$f")" = "$line" ] && hdr=$((hdr + 1))
    done
  fi
  runl=$(grep -cE '^I[0-9]+ payload=.* closed=[01]$' -- "$f"); runl=${runl:-0}
  sell=$(grep -cE '^selftest case=I[0-9]+ .* verdict=(pass|fail)$' -- "$f"); sell=${sell:-0}
  selv=$(grep -cE '^selftest case=I[0-9]+ .* verdict=pass$' -- "$f"); selv=${selv:-0}
  n=$(grep -cxF -- 'selftest cases=12 failures=0' "$f"); n=${n:-0}
  [ "$n" -eq 1 ] && summ=1
  n=$(grep -cE '^I[0-9]+ payload=.* closed=0$' -- "$f"); n=${n:-0}
  c0=${n:-0}
  n=$(grep -cxF -- 'closed=12/12 exit=0' "$f"); n=${n:-0}
  [ "$n" -eq 1 ] && cl=1
  printf 'sentinel=%s,ref=%s,digest=%s,time-basis=%s,run-utc=%s,not-future=%s,header-lines=%s,run-lines=%s,selftest-lines=%s,selftest-verdicts=%s,summary=%s,closed-0=%s,closed-line=%s' \
    "$sent" "$refhex" "$dig" "$tb" "$utc" "$notf" "$hdr" "$runl" "$sell" "$selv" "$summ" "$c0" "$cl"
}

# payload_match_ids FILE — the ids whose recorded payload differs from the
# canonical payload of this run. Prints a space separated list (empty when
# none). I2 uses it to compare values; I9 uses it to prove isolation.
payload_match_ids() {
  local f=$1 id rec want out=''
  [ -f "$f" ] || { printf ''; return 0; }
  for id in "${CHECK_IDS[@]}"; do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=$(payload_get "$id")
    if [ "$rec" != "$want" ]; then out="$out $id"; fi
  done
  if [ "${R41_ISOLATE_BREAK:-0}" = 1 ] && [ -n "$out" ]; then
    # the count-relative class: one mismatch flags every id, so no case is
    # isolated (the round-40 wave-2 MutH1H5 H7 class)
    out=''
    for id in "${CHECK_IDS[@]}"; do out="$out $id"; done
  fi
  printf '%s' "${out# }"
}

# ---------------------------------------------------------------------------
# I2 helpers: the canonical payload and the canonical rebuild
# ---------------------------------------------------------------------------

# i2_canonical FILE — the canonical I2 payload for FILE, computed WITHOUT
# reading FILE's own I2 line (the self-reference is closed, not trusted) and
# without its I8 line (I8 grades scratch fixtures, so the comparison stays a
# function of the tree and of the receipt's own facts).
i2_canonical() { # FILE
  local f=$1
  local shape refhex pm i8match anc=0 diffclean=0 diffread=ok sent
  shape=$(receipt_shape "$f")
  refhex=$(kv_get "$shape" ref)
  sent=$(kv_get "$shape" sentinel)
  pm=$(payload_match_count "$f" "${NON_I2[@]}")
  i8match=0
  local rec8 fresh8
  rec8=$(sed -n 's/^I8 payload=\(.*\) closed=[01]$/\1/p' -- "$f" 2>/dev/null | head -n 1)
  fresh8=$(payload_get I8)
  if [ -n "$rec8" ] && [ "$rec8" = "$fresh8" ]; then i8match=1; fi
  if [ -n "$refhex" ]; then
    if git -C "$LANE" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
      if git --no-optional-locks -C "$LANE" merge-base --is-ancestor "$refhex" "$REF_RESOLVED" 2>/dev/null; then
        anc=1
      fi
      local name x
      if name=$(git --no-optional-locks -C "$LANE" diff --name-only "$refhex" "$REF_RESOLVED" 2>/dev/null); then
        diffclean=1
        while IFS= read -r x; do
          [ -n "$x" ] || continue
          [ "$x" = "$RECEIPT" ] || diffclean=0
        done <<< "$name"
      else
        diffread=fail
      fi
    fi
  fi
  printf 'receipt=%s,sentinel=%s,ref=%s,digest=%s,time-basis=%s,run-utc=%s,not-future=%s,header-lines=%s,run-lines=%s,selftest-lines=%s,selftest-verdicts=%s,summary=%s,closed-line=%s,payload-match=%s/11,ancestor=%s,diff-clean=%s,diff-read=%s,i8-match=%s' \
    "$([ -f "$f" ] && echo 1 || echo 0)" "$sent" "$refhex" \
    "$(kv_get "$shape" digest)" "$(kv_get "$shape" time-basis)" \
    "$(kv_get "$shape" run-utc)" "$(kv_get "$shape" not-future)" \
    "$(kv_get "$shape" header-lines)" "$(kv_get "$shape" run-lines)" \
    "$(kv_get "$shape" selftest-lines)" "$(kv_get "$shape" selftest-verdicts)" \
    "$(kv_get "$shape" summary)" "$(kv_get "$shape" closed-line)" \
    "$pm" "$anc" "$diffclean" "$diffread" "$i8match"
}

# payload_match_count FILE ID... — how many of the listed ids have a recorded
# payload in FILE equal to the canonical payload of this run. A pure byte
# comparison: it never runs a check.
payload_match_count() {
  local f=$1; shift
  local n=0 id rec want
  for id in "$@"; do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=$(payload_get "$id")
    if [ "$rec" = "$want" ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

# selftest_others — the graded selftest lines of every case but I2 (I2's own
# case line is the self-reference and is graded by the shape fields).
selftest_others() {
  local id
  [ -n "${WORK:-}" ] || return 0
  for id in "${CHECK_IDS[@]}"; do
    [ "$id" = I2 ] && continue
    [ -f "$WORK/sel-$id.line" ] && cat -- "$WORK/sel-$id.line"
  done
}

# i2_rebuild FILE OUT — the canonical transcript for FILE: the header, the
# twelve run lines (I2's line rebuilt from the canonical payload, I8's line
# from the fresh payload), the graded selftest lines of every case but I2 and
# the tail.
i2_rebuild() { # FILE OUT
  local f=$1 out=$2
  local href sha utc id
  href=$(receipt_ref "$f"); [ -n "$href" ] || href=$REF_RESOLVED
  sha=$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")
  utc=$(ref_utc "$href"); [ -n "$utc" ] || utc=unreadable
  {
    printf '%s\n' "$SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in "${CHECK_IDS[@]}"; do
      case $id in
        I2) printf 'I2 payload=%s,cmp=1,i2-line=1 closed=1\n' "$(i2_canonical "$f")" ;;
        I8) printf 'I8 payload=%s closed=1\n' "$(payload_get I8)" ;;
        *)  printf '%s payload=%s closed=1\n' "$id" "$(payload_get "$id")" ;;
      esac
    done
    selftest_others
    printf 'selftest cases=12 failures=0\n'
    printf 'closed=12/12 exit=0\n'
  } > "$out"
}

# i2_compare FILE — 1 when FILE is byte-identical to the canonical rebuild on
# every line except the three self-referential ones (I2's own run line, I8's
# run line and I2's own selftest case line), which are graded by their own
# fields. 0 otherwise.
i2_compare() { # FILE
  local f=$1
  local rebuild=$MUT/i2-rebuild.txt
  [ -f "$f" ] || { printf '0'; return 0; }
  i2_rebuild "$f" "$rebuild" >/dev/null 2>&1
  grep -vE '^(I2|I8) payload=' -- "$f" | grep -v '^selftest case=I2 ' > "$MUT/i2-a.txt"
  grep -vE '^(I2|I8) payload=' -- "$rebuild" | grep -v '^selftest case=I2 ' > "$MUT/i2-b.txt"
  if cmp -s -- "$MUT/i2-a.txt" "$MUT/i2-b.txt"; then printf '1'; else printf '0'; fi
}

# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

# qualified_corrections FILE — the OUTSIDE-fence `Correction (round 41)` lines
# that grade round-40 C1 as not verified.
qualified_corrections() { # FILE
  fence_match "$1" '^Correction [(]round 41[)]' \
    | grep -E '(^|[^A-Za-z0-9])C1([^A-Za-z0-9]|$)' \
    | grep -iE 'round[ -]?40|r40' \
    | grep -iE 'not[ _-]?verified|unverified|withdraw'
}

check_i1() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'records=0,lines=0,graded=0,evidence=0/3,missing=3'; exit 1; }
    local total=0 graded=0 missing=0 ev=0 f n q stem seen=' '
    for f in "${RECORDS[@]}"; do
      if [ ! -f "$f" ]; then missing=$((missing + 1)); continue; fi
      n=$(fence_match "$f" '^Correction [(]round 41[)]' | grep -c . || true)
      total=$((total + n))
      q=$(qualified_corrections "$f" | grep -c . || true)
      if [ "$q" -ge 1 ]; then graded=$((graded + 1)); else missing=$((missing + 1)); fi
      for stem in "${EVIDENCE[@]}"; do
        case "$seen" in *" $stem "*) continue ;; esac
        if qualified_corrections "$f" | grep -qF -- "$stem"; then
          seen="$seen$stem "; ev=$((ev + 1))
        fi
      done
    done
    printf 'records=%s,lines=%s,graded=%s,evidence=%s/3,missing=%s' \
      "${#RECORDS[@]}" "$total" "$graded" "$ev" "$missing"
    [ "$graded" -eq 3 ] && [ "$ev" -eq 3 ] && [ "$missing" -eq 0 ] && exit 0
    exit 1
  )
}

check_i2() { # TREE REF
  local tree=$1
  local f canonical rec cmp ok=1
  f=$(receipt_source)
  canonical=$(i2_canonical "$f")
  cmp=$(i2_compare "$f")
  rec=$(sed -n 's/^I2 payload=\(.*\) closed=[01]$/\1/p' -- "$f" 2>/dev/null | head -n 1)
  [ -f "$f" ] || ok=0
  [ "$cmp" = 1 ] || ok=0
  [ -n "$rec" ] && [ "$rec" = "$canonical,cmp=1,i2-line=1" ] || ok=0
  [ "$(kv_get "$canonical" payload-match)" = 11/11 ] || ok=0
  [ "$(kv_get "$canonical" i8-match)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" sentinel)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" digest)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" time-basis)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" run-utc)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" not-future)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" header-lines)" = 5 ] || ok=0
  [ "$(kv_get "$canonical" run-lines)" = 12 ] || ok=0
  [ "$(kv_get "$canonical" selftest-lines)" = 12 ] || ok=0
  [ "$(kv_get "$canonical" selftest-verdicts)" = 12 ] || ok=0
  [ "$(kv_get "$canonical" summary)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" closed-line)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" ancestor)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" diff-clean)" = 1 ] || ok=0
  [ "$(kv_get "$canonical" diff-read)" = ok ] || ok=0
  if [ "$ok" -eq 1 ]; then
    printf '%s,cmp=1,i2-line=1' "$canonical"
    exit 0
  fi
  printf '%s,cmp=%s,i2-line=0' "$canonical" "$cmp"
  exit 1
}

check_i3() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'exact=0/2,substring=0/2,records=0,tally=0/3,mangled=0'; exit 1; }
    # the token-boundary probes: the honest values match, the substring forms do not
    local exact=0 sub=0
    value_present 'closed=7/8 exit=1' 'closed=7/8' && exact=$((exact + 1))
    value_present 'failures=1' 'failures=1' && exact=$((exact + 1))
    value_present 'closed=7/80 exit=1' 'closed=7/8' || sub=$((sub + 1))
    value_present 'failures=10' 'failures=1' || sub=$((sub + 1))
    # the records must name the round-40 truth as a BOUNDED token
    local tally=0 mangled=0 records=0 f
    for f in "${RECORDS[@]}"; do
      [ -f "$f" ] || continue
      records=$((records + 1))
      local lines hit=0 l
      lines=$(fence_match "$f" '^Correction [(]round 41[)]')
      while IFS= read -r l; do
        [ -n "$l" ] || continue
        if value_present "$l" "$ROUND40_TALLY"; then hit=1; break; fi
      done <<< "$lines"
      if [ "$hit" -eq 1 ]; then
        tally=$((tally + 1))
      elif printf '%s\n' "$lines" | grep -qE 'closed=10/1[0-9]'; then
        mangled=$((mangled + 1))
      fi
    done
    printf 'exact=%s/2,substring=%s/2,records=%s,tally=%s/3,mangled=%s' \
      "$exact" "$sub" "$records" "$tally" "$mangled"
    [ "$exact" -eq 2 ] && [ "$sub" -eq 2 ] && [ "$records" -eq 3 ] && [ "$tally" -eq 3 ] && exit 0
    exit 1
  )
}

# pending_scan FILE — the pending-marker clause: the number of unfinished
# markers in FILE, in ANY spelling (`⟨pending`, `⟨ pending`, `〈pending`,
# `<pending`, `[[pending`, case variants). The spelling class is broad on
# purpose: the clause enforces the SEMANTIC state "no unfinished marker", not
# one byte spelling (the round-40 wave-2 F7 escape).
pending_scan() { # FILE
  local f=$1 n
  [ -f "$f" ] || { printf 'pending=0,read=missing'; return 1; }
  n=$(grep -ciE '(⟨|〈|<|\[\[)[[:space:]]*pending' -- "$f" 2>/dev/null || true)
  n=${n:-0}
  printf 'pending=%s,read=ok' "$n"
  [ "$n" -eq 0 ] && return 0
  return 1
}

# erratum_block FILE — the `Erratum (round 41)` block of a lesson file (the
# lines from the erratum heading to the next heading, or EOF), or nothing.
erratum_block() { # FILE
  [ -f "$1" ] || return 0
  awk '
    /^(#+[ \t]*)?Erratum [(]round 41[)]/ { inb = 1; print; next }
    inb && /^#/ { exit }
    inb { print }
  ' "$1"
}

check_i4() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'records=0,fenced=0,eof=closed,erratum=0,gate=0,tally=0,census=0'; exit 1; }
    local records=0 fenced=0 eofok=1 f inside n
    for f in "${RECORDS[@]}"; do
      [ -f "$f" ] || { eofok=0; continue; }
      records=$((records + 1))
      [ "$(fence_eof "$f")" = CLOSED ] || eofok=0
      inside=$(fence_inside_match "$f" '^Correction [(]round 41[)]' | grep -c . || true)
      fenced=$((fenced + inside))
    done
    # the appended erratum (D4/D5) in either lesson file
    local erratum=0 gate=0 tally=0 census=0 block
    for f in "${LESSONS[@]}"; do
      [ -f "$f" ] || continue
      block=$(erratum_block "$f")
      [ -n "$block" ] || continue
      erratum=1
      printf '%s\n' "$block" | grep -qi 'Gate' && gate=1
      printf '%s\n' "$block" | grep -qF '25/35' && tally=1
      printf '%s\n' "$block" | grep -qi 'census' && census=1
    done
    printf 'records=%s,fenced=%s,eof=%s,erratum=%s,gate=%s,tally=%s,census=%s' \
      "$records" "$fenced" "$([ "$eofok" = 1 ] && echo closed || echo open)" \
      "$erratum" "$gate" "$tally" "$census"
    [ "$records" -eq 3 ] && [ "$fenced" -eq 0 ] && [ "$eofok" -eq 1 ] \
      && [ "$erratum" -eq 1 ] && [ "$gate" -eq 1 ] && [ "$tally" -eq 1 ] \
      && [ "$census" -eq 1 ] && exit 0
    exit 1
  )
}

# declared_blocks_check TREE REF FILE — the declared-blocks validator.
# Prints the payload and returns 0 only when every declaration is valid:
#   declared=N   the parsed declarations
#   valid=N      the declarations that pass every clause
#   tail=N       the declarations whose appended tail sha256 matches
#   malformed=N  the lines that are not `<path> <lines> <sha256>`
#   pure=1|0     no declaration has deletions
#   paths=1|0    every declared path is relative, safe and present
#   canon=1|0    every declared path canonicalizes UNDER the export root
#   nul=0|1      a NUL byte was seen in the declaration file
#   diff-read=ok|fail
declared_blocks_check() { # TREE REF FILE
  local tree=$1 ref=$2 p=$3
  local declared=0 valid=0 tail=0 malformed=0 pure=1 paths=1 canon=1 nul=0 diffread=ok
  local line path lines sha extra
  if [ ! -f "$p" ]; then
    printf 'declared=0,valid=0,tail=0,malformed=0,pure=1,paths=0,canon=0,nul=0,diff-read=missing,file=missing'
    return 1
  fi
  if [ "$(tr -d '\000' < "$p" | wc -c)" != "$(wc -c < "$p")" ]; then nul=1; fi
  local root real
  root=$(realpath -m -- "$tree")
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    set -f; set -- $line; set +f
    path=${1:-}; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
      malformed=$((malformed + 1)); continue
    fi
    case $lines in ''|*[!0-9]*) malformed=$((malformed + 1)); continue ;; esac
    [ "$lines" -ge 1 ] || { malformed=$((malformed + 1)); continue; }
    case $sha in ''|*[!0-9a-f]*) malformed=$((malformed + 1)); continue ;; esac
    [ "${#sha}" -eq 64 ] || { malformed=$((malformed + 1)); continue; }
    declared=$((declared + 1))
    local okp=1
    path_safe "$path" || okp=0
    if [ "$okp" -eq 1 ]; then
      if [ -L "$tree/$path" ]; then okp=0; fi
      if [ "$okp" -eq 1 ] && [ ! -f "$tree/$path" ]; then okp=0; fi
    fi
    # the canonicalization clause is graded on its own: a declared path that
    # resolves OUTSIDE the export root is the round-40 wave-2 T7 escape
    if path_safe "$path"; then
      real=$(realpath -m -- "$tree/$path" 2>/dev/null || printf '')
      case "$real" in
        "$root"/*) ;;
        *) canon=0 ;;
      esac
    else
      canon=0
    fi
    if [ "$okp" -eq 0 ]; then paths=0; continue; fi
    local got
    got=$(tail -n "$lines" -- "$tree/$path" | sha256sum | awk '{print $1; exit}')
    [ "$got" = "$sha" ] || continue
    tail=$((tail + 1))
    local nm add del
    if ! nm=$(git --no-optional-locks -C "$LANE" diff --numstat "$BASE_REF" "$ref" -- "$path" < /dev/null); then
      diffread=fail; continue
    fi
    [ -n "$nm" ] || continue
    set -f; set -- $nm; set +f
    add=${1:-}; del=${2:-}
    case $add in ''|*[!0-9]*) diffread=fail; continue ;; esac
    [ "$add" = "$lines" ] || continue
    [ "$del" = 0 ] || { pure=0; continue; }
    valid=$((valid + 1))
  done < "$p"
  printf 'declared=%s,valid=%s,tail=%s,malformed=%s,pure=%s,paths=%s,canon=%s,nul=%s,diff-read=%s,file=present' \
    "$declared" "$valid" "$tail" "$malformed" "$pure" "$paths" "$canon" "$nul" "$diffread"
  [ "$malformed" -eq 0 ] && [ "$valid" -eq "$declared" ] && [ "$pure" -eq 1 ] \
    && [ "$paths" -eq 1 ] && [ "$canon" -eq 1 ] && [ "$nul" -eq 0 ] && [ "$diffread" = ok ] && return 0
  return 1
}

check_i5() { # TREE REF
  local tree=$1 ref=$2
  local p=${R41_DECLARED:-$DECLARED}
  (
    cd "$tree" || { printf 'declared=0,valid=0,tail=0,malformed=0,pure=1,paths=0,canon=0,nul=0,diff-read=fail,file=missing'; exit 1; }
    declared_blocks_check "$tree" "$ref" "$p"
    exit $?
  )
}

check_i6() { # TREE REF
  local root=$SCRATCH_ROOT
  local realw='' realroot='' res n
  if [ -z "${WORK:-}" ]; then
    printf 'strays=0,read=fail,scanned=0'
    return 1
  fi
  realw=$( cd "$WORK" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail,scanned=0'; return 1; }
  if [ -d "$root" ]; then
    realroot=$( cd "$root" && pwd -P ) || { printf 'strays=0,read=fail,scanned=0'; return 1; }
  else
    realroot=$root
  fi
  res=$(scan_scratch "$realroot" "$realw")
  printf '%s' "$res"
  n=${res#strays=}; n=${n%%,*}
  case $n in ''|*[!0-9]*) printf 'strays=0,read=fail,scanned=0'; return 1 ;; esac
  case "$res" in *'read=ok'*) ;; *) return 1 ;; esac
  [ "$n" -eq 0 ] && return 0
  return 1
}

# registry_row_state FILE NAME — prints "rows=<n> cells=<n> broken=<n> ok=<n>"
# for the SKILL.md registry: a candidate row is a table row whose FIRST cell is
# exactly the instrument basename; it is well formed when it has enough cells,
# when the preceding line is a table row or a separator (never a blank line —
# the round-40 D6 defect) and when the contiguous table above it carries a
# header row naming `name`.
registry_row_state() { # FILE NAME
  local f=$1 name=$2
  local rows=0 ok=0 broken=0 cellsmax=0 ln prev
  local -a lns=()
  while IFS= read -r ln; do
    [ -n "$ln" ] || continue
    lns+=("$ln")
  done < <(fence_matchno "$f" '^[|]')
  local total=${#lns[@]} i=0
  while [ $i -lt $total ]; do
    ln=${lns[$i]}
    local num=${ln%%$'\t'*}
    local content=${ln#*$'\t'}
    local first nf
    first=$(printf '%s' "$content" | awk -F'|' '{ gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2 }')
    first=${first#\`}; first=${first%\`}
    if [ "$first" = "$name" ]; then
      rows=$((rows + 1))
      nf=$(printf '%s' "$content" | awk -F'|' '{print NF}')
      [ "$nf" -gt "$cellsmax" ] && cellsmax=$nf
      prev=$(sed -n "$((num - 1))p" -- "$f" 2>/dev/null)
      case "$prev" in
        '|'*) ;;
        *) broken=$((broken + 1)); i=$((i + 1)); continue ;;
      esac
      local head=0 j=$((i - 1)) c
      while [ $j -ge 0 ]; do
        c=${lns[$j]}
        c=${c#*$'\t'}
        case "$c" in '|'*) ;; *) break ;; esac
        if printf '%s' "$c" | grep -qiE '^\|[^|]*name[^|]*\|'; then head=1; break; fi
        j=$((j - 1))
      done
      if [ "$head" -eq 1 ] && [ "$nf" -ge 8 ]; then ok=$((ok + 1)); fi
    fi
    i=$((i + 1))
  done
  printf 'rows=%s,cells=%s,broken=%s,ok=%s' "$rows" "$cellsmax" "$broken" "$ok"
}

check_i7() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'mentions=0,rows=0,well-formed=0,table=0,cells=0,broken=0,r40-table=0'; exit 1; }
    local mentions=0 state rows cells broken ok r40state r40ok=0
    if [ ! -f SKILL.md ]; then
      printf 'mentions=0,rows=0,well-formed=0,table=0,cells=0,broken=0,r40-table=0'
      exit 1
    fi
    mentions=$(grep -c 'r41-closure\.sh' -- SKILL.md 2>/dev/null || true)
    mentions=${mentions:-0}
    state=$(registry_row_state SKILL.md r41-closure.sh)
    rows=$(kv_get "$state" rows); cells=$(kv_get "$state" cells)
    broken=$(kv_get "$state" broken); ok=$(kv_get "$state" ok)
    r40state=$(registry_row_state SKILL.md r40-closure.sh)
    r40ok=$(kv_get "$r40state" ok)
    printf 'mentions=%s,rows=%s,well-formed=%s,table=%s,cells=%s,broken=%s,r40-table=%s' \
      "$mentions" "$rows" "$([ "$ok" -ge 1 ] && echo 1 || echo 0)" \
      "$([ "$ok" -ge 1 ] && echo 1 || echo 0)" "$cells" "$broken" \
      "$([ "$r40ok" -ge 1 ] && echo 1 || echo 0)"
    [ "$ok" -ge 1 ] && [ "$broken" -eq 0 ] && exit 0
    exit 1
  )
}

# synthetic_receipt OUT — an honest receipt built from the fresh payloads of
# this run and the graded selftest lines. It is the base for the I8 forgery
# variants and the I9 isolation probes; it never reads the committed receipt.
synthetic_receipt() { # OUT
  local out=$1 id href sha utc
  href=$REF_RESOLVED
  sha=$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")
  utc=$(ref_utc "$href"); [ -n "$utc" ] || utc=unreadable
  {
    printf '%s\n' "$SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in "${CHECK_IDS[@]}"; do
      printf '%s payload=%s closed=1\n' "$id" "$(payload_get "$id")"
    done
    if [ -n "${SELFILE:-}" ] && [ -f "$SELFILE" ]; then cat -- "$SELFILE"; fi
    printf 'selftest cases=12 failures=0\n'
    printf 'closed=12/12 exit=0\n'
  } > "$out"
}

# forge_flags FILE — one independent verdict flag per receipt-forgery variant.
# A variant is flagged by ITS OWN clause, never by a count of mismatches (the
# round-40 wave-2 MutH1H5 class).
forge_flags() { # FILE
  local f=$1
  local payload=future=foreign=nonexistent=summary=tampered=missed
  local shape refhex
  shape=$(receipt_shape "$f")
  refhex=$(kv_get "$shape" ref)
  local pm
  pm=$(payload_match_count "$f" "${NON_I2_I8[@]}")
  if [ "$pm" -lt 10 ]; then payload=rejected; else payload=missed; fi
  if [ "$(kv_get "$shape" not-future)" = 1 ]; then future=missed; else future=rejected; fi
  if [ -n "$refhex" ] && ! git -C "$LANE" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
    foreign=rejected; nonexistent=rejected
  else
    foreign=missed; nonexistent=missed
  fi
  if [ "$(kv_get "$shape" run-lines)" = 0 ]; then summary=rejected; else summary=missed; fi
  if [ "$(kv_get "$shape" closed-0)" -gt 0 ] 2>/dev/null; then tampered=rejected; else tampered=missed; fi
  case "${R41_FORGE_DISABLE:-}" in
    payload-contradicting) payload=missed ;;
    future-dated) future=missed ;;
    foreign-ref) foreign=missed ;;
    nonexistent-ref) nonexistent=missed ;;
    summary-only) summary=missed ;;
    tampered-payload-line) tampered=missed ;;
  esac
  printf 'payload-contradicting=%s,future-dated=%s,foreign-ref=%s,nonexistent-ref=%s,summary-only=%s,tampered-payload-line=%s' \
    "$payload" "$future" "$foreign" "$nonexistent" "$summary" "$tampered"
}

check_i8() { # TREE REF
  local tree=$1
  (
    local d=$MUT/i8
    rm -rf -- "$d"; mkdir -p -- "$d" || exit 1
    synthetic_receipt "$d/honest.txt"
    local control cp cf
    control=$(forge_flags "$d/honest.txt")
    cp=$(kv_get "$control" payload-contradicting)
    cf=$(kv_get "$control" future-dated)
    sed -E 's/^I5 payload=.* closed=1$/I5 payload=zz-forged closed=1/' -- "$d/honest.txt" > "$d/payload.txt"
    sed -E 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$d/honest.txt" > "$d/future.txt"
    sed -E 's/^export-ref=.*$/export-ref=1111111111111111111111111111111111111111/' -- "$d/honest.txt" > "$d/foreign.txt"
    sed -E 's/^export-ref=.*$/export-ref=0000000000000000000000000000000000000000/' -- "$d/honest.txt" > "$d/nonexistent.txt"
    { sed -n '1,5p' -- "$d/honest.txt"; printf 'closed=12/12 exit=0\n'; } > "$d/summary.txt"
    sed -E 's/^I7 payload=.* closed=1$/I7 payload=zz-tampered closed=0/' -- "$d/honest.txt" > "$d/tampered.txt"
    local p1 f1 f2 f3 f4 f5
    p1=$(kv_get "$(forge_flags "$d/payload.txt")" payload-contradicting)
    f1=$(kv_get "$(forge_flags "$d/future.txt")" future-dated)
    f2=$(kv_get "$(forge_flags "$d/foreign.txt")" foreign-ref)
    f3=$(kv_get "$(forge_flags "$d/nonexistent.txt")" nonexistent-ref)
    f4=$(kv_get "$(forge_flags "$d/summary.txt")" summary-only)
    f5=$(kv_get "$(forge_flags "$d/tampered.txt")" tampered-payload-line)
    printf 'control=%s/%s,payload-contradicting=%s,future-dated=%s,foreign-ref=%s,nonexistent-ref=%s,summary-only=%s,tampered-payload-line=%s' \
      "$cp" "$cf" "$p1" "$f1" "$f2" "$f3" "$f4" "$f5"
    [ "$cp" = missed ] && [ "$cf" = missed ] || exit 1
    [ "$p1" = rejected ] && [ "$f1" = rejected ] && [ "$f2" = rejected ] \
      && [ "$f3" = rejected ] && [ "$f4" = rejected ] && [ "$f5" = rejected ] && exit 0
    exit 1
  )
}

check_i9() { # TREE REF
  local tree=$1
  (
    local d=$MUT/i9
    rm -rf -- "$d"; mkdir -p -- "$d" || exit 1
    synthetic_receipt "$d/honest.txt"
    local id n=0 iso=0 mism
    for id in "${CHECK_IDS[@]}"; do
      n=$((n + 1))
      sed -E "s/^$id payload=.* closed=1\$/$id payload=zz-tampered closed=1/" -- "$d/honest.txt" > "$d/t-$id.txt"
      mism=$(payload_match_ids "$d/t-$id.txt")
      if [ "$mism" = "$id" ]; then
        iso=$((iso + 1))
      fi
    done
    printf 'cases=%s,isolated=%s' "$n" "$iso"
    [ "$n" -eq 12 ] && [ "$iso" -eq 12 ] && exit 0
    exit 1
  )
}

# neg_accept TALLY EXIT I1 I2 I7 — the negative-control acceptance predicate,
# one line, killable: a tally that is not strictly below 12/12 is NEVER a
# negative control, and the tree-dependent checks I1, I2 and I7 must be red in
# the nested run (a leaf-capped green base has them green — the MutH6H10
# M-H8a class).
neg_accept() { # TALLY EXIT I1 I2 I7
  local k=$1 rc=$2 i1=$3 i2=$4 i7=$5
  case $k in ''|*[!0-9]*) return 1 ;; esac
  case $rc in ''|*[!0-9]*) return 1 ;; esac
  [ "$rc" -eq 1 ] || return 1
  if [ "${R41_NEG_WEAK:-0}" = 1 ]; then
    [ "$k" -le 12 ] || return 1
  else
    [ "$k" -lt 12 ] || return 1
  fi
  [ "$i1" -eq 0 ] || return 1
  [ "$i2" -eq 0 ] || return 1
  [ "$i7" -eq 0 ] || return 1
  return 0
}

check_i10() { # TREE REF
  local tree=$1
  (
    if [ "${R41_DEPTH:-0}" -ge 1 ]; then
      printf 'depth=1,base=?,r40=?,probe=0/3'
      exit 1
    fi
    local suite=$tree/corpus/instruments/r41-closure.sh
    if [ ! -f "$suite" ]; then
      printf 'suite=0,base=?,r40=?,probe=0/3'
      exit 1
    fi
    neg() { # REF TAG
      local o rc last k i1 i2 i7
      o=$(env R41_DEPTH=1 bash "$suite" --export-ref "$1" --lane "$LANE" \
            --work "$WORK/neg-$2" --scratch-root "$SCRATCH_ROOT" 2>&1); rc=$?
      last=$(printf '%s\n' "$o" | grep -E '^closed=' | tail -n 1)
      k='?'; i1='?'; i2='?'; i7='?'
      case $last in
        closed=*'/12'*) k=${last#closed=}; k=${k%%/*} ;;
      esac
      i1=$(printf '%s\n' "$o" | sed -n 's/^I1 payload=.* closed=\([01]\)$/\1/p' | tail -n 1)
      i2=$(printf '%s\n' "$o" | sed -n 's/^I2 payload=.* closed=\([01]\)$/\1/p' | tail -n 1)
      i7=$(printf '%s\n' "$o" | sed -n 's/^I7 payload=.* closed=\([01]\)$/\1/p' | tail -n 1)
      printf '%s %s %s %s %s' "$k" "$rc" "${i1:-?}" "${i2:-?}" "${i7:-?}"
    }
    local bk brc bi1 bi2 bi7 rk rrc ri1 ri2 ri7
    read -r bk brc bi1 bi2 bi7 <<< "$(neg "$BASE_REF" base)"
    read -r rk rrc ri1 ri2 ri7 <<< "$(neg "$R40_HEAD" r40)"
    local probe=0
    neg_accept 12 1 0 0 0 || probe=$((probe + 1))
    neg_accept 11 1 0 1 0 || probe=$((probe + 1))
    neg_accept 3 1 0 0 0 && probe=$((probe + 1))
    printf 'suite=1,base=%s/12,base-exit=%s,r40=%s/12,r40-exit=%s,probe=%s/3' \
      "$bk" "$brc" "$rk" "$rrc" "$probe"
    neg_accept "$bk" "$brc" "$bi1" "$bi2" "$bi7" || exit 1
    neg_accept "$rk" "$rrc" "$ri1" "$ri2" "$ri7" || exit 1
    [ "$probe" -eq 3 ] || exit 1
    exit 0
  )
}

# worktree_state REPO — the filing-time worktree-clean clause: the number of
# tracked files carrying a skip-worktree (S) or assume-unchanged (lower-case)
# marker, the number of tracked or untracked changes git status reports, and
# the number of gitignored untracked entries. `git status --porcelain` alone
# misses all three mechanisms (the round-40 wave-2 F8 escape).
worktree_state() { # REPO
  local repo=$1 flags dirty ignored
  flags=$(git -C "$repo" ls-files -v 2>/dev/null | awk '{ t = substr($0, 1, 1); if (t == "S" || t ~ /[a-z]/) c++ } END { print c + 0 }')
  dirty=$(git -C "$repo" status --porcelain --untracked-files=all 2>/dev/null | grep -c . || true)
  ignored=$(git -C "$repo" status --porcelain --ignored=matching --untracked-files=all 2>/dev/null | grep -c '^!!' || true)
  printf 'flags=%s,dirty=%s,ignored=%s' "${flags:-0}" "${dirty:-0}" "${ignored:-0}"
}

# worktree_markers REPO — the number of skip-worktree / assume-unchanged
# markers on tracked files.
worktree_markers() { # REPO
  local repo=$1 n
  n=$(git -C "$repo" ls-files -v 2>/dev/null | awk '{ t = substr($0, 1, 1); if (t == "S" || t ~ /[a-z]/) c++ } END { print c + 0 }')
  printf '%s' "${n:-0}"
}

# --- the eight committed CritKillRule escape states (F1-F8) ----------------

i11_probe_f1() { # a leftover nested under any top-level container
  local root=$MUT/i11/f1
  rm -rf -- "$root"; mkdir -p -- "$root/scratch/container/kasegi-r41-stray" "$root/work" || return 1
  local res; res=$(scan_scratch "$root/scratch" "$root/work")
  case "$res" in *'strays=0'*) return 1 ;; esac
  return 0
}

i11_probe_f2() { # the work dir inside the family container, a leftover inside it
  local root=$MUT/i11/f2
  rm -rf -- "$root"; mkdir -p -- "$root/scratch/kasegi-r41/work" "$root/scratch/kasegi-r41/nested/kasegi-r41-stray" || return 1
  local res; res=$(scan_scratch "$root/scratch" "$root/scratch/kasegi-r41/work")
  case "$res" in *'strays=0'*) return 1 ;; esac
  return 0
}

i11_probe_f3() { # a dot-prefixed family directory
  local root=$MUT/i11/f3
  rm -rf -- "$root"; mkdir -p -- "$root/scratch/.kasegi-r41-seat" "$root/work" || return 1
  local res; res=$(scan_scratch "$root/scratch" "$root/work")
  case "$res" in *'strays=0'*) return 1 ;; esac
  return 0
}

i11_probe_f4() { # case and separator variants of the family name
  local root=$MUT/i11/f4
  rm -rf -- "$root"; mkdir -p -- "$root/scratch" "$root/work" || return 1
  mkdir -p -- "$root/scratch/Kasegi-R41-Stray"
  mkdir -p -- "$root/scratch/kasegi_r41_stray"
  mkdir -p -- "$root/scratch/$(printf 'kasegi‑r41‑stray')"
  local res; res=$(scan_scratch "$root/scratch" "$root/work")
  case "$res" in *'strays=3'*) return 0 ;; esac
  return 1
}

i11_probe_f5() { # a family symlink resolving to an ancestor of the work dir
  local root=$MUT/i11/f5
  rm -rf -- "$root"; mkdir -p -- "$root/scratch" "$root/work" || return 1
  ln -s -- "$root" "$root/scratch/kasegi-r41-link" || return 1
  local res; res=$(scan_scratch "$root/scratch" "$root/work")
  case "$res" in *'strays=0'*) return 1 ;; esac
  return 0
}

i11_probe_f6() { # a missing scratch root must fail closed
  local res; res=$(scan_scratch "$MUT/i11/does-not-exist" "$MUT/i11")
  case "$res" in *'read=fail'*) return 0 ;; esac
  return 1
}

i11_probe_f7() { # an unfinished pending marker in any spelling
  local d=$MUT/i11/f7
  rm -rf -- "$d"; mkdir -p -- "$d" || return 1
  local br_l br_a
  br_l=$(printf '\xe2\x9f\xa8')
  br_a=$(printf '\xe2\x8c\xa9')
  {
    printf '# lesson\n\n## Gate\n\n'
    printf '%s pending\n' "$br_l"
    printf '%spending\n' "$br_a"
    printf '<pending\n'
    printf '%sPending\n' "$br_l"
    printf '%sPENDING\n' "$br_l"
  } > "$d/lesson.md"
  local res; res=$(pending_scan "$d/lesson.md")
  case "$res" in 'pending=0,'*) return 1 ;; esac
  return 0
}

i11_probe_f8() { # a skip-worktree marker hides a tracked change from git status
  local repo=$MUT/i11/f8-repo
  rm -rf -- "$repo"; mkdir -p -- "$repo" || return 1
  git -C "$repo" init -q || return 1
  local top real
  top=$(git -C "$repo" rev-parse --show-toplevel) || return 1
  real=$( cd "$repo" && pwd -P )
  [ "$top" = "$real" ] || return 1
  printf 'v1\n' > "$repo/tracked.txt"
  printf 'sub/\n' > "$repo/.gitignore"
  git -C "$repo" add -A || return 1
  git -C "$repo" -c user.email=r41-fixture@local -c user.name=r41-fixture \
    commit -q -m 'fixture' || return 1
  git -C "$repo" update-index --skip-worktree tracked.txt || return 1
  printf 'v1-exfiltrated\n' > "$repo/tracked.txt"
  mkdir -p -- "$repo/sub"; printf 'junk\n' > "$repo/sub/ignored-new"
  local res; res=$(worktree_state "$repo")
  case "$res" in 'flags=1,'*|'flags=0,'*'ignored=1'*) return 0 ;; esac
  return 1
}

check_i11() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'escapes=8,red=0'; exit 1; }
    local red=0 res='' id
    for id in F1 F2 F3 F4 F5 F6 F7 F8; do
      if [ "${R41_I11_BREAK:-}" = "$id" ]; then
        res="$res $id=green"; continue
      fi
      if "i11_probe_${id,,}"; then res="$res $id=red"; red=$((red + 1));
      else res="$res $id=green"; fi
    done
    # the two live clauses the escape states try to escape
    local pend
    pend=$(pending_scan "$tree/corpus/lessons/round-41.md")
    printf 'escapes=8,red=%s,%s,pending=%s' "$red" "${res# }" "${pend#pending=}"
    [ "$red" -eq 8 ] || exit 1
    case "$pend" in 'pending=0,'*) ;; *) exit 1 ;; esac
    exit 0
  )
}

check_i12() { # TREE REF
  local tree=$1 ref=$2
  local p=${R41_DECLARED:-$DECLARED}
  (
    cd "$tree" || { printf 'declared=0,valid=0,tail=0,pure=0,skill-del=0,province-del=0,density=0,deleted=0,census=0,ref-not-found=0,markers=0,neg-red=0'; exit 1; }
    local dstate declared valid tail pure
    dstate=$(declared_blocks_check "$tree" "$ref" "$p")
    declared=$(kv_get "$dstate" declared); valid=$(kv_get "$dstate" valid)
    tail=$(kv_get "$dstate" tail); pure=$(kv_get "$dstate" pure)
    # SKILL.md and PROVINCE.md are append-only
    local skdel=0 pvdel=0 nm add del path line
    if nm=$(git --no-optional-locks -C "$LANE" diff --numstat "$BASE_REF" "$ref" -- \
              SKILL.md PROVINCE.md < /dev/null); then
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        set -f; set -- $line; set +f
        add=${1:-}; del=${2:-}; path=${3:-}
        case $del in ''|*[!0-9]*) continue ;; esac
        case $path in
          SKILL.md) skdel=$((skdel + del)) ;;
          PROVINCE.md) pvdel=$((pvdel + del)) ;;
        esac
      done <<< "$nm"
    fi
    # density.py is byte-identical to base
    local dens=0
    [ "$(file_digest corpus/instruments/density.py)" = "$DENSITY_SHA" ] && dens=1
    # no tracked path is deleted by the round
    local deleted=0
    if nm=$(git --no-optional-locks -C "$LANE" diff --name-status --diff-filter=DR \
              "$BASE_REF" "$ref" < /dev/null); then
      [ -z "$nm" ] || deleted=$(printf '%s\n' "$nm" | count_lines)
      deleted=${deleted:-0}
    fi
    # the sources census exits 0 over the EXPORT's registry
    local census=0
    if [ -f "$CENSUS_SCRIPT" ] && [ -f corpus/SOURCES.md ]; then
      ( cd "$tree" && bash "$CENSUS_SCRIPT" validate --file corpus/SOURCES.md >/dev/null 2>&1 ) && census=1
    fi
    # an unresolvable --export-ref is a distinct red, never a vacuous tally
    local rnf=0 out rc
    out=$(bash "$SELF" --export-ref 0000000000000000000000000000000000000000 \
            --lane "$LANE" --work "$WORK/refnf" --scratch-root "$SCRATCH_ROOT" 2>&1); rc=$?
    if printf '%s\n' "$out" | grep -q 'ref-not-found' \
       && printf '%s\n' "$out" | grep -q '^suite-ref-status=ref-not-found$' \
       && printf '%s\n' "$out" | grep -q '^closed=0/12 exit=1$' \
       && [ "$rc" -eq 1 ]; then
      rnf=1
    fi
    # no skip-worktree / assume-unchanged marker hides a tracked change
    local markers; markers=$(worktree_markers "$LANE")
    # the negative controls are red (the I10 payload of this run)
    local negred=0 i10p
    i10p=$(payload_get I10)
    case $i10p in
      *'base='*'/12'*) case $i10p in *'base=12/12'*) negred=0 ;; *) negred=1 ;; esac ;;
    esac
    printf 'declared=%s,valid=%s,tail=%s,pure=%s,skill-del=%s,province-del=%s,density=%s,deleted=%s,census=%s,ref-not-found=%s,markers=%s,neg-red=%s' \
      "$declared" "$valid" "$tail" "$pure" "$skdel" "$pvdel" "$dens" "$deleted" "$census" "$rnf" "$markers" "$negred"
    [ "$valid" -eq "$declared" ] && [ "$pure" -eq 1 ] && [ "$skdel" -eq 0 ] && [ "$pvdel" -eq 0 ] \
      && [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && [ "$census" -eq 1 ] && [ "$rnf" -eq 1 ] \
      && [ "$markers" -eq 0 ] && [ "$negred" -eq 1 ] && exit 0
    exit 1
  )
}

run_check() { # ID TREE REF
  local id=$1; shift
  "check_${id,,}" "$@"
}

# ---------------------------------------------------------------------------
# the graded selftest
# ---------------------------------------------------------------------------

# selftest_prepare — the payload table the tree limbs read. Run once before
# the cases.
selftest_prepare() {
  : > "$PAYFILE"
  : > "$SELFILE"
}

# compute_payloads — the payload table, in dependency order. It is computed
# ONCE per run: a second computation would duplicate the rows and the first
# row would win, which is how a stale payload (and a stale forgery control)
# would survive.
compute_payloads() {
  local id p rc
  for id in "${PAYLOAD_ORDER[@]}"; do
    p=$(run_check "$id" "$EXPORT" "$REF_RESOLVED"); rc=$?
    printf '%s\t%s\t%s\n' "$id" "$p" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)" >> "$PAYFILE"
  done
}

# st_pos ID TREE REF — the positive limb of a case.
st_pos() { # ID TREE REF
  local id=$1 tree=$2 ref=$3 out rc
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  POS_PAYLOAD[$id]=$out
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s positive=pass payload=%s\n' "$id" "$out"
    return 0
  fi
  printf 'selftest detail=%s positive=fail rc=%s payload=%s\n' "$id" "$rc" "$out"
  return 1
}

# st_neg ID LABEL TREE REF NEEDLE — the defeat limb of a case: the fixture must
# be REJECTED, the payload must name the reopened limb and the payload must
# DIFFER from the positive payload (the comparison is on payload VALUES, not on
# the closed bit alone).
st_neg() { # ID LABEL TREE REF NEEDLE
  local id=$1 label=$2 tree=$3 ref=$4 needle=$5 out rc pos
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  pos=${POS_PAYLOAD[$id]:-}
  if [ "$rc" -ne 0 ] && printf '%s' "$out" | grep -qF -- "$needle" \
     && [ "$out" != "$pos" ]; then
    printf 'selftest detail=%s mutant=%s rejected=1 limb=%s\n' "$id" "$label" "$needle"
    return 0
  fi
  printf 'selftest detail=%s mutant=%s rejected=0 rc=%s payload=%s\n' \
    "$id" "$label" "$rc" "$out"
  FAILS=$((FAILS + 1))
  return 1
}

# st_verdict ID BAD OK N — the graded case line.
st_verdict() { # ID BAD OK N
  local id=$1 bad=$2 ok=$3 n=$4 pm v
  if [ "$bad" -eq 0 ]; then pm=1; v=pass; else pm=0; v=fail; fi
  if [ "$bad" -eq 0 ] && [ "$n" -ge 1 ] && [ "$ok" -eq "$n" ]; then pm=1; v=pass; else pm=0; v=fail; fi
  printf 'selftest case=%s mutants=%s/%s positive=%s payload-match=%s verdict=%s\n' \
    "$id" "$ok" "$n" "$([ "$pm" -eq 1 ] && echo pass || echo fail)" "$pm" "$v" \
    > "$WORK/sel-$id.line"
  if [ "$v" = pass ]; then return 0; fi
  FAILS=$((FAILS + 1))
  return 1
}

# fixture_tree DIR — a compact copy of the export with every file the tree
# limbs read. The copy is small (the lane tree is dominated by files no check
# reads) and every mutation therefore touches only the check under test.
fixture_tree() { # DIR
  local d=$1 f
  rm -rf -- "$d"; mkdir -p -- "$d" || return 1
  for f in "${RECORDS[@]}" SKILL.md PROVINCE.md corpus/instruments/density.py \
           corpus/instruments/r41-closure.sh corpus/SOURCES.md "${LESSONS[@]}"; do
    [ -f "$EXPORT/$f" ] || continue
    mkdir -p -- "$d/$(dirname -- "$f")"
    cp -p -- "$EXPORT/$f" "$d/$f" || return 1
  done
  return 0
}

# replace_line FILE PATTERN REPLACEMENT — replace the first line matching
# PATTERN (an ERE) with REPLACEMENT, in place.
replace_line() { # FILE PATTERN REPLACEMENT
  local f=$1 pat=$2 rep=$3 tmp
  tmp=$f.tmp.$$
  awk -v pat="$pat" -v rep="$rep" '
    !done && $0 ~ pat { print rep; done = 1; next }
    { print }
  ' "$f" > "$tmp" && mv -- "$tmp" "$f"
}

# append_line FILE TEXT
append_line() { # FILE TEXT
  printf '%s\n' "$2" >> "$1"
}

# --- the cases -------------------------------------------------------------

selftest_case_i1() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos I1 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I1-evidence; fixture_tree "$d" || return
  local rec
  for rec in "${RECORDS[@]}"; do
    replace_line "$d/$rec" '^Correction [(]round 41[)]' \
      'Correction (round 41): the round-40 claim C1 is not verified on the frozen counter; the round-40 receipt truth is closed=10/10 exit=0.'
  done
  st_neg I1 evidence-not-named "$d" "$REF_RESOLVED" 'evidence=0/3' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/I1-grading; fixture_tree "$d" || return
  replace_line "$d/LOG.md" '^Correction [(]round 41[)]' \
    'Correction (round 41): the round-40 claim C1 is verified; the kill-rule evidence is .ufo/waves/round-40/wave2/RevC1Counters.defeats.txt, .ufo/waves/round-40/wave2/CritKillRule.md and .ufo/waves/round-40/wave2/MutH6H10.md; the round-40 receipt truth is closed=10/10 exit=0.'
  st_neg I1 grading-absent "$d" "$REF_RESOLVED" 'graded=2' && ok=$((ok + 1))
  st_verdict I1 "$bad" "$ok" "$n"
}

selftest_case_i2() {
  local bad=0 ok=0 n=0 f savedr
  CASES=$((CASES + 1))
  savedr=${R41_RECEIPT_TARGET:-}
  f=$MUT/I2-honest.txt
  i2_fixture "$f"
  export R41_RECEIPT_TARGET="$f"
  st_pos I2 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1))
  sed -E 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$f" > "$f.future"
  export R41_RECEIPT_TARGET="$f.future"
  st_neg I2 future-dated-run-utc "$EXPORT" "$REF_RESOLVED" 'run-utc=0' && ok=$((ok + 1))
  n=$((n + 1))
  sed -E 's/^I5 payload=.* closed=1$/I5 payload=zz-forged closed=1/' -- "$f" > "$f.payload"
  export R41_RECEIPT_TARGET="$f.payload"
  st_neg I2 recorded-payload-contradicts "$EXPORT" "$REF_RESOLVED" 'payload-match=10/11' && ok=$((ok + 1))
  n=$((n + 1))
  { sed -n '1,5p' -- "$f"; printf 'closed=12/12 exit=0\n'; } > "$f.summary"
  export R41_RECEIPT_TARGET="$f.summary"
  st_neg I2 summary-only-body "$EXPORT" "$REF_RESOLVED" 'run-lines=0' && ok=$((ok + 1))
  n=$((n + 1))
  sed -E 's/^export-ref=.*$/export-ref=1111111111111111111111111111111111111111/' -- "$f" > "$f.foreign"
  export R41_RECEIPT_TARGET="$f.foreign"
  st_neg I2 foreign-ref "$EXPORT" "$REF_RESOLVED" 'ancestor=0' && ok=$((ok + 1))
  n=$((n + 1))
  sed -n '1,17p' "$f" > "$f.order"
  sed -n '19p' "$f" >> "$f.order"
  sed -n '18p' "$f" >> "$f.order"
  sed -n '20,$p' "$f" >> "$f.order"
  export R41_RECEIPT_TARGET="$f.order"
  st_neg I2 selftest-lines-reordered "$EXPORT" "$REF_RESOLVED" 'cmp=0' && ok=$((ok + 1))
  if [ -n "$savedr" ]; then export R41_RECEIPT_TARGET="$savedr"; else unset R41_RECEIPT_TARGET; fi
  st_verdict I2 "$bad" "$ok" "$n"
}

selftest_case_i3() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos I3 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I3-mangled; fixture_tree "$d" || return
  replace_line "$d/SCORECARD.md" '^Correction [(]round 41[)]' \
    'Correction (round 41): the round-40 claim C1 is not verified on the frozen counter; the round-40 receipt truth is closed=10/100 exit=0; the evidence is .ufo/waves/round-40/wave2/RevC1Counters.defeats.txt, .ufo/waves/round-40/wave2/CritKillRule.md and .ufo/waves/round-40/wave2/MutH6H10.md.'
  st_neg I3 mangled-value-token "$d" "$REF_RESOLVED" 'tally=2/3' && ok=$((ok + 1))
  st_verdict I3 "$bad" "$ok" "$n"
}

selftest_case_i4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos I4 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I4-fenced; fixture_tree "$d" || return
  append_line "$d/SHONEN.md" '```text'
  append_line "$d/SHONEN.md" 'Correction (round 41): pseudo-row inside a fence.'
  append_line "$d/SHONEN.md" '```'
  st_neg I4 fenced-correction-row "$d" "$REF_RESOLVED" 'fenced=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/I4-openfence; fixture_tree "$d" || return
  append_line "$d/LOG.md" '~~~text'
  append_line "$d/LOG.md" 'an opener that never closes'
  st_neg I4 fence-open-at-eof "$d" "$REF_RESOLVED" 'eof=open' && ok=$((ok + 1))
  st_verdict I4 "$bad" "$ok" "$n"
}

selftest_case_i5() {
  local bad=0 ok=0 n=0 d savedd
  CASES=$((CASES + 1))
  savedd=${R41_DECLARED:-$DECLARED}
  st_pos I5 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I5-escape; fixture_tree "$d" || return
  mkdir -p -- "$d/.ufo/waves/round-41"
  printf 'outside\n' > "$MUT/I5-outside.txt"
  ln -s -- "$MUT/I5-outside.txt" "$d/pwn"
  sha=$(sha256sum -- "$MUT/I5-outside.txt" | awk '{print $1; exit}')
  printf 'pwn 1 %s\n' "$sha" > "$d/.ufo/waves/round-41/declared-blocks.txt"
  export R41_DECLARED='.ufo/waves/round-41/declared-blocks.txt'
  st_neg I5 declared-path-escapes-root "$d" "$REF_RESOLVED" 'canon=0' && ok=$((ok + 1))
  export R41_DECLARED="$savedd"
  st_verdict I5 "$bad" "$ok" "$n"
}

selftest_case_i6() {
  local bad=0 ok=0 n=0 root save_root save_work res
  CASES=$((CASES + 1))
  save_root=$SCRATCH_ROOT
  save_work=$WORK
  st_pos I6 "$EXPORT" "$REF_RESOLVED" || bad=1
  # control: the passed --work dir is never a stray
  root=$MUT/I6-control; rm -rf -- "$root"; mkdir -p -- "$root/kasegi-r41-seat/work"
  SCRATCH_ROOT=$root; WORK=$root/kasegi-r41-seat/work
  res=$(run_check I6 "$EXPORT" "$REF_RESOLVED")
  case "$res" in
    'strays=0,read=ok,'*)
      printf 'selftest detail=I6 control=own-work-dir accepted=1 payload=%s\n' "$res" ;;
    *)
      printf 'selftest detail=I6 control=own-work-dir accepted=0 payload=%s\n' "$res"
      FAILS=$((FAILS + 1)) ;;
  esac
  n=$((n + 1)); root=$MUT/I6-stray; rm -rf -- "$root"
  mkdir -p -- "$root/kasegi-r41-stray" "$root/work"
  SCRATCH_ROOT=$root; WORK=$root/work
  st_neg I6 family-stray "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  n=$((n + 1)); root=$MUT/I6-nested; rm -rf -- "$root"
  mkdir -p -- "$root/container/kasegi-r41-stray" "$root/work"
  SCRATCH_ROOT=$root; WORK=$root/work
  st_neg I6 nested-family-stray "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  n=$((n + 1)); root=$MUT/I6-dot; rm -rf -- "$root"
  mkdir -p -- "$root/.kasegi-r41-seat" "$root/work"
  SCRATCH_ROOT=$root; WORK=$root/work
  st_neg I6 dot-prefixed-stray "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  n=$((n + 1)); root=$MUT/I6-case; rm -rf -- "$root"
  mkdir -p -- "$root/Kasegi_R41-stray" "$root/work"
  SCRATCH_ROOT=$root; WORK=$root/work
  st_neg I6 case-separator-stray "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  n=$((n + 1)); root=$MUT/I6-missing; rm -rf -- "$root"
  mkdir -p -- "$root/work"
  SCRATCH_ROOT=$root/missing-root; WORK=$root/work
  st_neg I6 unreadable-scratch-root "$EXPORT" "$REF_RESOLVED" 'read=fail' && ok=$((ok + 1))
  SCRATCH_ROOT=$save_root; WORK=$save_work
  st_verdict I6 "$bad" "$ok" "$n"
}

selftest_case_i7() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos I7 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I7-mention; fixture_tree "$d" || return
  grep -v '^| r41-closure\.sh ' "$d/SKILL.md" > "$d/SKILL.md.keep" && mv -- "$d/SKILL.md.keep" "$d/SKILL.md"
  printf '\nThe instrument r41-closure.sh is great and closes the round.\n' >> "$d/SKILL.md"
  st_neg I7 mention-only-row "$d" "$REF_RESOLVED" 'rows=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/I7-broken; fixture_tree "$d" || return
  printf '\n| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n\n| r41-closure.sh | gate | `bash corpus/instruments/r41-closure.sh --export-ref <hash>` | one line per check | selftest | receipt | scratch | kasegi |\n' >> "$d/SKILL.md"
  st_neg I7 row-after-blank-line "$d" "$REF_RESOLVED" 'broken=1' && ok=$((ok + 1))
  st_verdict I7 "$bad" "$ok" "$n"
}

selftest_case_i8() {
  local bad=0 ok=0 n=0 saved
  CASES=$((CASES + 1))
  st_pos I8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1))
  saved=${R41_FORGE_DISABLE:-}
  export R41_FORGE_DISABLE=payload-contradicting
  st_neg I8 forgery-detector-disabled "$EXPORT" "$REF_RESOLVED" 'payload-contradicting=missed' && ok=$((ok + 1))
  if [ -n "$saved" ]; then export R41_FORGE_DISABLE="$saved"; else unset R41_FORGE_DISABLE; fi
  st_verdict I8 "$bad" "$ok" "$n"
}

selftest_case_i9() {
  local bad=0 ok=0 n=0 saved
  CASES=$((CASES + 1))
  st_pos I9 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1))
  saved=${R41_ISOLATE_BREAK:-}
  export R41_ISOLATE_BREAK=1
  st_neg I9 count-relative-isolation "$EXPORT" "$REF_RESOLVED" 'isolated=0' && ok=$((ok + 1))
  if [ -n "$saved" ]; then export R41_ISOLATE_BREAK="$saved"; else unset R41_ISOLATE_BREAK; fi
  st_verdict I9 "$bad" "$ok" "$n"
}

selftest_case_i10() {
  local bad=0 ok=0 n=0 saved
  CASES=$((CASES + 1))
  st_pos I10 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1))
  saved=${R41_NEG_WEAK:-}
  export R41_NEG_WEAK=1
  st_neg I10 leaf-capped-green-base-accepted "$EXPORT" "$REF_RESOLVED" 'probe=2/3' && ok=$((ok + 1))
  if [ -n "$saved" ]; then export R41_NEG_WEAK="$saved"; else unset R41_NEG_WEAK; fi
  st_verdict I10 "$bad" "$ok" "$n"
}

selftest_case_i11() {
  local bad=0 ok=0 n=0 saved
  CASES=$((CASES + 1))
  st_pos I11 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1))
  saved=${R41_I11_BREAK:-}
  export R41_I11_BREAK=F3
  st_neg I11 escape-state-not-red "$EXPORT" "$REF_RESOLVED" 'red=7' && ok=$((ok + 1))
  if [ -n "$saved" ]; then export R41_I11_BREAK="$saved"; else unset R41_I11_BREAK; fi
  st_verdict I11 "$bad" "$ok" "$n"
}

selftest_case_i12() {
  local bad=0 ok=0 n=0 d savedd
  CASES=$((CASES + 1))
  savedd=${R41_DECLARED:-$DECLARED}
  st_pos I12 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/I12-density; fixture_tree "$d" || return
  append_line "$d/corpus/instruments/density.py" '# fixture mutation'
  st_neg I12 density-instrument-changed "$d" "$REF_RESOLVED" 'density=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/I12-census; fixture_tree "$d" || return
  printf '| S999 | not-a-registry-row\n' >> "$d/corpus/SOURCES.md"
  st_neg I12 census-not-clean "$d" "$REF_RESOLVED" 'census=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/I12-declared; fixture_tree "$d" || return
  mkdir -p -- "$d/.ufo/waves/round-41"
  printf 'PROVINCE.md 1 %s\n' "$(printf '%064d' 0)" > "$d/.ufo/waves/round-41/declared-blocks.txt"
  export R41_DECLARED='.ufo/waves/round-41/declared-blocks.txt'
  st_neg I12 declared-block-tail-mismatch "$d" "$REF_RESOLVED" 'valid=0' && ok=$((ok + 1))
  export R41_DECLARED="$savedd"
  st_verdict I12 "$bad" "$ok" "$n"
}

# judge_selftest_report FILE — a summary line alone must never pass: every
# case line must be well formed, must report positive=pass and verdict=pass,
# must carry mutants=<ok>/<n> with n >= 1 and ok == n, and must be backed by
# exactly n detail lines of which ok name rejected=1.
judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id line n ok det rej dup
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f"); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f"); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=12 failures=0$' "$f"); summary=${summary:-0}
  [ "$cases" -eq 12 ] && [ "$verdicts" -eq 12 ] && [ "$summary" -eq 1 ] || return 1
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

# run_selftest_cases — the twelve cases, in dependency order (I2 runs last:
# its positive limb needs the other eleven graded lines). Each case writes its
# verdict line to $WORK/sel-I<n>.line.
run_selftest_cases() {
  local id
  for id in I1 I3 I4 I5 I6 I7 I8 I9 I10 I11 I12 I2; do
    "selftest_case_${id,,}"
  done
}

# selftest_lines_ordered — the twelve graded case lines, in I1..I12 order.
selftest_lines_ordered() {
  local id
  for id in "${CHECK_IDS[@]}"; do
    [ -f "$WORK/sel-$id.line" ] && cat -- "$WORK/sel-$id.line"
  done
}

# ---------------------------------------------------------------------------
# the run
# ---------------------------------------------------------------------------

# i2_fixture OUT — an honest receipt built from the fresh payloads and the
# graded selftest lines of this run. It is the canonical transcript (the fixed
# point of the receipt contract) and the base of every receipt fixture.
i2_fixture() { # OUT
  local out=$1 href sha utc canon id
  href=$REF_RESOLVED
  sha=$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")
  utc=$(ref_utc "$href"); [ -n "$utc" ] || utc=unreadable
  {
    printf '%s\n' "$SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in "${CHECK_IDS[@]}"; do
      case $id in
        I2) printf 'I2 payload=pending closed=1\n' ;;
        I8) printf 'I8 payload=%s closed=1\n' "$(payload_get I8)" ;;
        *)  printf '%s payload=%s closed=1\n' "$id" "$(payload_get "$id")" ;;
      esac
    done
    selftest_others
    printf 'selftest case=I2 mutants=1/1 positive=pass payload-match=1 verdict=pass\n'
    printf 'selftest cases=12 failures=0\n'
    printf 'closed=12/12 exit=0\n'
  } > "$out"
  canon=$(i2_canonical "$out")
  {
    printf '%s\n' "$SENTINEL"
    printf 'export-ref=%s\n' "$href"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'time-basis=ref-commit\n'
    printf 'run-utc=%s\n' "$utc"
    for id in "${CHECK_IDS[@]}"; do
      case $id in
        I2) printf 'I2 payload=%s,cmp=1,i2-line=1 closed=1\n' "$canon" ;;
        I8) printf 'I8 payload=%s closed=1\n' "$(payload_get I8)" ;;
        *)  printf '%s payload=%s closed=1\n' "$id" "$(payload_get "$id")" ;;
      esac
    done
    selftest_others
    printf 'selftest case=I2 mutants=1/1 positive=pass payload-match=1 verdict=pass\n'
    printf 'selftest cases=12 failures=0\n'
    printf 'closed=12/12 exit=0\n'
  } > "$out"
}

# assemble_transcript — the receipt transcript of this run: the header, the
# twelve run lines, the twelve graded selftest lines, the selftest summary and
# the closed line.
assemble_transcript() {
  local id href sha utc k=0 e=1
  href=$(receipt_ref "$(receipt_source)"); [ -n "$href" ] || href=$REF_RESOLVED
  sha=$(file_digest "$EXPORT/corpus/instruments/r41-closure.sh")
  utc=$(ref_utc "$href"); [ -n "$utc" ] || utc=unreadable
  for id in "${CHECK_IDS[@]}"; do
    [ "$(payload_closed "$id")" = 1 ] && k=$((k + 1))
  done
  [ "$k" -eq 12 ] && e=0
  printf '%s\n' "$SENTINEL"
  printf 'export-ref=%s\n' "$href"
  printf 'suite-sha256=%s\n' "$sha"
  printf 'time-basis=ref-commit\n'
  printf 'run-utc=%s\n' "$utc"
  for id in "${CHECK_IDS[@]}"; do
    printf '%s payload=%s closed=%s\n' "$id" "$(payload_get "$id")" "$(payload_closed "$id")"
  done
  selftest_lines_ordered
  printf 'selftest cases=12 failures=%s\n' "$FAILS"
  printf 'closed=%s/12 exit=%s\n' "$k" "$e"
}

run_suite_report() {
  local id p rc k=0 n=0 bytes iter
  selftest_prepare
  compute_payloads
  # the graded selftest (its transcript is part of the receipt); the detail
  # lines stay out of stdout, only the twelve graded case lines are printed
  run_selftest_cases > "$WORK/selftest-detail.txt" 2>&1
  # the seed: the canonical transcript, so the first iteration is already the
  # fixed point of the receipt contract
  i2_fixture "$SEED"
  # I2 grades the receipt under test; the receipt is rewritten until the
  # transcript and the receipt agree
  for iter in 1 2 3 4; do
    p=$(run_check I2 "$EXPORT" "$REF_RESOLVED"); rc=$?
    printf 'I2\t%s\t%s\n' "$p" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)" > "$WORK/i2row.tsv"
    awk -F'\t' '$1 != "I2"' "$PAYFILE" > "$WORK/pay.tsv"
    cat -- "$WORK/pay.tsv" "$WORK/i2row.tsv" > "$PAYFILE"
    bytes=$(assemble_transcript)
    if [ -n "$RECEIPT_OUT" ]; then
      mkdir -p -- "$(dirname -- "$RECEIPT_OUT")" || die "cannot create receipt dir: $RECEIPT_OUT"
      printf '%s\n' "$bytes" > "$RECEIPT_OUT" || die "cannot write receipt: $RECEIPT_OUT"
      RECEIPT_WRITTEN=1
    fi
    # the fixed point: re-derive against the receipt that was just written
    local p2 rc2
    p2=$(run_check I2 "$EXPORT" "$REF_RESOLVED"); rc2=$?
    if [ "$p2" = "$p" ]; then break; fi
    printf 'I2\t%s\t%s\n' "$p2" "$([ "$rc2" -eq 0 ] && echo 1 || echo 0)" > "$WORK/i2row.tsv"
    awk -F'\t' '$1 != "I2"' "$PAYFILE" > "$WORK/pay.tsv"
    cat -- "$WORK/pay.tsv" "$WORK/i2row.tsv" > "$PAYFILE"
  done
  bytes=$(assemble_transcript)
  if [ -n "$RECEIPT_OUT" ]; then
    printf '%s\n' "$bytes" > "$RECEIPT_OUT" || die "cannot write receipt: $RECEIPT_OUT"
  fi
  printf '%s\n' "$bytes"
  for id in "${CHECK_IDS[@]}"; do
    [ "$(payload_closed "$id")" = 1 ] && k=$((k + 1))
  done
  n=$(printf '%s\n' "$bytes" | grep -c '^I[0-9]* payload='); n=${n:-0}
  if [ "$n" -ne 12 ]; then
    printf 'suite problem=self-report lines=%s expected=12\n' "$n"
    printf 'closed=0/12 exit=1\n'
    return 1
  fi
  [ "$k" -eq 12 ] && return 0
  return 1
}

run_selftest() {
  local f=$WORK/selftest-report.txt rc=0 id i
  selftest_prepare
  compute_payloads
  { run_selftest_cases; } > "$f" 2>&1
  selftest_lines_ordered >> "$f"
  printf 'selftest cases=%s failures=%s\n' "$CASES" "$FAILS" >> "$f"
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

  printf 'selftest cases=12 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    for i in $(seq 1 12); do
      printf 'selftest case=I%s positive=fail mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=12 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  {
    for i in $(seq 1 12); do
      printf 'selftest case=I%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=12 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  {
    for i in $(seq 1 11); do
      printf 'selftest case=I%s positive=pass mutants=1/1 verdict=pass\n' "$i"
      printf 'selftest detail=I%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=12 failures=0\n'
  } > "$WORK/forge-11-cases.txt"
  if judge_selftest_report "$WORK/forge-11-cases.txt"; then
    printf 'selftest judge=forged-11-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-11-cases rejected=1\n'
  fi

  {
    for i in $(seq 1 12); do
      printf 'selftest case=I%s positive=pass mutants=1/1\n' "$i"
      printf 'selftest detail=I%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=12 failures=0\n'
  } > "$WORK/forge-no-verdict.txt"
  if judge_selftest_report "$WORK/forge-no-verdict.txt"; then
    printf 'selftest judge=forged-no-verdict rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-no-verdict rejected=1\n'
  fi

  if [ "$CASES" -ne 12 ]; then
    printf 'selftest problem=cases=%s expected=12\n' "$CASES"
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
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  LANE=$( cd "$LANE" && pwd -P ) || die "cannot resolve lane: $LANE"
  case $MODE in
    run)
      if [ -z "$EXPORT_REF" ]; then
        printf 'r41-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r41-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
        exit 2
      fi
      prepare_export "$EXPORT_REF"
      run_suite_report
      ;;
    selftest)
      prepare_export "${EXPORT_REF:-HEAD}"
      printf 'selftest export-ref=%s suite-sha256=%s\n' "$REF_RESOLVED" "$(suite_digest)"
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
