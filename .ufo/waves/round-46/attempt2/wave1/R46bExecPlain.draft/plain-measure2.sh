#!/usr/bin/env bash
# plain-measure2.sh <tree> — round-46 (attempt 2) PLAIN measurement, seat R46bExecPlain (DRAFT).
#
# One invocation, one line per measurement, nine lines total, machine-parseable
# (`key=value`; the two counter lines quote the counter's own words verbatim).
#
#   a_frontier_rows=<n>       grep -cE '^\| F[0-9]+ \|' <tree>/corpus/README.md
#   b_frontier_counter=<...>   r44-frontier-count.py --root <scratch COPY of tree> --expect 29
#   c_sources_rows=<n>         grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <tree>/corpus/SOURCES.md
#   d_knowledge_files=<n>      find <tree>/corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
#   e_absence_sweep_files=<n>  grep -rliE 'repository securit. advisor|GHSA' <tree>/corpus/knowledge
#                              <tree>/corpus/SOURCES.md <tree>/corpus/README.md | wc -l
#   f_selftest_c1=<last line>  r46-counters-selftest-c1.py --pure PURE --work W --jobs 8 | tail -1
#   f_selftest_c2=<last line>  r46-counters-selftest-c2.py --pure PURE | tail -1
#   g_battery_c1=<summary>     r46-mutbat.py --root <tree> --pure PURE --work W --counter c1 --jobs 8
#   g_battery_c2=<summary>     r46-mutbat.py --root <tree> --pure PURE --work W --counter c2 --jobs 8
#
# BEFORE-values (the frozen base 04af9bc92229232ea5cce8b32bfe59dd969eb26d export):
#   a=28  b="frontier rows=28 admitted=28" (exit 1, SHORT of 29)  c=73  d=65  e=2
#   f="selftest cases=76 failures=0" / "selftest cases=137 failures=0"
#   g="mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0"
#     "mutbat counter=c2 mutants=21 caught=8  equivalent=0 uncaught=13 baseline_failures=0"
#   (the g pair is the committed receipt .ufo/waves/round-46/attempt2/controls/mutbat-before.txt)
# AFTER-values (the C2 target, for discrimination): a=29, b exit 0 (admitted=29), c>=74,
#   d=66, e=4, g uncaught=0 on both counters.
#
# WHY THE SCRIPTED FORM DIFFERS FROM THE CARD'S PROSE IN THREE PLACES (all documented,
# all behaviour-preserving for the measurement):
#   1. the frontier counter (b) runs against a scratch COPY of the tree, never the tree
#      itself: the copy is a byte copy of <tree>/corpus (the only bytes the counter reads)
#      and the copy is removed on exit, so the counter provably cannot mutate the tree.
#   2. the two selftests are bound to the tree under test with `--lane <tree>`, because
#      the counter a selftest grades is the one in `--lane`; without it both runs would
#      grade the LIVE LANE's counter and the base export's line would not be about the
#      base export.  `--work`/`--jobs` are only accepted by the c1 selftest; the c2
#      selftest's argparse rejects them (exit 2), so the c2 twin is run in the form its
#      own usage line documents (`--pure` only) and the form actually used is recorded.
#   3. the battery (g) is run as two parallel mutbat invocations (one per counter)
#      instead of one `--counter both` invocation: the summary lines are byte-identical
#      per counter and the wall time is the slower counter instead of their sum.
#
# ENV KNOBS
#   HYAKU_SCRATCH             scratch root (default /fast/scratch/hyaku); the script's own
#                             scratch is $HYAKU_SCRATCH/kasegi-r46/R46bExecPlain
#   PLAIN2_PURE               the pure base export (default /fast/scratch/hyaku/kasegi-r46/L1/pure2)
#   PLAIN2_LANE               the lane repo holding the instruments
#                             (default /home/vgpnk/Projects/shokunin/kasegi-shokunin)
#   PLAIN2_BATTERY_COUNTERS   which battery counters to run: "c1 c2" (default), "c1", "c2", or "none"
#   PLAIN2_BATTERY_TIMEOUT    seconds per battery invocation (default 0 = no limit)
#   PLAIN2_KEEP               1 = keep the scratch dir (default: removed on exit)
#
# The tree is only READ.  Nothing is written into <tree>; every byte this script writes
# lands under its scratch dir, which is removed on exit.
set -u

