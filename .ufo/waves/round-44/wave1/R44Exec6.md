# R44Exec6 — C2 source/knowledge census

**Scope:** read-only census of committed r43 C2 inputs, plus a timestamped snapshot of the concurrently changing worktree. No production edits. No tools installed. Scratch used: `/fast/scratch/hyaku/kasegi-r44/R44Exec6/` (default `/fast/scratch/hyaku` because `HYAKU_SCRATCH` was unset); removed before yield.

## Frozen baseline and exact counts

The do-nothing control identifies base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`. `git archive 5ab3a60a` was extracted under scratch; C2 corpus files are unchanged at freeze commit `66314015122b9aa32dc40f2f1815df56624c26d1` (`git diff --name-only 5ab3a60a 6631401` listed only six `.ufo/waves/round-44/` freeze files).

Commands run against the base export:

```sh
grep -cE '^\| F[0-9]+ \| .* \| admitted \|' "$S/base/corpus/README.md"
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$S/base/corpus/SOURCES.md"
find "$S/base/corpus/knowledge" -maxdepth 1 -name '*.md' | wc -l
```

Observed stdout: `25`, `68`, `62`. Registry IDs are contiguous S001–S068 (68 rows, no missing IDs). Base SOURCES contains 19 manifests/57 records; all 55 mined sources are captured and cited, none is uncaptured, uncited, or missing its declared `used-by` path. SOURCES validation on the base export exited 0 with only the two existing W04 duplicate-URL warnings (S028/S029).

**Frozen C2 counter defect:** claims.json C2 counter uses `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`, which does not match the actual table shape (`| F01 | topic | admitted |`). Against the base export it prints `0` and exits 1. The frozen control's shape-aware regex, `grep -cE '^\| F[0-9]+ \| .* \| admitted \|'`, prints `25`. Thus the claim's own frontier counter cannot report either the before or intended after count; the discrepancy is in the committed counter predicate, not the census data.

## Frontier candidate gaps in the frozen base

A static crosswalk of SOURCES rows, `used-by`, knowledge `source:`/`recheck:` declarations, manifest IDs, and README frontier source cells finds **nine mined sources outside every frontier row's `sources` cell**. S030 is excluded as a gap: its current knowledge entry is bound by F07 and describes S031; S030 is superseded historical context. The eight useful candidate leads plus that contextual exception are:

| Source | Knowledge entry / recorded ground | Evidence for gap |
|---|---|---|
| S016 | `anthropic-cvd-provenance-and-pacing.md`; ground says extends F02 with AI-origin labels and submission pacing | tier A/mined; captured in round-40; no frontier row lists S016 |
| S017 | `pz-reporting-transparency-trial.md`; ground calls it a fourth disclosure-timeline shape | tier A/mined; captured round-40; no frontier row lists S017 |
| S019 | `nist-sp800-216-vdp-framework.md`; ground explicitly says `core — no frontier row covers a government-side disclosure framework` | tier A/mined; captured round-40; no frontier row lists S019. Strong grouped candidate with S020/S021/S023 |
| S020 | `doj-vdp-framework-scope-and-authorization.md`; ground says it extends F09/F03 | tier A/mined; captured round-40; no frontier row lists S020 |
| S021 | `cisa-bod-20-01-vdp-minimums.md`; ground says it extends F03/F02 | tier A/mined; captured round-40; no frontier row lists S021 |
| S023 | `cisa-cvd-program-stages.md`; ground says it adds CISA's coordinator-side stages/CNA role beside F06 | tier A/mined; captured round-40; no frontier row lists S023 |
| S025 | `cve-bench-agent-exploitation-benchmark.md`; ground says it adds capability measurement to F04 | tier A/mined; captured round-40; no frontier row lists S025 |
| S067 | `claim-package-gate.md`; a capability entry, not currently a frontier row | round-43 tier-A/mined curl advisory; captured at `corpus/source-snapshots/round-43/S067.txt`; no frontier row lists S067 |
| S030 | `cna-assignment-and-vulnerability-rules.md` declares current S031; prose retains S030 as superseded history | Not a new candidate: F07 lists S031, not S030; S030 is not in any frontier `sources` cell |

The most explicit new frontier candidate is a **government-side vulnerability-disclosure framework** grouping S019/S020/S021/S023: NIST's entry explicitly labels that area `core`, while DOJ/CISA entries separately describe adjacent expansions of F03/F06. Other valid leads are the S067 vendor-advisory/claim-package provenance surface and the S016/S017/S025 expansions recorded against F02/F04. These are candidate gaps, not admissions or proof that any one should be selected.

Other useful census facts: 34 base knowledge files are not named in a frontier entry cell (26 are operational/non-source entries; 8 are source-grounded knowledge entries outside the frontier). All frontier source IDs resolve to registry rows, and every frontier entry path resolves. The 13 rejected base rows retain their own flip criteria in SOURCES.md; none is counted as mined coverage. S068 is the round-43 rejected tier-B duplicate/derived GitHub advisory, not an admitted candidate; its recorded flip requires a Reviewed entry with package/version ranges or fixing commit.

## Round-43 paths relevant to C2

`git diff --name-status ab98fac9 dbd2e106 -- corpus/SOURCES.md corpus/knowledge corpus/source-snapshots` shows SOURCES modification, addition of `corpus/knowledge/claim-package-gate.md`, and additions `corpus/source-snapshots/round-43/S067.txt` plus `manifest.json` (the SOURCES/knowledge ledger also has unrelated appended/corrective changes). The r43 manifest binds S067 to URL `https://curl.se/docs/CVE-2025-9086.html`, SHA-256 `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b`, 3,822 bytes/109 lines; `sha256sum` and `wc -lc` reproduce those file values. S067's `used-by` and knowledge `source:` point to `claim-package-gate.md`; that path exists. The companion S068 row is rejected with a recorded falsifiable flip.

