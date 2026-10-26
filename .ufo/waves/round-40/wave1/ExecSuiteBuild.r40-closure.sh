#!/usr/bin/env bash
# r40-closure.sh — round-40 closure counter for claim C1 (depth:verifiability).
#
# Ten checks H1-H10. Each closes one defect class the round-39 verifier routed
# (corpus/lessons/round-39-verifier-spotcheck.md §5: R1-R7) or a round-39
# instrument attack finding (wave2/CritG2Exploit.md: G2 validated the shape and
# digest of the receipt but never compared a recorded payload with the export;
# wave2/CritC1Kill.md: G6 scanned two fixed scratch names and was live-state
# dependent):
#   H1 suite+registry row   the export carries this suite's exact bytes and a
#                           registry row for it in SKILL.md or the instruments
#                           README.
#   H2 corrections          a `Correction (round 40)` line in SCORECARD.md,
#                           LOG.md, SHONEN.md and corpus/lessons/round-39.md
#                           names the final round-39 receipt values
#                           (`closed=7/8`, `failures=1`) OUTSIDE any fence.
#   H3 criterion            corpus/QUALITY.md carries a table criterion row
#                           citing M39-2.
#   H4 located quotes       the round-39 lesson Gate blocks for S056/S058/S059
#                           each carry a URL, an access date, a located quote of
#                           <=25 words, and fail closed on an oversize quote.
#   H5 forgery rejection    a recorded payload contradicting the export, a
#                           future-dated run-utc, and a summary-only body are
#                           each REJECTED by the receipt verifier H7 uses.
#   H6 scratch siblings     a live scan of the scratch root by NAME FAMILY
#                           (`kasegi-r39*`, `kasegi-r40*`), not by a fixed pair,
#                           counts every sibling that does not contain this
#                           run's --work dir; fail-closed on a scan error.
#   H7 receipt transcript   the committed receipt is byte-identical to the
#                           transcript of the run that produced it: header,
#                           ten re-derived payload lines, one closed line.
#   H8 negative controls    the export's own suite run over the base commit and
#                           the round-39 judged head prints closed<10/10 exit=1.
#   H9 declared blocks      every `<path> <lines> <sha256>` declaration in
#                           .ufo/waves/round-40/declared-blocks.txt equals the
#                           whole appended tail, equals the added-line count of
#                           `git diff --numstat <base> <ref> -- <path>`, and the
#                           path has zero deletions.
#   H10 no-harm guard       SKILL.md and PROVINCE.md are append-only, the
#                           depth:density instrument `corpus/instruments/density.py`
#                           is byte-identical to the base commit, and the round's
#                           diff deletes no tracked path.
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -xf - -C <work>/export
# and every tree limb reads bytes only under that export root. Live reads are
# H6's scratch scan (host state by definition) and the ref-scoped git limbs
# (H7's ancestry/diff, H8's nested runs, H9's numstat, H10's numstat and
# name-status); all of them run with `--no-optional-locks` so the lane is never
# written to. Nothing is written under the lane by this suite except the single
# file named by `--receipt-out` (the caller's explicit request). --work must lie
# outside the lane; its `export/`, `mut/`, `neg-*` and `h5/` subdirectories are
# cleared before use, so a reused work dir can never satisfy a check with stale
# bytes. A plain run (no --export-ref, no --selftest) refuses with exit 2,
# because a suite that reads the working tree can be turned green by edits that
# were never committed.
#
# Usage:
#   bash corpus/instruments/r40-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run H1-H10 against the export. Prints the receipt
#       transcript — five header lines, one `H<n> payload=<k=v,...> closed=0|1`
#       line per check, and a final `closed=K/10 exit=0|1` — to stdout. Exit 0
#       only for K=10, exit 1 otherwise.
#   bash corpus/instruments/r40-closure.sh --export-ref <hash> --receipt-out PATH
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Same, and write the transcript to PATH: the file always equals the
#       stdout of the run that wrote it, red or green (a red run's receipt
#       carries its own closed=0 lines and its own red tally; a receipt is never
#       a tally the run did not print). Use this to PRODUCE the receipt at the
#       judged head J (the tree that does not yet contain the receipt); commit
#       exactly those bytes as Y = J + receipt, and only when they read
#       closed=10/10. The suite creates PATH's parent directory if needed and
#       writes that one file.
#   bash corpus/instruments/r40-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check at least one scratch fixture that reopens
#       exactly one clause must be REJECTED, and the rejection payload must name
#       the reopened limb, so a fixture proves the check discriminates rather
#       than that it can be satisfied by a summary. Prints one GRADED
#       `selftest case=H<i> positive=pass|fail mutants=<ok>/<n> verdict=pass|fail`
#       line per check, the `selftest detail=` lines behind them, the
#       `selftest judge=` lines (own report accepted, six forged reports
#       rejected) and `selftest cases=10 failures=<k>`; exit 0 only when all ten
#       cases ran, every positive passed and every mutant was rejected.
#   bash corpus/instruments/r40-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# THE RECEIPT CONTRACT (v4). The receipt is a transcript, not a summary:
#
#   all-gates v4
#   export-ref=<40 hex>
#   suite-sha256=<64 hex>
#   time-basis=ref-commit
#   run-utc=<YYYY-MM-DDTHH:MM:SSZ>
#   H1 payload=... closed=1
#   ... H2-H9 ...
#   H10 payload=... closed=1
#   closed=10/10 exit=0
#
# `export-ref` is the commit the transcript was teed at (the judged head J when
# the receipt is committed at Y = J + receipt). It may not be this run's ref:
# a commit cannot contain its own hash, so the receipt names the parent and the
# suite verifies `git diff --name-only <that ref> <this ref>` lists nothing but
# the receipt. `time-basis=ref-commit` states exactly what `run-utc` is: the
# committer instant of `export-ref`, read from the lane with
# `git log -1 --format=%ct` and printed as UTC — NOT a wall-clock stamp. That
# is deliberate: a wall-clock run-utc makes a receipt unreproducible, and a
# wall-clock stamp that outran its own commit was the round-39 R1/M39-1
# false-provenance defect. A `run-utc` that does not equal the ref's committer
# instant, or that post-dates the verification clock, is RED.
#
# H7 re-derives the transcript: it recomputes every payload from the export,
# compares each recorded `H<n> payload=` with the recomputed one, rebuilds the
# canonical transcript line by line (the H7 line itself is rebuilt from the
# receipt minus its own H7 line, so the self-reference is closed rather than
# trusted) and requires `cmp` equality with the committed receipt. A forged
# value, a re-stamped timestamp, a foreign ref, an extra line, a duplicate id or
# a summary-only body therefore reds the run.
#
# No path, no flag and no clock is printed: the transcript is a function of the
# tree and the ref-scoped facts only, so two plain runs over the same ref are
# byte-identical and the receipt equals a re-run with nothing normalised.
#
# THE GREEN WINDOW (measured, not assumed). H7 requires the receipt inside the
# export. A commit cannot contain its own hash, so at J the receipt is absent by
# construction and the suite prints `closed=9/10 exit=1` (H7 red, fail-closed).
# The 10/10 window is the lane tip Y = J + the receipt alone
# (`git diff --name-only J Y` = that one path). Production of the receipt is
# `--receipt-out` at J: the bytes it writes name J and are byte-identical to the
# transcript a plain run prints at Y.
#
# Documented limits (measured, not hidden):
#   - H6 is LIVE (host state by definition) and cannot be a pure function of a
#     commit: a receipt produced on a clean scratch root is reproduced only on a
#     clean scratch root. It scans the scratch root's TOP LEVEL by name family;
#     entries nested inside the one family directory that contains --work are
#     the caller's own space and are not audited. Its payload prints only the
#     stray count and the read state, so moving --work inside or outside the
#     scratch root does not change the transcript.
#   - H8 executes the export's own suite copy, in leaf mode (`R40_LEAF=1`), so
#     the negative controls terminate at depth 1. `R40_NEG_BASE` /
#     `R40_NEG_R39` exist only so the selftest can reopen the exit-code clause.
#   - H9 measures `git diff --numstat <base> <ref>`, so a ref older than the
#     base constant cannot be measured (red, not skipped). A path declared
#     twice is validated twice.
#   - H10 pins the base digest of density.py; an intentional change to the
#     depth:density instrument is a red until this constant is moved in a round
#     that says so.
#   - H4 accepts a located quote as one double-quoted span of 1..25 words plus a
#     `:NN` / `line NN` / `page N` / `§` / `section` location token in the same
#     Gate block; a quote that is present but unlocatable does not count.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku
BASE_REF=a7af2ce63bce153757d39bf66b366a96caf30c13
R39_HEAD=8371e7ac9f32cae5ed72f8c28205634603f836fa
DENSITY_SHA=ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710
RECEIPT=.ufo/waves/round-40/final-gates/all-gates.txt
DECLARED=.ufo/waves/round-40/declared-blocks.txt
SENTINEL='all-gates v4'
CHECK_IDS=(H1 H2 H3 H4 H5 H6 H7 H8 H9 H10)
# dependency order: H5 reads the eight payloads, H7 reads all nine others
EIGHT=(H1 H2 H3 H4 H6 H8 H9 H10)
NINE=(H1 H2 H3 H4 H5 H6 H8 H9 H10)
DEP_ORDER=(H1 H2 H3 H4 H6 H8 H9 H10 H5)

