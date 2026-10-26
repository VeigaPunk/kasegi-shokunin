#!/usr/bin/env bash
# run.sh — assert every G4' seat-identity fixture tree against its expected
# `G4 payload=... closed=` line. Run from any cwd; writes nothing.
#
#   run.sh
#
# Exit 0 iff every case matches its expected line and exit code, else 1.
set -u
here=$(cd -- "$(dirname -- "$0")" && pwd)
checker=$here/check-g4.sh
[ -f "$checker" ] || { printf 'missing=check-g4.sh\n'; exit 1; }

n=0
fail=0
for tsv in expected.tsv expected-controls.tsv; do
  [ -f "$here/$tsv" ] || { printf 'missing=%s\n' "$tsv"; exit 1; }
  while IFS=$'\t' read -r case tree want; do
    case $case in ''|'#'*) continue ;; esac
    n=$((n + 1))
    got=$(bash "$checker" "$here/$tree"); rc=$?
    exp_rc=1
    case $want in *' closed=1') exp_rc=0 ;; esac
    if [ "$got" = "$want" ] && [ "$rc" -eq "$exp_rc" ]; then
      printf 'case=%s rc=%s match=1 %s\n' "$case" "$rc" "$got"
    else
      printf 'case=%s rc=%s match=0 got=[%s] want=[%s]\n' "$case" "$rc" "$got" "$want"
      fail=$((fail + 1))
    fi
  done < "$here/$tsv"
done
if [ "$n" -gt 0 ] && [ "$fail" -eq 0 ]; then
  printf 'fixtures=%s failures=0\n' "$n"
  exit 0
fi
printf 'fixtures=%s failures=%s\n' "$n" "$fail"
exit 1
