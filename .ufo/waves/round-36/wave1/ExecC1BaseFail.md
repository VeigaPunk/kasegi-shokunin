# ExecC1BaseFail — negative-path run of r36-closure.sh

Round 36, claim C1 (`depth:verifiability`), seat ExecC1BaseFail (leaf executor).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims-freeze commit).

**Verdict: both frozen negative expectations hold on the final bytes.**
`--export-ref 3266c993…` → `closed=0/9 exit=1` (all nine checks open, incl. E1/E3/E5/E6/E7/E8).
`--export-ref 0aee0ef1…` → `closed=3/9 exit=1` (closed E5/E6/E7; open E1, E2, E3, E4, E8, E9), i.e. `closed<9/9 exit=1` with E1/E3/E8 open as the claim requires.

## Instrument under test

| field | value |
|---|---|
| landed path | `corpus/instruments/r36-closure.sh` (appeared in the lane worktree at 2026-10-26T12:53:39-0300, **untracked** at run time — written by the L1/author seat, not by me) |
| draft path | `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh` (author scratch, removed at the author's yield) |
| sha256 | `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` for **both** paths byte-for-byte; the run header prints the same `suite-sha256=` |
| lines | 894 |
| `bash -n` | clean |
| preserved copy | `/fast/scratch/hyaku/kasegi-r36/ExecC1BaseFail/draft/r36-closure.sh`, sha256 identical; scratch copy is removed at yield, full text is in `.ufo/waves/round-36/wave1/ExecC1SuiteBuild.md` |
| draft lineage | `1019d64d` (710 ln), `948d55ff` (intermediate), `ff616adc` (737 ln), `76273416` (817 ln), `4db1ae70` (894 ln, declared FINAL and landed). Every revision I measured printed the same negative verdict shape (base 0/9; head well below 9/9 with E1/E3/E8 open), so the negative signal is stable across the draft churn; the numbers below are the final bytes. |

Interface used (from the suite's own header): `--export-ref <hash> [--lane DIR] [--work DIR] [--scratch-root DIR]`; the
suite runs `git -C <lane> archive <hash> | tar -x -C <work>/export` and every check reads only under that export,
except the declared ref-scoped read-only git limbs (E1 commit existence/ancestry, E4 tracking lints, E9 quiescence).
The plain run mode is refused with exit 2 by design, so the export mode is the only mode tested here.

## Commands actually run

Primary evidence — the landed instrument, canonical form (the frozen counting command, no optional args; scratch bound
through `TMPDIR` so nothing lands in an inherited temp dir):

```bash
S=/fast/scratch/hyaku/kasegi-r36/ExecC1BaseFail
export TMPDIR="$S/tmp2"
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
bash corpus/instruments/r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c
bash corpus/instruments/r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988
```

Run at 2026-10-26T15:53:58Z. Two control runs on the same bytes:
- the preserved draft copy from my scratch (`$S/draft/r36-closure.sh`, same sha256) with the same canonical args:
  identical per-check payloads and identical `closed=K/9` lines (case 1 `0/9`, case 2 `3/9`), run 2026-10-26T15:52:31Z;
- the draft with explicit `--lane <lane> --work $S/work-{base,head}`: identical verdicts, header adds
  `deviation=non-default --lane` (the suite flags the explicit lane flag even when it names the default lane).
Both `--work` dirs and both `TMPDIR` scratch dirs are empty after the runs (the suite clears its extraction on exit).

## Case 1 — r35 base export, `3266c9937b03062d9bbc2f436e20820115ed179c` (tree `1249622d9c1e66afe359ef96bfaa44f243c8cc23`)

stdout (verbatim from the landed run), exit code 1, stderr empty:

```
export-ref=3266c9937b03062d9bbc2f436e20820115ed179c mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
E1 payload=placeholders=1,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=0,erratum-row=0,erratum-mean=0 closed=0
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=0,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=0 closed=0
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=0 closed=0
E7 payload=supersedes-r22=0,supersedes-r23=0 closed=0
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=0,round35-lesson=0 closed=0
E9 payload=status-dirty=10,scratch-seat-dirs=14,head-match=0,lane-root=1,scratch-root=present closed=0
closed=0/9 exit=1
```

Expectation: `closed=0/9 exit=1` with at least E1/E3/E5/E6/E7/E8 open. **Met exactly (9/9 open).**

## Case 2 — r35 judged head export, `0aee0ef105395a2f1d6ace7eaeef13871bb26988` (tree `ce2befeef60131bee9bbd7ebe701305daf2f291f`)

stdout (verbatim from the landed run), exit code 1, stderr empty:

```
export-ref=0aee0ef105395a2f1d6ace7eaeef13871bb26988 mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
E1 payload=placeholders=1,lane-hash-markers=0,round36-section=0,round36-final-lane-commits=0,bound=0 closed=0
E2 payload=erratum-marker=1,erratum-row=0,erratum-mean=3 closed=0
E3 payload=registry-r35-defect-closure=0,registry-r36-closure=0 closed=0
E4 payload=tracked-ref=0,tracked-index=1,provenance-note=0 closed=0
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=0,names-corrected-line=0,stale-line=1,round35-lesson=1 closed=0
E9 payload=status-dirty=10,scratch-seat-dirs=14,head-match=0,lane-root=1,scratch-root=present closed=0
closed=3/9 exit=1
```

Expectation: `closed<9/9 exit=1` with E1 or E3 or E8 open. **Met (3/9; E5/E6/E7 closed, as the author predicted for
these bytes; E2 open because that head carries the stale depth:density row and no corrected 201.2 row).**

## Attribution — the verdicts are the bytes, not harness noise

Independent reads on freshly re-extracted copies of the same two refs (raw `grep`/`git ls-tree`), so each open check
is traceable to a real clause:

| check | case 1 (3266c99) | case 2 (0aee0ef) | source read |
|---|---|---|---|
| E1 | open: `placeholders=1` | open: `placeholders=1`, `round36-section=0` | `SCORECARD.md:1240` `**Round-34 final lane commit: filled by the L1 in the closing commit.**`; at 0aee0ef the prose placeholder survives at `SCORECARD.md:1271` (`final lane commit filled by the L1 in the closing commit.`). `grep -c 'Round 36' SCORECARD.md` = 0 in both exports, so the round-36-scoped section the final check requires is absent by construction here. |
| E2 | open (`marker=0, row=0, mean=0`) | open (`marker=1, row=0, mean=3`) | at 0aee0ef `SCORECARD.md:1246` carries `Erratum (round 35): … mean 201.2 …` and `201.2` appears 3×, but the corrected **depth:density row** is absent (the only depth:density table row is the round-35 move-log row at `:1269`). Base carries neither marker nor mean. |
| E3 | open (0/0 registry rows) | open (0/0) | `grep -c 'r35-defect-closure.sh' SKILL.md` = 0 and `grep -c 'r36-closure.sh' SKILL.md` = 0 in both exports (read as section-scoped rows) |
| E4 | open | open | `git ls-tree -r --name-only 0aee0ef -- .ufo/waves/round-35/` contains no `wave1-results.json` and no `.provenance.md` (only wave-1 receipts such as `wave1/ExecD4ResultsTrack.md`); the frozen `git ls-files` limb reads 1 because the live lane index tracks the round-35 results file |
| E5 | open | closed | `.ufo/waves/round-35/claims-erratum-d5.md` absent at base, present (non-empty) at head |
| E6 | open | closed | `grep -c 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md` = 0 → 1 |
| E7 | open | closed | `grep -c 'supersedes R2[23]' corpus/QUALITY.md` = 0 → 2 (row-shaped read) |
| E8 | open (`m36=0, names-corrected-line=0, stale=0, round35-lesson=0`) | open (`m36=0, names-corrected-line=0, stale=1, round35-lesson=1`) | `corpus/lessons/round-36.md` absent in both exports; `corpus/lessons/round-35.md:15` at 0aee0ef still carries `source-recheck exit 0 on committed bytes` |
| E9 | open (`dirty=10, seat-dirs=14, head-match=0, lane-root=1, scratch-root=present`) | open (same counters at that instant) | live limb by construction: the lane worktree has 10 untracked entries at run time (the 9 round-36 wave entries plus the newly landed untracked `corpus/instruments/r36-closure.sh`), 14 seat dirs existed under `/fast/scratch/hyaku/kasegi-r36`, and neither export ref is lane `HEAD` `b47f2cdf…` |

Check-count arithmetic: 0 closed of 9 (case 1) and 3 closed of 9 (case 2); the printed `closed=K/9` matches the
`closed=0|1` field count in both runs, so the summary line is not a canned string.

## Landing risks observed from the negative side (not suite bugs)

1. **E1 now needs a round-36 SCORECARD section** carrying the Final lane commit line whose 40-hex hash exists and is an
   ancestor of the exported ref (the check is scoped to the last `Round[- ]36` block). The live tree at `b47f2cdf`
   already reads 0 for both placeholder tokens, so only that section + binding remains.
2. **E2 needs the corrected depth:density row**, not just the erratum prose and the `201.2` mean: at 0aee0ef the prose
   is present and the corrected row is not, which is why E2 reads open there. The round-36 closing SCORECARD must carry
   the corrected row (while keeping the `Erratum (round 35)` marker and mean the check also requires).
3. **E4 cannot close at the final head as the tree stands.** `.ufo/waves/round-35/wave1-results.json` is tracked, but
   `.ufo/waves/round-35/wave1-results.json.provenance.md` does **not** exist (live `ls`: only `wave1-results.json`; the
   round-34 pair is the template). The final check also requires that note to be non-empty, so the L1 must commit a
   non-empty note. This is the one landing item my seat cannot fix.
4. **E3 and E8 are landing requirements.** The two exact-basename section-scoped rows in `SKILL.md`
   (`r35-defect-closure.sh`, `r36-closure.sh`) and `corpus/lessons/round-36.md` with the `M36` rows plus removal of the
   stale `source-recheck exit 0 on committed bytes` line from `corpus/lessons/round-35.md` are absent as measured.
5. **E9 is live and can only close at filing**: committed round-36 wave files (porcelain empty), no leftover
   `/fast/scratch/hyaku/kasegi-r36` seat dirs, exported ref == lane HEAD. Its counters move while the wave runs
   (observed seat-dirs 48 → 40 → 24 → 16 → 14 and status-dirty 9 → 10 across revisions), which is the intended signal.

## Scope, side effects, tooling

- Writes: this receipt and scratch only (`/fast/scratch/hyaku/kasegi-r36/ExecC1BaseFail/` — exports, the preserved
  draft copy, per-case stdout/stderr, runner scripts, `tmp/`, `tmp2/`). I did **not** create or modify
  `corpus/instruments/r36-closure.sh`; it is another seat's untracked landing that I only executed. No other
  lane/fleet/source-tree file was written; no mutating git command was run (only `archive`, `rev-parse`, `cat-file`,
  `merge-base`, `ls-tree`, `ls-files`, `status`).
- After all runs the lane worktree shows exactly the pre-existing wave state plus that landed untracked instrument:
  `git status --porcelain` = 9 untracked `.ufo/waves/round-36` entries + `?? corpus/instruments/r36-closure.sh`, 0
  modified tracked files, `.git/index.lock` absent (E9 uses `git status --no-optional-locks`).
- Tooling: no installs or upgrades (suite is self-contained bash + coreutils + git).
