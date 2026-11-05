#!/bin/bash
# Runs selftest (a) and base census (b) for orig and each mutant; prints one row per run.
S=/fast/scratch/hyaku/kasegi-r73/K73MutateCounter
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
cd "$S" || exit 2
for id in orig M1 M2 M3 M4 M5 M6 M7 M8; do
  if [ "$id" = orig ]; then f="$S/orig.py"; else f="$S/mut-$id.py"; fi
  TMPDIR="$S" python3 "$f" --selftest > "$S/out-$id-selftest.txt" 2>&1; sr=$?
  sl=$(tail -n 1 "$S/out-$id-selftest.txt")
  sl1=$(tail -n 2 "$S/out-$id-selftest.txt" | head -n 1)
  left1=$(ls -d "$S"/recheck-cwd-* 2>/dev/null | wc -l)
  TMPDIR="$S" python3 "$f" --root "$S/base" --lane "$L" > "$S/out-$id-census.txt" 2>&1; cr=$?
  cl=$(tail -n 2 "$S/out-$id-census.txt" | head -n 1)
  cres=$(tail -n 1 "$S/out-$id-census.txt")
  left2=$(ls -d "$S"/recheck-cwd-* 2>/dev/null | wc -l)
  echo "ID=$id | selftest_rc=$sr | selftest_last=[$sl] | leftover_after_selftest=$left1 | census_rc=$cr | census_line=[$cl] | census_result=[$cres] | leftover_after_census=$left2"
done
