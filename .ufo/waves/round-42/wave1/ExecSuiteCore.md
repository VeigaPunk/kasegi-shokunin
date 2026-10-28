# ExecSuiteCore — round-42 C1 `corpus/instruments/r42-closure.sh` (J1–J13)

Seat **ExecSuiteCore** (executor, leaf). Lane `kasegi-shokunin`. Base
`5053a7f46de35784cff4b56756906e9014a38276`. Judged-head candidate at the final
run: `f66b8e05946ef20720b26cc4b71d6c9dfd18afc7` (the L1's J; the lane tip moved
to `d238e36c` after my last edit, which still carries an older suite — see §6).

Nothing was installed, no network fetch, no pacman, no mutating git command
anywhere. Scratch `/fast/scratch/hyaku/kasegi-r42/ExecSuiteCore` is removed
before yield.

## Deliverables (beside this receipt)

| file | lines | sha256 |
|---|---|---|
| `ExecSuiteCore.r42-closure.sh` (landable suite, byte-exact) | 2175 | `177a33a2dc2b85c69a1e6eaa02ec3fd2990a1ff77724a70164d33ac71b68a160` |
| `ExecSuiteCore.transcripts.txt` (teed observed runs) | 130 | `9ac1574e603ea53ac23806777192db9d93b15c07346021f3b14f4c24d5b143a8` |

Self-contained: `bash` + `python3` + coreutils, plus `git` and `tar` for the
export. No network, no `source` of any sibling artifact — a closure suite that
has to fetch its own limbs cannot be replayed from an export.

## 1. Shape (the C1 predicate, implemented literally)

* **Export mode only.** A plain run prints `r42-closure: a plain run is refused
  (export mode only)` and exits 2. The tree comes from
  `git -C <lane> archive <resolved> | tar -x -C <work>/export`, `<work>`
  defaulting to `<scratch-root>/r42-<ref12>/work`, outside the lane.
* **An unresolvable ref is a red, not a pass**: `ERROR ref-not-found ref=<arg>
  closed=0 exit=1`, exit 1.
* **Run transcript** (19 lines): `all-gates v2`, `export-ref`,
  `suite-sha256`, `time-basis=ref-commit`, `run-utc`, thirteen
  `J<n> payload=... closed=0|1` lines in J1..J13 order, `closed=<n>/13 exit=0|1`.
* **Receipt** (`--receipt-out`): those 19 lines plus the thirteen graded
  `selftest case=J<n> ...` lines and `selftest cases=13 failures=<k>` — 33 lines,
  the teed transcript of run + selftest. `run-utc` is the committer instant of
  the named ref, never wall-clock.
* **`--selftest --export-ref`** prints only the thirteen graded lines and the
  summary (14 lines), exit 0 only on zero failures.

## 2. Measured at `f66b8e05` — the whole predicate

```
closed=13/13 exit=0
selftest cases=13 failures=0        (exit 0; every case positive=pass payload-match=1)
```

| J | family | payload at J |
|---|---|---|
| J1 | F-EVID | `records=1,blocks=2,graded=1,evidence=2,missing=0,wrong-grade=0,per-record=SCORECARD.md=2/2;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=rejected` |
| J2 | F-TOKEN | `boundary=10/10,truth-tokens=3,stated=3,mangled=0,truth-stated=1,token=whole,replay=RevC1Counters.defeats.txt=rejected` |
| J3 | F-TABLE | `tables=18,rows=73,r42-rows=1,r40-rows=1,r40-split=0,bare=0,lead=0,replay=MutSkillTablePipes.md=3/3` |
| J4 | F-DECL | `declared=324,valid=323,missing=0,escape=0,stale=0,coverage=11/11,file=present,replay=CritDeclarationCoverage.md=2/2` |
| J5 | F-SCAN | `strays=8,scanned=8,read=ok,outside=2,outside-scanned=10,scope=materialized,replay=MutScratchTiming.md=outside=detected,inside=detected` |
| J6 | F-BIND | `instrument=present,base=1,missing-path=1,url-mutated=1,digest-mutated=1,rule=reject,replay=MutBindingExistence.md=rejected` |
| J7 | F-FLIP | `instrument=present,base=1,status-flip=1,no-pass=1,rows=25,admitted=25,replay=MutFrontierParser.md=rejected` |
| J8 | F-RCPT | `sentinel=1,lines=1,ref=1,digest=1,time-basis=1,utc=1,ancestor=1,diff=1,run-lines=1,selftest-lines=1,verdicts=1,summary=1,closed-line=1,no-stray=1,payload-match=1,forged=1,payload-match=12/12,forged=6/6` |
| J9 | negatives | `depth=1,base=1,r41=1,accept=tree-red,cap=nested` |
| J10 | isolation | `cases=13,isolated=13,canary=0,graded-lines=13,fixture=synthetic` |
| J11 | F-CORR | `corrections=33,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0` |
| J12 | no-harm | `deleted=0,density=1,density-sha=ee803726a322,diff-read=ok,base=5053a7f4` |
| J13 | quiescence | `faithful=1,extra=0,missing=0,scratch-strays=0,scratch-read=ok,markers=0,named=1` |

Control refs, same bytes:

* base `5053a7f4…` → `closed=5/13 exit=1`
* round-41 judged head `1f74646…` → `closed=4/13 exit=1`

