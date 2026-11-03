#!/usr/bin/env bash
# round-58 do-nothing receipts (run before the freeze). Each receipt is one unedited tee of one run set.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
BASE=1e5c8f2cdc1c9d14672444c6fca0e67414366494
S=/fast/scratch/hyaku/kasegi-r58/pre-frozen
D=$S/base
C=$L/.ufo/waves/round-58/controls
export TMPDIR=/fast/scratch/hyaku/kasegi-r58/tmp
mkdir -p "$TMPDIR"
hdr() { { echo "# $1"; echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname) base=$BASE"; echo; } > "$2"; }
run() { local r=$1; shift; { echo "## $1"; shift; echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit=$?]"; echo; } >> "$r"; }

R=$C/do-nothing-c1-r58.txt
hdr "round-58 C1 do-nothing control at the lane root (tree == base HEAD for every file the ledger reads)" "$R"
run "$R" "C1 ledger audit (frozen before: FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 - the base already green)" "cd $L && python3 corpus/instruments/figure-audit.py | tail -1"
run "$R" "C1 selftest at base (frozen before: selftest cases=5 failures=0 exit 0)" "cd $L && python3 corpus/instruments/figure-audit.py --selftest | tail -1"
run "$R" "C1 M57-8 red fixture at base (frozen before: derived=UNAVAILABLE reason=derive-exit-1 stale)" "cd $L && python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json | grep d53-1"
run "$R" "C1 ledger entry count at base (frozen before: 35)" "cd $L && grep -c '\"id\"' corpus/instruments/figure-audit-ledger.json"
run "$R" "C1 mutant battery at base (frozen before: script absent)" "cd $L && ls corpus/instruments/figure-audit-mutbat.py 2>&1; echo absent-check"

R=$C/do-nothing-c2-r58.txt
hdr "round-58 C2 do-nothing control (pure base export; zero F39, the round-57 state)" "$R"
run "$R" "C2 frontier census at base (frozen before: rows=38 admitted=38 closed=38 problem-rows=0 registry=90; entries=41 pass=41 exit=0)" "cd $D && python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F39|FRONTIER-FAIL F39|entries='; echo counter-pipe-exit=\${PIPESTATUS[0]}"
run "$R" "C2 F39 row count at base (frozen before: 0)" "cd $D && grep -cE '^\| F39 ' corpus/README.md"
run "$R" "C2 knowledge files at base (frozen before: 76)" "cd $D && ls corpus/knowledge/*.md | wc -l"
run "$R" "C2 expected entries at base (frozen before: 76)" "cd $D && grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt"
run "$R" "C2 capture binding at base (frozen before: records=73 bound=73 unbound=0)" "cd $D && python3 corpus/instruments/capture-binding-check.py | tail -1"
run "$R" "C2 lead line sha at base (frozen before: 631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547)" "cd $D && grep 'rate of autonomous AI cyber-capability progress' corpus/SOURCES.md | sha256sum"

R=$C/do-nothing-r67-probe-a2-r58.txt
hdr "round-58 R67 probe a2 replica on the base export (C2 counter limb; the round-57 stub admitted by the frozen counter, carried as a named open item)" "$R"
rm -rf "$S/probe-a2"; cp -a "$D" "$S/probe-a2"
K2="$S/probe-a2/corpus/knowledge/iso-29147-30111-standard-records.md"
{ head -n 7 "$K2"; printf '%s\n' '(stub body: round-58 probe a2 replica - the claims, distinctness notes and limits are removed; only S089 and S090 are named)'; } > "$K2.tmp" && mv "$K2.tmp" "$K2"
run "$R" "probe a2 entry size (stub: 8 lines, no body)" "cd $S/probe-a2 && wc -l corpus/knowledge/iso-29147-30111-standard-records.md"
run "$R" "probe a2 frontier counter (want if R67 closed: exit 1; observed: admitted)" "cd $S/probe-a2 && python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-PASS F38|entries='; echo counter-pipe-exit=\${PIPESTATUS[0]}"
echo WROTE