## Concurrent worktree snapshot (not committed evidence)

Other seats were actively editing shared worktree files during this census. I copied the C2 corpus inputs to scratch and recorded SHA-256s in `wsnap/digests.txt`; snapshot time is in `wsnap/SNAPSHOT-UTC.txt`. At that snapshot, the exact frozen-control-shaped counters printed: frontier `26`, SOURCES `70`, knowledge `63`. C2 claims' narrower frontier regex still printed `0` (exit 1). The worktree contained F26, S069 (tier-A/mined), S070 (tier-C/rejected), `google-cloud-vrp-customer-resource-boundary.md`, round-44/S069 capture+manifest, and an updated expected-list count of 63. The snapshot census found 58 manifest records; all 56 mined sources were captured/cited and all registry `used-by` paths resolved. SOURCES validation on this scratch snapshot exited 0 with the same W04 warnings as baseline.

The round-44 S069 capture digest is `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2` (45,681 bytes/1,132 lines), matching the manifest; local `source-recheck.py --manifest …/round-44/manifest.json --source S069` printed Q1/Q2/Q3 OK and exited 0. The S069 manifest URL and registry URL matched when checked after a concurrent manifest edit; an earlier read saw a different manifest URL, so only the copied snapshot represents the state used for the counts above.

**Current F26 gate risk observed in that snapshot:** its README entry cell is backtick-wrapped; `frontier-recheck-count.py:104` explicitly accepts optional backticks, so the path shape itself is supported. However its entry's line 5 is `recheck: 180d — cd … && python3 …source-recheck.py …`. The harness extracts the full value with `RECHECK_LINE` (`:109`) and executes it with `bash -c` (`:269-270`); its precheck only tests for the substring `source-recheck.py` and required options (`:251-263`). Exact shell probe `bash -c '180d — cd … && true'` printed `bash: line 1: 180d: command not found`, exit 127. Therefore this captured F26 entry would fail the frontier recheck harness (`recheck-exit-127`) unless its recheck line is corrected before integration. I did not run the frontier harness; this is a direct parser-path reading plus exact shell behavior evidence.

## Limitations / handoff

This report is a census, not an admission recommendation or a non-author verdict. Shared files were changing during the run; all base figures are pinned to the committed base export, and worktree figures apply only to the copied snapshot identified by the scratch digests. No build, lint, test suite, formatter, or frontier gate was run. No tool install/update occurred.