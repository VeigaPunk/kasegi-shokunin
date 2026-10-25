#!/usr/bin/env bash
# census-grammar-test.sh — round-28 wave-1: run the FLEET census validator (read-only) against
# SCRATCH registries that mimic the two possible adoptions, to measure the staged rows'
# schema conformance against the real grammar.
#
#   scratch A: lane SOURCES.md + staged S042 appended as lane S042   (the planned adoption)
#   scratch B: scratch A + staged S043 appended as a NEW row S043     (the row that must NOT
#              be registered — staged S043 maps onto lane S041 by document)
#
# Writes ONLY under .ufo/waves/round-28/assimilation/schema/.
# The census script is read-only and is invoked with --file (stdout only, no --out).
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
A=$LANE/.ufo/waves/round-28/assimilation
SCH=$A/schema
TODAY=2026-10-25

mkdir -p "$SCH/corpus"

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

echo "== round-28 wave-1 census-grammar test (scratch registries) =="
echo "census: $CENSUS"
echo "today: $TODAY"
echo

# ---- scratch A: lane registry + staged S042 as lane S042 -------------------
{
  cat "$LANE/corpus/SOURCES.md"
  grep -E '^ {0,3}\| *S042 *\|' "$PKG/SOURCES.append.md"
} > "$SCH/corpus/SOURCES.md"
cp "$LANE/corpus/SOURCES.md" "$SCH/corpus/SOURCES.md.lane-only"

echo "-- scratch A (lane registry + staged S042) --"
run "cp $SCH/corpus/SOURCES.md.lane-only $SCH/corpus/SOURCES.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY"
echo

# ---- scratch B: scratch A + staged S043 as a new row ------------------------
{
  grep -E '^ {0,3}\| *S042 *\|' "$PKG/SOURCES.append.md"
  grep -E '^ {0,3}\| *S043 *\|' "$PKG/SOURCES.append.md"
} > "$SCH/staged-extra-rows.md"

{
  cat "$LANE/corpus/SOURCES.md"
  cat "$SCH/staged-extra-rows.md"
} > "$SCH/corpus/SOURCES.md"

echo "-- scratch B (lane registry + staged S042 + staged S043 as a NEW row) --"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY"
echo

echo "-- scratch B: what the duplicate-URL verdict says about S041 vs S043 --"
run "grep -nE '^ {0,3}\\| *S04[13] *\\|' $SCH/corpus/SOURCES.md | cut -c1-150"
