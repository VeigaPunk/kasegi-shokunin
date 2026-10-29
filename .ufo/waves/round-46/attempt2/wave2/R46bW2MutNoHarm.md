# R46bW2MutNoHarm — mutation test of noharm.sh (round 46, attempt 2, wave 2)

VERDICT: BROKEN

Attacked artifact: `.ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh`
(sha256 675b566498a490ded244a19bb2721a5e23bd664ac4366d1a3c3916cb7ce5d776, copied byte-identical to scratch).
Lane HEAD at run time: 96379ae26ef9443097b860ddb33ef924b2cd5b5a (wave-1 integration, not fe0f56b).

## Method

- Fixtures (scratch, removed on exit): `F0` = `git clone --no-checkout` of the lane, detached at 96379ae (clean);
  `F1` = F0 plus three planted uncommitted deletions: last line of `corpus/knowledge/cvss-v4-severity-and-vector.md`,
  line 140 of `corpus/lessons/round-25.md` (text begins `-- corpus/knowledge/claim-gates.md`), last line of a wave file.
- Each mutant = the draft with `L=` pointed at the fixture (the only substitution; the unmutated copy diffs from the
  draft on that one line) plus one sed mutation. Every mutant was checked to differ from its control text.
- Runs: 28 full runs (control + 13 mutants on F0 and F1, default args), plus 6 variant runs
  (base-as-TREE `<04af9bc> <base export>`; F1 with BASE=96379ae). Control re-run: byte-identical (after normalizing scratch paths and the elapsed footer).
- Discrimination by diff against the same-fixture control, after normalizing scratch names and dropping the
  `rc=… elapsed=…` footer.

## Per-mutant results

| # | Mutant (what was changed) | Verdict | Output evidence |
|---|---|---|---|
| M1a | drop the `:(exclude)` pathspec in (1a) and (1b) | KILLED | F0: `grep -c attempt2` on the mutant's (1a) = 664 rows of wave-dir additions now visible. F1 (BASE=96379ae): `SUMMARY deleted_lines=2 … findings=2` vs control `=1`, new `FINDING … .ufo/waves/round-46/attempt2/freeze.txt` |
| M1b | invert: pathspec = wave dir only (outside files hidden) | KILLED | F0: control `SUMMARY deleted_lines=27 pre_justified=0 findings=27` → mutant `SUMMARY deleted_lines=0 pre_justified=0 findings=0` (a false clean). F1 BASE=96379ae: same count 1, but the finding name swaps from cvss to freeze.txt (count-only check would miss it) |
| M1c | exclusion kept in (1a) only, dropped in (1b) | KILLED only in F1/BASE=96379ae (3-line diff, names freeze.txt). SURVIVED on the default fixtures (F0, F1@04af9bc): no base-existing wave-dir deletion exists to expose it |
| M2 | delete `run "(2)" …density.py` | KILLED | `grep -c '^--- (2)'` = 0; 49-line diff; section (2) header and table vanish |
| M3 | BASE default = 914ca0b (attempt-1 base) | KILLED | header `noharm.sh  base=914ca0b6956f01d87b2e252ffad06fe74ec5d9ba  tree=<L>` (contradicts the frozen base 04af9bc); (1b) `SUMMARY deleted_lines=6 pre_justified=2 findings=4` vs `27/0/27` |
| M4 | BASE default = HEAD | KILLED by header only | header `noharm.sh  base=HEAD  tree=<L>`; (1b) `SUMMARY deleted_lines=0 pre_justified=0 findings=0`. The budget reads a false clean; the base string is the only tell |
| M5 | `strip()` no-op (`return substr(p,3)` removed) | KILLED | names keep the diff prefix: `FINDING        DELETED w/corpus/instruments/knowledge-expected.txt: …` (58-line diff) |
| M6 | REGROUND list cut to one entry | KILLED | (1c) loses `32	1	corpus/knowledge/claim-package-contract.md` and its `DELETED` line; (1b) unchanged |
| M7 | remove `trap 'rm -rf -- "$S"' EXIT` | SURVIVED on output (stdout identical to control) — KILLED only by a leak probe | `ls -d $HYAKU_SCRATCH/kasegi-r46/R46bExecNoharm-*` = 2 after the full batch; the two no-trap runs are the only ones without cleanup (control runs left none) |
| M8 | (7b) uses base export as the tree | SURVIVED at the printed granularity | (7a)/(7b) tail lines identical: `c1-gate fixed=2/7 exit=1` both. Full c1 output differs only in limb L1: `gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65` vs `lines=66/base=65` (run directly, `chk/c1-*.txt`) |
| M9 | (7d) uses base export as the tree | KILLED | `c2-gate fixed=5/7 exit=1` (control, live) vs `c2-gate fixed=7/7 exit=0` (mutant) |
| M10 | (2) density reads `$L/SKILL.md` instead of `$TREE/SKILL.md` | SURVIVED with default args (TREE defaults to L); KILLED when TREE ≠ L | base-as-TREE variant: `--- (2) $ python3 <L>/corpus/instruments/density.py <BASE-EXPORT>/SKILL.md` (control) vs `<L>/SKILL.md` (mutant); `(1166 lines, 33 blocks)` vs `(1173 lines, 34 blocks)`; mean dens 258.7 vs 275.1 |
| M12 | exit code masked (`local rc=0`) | KILLED | section (5) `exit=1` → `exit=0` (line 481 of the mutant output); recheck-audit really exits 1 |

