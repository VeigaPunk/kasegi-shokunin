#!/usr/bin/env bash
# census-grammar-test3.sh — round-28 wave-1 (v3, robust insertion): run the FLEET census
# validator (read-only, stdout only) against SCRATCH registries that place the candidate row
# INSIDE the `## Registry` section (immediately before the `## Paths` heading), with the
# knowledge tree reachable so E11 is meaningful.
#
#   scratch 0: live lane registry as-is
#   scratch 1: live registry + the PACKAGE's own staged S042 row appended as a SECOND S042 row
#   scratch 2: live registry + the PACKAGE's own staged S043 row appended as a new row
#
# Writes ONLY under .ufo/waves/round-28/assimilation/schema3/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
A=$LANE/.ufo/waves/round-28/assimilation
SCH=$A/schema3
TODAY=2026-10-25

rm -rf "$SCH"
mkdir -p "$SCH/corpus"
ln -s "$LANE/corpus/knowledge" "$SCH/corpus/knowledge"

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

build() { # <outfile> <rowfile>
  python3 - "$LANE/corpus/SOURCES.md" "$2" "$1" <<'PY'
import sys
src, rowfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
row = open(rowfile, encoding='utf-8').read().rstrip('\n')
lines = open(src, encoding='utf-8').read().split('\n')
idx = next(i for i, l in enumerate(lines) if l.lstrip(' ').startswith('## Paths'))
lines.insert(idx, row)
open(out, 'w', encoding='utf-8').write('\n'.join(lines))
print(f"inserted staged row before line {idx+1} (## Paths)")
PY
}

echo "== round-28 wave-1 census-grammar test v3 (rows inside the Registry section) =="
echo "census: $CENSUS   today: $TODAY"
echo

echo "-- scratch 0: live lane registry as-is --"
cp "$LANE/corpus/SOURCES.md" "$SCH/corpus/SOURCES.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE '	E11	'"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -E '	E11	'"
echo

echo "-- scratch 1: live registry + the PACKAGE's own staged S042 row (duplicate id test) --"
grep -E '^ {0,3}\| *S042 *\|' "$PKG/SOURCES.append.md" > "$SCH/staged-S042.md"
build "$SCH/corpus/SOURCES.md" "$SCH/staged-S042.md"
run "grep -nE '^ {0,3}\| *S04[12] *\\|' $SCH/corpus/SOURCES.md | cut -c1-90"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE '	E11	'"
echo

echo "-- scratch 2: live registry + the PACKAGE's own staged S043 row (new-id test) --"
grep -E '^ {0,3}\| *S043 *\|' "$PKG/SOURCES.append.md" > "$SCH/staged-S043.md"
build "$SCH/corpus/SOURCES.md" "$SCH/staged-S043.md"
run "grep -nE '^ {0,3}\| *S04[123] *\\|' $SCH/corpus/SOURCES.md | cut -c1-90"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE '	E11	'"
echo

echo "-- scratch 2 detail: the E04/W04 duplicate-url verdicts for the S041/S043 pair --"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -E 'S041|S043'"
