#!/usr/bin/env bash
# round-92 C1 pre-freeze controls: every variant is a commit in a shared scratch clone at
# BASE; the frozen predicate (frozen map unless the control names its own, map sha,
# labels rev, targets) runs on each.
# Usage: c1-controls-r92.sh LANE SCRATCH
set -u
L=$1; S=$2; W=$L/.ufo/waves/round-92
BASE=0628fd247914555838a42c02ba5d4ac08b7e095d
LABELS=d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d
MAPSHA=6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772
T=corpus/knowledge/triage-thresholds.md
mkdir -p "$S"; C=$S/c1clone; rm -rf "$C"
git clone -q --shared "$L" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "fixture toplevel mismatch"; exit 2; }
commit() { git -C "$C" -c user.name=fixture -c user.email=fixture@invalid commit -q --allow-empty -am "$1"; git -C "$C" rev-parse HEAD; }
variant() { # name, map-to-apply
  git -C "$C" checkout -q --detach $BASE
  [ -n "$2" ] && python3 -B $W/c1/apply-map.py --root "$C" --map "$2" >/dev/null
  commit "$1"
}
run() { # name, after-rev, map
  echo "== control $1 (after=$2 map=$(basename "$3"))"
  python3 -B $W/c1/knowledge-meter.py --lane "$C" --base-rev $BASE --after-rev "$2" --map "$3" \
    --labels-rev $LABELS --base-target 947/1947 --target 960/1944 --map-sha256 $MAPSHA --work "$S/w" | grep -E '^(LIMB|KNOWLEDGE-METER)'
}
M=$W/c1/repair-map.tsv
grep -v ':249	' $M > "$S/map-partial.tsv"
cp $M "$S/map-excluded437.tsv"; printf '%s:437\tintake-surface.md:75-76\t`intake-surface.md:75-76`\t`corpus/knowledge/intake-surface.md:89-90`\n' $T >> "$S/map-excluded437.tsv"
cp $M "$S/map-noedit.tsv"; printf 'corpus/knowledge/citation-bases.md:14\tclaim-gates.md:3\t`claim-gates.md:3`\t`corpus/knowledge/claim-gates.md:3`\n' >> "$S/map-noedit.tsv"
grep -v ':155	' $M > "$S/map-token155.tsv"; printf '%s:155\tmission-control.md:37-38\t`mission-control.md:37-38`\t`corpus/knowledge/mission-control.md:56-57`\n' $T >> "$S/map-token155.tsv"
grep -v ':58	' $M > "$S/map-dash58.tsv"; printf '%s:58\tmission-control.md:20-21\tMATCHES: `SKILL.md:117`, `mission-control.md:20-21`\t—\n' $T >> "$S/map-dash58.tsv"
sed 's#^\('$T':86\)\tintake-surface.md:71\t#\1\tintake-surface.md:83-88\t#' $M > "$S/map-wrongkey86.tsv"
grep -v ':59	' $M > "$S/map-skipqualify.tsv"
run candidate "$(variant candidate $M)" $M
run no-work "$(variant no-work '')" $M
run partial-24-of-25 "$(variant partial "$S/map-partial.tsv")" $M
run partial-own-map "$(git -C "$C" rev-parse HEAD)" "$S/map-partial.tsv"
run skip-qualify-59-own-map "$(variant skipq "$S/map-skipqualify.tsv")" "$S/map-skipqualify.tsv"
run excluded-437-applied "$(variant excl "$S/map-excluded437.tsv")" "$S/map-excluded437.tsv"
run no-edit-qualified "$(variant noedit "$S/map-noedit.tsv")" "$S/map-noedit.tsv"
run named-cell-155-token-only "$(variant tok155 "$S/map-token155.tsv")" "$S/map-token155.tsv"
run drop-token-58-as-dash-cell "$(variant dash58 "$S/map-dash58.tsv")" "$S/map-dash58.tsv"
run wrong-key-column-86 "$(variant wk86 "$S/map-wrongkey86.tsv")" "$S/map-wrongkey86.tsv"
# working-tree-only: candidate applied but not committed; the pinned meter reads the commit
git -C "$C" checkout -q --detach $BASE; python3 -B $W/c1/apply-map.py --root "$C" --map $M >/dev/null
run working-tree-only "$(git -C "$C" rev-parse HEAD)" $M
git -C "$C" checkout -q -- .
rm -rf "$C" "$S/w"
