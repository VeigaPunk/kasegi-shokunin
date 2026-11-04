#!/usr/bin/env bash
# usage: run.sh <tree-dir> <label> [census-explicit-dir]
T=$1; LABEL=$2; EXPL=$3
export TMPDIR=/fast/scratch/hyaku/kasegi-r68/ExecC2Counters/tmp
mkdir -p "$TMPDIR"
cd "$T" || exit 9
echo "=== $LABEL tree=$T"
echo "\$ python3 corpus/instruments/frontier-recheck-count.py"
python3 corpus/instruments/frontier-recheck-count.py; echo "[exit=$?]"
echo "\$ python3 corpus/instruments/capture-binding-check.py"
python3 corpus/instruments/capture-binding-check.py; echo "[exit=$?]"
echo "\$ wc -l corpus/instruments/knowledge-expected.txt"
wc -l corpus/instruments/knowledge-expected.txt; echo "[exit=$?]"
echo "\$ grep -vc '^#' corpus/instruments/knowledge-expected.txt"
grep -vc '^#' corpus/instruments/knowledge-expected.txt; echo "[exit=$?]"
echo "\$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi"
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "[exit=$?]"
if [ -n "$EXPL" ]; then
  echo "\$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate $EXPL"
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate "$EXPL"; echo "[exit=$?]"
fi
