#!/usr/bin/env bash
# r36-closure.sh — round-36 closure counter for claim C1 (depth:verifiability).
#
# Nine checks E1-E9, one per routed defect of the round-35 verifier spot-check
# plus the two standing closure-order defects. Each check exits 0 when its defect
# is CLOSED and non-zero while it is still OPEN, so the suite is a fail-closed
# gate over the bytes of a named lane head.
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -x -C <scratch>/export
# and every check reads its bytes only under that export root. The sole live
# reads are E9's quiescence limbs (worktree status, HEAD, scratch root) and E4's
# frozen `git ls-files` index limb, which are live by definition and cannot be
# answered from an export. A plain run (no --export-ref, no --selftest) refuses
# with exit 2, because a suite that reads the working tree can be turned green by
# edits that were never committed.
# The only ref-scoped git reads that cannot be answered from the export bytes —
# E1's commit existence/ancestry, E4's tracking lints, E9's quiescence — are
# read-only git subcommands against the lane repo (archive, rev-parse, cat-file
# -e, merge-base --is-ancestor, ls-tree, ls-files, status --porcelain; the status
# read runs with --no-optional-locks so it does not take .git/index.lock even
# transiently). Nothing is written under the lane; the only writes are the
# extraction and the selftest fixtures
# under --work (or a mktemp dir honouring TMPDIR), both removed on exit.
# --work must lie outside the lane; its `export/` and `mut/` subdirectories are
# cleared before use, so a reused work dir can never satisfy a check with stale
# bytes.
#
# Usage:
#   bash corpus/instruments/r36-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run E1-E9 against the export. Prints one
#       `E<n> payload=<...> closed=0|1` line per check and a final
#       `closed=K/9 exit=0|1`; exit 0 only for K=9, exit 1 otherwise.
#   bash corpus/instruments/r36-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check one or two scratch fixtures that reopen
#       exactly one clause of that check must be REJECTED, and the rejection
#       payload must name the reopened limb — so a fixture proves the check
#       discriminates rather than that it can be satisfied by a summary.
#       Prints one `selftest case=E<i> positive=... mutants=<ok>/<n> verdict=...`
#       line per check, the `selftest detail=` lines behind them, the
#       `selftest judge=` lines (own report accepted, three forged reports
#       rejected) and `selftest cases=9 failures=0`; exit 0 only when all nine
#       cases were executed, every positive passed and every mutant was rejected.
#   bash corpus/instruments/r36-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# The nine checks:
#   E1  Structural placeholder/hash binding. SCORECARD.md in the export carries
#       0 `filled by the L1` lines and 0 `<LANE_HASH>` marker lines, AND every
#       40-hex value on a `Final lane commit:` line (that line or the four lines
#       after it) exists as a commit in the lane repo and is an ancestor of the
#       exported ref. A closure that names a hash nobody can resolve, or names a
#       commit on a side branch, is not a binding.
#   E2  SCORECARD.md carries the round-34 depth:density erratum: the erratum
#       anchor `round-34 depth:density row` >= 1 AND the corrected mean `201.2`
#       >= 1 (the round-35 base carries 0 of each). The anchor limb is what keeps
#       a stray prose `201.2` elsewhere in SCORECARD.md from standing in for the
#       erratum row.
#   E3  SKILL.md registers BOTH closure instruments as registry ROWS by exact
#       basename at the Gates & probes registry home: the first table column
#       reads `r35-defect-closure.sh` (optional backticks) AND `r36-closure.sh`,
#       inside a `## …Gates & probes registry…` section (closed by the next
#       `## ` heading). A prose sentence that merely names them, or a row-shaped
#       line outside such a section, does not close this check — the round-35
#       spot-check's routed defect was a clause satisfied by mention or negation.
#   E4  `.ufo/waves/round-35/wave1-results.json` is tracked at the exported ref
#       (`ls-tree -r --name-only <ref> -- <path>` = 1 line) AND in the lane index
#       (the frozen `git ls-files` limb = 1 line) AND the provenance note
#       `<path>.provenance.md` exists in the export beside it.
#   E5  `.ufo/waves/round-35/claims-erratum-d5.md` exists in the export.
#   E6  The round-34 wave-1 integration receipt carries the appended
#       `Correction (round 35)` note. The receipt path is derived from the
#       export's own `ls-tree` listing (one candidate, fixture copies under
#       corpus/instruments/ excluded), not assumed.
#   E7  corpus/QUALITY.md carries both appended supersession ROWS: a table row
#       whose third column begins `supersedes R22` (>= 1) and the same for
#       `supersedes R23` (>= 1). A prose sentence quoting the row text does not
#       close the check.
#   E8  The round-36 lesson records the E8 correction: `M36` >= 1 rows in
#       corpus/lessons/round-36.md AND the corrected line is NAMED there
#       (`source-recheck` >= 1, so a lesson that never says what it corrected
#       fails) AND the false-evidence line is gone from
#       corpus/lessons/round-35.md (`source-recheck exit 0 on committed bytes`
#       == 0, and that lesson file must EXIST — an absent file does not read as
#       "stale line absent"). A lesson that keeps the stale evidence line fails
#       even when the new mistake rows are present.
#   E9  Quiescence. Four limbs: (a) the status repo IS the lane root
#       (`rev-parse --show-toplevel` equals its physical path — an export path or
#       a subdirectory inside another repository would otherwise inherit that
#       repo's cleanliness); (b) the lane worktree is clean
#       (`git status --porcelain` prints nothing); (c) the round-36 scratch root
#       has no leftover seat directories (`find <scratch-root> -mindepth 1
#       -maxdepth 1 -type d` empty, the suite's own --work dir excluded by
#       absolute path); (d) the exported ref IS the lane's standing HEAD
#       (`rev-parse HEAD`), so an export of a stale commit cannot read quiescent.
#       The payload also reports `scratch-root=present|absent`, so a typo'd
#       --scratch-root is visible rather than silently reading zero seats.
#       Limb (d) is the staleness guard: without it (measured by removing it on a
#       quiescent scratch root) the r35 base export reads 1/9 and the r35 judged
#       head 5/9, not the frozen 0/9 and the required <9/9.
#
# Documented limits (measured, not hidden):
#   - E1 matches the two placeholder spellings the round-35 spot-check and this
#     round's kill rule name literally. Prose placeholders ("the L1 fills this
#     line in") are not matched; the round-35 instrument records the same
#     residue and it is still open as a checker-brittleness item.
#   - E8 binds "correction recorded" through the `M36` mistake rows, the named
#     corrected instrument (`source-recheck`) and the removal of the stale line.
#     It does not require the lesson to quote the stale sentence verbatim,
#     because the correction's wording is the L1's.
#   - E9's limbs are live by construction (worktree, scratch root, HEAD). A
#     historical export can only be evaluated as "not quiescent now"; that is
#     the intended reading and the reason the negative controls are 0/9 and
#     <9/9 rather than "the old tree was clean when it was written".
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r36
CHECK_IDS=(E1 E2 E3 E4 E5 E6 E7 E8 E9)

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

