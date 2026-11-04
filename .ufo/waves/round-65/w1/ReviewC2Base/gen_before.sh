#!/bin/bash
# Generate before.txt: every number comes from the literal command printed above it.
set -u
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
EXP=/fast/scratch/hyaku/kasegi-r65/ReviewC2Base/base
OUT=/fast/scratch/hyaku/kasegi-r65/ReviewC2Base/before.txt
: > "$OUT"

run() { # run "<label>" "<cmd>"
  printf '\n$ %s\n' "$2" >> "$OUT"
  ( cd "$LANE" && eval "$2" ) >> "$OUT" 2>&1
  printf '[exit=%d]\n' "$?" >> "$OUT"
}

run_exp() {
  printf '\n$ %s\n' "$2" >> "$OUT"
  ( cd "$EXP" && eval "$2" ) >> "$OUT" 2>&1
  printf '[exit=%d]\n' "$?" >> "$OUT"
}

b() { printf 'BEFORE %s %s\n' "$1" "$2" >> "$OUT"; }

{
  printf 'BEFORE-MEASUREMENT base commit a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b\n'
  printf 'BEFORE-MEASUREMENT lane %s (git HEAD == base, working tree clean except untracked wave dirs)\n' "$LANE"
  printf 'BEFORE-MEASUREMENT export %s is `git archive <base> | tar -x`\n' "$EXP"
  printf 'BEFORE-MEASUREMENT date %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'BEFORE-MEASUREMENT canonical cwd for every recheck: the lane root (recheck-audit strict limb (d) cdroot)\n'
} >> "$OUT"

echo "# ---- identity of the bytes measured" >> "$OUT"
run "instrument digests" "sha256sum corpus/instruments/frontier-recheck-count.py corpus/instruments/capture-binding-check.py corpus/instruments/recheck-audit.py corpus/instruments/knowledge-expected.txt; git rev-parse HEAD"

echo "# ---- counter 1: frontier census (lane root, canonical)" >> "$OUT"
run "frontier census" "python3 corpus/instruments/frontier-recheck-count.py"
echo "# ---- counter 1b: same counter on the scratch export (cross-check)" >> "$OUT"
run_exp "frontier census (export)" "python3 corpus/instruments/frontier-recheck-count.py"

echo "# ---- counter 2: capture binding (lane root, canonical)" >> "$OUT"
run "capture binding" "python3 corpus/instruments/capture-binding-check.py"

echo "# ---- counter 3: recheck audit (lane root, canonical)" >> "$OUT"
run "recheck audit" "python3 corpus/instruments/recheck-audit.py"

echo "# ---- counter 3b: recheck audit on the scratch export (NOT a base measurement: strict limb (d) cdroot fails)" >> "$OUT"
run_exp "recheck audit (export)" "python3 corpus/instruments/recheck-audit.py"

echo "# ---- entries/knowledge expected-list checks (lane root)" >> "$OUT"
run "expected list lines" "wc -l corpus/instruments/knowledge-expected.txt"
run "expected list sorted" "LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt; echo sort_c_exit=\$?"
run "expected list composition" "grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt; grep -vc '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt"
run "knowledge entries" "ls corpus/knowledge/*.md | wc -l"

echo "# ---- registry and frontier row counts (lane root)" >> "$OUT"
run "registry rows" "grep -c '^| S[0-9]' corpus/SOURCES.md"
run "frontier rows regex" "grep -c '^| F[0-9]' corpus/README.md"
run "frontier rows regex strict" "grep -cE '^\| F[0-9]+ \|' corpus/README.md"
run "frontier rows that are not census rows" "grep -n '^| F[0-9]' corpus/README.md | grep -v '| admitted |' | cut -c1-90"
run "census row count from counter output" "python3 corpus/instruments/frontier-recheck-count.py | grep -oE 'rows=[0-9]+' "

{
  printf '\n# ---- BEGIN before values (each value is the literal output above)\n'
} >> "$OUT"

b base_commit a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b
b frontier_entries 46
b frontier_pass 46
b frontier_exit 0
b frontier_census_rows 43
b frontier_census_admitted 43
b frontier_census_closed 43
b frontier_census_problem_rows 0
b frontier_census_registry 97
b capture_records 78
b capture_bound 78
b capture_unbound 0
b capture_with_url 78
b capture_with_fetched_utc 40
b capture_with_archival 38
b capture_snapshot_dirs 38
b capture_manifest_dirs 38
b capture_missing_manifest 0
b capture_multi_row_url 7
b capture_digest_unpinned 0
b capture_orphans 1
b capture_orphan_name S040-live.txt
b capture_exit 0
b recheck_lines 81
b recheck_total_knowledge 81
b recheck_strict_pass 72
b recheck_cdroot_fail 0
b recheck_instrument_fail 0
b recheck_own_fail 0
b recheck_executes 59
b recheck_gated 22
b recheck_broken 0
b recheck_parse_fail 0
b recheck_cwd_fail 9
b recheck_paths_fail 0
b recheck_expect_present 1
b recheck_expected 81
b recheck_missing 0
b recheck_unexpected 0
b recheck_exit 1
b knowledge_expected_lines 83
b knowledge_expected_comment_lines 2
b knowledge_expected_path_lines 81
b knowledge_expected_sort_c_exit 0
b knowledge_md_files 81
b registry_rows 97
b readme_F_rows_grep 45
b readme_F_rows_grepE 45
b readme_census_rows 43
b readme_F_rows_non_census 2
b export_frontier_entries 46
b export_recheck_strict_pass 1
b export_recheck_cdroot_fail 71

printf '\n# ---- END before values\n' >> "$OUT"
wc -l "$OUT"
