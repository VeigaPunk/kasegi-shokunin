#!/usr/bin/env bash
# kasegi round 58 - pre-freeze evidence run set A: neighbor screen (live tree) +
# do-nothing controls (pure base export 1e5c8f2). One run set per receipt, unedited tee.
set -u
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=/fast/scratch/hyaku/kasegi-r58/pre-frozen
BASE=1e5c8f2cdc1c9d14672444c6fca0e67414366494
C=$L/.ufo/waves/round-58/controls
mkdir -p "$S" "$C"
cd "$L" || exit 9

run() { # run <receipt> -- cmd...
  local r=$1; shift; shift
  { printf '$ %s\n' "$*"; "$@" 2>&1; printf '[exit=%s]\n\n' "$?"; } >> "$r"
}
receipt_init() {
  printf '# %s - one run set, unedited tee\nrun-utc=%s host=%s base=%s\n\n' \
    "$2" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(hostname)" "$BASE" > "$1"
}

########## A. neighbor screen (live tree) ##########
R=$C/neighbor-screen-r58.txt
receipt_init "$R" "round-58 extended pre-freeze neighbor screen (rev 1)"
{
  echo '## limb 1: held-row hits for the AISI surface across the front-door files'
} >> "$R"
run "$R" -- bash -c "grep -rn 'aisi.gov.uk' corpus/knowledge corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md | grep -v source-snapshots; true"
{
  echo '## limb 2: held-row hits for the capability-measurement tokens (file lists)'
} >> "$R"
run "$R" -- bash -c "grep -rlc 'AI Security Institute' corpus/knowledge/*.md corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md; echo '-- time horizon files:'; grep -rlc 'time horizon' corpus/knowledge/*.md corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md; echo '-- METR files:'; grep -rlc 'METR' corpus/knowledge/*.md corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md; echo '-- autonomous cyber files:'; grep -rlc 'autonomous cyber' corpus/knowledge/*.md corpus/README.md PROVINCE.md corpus/SOURCES.md SKILL.md; true"
{
  echo '## limb 3: the recorded lead line (bytes-unchanged check) at base'
} >> "$R"
run "$R" -- bash -c "grep -n \"rate of autonomous AI cyber-capability progress\" corpus/SOURCES.md; echo '-- loose string count:'; grep -c \"rate of autonomous AI cyber-capability progress\" corpus/SOURCES.md; echo '-- exact-line sha at base:'; git show $BASE:corpus/SOURCES.md | grep 'rate of autonomous AI cyber-capability progress' | sha256sum"
{
  echo '## limb 4: downstream-consumer sweep over corpus/source-snapshots/'
} >> "$R"
run "$R" -- bash -c "grep -rln 'aisi.gov.uk' corpus/source-snapshots/ | sort; echo '-- time-horizon token snapshots:'; grep -rln 'time horizon' corpus/source-snapshots/ | sort; echo '-- METR token snapshots:'; grep -rln 'METR' corpus/source-snapshots/ | sort; true"
{
  echo '## limb 5: sibling-province adjacency probe (read-only, fleet root)'
} >> "$R"
run "$R" -- bash -c "grep -in 'cyber\|capability\|benchmark' /home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md | head -10; true"

########## B. base export + do-nothing controls ##########
D=$S/base
rm -rf "$D"; mkdir -p "$D"
git -C "$L" archive $BASE | tar -x -C "$D"
R=$C/do-nothing-c1-r58.txt
receipt_init "$R" "round-58 C1 do-nothing control (pure base export; the before-state the claims are frozen against)"
{
  echo '## limb A (fold): the audit is green at base over the CURRENT ledger and the 8 new ids are absent'
} >> "$R"
run "$R" -- bash -c "cd $D && python corpus/instruments/figure-audit.py | tail -1"
run "$R" -- bash -c "cd $D && grep -c '\"id\"' corpus/instruments/figure-audit-ledger.json"
run "$R" -- bash -c "cd $D && for id in frontier-rows-r57 registry-rows-r57 entries-r57 knowledge-expected-r57 knowledge-files-r57 census-fresh-literal-r57 census-internal-r57-receipt census-gone-r57-receipt; do printf '%s=' \$id; grep -c \"\\\"id\\\": \\\"\$id\\\"\" corpus/instruments/figure-audit-ledger.json; done"
{
  echo '## limb B (census): the freshness gate reads stale at base on this host'
} >> "$R"
run "$R" -- bash -c "cd $D && python corpus/instruments/census-freshness-check.py . ; echo gate-exit=\$?"
{
  echo '## limb C (M57-8 fixture): the r54 red fixture is degenerate-red on this host (UNAVAILABLE, not the filed-vs-want reason)'
} >> "$R"
run "$R" -- bash -c "cd $D && python corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json; echo fixture-exit=\$?"
{
  echo '## limb D (R67 counter): the round-57 probe a2 stub tree is ADMITTED by the base counter'
} >> "$R"
P=$S/probe-a2
rm -rf "$P"; cp -a "$D" "$P"
K=$P/corpus/knowledge/iso-29147-30111-standard-records.md
{ head -n 7 "$K"; printf '%s\n' '(stub body: CriticFrontier probe a2 replica - the four falsifiable claims, the distinctness notes and the limits are removed; only the sources S089 and S090 are named here)'; } > "$K"
run "$R" -- bash -c "cd $P && wc -l corpus/knowledge/iso-29147-30111-standard-records.md"
run "$R" -- bash -c "cd $P && python corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F38|entries='; echo counter-exit=\$?"

R=$C/do-nothing-c2-r58.txt
receipt_init "$R" "round-58 C2 do-nothing control (pure base export; zero F39, the r57 state holds)"
run "$R" -- bash -c "cd $D && python corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F39|entries='; echo counter-exit=\$?"
run "$R" -- bash -c "cd $D && grep -cE '^\| F39 ' corpus/README.md; true"
run "$R" -- bash -c "cd $D && ls corpus/knowledge/*.md | wc -l"
run "$R" -- bash -c "cd $D && grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt"
run "$R" -- bash -c "cd $D && python corpus/instruments/capture-binding-check.py | tail -1; echo bind-exit=\$?"
run "$R" -- bash -c "cd $D && git -C $L rev-parse --verify $BASE >/dev/null && echo base-present"
echo DONE-ALL
