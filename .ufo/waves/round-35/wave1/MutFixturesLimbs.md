# MutFixturesLimbs — one-limb fixture mutants for `corpus/instruments/r35-fixtures/D1..D7`

Round 35, wave 1, seat `MutFixturesLimbs` (mutation-tester). Assignment: for each round-34
verifier-routed defect D1–D7 (`corpus/lessons/round-34-verifier-spotcheck.md` §6), take the committed
defect fixture `corpus/instruments/r35-fixtures/D<i>` and (a) mutate it so the defect is absent (the
fix applied) — the check must then pass on that mutant fixture and still fail on the original; and
(b) a mutant adding an unrelated second defect — the check must still fail for its own defect. This
proves each fixture isolates exactly one limb. All work on isolated scratch copies under
`/fast/scratch/hyaku/kasegi-r35/MutFixturesLimbs/`; the committed fixture bytes were never modified
(§7). **Leaf seat: it did not commit, did not stage, did not spawn subagents, and wrote only its
scratch tree and this receipt.**

## Verdict

**21/21 detector runs as expected — 0 survived, 0 inconclusive, 0 baseline failures.** For every
defect D1–D7: the pristine fixture fails exactly its own check (`closed=6/7 exit=1`, only `D<i>`
open); the fix-applied mutant passes all seven checks (`closed=7/7 exit=0`); the unrelated
second-defect mutant still fails for its own defect, and the second defect is caught by its own
check (`closed=5/7 exit=1`, open exactly `D<i>` and `D<j>`). Every fixture therefore isolates
exactly one limb, in both directions.

## 1. Method

- **Pinning.** The detector is a scratch copy of `corpus/instruments/r35-defect-closure.sh` pinned
  by digest before the matrix: sha256
  `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304` (773 lines). Every run below
  used that pinned copy; the live file's digest was re-checked equal at seat end (§7).
- **Loader.** Each tree is materialized fresh exactly like the suite's own `materialize`
  (`r35-defect-closure.sh:567-576`): `cp -a <src>/. <dest>/`, `git init -q`, `git add -A`. This is
  what makes D4's tracking limb read the fixture's own index instead of the enclosing lane worktree
  (`r35-fixtures/README.md` §"How to run the set").
- **Detector.** One bounded behavioral detector for every run: `bash <pinned>/r35-defect-closure.sh
  --root <tree>`, judged on the seven per-check lines (`D<i> check=... open=0|1`) plus the summary
  (`closed=K/7 exit=0|1`) and the suite's own exit code. No check was re-implemented or hand-grepped;
  the suite's own judgement is the only detector.
- **Mutation design.** Two mutants per fixture, both the smallest behavior-bearing edit:
  - `fix` — the fixture's own defect removed, mirroring the real round-35 landing shape (D1:
    placeholder line deleted, correction line naming `c1c6a5f` appended; D2: erratum line carrying
    `round-34 depth:density row` + `201.2` appended, stale row bytes untouched; D3: registry row
    carrying both instrument names appended; D4: provenance note created + `git add -f` the results
    file; D5: a `per-id occurrences` line appended; D6: dead-seat line deleted, `Correction
    (round 35)` line appended; D7: `supersedes R22`/`supersedes R23` rows appended).
  - `second-D<j>` — one unrelated defect from limb `D<j>` reintroduced, rotation `j = i%7+1`
    (D1+D2, D2+D3, D3+D4, D4+D5, D5+D6, D6+D7, D7+D1), applied to the limb's own file only.
- **Expectations.** pristine → `closed=6/7 exit=1` with only `D<i>` open; fix → `closed=7/7
  exit=0`; second → `closed=5/7 exit=1` with exactly `D<i>` and `D<j>` open.
- **No tool installs.** Nothing was installed or upgraded for this seat (bash/grep/git/python3
  sufficed); the tooling-authorization record is therefore empty.

## 2. Suite-revision observation (concurrent writer, disclosed)

