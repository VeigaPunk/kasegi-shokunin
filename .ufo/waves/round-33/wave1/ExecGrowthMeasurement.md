# ExecGrowthMeasurement — round-33 committed wave-evidence growth (considerthese 2026-10-25 proposal 1)

Seat: `ExecGrowthMeasurement` (leaf). Answering model, as the workstation reports it: `opencode-go/deepseek-v4.1-flash`. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; integration byte measured: `9f9848816503aa0cd566fc2efdc5e69ea501a253` ("round-33: wave-1 integration (C1 capture-binding-check + manifest binding; C2 F16 admitted; wave receipts)"). Snapshot time `2026-10-26T04:39:07Z`. Measurement domain: `.ufo/waves/round-33` only; no tool installed or upgraded (pacman untouched).

Verdict up front: the round committed **1,366,042 B (1.30 MiB) of wave evidence** — **27.3 % of the 5 MB budget the dispatch sets, under budget by 3,633,958 B** — with **0 corpus-copy paths** and **0 scratch trees**. The 5 MB figure is the round-33 dispatch item's budget; R14 itself only requires that "per-round repo growth is measurable from committed bytes" (`corpus/QUALITY.md:83`, 7 words).

## §0 Instrument and its controls (what the counter can and cannot see)

The instrument is git plumbing, unchanged this round: `ls-tree -r -l <rev> -- <path>` sums committed blob bytes; `diff --stat/--numstat <base> [<rev>] -- <path>` counts committed file/line deltas. Two limbs were exercised, both with a failing control:

| limb | control | reading |
|---|---|---|
| `diff` counts committed change only | fixture repo (`mktemp -d` under my scratch, `git init -q`, toplevel verified `= $D`): base commit, then one **untracked** `u.md` | `UNTRACKED numstat=0 statfiles=0`; after `git add`+commit: `COMMITTED numstat=1 stat= 1 file changed, 1 insertion(+)` — an uncommitted receipt is invisible to the diff counter |
| `ls-tree -l` measures committed bytes | same fixture after the commit | `ls-tree total=14` (= 4 B tracked `f.txt` + 10 B new `u.md`), matching file sizes |
| counter is not always-positive | `git diff --numstat BASE HEAD -- .ufo/waves/round-27` and `-- .ufo/waves/round-31` (untouched this round) | 0 lines each |
| baseline is genuinely empty | `git ls-tree -r -l BASE -- .ufo/waves/round-33` (dir absent at BASE) | 0 entries |

This is why the committed numbers below are quoted from `BASE..HEAD`, not from the worktree: at `04:31:42Z`, with 40 receipts on disk (713,392 B in `wave1/`), `git diff BASE -- .ufo/waves/round-33` reported only the 21 tracked planner files — a **PRE-STATE worktree reading (1,074,537 B for the wave dir) that is not comparable to a committed column**. The re-run that replaces it is `git diff --stat BASE HEAD -- .ufo/waves/round-33` after the integration commit; that run is §1.

## §1 The three item commands at the integration byte

```
$ git -C . diff --stat 690b69da 9f98488 -- .ufo/waves/round-33 | tail -1
 132 files changed, 17170 insertions(+)
$ git -C . diff --numstat 690b69da 9f98488 -- .ufo/waves/round-33 | awk '{s+=$1} END{print s+0}'
17170
$ git -C . diff --stat 690b69da -- .ufo/waves/round-33 | tail -1     # worktree form, 04:36Z, in-flight
 132 files changed, 17181 insertions(+)
$ git -C . diff --stat 690b69da -- .ufo/waves/round-33 | tail -1     # same command, 04:39:50Z
 132 files changed, 17198 insertions(+)
```

The gap is post-commit in-flight drift, not evidence: `git status --porcelain -- .ufo/waves/round-33` moves while seats edit (` M wave1/ExecDeterminism.md`, ` M wave1/ExecEntryF16.md`; the same command read `17181` at 04:36Z and `17198` at 04:39:50Z). M30-3 applies: the worktree column is non-comparative; the committed `17170` is the citable figure, and the receipt you are reading is itself untracked (`?? wave1/ExecGrowthMeasurement.md`), hence outside every worktree count above.

