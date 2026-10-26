# ExecNoHarmFixture — M38-7 misroot reproduction and guard proof (kasegi round 39)

Seat: `ExecNoHarmFixture` (leaf executor), lane `kasegi-shokunin`, milestone round-39.
Base commit `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims-freeze `dcd31701720a6a4929a32471a62011ed87103421`.
Item: reproduce the M38-7 misroot in a sandbox, prove the mandated guard refuses it, and
state what a round-39 wave context must carry.

Deliverable (written last, beside this receipt):

```
.ufo/waves/round-39/wave1/ExecNoHarmFixture.guard-demo.txt   502 lines   31415 B
sha256 0330286af302fc9186e44ccb3c13fba5d373ca55755ff647de6ca3118a9a56f2
```

The transcript is generated end-to-end by `demo.sh`; every `$ …` line in it is the exact
string bash evaluated, and every `[exit N]` is that command's status. Sections 9 and 10 of
the transcript carry the paste-ready wave-context clause and the byte source of all four
sandbox scripts.

Scratch: `S=/fast/scratch/hyaku/kasegi-r39/ExecNoHarmFixture/` — removed before this receipt
was filed (§6). No tool was installed. Lane writes were exactly the two allowed paths (this
receipt and the transcript above); no fleet-root, source-tree or sibling-repo file was written,
and no git mutation ran outside the sandbox repos created under `S` (`git status --porcelain`
at the lane shows no tracked modification; the fleet root shows 1 pre-existing entry, 0
tracked-name entries, no `kasegi` line).

## 1. What was built

`S` holds one fake fleet root, two fixture builders, the M38-7-shaped driver and the guard:

| file | role | sha256 |
|---|---|---|
| `build-fleet.sh` | fake fleet root F: `LOG.md` 40 lines, `SCORECARD.md` 60 lines, `MANIFEST.json`, committed; asserts `git rev-parse --show-toplevel` == F | `e28511ec…09bea` |
| `fresh-fixture.sh` | clean one-commit fixture repo D at its own worktree root | `8c446944…a1ed6c` |
| `misroot-driver.sh` | the M38-7 shape: six **relative** writes (`LOG.md`, `SCORECARD.md`, `PROVINCE.md`, `SHONEN.md`, `SKILL.md`, `corpus/README.md`) **before** it learns the fixture root, then `cd "$1"`, `git add -A`, `git commit` | `719fa2af…ce1ba` |
| `guard-run.sh` | the mandated guard: clause 1 cwd under scratch and outside every protected root; clause 2 no declared write inside a protected root; clause 3 fixture toplevel == fixture dir; clause 4 `cd` into scratch then exec | `77580487…73d41` |

The four clauses are the fix cell of `corpus/lessons/round-38.md:289` turned into executable
form. The driver is deliberately left defective: the barrier is the guard, not the driver,
because a seat cannot be trusted to notice its own cwd.

## 2. Measured results (recorded lines from the transcript, §8)

```
label                                          | F         | driver      | exit
-----------------------------------------------+-----------+-------------+--------
LIMB 1 unguarded (cwd=F)                       | F=CHANGED | driver=yes  | exit=0
LIMB 2a guard clause 1 (prefix)                | F=same    | driver=no   | exit=90
LIMB 2b guard clause 1 (protected)             | F=same    | driver=no   | exit=90
LIMB 3 guard clause 2 (writes)                 | F=same    | driver=no   | exit=90
LIMB 4a guard clause 3 (toplevel)              | F=same    | driver=no   | exit=90
LIMB 4b unguarded nested control               | F=same    | driver=yes  | exit=0
LIMB 5 positive (cwd under S)                  | F=same    | driver=yes  | exit=0
```

F's fingerprint is a sorted sha256 of every file outside `.git`; baseline and final digest are
both `1a2df6bb10ce62a7a7528e5836de6f37db21a058fdd5c635e927b55720ad222b`.
`driver=yes/no` is read from the driver's own `$D/setup.log` side effect, not asserted.

### Limb 1 — unguarded reproduction (cwd = F, the M38-7 invocation)

```
$ cd '<F>' && bash '<S>/misroot-driver.sh' '<D>'
driver: finished, cwd=<D> fixture=<D>
$ git -C '<F>' diff --stat
 LOG.md       | 41 +---------------------------------------
 SCORECARD.md | 61 +-----------------------------------------------------------
 2 files changed, 2 insertions(+), 100 deletions(-)
$ wc -l '<F>/LOG.md' '<F>/SCORECARD.md'
 1 …/LOG.md
 1 …/SCORECARD.md