The suite was being revised by sibling seats while this seat ran. Observed sha256 revisions of
`corpus/instruments/r35-defect-closure.sh`: `bed8f654…` (643 lines, first pin) → `c748dd70…` (735
lines, fixture-worktree loader + committed controls added) → `d7ad8438…` (773 lines, `others=6/6`
case-line field, D1 gains the `<LANE_HASH>` marker clause, `fix_re` retargeted D4 `tracked=0` →
`provenance=0` and D5 `erratum-file=absent` → `per-id-occurrences=0`). The matrix below ran entirely
on the final revision `d7ad8438…`. The `fix_re` retargeting matters for fixture attribution: under
the earlier spelling, fixture D5's rejection payload
(`erratum-file=present,discriminating-invocation=2,per-id-occurrences=0`) could not be attributed by
`fix_re(D5)`; the landed spelling attributes it. No matrix verdict depends on `fix_re` — the
detector is the plain `--root` run.

## 3. Matrix outcomes (21 runs, three full passes each; table from the final pass)

| run | expected | observed | verdict |
|---|---|---|---|
| `D1-pristine` | closed=6/7 exit=1; open: D1 | closed=6/7 exit=1; open: D1 | met |
| `D1-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D1-second-D2` | closed=5/7 exit=1; open: D1,D2 | closed=5/7 exit=1; open: D1,D2 | met |
| `D2-pristine` | closed=6/7 exit=1; open: D2 | closed=6/7 exit=1; open: D2 | met |
| `D2-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D2-second-D3` | closed=5/7 exit=1; open: D2,D3 | closed=5/7 exit=1; open: D2,D3 | met |
| `D3-pristine` | closed=6/7 exit=1; open: D3 | closed=6/7 exit=1; open: D3 | met |
| `D3-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D3-second-D4` | closed=5/7 exit=1; open: D3,D4 | closed=5/7 exit=1; open: D3,D4 | met |
| `D4-pristine` | closed=6/7 exit=1; open: D4 | closed=6/7 exit=1; open: D4 | met |
| `D4-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D4-second-D5` | closed=5/7 exit=1; open: D4,D5 | closed=5/7 exit=1; open: D4,D5 | met |
| `D5-pristine` | closed=6/7 exit=1; open: D5 | closed=6/7 exit=1; open: D5 | met |
| `D5-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D5-second-D6` | closed=5/7 exit=1; open: D5,D6 | closed=5/7 exit=1; open: D5,D6 | met |
| `D6-pristine` | closed=6/7 exit=1; open: D6 | closed=6/7 exit=1; open: D6 | met |
| `D6-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D6-second-D7` | closed=5/7 exit=1; open: D6,D7 | closed=5/7 exit=1; open: D6,D7 | met |
| `D7-pristine` | closed=6/7 exit=1; open: D7 | closed=6/7 exit=1; open: D7 | met |
| `D7-fix` | closed=7/7 exit=0; open: none | closed=7/7 exit=0; open: none | met |
| `D7-second-D1` | closed=5/7 exit=1; open: D7,D1 | closed=5/7 exit=1; open: D1,D7 | met |

## 4. Full detector outputs (verbatim, one block per run)

Each block: the pinned suite invoked as `bash <pinned>/r35-defect-closure.sh --root <materialized
tree>`; the seven check lines, the summary, and `suite_exit=` are the recorded stdout plus exit
code. Three consecutive passes produced byte-identical blocks for every run (§7).

### Run `D1-pristine`

```
D1-pristine
$ bash r35-defect-closure.sh --root <materialized D1-pristine>
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D1-fix`

```
D1-fix
$ bash r35-defect-closure.sh --root <materialized D1-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D1-second-D2`