# suite_digest — sha256 of the bytes actually executing, printed in the report so
# a reader can bind a `closed=9/9` line to the instrument that produced it.
suite_digest() {
  local s=${BASH_SOURCE[0]:-}
  if [ -n "$s" ] && [ -r "$s" ]; then
    sha256sum -- "$s" 2>/dev/null | awk '{print $1; exit}'
  else
    printf 'unreadable'
  fi
}

usage() {
  # the header block only: line 2 through the last comment line before the
  # option-less `set` line, so the help cannot drift from the docs.
  sed -n '2,/^set -uo pipefail$/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'
}

die() { # MESSAGE...
  printf 'r36-closure: %s\n' "$*" >&2
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
        printf 'r36-closure: unknown argument: %s\n' "$1" >&2
        usage >&2
        exit 2 ;;
    esac
  done
}

cleanup() {
  [ -n "${EXPORT:-}" ] && rm -rf -- "$EXPORT"
  [ -n "${MUT:-}" ] && rm -rf -- "$MUT"
  if [ "${WORK_AUTO:-0}" = 1 ] && [ -n "${WORK:-}" ]; then rm -rf -- "$WORK"; fi
}

make_work() {
  if [ -n "$WORK_ARG" ]; then
    # Guard BEFORE creating anything: a refused --work must leave no trace.
    local norm
    norm=$(realpath -m -- "$WORK_ARG" 2>/dev/null) \
      || die "cannot resolve work dir: $WORK_ARG"
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
    WORK=$(mktemp -d -t r36-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  # Clear both owned subdirectories: a reused --work must never let a stale
  # export satisfy a check (e.g. an old claims-erratum-d5.md under export/).
  rm -rf -- "$EXPORT" "$MUT"
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

# e1_final_hashes FILE — the 40-hex tokens on a `[Ff]inal lane commit` line (or
# in the four lines after it) inside the LAST `Round[- ]36` heading block. Scoping
# to the round-36 block is what stops the historical round-33/34/35 lines from
# satisfying the check: a closure section that carries no bound line is red.
# Splitting on non-hex runs keeps a 64-hex digest from being read as 40-hex.
e1_final_hashes() {
  awk '
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i <= NR; i++)
        if (line[i] ~ /^#{1,4} .*Round[- ]?36([^0-9]|$)/) start = i
      if (start == 0) exit
      for (i = start; i <= NR; i++) {
        if (line[i] ~ /[Ff]inal lane commit/) {
          for (j = i; j <= i + 4 && j <= NR; j++) {
            n = split(line[j], f, /[^0-9a-f]+/)
            for (k = 1; k <= n; k++) if (length(f[k]) == 40) print f[k]
          }
        }
      }
    }
  ' "$1" | sort -u
}

# e1_has_round36 FILE — 1 when SCORECARD.md carries a Round[- ]36 heading.
e1_has_round36() {
  awk '/^#{1,4} .*Round[- ]?36([^0-9]|$)/ { found = 1 } END { print found + 0 }' "$1"
}

# e3_registry_rows FILE BASENAME — count table rows whose first cell is exactly
# BASENAME (optional backticks), counting only inside a Gates & probes registry
# section (`## …Gates & probes registry…`, closed by the next `## ` heading).
# Section scoping is what stops a quoted row or a prose mention elsewhere in
# SKILL.md from satisfying the registry check.
e3_registry_rows() {
  awk -v name="$2" '
    BEGIN { b = name; gsub(/\./, "\\.", b); pat = "^\\|[[:space:]]*`?" b "`?[[:space:]]*\\|" }
    /^## / { inreg = ($0 ~ /Gates & probes registry/); next }
    inreg && $0 ~ pat { n++ }
    END { print n + 0 }
  ' "$1"
}

count_lines() { # reads stdin
  grep -c . 2>/dev/null || true
}

# ---------------------------------------------------------------------------
# checks — every one cd's into the export root and reads relative paths there
# ---------------------------------------------------------------------------

check_e1() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    [ -f SCORECARD.md ] || { printf 'scorecard-missing'; exit 1; }
    local ph lh section total=0 bound=0 h
    # Both placeholder literals are assembled so this instrument does not itself
    # contain the tokens it hunts for.
    ph=$(grep -cF -- "filled by the $(printf 'L1')" SCORECARD.md 2>/dev/null); ph=${ph:-0}
    lh=$(grep -cF -- "<LANE$(printf '_HASH')>" SCORECARD.md 2>/dev/null); lh=${lh:-0}
    section=$(e1_has_round36 SCORECARD.md); section=${section:-0}
    while IFS= read -r h; do
      [ -n "$h" ] || continue
      total=$((total + 1))
      if git -C "$LANE" cat-file -e "${h}^{commit}" 2>/dev/null \
         && git -C "$LANE" merge-base --is-ancestor "$h" "$ref" 2>/dev/null; then
        bound=$((bound + 1))
      fi
    done < <(e1_final_hashes SCORECARD.md)
    printf 'placeholders=%s,lane-hash-markers=%s,round36-section=%s,round36-final-lane-commits=%s,bound=%s' \
      "$ph" "$lh" "$section" "$total" "$bound"
    [ "$ph" -eq 0 ] && [ "$lh" -eq 0 ] && [ "$section" -eq 1 ] \
      && [ "$total" -ge 1 ] && [ "$bound" -eq "$total" ] && exit 0
    exit 1
  )
}

