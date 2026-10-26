#!/usr/bin/env bash
# collide.sh <registry-md> <staged-md> <pattern-kind: wide|col0>
set -u
reg=$1; staged=$2; kind=${3:-wide}
if [ "$kind" = col0 ]; then pat='^\|[[:space:]]*S[0-9]{3,}'; else pat='^ {0,3}\|[[:space:]]*S[0-9]{3,}'; fi
t=$(mktemp -d) || exit 9
grep -oE "$pat" "$reg"    | grep -oE 'S[0-9]+' | sort > "$t/reg"    || true
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$staged" | grep -oE 'S[0-9]+' | sort > "$t/staged" || true
comm -12 "$t/reg" "$t/staged" > "$t/coll"
printf 'kind=%s reg_ids=%s staged_ids=%s collisions=%s ids=%s\n' \
  "$kind" "$(wc -l < "$t/reg")" "$(wc -l < "$t/staged")" "$(wc -l < "$t/coll")" "$(tr '\n' ' ' < "$t/coll" | sed 's/ $//')"
rc=0; [ -s "$t/coll" ] || rc=0
[ "$(wc -l < "$t/reg")" -ge 1 ] || rc=2
rm -rf "$t"; exit $rc
