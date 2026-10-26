#!/usr/bin/env bash
# r38-closure.sh — round-38 closure counter for claim C1 (depth:verifiability).
#
# Eight checks G1-G8. G1-G7 close the routed defects of the round-37 verifier
# spot-check (corpus/lessons/round-37-verifier-spotcheck.md §5: D-A, D-B, D-C,
# D3, D-D, D-E) plus the L1-found defect D-F, by reading the round-38 evidence
# bytes themselves; G8 carries the round-37 suite (r37-closure.sh E1-E14)
# forward and requires it to stay green on the same exported ref. Each check
# exits 0 when its defect is CLOSED and non-zero while it is still OPEN, so the
# suite is a fail-closed gate over the bytes of an exported commit.
#
# EXPORT MODE IS THE ONLY RUN MODE. `--export-ref <hash>` extracts the lane tree
# with
#   git -C <lane> archive <hash> | tar -xf - -C <work>/export
# and every check reads its bytes only under that export root. The only live
# reads are G6's scratch-root scan (host state by definition), G2's ancestry and
# post-receipt diff limbs and G3's added-lines limb, which are ref-scoped
# git reads against the lane repo (cat-file, merge-base --is-ancestor, diff,
# rev-parse) and cannot be answered from the export. Nothing is written under
# the lane; the only writes are the extraction and the selftest fixtures under
# --work (or a mktemp dir honouring TMPDIR), both removed on exit. --work must
# lie outside the lane; its `export/` and `mut/` subdirectories are cleared
# before use, so a reused work dir can never satisfy a check with stale bytes.
# A plain run (no --export-ref, no --selftest) refuses with exit 2, because a
# suite that reads the working tree can be turned green by edits that were never
# committed.
#
# Usage:
#   bash corpus/instruments/r38-closure.sh --export-ref <hash> [--lane DIR]
#        [--work DIR] [--scratch-root DIR]
#       Extract <hash> and run G1-G8 against the export. Prints one
#       `G<n> payload=<...> closed=0|1` line per check and a final
#       `closed=K/8 exit=0|1`; exit 0 only for K=8, exit 1 otherwise.
#   bash corpus/instruments/r38-closure.sh --selftest [--export-ref <hash>]
#        [--lane DIR] [--work DIR] [--scratch-root DIR]
#       Positive limb: every check must pass on the export (default: HEAD).
#       Mutant limb: for each check at least two scratch fixtures that reopen
#       exactly one clause must be REJECTED, and the rejection payload must name
#       the reopened limb, so a fixture proves the check discriminates rather
#       than that it can be satisfied by a summary. Prints one
#       `selftest case=G<i> positive=... mutants=<ok>/<n> verdict=...` line per
#       check, the `selftest detail=` lines behind them, the `selftest judge=`
#       lines (own report accepted, four forged reports rejected) and
#       `selftest cases=8 failures=<k>`; exit 0 only when all eight cases ran,
#       every positive passed and every mutant was rejected.
#   bash corpus/instruments/r38-closure.sh -h|--help
#       This text.
#
#   Plain run (no --export-ref, no --selftest) is refused: exit 2.
#
# The eight checks:
#   G1 (D-A) Front doors. In the export, PROVINCE.md and corpus/README.md each
#       carry >=1 line beginning `Correction (round 38)` that names the round-37
#       append range (PROVINCE: `L79-L152`; README: `L399-L454`) and contains the
#       word `misplaced`; a CommonMark fence walk over each whole file ends
#       CLOSED (a line matching `^ {0,3}``` ` opens a fence when closed — an info
#       string is allowed — and while open only a line matching
#       `^ {0,3}```[[:space:]]*$` closes it); and
#       `.ufo/waves/round-38/declared-blocks.txt` exists, declares >=1 block for
#       each of the two front doors, and every declaration line
#       `<path> <lines> <sha256>` satisfies
#       `tail -n <lines> <path> | sha256sum` = <sha256>. A pasted receipt is
#       closed by a named correction, and "the append is what the author says it
#       is" is bound to bytes, not to prose.
#   G2 (D-B) Judged-head binding. `.ufo/waves/round-38/final-gates/all-gates.txt`
#       in the export starts with `all-gates v2`; carries exactly one
#       `export-ref=<40 hex>` whose commit exists in the lane and is
#       ancestor-or-equal of the exported ref, and `git diff --name-only
#       <export-ref> <ref>` lists nothing but that receipt (the judged head J is
#       the commit the receipt records; the lane tip adds only the receipt);
#       exactly one `suite-sha256=<digest>` equal to the digest of the bytes
#       executing; exactly the eight `G<n> payload=... closed=1` lines (no
#       closed=0, no duplicate id); the `closed=8/8 exit=0` line; exactly eight
#       `selftest case=G<n> ` lines and one `selftest cases=8 failures=0`. Plus:
#       the SCORECARD.md `## Round 38` section and SHONEN.md name the judged head
#       ONLY by reference (`judged head: export-ref of
#       .ufo/waves/round-38/final-gates/all-gates.txt`), and no line in that
#       section — or among SHONEN's round-38 lines — labels any hash as a final
#       or judged head.
#   G3 (D-C) Pending-marker resolutions. corpus/lessons/round-37.md carries the
#       heading `## Pending-marker resolutions (round 38)` followed by table
#       rows naming each of `L10`, `L90`, `L95`, `L216`, `L265`, `L300`, `L320`,
#       `L85` (eight distinct line tokens, each in some row); and the added (`+`,
#       not `+++`) lines of `git diff <base> <ref>` over the lane tree, minus
#       `.ufo/` and this suite's own paths, contain ZERO occurrences of the
#       widened placeholder vocabulary (`⟨pending`, `<fill>`,
#       `filled by the L1`, `<LANE_HASH>`, `<r38-`) and ZERO word-bounded
#       `TBD` / `TODO`. The base commit is a constant of this file.
#   G4 (D3) Closure order. For every `.ufo/waves/round-38/*-dispatch.json` in the
#       export (at least one required), a results file exists in the same
#       directory — the `-results.json` sibling, or `<wave>-results.json` naming
#       the same wave — parses as JSON, and its seat-entry count equals
#       `len(taskCall.tasks)` of the dispatch. A dispatch whose seats never
#       reported a result count is a round that closed before its evidence.
#   G5 (D-D) Label drift. The SCORECARD.md `## Round 38` section contains zero
#       `Final lane commit:` lines, and SCORECARD.md carries >=1 line beginning
#       `Correction (round 38)` that names `f3246559` and calls it `anchor
#       ancestor`. The stale round-37 label is corrected, not repeated.
#   G6 (D-E) Scratch quiescence, LIVE (not export) and FAIL-CLOSED. Under the
#       scratch root, `kasegi-r36` and `kasegi-r37` are absent or hold zero
#       entries; `kasegi-r38` is absent or holds no entry other than the
#       canonical path of this run's own --work dir (or that dir's top-level
#       parent under `kasegi-r38`), and the parent is tolerated only when every
#       level below it holds nothing but the next path component toward --work
#       (a sibling leftover is residual). Entries are counted by walking every
#       top-level entry, so files, dotfiles and symlinks count exactly like
#       directories; a directory whose scan fails is RED (`read=fail`), never
#       silently zero, and the tolerated entry is printed (`tolerated=`).
#   G7 (D-F) Ledger fill. corpus/knowledge/considerthese-proposals-ledger.md
#       carries the heading `## Round-37 dispositions — filled (round 38)`
#       AFTER `## Round-37 dispositions (appended 2026-10-26, R31 home)`; inside
#       the filled section a line beginning `Correction (round 38)` and at least
#       seven table data rows whose first cell starts with the proposal numbers
#       1..7 (each of 1-7 present). An empty heading with a report claiming a
#       table does not close.
#   G8 (carry-over) The export's own corpus/instruments/r37-closure.sh, run with
#       `--export-ref <ref> --lane <lane> --work <work>/r37`, ends with
#       `closed=14/14 exit=0`. The round-37 gate must still hold on the round-38
#       head; a round that breaks its predecessor's evidence has not closed it.
#
# Documented limits (measured, not hidden):
#   - G1's fence walk is the contract's rule (backtick fences, opener with an
#     optional info string, closer with nothing but blanks). It does not model
#     tilde fences or longer closing runs; a `~~~`-closed front door is red.
#   - G1 counts `Correction (round 38)` only at line start; a correction quoted
#     mid-paragraph does not close. `misplaced` is matched word-bounded.
#   - G1 validates every non-comment declaration line; one bad line makes
#     `declared-ok=0` even when the other lines are right.
#   - G2's head-token rule is literal and has no exemption: a SHOULD-clean
#     sentence that puts any 7+ hex token after `final …head|commit` or `judged
#     head` on one line is red, even when the hash is not the head. Keep hash
#     tokens off those lines.
#   - G3's added-line scan reads the lane diff, not the export: a line added and
#     then removed inside the same commit range is invisible, and the diff is
#     scoped to the two exclusions the contract names.
#   - G4 reads the FIRST `-results.json` sibling or the `<wave>-results.json`
#     named by the dispatch; it compares counts, not identities, so a results
#     file that lists the right number of wrong seats is not caught here.
#   - G6 tolerates this run's own work dir (and its top-level parent under
#     `kasegi-r38`) because a seat that keeps its work under its own scratch
#     would otherwise red itself; the parent is tolerated only through an empty
#     chain (each level holds just the next component toward --work), the entry
#     used is printed as `tolerated=`, and the residual is zero whenever --work
#     lies outside `kasegi-r38`. The CONTENTS of --work itself are not audited:
#     it is the caller's own space, cleared only of `export/` and `mut/`.
#   - G8 executes the exported r37 suite, which takes its OWN live reads (its E9
#     worktree/HEAD/scratch limbs) against --lane; a dirty lane or a stale HEAD
#     reds G8 by construction.
#
# Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
# 2 harness error (unknown or missing argument, unresolvable ref, unreadable
# lane or export, archive failure). The plain-run refusal is exit 2.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
SCRATCH_ROOT=/fast/scratch/hyaku
BASE_REF=a173b0c2b98c5ae39599fa9be76027fbbead0b9e
CHECK_IDS=(G1 G2 G3 G4 G5 G6 G7 G8)

