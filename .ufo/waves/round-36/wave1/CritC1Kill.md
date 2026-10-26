# CritC1Kill — round 36, attack matrix for the final `r36-closure.sh` (C1)

Seat: critic `CritC1Kill`, leaf of round-36 wave 1. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(worktree `b47f2cdf…`, parent = claims freeze). Assignment: make each E-check pass while its defect is
present — including E1 by removing/repudiating the Final-lane-commit line, E3 by a near-name row, E8 by a
different phrase, E9 by deleting the check — test the kill-rule clauses (count-zero escapes, summary-only
selftest, worktree fallback), and report the limits that remain with counters bound to bytes.

**Artifact under test.** Final draft by `ExecC1SuiteBuild`, pinned in scratch:

| digest | bytes / lines | state |
|---|---|---|
| `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` | 39022 B / 894 | **final; every row below measured on it** |
| `76273416…` (817), `ff616adc…` (737) | 34631 / 28980 B | superseded; their failures are summarised in §2 |

The suite was a scratch draft when the matrix ran; it has since been **integrated byte-identically** as
`caa3146` (`corpus/instruments/r36-closure.sh`, `sha256 = 4db1ae70…`, verified from the committed file), so
every number below is a result for the committed bytes. Method: pin the draft, `source` it in a harness
(it guards `main` behind `BASH_SOURCE = $0`), call `run_check <En> <TREE> <REF>` on scratch trees built
from `git archive b47f2cdf…` (SCORECARD.md `ed6e931f…`, SKILL.md `daeff71b…`, QUALITY.md `d4f83bb1…`,
round-35.md `af6e2c99…`); each tree differs by exactly one mutation; a row reading `closed=1` with the
defect present is a survivor. No lane file was written; no mutating git outside my own scratch `git init`
fixtures. Post-integration state is in §7.

**Reproduced counters (byte-bound).**

```
3266c993  closed=0/9 exit=1   (E1 ph=1,section=0; E2 0/0/0; E3 0/0; E4 tref=0 note=0; E5 0; E6 corr=0;
                               E7 0/0; E8 0/0/stale=0/lesson35=0; E9 dirty=9 seats=18 head=0)
0aee0ef1  closed=3/9 exit=1   (E5,E6,E7 closed; E2 marker=1,row=0; E1 section=0; E4 tref=0; E8 stale=1)
b47f2cdf  closed=4/9 exit=1   (E2,E5,E6,E7 closed; E1 section=0; E3 0/0; E4 note=0; E8 m36=0)
selftest  cases=9 failures=5  at b47f2cdf (positives E1,E3,E4,E8,E9 = the unlanded limbs);
          mutants 4/4 3/3 5/5 1/1 1/1 1/1 2/2 4/4 4/4; four forged reports rejected; own report accepted=0
report    export-ref=… mode=export lane=<abs> suite-sha256=4db1ae70…   (new in this revision)
```

E1 at `b47f2cdf` is now **open** (`round36-section=0`): the round-36 section is an explicit landing
obligation, which is what the frozen kill rule demands.

## 1. Attack matrix (final digest `4db1ae70…`)

`S` = survives (check closed, defect present), `K` = killed (check open), `C` = control.