check_e2() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local marker row mean
    # The erratum statement, the corrected depth:density row, and the corrected
    # mean. Requiring the marker and the row stops a prose sentence that quotes
    # the phrase or the number from standing in for the erratum.
    marker=$(grep -cF -- 'Erratum (round 35)' SCORECARD.md 2>/dev/null); marker=${marker:-0}
    row=$(grep -cE -- '^\|[[:space:]]*depth:density[[:space:]]*\|[[:space:]]*9[[:space:]]*\|[[:space:]]*mean \*\*201\.2\*\*' SCORECARD.md 2>/dev/null); row=${row:-0}
    mean=$(grep -cE -- '201\.2' SCORECARD.md 2>/dev/null); mean=${mean:-0}
    printf 'erratum-marker=%s,erratum-row=%s,erratum-mean=%s' "$marker" "$row" "$mean"
    [ "$marker" -ge 1 ] && [ "$row" -ge 1 ] && [ "$mean" -ge 1 ] && exit 0
    exit 1
  )
}

check_e3() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local a b
    # Registry ROWS inside a Gates & probes registry section, not mentions: the
    # exact basename in the first table column (optional backticks). Round 35's
    # routed defect 3 was precisely "the clause greps are satisfied by a mention
    # or a negation", and the round-35 row named `r-defect-closure.sh`, the
    # round-33/34 instrument, which is why the exact basename is its own check.
    a=$(e3_registry_rows SKILL.md 'r35-defect-closure.sh')
    b=$(e3_registry_rows SKILL.md 'r36-closure.sh')
    printf 'registry-r35-defect-closure=%s,registry-r36-closure=%s' "$a" "$b"
    [ "$a" -ge 1 ] && [ "$b" -ge 1 ] && exit 0
    exit 1
  )
}

