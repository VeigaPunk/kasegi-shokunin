VERDICT: DRAFT-READY

# R46bMutBattery — mutation-testing the round-46 battery runner itself

Seat: R46bMutBattery (leaf, no delegation). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Target: `corpus/instruments/r46-mutbat.py` (the round-46 attempt-2 mutation-battery runner, sha256
`f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`, byte-identical to the frozen
`freeze.txt` `mutbat-sha256-v1`). The committed runner was never modified: every mutant was a
single-line edit of a scratch **copy** under `/fast/scratch/hyaku/kasegi-r46/R46bMutBattery/`.

## 0. What was attacked and how

The seat spec asks: does the battery's **own output contract** catch a battery that (a) reports
caught when failures==0, (b) swaps caught/equivalent, (c) skips a mutant silently on copy failure,
(d) exits 0 with uncaught>0. I built 16 single-line (one 2-line) mutants of the runner, ran each
against 6 scenario trees, and graded every run with a checker written **only** against the runner's
own stdout + process exit status — no external reference, no outside knowledge.

**Harness (scratch only; nothing under the lane was written except this report and the draft dir).**

- Base tree: `git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/tree`
  (frozen base rev from `freeze.txt`).
- PURE export: `cp -a /fast/scratch/hyaku/kasegi-r46/L1/pure2 $S/pure` (copy, never edited).
- **Fidelity check of the fast harness.** The real selftests cost ~10 min per run, so the harness
  replaces the two selftests with a stub that replays the **frozen** per-mutant failure counts
  (`controls/mutbat-before.txt`) keyed by the sha256 of the counter file under test. The stub is
  faithful iff the runner's output over the stub tree is byte-identical to the frozen receipt:

```
$ diff <(grep -v '^BATEXIT=' /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/controls/mutbat-before.txt) \
       /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/work/stub-baseline.txt && echo IDENTICAL
IDENTICAL to frozen receipt (excluding BATEXIT line)
```

  The stub tree is therefore a faithful stand-in for the runner's own grading/printing/exit logic,
  which is exactly what this seat attacks. **Limitation:** the stub replays *recorded* failure
  counts; it does not re-derive them. Two real-selftest spot-checks were run to confirm the
  replayed values (both matched — see §7.2).

- Scenarios (each a scratch tree; the runner is invoked identically in all of them):

