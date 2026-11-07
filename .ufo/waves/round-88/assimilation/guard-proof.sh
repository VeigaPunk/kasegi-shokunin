#!/usr/bin/env bash
# guard-proof.sh — reproducible transcript for the §10 id-collision guard.
set -u

FX=$(mktemp -d /fast/scratch/hyaku/kasegi-r88/l1/fx.XXXXXX)
trap 'rm -rf "$FX"' EXIT

cat > "$FX/fixture-SOURCES.md" << 'FIXTURE'
| id | source |
|---|---|
| S001 | Alpha |
  | S002 | Beta |
FIXTURE

cat > "$FX/fixture-staged.md" << 'FIXTURE'
| id | source |
|---|---|
| S002 | Beta staged |
| S003 | Gamma staged |
FIXTURE

echo "== §10 id-collision guard: failure-mode proof =="
echo "fixture registry: $FX/fixture-SOURCES.md (row S002 is INDENTED by two spaces)"
echo "fixture staged:   $FX/fixture-staged.md (carries S002 at column 0)"
echo

echo "-- A. GUARD PATTERN (0-3 leading spaces: '^ {0,3}\|[[:space:]]*S[0-9]{3,}') --"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$FX/fixture-SOURCES.md" | grep -oE 'S[0-9]+' | sort > "$FX/a-reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$FX/fixture-staged.md" | grep -oE 'S[0-9]+' | sort > "$FX/a-staged-ids"
comm -12 "$FX/a-reg-ids" "$FX/a-staged-ids" > "$FX/a-collisions"

printf 'a-reg-ids:    '; tr '\n' ' ' < "$FX/a-reg-ids"; echo
printf 'a-staged-ids: '; tr '\n' ' ' < "$FX/a-staged-ids"; echo
printf 'a-collisions lines=%d\n' "$(wc -l < "$FX/a-collisions")"
cat "$FX/a-collisions"
echo

echo "-- B. COLUMN-ZERO-ONLY PATTERN ('^\|[[:space:]]*S[0-9]{3,}') over identical fixtures --"
grep -oE '^\|[[:space:]]*S[0-9]{3,}' "$FX/fixture-SOURCES.md" | grep -oE 'S[0-9]+' | sort > "$FX/b-reg-ids"
grep -oE '^\|[[:space:]]*S[0-9]{3,}' "$FX/fixture-staged.md" | grep -oE 'S[0-9]+' | sort > "$FX/b-staged-ids"
comm -12 "$FX/b-reg-ids" "$FX/b-staged-ids" > "$FX/b-collisions"

printf 'b-reg-ids:    '; tr '\n' ' ' < "$FX/b-reg-ids"; echo
printf 'b-staged-ids: '; tr '\n' ' ' < "$FX/b-staged-ids"; echo
printf 'b-collisions lines=%d\n' "$(wc -l < "$FX/b-collisions")"
cat "$FX/b-collisions"
echo

echo "-- C. VERDICT --"
if [[ $(wc -l < "$FX/a-collisions") -gt 0 && $(wc -l < "$FX/b-collisions") -eq 0 ]]; then
  echo "PASS: Guard pattern detected collision (S002); column-zero-only pattern missed it (0 collisions)."
else
  echo "FAIL: Unexpected outcome"
  exit 1
fi
