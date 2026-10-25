#!/usr/bin/env bash
# row-grammar-test.sh — round-28 wave-1 (isolated): measure each candidate staged row's OWN
# conformance against the fleet census grammar, with the row tested ALONE (no live duplicates).
#
#   A: live registry MINUS the live S042 row, PLUS the package's staged S042 row
#   B: live registry MINUS the live S041 row, PLUS the package's staged S043 row
#      (staged S043 is the SAME document as lane S041, so this measures what a naive
#       "append the staged row under its own id" adoption would do to the registry)
#   C: live registry PLUS one staged row with a PROSE recheck cell (S081) — measures whether
#      the census E09 rule fires on the package's prose recheck cells
#
# Writes ONLY under .ufo/waves/round-28/assimilation/schema4/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
A=$LANE/.ufo/waves/round-28/assimilation
SCH=$A/schema4
TODAY=2026-10-25

rm -rf "$SCH"; mkdir -p "$SCH/corpus"
ln -s "$LANE/corpus/knowledge" "$SCH/corpus/knowledge"

run() { printf '$ %s\n' "$*"; bash -c "$*"; rc=$?; printf '[exit %s]\n\n' "$rc"; }

# <out> <drop_id> <add_rowfile>
build() {
  python3 - "$LANE/corpus/SOURCES.md" "$2" "$3" "$1" <<'PY'
import sys
src, drop, rowfile, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
row = open(rowfile, encoding='utf-8').read().rstrip('\n')
lines = open(src, encoding='utf-8').read().split('\n')
def isrow(l):
    p = l.lstrip(' ')
    return len(l) - len(p) <= 3 and p.startswith('|') and p[1:].strip().startswith(drop + ' ')
lines = [l for l in lines if not isrow(l)]
idx = next(i for i, l in enumerate(lines) if l.lstrip(' ').startswith('## Paths'))
lines.insert(idx, row)
open(out, 'w', encoding='utf-8').write('\n'.join(lines))
print(f"dropped live {drop}; inserted staged row before line {idx+1}")
PY
}

echo "== round-28 wave-1 isolated row-grammar test =="
echo "census: $CENSUS   today: $TODAY"
echo

echo "-- A: staged S042 alone (live S042 removed) --"
grep -E '^ {0,3}\| *S042 *\|' "$PKG/SOURCES.append.md" > "$SCH/row-S042.md"
build "$SCH/corpus/SOURCES.md" S042 "$SCH/row-S042.md"
run "grep -cE '^ {0,3}\| *S042 *\|' $SCH/corpus/SOURCES.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE '	E11	'"
echo

echo "-- B: staged S043 alone (live S041 removed) --"
grep -E '^ {0,3}\| *S043 *\|' "$PKG/SOURCES.append.md" > "$SCH/row-S043.md"
build "$SCH/corpus/SOURCES.md" S041 "$SCH/row-S043.md"
run "grep -cE '^ {0,3}\| *S04[13] *\|' $SCH/corpus/SOURCES.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -vE '	E11	'"
echo

echo "-- C: a staged row with a PROSE recheck cell (S081) --"
grep -E '^ {0,3}\| *S081 *\|' "$PKG/SOURCES.append.md" > "$SCH/row-S081.md"
build "$SCH/corpus/SOURCES.md" NONE "$SCH/row-S081.md"
run "$CENSUS validate --file $SCH/corpus/SOURCES.md --today $TODAY | grep -E 'S081|E09'"
echo "(E09 on S081 = the package's prose recheck cells violate the census grammar; the two"
echo " adopted rows S042/S043 both carry a bare '180d' and are unaffected)"
