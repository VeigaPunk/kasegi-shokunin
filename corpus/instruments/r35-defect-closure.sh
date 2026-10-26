#!/usr/bin/env bash
# r35-defect-closure.sh — C1 closure counter for the seven round-34
# verifier-routed defects D1-D7 (`corpus/lessons/round-34-verifier-spotcheck.md`
# §6). One check function per defect; each check exits 0 when its defect is
# CLOSED and non-zero while it is still OPEN, so the suite is a fail-closed gate
# over the landed tree.
#
# Usage:
#   bash corpus/instruments/r35-defect-closure.sh
#       Plain run against the lane root (the absolute path below). Prints one
#       `D<i> check=<payload> open=0|1` line per defect and a final
#       `closed=K/7 exit=0|1`; exit 0 only for K=7.
#   bash corpus/instruments/r35-defect-closure.sh --root DIR
#       The same seven checks against another tree (e.g. a `git archive`
#       extraction of the lane base): the base-bytes run must read
#       `closed=0/7 exit=1`, because all seven defects are open there.
#   bash corpus/instruments/r35-defect-closure.sh --selftest
#       For each check: (a) run it on the tree under test — the lane root, or the
#       `--root DIR` given (so `--root <all-fixed tree> --selftest` is the
#       green-path run) — and it must pass;
#       (b) run it on the committed defect fixture `corpus/instruments/
#       r35-fixtures/D<i>` — it must be rejected, and the rejection must name
#       that defect's own clause; (c) run it on one scratch mutant per clause —
#       a copy of the LIVE inputs with exactly that one clause reopened — and
#       require rejection with every other clause still reading closed, so the
#       failure is attributable to the reopened clause alone. Each fixture tree is
#       measured as its own git worktree: copied to scratch, `git init` +
#       `git add -A`, so a fixture `.gitignore` is honoured and D4's tracking limb
#       reads the fixture rather than the enclosing lane worktree. Two committed
#       controls are then run over all seven checks: `r35-fixtures/clean` must
#       pass 7/7 and `r35-fixtures/two-defect/D1D2` must fail exactly D1 and D2.
#       Because a fixture breaks one limb only, the other six checks must pass on
#       that same tree — the case line reports that as `others=6/6`, so a rejection
#       is attributable to the broken limb rather than to a shared gap. There are
#       seventeen mutants in all: every clause of every check has one. The one
#       cascading mutant (D5's `-erratum-file`, which removes the erratum file)
#       necessarily takes the two statement clauses with it, so it is credited on
#       the rejection naming the absent file rather than on the closed-other-clauses
#       rule, and its detail line carries `cascade=1`.
#       Prints one `selftest case=D<i> live=... fixture=... mutants=n/n others=6/6
#       verdict=...` line per defect, one `selftest detail=` line per fixture and
#       mutant run, the two `selftest control=` lines, and `selftest cases=7
#       failures=0` only when every check passes live, rejects its own fixture with
#       the other six passing on it, passes all of its clause mutants and both
#       controls agree.
#
# Documented limit (not a live blind spot). D1's placeholder clause matches the
# two spellings the round-34 spot-check and this round's kill rule name literally:
# `filled by the L1` (the recurrence at SCORECARD.md:1242) and the `<LANE_HASH>`
# token (the round-33 spelling). The other round-34 placeholder was prose —
# "the L1 fills this line in the closing commit" — and a literal matcher cannot
# cover prose placeholders without matching legitimate prose that quotes them, so
# that spelling is measured as 0 at base and at tip rather than asserted. The
# residue is the spelling-brittleness the spot-check flagged for R1; it is
# recorded, not hidden (round-35 reviewer observation 1).
#
# The seven checks:
#   D1  SCORECARD.md carries 0 `filled by the L1` placeholder lines, 0 literal
#       `<LANE_HASH>` marker tokens (the two spellings the round-34 R1 check
#       missed), AND >=1 citation of the round-34 tip hash `c1c6a5f` (the
#       appended correction).
#   D2  SCORECARD.md carries the appended round-34 depth:density-row erratum:
#       `round-34 depth:density row` >=1 AND the corrected mean `201.2` >=1 AND
#       the stale row's own opening bytes still present verbatim (the stale row
#       is corrected by appending, not by rewriting it in place — the
#       append-only reading of "diff shows 0 deletions" for that row, which a
#       `git diff --numstat` deletion count cannot express on a git-free export).
#   D3  SKILL.md registers both round-34 instruments at the Gates & probes
#       registry home: `r-defect-closure` >=1 AND `kill-rule-check` >=1.
#   D4  `.ufo/waves/round-34/wave1-results.json` is tracked
#       (`git ls-files ... | wc -l` == 1) AND the provenance note
#       `...wave1-results.json.provenance.md` exists beside it.
#   D5  `.ufo/waves/round-35/claims-erratum-d5.md` exists AND carries the
#       `discriminating invocation` and `per-id occurrences` statements.
#   D6  `.ufo/waves/round-34/wave1/L1Integration.md` no longer carries the stale
#       dead-seat sentence (`did not file a receipt (dead seat` == 0) AND carries
#       the appended `Correction (round 35)` note.
#   D7  corpus/QUALITY.md carries both appended supersession rows
#       (`supersedes R22` >=1 AND `supersedes R23` >=1).
#
# Do-nothing control and the discriminator (C1). The fakes under
# `.ufo/waves/round-34/c1-controls/fake-suite.sh` (and the round-35 fake beside
# it, when present) print a claimed summary — `closed=9/9 exit=0` / `closed=7/7
# exit=0`, and for `--selftest` a bare `cases=N failures=0` — while performing no
# check at all. They cannot satisfy this suite's own judgement: `report_ok`
# re-parses the selftest report and requires exactly seven distinct
# `selftest case=D<i>` lines with `live=pass fixture=rejected`, a per-defect
# fixture `reason=` that matches that defect's clause semantics, at least one
# mutant detail line per defect, and a case-line mutant count equal to the number
# of detail lines. A summary line alone contains no case line, so it is rejected;
# the same judgement is re-proved on two machine-generated forgeries and on the
# fake suites themselves (`selftest judge=forged-summary|forged-caselines|
# short-report|fake-suite|fake-plain rejected=1`). `plain_report_ok` applies the
# same rule to the plain run: seven named `D<i> check=...` lines and a summary
# that agrees with their open counts.
#
# Read-only: every check only reads files under its root, and the plain run writes
# nothing at all. Its one git invocation is `git ls-files` (an index read, no git
# mutation; D4 cannot be counted any other way, and it is the frozen counting
# command). The only writes are the scratch trees `--selftest` builds under
# ${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}, removed on exit; the two D4 mutants run
# `git init` + `git add` inside that scratch directory only. Nothing outside the
# scratch directory is written, and no git mutation ever touches the lane repo.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (bad argument, unreadable root or scratch base).
set -uo pipefail

LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SELF_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
FIXTURES=$SELF_DIR/r35-fixtures
RD_ROOT=$LANE_ROOT
MODE=run
SCRATCH_BASE=${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}

usage() {
  cat <<'EOF'
usage: bash corpus/instruments/r35-defect-closure.sh [--root DIR] [--selftest]

  (no argument)  run the seven D1-D7 closure checks against the lane root;
                 prints `D<i> check=<payload> open=0|1` and `closed=K/7 exit=0|1`
  --root DIR     run them against another tree (base export -> `closed=0/7 exit=1`)
  --selftest     live pass + committed defect fixture rejection + one scratch
                 mutant per clause; prints `selftest cases=7 failures=0`.
                 The "live" tree is DIR when --root is given (default: the lane
                 root), so `--root <all-fixed tree> --selftest` is the green-path
                 run; the defect fixtures are always the committed ones beside
                 this script.
EOF
}

while [ $# -gt 0 ]; do
  case $1 in
    --root)
      [ $# -ge 2 ] || { printf 'r35-defect-closure: --root needs a directory\n' >&2; exit 2; }
      RD_ROOT=$2
      shift 2
      ;;
    --selftest)
      MODE=selftest
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'r35-defect-closure: unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
done

if [ ! -d "$RD_ROOT" ]; then
  printf 'r35-defect-closure: root is not a directory: %s\n' "$RD_ROOT" >&2
  exit 2
fi

# --- D1 ----------------------------------------------------------------------
check_d1() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local ph lh cor
    ph=$(grep -c -F -- 'filled by the L1' SCORECARD.md 2>/dev/null); ph=${ph:-0}
    lh=$(grep -c -F -- '<LANE''_HASH>' SCORECARD.md 2>/dev/null); lh=${lh:-0}
    cor=$(grep -c -F -- 'c1c6a5f' SCORECARD.md 2>/dev/null); cor=${cor:-0}
    printf 'placeholders=%s,lane-hash-markers=%s,correction-c1c6a5f=%s' "$ph" "$lh" "$cor"
    [ "$ph" -eq 0 ] && [ "$lh" -eq 0 ] && [ "$cor" -ge 1 ] && exit 0
    exit 1
  )
}

# --- D2 ----------------------------------------------------------------------
check_d2() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local er mean row
    er=$(grep -c -F -- 'round-34 depth:density row' SCORECARD.md 2>/dev/null); er=${er:-0}
    mean=$(grep -c -F -- '201.2' SCORECARD.md 2>/dev/null); mean=${mean:-0}
    row=$(grep -c -E -- '^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances' SCORECARD.md 2>/dev/null); row=${row:-0}
    printf 'erratum-row=%s,erratum-mean=%s,row-bytes=%s' "$er" "$mean" "$row"
    [ "$er" -ge 1 ] && [ "$mean" -ge 1 ] && [ "$row" -ge 1 ] && exit 0
    exit 1
  )
}

# --- D3 ----------------------------------------------------------------------
check_d3() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local rdc krc
    rdc=$(grep -c -F -- 'r-defect-closure' SKILL.md 2>/dev/null); rdc=${rdc:-0}
    krc=$(grep -c -F -- 'kill-rule-check' SKILL.md 2>/dev/null); krc=${krc:-0}
    printf 'registry-r-defect-closure=%s,registry-kill-rule=%s' "$rdc" "$krc"
    [ "$rdc" -ge 1 ] && [ "$krc" -ge 1 ] && exit 0
    exit 1
  )
}

