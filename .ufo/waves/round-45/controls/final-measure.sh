#!/usr/bin/env bash
# Round-45 final measurement: one invocation, committed-export basis. Usage: final-measure.sh <tip-rev> <scratch-dir>
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=dc5bb8c6e31efc4a6650819df85e79b72fd64bcd
TIP=$1; S=$2
rm -rf "$S"; mkdir -p "$S/base" "$S/tip"
git -C $L archive $BASE | tar -x -C "$S/base"
git -C $L archive "$TIP" | tar -x -C "$S/tip"
export TMPDIR="$S"
run() { echo "\$ $*"; "$@"; echo "exit=$?"; }
echo "measured-at-rev: $TIP base: $BASE"
cd "$S/tip"
echo "## C1 (depth:verifiability)"
run python3 -B corpus/instruments/r45-routed-defects.py --root "$S/base" --baseline "$S/base"
run python3 -B corpus/instruments/r45-routed-defects.py --root "$S/tip" --baseline "$S/base"
run python3 -B corpus/instruments/freeze-check.py --claims "$S/tip/.ufo/waves/round-45/claims.json" --tool-root "$S/tip" --base "$S/base"
run python3 -B corpus/instruments/freeze-check.py --selftest --work "$S/w1"
run python3 -B corpus/instruments/r44-frontier-count.py --selftest --work "$S/w2"
run python3 -B corpus/instruments/r45-counters-selftest-c1.py --lane "$S/tip" --base "$S/base"
echo "## C2 (coverage)"
run python3 -B corpus/instruments/r45-c2-gate.py --root "$S/base"
run python3 -B corpus/instruments/r45-c2-gate.py --root "$S/tip"
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/base" --expect 27
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/tip" --expect 27
run python3 -B corpus/instruments/r45-counters-selftest-c2.py --lane "$S/tip"
echo "## counting commands (CORPUS.md rules)"
( cd "$S/base"; echo "base SOURCES rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)  knowledge: $(find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l)" )
( cd "$S/tip"; echo "tip SOURCES rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)  knowledge: $(find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l)" )
echo "## census, recheck, binding, density (tip export; census on the tip SOURCES.md)"
run bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/tip/corpus/SOURCES.md"
run python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071
run python3 -B corpus/instruments/source-recheck.py --manifest .ufo/waves/round-45/source-recon/S072.manifest.json --source S072
run python3 -B corpus/instruments/capture-binding-check.py --root "$S/tip"
run python3 -B corpus/instruments/frontier-recheck-count.py --root "$S/tip"
run python3 -B corpus/instruments/density.py SKILL.md --label r45final
(cd "$S/base" && run python3 -B corpus/instruments/density.py SKILL.md --label r45base)
run python3 -B corpus/instruments/anchorcheck.py SKILL.md