[ $# -eq 1 ] && [ -d "$1" ] || { echo "usage: plain-measure2.sh <tree>" >&2; exit 2; }

LANE=${PLAIN2_LANE:-/home/vgpnk/Projects/shokunin/kasegi-shokunin}
PURE=${PLAIN2_PURE:-/fast/scratch/hyaku/kasegi-r46/L1/pure2}
SCRATCH_BASE=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
SEAT=${PLAIN2_SCRATCH:-$SCRATCH_BASE/kasegi-r46/R46bExecPlain}
BATT_COUNTERS=${PLAIN2_BATTERY_COUNTERS:-c1 c2}
BATT_TIMEOUT=${PLAIN2_BATTERY_TIMEOUT:-0}

T=$(cd "$1" && pwd -P) || exit 2
[ -d "$PURE" ] || { echo "plain-measure2: pure export missing: $PURE" >&2; exit 2; }

S="$SEAT"
rm -rf "$S"
mkdir -p "$S/tmp" "$S/w" || { echo "plain-measure2: cannot create scratch $S" >&2; exit 2; }
cleanup() { [ "${PLAIN2_KEEP:-0}" = "1" ] || rm -rf -- "$S"; }
trap cleanup EXIT
export TMPDIR="$S/tmp"          # explicit: never rely on an inherited TMPDIR
export HYAKU_SCRATCH="$S"        # the c2 selftest builds its scratch under $HYAKU_SCRATCH
export PYTHONDONTWRITEBYTECODE=1

INSTR="$LANE/corpus/instruments"

# ---------------------------------------------------------------- (a) frontier rows
a=$(grep -cE '^\| F[0-9]+ \|' "$T/corpus/README.md")

# ---------------------------------------------------------------- (b) frontier counter
# scratch COPY of the tree (the counter reads <tree>/corpus/README.md only; .git and .ufo
# are excluded from the copy because no corpus byte lives in them)
DCOPY="$S/tree-copy"
mkdir -p "$DCOPY"
( cd "$T" && tar --exclude=./.git --exclude=./.ufo -cf - . ) | tar -xf - -C "$DCOPY"
b_out=$(python3 "$INSTR/r44-frontier-count.py" --root "$DCOPY" --expect 29 2>&1)
b_rc=$?
b=$(printf '%s' "$b_out" | tr '\n' ';')
b="frontier rows/admitted=[$b] exit=$b_rc"

# ---------------------------------------------------------------- (c) SOURCES rows
c=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$T/corpus/SOURCES.md")

# ---------------------------------------------------------------- (d) knowledge files
d=$(find "$T/corpus/knowledge" -maxdepth 1 -name '*.md' | wc -l)

# ---------------------------------------------------------------- (e) absence sweep
e=$(grep -rliE 'repository securit. advisor|GHSA' "$T/corpus/knowledge" "$T/corpus/SOURCES.md" "$T/corpus/README.md" | wc -l)

# ---------------------------------------------------------------- (f) selftest baselines
mkdir -p "$S/w/c1"
f1_out=$( (cd "$T" && python3 "$INSTR/r46-counters-selftest-c1.py" --lane "$T" --pure "$PURE" --work "$S/w/c1" --jobs 8) 2>&1 )
f1_rc=$?
f1=$(printf '%s' "$f1_out" | tail -1)
# the c2 selftest takes neither --work nor --jobs: try the twin form first, fall back
# to the form its own usage line documents, and record which form was used.
mkdir -p "$S/w/c2"
f2_out=$( (cd "$T" && python3 "$INSTR/r46-counters-selftest-c2.py" --lane "$T" --pure "$PURE" --work "$S/w/c2" --jobs 8) 2>&1 )
f2_rc=$?
f2_form="--pure --work --jobs"
if [ "$f2_rc" -eq 2 ]; then
  f2_form="--pure only (--work/--jobs rejected by argparse: $(printf '%s' "$f2_out" | grep -m1 'unrecognized arguments'))"
  f2_out=$( (cd "$T" && python3 "$INSTR/r46-counters-selftest-c2.py" --lane "$T" --pure "$PURE") 2>&1 )
  f2_rc=$?
fi
f2=$(printf '%s' "$f2_out" | tail -1)

# ---------------------------------------------------------------- (g) mutation battery
b_c1="not-run"; b_c2="not-run"
run_battery() {
  # $1 = counter (c1|c2); writes the summary line to stdout
  local w="$S/w/bat-$1" log="$S/w/bat-$1.log"
  mkdir -p "$w"
  local cmd=(python3 "$INSTR/r46-mutbat.py" --root "$T" --pure "$PURE" --work "$w" --counter "$1" --jobs 8)
  if [ "$BATT_TIMEOUT" -gt 0 ] 2>/dev/null; then
    timeout "$BATT_TIMEOUT" "${cmd[@]}" >"$log" 2>&1
  else
    "${cmd[@]}" >"$log" 2>&1
  fi
  local rc=$?
  grep -E '^mutbat counter=' "$log" | tail -1 || true
  return $rc
}
battery_pids=""
for cc in $BATT_COUNTERS; do
  case "$cc" in
    c1|c2) ;;
    none) continue ;;
    *) echo "plain-measure2: unknown battery counter '$cc'" >&2; exit 2 ;;
  esac
  run_battery "$cc" >"$S/w/bat-$cc.out" 2>/dev/null &
  battery_pids="$battery_pids $!:$cc"
done
for entry in $battery_pids; do
  pid=${entry%%:*}
  cc=${entry##*:}
  wait "$pid" 2>/dev/null
  line=$(cat "$S/w/bat-$cc.out" 2>/dev/null | tail -1)
  case "$cc" in
    c1) b_c1="${line:-ERROR: no summary line}" ;;
    c2) b_c2="${line:-ERROR: no summary line}" ;;
  esac
done

printf 'a_frontier_rows=%s\n' "$a"
printf 'b_frontier_counter=%s\n' "$b"
printf 'c_sources_rows=%s\n' "$c"
printf 'd_knowledge_files=%s\n' "$d"
printf 'e_absence_sweep_files=%s\n' "$e"
printf 'f_selftest_c1=%s (rc=%s)\n' "$f1" "$f1_rc"
printf 'f_selftest_c2=%s (rc=%s; form: %s)\n' "$f2" "$f2_rc" "$f2_form"
printf 'g_battery_c1=%s\n' "$b_c1"
printf 'g_battery_c2=%s\n' "$b_c2"

# optional: keep the battery logs (per-mutant lines) outside the scratch dir
if [ -n "${PLAIN2_LOG_DIR:-}" ]; then
  mkdir -p "$PLAIN2_LOG_DIR" 2>/dev/null
  for f in "$S"/w/bat-*.log "$S"/w/bat-*.out; do
    [ -f "$f" ] && cp -f "$f" "$PLAIN2_LOG_DIR/" 2>/dev/null
  done
  : >"$PLAIN2_LOG_DIR/LASTLINE.txt"
  printf '%s\n' "$a" "$b" "$c" "$d" "$e" "$f1" "$f2" "$b_c1" "$b_c2" >>"$PLAIN2_LOG_DIR/LASTLINE.txt"
fi
