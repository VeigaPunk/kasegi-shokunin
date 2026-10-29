#!/usr/bin/env bash
# Round-46 final measurement: one invocation, committed-export basis. Usage: final-measure.sh <tip-rev> <scratch-dir>
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=914ca0b6956f01d87b2e252ffad06fe74ec5d9ba
TIP=$1; S=$2
rm -rf "$S"; mkdir -p "$S/base" "$S/tip"
git -C $L archive $BASE | tar -x -C "$S/base"
git -C $L archive "$TIP" | tar -x -C "$S/tip"
export TMPDIR="$S"
run() { echo "\$ $*"; "$@"; echo "exit=$?"; }
echo "measured-at-rev: $TIP base: $BASE"
cd "$S/tip"
echo "## C1 (depth:verifiability) - counter"
run python3 -B corpus/instruments/r46-c1-gate.py --root "$S/base" --baseline "$S/base" --work "$S"
run python3 -B corpus/instruments/r46-c1-gate.py --root "$S/tip" --baseline "$S/base" --work "$S"
run python3 -B corpus/instruments/freeze-check.py --claims "$S/tip/.ufo/waves/round-46/claims.json" --tool-root "$S/tip" --base "$S/base"
echo "## C1 - plain measures (no python counter)"
for T in base tip; do
  echo "# $T"
  ( cd "$S/$T"; echo "recheck lines guarded by test -d ~/Projects: $(grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l)" )
done
for T in base tip; do echo "# r46-plain-measure.sh $T"; bash "$S/tip/corpus/instruments/r46-plain-measure.sh" "$S/$T"; done
for e in claim-gates.md claim-package-contract.md; do echo "# plain-rows.sh tip $e"; bash "$S/tip/.ufo/waves/round-46/controls/plain-rows.sh" "$S/tip" "$e" | tail -1; done
echo "## C2 (coverage) - counter"
run python3 -B corpus/instruments/r46-c2-gate.py --root "$S/base"
run python3 -B corpus/instruments/r46-c2-gate.py --root "$S/tip"
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/base" --expect 28
run python3 -B corpus/instruments/r44-frontier-count.py --root "$S/tip" --expect 28
echo "## C2 - plain measures"
for T in base tip; do
  ( cd "$S/$T"
    echo "# $T frontier rows: $(grep -cE '^\| F[0-9]+ \|' corpus/README.md)  SOURCES rows: $(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)  knowledge: $(find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l)"
    echo "# $T absence sweep files: $(grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l)" )
done
echo "## selftests (tip export)"
for f in r46-counters-selftest-c1.py r46-counters-selftest-c2.py; do
  [ -f "corpus/instruments/$f" ] && run python3 -B corpus/instruments/$f --lane "$S/tip" --pure "$S/base"
done
[ -f corpus/instruments/r46-landing-gate.py ] && run python3 -B corpus/instruments/r46-landing-gate.py --selftest --work "$S/w3"
echo "## census, recheck, binding, density (tip export; census on the tip SOURCES.md)"
run bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/tip/corpus/SOURCES.md"
run python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073
run python3 -B corpus/instruments/capture-binding-check.py --root "$S/tip"
run python3 -B corpus/instruments/frontier-recheck-count.py --root "$S/tip"
run python3 -B corpus/instruments/density.py SKILL.md --label r46final
(cd "$S/base" && run python3 -B corpus/instruments/density.py SKILL.md --label r46base)
run python3 -B corpus/instruments/anchorcheck.py SKILL.md
echo "## live lane recheck-audit (committed tip, run in the lane itself)"
(cd $L && run python3 -B corpus/instruments/recheck-audit.py --root $L --quiet)
