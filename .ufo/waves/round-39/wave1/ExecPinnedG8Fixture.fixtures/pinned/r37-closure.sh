#!/usr/bin/env bash
# r37-closure.sh — round-37 closure counter for claim C1 (depth:verifiability).
#
# Fourteen checks E1-E14. E1-E9 carry the round-36 closure semantics (with E9
# rewritten fail-closed); E10-E14 close the six routed defects D1-D6 of the
# round-36 verifier spot-check (corpus/lessons/round-36-verifier-spotcheck.md §5)
# by reading the round-37 evidence bytes themselves. Each check exits 0 when its
# defect is CLOSED and non-zero while it is still OPEN, so the suite is a
# fail-closed gate over the bytes of a named lane head.
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
# transiently, and its exit status is READ — a failed status read is RED, never
# a default of zero dirty lines). Nothing is written under the lane; the only
# writes are the extraction and the selftest fixtures
# under --work (or a mktemp dir honouring TMPDIR), both removed on exit.
# --work must lie outside the lane; its `export/` and `mut/` subdirectories are
# cleared before use, so a reused work dir can never satisfy a check with stale
# bytes.
#
# Usage:
#   bash corpus/instruments/r37-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run E1-E14 against the export. Prints one
#       `E<n> payload=<...> closed=0|1` line per check and a final
#       `closed=K/14 exit=0|1`; exit 0 only for K=14, exit 1 otherwise.
#   bash corpus/instruments/r37-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check one or more scratch fixtures that reopen
#       exactly one clause of that check must be REJECTED, and the rejection
#       payload must name the reopened limb — so a fixture proves the check
#       discriminates rather than that it can be satisfied by a summary.
#       Prints one `selftest case=E<i> positive=... mutants=<ok>/<n> verdict=...`
#       line per check, the `selftest detail=` lines behind them, the
#       `selftest judge=` lines (own report accepted, six forged reports
#       rejected, including a 13-case and a duplicated-id report) and
#       `selftest cases=14 failures=0`; exit 0 only
#       when all fourteen cases were executed, every positive passed and every
#       mutant was rejected.
#   bash corpus/instruments/r37-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# The fourteen checks:
#   E1  Structural placeholder/hash binding. SCORECARD.md in the export carries
#       0 `filled by the L1` lines and 0 `<LANE_HASH>` marker lines, a
#       Round[- ]?37 heading exists, AND every 40-hex value on a
#       `Final lane commit:` line (that line or the four lines after it) inside
#       the LAST round-37 heading block exists as a commit in the lane repo and
#       is an ancestor of the exported ref. A closure that names a hash nobody
#       can resolve, or names a commit on a side branch, is not a binding.
#   E2  SCORECARD.md carries the round-34 depth:density erratum: the erratum
#       anchor `Erratum (round 35)` >= 1, the corrected depth:density row >= 1
#       AND the corrected mean `201.2` >= 1.
#   E3  SKILL.md registers BOTH closure instruments as registry ROWS by exact
#       basename at the Gates & probes registry home: the first table column
#       reads `r35-defect-closure.sh` (optional backticks) AND `r36-closure.sh`,
#       inside a `## …Gates & probes registry…` section (closed by the next
#       `## ` heading). A prose sentence that merely names them does not close
#       this check.
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
#       (`source-recheck` >= 1) AND the false-evidence line is gone from
#       corpus/lessons/round-35.md (`source-recheck exit 0 on committed bytes`
#       == 0, and that lesson file must EXIST).
#   E9  Quiescence, FAIL-CLOSED. Five limbs: (a) the status repo IS the lane root
#       (`rev-parse --show-toplevel` equals its physical path); (b) the lane
#       worktree is clean — the `git status --porcelain` read's EXIT STATUS is
#       read, and a failed read prints `status-read=failed` and closes the check
#       RED (no default of zero dirty lines, no stderr suppression on the read);
#       (c) the round-37 scratch root has no leftover seat directories
#       (`find <scratch-root> -mindepth 1 -maxdepth 1 -type d` empty, the suite's
#       own --work dir excluded by absolute path); (d) the exported ref IS the
#       lane's standing HEAD (`rev-parse HEAD`); (e) the payload reports
#       `scratch-root=present|absent` so a typo'd --scratch-root is visible.
#       Limb (d) is the staleness guard: an export of a stale commit cannot read
#       quiescent.
#   E10 (D1) The export's `.ufo/waves/round-37/final-gates/all-gates.txt`
#       (tracked at the exported ref) satisfies the `all-gates v1` receipt
#       contract: first line `all-gates v1`; exactly one `export-ref=<40 hex>`,
#       one `suite-sha256=<64 hex>` and one `run-utc=<strict UTC>` header line,
#       no other header line; `export-ref` resolves and is an
#       ANCESTOR-OR-EQUAL of the exported ref; `suite-sha256` equals the sha256
#       of the export's `corpus/instruments/r37-closure.sh` AND of the bytes
#       executing; the `== run ==` block carries exactly the fourteen
#       `E<n> payload=… closed=1` lines (no `closed=0`) and exactly one
#       `closed=14/14 exit=0`; the `== selftest ==` block carries the fourteen
#       `selftest case=E<n> ` lines with `positive=pass`, `verdict=pass`,
#       `mutants=<o>/<n>` with `n>=1` and `o==n`, exactly `n` matching
#       `selftest detail=E<n> mutant=… rejected=1` lines, and exactly one
#       `selftest cases=14 failures=0`; for each id except E10 the recorded
#       payload KEY SET equals the key set this run just produced (values may
#       differ — E9's limbs are live — the shape may not); and no receipt
#       placeholder/template token is present. E10 is therefore evaluated LAST:
#       the run collects the other thirteen lines first. Ancestry (not
#       equality) is what makes a receipt committed one commit before its
#       verification legitimate; the cross-run key set is what stops a
#       hand-written green block from satisfying the check.
#   E11 (D2) LOG.md's round-37 entry (the LAST `## …Round[- ]?37…` block) names
#       the correction of the round-36 C1 bullet's false
#       `corpus/instruments/r36-fixtures/` path: a `Correction (round 37)`
#       marker, the false path named, and a falsity statement (`absent` /
#       `never committed` / `does not exist` / `not present`).
#   E12 (D4) The round-37 SCORECARD section (the LAST `## …Round[- ]?37…` block,
#       closed by the next `## ` heading) and corpus/lessons/round-37.md both
#       label the r36 lane head `c20300df` as `anchor ancestor`, and the stale
#       label `Final lane commit: e666d902` appears NOWHERE inside the round-37
#       SCORECARD section.
#   E13 (D5) SKILL.md's Gates & probes registry carries a `r36-closure.sh` row
#       whose type cell is a SINGLE choice (`gate` or `probe`, never the literal
#       `gate|probe`) and whose verdict-map cell maps exit `2` to
#       `could-not-evaluate` (the plain-run refusal / harness-error verdict).
#   E14 (D6) Shape check on the export's corpus/instruments/r37-closure.sh: the
#       fail-open default literal (the `porcelain` parameter expansion with a
#       `:-0` default; spelled split here so this file never contains it)
#       appears 0 times; every line that performs a
#       `status --porcelain` read carries neither of the two classic
#       suppression spellings (stderr to /dev/null, or `|| true`); at
#       least one such read site exists and the fail-closed marker
#       `status-read=failed` is present.
#
# Documented limits (measured, not hidden):
#   - E1 matches the two placeholder spellings the round-36 spot-check and the
#     round-37 kill rule name literally. Prose placeholders ("the L1 fills this
#     line in") are not matched.
#   - E3/E13 read markdown TABLE cells only, inside a Gates & probes registry
#     section. E13 requires at least ONE conforming r36-closure.sh row: the
#     append-only house rule means the round-36 row's `gate|probe` cell cannot
#     be edited away, so the correction lands as an appended row.
#   - E8 binds "correction recorded" through the `M36` mistake rows, the named
#     corrected instrument (`source-recheck`) and the removal of the stale line.
#   - E9's limbs are live by construction (worktree, scratch root, HEAD). A
#     historical export can only be evaluated as "not quiescent now"; that is
#     the intended reading.
#   - E10 checks the receipt's shape, digest, ancestry and cross-run payload
#     shape. It cannot prove the recorded VALUES were green at the ref they
#     name (that ref is an ancestor, by R1's ancestor-or-equal rule); the truth
#     of the numbers is the live run at the verifying ref, and the digest rule
#     is what keeps that live run the same instrument. The cross-run limb
#     compares payload KEY SETS, not values, because E9's limbs are live by
#     design. A receipt cannot record the run that contains it, so the round-37
#     construction records a run made one commit earlier (the bootstrap is
#     disclosed in the receipt header and in the round-37 lesson).
#   - E12 counts the `c20300df` and `anchor ancestor` tokens inside the scoped
#     round-37 SCORECARD section and the round-37 lesson; it does not require
#     them on one physical line, because the house form may place the hash and
#     the label in adjacent table cells or wrap the line.
#   - E14 is a SHAPE check: it reads the committed bytes, not the runtime
#     behaviour. A status read that is fail-closed in code but spelled with a
#     suppression token is red by shape, which is the D6 requirement.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r37
CHECK_IDS=(E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13 E14)