# SELF — absolute physical path of the executing bytes. Resolved once at load
# time because G2 calls suite_digest() from inside a subshell that has cd'd into
# the export tree; a relative BASH_SOURCE would then name the wrong file.
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
# a reader can bind a `closed=8/8` line (and the committed all-gates.txt) to the
# instrument that produced it.
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
  printf 'r38-closure: %s\n' "$*" >&2
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
        printf 'r38-closure: unknown argument: %s\n' "$1" >&2
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
    WORK=$(mktemp -d -t r38-closure.XXXXXXXX) || die 'cannot create a work dir'
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

count_lines() { # reads stdin
  grep -c . 2>/dev/null || true
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

# fence_state FILE — CommonMark fenced-code walk, contract spelling: while
# closed, a line matching `^ {0,3}``` ` opens a fence (an info string may
# follow); while open, only a line matching `^ {0,3}```[[:space:]]*$` closes it.
# Prints `closed` or `open` at EOF.
fence_state() { # FILE
  awk -v f='```' '
    { s = $0
      if (!open) {
        if (s ~ ("^ {0,3}" f)) open = 1
      } else {
        if (s ~ ("^ {0,3}" f "[ \t]*$")) open = 0
      }
    }
    END { print (open ? "open" : "closed") }
  ' "$1"
}

# g1_correction FILE TOKEN — lines that BEGIN with `Correction (round 38)`, name
# TOKEN, and contain the word `misplaced`.
g1_correction() { # FILE TOKEN
  awk -v tok="$2" '
    index($0, "Correction (round 38)") == 1 {
      if (index($0, tok) > 0 && $0 ~ /(^|[^[:alnum:]_])misplaced([^[:alnum:]_]|$)/) n++
    }
    END { print n + 0 }
  ' "$1"
}

# g1_declared TREE — prints `<valid-lines> <ok>`: how many declaration lines
# validate, and whether every line validated with >=1 declaration for each of
# PROVINCE.md and corpus/README.md.
g1_declared() { # TREE
  local tree=$1 p=.ufo/waves/round-38/declared-blocks.txt
  local valid=0 have_p=0 have_r=0 bad=0 line path lines sha extra got
  if [ ! -f "$tree/$p" ]; then printf '0 0'; return; fi
  while IFS= read -r line || [ -n "$line" ]; do
    case $line in ''|'#'*) continue ;; esac
    set -f
    set -- $line
    set +f
    path=$1; lines=${2:-}; sha=${3:-}; extra=${4:-}
    if [ -z "$path" ] || [ -z "$lines" ] || [ -z "$sha" ] || [ -n "$extra" ]; then
      bad=1; continue
    fi
    case $lines in ''|*[!0-9]*) bad=1; continue ;; esac
    [ "$lines" -ge 1 ] || { bad=1; continue; }
    case $sha in ''|*[!0-9a-f]*) bad=1; continue ;; esac
    [ "${#sha}" -eq 64 ] || { bad=1; continue; }
    [ -f "$tree/$path" ] || { bad=1; continue; }
    got=$(tail -n "$lines" -- "$tree/$path" | sha256sum | awk '{print $1; exit}')
    if [ "$got" != "$sha" ]; then bad=1; continue; fi
    valid=$((valid + 1))
    case $path in
      PROVINCE.md) have_p=1 ;;
      corpus/README.md) have_r=1 ;;
    esac
  done < "$tree/$p"
  if [ "$bad" -eq 0 ] && [ "$have_p" -eq 1 ] && [ "$have_r" -eq 1 ]; then
    printf '%s 1' "$valid"
  else
    printf '%s 0' "$valid"
  fi
}

# ---------------------------------------------------------------------------
# checks — every one cd's into the export root and reads relative paths there
# ---------------------------------------------------------------------------