# --- D4 ----------------------------------------------------------------------
check_d4() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local tracked prov
    tracked=$(git ls-files -- .ufo/waves/round-34/wave1-results.json 2>/dev/null | wc -l)
    tracked=$(printf '%s' "${tracked:-0}" | tr -dc '0-9'); tracked=${tracked:-0}
    if [ -f .ufo/waves/round-34/wave1-results.json.provenance.md ]; then prov=1; else prov=0; fi
    printf 'tracked=%s,provenance=%s' "$tracked" "$prov"
    [ "$tracked" -eq 1 ] && [ "$prov" -eq 1 ] && exit 0
    exit 1
  )
}

# --- D5 ----------------------------------------------------------------------
check_d5() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local ef=absent disc occ
    disc=0
    occ=0
    if [ -f .ufo/waves/round-35/claims-erratum-d5.md ]; then
      ef=present
      disc=$(grep -c -F -- 'discriminating invocation' .ufo/waves/round-35/claims-erratum-d5.md 2>/dev/null); disc=${disc:-0}
      occ=$(grep -c -F -- 'per-id occurrences' .ufo/waves/round-35/claims-erratum-d5.md 2>/dev/null); occ=${occ:-0}
    fi
    printf 'erratum-file=%s,discriminating-invocation=%s,per-id-occurrences=%s' "$ef" "$disc" "$occ"
    [ "$ef" = present ] && [ "$disc" -ge 1 ] && [ "$occ" -ge 1 ] && exit 0
    exit 1
  )
}

# --- D6 ----------------------------------------------------------------------
check_d6() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local stale corr
    stale=$(grep -c -F -- 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md 2>/dev/null); stale=${stale:-0}
    corr=$(grep -c -F -- 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md 2>/dev/null); corr=${corr:-0}
    printf 'dead-seat-sentence=%s,correction-round-35=%s' "$stale" "$corr"
    [ "$stale" -eq 0 ] && [ "$corr" -ge 1 ] && exit 0
    exit 1
  )
}

# --- D7 ----------------------------------------------------------------------
check_d7() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    local r22 r23
    r22=$(grep -c -F -- 'supersedes R22' corpus/QUALITY.md 2>/dev/null); r22=${r22:-0}
    r23=$(grep -c -F -- 'supersedes R23' corpus/QUALITY.md 2>/dev/null); r23=${r23:-0}
    printf 'supersedes-R22=%s,supersedes-R23=%s' "$r22" "$r23"
    [ "$r22" -ge 1 ] && [ "$r23" -ge 1 ] && exit 0
    exit 1
  )
}

# --- clause table ------------------------------------------------------------
# clause_specs ID: one `LABEL<TAB>OPEN_RE<TAB>CLOSED_RE` line per clause of that
# check. OPEN_RE matches the payload when that clause is still open, CLOSED_RE
# when it is closed; `isolate_ok` uses the closed forms to prove that a mutant
# reopened exactly one clause and nothing else.
clause_specs() {
  case $1 in
    D1) printf '%s\t%s\t%s\n' \
          'placeholders' 'placeholders=[1-9]' 'placeholders=0' \
          'lane-hash-markers' 'lane-hash-markers=[1-9]' 'lane-hash-markers=0' \
          'correction-c1c6a5f' 'correction-c1c6a5f=0' 'correction-c1c6a5f=[1-9]'
        ;;
    D2) printf '%s\t%s\t%s\n' \
          'erratum-row' 'erratum-row=0' 'erratum-row=[1-9]' \
          'erratum-mean' 'erratum-mean=0' 'erratum-mean=[1-9]' \
          'row-bytes' 'row-bytes=0' 'row-bytes=[1-9]'
        ;;
    D3) printf '%s\t%s\t%s\n' \
          'registry-r-defect-closure' 'registry-r-defect-closure=0' 'registry-r-defect-closure=[1-9]' \
          'registry-kill-rule' 'registry-kill-rule=0' 'registry-kill-rule=[1-9]'
        ;;
    D4) printf '%s\t%s\t%s\n' \
          'tracked' 'tracked=0' 'tracked=1' \
          'provenance' 'provenance=0' 'provenance=1'
        ;;
    D5) printf '%s\t%s\t%s\n' \
          'erratum-file' 'erratum-file=absent' 'erratum-file=present' \
          'discriminating-invocation' 'discriminating-invocation=0' 'discriminating-invocation=[1-9]' \
          'per-id-occurrences' 'per-id-occurrences=0' 'per-id-occurrences=[1-9]'
        ;;
    D6) printf '%s\t%s\t%s\n' \
          'dead-seat-sentence' 'dead-seat-sentence=[1-9]' 'dead-seat-sentence=0' \
          'correction-round-35' 'correction-round-35=0' 'correction-round-35=[1-9]'
        ;;
    D7) printf '%s\t%s\t%s\n' \
          'supersedes-R22' 'supersedes-R22=0' 'supersedes-R22=[1-9]' \
          'supersedes-R23' 'supersedes-R23=0' 'supersedes-R23=[1-9]'
        ;;
    *) return 1 ;;
  esac
}

