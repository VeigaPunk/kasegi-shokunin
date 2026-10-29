VERDICT: HOLDS

Scope: no-harm sweep of the committed integration 5437afeaf9b642c267bba3c31f00ae701e49da68 against base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba (wave 2 seat R46W2RevNoHarm). Holds for the committed tip. Finding F0 (working-tree drift) is a blocker for the L1 commit step, not for the tip itself.

Scratch used and removed: /fast/scratch/hyaku/kasegi-r46/R46W2RevNoHarm (tip export, full-base export, copies for the census regeneration). Nothing was committed, pushed or indexed. Read-only git only.

## Findings

### N1 Deletions: exactly the two expected lines (HOLDS)
Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --numstat 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba 5437afeaf9b642c267bba3c31f00ae701e49da68 -- . ':!.ufo/waves/round-46'`
Output (deletion column nonzero only where marked):
```
2	0	PROVINCE.md
15	0	corpus/README.md
6	0	corpus/SOURCES.md
1	0	corpus/instruments/knowledge-expected.txt
342	0	corpus/instruments/r46-c1-gate.py
354	0	corpus/instruments/r46-c2-gate.py
480	0	corpus/instruments/r46-counters-selftest-c1.py
531	0	corpus/instruments/r46-counters-selftest-c2.py
637	0	corpus/instruments/r46-landing-gate.py
35	0	corpus/instruments/r46-plain-measure.sh
36	1	corpus/knowledge/claim-gates.md
30	1	corpus/knowledge/claim-package-contract.md
49	0	corpus/knowledge/github-private-vulnerability-reporting.md
589	0	corpus/source-snapshots/round-46/S073.txt
63	0	corpus/source-snapshots/round-46/manifest.json
```
Command: `git diff 914ca0b… 5437afe… -- corpus/knowledge | grep '^-' | grep -v '^---'`
Output (the removed lines, both are the gated recheck lines of the two re-grounded entries):
```
-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  # on-restoration — fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15
```
Each is replaced by `recheck: … r46-c1-gate.py --entry …` and the base line survives as `restoration-recheck:`, so no citation or restoration path is lost. Full-tree `git diff --numstat` (excluding round-46 .ufo) totals: added=3170 deleted=2. Axis: depth:verifiability (intended), no harm to density or coverage.

### N2 depth:density 9 on SKILL.md: unchanged (HOLDS)
Command: `python3 corpus/instruments/density.py SKILL.md --label x` in a full base export and a tip export; `diff` of the two outputs was empty (exit 0). SKILL.md is byte-identical: `cmp` printed `SAME`. Both print `| | **mean dens** | | | | | | | | **249.1** |`.
Note: the first base export I used was the corpus-only pure export (no `.ufo/`), which made anchorcheck report BASE-ABSENT artefacts; density was unaffected. I replaced it with `git archive 914ca0b…` for the anchor control.

### N3 anchorcheck on SKILL.md (HOLDS)
Command: `python3 corpus/instruments/anchorcheck.py SKILL.md` on the full base and the tip export. Both exit 0 and the outputs are identical (diff empty). Line 2 prints:
`== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
Control: the corpus-only pure base gave `… 13 in-range cite instances … BASE-ABSENT=3` and exit 1. That is the export missing `.ufo/waves/round-33` and round-34, not a tip defect.

### N4 recheck-audit (HOLDS on the lane root, as specified)
Command: `python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet`, run at about 21:18 and again earlier, both exit 0:
```
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
```
Matches the expected `executes=43 gated=22 broken=0`, `strict pass=65/65`, `expected=65 missing=0`.
Controls: the full base gave `executes=40 gated=24 broken=0` with `lines=64`, so the counts move in the direction the integration predicts (+3 executes, −2 gated). Running the audit against a tip export instead of the lane root gave `strict pass=1/65 cdroot_fail=64` because the recheck lines hardcode `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`. That is an export artefact; the lane root is the correct root.

### N5 capture-binding-check (HOLDS 60/60)
Command: `python3 corpus/instruments/capture-binding-check.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (exit 0):
```
AUDIT records=60 with_url=60 with_fetched_utc=22 with_archival=38 snapshot_dirs=22 manifest_dirs=22 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=60 bound=60 unbound=0
```
Control (full base): `AUDIT records=59 … ` and `records=59 bound=59 unbound=0`. Default mode is read-only: the `write_*` and `case_*` helpers are reached only from `--selftest`.

### N6 frontier counts (HOLDS, F28 closed)
Command: `python3 corpus/instruments/frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (exit 0):
`FRONTIER-CENSUS rows=28 admitted=28 closed=28 problem-rows=0 registry=73`, `FRONTIER-PASS F28 ids=S073`, `PASS     F28  corpus/knowledge/github-private-vulnerability-reporting.md ids=S073 exit=0`, `entries=31 pass=31 exit=0`.
Control (full base): `FRONTIER-CENSUS rows=27 admitted=27 closed=27 problem-rows=0 registry=72` and `entries=30 pass=30 exit=0`.
Command: `python3 corpus/instruments/r44-frontier-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --expect 28` → `frontier rows=28 admitted=28` (exit 0). Control: `frontier expected=28 admitted=27 verdict=SHORT exit=1`.