```
D1-second-D2
$ bash r35-defect-closure.sh --root <materialized D1-second-D2>
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

### Run `D2-pristine`

```
D2-pristine
$ bash r35-defect-closure.sh --root <materialized D2-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D2-fix`

```
D2-fix
$ bash r35-defect-closure.sh --root <materialized D2-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D2-second-D3`

```
D2-second-D3
$ bash r35-defect-closure.sh --root <materialized D2-second-D3>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

### Run `D3-pristine`

```
D3-pristine
$ bash r35-defect-closure.sh --root <materialized D3-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D3-fix`

```
D3-fix
$ bash r35-defect-closure.sh --root <materialized D3-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D3-second-D4`

```
D3-second-D4
$ bash r35-defect-closure.sh --root <materialized D3-second-D4>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

### Run `D4-pristine`

```
D4-pristine
$ bash r35-defect-closure.sh --root <materialized D4-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D4-fix`

```
D4-fix
$ bash r35-defect-closure.sh --root <materialized D4-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D4-second-D5`

```
D4-second-D5
$ bash r35-defect-closure.sh --root <materialized D4-second-D5>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

### Run `D5-pristine`

```
D5-pristine
$ bash r35-defect-closure.sh --root <materialized D5-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D5-fix`

```
D5-fix
$ bash r35-defect-closure.sh --root <materialized D5-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D5-second-D6`

```
D5-second-D6
$ bash r35-defect-closure.sh --root <materialized D5-second-D6>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

### Run `D6-pristine`

```
D6-pristine
$ bash r35-defect-closure.sh --root <materialized D6-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
suite_exit=1
```

### Run `D6-fix`

```
D6-fix
$ bash r35-defect-closure.sh --root <materialized D6-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D6-second-D7`

```
D6-second-D7
$ bash r35-defect-closure.sh --root <materialized D6-second-D7>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=5/7 exit=1
suite_exit=1
```

### Run `D7-pristine`

```
D7-pristine
$ bash r35-defect-closure.sh --root <materialized D7-pristine>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=6/7 exit=1
suite_exit=1
```

### Run `D7-fix`

```
D7-fix
$ bash r35-defect-closure.sh --root <materialized D7-fix>
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

### Run `D7-second-D1`

```
D7-second-D1
$ bash r35-defect-closure.sh --root <materialized D7-second-D1>
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=5/7 exit=1
suite_exit=1
```

## 5. Mutant diffs (pristine → mutant, `.git` excluded; verbatim)

These are the before/after bytes of every mutant. Each mutant touches exactly one file; the three
`Only in` lines are whole-file add/delete mutations (D3-second-D4 and D4-second-D5 delete a file,
D4-fix adds one); the D4 index operations (`git add -f` / `git rm --cached`) are recorded in §1 and
are visible in the payloads (`tracked=0↔1`).

