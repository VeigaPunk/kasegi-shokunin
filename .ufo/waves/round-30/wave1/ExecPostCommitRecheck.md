# Round-30 post-commit recheck executor report

## Implementation

Added executable `.ufo/waves/round-30/post-commit-recheck.sh`. It runs from any working directory by entering the lane root, executes frozen C1 A1/A2/B1/B2 fixture counters, then C2 frontier/entry/source-row/registry counts, census, frontier harness and each round-30 source recheck. It prints each requested summary field (`a1_exit`, `a2_exit`, `b1_exit`, `b2_exit`, `frontier`, `entries_citing_s046_047`, `S046_S047_rows`, `registry_rows`, `census_exit`, `harness_exit`, `recheck_exit`, final `post_commit_recheck_exit`) and returns nonzero on failed expectations. It does not access network or mutate repository metadata.

## Exact dry-run evidence (current working tree)

`bash -n .ufo/waves/round-30/post-commit-recheck.sh` succeeded. Dry-run output:

```text
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
a1_exit=1
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
a2_exit=1
S043:manifest MISMATCH reason=stem-mismatch
b1_exit=1
S045:manifest MISMATCH reason=stem-mismatch
b2_exit=1
frontier=14
entries_citing_s046_047=0
S046_S047_rows=2
registry_rows=47
kasegi\tW04\tS028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi\tW04\tS029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi\tE11\tS046 missing used-by corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
kasegi\tE11\tS047 missing used-by corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
census_exit=1
[Harness lists F01-F13 PASS, then:]
FAIL     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=-              exit=-    problems=missing-entry
entries=17 pass=16 exit=1
harness_exit=1
manifest UNAVAILABLE reason=missing
manifest UNAVAILABLE reason=missing
manifest UNAVAILABLE reason=missing
recheck_exit=1
post_commit_recheck_exit=5
```

## Risks / blockers

At measurement time, the assigned F14 entry and `corpus/source-snapshots/round-30/manifest.json` were not on disk; SOURCES S046/S047 used-by targets were missing. Thus dry run is correctly red for C2 and cannot yet demonstrate final green values; script should be re-run by L1 after integration. `entries_citing_s046_047` measured 0 (rather than target 1) on these bytes. The harness and recheck gates explicitly require F14 and round-30 manifest assertions. No tools installed. Only script and this exclusive report were written.