# fix_re ID: the clause pattern the committed defect fixture D<i> must exhibit.
# Each pattern is the limb's own clause at its open value, so a fixture that is
# rejected for an unrelated reason does not count as a pass. The D4 fixture
# breaks the provenance limb (it carries the results file and a .gitignore naming
# it, so the tracked limb is proved by the `clean` control instead, and the
# no-git direction by the base-tree run).
fix_re() {
  case $1 in
    D1) printf '%s' 'placeholders=[1-9]' ;;
    D2) printf '%s' 'erratum-row=0' ;;
    D3) printf '%s' 'registry-r-defect-closure=0' ;;
    D4) printf '%s' 'provenance=0' ;;
    D5) printf '%s' 'per-id-occurrences=0' ;;
    D6) printf '%s' 'dead-seat-sentence=[1-9]' ;;
    D7) printf '%s' 'supersedes-R22=0' ;;
    *) return 1 ;;
  esac
}

# mutant_specs ID: one `NAME<TAB>CLAUSE_LABEL[<TAB>cascade]` line per scratch
# mutant — the clause that mutant reopens. Every clause of every check has exactly
# one mutant. A mutant marked `cascade` reopens a precondition whose violation
# forces the dependent clauses to their open values too (D5's erratum file: with
# the file absent the two statements cannot be found either), so it is credited on
# the rejection naming that clause instead of on the closed-other-clauses rule.
mutant_specs() {
  case $1 in
    D1) printf '%s\t%s\n' \
          '+placeholders' 'placeholders' \
          '+lane-hash-markers' 'lane-hash-markers' \
          '-c1c6a5f' 'correction-c1c6a5f' ;;
    D2) printf '%s\t%s\n' \
          '-erratum-row' 'erratum-row' \
          '-erratum-mean' 'erratum-mean' \
          '-row-bytes' 'row-bytes' ;;
    D3) printf '%s\t%s\n' \
          '-registry-r-defect-closure' 'registry-r-defect-closure' \
          '-registry-kill-rule' 'registry-kill-rule' ;;
    D4) printf '%s\t%s\n' '-tracked' 'tracked' '-provenance' 'provenance' ;;
    D5) printf '%s\t%s\t%s\n' \
          '-erratum-file' 'erratum-file' 'cascade' \
          '-discriminating-invocation' 'discriminating-invocation' '' \
          '-per-id-occurrences' 'per-id-occurrences' ''
        ;;
    D6) printf '%s\t%s\n' \
          '+dead-seat-sentence' 'dead-seat-sentence' \
          '-correction-round-35' 'correction-round-35' ;;
    D7) printf '%s\t%s\n' \
          '-supersedes-R22' 'supersedes-R22' \
          '-supersedes-R23' 'supersedes-R23' ;;
    *) return 1 ;;
  esac
}

# --- driver ------------------------------------------------------------------

CHECK_IDS=(D1 D2 D3 D4 D5 D6 D7)
CHECK_FNS=(check_d1 check_d2 check_d3 check_d4 check_d5 check_d6 check_d7)

copy_live() { # REL DEST — copies from the tree under test (--root), not always the lane
  local rel=$1 dest=$2
  [ -f "$RD_ROOT/$rel" ] || return 1
  mkdir -p "$dest/$(dirname -- "$rel")"
  cp -p "$RD_ROOT/$rel" "$dest/$rel"
}

filter_out() { # FILE FIXED_STRING
  local f=$1 pat=$2
  grep -v -F -- "$pat" "$f" >"$f.tmp" || true
  mv "$f.tmp" "$f"
}