```diff
=== D1 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D1-pristine/SCORECARD.md D1-fix/SCORECARD.md
--- D1-pristine/SCORECARD.md	2026-10-26 03:37:50.075035426 -0300
+++ D1-fix/SCORECARD.md	2026-10-26 03:40:28.627675799 -0300
@@ -19,5 +19,5 @@
 this paragraph supersedes only those two numbers.
 
 <!-- limb D1 broken: the round-34 placeholder prose is still here and no tip hash is named -->
-**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
 was measured at the wave-1 integration state.
+**Round-34 final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (fix-mutant, MutFixturesLimbs round 35).

=== D1 second-defect mutant diff (pristine -> second-D2), .git excluded ===
diff -r D1-pristine/SCORECARD.md D1-second-D2/SCORECARD.md
--- D1-pristine/SCORECARD.md	2026-10-26 03:37:50.075035426 -0300
+++ D1-second-D2/SCORECARD.md	2026-10-26 03:40:28.653543665 -0300
@@ -13,9 +13,7 @@
 
 
 <!-- limb D2 fixed: the appended erratum below names the stale row and the corrected mean -->
-**Erratum (round 35) — round-34 depth:density row.** The row above is stale on two counts: at the
 round-34 tip `SKILL.md` and `PROVINCE.md` each carry +1 appended line (0 changed lines is wrong), and
-the corrected `density.py` mean is **201.2**, not 201.7. The row's filed bytes are left untouched;
 this paragraph supersedes only those two numbers.
 
 <!-- limb D1 broken: the round-34 placeholder prose is still here and no tip hash is named -->

=== D2 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D2-pristine/SCORECARD.md D2-fix/SCORECARD.md
--- D2-pristine/SCORECARD.md	2026-10-26 03:37:50.075195626 -0300
+++ D2-fix/SCORECARD.md	2026-10-26 03:40:28.703555337 -0300
@@ -16,3 +16,4 @@
 **Final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (recorded in round 35; the
 placeholder prose this line replaces named no hash). Every value in this section was measured at the
 wave-1 integration state.
+Erratum (round 35, fix-mutant): the round-34 depth:density row is corrected by this appended erratum; the measured mean is 201.2.

=== D2 second-defect mutant diff (pristine -> second-D3), .git excluded ===
diff -r D2-pristine/SKILL.md D2-second-D3/SKILL.md
--- D2-pristine/SKILL.md	2026-10-26 03:37:50.075106816 -0300
+++ D2-second-D3/SKILL.md	2026-10-26 03:40:28.728749822 -0300
@@ -7,5 +7,3 @@
 
 | name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
 |---|---|---|---|---|---|---|---|
-| r-defect-closure.sh | gate | cd <lane> && bash corpus/instruments/r35-defect-closure.sh [--root DIR] | exit 0 iff `closed=7/7`; 1 while any round-34 verifier defect D1-D7 is open | cd <lane> && bash corpus/instruments/r35-defect-closure.sh --selftest -> `selftest cases=7 failures=0` | `.ufo/waves/round-35/wave1/R35Closure.md` | all inputs read-only + its own receipt dir | kasegi |
-| kill-rule-check.py | probe | cd <lane> && python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH] | exit 0 iff a `--fake` instrument is rejected; 1 when the fake passes | python3 corpus/instruments/kill-rule-check.py --selftest | `.ufo/waves/round-34/wave1/ExecKillRuleCheck.json` | all inputs read-only + its own receipt dir | kasegi |

=== D3 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D3-pristine/SKILL.md D3-fix/SKILL.md
--- D3-pristine/SKILL.md	2026-10-26 03:37:50.075323926 -0300
+++ D3-fix/SKILL.md	2026-10-26 03:40:28.776016523 -0300
@@ -9,3 +9,4 @@
 |---|---|---|---|---|---|---|---|
 | recheck-audit.py | gate | cd <lane> && python3 corpus/instruments/recheck-audit.py | exit 0 clean; 1 failed; undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | `.ufo/waves/round-26/c1-receipt-index.txt` | corpus/ read-only + its own receipt dir | kasegi |
 | anchorcheck.py | gate | cd <lane> && python3 corpus/instruments/anchorcheck.py <file.md> | fail-closed: exit 0 clean; 1 on a fail class | python3 corpus/instruments/anchorcheck.py --selftest | `.ufo/waves/round-28/c1-receipt-index.txt` | all inputs read-only + its own receipt dir | kasegi |
+| fix-mutant registry row: r-defect-closure and kill-rule-check registered (D3 fix). |

=== D3 second-defect mutant diff (pristine -> second-D4), .git excluded ===
Only in D3-pristine/.ufo/waves/round-34: wave1-results.json.provenance.md

=== D4 fix-mutant diff (pristine -> fix), .git excluded ===
Only in D4-fix/.ufo/waves/round-34: wave1-results.json.provenance.md

=== D4 second-defect mutant diff (pristine -> second-D5), .git excluded ===
Only in D4-pristine/.ufo/waves/round-35: claims-erratum-d5.md

=== D5 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D5-pristine/.ufo/waves/round-35/claims-erratum-d5.md D5-fix/.ufo/waves/round-35/claims-erratum-d5.md
--- D5-pristine/.ufo/waves/round-35/claims-erratum-d5.md	2026-10-26 03:37:50.075594876 -0300
+++ D5-fix/.ufo/waves/round-35/claims-erratum-d5.md	2026-10-26 03:40:28.914455595 -0300
@@ -20,3 +20,4 @@
 
 `every assertion occurrences=1` is false as written: Q9 and Q17 appear twice each and are
 anchor-verified instead of unique, while every other assertion appears exactly once.
+Fix-mutant appendix: the per-id occurrences statement — every assertion is checked with its own occurrence count printed per id.

=== D5 second-defect mutant diff (pristine -> second-D6), .git excluded ===
diff -r D5-pristine/.ufo/waves/round-34/wave1/L1Integration.md D5-second-D6/.ufo/waves/round-34/wave1/L1Integration.md
--- D5-pristine/.ufo/waves/round-34/wave1/L1Integration.md	2026-10-26 03:37:50.075567516 -0300
+++ D5-second-D6/.ufo/waves/round-34/wave1/L1Integration.md	2026-10-26 03:40:28.939560251 -0300
@@ -9,7 +9,7 @@
   `wave1/ExecRDefectClosureSuite.md` §5 (base `closed=0/9`, exit 1) and the wave receipts.
 
 <!-- limb D6 fixed: the stale dead-seat note is superseded, and the stale sentence is not quoted here -->
-**Correction (round 35) — stale dead-seat note.** An earlier revision of this file said a round-33
 summary seat had filed no receipt. That sentence was stale: `wave1/ExecRegressionC1.md` is committed
 at `c1c6a5f` and this correction supersedes the stale note. The round-33 summary seat did file a
 receipt.
+- The round-33 summary `ExecRegressionC1` did not file a receipt (dead seat, 1 of 65); the

=== D6 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D6-pristine/.ufo/waves/round-34/wave1/L1Integration.md D6-fix/.ufo/waves/round-34/wave1/L1Integration.md
--- D6-pristine/.ufo/waves/round-34/wave1/L1Integration.md	2026-10-26 03:37:50.075743476 -0300
+++ D6-fix/.ufo/waves/round-34/wave1/L1Integration.md	2026-10-26 03:40:28.988942352 -0300
@@ -9,5 +9,5 @@
   `wave1/ExecRDefectClosureSuite.md` §5 (base `closed=0/9`, exit 1) and the wave receipts.
 
 <!-- limb D6 broken: the stale dead-seat sentence stands and no round-35 correction was appended -->
-- The round-33 summary `ExecRegressionC1` did not file a receipt (dead seat, 1 of 65); the
   regression battery is covered by this L1 re-run and the wave receipts.
+Correction (round 35): the ExecRegressionC1 receipt is committed in c1c6a5f; the dead-seat sentence above was stale (fix-mutant).

=== D6 second-defect mutant diff (pristine -> second-D7), .git excluded ===
diff -r D6-pristine/corpus/QUALITY.md D6-second-D7/corpus/QUALITY.md
--- D6-pristine/corpus/QUALITY.md	2026-10-26 03:37:50.075732056 -0300
+++ D6-second-D7/corpus/QUALITY.md	2026-10-26 03:40:29.013888238 -0300
@@ -8,5 +8,3 @@
 | R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. | `corpus/lessons/round-33-verifier-spotcheck.md:167-169` (R2 — the frozen parenthetical that literally read `bound=38`); M34-2 at `.ufo/waves/round-34/claims.json` |
 | R23 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. | `considerthese/2026-10-25.md:76` proposal 6 (2026-10-25) |
 <!-- limb D7 fixed: appended supersession rows for R22 and R23 exist -->
-| R27 | (round 35) A record row's grounding cell is corrected by an appended supersession row that names the wrong grounding it replaces and the mistake it should have named. | supersedes R22 — the row named M34-2 as its grounding; the grounding is M34-3 (`corpus/lessons/round-34.md` open item 10, `.ufo/waves/round-34/mistakes-erratum-1.md`). |
-| R28 | (round 35) A record row grounded in a proposal file is re-grounded on the round lesson that mined the proposal. | supersedes R23 — the grounded-in cell cited `considerthese/2026-10-25.md:76`; the grounding is the round-34 lesson §considerthese (`corpus/lessons/round-34.md`). |

=== D7 fix-mutant diff (pristine -> fix), .git excluded ===
diff -r D7-pristine/corpus/QUALITY.md D7-fix/corpus/QUALITY.md
--- D7-pristine/corpus/QUALITY.md	2026-10-26 03:37:50.075959067 -0300
+++ D7-fix/corpus/QUALITY.md	2026-10-26 03:40:29.061189628 -0300
@@ -7,3 +7,5 @@
 |---|---|---|
 | R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. | `corpus/lessons/round-33-verifier-spotcheck.md:167-169` (R2 — the frozen parenthetical that literally read `bound=38`); M34-2 at `.ufo/waves/round-34/claims.json` |
 | R23 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. | `considerthese/2026-10-25.md:76` proposal 6 (2026-10-25) |
+| R-fix-mutant | supersedes R22 | grounding corrected to M34-3 |
+| R-fix-mutant | supersedes R23 | grounding corrected to the round-34 lesson §considerthese |

=== D7 second-defect mutant diff (pristine -> second-D1), .git excluded ===
diff -r D7-pristine/SCORECARD.md D7-second-D1/SCORECARD.md
--- D7-pristine/SCORECARD.md	2026-10-26 03:37:50.075777036 -0300
+++ D7-second-D1/SCORECARD.md	2026-10-26 03:40:29.085512594 -0300
@@ -19,6 +19,6 @@
 this paragraph supersedes only those two numbers.
 
 <!-- limb D1 fixed: no placeholder prose, and the round-34 tip hash is named -->
-**Final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (recorded in round 35; the
 placeholder prose this line replaces named no hash). Every value in this section was measured at the
 wave-1 integration state.
+**Round-34 final lane commit: filled by the L1 in the closing commit.**
```