# SELF — absolute physical path of the executing bytes. Resolved once at load
# time because the H1 digest limb calls suite_digest() from a subshell that has
# cd'd into the export tree; a relative BASH_SOURCE would name the wrong file.
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
RECEIPT_OUT=
REF_RESOLVED=
WORK=
EXPORT=
MUT=
WORK_AUTO=0
CASES=0
FAILS=0
PAYFILE=
H5_SOURCE=
H7_TARGET=

# suite_digest — sha256 of the bytes actually executing. Printed in the header so
# a reader can bind a `closed=10/10` line (and the committed receipt) to the
# instrument that produced it. An unreadable SELF prints `unreadable`, which
# matches no 64-hex digest.
suite_digest() {
  local s=${SELF:-}
  if [ -z "$s" ] || [ ! -r "$s" ]; then printf 'unreadable'; return 0; fi
  sha256sum -- "$s" | awk '{print $1; exit}'
}

# file_digest FILE — sha256 of an arbitrary file, `unreadable` when the read
# fails (never an empty string a missing digest could be compared to).
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
  printf 'r40-closure: %s\n' "$*" >&2
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
        printf 'r40-closure: unknown argument: %s\n' "$1" >&2
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
  [ -n "${WORK:-}" ] && rm -rf -- "$WORK/neg-base" "$WORK/neg-r39"
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
    WORK=$(mktemp -d -t r40-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  PAYFILE=$WORK/payloads.tsv
  # Clear every owned subdirectory: a reused --work must never let a stale
  # export or a stale fixture satisfy a check.
  rm -rf -- "$EXPORT" "$MUT" "$WORK/neg-base" "$WORK/neg-r39" "$WORK/h5"
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
# closed by the next `^## ` heading (or EOF).
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

# path_safe PATH — a declaration may only name a plain relative path inside the
# export: no absolute path, no `..` component, no empty component.
path_safe() { # PATH
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

# kv_get STR KEY — the value of `KEY=` in a comma-joined k=v payload.
kv_get() { # STR KEY
  printf '%s\n' "$1" | tr ',' '\n' | sed -n "s/^$2=//p" | head -n 1
}

# ref_utc REF — the committer instant of REF as `YYYY-MM-DDTHH:MM:SSZ`, or an
# empty string when the ref cannot be read. Deterministic: it is a property of
# the commit, not of the clock.
ref_utc() { # REF
  local e
  [ -n "${1:-}" ] || return 1
  e=$(git -C "$LANE" log -1 --format=%ct "$1" 2>/dev/null) || return 1
  case $e in ''|*[!0-9]*) return 1 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}

# receipt_ref FILE — the single `export-ref=<40 hex>` of a receipt, or empty.
receipt_ref() { # FILE
  local f=$1 n
  [ -f "$f" ] || return 0
  n=$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f"); n=${n:-0}
  [ "$n" -eq 1 ] || return 0
  sed -n 's/^export-ref=//p' -- "$f" | head -n 1
}

# iso_past ISO — 1 when ISO is a well-formed UTC stamp no later than the
# verification clock plus 120 seconds of skew, 0 otherwise.
iso_past() { # ISO
  local iso=$1 n
  case $iso in
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z) ;;
    *) printf '0'; return 0 ;;
  esac
  n=$(date -u -d "$iso" +%s 2>/dev/null) || { printf '0'; return 0; }
  if [ "$n" -le $(( $(date -u +%s) + 120 )) ]; then printf '1'; else printf '0'; fi
}

# payload_get ID — the canonical payload this run computed for ID (from
# PAYFILE), or an empty string when it has not run yet.
payload_get() { # ID
  [ -n "$PAYFILE" ] && [ -f "$PAYFILE" ] || return 0
  awk -F'\t' -v id="$1" '$1 == id { print $2; exit }' "$PAYFILE"
}

# payload_closed ID — the recorded closed status (1|0) for ID, defaulting to 1
# when the check has not run yet.
payload_closed() { # ID
  local c
  [ -n "$PAYFILE" ] && [ -f "$PAYFILE" ] || { printf '1'; return 0; }
  c=$(awk -F'\t' -v id="$1" '$1 == id { print $3; exit }' "$PAYFILE")
  case $c in 0|1) printf '%s' "$c" ;; *) printf '1' ;; esac
}