check_e4() { # TREE REF
  local tree=$1 ref=$2 p=.ufo/waves/round-35/wave1-results.json
  local t_ref t_idx note=0
  t_ref=$(git -C "$LANE" ls-tree -r --name-only "$ref" -- "$p" 2>/dev/null | count_lines)
  t_idx=$(git -C "$LANE" ls-files -- "$p" 2>/dev/null | count_lines)
  t_ref=${t_ref:-0}; t_idx=${t_idx:-0}
  if ( cd "$tree" && [ -f "$p.provenance.md" ] && [ -s "$p.provenance.md" ] ) 2>/dev/null; then note=1; fi
  printf 'tracked-ref=%s,tracked-index=%s,provenance-note=%s' "$t_ref" "$t_idx" "$note"
  [ "$t_ref" -eq 1 ] && [ "$t_idx" -eq 1 ] && [ "$note" -eq 1 ] && return 0
  return 1
}

check_e5() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-35/claims-erratum-d5.md ok=0
    if [ -f "$p" ] && [ -s "$p" ]; then ok=1; fi
    printf 'claims-erratum-d5=%s' "$ok"
    [ "$ok" -eq 1 ] && exit 0
    exit 1
  )
}

check_e6() { # TREE REF
  local tree=$1 ref=$2
  local cand n path cor
  cand=$(git -C "$LANE" ls-tree -r --name-only "$ref" 2>/dev/null \
    | grep -E '(^|/)\.ufo/waves/round-34/wave1/L1Integration\.md$' \
    | grep -v '^corpus/instruments/')
  n=$(printf '%s\n' "$cand" | count_lines); n=${n:-0}
  if [ "$n" -ne 1 ]; then
    printf 'path-candidates=%s,correction-round35=0' "$n"
    return 1
  fi
  path=$cand
  cor=$( ( cd "$tree" && grep -cF -- 'Correction (round 35)' "$path" 2>/dev/null ) || true )
  cor=${cor:-0}
  printf 'path=%s,correction-round35=%s' "$path" "$cor"
  [ "$cor" -ge 1 ] && return 0
  return 1
}

check_e7() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local r22 r23
    # Rows, not prose: the third column of a QUALITY.md row begins with the
    # supersession statement. A sentence that mentions the row text must not
    # close the check (round-35 routed defect 3/D7 class).
    r22=$(grep -cE -- '^\|[[:space:]]*R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R22($|[^0-9])' corpus/QUALITY.md 2>/dev/null); r22=${r22:-0}
    r23=$(grep -cE -- '^\|[[:space:]]*R[0-9]+[[:space:]]*\|[^|]*\|[[:space:]]*supersedes R23($|[^0-9])' corpus/QUALITY.md 2>/dev/null); r23=${r23:-0}
    printf 'supersedes-r22=%s,supersedes-r23=%s' "$r22" "$r23"
    [ "$r22" -ge 1 ] && [ "$r23" -ge 1 ] && exit 0
    exit 1
  )
}