| id | tree | purpose |
|----|------|---------|
| S1 | stub tree, both counters | the frozen-receipt scenario (the runner's normal run) |
| S2 | stub tree + `--equivalent` map (one real proof file, one dangling proof path) | exercises the `equivalent` branch |
| S3 | c1 counter drifted (`MIN_ROWS = 6` → `MIN_ROWS = 7`, so mutant M16's anchor occurs 0 times) | the runner must fail **loudly**, not mis-grade |
| S4 | the c1 selftest crashes (prints no verdict) | the runner must report `BASELINE-DIRTY` |
| S5 | the tree's `corpus/instruments` holds an unreadable file | the mutant **copy** fails |
| S6 | one mutant's selftest crashes mid-run | the runner must still print that mutant's line |

- **Do-nothing control:** `N01` changes `bad = 0` to `bad = 0  # noqa: do-nothing control`
  (one line, semantics-preserving). Its stdout is byte-identical to the control in **all six**
  scenarios — the harness therefore discriminates and does not merely flag anything.

```
$ for s in S1 S2 S3 S4 S5 S6; do diff -q out/CONTROL-$s.txt out/N01-$s.txt >/dev/null && echo "  $s: identical"; done
  S1: identical
  S2: identical
  S3: identical
  S4: identical
  S5: identical
  S6: identical
```

- **Control runs.** The pristine runner passes the output contract in every scenario
  (`CONTRACT-OK` × 6), so every violation reported below is caused by the mutant, not by the harness.

## 1. The output contract used as the detector

Derived from the runner's own docstring (`r46-mutbat.py:9-26`) and its own printed line shapes:

- **R1** every stdout line is one of the runner's three shapes (`mutant=…`, `mutbat counter=…`,
  `mutbat counter=… BASELINE-DIRTY …`).
- **R2** per graded counter, the number of `mutant=` lines == the summary's `mutants=`.
- **R3** per graded counter, the summary's `caught`/`equivalent`/`uncaught` == the **count** of
  `mutant=` lines carrying that verdict, and `caught+equivalent+uncaught == mutants`.
- **R4/R5/R6** per `mutant=` line: `verdict=caught ⟺ mutant_failures >= 1`;
  `verdict=equivalent ⇒ mutant_failures < 1`; `verdict=uncaught ⇒ mutant_failures < 1`.
  (This is the stdout projection of the runner's own predicate at `r46-mutbat.py:166-174`.)
- **R7** a `BASELINE-DIRTY` counter contributes no `mutant=` line and no summary line.
- **R8** the exit status is justified by the stdout: exit 0 requires every requested counter to
  have a summary line, every summary to report `uncaught=0`, and no `BASELINE-DIRTY` line.
- **R9** per graded counter, every `mutant=` line carries the summary's `baseline_failures` value, and it is 0.
- **R10** the `mutant=` ids == that counter's mutant-table ids, in order.

Two further tiers are reported but **never counted as a D1 kill**: **X1** (external input: a
`verdict=equivalent` mutant must have a committed proof file that exists — needs the `--equivalent`
map and the filesystem) and **O1** (an observation: a `mutant_failures=-1` line, the runner's
undocumented "no verdict at all" sentinel, which the **pristine** runner also emits).

A second, weaker tier **D2** (reference diff: the mutated stdout+exit vs. the pristine runner's
stdout+exit on the same scenario) is reported separately. D2 is *not* the output contract.

## 2. Results matrix (verdict per mutant × scenario)

`KILLED-D1` = the output contract is violated. `KILLED-D2` = contract holds, but the output differs
from the pristine runner's. `SURVIVED` = indistinguishable from the pristine runner's.

```
ID   CLASS                              S1         S2         S3         S4         S5         S6
B01  caught-when-failures-zero        KILLED-D1  KILLED-D1  KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1
B02  swap-caught-equivalent-in-summary KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1  SURVIVED   KILLED-D1
B03  swap-verdict-label-equivalent    SURVIVED   KILLED-D1  SURVIVED   SURVIVED   SURVIVED   SURVIVED
B04  equivalent-without-proof-file    SURVIVED   KILLED-D2  SURVIVED   SURVIVED   SURVIVED   SURVIVED
B05  exit-0-despite-uncaught          KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1  SURVIVED   KILLED-D1
B06  skip-a-mutant-silently           KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1  SURVIVED   KILLED-D1
B07  apply-failure-swallowed          SURVIVED   SURVIVED   KILLED-D2  SURVIVED   SURVIVED   SURVIVED
B08  baseline-dirty-ignored           SURVIVED   SURVIVED   SURVIVED   KILLED-D2  SURVIVED   SURVIVED
B09  uncaught-not-counted             KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1  SURVIVED   KILLED-D1
B10  verdict-label-uncaught-to-caught KILLED-D1  KILLED-D1  KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1
B11  exit-flag-not-set                KILLED-D1  KILLED-D1  SURVIVED   SURVIVED   SURVIVED   KILLED-D1
B12  mutant-count-lie                 KILLED-D1  KILLED-D1  SURVIVED   KILLED-D1  SURVIVED   KILLED-D1
B13  per-mutant-line-omitted          SURVIVED   SURVIVED   SURVIVED   SURVIVED   SURVIVED   KILLED-D1
M01  copy-failure-skipped-silently    SURVIVED   SURVIVED   SURVIVED   SURVIVED   KILLED-D1  SURVIVED
N01  do-nothing-control               SURVIVED   SURVIVED   SURVIVED   SURVIVED   SURVIVED   SURVIVED
```

Each mutant's edit was asserted to occur exactly once in the runner source, and the diff was
asserted to touch exactly one line (the harness aborts otherwise), so every entry above is a
single-line edit of `r46-mutbat.py`.

## 3. The four defect classes the seat spec names

### (a) "reports caught when failures==0" — **CAUGHT**

`B01` changes `r46-mutbat.py:166` from `if mf >= 1:` to `if mf >= 0:`. The battery then grades a
zero-failure mutant as caught. In S1:

```
mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=caught
mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=0 verdict=caught
mutbat counter=c1 mutants=20 caught=20 equivalent=0 uncaught=0 baseline_failures=0
mutbat counter=c2 mutants=21 caught=21 equivalent=0 uncaught=0 baseline_failures=0
```

This is the worst case in the matrix: **the summary reads as a clean pass** (`caught=20
uncaught=0`, exit 0). It is caught only because the *per-mutant lines* still carry
`mutant_failures=0`, so **R4** fires:

```
CONTRACT-FAIL B01-S1.txt
  VIOLATION R4 counter c1: mutant M06-L3-home-dropped verdict=caught but mutant_failures=0
  VIOLATION R4 counter c1: mutant M07-L3-home-no-abs verdict=caught but mutant_failures=0
  ...
```

**Load-bearing detail:** the detection lives entirely in the per-mutant lines. A reviewer who
reads *only* the `mutbat counter=…` summary line sees `caught=20 uncaught=0` and a clean exit.
The spec's own framing ("a reviewer diffing `mutbat … uncaught=<u> exit=` against the per-mutant
lines") is exactly right, and the per-mutant lines are what carry the signal.

### (b) "swaps caught/equivalent" — **CAUGHT (both variants), but one only with an `--equivalent` map**

`B02` swaps the two counts in the summary print (`r46-mutbat.py:177`):

```
mutbat counter=c1 mutants=20 caught=0 equivalent=13 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=0 equivalent=8 uncaught=13 baseline_failures=0
```

**R3** catches it (`summary caught=0 but 13 per-mutant lines say caught`).

`B03` swaps the verdict *label* on the equivalent branch (`r46-mutbat.py:171`:
`verdict = "equivalent"` → `verdict = "caught"`). This one is **only** caught when an
`--equivalent` map actually produces an equivalent verdict — i.e. in **S2**, not in S1:

```
S1 (no --equivalent map): the runner reports equivalent=0, so the swapped label is never used:
  mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
  -> SURVIVED (stdout byte-identical to the control)

S2 (--equivalent map with one real proof file):
  mutant=G1c-src-boundary baseline_failures=0 mutant_failures=0 verdict=caught
  mutbat counter=c2 mutants=21 caught=8 equivalent=1 uncaught=12 baseline_failures=0
  -> KILLED-D1: R4 (verdict=caught but mutant_failures=0) and R3
```

**Consequence for the wave:** the `equivalent` branch of the runner is *unexercised* by the frozen
receipt (`controls/mutbat-before.txt` shows `equivalent=0` for both counters). Any reviewer
mutation-testing the `equivalent` path must supply `--equivalent`; otherwise the mutants are
invisible. This is a coverage statement about the **battery's own test surface**, not a defect in
the runner.

`B04` (drops the `os.path.isfile(eq[mid])` check, so a mutant is credited equivalent although its
proof file does not exist) is **NOT caught by the output contract**: the stdout stays internally
consistent (`verdict=equivalent` with `mutant_failures=0` satisfies R5). It is caught only by the
external tier X1, which needs the `--equivalent` map *and* the filesystem:

```
CONTRACT-OK B04-S2.txt
  EXTERNAL X1 counter c2: mutant G2a-verified-prefix verdict=equivalent but proof file
         /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/NO-SUCH-PROOF.md does not exist
```

**This is a genuine gap in the output contract:** "equivalent" is the runner's only non-mechanical
verdict, and nothing in the stdout says *which* proof justified it. A reviewer cannot detect a
forged equivalent from the runner's own output; the `--equivalent` map must be checked separately.

### (c) "skips a mutant silently on copy failure" — **CAUGHT, but only when the copy actually fails**

`M01` (2-line) adds `except Exception: continue` around the mutant application so a failed copy is
swallowed and that mutant is skipped. In **S5** (the copy fails):

```
mutbat counter=c1 mutants=20 caught=0 equivalent=0 uncaught=0 baseline_failures=0
mutbat counter=c2 mutants=21 caught=0 equivalent=0 uncaught=0 baseline_failures=0
```

**0** per-mutant lines, yet the summary claims `mutants=20`/`mutants=21`. **R2/R3/R10** all fire:

```
CONTRACT-FAIL M01-S5.txt
  VIOLATION R2 counter c1: summary mutants=20 but 0 per-mutant lines were printed
  VIOLATION R3 counter c1: caught+equivalent+uncaught=0 != mutants=20
  VIOLATION R10 counter c1: per-mutant ids differ from the mutant table (0 printed vs 20 in table, order different-set)
```

The pristine runner in S5 does not skip: it dies with a traceback (loud failure), which is the
documented intent (`r46-mutbat.py:14-15`, "a drifted counter fails loudly instead of mutating the
wrong line"). So the mutant converts a loud failure into a **silent** one that reads like a clean
run — and R2/R3/R10 catch it because the summary's `mutants=` is the *table* length, not the number
of lines actually printed. This is the strongest argument for keeping the per-mutant line count
bound to the summary: it is what makes a silent skip visible.

`B13` (omits the `mutant=` line when the selftest produced no verdict) is caught in **S6** only
(`mutant_failures=-1`); in the other five scenarios `mf` is never negative, so the mutant is inert.

`B06` (skips the last mutant of the table via `mutants[:-1]`) is caught by R2/R3/R10 in S1/S2/S4/S6:
the summary still claims `mutants=20` while 19 lines were printed.

### (d) "exits 0 with uncaught>0" — **CAUGHT, but only via the exit status**

`B05` changes `r46-mutbat.py:180` from `return 1 if bad else 0` to `return 0`; `B11` changes
`bad += 1` to `bad += 0`. Both are caught by **R8**:

```
B05 S1: CONTRACT-FAIL B05-S1.txt
  VIOLATION R8 exit status 0 but a summary reports uncaught>0
B11 S1: CONTRACT-FAIL B11-S1.txt
  VIOLATION R8 exit status 0 but a summary reports uncaught>0
```

**Load-bearing detail, and the most important finding of this seat:** in S1 the mutated runner's
stdout is **byte-identical** to the pristine runner's —

```
$ diff out/CONTROL-S1.txt out/B05-S1.txt && echo IDENTICAL
IDENTICAL stdout
```

— so *only* the process exit status distinguishes them (pristine `rc=1`, mutant `rc=0`). This makes
**R8** (and the exit status) load-bearing for the whole "exits 0 with uncaught>0" class.

## 4. The documentation/contract defect this exposed (evidence for L1)

`r46-mutbat.py:26` (the docstring's OUTPUT section) promises the summary line ends with
`exit=0|1`:

```
    `mutbat counter=<c> mutants=<n> caught=<k> equivalent=<e> uncaught=<u> baseline_failures=<b> exit=0|1`
```

The implementation at `r46-mutbat.py:176-177` never prints that field:

```
        print("mutbat counter=%s mutants=%d caught=%d equivalent=%d uncaught=%d baseline_failures=0" %
              (which, len(mutants), caught, equivalent, uncaught))
```

`grep -n "exit=" r46-mutbat.py` finds the string **only in the docstring**; the frozen receipt
confirms the printed form carries no `exit=`:

```
$ grep '^mutbat ' .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

(The receipt's trailing `BATEXIT=1` is the *harness's* line, not the runner's — the runner never
emits it.)

**Consequence.** The runner's own documented output contract is not met, and the missing field is
exactly the one that carries the exit status. Since the "exits 0 with uncaught>0" defect class is
detectable *only* by the exit status (§3d — stdout is byte-identical), a reviewer working from the
documented contract would look for `exit=` in the summary line and find nothing. Two options for
L1, both one-line:
1. print the field the docstring already promises (`exit=%d` at the end of the summary line), or
2. amend the docstring to drop `exit=0|1` and state that the exit status is the process exit code.

Recommendation: **option 1** — it makes the exit status self-describing in the runner's own output,
which is what the R8 class of detection needs, and it closes the docstring/implementation mismatch
without changing the receipt's summary fields that `freeze.txt` and `claims.json` quote (the extra
trailing field is additive).

Note for integration: this is an **errata proposal for L1**, not a change I made. The committed
runner is read-only for this seat and is byte-unchanged (`sha256` still
`f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`).

## 5. Which defect classes the output contract does **not** catch

Three of the sixteen mutants are never caught by the output contract (D1) in any scenario:

| mutant | class | why D1 misses it | what does catch it |
|--------|-------|------------------|--------------------|
| `B04` | equivalent-without-proof-file | the stdout stays internally consistent; nothing says *which* proof justified an `equivalent` verdict | the external X1 rule (needs the `--equivalent` map + filesystem) |
| `B07` | apply-failure-swallowed (the drift guard `raise SystemExit` → `return None`) | the mis-graded mutant is printed with a normal-looking line; in the scenarios where no anchor has drifted the mutant is inert | D2 only, and only in S3 where the pristine runner aborts loudly and the mutant does not |
| `B08` | baseline-dirty-ignored (`if baseline != 0:` → `if baseline == 999:`) | the dirty-baseline counter is graded anyway; every mutant line reads `mutant_failures=-1 verdict=uncaught`, which satisfies R4/R5/R6 | D2 only (S4): the pristine runner prints `BASELINE-DIRTY` and grades nothing, the mutant prints 20 lines |

`B07` and `B08` share one root cause worth reporting: **the runner's output does not distinguish
"the selftest ran and found nothing" from "the selftest never ran"** — both surface as
`mutant_failures=-1 verdict=uncaught` (the O1 observation tier). That sentinel is undocumented in
the runner's docstring and is not derivable from any other field on the line. A reviewer reading
the runner's own output cannot tell a genuine coverage hole (`mutant_failures=0`) from a crashed
selftest (`mutant_failures=-1`) without out-of-band knowledge.

Additionally, `B03` (the equivalent-label swap) is caught **only** when `--equivalent` is supplied
(§3b) — the frozen receipt exercises the `equivalent` branch zero times.

## 6. Discrimination against the do-nothing control

`N01` (comment-only, one line) is byte-identical to the control in all six scenarios (§0), and the
six **pristine** control runs are `CONTRACT-OK` in all six scenarios. Every `KILLED-D1` in §2 is
therefore caused by the mutant's semantics, not by the checker being trigger-happy or by the
harness perturbing the run. The `SURVIVED` cells are likewise real: in each of them the mutated
runner's stdout **and** exit status are indistinguishable from the pristine runner's.

## 7. Limitations

1. **The stub replays recorded counts.** The harness's selftest stub returns the frozen
   per-mutant failure counts (`controls/mutbat-before.txt`) keyed by counter sha256, instead of
   re-running the ~10-minute real selftests. This is sound for attacking the *runner's* logic
   (proved: the runner's output over the stub tree is byte-identical to the frozen receipt), and
   one real spot-check confirms the replayed value itself (§7.2). It does **not** re-verify every
   count, and it says nothing about the counts at the tip. **The tip's real per-mutant counts must
   come from a real battery run, not from this harness.**
2. **Real-selftest spot-checks completed and confirm the stub's replay.** Two real runs against the
   real selftests, with the mutated counter images the battery itself would build:

```
$ python3 -B corpus/instruments/r46-counters-selftest-c1.py --lane $S/tree --pure $S/pure \
      --counter $S/dst-c1/corpus/instruments/r46-c1-gate.py --work $S/real3/c1d --jobs 2
...
selftest cases=76 failures=26

$ python3 -B corpus/instruments/r46-counters-selftest-c2.py --lane $S/tree --pure $S/pure \
      --counter $S/dst-c2/corpus/instruments/r46-c2-gate.py
...
selftest cases=137 failures=94
```

   against the frozen receipt's `mutant=M01-L1-target-24 … mutant_failures=26 verdict=caught` and
   `mutant=G3c-kind-dead … mutant_failures=94 verdict=caught`. **Both replayed counts are
   confirmed against the real selftests**, so the stub table is not merely self-consistent with the
   receipt. (Both runs were slow only because of host contention from sibling seats: load average
   ~200–254 with 44–53 concurrent `r46-counters-selftest` processes, `cat /proc/loadavg` →
   `253.99 268.47 258.07`; the c2 run took ~28 min under that load.)

   These two spot-checks confirm **2 of the 41** replayed counts. The other 39 are the frozen
   receipt's values, re-used verbatim and not re-derived by me.
3. **The scenario trees are synthetic.** S3 (drift), S4/S6 (crashing selftest) and S5 (unreadable
   file) are constructed failure modes, not states the committed corpus can currently reach. They
   exist to reach the runner's failure branches; they do not assert that those branches are
   reachable in production.
4. **`B03`'s catch is map-dependent** — see §5. The `equivalent` branch needs `--equivalent` to be
   exercised at all.
5. **Single-line discipline was enforced by the harness** (anchor occurs exactly once; exactly one
   line differs), but `M01` is a deliberate 2-line edit (it needs an `except` clause) and is
   labelled as such everywhere.
6. **Only the runner was mutated.** The two counters, the two selftests and the frozen claims were
   read-only throughout; the lane was not modified except for this report and the draft dir.

## 8. Tools

No tools were installed or upgraded for this seat (nothing was missing); the host tooling directive
was read and satisfied vacuously. Everything ran on the host's `python3` (3.14.8) with the stdlib
only, plus `git archive` for the read-only base export. No `pacman` transaction was attempted.

## 9. Evidence index (all under the seat's scratch, removed at exit)

- `mutate_battery.py` — the harness (scenario builder, mutant table, runner, verdict logic).
- `contract_check.py` — the D1/X1/O1 checker.
- `stub-selftest.py` — the replay stub.
- `out/CONTROL-S{1..6}.txt`, `out/{B01..B13,M01,N01}-S{1..6}.txt` (+`.err`, `.cmd`) — every run's
  stdout/stderr/exact command line.
- `spotcheck/real-c1-M01.txt`, `spotcheck/real-c2-G3c.txt` — the two **real**-selftest fidelity
  runs (`selftest cases=76 failures=26` and `selftest cases=137 failures=94`).
- `results.json` — the machine-readable matrix.
- Copies of the harness, the checker and the result matrix are in this seat's draft directory
  `.ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/`.

**Reproducibility.** Each run's exact command line is stored next to its output (`*.txt.cmd`). The
control run in S1:

```
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py \
  --root /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/sc-S1 \
  --pure  /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/pure \
  --work  /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/work/CONTROL-S1/w \
  --counter both --jobs 8
```

and the `M01` (copy-failure-skipped) kill in S5 differs only in the runner path
(`…/mutbat-M01.py`, the scratch copy carrying the 2-line edit):

```
/usr/bin/python3 -B /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/mutbat-M01.py \
  --root /fast/scratch/hyaku/kasegi-r46/R46bMutBattery/sc-S5 … --counter both --jobs 8
```

The mutant copies are scratch files; the committed runner was never the target of an edit:

```
$ diff mutbat-B05.py <lane>/corpus/instruments/r46-mutbat.py
180c180
<     return 0
---
>     return 1 if bad else 0
```

## 10. Recommended L1 actions (not performed by this seat)

1. Close the docstring/implementation mismatch on the `exit=0|1` summary field (§4). One line.
2. Record in the wave's errata that the runner's `equivalent` branch is unexercised by the frozen
   receipt and that mutation-testing it requires `--equivalent` (§3b).
3. Consider documenting the `mutant_failures=-1` sentinel in the runner's docstring, since the
   runner's own output currently cannot distinguish "selftest found nothing" from "selftest never
   ran" (§5).

Nothing here contradicts the frozen claims: the frozen receipt is reproduced byte-identically by
the pristine runner, and this seat's mutants are scratch copies only.
