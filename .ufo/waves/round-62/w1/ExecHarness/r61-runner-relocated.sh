#!/usr/bin/env bash
# round-61 C1 python-head confinement probe runner (wave evidence, committed).
# usage: c1-probe-run-r61.sh <figure-audit.py path> <scratch dir>
# Each probe derive runs ALONE through the instrument in its own fresh root. The root holds
# g.txt ("35"), a corpus/instruments/ directory (so the traversal path's intermediates exist),
# an in-instruments counter (tiny-ok.py, prints 35), an out-of-instruments marker script per
# probe, and a symlink inside corpus/instruments/ that resolves outside it.
# A probe is EXECUTED when its MARK-* file appears in its root; REFUSED when the instrument
# exits 2 before running the derive (the gate's refusal path). The instrument path is resolved
# absolute before any cd (R77). Baseline: GNU coreutils, bash and python3.
# Missing instrument, unsafe scratch or fixture setup failure exits nonzero.
set -eu
[ "$#" = 2 ] || { echo "HARNESS-USAGE want-instrument-and-scratch"; exit 2; }
INSTR=$(realpath "$1" 2>/dev/null) || { echo "HARNESS-USAGE missing-instrument"; exit 2; }
S=$(realpath -m "$2" 2>/dev/null) || { echo "HARNESS-USAGE missing-scratch"; exit 2; }
case "$S" in /fast/scratch/hyaku/kasegi-r62/*/*) ;; *) echo "HARNESS-USAGE unsafe-scratch $S"; exit 2;; esac
[ -f "$INSTR" ] || { echo "HARNESS-USAGE not-a-file $INSTR"; exit 2; }
rm -rf -- "$S"
mkdir -p -- "$S" || { echo "HARNESS-USAGE unwritable-scratch $S"; exit 2; }
trap 'rm -rf -- "$S"' EXIT
echo "instrument=$INSTR sha256=$(sha256sum "$INSTR" | cut -c1-16)"
echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

run() {
  id=$1; want=$2; derive=$3; marker=$4
  r="$S/r-$id"
  mkdir -p "$r/corpus/instruments" || { echo "probe=$id HARNESS-FIXTURE-FAIL"; return 1; }
  printf '35\n' > "$r/g.txt"
  printf 'open(%s,"w").write("x")\n' "\"$marker\"" > "$r/outside-$id.py"
  cp -- "$r/outside-$id.py" "$S/outside-$id.py"   # P2's three-up path resolves to $S
  printf 'print(35)\n' > "$r/corpus/instruments/tiny-ok.py"
  ln -sf "$r/outside-$id.py" "$r/corpus/instruments/link-$id.py"
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"probe","recorded":sys.argv[2],"derive":sys.argv[3],"want":sys.argv[2]}]}, open(sys.argv[4],"w"))' "$id" "$want" "$derive" "$r/one.json"
  rc=0
  ( cd "$r" && python3 "$INSTR" --ledger "$r/one.json" --root "$r" > "$r/out.txt" 2>&1 ) || rc=$?
  printf '%s\n' "$rc" > "$r/rc"
  m=$(find "$r" -maxdepth 1 -name 'MARK-*' -type f | wc -l)
  echo "probe=$id derive=$(printf '%s' "$derive" | tr '\n' '|') exit=$(cat "$r/rc") markers=$m :: $(head -1 "$r/out.txt")"
}

# P1/P2/P3: the class under claim — a python-head path that STARTS with corpus/instruments/
# but resolves outside it (two ups, three ups, a symlink) executes on the base gate.
run P1-traversal-2up 35 "python3 corpus/instruments/../../outside-P1-traversal-2up.py" MARK-P1
run P2-traversal-3up 35 "python3 corpus/instruments/../../../outside-P2-traversal-3up.py" MARK-P2
run P3-symlink-out 35 "python3 corpus/instruments/link-P3-symlink-out.py" MARK-P3
# P4: absolute path out of the root is already refused on base (negative control; must stay refused).
run P4-absolute-out 35 "python3 $S/outside-P4-absolute-out.py" MARK-P4
# P5/P6: legitimate counters inside corpus/instruments/ are admitted on both sides (no over-refusal);
# P6 carries a '..' that normalizes back inside.
run P5-inside-ok 35 "python3 corpus/instruments/tiny-ok.py" MARK-P5
run P6-inside-normalized 35 "python3 corpus/instruments/../instruments/tiny-ok.py" MARK-P6
# round-60 regression controls: must stay admitted on both sides.
run CTRL-quoted-semicolon 35 "cat g.txt | grep -e '35' -e ';'" MARK-CTRL1
run CTRL-plain-count 1 "cat g.txt | wc -l" MARK-CTRL2