Both satisfy `closed<13/13 exit=1`. At base the red set is
J1 (no round-42 correction lines), J2 (`stated=0`), J3 (`bare=5`,
`r40-split=1`, no r42 row), J4 (`file=absent`), J6 (`digest-mutated=0`, replay
accepted), J7 (`status-flip=0`, replay accepted), J8, J11 (`unexcused=4`, no
marker), J12; at the r41 head J12 is red too, with `deleted=1` —
`corpus/lessons/round-41-verifier-spotcheck.md` is deleted between base and that
ref, and the no-harm guard catches it.

## 3. Replay limbs

J1–J7 each carry an inline REPLAY limb: it re-executes its family's **committed**
defeat artifact (bound by sha256, all seven verified byte-identical to
`.ufo/waves/round-4*/wave2/`) against the current suite bytes and requires
rejection. An artifact whose bytes are not the pinned commit is reported
`artifact-missing:<name>` and the limb fails — a missing defeat cannot be graded
as repaired. The selftest additionally re-runs each limb as `mutants=<ok>/<n>`.

## 4. Three defects this seat found and closed in its own suite

All three were holes in **my** checks, not in the lane's work, and all three were
found by the L1's re-run at `f66b8e05`:

1. **J1's replay stripped the wrong round.** `replay_j1` (and the selftest's
   `strip_evidence_copy`, and `replay_j2`'s tally mangling) selected "the first
   Correction line that mentions a claim" with no round filter, i.e.
   `Correction (round 39)` at SCORECARD.md 1560 / LOG.md 1719 / SHONEN.md 221. J1
   only grades round-42 lines, so blanking a round-39 line left J1 green and the
   limb reported the mutant **accepted** — a defeat that is not really replayed.
   It looked healthy earlier only because SCORECARD.md 1632 still had
   `missing=1`, which made the mutant red for the wrong reason. Fixed: strip and
   mangle only lines whose round is 42, and only lines that actually **carry** a
   resolvable identifier, so the mutant can never be vacuous. Evidence
   resolution now also runs against the fixture tree, so a mutant cannot borrow
   identifiers from the live export.
2. **J4 counted the receipt as a defect.** The receipt is the artifact the run
   produces, so it can never exist inside its own export; folding "declared but
   absent" into `escape` made a correct 324-line declaration read
   `declared=324,valid=323,escape=1`. Fixed: `escape` now means only
   absolute/`..`/symlink-outside-root, an absent declaration is `stale` and is
   reported with `stale-first=<path>`, and the receipt path is exempt from the
   stale rule.
3. **J8 and J10 were self-referential, and the fixed point did not converge.**
   J10's payload folded other cases' verdicts into `graded-lines`, and J8's
   canonical block contained J8's own line, so a green tree could never produce
   `failures=0`. Fixed: `graded-lines` counts well-formed graded lines (always
   13 — J10 grades isolation, not other verdicts), and J8's payload is resolved
   against a synthetic clean block before the cases run, so it is knowable in
   one pass. The receipt's strict facts (`verdicts`, `summary == (13,0)`) are
   back.

## 5. Why the receipt can be written at J and re-derived at Y

At J no receipt exists yet, so J8 grades a **canonical** transcript built from
the run's own payloads. Every payload is a pure function of the exported tree —
no wall clock, no host path, no `$TMPDIR`, no ref name (J13's payload
deliberately drops the ref it was measured at) — so the twelve deterministic
payloads recorded at J re-derive byte-identically at Y and `payload-match` is
12/12 on both sides. J8 alone is excluded from that comparison. The receipt's
`run-utc` is the committer instant of J, and `diff` requires at most one changed
path between the named ref and the current one — the receipt itself.

## 6. State of the lane at wrap-up (for the L1 / operator)

The L1 committed `d238e36c` carrying suite `d92c0de1…`, which is **not** the
final build; its receipt at `J=d238e36` reports `closed=9/13 exit=1`. The final
build `177a33a2…` is measured green at `f66b8e05` but is a wave-1 artifact, not
a commit. To converge, the L1 needs to: copy
`wave1/ExecSuiteCore.r42-closure.sh` to `corpus/instruments/r42-closure.sh`,
commit that as J, then run
`--export-ref <J> --receipt-out .ufo/waves/round-42/final-gates/all-gates.txt`
and commit the receipt as Y. The 324-line declared-blocks file that is already
landed is sufficient; the 465-line regeneration is not required on my account.

## 7. Risks a falsifier should attack

* **J1 accepts any resolvable identifier** (a path, a 40-hex commit, or a known
  defeat stem) on a correction line; it does not judge whether the identifier is
  the *right* one. The defect it does close is the union: evidence stripped from
  one record's round-42 line reds it.
* **J6/J7 depend on the patched instruments** (`capture-binding-check.py`,
  `frontier-recheck-count.py`) being the landed bytes; both are green at
  `f66b8e05`.
* **J9 costs two nested depth-1 exports per run** (~150 s of the ~250 s total).
  That is the price of a negative control that is tree-red rather than cap-red;
  the cheap variant is the M-H8a defect.
* **J13 reads the live lane index** for skip-worktree markers (0 today).
* The suite never writes the lane, never commits, and removes nothing outside
  `<scratch-root>`.
