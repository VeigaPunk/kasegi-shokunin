#!/usr/bin/env bash
# noharm.sh <base-rev> <tree>  -- round-46 attempt-2 no-harm / no-regression sheet.
#
# Usage:  noharm.sh [<base-rev>] [<tree>]
#   <base-rev>  git revision the wave is measured against (default: the frozen
#               attempt-2 base 04af9bc92229232ea5cce8b32bfe59dd969eb26d)
#   <tree>      tree to measure: a lane working tree or an exported tree
#               (default: the live lane /home/vgpnk/Projects/shokunin/kasegi-shokunin)
#
# Reads the lane, writes nothing in it.  All scratch lives under
# $HYAKU_SCRATCH/kasegi-r46/R46bExecNoharm-* and is removed on exit.
#
# Sections (all seven card items, in order):
#   (1) no-harm budget: every DELETED line outside the wave dir, named by file
#       and classified PRE-JUSTIFIED (a recheck-line replacement in one of the
#       two prior-attempt re-grounded entries) or FINDING (anything else)
#   (1b) prior-attempt recheck replacement accounting (the two entries)
#   (2) density.py
#   (3) anchorcheck.py
#   (4) capture-binding-check.py
#   (5) recheck-audit.py
#   (6) frontier-recheck-count.py
#   (7) the two prior-attempt counters r46-c1-gate.py / r46-c2-gate.py:
#       base-vs-base (do-nothing control), base-vs-tree (base-vs-live)
#   (7b) receipt replay at the attempt-1 receipt inputs (base 914ca0b)
set -u

L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=${1:-04af9bc92229232ea5cce8b32bfe59dd969eb26d}
TREE=${2:-$L}
R15BASE=${NOHARM_R15_BASE:-914ca0b6956f01d87b2e252ffad06fe74ec5d9ba}
WAVE_EXCLUDE=':(exclude).ufo/waves/round-46/attempt2'

# the two entries the prior attempt re-grounded (their recheck line was replaced)
REGROUND="corpus/knowledge/claim-gates.md corpus/knowledge/claim-package-contract.md"

