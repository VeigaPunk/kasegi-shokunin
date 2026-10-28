# ExecReplayHarness — round-42 replay-limb library

Seat: ExecReplayHarness (wave 1). Scope: build the replay-limb library the
round-42 closure suite sources, plus the defeat catalog spec. No subagents
dispatched; no labrat probe used. No tools installed or upgraded; no network
fetches; no mutating git/jj command anywhere.

## Files

| path | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-42/wave1/ExecReplayHarness.sh` | 997 | `4eee72b1c0914aee46e8abc546821723834daa41c32ffd12d18532eaa9fce7eb` |
| `.ufo/waves/round-42/wave1/ExecReplayHarness.spec.txt` | 402 | `b5dec3b496d0cf11bf2df3ac7b625deeec3ac9f264288b308e4f691b6c4216c4` |

Both are byte-exact deliverables written beside this receipt, as the seat
assignment requires. The spec file contains only landable bytes (the
artifact -> family -> mechanism map and the UNMAPPED list); the validation
transcripts live here, in the receipt.

## What was built

`ExecReplayHarness.sh` is a sourceable bash library exposing

```
replay_defeat <artifact> <mode>      # fixture | export | list
replay_report   [mode]                # verdict table on stdout
```

`replay_defeat` materializes the mutated input state a committed defeat
artifact describes, runs the CURRENT suite's named check limb over it, and
returns **0 iff the limb REJECTS it** (nonzero exit, or `closed=0`).

Two properties make the verdict meaningful, and both were required by the
round-41 verifier's own findings:

1. **The limb is invoked as a function, never by re-running the 91KB suite
   binary.** The library sources the suite in a subshell and calls its
   `check_<id>` function, or runs the corpus instrument directly for the two
   instrument families. This is what the seat assignment requires ("No defeats
   are replayed by re-running 91KB files").
2. **Every case runs the limb twice: once on the pristine fixture (the
   control) and once on the mutated fixture.** The control must be green. A
   limb that rejects everything would otherwise score every defeat as closed
   — the vacuous-pass failure the round-41 verdict rejected. When the control
   is red the case is `UNGRADED` (exit 2), never a pass.

Exit codes: 0 = every selected defeat rejected (family closed); 1 = at least
one defeat accepted (family still open — the kill signal); 2 = not gradable.

The suite, lane, ref, round token, scratch family name, truth tally token,
evidence stems, record list and declared-blocks path are all **discovered
from the suite source**, not hardcoded, so one library drives any round's
suite. `REPLAY_LIMB_MAP` lets the L1 pin the final family -> check binding
(the library's default candidates are `check_j1`..`check_j7` for the r42
suite with `check_i1`..`check_i12` as r41 fallbacks).

Nothing is written outside the scratch root the library creates; the lane is
read-only throughout (`git archive`, `git diff --name-only`, `git log`).

## Verification

Run against the current suite bytes
(`corpus/instruments/r41-closure.sh` at the round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`, base
`5b29ea1439450b712581edf5f0f0bf98dfb262ab`):

```
export REPLAY_SCRATCH=$S
export REPLAY_SUITE=<lane>/corpus/instruments/r41-closure.sh
export REPLAY_LANE=<lane>
export REPLAY_REF=1f7464612ac4c44e39886b82e812610d3c039b13
export REPLAY_BASE_REF=5b29ea1439450b712581edf5f0f0bf98dfb262ab
. <lane>/.ufo/waves/round-42/wave1/ExecReplayHarness.sh
replay_report fixture
```

Complete output (all 27 cases grade; 12 ACCEPTED, 15 REJECTED, exit 1):