# SELF — absolute physical path of the executing bytes. Resolved once at load
# time because E10 calls suite_digest() from inside a subshell that has cd'd
# into the export tree; a relative BASH_SOURCE would then name the wrong file.
SELF=${BASH_SOURCE[0]:-}
case $SELF in
  /*) ;;
  *)  if [ -n "$SELF" ] && [ -d "$(dirname -- "$SELF")" ]; then
        SELF=$( cd -- "$(dirname -- "$SELF")" 2>/dev/null && pwd -P )/$(basename -- "$SELF")
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

# suite_digest — sha256 of the bytes actually executing, printed in the report so
# a reader can bind a `closed=14/14` line (and the committed all-gates.txt) to
# the instrument that produced it.
suite_digest() {
  local s=${SELF:-}
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
  printf 'r37-closure: %s\n' "$*" >&2
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
        printf 'r37-closure: unknown argument: %s\n' "$1" >&2
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
    WORK=$(mktemp -d -t r37-closure.XXXXXXXX) || die 'cannot create a work dir'
    WORK_AUTO=1
  fi
  EXPORT=$WORK/export
  MUT=$WORK/mut
  # Clear both owned subdirectories: a reused --work must never let a stale
  # export satisfy a check (e.g. an old all-gates.txt under export/).
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
# in the four lines after it) inside the LAST `Round[- ]37` heading block.
# Scoping to the round-37 block is what stops the historical round-33/34/35/36
# lines from satisfying the check: a closure section that carries no bound line
# is red. Splitting on non-hex runs keeps a 64-hex digest from being read as
# 40-hex.
e1_final_hashes() {
  awk '
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i <= NR; i++)
        if (line[i] ~ /^#{1,4} .*Round[- ]?37([^0-9]|$)/) start = i
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

# e1_has_round37 FILE — 1 when SCORECARD.md carries a Round[- ]37 heading.
e1_has_round37() {
  awk '/^#{1,4} .*Round[- ]?37([^0-9]|$)/ { found = 1 } END { print found + 0 }' "$1"
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

# e13_rows FILE NAME — print `<type-cell>\t<verdict-map-cell>` for each registry
# row whose first cell is exactly NAME. Cells are split on unescaped pipes: the
# markdown escape `\|` is temporarily replaced so it cannot split a cell.
e13_rows() {
  awk -v name="$2" '
    BEGIN { b = name; gsub(/\./, "\\.", b); pat = "^\\|[[:space:]]*`?" b "`?[[:space:]]*\\|" }
    /^## / { inreg = ($0 ~ /Gates & probes registry/); next }
    inreg && $0 ~ pat {
      line = $0
      gsub(/\\\|/, "\001", line)
      n = split(line, c, "|")
      t = c[3]; v = c[5]
      gsub(/^[[:space:]]+/, "", t); gsub(/[[:space:]]+$/, "", t)
      gsub(/^[[:space:]]+/, "", v); gsub(/[[:space:]]+$/, "", v)
      gsub(/\001/, "|", t); gsub(/\001/, "|", v)
      print t "\t" v
    }
  ' "$1"
}

# e12_section FILE — the LAST `## …Round[- ]?37…` block in FILE, closed by the
# next `## ` heading (or EOF). Section scoping is what makes the "stale label
# appears nowhere inside the round-37 SCORECARD section" limb a real assertion
# instead of a file-wide one that the round-36 history line would satisfy.
e12_section() {
  awk '
    { line[NR] = $0 }
    END {
      start = 0
      for (i = 1; i <= NR; i++)
        if (line[i] ~ /^## .*Round[- ]?37([^0-9]|$)/) start = i
      if (start == 0) exit
      for (i = start; i <= NR; i++) {
        if (i > start && line[i] ~ /^## /) break
        print line[i]
      }
    }
  ' "$1"
}

# e11_block FILE — the LAST `## …Round[- ]?37…` block in LOG.md, closed by the
# next `## ` heading (or EOF).
e11_block() {
  e12_section "$1"
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
    section=$(e1_has_round37 SCORECARD.md); section=${section:-0}
    while IFS= read -r h; do
      [ -n "$h" ] || continue
      total=$((total + 1))
      if git -C "$LANE" cat-file -e "${h}^{commit}" 2>/dev/null \
         && git -C "$LANE" merge-base --is-ancestor "$h" "$ref" 2>/dev/null; then
        bound=$((bound + 1))
      fi
    done < <(e1_final_hashes SCORECARD.md)
    printf 'placeholders=%s,lane-hash-markers=%s,round37-section=%s,round37-final-lane-commits=%s,bound=%s' \
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
    # exact basename in the first table column (optional backticks).
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
    # close the check.
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
    # mention the instrument whose output was the false evidence line.
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
  local out porcelain_lines=0 dirty_disp=0 status_state=ok left=0
  local head head_ok=0 root_ok=0 skip='' d dp top root sroot_state=absent
  if ! git -C "$srepo" rev-parse --git-dir >/dev/null 2>&1; then
    printf 'status-repo=unreadable,status-read=failed,scratch-seat-dirs=?,head-match=0,lane-root=0,scratch-root=?'
    return 1
  fi
  # The status repo must BE the lane root: an export path or a subdirectory of
  # some enclosing repository would otherwise report another tree's cleanliness.
  root=$( cd "$srepo" 2>/dev/null && pwd -P )
  top=$(git -C "$srepo" rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$top" ] && [ -n "$root" ] && [ "$top" = "$root" ]; then root_ok=1; fi
  # FAIL-CLOSED status read: the exit status of the read is what decides, not a
  # `${…:-0}` default. A read that fails is RED (`status-read=failed`); there is
  # deliberately no stderr suppression on this command, so a broken repository
  # cannot be mistaken for a clean one.
  # --no-optional-locks: plain `git status` takes and unlinks .git/index.lock,
  # a transient write under the lane. This suite must leave the lane untouched.
  if out=$(git --no-optional-locks -C "$srepo" status --porcelain); then
    porcelain_lines=$(printf '%s' "$out" | count_lines)
    porcelain_lines=${porcelain_lines:-0}
    dirty_disp=$porcelain_lines
  else
    status_state=failed
    # A failed read leaves the dirty count UNKNOWN; it is printed as `?`, never
    # as 0, so the payload cannot be misread as "clean".
    dirty_disp='?'
  fi
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
  printf 'status-read=%s,status-dirty=%s,scratch-seat-dirs=%s,head-match=%s,lane-root=%s,scratch-root=%s' \
    "$status_state" "$dirty_disp" "$left" "$head_ok" "$root_ok" "$sroot_state"
  [ "$status_state" = ok ] && [ "$porcelain_lines" -eq 0 ] && [ "$left" -eq 0 ] \
    && [ "$head_ok" -eq 1 ] && [ "$root_ok" -eq 1 ] && return 0
  return 1
}

# payload_keys FILE ID — the sorted key set of a recorded line
# `E<id> payload=<k=v,...> closed=0|1`. Values may differ between the ref a
# receipt was recorded at and the ref it is verified at (E9's limbs are live);
# the key set may not.
payload_keys() { # FILE ID
  sed -n "s/^$2 payload=\(.*\) closed=[01]$/\1/p" "$1" | head -n 1 \
    | tr ',' '\n' | sed -n 's/^\([A-Za-z0-9_.-]*\)=.*/\1/p' | sort -u
}