check_e8() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local m36 names stale=0 lesson35=0
    m36=$(grep -cF -- 'M36' corpus/lessons/round-36.md 2>/dev/null); m36=${m36:-0}
    # The correction must NAME the line it corrects: the round-36 lesson has to
    # mention the instrument whose output was the false evidence line. "Rows
    # exist" alone would close the check while the lesson never records what it
    # corrected.
    names=$(grep -cF -- 'source-recheck' corpus/lessons/round-36.md 2>/dev/null); names=${names:-0}
    # The absence limb is only meaningful when the lesson it applies to exists;
    # a missing round-35 lesson must not read as "stale line absent".
    if [ -f corpus/lessons/round-35.md ]; then
      lesson35=1
      stale=$(grep -cF -- 'source-recheck exit 0 on committed bytes' \
        corpus/lessons/round-35.md 2>/dev/null); stale=${stale:-0}
    fi
    printf 'm36-rows=%s,names-corrected-line=%s,stale-line=%s,round35-lesson=%s' \
      "$m36" "$names" "$stale" "$lesson35"
    [ "$m36" -ge 1 ] && [ "$names" -ge 1 ] && [ "$stale" -eq 0 ] \
      && [ "$lesson35" -eq 1 ] && exit 0
    exit 1
  )
}

check_e9() { # TREE REF [SCRATCH_ROOT [STATUS_REPO [EXPECTED_HEAD]]]
  local ref=$2
  local sroot=${3:-$SCRATCH_ROOT}
  local srepo=${4:-$LANE}
  local want=${5:-$ref}
  local porcelain left=0 head head_ok=0 root_ok=0 skip= d dp top root sroot_state=absent
  if ! git -C "$srepo" rev-parse --git-dir >/dev/null 2>&1; then
    printf 'status-repo=unreadable,scratch-seat-dirs=?,head-match=0,lane-root=0,scratch-root=?'
    return 1
  fi
  # The status repo must BE the lane root: an export path or a subdirectory of
  # some enclosing repository would otherwise report another tree's cleanliness.
  root=$( cd "$srepo" 2>/dev/null && pwd -P )
  top=$(git -C "$srepo" rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$top" ] && [ -n "$root" ] && [ "$top" = "$root" ]; then root_ok=1; fi
  # --no-optional-locks: plain `git status` takes and unlinks .git/index.lock,
  # a transient write under the lane. This suite must leave the lane untouched.
  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
  porcelain=${porcelain:-0}
  if [ -n "${WORK:-}" ]; then skip=$( cd "$WORK" 2>/dev/null && pwd -P ); fi
  if [ -d "$sroot" ]; then
    sroot_state=present
    while IFS= read -r d; do
      [ -n "$d" ] || continue
      dp=$( cd "$d" 2>/dev/null && pwd -P )
      if [ -n "$skip" ] && [ "$dp" = "$skip" ]; then continue; fi
      left=$((left + 1))
    done < <(find "$sroot" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
  fi
  head=$(git -C "$srepo" rev-parse --verify --quiet HEAD 2>/dev/null)
  if [ -n "$head" ] && [ "$head" = "$want" ]; then head_ok=1; fi
  printf 'status-dirty=%s,scratch-seat-dirs=%s,head-match=%s,lane-root=%s,scratch-root=%s' \
    "$porcelain" "$left" "$head_ok" "$root_ok" "$sroot_state"
  [ "$porcelain" -eq 0 ] && [ "$left" -eq 0 ] && [ "$head_ok" -eq 1 ] \
    && [ "$root_ok" -eq 1 ] && return 0
  return 1
}

run_check() { # ID TREE REF [EXTRA...]
  local id=$1; shift
  # one name derivation instead of a second registry beside CHECK_IDS
  "check_${id,,}" "$@"
}

# ---------------------------------------------------------------------------
# plain (export) run
# ---------------------------------------------------------------------------

run_suite_report() {
  local lines='' id out rc k=0 n=0 counted=0
  printf 'export-ref=%s mode=export lane=%s suite-sha256=%s\n' \
    "$REF_RESOLVED" "$LANE" "$(suite_digest)"
  if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
  if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
  for id in "${CHECK_IDS[@]}"; do
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
    if [ "$rc" -eq 0 ]; then
      k=$((k + 1))
      lines="${lines}${id} payload=${out} closed=1"$'\n'
    else
      lines="${lines}${id} payload=${out} closed=0"$'\n'
    fi
  done
  printf '%s' "$lines"
  n=$(printf '%s' "$lines" | grep -c '^E[1-9] payload=')
  if [ "$n" -ne 9 ]; then
    printf 'suite problem=self-report lines=%s expected=9\n' "$n"
    printf 'closed=0/9 exit=1\n'
    return 1
  fi
  counted=$(printf '%s' "$lines" | grep -c 'closed=1$')
  if [ "$counted" -ne "$k" ]; then
    printf 'suite problem=self-report closed=%s counted=%s\n' "$k" "$counted"
    printf 'closed=0/9 exit=1\n'
    return 1
  fi
  if [ "$k" -eq 9 ]; then
    printf 'closed=%s/9 exit=0\n' "$k"
    return 0
  fi
  printf 'closed=%s/9 exit=1\n' "$k"
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

st_pos() { # ID TREE REF
  local id=$1 out rc
  out=$(run_check "$id" "$2" "$3" 2>/dev/null); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s positive=pass payload=%s\n' "$id" "$out"
    return 0
  fi
  printf 'selftest detail=%s positive=fail rc=%s payload=%s\n' "$id" "$rc" "$out"
  return 1
}

st_neg() { # ID LABEL TREE REF NEEDLE [EXTRA...]
  local id=$1 label=$2 tree=$3 ref=$4 needle=$5; shift 5
  local out rc
  out=$(run_check "$id" "$tree" "$ref" "$@" 2>/dev/null); rc=$?
  if [ "$rc" -ne 0 ] && printf '%s' "$out" | grep -qF -- "$needle"; then
    printf 'selftest detail=%s mutant=%s rejected=1 limb=%s\n' "$id" "$label" "$needle"
    return 0
  fi
  printf 'selftest detail=%s mutant=%s rejected=0 rc=%s payload=%s\n' \
    "$id" "$label" "$rc" "$out"
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

selftest_case_E1() {
  local bad=0 ok=0 n=0 h d
  CASES=$((CASES + 1))
  st_pos E1 "$EXPORT" "$REF_RESOLVED" || bad=1
  h=$(e1_final_hashes "$EXPORT/SCORECARD.md" | head -n 1)
  [ -n "$h" ] || h=$REF_RESOLVED
  n=$((n + 1)); d=$MUT/E1-placeholder; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\nfilled by the %s\n' "$h" 'L1' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 placeholder "$d" "$REF_RESOLVED" 'placeholders=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-lanehash; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\n<%s>\n' "$h" 'LANE_HASH' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 lane-hash-marker "$d" "$REF_RESOLVED" 'lane-hash-markers=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-unbound; mut_reset "$d"
  printf '## Round 36\n\n**Final lane commit: `%s`**\n' \
    '0123456789abcdef0123456789abcdef01234567' | mut_put "$d" SCORECARD.md
  st_neg E1 unbound-hash "$d" "$REF_RESOLVED" 'bound=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-history; mut_reset "$d"
  printf '**Final lane commit: `%s`**\n' "$h" | mut_put "$d" SCORECARD.md
  st_neg E1 history-only "$d" "$REF_RESOLVED" 'round36-section=0' && ok=$((ok + 1))
  st_verdict E1 "$bad" "$ok" "$n"
}

selftest_case_E2() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E2 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E2; mut_reset "$d"
  printf '| depth:density | 9 | mean **201.7**, 25 blocks |\n' | mut_put "$d" SCORECARD.md
  st_neg E2 stale-mean "$d" "$REF_RESOLVED" 'erratum-mean=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E2-prose; mut_reset "$d"
  printf '## Round 36\n\nNote: the round-34 depth:density row was corrected last round; guard mean 201.2.\n' \
    | mut_put "$d" SCORECARD.md
  st_neg E2 prose-not-row "$d" "$REF_RESOLVED" 'erratum-row=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E2-marker; mut_reset "$d"
  printf 'Erratum (round 35): the depth:density mean is 201.2, corrected.\n' \
    | mut_put "$d" SCORECARD.md
  st_neg E2 marker-without-row "$d" "$REF_RESOLVED" 'erratum-row=0' && ok=$((ok + 1))
  st_verdict E2 "$bad" "$ok" "$n"
}

selftest_case_E3() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E3 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E3-r35only; mut_reset "$d"
  printf '| r35-defect-closure.sh | gate | bash ... |\n' | mut_put "$d" SKILL.md
  st_neg E3 r36-row-absent "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-r36only; mut_reset "$d"
  printf '| r36-closure.sh | gate | bash ... |\n' | mut_put "$d" SKILL.md
  st_neg E3 r35-row-absent "$d" "$REF_RESOLVED" 'registry-r35-defect-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-inexact; mut_reset "$d"
  printf '| r-defect-closure.sh | gate | bash ... |\n| r36-closure.sh | gate | bash ... |\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 inexact-basename "$d" "$REF_RESOLVED" 'registry-r35-defect-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-mention; mut_reset "$d"
  printf 'The gate later reads r36-closure.sh and r35-defect-closure.sh.\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 mention-not-row "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E3-outside; mut_reset "$d"
  printf '## Cited paths\n\n| r35-defect-closure.sh | gate | x |\n| r36-closure.sh | gate | x |\n' \
    | mut_put "$d" SKILL.md
  st_neg E3 rows-outside-registry "$d" "$REF_RESOLVED" 'registry-r36-closure=0' && ok=$((ok + 1))
  st_verdict E3 "$bad" "$ok" "$n"
}

selftest_case_E4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E4 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E4; mut_reset "$d"
  printf '{"wave": 1}\n' | mut_put "$d" .ufo/waves/round-35/wave1-results.json
  st_neg E4 provenance-absent "$d" "$REF_RESOLVED" 'provenance-note=0' && ok=$((ok + 1))
  st_verdict E4 "$bad" "$ok" "$n"
}

selftest_case_E5() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E5 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E5; mut_reset "$d"
  printf 'no erratum here\n' | mut_put "$d" README.md
  st_neg E5 erratum-absent "$d" "$REF_RESOLVED" 'claims-erratum-d5=0' && ok=$((ok + 1))
  st_verdict E5 "$bad" "$ok" "$n"
}