check_g1() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local pcor=0 rcor=0 pf=open rf=open decl='0 0' valid=0 dok=0
    if [ -f PROVINCE.md ]; then
      pcor=$(g1_correction PROVINCE.md 'L79-L152')
      pf=$(fence_state PROVINCE.md)
    fi
    if [ -f corpus/README.md ]; then
      rcor=$(g1_correction corpus/README.md 'L399-L454')
      rf=$(fence_state corpus/README.md)
    fi
    decl=$(g1_declared "$tree")
    valid=${decl%% *}
    dok=${decl##* }
    printf 'province-correction=%s,readme-correction=%s,province-fence=%s,readme-fence=%s,declared-blocks=%s,declared-ok=%s' \
      "$pcor" "$rcor" "$pf" "$rf" "$valid" "$dok"
    [ "$pcor" -ge 1 ] && [ "$rcor" -ge 1 ] && [ "$pf" = closed ] && [ "$rf" = closed ] \
      && [ "$dok" -eq 1 ] && [ "$valid" -ge 2 ] && exit 0
    exit 1
  )
}

check_g2() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=.ufo/waves/round-38/final-gates/all-gates.txt
    local phrase='judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt'
    local file=0 sentinel=0 xref='' xsha='' ancestor=0 diffclean=0 digest=0
    local runlines=0 closedline=0 stlines=0 stsum=0 scref=0 shonenref=0 headtok=0
    local n got name bad sec scoped
    if [ -f "$p" ]; then
      file=1
      [ "$(sed -n '1p' "$p")" = 'all-gates v2' ] && sentinel=1
      n=$(grep -cE '^export-ref=[0-9a-f]{40}$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && xref=$(sed -n 's/^export-ref=//p' "$p")
      n=$(grep -cE '^suite-sha256=[0-9a-f]{64}$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && xsha=$(sed -n 's/^suite-sha256=//p' "$p")
      if [ -n "$xref" ] && git -C "$LANE" cat-file -e "${xref}^{commit}" 2>/dev/null; then
        if git -C "$LANE" merge-base --is-ancestor "$xref" "$ref" 2>/dev/null; then
          ancestor=1
        fi
        if name=$(git -C "$LANE" diff --name-only "$xref" "$ref"); then
          bad=0
          while IFS= read -r scoped; do
            [ -n "$scoped" ] || continue
            [ "$scoped" = "$p" ] || bad=1
          done <<< "$name"
          [ "$bad" -eq 0 ] && diffclean=1
        fi
      fi
      if [ -n "$xsha" ] && [ "$xsha" = "$(suite_digest)" ]; then digest=1; fi
      n=$(grep -cE '^G[1-8] payload=.* closed=1$' "$p"); n=${n:-0}
      got=$(grep -E '^G[1-8] payload=.* closed=1$' "$p" \
        | sed -n 's/^\(G[1-8]\) payload=.*/\1/p' | sort -u | count_lines); got=${got:-0}
      [ "$n" -eq 8 ] && [ "$got" -eq 8 ] && runlines=1
      n=$(grep -cE '^closed=8/8 exit=0$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && closedline=1
      n=$(grep -cE '^selftest case=G[1-8] ' "$p"); n=${n:-0}
      got=$(grep -E '^selftest case=G[1-8] ' "$p" \
        | sed -n 's/^selftest case=\(G[1-8]\) .*/\1/p' | sort -u | count_lines); got=${got:-0}
      [ "$n" -eq 8 ] && [ "$got" -eq 8 ] && stlines=1
      n=$(grep -cE '^selftest cases=8 failures=0$' "$p"); n=${n:-0}
      [ "$n" -eq 1 ] && stsum=1
    fi
    if [ -f SCORECARD.md ]; then
      sec=$(md_section SCORECARD.md '^## Round 38([^0-9]|$)')
      if [ -n "$sec" ]; then
        n=$(printf '%s\n' "$sec" | grep -cF -- "$phrase"); n=${n:-0}
        [ "$n" -ge 1 ] && scref=1
        n=$(printf '%s\n' "$sec" \
          | grep -ciE '(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}'); n=${n:-0}
        headtok=$((headtok + n))
      fi
    fi
    if [ -f SHONEN.md ]; then
      n=$(grep -cF -- "$phrase" SHONEN.md); n=${n:-0}
      [ "$n" -ge 1 ] && shonenref=1
      scoped=$(grep -E 'round 38|round-38' SHONEN.md)
      if [ -n "$scoped" ]; then
        n=$(printf '%s\n' "$scoped" \
          | grep -ciE '(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}'); n=${n:-0}
        headtok=$((headtok + n))
      fi
    fi
    printf 'receipt=%s,sentinel=%s,export-ref=%s,ancestor=%s,diff-clean=%s,digest-match=%s,run-lines=%s,closed-line=%s,selftest-lines=%s,selftest-summary=%s,scorecard-ref=%s,shonen-ref=%s,head-token-lines=%s' \
      "$file" "$sentinel" "$([ -n "$xref" ] && echo 1 || echo 0)" "$ancestor" "$diffclean" \
      "$digest" "$runlines" "$closedline" "$stlines" "$stsum" "$scref" "$shonenref" "$headtok"
    [ "$file" -eq 1 ] && [ "$sentinel" -eq 1 ] && [ -n "$xref" ] && [ "$ancestor" -eq 1 ] \
      && [ "$diffclean" -eq 1 ] && [ "$digest" -eq 1 ] && [ "$runlines" -eq 1 ] \
      && [ "$closedline" -eq 1 ] && [ "$stlines" -eq 1 ] && [ "$stsum" -eq 1 ] \
      && [ "$scref" -eq 1 ] && [ "$shonenref" -eq 1 ] && [ "$headtok" -eq 0 ] && exit 0
    exit 1
  )
}

check_g3() { # TREE REF
  local tree=$1 ref=$2
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local lesson=corpus/lessons/round-37.md
    local sec='' rows='' sect=0 tokens=0 tok pending=0 placeholders=0 diffread=fail
    local out added n
    if [ -f "$lesson" ]; then
      sec=$(md_section "$lesson" '^## Pending-marker resolutions [(]round 38[)]$')
      if [ -n "$sec" ]; then
        sect=1
        rows=$(printf '%s\n' "$sec" | grep '^|')
        for tok in L10 L90 L95 L216 L265 L300 L320 L85; do
          if printf '%s\n' "$rows" | grep -qE "(^|[^0-9])${tok}([^0-9]|$)"; then
            tokens=$((tokens + 1))
          fi
        done
      fi
    fi
    if out=$(git -C "$LANE" diff --no-color "$BASE_REF" "$ref" -- . \
               ':!.ufo' ':!corpus/instruments/r38-closure.sh' \
               ':!corpus/instruments/r38-fixtures'); then
      diffread=ok
      added=$(printf '%s\n' "$out" | grep '^+' | grep -v '^+++')
      for tok in "⟨pending" '<fill>' 'filled by the L1' '<LANE_HASH>' '<r38-'; do
        n=$(printf '%s\n' "$added" | grep -cF -- "$tok"); n=${n:-0}
        pending=$((pending + n))
      done
      n=$(printf '%s\n' "$added" \
        | grep -cE '(^|[^[:alnum:]_])(TBD|TODO)([^[:alnum:]_]|$)'); n=${n:-0}
      placeholders=$((placeholders + n))
    fi
    printf 'resolutions-section=%s,line-tokens=%s,added-pending=%s,added-placeholders=%s,diff-read=%s' \
      "$sect" "$tokens" "$pending" "$placeholders" "$diffread"
    [ "$sect" -eq 1 ] && [ "$tokens" -eq 8 ] && [ "$pending" -eq 0 ] \
      && [ "$placeholders" -eq 0 ] && [ "$diffread" = ok ] && exit 0
    exit 1
  )
}