```
case	family	artifact	verdict	rc	payload
e1.evidence-not-named	F-EVID	CritC1KillRule.md	ACCEPTED	1	records=3,lines=14,graded=3,evidence=3/3,missing=0
e2.evidence-not-named-log	F-EVID	RevC1Counters.md	ACCEPTED	1	records=3,lines=14,graded=3,evidence=3/3,missing=0
e3.evidence-not-named-shonen	F-EVID	RevC1Counters.md	ACCEPTED	1	records=3,lines=14,graded=3,evidence=3/3,missing=0
e4.evidence-not-named-union	F-EVID	CritC1KillRule.md	ACCEPTED	1	records=3,lines=14,graded=3,evidence=3/3,missing=0
t1.mangled-tally-first-line	F-TOKEN	CritC1KillRule.md	ACCEPTED	1	exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0
t2.mangled-tally-every-correction	F-TOKEN	MutSuite.findings.txt	REJECTED	0	exact=2/2,substring=2/2,records=3,tally=2/3,mangled=1
t3.mangled-tally-every-mention	F-TOKEN	RevC1Counters.defeats.txt	REJECTED	0	exact=2/2,substring=2/2,records=3,tally=2/3,mangled=1
b1.registry-bare-pipe	F-TABLE	MutSkillTablePipes.md	ACCEPTED	1	mentions=1,rows=1,well-formed=1,table=1,cells=11,broken=0,r40-table=1
b2.registry-leading-space	F-TABLE	MutSkillTablePipes.md	ACCEPTED	1	mentions=1,rows=1,well-formed=1,table=1,cells=10,broken=0,r40-table=1
b3.registry-mention-only	F-TABLE	RevC1Counters.defeats.txt	REJECTED	0	mentions=1,rows=0,well-formed=0,table=0,cells=0,broken=0,r40-table=1
b4.registry-blank-line	F-TABLE	CritC1KillRule.md	REJECTED	0	mentions=1,rows=1,well-formed=0,table=0,cells=10,broken=1,r40-table=1
d1.declared-omits-changed-path	F-DECL	CritDeclarationCoverage.md	ACCEPTED	1	declared=153,valid=153,tail=153,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok,file=present
d2.declared-symlink-outside	F-DECL	CritI12Necessity.md	REJECTED	0	declared=153,valid=152,tail=152,malformed=0,pure=1,paths=0,canon=0,nul=0,diff-read=ok,file=present
d3.declared-short-of-added	F-DECL	MutH6H10.md	REJECTED	0	declared=153,valid=152,tail=152,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok,file=present
s1.stray-outside-root	F-SCAN	MutScratchTiming.md	ACCEPTED	1	strays=0,read=ok,scanned=0
s2.stray-case-separator	F-SCAN	CritKillRule.md	REJECTED	0	strays=1,read=ok,scanned=1
s3.stray-dot-prefixed	F-SCAN	CritKillRule.md	REJECTED	0	strays=1,read=ok,scanned=1
s4.stray-nested	F-SCAN	CritKillRule.md	REJECTED	0	strays=1,read=ok,scanned=1
s5.stray-ancestor-symlink	F-SCAN	CritKillRule.h6-escapes.sh	REJECTED	0	strays=1,read=ok,scanned=1
s6.scan-root-missing	F-SCAN	CritKillRule.md	REJECTED	0	strays=0,read=fail,scanned=0
s7.stray-unreadable	F-SCAN	CritKillRule.h6-escapes.sh	REJECTED	0	strays=0,read=fail,scanned=0
s8.stray-sibling-round	F-SCAN	MutScratchTiming.md	ACCEPTED	1	strays=0,read=ok,scanned=0
c1.binding-missing-path	F-BIND	MutBindingExistence.md	ACCEPTED	1	records=55 bound=55 unbound=0
c2.binding-url-case	F-BIND	MutBindingExistence.md	REJECTED	0	records=55 bound=54 unbound=1
c3.binding-url-trailing-slash	F-BIND	MutBindingExistence.md	REJECTED	0	records=55 bound=54 unbound=1
p1.frontier-status-flip	F-FLIP	MutC2Chain.md	ACCEPTED	1	entries=26 pass=26 exit=0
p2.frontier-decoy-row	F-FLIP	MutFrontierParser.md	REJECTED	0	entries=28 pass=27 exit=1
REPORT_EXIT=1
```

This transcript is the harness's own validation: every ACCEPTED row
reproduces a defect the corresponding committed wave-2 artifact recorded as
surviving, and every REJECTED row is a defect the artifact recorded as
closed.

