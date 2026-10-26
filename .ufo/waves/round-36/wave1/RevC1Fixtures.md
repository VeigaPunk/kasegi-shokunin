# RevC1Fixtures — review of ExecC1Fixtures' red/green fixture matrix (round 36, wave 1)

Seat: reviewer, leaf (no subagents used). Axis under judgment: depth:verifiability.
Subject: the fixture matrix built by ExecC1Fixtures for the draft C1 suite
`r36-closure.sh` (checks E1–E9), per my item: one-limb isolation, red fails only
its own check, green passes, no shared mutation, counts per check, plus two
fixtures reproduced by me.

**Verdict: matrix HOLDS.** Every dimension of my item verified by my own runs in
my own scratch, independent of the executor's saved outputs. One sha discrepancy
found and resolved (§5); residual risks are boundary notes, none rise to a
fixture defect (§6).

## 1. Byte chain

ExecC1Fixtures' scratch was copied to my scratch at 12:46:29, before their
12:47:54 receipt and their yield cleanup. sha256 of my copies vs their receipt §1:

| script | my copy | receipt | match |
|---|---|---|---|
| r36-closure.sh | `4283a9d3eae8…` | `4283a9d3eae8…` | yes |
| r36-fixture-gen.py | `20de0cb39b2d…` | `474a27eef6d8…` | **no — resolved** |
| matrix.py | `2e640fcf6dff…` | `2e640fcf6dff…` | yes |
| clause.py | `4cb8ac3fbfea…` | `4cb8ac3fbfea…` | yes |
| suitemut.py | `2def666d6f01…` | `2def666d6f01…` | yes |

The generator was edited between my copy and their receipt. The receipt embeds
the final generator verbatim (Appendix); I extracted and hashed the embedded
copy: `474a27eef6d8…` exactly as claimed. `diff` my copy vs embedded: **1 line,
a docstring usage line (`mutate DEST NAME BASE`) — zero behavioral change**, so
every result below, run on my copy, holds byte-for-byte for the final generator.
Fixture base `src` is a pruned b47f2cd export: I rebuilt the full
`git archive b47f2cd` extraction and diffed — all shared files byte-identical,
their tree only omits paths no check reads (the provenance note and round-36
lesson are absent from src on purpose; `normalise()` authors them).

## 2. Full matrix — my rerun (fresh fixtures rebuilt from src by matrix.py in my scratch)

```
green closed=9/9 exit=0 opens=none
E1..E9 red_exit=1 green_exit=0 closed=8/9 own_open=1 others_open=none  (9/9 rows pass)
E4b red_exit=1 target=E4 own_open=1 others_open=none
E9b red_exit=1 target=E9 own_open=1 others_open=none
export 3266c993 (r35 base)    closed=0/9 exit=1
export 0aee0ef  (r35 judged)  closed=4/9 exit=1
export b47f2cd  (freeze)      closed=5/9 exit=1
matrix rows=9 failures=0
```

Matches receipt §3 row for row. Counts per check: every red tree reads exactly
`closed=8/9` with its own check open and the other eight closed — red fixtures
fail only their own check; green passes 9/9 exit 0.

## 3. One-limb isolation — delta audit (red worktrees vs green, and git-level)

| fixture | delta vs green | check-only? |
|---|---|---|
| red-E1 | SCORECARD.md, 4 lines (987,988,1130,1409): bound hash → `filled by the L1…` inside Final-lane-commit blocks | yes |
| red-E2 | SCORECARD.md, 1 line (1246): erratum wording `depth:density`→`depth density` | yes |
| red-E3 | SKILL.md only: `| r35-defect-closure.sh` registry row removed (payload `row_r35=0 row_r36=1`) | yes |
| red-E4 | provenance note file removed; results.json still tracked | yes |
| red-E5 | `.ufo/waves/round-35/claims-erratum-d5.md` removed | yes |
| red-E6 | L1Integration.md only: `Correction (round 35)`→`(round 34)` | yes |
| red-E7 | QUALITY.md, 1 line (249): `supersedes R22 —`→`R22 citation unchanged —` | yes |
| red-E8 | `corpus/lessons/round-36.md` removed (stray path `.ufo/waves/round-36/wave1/stray.md` cannot collide: different tree) | yes |
| red-E9 | only adds untracked `.ufo/waves/round-36/` (`?? ` status line; worktree otherwise identical) | yes |
| red-E4b | worktree byte-identical; index-only drop (`rm --cached` + `.git/info/exclude`): `ls-files` results.json=0, provenance=1, `status --porcelain`=0 | yes |
| red-E9b | worktree byte-identical; defect lives in the scratch root (stray seat dir) | yes |

**No shared mutation:** the only file two reds share is SCORECARD.md (E1, E2);
their changed line sets are disjoint (987/988/1130/1409 vs 1246) and each red
leaves the sibling check closed (E1 `open=0` on red-E2, E2 `open=0` on red-E1 —
observed in both their saved runs and my rerun). All other reds touch files no
other check reads.