# payload_matches FILE PAYFILE ID... — how many of the listed ids have a
# recorded `H<n> payload=` line in FILE equal to the canonical payload in
# PAYFILE. Pure: it compares bytes, it never runs a check.
payload_matches() { # FILE PAYFILE ID...
  local f=$1 pay=$2; shift 2
  local n=0 id rec want
  for id in "$@"; do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=''
    if [ -n "$pay" ] && [ -f "$pay" ]; then
      want=$(awk -F'\t' -v id="$id" '$1 == id { print $2; exit }' "$pay")
    fi
    if [ -n "$rec" ] && [ -n "$want" ] && [ "$rec" = "$want" ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}

# receipt_shape FILE — the shape and provenance facts of a receipt, with no
# payload recomputation and no ancestry read:
#   sentinel,ref,digest,time-basis,run-utc,not-future,header-lines,run-lines,
#   body-lines,closed-0,closed-line
# `digest` compares the recorded suite-sha256 with the export's own copy;
# `run-utc` compares the recorded stamp with the committer instant of the
# receipt's `export-ref`; `not-future` compares it with the verification clock.
receipt_shape() { # FILE
  local f=$1
  local sent=0 refhex='' dig=0 tb=0 utc=0 notf=0 hdr=0 runl=0 body=0 c0=0 cl=0
  local n u want total i line
  if [ ! -f "$f" ]; then
    printf 'sentinel=0,ref=,digest=0,time-basis=0,run-utc=0,not-future=0,header-lines=0,run-lines=0,body-lines=0,closed-0=0,closed-line=0'
    return 1
  fi
  [ "$(sed -n '1p' -- "$f")" = "$SENTINEL" ] && sent=1
  n=$(grep -cE '^export-ref=[0-9a-f]{40}$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then refhex=$(sed -n 's/^export-ref=//p' -- "$f" | head -n 1); fi
  n=$(grep -cE '^suite-sha256=[0-9a-f]{64}$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then
    u=$(sed -n 's/^suite-sha256=//p' -- "$f" | head -n 1)
    [ "$u" = "$(file_digest "$EXPORT/corpus/instruments/r40-closure.sh")" ] && dig=1
  fi
  n=$(grep -cxF -- 'time-basis=ref-commit' "$f"); n=${n:-0}
  [ "$n" -eq 1 ] && tb=1
  # header-lines: the first five lines must be the five header lines in order.
  if [ -n "$refhex" ]; then
    want="export-ref=$refhex"
    i=0
    for line in "$SENTINEL" "$want" "suite-sha256=$(file_digest "$EXPORT/corpus/instruments/r40-closure.sh")" \
                'time-basis=ref-commit' "run-utc=$(ref_utc "$refhex")"; do
      i=$((i + 1))
      [ "$(sed -n "${i}p" -- "$f")" = "$line" ] && hdr=$((hdr + 1))
    done
  fi
  n=$(grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' -- "$f"); n=${n:-0}
  if [ "$n" -eq 1 ]; then
    u=$(sed -n 's/^run-utc=//p' -- "$f" | head -n 1)
    [ "$(iso_past "$u")" = 1 ] && notf=1
    if [ -n "$refhex" ] && [ "$u" = "$(ref_utc "$refhex")" ]; then utc=1; fi
  fi
  runl=$(grep -cE '^H[0-9]+ payload=.* closed=[01]$' -- "$f"); runl=${runl:-0}
  c0=$(grep -cE '^H[0-9]+ payload=.* closed=0$' -- "$f"); c0=${c0:-0}
  n=$(grep -cxF -- 'closed=10/10 exit=0' "$f"); n=${n:-0}
  [ "$n" -eq 1 ] && cl=1
  total=$(count_lines < "$f"); total=${total:-0}
  body=$((total - 5)); [ "$body" -ge 0 ] || body=0
  printf 'sentinel=%s,ref=%s,digest=%s,time-basis=%s,run-utc=%s,not-future=%s,header-lines=%s,run-lines=%s,body-lines=%s,closed-0=%s,closed-line=%s' \
    "$sent" "$refhex" "$dig" "$tb" "$utc" "$notf" "$hdr" "$runl" "$body" "$c0" "$cl"
}

# assemble_transcript H7VAL [CLOSED] [actual|green] — the canonical transcript
# for this run's facts and this export's payloads, on stdout. H7VAL empty prints
# a `pending` H7 line, so the same function builds the H7-under-test file and
# the final bytes. CLOSED defaults to the green `closed=10/10 exit=0` line; in
# `actual` mode each line carries this run's recorded status.
assemble_transcript() { # H7VAL [CLOSED] [actual|green]
  local h7=${1:-} closed=${2:-closed=10/10 exit=0} mode=${3:-green} id p c
  local href sha utc
  href=$(receipt_ref "$EXPORT/$RECEIPT")
  [ -n "$href" ] || href=$REF_RESOLVED
  sha=$(file_digest "$EXPORT/corpus/instruments/r40-closure.sh")
  utc=$(ref_utc "$href"); [ -n "$utc" ] || utc=unreadable
  printf '%s\n' "$SENTINEL"
  printf 'export-ref=%s\n' "$href"
  printf 'suite-sha256=%s\n' "$sha"
  printf 'time-basis=ref-commit\n'
  printf 'run-utc=%s\n' "$utc"
  for id in "${CHECK_IDS[@]}"; do
    c=1
    [ "$mode" = actual ] && c=$(payload_closed "$id")
    if [ "$id" = H7 ]; then
      printf 'H7 payload=%s closed=%s\n' "${h7:-pending}" "$c"
      continue
    fi
    p=$(payload_get "$id"); [ -n "$p" ] || p=pending
    printf '%s payload=%s closed=%s\n' "$id" "$p" "$c"
  done
  printf '%s\n' "$closed"
}

# h7_inner FILE — the canonical H7 payload for a receipt, WITHOUT its own H7
# line: the self-reference is closed by never reading the line under test. The
# canonical value is this string with `,h7-line=1` appended.
h7_inner() { # FILE
  local f=$1 shape refhex sent anc=0 diffclean=0 diffread=ok pm=0 x name
  shape=$(receipt_shape "$f")
  refhex=$(kv_get "$shape" ref)
  sent=$(kv_get "$shape" sentinel)
  if [ -z "$refhex" ]; then
    printf 'receipt=%s,sentinel=0,ref=,digest=%s,time-basis=%s,run-utc=%s,not-future=%s,header-lines=%s,run-lines=%s,body-lines=%s,closed-0=%s,closed-line=%s,ancestor=0,diff-clean=0,diff-read=%s,payload-match=0' \
      "$([ -f "$f" ] && echo 1 || echo 0)" \
      "$(kv_get "$shape" digest)" "$(kv_get "$shape" time-basis)" \
      "$(kv_get "$shape" run-utc)" "$(kv_get "$shape" not-future)" \
      "$(kv_get "$shape" header-lines)" "$(kv_get "$shape" run-lines)" \
      "$(kv_get "$shape" body-lines)" "$(kv_get "$shape" closed-0)" \
      "$(kv_get "$shape" closed-line)" "$diffread"
    return 1
  fi
  if git -C "$LANE" cat-file -e "${refhex}^{commit}" 2>/dev/null; then
    if git --no-optional-locks -C "$LANE" merge-base --is-ancestor "$refhex" "$REF_RESOLVED" 2>/dev/null; then
      anc=1
    fi
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
  pm=$(payload_matches "$f" "$PAYFILE" "${NINE[@]}")
  printf '%s,ancestor=%s,diff-clean=%s,diff-read=%s,payload-match=%s' \
    "$shape" "$anc" "$diffclean" "$diffread" "$pm"
}

# ---------------------------------------------------------------------------
# checks — every one cd's into the export root and reads relative paths there
# ---------------------------------------------------------------------------

check_h1() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local suite=corpus/instruments/r40-closure.sh
    local have=0 dig=0 reg=0 where=none
    if [ -f "$suite" ]; then
      have=1
      [ "$(sed -n '1p' -- "$suite")" = '#!/usr/bin/env bash' ] || have=0
    fi
    if [ -f "$suite" ] && [ "$(file_digest "$suite")" = "$(suite_digest)" ]; then dig=1; fi
    # A registry row is a markdown table row naming the instrument, in the
    # SKILL.md instrument table or the corpus/instruments README.
    local s=0 r=0
    if [ -f SKILL.md ] && grep -qE '^\|[^|]*`?r40-closure\.sh`?[^|]*\|' -- SKILL.md; then s=1; fi
    if [ -f corpus/instruments/README.md ] \
       && grep -qE '^\|[^|]*`?r40-closure\.sh`?[^|]*\|' -- corpus/instruments/README.md; then r=1; fi
    if [ "$s" -eq 1 ] && [ "$r" -eq 1 ]; then where=both; reg=1
    elif [ "$s" -eq 1 ]; then where=skill; reg=1
    elif [ "$r" -eq 1 ]; then where=readme; reg=1; fi
    printf 'suite=%s,digest=%s,registry=%s,registry-in=%s' "$have" "$dig" "$reg" "$where"
    [ "$have" -eq 1 ] && [ "$dig" -eq 1 ] && [ "$reg" -eq 1 ] && exit 0
    exit 1
  )
}

# h2_scan FILE — one fence-aware pass over a record. Prints `<lines> <named>
# <open|closed>`: `lines` counts `Correction (round 40)` lines OUTSIDE a fence,
# `named` those of them that carry both final round-39 receipt values, and the
# last field is the fence state at EOF. Fence spelling: opener = up to three
# blanks then three backticks or three tildes and an optional info string;
# closer = up to three blanks then three of the SAME character and blanks only.
h2_scan() { # FILE
  [ -f "$1" ] || { printf '0 0 absent'; return 0; }
  awk '
    { s = $0
      if (!open) {
        if (index(s, "Correction (round 40)") == 1) {
          lines++
          if (index(s, "closed=7/8") > 0 && index(s, "failures=1") > 0) named++
        }
        if (s ~ /^ {0,3}```/) { open = 1; ftype = "`" }
        else if (s ~ /^ {0,3}~~~/) { open = 1; ftype = "~" }
      } else {
        if (ftype == "`" && s ~ /^ {0,3}```[ \t]*$/) open = 0
        else if (ftype == "~" && s ~ /^ {0,3}~~~[ \t]*$/) open = 0
      }
    }
    END { print lines + 0, named + 0, (open ? "open" : "closed") }
  ' "$1"
}

check_h2() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local f l n st
    local total=0 named=0 missing=0 fences=closed
    for f in SCORECARD.md LOG.md SHONEN.md corpus/lessons/round-39.md; do
      read -r l n st <<< "$(h2_scan "$f")"
      total=$((total + l)); named=$((named + n))
      [ "$n" -ge 1 ] || missing=$((missing + 1))
      [ "$st" = open ] && fences=open
    done
    printf 'corrections=%s,named=%s,missing=%s,fences=%s' "$total" "$named" "$missing" "$fences"
    [ "$missing" -eq 0 ] && [ "$fences" = closed ] && exit 0
    exit 1
  )
}

check_h3() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local mentions=0 rows=0
    if [ -f corpus/QUALITY.md ]; then
      mentions=$(grep -cF -- 'M39-2' corpus/QUALITY.md); mentions=${mentions:-0}
      rows=$(grep -E '^\|' -- corpus/QUALITY.md | grep -cF -- 'M39-2'); rows=${rows:-0}
    fi
    printf 'mentions=%s,rows=%s' "$mentions" "$rows"
    [ "$mentions" -ge 1 ] && [ "$rows" -ge 1 ] && exit 0
    exit 1
  )
}

# h4_code FILE CODE — evaluates every Gate block that mentions CODE and prints
# `<ok> <maxwords> <oversize>`: ok=1 when some block carries a URL, an access
# date, a location token and a quoted span of 1..25 words; oversize counts quoted
# spans that were rejected for length. A block starts at a mention of CODE and
# runs while lines are non-blank, are not a heading, and do not start another
# S0xx row.
h4_code() { # FILE CODE
  awk -v code="$2" '
    function words(q,   a) { return split(q, a, /[^ \t\n]+/) }
    function inhabit(   url, date, loc, n, w, c, over, rest, q) {
      url = (buf ~ /https?:\/\/[^ )>]+/) ? 1 : 0
      date = (buf ~ /(19|20)[0-9][0-9]-[0-9][0-9]-[0-9][0-9]/) ? 1 : 0
      loc = (buf ~ /:[0-9]+/ || buf ~ /[Ll]ines? ?[0-9]/ || buf ~ /[Pp]ages? ?[0-9]/ \
             || buf ~ /L[0-9]+/ || buf ~ /#[A-Za-z0-9._-]+/ || buf ~ /§/ \
             || buf ~ /[Ss]ection/ || buf ~ /[Pp]ara(graph)? ?[0-9]/) ? 1 : 0
      n = 0; w = 0; over = 0
      rest = buf
      while (match(rest, /"[^"]{1,600}"/)) {
        q = substr(rest, RSTART + 1, RLENGTH - 2)
        rest = substr(rest, RSTART + RLENGTH)
        c = words(q)
        if (c > 25) over++
        else if (c >= 1 && url && date && loc && c > w) { w = c; n = 1 }
      }
      rest = buf
      while (match(rest, /“[^”]{1,600}”/)) {
        q = substr(rest, RSTART + 1, RLENGTH - 2)
        rest = substr(rest, RSTART + RLENGTH)
        c = words(q)
        if (c > 25) over++
        else if (c >= 1 && url && date && loc && c > w) { w = c; n = 1 }
      }
      if (n) { ok = 1; if (w > bestw) bestw = w }
      overs += over
      buf = ""
    }
    { s = $0
      if (s ~ /^[ \t]*$/) { if (inb) inhabit(); inb = 0; next }
      if (s ~ /^#/) { if (inb) inhabit(); inb = 0; next }
      if (index(s, code)) { if (inb) inhabit(); inb = 1; buf = s; next }
      if (inb) {
        if (s ~ /S0[0-9][0-9]/) { inhabit(); inb = 0 }
        else buf = buf "\n" s
      }
    }
    END { if (inb) inhabit(); printf "%d %d %d\n", ok + 0, bestw + 0, overs + 0 }
  ' "$1"
}

check_h4() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local f=corpus/lessons/round-39.md
    local code ok words over
    local s056=0 s058=0 s059=0 oversize=0
    if [ ! -f "$f" ]; then
      printf 's056=0,s058=0,s059=0,oversize=0'
      exit 1
    fi
    for code in S056 S058 S059; do
      read -r ok words over <<< "$(h4_code "$f" "$code")"
      oversize=$((oversize + over))
      case $code in
        S056) s056=$ok ;;
        S058) s058=$ok ;;
        S059) s059=$ok ;;
      esac
    done
    printf 's056=%s,s058=%s,s059=%s,oversize=%s' "$s056" "$s058" "$s059" "$oversize"
    [ "$s056" -eq 1 ] && [ "$s058" -eq 1 ] && [ "$s059" -eq 1 ] && exit 0
    exit 1
  )
}

check_h5() { # TREE REF
  local tree=$1
  local src=${H5_SOURCE:-$tree/$RECEIPT}
  local ids=("${EIGHT[@]}")
  local shape control utc forged future summary
  local d=$MUT/h5
  (
    if [ ! -f "$src" ]; then
      printf 'source=0,control=0/8,utc=0,forged-payload=accepted,future-dated=accepted,summary-only=accepted'
      exit 1
    fi
    shape=$(receipt_shape "$src")
    utc=$(kv_get "$shape" not-future); [ -n "$utc" ] || utc=0
    control=$(payload_matches "$src" "$PAYFILE" "${ids[@]}")
    mkdir -p -- "$d" || { printf 'source=0,control=0/8,utc=0,forged-payload=accepted,future-dated=accepted,summary-only=accepted'; exit 1; }
    # variant 1 — a recorded payload that contradicts the export
    sed -E 's/^H3 payload=.* closed=[01]$/H3 payload=quality=99,rows=99 closed=1/' -- "$src" > "$d/forged.txt"
    if [ "$(payload_matches "$d/forged.txt" "$PAYFILE" "${ids[@]}")" -lt "$control" ]; then
      forged=rejected
    else
      forged=accepted
    fi
    # variant 2 — a future-dated run-utc
    sed -E "s/^run-utc=.*\$/run-utc=2999-01-01T00:00:00Z/" -- "$src" > "$d/future.txt"
    if [ "$(kv_get "$(receipt_shape "$d/future.txt")" not-future)" = 1 ]; then
      future=accepted
    else
      future=rejected
    fi
    # variant 3 — a summary-only body (header and closed line, no per-check lines)
    { sed -n '1,5p' -- "$src"; printf 'closed=10/10 exit=0\n'; } > "$d/summary.txt"
    if [ "$(kv_get "$(receipt_shape "$d/summary.txt")" run-lines)" = 0 ] \
       && [ "$(kv_get "$(receipt_shape "$d/summary.txt")" closed-line)" = 1 ]; then
      summary=rejected
    else
      summary=accepted
    fi
    printf 'source=1,control=%s/8,utc=%s,forged-payload=%s,future-dated=%s,summary-only=%s' \
      "$control" "$utc" "$forged" "$future" "$summary"
    [ "$control" -eq 8 ] && [ "$utc" = 1 ] && [ "$forged" = rejected ] \
      && [ "$future" = rejected ] && [ "$summary" = rejected ] && exit 0
    exit 1
  )
}

check_h6() { # TREE REF
  local root=$SCRATCH_ROOT
  local realw='' realroot='' e b r out
  local strays=0 read=ok
  if [ -z "${WORK:-}" ]; then
    printf 'strays=0,read=fail'
    return 1
  fi
  realw=$( cd "$WORK" 2>/dev/null && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
  if [ -d "$root" ]; then
    realroot=$( cd "$root" && pwd -P ) || { printf 'strays=0,read=fail'; return 1; }
    if ! out=$(find "$realroot" -mindepth 1 -maxdepth 1 -print 2>/dev/null); then
      printf 'strays=0,read=fail'
      return 1
    fi
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      b=${e##*/}
      case $b in
        kasegi-r39*|kasegi-r40*) ;;
        *) continue ;;
      esac
      r=$( cd "$e" 2>/dev/null && pwd -P ) || { read=fail; continue; }
      case $realw in
        "$r"|"$r"/*) continue ;;
      esac
      # Any matching family entry that does not contain this run's --work dir is
      # a leftover: an EMPTY one counts too, because a seat that merely emptied
      # its scratch still left the entry at filing.
      strays=$((strays + 1))
    done <<< "$out"
  fi
  printf 'strays=%s,read=%s' "$strays" "$read"
  [ "$read" = ok ] && [ "$strays" -eq 0 ] && return 0
  return 1
}

check_h7() { # TREE REF
  local tree=$1
  local f=${H7_TARGET:-$tree/$RECEIPT}
  local inner canonical rec shape refhex sha utc rebuild ok=1 x
  (
    inner=$(h7_inner "$f")
    canonical="$inner,h7-line=1"
    rec=$(sed -n 's/^H7 payload=\(.*\) closed=[01]$/\1/p' -- "$f" 2>/dev/null | head -n 1)
    if [ -n "$rec" ] && [ "$rec" = "$canonical" ]; then
      printf '%s' "$canonical"
    else
      printf '%s,h7-line=0' "$inner"
    fi
    # byte identity: rebuild the canonical transcript from this run's payloads,
    # this receipt's declared ref and the canonical H7 value, then cmp.
    shape=$(receipt_shape "$f")
    refhex=$(kv_get "$shape" ref)
    sha=$(file_digest "$EXPORT/corpus/instruments/r40-closure.sh")
    utc=''
    [ -n "$refhex" ] && utc=$(ref_utc "$refhex")
    [ -n "$utc" ] || utc=unreadable
    rebuild=$MUT/h7-rebuild.txt
    {
      printf '%s\n' "$SENTINEL"
      printf 'export-ref=%s\n' "$refhex"
      printf 'suite-sha256=%s\n' "$sha"
      printf 'time-basis=ref-commit\n'
      printf 'run-utc=%s\n' "$utc"
      for x in "${CHECK_IDS[@]}"; do
        if [ "$x" = H7 ]; then
          printf 'H7 payload=%s closed=1\n' "$canonical"
        else
          printf '%s payload=%s closed=1\n' "$x" "$(payload_get "$x")"
        fi
      done
      printf 'closed=10/10 exit=0\n'
    } > "$rebuild"
    [ "$(kv_get "$shape" sentinel)" = 1 ] || ok=0
    [ "$(kv_get "$shape" digest)" = 1 ] || ok=0
    [ "$(kv_get "$shape" time-basis)" = 1 ] || ok=0
    [ "$(kv_get "$shape" run-utc)" = 1 ] || ok=0
    [ "$(kv_get "$shape" not-future)" = 1 ] || ok=0
    [ "$(kv_get "$shape" header-lines)" = 5 ] || ok=0
    [ "$(kv_get "$shape" run-lines)" = 10 ] || ok=0
    [ "$(kv_get "$shape" body-lines)" = 11 ] || ok=0
    [ "$(kv_get "$shape" closed-0)" = 0 ] || ok=0
    [ "$(kv_get "$shape" closed-line)" = 1 ] || ok=0
    [ "$(kv_get "$inner" payload-match)" = 9 ] || ok=0
    [ "$(kv_get "$inner" ancestor)" = 1 ] || ok=0
    [ "$(kv_get "$inner" diff-clean)" = 1 ] || ok=0
    [ "$(kv_get "$inner" diff-read)" = ok ] || ok=0
    [ -n "$rec" ] && [ "$rec" = "$canonical" ] || ok=0
    cmp -s -- "$rebuild" "$f" || ok=0
    [ "$ok" -eq 1 ] && exit 0
    exit 1
  )
}

check_h8() { # TREE REF
  local tree=$1
  local base=${R40_NEG_BASE:-$BASE_REF}
  local r39=${R40_NEG_R39:-$R39_HEAD}
  local suite=$tree/corpus/instruments/r40-closure.sh
  local out rc last b k r rk
  if [ "${R40_LEAF:-0}" = 1 ]; then
    printf 'leaf=1,base=?,r39=?'
    return 1
  fi
  if [ ! -f "$suite" ]; then
    printf 'suite=0,base=?,r39=?'
    return 1
  fi
  neg() { # REF TAG
    local o c l k
    o=$(env -u R40_NEG_BASE -u R40_NEG_R39 R40_LEAF=1 bash "$suite" \
        --export-ref "$1" --lane "$LANE" --work "$WORK/neg-$2" \
        --scratch-root "$SCRATCH_ROOT" 2>&1); c=$?
    l=$(printf '%s\n' "$o" | grep -v '^$' | tail -n 1)
    k='?'
    case $l in
      closed=*/10\ exit=*) k=${l#closed=}; k=${k%%/*} ;;
    esac
    printf '%s %s' "$k" "$c"
  }
  read -r b rc <<< "$(neg "$base" base)"
  read -r r rk <<< "$(neg "$r39" r39)"
  printf 'base=%s/10,base-exit=%s,r39=%s/10,r39-exit=%s' "$b" "$rc" "$r" "$rk"
  case $b in ''|*[!0-9]*) return 1 ;; esac
  case $r in ''|*[!0-9]*) return 1 ;; esac
  [ "$b" -lt 10 ] && [ "$rc" -eq 1 ] && [ "$r" -lt 10 ] && [ "$rk" -eq 1 ] && return 0
  return 1
}

check_h9() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=$DECLARED
    local line path lines sha extra got nm add del
    local declared=0 valid=0 tail=0 pure=1 paths=1 diffread=ok
    if [ ! -f "$p" ]; then
      printf 'declared=0,valid=0,tail=0,pure=1,paths=1,diff-read=missing'
      exit 1
    fi
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
      if ! path_safe "$path"; then paths=0; continue; fi
      if [ ! -f "$tree/$path" ]; then paths=0; continue; fi
      got=$(tail -n "$lines" -- "$tree/$path" | sha256sum | awk '{print $1; exit}')
      [ "$got" = "$sha" ] || continue
      if ! nm=$(git --no-optional-locks -C "$LANE" diff --numstat "$BASE_REF" "$ref" -- "$path" < /dev/null); then
        diffread=fail
        continue
      fi
      if [ -z "$nm" ]; then continue; fi
      set -f
      set -- $nm
      set +f
      add=${1:-}; del=${2:-}
      case $add in ''|*[!0-9]*) diffread=fail; continue ;; esac
      [ "$add" = "$lines" ] || continue
      tail=$((tail + 1))
      [ "$del" = 0 ] || { pure=0; continue; }
      valid=$((valid + 1))
    done < "$p"
    printf 'declared=%s,valid=%s,tail=%s,pure=%s,paths=%s,diff-read=%s' \
      "$declared" "$valid" "$tail" "$pure" "$paths" "$diffread"
    [ "$diffread" = ok ] && [ "$declared" -ge 1 ] && [ "$valid" -eq "$declared" ] \
      && [ "$pure" -eq 1 ] && [ "$paths" -eq 1 ] && exit 0
    exit 1
  )
}

check_h10() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local dens=0 skdel=0 pvdel=0 deleted=0 diffread=ok nm add del path line
    if [ "$(file_digest corpus/instruments/density.py)" = "$DENSITY_SHA" ]; then dens=1; fi
    if nm=$(git --no-optional-locks -C "$LANE" diff --numstat "$BASE_REF" "$ref" -- \
              SKILL.md PROVINCE.md < /dev/null); then
      while IFS= read -r line; do
        [ -n "$line" ] || continue
        set -f; set -- $line; set +f
        add=${1:-}; del=${2:-}; path=${3:-}
        case $del in ''|*[!0-9]*) diffread=fail; continue ;; esac
        case $path in
          SKILL.md) skdel=$((skdel + del)) ;;
          PROVINCE.md) pvdel=$((pvdel + del)) ;;
        esac
      done <<< "$nm"
    else
      diffread=fail
    fi
    if nm=$(git --no-optional-locks -C "$LANE" diff --name-status --diff-filter=DR \
              "$BASE_REF" "$ref" < /dev/null); then
      [ -z "$nm" ] || deleted=$(printf '%s\n' "$nm" | count_lines)
      deleted=${deleted:-0}
    else
      diffread=fail
    fi
    printf 'skill-del=%s,province-del=%s,density=%s,deleted=%s,diff-read=%s' \
      "$skdel" "$pvdel" "$dens" "$deleted" "$diffread"
    [ "$diffread" = ok ] && [ "$skdel" -eq 0 ] && [ "$pvdel" -eq 0 ] \
      && [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && exit 0
    exit 1
  )
}

run_check() { # ID TREE REF
  local id=$1; shift
  # one name derivation instead of a second registry beside CHECK_IDS
  "check_${id,,}" "$@"
}

# ---------------------------------------------------------------------------
# the run: payloads in dependency order, then the transcript
# ---------------------------------------------------------------------------

run_suite_report() {
  local id p rc k=0 n=0 counted=0 transcript closed h7val bytes iter
  local -A RC=()
  : > "$PAYFILE"
  for id in "${DEP_ORDER[@]}"; do
    if [ "$id" = H5 ]; then
      if [ -f "$EXPORT/$RECEIPT" ]; then
        H5_SOURCE=$EXPORT/$RECEIPT
      else
        H5_SOURCE=$WORK/h5-source.txt
        assemble_transcript '' > "$H5_SOURCE"
      fi
    fi
    p=$(run_check "$id" "$EXPORT" "$REF_RESOLVED"); rc=$?
    RC[$id]=$rc
    printf '%s\t%s\t%s\n' "$id" "$p" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)" >> "$PAYFILE"
  done
  H7_TARGET=$EXPORT/$RECEIPT
  if [ -n "$RECEIPT_OUT" ]; then
    # Seed the file H7 reads with a pending H7 line and the canonical green
    # flags. The loop below then settles it to the transcript this run prints —
    # a red run's receipt carries its own red flags and red tally, because a
    # receipt is never a tally the run did not print.
    mkdir -p -- "$(dirname -- "$RECEIPT_OUT")" || die "cannot create receipt dir: $RECEIPT_OUT"
    assemble_transcript '' > "$WORK/h7-source.txt"
    h7val=$(h7_inner "$WORK/h7-source.txt"),h7-line=1
    printf '%s\n' "$(assemble_transcript "$h7val")" > "$RECEIPT_OUT" \
      || die "cannot write receipt: $RECEIPT_OUT"
    H7_TARGET=$RECEIPT_OUT
  fi
  iter=0
  while :; do
    p=$(run_check H7 "$EXPORT" "$REF_RESOLVED"); rc=$?
    RC[H7]=$rc
    k=0
    for id in "${CHECK_IDS[@]}"; do
      [ "${RC[$id]}" -eq 0 ] && k=$((k + 1))
    done
    if [ "$k" -eq 10 ]; then closed='closed=10/10 exit=0'; else closed="closed=$k/10 exit=1"; fi
    printf 'H7\t%s\t%s\n' "$p" "$([ "$rc" -eq 0 ] && echo 1 || echo 0)" > "$WORK/h7row.tsv"
    awk -F'\t' '$1 != "H7"' "$PAYFILE" > "$WORK/pay.tsv"
    cat -- "$WORK/pay.tsv" "$WORK/h7row.tsv" > "$PAYFILE"
    bytes=$(assemble_transcript "$p" "$closed" actual)
    [ -z "$RECEIPT_OUT" ] && break
    [ "$bytes" = "$(cat -- "$RECEIPT_OUT")" ] && break
    printf '%s\n' "$bytes" > "$RECEIPT_OUT" || die "cannot write receipt: $RECEIPT_OUT"
    iter=$((iter + 1))
    [ "$iter" -ge 4 ] && break
  done
  transcript=$bytes
  printf '%s\n' "$transcript"
  n=$(printf '%s\n' "$transcript" | grep -c '^H[0-9]* payload='); n=${n:-0}
  if [ "$n" -ne 10 ]; then
    printf 'suite problem=self-report lines=%s expected=10\n' "$n"
    printf 'closed=0/10 exit=1\n'
    return 1
  fi
  counted=$(printf '%s\n' "$transcript" | grep -c 'closed=1$'); counted=${counted:-0}
  if [ "$counted" -ne "$k" ]; then
    printf 'suite problem=self-report closed=%s counted=%s\n' "$k" "$counted"
    printf 'closed=0/10 exit=1\n'
    return 1
  fi
  [ "$k" -eq 10 ] && return 0
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
  git -C "$1" -c user.email=r40-fixture@local -c user.name=r40-fixture \
    commit -q -m "$2" || return 1
  git -C "$1" rev-parse --verify HEAD || return 1
}

# hist_repo_ready REPO — one fixture repository that contains the round-40 base
# commit and the round-39 judged head. Created under --work (outside the lane),
# its toplevel is asserted before any commit, and the fetch is ref-scoped so no
# other lane state leaks in. Prints the physical path on success.
hist_repo_ready() { # REPO
  local repo=$1 top real
  if [ -d "$repo/.git" ]; then printf '%s' "$repo"; return 0; fi
  mkdir -p -- "$repo" || return 1
  git -C "$repo" init -q || return 1
  top=$(git -C "$repo" rev-parse --show-toplevel) || return 1
  real=$( cd "$repo" && pwd -P )
  [ "$top" = "$real" ] || return 1
  git -C "$repo" fetch -q --no-tags "$LANE" "$BASE_REF" "$R39_HEAD" || return 1
  git -C "$repo" checkout -q --detach "$BASE_REF" || return 1
  printf '%s' "$real"
}

hist_reset() { # REPO
  git -C "$1" checkout -q -f --detach "$BASE_REF" || return 1
  git -C "$1" clean -qfd || return 1
}

# h1_tree DIR MODE — MODE=green|nosuite|norow|baddigest
h1_tree() { # DIR MODE
  local d=$1 mode=$2
  mut_reset "$d"
  mkdir -p -- "$d/corpus/instruments"
  cp -- "$SELF" "$d/corpus/instruments/r40-closure.sh" || return 1
  {
    printf '# skill\n\n| instrument | kind | run |\n|---|---|---|\n'
    [ "$mode" = norow ] || printf '| `r40-closure.sh` | gate | `bash corpus/instruments/r40-closure.sh --export-ref <hash>` |\n'
  } > "$d/SKILL.md"
  case $mode in
    nosuite) rm -f -- "$d/corpus/instruments/r40-closure.sh" ;;
    baddigest) printf '\n# fixture mutation\n' >> "$d/corpus/instruments/r40-closure.sh" ;;
  esac
  return 0
}

# h2_tree DIR MODE — MODE=green|nolesson|badvalues|openfence
h2_tree() { # DIR MODE
  local d=$1 mode=$2 f line
  mut_reset "$d"
  line='Correction (round 40): the final round-39 receipt values at 8371e7ac9f32cae5ed72f8c28205634603f836fa are closed=7/8 exit=1, and its selftest recorded failures=1; the 8/8 quote is report-only.'
  for f in SCORECARD.md LOG.md SHONEN.md corpus/lessons/round-39.md; do
    [ "$mode" = nolesson ] && [ "$f" = corpus/lessons/round-39.md ] && continue
    mkdir -p -- "$d/$(dirname -- "$f")"
    printf '# %s\n\n' "$f" >> "$d/$f"
    if [ "$mode" = badvalues ] && [ "$f" = corpus/lessons/round-39.md ]; then
      printf 'Correction (round 40): the round-39 receipt closed=8/8 exit=1 with no selftest line.\n' >> "$d/$f"
    else
      printf '%s\n' "$line" >> "$d/$f"
    fi
    [ "$mode" = openfence ] && [ "$f" = SCORECARD.md ] && printf '\n~~~text\nan opener that never closes\n' >> "$d/$f"
  done
  return 0
}

# h3_tree DIR MODE — MODE=green|nomention|prose
h3_tree() { # DIR MODE
  local d=$1 mode=$2
  mut_reset "$d"
  mkdir -p -- "$d/corpus"
  {
    printf '# QUALITY\n\n| id | criterion | grounded in |\n|---|---|---|\n'
    case $mode in
      green)
        printf '| R37 | A receipt is the unedited tee of one observed run; its run-utc is printed by the run, never restamped. | M39-2 (`corpus/lessons/round-39.md` § Mistakes) — R1 |\n' ;;
      nomention)
        printf '| R37 | A receipt is the unedited tee of one observed run. | M39-1 |\n' ;;
      prose)
        printf '\nThe M39-2 row records overstatement, and this paragraph cites it without a table criterion row.\n' ;;
    esac
  } > "$d/corpus/QUALITY.md"
  return 0
}

# h4_tree DIR MODE — MODE=green|nos059|oversize|nourl
h4_tree() { # DIR MODE
  local d=$1 mode=$2 q056 q058 q059
  mut_reset "$d"
  mkdir -p -- "$d/corpus/lessons"
  q056='- S056 (CISA Minimum Requirements for VEX) — https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex — accessed 2026-10-26 — "a consumer may require a minimum set of VEX fields before accepting a document" (page 3, lines 12-14).'
  q058='- S058 (OpenVEX v0.2.0) — https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md — accessed 2026-10-26 — "labels are the recommended mechanism for conveying status" (section 4, line 88).'
  q059='- S059 (CycloneDX v1.7 analysis) — https://cyclonedx.org/docs/1.7/json/ — accessed 2026-10-26 — "the analysis object states the state and justification for each affected component" (lines 410-412).'
  case $mode in
    nos059) q059='- S059 (CycloneDX v1.7 analysis) — REJECTED: different vocabulary; flip: a scoped analysis capture.' ;;
    oversize) q059='- S059 (CycloneDX v1.7 analysis) — https://cyclonedx.org/docs/1.7/json/ — accessed 2026-10-26 — "the analysis object states the state and justification for each affected component and it also carries a detail field for free text plus a first issued timestamp and a last updated timestamp" (lines 410-412).' ;;
    nourl) q056='- S056 (CISA Minimum Requirements for VEX) — accessed 2026-10-26 — "a consumer may require a minimum set of VEX fields" (page 3, lines 12-14).' ;;
  esac
  {
    printf '# Round 39 — kasegi\n\n## Gate\n\n### Rejected\n'
    printf -- '- S055 (older row) — REJECTED: mirrored.\n'
    printf '\n### Rejected — located quotes (round 40)\n\n'
    printf '%s\n\n' "$q056"
    printf '%s\n\n' "$q058"
    printf '%s\n' "$q059"
  } > "$d/corpus/lessons/round-39.md"
  return 0
}

# h5_fixture DIR MODE — a receipt built from this run's canonical payloads.
# MODE=green|forged|future. H5 reads the file through H5_SOURCE.
h5_fixture() { # DIR MODE
  local d=$1 mode=$2 f
  mut_reset "$d"
  f=$d/all-gates.txt
  assemble_transcript '' > "$f"
  case $mode in
    forged)
      # a payload string that no export can produce: the comparison is byte
      # equality, so the contradiction does not depend on the tree
      sed -E -i 's/^H3 payload=.* closed=1$/H3 payload=zz-forged closed=1/' -- "$f" ;;
    future)
      sed -E -i 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$f" ;;
  esac
  printf '%s' "$f"
}

# h7_fixture DIR MODE — a receipt to feed H7. MODE=absent|future|ancestor|
# digest|extraline|h7line. The fixture is written with this export's digest so
# exactly one clause reopens.
h7_fixture() { # DIR MODE
  local d=$1 mode=$2 f sha utc href
  mut_reset "$d"
  f=$d/all-gates.txt
  [ "$mode" = absent ] && { printf '%s' "$f"; return 0; }
  sha=$(file_digest "$EXPORT/corpus/instruments/r40-closure.sh")
  href=$(receipt_ref "$EXPORT/$RECEIPT"); [ -n "$href" ] || href=$REF_RESOLVED
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
    printf 'closed=10/10 exit=0\n'
  } > "$f"
  case $mode in
    future) sed -E -i 's/^run-utc=.*$/run-utc=2999-01-01T00:00:00Z/' -- "$f" ;;
    ancestor) sed -E -i 's/^export-ref=.*$/export-ref=0000000000000000000000000000000000000000/' -- "$f" ;;
    digest) sed -E -i 's/^suite-sha256=.*$/suite-sha256=0000000000000000000000000000000000000000000000000000000000000000/' -- "$f" ;;
    extraline) printf 'notes=fixture\n' >> "$f" ;;
    h7line) sed -E -i 's/^H7 payload=.* closed=1$/H7 payload=tampered closed=1/' -- "$f" ;;
  esac
  printf '%s' "$f"
}

# h9_fixture REPO MODE — a fixture commit whose two appended front-door tails
# are declared exactly. MODE=green|short|sha|del|escape|missing.
h9_fixture() { # REPO MODE
  local repo=$1 mode=$2 p added n sha
  hist_reset "$repo" || return 1
  printf '[r40 fixture amendment] F23 — fixture frontier line.\n\n' >> "$repo/PROVINCE.md"
  printf '\n## Round-40 fixture admission (appended 2026-10-26)\n\nF23 admitted.\n' >> "$repo/corpus/README.md"
  case $mode in
    del)
      # rewrite an existing PROVINCE.md line: the declared tail still matches,
      # but the path now has deletions
      awk 'NR == 5 { print "[rewritten]"; next } { print }' "$repo/PROVINCE.md" > "$repo/.ufo-tmp" \
        && mv -- "$repo/.ufo-tmp" "$repo/PROVINCE.md" ;;
  esac
  mkdir -p -- "$repo/.ufo/waves/round-40"
  : > "$repo/.ufo/waves/round-40/declared-blocks.txt"
  for p in PROVINCE.md corpus/README.md; do
    added=$(git -C "$repo" diff --numstat "$BASE_REF" -- "$p" 2>/dev/null | awk 'NF >= 2 { print $1; exit }')
    added=${added:-0}
    n=$added
    [ "$mode" = short ] && n=$((added - 1))
    [ "$n" -ge 1 ] || n=1
    sha=$(tail -n "$n" -- "$repo/$p" | sha256sum | awk '{print $1; exit}')
    [ "$mode" = sha ] && sha=$(printf '%064d' 0)
    printf '%s %s %s\n' "$p" "$n" "$sha" >> "$repo/.ufo/waves/round-40/declared-blocks.txt"
  done
  case $mode in
    escape)
      printf 'stray\n' > "$(dirname -- "$repo")/outside-fixture.md"
      sha=$(sha256sum -- "$(dirname -- "$repo")/outside-fixture.md" | awk '{print $1; exit}')
      printf '../outside-fixture.md 1 %s\n' "$sha" >> "$repo/.ufo/waves/round-40/declared-blocks.txt" ;;
    missing)
      sha=$(printf '%s' 'absent' | sha256sum | awk '{print $1; exit}')
      printf 'corpus/absent-fixture.md 1 %s\n' "$sha" >> "$repo/.ufo/waves/round-40/declared-blocks.txt" ;;
  esac
  mkdir -p -- "$repo/.ufo/waves/round-40/final-gates"
  printf 'fixture\n' > "$repo/.ufo/waves/round-40/final-gates/all-gates.txt"
  fixture_commit "$repo" "h9 fixture $mode"
}

# h10_fixture REPO MODE — MODE=green|density|deletion|rmpath
h10_fixture() { # REPO MODE
  local repo=$1 mode=$2
  hist_reset "$repo" || return 1
  printf '\n[r40 fixture] SKILL append only.\n' >> "$repo/SKILL.md"
  printf '\n[r40 fixture] PROVINCE append only.\n\n' >> "$repo/PROVINCE.md"
  case $mode in
    density) printf '\n# fixture mutation\n' >> "$repo/corpus/instruments/density.py" ;;
    deletion)
      awk 'NR == 7 { next } { print }' "$repo/SKILL.md" > "$repo/.ufo-tmp" \
        && mv -- "$repo/.ufo-tmp" "$repo/SKILL.md" ;;
    rmpath) git -C "$repo" rm -q -- corpus/instruments/anchorcheck.py ;;
  esac
  fixture_commit "$repo" "h10 fixture $mode"
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

# selftest_prepare — the payload file and the receipt sources H5/H7 read, built
# from the export under test. Run once before the cases.
selftest_prepare() {
  local id p
  : > "$PAYFILE"
  for id in "${EIGHT[@]}"; do
    p=$(run_check "$id" "$EXPORT" "$REF_RESOLVED")
    printf '%s\t%s\t1\n' "$id" "$p" >> "$PAYFILE"
  done
  if [ -f "$EXPORT/$RECEIPT" ]; then
    H5_SOURCE=$EXPORT/$RECEIPT
  else
    H5_SOURCE=$WORK/h5-source.txt
    assemble_transcript '' > "$H5_SOURCE"
  fi
  p=$(run_check H5 "$EXPORT" "$REF_RESOLVED")
  printf 'H5\t%s\t1\n' "$p" >> "$PAYFILE"
  H7_TARGET=$EXPORT/$RECEIPT
}

# --- selftest cases -------------------------------------------------------

selftest_case_H1() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos H1 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/H1-nosuite; h1_tree "$d" nosuite
  st_neg H1 suite-absent "$d" "$REF_RESOLVED" 'suite=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H1-norow; h1_tree "$d" norow
  st_neg H1 registry-row-absent "$d" "$REF_RESOLVED" 'registry=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H1-baddigest; h1_tree "$d" baddigest
  st_neg H1 export-bytes-differ "$d" "$REF_RESOLVED" 'digest=0' && ok=$((ok + 1))
  st_verdict H1 "$bad" "$ok" "$n"
}

selftest_case_H2() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos H2 "$EXPORT" "$REF_RESOLVED" || bad=1
  d=$MUT/H2-green; h2_tree "$d" green
  st_control H2 four-records-green "$d" "$REF_RESOLVED"
  n=$((n + 1)); d=$MUT/H2-nolesson; h2_tree "$d" nolesson
  st_neg H2 lesson-correction-absent "$d" "$REF_RESOLVED" 'missing=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H2-badvalues; h2_tree "$d" badvalues
  st_neg H2 values-not-named "$d" "$REF_RESOLVED" 'missing=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H2-openfence; h2_tree "$d" openfence
  st_neg H2 fence-open-at-eof "$d" "$REF_RESOLVED" 'fences=open' && ok=$((ok + 1))
  st_verdict H2 "$bad" "$ok" "$n"
}

selftest_case_H3() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos H3 "$EXPORT" "$REF_RESOLVED" || bad=1
  d=$MUT/H3-green; h3_tree "$d" green
  st_control H3 criterion-row-green "$d" "$REF_RESOLVED"
  n=$((n + 1)); d=$MUT/H3-nomention; h3_tree "$d" nomention
  st_neg H3 row-absent-at-all "$d" "$REF_RESOLVED" 'mentions=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H3-prose; h3_tree "$d" prose
  st_neg H3 mention-without-criterion-row "$d" "$REF_RESOLVED" 'rows=0' && ok=$((ok + 1))
  st_verdict H3 "$bad" "$ok" "$n"
}

selftest_case_H4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos H4 "$EXPORT" "$REF_RESOLVED" || bad=1
  d=$MUT/H4-green; h4_tree "$d" green
  st_control H4 three-located-quotes "$d" "$REF_RESOLVED"
  n=$((n + 1)); d=$MUT/H4-nos059; h4_tree "$d" nos059
  st_neg H4 s059-block-absent "$d" "$REF_RESOLVED" 's059=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H4-oversize; h4_tree "$d" oversize
  st_neg H4 quote-over-25-words "$d" "$REF_RESOLVED" 'oversize=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/H4-nourl; h4_tree "$d" nourl
  st_neg H4 url-absent "$d" "$REF_RESOLVED" 's056=0' && ok=$((ok + 1))
  st_verdict H4 "$bad" "$ok" "$n"
}

selftest_case_H5() {
  local bad=0 ok=0 n=0 f saved
  CASES=$((CASES + 1))
  saved=$H5_SOURCE
  st_pos H5 "$EXPORT" "$REF_RESOLVED" || bad=1
  f=$(h5_fixture "$MUT/H5-green" green)
  H5_SOURCE=$f
  st_control H5 canonical-source-green "$EXPORT" "$REF_RESOLVED"
  n=$((n + 1)); f=$(h5_fixture "$MUT/H5-forged" forged)
  H5_SOURCE=$f
  st_neg H5 recorded-payload-contradicts-export "$EXPORT" "$REF_RESOLVED" 'control=7/8' \
    && ok=$((ok + 1))
  n=$((n + 1)); f=$(h5_fixture "$MUT/H5-future" future)
  H5_SOURCE=$f
  st_neg H5 source-future-dated "$EXPORT" "$REF_RESOLVED" 'utc=0' && ok=$((ok + 1))
  H5_SOURCE=$saved
  st_verdict H5 "$bad" "$ok" "$n"
}

selftest_case_H6() {
  local bad=0 ok=0 n=0 root save_root save_work out rc
  CASES=$((CASES + 1))
  save_root=$SCRATCH_ROOT
  save_work=$WORK
  # control: the passed --work dir under a family entry never reds the run
  root=$MUT/H6-control; mut_reset "$root"; mkdir -p -- "$root/kasegi-r40-gold/work"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r40-gold/work
  out=$(run_check H6 "$EXPORT" "$REF_RESOLVED"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=H6 control=own-work-dir accepted=1 payload=%s\n' "$out"
  else
    printf 'selftest detail=H6 control=own-work-dir accepted=0 rc=%s payload=%s\n' "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
  # control: the same family entry as a SIBLING of the one holding --work is a
  # leftover even when empty, so the fixture below proves the count discriminates
  root=$MUT/H6-empty; mut_reset "$root"
  mkdir -p -- "$root/kasegi-r39" "$root/kasegi-r40-gold/work"
  SCRATCH_ROOT=$root; WORK=$root/kasegi-r40-gold/work
  n=$((n + 1))
  st_neg H6 empty-sibling-family-entry "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  root=$MUT/H6-r39; mut_reset "$root"
  mkdir -p -- "$root/kasegi-r39-stray/seat" "$root/clean"
  printf 'x\n' > "$root/kasegi-r39-stray/seat/leftover.txt"
  SCRATCH_ROOT=$root; WORK=$root/clean
  n=$((n + 1))
  st_neg H6 r39-sibling-family "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  root=$MUT/H6-r40; mut_reset "$root"
  mkdir -p -- "$root/kasegi-r40-stray" "$root/kasegi-r40-gold/work"
  SCRATCH_ROOT=$root; WORK=$root/kasegi-r40-gold/work
  n=$((n + 1))
  st_neg H6 r40-sibling-family "$EXPORT" "$REF_RESOLVED" 'strays=1' && ok=$((ok + 1))
  root=$MUT/H6-unreadable; mut_reset "$root"; mkdir -p -- "$root/kasegi-r40-x"
  chmod 000 -- "$root"
  SCRATCH_ROOT=$root; WORK=$save_work
  n=$((n + 1))
  st_neg H6 unreadable-scratch-root "$EXPORT" "$REF_RESOLVED" 'read=fail' && ok=$((ok + 1))
  chmod 700 -- "$root"
  SCRATCH_ROOT=$save_root; WORK=$save_work
  st_verdict H6 "$bad" "$ok" "$n"
}

selftest_case_H7() {
  local bad=0 ok=0 n=0 f saved
  CASES=$((CASES + 1))
  saved=$H7_TARGET
  st_pos H7 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-absent" absent)
  H7_TARGET=$f
  st_neg H7 receipt-absent "$EXPORT" "$REF_RESOLVED" 'receipt=0' && ok=$((ok + 1))
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-future" future)
  H7_TARGET=$f
  st_neg H7 future-dated-run-utc "$EXPORT" "$REF_RESOLVED" 'not-future=0' && ok=$((ok + 1))
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-ancestor" ancestor)
  H7_TARGET=$f
  st_neg H7 export-ref-not-ancestor "$EXPORT" "$REF_RESOLVED" 'ancestor=0' && ok=$((ok + 1))
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-digest" digest)
  H7_TARGET=$f
  st_neg H7 suite-digest-mismatch "$EXPORT" "$REF_RESOLVED" 'digest=0' && ok=$((ok + 1))
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-extra" extraline)
  H7_TARGET=$f
  st_neg H7 extra-body-line "$EXPORT" "$REF_RESOLVED" 'body-lines=12' && ok=$((ok + 1))
  n=$((n + 1)); f=$(h7_fixture "$MUT/H7-h7line" h7line)
  H7_TARGET=$f
  st_neg H7 h7-line-tampered "$EXPORT" "$REF_RESOLVED" 'h7-line=0' && ok=$((ok + 1))
  H7_TARGET=$saved
  st_verdict H7 "$bad" "$ok" "$n"
}

selftest_case_H8() {
  local bad=0 ok=0 n=0 save_b save_r
  CASES=$((CASES + 1))
  save_b=${R40_NEG_BASE:-}
  save_r=${R40_NEG_R39:-}
  st_pos H8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); R40_NEG_BASE=/nonexistent-ref-for-fixture
  st_neg H8 base-ref-unresolvable "$EXPORT" "$REF_RESOLVED" 'base-exit=2' && ok=$((ok + 1))
  n=$((n + 1)); R40_NEG_BASE=$save_b; R40_NEG_R39=/nonexistent-ref-for-fixture
  st_neg H8 r39-ref-unresolvable "$EXPORT" "$REF_RESOLVED" 'r39-exit=2' && ok=$((ok + 1))
  if [ -n "$save_b" ]; then R40_NEG_BASE=$save_b; else unset R40_NEG_BASE; fi
  if [ -n "$save_r" ]; then R40_NEG_R39=$save_r; else unset R40_NEG_R39; fi
  st_verdict H8 "$bad" "$ok" "$n"
}

selftest_case_H9() {
  local bad=0 ok=0 n=0 repo c saved
  CASES=$((CASES + 1))
  st_pos H9 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$(hist_repo_ready "$MUT/hrepo") || {
    printf 'selftest detail=H9 fixture=repo-init-failed\n'
    st_verdict H9 1 "$ok" 1
    return
  }
  saved=$LANE
  LANE=$repo
  c=$(h9_fixture "$repo" green)
  [ -n "$c" ] && st_control H9 declared-whole-tail-green "$repo" "$c"
  n=$((n + 1)); c=$(h9_fixture "$repo" short)
  [ -n "$c" ] && st_neg H9 declared-short-of-added "$repo" "$c" 'valid=0' && ok=$((ok + 1))
  n=$((n + 1)); c=$(h9_fixture "$repo" sha)
  [ -n "$c" ] && st_neg H9 tail-sha-mismatch "$repo" "$c" 'valid=0' && ok=$((ok + 1))
  n=$((n + 1)); c=$(h9_fixture "$repo" del)
  [ -n "$c" ] && st_neg H9 declared-path-with-deletions "$repo" "$c" 'pure=0' && ok=$((ok + 1))
  n=$((n + 1)); c=$(h9_fixture "$repo" escape)
  [ -n "$c" ] && st_neg H9 declaration-path-escape "$repo" "$c" 'paths=0' && ok=$((ok + 1))
  n=$((n + 1)); c=$(h9_fixture "$repo" missing)
  [ -n "$c" ] && st_neg H9 declaration-absent-path "$repo" "$c" 'paths=0' && ok=$((ok + 1))
  LANE=$saved
  st_verdict H9 "$bad" "$ok" "$n"
}

selftest_case_H10() {
  local bad=0 ok=0 n=0 repo c saved
  CASES=$((CASES + 1))
  st_pos H10 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$(hist_repo_ready "$MUT/hrepo") || {
    printf 'selftest detail=H10 fixture=repo-init-failed\n'
    st_verdict H10 1 "$ok" 1
    return
  }
  saved=$LANE
  LANE=$repo
  c=$(h10_fixture "$repo" green)
  [ -n "$c" ] && st_control H10 append-only-green "$repo" "$c"
  n=$((n + 1)); c=$(h10_fixture "$repo" density)
  [ -n "$c" ] && st_neg H10 density-instrument-changed "$repo" "$c" 'density=0' \
    && ok=$((ok + 1))
  n=$((n + 1)); c=$(h10_fixture "$repo" deletion)
  [ -n "$c" ] && st_neg H10 skill-line-deleted "$repo" "$c" 'skill-del=1' && ok=$((ok + 1))
  n=$((n + 1)); c=$(h10_fixture "$repo" rmpath)
  [ -n "$c" ] && st_neg H10 tracked-path-deleted "$repo" "$c" 'deleted=1' && ok=$((ok + 1))
  LANE=$saved
  st_verdict H10 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id line n ok det rej dup
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f"); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f"); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=10 failures=0$' "$f"); summary=${summary:-0}
  [ "$cases" -eq 10 ] && [ "$verdicts" -eq 10 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=H<i> mutant=`
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
  selftest_prepare
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

  printf 'selftest cases=10 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    for i in $(seq 1 10); do
      printf 'selftest case=H%s positive=pass mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=10 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  # the detail-free all-pass forgery: ten case lines claiming pass with
  # mutants=0/0 and no fixture detail behind them
  {
    for i in $(seq 1 10); do
      printf 'selftest case=H%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=10 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  # the 9-case forgery: every line well-formed, one check never ran
  {
    for i in $(seq 1 9); do
      printf 'selftest case=H%s positive=pass mutants=1/1 verdict=pass\n' "$i"
      printf 'selftest detail=H%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=10 failures=0\n'
  } > "$WORK/forge-9-cases.txt"
  if judge_selftest_report "$WORK/forge-9-cases.txt"; then
    printf 'selftest judge=forged-9-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-9-cases rejected=1\n'
  fi

  # the field-free forgery: positive=pass and matching details, but no
  # `verdict=` field at all — an ungraded case line must not satisfy a case
  {
    for i in $(seq 1 10); do
      printf 'selftest case=H%s positive=pass mutants=1/1\n' "$i"
      printf 'selftest detail=H%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=10 failures=0\n'
  } > "$WORK/forge-no-verdict.txt"
  if judge_selftest_report "$WORK/forge-no-verdict.txt"; then
    printf 'selftest judge=forged-no-verdict rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-no-verdict rejected=1\n'
  fi

  if [ "$CASES" -ne 10 ]; then
    printf 'selftest problem=cases=%s expected=10\n' "$CASES"
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
        printf 'r40-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r40-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
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
