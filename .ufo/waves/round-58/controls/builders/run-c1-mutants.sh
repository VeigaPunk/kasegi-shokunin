#!/usr/bin/env bash
# round-58 C1 do-nothing receipt: figure-audit selftest mutants m4 (drop a case) and m6 (read-only gate off),
# built by exact-once sed over the BASE instrument bytes in the base export. One run set, unedited tee.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=/fast/scratch/hyaku/kasegi-r58/pre-frozen
D=$S/base
R=$L/.ufo/waves/round-58/controls/do-nothing-c1-mutants-r58.txt
P=$D/corpus/instruments/figure-audit.py
M=$S/mut; rm -rf "$M"; mkdir -p "$M"
{
  echo "# round-58 C1 do-nothing mutant receipt (lane root at base 1e5c8f2; mutants built from the base instrument bytes); one run set, unedited tee"
  echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname)"
  echo
  echo "## site counts (exact-once requirement)"
  echo "\$ grep -c 'run_case(\"stale-literal\"' $P ; grep -c 'return head.startswith(READ_ONLY_HEADS)' $P"
  echo "$(grep -c 'run_case("stale-literal"' $P) $(grep -c 'return head.startswith(READ_ONLY_HEADS)' $P)"
  echo
} > "$R"
sed '/run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)/d' "$P" > "$M/m4-figure-audit.py"
sed 's/return head.startswith(READ_ONLY_HEADS)/return True/' "$P" > "$M/m6-figure-audit.py"
cp "$P" "$M/pristine-figure-audit.py"
cp "$D/.ufo/waves/round-54/controls/red-d53-ledger.json" "$M/" 2>/dev/null || true
cd "$L" || exit 9
for m in pristine m4 m6; do
  {
    echo "## mutant $m: selftest"
    echo "\$ python3 $M/$m-figure-audit.py --selftest | tail -1"
    python3 "$M/$m-figure-audit.py" --selftest 2>&1 | tail -1
    echo "[exit=${PIPESTATUS[0]}]"
    echo
  } >> "$R"
done
for m in pristine m4 m6; do
  {
    echo "## mutant $m: ledger audit over the 35-figure ledger at the lane root (tree == base HEAD 1e5c8f2; the pure export lacks .git and reads rev-pinned derives UNAVAILABLE)"
    echo "\$ python3 $M/$m-figure-audit.py --root $L --ledger $L/corpus/instruments/figure-audit-ledger.json | tail -1"
    python3 "$M/$m-figure-audit.py" --root "$L" --ledger "$L/corpus/instruments/figure-audit-ledger.json" 2>&1 | tail -1
    echo "[exit=${PIPESTATUS[0]}]"
    echo
  } >> "$R"
done
{
  echo "## M57-8 fixture on this host (lane root, base instrument)"
  echo "\$ python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json"
  python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json 2>&1
  echo "[exit=$?]"
} >> "$R"
echo WROTE "$R"