| # | check | attack (tree = HEAD export + one mutation) | verdict | payload |
|---|---|---|---|---|
| B1 | E1 | no round-36 heading at all (HEAD bytes) | K | `round36-section=0` |
| B2 | E1 | `## Round 36 — closure` + a line naming a **nonexistent** hash | K | `section=1,commits=1,bound=0` |
| B3 | E1 | same, naming the r36 **base** `cc692008…` (stale ancestor) | **S** | `section=1,commits=1,bound=1` |
| B4 | E1 | base hash plus `— WRONG, superseded; not the closing commit` | **S** | `commits=1,bound=1` |
| B5 | E1 | ancestor + nonexistent hash in one line | K | `commits=2,bound=1` |
| B6 | E1 | real round-36 section has no line; a **last** `## Round-36 appendix` carries a bound decoy | **S** | `section=1,commits=1,bound=1` |
| B7 | E1 | prose placeholder inside the round-36 section (`The L1 fills this line…`) | K | `commits=0` |
| B8 | E2 | `No Erratum (round 35) is owed.` + `\| depth:density \| 9 \| mean **201.2**, measured on the wrong bytes \|` | **S** | `marker=1,row=1,mean=1` |
| B9 | E2 | fabricated matching row without the marker | K | `marker=0` |
| B10 | E3 | rows inside `## Round-36 Gates & probes registry retraction (r36-closure.sh withdrawn)` | **S** | `1/1` |
| B11 | E3 | near-name rows `…sh.bak` / `…sh.old` | K | `0/0` |
| B12 | E4 | provenance note = **1 byte** `x` (results.json untouched) | **S** | `tref=1,tidx=1,note=1` |
| B13 | E4 | 0-byte note | K | `note=0` |
| B14 | E5 | erratum file = **1 byte** `x`, no statements | **S** | `claims-erratum-d5=1` |
| B15 | E5 | 0-byte file / directory | K | `=0` |
| B16 | E6 | `The prior \`Correction (round 35)\` note was wrong and has been withdrawn.` | **S** | `correction-round35=1` |
| B17 | E7 | rows whose third cell reads `supersedes R22 is not needed…` / `R23 is not needed either` | **S** | `1/1` |
| B18 | E7 | prose negation / prose mention | K | `0/0` |
| B19 | E8 | `round-36.md` = `M36 source-recheck` (two bare tokens) | **S** | `m36=1,names=1,stale=0,lesson35=1` |
| B20 | E8 | stale claim **respelled** in round-35.md (`source-recheck S052 exit 0 on committed bytes`) | **S** | `stale=0` |
| B21 | E8 | faithful append-only correction **quoted in round-35.md** | K | `stale=1` (see §3.8) |
| B22 | E9 | leftover regular file in the scratch root | **S** | `scratch-seat-dirs=0` |
| B23 | E9 | leftover symlink named like a seat dir | **S** | `scratch-seat-dirs=0` |
| B24 | E9 | `--scratch-root <empty dir>` while the canonical root held 18 seat dirs | **S** | `scratch-root=present,seat-dirs=0` |
| B25 | E9 | real seat dir (control) | K | `seat-dirs=1` |
| B26 | all | suite on a **fabricated lane** (`--lane` + its own head): one round-36 section naming the repo's seed commit, one registry section with two stub rows, `{}` results, 1-byte provenance/erratum, `M36 source-recheck`, two `supersedes` rows | **S** | `closed=9/9 exit=0` + `deviation=non-default --lane` + `deviation=non-default --scratch-root` |
| B27 | judge | 9 fabricated `selftest case=E<n> … mutants=1/1 verdict=pass` + 9 fabricated `selftest detail=E<n> mutant=forged rejected=1` + summary | **S** | `judge_selftest_report` ACCEPTED |
| B28 | judge | summary-only; `mutants=0/0` case lines | K | both rejected |

## 2. What the superseded revisions failed, and what this one fixed

`ff616adc…` (first draft) had: E1 history-bound (no round-36 line green; lowercase bogus hash green),
E2 prose-satisfiable, E3 substring-satisfiable by `.bak`/`.old` rows and prose, E4/E5 0-byte and directory
passes, E7 prose pass, E8 bare `M36`, E9 no lane-root limb, judge accepting 9 forged case lines, and a
report header with no lane/digest. `76273416…` fixed E3 section-scoping, E7 row shape, E8's
`names-corrected-line` + `round35-lesson` limbs, E9's `lane-root` limb and `--no-optional-locks`.

This revision additionally fixes: E1 section-scoping with `[Ff]inal` case and all-values-ancestral
(B1/B2/B5/B7 now red), E2's marker + row shape (B9 red), E3 cell-equality (B11 red), E4/E5 non-emptiness
(B13/B15 red), the judge's per-id detail/mutant-count cross-check (B28 red), and the report's
`lane=`/`suite-sha256=` header. Each of those is a real, measured improvement — the instrument is no
longer satisfied by a bare summary or a mention.

