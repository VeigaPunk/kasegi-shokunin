#!/usr/bin/env bash
# census-grammar-test2.sh — round-28 wave-1 (corrected): run the FLEET census validator
# (read-only, stdout only) against SCRATCH registries that place the candidate row INSIDE the
# `## Registry` section, with the knowledge tree reachable so E11 is meaningful.
#
#   scratch 0: live lane registry as-is (S042 already appended by ScribeRegistryC2)
#   scratch 1: live lane registry + STAGED S042 row (the package's own wording) inside Registry
#   scratch 2: live lane registry + STAGED S043 row inside Registry (the row that must NOT be
#              registered as a new id — it is the SAME document as lane S041)
#
# Writes ONLY under .ufo/waves/round-28/assimilation/schema2/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
A=$LANE/.ufo/waves/round-28/assimilation
SCH=$A/schema2
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

# insert a row file right before the `## Paths` heading (i.e. at the end of the Registry section)
build() { # <outfile> <rowfile...>
  local out=$1; shift
  awk -v rowfile="$(printf '%s|' "$@")" 'BEGIN{ rows=""; n=split(rowfile,arr,"|"); for(i=1;i<=n;i++) if(arr[i]!="") rows=rows arr[i] "\n" }
    /^ {0,3}## Paths/ { printf "%s", rows }
    { print }' "$LANE/corpus/SOURCES.md" > "$out"
}

echo "== round-28 wave-1 census-grammar test v2 (rows inside the Registry section) =="
echo "census: $CENSUS   today: $TODAY"
echo

echo "-- scratch 0: live lane registry as-is --"
cp "$LANE/corpus/SOURCES.md" "$SCH/corpus/SOURCES.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE 'E11' "
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -cE 'E11' | sed 's/^/E11 count: /'"
echo

echo "-- scratch 1: live registry + the PACKAGE's own staged S042 row --"
grep -E '^ {0,3}\| *S042 *\|' "$PKG/SOURCES.append.md" > "$SCH/staged-S042.md"
build "$SCH/corpus/SOURCES.md" "$SCH/staged-S042.md"
run "grep -nE '^ {0,3}\| *S04[12] *\\|' $SCH/corpus/SOURCES.md | cut -c1-90"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE 'E11'"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -E 'E01|E02|E03|E04|E05|E06|E07|E08|E09|E10|E12'"
echo "(empty = no schema violation for the staged S042 row)"
echo

echo "-- scratch 2: live registry + the PACKAGE's own staged S043 row (must NOT be a new id) --"
grep -E '^ {0,3}\| *S043 *\|' "$PKG/SOURCES.append.md" > "$SCH/staged-S043.md"
build "$SCH/corpus/SOURCES.md" "$SCH/staged-S043.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE 'E11'"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -E 'E01|E02|E03|E04|E05|E06|E07|E08|E09|E10|E12'"