# g4_json FILE EXPR — one python3 read of a JSON file; EXPR selects the value.
# Kept in one place so every limb parses with the same stdlib reader.
g4_json() { # FILE EXPR
  python3 -c '
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("ERR")
    sys.exit(0)
expr = sys.argv[2]
if expr == "wave":
    print(d.get("wave") or "")
elif expr == "tasks":
    t = (d.get("taskCall") or {}).get("tasks")
    print(len(t) if isinstance(t, list) else -1)
elif expr == "seats":
    r = d.get("results")
    if isinstance(r, list):
        print(len(r))
    elif isinstance(d.get("seats"), int):
        print(d["seats"])
    else:
        print(-1)
else:
    print("ERR")
' "$1" "$2"
}

check_g4() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local dir=.ufo/waves/round-38
    local disp=0 pairs=0 seatsok=0 read=fail f base res wave rtasks rseats rwave
    if [ -d "$dir" ]; then
      read=ok
      while IFS= read -r f; do
        [ -n "$f" ] || continue
        disp=$((disp + 1))
        base=${f%-dispatch.json}
        res=$base-results.json
        wave=$(g4_json "$f" wave)
        rtasks=$(g4_json "$f" tasks)
        case $wave in ''|ERR) continue ;; esac
        case $rtasks in ''|*[!0-9-]*) continue ;; esac
        [ "$rtasks" -ge 0 ] || continue
        if [ ! -f "$res" ] && [ -f "$dir/$wave-results.json" ]; then
          res=$dir/$wave-results.json
          rwave=$(g4_json "$res" wave)
          [ "$rwave" = "$wave" ] || continue
        fi
        [ -f "$res" ] || continue
        pairs=$((pairs + 1))
        rseats=$(g4_json "$res" seats)
        case $rseats in ''|*[!0-9-]*) continue ;; esac
        [ "$rseats" -eq "$rtasks" ] && seatsok=$((seatsok + 1))
      done < <(find "$dir" -maxdepth 1 -name '*-dispatch.json' | sort)
    fi
    printf 'dispatches=%s,pairs=%s,seats-ok=%s,read=%s' "$disp" "$pairs" "$seatsok" "$read"
    [ "$read" = ok ] && [ "$disp" -ge 1 ] && [ "$pairs" -eq "$disp" ] \
      && [ "$seatsok" -eq "$disp" ] && exit 0
    exit 1
  )
}

check_g5() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local sec='' sect=0 fin=0 cor=0 h=0 aa=0
    if [ -f SCORECARD.md ]; then
      sec=$(md_section SCORECARD.md '^## Round 38([^0-9]|$)')
      [ -n "$sec" ] && sect=1
      if [ "$sect" -eq 1 ]; then
        fin=$(printf '%s\n' "$sec" | grep -cF 'Final lane commit:'); fin=${fin:-0}
      fi
      cor=$(awk 'index($0, "Correction (round 38)") == 1 && index($0, "f3246559") > 0 \
                 && tolower($0) ~ /anchor[- ]ancestor/ { n++ } END { print n + 0 }' SCORECARD.md)
      h=$(grep -cF -- 'f3246559' SCORECARD.md); h=${h:-0}
      aa=$(grep -ciE -- 'anchor[- ]ancestor' SCORECARD.md); aa=${aa:-0}
    fi
    printf 'round38-section=%s,final-lane-commit-lines=%s,correction=%s,f3246559=%s,anchor-ancestor=%s' \
      "$sect" "$fin" "$cor" "$h" "$aa"
    [ "$sect" -eq 1 ] && [ "$fin" -eq 0 ] && [ "$cor" -ge 1 ] && exit 0
    exit 1
  )
}

# g6_root_state DIR — absent|empty|present|unreadable. Every entry counts
# (file, dotfile, symlink, directory); a scan that fails is `unreadable`, never
# `empty`.
g6_root_state() { # DIR
  local d=$1 out n=0
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

# g6_chain_ok ANCESTOR WORK — the ancestor carve-out's guard: every level
# strictly between ANCESTOR and WORK must hold exactly one entry, the next
# component of the canonical path toward WORK. A sibling leftover under the
# tolerated parent is therefore still RESIDUAL.
g6_chain_ok() { # ANCESTOR WORK
  local dir=$1 rest=${2#"$1"/} next e real n=0
  while [ -n "$rest" ]; do
    next=${rest%%/*}
    n=0; real=''
    while IFS= read -r e; do
      [ -n "$e" ] || continue
      n=$((n + 1))
      real=$( cd "$e" 2>/dev/null && pwd -P )
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

check_g6() { # TREE REF
  local sroot=$SCRATCH_ROOT
  local r36=absent r37=absent r38=absent read=ok work=outside
  local realw='' e real out tol=none
  if [ -n "${WORK:-}" ]; then realw=$( cd "$WORK" 2>/dev/null && pwd -P ); fi
  if [ -z "$realw" ]; then
    printf 'r36=?,r37=?,r38=?,work=unknown,tolerated=none,read=fail'
    return 1
  fi
  [ -d "$sroot" ] && sroot=$( cd "$sroot" && pwd -P )
  case $realw in "$sroot"/kasegi-r38/*) work=inside ;; esac
  r36=$(g6_root_state "$sroot/kasegi-r36")
  r37=$(g6_root_state "$sroot/kasegi-r37")
  [ "$r36" = unreadable ] && read=fail
  [ "$r37" = unreadable ] && read=fail
  # r38: this run's own work dir (or its top-level parent under kasegi-r38) is
  # tolerated, but only when the chain from that parent to WORK is empty of
  # anything else. Entries are judged by realpath, never by name.
  if [ -d "$sroot/kasegi-r38" ]; then
    if out=$(find "$sroot/kasegi-r38" -mindepth 1 -maxdepth 1 -print); then
      r38=empty
      while IFS= read -r e; do
        [ -n "$e" ] || continue
        real=$( cd "$e" 2>/dev/null && pwd -P )
        if [ -z "$real" ]; then
          r38=present; continue
        fi
        if [ "$real" = "$realw" ]; then
          tol=$real; continue
        fi
        case $realw in
          "$real"/*)
            if g6_chain_ok "$real" "$realw"; then tol=$real; else r38=present; fi
            continue ;;
        esac
        r38=present
      done < <(printf '%s\n' "$out")
    else
      r38=unreadable
      read=fail
    fi
  elif [ -e "$sroot/kasegi-r38" ] || [ -L "$sroot/kasegi-r38" ]; then
    r38=present
  fi
  printf 'r36=%s,r37=%s,r38=%s,work=%s,tolerated=%s,read=%s' \
    "$r36" "$r37" "$r38" "$work" "$tol" "$read"
  [ "$read" = ok ] && [ "$r36" != present ] && [ "$r36" != unreadable ] \
    && [ "$r37" != present ] && [ "$r37" != unreadable ] \
    && [ "$r38" != present ] && [ "$r38" != unreadable ] && return 0
  return 1
}

check_g7() { # TREE REF
  local tree=$1
  (
    cd "$tree" || { printf 'tree-unreadable'; exit 2; }
    local p=corpus/knowledge/considerthese-proposals-ledger.md
    local a=0 b=0 filled=0 cor=0 rows=0 missing=0 sec=''
    if [ -f "$p" ]; then
      a=$(grep -nF -- '## Round-37 dispositions (appended 2026-10-26, R31 home)' "$p" \
        | head -n 1 | cut -d: -f1); a=${a:-0}
      b=$(grep -nF -- '## Round-37 dispositions — filled (round 38)' "$p" \
        | head -n 1 | cut -d: -f1); b=${b:-0}
      if [ "$a" -gt 0 ] && [ "$b" -gt "$a" ]; then
        filled=1
        sec=$(awk -v s="$b" 'NR >= s { if (NR > s && $0 ~ /^## /) exit; print }' "$p")
        cor=$(printf '%s\n' "$sec" | grep -c '^Correction (round 38)'); cor=${cor:-0}
        rows=$(printf '%s\n' "$sec" | awk -F'|' '
          /^\|/ {
            c = $2
            gsub(/^[ \t]+|[ \t]+$/, "", c)
            if (c ~ /^[0-9]+/) {
              sub(/\..*/, "", c)
              if (c + 0 >= 1 && c + 0 <= 7) seen[c + 0] = 1
            }
          }
          END { n = 0; for (i = 1; i <= 7; i++) if (seen[i]) n++; print n }
        ')
        rows=${rows:-0}
        missing=$((7 - rows))
      fi
    fi
    printf 'filled-section=%s,correction=%s,proposal-rows=%s,missing=%s' \
      "$filled" "$cor" "$rows" "$missing"
    [ "$filled" -eq 1 ] && [ "$cor" -ge 1 ] && [ "$rows" -ge 7 ] && [ "$missing" -eq 0 ] && exit 0
    exit 1
  )
}

