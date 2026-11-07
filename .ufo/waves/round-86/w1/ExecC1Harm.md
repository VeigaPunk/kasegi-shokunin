# ExecC1Harm — C1 harm probe (round 86, attempt 1)

**Method.** Two `git clone --shared` checkouts under scratch
`/fast/scratch/hyaku/kasegi-r86/ExecC1Harm/` (since deleted after receipt copy):
`before/` = freeze `252df0c90c066d83d229e3107811a6bc05e8feed` untouched;
`after/` = same freeze + `python3 -B .ufo/waves/round-86/c1/apply-map.py
--root <after> --map .ufo/waves/round-86/c1/repair-map.json`
(`APPLY files_changed=14 keys=203`). Every lane gate/instrument whose docstring
says it reads `corpus/knowledge/` or knowledge-entry citations was run
identically on both clones with `TMPDIR=$S` and `python3 -B` (usage line read
first per tool; full `resolve.py` census never run — the knowledge-meter counter
is the scope reading). Changed files: 14 entries under `corpus/knowledge/`
(the `git diff --name-only` set: anthropic-cvd-provenance-and-pacing,
cisa-bod-20-01-vdp-minimums, cisa-cvd-program-stages,
cve-bench-agent-exploitation-benchmark, cve-services-publication-api,
doj-vdp-framework-scope-and-authorization,
github-advisory-database-curation-semantics,
github-global-security-advisories-rest-api,
github-private-vulnerability-reporting,
github-repository-security-advisories, iso-29147-30111-standard-records,
linux-kernel-security-bugs-reporting-process, zdi-disclosure-policy,
zdi-disclosure-process-and-vendor-coordination). No `recheck:` line is touched
(`grep -c "^recheck:"` over all 542 changed diff lines = 0).

**Frozen counter (scope check).** `python3 -B
.ufo/waves/round-86/c1/knowledge-meter.py --lane <after> --base-rev
252df0c… --map .ufo/waves/round-86/c1/repair-map.json --target 596/1716
--map-sha256 dd40455a… --work <scratch>/w` →
`KNOWLEDGE-METER base=398/1721 after=596/1716 target=596/1716 keys=203
mirror_absent=True`; LIMB M1 pass, M2 pass (removed=203 keys=203
stray_removed=0 stray_added=0 unrepaired=0), M3 pass (same_files=True
bad_lines=0 keys_hit=203), M4 pass, M5 pass, M6 pass;
`KNOWLEDGE-METER-RESULT pass rc=0`. The map reproduces the frozen target
exactly and changes no verdict other than the intended M1/M2/M3 flips.

## Per-tool results (command; before rc/summary; after rc/summary; verdict change?)

