# R46bRevMutbat — attack review of the mutation battery `corpus/instruments/r46-mutbat.py`

VERDICT: INFO — the battery is sound on its committed inputs (all 41 mutant triples are live,
single-occurrence, bytecode-effective edits; the frozen before-value reproduces in prefix), but the
battery enforces only half of the claim's caught-or-equivalent predicate by itself. Three
verification gaps exist; each is demonstrated live below. The C1 claim's kill rule already covers
all three by manual reviewer action (empty-proof kill, do-nothing control, falsified-equivalence
kill) — nothing here breaks the claim — but no receipt the battery PRINTS proves them. The
receipts the after-value run must carry are listed in §6.

Scope: the battery only (per seat spec). All commands run by this seat; scratch
`/fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/` (removed after the report lands; receipts quoted
inline). No tools installed (stdlib only). Lane instruments never written; the only writes under
the lane are this Report.

## 1. Mutant-table audit: no dead-text triples (item 1)

Method: for every triple in `C1_MUTANTS`/`C2_MUTANTS` (imported from the frozen battery,
sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8` — matches freeze.txt),
(a) count occurrences of `old` in the target gate, (b) classify the occurrence's token context
with `tokenize` (COMMENT / STRING / CODE), (c) apply the edit and compare against the pristine
gate both as an AST with docstrings stripped and as `dis` bytecode text. An edit landing in dead
text leaves both identical.

Command: `python3 /fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/audit_triples.py` (script kept in
scratch until this report landed; logic reproduced inline below). Verdict line of its output:

```
total triples: 41
dead/no-op or drifted: NONE
```

Every triple occurs EXACTLY ONCE (the battery's own drift assert at r46-mutbat.py apply_mutant
therefore holds for both tables today) and every edit changes the compiled bytecode (`EFFECTIVE`
for 41/41). One nuance worth naming: `c1 M05-L3-shape-loose` is the only triple whose `old`
(`(?:[ \t]+#.*)?$`) classifies as a STRING token — it sits inside the raw-string regex of
`exact_line()` at `corpus/instruments/r46-c1-gate.py:73`. That string IS the operative pattern
(the edit relaxes the exact-recheck-line shape and was graded caught, mutant_failures=3, in
controls/mutbat-before.txt); bytecode comparison confirms the edit is live. No triple lands in a
comment or docstring; no drifted counter.

Discriminator against a do-nothing audit: the check is not "does the substring match" (all 41
match) but "does the compiled program change" — a comment-only edit compiles to identical
bytecode and would have been flagged `NO-OP-EDIT`. None was.

## 2. Baseline: `failures=0` with zero cases graded is accepted (item 2) — MEDIUM, tool gap

The battery parses exactly one datum from the selftest (`r46-mutbat.py:107-108`):

```
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-2000:]
```

`p.returncode` is never inspected; no case census is parsed; stderr is dropped. Demonstrations
against the REAL unmodified battery binary, using a scratch tree whose only content is the two
gate files plus a stub selftest that prints a green summary and grades nothing:

```
$ cat stubtree/corpus/instruments/r46-counters-selftest-c1.py
import sys
print("selftest cases=0 failures=0")
sys.exit(0)

$ python3 corpus/instruments/r46-mutbat.py --root $S/stubtree --pure $S/pure2copy \
    --work $S/work-stubA --counter both --jobs 8
...
mutbat counter=c1  mutants=20 caught=0 equivalent=0  uncaught=20 baseline_failures=0
mutbat counter=c2  mutants=21 caught=0 equivalent=0  uncaught=21 baseline_failures=0
EXIT=1
```

The do-nothing control is NOT green without the equivalent map (good: the uncaught bucket does
the work), but note `baseline_failures=0` — the "baseline must be clean" gate is passed by a stub.
Second variant, stub exits 1:

```
$ cat stubtree-exit1/.../r46-counters-selftest-c1.py
import sys
print("selftest cases=0 failures=0")
sys.exit(1)

$ python3 corpus/instruments/r46-mutbat.py --root $S/stubtree-exit1 --pure $S/pure2copy \
    --work $S/work-stubC --counter c1 --jobs 8
mutbat counter=c1 mutants=20 caught=0 equivalent=0 uncaught=20 baseline_failures=0
```

A selftest that graded nothing, printed `cases=0`, and EXITED 1 still reads baseline_failures=0.
The battery's trust model is: the tree's selftest is honest. For the committed selftests that
holds (§3); the receipt, however, never proves it.

## 3. The committed selftests: no skip path found (item 2, negative result)

Read of both committed selftests plus targeted runs:

- Single print site: `grep -n 'failures=' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py` prints exactly two live lines — the final summaries (`selftest-c1.py:670`, `selftest-c2.py:614`; the other two hits are docstrings). The battery's last-match regex cannot be fed a stale per-case `failures=0` by these files as committed.
- c1 pool: `cf.ThreadPoolExecutor(max_workers=max(1, a.jobs))` + `results.extend(ex.map(one, CASES))` (selftest-c1.py:626-627). `map` collects in submission order and re-raises any worker exception into the main thread during `extend` — an exception in any case recipe or counter run kills the process BEFORE the summary line; the battery then reads no `failures=` and gets -1 (for a mutant: verdict uncaught; for the baseline: BASELINE-DIRTY). No per-case try/except exists anywhere in either selftest (grep `except` in both files: only `OSError`/subprocess hygiene in helpers, none wrapping case bodies).
- Case registration cannot silently drop: c2 `add = C.append` (selftest-c2.py:364); c1's `ROWLEVEL` rebuild (selftest-c1.py:535-546) rewrites targets and appends a stubbed-gate variant per row-level case — statically counted, the rebuilt table has 72 entries, plus the 4 serial results (TIP-7of7, CONTROL-do-nothing, HOME-bounties-do-nothing, HOME-bounties-tip) = 76, matching controls/selftest-baselines.txt `selftest cases=76 failures=0`. Programmatic name-uniqueness check on the 72: no duplicates.
- A silently-nooping recipe is loud: a `mut` case whose tree ends unmutated reads fixed=7 and is counted a failure (selftest-c1.py:657-661 `rejected = fixed < 7 or rc != 0`; selftest-c2.py `if fixed == 7: reasons.append("tree read 7/7")`).
- Both counters fail closed: c1 gate wraps `gate_list` in `except Exception` → all seven limbs red (`r46-c1-gate.py:372-375`); c2 wraps each gate fn → `exception-<name>` red (`r46-c2-gate.py:360-365`).
- --jobs race: first-party evidence. `--jobs 8` and `--jobs 1` runs of the c1 selftest at the
  base export both print `selftest cases=76 failures=0` (exit 0), and their per-case lines are
  byte-identical:

  ```
  $ diff <(grep '^case ' stbase-c1.txt) <(grep '^case ' stbase-c1-jobs1.txt) && echo IDENTICAL
  IDENTICAL: all 76 per-case lines match between --jobs 8 and --jobs 1
  ```

  (74 verdict=OK + the two disclosed `residual` readings — R-rows-inside-code-fence
  RESIDUAL-NOW-RED and R-claim-text-unrelated-to-anchor RESIDUAL-FALSE-GREEN; both printed, not
  counted, matching the committed receipt's residual line.) No case-count or verdict drift, and
  the ordered `ex.map` collection gives no aggregation channel for a race to hide a case.

So: a selftest printing `failures=0` while systematically skipping cases is not reachable in the
committed selftests by any path I could construct; it is reachable the moment a tree supplies its
own selftest (§2), which is exactly what the claim's do-nothing-control kill rule exists to catch
manually.

## 4. Equivalent classification: an empty proof file is accepted (item 3) — HIGH, tool gap

The whole acceptance test (`r46-mutbat.py`, main loop):

```
            if mf >= 1:
                caught += 1
                verdict = "caught"
            elif mid in eq and os.path.isfile(eq[mid]):
                equivalent += 1
                verdict = "equivalent"
```

`os.path.isfile` is true for a 0-byte file. End-to-end demonstration with the real battery
binary: one empty file mapped for all 41 mutant ids.

```
$ stat -c '%s bytes %n' $S/EMPTY-PROOF.txt
0 bytes /fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/EMPTY-PROOF.txt
$ python3 corpus/instruments/r46-mutbat.py --root $S/stubtree --pure $S/pure2copy \
    --work $S/work-stubB --counter both --jobs 8 --equivalent $S/allempty-eq.json
mutant=M01-L1-target-24  baseline_failures=0 mutant_failures=0 verdict=equivalent
... (41 lines, all verdict=equivalent) ...
mutbat counter=c1 mutants=20 caught=0 equivalent=20 uncaught=0 baseline_failures=0
mutbat counter=c2 mutants=21 caught=0 equivalent=21 uncaught=0 baseline_failures=0
EXIT=0
```

Zero cases graded, zero-byte proofs, `uncaught=0`, exit 0. Two aggravating facts:

1. The same branch covers harness crashes: `run_selftest` returns -1 when no `failures=` line is
   printed (selftest died), and `mf >= 1` is false for -1, so a crashed mutant run is also
   "equivalent" whenever a proof path is on file. The battery cannot distinguish "the selftest
   ran and the mutant is benign" from "the selftest never ran".
2. On the real base tree today, 20 mutants sit at mutant_failures=0 (c1: M06 M07 M13 M14 M18 M19
   M20; c2: G1c G2a G2b G2c G3a G4b G5c G6a G6b G6c G7a G7b G7c — controls/mutbat-before.txt,
   sha256 13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd, matching freeze.txt).
   An all-empty map on the REAL tree flips exactly those 20 to equivalent and prints the
   claim's after-shape (`caught+equivalent=mutants, uncaught=0, baseline_failures=0`) with no
   selftest extension ever written. I did not complete a full real-tree empty-map run in seat
   budget (a full battery pass is ~20 min per c1 mutant; §5) — the mechanism is proven on the
   real binary via the stub tree and the branch is the same three lines for any tree.

The claim's kill rule anticipates this ("an equivalent verdict's proof file is missing, empty, or
falsified … kills the claim") — but that kill is enforced by reviewers reading the map, not by
the battery. Nothing in the printed receipt distinguishes the forged run above from an honest
one except the (unhashed, unvalidated) proof paths.

## 5. Reproduction of the frozen before-value (prefix)

Full command (claim counter_cmd shape): `python3 corpus/instruments/r46-mutbat.py --root
/fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/base-export --pure
/fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/pure2copy --work .../work-repro --counter both
--jobs 8`, where base-export is `git archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus`
and pure2copy is a byte-copy of the L1's pure2 export. Environment validity checked first:
`git diff 04af9bc9..HEAD` over the two gates + two selftests is empty, and the battery's sha256
matches freeze.txt (both quoted in §1/§4).

My run's surviving output before the seat's 3500s wall:

```
mutant=M01-L1-target-24  baseline_failures=0 mutant_failures=26 verdict=caught
mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=8 verdict=caught
```

Identical to the first two lines of controls/mutbat-before.txt (M01=26, M02=8) after an identical
clean c1 baseline — the frozen environment reproduces. Completing all 41 mutant runs is infeasible
in this seat's budget (the two c1 mutants plus baseline consumed ~58 min; the committed receipt
required a much longer wall). Limitation, not a discrepancy: no line I produced contradicts the
committed receipt, and the two reproduced lines are the strongest-variance ones (26 and 8
failures).

Selftest baselines re-run by this seat at the base export (first-party cases= evidence; the
battery itself never prints a case count):

```
$ python3 $S/base-export/corpus/instruments/r46-counters-selftest-c1.py \
    --pure $S/pure2copy --work $S/work-stbase-c1 --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
EXIT=0

$ HYAKU_SCRATCH=/fast/scratch/hyaku python3 $S/base-export/corpus/instruments/r46-counters-selftest-c2.py \
    --pure $S/pure2copy
selftest cases=137 failures=0
EXIT=0
```

Both match controls/selftest-baselines.txt exactly (76/0 and 137/0; c1 wall ~13 min at
--jobs 8, ~34 min at --jobs 1, c2 ~11 min). The --jobs 1 c1 run is the race-control arm of §3.

## 6. Receipts the C1 after-value must require (proposal)

R1. Battery-side honesty check: require the selftest exit code 0 AND parse `cases=(\d+)` from the
same summary; print `cases=` into every mutant line and both summaries; refuse baseline=0 when
cases=0 or rc!=0. Kills §2's stub acceptance at the tool level.
R2. Proof-file receipts for every equivalent verdict: (a) size floor (>0, e.g. >=256 bytes);
(b) the file names the mutant id and the targeted clause and argues verdict-invariance on every
input class (the claim's kill rule already demands this of the text — the battery should demand
of the file that it EXISTS as text: non-empty, committed under `.ufo/waves/round-46/attempt2/`,
never under /tmp or scratch); (c) the battery sha256s each proof file into its receipt; (d) a
reviewer falsification pass on each equivalence (already in the kill rule) with the constructed
input quoted in the wave record.
R3. Crash != equivalent: when `mutant_failures == -1` (no summary line — selftest died), the
verdict must be `error`, never eligible for the equivalent branch. Kills §4 aggravator 1.
R4. Do-nothing control pair recorded next to the after-run: (i) base selftest at the base export
reproduces the committed before pair (c1 uncaught=7, c2 uncaught=13) — the claim already requires
this; (ii) a stub-selftest tree (prints `failures=0`, grades nothing) grades uncaught=41 / exit 1
under the wave's real --equivalent map. (ii) is the control that fails today if the map's proofs
are empty — see §4.
R5. Receipt completeness: the battery should persist each mutant's selftest stdout tail (it
currently keeps the last 2000 chars in memory and prints them only on a dirty baseline) so the
after-run receipt is independently auditable line-by-line.

## 7. Limitations

- Full-battery and full-real-tree empty-map runs did not complete in seat budget; §4's real-tree
  flip is proven by the branch (three lines, quoted), the real-binary stub-tree run (41/41), and
  the 20 real mf=0 mutants named from the hashed committed receipt.
- §3's exception-path analysis is code inspection plus targeted greps, not a fuzzing campaign;
  the two first-party baseline re-runs (§5) back the case-count half.
- The c2 selftest reads its snapshot/manifest/knowledge inputs from `--lane` (default = the live
  lane, e.g. selftest-c2.py:73 `Snap(a.lane)`); a battery receipt is reproducible only while the
  lane corpus is frozen. The freeze record covers this; noted so the after-run records the lane
  rev next to the receipt.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevMutbat/` removed after this report was written;
  every material output is quoted inline above.