## 6. Committed-control anchors (run through the same runner)

```
$ bash <pinned>/r35-defect-closure.sh --root <materialized r35-fixtures/clean>
ctl-clean
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
$ bash <pinned>/r35-defect-closure.sh --root <materialized r35-fixtures/two-defect/D1D2>
ctl-two-defect-D1D2
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=5/7 exit=1
suite_exit=1
```

`clean` passes 7/7 and `two-defect/D1D2` fails exactly D1 and D2 — the suite is neither
always-reject nor blind to which limb broke, independently of the seven fixtures under test.

## 7. Fixture stability and restoration evidence

- **The committed fixtures were never written by this seat.** All 65 fixture files carry mtime
  `≤ 2026-10-26T03:37:50.076-03:00` (the fixture build's completion), before this seat's first
  detector run; first/last mtimes: `2026-10-26+03:37:50.0748745860 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/README.md` / `2026-10-26+03:37:50.0762984970 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/fixtures.json`.
- **Digest stability across passes.** Per-file sha256 of every fixture file captured after matrix
  pass 2 (T2) and after pass 3 (T3): the two lists are byte-identical (`diff` empty). T3 list:
  ```
  346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/corpus/QUALITY.md
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/clean/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/corpus/QUALITY.md
a4f21d974f5dbef51fd7af40e30cbdcf1c1ff92f542243a37e15880f7b43e215  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D1/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/corpus/QUALITY.md
8d37f176e250ad269701f7dff527d0cc01c79b7e0eede0285705c7a84f9d2a36  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D2/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/corpus/QUALITY.md
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/SCORECARD.md
ace0e887f632b1930b74e9be0a01fe6021e78fab87aacd1d4d8e2cbeacc642f9  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D3/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/corpus/QUALITY.md
b0f1ac5f179723478c9921aeb4249e2322ee2e0a63a249b871e16a556e2c950e  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/.gitignore
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/.ufo/waves/round-34/wave1-results.json
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D4/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/corpus/QUALITY.md
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/.ufo/waves/round-34/wave1-results.json.provenance.md
2292d081a0a92a019802e80172c68d9f881118677c44a5bc9388b420157fadc0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D5/.ufo/waves/round-35/claims-erratum-d5.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/corpus/QUALITY.md
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/SKILL.md
aebf5bcc285bece5b836f5d934658476df918001747ec295223cc3c8a38aac88  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D6/.ufo/waves/round-35/claims-erratum-d5.md
0efdf7a196d1c0fc6ff05a73a556ae2a2b24a54b947425fcc44e04cea90725fb  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/corpus/QUALITY.md
cf0871072b3909e4af181386acc2095a47b40cf492243a4088f051905ce696fc  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/D7/.ufo/waves/round-35/claims-erratum-d5.md
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/fixtures.json
9bcb39cb5315abe0cd20f39599e03519542f4ae9936f01b4b0e0e80140b272d2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/README.md
346d1c1ce5873355c264d42f9b1ed1bb083a5b9f04b1a358e523a7411c22fced  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/corpus/QUALITY.md
092e3a8189156e81cd809ba3cd3f6486a25a27af43a594bd50b3b06b0f20ab21  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/SCORECARD.md
b3e65baf8e81322eadbbf4327c688b4c9e33a9fc33eef09c0da7e614890db01b  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/SKILL.md
549dd352195c5b25d431c5f1eec89efbcf2421d4556328a1ce93f5c254b839c2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/.ufo/waves/round-34/wave1/L1Integration.md
a27fe46892493655fecf412b6eea2022ff5e0f1a98d9deef82cb02dfaf45fd66  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/.ufo/waves/round-34/wave1-results.json
f2ba0bcc681a73bb82fe9d7953a5881617a292e09cf21a1efc5474a49b0656f3  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/.ufo/waves/round-34/wave1-results.json.provenance.md
ec9a82869dc115eb6543b7489570578ae29dea1e995fdb77bf9d1bd047178531  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r35-fixtures/two-defect/D1D2/.ufo/waves/round-35/claims-erratum-d5.md
  ```
- **Determinism.** All three matrix passes produced byte-identical detector blocks per run
  (verified programmatically: 21 files × 3 blocks, all equal).
- **Per-mutant-tree digests** (sha256 over the sorted per-file `sha256sum` lines, `.git` excluded;
  the pristine row is the fixture's materialized copy):
  ```
  D1-pristine	files=7	tree_sha256=dc3d2f77675f118e29c8694de00d688d913e9def858a7b32efbadfd5eed94496
D1-fix	files=7	tree_sha256=50d8daf1bbb4346e0d29f1cc19e3f1e6cdc7f6fcaa636116720e2509d1721e60
D1-second-D2	files=7	tree_sha256=a2dc47456d2b5f3c8ed1cba16786b1b88ff02d62a7d4b8666889e28697d99d8a
D2-pristine	files=7	tree_sha256=7b4ba7893f36087427bd5dc52d6b52abd50d238d4fc54caa4c5e0a36d1f9c6bf
D2-fix	files=7	tree_sha256=4b2a058aad0d90fcd0a107989a2672e3a7199cb3228243bcecc110aade00377e
D2-second-D3	files=7	tree_sha256=90fdf4bc3e6c8e1f42b8bf4eac5b55885bfeaa1119d1c4b0f3f642e4a0a81640
D3-pristine	files=7	tree_sha256=9d86c544dfafa57630492b3e69334781100705fb211580755505474490135d4c
D3-fix	files=7	tree_sha256=40e3880bb385b9a7d874846add2c939b6572f172281b30da6d9a133758236287
D3-second-D4	files=6	tree_sha256=568f5163d652da405878fbbc42ffa25001da53b91ca20861cc49b9d2705ce745
D4-pristine	files=7	tree_sha256=0df007c3a28344c0d6e62305dac5e7e1df9a12a18ce3a401ab89a68b74f42f56
D4-fix	files=8	tree_sha256=9d45b2496b629b284b0953dea4ada0fced88500510e22ee199b1b69d50937d74
D4-second-D5	files=6	tree_sha256=f834007579aba25df0c097b610b349082fe3df32dfd4fa1578849cda8a3f55b7
D5-pristine	files=7	tree_sha256=6f322db03f38d54cdb1b5e0151466fe579721121105c4325eb88447acb45c710
D5-fix	files=7	tree_sha256=dfb6c9313802bc7ad7d969dbd1a852fdd5dcbcd8b7c06f4f1c1c2d80bab13f26
D5-second-D6	files=7	tree_sha256=0a2640260d7e881f832b92edc928d49737bbf88fce77d4f9b11221e7aa50b907
D6-pristine	files=7	tree_sha256=0c34c9f8aa31b3a642565730ce9d2df050605cbb8fd0d3ec0c6c5d4bc3c5c154
D6-fix	files=7	tree_sha256=af8b150f9f287cdb246e666d52585c191cbaa526929bf60617feab60a2f867bf
D6-second-D7	files=7	tree_sha256=eecb72c7dd53e4756fb3daef0a9ccc86f786d7c660fff82fde0c8f7780479e47
D7-pristine	files=7	tree_sha256=8815320f73522bfab1caabc8b89b28e3983228a55fa7b92facc5c2ddfabd8856
D7-fix	files=7	tree_sha256=be3c95945c0848c4f201525480031b21bccb5c127c3029958614fe41fecd1443
D7-second-D1	files=7	tree_sha256=203c39a28ea8ae61f75ea52c0e35a50259f0f47df7d79404529e56f1c16cf16d
  ```
- **Scratch cleanup.** The whole seat scratch tree
  `/fast/scratch/hyaku/kasegi-r35/MutFixturesLimbs/` is deleted after this receipt lands in the
  wave dir; nothing outside the lane repo and the scratch tree was written.

## 8. Findings for the L1

1. **One-limb isolation holds for all seven fixtures, both directions** (§3): the fix-applied
   mutant passes and the pristine fixture fails on its own clause; the unrelated-second-defect
   mutant leaves the own-clause failure intact and the second defect is detected by its own check.
   No fixture is vacuous; no check is masked by another limb's defect.
2. **Coverage bonus — the `erratum-file=absent` clause is exercised only by a mutant.** No committed
   fixture omits `claims-erratum-d5.md` (D5's fixture keeps the file and drops the
   `per-id occurrences` literal, matching `fix_re(D5)`); the `erratum-file=absent` clause is
   exercised by this seat's `D4-second-D5` mutant (payload `erratum-file=absent,...` open=1, §4).
   ExecSelftestFixtures' receipt flags the same gap; this run is the measured confirmation.
3. **Cross-limb detection independence** (§3, second-defect column): in all seven second-defect
   runs the added defect flipped exactly its own check and nothing else — no check's verdict
   depends on another limb's state.
4. **Suite revision during the wave** (§2): three revisions observed; the matrix ran on the final
   `d7ad8438…`. If the suite moves again before the L1's closing commit, the parent should re-run
   `--selftest` (the suite's own loader reproduces this matrix's construction) — this receipt's
   verdicts are pinned to `d7ad8438…` bytes.
5. **No defects to route.** Every expectation was met on the first full pass and reproduced twice;
   no baseline failure, no surviving mutant, no inconclusive run.

Report: .ufo/waves/round-35/wave1/MutFixturesLimbs.md
