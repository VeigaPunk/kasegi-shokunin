#!/usr/bin/env bash
set -u
S=/fast/scratch/hyaku/kasegi-r89/ExecC1Indep
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=090a46f89932324787e00ca20b1007f893934c9a
LAND=eb5f0df8eaceca617465e493c710e8626e9aa618
export TMPDIR=$S
D=$S/land/c1
rm -rf "$D"
git clone --shared --quiet "$LANE" "$D" || { echo "CLONE FAILED"; exit 3; }
TL=$(git -C "$D" rev-parse --show-toplevel)
test "$TL" = "$D" || { echo "TOPLEVEL MISMATCH: $TL"; exit 3; }
git -C "$D" checkout --quiet "$LAND"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "TOPLEVEL MISMATCH AFTER CHECKOUT"; exit 3; }
echo "--- frozen file digests on disk (must equal claims.json pins):"
sha256sum "$LANE/.ufo/waves/round-89/c1/knowledge-meter.py" \
          "$LANE/.ufo/waves/round-89/c1/repair-map.json" \
          "$LANE/.ufo/waves/round-89/c1/labels.tsv" | sed "s#$LANE/##"
echo '=== INDEPENDENT METER (ExecC1Indep) ==='
python3 -B "$S/indep_meter.py" --lane "$D" --base-rev "$BASE" --after-rev "$LAND" \
  --map "$LANE/.ufo/waves/round-89/c1/repair-map.json" \
  --labels "$LANE/.ufo/waves/round-89/c1/labels.tsv" \
  --work "$S/work" 2>&1 | tee "$S/indep-out.txt"
echo "indep_rc=${PIPESTATUS[0]}"
echo '=== FROZEN COUNTER (knowledge-meter.py) on shared clone of the landing ==='
python3 -B "$LANE/.ufo/waves/round-89/c1/knowledge-meter.py" --lane "$D" --base-rev "$BASE" --after-rev "$LAND" \
  --map "$LANE/.ufo/waves/round-89/c1/repair-map.json" \
  --labels "$LANE/.ufo/waves/round-89/c1/labels.tsv" \
  --target 785/1797 \
  --map-sha256 c29f4c2186ed13495a9b03866f2412c6da5b95f7425b93f7dd1675a986d0e2ec \
  --labels-sha256 8aed5bded717a92df78943ea41332bd3a46b90858ec1396bc797eec85644050d \
  --work "$S/meterwork" 2>&1 | tee "$S/counter-out.txt"
echo "counter_rc=${PIPESTATUS[0]}"
echo '=== P2 PIN RECHECK (all claims.json instrument pins at C1 landing) ==='
python3 -B "$S/pins_check.py" 2>&1 | tee "$S/pins-out.txt"
echo "pins_rc=${PIPESTATUS[0]}"
echo '--- clone HEAD:'
git -C "$D" log --oneline -1
