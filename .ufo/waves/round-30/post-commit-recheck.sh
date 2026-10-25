#!/usr/bin/env bash
# Run from any cwd; intended for the lane's post-integration-commit tree.
set -u
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 2

failures=0
run_counter() {
  local label=$1; shift
  local output status
  output=$("$@" 2>&1)
  status=$?
  printf '%s\n' "$output"
  printf '%s_exit=%s\n' "$label" "$status"
  if (( status != 1 )); then
    # C1 controls are deliberately negative fixtures: exit 1 is the expected result.
    if [[ $label == a1 || $label == a2 || $label == b1 || $label == b2 ]]; then
      failures=$((failures + 1))
    fi
  fi
  if [[ $label == a1 ]] && ! grep -q 'F98' <<<"$output"; then failures=$((failures + 1)); fi
  if [[ $label == a2 ]] && ! grep -qi 'duplicate' <<<"$output"; then failures=$((failures + 1)); fi
  if [[ $label == b1 ]] && ! grep -q 'stem-mismatch' <<<"$output"; then failures=$((failures + 1)); fi
  if [[ $label == b2 ]] && ! grep -Eq 'occurrence-not-unique|occurrences=2' <<<"$output"; then failures=$((failures + 1)); fi
}

run_counter a1 python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1
run_counter a2 python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a2
run_counter b1 python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043
run_counter b2 python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045

frontier=$(awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md)
entries=$(grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l)
source_rows=$(grep -cE '^\|[[:space:]]*S04[6-7][[:space:]]*\|' corpus/SOURCES.md || true)
registry_rows=$(grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md || true)
printf 'frontier=%s\nentries_citing_s046_047=%s\nS046_S047_rows=%s\nregistry_rows=%s\n' "$frontier" "$entries" "$source_rows" "$registry_rows"
[[ $frontier == 14 && $entries == 1 && $source_rows == 2 && $registry_rows == 47 ]] || failures=$((failures + 1))

/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
census_status=$?
printf 'census_exit=%s\n' "$census_status"
(( census_status == 0 )) || failures=$((failures + 1))

harness_output=$(python3 corpus/instruments/frontier-recheck-count.py 2>&1)
harness_status=$?
printf '%s\n' "$harness_output"
printf 'harness_exit=%s\n' "$harness_status"
if (( harness_status != 0 )) || ! grep -q 'entries=17 pass=17 exit=0' <<<"$harness_output" || ! grep -q 'PASS F14 .*ids=S046,S047,S041' <<<"$harness_output"; then failures=$((failures + 1)); fi

recheck_status=0
for source in S046 S047 S041; do
  output=$(python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source "$source" 2>&1)
  status=$?
  printf '%s\n' "$output"
  if (( status != 0 )) || ! grep -q "$source:sha256 OK" <<<"$output"; then recheck_status=1; fi
done
printf 'recheck_exit=%s\n' "$recheck_status"
(( recheck_status == 0 )) || failures=$((failures + 1))
printf 'post_commit_recheck_exit=%s\n' "$failures"
exit "$failures"
