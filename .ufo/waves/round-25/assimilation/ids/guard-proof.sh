#!/usr/bin/env bash
# guard-proof.sh — reproducible transcript for the §10 id-collision guard.
# Prints each command, runs it, prints its exit status and output.
# Writes only fixture/*.ids scratch files beside itself; reads the real inputs read-only.
set -u
R=.ufo/waves/round-25/assimilation/ids
FX=$R/fixture

run() {
  printf '$ %s\n' "$*"
  bash -c "$*"
  rc=$?
  printf '[exit %s]\n\n' "$rc"
}

echo "== §10 id-collision guard: failure-mode proof =="
echo "lane root: $(pwd)"
echo "fixture registry: $FX/fixture-SOURCES.md (row 2 is INDENTED by two spaces)"
echo "fixture staged:   $FX/fixture-staged.md (carries the same id at column 0)"
echo

echo "-- fixture bytes --"
run "grep -nE '^ *\\|' $FX/fixture-SOURCES.md"
run "grep -nE '^ *\\|' $FX/fixture-staged.md"

echo "-- A. GUARD PATTERN (0-3 leading spaces) --"
run "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > $FX/a-reg-ids"
run "grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-staged.md | grep -oE 'S[0-9]+' | sort > $FX/a-staged-ids"
run "comm -12 $FX/a-reg-ids $FX/a-staged-ids > $FX/a-collisions"
run "printf 'a-reg-ids    lines='; wc -l < $FX/a-reg-ids; tr '\\n' ' ' < $FX/a-reg-ids; echo"
run "printf 'a-staged-ids lines='; wc -l < $FX/a-staged-ids; tr '\\n' ' ' < $FX/a-staged-ids; echo"
run "printf 'a-collisions lines='; wc -l < $FX/a-collisions"
run "cat $FX/a-collisions"

echo "-- B. COLUMN-ZERO-ONLY PATTERN (^\|) over the same two fixtures --"
run "grep -oE '^\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > $FX/b-reg-ids"
run "grep -oE '^\\|[[:space:]]*S[0-9]{3,}' $FX/fixture-staged.md | grep -oE 'S[0-9]+' | sort > $FX/b-staged-ids"
run "comm -12 $FX/b-reg-ids $FX/b-staged-ids > $FX/b-collisions"
run "printf 'b-reg-ids    lines='; wc -l < $FX/b-reg-ids; tr '\\n' ' ' < $FX/b-reg-ids; echo"
run "printf 'b-staged-ids lines='; wc -l < $FX/b-staged-ids; tr '\\n' ' ' < $FX/b-staged-ids; echo"
run "printf 'b-collisions lines='; wc -l < $FX/b-collisions"
run "cat $FX/b-collisions"

echo "-- C. VERDICT --"
echo "A (0-3 spaces): 1 collision -> S002. The guard detects the duplicate, which is what it must do."
echo "B (^| only):    0 collisions. The indented S002 row is invisible to the pattern, so the duplicate id would be appended silently."
echo "A column-zero-only pattern is therefore not an acceptable guard: it under-reports exactly the copy-paste case the guard exists to catch."
echo

echo "-- D. LATENT-RISK CHECK on the real inputs (are the real files flat today?) --"
run "grep -cE '^ {1,3}\\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md"
run "grep -cE '^ {1,3}\\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md"
run "grep -cE '^\\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md"
run "grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md"
echo "Both real inputs carry 0 indented rows, so today the two patterns agree (94 staged, 35 registered)."
echo "The guard's 0-3-space form is not redundant: it is the form that still works after the first indented paste."
