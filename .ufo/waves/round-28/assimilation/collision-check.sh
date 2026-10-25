#!/usr/bin/env bash
# collision-check.sh — round-28 wave-1 §id-collision guard.
# Read-only on the lane registry and on the read-only staged package.
# Writes ONLY under .ufo/waves/round-28/assimilation/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
PKG=/home/vgpnk/Projects/shokuknow/merge/kasegi
A=$LANE/.ufo/waves/round-28/assimilation
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

cd "$LANE" || exit 1

echo "== round-28 wave-1 id-collision check =="
echo "lane root: $LANE"
echo "staged package (read-only): $PKG/SOURCES.append.md"
echo "pattern: $PAT"
echo

echo "-- 1. lane registry ids --"
run "grep -oE '$PAT' $LANE/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids"
run "printf 'reg-ids lines='; wc -l < $A/reg-ids; tr '\n' ' ' < $A/reg-ids; echo"

echo "-- 2. staged ids --"
run "grep -oE '$PAT' $PKG/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $A/staged-ids"
run "printf 'staged-ids lines='; wc -l < $A/staged-ids; tr '\n' ' ' < $A/staged-ids; echo"

echo "-- 3. collisions (comm -12) --"
run "comm -12 $A/reg-ids $A/staged-ids > $A/collisions"
run "printf 'collisions lines='; wc -l < $A/collisions"
run "cat $A/collisions"

echo "-- 4. indented-row latent-risk check on the real inputs --"
run "grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' $LANE/corpus/SOURCES.md"
run "grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}' $PKG/SOURCES.append.md"
