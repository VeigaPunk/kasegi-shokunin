# ExecInstrumentsSynopsis — round-36 instruments synopsis (no-harm baseline)

- Seat: `ExecInstrumentsSynopsis` (executor, leaf)
- Round: 36 / milestone round-36 — judged on `depth:verifiability`, `freshness`
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — HEAD `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze), base `cc692008b0cfd58d18275aa6c4aed79620120799`
- Runtime: `python3 3.14.8`, `bash 5.3.20(1)-release`, Linux 7.2.11-arch1-1 x64
- Scratch: `/fast/scratch/hyaku/kasegi-r36/ExecInstrumentsSynopsis` (`TMPDIR` and `HYAKU_SCRATCH` both bound there; removed before yield)
- Tooling installed/upgraded: **none** (no pacman, no `uv`, no `npx`, no binary drops). Nothing in `~/.omp/agent/` touched.

## 1. Verdict

**26 instrument runs, 26 × exit 0, zero red.** Every committed instrument's own gate passes on the round-36 base bytes; the no-harm baseline for C1/C2 is GREEN. Four registry digest pins re-verified live (`kill-rule-check` counter `c279d952…`, its instrument `3d9e5e0d…`, `r-defect-closure.sh` `809aaf90…`, `limb-ledger.json` `c042adf6…`), and `SKILL.md` measures `daeff71b…` — the same blob `SCORECARD.md:1314` scores.

No failure was found, so there is nothing to route as a defect. Two **observations** (§6) are recorded instead: a structurally stale census of record and an older pinned count set drifting with growth. Neither is quoted by any live round-36 cell.

## 2. Method and read-only bound

All runs `cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the lane root), with `TMPDIR`/`HYAKU_SCRATCH` under the seat scratch dir; `KASEGI_BOUNTIES` unset (canonical arm).

Read-only proof, before and after the whole matrix:

- `git rev-parse HEAD` → `b47f2cd…` unchanged.
- `git status --porcelain` → **9** entries before, **9** after, every one an untracked path under `.ufo/waves/round-36/` (wave scaffolding + sibling receipts). `git status --porcelain | grep -v '^?? \.ufo/waves/round-36/'` → empty: **zero tracked modifications**.
- No scratch dir, log, or generated file written anywhere under the lane; `find` for the seat path inside the lane → empty.

One instrument had to be sandboxed: **`resolve.py` unconditionally writes its own directory's `citation-survival.tsv` and `citation-survival.md`** (`resolve.py:608`, and the `.tsv` open above it), both tracked. It was run from **byte-identical copies** (`sha256 db5e0767…`) in scratch, with the lane root passed as `argv[1]`. The generated-report exclusion is root-relative (`GENERATED_REPORT = "corpus/instruments/citation-survival.md"`, `resolve.py:135`, compared against `os.path.relpath(candidate, repo)` at `resolve.py:311`), so the copy measures exactly the tree named on the command line — the copy changes only *where the census lands*, not what is measured. This is the same scratch-export practice the lane set for itself in `SCORECARD.md:177`. The committed census bytes are unchanged (digest below), and running it in place would have dirtied the lane.

## 3. Run matrix

