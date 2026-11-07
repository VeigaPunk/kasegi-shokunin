#!/usr/bin/env bash
# round-91 C1 pre-freeze controls: every variant is a commit in a shared scratch clone at
# BASE; the frozen predicate (frozen map, map sha, labels rev, targets) runs on each.
# Usage: c1-controls-r91.sh LANE SCRATCH
set -u
L=$1; S=$2; W=$L/.ufo/waves/round-91
BASE=bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1
LABELS=e993fd181e320f1f21e06b05e16c68b0f07cff76
MAPSHA=55d50b661bcf79ad5a435c7d7bc86e3954e9910f7dabc480236224170c8c0a7a
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
    --labels-rev $LABELS --base-target 890/1883 --target 891/1880 --map-sha256 $MAPSHA --work "$S/w" | grep -E '^(LIMB|KNOWLEDGE-METER)'
}
M=$W/c1/repair-map.tsv
grep -v ':457' $M > "$S/map-partial.tsv"
cp $M "$S/map-superset.tsv"; printf 'corpus/knowledge/triage-thresholds.md:56\t| — |\t| MATCHES: `claim-gates.md:29-36` |\n' >> "$S/map-superset.tsv"
sed 's#`corpus/knowledge/ev-model.md:13-25`#`corpus/knowledge/ev-model.md:6-20`#' $M > "$S/map-wrongrange.tsv"
sed 's#^\(corpus/knowledge/triage-thresholds.md:457\)\t.*#\1\tMATCHES for gate-enforced rows\t—#' $M > "$S/map-dash457.tsv"
run candidate "$(variant candidate $M)" $M
run no-work "$(variant no-work '')" $M
run partial-5-of-6 "$(variant partial "$S/map-partial.tsv")" $M
run partial-own-map "$(git -C "$C" rev-parse HEAD)" "$S/map-partial.tsv"
run superset-unlabelled-edit "$(variant superset "$S/map-superset.tsv")" $M
run wrong-range-454 "$(variant wrongrange "$S/map-wrongrange.tsv")" "$S/map-wrongrange.tsv"
run label-ignored-457 "$(variant dash457 "$S/map-dash457.tsv")" "$S/map-dash457.tsv"
# working-tree-only: candidate applied but not committed; the pinned meter reads the commit
git -C "$C" checkout -q --detach $BASE; python3 -B $W/c1/apply-map.py --root "$C" --map $M >/dev/null
run working-tree-only "$(git -C "$C" rev-parse HEAD)" $M
git -C "$C" checkout -q -- .
rm -rf "$C" "$S/w"
