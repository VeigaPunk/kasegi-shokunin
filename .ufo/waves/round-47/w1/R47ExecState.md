# Round-state receipts — R47ExecState

Axes: depth:verifiability; coverage. Commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; fresh base export is `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8` via `git archive` into seat scratch.

## (1) Sources census validation
Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
```text
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md

[exit code: 0]
```

## (2) Capture binding check
Command: `python3 corpus/instruments/capture-binding-check.py --root .`
```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-45 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-47 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=63 with_url=63 with_fetched_utc=25 with_archival=38 snapshot_dirs=24 manifest_dirs=24 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S075 dir=round-47
FAIL rule=no-row record=S076 dir=round-47
records=63 bound=61 unbound=2

[exit code: 1]
```

## (3) Current-tree recheck audit
Command: `python3 corpus/instruments/recheck-audit.py --root . --quiet`
```text
strict pass=66/66 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=44 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=66 total=66 pass=66 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=66 missing=0 unexpected=0 exit=0

[exit code: 0]
```

## (4) Base-export recheck audit
Command: `python3 corpus/instruments/recheck-audit.py --root /fast/scratch/hyaku/kasegi-r47/R47ExecState/base --quiet`
```text
strict pass=1/66 cdroot_fail=65 instrument_fail=0 own_fail=0
executes=44 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=66 total=66 pass=66 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=66 missing=0 unexpected=0 exit=1

[exit code: 1]
```

## (5) Frozen-counter do-nothing replay
Command: `python3 corpus/instruments/freeze-check.py --claims .ufo/waves/round-47/claims.json --tool-root . --base /fast/scratch/hyaku/kasegi-r47/R47ExecState/base --work /fast/scratch/hyaku/kasegi-r47/R47ExecState/work`
```text
claim C1 base_read=routed-defects total=11 fixed=0 unresolved=11 exit=1 verdict=ok
claim C2 base_read=f30-gate fixed=1/7 exit=1 verdict=ok
freeze-check claims=2 base_ok=2 exit=0

[exit code: 0]
```

## Control and limitations
The do-nothing control is the frozen base export above, not the current working tree. Freeze-check emitted no `finding FC-*` lines; its three claim/summary lines at 76–78 are the complete output, with each expected-before line matched and no expected-after line present (per the counter's `verdict=ok`). No full mutation battery was run. Known pre-freeze receipt remains 35/19/16 (C1) and 21/3/18 (C2), total 34 survivors; this run does not reclassify survivors or prove mutants equivalent. Capture binding check remains red for S075 and S076 (`no-row`, lines 44–45); recheck audit against current tree passes while base audit fails as expected for the frozen control.