## 3. Limits that remain (measured; the suite's own selftest is not proof)

1. **E1 still accepts any ancestor.** B3 (round-36 line naming the **base** commit) and B4 (a
   self-repudiating line naming it) are green: the check proves the named commit exists and is ancestral,
   not that it is the closing commit. B6 shows the "LAST `Round[- ]?36` heading" rule: a trailing
   `## Round-36 appendix` with a bound decoy satisfies it while the real closure section carries no line.
   *Correction:* accept only the export ref's first parent (or ref itself when the line sits in the
   closing append), and scope to the last heading whose text does not contain `appendix|superseded`.
2. **E2's marker is a substring and its row is only a shape.** B8: `No Erratum (round 35) is owed.`
   supplies the marker and a fabricated `| depth:density | 9 | mean **201.2**, measured on the wrong
   bytes |` supplies the row. *Correction:* require the marker line not to be negated and require the row's
   remaining cells (blocks / cites) and the "corrected mean" sentence.
3. **E3 counts rows, not registration.** B10: rows inside a heading that declares the instrument
   *withdrawn*, with `not-a-probe` in the type cell, close it. *Correction:* require the type cell to
   contain `gate|probe` and reject section headings containing `retraction|withdrawn`.
4. **E4 content is unbound.** B12: a 1-byte note and an unmodified `{}` results file pass; the check never
   opens either. Disclosed limit of the claim's wording ("tracked with provenance note").
5. **E5 content is unbound.** B14: a 1-byte file passes; r35 D5's `discriminating invocation` /
   `per-id occurrences` limbs were dropped. *Correction:* restore both tokens.
6. **E6 is a phrase test.** B16 (withdrawal) passes; it also cannot distinguish the append the spot-check
   ordered from the rewrite r35 shipped — at `0aee0ef` it reads closed on exactly the `−3/+6` rewrite
   `corpus/lessons/round-35-verifier-spotcheck.md:112` filed. *Correction:* require zero deletions for
   that path against the round-34 integration commit and a cited defect id.
7. **E7 is row-shaped but content-blind.** B17: a row whose cell negates the supersession passes; and
   round-35's R26/R27 rows already satisfy the literals, so round-36 can add nothing. *Correction:*
   require this round's minted ids and reject `not|withdrawn|no … needed`.
8. **E8 verifies two tokens and an already-true absence.** B19 (`M36 source-recheck`) passes; B20 shows
   the stale claim surviving respelled. The `stale-line=0` limb was already 0 at the round-36 base
   (measured; the literal left when `980aa3d` replaced `corpus/lessons/round-35.md` wholesale, not because
   a correction landed), so it adds no round-36 discrimination. The builder's rebuttal is fair — the
   correction belongs in `round-36.md`, so B21 (quoting it in `round-35.md`) is the wrong placement — but
   the residual is that a lesson saying `M36 source-recheck` proves nothing about *what* was corrected.
   *Correction:* require `M36-[0-9]` at row start and a quoted fragment of the corrected sentence in
   `round-36.md`.
9. **E9 has type and path escapes.** B22/B23 (a leftover file, or a symlink named like a seat dir, reads as
   zero seat dirs — only `-type d` at depth 1 is counted) and B24 (`--scratch-root` may name an empty dir;
   the payload now exposes it as `scratch-root=present` and `deviation=`, but the pass/fail does not
   gate). *Correction:* count any entry, and refuse a non-canonical `--scratch-root`/`--lane` outside
   `--selftest`.
