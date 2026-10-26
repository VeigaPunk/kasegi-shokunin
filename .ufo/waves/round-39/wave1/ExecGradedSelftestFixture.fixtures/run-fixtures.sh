#!/usr/bin/env bash
# run-fixtures.sh — run judge-g2-cases.sh over every fixture receipt in this
# directory and compare the judge's single output line and exit code against
# expected.tsv.  Usage: ./run-fixtures.sh   (no arguments, no writes)
set -u

dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 2
pass=0
fail=0
n=0

while IFS=$'\t' read -r fixture want want_rc; do
  case "$fixture" in ''|'#'*) continue ;; esac
  n=$((n + 1))
  got=$(bash "$dir/judge-g2-cases.sh" "$dir/$fixture")
  got_rc=$?
  if [ "$got" = "$want" ] && [ "$got_rc" -eq "$want_rc" ]; then
    pass=$((pass + 1))
    verdict=pass
  else
    fail=$((fail + 1))
    verdict=fail
  fi
  printf 'fixture=%s expected-rc=%s observed-rc=%s verdict=%s\n' \
    "$fixture" "$want_rc" "$got_rc" "$verdict"
  if [ "$verdict" = fail ]; then
    printf '  want=%s\n  got =%s\n' "$want" "$got"
  fi
done < "$dir/expected.tsv"

printf 'fixtures=%s pass=%s failures=%s\n' "$n" "$pass" "$fail"
[ "$fail" -eq 0 ] && [ "$n" -gt 0 ]
