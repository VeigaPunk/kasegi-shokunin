#!/usr/bin/env bash
# round-57 gate-final sequence. Run from the lane root:
#   bash .ufo/waves/round-57/controls/gate-final-r57.sh > .ufo/waves/round-57/controls/gate-final-r57.txt 2>&1
# The receipt is this script's stdout+stderr as printed by one run (R39): no hand-written header.
cd "$(dirname "$0")/../../../.." || exit 9
echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(uname -n) base=$(git rev-parse --short HEAD 2>/dev/null)"
echo '$ python3 corpus/instruments/resolve.py .'
python3 corpus/instruments/resolve.py . 2>&1 | tail -3; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python3 corpus/instruments/census-freshness-check.py .'
python3 corpus/instruments/census-freshness-check.py . 2>&1 | tail -2; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python corpus/instruments/figure-audit.py | tail -1'
python corpus/instruments/figure-audit.py | tail -1; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python corpus/instruments/frontier-recheck-count.py | grep -E "FRONTIER-CENSUS|FRONTIER-PASS F38|entries="'
python corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F38|entries='; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089 | tail -1'
python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089 | tail -1; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S090 | tail -1'
python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S090 | tail -1; echo "[exit=${PIPESTATUS[0]}]"
echo '$ python corpus/instruments/capture-binding-check.py | tail -1'
python corpus/instruments/capture-binding-check.py | tail -1; echo "[exit=${PIPESTATUS[0]}]"
echo '$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi'
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi | tail -1; echo "[exit=${PIPESTATUS[0]}]"
echo '$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt'
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt && echo sort-ok; echo "[exit=$?]"
echo '$ counts: F-rows, registry rows, knowledge files, expected entries'
echo "F-rows=$(grep -cE '^\| F[0-9]+ \|' corpus/README.md) registry=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md) knowledge=$(ls corpus/knowledge/*.md | wc -l) expected=$(grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt)"
