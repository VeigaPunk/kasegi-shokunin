#!/usr/bin/env bash
# round-58 after-state counting run set. $1 = root to measure; $2 = receipt path; $3 = label.
# One run set, unedited tee: every command's output and exit code are appended as printed.
set -u
ROOT=$1; OUT=$2; LABEL=$3
cd "$ROOT" || exit 9
{
  echo "# round-58 after-state counting run set - $LABEL"
  echo "run-utc=$(date -u +%Y-%m-%dT%H:%M:%SZ) host=$(hostname) root=$ROOT"
  echo
} > "$OUT"
run() { local d=$1; shift; { echo "## $d"; echo "\$ $*"; "$@" 2>&1; echo "[exit=$?]"; echo; } >> "$OUT"; }
runsh() { local d=$1; shift; { echo "## $d"; echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit=$?]"; echo; } >> "$OUT"; }
run "C1 selftest (want: selftest cases=6 failures=0, exit 0)" python3 corpus/instruments/figure-audit.py --selftest
run "C1 mutant battery (want: mutbat killed=2/2 survivors=0 controls=pass, exit 0)" python3 corpus/instruments/figure-audit-mutbat.py
run "C1 red fixture d53 (want: derived=33 not UNAVAILABLE, stale, exit 1)" python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json
run "C1 ledger audit (want: FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0)" python3 corpus/instruments/figure-audit.py
runsh "C1 ledger entry count (want: 35)" "grep -c '\"id\"' corpus/instruments/figure-audit-ledger.json"
run "C2 frontier census (want: rows=39 admitted=39 closed=39 problem-rows=0 registry=91; FRONTIER-PASS F39 ids=S091; entries=42 pass=42 exit=0)" bash -c "python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F39|FRONTIER-FAIL|entries='; echo counter-pipe-exit=\${PIPESTATUS[0]}"
run "C2 source-recheck S091 (want: sha256 OK + 9 Q OK occurrences=1, exit 0)" python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091
run "C2 capture binding (want: records=74 bound=74 unbound=0, exit 0)" python3 corpus/instruments/capture-binding-check.py
runsh "C2 knowledge files (want: 77)" "ls corpus/knowledge/*.md | wc -l"
runsh "C2 knowledge-expected entries (want: 77)" "grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt"
runsh "C2 expected list sort (want: exit 0)" "LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt && echo sort-ok"
runsh "C2 frontier F39 row count (want: 1)" "grep -cE '^\| F39 ' corpus/README.md"
runsh "C2 lead line sha (want: 631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547)" "grep 'rate of autonomous AI cyber-capability progress' corpus/SOURCES.md | sha256sum"
runsh "C2 registry rows (want: 91)" "grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md"
runsh "C2 census validate (want: exit 0)" "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md; echo validate-exit=\$?"
echo DONE >> "$OUT"