check_e10() { # TREE REF [LIVE_LINES]
  local tree=$1 ref=$2 live=${3:-}
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-37/final-gates/all-gates.txt
    local suite=corpus/instruments/r37-closure.sh
    local file=0 sfile=0 hdr=0 anc=0 dig=0 runl=0 rclosed=0 stc=0 stsum=0 cross=0 ph=0
    local hdrtext='' ids got xref xsha asha line o m det allok=1
    [ -f "$p" ] && file=1
    if [ -f "$suite" ] \
       && [ "$(git -C "$LANE" ls-tree -r --name-only "$ref" -- "$suite" 2>/dev/null | count_lines)" -eq 1 ]; then
      sfile=1
    fi
    # expected id set in the order `sort -u` produces it (E1 E10 E11 … E2 …)
    ids=$(for i in $(seq 1 14); do printf 'E%s\n' "$i"; done | sort -u)
    if [ "$file" -eq 1 ]; then
      hdrtext=$(awk '/^== /{exit} {print}' "$p")
      if [ "$(printf '%s\n' "$hdrtext" | head -n 1)" = 'all-gates v1' ] \
         && [ "$(printf '%s\n' "$hdrtext" | grep -cE '^export-ref=[0-9a-f]{40}$')" -eq 1 ] \
         && [ "$(printf '%s\n' "$hdrtext" | grep -cE '^suite-sha256=[0-9a-f]{64}$')" -eq 1 ] \
         && [ "$(printf '%s\n' "$hdrtext" | grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')" -eq 1 ] \
         && [ "$(printf '%s\n' "$hdrtext" | grep -vcE '^(all-gates v1|export-ref=[0-9a-f]{40}|suite-sha256=[0-9a-f]{64}|run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z|#.*|)$')" -eq 0 ]; then
        hdr=1
      fi
      if [ "$hdr" -eq 1 ]; then
        xref=$(printf '%s\n' "$hdrtext" | sed -n 's/^export-ref=//p')
        xsha=$(printf '%s\n' "$hdrtext" | sed -n 's/^suite-sha256=//p')
        # ancestor-or-equal, never equality: the receipt is committed by a
        # commit AFTER the head it records.
        if git -C "$LANE" cat-file -e "${xref}^{commit}" 2>/dev/null \
           && git -C "$LANE" merge-base --is-ancestor "$xref" "$ref" 2>/dev/null; then
          anc=1
        fi
        if [ "$sfile" -eq 1 ] && [ -n "$xsha" ]; then
          asha=$(sha256sum -- "$suite" | awk '{print $1; exit}')
          # the digest must equal BOTH the exported suite bytes and the bytes
          # actually executing: a receipt from another suite version is red.
          if [ "$asha" = "$xsha" ] && [ "$xsha" = "$(suite_digest)" ]; then dig=1; fi
        fi
      fi
      # run block: exactly one closed=1 line per check id, no closed=0 line
      got=$(grep -E '^E[0-9]+ payload=.* closed=1$' "$p" | sed -n 's/^\(E[0-9][0-9]*\) payload=.*/\1/p' | sort -u)
      if [ "$got" = "$ids" ]; then runl=14; else runl=$(printf '%s\n' "$got" | count_lines); fi
      runl=${runl:-0}
      if [ "$(grep -cE '^E[0-9]+ payload=.* closed=0$' "$p")" -ne 0 ]; then runl=0; fi
      if [ "$(grep -cE '^closed=14/14 exit=0$' "$p")" -eq 1 ]; then rclosed=1; fi
      # selftest block: ids once each, positive+verdict pass, mutants o==n>=1
      # with exactly n rejected=1 detail lines behind each case
      got=$(grep -E '^selftest case=E[0-9]+ ' "$p" | sed -n 's/^selftest case=\(E[0-9][0-9]*\) .*/\1/p' | sort -u)
      if [ "$got" = "$ids" ]; then
        stc=0
        for id in $ids; do
          allok=1
          line=$(grep -m1 "^selftest case=${id} " "$p")
          printf '%s' "$line" | grep -q 'positive=pass' || allok=0
          printf '%s' "$line" | grep -q 'verdict=pass$' || allok=0
          o=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
          m=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
          if [ -z "$o" ] || [ -z "$m" ] || [ "$m" -lt 1 ] || [ "$o" -ne "$m" ]; then allok=0; fi
          det=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$p"); det=${det:-0}
          [ "$det" -eq "${m:-0}" ] || allok=0
          stc=$((stc + allok))
        done
      else
        stc=$(printf '%s\n' "$got" | count_lines)
      fi
      stc=${stc:-0}
      if [ "$(grep -cE '^selftest cases=14 failures=0$' "$p")" -eq 1 ]; then stsum=1; fi
      # cross-run shape binding: for every id but E10 (self-referential), the
      # recorded payload KEY SET must equal this run's key set for that id
      if [ -n "$live" ] && [ -f "$live" ]; then
        cross=1
        for id in $ids; do
          [ "$id" = E10 ] && continue
          if [ "$(payload_keys "$p" "$id")" != "$(payload_keys "$live" "$id")" ]; then
            cross=0; break
          fi
        done
      fi
      ph=$(grep -cE '<(hash|sha|digest|ref|payload|N|n|id)>|TODO|TBD' "$p"); ph=${ph:-0}
    fi
    printf 'all-gates=%s,suite-file=%s,header=%s,ancestor=%s,digest-match=%s,run-lines=%s,recorded-closed=%s,selftest-cases=%s,selftest-summary=%s,crossrun=%s,placeholders=%s' \
      "$file" "$sfile" "$hdr" "$anc" "$dig" "$runl" "$rclosed" "$stc" "$stsum" "$cross" "$ph"
    [ "$file" -eq 1 ] && [ "$sfile" -eq 1 ] && [ "$hdr" -eq 1 ] && [ "$anc" -eq 1 ] \
      && [ "$dig" -eq 1 ] && [ "$runl" -eq 14 ] && [ "$rclosed" -eq 1 ] \
      && [ "$stc" -eq 14 ] && [ "$stsum" -eq 1 ] && [ "$cross" -eq 1 ] \
      && [ "$ph" -eq 0 ] && exit 0
    exit 1
  )
}