check_g8() { # TREE REF
  local tree=$1 ref=$2
  local suite=corpus/instruments/r37-closure.sh
  local have=0 closed=0 rc=1 out last
  [ -f "$tree/$suite" ] && have=1
  if [ "$have" -eq 1 ]; then
    out=$(bash "$tree/$suite" --export-ref "$ref" --lane "$LANE" \
            --work "$WORK/r37" 2>&1); rc=$?
    last=$(printf '%s\n' "$out" | grep -v '^$' | tail -n 1)
    [ "$last" = 'closed=14/14 exit=0' ] && closed=1
  fi
  printf 'r37-suite=%s,r37-closed=%s,r37-exit=%s' "$have" "$closed" "$rc"
  [ "$have" -eq 1 ] && [ "$closed" -eq 1 ] && [ "$rc" -eq 0 ] && return 0
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
  local -A PAY=() RC=()
  printf 'export-ref=%s mode=export lane=%s suite-sha256=%s\n' \
    "$REF_RESOLVED" "$LANE" "$(suite_digest)"
  if [ "$LANE_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --lane\n'; fi
  if [ "$SCRATCH_OVERRIDE" -eq 1 ]; then printf 'deviation=non-default --scratch-root\n'; fi
  for id in "${CHECK_IDS[@]}"; do
    out=$(run_check "$id" "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
    PAY[$id]=$out; RC[$id]=$rc
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

st_neg() { # ID LABEL TREE REF NEEDLE
  local id=$1 label=$2 tree=$3 ref=$4 needle=$5
  local out rc
  out=$(run_check "$id" "$tree" "$ref" 2>/dev/null); rc=$?
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

# --- G1 fixtures -----------------------------------------------------------

# g1_declare DIR — write declared-blocks.txt for the last two lines of each
# front door, so a fixture mutant can reopen one clause and leave the rest.
g1_declare() { # DIR
  local d=$1 p n=2 sha
  mkdir -p -- "$d/.ufo/waves/round-38"
  : > "$d/.ufo/waves/round-38/declared-blocks.txt"
  for p in PROVINCE.md corpus/README.md; do
    sha=$(tail -n "$n" -- "$d/$p" | sha256sum | awk '{print $1; exit}')
    printf '%s %s %s\n' "$p" "$n" "$sha" >> "$d/.ufo/waves/round-38/declared-blocks.txt"
  done
}

# g1_fixture DIR [pcor=yes|no] [ropen=yes|no] [flip=yes|no] — a complete green
# G1 tree, with one knob per clause.
g1_fixture() { # DIR [knob...]
  local d=$1; shift
  local pcor=yes ropen=no flip=no kv
  for kv in "$@"; do
    case $kv in
      pcor=*) pcor=${kv#pcor=} ;;
      ropen=*) ropen=${kv#ropen=} ;;
      flip=*) flip=${kv#flip=} ;;
    esac
  done
  mut_reset "$d"
  mkdir -p -- "$d/corpus" "$d/.ufo/waves/round-38"
  {
    printf '# Province — front door\n\n```text\nfront-door example\n```\n\n'
    printf '<!-- round-38 append below -->\n'
    if [ "$pcor" = yes ]; then
      printf 'Correction (round 38): the round-37 append at L79-L152 is misplaced receipt scaffolding; the front door is corrected in place.\n'
    fi
  } | mut_put "$d" PROVINCE.md
  {
    printf '# Corpus front door\n\n```text\nexample\n```\n\n'
    [ "$ropen" = yes ] && printf '```js\nlet x = 1;\n'
    printf '<!-- round-38 append below -->\n'
    printf 'Correction (round 38): the round-37 append at L399-L454 is misplaced receipt scaffolding; the admission heading is restored.\n'
  } | mut_put "$d" corpus/README.md
  g1_declare "$d"
  if [ "$flip" = yes ]; then
    # flip one byte INSIDE the declared block, after the declaration was made,
    # so exactly the declaration-to-bytes binding reopens
    {
      printf '# Corpus front door\n\n```text\nexample\n```\n\n'
      [ "$ropen" = yes ] && printf '```js\nlet x = 1;\n'
      printf '<!-- round-38 append begins -->\n'
      printf 'Correction (round 38): the round-37 append at L399-L454 is misplaced receipt scaffolding; the admission heading is restored.\n'
    } | mut_put "$d" corpus/README.md
  fi
}

# --- G2 fixtures -----------------------------------------------------------

# g2_fixture DIR [sentinel=text] [xref=HASH] [digest=HASH] [scref=yes|no]
#              [shonenref=yes|no] [headline=yes|no] — a complete green G2 tree.
g2_fixture() { # DIR [knob...]
  local d=$1; shift
  local phrase='judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt'
  local sentinel='all-gates v2' xref=$REF_RESOLVED digest scref=yes shonenref=yes
  local headline=no zero i kv
  digest=$(suite_digest)
  for kv in "$@"; do
    case $kv in
      sentinel=*) sentinel=${kv#sentinel=} ;;
      xref=*) xref=${kv#xref=} ;;
      digest=*) digest=${kv#digest=} ;;
      scref=*) scref=${kv#scref=} ;;
      shonenref=*) shonenref=${kv#shonenref=} ;;
      headline=*) headline=${kv#headline=} ;;
    esac
  done
  mut_reset "$d"
  mkdir -p -- "$d/.ufo/waves/round-38/final-gates"
  {
    printf '%s\n' "$sentinel"
    printf 'export-ref=%s\n' "$xref"
    printf 'suite-sha256=%s\n' "$digest"
    printf 'run-utc=2026-10-26T18:00:00Z\n'
    printf '\n== run ==\n'
    for i in 1 2 3 4 5 6 7 8; do printf 'G%s payload=fixture closed=1\n' "$i"; done
    printf 'closed=8/8 exit=0\n'
    printf '== selftest ==\n'
    for i in 1 2 3 4 5 6 7 8; do
      printf 'selftest case=G%s positive=pass mutants=2/2 verdict=pass\n' "$i"
    done
    printf 'selftest cases=8 failures=0\n'
  } > "$d/.ufo/waves/round-38/final-gates/all-gates.txt"
  {
    printf '## Round 38 result\n\n'
    [ "$scref" = yes ] && printf '%s\n' "$phrase"
    [ "$headline" = yes ] && printf 'Final head: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b\n'
    printf '\n| Axis | Score |\n|---|---|\n'
  } | mut_put "$d" SCORECARD.md
  {
    printf '# checklist\n\n'
    if [ "$shonenref" = yes ]; then
      printf -- '- [~] box 3 — evidence (round 38): %s\n' "$phrase"
    else
      printf -- '- [~] box 3 — evidence (round 38): suite and harness commands ran.\n'
    fi
  } | mut_put "$d" SHONEN.md
}

# --- G4 / G5 / G7 fixtures -------------------------------------------------

# g4_fixture DIR [results=yes|no] [seats=N]
g4_fixture() { # DIR [knob...]
  local d=$1; shift
  local results=yes seats=3 kv i
  for kv in "$@"; do
    case $kv in
      results=*) results=${kv#results=} ;;
      seats=*) seats=${kv#seats=} ;;
    esac
  done
  mut_reset "$d"
  mkdir -p -- "$d/.ufo/waves/round-38"
  {
    printf '{"schema":"ufo-swarm-wave-dispatch-v1","wave":"kasegi-r38-build","taskCall":{"tasks":['
    for i in 1 2 3; do
      [ "$i" -gt 1 ] && printf ','
      printf '{"name":"Seat%s"}' "$i"
    done
    printf ']}}\n'
  } > "$d/.ufo/waves/round-38/wave1-dispatch.json"
  if [ "$results" = yes ]; then
    {
      printf '{"lane":"kasegi","round":38,"wave":"kasegi-r38-build","seats":%s,"results":[' "$seats"
      for i in $(seq 1 "$seats"); do
        [ "$i" -gt 1 ] && printf ','
        printf '{"name":"Seat%s","agent":"executor","output":"x"}' "$i"
      done
      printf ']}\n'
    } > "$d/.ufo/waves/round-38/wave1-results.json"
  fi
}

# g5_fixture DIR [section=yes|no] [final=yes|no] [correction=yes|no]
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
    printf '## Round 37 result\n\nFinal lane commit: f3246559bed2fd085dde860e00247ce394f02bad (wave-evidence ancestor)\n\n'
    if [ "$section" = yes ]; then
      printf '## Round 38 result\n\n| Axis | Score |\n|---|---|\n'
      [ "$final" = yes ] && printf 'Final lane commit: abc1234def5678\n'
    fi
    [ "$correction" = yes ] && \
      printf 'Correction (round 38): f3246559 is the round-37 wave-evidence anchor ancestor, not a final head.\n'
  } | mut_put "$d" SCORECARD.md
}

# g7_fixture DIR [rows=7] [drop=N] [correction=yes|no]
g7_fixture() { # DIR [knob...]
  local d=$1; shift
  local drop=0 correction=yes kv i
  for kv in "$@"; do
    case $kv in
      drop=*) drop=${kv#drop=} ;;
      correction=*) correction=${kv#correction=} ;;
    esac
  done
  mut_reset "$d"
  {
    printf '# ledger\n\n## Round-37 dispositions (appended 2026-10-26, R31 home)\n\n\n\n'
    printf '## Re-pin note\n\nA note.\n\n'
    printf '## Round-37 dispositions — filled (round 38)\n\n'
    [ "$correction" = yes ] && \
      printf 'Correction (round 38): the empty round-37 section above is filled here.\n\n'
    printf '| proposal | disposition | evidence |\n|---|---|---|\n'
    for i in 1 2 3 4 5 6 7; do
      [ "$i" -eq "$drop" ] && continue
      printf '| %s. proposal %s | mined | ledger row %s |\n' "$i" "$i" "$i"
    done
  } | mut_put "$d" corpus/knowledge/considerthese-proposals-ledger.md
}

# --- selftest cases --------------------------------------------------------

selftest_case_G1() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G1 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G1-nocorrection; g1_fixture "$d" pcor=no
  st_neg G1 province-correction-absent "$d" "$REF_RESOLVED" 'province-correction=0' \
    && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G1-openfence; g1_fixture "$d" ropen=yes
  st_neg G1 readme-fence-open "$d" "$REF_RESOLVED" 'readme-fence=open' \
    && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G1-declared; g1_fixture "$d" flip=yes
  st_neg G1 declared-block-byte-flip "$d" "$REF_RESOLVED" 'declared-ok=0' \
    && ok=$((ok + 1))
  st_verdict G1 "$bad" "$ok" "$n"
}

selftest_case_G2() {
  local bad=0 ok=0 n=0 d repo top real br c1 ref side saved
  CASES=$((CASES + 1))
  st_pos G2 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G2-sentinel; g2_fixture "$d" 'sentinel=all-gates v1'
  st_neg G2 sentinel-v1 "$d" "$REF_RESOLVED" 'sentinel=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-digest; g2_fixture "$d" "digest=$(printf '%064d' 0)"
  st_neg G2 digest-mismatch "$d" "$REF_RESOLVED" 'digest-match=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G2-headline; g2_fixture "$d" headline=yes
  st_neg G2 final-head-hash-in-section "$d" "$REF_RESOLVED" 'head-token-lines=1' \
    && ok=$((ok + 1))
  # the landing hazard: the round-38 SCORECARD correction line, landed INSIDE
  # the section, quotes `Final lane commit: f3246559` and names the judged head
  # by hash -- both phrases are exactly what the zero-token rule forbids there
  n=$((n + 1)); d=$MUT/G2-correction-inside; g2_fixture "$d"
  printf 'Correction (round 38): the round-37 section'\''s `Final lane commit: f3246559\xe2\x80\xa6` line names a wave-evidence anchor ancestor, not a final head; the round-37 judged head is 2387dcf6ccfefcfb703783387b9aade8fc82abfa.\n' \
    >> "$d/SCORECARD.md"
  st_neg G2 correction-line-inside-section "$d" "$REF_RESOLVED" 'head-token-lines=1' \
    && ok=$((ok + 1))
  # history mutants need real commits: a fixture repo whose toplevel is itself
  repo=$MUT/G2-repo; mut_reset "$repo"
  if ! git -C "$repo" init -q 2>/dev/null; then
    printf 'selftest detail=G2 fixture=repo-init-failed\n'
    st_verdict G2 1 "$ok" "$n"
    return
  fi
  top=$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)
  real=$( cd "$repo" && pwd -P )
  if [ "$top" != "$real" ]; then
    printf 'selftest detail=G2 fixture=toplevel-mismatch top=%s want=%s\n' "$top" "$real"
    st_verdict G2 1 "$ok" "$n"
    return
  fi
  br=$(git -C "$repo" symbolic-ref --short HEAD 2>/dev/null)
  g2_fixture "$repo" xref=0000000000000000000000000000000000000000
  git -C "$repo" add -A 2>/dev/null
  git -C "$repo" -c user.email=r38@local -c user.name=r38 commit -q -m base 2>/dev/null
  c1=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  g2_fixture "$repo" "xref=$c1"
  git -C "$repo" add -A 2>/dev/null
  git -C "$repo" -c user.email=r38@local -c user.name=r38 commit -q -m receipt 2>/dev/null
  ref=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  git -C "$repo" checkout -q -b side 2>/dev/null
  git -C "$repo" -c user.email=r38@local -c user.name=r38 commit -q --allow-empty -m side 2>/dev/null
  side=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  git -C "$repo" checkout -q "$br" 2>/dev/null
  # non-ancestor, same tree: the export-ref resolves but is not an ancestor
  g2_fixture "$repo" "xref=$side"
  n=$((n + 1)); saved=$LANE
  LANE=$repo
  st_neg G2 export-ref-not-ancestor "$repo" "$ref" 'ancestor=0' && ok=$((ok + 1))
  LANE=$saved
  # extra file in the post-receipt diff: a commit after the receipt adds one
  g2_fixture "$repo" "xref=$c1"
  printf 'notes\n' > "$repo/NOTES.md"
  git -C "$repo" add -A 2>/dev/null
  git -C "$repo" -c user.email=r38@local -c user.name=r38 commit -q -m notes 2>/dev/null
  ref=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  n=$((n + 1)); saved=$LANE
  LANE=$repo
  st_neg G2 post-receipt-diff-extra "$repo" "$ref" 'diff-clean=0' && ok=$((ok + 1))
  LANE=$saved
  st_verdict G2 "$bad" "$ok" "$n"
}

