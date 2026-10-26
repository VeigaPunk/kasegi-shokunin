# MutC1Fixtures — round-37 wave1 receipt (mutation validation of the planned E1–E14 fixtures)

- **Seat:** MutC1Fixtures (leaf, mutation-tester) · **Round:** kasegi-shokunin 37, hyaku run 9 · **Date:** 2026-10-26
- **Item:** validate that the planned E1–E14 fixtures of `corpus/instruments/r37-closure.sh` are **minimal and discriminating**: for each fixture, remove the one defect it introduces and show the check then PASSES (fixture load-bearing); show a non-minimal fixture (defect + unrelated change) is unnecessary.
- **Headline verdict: VALIDATED — 226/226 cases PASS.** Every one of the fourteen checks rejects its defect fixture with the named limb, passes when that single defect is removed (bytes restored, sha-verified), and is indifferent to unrelated changes in both directions. No fixture needs a non-minimal form.

## Method

Mid-run the suite **landed** (F0 integration `0acffc8`, F0b fix `a4b6a8c`), so the validation was upgraded from scratch mirror prototypes to the **real committed suite** (`mirrorR` = byte-identical copy; sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`). A preliminary run against scratch mirrors of the r36 suite (`mirrorA`, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`) was kept as secondary evidence for the E9 fail-open comparison (spot-check D6).

- **Green tree:** pristine `git archive` extract of `a4b6a8ca0c3ad83c4f01bd47ea2afe2ed989df23` (the head at validation time), copied once into a worktree; every case mutates it **in place** and restores the exact prior bytes (sha-verified against a per-file hash map of the extract).
- **Fixture lanes:** `FX` = mktemp git repo carrying full lane history, `reset --hard` to `a4b6a8c…` (toplevel verified = repo root); `FX2` = FX + a committed `all-gates v1` receipt built from this run's own live check lines (HEAD `acd1f35df0bd8c7c496189244a5cd0b332ff70a7`). All git-scoped limbs (E1 binding, E4 ls-tree/ls-files, E10 ancestor/digest) resolve inside the fixture lane — fully isolated from the live lane.
- **Case protocol per fixture:** (a) verbatim replay of the suite's own selftest mutant → must REJECT with the fixture's limb; (b) the same defect as a minimal single-clause mutation of the green tree → must REJECT; (c) exact revert of that defect → must PASS; (d) reverted + unrelated change → must PASS, and defect + unrelated change → must REJECT.
- All scratch under `/fast/scratch/hyaku/kasegi-r37/MutC1Fixtures/` (removed before this receipt was filed); the lane repo was only read.

## Baselines (whole-suite runs, actual output)

| Run | Command shape | Result |
|---|---|---|
| selftest on FX2 | `r37-closure.sh --selftest --lane FX2` | `selftest cases=14 failures=0`, `judge=own-report accepted=1`, rc=0 |
| suite on FX2 (receipt committed) | `--lane FX2 --export-ref HEAD` | `closed=14/14 exit=0`, rc=0 |
| suite on FX (no receipt) | `--lane FX --export-ref HEAD` | `closed=13/14 exit=1` — only `E10 closed=0` |
| suite on r36 base | `--export-ref cc692008b…` (live lane) | `closed=4/14 exit=1`; red: E1,E3,E4,E8,E9,E10,E11,E12,E13,E14; green: E2,E5,E6,E7 |
| suite on r36 judged head | `--export-ref a23dc4788…` (live lane) | `closed=7/14 exit=1`; red: E1,E9,E10–E14 (E10–E14 open there, as the claim requires); green: E2–E8 |
| suite on FX2 + untracked file | `--lane FX2 --export-ref HEAD` | `closed=13/14 exit=1` — only `E9 closed=0` (`status-dirty=1`); restored → `closed=14/14 exit=0` |
| r36-mirror controls | `r36-closure.sh` on FX pristine / dirty / live-lane refs | `closed=9/9 exit=0` (pristine), `8/9` (dirty), `8/9` (a23dc43 live: E9 live-red), `4/9` (cc69200); `--selftest` → `cases=9 failures=0` both mirrors |

## Per-fixture evidence

Every row: expected verdict → **actual** rc + payload (trimmed). "revert" = the same defect applied then exactly restored (sha-verified) before the check runs. "-unrel" rows add an unrelated file (`notes/unrelated.txt`) or unrelated line on top.