Tally: 13 mutants; 11 killed (M1c and M10 only under fixtures that expose them); 2 survive the printed output (M7, M8).

## Findings on the sheet itself (from the control runs, not mutants)

1. **B1 — budget undercounts (BROKEN).** Section (1b) silently drops any deleted line whose text begins with `-- `
   (git prints it as `--- …`, and the awk `/^--- /` rule treats it as a file header). Quote, control on F1 (BASE=96379ae):
   (1a) `    0	1	corpus/lessons/round-25.md` and `    0	1	corpus/knowledge/cvss-v4-severity-and-vector.md`;
   (1b) only `FINDING DELETED corpus/knowledge/cvss-v4-severity-and-vector.md …` and `SUMMARY deleted_lines=1 … findings=1`.
   Cross-check: `git diff --numstat 04af9bc… -- . ':(exclude).ufo/waves/round-46/attempt2' | awk '{d+=$2}END{print d}'` = 29 on F1 (27 real + 2 planted) while SUMMARY = 28 at BASE=04af9bc. The sheet does not compare its own (1a) total with (1b); the mismatch is silent.
   Real-tree instance: `corpus/lessons/round-25.md` is clean in the lane, so this is latent, not an exposed gap in HEAD.
2. **B2 — the draft's recorded receipt is stale.** At HEAD 96379ae the unmutated script prints
   `SUMMARY deleted_lines=27 pre_justified=0 findings=27` (knowledge-expected.txt 3, r46-c2-gate.py 9, r46-counters-selftest-c1.py 11, r46-counters-selftest-c2.py 4 deleted lines), while `noharm-live.txt` in the draft shows `deleted_lines=0`. The budget result in the draft predates the integration commit; every one of these 27 deletions is a FINDING with no errata category.
3. **B3 — c2 gate red at HEAD (surfaced by the sheet's (7d) row).** Direct runs:
   - `fe0f56b` (freeze tree): `c2-gate fixed=7/7 exit=0`
   - `96379ae` (HEAD): `c2-gate fixed=5/7 exit=1`; `gate G1 pass=0 read=rows=29 admitted=29 dup=0`; `gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1`
   - base 04af9bc: `7/7`. The draft's "7/7 at the live tree" predates the F29 admission (28 rows / 65 entries are pinned in r46-c2-gate.py).
4. **B4 — (7a)/(7b) and (7c)/(7d) print only `tail -1`.** At this base C1 reads `2/7` both for base-vs-base and base-vs-live; the (7b) row cannot discriminate its own tree from the do-nothing control at the summary level (M8). Printing the full limb output (or diffing it against (7a)) closes that.
5. **B5 — the trap is unobservable.** "removed on exit" is asserted in the header but never shown; M7 is only visible on the filesystem.

## Limitations

- The live lane was not run directly: the sheet's (1) reads the live working tree (which has uncommitted files), so all results are on the scratch clone F0/F1 with `L=` substituted. The instruments ran from the clone's copies at 96379ae.
- F1's planted deletions are artificial; they exist to expose M1a/M1b/M1c and B1.
- M1c and M10 are detected only under fixtures where the relevant input exists; their default-fixture survival is reported, not hidden.
- One control re-run was done for determinism; mutant runs were single-shot (no repeat for nondeterminism).
- No installs or updates were made (pacman paused; no tool installed). No commit, push, git/jj/index mutation in the lane; fixtures are clones of the lane under scratch only; the lane was only read.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2MutNoHarm` (including the two leaked M7 dirs) is removed on exit.