| artifact | committed finding | harness verdict |
|---|---|---|
| CritC1KillRule.md | I1 `evidence-not-named` escape, `evidence=3/3` | e1 ACCEPTED, `evidence=3/3` |
| RevC1Counters.md | I3 token-boundary escape; I1 union escape | t1/e2/e3 ACCEPTED, `tally=3/3`, `evidence=3/3` |
| CritC1KillRule.md (canonical) | I1 `evidence-not-named` union mutant (first block of every record) | e4 ACCEPTED, `evidence=3/3` — matches ExecJ1Evidence's independently verified r41 reading |
| MutSkillTablePipes.md | bare pipe and leading space survive | b1 ACCEPTED `cells=11`, b2 ACCEPTED `cells=10` |
| CritDeclarationCoverage.md | declarations validate a subset, not completeness | d1 ACCEPTED, `valid=153` |
| CritI12Necessity.md | T7 symlink must be rejected | d2 REJECTED, `canon=0,paths=0` |
| MutH6H10.md | M-H9a declared-short-of-added | d3 REJECTED, `tail=152` |
| MutScratchTiming.md | outside-root stray not observed | s1 ACCEPTED, `strays=0`; s8 ACCEPTED (a sibling round's family is invisible too) |
| CritKillRule.md | F1-F8 scratch escapes | s2-s4/s6 REJECTED, `strays=1` / `read=fail` |
| CritKillRule.h6-escapes.sh | m5/m9 scenarios | s5/s7 REJECTED |
| MutC2Chain.md | status flip leaves the denominator silently | p1 ACCEPTED, `entries=26 pass=26 exit=0` |
| MutFrontierParser.md | decoy row must fail | p2 REJECTED, `entries=28 pass=27 exit=1` |
| MutBindingExistence.md | missing capture path is not a binding failure | c1 ACCEPTED, `bound=55` |

### One committed finding does not reproduce

The round-41 artifact `MutBindingExistence.md` reports all three F-BIND
variants as surviving, and prints the **byte-identical** counter line
`records=63 bound=63 unbound=0 exit 0` for the pristine baseline and for all
three mutated probes. That identity is the signature of a probe that never
re-read its own mutation: `capture-binding-check.py`'s `--root` default is
the lane, so a run without `--root` grades the pristine lane and cannot see a
scratch-copy edit.

Re-measured at the same reference
(`ad7147532cb702b0d541d40499874552183d9132`) with `--root` pointed at the
mutated copy:

```
pathcase        rc=1  records=63 bound=62 unbound=1
                  FAIL rule=url-mismatch record=S063 row=S063 dir=round-41
trailingslash   rc=1  records=63 bound=62 unbound=1
                  FAIL rule=url-mismatch record=S063 row=S063 dir=round-41
missingpath     rc=0  records=63 bound=63 unbound=0
```

and, confirming the default-root mechanism:

```
$ python3 corpus/instruments/capture-binding-check.py          # no --root
records=55 bound=55 unbound=0      rc=0                       # the pristine lane
```

So the two URL variants are already rejected by the current instrument; only
the missing-path variant survives. The library therefore grades c1 as the
open F-BIND defect and c2/c3 as already closed. **The L1 decides** whether
c2/c3 stay in the r42 replay set. This is recorded in the spec file.

### Mechanism confirmed independently

The F-FLIP blind spot was reproduced directly, outside the library, by
flipping the status cell of the last admitted frontier row in a scratch
export of `corpus/README.md`:

```
flipping line 563 : | F24 | RFC 9116 security.txt — ...
PASS     F23  knowledge/cyclonedx-analysis-subtree.md   ids=S060  exit=0
entries=26 pass=26 exit=0
```

The flipped row disappears from the denominator and the counter still exits
0 — exactly the recorded blind spot.

### Cross-seat integration (ExecJ1Evidence)

The J1 seat reported that a round-42 J1 grounds each declared evidence
identifier in the committed wave-2 artifact and fails `evidence-not-grounded`
on a records-only tree.  Adopted:

* F-EVID / F-TOKEN fixtures now carry EVERY `round-4*/wave2` tree the export
  holds.  A first attempt derived the directory from the running suite's
  round token (`round-<round-1>`), which the J1 seat flagged as a real
  hazard: the r42 J1 audits the ROUND-41 correction blocks
  (`J1_ROUNDS=(41)`) and therefore grounds under
  `.ufo/waves/round-40/wave2` **even when the r42 suite runs**.  A
  round-token-derived set would carry round-41/wave2 only, `check_j1` would
  then red on the PRISTINE control as `evidence-not-grounded`, and the case
  would be UNGRADED — not gradable for the wrong reason.  Carrying the
  superset is the safe rule.  Verified: the fixture carries both
  `.ufo/waves/round-40/wave2` (107 artifacts) and `.ufo/waves/round-41/wave2`.
* Polarity of the landed J1 limb, confirmed by that seat: `check_j1` exits 0
  with `closed=1` when the defect is ABSENT and exits 1 with `closed=0` when
  it is present.  The library's rejection test (`rc != 0` or output contains
  `closed=0`) therefore maps `check_j1`'s red to REJECTED, which is what the
  replay needs.  `check_j1` takes `$1` only and needs no globals, which the
  library's call form satisfies.