$ git -C '<F>' status --porcelain
 M LOG.md
 M SCORECARD.md
?? PROVINCE.md
?? SHONEN.md
?? SKILL.md
?? corpus/
```

Tracked `LOG.md` 40 → 1 line and `SCORECARD.md` 60 → 1 line (100 deletions); `PROVINCE.md`
(43 B), `SHONEN.md` (41 B), `SKILL.md` (40 B) and `corpus/README.md` (48 B) created. That is the
M38-7 event list exactly (`corpus/lessons/round-38.md:289`: "it truncated the fleet-root
`LOG.md`/`SCORECARD.md` and created `PROVINCE.md`, `SHONEN.md`, `SKILL.md` and `corpus/*` there").

### Limb 2a — guard clause 1, prefix test (the literal fix cell)

```
$ cd '<F>' && SCRATCH_ROOT='<S>/work' FIXTURE_DIR='<D>' bash '<S>/guard-run.sh' bash '<S>/misroot-driver.sh' '<D>'
guard: REFUSED [CWD]: caller cwd '<F>' is not under scratch '<S>/work'
guard: driver not started
[exit 90]
$ ls '<D>/setup.log'
ls: cannot access '…/fixture/setup.log': No such file or directory
```

F digest after the limb = baseline; the driver never started.

### Limb 2b — guard clause 1, protected-root exclusion

```
$ cd '<F>' && SCRATCH_ROOT='<S>' FIXTURE_DIR='<D>' FLEET_ROOT='<F>' bash '<S>/guard-run.sh' bash '<S>/misroot-driver.sh' '<D>'
guard: REFUSED [CWD]: caller cwd '<F>' is inside protected root '<F>'
guard: driver not started
[exit 90]
```

### Limb 3 — guard clause 2, declared writes

```
$ cd '<S>/work' && … FLEET_ROOT='<F>' DRIVER_WRITES='<F>/LOG.md <F>/SCORECARD.md' bash '<S>/guard-run.sh' bash '<S>/misroot-driver.sh' '<D>'
guard: REFUSED [TRACKED-WRITE]: declared write '<F>/LOG.md' is inside fleet root '<F>' and is tracked at HEAD
guard: driver not started
[exit 90]
$ ls -A '<S>/work'
```

### Limb 4 — guard clause 3, fixture toplevel

```
$ git -C '<NESTED>/nested' rev-parse --show-toplevel
<NESTED>
$ cd '<S>/work' && … FIXTURE_DIR='<NESTED>/nested' bash '<S>/guard-run.sh' bash '<S>/misroot-driver.sh' '<NESTED>/nested'
guard: REFUSED [TOPLEVEL]: fixture toplevel '<NESTED>' != fixture dir '<NESTED>/nested'
guard: driver not started
[exit 90]
$ git -C '<NESTED>' log --oneline
63b7d23 fixture fleet root
```

Unguarded control (4b) on that copy, so the clause is not decorative:

```
$ cd '<NESTED>' && bash '<S>/misroot-driver.sh' '<NESTED>/nested'
$ git -C '<NESTED>' log --stat --oneline -1
5270856 fixture: setup from misroot-driver.sh
 LOG.md           | 41 +------------------------------------
 PROVINCE.md      |  1 +
 SCORECARD.md     | 61 +-------------------------------------------------------
 SHONEN.md        |  1 +
 SKILL.md         |  1 +
 corpus/README.md |  1 +
 nested/setup.log |  1 +
 7 files changed, 7 insertions(+), 100 deletions(-)
```

`git add -A` from a subdirectory staged the whole enclosing worktree: the truncation became a
commit in the wrong repo. The guard's toplevel assertion refuses that path before any mutation.

### Limb 5 — positive: all clauses green

```
$ cd '<S>/work-pos' && … DRIVER_CWD='<S>/work-pos' bash '<S>/guard-run.sh' bash '<S>/misroot-driver.sh' '<D>'
guard: PASS [cwd=<S>/work-pos toplevel=<D> fleet=<F>]
driver: finished, cwd=<D> fixture=<D>
$ ls -A '<S>/work-pos'
corpus
LOG.md
PROVINCE.md
SCORECARD.md
SHONEN.md
SKILL.md
$ wc -l '<S>/work-pos/LOG.md'
 1 '<S>/work-pos/LOG.md'
```

The relative writes landed in scratch; F stayed byte-identical; the commit landed in D.

## 3. What failed first (why this receipt is not a happy path)

The first version of the guard **passed the M38-7 invocation**. It tested only "caller cwd is
under `$S`", and the sandbox's fake fleet root was created *inside* `$S`, so `cwd=F` satisfied
the prefix test and the driver ran. That is exactly the class this round is scoring — a guard
whose negative limb cannot fail — and it was caught by running the red limb rather than by
reading the guard. Fixes, both in the transcript's final bytes:

1. clause 1 now also refuses a caller cwd inside a protected root (`FLEET_ROOT`), so a prefix
   test can never be satisfied by the very tree it is meant to protect (limb 2b);
2. the second run also exposed that `cp -a "$F" "$PRISTINE"` had nested into a stale directory
   from the first run, so "restored" F was not byte-identical; the demo now clears the sandbox
   subtree before building and the restore is verified by digest (`VERDICT[after restore]:
   F byte-identical to baseline`).

## 4. What a round-39 wave context must carry

Full paste-ready text is §9 of the deliverable. The load-bearing points:

1. Scratch first: `S=/fast/scratch/hyaku/kasegi-r39/<SEATNAME>/`, `cd "$S"` before any write.
2. Every fixture driver goes through the guard; the guard refuses (exit 90, driver not started)
   unless the caller cwd is under S and outside every protected root, no declared write is
   inside a protected root, and the fixture's `rev-parse --show-toplevel` equals the fixture.
3. Only then does the guard `cd` into scratch and exec, so relative writes can only land in
   scratch.
4. The seat must record **one refused run beside one positive run**; a guard with no recorded
   refusal is prose, not enforcement (this is the lesson of §3).
5. `corpus/instruments/ExecNoHarm.sh` is not re-run from the fleet root (fix cell, verbatim).

Limits stated in the deliverable rather than hidden: clause 2 is a declaration check and cannot
see an undeclared absolute write (clause 1 is the enforcement); the protected-root exclusion
matters because a prefix test alone is satisfied whenever the protected tree is nested under the
prefix; and the demonstration's F is a stand-in inside seat scratch, so no fleet or lane bytes
were at risk in any limb.

## 5. Checks I ran on the deliverable

```
wc -l  .ufo/waves/round-39/wave1/ExecNoHarmFixture.guard-demo.txt      → 502
sha256sum …/ExecNoHarmFixture.guard-demo.txt                            → 0330286a…a56f2
grep -c 'exit=90' …/ExecNoHarmFixture.guard-demo.txt                    → 8   (4 RECORD + 4 limb exits)
grep -n 'RECORD' …                                                      → 7 records, one per limb (§2 table)
tail -3 …                                                               → demo wall time: 459 ms
```

The deliverable is generated, not hand-written: `demo.sh` in `$S` produced it in one pass with
`rc=0` and the wall time above.

## 6. Scratch quiescence

`rm -rf /fast/scratch/hyaku/kasegi-r39/ExecNoHarmFixture` ran after the deliverable copy and
before this file was written. Measured after removal:

```
$ test -e /fast/scratch/hyaku/kasegi-r39/ExecNoHarmFixture && echo PRESENT || echo ABSENT
ABSENT
$ ls -A /fast/scratch/hyaku/kasegi-r39/
CritDesignReview   CritFreezeAudit   ExecArchiveNoHarmMirror   ExecCensusAfterMirror
ExecConsidertheseLedger   ExecHarnessProbe   ExecNoPlaceholderScan   ExecProofSuiteSelftest
ExecRunbookChecks   ExecSuiteBuild   ExecWholeTailFixture   RevAssimilationBlock
RevControls-2   RevFrontierAmendments   RevRowsCensus   RevScratchDiscipline
ScribeShonen   ScribeSpotCheckList   ScribeWaveEvidence
```

The remaining entries belong to other live round-39 seats; this seat added and removed exactly
one, and `ExecNoHarmFixture` is absent at filing.

## 7. Risks and blockers

- **No blocker.** The assignment is complete: both limbs measured, deliverable shipped.
- Residual risk R1: the guard is shipped as a sandbox script inside the transcript, not as a
  lane instrument. Landing it (e.g. under `corpus/instruments/`) is the L1's call and outside
  this seat's write scope; the transcript's appendix is byte-complete for that purpose.
- Residual risk R2: clause 2 cannot see undeclared absolute writes. If the L1 wants runtime
  enforcement of absolute targets, the driver would have to run under a narrow `--work` root
  or a mount namespace; that is a larger change than this item and is stated, not attempted.
- Residual risk R3: the sandbox F is a three-file stand-in; it reproduces the M38-7 event list
  but not the fleet's full tracked set. The guard's clauses do not depend on file count.

## 8. Tooling

None installed or upgraded this round. `git 2.56.0`, `bash 5.3.20`, `sha256sum`, `date` used as
present; `pacman` not invoked.