| Tool | Command (run inside each clone) | Before | After | Verdict changed? |
|---|---|---|---|---|
| `corpus/instruments/citation-ground-check.py` | `python3 -B corpus/instruments/citation-ground-check.py --root $S/{before,after}` | rc=1, `unresolved-class=1 class-lane-bare=1 class-fleet-relative=0 class-total=20 ledger-rows=68 rows-resolving=68 findings=2 verdict=failed` (2 findings: `row-new-absent kake-shokunin/…security-txt-publishing.md:63 …SOURCES.md:111` + `class-lane-bare SOURCES.md:142 corpus/lessons/round-57.md:5`; 19 blocked-protected) | rc=1, byte-identical stdout (`diff` empty) | **No** |
| `corpus/instruments/capture-binding-check.py` | `python3 -B corpus/instruments/capture-binding-check.py --root $S/{before,after}` | rc=0, `AUDIT records=103 with_url=103 … snapshot_dirs=59 manifest_dirs=59 missing_manifest=0 … orphans=1 orphan=S040-live.txt records=103 bound=103 unbound=0` | rc=0, byte-identical | **No** |
| `corpus/instruments/gate-quote-audit.py` | `python3 -B corpus/instruments/gate-quote-audit.py --root $S/{before,after}` | rc=1, `GATE-QUOTE-AUDIT annotated=10 ok=8 erratum-on-record=2 failures=2` | rc=1, byte-identical | **No** |
| `corpus/instruments/figure-audit.py` | `python3 -B corpus/instruments/figure-audit.py --root $S/{before,after} --ledger corpus/instruments/figure-audit-ledger.json` | rc=0, `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` | rc=0, byte-identical | **No** |
| `corpus/instruments/recheck-audit.py` | `python3 -B corpus/instruments/recheck-audit.py --root $S/{before,after}` | rc=1, `strict pass=0/98 cdroot_fail=98 instrument_fail=0 own_fail=0 executes=76 gated=22 broken=0 lines=98 total=98 pass=98 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1 expect=present expected=98 missing=0 unexpected=0 exit=1` | rc=1, byte-identical | **No** |
| `corpus/instruments/recheck-cwd-census.py` | `python3 -B corpus/instruments/recheck-cwd-census.py --root $S/{before,after} --lane $S/{before,after}` | rc=1, `RECHECK-CWD entries=98 noprefix=98 exit2_foreign=0 exit0_foreign=76 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0 RECHECK-CWD-RESULT nonconformant` | rc=1, byte-identical | **No** |
| `corpus/instruments/score-gap.py` | `python3 -B corpus/instruments/score-gap.py --root $S/{before,after}` | rc=0, `census-lane: 1227/5152 = 23.82% census-skill: 132/701 = 18.83% gap: 22 of 98 rechecks still gated…` | rc=0, census-lane/census-skill/gap lines identical (committed census bytes unchanged — the map edits knowledge files, the census is generated over SKILL.md + corpus and is stale in both roots identically) | **No** |
| `corpus/instruments/frontier-recheck-count.py` | `python3 -B corpus/instruments/frontier-recheck-count.py --root $S/{before,after}` | rc=0, `entries=63 pass=63 exit=0` | rc=0, byte-identical | **No** |
| `corpus/instruments/resolve-dispatch-check.py` | `python3 -B corpus/instruments/resolve-dispatch-check.py` | rc=0, `cases=8 pass=8 exit=0` (resolver sha256 `db5e0767…` matches claims.json) | rc=0, byte-identical | **No** |
| `corpus/instruments/census-freshness-check.py` | `python3 -B corpus/instruments/census-freshness-check.py $S/{before,after}` | rc=1, `CENSUS-FRESH=stale files=citation-survival.md+citation-survival.tsv (committed bytes differ from what resolve.py generates over the current tree; regenerate the census or repair the tree)` | rc=1, byte-identical | **No** |
| `corpus/instruments/r46-plain-measure.sh` (reads `corpus/knowledge/*.md`; grep/bash only) | `bash corpus/instruments/r46-plain-measure.sh $S/{before,after}` | rc=0, `c1a=21 c1b=22 c2a=60 c2b=123 c2c=98 c2d=5` | rc=0, byte-identical | **No** |
| `corpus/instruments/anchorcheck.py` (per changed knowledge file) | `python3 -B corpus/instruments/anchorcheck.py <each changed corpus/knowledge/*.md>` | rc=0 each; bare `S<digits>.txt[:N]` cites read `BASE-ABSENT md:<ln> S… (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S….txt)` because the mirror root is absent in the scratch clone | rc=0 each; the same cites now read `OK md:<ln> corpus/source-snapshots/round-*/S….txt:<N> [cited line text]` with the anchor verified in range against committed bytes (29 `OK md:` lines across the 14 files, incl. the retained anchor pairs `S078:6,125`, `S103:273,13,356,486`, `S105:572,600,603`, `S106:28,31,47,49,60,70`, `S071:117,332,333-334`, `S075:25,26`) | **Yes — by design**: `BASE-ABSENT` (not a fail class; rc stays 0 in both) becomes `OK`/in-range. This is the harm probe's positive control: the repointed anchors are verified in range against committed bytes, never `PAST-EOF` or `MISSING-FILE` |
| `corpus/instruments/density.py` (per changed knowledge file) | `python3 -B corpus/instruments/density.py <file> --label {before,after}` | — | — | **No density harm**: total path-citation instances identical per file before/after (3, 15, 14, 17, 21, 11, 61, 48, 35, 50, 18, 59, 26, 89 across the 14 files; block counts unchanged) — repointing a citation to its full path does not change the path-like token count. (P4's `density.py SKILL.md` gate is unaffected: only knowledge files change.) |

## Frozen controls (re-run)

`bash .ufo/waves/round-86/controls/c1-controls-r86.sh $S/c1c`
(`$S` = seat scratch root) → rc=0, output `diff` against
`.ufo/waves/round-86/controls/c1-controls-r86.txt` is **empty — matches modulo
scratch paths** (first line `counter_sha256=03df491b… map_sha256=dd40455a…
resolve_sha256=db5e0767… base=d7296645… target=596/1716`; all six controls
reproduce: do-nothing fail 398/1721 rc=1, positive pass 596/1716 rc=0,
partial fail 494/1716 rc=1, de-cite fail 398/1518 rc=1, pad fail 597/1717 rc=1,
wrong-file fail M4 `S071.txt:117` rc=1, map-sha fail M6 rc=1).

## Verdict

**No harm found.** The frozen 203-key map changes exactly the intended
things — the knowledge-meter flips `398/1721 → 596/1716` (M1/M2/M3
green; M2 `stray_removed=0 stray_added=0 unrepaired=0`; M3 `bad_lines=0
keys_hit=203`) — and every other knowledge-reading gate in the lane reads
**byte-identical** before/after (citation-ground, capture-binding,
gate-quote, figure-audit, recheck-audit, recheck-cwd, score-gap census+gap,
frontier-recheck, resolve-dispatch, census-freshness, plain-measure), while
`anchorcheck` improves `BASE-ABSENT` → verified-in-range `OK` on every
repointed anchor (the map's own correctness control) and `density.py` per
changed file is unchanged (instance and block counts identical). No tool flips
red→green or green→red except the intended meter flips; no knowledge file,
`recheck:` line, ledger, manifest, or census byte other than the 203 key
replacements is touched.

**Risks / notes (not blockers).**
- Pre-existing reds are identical on both sides and therefore not C1 harms:
  citation-ground rc=1 (2 findings), gate-quote rc=1 (2 MISMATCH), recheck
  gates rc=1 (98/98 noprefix / 22 gated), census-fresh rc=1 (stale census in
  the scratch root). The map does not perturb any of them.
- `anchorcheck` in a scratch clone reads `BASE-ABSENT` for bare cites (mirror
  absent) and `OK` for repointed cites — the improvement is in the
  informational (non-fail) bucket; both sides exit 0. In the fleet root the
  same improvement holds for the INTERNAL reachability question, which is
  exactly what the meter's M4 asserts.
- Receipts (92 files: every tool's `.out`, `.err`, `.rc`, `.both` for
  before/after, `diff`-empty attestations are the identical outputs,
  `density-changed.txt` per-file instance counts, `anchor-changed.txt`
  per-file anchorcheck before/after, `knowledge-meter-after.out`,
  `c1-controls.out`) are beside this report under
  `ExecC1Harm-receipts/`; the scratch clones were deleted after the copy
  (`trap`-equivalent manual `rm -rf` — verified gone).

**Files written.**
- `.ufo/waves/round-86/w1/ExecC1Harm.md` (this report).
- `.ufo/waves/round-86/w1/ExecC1Harm-receipts/` (92 receipt files listed above).

**Tools installed/upgraded:** none (read-only probe; `pacman` untouched per
host pause). No network use (only `git clone --shared` of the local lane,
read-only `git diff`/`checkout` inside the scratch clones).