10. **Nothing gates the green to the lane or the instrument bytes.** B26 prints `closed=9/9 exit=0` on a
    fabricated repo; the new header prints `lane=` and `suite-sha256=` (good — the digest is the executing
    file's own sha256, verified here as `4db1ae70…`), but both are self-reported and `deviation=` does not
    gate. B27 shows the judge still accepts a fully fabricated report one layer deeper (matching detail
    lines and mutant counts, no fixture executed); the committed do-nothing control is still not run.
    *Correction:* make the frozen counter require `lane=<canonical>` and the pinned digest, hard-fail
    `--lane`/`--scratch-root` outside `--selftest`, and run the committed fake suite.
11. **Export containment is not hermetic.** The export carries 6 absolute symlinks into the live lane (58
    symlinks total), e.g. `.ufo/waves/round-29/wave1/CritC2Kill-scratch/corpus/instruments -> …/kasegi-shokunin/corpus/instruments`.
    No E1–E9 path traverses one today (all nine read fixed regular files: verified), so there is no
    live-byte survivor now, but the header's "every check reads its bytes only under that export root" is
    false for a tree containing such a link. *Correction:* after extraction, fail on any absolute symlink
    or any symlink resolving outside the export root.

## 4. Kill-rule clause results

| clause (frozen C1 `kill_rule`) | result |
|---|---|
| suite missing (`ls_exit=2`) | **false now**: the instrument is committed at `caa3146`, `sha256 = 4db1ae70…` |
| final-head export `closed=9/9 exit=0` | `b47f2cdf…` 4/9 → `caa3146`/`e666d90` 6/9 → `2c26a97` **8/9** (only E9 open); unproven until the closing commit |
| `--selftest cases=9 failures=0` | 9 cases, 5 failures at `b47f2cdf…` (E1,E3,E4,E8,E9 = unlanded limbs); green only when they land |
| any E-check can pass with its defect present | **FIRES** — B3/B4/B6, B8, B10, B12, B14, B16, B17, B19/B20, B22/B23/B24, B26/B27 |
| `grep -c 'filled by the L1' SCORECARD.md != 0` | 0 at `b47f2cdf` (measured); 1 at `0aee0ef` |
| lane status empty at filing | **not now**: 9 untracked round-36 dispatch paths under `.ufo/waves/round-36/`; L1's to commit |
| no leftover `kasegi-r36` seat dirs | **not now**: 18 dirs at the last read; this seat's own removed at yield |
| Final lane commit hash exists and is ancestral | **enforced now** for a line in the round-36 section (B2 red); **not** that it is the closing commit (B3/B4 green) |

## 5. Verdict

**Axis impacted: `depth:verifiability` (C1) only** — nothing installed, no coverage/density/calibration
byte touched.

The final draft is materially stronger than both predecessors: export-only, no worktree fallback, a
section-scoped E1 that rejects a missing round-36 line and an unresolvable hash, row-shaped E3/E7 that
reject mentions, a judge that rejects summary-only and mutant-free reports, a deleted-check guard, a
report header that now carries the lane path and the executing file's sha256, and it reproduces exactly the
expected base 0/9 / judged 3/9 / HEAD 4/9 and the 9-case / 5-failure selftest. Every survivor above is a
*shape* rather than a mention: the instrument now measures forms (section, row, non-empty file, token
pair), and the remaining gaps are that the forms are not tied to the semantics they stand for (an
ancestor is not the closing commit, a row can negate its own content, two tokens are not a correction).
The honest reading for the canonical judge is that the instrument supports a **hold at 4**, not a move:
C1 cannot be scored above held while B3/B8/B10/B17/B19 are reachable, and the disclosure must name them
(as round 35 disclosed its own). The smallest set that would change the verdict: E1 bound to the export
ref (or its first parent) and to a non-`appendix` heading; E2 non-negated marker + populated row; E3
type-cell `gate|probe` and no retraction heading; E5's two statement limbs; E7 this round's ids; E8
`M36-[0-9]` + a quoted fragment; E9 any-entry counting; gating on canonical lane/digest and running the
committed fake suite.

## 6. Post-integration state and the builder's disposition

The instrument was integrated **byte-identically** before my matrix landed: `caa3146`
(`corpus/instruments/r36-closure.sh`, `sha256 = 4db1ae70…`, confirmed from the committed file — the
digest the builder pins is the digest I attacked). Measured on the committed bytes, default lane and
scratch root, `--work` in scratch:

```
caa3146   closed=6/9 exit=1   E1 open (round36-section=1, bound=0) · E4 note=0 · E9 dirty=1 seats=1 head=0
e666d90   closed=6/9 exit=1   same
2c26a97   closed=8/9 exit=1   only E9 open (status-dirty=1, scratch-seat-dirs=3, head-match=1)
```

`2c26a97` ("round-36: E1 Final lane commit line, E4 provenance note, lesson hash") is the landing order the
suite predicts: E1 and E4 closed as soon as their bytes were committed, E9 remains until the closing
commit clears the worktree and the seat dirs.

**The real E1 green is the B3 class in the lane's own bytes.** At `2c26a97` the round-36 line reads
`Final lane commit: e666d902…` (`SCORECARD.md:1492`) while `HEAD` is `2c26a97` — the line names an
ancestor, which is exactly what the check accepts (`round36-final-lane-commits=1,bound=1`). This is inside
the frozen limb ("exists and is an ancestor"), but `bound=1` must not be read as "the line names the final
commit": it names the pre-closing commit, as B3's base-hash tree does.

**Builder disposition (IRC).** No re-cut of the integrated instrument (it was integrated before the matrix
landed); the 12 post-integration survivors were triaged into (a) **literal-conforming limits** — E1
ancestor, E4 existence+non-empty, E5 presence, E6 marker, E9 dirs-only, judge shape — and (b) the
**round-37 backlog with exact edits** — E3 retraction heading + `gate|probe` type cell, E7 negation row,
E8 `M36-[0-9]` + quoted fragment, E2 non-negated marker + r35's row-bytes limb, canonical
lane/scratch-root gating, and an E1 `on-head` limb first.

**Critic's standing.** I accept (a) as claim-literal limits: the frozen predicate names existence or
presence, so a 1-byte note or a base-hash ancestor is inside the wording and is not a clause-4 hit. But
B10 (E3), B17 (E7) and B19 (E8) are clause-4 hits **by the builder's own classification** ("do not
conform"): each check's stated defect is a registration, a supersession row, or a recorded correction, and
a retraction row, a self-negating row, or the two tokens `M36 source-recheck` satisfy the check without it.
B24/B26 are clause-4 hits only when a run passes `--scratch-root`/`--lane`; the frozen counting command
does not, so they are invocation-scope warnings, not counter defects. Verdict unchanged: **hold at 4**,
with the round-37 backlog as the exact fix list. The instrument is a sound gate for the shapes it names,
not proof of the semantics those shapes stand for.

Not re-run by this seat: the final-head `--selftest` (the L1's counted run; at `2c26a97` its E9 positive
fails on the dirty worktree, so it cannot be green yet).

## 7. Hygiene

- Tooling: none installed, none needed (`bash` 5.x, `git`, `awk`, `sed`, `realpath`, `sha256sum` as present).
- Scratch: `/fast/scratch/hyaku/kasegi-r36/CritC1Kill/` (drafts, export, attack trees, fake lanes,
  fixtures); removed before yield.
- Writes: this receipt only. No lane repo, fleet, sibling lane, or source-tree file was written; no
  mutating git outside my own scratch `git init` fixtures.
- Read state: the lane advanced under the review — attack base `b47f2cdf…` → integration `caa3146` →
  wave evidence `e666d90` → closure bytes `2c26a97` (the `2c26a97` line's own claim). At the last read:
  `git status --porcelain` = 1 modified path (`.ufo/waves/round-36/wave1/SimplReport.md`), canonical
  scratch root = 3 seat dirs (18 during the attack run). Three drafts reviewed (`ff616adc` 737 lines,
  `76273416` 817, `4db1ae70` 894) plus the committed instrument `caa3146` (byte-identical to
  `4db1ae70`); the 28 rows of §1 are re-runnable against any later digest.