# build_mutant ID NAME DEST: a scratch tree holding only the files that check
# reads, copied from the LIVE tree, with exactly that one clause reopened. The
# other clauses keep their live (closed) values, which is what makes the
# rejection attributable (see `isolate_ok`).
build_mutant() { # ID NAME DEST
  local id=$1 name=$2 dest=$3
  mkdir -p "$dest" || return 1
  case "$id:$name" in
    D1:+placeholders)
      copy_live SCORECARD.md "$dest" || return 1
      printf '\n**Round-34 final lane commit: filled by the L1 in the closing commit.**\n' \
        >>"$dest/SCORECARD.md"
      ;;
    D1:+lane-hash-markers)
      copy_live SCORECARD.md "$dest" || return 1
      printf '\n**Final lane commit: <%s>**\n' 'LANE''_HASH' >>"$dest/SCORECARD.md"
      ;;
    D1:-c1c6a5f)
      copy_live SCORECARD.md "$dest" || return 1
      filter_out "$dest/SCORECARD.md" 'c1c6a5f'
      ;;
    D2:-erratum-row)
      copy_live SCORECARD.md "$dest" || return 1
      filter_out "$dest/SCORECARD.md" 'round-34 depth:density row'
      ;;
    D2:-erratum-mean)
      copy_live SCORECARD.md "$dest" || return 1
      sed -i 's/201\.2/201.9/g' "$dest/SCORECARD.md" || return 1
      ;;
    D2:-row-bytes)
      copy_live SCORECARD.md "$dest" || return 1
      sed -i 's/mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances/mean **201.9**, 25 blocks, 710 path-citation instances/' \
        "$dest/SCORECARD.md" || return 1
      ;;
    D3:-registry-r-defect-closure)
      copy_live SKILL.md "$dest" || return 1
      filter_out "$dest/SKILL.md" 'r-defect-closure'
      ;;
    D3:-registry-kill-rule)
      copy_live SKILL.md "$dest" || return 1
      filter_out "$dest/SKILL.md" 'kill-rule-check'
      ;;
    D4:-tracked)
      copy_live .ufo/waves/round-34/wave1-results.json "$dest" || return 1
      copy_live .ufo/waves/round-34/wave1-results.json.provenance.md "$dest" || return 1
      git init -q "$dest" >/dev/null 2>&1 || return 1
      git -C "$dest" add -- .ufo/waves/round-34/wave1-results.json.provenance.md >/dev/null 2>&1 || return 1
      ;;
    D4:-provenance)
      copy_live .ufo/waves/round-34/wave1-results.json "$dest" || return 1
      git init -q "$dest" >/dev/null 2>&1 || return 1
      git -C "$dest" add -- .ufo/waves/round-34/wave1-results.json >/dev/null 2>&1 || return 1
      ;;
    D5:-erratum-file)
      # the defect itself: the erratum file does not exist (its directory does)
      mkdir -p "$dest/.ufo/waves/round-35" || return 1
      ;;
    D5:-discriminating-invocation)
      copy_live .ufo/waves/round-35/claims-erratum-d5.md "$dest" || return 1
      filter_out "$dest/.ufo/waves/round-35/claims-erratum-d5.md" 'discriminating invocation'
      ;;
    D5:-per-id-occurrences)
      copy_live .ufo/waves/round-35/claims-erratum-d5.md "$dest" || return 1
      filter_out "$dest/.ufo/waves/round-35/claims-erratum-d5.md" 'per-id occurrences'
      ;;
    D6:+dead-seat-sentence)
      copy_live .ufo/waves/round-34/wave1/L1Integration.md "$dest" || return 1
      printf '%s\n' '- The round-33 summary `ExecRegressionC1` did not file a receipt (dead seat, 1 of 65); the' \
        >>"$dest/.ufo/waves/round-34/wave1/L1Integration.md"
      ;;
    D6:-correction-round-35)
      copy_live .ufo/waves/round-34/wave1/L1Integration.md "$dest" || return 1
      filter_out "$dest/.ufo/waves/round-34/wave1/L1Integration.md" 'Correction (round 35)'
      ;;
    D7:-supersedes-R22)
      copy_live corpus/QUALITY.md "$dest" || return 1
      filter_out "$dest/corpus/QUALITY.md" 'supersedes R22'
      ;;
    D7:-supersedes-R23)
      copy_live corpus/QUALITY.md "$dest" || return 1
      filter_out "$dest/corpus/QUALITY.md" 'supersedes R23'
      ;;
    *)
      return 1
      ;;
  esac
}

# clause_open_re ID LABEL: print that clause's open-form regex.
clause_open_re() {
  local label open_re closed_re
  while IFS=$'\t' read -r label open_re closed_re; do
    [ -n "${label:-}" ] || continue
    if [ "$label" = "$2" ]; then
      printf '%s' "$open_re"
      return 0
    fi
  done < <(clause_specs "$1")
  return 1
}

# isolate_ok ID LABEL PAYLOAD: the payload must show LABEL open and every other
# clause of the same check closed.
isolate_ok() {
  local id=$1 want=$2 payload=$3 label open_re closed_re
  while IFS=$'\t' read -r label open_re closed_re; do
    [ -n "${label:-}" ] || continue
    if [ "$label" = "$want" ]; then
      printf '%s' "$payload" | grep -Eq -- "$open_re" || return 1
    else
      printf '%s' "$payload" | grep -Eq -- "$closed_re" || return 1
    fi
  done < <(clause_specs "$id")
  return 0
}

run_check() { # ROOT FN -> sets PAYLOAD, returns the check status
  local root=$1 fn=$2
  PAYLOAD=$("$fn" "$root")
  return $?
}

run_plain() {
  local i id rc closed=0 open
  for i in "${!CHECK_IDS[@]}"; do
    id=${CHECK_IDS[$i]}
    run_check "$RD_ROOT" "${CHECK_FNS[$i]}"
    rc=$?
    if [ "$rc" -eq 0 ]; then
      open=0
      closed=$((closed + 1))
      printf '%s check=%s open=0\n' "$id" "${PAYLOAD:-undescribed}"
    elif [ "$rc" -eq 2 ]; then
      printf '%s check=%s harness-error=1 open=1\n' "$id" "${PAYLOAD:-undescribed}"
    else
      open=1
      printf '%s check=%s open=1\n' "$id" "${PAYLOAD:-undescribed}"
    fi
  done
  if [ "$closed" -eq 7 ]; then
    printf 'closed=7/7 exit=0\n'
    return 0
  fi
  printf 'closed=%d/7 exit=1\n' "$closed"
  return 1
}