selftest_case_E6() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E6 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E6; mut_reset "$d"
  printf 'Correction (round 34) only.\n' \
    | mut_put "$d" .ufo/waves/round-34/wave1/L1Integration.md
  st_neg E6 correction-absent "$d" "$REF_RESOLVED" 'correction-round35=0' && ok=$((ok + 1))
  st_verdict E6 "$bad" "$ok" "$n"
}

selftest_case_E7() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E7 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E7; mut_reset "$d"
  printf '| R26 | ... | supersedes R22 - grounding fixed. |\n' | mut_put "$d" corpus/QUALITY.md
  st_neg E7 r23-row-absent "$d" "$REF_RESOLVED" 'supersedes-r23=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E7-prose; mut_reset "$d"
  printf 'Note: this row supersedes R22 and supersedes R23 in spirit.\n' \
    | mut_put "$d" corpus/QUALITY.md
  st_neg E7 prose-not-row "$d" "$REF_RESOLVED" 'supersedes-r22=0' && ok=$((ok + 1))
  st_verdict E7 "$bad" "$ok" "$n"
}

selftest_case_E8() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E8-nom36; mut_reset "$d"
  printf 'round 36 lesson without the mistake rows\n' | mut_put "$d" corpus/lessons/round-36.md
  printf 'clean lesson\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 m36-absent "$d" "$REF_RESOLVED" 'm36-rows=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-stale; mut_reset "$d"
  printf 'M36-1 source-recheck false line corrected here\n' | mut_put "$d" corpus/lessons/round-36.md
  printf 'gate says source-recheck exit 0 on committed bytes\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 stale-line-present "$d" "$REF_RESOLVED" 'stale-line=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-unnamed; mut_reset "$d"
  printf 'M36-1 correction recorded: the stale evidence line is withdrawn\n' \
    | mut_put "$d" corpus/lessons/round-36.md
  printf 'clean lesson\n' | mut_put "$d" corpus/lessons/round-35.md
  st_neg E8 corrected-line-unnamed "$d" "$REF_RESOLVED" 'names-corrected-line=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E8-nolesson35; mut_reset "$d"
  printf 'M36-1 source-recheck false line corrected here\n' | mut_put "$d" corpus/lessons/round-36.md
  st_neg E8 round35-lesson-absent "$d" "$REF_RESOLVED" 'round35-lesson=0' && ok=$((ok + 1))
  st_verdict E8 "$bad" "$ok" "$n"
}