selftest_case_G3() {
  local bad=0 ok=0 n=0 d repo top real br c1 saved
  CASES=$((CASES + 1))
  st_pos G3 "$EXPORT" "$REF_RESOLVED" || bad=1
  # the added-lines limb reads the lane diff, so its mutant needs a commit whose
  # parent is the real base: fetch the lane history into a verified fixture repo
  repo=$MUT/G3-repo; mut_reset "$repo"
  if ! git -C "$repo" init -q 2>/dev/null; then
    printf 'selftest detail=G3 fixture=repo-init-failed\n'
    st_verdict G3 1 "$ok" "$n"
    return
  fi
  top=$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)
  real=$( cd "$repo" && pwd -P )
  if [ "$top" != "$real" ]; then
    printf 'selftest detail=G3 fixture=toplevel-mismatch top=%s want=%s\n' "$top" "$real"
    st_verdict G3 1 "$ok" "$n"
    return
  fi
  if ! git -C "$repo" fetch -q --no-tags "$LANE" HEAD 2>/dev/null; then
    printf 'selftest detail=G3 fixture=fetch-failed\n'
    st_verdict G3 1 "$ok" "$n"
    return
  fi
  git -C "$repo" update-ref refs/heads/base "$BASE_REF" 2>/dev/null
  git -C "$repo" -c advice.detachedHead=false checkout -q "$BASE_REF" 2>/dev/null
  br=$(git -C "$repo" symbolic-ref --short HEAD 2>/dev/null)
  [ -n "$br" ] || br=base
  # a green resolutions section, so only the placeholder vocabulary is reopened
  {
    printf '\n## Pending-marker resolutions (round 38)\n\n| line | what was deferred | resolved value | evidence |\n|---|---|---|---|\n'
    for tok in L10 L90 L95 L216 L265 L300 L320 L85; do
      printf '| %s | deferred note | resolved at the judged head | receipt |\n' "$tok"
    done
  } >> "$repo/corpus/lessons/round-37.md"
  printf 'TODO fill this line in\n' > "$repo/corpus/lessons/r38-probe.md"
  git -C "$repo" add -A 2>/dev/null
  git -C "$repo" -c user.email=r38@local -c user.name=r38 commit -q -m probe 2>/dev/null
  c1=$(git -C "$repo" rev-parse --verify HEAD 2>/dev/null)
  n=$((n + 1)); saved=$LANE
  LANE=$repo
  st_neg G3 added-placeholder-token "$repo" "$c1" 'added-placeholders=1' \
    && ok=$((ok + 1))
  # drop one resolved line token from the section: the table limb reopens
  d=$MUT/G3-token; mut_reset "$d"
  {
    printf '## Pending-marker resolutions (round 38)\n\n| line | what was deferred | resolved value | evidence |\n|---|---|---|---|\n'
    for tok in L10 L90 L95 L216 L300 L320 L85; do
      printf '| %s | deferred note | resolved at the judged head | receipt |\n' "$tok"
    done
  } | mut_put "$d" corpus/lessons/round-37.md
  # diff the base against itself for this mutant: the section comes from the
  # tree, and the placeholder limb must stay green so only the table reopens
  st_neg G3 missing-line-token "$d" "$BASE_REF" 'line-tokens=7' && ok=$((ok + 1))
  LANE=$saved
  n=$((n + 1))
  st_verdict G3 "$bad" "$ok" "$n"
}

