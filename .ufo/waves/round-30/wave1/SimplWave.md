# SimplWave — round-30 wave-1 YAGNI / exclusion pass (kasegi-shokunin)

Seat: `SimplWave` (L2 simplifier, leaf; no subagent dispatch). Lane: `kasegi-shokunin`.
Measured: 2026-10-25, working tree at lane tip (round-30 wave in flight). No tool installed;
no git/jj mutation; no network contact (local byte checks only).

Bytes pinned for this report (sha256):
- `corpus/instruments/frontier-recheck-count.py` = `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`
- `corpus/instruments/source-recheck.py` = `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`
- `corpus/source-snapshots/round-30/manifest.json` = `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6`
- F14 entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` = `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32`
- Freeze commit `3c557354…`: `c1-controls/q9/manifest-b1.json`=`d2e09c89…`, `manifest-b2.json`=`3a13e5c3…` (working tree byte-identical at final measurement).

## 1. What the final commit must keep (preserved contract)

Claim/fixture contract — nothing in this set may be excluded:
- `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`, `claims.json` (committed at freeze; C1 do-nothing control cites `before.txt`).
- C1 counter fixtures (committed at freeze): `c1-controls/harness-root-a1/`, `harness-root-a2/`, `c1-controls/q9/manifest-b1.json`, `manifest-b2.json`, `B2.txt`, `S045.txt` — all four C1 `counter_commands` and `post-commit-recheck.sh` (lines 26–29) reference exactly these paths.
- C2 production assets (already in corpus, outside wave dirs): F14 entry, `corpus/source-snapshots/round-30/{S046,S047,S041}.txt` + `manifest.json`, SOURCES rows S046/S047, README F14 row.
- Assimilation mapping files (`assimilation/{collisions,staged-ids,reg-ids,quarantine-slice}`) and `wave1/swarm-registry.json`; `wave1/harness-after.txt`; `wave1/post-commit-recheck.sh`.
- All wave1 seat reports (`*.md`), incl. `ScribeLessonGate.md` / `ScribeMistakes.md` (lesson inputs), `ExecBeforeVerify.md`, `ScoutInstrumentBaseline.md`, `ExecImplFrontierHarness.md`, `ExecImplSourceRecheck.md` + `ExecImplSourceRecheck.diff`, `ExecMutantsC1.md`, `CritC1Kill.md`, `ExecPostCommitRecheck.md`, etc. Round-29 precedent retains the full seat-report set; no lesson draft references anything outside this set.

Cross-check result: **no required path (counter, kill rule, post-commit script, lesson draft) points at any file recommended for exclusion below.**

## 2. Exclusion candidates — wave1/

| Path | Size | Reason | Verdict |
|---|---|---|---|
| `CritC2Kill-lab/` (7 mirrors M0/Mbase-Stub/Mcopy-Dup/Mdecoy/Mfake-Cap/MrowOnly/MrowOnlyB) | 20,486,827 B, 1071 files | **Bulk corpus copy (R14 violation)** — each mirror is a full byte-identical copy of the lane (sample: `M0/…/corpus/SOURCES.md`, `resolve.py`, `lessons/round-29.md`, `source-snapshots/round-24/S032.txt` all equal the real corpus hashes). 70.5% of wave1 bytes. The critic's findings live in `CritC1Kill.md`; mirrors are scratch. | **EXCLUDE** (recreate via `git archive`/tarball if a re-run is ever needed — R14) |
| `CritC1Kill-attack/` | 101,164 B, 31 files | Attack fixture roots (a1/a2/b0/b2iso stubs), `make-mutants.py`, raw outputs — scratch; evidence summarized in `CritC1Kill.md` / `ExecMutantsC1.md`. | **EXCLUDE** |
| `RevEngIntent-scratch/` | 45,065 B, 16 files | Scratch copies of fixture stubs (dup-entry.md, S003.txt 68 B, manifests); findings are in `RevEngIntent.md`. | **EXCLUDE** |
| `ExecImplSourceRecheck-b2/` | 612 B, 3 files | Superseded intermediate B2 manifests/fixtures; final fixtures are `c1-controls/q9/*`. | **EXCLUDE** |
| `ExecImplSourceRecheck.pre.py` | 11,854 B | Stale pre-edit snapshot; sha256 `9fe6a4a0…` = base bytes, byte-identical to `c1-controls/mutants/freeze-source-recheck.py`, retrievable via `git show a94871315:corpus/instruments/source-recheck.py`. | **EXCLUDE** |
| `build-spec.py` | 45,814 B | Dispatch-time generator scaffolding; its outputs (`wave1-spec.json`, `wave1-dispatch.json`) already exist. Round-29 kept its copy at wave root — precedent conflict; generator is dead weight after integration. | **Exclude (optional)** — keep only if L1 wants spec provenance |
| `fetch/` (s037.html, s048.html, s054.pdf, s065.pdf, s065.txt, s068.html) | 8,138,768 B | Quarantine-slice live fetch evidence for verdicts (round-29 retained the equivalent `assimilation/fetch/`). Not corpus copies (R14 n/a). `s065.pdf` alone is 7,465,472 B. | **KEEP per precedent**; optional trim of `s065.pdf` (verdicts remain reproducible by refetch, but URL liveness is the tradeoff) |
| `swarm-registry.json` | 13,339 B | Wave membership/roles map (round-29 kept). | Keep |

## 3. Exclusion candidates — c1-controls/ (wave-added only)

Files committed at freeze (a1.out/a1.err, before.txt, harness-root-*, q9/*) are baseline, not wave outputs — no recommendation.

| Path | Size | Reason | Verdict |
|---|---|---|---|
| `before-run-2.txt` | 2,048 B | Duplicate receipt: same instrument digests and outputs as committed `before.txt` (re-run at freeze bytes); nothing unique (full traceback variant also in `a1.err`). | **EXCLUDE** |
| `mutants/freeze-frontier-recheck-count.py`, `mutants/freeze-source-recheck.py` | ~19 KB | Byte-identical copies of base instruments (`c8a62888…` / `9fe6a4a0…`), already recorded as digests in `before.txt` and in `git show <base>`; `freeze-source-recheck.py` duplicates `ExecImplSourceRecheck.pre.py`. | **EXCLUDE** |
| `mutants/control-a1/a2/b1/b2.{out,err}` | ~1.6 KB | Baseline (do-nothing) probe outputs — content duplicative of `before.txt` + `ScoutInstrumentBaseline.md`; unique only in stream splitting (stdout vs stderr). Round-29 kept `base-control-*` as lesson receipts. | **KEEP (cheap, precedent)** or trim if the lesson cites only `before.txt` |
| `mutants/digest-poll.log` | 278 B | Unique mid-wave drift evidence (base → landed digests, 18:50:10 → 18:50:40Z) — supports the M29-6-class drift narrative. | **KEEP** |

## 4. Observed hazards (not exclusions)

1. **Frozen fixture transiently modified mid-wave.** `c1-controls/q9/manifest-b2.json` deviated from freeze bytes during measurement (`"path": "B2.txt"` → `"S045.txt"`, self-inconsistent: sha256 `55124b0e…` belongs to B2.txt) then returned to freeze-identical bytes. Final working-tree bytes match `3c557354` — but L1 should re-verify before integration and pin the frozen set (edits to frozen fixtures should land as appended corrections, not in-place).
2. **B2 fixture exercises the stem limb, not the occurrence limb.** With the frozen fixture (id S045, path B2.txt) the landed instrument exits 1 `reason=stem-mismatch` first — `reason=occurrence-not-unique` is never reached (quote occurs 2× in B2.txt but is shadowed). Literal kill rule ("B2 exits 1 with a failure reason") passes; the predicate sentence's limb is not independently demonstrated by this fixture. Flag for `RevC1Controls`/lesson.
3. `wave1-dispatch.json` and `run.out` are byte-identical (`6c8f48b1…`) — `run.out` is a pure duplicate log; `plan.out`/`plan.err`/`run.err` are planner/flush logs; `kasegi-r30-build.ready(.dispatched)` are orchestrator markers. All are outside the two scoped dirs; recommend dropping the duplicates/logs at integration (round-29 precedent kept them, but they are pure dispatch scaffolding).

## 5. Bottom line

- Exclude: `CritC2Kill-lab/` (~20.5 MB), `CritC1Kill-attack/`, `RevEngIntent-scratch/`, `ExecImplSourceRecheck-b2/`, `ExecImplSourceRecheck.pre.py`, `c1-controls/before-run-2.txt`, `c1-controls/mutants/freeze-*.py` (~20.7 MB total ≈ 71% of wave1 bytes); optional: `build-spec.py`, `fetch/s065.pdf`, `control-*`, root run/plan logs.
- Keep: all seat reports, committed fixtures, `assimilation/`, `swarm-registry.json`, `digest-poll.log`, `harness-after.txt`, `post-commit-recheck.sh`, `fetch/` (precedent).
- Verified: nothing required by claims C1/C2 counters, kill rules, `post-commit-recheck.sh`, or lesson drafts (`ScribeLessonGate.md`, `ScribeMistakes.md`) is in the exclusion set; no bulk corpus copy remains post-exclusion (lab mirrors are the only byte-identical corpus copies; harness fixtures are purpose-built stubs; `q9/S045.txt` is the single round-29 capture the committed B1 fixture needs).
