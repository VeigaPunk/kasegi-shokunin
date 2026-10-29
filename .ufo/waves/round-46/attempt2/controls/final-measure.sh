#!/usr/bin/env bash
# Round-46 attempt-2 final measurement: one invocation, committed-export basis. Usage: final-measure.sh <tip-rev> <scratch-dir>
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=04af9bc92229232ea5cce8b32bfe59dd969eb26d
PURE=/fast/scratch/hyaku/kasegi-r46/L1/pure2
TIP=$1; S=$2
rm -rf "$S"; mkdir -p "$S/base" "$S/tip"
git -C $L archive $BASE | tar -x -C "$S/base"
git -C $L archive "$TIP" | tar -x -C "$S/tip"
export TMPDIR="$S"
run() { echo "\$ $*"; "$@"; echo "exit=$?"; }
echo "measured-at-rev: $TIP base: $BASE"
cd "$S/tip"
echo "## C1 (depth:verifiability) - the battery, before-value replay at base and after at tip"
run python3 -B corpus/instruments/r46-mutbat.py --root "$S/base" --pure "$PURE" --work "$S/w-base" --counter both --jobs 8
run python3 -B corpus/instruments/r46-mutbat.py --root "$S/tip" --pure "$PURE" --work "$S/w-tip" --counter both --jobs 8
echo "## C1 - extended selftest baselines (tip export)"
run python3 -B corpus/instruments/r46-counters-selftest-c1.py --pure "$PURE" --work "$S/w-s1" --jobs 8
run python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure "$PURE"
[ -f corpus/instruments/r46-selftest-f29.py ] && run python3 -B corpus/instruments/r46-selftest-f29.py --work "$S/w-s3"
echo "## C1 - plain measures (no battery)"
for T in base tip; do
  ( cd "$S/$T"; echo "# $T case counts: $(grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py 2>/dev/null) c1 $(grep -c 'def case_' corpus/instruments/r46-counters-selftest-c2.py 2>/dev/null) c2" )
done
echo "## C2 (coverage) - admission gate"
run python3 -B corpus/instruments/r46-f29-gate.py --root "$S/base"
run python3 -B corpus/instruments/r46-f29-gate.py --root "$S/tip"
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/base" --expect 28
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/tip" --expect 29
echo "## C2 - plain measures"
for T in base tip; do
  ( cd "$S/$T"
    echo "# $T frontier rows: $(grep -cE '^\| F[0-9]+ \|' corpus/README.md)  SOURCES rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)  knowledge: $(find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l)"
    echo "# $T absence sweep files: $(grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l)" )
done
echo "## prior-attempt instruments on the same exports (no-harm; the C1 gate's baseline is the attempt-1 pre-round base 914ca0b — its L2 measures the attempt-1 re-grounding)"
mkdir -p "$S/base-914"; git -C $L archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba | tar -x -C "$S/base-914"
run python3 -B corpus/instruments/r46-c1-gate.py --root "$S/tip" --baseline "$S/base-914" --work "$S/w-h1"
run python3 -B corpus/instruments/r46-c1-gate.py --root "$S/base-914" --baseline "$S/base-914" --work "$S/w-h1"
echo "## r46-c2-gate.py v1.3 (attempt-2 erratum E3: the ledger exemption) at its era export and at this tip"
mkdir -p "$S/era-eb874bc"; git -C $L archive eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7 | tar -x -C "$S/era-eb874bc"
cp corpus/instruments/r46-c2-gate.py "$S/era-eb874bc/corpus/instruments/r46-c2-gate.py"
run python3 -B "$S/era-eb874bc/corpus/instruments/r46-c2-gate.py" --root "$S/era-eb874bc"
echo "# (expected 7/7: the v1.3 amendment keeps the attempt-1 receipts reproducible at the attempt-1 tree; the counter's v1.3 bytes are the only difference)"
run python3 -B corpus/instruments/r46-c2-gate.py --root "$S/tip"
echo "# (the tip reading moves G1 28->29 and G6 65->66 BY THIS ROUND'S LANDING: the attempt-1 counter names the attempt-1 after-state; the moved limbs are this round's C2 after-state, graded by r46-f29-gate.py)"
echo "## census, recheck, binding, density (tip export)"
run bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/tip/corpus/SOURCES.md"
run python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
run python3 -B corpus/instruments/capture-binding-check.py --root "$S/tip"
run python3 -B corpus/instruments/frontier-recheck-count.py --root "$S/tip"
run python3 -B corpus/instruments/density.py SKILL.md --label r46b-final
(cd "$S/base" && run python3 -B corpus/instruments/density.py SKILL.md --label r46b-base)
run python3 -B corpus/instruments/anchorcheck.py SKILL.md
echo "## live lane recheck-audit (committed tip, run in the lane itself)"
(cd $L && run python3 -B corpus/instruments/recheck-audit.py --root $L --quiet)