selftest_case_G4() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G4 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G4-noresults; g4_fixture "$d" results=no
  st_neg G4 results-absent "$d" "$REF_RESOLVED" 'pairs=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G4-shortresults; g4_fixture "$d" seats=2
  st_neg G4 seat-count-short "$d" "$REF_RESOLVED" 'seats-ok=0' && ok=$((ok + 1))
  st_verdict G4 "$bad" "$ok" "$n"
}

selftest_case_G5() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G5 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G5-final; g5_fixture "$d" final=yes
  st_neg G5 final-label-in-section "$d" "$REF_RESOLVED" 'final-lane-commit-lines=1' \
    && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G5-nocorrection; g5_fixture "$d" correction=no
  st_neg G5 correction-absent "$d" "$REF_RESOLVED" 'correction=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G5-nosection; g5_fixture "$d" section=no
  st_neg G5 round38-section-absent "$d" "$REF_RESOLVED" 'round38-section=0' \
    && ok=$((ok + 1))
  # the landing hazard: the correction line landed inside the section carries
  # the forbidden `Final lane commit:` token, even though it corrects that label
  n=$((n + 1)); d=$MUT/G5-correction-inside
  {
    printf '## Round 37 result\n\nFinal lane commit: f3246559bed2fd085dde860e00247ce394f02bad (wave-evidence ancestor)\n\n'
    printf '## Round 38 result\n\n'
    printf 'Correction (round 38): the round-37 section'\''s `Final lane commit: f3246559\xe2\x80\xa6` line names a wave-evidence anchor ancestor, not a final head.\n'
  } | mut_put "$d" SCORECARD.md
  st_neg G5 correction-line-inside-section "$d" "$REF_RESOLVED" 'final-lane-commit-lines=1' \
    && ok=$((ok + 1))
  st_verdict G5 "$bad" "$ok" "$n"
}