### N7 Re-grounded rows and re-ground gate (HOLDS)
Command: `python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`, output tail `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`.
Command: `… --entry corpus/knowledge/claim-package-contract.md`, output tail `reground entry=claim-package-contract.md rows=21 ok=21 files=4 distinct=1 exit=0`.
Control (full base, claim-gates): `reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0`.
Both pass on the committed bytes, and also when re-run on the tip export.

### N8 Census (HOLDS for SKILL.md scope; corpus changed by design)
Command: `python3 corpus/instruments/resolve.py <root>`, run on copies of the full-base and tip exports (it writes `citation-survival.md/.tsv` into its root, so the lane was not used). Outputs:
- tip: `distinct=4351 resolves=41 mirror=0 internal=913 other=0 gone=3397 skill=102/646 corpus=922/3970 all=954/4351`
- base: `distinct=4279 resolves=40 mirror=0 internal=865 other=0 gone=3374 skill=102/646 corpus=873/3898 all=905/4279`
- SKILL.md alone is `102/646 = 15.79%` at both. The 381 rows whose scope is exactly `SKILL` are identical between base and tip after normalising the scratch root name.
- Citations present in base but absent in tip: 0. Citations new at tip: 72 (from the new entry, the re-ground rows and the counters).
Limitation: the committed census of record (`corpus/instruments/citation-survival.md`, round 18, `134/1480 = 9.05%`) does not reproduce on this host. Even the base regeneration gives 905/4279, so the difference is host and mirror drift, not the integration. I did not refresh the committed census (out of scope, and it is a lane-owned artefact).

### N9 Base-to-tip counts on the lane root: no harm to coverage (HOLDS)
Coverage axis: the F28 row is admitted (`FRONTIER-PASS F28 … exit=0`), S073 is bound (`records=60 bound=60`), and the pinned capture digest matches the manifest: `sha256sum corpus/source-snapshots/round-46/S073.txt` = `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, identical to `"sha256": "66c96a…1930"` in `corpus/source-snapshots/round-46/manifest.json`.

## F0 Working-tree drift (blocker for L1 commit; not a defect in 5437)
- At my first `git status --short | grep -v '^??'` in the lane (before the 21:13 edits), there were no tracked modifications. Lane HEAD was `0d121a2` (wave-2 spec commit on top of 5437afe); `git diff --stat 5437afe HEAD -- . ':!.ufo'` was empty.
- At about 21:18 the lane has seven tracked modifications, not made by my commands:
```
 M PROVINCE.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/r46-landing-gate.py
 M corpus/knowledge/claim-gates.md
 M corpus/knowledge/claim-package-contract.md
 M corpus/knowledge/github-private-vulnerability-reporting.md
```
`git diff --numstat 5437afe -- . ':!.ufo'` gives `PROVINCE.md 1/1`, `corpus/README.md 2/2`, `corpus/SOURCES.md 4/4`, `r46-landing-gate.py 23/22`, `claim-gates.md 7/7`, `claim-package-contract.md 8/6`, `github-private-vulnerability-reporting.md 10/10`.
- mtimes: F28 entry 21:13:19, claim-gates 21:13:58, contract 21:14:03, SOURCES/README/PROVINCE 21:14:39 (one batch), landing-gate 21:17:27.
- Attribution: my commands do not write to the lane. `capture-binding-check.py` default mode is read-only (its writers run only under `--selftest`); `recheck-audit`, `frontier-recheck-count`, `r44-frontier-count` and `r46-c1-gate` write only to temporary directories (`shutil.rmtree` on their `sc`/`tmp` paths); `resolve.py` ran on copies. The edits are another writer's, probably the L1 integrating post-wave-1 fixes.
- Why it matters: if these uncommitted edits are committed as they stand, the deletion set stops being the two expected lines. The working tree removes lines in `claim-gates.md` and `claim-package-contract.md` (for example the `G12`, `G14`, `G15`, `G17`, `G24`, `G25` table rows) and `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` and `r46-landing-gate.py` lose lines. Re-run N1 and the re-ground gate on the new commit before it lands. The lane-root audit still gives 65/65 on the drifted tree, since the count is preserved, but that does not clear the deletion rule.

## Limitations
- The "lane working tree equals 5437" premise was true only at my first status check; the sweep numbers for N1–N3, N5, N8 come from committed bytes (the tip export and git plumbing). N4, N6, N7 were run on the lane root and are reported as run.
- The density and anchorcheck controls use the full base archive; the corpus-only pure export was only used for an earlier, discarded first pass.
- I did not run the counter selftests, the landing gate, or the claim-package instruments; those belong to other seats.
- Live-target testing was not performed; the corpus is documentation only.