| # | instrument (digest[:12], lines) | command | exit | key output line |
|---|---|---|---|---|
| 01 | `density.py` `ee803726a322`, 208 | `python3 corpus/instruments/density.py SKILL.md` | 0 | `# Density census — SKILL.md (1104 lines, 26 blocks)` … `**mean dens** … **220.9**`; `Total path-citation instances: 742 across 26 blocks.` |
| 02 | `resolve.py` `db5e0767c60c`, 622 (copy A) | `python3 <scratch>/lane_copy/corpus/instruments/resolve.py /home/vgpnk/Projects/shokunin/kasegi-shokunin` | 0 | `distinct=3059 resolves=32 mirror=0 internal=536 other=0 gone=2491 skill=83/589 corpus=538/2702 all=568/3059` |
| 03 | `anchorcheck.py` `d0f35f8ccdcf`, 563 | `python3 corpus/instruments/anchorcheck.py SKILL.md` | 0 | `== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |
| 04 | `mirror-containment-check.py` `dddd55496b55` | `python3 corpus/instruments/mirror-containment-check.py` | 0 | `cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=db5e0767… matrix_sha256=d05b1e0c…` |
| 05 | `source-recheck.py` `fd2e01e88c8c`, 415 | `python3 corpus/instruments/source-recheck.py --selftest` | 0 | `selftest cases=10 failures=0` (all ten `SELFTEST … PASS`) |
| 06 | `source-recheck.py` | `… --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | 0 | `S051:sha256 OK` + 18 `S051:Q*` assertion lines all `OK` (`S051:Q9 OK occurrences=2 anchor=77-ok`) |
| 07 | `source-recheck.py` | `… --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | 0 | `S052:sha256 OK` + `S052:Q1..Q5 OK` (`Q4 … anchor=15472-ok`, `Q5 … anchor=19165-ok`) |
| 08 | `capture-binding-check.py` `3d9e5e0ddbaa`, 892 | `python3 corpus/instruments/capture-binding-check.py` | 0 | `AUDIT records=42 with_url=42 with_fetched_utc=4 with_archival=38 snapshot_dirs=11 manifest_dirs=11 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt` / `records=42 bound=42 unbound=0` |
| 09 | `capture-binding-check.py` | `… --selftest` | 0 | `selftest cases=23 failures=0` (incl. `case=summary-only-selftest-rejected … verdict=pass`, `case=complete-selftest-report-accepted … pass`) |
| 10 | `frontier-recheck-count.py` `1be79af60cb5` | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | `PASS F01…F18`; `entries=21 pass=21 exit=0` (last row `PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0`) |
| 11 | `recheck-audit.py` `5d4842da6103` | `python3 corpus/instruments/recheck-audit.py` | 0 | `strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0`; `executes=23 gated=24 broken=0`; `lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; `expect=present expected=47 missing=0 unexpected=0 exit=0` |
| 12 | `recheck-audit.py` | `… --selftest` | 0 | 18 `selftest …` lines, every one ending `ok` (no aggregate line is printed by this instrument) |
| 13 | `kill-rule-check.py` `c279d952cba5` | `python3 corpus/instruments/kill-rule-check.py --scratch <scratch>/tmp` | 0 | `KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0d… bytes=40556 lines=892 floor=19 counter_sha256=c279d952…`; `mutants=3 killed=3 survivors=0 invalid=0`; `gates=7 failed=0`; `controls=4 rejected=4`; `survivors=0` |
| 14 | `kill-rule-check.py` | `… --selftest` | 0 | `selftest cases=3 failures=0` |
| 15 | `r-defect-closure.sh` `809aaf9078a2`, 832 | `bash corpus/instruments/r-defect-closure.sh` | 0 | `closed=9/9 exit=0` (R1–R9 all `open=0`) |
| 16 | `r35-defect-closure.sh` `0ae4b4848b10`, 834 | `bash corpus/instruments/r35-defect-closure.sh` | 0 | `closed=7/7 exit=0` (D1–D7 all `open=0`) |
| 17 | `limb-mutation-check.py` `237fd07cbcb4` | `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json --root <lane>` | 0 | `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` (guards `cases=3 failures=0`) |
| 18 | `r-defect-closure.sh` | `bash corpus/instruments/r-defect-closure.sh --selftest` | 0 | `selftest cases=9 failures=0`; `judge=forged-summary rejected=1` / `short-report rejected=1` / `complete-report accepted=1` |
| 19 | `r35-defect-closure.sh` | `bash corpus/instruments/r35-defect-closure.sh --selftest` | 0 | `selftest cases=7 failures=0`; `control=two-defect closed=5/7 failed=D1,D2 verdict=pass`; judges reject forged summary/baselines/short/fake-suite/fake-plain and accept complete |
| 20 | `capture-source.py` `e1831888d719` | `python3 corpus/instruments/capture-source.py --selftest` | 0 | `selftest normalize=ok deterministic=ok` |
| 21 | `score-gap.py` `57584fda83b8` | `python3 corpus/instruments/score-gap.py --selftest` | 0 | `selftest fields=7 failures=0` (4 `exit2-*` INPUT-UNREADABLE cases rc=2) |
| 22 | `resolve-dispatch-check.py` `acbb687094f0` | `python3 corpus/instruments/resolve-dispatch-check.py` | 0 | `cases=8 pass=8 exit=0`; `resolver=db5e0767… checker=acbb6870…` |
| 23 | `test_resolve.py` `16a6ff281d89` | `python3 corpus/instruments/test_resolve.py` | 0 | `Ran 10 tests in 0.157s` / `OK` |
| 24 | `density.py` (rerun) | same as 01 | 0 | run byte-identical to run 01 (`sha256 e9aa94cd57ba591e` over stdout) |
| 25 | `resolve.py` (copy A) | same as 02 | 0 | fresh census: `citation-survival.md` sha256 `10e8bce8…`, `.tsv` sha256 `27365d4e…` |
| 26 | `resolve.py` (copy B, second tree) | same as 02 | 0 | `.tsv` and `.md` **byte-identical** to copy A → deterministic on fixed bytes |