[ -d "$TREE" ] || { echo "noharm.sh: tree $TREE is not a directory" >&2; exit 2; }
case "$TREE" in /*) ;; *) TREE=$(cd "$TREE" && pwd -P) ;; esac

SCRATCH_ROOT=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
mkdir -p "$SCRATCH_ROOT/kasegi-r46" || exit 2
S=$(mktemp -d -p "$SCRATCH_ROOT/kasegi-r46" R46bExecNoharm-XXXXXX) || exit 2
trap 'rm -rf -- "$S"' EXIT
export TMPDIR="$S"
export PYTHONDONTWRITEBYTECODE=1

echo "noharm.sh  base=$BASE  tree=$TREE"
echo "scratch=$S (removed on exit)"
echo

# ------------------------------------------------------------------ helpers
run() {  # run <label> <cmd...>   -> prints the command, its output, its exit code
  local label=$1; shift
  echo "--- $label \$ $*"
  "$@" 2>&1 | sed 's/^/    /'
  local rc=${PIPESTATUS[0]}
  echo "    exit=$rc"
  echo
}

# ------------------------------------------------------------------ (1)
echo "== (1) no-harm budget: deleted lines outside the wave dir =="
echo "--- (1a) \$ git -C $L diff --numstat $BASE -- . $WAVE_EXCLUDE"
git -C "$L" diff --numstat "$BASE" -- . "$WAVE_EXCLUDE" | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "--- (1b) deleted lines, named by file, classified"
git -C "$L" diff -U0 "$BASE" -- . "$WAVE_EXCLUDE" \
| awk '
    function strip(p) { if (p ~ /^[a-z]\//) return substr(p, 3); return p }
    /^--- /                { a = strip(substr($0, 5)); next }
    /^\+\+\+ /             { b = strip(substr($0, 5)); file = (b == "/dev/null") ? a : b; next }
    /^-/ && !/^--- /       { print file "\t" substr($0, 2) }
  ' > "$S/deleted.tsv"
awk -v reground="$REGROUND" '
    BEGIN { n_pre = 0; n_find = 0 }
    {
      path = $0; sub(/\t.*$/, "", path)
      line = $0; sub(/^[^\t]*\t/, "", line)
      is_reground = (index(" " reground " ", " " path " ") > 0)
      is_recheck  = (line ~ /^recheck:/)
      if (is_reground && is_recheck) { n_pre++; print "PRE-JUSTIFIED  DELETED " path ": " line }
      else                         { n_find++; print "FINDING        DELETED " path ": " line }
    }
    END {
      print "SUMMARY deleted_lines=" (n_pre + n_find) " pre_justified=" n_pre " findings=" n_find
    }
  ' "$S/deleted.tsv" | sed 's/^/    /'
echo
echo "--- (1c) the same diff restricted to the two prior-attempt re-grounded entries"
git -C "$L" diff --numstat "$R15BASE" -- $REGROUND | sed 's/^/    /'
echo "    (expect: 1 deletion per entry -- the replaced recheck line)"
git -C "$L" diff -U0 "$R15BASE" -- $REGROUND \
| awk '
    function strip(p) { if (p ~ /^[a-z]\//) return substr(p, 3); return p }
    /^--- /                { a = strip(substr($0, 5)); next }
    /^\+\+\+ /             { b = strip(substr($0, 5)); file = (b == "/dev/null") ? a : b; next }
    /^-/ && !/^--- /       { print "    DELETED " file ": " substr($0, 2) }
  '
echo

# ------------------------------------------------------------------ (2)..(6)
run "(2)" python3 "$L/corpus/instruments/density.py" "$TREE/SKILL.md"
run "(3)" python3 "$L/corpus/instruments/anchorcheck.py" "$TREE/SKILL.md"
run "(4)" python3 "$L/corpus/instruments/capture-binding-check.py" --root "$TREE"
run "(5)" python3 "$L/corpus/instruments/recheck-audit.py" --root "$TREE" --quiet
run "(6)" python3 "$L/corpus/instruments/frontier-recheck-count.py" --root "$TREE"

# ------------------------------------------------------------------ (7)
mkdir -p "$S/base" "$S/r15base"
git -C "$L" archive "$BASE"    | tar -x -C "$S/base"
git -C "$L" archive "$R15BASE" | tar -x -C "$S/r15base"

echo "== (7) the prior-attempt counters (r46-c1-gate.py, r46-c2-gate.py) =="
echo "--- (7a) do-nothing control: c1 --root <base export> --baseline <base export>"
python3 "$L/corpus/instruments/r46-c1-gate.py" --root "$S/base" --baseline "$S/base" --work "$S/w-bb" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "--- (7b) base-vs-live: c1 --root <tree> --baseline <base export>"
python3 "$L/corpus/instruments/r46-c1-gate.py" --root "$TREE" --baseline "$S/base" --work "$S/w-bl" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "--- (7c) do-nothing control: c2 --root <base export>"
python3 "$L/corpus/instruments/r46-c2-gate.py" --root "$S/base" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "--- (7d) base-vs-live: c2 --root <tree>"
python3 "$L/corpus/instruments/r46-c2-gate.py" --root "$TREE" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "--- (7e) receipt replay at the attempt-1 receipt inputs (base $R15BASE)"
echo "    (attempt-1 receipt: c1 --root tip --baseline r15base -> 7/7 green; c2 --root r15base -> 1/7 red)"
python3 "$L/corpus/instruments/r46-c1-gate.py" --root "$TREE" --baseline "$S/r15base" --work "$S/w-r15" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
python3 "$L/corpus/instruments/r46-c2-gate.py" --root "$S/r15base" 2>&1 | tail -1 | sed 's/^/    /'
echo "    exit=${PIPESTATUS[0]}"
echo
echo "== end noharm.sh =="