check_e11() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local blk=0 marker=0 named=0 falsity=0 body=''
    if [ -f LOG.md ]; then
      body=$(e11_block LOG.md)
      [ -n "$body" ] && blk=1
    fi
    if [ "$blk" -eq 1 ]; then
      marker=$(printf '%s\n' "$body" | grep -cF -- 'Correction (round 37)'); marker=${marker:-0}
      named=$(printf '%s\n' "$body" | grep -cF -- 'corpus/instruments/r36-fixtures/'); named=${named:-0}
      # A correction that names the path but never says the path was wrong is
      # not a correction of the false path; the falsity must be stated.
      falsity=$(printf '%s\n' "$body" \
        | grep -cEi -- 'absent|never committed|does not exist|not present'); falsity=${falsity:-0}
    fi
    printf 'log37-block=%s,correction-marker=%s,false-path-named=%s,falsity-stated=%s' \
      "$blk" "$marker" "$named" "$falsity"
    [ "$blk" -eq 1 ] && [ "$marker" -ge 1 ] && [ "$named" -ge 1 ] \
      && [ "$falsity" -ge 1 ] && exit 0
    exit 1
  )
}

check_e12() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local sec='' sec_ok=0 h=0 a=0 stale=0 lesson=0 lh=0 la=0
    if [ -f SCORECARD.md ]; then
      sec=$(e12_section SCORECARD.md)
      [ -n "$sec" ] && sec_ok=1
    fi
    if [ "$sec_ok" -eq 1 ]; then
      h=$(printf '%s\n' "$sec" | grep -cF -- 'c20300df'); h=${h:-0}
      a=$(printf '%s\n' "$sec" | grep -ciE -- 'anchor[- ]ancestor'); a=${a:-0}
      stale=$(printf '%s\n' "$sec" | grep -cF -- 'Final lane commit: e666d902'); stale=${stale:-0}
    fi
    if [ -f corpus/lessons/round-37.md ]; then
      lesson=1
      lh=$(grep -cF -- 'c20300df' corpus/lessons/round-37.md 2>/dev/null); lh=${lh:-0}
      la=$(grep -ciE -- 'anchor[- ]ancestor' corpus/lessons/round-37.md 2>/dev/null); la=${la:-0}
    fi
    printf 'scorecard37-section=%s,c20300df=%s,anchor-ancestor=%s,stale-e666d902=%s,lesson37=%s,lesson-c20300df=%s,lesson-anchor-ancestor=%s' \
      "$sec_ok" "$h" "$a" "$stale" "$lesson" "$lh" "$la"
    [ "$sec_ok" -eq 1 ] && [ "$h" -ge 1 ] && [ "$a" -ge 1 ] && [ "$stale" -eq 0 ] \
      && [ "$lesson" -eq 1 ] && [ "$lh" -ge 1 ] && [ "$la" -ge 1 ] && exit 0
    exit 1
  )
}

check_e13() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local rows total=0 single=0 exit2=0 t v
    rows=$(e13_rows SKILL.md 'r36-closure.sh')
    total=$(printf '%s\n' "$rows" | count_lines); total=${total:-0}
    while IFS=$'\t' read -r t v; do
      [ -n "$t" ] || continue
      case $t in
        gate|probe) ;;
        *) continue ;;
      esac
      single=$((single + 1))
      printf '%s' "$v" | grep -qE -- '2[^[:alnum:]]{0,8}could-not-evaluate' || continue
      exit2=$((exit2 + 1))
    done <<< "$rows"
    printf 'registry-rows=%s,single-choice-type=%s,exit2-verdict=%s' "$total" "$single" "$exit2"
    [ "$total" -ge 1 ] && [ "$single" -ge 1 ] && [ "$exit2" -ge 1 ] && exit 0
    exit 1
  )
}