# report_ok REPORT: exit 0 only for the complete seven-case evidence form this
# suite's own selftest produces — summary lines are not evidence, and a case line
# must be backed by fixture and mutant detail lines that agree with it.
report_ok() {
  local report=$1 lines ids id n mc
  lines=$(printf '%s\n' "$report" \
    | grep -cE '^selftest case=D[1-7] live=pass fixture=rejected mutants=[0-9]+/[0-9]+ others=6/6 verdict=pass$' || true)
  [ "${lines:-0}" -eq 7 ] || return 1
  ids=$(printf '%s\n' "$report" | sed -n 's/^selftest case=\(D[1-7]\) .*/\1/p' | sort -u | tr '\n' ' ')
  [ "$ids" = "D1 D2 D3 D4 D5 D6 D7 " ] || return 1
  for id in "${CHECK_IDS[@]}"; do
    printf '%s\n' "$report" \
      | grep -Eq "^selftest detail=$id fixture reason=.*$(fix_re "$id")" || return 1
    n=$(printf '%s\n' "$report" | grep -cE "^selftest detail=$id mutant=[^ ]+ reason=" || true)
    [ "${n:-0}" -ge 1 ] || return 1
    mc=$(printf '%s\n' "$report" \
      | sed -n "s/^selftest case=$id .*mutants=\([0-9][0-9]*\)\/\([0-9][0-9]*\) .*/\1/p" | head -1)
    [ "${mc:-0}" = "$n" ] || return 1
  done
  printf '%s\n' "$report" | grep -qx 'selftest cases=7 failures=0'
}

# plain_report_ok REPORT: same judgement for the plain run — seven named check
# lines, one per defect id, and a summary that agrees with their open counts.
plain_report_ok() {
  local report=$1 ids lines closed
  lines=$(printf '%s\n' "$report" | grep -cE '^D[1-7] check=[^ ]+( harness-error=1)? open=[01]$' || true)
  [ "${lines:-0}" -eq 7 ] || return 1
  ids=$(printf '%s\n' "$report" | sed -n 's/^\(D[1-7]\) check=.*/\1/p' | sort -u | tr '\n' ' ')
  [ "$ids" = "D1 D2 D3 D4 D5 D6 D7 " ] || return 1
  closed=$(printf '%s\n' "$report" | grep -c ' open=0$' || true)
  closed=${closed:-0}
  if [ "$closed" -eq 7 ]; then
    printf '%s\n' "$report" | grep -qx 'closed=7/7 exit=0'
  else
    printf '%s\n' "$report" | grep -qx "closed=${closed}/7 exit=1"
  fi
}

judge_selftest_report() { # REPORT STATUS
  local report=$1 status=$2 forged7="" id f fout pout
  # 1. A claimed summary with no case lines.
  if report_ok 'selftest cases=7 failures=0'; then
    printf 'selftest problem=judge forged-summary accepted\n'
    return 1
  fi
  printf 'selftest judge=forged-summary rejected=1\n'
  # 2. A shape-complete forgery whose case lines claim mutants=0/0 while the
  #    detail lines exist: the mutant-count cross-check must reject it.
  for id in "${CHECK_IDS[@]}"; do
    forged7+="selftest detail=$id fixture reason=$(fix_re "$id")"$'\n'
    forged7+="selftest detail=$id mutant=forged reason=forged"$'\n'
    forged7+="selftest case=$id live=pass fixture=rejected mutants=0/0 others=6/6 verdict=pass"$'\n'
  done
  forged7+='selftest cases=7 failures=0'
  if report_ok "$forged7"; then
    printf 'selftest problem=judge forged-caselines accepted\n'
    return 1
  fi
  printf 'selftest judge=forged-caselines rejected=1\n'
  # 3. A report short one case (and its details).
  if report_ok "$(printf '%s\n' "$report" | grep -v '^selftest case=D7 \|^selftest detail=D7 ')"; then
    printf 'selftest problem=judge short-report accepted\n'
    return 1
  fi
  printf 'selftest judge=short-report rejected=1\n'
  # 4. The committed do-nothing controls: a summary-only fake must be rejected
  #    both as a selftest report and as a plain report.
  f=""
  for candidate in \
    "$RD_ROOT/.ufo/waves/round-35/c1-controls/fake-suite.sh" \
    "$LANE_ROOT/.ufo/waves/round-35/c1-controls/fake-suite.sh" \
    "$RD_ROOT/.ufo/waves/round-34/c1-controls/fake-suite.sh" \
    "$LANE_ROOT/.ufo/waves/round-34/c1-controls/fake-suite.sh"; do
    if [ -f "$candidate" ]; then f=$candidate; break; fi
  done
  if [ -n "$f" ]; then
    fout=$(bash "$f" --selftest 2>/dev/null)
    pout=$(bash "$f" 2>/dev/null)
    if report_ok "$fout"; then
      printf 'selftest problem=judge fake-suite accepted path=%s\n' "$f"
      return 1
    fi
    printf 'selftest judge=fake-suite rejected=1 path=%s output=%s\n' \
      "$(printf '%s' "$f" | sed -e "s#^$LANE_ROOT/##" -e "s#^$RD_ROOT/##")" \
      "$(printf '%s' "$fout" | tr '\n' ';')"
    if plain_report_ok "$pout"; then
      printf 'selftest problem=judge fake-plain accepted path=%s\n' "$f"
      return 1
    fi
    printf 'selftest judge=fake-plain rejected=1 output=%s\n' "$(printf '%s' "$pout" | tr '\n' ';')"
  else
    printf 'selftest judge=fake-suite absent=1\n'
  fi
  # 5. The real report.
  if [ "$status" -ne 0 ]; then
    printf 'selftest problem=self-report status=%d\n' "$status"
    return 1
  fi
  if ! report_ok "$report"; then
    printf 'selftest problem=self-report cases=%s expected=7\n' \
      "$(printf '%s\n' "$report" | grep -c '^selftest case=' || true)"
    return 1
  fi
  printf 'selftest judge=complete-report accepted=1\n'
  return 0
}

