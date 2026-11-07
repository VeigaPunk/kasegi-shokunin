#!/bin/bash
# P5 attack: run the frozen control against scratch lanes whose r84 counter is a mutant.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=/fast/scratch/hyaku/kasegi-r84/MutCounter
CTL=$L/.ufo/waves/round-84/controls/c1-counter-mutants-r84.py
for M in "$@"; do
  D=$S/lane-$M
  mkdir -p $D/.ufo/waves/round-83/c1 $D/.ufo/waves/round-84/c1 $D/w
  cp $L/.ufo/waves/round-83/c1/mutbat.py $D/.ufo/waves/round-83/c1/mutbat.py
  if [ "$M" = "PRISTINE" ]; then cp $L/.ufo/waves/round-84/c1/mutbat.py $D/.ufo/waves/round-84/c1/mutbat.py
  else cp $S/mut/$M.py $D/.ufo/waves/round-84/c1/mutbat.py; fi
  TMPDIR=$D/w python3 -B $CTL --lane $D --work $D/w > $S/receipts/p5-$M.txt 2>&1
  echo "=== lane r84=$M rc=$?"; cat $S/receipts/p5-$M.txt
done