Committed bytes, the budget denominator's numerator:

```
$ git -C . ls-tree -r -l HEAD -- .ufo/waves/round-33 | awk '{s+=$4;n++} END{print "files="n" bytes="s}'
files=132 bytes=1366042
```

Composition of those 132 files (all from `ls-tree -r -l`, split by path class):

| class | files | bytes | share |
|---|---|---|---|
| seat receipts `wave1/*.md` | 52 | 771,618 | 56.5 % |
| seat support dumps `wave1/{ExecCaptureBinding,ExecRegressionC1,ScribeInstrReadme,ScribeSkillGate}/` + `wave1/swarm-registry.json` | 58 | 233,279 | 17.1 % |
| wave root (planner + controls + logs) | 22 | 361,145 | 26.4 % |
| **total** | **132** | **1,366,042** | 100 % |

Wave-root detail: `wave1-dispatch.json` 98,685 + `wave1-plan.out` 97,958 + `wave1-spec.json` 72,624 + `build-spec.py` 65,308 = **334,575 B (24.5 % of all wave evidence is machine-generated planner text)**; `c1-controls` 1,655 B and `c2-controls` 2,465 B together are 0.3 %.

## §2 Per-item receipt size table

```
$ du -sh .ufo/waves/round-33/wave1/*.md | sort -rh | head -8
28K  .ufo/waves/round-33/wave1/ScoutPackageThemes.md
28K  .ufo/waves/round-33/wave1/RevRowS050.md
24K  .ufo/waves/round-33/wave1/SentCred.md
24K  .ufo/waves/round-33/wave1/RevClaimsFreeze.md
24K  .ufo/waves/round-33/wave1/ExecRegistryAppend.md
24K  .ufo/waves/round-33/wave1/ExecQuarantine.md
24K  .ufo/waves/round-33/wave1/ExecForeignCwd.md
24K  .ufo/waves/round-33/wave1/ExecEntryF16.md
```