selftest_case_G6() {
  local bad=0 ok=0 n=0 root save_root save_work rc out
  CASES=$((CASES + 1))
  st_pos G6 "$EXPORT" "$REF_RESOLVED" || bad=1
  save_root=$SCRATCH_ROOT
  save_work=$WORK
  # control (not a mutant): a run whose own work dir is the only entry under
  # kasegi-r38 must be accepted, or a seat-scratch run reds itself
  root=$MUT/g6-control
  mut_reset "$root"
  mkdir -p -- "$root/kasegi-r38/seat/work"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r38/seat/work
  out=$(run_check G6 "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=G6 control=own-work-dir accepted=1 payload=%s\n' "$out"
  else
    printf 'selftest detail=G6 control=own-work-dir accepted=0 rc=%s payload=%s\n' "$rc" "$out"
    FAILS=$((FAILS + 1))
  fi
  WORK=$save_work
  # mutants: a stray entry in each root
  root=$MUT/g6-r36; mut_reset "$root"; mkdir -p -- "$root/kasegi-r36"
  printf 'x\n' > "$root/kasegi-r36/leftover.txt"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 r36-leftover-file "$EXPORT" "$REF_RESOLVED" 'r36=present' && ok=$((ok + 1))
  root=$MUT/g6-r37; mut_reset "$root"; mkdir -p -- "$root/kasegi-r37"
  printf 'x\n' > "$root/kasegi-r37/build-spec.py"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 r37-leftover-file "$EXPORT" "$REF_RESOLVED" 'r37=present' && ok=$((ok + 1))
  root=$MUT/g6-r38; mut_reset "$root"; mkdir -p -- "$root/kasegi-r38/leftover-seat"
  SCRATCH_ROOT=$root
  n=$((n + 1))
  st_neg G6 r38-residual-seat "$EXPORT" "$REF_RESOLVED" 'r38=present' && ok=$((ok + 1))
  # the parent carve-out must not launder a seat dir: the tolerated child may
  # hold only the chain toward WORK, so a sibling leftover under it is residual
  root=$MUT/g6-r38-parent
  mut_reset "$root"
  mkdir -p -- "$root/kasegi-r38/seat/work"
  printf 'x\n' > "$root/kasegi-r38/seat/leftover.txt"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r38/seat/work
  n=$((n + 1))
  st_neg G6 r38-parent-sibling-leftover "$EXPORT" "$REF_RESOLVED" 'r38=present' \
    && ok=$((ok + 1))
  WORK=$save_work
  # control (not a mutant): a clean nested chain toward WORK is accepted
  root=$MUT/g6-r38-nested
  mut_reset "$root"
  mkdir -p -- "$root/kasegi-r38/seat/work/deep"
  SCRATCH_ROOT=$root
  WORK=$root/kasegi-r38/seat/work/deep
  out=$(run_check G6 "$EXPORT" "$REF_RESOLVED" 2>/dev/null); rc=$?
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
  n=$((n + 1)); d=$MUT/G7-dropped; g7_fixture "$d" drop=4
  st_neg G7 proposal-row-absent "$d" "$REF_RESOLVED" 'missing=1' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G7-nocorrection; g7_fixture "$d" correction=no
  st_neg G7 correction-absent "$d" "$REF_RESOLVED" 'correction=0' && ok=$((ok + 1))
  st_verdict G7 "$bad" "$ok" "$n"
}

selftest_case_G8() {
  local bad=0 ok=0 n=0 d
  CASES=$((CASES + 1))
  st_pos G8 "$EXPORT" "$REF_RESOLVED" || bad=1
  n=$((n + 1)); d=$MUT/G8-red; mut_reset "$d"
  mkdir -p -- "$d/corpus/instruments"
  printf '#!/usr/bin/env bash\nprintf "export-ref=x\\n"\nprintf "closed=13/14 exit=1\\n"\nexit 1\n' \
    > "$d/corpus/instruments/r37-closure.sh"
  st_neg G8 carry-over-red "$d" "$REF_RESOLVED" 'r37-closed=0' && ok=$((ok + 1))
  n=$((n + 1)); d=$MUT/G8-absent; mut_reset "$d"
  mkdir -p -- "$d/corpus"
  st_neg G8 carry-over-suite-absent "$d" "$REF_RESOLVED" 'r37-suite=0' && ok=$((ok + 1))
  st_verdict G8 "$bad" "$ok" "$n"
}

# ---------------------------------------------------------------------------
# selftest report judgement — a summary line alone must never pass
# ---------------------------------------------------------------------------

judge_selftest_report() { # FILE
  local f=$1 cases verdicts summary id hit=0 line n ok det rej dup
  [ -f "$f" ] || return 1
  cases=$(grep -c '^selftest case=' "$f" 2>/dev/null); cases=${cases:-0}
  verdicts=$(grep -c '^selftest case=.*verdict=pass$' "$f" 2>/dev/null); verdicts=${verdicts:-0}
  summary=$(grep -c '^selftest cases=8 failures=0$' "$f" 2>/dev/null); summary=${summary:-0}
  [ "$cases" -eq 8 ] && [ "$verdicts" -eq 8 ] && [ "$summary" -eq 1 ] || return 1
  # Every check id appears exactly once as a passing case line, and that line's
  # mutants=<ok>/<n> must be matched by exactly n `selftest detail=G<i> mutant=`
  # lines of which ok name rejected=1. A fabricated case line carrying
  # `mutants=0/0` (no fixture ran) is rejected: n must be >= 1 and the detail
  # lines must exist.
  for id in "${CHECK_IDS[@]}"; do
    dup=$(grep -c "^selftest case=${id} " "$f" 2>/dev/null); dup=${dup:-0}
    [ "$dup" -eq 1 ] || return 1
    line=$(grep -m1 "^selftest case=${id} " "$f" 2>/dev/null)
    [ -n "$line" ] || return 1
    printf '%s' "$line" | grep -q 'verdict=pass$' || return 1
    n=$(printf '%s' "$line" | sed -n 's/.*mutants=[0-9][0-9]*\/\([0-9][0-9]*\).*/\1/p')
    ok=$(printf '%s' "$line" | sed -n 's/.*mutants=\([0-9][0-9]*\)\/[0-9][0-9]*.*/\1/p')
    [ -n "$n" ] && [ -n "$ok" ] && [ "$n" -ge 1 ] || return 1
    det=$(grep -c "^selftest detail=${id} mutant=" "$f" 2>/dev/null); det=${det:-0}
    rej=$(grep -c "^selftest detail=${id} mutant=.*rejected=1" "$f" 2>/dev/null); rej=${rej:-0}
    [ "$det" -eq "$n" ] && [ "$rej" -eq "$ok" ] && [ "$ok" -eq "$n" ] || return 1
    hit=$((hit + 1))
  done
  [ "$hit" -eq 8 ]
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

  # the 7-case forgery: every line well-formed, one check never ran. The case
  # count and the per-id requirement must both reject it.
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
        printf 'r38-closure: refusing to run against the live worktree: this suite is export-mode only.\n' >&2
        printf 'r38-closure: pass --export-ref <hash> (see --help) or --selftest.\n' >&2
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
