#!/bin/sh
# Run the copied (single-line-meter-parameterized) round-95 control harness
# against one mutant per argument, pinned to cand53 = 53ec479 (C1 landing).
S=/fast/scratch/hyaku/kasegi-r95/MutC1Counter
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
R93="$L/.ufo/waves/round-93/c1/knowledge-meter.py"
for name in "$@"; do
  mkdir -p "$S/work/$name" "$S/out/$name"
  if [ "$name" = "pristine53" ]; then
    METER_PATH="$S/mutants/pristine.py"
  else
    METER_PATH="$S/mutants/$name.py"
  fi
  echo "=== RUN $name meter=$METER_PATH $(date -Is)" >> "$S/log/runs.txt"
  METER_PATH="$METER_PATH" TMPDIR="$S" python3 -B "$S/harness.py" "$S/cand53" "$R93" "$S/work/$name" "$S/out/$name" > "$S/log/$name.log" 2>&1
  rc=$?
  echo "=== END $name rc=$rc $(date -Is)" >> "$S/log/runs.txt"
done