check_e14() { # TREE REF
  local tree=$1 p=corpus/instruments/r37-closure.sh
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    if [ ! -f "$p" ]; then
      printf 'suite-file=0,porcelain-default=?,status-read-swallow=?,status-read-sites=0,fail-closed-marker=0'
      exit 1
    fi
    local needle dflt swallow=0 sites=0 marker=0 line
    # Assembled so this instrument's own bytes never contain the literal it
    # hunts for (the same reason E1 assembles its placeholder spellings).
    needle="porcelain$(printf '%s' ':-0')"
    dflt=$(grep -cF -- "$needle" "$p" 2>/dev/null); dflt=${dflt:-0}
    sites=$(grep -cF -- 'status --porcelain' "$p"); sites=${sites:-0}
    if [ "$sites" -ge 1 ]; then
      while IFS= read -r line; do
        printf '%s' "$line" | grep -qF -- '2>/dev/null' && swallow=$((swallow + 1))
        printf '%s' "$line" | grep -qF -- '|| true' && swallow=$((swallow + 1))
      done < <(grep -F -- 'status --porcelain' "$p")
    fi
    marker=$(grep -cF -- 'status-read=failed' "$p" 2>/dev/null); marker=${marker:-0}
    printf 'suite-file=1,porcelain-default=%s,status-read-swallow=%s,status-read-sites=%s,fail-closed-marker=%s' \
      "$dflt" "$swallow" "$sites" "$marker"
    [ "$dflt" -eq 0 ] && [ "$swallow" -eq 0 ] && [ "$sites" -ge 1 ] \
      && [ "$marker" -ge 1 ] && exit 0
    exit 1
  )
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
  local lines='' id out rc k=0 n=0 counted=0 live=$WORK/live-lines.txt
  local -A PAY=() RC=()
  printf 'export-ref=%s mode=export lane=%s suite-sha256=%s\n' \
    "$REF_RESOLVED" "$LANE" "$(suite_digest)"
  if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
  if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
  : > "$live"
  # E10 is evaluated LAST: it compares the recorded receipt's payload shapes
  # against the lines this run just produced, so every other check must have
  # produced its line first.
  for id in "${CHECK_IDS[@]}"; do
    [ "$id" = E10 ] && continue
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
    PAY[$id]=$out; RC[$id]=$rc
    if [ "$rc" -eq 0 ]; then
      printf '%s payload=%s closed=1\n' "$id" "$out" >> "$live"
    else
      printf '%s payload=%s closed=0\n' "$id" "$out" >> "$live"
    fi
  done
  out=$(run_check E10 "$EXPORT" "$REF_RESOLVED" "$live" 2>/dev/null); rc=$?
  PAY[E10]=$out; RC[E10]=$rc
  for id in "${CHECK_IDS[@]}"; do
    if [ "${RC[$id]}" -eq 0 ]; then
      k=$((k + 1))
      lines="${lines}${id} payload=${PAY[$id]} closed=1"$'\n'
    else
      lines="${lines}${id} payload=${PAY[$id]} closed=0"$'\n'
    fi
  done
  printf '%s' "$lines"
  n=$(printf '%s' "$lines" | grep -c '^E[0-9][0-9]* payload=')
  if [ "$n" -ne 14 ]; then
    printf 'suite problem=self-report lines=%s expected=14\n' "$n"
    printf 'closed=0/14 exit=1\n'
    return 1
  fi
  counted=$(printf '%s' "$lines" | grep -c 'closed=1$')
  if [ "$counted" -ne "$k" ]; then
    printf 'suite problem=self-report closed=%s counted=%s\n' "$k" "$counted"
    printf 'closed=0/14 exit=1\n'
    return 1
  fi
  if [ "$k" -eq 14 ]; then
    printf 'closed=%s/14 exit=0\n' "$k"
    return 0
  fi
  printf 'closed=%s/14 exit=1\n' "$k"
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

st_pos() { # ID TREE REF [EXTRA...]
  local id=$1 tree=$2 ref=$3; shift 3
  local out rc
  out=$(run_check "$id" "$tree" "$ref" "$@" 2>/dev/null); rc=$?
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

# suite_copy DIR — byte-identical copy of the executing suite at
# DIR/corpus/instruments/r37-closure.sh, so a receipt fixture's suite-file and
# digest limbs can match while a mutant reopens exactly one other clause.
suite_copy() { # DIR
  mkdir -p -- "$1/corpus/instruments"
  cp -- "$SELF" "$1/corpus/instruments/r37-closure.sh"
}

# mk_gates DEST LIVE [knob...] — build an `all-gates v1` receipt fixture from the
# live lines this run produced. Defaults build a receipt every limb accepts; each
# knob reopens exactly one clause:
#   sentinel=no          omit the `all-gates v1` first line
#   xref=<40 hex>        header export-ref
#   sha=<64 hex>         header suite-sha256
#   utc=<value>          header run-utc
#   extra=<line>         one extra header line
#   run=all|drop:E<n>|dup|open
#   closed=<line>        the closed= line
#   cases=all|drop:E<n>|failpos|zero
#   sum=<line>           the selftest summary line
mk_gates() { # DEST LIVE [knob...]
  local dest=$1 live=$2; shift 2
  local sentinel=yes xref=$REF_RESOLVED sha utc='2026-10-26T00:00:00Z' extra=''
  local run=all closedline='closed=14/14 exit=0' cases=all sumline='selftest cases=14 failures=0'
  local kv i
  sha=$(suite_digest)
  for kv in "$@"; do
    case $kv in
      sentinel=*) sentinel=${kv#sentinel=} ;;
      xref=*) xref=${kv#xref=} ;;
      sha=*) sha=${kv#sha=} ;;
      utc=*) utc=${kv#utc=} ;;
      extra=*) extra=${kv#extra=} ;;
      run=*) run=${kv#run=} ;;
      closed=*) closedline=${kv#closed=} ;;
      cases=*) cases=${kv#cases=} ;;
      sum=*) sumline=${kv#sum=} ;;
    esac
  done
  mkdir -p -- "$(dirname -- "$dest")"
  {
    [ "$sentinel" = yes ] && printf 'all-gates v1\n'
    printf 'export-ref=%s\n' "$xref"
    printf 'suite-sha256=%s\n' "$sha"
    printf 'run-utc=%s\n' "$utc"
    printf '# fixture: generated by the r37-closure selftest, never lane evidence\n'
    [ -n "$extra" ] && printf '%s\n' "$extra"
    printf '\n== run ==\n'
    case $run in
      all) cat -- "$live" ;;
      drop:*) grep -v -- "^${run#drop:} " "$live" ;;
      dup) grep -v '^E8 ' "$live"; grep '^E9 ' "$live" | head -n 1 ;;
      open) sed -e 's/ closed=1$/ closed=0/' "$live" ;;
    esac
    printf '%s\n' "$closedline"
    printf '== selftest ==\n'
    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do
      [ "$cases" = "drop:E$i" ] && continue
      case $cases in
        failpos)
          if [ "$i" -eq 9 ]; then
            printf 'selftest case=E9 positive=fail mutants=1/1 verdict=pass\n'
            printf 'selftest detail=E9 mutant=x rejected=1 limb=x\n'
          else
            printf 'selftest case=E%s positive=pass mutants=1/1 verdict=pass\n' "$i"
            printf 'selftest detail=E%s mutant=x rejected=1 limb=x\n' "$i"
          fi ;;
        zero) printf 'selftest case=E%s positive=pass mutants=0/0 verdict=pass\n' "$i" ;;
        *)
          printf 'selftest case=E%s positive=pass mutants=1/1 verdict=pass\n' "$i"
          printf 'selftest detail=E%s mutant=x rejected=1 limb=x\n' "$i" ;;
      esac
    done
    printf '%s\n' "$sumline"
  } > "$dest"
}