# materialize SRC DEST: a scratch copy of a committed fixture tree, with its own
# throwaway git repo and the index built by `git add -A` (so a fixture's
# .gitignore is honoured and `git ls-files` measures the fixture, not the
# enclosing lane worktree).
materialize() { # SRC DEST
  local src=$1 dest=$2
  [ -d "$src" ] || return 1
  mkdir -p "$dest" || return 1
  cp -a "$src/." "$dest/" || return 1
  git init -q "$dest" >/dev/null 2>&1 || return 1
  git -C "$dest" add -A >/dev/null 2>&1 || return 1
  return 0
}

run_selftest() {
  local scratch
  scratch=$(mktemp -d "$SCRATCH_BASE/r35-closure.XXXXXX") || {
    printf 'selftest problem=scratch-base path=%s\n' "$SCRATCH_BASE"
    return 2
  }
  trap 'rm -rf -- "$scratch"' RETURN
  local i id fn live_out live_rc fix_out fix_rc case_ok live_state fix_state
  local name label cascade dest mout mrc mtotal mok j oout orc oth oth_failed
  local failures=0
  for i in "${!CHECK_IDS[@]}"; do
    id=${CHECK_IDS[$i]}
    fn=${CHECK_FNS[$i]}
    case_ok=1
    oth=0
    oth_failed=""
    # (a) live tree: the check must pass.
    live_out=$("$fn" "$RD_ROOT")
    live_rc=$?
    if [ "$live_rc" -eq 0 ]; then
      live_state=pass
    else
      live_state=fail
      case_ok=0
    fi
    # (b) committed defect fixture: must be rejected on this defect's clause.
    # The fixture is measured as its own git worktree (a scratch copy with
    # `git init` + `git add -A`), so D4's tracking limb reads the fixture and a
    # fixture .gitignore is honoured.
    fixroot=$scratch/fixture-$id
    if ! materialize "$FIXTURES/$id" "$fixroot"; then
      case_ok=0
      fix_state=unusable
      printf 'selftest problem=fixture-missing id=%s path=%s\n' "$id" "${FIXTURES#"$LANE_ROOT"/}/$id"
    else
      fix_out=$("$fn" "$fixroot")
      fix_rc=$?
      if [ "$fix_rc" -ne 0 ] && printf '%s' "$fix_out" | grep -Eq -- "$(fix_re "$id")"; then
        fix_state=rejected
        printf 'selftest detail=%s fixture reason=%s\n' "$id" "$fix_out"
      else
        fix_state=pass
        case_ok=0
        printf 'selftest detail=%s fixture reason=%s verdict=unexpected rc=%d\n' "$id" "$fix_out" "$fix_rc"
      fi
      # The fixture breaks one limb only: the other six checks must pass on it,
      # so a rejection is attributable to that limb and not to a shared gap.
      oth=0
      oth_failed=""
      for j in "${!CHECK_IDS[@]}"; do
        [ "${CHECK_IDS[$j]}" = "$id" ] && continue
        oout=$("${CHECK_FNS[$j]}" "$fixroot")
        orc=$?
        if [ "$orc" -eq 0 ]; then
          oth=$((oth + 1))
        else
          oth_failed+="${CHECK_IDS[$j]} "
        fi
      done
      if [ "$oth" -ne 6 ]; then
        case_ok=0
        printf 'selftest detail=%s others passed=%d/6 failed=%s\n' \
          "$id" "$oth" "$(printf '%s' "${oth_failed:-none}" | tr ' ' ',')"
      fi
    fi
    # (c) one scratch mutant per clause, built from the live bytes.
    mtotal=0
    mok=0
    while IFS=$'\t' read -r name label cascade; do
      [ -n "${name:-}" ] || continue
      cascade=${cascade:-}
      mtotal=$((mtotal + 1))
      dest=$scratch/$id-$name
      if ! build_mutant "$id" "$name" "$dest"; then
        case_ok=0
        printf 'selftest problem=mutant-build id=%s name=%s\n' "$id" "$name"
        continue
      fi
      mout=$("$fn" "$dest")
      mrc=$?
      if [ "$mrc" -eq 0 ]; then
        case_ok=0
        printf 'selftest detail=%s mutant=%s reason=%s verdict=unexpected rc=0\n' \
          "$id" "$label" "$mout"
      elif [ "$cascade" = cascade ]; then
        if printf '%s' "$mout" | grep -Eq -- "$(clause_open_re "$id" "$label")"; then
          mok=$((mok + 1))
          printf 'selftest detail=%s mutant=%s reason=%s cascade=1\n' "$id" "$label" "$mout"
        else
          case_ok=0
          printf 'selftest detail=%s mutant=%s reason=%s verdict=unexpected rc=%d\n' \
            "$id" "$label" "$mout" "$mrc"
        fi
      elif isolate_ok "$id" "$label" "$mout"; then
        mok=$((mok + 1))
        printf 'selftest detail=%s mutant=%s reason=%s\n' "$id" "$label" "$mout"
      else
        case_ok=0
        printf 'selftest detail=%s mutant=%s reason=%s verdict=unexpected rc=%d\n' \
          "$id" "$label" "$mout" "$mrc"
      fi
    done < <(mutant_specs "$id")
    if [ "$case_ok" -eq 1 ]; then
      printf 'selftest case=%s live=%s fixture=%s mutants=%d/%d others=%d/6 verdict=pass\n' \
        "$id" "$live_state" "$fix_state" "$mok" "$mtotal" "$oth"
    else
      failures=$((failures + 1))
      printf 'selftest case=%s live=%s fixture=%s mutants=%d/%d others=%d/6 verdict=fail\n' \
        "$id" "$live_state" "$fix_state" "$mok" "$mtotal" "$oth"
      printf 'selftest detail=%s live-reason=%s\n' "$id" "${live_out:-empty}"
    fi
  done
  # Controls (committed beside the fixtures): `clean` must pass all seven
  # checks and `two-defect/D1D2` must fail exactly D1 and D2. Together they show
  # the suite is neither always-reject nor blind to which limb broke.
  local controls_ok=1 croot cid cfn cout crc cclosed cfailed
  croot=$scratch/control-clean
  if materialize "$FIXTURES/clean" "$croot"; then
    cclosed=0
    cfailed=""
    for i in "${!CHECK_IDS[@]}"; do
      cid=${CHECK_IDS[$i]}
      cfn=${CHECK_FNS[$i]}
      cout=$("$cfn" "$croot")
      crc=$?
      if [ "$crc" -eq 0 ]; then
        cclosed=$((cclosed + 1))
      else
        cfailed+="$cid "
      fi
    done
    if [ "$cclosed" -eq 7 ]; then
      printf 'selftest control=clean closed=7/7 verdict=pass\n'
    else
      controls_ok=0
      printf 'selftest control=clean closed=%d/7 failed=%s verdict=fail\n' \
        "$cclosed" "$(printf '%s' "${cfailed:-none}" | tr ' ' ',')"
    fi
  else
    controls_ok=0
    printf 'selftest problem=control-missing path=corpus/instruments/r35-fixtures/clean\n'
  fi
  cfailed=""
  croot=$scratch/control-two-defect
  if materialize "$FIXTURES/two-defect/D1D2" "$croot"; then
    cclosed=0
    for i in "${!CHECK_IDS[@]}"; do
      cid=${CHECK_IDS[$i]}
      cfn=${CHECK_FNS[$i]}
      cout=$("$cfn" "$croot")
      crc=$?
      if [ "$crc" -eq 0 ]; then
        cclosed=$((cclosed + 1))
      else
        cfailed+="$cid "
      fi
    done
    if [ "$cclosed" -eq 5 ] && [ "$cfailed" = "D1 D2 " ]; then
      printf 'selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass\n'
    else
      controls_ok=0
      printf 'selftest control=two-defect closed=%d/7 failed=%s verdict=fail\n' \
        "$cclosed" "$(printf '%s' "${cfailed:-none}" | tr ' ' ',')"
    fi
  else
    controls_ok=0
    printf 'selftest problem=control-missing path=corpus/instruments/r35-fixtures/two-defect/D1D2\n'
  fi
  if [ "$failures" -eq 0 ] && [ "$controls_ok" -eq 1 ]; then
    printf 'selftest cases=7 failures=0\n'
    return 0
  fi
  printf 'selftest cases=7 failures=%d control-failures=%d\n' \
    "$failures" "$((1 - controls_ok))"
  return 1
}

if [ "$MODE" = selftest ]; then
  REPORT=$(run_selftest)
  STATUS=$?
  printf '%s\n' "$REPORT"
  judge_selftest_report "$REPORT" "$STATUS" || exit 1
  exit "$STATUS"
fi

REPORT=$(run_plain)
STATUS=$?
printf '%s\n' "$REPORT"
if ! plain_report_ok "$REPORT"; then
  printf 'suite problem=self-report plain-lines=%s expected=7\n' \
    "$(printf '%s\n' "$REPORT" | grep -c '^D[1-7] check=' || true)"
  exit 1
fi
exit "$STATUS"