selftest_case_E9() {
  local bad=0 ok=0 n=0 repo sroot top real head
  CASES=$((CASES + 1))
  st_pos E9 "$EXPORT" "$REF_RESOLVED" || bad=1
  repo=$MUT/e9repo; sroot=$MUT/e9scratch
  mut_reset "$repo"; mut_reset "$sroot"
  if ! git -C "$repo" init -q 2>/dev/null; then
    printf 'selftest detail=E9 fixture=repo-init-failed\n'; FAILS=$((FAILS + 1)); return
  fi
  top=$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)
  real=$( cd "$repo" && pwd -P )
  if [ "$top" != "$real" ]; then
    printf 'selftest detail=E9 fixture=toplevel-mismatch top=%s want=%s\n' "$top" "$real"
    FAILS=$((FAILS + 1)); return
  fi
  printf 'x\n' > "$repo/tracked.txt"
  git -C "$repo" add -- tracked.txt 2>/dev/null
  git -C "$repo" -c user.email=r36@local -c user.name=r36 commit -q -m fixture 2>/dev/null
  head=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  printf 'untracked\n' > "$repo/dirty.txt"
  n=$((n + 1))
  st_neg E9 dirty-worktree "$EXPORT" "$REF_RESOLVED" 'status-dirty=1' \
    "$sroot" "$repo" "$head" && ok=$((ok + 1))
  rm -f -- "$repo/dirty.txt"
  mkdir -p -- "$sroot/leftover-seat"
  n=$((n + 1))
  st_neg E9 leftover-seat-dir "$EXPORT" "$REF_RESOLVED" 'scratch-seat-dirs=1' \
    "$sroot" "$repo" "$head" && ok=$((ok + 1))
  n=$((n + 1))
  mut_reset "$MUT/e9scratch-empty"
  st_neg E9 stale-ref "$EXPORT" "$REF_RESOLVED" 'head-match=0' \
    "$MUT/e9scratch-empty" "$repo" "0000000000000000000000000000000000000000" \
    && ok=$((ok + 1))
  # a status repo that is a subdirectory of an enclosing repo: cleanliness and
  # HEAD would be inherited from the parent, so the lane-root limb must reject it
  mkdir -p -- "$repo/sub"
  n=$((n + 1))
  st_neg E9 enclosing-repo "$EXPORT" "$REF_RESOLVED" 'lane-root=0' \
    "$sroot" "$repo/sub" "$head" && ok=$((ok + 1))
  st_verdict E9 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id hit=0 line n ok det rej
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f" 2>/dev/null); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f" 2>/dev/null); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=9 failures=0$' "$f" 2>/dev/null); summary=${summary:-0}
  [ "$cases" -eq 9 ] && [ "$verdicts" -eq 9 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=E<i> mutant=`
  # lines of which ok name rejected=1. A fabricated case line carrying
  # `mutants=0/0` (no fixture ran) is rejected: n must be >= 1 and the detail
  # lines must exist. This is the round-35 report_ok rule.
  for id in "${CHECK_IDS[@]}"; do
    line=$(grep -m1 "^selftest case=${id} " "$f" 2>/dev/null)
    [ -n "$line" ] || return 1
    printf '%s' "$line" | grep -q "verdict=pass$" || return 1
    n=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
    ok=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
    [ -n "$n" ] && [ -n "$ok" ] && [ "$n" -ge 1 ] || return 1
    det=$(grep -c "^selftest detail=${id} mutant=" "$f" 2>/dev/null); det=${det:-0}
    rej=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$f" 2>/dev/null); rej=${rej:-0}
    [ "$det" -eq "$n" ] && [ "$rej" -eq "$ok" ] && [ "$ok" -eq "$n" ] || return 1
    hit=$((hit + 1))
  done
  [ "$hit" -eq 9 ]
}

run_selftest() {
  local f=$WORK/selftest-report.txt rc=0 id
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

  printf 'selftest cases=9 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    local i
    for i in 1 2 3 4 5 6 7 8 9; do
      printf 'selftest case=E%s positive=fail mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=9 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  # the detail-free all-pass forgery: nine case lines claiming pass with
  # mutants=0/0 and no fixture detail behind them (MutC1Fixtures' vacuous report)
  {
    local i
    for i in 1 2 3 4 5 6 7 8 9; do
      printf 'selftest case=E%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=9 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  if [ "$CASES" -ne 9 ]; then
    printf 'selftest problem=cases=%s expected=9\n' "$CASES"
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
  # cwd (a relative --lane used to resolve against the export tree inside E1's
  # subshell and read a false red).
  [ -d "$LANE" ] || die "lane is not a directory: $LANE"
  LANE=$( cd "$LANE" && pwd -P ) || die "cannot resolve lane: $LANE"
  case $MODE in
    run)
      if [ -z "$EXPORT_REF" ]; then
        printf 'r36-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r36-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
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