selftest_case_E1() {
  local bad=0 ok=0 n=0 h d
  CASES=$((CASES + 1))
  st_pos E1 "$EXPORT" "$REF_RESOLVED" || bad=1
  h=$REF_RESOLVED
  n=$((n + 1)); d=$MUT/E1-placeholder; mut_reset "$d"
  printf '## Round 37\n\n**Final lane commit: `%s`**\nfilled by the %s\n' "$h" 'L1' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 placeholder "$d" "$REF_RESOLVED" 'placeholders=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-lanehash; mut_reset "$d"
  printf '## Round 37\n\n**Final lane commit: `%s`**\n<%s>\n' "$h" 'LANE_HASH' \
    | mut_put "$d" SCORECARD.md
  st_neg E1 lane-hash-marker "$d" "$REF_RESOLVED" 'lane-hash-markers=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-unbound; mut_reset "$d"
  printf '## Round 37\n\n**Final lane commit: `%s`**\n' \
    '0123456789abcdef0123456789abcdef01234567' | mut_put "$d" SCORECARD.md
  st_neg E1 unbound-hash "$d" "$REF_RESOLVED" 'bound=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E1-history; mut_reset "$d"
  printf '**Final lane commit: `%s`**\n' "$h" | mut_put "$d" SCORECARD.md
  st_neg E1 history-only "$d" "$REF_RESOLVED" 'round37-section=0' && ok=$((ok + 1))
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
  printf '## Round 37\n\nNote: the round-34 depth:density row was corrected last round; guard mean 201.2.\n' \
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
  git -C "$repo" -c user.email=r37@local -c user.name=r37 commit -q -m fixture 2>/dev/null
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
  # fail-closed limb: a status READ that fails must be RED and must say so.
  # A corrupt .git/index keeps `rev-parse --git-dir` working while
  # `git status --porcelain` fails, which is exactly the D6 shape.
  n=$((n + 1)); mut_reset "$MUT/e9broken"
  if git -C "$MUT/e9broken" init -q 2>/dev/null; then
    printf 'garbage-not-an-index\n' > "$MUT/e9broken/.git/index"
    st_neg E9 status-read-failed "$EXPORT" "$REF_RESOLVED" 'status-read=failed' \
      "$MUT/e9scratch-empty" "$MUT/e9broken" "$head" && ok=$((ok + 1))
  else
    printf 'selftest detail=E9 fixture=broken-repo-init-failed\n'
  fi
  st_verdict E9 "$bad" "$ok" "$n"
}

selftest_case_E10() {
  local bad=0 ok=0 n=0 d live=$MUT/e10-live.txt id out rc z40 z64 p
  CASES=$((CASES + 1))
  z40=$(printf '%040d' 0)
  z64=$(printf '%064d' 0)
  # the live lines E10's cross-run limb compares against: this run's own pass
  # over the thirteen checks that are not E10, plus a synthesized E10 line so a
  # fixture receipt carries the full fourteen-line run block (E10 itself is
  # exempt from the cross-run key-set comparison).
  : > "$live"
  for id in "${CHECK_IDS[@]}"; do
    [ "$id" = E10 ] && continue
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
    printf '%s payload=%s closed=1\n' "$id" "$out" >> "$live"
  done
  printf 'E10 payload=fixture-bootstrap closed=1\n' >> "$live"
  st_pos E10 "$EXPORT" "$REF_RESOLVED" "$live" || bad=1
  p=.ufo/waves/round-37/final-gates/all-gates.txt
  n=$((n + 1)); d=$MUT/E10-missing; mut_reset "$d"
  st_neg E10 all-gates-absent "$d" "$REF_RESOLVED" 'all-gates=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-digest; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" "sha=$z64"
  st_neg E10 digest-mismatch "$d" "$REF_RESOLVED" 'digest-match=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-xref; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" "xref=$z40"
  st_neg E10 export-ref-unresolvable "$d" "$REF_RESOLVED" 'ancestor=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-utc; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'utc=not-a-timestamp'
  st_neg E10 run-utc-invalid "$d" "$REF_RESOLVED" 'header=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-sentinel; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'sentinel=no'
  st_neg E10 sentinel-missing "$d" "$REF_RESOLVED" 'header=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-shape; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'extra=garbage header line'
  st_neg E10 header-shape "$d" "$REF_RESOLVED" 'header=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-rundrop; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'run=drop:E13'
  st_neg E10 run-line-missing "$d" "$REF_RESOLVED" 'run-lines=13' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-rundup; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'run=dup'
  st_neg E10 run-id-duplicated "$d" "$REF_RESOLVED" 'run-lines=13' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-runopen; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'run=open'
  st_neg E10 run-line-open "$d" "$REF_RESOLVED" 'run-lines=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-closed; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'closed=closed=13/14 exit=0'
  st_neg E10 closed-line-wrong "$d" "$REF_RESOLVED" 'recorded-closed=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-casedrop; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'cases=drop:E13'
  st_neg E10 selftest-case-missing "$d" "$REF_RESOLVED" 'selftest-cases=13' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-casefail; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'cases=failpos'
  st_neg E10 selftest-positive-failed "$d" "$REF_RESOLVED" 'selftest-cases=13' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-casezero; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'cases=zero'
  st_neg E10 selftest-mutants-zero "$d" "$REF_RESOLVED" 'selftest-cases=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-summary; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'sum=selftest cases=14 failures=1'
  st_neg E10 selftest-summary-failed "$d" "$REF_RESOLVED" 'selftest-summary=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-crossrun; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live"
  sed -i -e 's/^E9 payload=\(.*\) closed=1$/E9 payload=\1,extra-key=1 closed=1/' "$d/$p"
  st_neg E10 crossrun-key-drift "$d" "$REF_RESOLVED" 'crossrun=0' "$live" && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E10-placeholder; mut_reset "$d"; suite_copy "$d"
  mk_gates "$d/$p" "$live" 'extra=# TODO fill the export-ref'
  st_neg E10 placeholder-present "$d" "$REF_RESOLVED" 'placeholders=1' "$live" && ok=$((ok + 1))
  st_verdict E10 "$bad" "$ok" "$n"
}