Instrument and data digests used above (full): `kill-rule-check.py` `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`; `capture-binding-check.py` `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`; `r-defect-closure.sh` `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d`; `r35-defect-closure.sh` `0ae4b4848b10…`; `limb-ledger.json` `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be`; `SKILL.md` `daeff71be4d0ee99…` (1104 lines); `SCORECARD.md` `ed6e931f795c070e…`; `corpus/QUALITY.md` `d4f83bb1206f5084…`; `corpus/source-snapshots/round-26/manifest.json` `33ac33c3caa6d43f…`.

## 4. Multi-part evidence detail

### 4.1 `source-recheck.py`

- Self-test: `selftest cases=10 failures=0`, all ten printed `SELFTEST <case> PASS expected-exit=E observed-exit=E` — including `missing-manifest` (exit 2), `stem-mismatch`, `double-occurrence`, `double-occurrence-anchored`, `double-occurrence-out-of-range`, `double-occurrence-broken`, `quote-absent`.
- Known S rows: **S051** (round-34 capture, `manifest.json` sha-backed) → 19 `OK` lines = `sha256` + Q1–Q18, each with its anchor verdict (`anchor=46-ok`, `52-ok`, `53-ok`, `55-ok`, `74-ok`, `75-ok`, `77-ok`); **S052** (round-35 CISA KEV capture) → `sha256 OK` + Q1–Q5, `anchor=2/3/4/15472/19165-ok`. Exit 0 both.

### 4.2 `capture-binding-check.py` and the one orphan

Plain: `records=42 bound=42 unbound=0`, exit 0. One file in the snapshot tree is bound by declaration rather than by a record: `orphans=1 orphan=S040-live.txt`. Verified benign — `corpus/source-snapshots/round-26/manifest.json` carries a top-level `orphans` entry for it with `row: S040`, `row_url`, `captured_url`, `fetched_utc: 2026-10-25T12:34:27Z` and `sha256 b7f7b55ff3fc…`; per the instrument's rule A2 a declared orphan is listed and keeps exit 0 (`capture-binding-check.py:20-25`). Selftest `cases=23 failures=0` matches the round-34 registry correction (`cases=23`).

### 4.3 `kill-rule-check.py` — do not read `mutant=fail` as red

`mutant-probe … pristine=pass mutant=fail` is the *desired* verdict for a killed mutant; the summary is what judges: `mutants=3 killed=3 survivors=0 invalid=0`, `gates=7 failed=0`, `controls=4 rejected=4`, `survivors=0`, exit 0. The header re-pins the instrument under test at `sha256=3d9e5e0d… bytes=40556 lines=892 floor=19`, matching the `SKILL.md` round-34 correction and the live `sha256sum`.

### 4.4 Closure suites — per-check payloads (live reads)

`r-defect-closure.sh` (round-33 R1–R9), `closed=9/9 exit=0`:

```
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
```