### E1 — structural placeholder/hash binding (20/20)
| Fixture | Defect removed for the green case | Expected → Actual |
|---|---|---|
| v-placeholder / v-lanehash / v-unbound / v-history (suite's own selftest mutants, replayed) | — | RED `placeholders=1` / `lane-hash-markers=1` / `bound=0` / `round37-section=0` — all rc=1, needles present |
| d-placeholder | drop the `filled by the L1` line | RED rc=1 `placeholders=1,…,round37-final-lane-commits=1,bound=1` → revert GREEN rc=0 `placeholders=0,…` |
| d-lanehash | drop the `<LANE_HASH>` line | RED rc=1 `lane-hash-markers=1` → revert GREEN rc=0 `lane-hash-markers=0` |
| d-unbound | restore the bound hash `f3246559…` | RED rc=1 `round37-final-lane-commits=1,bound=0` → revert GREEN rc=0 `bound=1` |
| d-nosection | restore the `## Round 37 result` heading | RED rc=1 `round37-section=0` → revert GREEN rc=0 `round37-section=1` |
| all four × -unrel | — | defect+unrelated still RED (needles unchanged); reverted+unrelated still GREEN |

### E2 — round-34 depth:density erratum (11/11)
- v-stale-mean RED `erratum-mean=0`; v-prose RED `erratum-row=0`; v-marker-only RED `erratum-row=0` (all rc=1).
- d-row (mean `201.2`→`201.9` in the erratum row): RED rc=1 `erratum-marker=1,erratum-row=0,erratum-mean=7` → revert GREEN rc=0 `erratum-row=1,erratum-mean=7`.
- d-marker (delete the `Erratum (round 35)` line): RED rc=1 `erratum-marker=0,erratum-row=1` → revert GREEN rc=0 `erratum-marker=1`.
- ±unrelated: verdicts unchanged in both directions.

### E3 — SKILL.md registry exact-basename rows (13/13)
- v-r35only / v-r36only / v-inexact / v-mention / v-outside: all RED with `registry-r36-closure=0` or `registry-r35-defect-closure=0` as designed.
- d-del36 (delete both `r36-closure.sh` rows): RED rc=1 `registry-r35-defect-closure=1,registry-r36-closure=0` → revert GREEN rc=0 `registry-r36-closure=2`.
- d-inexact35 (first cell `r35-defect-closure.sh`→`r-defect-closure.sh`): RED rc=1 `registry-r35-defect-closure=0,registry-r36-closure=2` → revert GREEN rc=0.
- ±unrelated: unchanged.

### E4 — round-35 wave1-results.json tracked + provenance note (9/9)
- v-prov-absent RED `tracked-ref=1,tracked-index=1,provenance-note=0`.
- d-delnote (delete the provenance file): RED rc=1 `provenance-note=0` → revert GREEN rc=0 `provenance-note=1` (ref/index limbs stayed 1 throughout — the tree-side clause is the one that flips).
- d-emptynote (0-byte note): RED rc=1 `provenance-note=0` → revert GREEN. ±unrelated: unchanged.

### E5 — claims-erratum-d5.md present (5/5)
- v-absent RED `claims-erratum-d5=0`; d-del RED rc=1 `claims-erratum-d5=0` → revert GREEN rc=0 `claims-erratum-d5=1`. ±unrelated: unchanged.

### E6 — round-34 receipt `Correction (round 35)` (5/5)
- v-correction-absent RED `correction-round35=0`; d-delcor RED rc=1 `path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=0` → revert GREEN rc=0 `correction-round35=1`. ±unrelated: unchanged.

### E7 — QUALITY supersedes-R22/R23 rows (10/10)
- v-r23absent RED `supersedes-r23=0`; v-prose RED `supersedes-r22=0`.
- d-delR23 (delete the R27 row): RED rc=1 `supersedes-r22=1,supersedes-r23=0` → revert GREEN rc=0 `supersedes-r23=1`.
- d-proseify22 (R26 row's third column no longer begins `supersedes R22`): RED rc=1 `supersedes-r22=0,supersedes-r23=1` → revert GREEN. ±unrelated: unchanged.

### E8 — round-36 lesson correction record (20/20)
- v-nom36 / v-stale / v-unnamed / v-nolesson35: RED with `m36-rows=0` / `stale-line=1` / `names-corrected-line=0` / `round35-lesson=0`.
- d-delM36: RED rc=1 `m36-rows=0,names-corrected-line=2,…` → revert GREEN rc=0 `m36-rows=4,names-corrected-line=3`.
- d-unnamed (all `source-recheck` mentions removed from round-36.md): RED rc=1 `names-corrected-line=0` → revert GREEN rc=0 `names-corrected-line=3`.
- d-stale (stale line appended to round-35.md): RED rc=1 `stale-line=1` → revert GREEN rc=0 `stale-line=0`.
- d-nolesson35 (round-35.md deleted): RED rc=1 `round35-lesson=0` → revert GREEN. ±unrelated: unchanged.

### E9 — quiescence, fail-closed (18/18) — the D6 demonstration
On a fixture repo with controlled limbs (clean tree, empty scratch root, HEAD = exported ref):
- **pos-quiescent: GREEN** rc=0 `status-read=ok,status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present` (both the committed r37 code and the r36 code agree on a genuinely clean state).
- **The D6 discriminator — a failing status read** (corrupt `.git/index`; `git status --porcelain` exits non-zero, stderr preserved in the log):
  - r36 code (committed `r36-closure.sh`): **rc=0, `status-dirty=0`** — the fail-open `${porcelain:-0}` default treats the failed read as clean. This is the false pass D6 routed.
  - r37 code: **rc=1, `status-read=failed,status-dirty=?,…`** — red, dirty count printed as `?`, never 0. Removing the one defect (the `:-0` default) is exactly what makes the limb discriminate; the positive limb still passes on clean bytes.
- Per-limb fixtures, each red until its single violation is removed: dirty worktree (`status-dirty=1` → green after removal), leftover seat dir (`scratch-seat-dirs=1` → green), stale head (`head-match=0` with want=000…0 → green with want=HEAD), enclosing repo (`lane-root=0` for srepo=FX/sub → green for srepo=FX). The r36 code rejects all four identically — the rewrite changed only the status limb.
- Non-minimal controls: a stray **file** (not dir) in the scratch root → still GREEN (the seat limb is dir-scoped); corrupt index + leftover dir together → RED (each limb independently sufficient; the combined fixture is unnecessary).
- End-to-end: FX2 + untracked file → suite `closed=13/14 exit=1` with only `E9 closed=0`; file removed → `closed=14/14 exit=0`.

### E10 — all-gates receipt binding (34/34)
Live lines were harvested from this run's own 13 non-E10 checks over the green tree (all `closed=1`) plus a synthesized E10 line; receipts were built with the suite's `mk_gates` knob semantics. The **green receipt** passes every limb: rc=0 `all-gates=1,suite-file=1,header=1,ancestor=1,digest-match=1,run-lines=14,recorded-closed=1,selftest-cases=14,selftest-summary=1,crossrun=1,placeholders=0`. Each knob fixture is red on exactly its limb and green once that one defect is removed (the shared well-formed receipt):
| Knob fixture | Limb that fires (actual) |
|---|---|
| receipt absent | `all-gates=0` |
| digest = 64 zeros (wrong suite version) | `digest-match=0` |
| export-ref = 40 zeros | `ancestor=0` |
| run-utc invalid / sentinel missing / extra header line | `header=0` |
| run block drop:E13 / dup E9 / all-open | `run-lines=13` / `run-lines=13` / `run-lines=0` |
| closed=13/14 line | `recorded-closed=0` |
| selftest case drop:E13 / failpos / mutants=0/0 | `selftest-cases=13` / `13` / `0` |
| summary `failures=1` | `selftest-summary=0` |
| E9 payload key drift (`extra-key=1`) | `crossrun=0` — a receipt whose recorded payload *shape* differs from the live run is red even with a correct digest |
| `# TODO` placeholder line | `placeholders=1` |
All knobs ±unrelated: unchanged. The crossrun limb is what stops a hand-edited or stale-version receipt from satisfying E10 by shape alone.

### E11 — LOG.md round-37 named correction of the false `r36-fixtures/` path (20/20)
- v-none / v-nocorrection / v-nopath / v-nofalsity (suite's own fixtures): RED with `log37-block=0` / `correction-marker=0` / `false-path-named=0` / `falsity-stated=0`.
- Minimal defects on the green tree, each red until reverted: marker renamed (`Correction (round 37)`→`Correction (round 36 record)`) → `correction-marker=0`; path redacted block-wide → `false-path-named=0`; falsity wording mangled block-wide → `falsity-stated=0`; whole round-37 block deleted → `log37-block=0`. Every revert → GREEN rc=0 (`log37-block=1,correction-marker=1,false-path-named=1,falsity-stated=3`). ±unrelated: unchanged.

### E12 — anchor-ancestor labeling, stale label absent (26/26)
- v-nosection / v-noanchor / v-nohash / v-stale / v-nolesson / v-lesson-unbound (suite's own fixtures): RED with `scorecard37-section=0` / `anchor-ancestor=0` / `c20300df=0` / `stale-e666d902=1` / `lesson37=0` / `lesson-c20300df=0`.
- Minimal defects on the green tree, each red until reverted: `Anchor ancestor` phrase removed from the round-37 SCORECARD section → `anchor-ancestor=0`; `c20300df` redacted from the section → `c20300df=0`; stale `Final lane commit: e666d902…` appended inside the round-37 section → `stale-e666d902=1`; round-37 lesson deleted → `lesson37=0`; lesson's `c20300df` mentions redacted → `lesson-c20300df=0`. Every revert → GREEN rc=0 (`scorecard37-section=1,c20300df=1,anchor-ancestor=1,stale-e666d902=0,lesson37=1,lesson-c20300df=5,lesson-anchor-ancestor=2`). ±unrelated: unchanged.

### E13 — registry row type cell + exit-2 verdict, same row (13/13)
- v-type-cell / v-verdict / v-outside / v-split (suite's own fixtures): RED with `single-choice-type=0` / `exit2-verdict=0` / `registry-rows=0` / `exit2-verdict=0` (the split fixture proves both clauses must hold on the SAME row).
- **Control (not a mutant): the append-only correction shape — old `gate\|probe` row kept + corrected row appended — is ACCEPTED** rc=0 `registry-rows=2,single-choice-type=1,exit2-verdict=1`. The check does not criminalize the historical row.
- Minimal defects on the green tree's corrected row: type cell back to `gate\|probe` → RED `single-choice-type=0`; ` \| 2 could-not-evaluate` removed from the verdict cell → RED `exit2-verdict=0`. Reverts → GREEN. ±unrelated: unchanged.

### E14 — fail-closed quiescence shape of the suite bytes (15/15)
- v-default / v-swallow / v-nomarker (suite's own synthetic suite-files): RED with `porcelain-default=1` / `status-read-swallow=1` / `fail-closed-marker=0`.
- Minimal defects on the real suite bytes, each red until reverted: a `porcelain:-0` defaulting line appended → RED rc=1 `porcelain-default=1,status-read-swallow=0,status-read-sites=10,fail-closed-marker=8`; a `status --porcelain 2>/dev/null` swallow line appended → RED `status-read-swallow=1`; the `status-read=failed` marker removed → RED `fail-closed-marker=0`. Reverts → GREEN rc=0 (`porcelain-default=0,status-read-swallow=0,…,fail-closed-marker=8`). ±unrelated: unchanged. Note E14 requires the fail-closed marker to be PRESENT — absence of the defect shapes alone is not green.

## Non-minimal fixtures are unnecessary

For every check: the minimal single-defect mutation of the green tree already rejects (so no extra content is needed to trip the check), and the reverted state plus an unrelated change still passes (so no extra content is needed to keep it honest). The defect+unrelated variants reject identically to the minimal ones — the unrelated element never rescues, substitutes, or strengthens a fixture. Fourteen of fourteen planned fixture sets are minimal and discriminating.

## Restoration and integrity evidence

- Worktree: after 219 mutation cases, byte-identical to the `a4b6a8c…` extract (0 drifted files, 0 extra files; per-file sha map).
- Fixture lanes: FX worktree clean, HEAD restored, `.git/index` restored (sha256 match with the pre-corruption snapshot); FX2 clean, HEAD `acd1f35d…` unchanged after the E9 flip runs.
- Mirrors: `mirrorR` and `mirrorA` sha256 unchanged through the run.
- Lane repo: `git status --porcelain` + HEAD identical before/after the whole run (delta empty); `corpus/instruments/r37-closure.sh` and `r36-closure.sh` on disk still equal their HEAD blobs. The lane's HEAD moved during the seat's lifetime (F0 integration landed mid-run) — environmental, not from this seat; this seat wrote nothing outside its scratch dir and this receipt.
- One known state note: the run summary's `FX_head_restored=false` is the intended final state (FX's HEAD is the receipt commit `acd1f35d…` because FX2 == FX by construction), not drift.

## Findings for the suite owner

1. All fourteen checks' fixture sets are load-bearing and discriminating; no fixture can pass while its defect is present (the C1 kill-rule clause is safe).
2. E1 nuance worth knowing: `e1_final_hashes` collects every 40-hex token within the four lines after each `Final lane commit` line. At the a23dc43 judged head the round-36 window binds two tokens (`e666d902…`, `274fa9ae…`), so an unbound-hash fixture there flips `bound` 2→1 (still red); at the round-37 tree the window binds exactly one (`f3246559…`) and flips 1→0. Both discriminate; the `bound == total` clause is the discriminator.
3. E10's crossrun limb (recorded payload key sets == live run key sets) is what defeats a stale-version or hand-edited receipt even with a correct digest — keep it in any future suite revision.
4. E13's same-row clause plus the appended-correction control is the right pair: it rejects clause-splitting while accepting the append-only fix shape actually used in SKILL.md.
5. E14's positive limb requires the `status-read=failed` marker to be present in the suite bytes — a future refactor that renames that marker must update E14 with it.

## Tooling

No tools were installed or upgraded (bash, python3, git only). No pacman, no uv, no network installs.

## Artifacts

Raw per-case records (226 rows: `results2.tsv`) and suite logs lived under the seat scratch dir and were removed with it after this receipt was filed; every load-bearing payload is quoted above. Scratch dir `/fast/scratch/hyaku/kasegi-r37/MutC1Fixtures/` removed before filing.