selftest_case_E11() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E11 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E11-none; mut_reset "$d"
  printf '## Round 36 — old entry\n\nno round-37 block here\n' | mut_put "$d" LOG.md
  st_neg E11 no-round37-block "$d" "$REF_RESOLVED" 'log37-block=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E11-nocorrection; mut_reset "$d"
  printf '## Round 37 — entry\n\n- C1 landed the suite; the false path corpus/instruments/r36-fixtures/ was never committed.\n' \
    | mut_put "$d" LOG.md
  st_neg E11 no-correction-marker "$d" "$REF_RESOLVED" 'correction-marker=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E11-nopath; mut_reset "$d"
  printf '## Round 37 — entry\n\n- Correction (round 37): the old bullet was wrong and stands corrected.\n' \
    | mut_put "$d" LOG.md
  st_neg E11 path-not-named "$d" "$REF_RESOLVED" 'false-path-named=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E11-nofalsity; mut_reset "$d"
  printf '## Round 37 — entry\n\n- Correction (round 37): the old bullet named corpus/instruments/r36-fixtures/.\n' \
    | mut_put "$d" LOG.md
  st_neg E11 falsity-not-stated "$d" "$REF_RESOLVED" 'falsity-stated=0' && ok=$((ok + 1))
  st_verdict E11 "$bad" "$ok" "$n"
}

# E12 fixture helper: a valid round-37 SCORECARD section + lesson, so a mutant
# reopens exactly one clause.
e12_fixture() { # DIR SECTION_LINE...
  local d=$1; shift
  mut_reset "$d"
  {
    printf '## Round 36 — old section\n\nFinal lane commit: e666d902337a49dcbfc77880939874f39c6f477b\n'
    printf '%s\n' "$@"
  } | mut_put "$d" SCORECARD.md
  printf 'M37-3 the r36 lane head c20300df is the anchor ancestor, not the r37 final tip\n' \
    | mut_put "$d" corpus/lessons/round-37.md
}

selftest_case_E12() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E12 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E12-nosection; mut_reset "$d"
  printf '## Round 36 — old section\n\nFinal lane commit: e666d902337a49dcbfc77880939874f39c6f477b\n' \
    | mut_put "$d" SCORECARD.md
  printf 'M37-3 c20300df anchor ancestor\n' | mut_put "$d" corpus/lessons/round-37.md
  st_neg E12 no-round37-section "$d" "$REF_RESOLVED" 'scorecard37-section=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E12-noanchor; e12_fixture "$d" \
    '## Round 37 result' '' 'the r36 lane head c20300df is the previous round tip'
  st_neg E12 anchor-label-absent "$d" "$REF_RESOLVED" 'anchor-ancestor=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E12-nohash; e12_fixture "$d" \
    '## Round 37 result' '' 'the r36 lane head is the anchor ancestor'
  st_neg E12 anchor-hash-absent "$d" "$REF_RESOLVED" 'c20300df=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E12-stale; e12_fixture "$d" \
    '## Round 37 result' '' 'the r36 lane head c20300df is the anchor ancestor' \
    'Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b'
  st_neg E12 stale-label-in-section "$d" "$REF_RESOLVED" 'stale-e666d902=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E12-nolesson; e12_fixture "$d" \
    '## Round 37 result' '' 'the r36 lane head c20300df is the anchor ancestor'
  rm -f -- "$d/corpus/lessons/round-37.md"
  st_neg E12 lesson-absent "$d" "$REF_RESOLVED" 'lesson37=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E12-lesson-unbound; e12_fixture "$d" \
    '## Round 37 result' '' 'the r36 lane head c20300df is the anchor ancestor'
  printf 'M37-3 label drift corrected\n' | mut_put "$d" corpus/lessons/round-37.md
  st_neg E12 lesson-not-bound "$d" "$REF_RESOLVED" 'lesson-c20300df=0' && ok=$((ok + 1))
  st_verdict E12 "$bad" "$ok" "$n"
}

selftest_case_E13() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos E13 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/E13-type-cell; mut_reset "$d"
  printf '## Gates & probes registry\n\n| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n| r36-closure.sh | gate\\|probe | bash x | 0 closed \\| 1 open \\| 2 could-not-evaluate | bash x --selftest | none | read-only | kasegi |\n' \
    | mut_put "$d" SKILL.md
  st_neg E13 type-cell-not-single "$d" "$REF_RESOLVED" 'single-choice-type=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E13-verdict; mut_reset "$d"
  printf '## Gates & probes registry\n\n| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n| r36-closure.sh | gate | bash x | 0 closed \\| 1 open | bash x --selftest | none | read-only | kasegi |\n' \
    | mut_put "$d" SKILL.md
  st_neg E13 exit2-verdict-absent "$d" "$REF_RESOLVED" 'exit2-verdict=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E13-outside; mut_reset "$d"
  printf '## Cited paths\n\n| r36-closure.sh | gate | bash x | 2 -> could-not-evaluate | bash x --selftest | none | read-only | kasegi |\n' \
    | mut_put "$d" SKILL.md
  st_neg E13 row-outside-registry "$d" "$REF_RESOLVED" 'registry-rows=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E13-split; mut_reset "$d"
  printf '## Gates & probes registry\n\n| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n| r36-closure.sh | gate | bash x | 0 closed \\| 1 open | bash x --selftest | none | read-only | kasegi |\n| r36-closure.sh | gate\\|probe | bash x | 0 closed \\| 1 open \\| 2 could-not-evaluate | bash x --selftest | none | read-only | kasegi |\n' \
    | mut_put "$d" SKILL.md
  # the two clauses must hold on the SAME row: one row with the right type and
  # another with the exit-2 map is not a corrected row.
  st_neg E13 clauses-split-across-rows "$d" "$REF_RESOLVED" 'exit2-verdict=0' && ok=$((ok + 1))
  # control (not a mutant, not counted): append-only means the round-36 row's
  # `gate|probe` cell stays and the correction is an appended row -- that shape
  # must be ACCEPTED, never made red by the presence of the old row.
  d=$MUT/E13-appended; mut_reset "$d"
  printf '## Gates & probes registry\n\n| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n| r36-closure.sh | gate\\|probe | bash x | 0 closed \\| 1 open | bash x --selftest | none | read-only | kasegi (round 36) |\n| r36-closure.sh | probe | bash x --export-ref <hash> | 0 closed \\| 1 open \\| 2 could-not-evaluate | bash x --selftest | none | read-only | kasegi (round 37 correction) |\n' \
    | mut_put "$d" SKILL.md
  out=$(run_check E13 "$d" "$REF_RESOLVED" 2>/dev/null); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=E13 control=appended-correction-shape accepted=1\n'
  else
    printf 'selftest detail=E13 control=appended-correction-shape accepted=0 rc=%s payload=%s\n' "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
  st_verdict E13 "$bad" "$ok" "$n"
}