* `e4.evidence-not-named-union` was added as the canonical F-EVID case (strip
  the first Correction block of every record, exactly r41's
  `selftest_case_i1`, and exactly that seat's `j1_mutant_union`).  Reproduced
  the J1 seat's verified result: committed r41 I1 returns `evidence=3/3`
  rc=0 on it.  (`e1`-`e3` are the per-record variants.)  A records-only fixture would
  instead have made the control red and the case UNGRADED — the fail-closed
  path, never a false pass.
* The library's default candidates already try `check_j1..check_j7` before the
  r41 `check_i1..check_i12` fallbacks, so a J-limb landing in
  `r42-closure.sh` is picked up with no configuration; `REPLAY_LIMB_MAP`
  overrides the name if it differs.

**Cross-verified by the J1 seat** (lane HEAD `514ff62`; limb re-landed as
`ExecJ1Evidence.sh` sha256
`20d95cfbbe5f203dc3dbb4808eddf9a61508546904391f19249bf29a49382463`, 574
lines, `mutants=6/6 positive=pass failures=0`).  All four F-EVID cases flip
from ACCEPTED to rejected when `check_j1` is the limb:

```
pristine   evidence=4/4 closed=1 rc=0  union 3/3
e4         evidence=1/4 closed=0 rc=1  union 3/3  fail=SCORECARD.md:1602;LOG.md:1736;SHONEN.md:221
e1         evidence=2/4 closed=0 rc=1  union 3/3  fail=1602;1607
e2         evidence=3/4 closed=0 rc=1  union 3/3  fail=LOG.md:1736
e3         evidence=3/4 closed=0 rc=1  union 3/3  fail=SHONEN.md:221
```

Two facts this pinned down, both now recorded in the spec:

* `evidence=<n>/<m>` counts MEMBERS (correction blocks; m=4 on the round-41
  record set), not identifiers.  The identifier set stays the three round-41
  stems.  `union=<k>/3` is the id overlap and stays 3/3 on every mutant —
  that is the defect the per-block rule closes.
* `e1` strips TWO members, not one, because SCORECARD.md carries the D-r41-1
  duplicated block (L1602 and L1607).  `e4` leaves SCORECARD:1607 holding all
  three identifiers, which is exactly why the union tally cannot see the
  removal.

The J1 seat also re-landed its limb after finding that `prior` was computed in
the same `local` statement as `round`, so it worked only by dynamic scope and
aborted with `round: unbound variable` under `set -u` — the same
`local`-ordering class as defect 4 in my own list below.

### Suite-independent behaviour

* `bash -n` clean; runs under `set -uo pipefail` (the r41 suite's own flags).
* `replay_defeat all list` works before any initialization (no suite needed).
* `replay_defeat <artifact> export` re-uses the same mutators over a full
  `git archive` export of the ref; exit 1 as expected at the current bytes.
* Discovery resolves the suite, lane, ref, round token (`41`), family token
  (`kasegi-r41`), tally token (`closed=10/10`), records, evidence stems and
  declared-blocks path from the suite source.
* I never wrote to the lane: the only paths attributable to this seat are the
  three untracked `ExecReplayHarness.*` files in
  `.ufo/waves/round-42/wave1/`.  The working tree does show MODIFIED tracked
  files (`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`,
  several `corpus/` files) — those are other seats' in-flight round-42 work,
  not mine.  That is also why the library is ref-scoped throughout (export of
  `REPLAY_REF`, instrument read from the fixture tree): a mid-wave working-tree
  edit must not be able to move a verdict.

## Defects found and fixed in my own deliverable during development

Recorded because each would have produced a silently wrong verdict:

1. `awk` rejects `--` after the program text (`awk 'prog' -- file`); it must
   precede the program. Fixed in eight places.
2. `grep` accepts one `--`; a second one is read as a filename.
3. `sed`'s default `s/…/…/` delimiter collides with the `/` inside the tally
   token `closed=10/10`; switched to `#`, and the trailing-boundary guard
   keeps the substitution idempotent.
4. `local a=$1 b=$2 c="$a/$b"` does not see `a` yet inside one `local`
   statement; split into two statements.
5. `REPLAY_SUITE` was both the input and the resolved output, so a second
   `replay_init` skipped discovery and left derived variables unset; the
   input is now captured separately and init is idempotent.
6. `REPLAY_SUITE` must be sourced from the suite's own path, which the
   library reads via `SELF`; when the suite has not been sourced the limb
   lookup falls back to a subshell that sources it.
7. The evidence/tally mutations initially rewrote the wrong round's
   correction lines (the tree carries every earlier round too); they are now
   scoped to the suite's own round, and the tally mutation targets the first
   correction block that actually carries the tally token.
8. The F-BIND missing-path mutation initially fired the orphan-capture rule
   (a different defect); the old capture is now removed with it, so the
   dangling path is the only defect present.
9. `replay_cleanup` removed the base export while `replay_init` was cached, so
   a SECOND `replay_defeat` call in the same shell found no fixture source and
   graded every case UNGRADED (exit 2).  Caught by replaying the seven
   families one call at a time (the single `replay_report` pass hid it, because
   cleanup runs once at the end).  The base export now lives outside the case
   root and cleanup resets the init flag.
10. A limb may GROUND evidence identifiers in the committed wave-2 artifacts
    (`evidence-not-grounded` on a records-only tree, reported by the J1 seat).
    Without carrying `.ufo/waves/round-<round-1>/wave2/` the control run goes
    red and every F-EVID/F-TOKEN case would have reported UNGRADED (exit 2) —
    correct fail-closed behaviour, but no evidence.  The fixture now carries
    it.
11. The `py:` limbs ran the instrument from the LIVE WORKING TREE while the
    corpus under test was a ref-scoped export.  A concurrent seat editing
    `capture-binding-check.py` / `frontier-recheck-count.py` silently changed
    the verdicts mid-wave (observed: F-BIND and F-FLIP flipped from ACCEPTED
    to REJECTED between two runs over the SAME ref).  The instrument now runs
    from the fixture tree, i.e. the export of the ref under test, which
    restores the export-mode guarantee that an uncommitted edit cannot move a
    verdict.
12. The first version of the canonical `e4` case stripped evidence from
    EVERY block of every record, which the r41 limb already rejects
    (`evidence=0/3`); that is not the committed mutant and it is not an
    escape.  The committed `selftest_case_i1` replaces only the FIRST block
    per record, so `evidence` stays 3/3 and the defect escapes.  `e4` now
    reproduces the committed shape and reads `evidence=3/3` rc=0, matching the
    J1 seat's independent verification.

## Risks and limits

* The r42 suite does not exist yet (`corpus/instruments/r42-closure.sh` is
  absent at this commit; `r41-closure.sh` is the newest). The library was
  therefore validated against the r41 suite with the r42 `check_j*` names
  resolved through `REPLAY_LIMB_MAP`. When the r42 suite lands, the L1 sets
  that map; the library needs no code change.
* The family -> check-id assignment (which J-check owns which family) is the
  L1's decision. The library's defaults are the claim's own ordering
  (J1..J7 for F-EVID, F-TOKEN, F-TABLE, F-DECL, F-SCAN, F-BIND, F-FLIP).
* J8-J13 (receipt integrity, negative controls, graded-selftest isolation,
  correction uniqueness, no-deletion/density, scratch quiescence) are outside
  the seven routed families. The receipt-integrity artifacts
  (`CritDigestSelftest.md`, `CritReceiptBootstrap.md`) and the round-40
  receipt mutants are listed UNMAPPED in the spec with a proposed family
  (F-RECEIPT) for the L1 to decide.
* The claim's J5 asks for two distinct things from the r42 scan, and the
  catalog covers both: an outside-configured-root stray under a seat-named
  dir (`s1`, placed via `REPLAY_STRAY_DIR`, default the parent of the
  configured scratch root) and coverage of the whole `kasegi-r4[0-9]*`
  prefix (`s8`, a stray named for the sibling round).  Both are ACCEPTED at
  the round-41 bytes: `s8` is invisible because the round-41 scan matches
  only `kasegi-r41`.  The r42 J-limb's own scan domain is the L1's design
  choice; the library's job is to materialize the defect state, which it
  does.
* All scratch state is created under `REPLAY_SCRATCH` and removed by
  `replay_cleanup`; nothing is written to host-global paths, so a replay
  never turns another seat's scratch scan red while it runs.  (While
  materializing `s1`/`s8` a family-named directory exists for the duration of
  one limb call, inside the seat's own scratch root.)

## Hygiene

* Scratch `/fast/scratch/hyaku/kasegi-r42/ExecReplayHarness` was created for
  all fixtures and removed before this receipt was written.
* Writes: this receipt and the two deliverable files in
  `.ufo/waves/round-42/wave1/`, plus scratch under the seat scratch dir. No
  other lane, fleet or source-tree file was touched; no fleet-root tracked
  file was written; no PATH directory was written.
* Disk guard checked with `scripts/hyaku/disk-guard.sh status` before the
  heavy pass (`/fast/scratch/hyaku` 27%, 590.2G free) and again after
  (31%, 558.0G free).
* No tool installs or upgrades (no pacman); no network fetches; no mutating
  git/jj command anywhere.

Report: .ufo/waves/round-42/wave1/ExecReplayHarness.md
