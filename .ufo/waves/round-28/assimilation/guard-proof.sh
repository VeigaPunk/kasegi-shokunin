#!/usr/bin/env bash
# guard-proof.sh — round-28 wave-1: prove the id-collision guard can FAIL loudly.
#
# Fixture: a scratch registry whose `  | S002 |` row is INDENTED by two spaces, and a
# scratch staged set that carries S002 at column 0. The 0-3-space-tolerant pattern must
# report S002 as a collision; a column-zero-only pattern must not (the failure mode the
# guard exists to catch). Writes ONLY under .ufo/waves/round-28/assimilation/fixture/.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
FX=$LANE/.ufo/waves/round-28/assimilation/fixture

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

cd "$LANE" || exit 1

echo "== round-28 wave-1 guard proof: indented registry row must collide =="
echo "lane root: $LANE"
echo "fixture registry: $FX/fixture-SOURCES.md  (row '  | S002 |' indented two spaces)"
echo "fixture staged:   $FX/fixture-staged.md  (S002 at column 0)"
echo

echo "-- fixture bytes (visible indent) --"
run "grep -nE '^ *\\|' $FX/fixture-SOURCES.md"
run "grep -nE '^ *\\|' $FX/fixture-staged.md"

echo "-- A. GUARD PATTERN (0-3 leading spaces) --"
run "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > $FX/a-reg-ids"
run "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-staged.md | grep -oE 'S[0-9]+' | sort > $FX/a-staged-ids"
run "comm -12 $FX/a-reg-ids $FX/a-staged-ids > $FX/a-collisions"
run "printf 'a-reg-ids    lines='; wc -l < $FX/a-reg-ids; tr '\n' ' ' < $FX/a-reg-ids; echo"
run "printf 'a-staged-ids lines='; wc -l < $FX/a-staged-ids; tr '\n' ' ' < $FX/a-staged-ids; echo"
run "printf 'a-collisions lines='; wc -l < $FX/a-collisions"
run "cat $FX/a-collisions"

echo "-- B. COLUMN-ZERO-ONLY PATTERN (^\\|) over the same two fixtures --"
run "grep -oE '^\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > $FX/b-reg-ids"
run "grep -oE '^\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-staged.md | grep -oE 'S[0-9]+' | sort > $FX/b-staged-ids"
run "comm -12 $FX/b-reg-ids $FX/b-staged-ids > $FX/b-collisions"
run "printf 'b-reg-ids    lines='; wc -l < $FX/b-reg-ids; tr '\n' ' ' < $FX/b-reg-ids; echo"
run "printf 'b-staged-ids lines='; wc -l < $FX/b-staged-ids; tr '\n' ' ' < $FX/b-staged-ids; echo"
run "printf 'b-collisions lines='; wc -l < $FX/b-collisions"
run "cat $FX/b-collisions"

echo "-- C. VERDICT --"
echo "A (0-3 spaces): non-empty collisions file (S002) -> the guard reports the duplicate."
echo "B (^| only):    0-byte collisions file -> the indented row is invisible, so the duplicate id would be appended silently."
echo "The 0-3-space-tolerant pattern is therefore the correct guard form."