selftest_case_E14() {
  local bad=0 ok=0 n=0 d sw
  CASES=$((CASES + 1))
  st_pos E14 "$EXPORT" "$REF_RESOLVED" || bad=1
  # the literal is assembled here too, so this file never carries it
  sw='2>'"$(printf '%s' '/dev/null')"
  n=$((n + 1)); d=$MUT/E14-default; mut_reset "$d"
  mkdir -p -- "$d/corpus/instruments"
  {
    printf 'porcelain=\"$(git status --porcelain)\"\n'
    printf 'n=${porcelain%s}\n' "$(printf '%s' ':-0')"
    printf 'echo status-read=failed\n'
  } > "$d/corpus/instruments/r37-closure.sh"
  st_neg E14 fail-open-default "$d" "$REF_RESOLVED" 'porcelain-default=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E14-swallow; mut_reset "$d"
  mkdir -p -- "$d/corpus/instruments"
  {
    printf 'out=$(git -C \"$r\" status --porcelain %s)\n' "$sw"
    printf 'echo status-read=failed\n'
  } > "$d/corpus/instruments/r37-closure.sh"
  st_neg E14 status-read-swallowed "$d" "$REF_RESOLVED" 'status-read-swallow=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/E14-nomarker; mut_reset "$d"
  mkdir -p -- "$d/corpus/instruments"
  printf 'if out=$(git -C \"$r\" status --porcelain); then :; fi\n' \
    > "$d/corpus/instruments/r37-closure.sh"
  st_neg E14 fail-closed-marker-absent "$d" "$REF_RESOLVED" 'fail-closed-marker=0' && ok=$((ok + 1))
  st_verdict E14 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id hit=0 line n ok det rej dup
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f" 2>/dev/null); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f" 2>/dev/null); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=14 failures=0$' "$f" 2>/dev/null); summary=${summary:-0}
  [ "$cases" -eq 14 ] && [ "$verdicts" -eq 14 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=E<i> mutant=`
  # lines of which ok name rejected=1. A fabricated case line carrying
  # `mutants=0/0` (no fixture ran) is rejected: n must be >= 1 and the detail
  # lines must exist.
  for id in "${CHECK_IDS[@]}"; do
    dup=$(grep -c "^selftest case=${id} " "$f" 2>/dev/null); dup=${dup:-0}
    [ "$dup" -eq 1 ] || return 1
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
  [ "$hit" -eq 14 ]
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

  printf 'selftest cases=14 failures=0\n' > "$WORK/forge-caselines.txt"
  if judge_selftest_report "$WORK/forge-caselines.txt"; then
    printf 'selftest judge=forged-caselines rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-caselines rejected=1\n'
  fi

  {
    for i in $(seq 1 14); do
      printf 'selftest case=E%s positive=fail mutants=0/1 verdict=fail\n' "$i"
    done
    printf 'selftest cases=14 failures=0\n'
  } > "$WORK/forge-failed-cases.txt"
  if judge_selftest_report "$WORK/forge-failed-cases.txt"; then
    printf 'selftest judge=forged-failed-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-failed-cases rejected=1\n'
  fi

  # the detail-free all-pass forgery: fourteen case lines claiming pass with
  # mutants=0/0 and no fixture detail behind them
  {
    for i in $(seq 1 14); do
      printf 'selftest case=E%s positive=pass mutants=0/0 verdict=pass\n' "$i"
    done
    printf 'selftest cases=14 failures=0\n'
  } > "$WORK/forge-detail-free.txt"
  if judge_selftest_report "$WORK/forge-detail-free.txt"; then
    printf 'selftest judge=forged-detail-free rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-detail-free rejected=1\n'
  fi

  # the 13-case forgery: every line well-formed, one check never ran. The case
  # count and the per-id requirement must both reject it.
  {
    for i in $(seq 1 13); do
      printf 'selftest case=E%s positive=pass mutants=1/1 verdict=pass\n' "$i"
      printf 'selftest detail=E%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest cases=14 failures=0\n'
  } > "$WORK/forge-13-cases.txt"
  if judge_selftest_report "$WORK/forge-13-cases.txt"; then
    printf 'selftest judge=forged-13-cases rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-13-cases rejected=1\n'
  fi

  # the duplicated-id forgery: fourteen case lines but E1 twice and E14 never.
  {
    for i in $(seq 1 13); do
      printf 'selftest case=E%s positive=pass mutants=1/1 verdict=pass\n' "$i"
      printf 'selftest detail=E%s mutant=fake rejected=1 limb=x\n' "$i"
    done
    printf 'selftest case=E1 positive=pass mutants=1/1 verdict=pass\n'
    printf 'selftest detail=E1 mutant=fake rejected=1 limb=x\n'
    printf 'selftest cases=14 failures=0\n'
  } > "$WORK/forge-duplicate-id.txt"
  if judge_selftest_report "$WORK/forge-duplicate-id.txt"; then
    printf 'selftest judge=forged-duplicate-id rejected=0\n'; rc=1
  else
    printf 'selftest judge=forged-duplicate-id rejected=1\n'
  fi

  if [ "$CASES" -ne 14 ]; then
    printf 'selftest problem=cases=%s expected=14\n' "$CASES"
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
        printf 'r37-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r37-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
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