Byte-exact committed table (overrides `du`'s 4 KiB rounding), top 8 of 52:

| bytes | receipt |
|---:|---|
| 27,259 | `wave1/RevRowS050.md` |
| 24,644 | `wave1/ScoutPackageThemes.md` |
| 24,004 | `wave1/CritExpansion.md` |
| 23,356 | `wave1/ExecQuarantine.md` |
| 23,181 | `wave1/SentCred.md` |
| 22,636 | `wave1/CritC2Kill.md` |
| 22,560 | `wave1/ExecRegistryAppend.md` |
| 22,449 | `wave1/ExecEntryF16.md` |

Distribution over the 52 committed receipts: mean **14,839 B**, median **14,063 B**, p90 **22,560 B**, max **27,259 B** — no outlier receipt dominates; the largest is 2.0 % of the wave's bytes.

## §3 Budget verdict (5 MB, R14)

- measured: **1,366,042 B** committed at `9f98488`.
- budget: 5,000,000 B (round-33 dispatch item).
- share: **27.3 %**; headroom **3,633,958 B**; **under budget**.
- coverage caveat: 52 of 64 dispatched seats have committed receipts; the 12 absent at the integration byte are `CritMistakes`, `ExecGrowthMeasurement` (this one), `ExecNoHarmFinal`, `ExecScratchDiscipline`, `ExecWaveEvidencePack`, `RevC1BeforeAfter`, `RevGateSpot`, `ScribeLesson`, `ScribeReportDraft`, `ScribeScorecard`, `ScribeShonen`, `SimplifierCleanup`. An arithmetic projection at the observed mean (12 × 14,839 B ≈ 178,068 B) lands at ≈ 1,544,110 B — **a projection, not a measurement**; the post-closure re-run is `git -C {LANE} ls-tree -r -l HEAD -- .ufo/waves/round-33 | awk '{s+=$4} END{print s}'` (plus the two diff commands of §1).
- R14 conformance is separate from the byte total: the largest single control/fixture tree in the wave is `ExecRegressionC1` at 95,376 B / 22 flat text files (21 `.txt`, 1 `.patch`) — under R14's "larger than a few hundred kilobytes" threshold, so no tarball was required, and none was committed.

## §4 Hygiene — no corpus copy, no scratch tree

```
$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-33 | grep -c '/corpus/'
0
$ find .ufo/waves/round-33 \( -name corpus -o -name '.git' -o -name node_modules \) -print
        (no output)
$ find .ufo/waves/round-33 -name '*.tar*' -o -name '*.zip' -o -name '*.tgz'
        (no output)
$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-33 | grep -c 'fast/scratch'
0
```

Contrast with the bloat the proposal targets, re-measured on committed bytes rather than quoted from the daily note: `round-25` holds **3,773 committed files / 57,511,001 B**, of which **3,097 paths contain `/corpus/`** — the full-corpus-copy pattern R14 forbids; round-33 holds 132 files and 0 `/corpus/` paths. 48 committed wave-33 files contain the literal string `kasegi-r33` (the planner prompt text embedded in `build-spec.py`, the dispatch/spec/plan JSON and seat receipts that record their scratch root) — **path mentions inside text, not tree copies**: `grep -c 'fast/scratch'` over committed *paths* is 0 and the tree contains no directory named after a scratch tree.

## §5 Longitudinal growth, same instrument, all rounds (committed `ls-tree` bytes at HEAD `9f98488`)

| round | files | committed bytes |
|---|---:|---:|
| 23 | 104 | 1,691,701 |
| 24 | 82 | 1,079,812 |
| 25 | 3,773 | 57,511,001 |
| 26 | 1,535 | 26,199,699 |
| 27 | 10 | 10,126 |
| 28 | 361 | 5,696,697 |
| 29 | 222 | 3,878,016 |
| 30 | 153 | 1,796,861 |
| 31 | 243 | 2,991,556 |
| 32 | 23 | 401,010 (wave-1 withdrawn, no seat ran) |
| **33** | **132** | **1,366,042** |

Round-33 is the second-smallest wave that produced receipts, behind round-24 (1,079,812 B; round-27 committed only c1/c2 controls and round-32's wave-1 was withdrawn), 42× smaller than round-25 and 2.2× smaller than round-31. Whole-round repo growth for comparison (`git diff --numstat BASE HEAD`): 151 files, 18,434 insertions, of which the wave dir accounts for **17,170 lines (93.1 %)**; new-file bytes across the range total 1,417,861 B, of which wave evidence is **1,366,042 B (96.3 %)** and the corpus/registry/manifest delta 51,819 B.

## §6 Where the remaining bytes are (waste candidates, measured)

| candidate | bytes | share of wave evidence |
|---|---:|---:|
| planner artifacts (`wave1-dispatch.json`, `wave1-plan.out`, `wave1-spec.json`, `build-spec.py`) | 334,575 | 24.5 % |
| anchor dumps (`ExecRegressionC1/anchor.txt` 38,931, `anchor-base.txt` 26,015, `ScribeSkillGate/anchor-final.txt` 38,917, `anchor-after3.txt` 38,917) | 142,780 | 10.4 % |

The two `ScribeSkillGate` anchor dumps are the same size but **different bytes** (`sha256 7c037484…` vs `2ef8fb8f…`), so they are a near-duplicate rather than a copy; the two `ExecRegressionC1` dumps differ in size (38,931 vs 26,015 B) and therefore in content. Compressing the four support directories as one `tar.gz -9` stream yields **43,009 B from 233,279 B (18.4 %)** — the R14 tarball route would have saved ≈ 190 KB here, and R14's threshold was not crossed, so this is headroom for a future round, not a defect in this one. No committed wave file reaches 200,000 B; the largest are the three planner JSON/logs and `build-spec.py` above.

## §7 Cleanup and re-run state

Scratch root `$HYAKU_SCRATCH/kasegi-r33/ExecGrowthMeasurement/` (fixture repo, PRE-STATE capture, added-file list) was deleted before this yield; the fixture and every command above ran with `-C` on an explicit path, and no git/jj mutation was issued in the lane (read-only plumbing only: `rev-parse`, `log`, `show --stat`, `diff`, `ls-tree`, `status`). Nothing outside `.ufo/waves/round-33/wave1/ExecGrowthMeasurement.md` was written. This receipt's own bytes are outside the §3 figure (written after the integration byte); a consumer wanting the closed number runs the §3 re-run after the L1 commits this receipt.