`r35-defect-closure.sh` (round-34 D1–D7), `closed=7/7 exit=0`:

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=4 open=0
D2 check=erratum-row=1,erratum-mean=6,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
```

`D4` needs git context (`git ls-files`), so the plain run was executed in the lane worktree — the only place it can be measured honestly; the directory is untouched and both suites are export-compatible via `--root`.

### 4.5 `limb-mutation-check.py`

`limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`, guards `cases=3 failures=0`, exit 0. All nine `RA-*` limbs, the three `SR-*` and the two `FR-*` revert to `verdict=killed`; `CTL-noop`→`invalid:noop`, `CTL-nocompile`→`invalid:nocompile`, `CTL-equivalent`→`survivor`, each as expected. Ledger digest `c042adf6…` equals the `SKILL.md` round-31 pin.

### 4.6 `recheck-audit.py`

`lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`, `strict pass=47/47`, `executes=23 gated=24 broken=0`, and the expected-list check `expected=47 missing=0 unexpected=0 exit=0` against the committed receipt index.

### 4.7 `resolve.py` — live census vs the census of record (stale, structurally)

Fresh run over HEAD (deterministic, copy A ≡ copy B byte-for-byte):

- `distinct=3059 resolves=32 mirror=0 internal=536 other=0 gone=2491`
- `SKILL.md alone: 83/589 = 14.09%`; `corpus alone: 538/2702 = 19.91%`; `lane total: 568/3059 = 18.57%`
- scope line `SKILL.md + corpus/**/*.md` — 151 files contribute at least one path-like citation (of 159 corpus `.md` + `SKILL.md` scanned; the generated census is excluded by `resolve.py:135`).

Committed census of record (`corpus/instruments/citation-survival.md`, `.tsv`, unchanged by me): `SKILL.md alone: 32/506 = 6.32%`; `corpus alone: 118/1153 = 10.23%`; `lane total: 134/1480 = 9.05%`; scope `(50 files)`. Its last regeneration is `644ed37` (round-20, 2026-10-14), and `git ls-tree` at that commit shows 50 corpus `.md` files against 160 today. See §6.1.

### 4.8 `density.py` — independent reproduction of the scored row

`# Density census — SKILL.md (1104 lines, 26 blocks)`, `mean dens 220.9`, `742` path-citation instances, block 26 (round-35 Gates & probes addition) `712.5`. This is exactly the triple `SCORECARD.md:1314` records for the landed tree (`mean 220.9 / 26 blocks / 742 cites`, `SKILL.md daeff71b…`), on the same blob, with the same instrument (`ee803726…`). Two runs byte-identical. So the round-35 no-harm guard row is not just asserted — a second, independent measurement reproduces it.

## 5. Base-state cells the frozen claims must move (fail-before anchors, recorded)

Measured on HEAD `b47f2cd…` before any round-36 landing — the parent can use these as the "before" side of C1/C2:

| cell | base reading | command |
|---|---|---|
| `corpus/instruments/r36-closure.sh` | **absent** (`ls` → no such file) | `ls corpus/instruments/r36-closure.sh` |
| `SKILL.md` registry, exact basename `r36-closure` | **0** | `grep -c r36-closure SKILL.md` |
| `SKILL.md` registry, exact basename `r35-defect-closure` | **0** | `grep -c r35-defect-closure SKILL.md` |
| `grep -c r-defect-closure SKILL.md` / `kill-rule-check` | 4 / 4 | same |
| Frontier harness | `entries=21 pass=21 exit=0` (F01–F18; no F19) | `python3 corpus/instruments/frontier-recheck-count.py` |
| `corpus/knowledge/*.md` | **47** | `ls corpus/knowledge/*.md \| wc -l` |
| `corpus/SOURCES.md` registry | **52** rows, `S053` → 0 | `grep -cE '^\| S0[0-9]{2} ' corpus/SOURCES.md` |
| `corpus/source-snapshots/round-36/` | **absent** | `ls -d corpus/source-snapshots/round-36` |
| `.ufo/waves/round-36/c2-controls/` | `before.txt` only (no `junk-f19.md`) | `ls .ufo/waves/round-36/c2-controls/` |
| captures bound | `records=42 bound=42 unbound=0` (S051 + S052 already landed) | `capture-binding-check.py` |

So at base the C1 E3 target (both registry rows + the `r36-closure.sh` file) and the C2 F19 cell (`entries=22`, `S053`, knowledge 48) are exactly as the frozen claims describe them *before* landing — nothing has pre-landed half of either claim, and nothing already landed contradicts them.

## 6. Observations and risks

### 6.1 The census of record is stale by ~16 rounds (not a red gate, but do not quote it as current)

`resolve.py` regenerates `corpus/instruments/citation-survival.tsv`/`.md` **in place inside the lane**, so nobody runs it during a round (it would rewrite two tracked files); its committed snapshot is round-20 bytes with a 50-file scope. Consequences measured here:

- Committed file says `SKILL.md 32/506 = 6.32%`, `lane 134/1480 = 9.05%`.
- The same instrument on HEAD says `SKILL.md 83/589 = 14.09%`, `lane 568/3059 = 18.57%` (deterministic across two independent copies).

