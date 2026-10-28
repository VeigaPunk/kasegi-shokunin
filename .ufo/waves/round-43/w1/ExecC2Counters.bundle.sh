#!/usr/bin/env bash
# ExecC2Counters.bundle.sh — kasegi round 43, C2 (coverage) counting commands.
#
# Ten read-only counts over a lane root, one line each:
#   <n>. <command> -> <value>
# Run from anywhere: LANE=<lane-root> bash ExecC2Counters.bundle.sh
# Without LANE the script resolves the repository that contains it.
# $TMPDIR is honoured and passed to every child; the script itself creates no
# files and writes nothing under the lane.
set -uo pipefail

LANE=${LANE:-}
if [ -z "$LANE" ]; then
  LANE=$(git -C "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" rev-parse --show-toplevel 2>/dev/null) || LANE=
fi
if [ -z "$LANE" ] || [ ! -f "$LANE/corpus/SOURCES.md" ]; then
  echo "bundle: lane root unresolved; set LANE=<lane-root>" >&2
  exit 2
fi
cd "$LANE" || exit 2
export TMPDIR=${TMPDIR:-/tmp}

line() { printf '%s. %s -> %s\n' "$1" "$2" "$3"; }

# 1. frontier rows: the `| F<n> |` rows of corpus/README.md the frontier census enumerates.
cmd="grep -cE '^\|[[:space:]]*F[0-9]+[[:space:]]*\|' corpus/README.md"
v=$(grep -cE '^\|[[:space:]]*F[0-9]+[[:space:]]*\|' corpus/README.md)
line 1 "$cmd" "$v"

# 2. registry rows: the `| S<n> |` rows of corpus/SOURCES.md.
cmd="grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md"
v=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)
line 2 "$cmd" "$v"

# 3. S067 status probe: registry rows at or above S067, and the S067 row's status cell.
PROBE_S067='$2 ~ /^ *S[0-9]+ *$/ {id=$2; gsub(/[^0-9]/,"",id); if (id+0>=67) n++; if (id+0==67) {s=$9; gsub(/^ +| +$/,"",s); found=1}} END {printf "rows>=S067=%d status=%s\n", n+0, (found ? s : "absent")}'
cmd="awk -F'|' '$PROBE_S067' corpus/SOURCES.md"
v=$(awk -F'|' "$PROBE_S067" corpus/SOURCES.md)
line 3 "$cmd" "$v"

# 4. knowledge entries citing S067 in their `source:` header.
cmd="grep -rlE '^source: S067' corpus/knowledge | wc -l"
v=$(grep -rlE '^source: S067' corpus/knowledge | wc -l)
line 4 "$cmd" "$v"

# 5. knowledge file count.
cmd="ls corpus/knowledge/*.md | wc -l"
v=$(ls corpus/knowledge/*.md | wc -l)
line 5 "$cmd" "$v"

# 6. capture binding: the `records=` line of capture-binding-check.py.
cmd="python3 corpus/instruments/capture-binding-check.py"
out=$(python3 corpus/instruments/capture-binding-check.py 2>&1); rc=$?
v=$(printf '%s\n' "$out" | grep -E '^records=' | tail -1)
line 6 "$cmd" "${v:-no-records-line} exit=$rc"

# 7. recheck audit: the expected-entry count and its exit.
cmd="python3 corpus/instruments/recheck-audit.py --quiet"
out=$(python3 corpus/instruments/recheck-audit.py --quiet 2>&1); rc=$?
v=$(printf '%s\n' "$out" | awk '{for (i=1;i<=NF;i++) if ($i ~ /^expected=[0-9]+$/) {print $i; exit}}')
line 7 "$cmd" "${v:-no-expected-line} exit=$rc"

# 8. frontier harness: its `entries=` summary line.
cmd="python3 corpus/instruments/frontier-recheck-count.py"
out=$(python3 corpus/instruments/frontier-recheck-count.py 2>&1); rc=$?
v=$(printf '%s\n' "$out" | grep -E '^entries=' | tail -1)
line 8 "$cmd" "${v:-no-entries-line} shell-exit=$rc"

# 9. census: the validator exit for the kasegi lane.
cmd="bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi"
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi >/dev/null 2>&1; rc=$?
line 9 "$cmd" "exit=$rc"

# 10. claim-package defect fixtures present on disk.
cmd="ls corpus/instruments/fixtures/claim-package/ | grep -c '^defect-'"
v=$(ls corpus/instruments/fixtures/claim-package/ 2>/dev/null | grep -c '^defect-')
if [ ! -d corpus/instruments/fixtures/claim-package ]; then
  v="$v dir=absent"
fi
line 10 "$cmd" "$v"