Clause coverage is complete across red + mutants (14 mutants, my rerun of
clause.py: `clause cases=14 failures=0`, each opening only its own check):
E1 4/4 clauses (E1a prose, E1b token, E1c object-absent, E1d orphan-not-ancestor),
E2 2/2 (red-E2 row, E2b mean), E3 2/2 + mention-control E3c (both rows gone,
basenames in prose → still open, so the row anchor is not mention-satisfiable),
E4 2/2 (red-E4 provenance, red-E4b tracked), E5 3/3, E6 2/2, E7 2/2 (red-E7 R22,
E7b R23), E8 3/3 + red-E8 (lesson absent), E9 2/2 (red-E9 dirty, red-E9b leftover).
Non-vacuity is over-determined: green control + own/others-open accounting +
14 clause kills + 3 suite mutants + forged-summary rejection (suite mutants and
cross-run are receipt §5/§6; I did not rerun those two drivers — see §6 R3).

## 4. Two fixtures reproduced by hand (my item's reproduction duty)

Built fresh in my scratch from `python3 r36-fixture-gen.py green src my-green`
(HEAD=`0ef3a50a…`, BASE=`d540b7cf…`), then hand-applied the documented deltas
with sed and committed inside fixtures whose `rev-parse --show-toplevel` I
verified equal to the fixture dir. Suite run with `--root X --gitroot X` and
`KASEGI_R36_SCRATCH` pointed at my empty dir:

- **my-red-E2** (erratum wording, my own commit): `E2 check=erratum_rows=0 … open=1`,
  all others `open=0`, `closed=8/9 exit=1`. E1 stays closed on the same file.
- **my-red-E7** (`supersedes R22` → `R22 citation unchanged`): `E7 check=supersedes_R22=0
  supersedes_R23=1 … open=1`, all others closed, `closed=8/9 exit=1`.
- **my-green** (same generator, no delta): `closed=9/9 exit=0`.

Both reproductions agree with the claimed matrix rows (red_exit=1, green_exit=0,
own check only).

## 5. Findings

1. **[resolved] Generator sha in receipt §1 vs bytes I copied** — see §1. The
   receipt is honest: its embedded verbatim copy hashes to the claimed
   `474a27ee…`; my earlier copy differs by one docstring line only. No action.
2. **[strength] E1c/E1d are genuinely two-sided** — nonexistent object
   (`hash_exists=0`) vs orphan commit (`exists=1 ancestor=0`) discriminate the
   existence and ancestry limbs of the E1 hash binding separately.
3. **[strength] red-E4b isolates "tracked" with a clean worktree** — index-only
   mutation via `info/exclude` proves the E4 tracking limb without dirtiness
   leaking into E9.
4. **[strength] Fixture epistemics are correct** — the green fixture's registry
   rows, round-36 lesson and provenance note are fixture-authored (receipt §2
   says so explicitly); the fixtures prove the checks discriminate, not that
   round 36 landed. No fixture output is presented as lane evidence.

## 6. Residual risk and verification gaps

- **R1 (boundary, by design):** E9 in `--export-ref` mode reads the live lane
  worktree and the real `/fast/scratch/hyaku/kasegi-r36` root, so export runs
  are not hermetic; the frozen counting command inherits this. The receipt
  discloses it; the frozen clause ("porcelain empty now") can only close at
  filing. Not a fixture defect.
- **R2 (reading note):** red-E1 opens two E1 clauses at once (placeholder tokens
  and hash binding). The isolation claim is per limb/check and holds; per-clause
  attribution is supplied by mut-E1a…E1d. Similarly E3c opens both E3 rows by
  construction (mention control).
- **R3 (not rerun by me):** suitemut.py (suite can fail, 4/4) and cross.py
  (fixtures against ExecC1SuiteBuild's landing suite, incl. the disclosed E8b/E8d
  survivors at `76273416…` and beyond-frozen-wording residuals E5b/E5c/E6b). Out
  of my item's dimensions; recorded here so the main agent knows those numbers
  rest on the executor's runs, not mine. The E8b/E8d survivor disclosure is
  relevant to C1 suite review (RevC1Suite's lane), not to this matrix.
- **R4 (ephemerality):** fixture trees and drivers lived only in scratch
  (removed at yield). The receipt embeds the generator verbatim + driver
  contracts + per-fixture run commands; matrix.py/clause.py/suitemut.py shas are
  recorded but sources are not embedded (declared rewritable "in minutes"). My
  review reproduced everything from the pre-cleanup copy, so the recorded
  behavior is real; a third party rebuilding drivers from the contracts should
  re-hash against §1.
- **R5:** I did not rerun the export-mode controls beyond what matrix.py's tail
  does (they ran as part of my §2 rerun: 0/9, 4/9, 5/9 all reproduced).

## 7. Provenance

- All runs in `/fast/scratch/hyaku/kasegi-r36/RevC1Fixtures/` (removed after
  receipt). No lane-repo writes except this receipt. Read-only git only
  (archive/diff/ls-files/status/rev-parse/show-toplevel); mutating git solely
  inside scratch fixture repos with verified toplevels, mirroring the suite's
  own selftest pattern.
- Tools installed: none (python3/bash/git sufficient). pacman untouched.
- Cross-checked artifacts: ExecC1Fixtures.md §1–§5, their out-*.txt (pre-cleanup),
  `git archive b47f2cd` equivalence check for `src`.