Why it is not a defect now: no round-36 cell claims a current census rate. `SCORECARD.md`'s `depth:verifiability` rates are explicitly round-15/19 historical entries (`SCORECARD.md:66,103`) and the round-31 registry row quotes the same `32/506` snapshot; the round-36 C1 claim is the closure suite, which does not read the census. Why it still matters: the phrase "census of record" invites a judge to read those bytes as current. The lane's own remedy is already written down (`SCORECARD.md:177`: run `resolve.py` in pre/post scratch exports and diff) — which is what §4.7 did. Refreshing the tracked file is outside this seat's write scope and would be a scored move, not a no-harm one.

### 6.2 Older pinned counts in the registry rows have drifted (growth, not regression)

Older rows quote "measured at append time" values that the tree has since outgrown: `anchorcheck.py SKILL.md` now reads **16** in-range / 0 bad (the `score-gap.py` row quotes 7), `recheck-audit.py` now reads `lines=47` (round-31 row: 44), `frontier-recheck-count.py` `entries=21` (round-30 row: 18). Every one of these rows is phrased as an append-time measurement, none claims currency, and every gate is green at the new value — so this is drift, not failure. It is recorded because a verifier diffing row text against live output will see it.

### 6.3 `mutant=fail` in `kill-rule-check.py` is the passing verdict

A verifier grepping for `fail` in the kill-rule transcript gets hits by design (a killed mutant must change its exit/observation). The summary is authoritative: `survivors=0`, `gates=7 failed=0`.

### 6.4 `resolve.py` cannot be run in place without dirtying the lane

Recorded so no later seat "fixes" the census by running it in the worktree: the instrument opens its own directory's `.tsv`/`.md` for writing. Any future "refresh the census" move must either be a scored, L1-approved byte change or a scratch-copy run; the copy is otherwise measurement-identical (root-relative exclusion, `resolve.py:135,311`).

### 6.5 E9-adjacent note (not mine to fix)

`git status --porcelain` is **9 untracked** entries under `.ufo/waves/round-36/` while the wave is in flight (wave scaffolding, spec files, `wave1/`). My receipt adds no new top-level entry — it lands inside the already-untracked `wave1/`. The final quiescence reading for E9 is the parent's post-integration measurement, not this baseline.

## 7. Re-verify (exact, from the lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/{density.py,resolve.py,anchorcheck.py,mirror-containment-check.py,source-recheck.py,capture-binding-check.py,frontier-recheck-count.py,recheck-audit.py,kill-rule-check.py,r-defect-closure.sh,r35-defect-closure.sh,limb-mutation-check.py,limb-ledger.json}
python3 corpus/instruments/density.py SKILL.md                    # mean 220.9, 26 blocks, 742
python3 corpus/instruments/anchorcheck.py SKILL.md               # 16 in-range, 0 bad, exit 0
python3 corpus/instruments/mirror-containment-check.py           # cases=24 pass=24
python3 corpus/instruments/source-recheck.py --selftest          # cases=10 failures=0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
python3 corpus/instruments/capture-binding-check.py              # records=42 bound=42 unbound=0
python3 corpus/instruments/capture-binding-check.py --selftest   # cases=23 failures=0
python3 corpus/instruments/frontier-recheck-count.py             # entries=21 pass=21 exit=0
python3 corpus/instruments/recheck-audit.py                      # lines=47 pass=47 exit=0
python3 corpus/instruments/kill-rule-check.py                    # survivors=0, gates=7 failed=0
bash corpus/instruments/r-defect-closure.sh                      # closed=9/9 exit=0
bash corpus/instruments/r35-defect-closure.sh                    # closed=7/7 exit=0
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json   # limbs=13 killed=13
# resolve.py: run a COPY, not the lane's own file (see §6.4)
```

Expected values for every line are in §3/§4. All runs used stdlib Python 3.14.8 and bash 5.3.20; no network access was needed except none — every instrument here is local-bytes only.

## 8. What I did not do (scope)

- No lane bytes edited (verified: zero tracked modifications before/after; `SKILL.md`, `SCORECARD.md`, `QUALITY.md`, `corpus/instruments/*`, `corpus/SOURCES.md` all untouched).
- No frozen claim scored, no defect routed, no C1/C2 cell authored — this receipt is the no-harm baseline and the fail-before side only.
- No git mutation, no commit/add/stash/checkout, no `pacman`, no installs.
- Scratch dir `/fast/scratch/hyaku/kasegi-r36/ExecInstrumentsSynopsis` removed after this receipt was written (full transcripts existed only there; every line that matters is quoted above).
