#!/usr/bin/env bash
# LabExportClean — replay of the round-40 H6 isolation probe (read-only on the lane).
# Builds a fixture clone Y' = J + all-gates.txt under its own scratch dir, then runs
# r40-closure.sh with dirty/clean --scratch-root and clean/pre-populated --work.
# Usage: bash LabExportClean.isolation-replay.sh [SCRATCH_DIR]   (SCRATCH_DIR removed on exit)
set -uo pipefail
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=${1:-/fast/scratch/hyaku/kasegi-r40/LabExportClean-replay}
case $S in /fast/scratch/hyaku/kasegi-r40/*|/tmp/*) ;; *) echo "refusing scratch $S" >&2; exit 2 ;; esac
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S" && cd "$S" && export TMPDIR=$S
git clone -q --no-hardlinks "$L" "$S/lane" || exit 2
[ "$(git -C "$S/lane" rev-parse --show-toplevel)" = "$S/lane" ] || exit 2
J=$(git -C "$S/lane" rev-parse HEAD)
mkdir -p "$S/lane/.ufo/waves/round-40/final-gates"
cp "$L/.ufo/waves/round-40/final-gates/all-gates.txt" "$S/lane/.ufo/waves/round-40/final-gates/"
git -C "$S/lane" add .ufo/waves/round-40/final-gates/all-gates.txt
git -C "$S/lane" -c user.name=fx -c user.email=fx@local commit -q -m "fixture Y'"
Y=$(git -C "$S/lane" rev-parse HEAD)
echo "J=$J Y'=$Y"
R=$S/lane/corpus/instruments/r40-closure.sh
mk() { mkdir -p "$S/sbx/$1/root/kasegi-r41-ignored" "$S/sbx/$1/root/gates-work" "$S/sbx/$1/work"; }
for n in A B C D F H I; do mk $n; done
mkdir -p "$S/sbx/B/root/kasegi-r40-stray" "$S/sbx/D/root/kasegi-r40-stray"
for n in C D; do w=$S/sbx/$n/work
  mkdir -p "$w/export/corpus/instruments" "$w/mut" "$w/neg-base" "$w/neg-r39" "$w/h5"
  echo forged > "$w/export/corpus/instruments/r40-closure.sh"; echo junk > "$w/export/SCORECARD.md"
  printf 'H1\tsuite=1\t1\n' > "$w/payloads.tsv"; echo forged > "$w/h5-source.txt"; echo forged > "$w/h7-source.txt"
done
rm -rf "$S/sbx/F/work"; mkdir -p "$S/sbx/F/root/kasegi-r40-seat/work" "$S/sbx/F/root/kasegi-r40-seat/other-seat"
echo leftover > "$S/sbx/F/root/kasegi-r40-seat/other-seat/leftover.txt"
mkdir -p "$S/sbx/H/root/.kasegi-r40-seat"; echo x > "$S/sbx/H/root/.kasegi-r40-seat/f"
echo x > "$S/sbx/I/root/kasegi-r40-file"
run() { # NAME WORK [extra args]
  local n=$1 w=$2; shift 2
  echo "== $n"; bash "$R" "$@" --export-ref "$Y" --lane "$S/lane" --work "$w" --scratch-root "$S/sbx/$n/root" > "$S/$n.out" 2> "$S/$n.err"
  echo "rc=$? $(grep -E '^H6' "$S/$n.out") $(grep -E '^closed=|^selftest cases=' "$S/$n.out")"
}
run A "$S/sbx/A/work"; run B "$S/sbx/B/work"; run C "$S/sbx/C/work"; run D "$S/sbx/D/work"
run F "$S/sbx/F/root/kasegi-r40-seat/work"; run H "$S/sbx/H/work"; run I "$S/sbx/I/work"
cmp "$S/A.out" "$S/C.out" && echo "A==C stdout byte-identical (pre-populated work does not leak)"
run B "$S/sbx/B/work" --selftest
grep -E 'selftest case=H(5|6|7) ' "$S/B.out"
