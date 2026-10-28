# R44Critic1 — can C1's eight routed defects be gamed?

Seat: read-only critic. Item: falsify C1's frozen baseline—can the eight routed defect count or status be gamed?
Frozen base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`. Initial lane HEAD: `66314015122b9aa32dc40f2f1815df56624c26d1`.

## Finding

**Yes. The live C1 counter rejects do-nothing, but accepts a forged fixed state: 8/8 resolved from marker-only files and one newline on a copy of the frozen base.** This directly falsifies the sufficiency of the after-state predicate. The frozen raw defect-count command is also revision-unstable. No C2 judgment offered.

### F1 — counter's do-nothing check passes, forged after-state passes too

A sibling-created, untracked `corpus/instruments/r44-routed-defects.py` appeared during inspection and changed while being read. I snapshot-tested it; snapshot SHA-256 `8a5a9c2bd6ac04b08c93e31c7dd9c228b4bd737c240e17f58191b7f303691ee6` (later snapshot SHA `9566b225...`; see caveat below).

Do-nothing replay (both root and baseline were a `git archive` export of the frozen base):

```
python3 counter-snapshot.py --root <base-export> --baseline <base-export>
frozen_defects=8 fixed=0 unresolved=8 exit=1
```

So the counter does not pass its own kill rule on the untouched base. But I copied the same base and added only marker strings/files: `closed=13/19 superseded exit 127 exit=2 missing-suite-base.txt` in errata; required substrings in a lesson; `seats=73` and 73 fake names; the required `export-ref` in a text file; and instrument names in SKILL.md. I appended `\n` to SHONEN.md for the actual trailing-blank-line check. No historical transcript, correct seat registry, or substantive corrections were added.

```
python3 counter-snapshot.py --root forge --baseline <base-export>
RD43-1 ... resolved=1
...
RD43-8 ... resolved=1
frozen_defects=8 fixed=8 unresolved=0 exit=0
```

The live 79-line counter snapshot uses substring predicates for seven defects and a byte-tail test for SHONEN. Its RD43-5 accepts 73 arbitrary names even though round-44 dispatch has 66 members (`wave1-dispatch.json`: `counts={"spawn":66,"resume":0,"total":66}`, 66 registry members). RD43-4 checks phrases in `corpus/lessons/round-44.md`, not the report named by defect 4. RD43-7 checks instrument names in SKILL.md and a lesson phrase, not the SHONEN pointer or the instruments registry. RD43-8 accepts an `exit=127` string in a file, not proof that the absent suite was run. RD43-1's SCORECARD condition was already true at base: the first `closed=13/19` is followed later by `Correction (round 43` and `superseded`; only the new errata-marker condition blocks it.

This is the strongest direct counterexample: the do-nothing test is necessary but not sufficient; the counter gives a green final result to a fabricated state. The smallest safe correction is evidence-grounding per defect (bind to the named historical artifact or a declared, verified replacement) and a forged-state negative test that rejects this fixture.

### F2 — selftest validates substring dependence, not evidence grounding

A later counter snapshot (`3690413c63c664da890e39c0a0b9494feeaf3f381693217dbd2eb2d555251aa6`) added `seed_fixture()`, which itself writes marker-only SCORECARD/errata/lesson/registry/transcript/SKILL content and `SHONEN.md = b"evidence\n\n"`. Its selftest deletes one needle per mutant. The captured selftest attempt failed before producing results:

```
NameError: name 'missing_run' is not defined
  ... in check(), line 52
```

The file changed again during review, so this is a snapshot-specific observation, not a claim about a later integration. The seeded positive case still demonstrates that marker presence, not semantic evidence, is the test's accepted success shape.

### F3 — defect 1's K18-compatible marker is already in the frozen defect text

`corpus/lessons/round-43-verifier-spotcheck.md:101` itself contains both `closed=13/19` and the phrase `Correction (round 43)` in an instruction to append a correction. K18 (`corpus/instruments/r43-limbs/k18-transcript.sh:152-171,236-240`) puts tokens from any such line into a global `superseded` set. On a base export K18 reports:

```
K18 payload=quotes=68,bound=52,report-only=1,superseded=14,unbound=1 closed=0
```

Removing `Correction (round 43)` from that instruction, without changing the quoted defect, yields `superseded=10,unbound=5`; verbose output then identifies four unbound `closed=13/19` occurrences. Thus a K18-style correction-presence predicate for defect 1 would count it fixed at do-nothing. This reproduces a known issue from round-43 `CritTokenRead.md:77-88`: instruction/denial text can be mistaken for a correction. The actual R44 counter used a different errata marker and did reject do-nothing; this finding applies to any counter predicate that reuses K18's supersede semantics.

K18's binding is also token-global: adding an arbitrary `closed=13/19 exit=1` summary line under `final-gates/` changes its output `bound=52` → `bound=56`, without proving a run of the landed suite at `ab98fac9` (the suite path is absent there; `git cat-file -e ab98fac9:corpus/instruments/r43-closure.sh` exits 128). K18's own red at the frozen base is the unrelated spotcheck quote `selftest cases=10 failures=9` at line 61 (`unbound=1`). A `report-only` label on that line flips K18 to `closed=1` with no evidence; a prose `Correction (round 43)` line quoting it does likewise. This is adjacent evidence that the inherited gate has marker escapes, not one of the eight C1 fixes.

### F4 — frozen count command is shape-sensitive

The frozen control's exact command (`controls/do-nothing.txt:5`) returns 8 on the pristine file. On a scratch copy, un-bolding item 5 while keeping its defect text byte-identical returns 7; appending a column-zero `6. Routed defects ...` line returns 9; appending an eight-item numbered/bold correction block returns 16. Scoped alternative `sed -n '/^## 6\. Routed defects/,/^## 7\./p' FILE | grep -cE '^[0-9]+\. \*\*'` remains 8. The live counter's baseline-derived count guard mitigates this if `--baseline` is the frozen base and fails closed when it does not count 8; the frozen control command itself remains revision-unstable, and the counter does not bind the supplied baseline to a ref/blob.

### F5 — defect 5 changes the evidence subject

At inspected HEAD, round-43 `w1-REGISTRY.txt:7` remains `names=`; `r42-at-de09313-selftest.txt` has zero `export-ref` and zero `de09313` occurrences. The round-44 registry was absent at the initial HEAD. These historical files cannot be changed append-only; the counter instead checks new round-44 control files. It also tests `.tmp` absence in the root (so that clause is observable when run on a working tree, but not as committed evidence). No committed emitter for `w1-REGISTRY.txt` was found in the fleet source search. The substitution must be declared and the new registry checked against the actual dispatch, not a hard-coded `seats=73`.

### F6 — count/claim binding and remaining gaps

- C1 claims.json:15 points at `.ufo/waves/round-44/controls/c1-do-nothing.txt`; that file was absent. Only `controls/do-nothing.txt` existed. C1 before/after cells had no `closed=`, `failures=`, or `cases=` tokens, so K17's token/control binding has nothing to grade for C1.
- Defect 6's remedy is conditional (“when the file is next appended”). At base/initial HEAD, SHONEN ended in `0a` rather than the base `0a 0a`, and was unchanged base→initial HEAD. The counter's explicit `endswith(b"\n\n")` does correctly grade the bytes, but the lane must actually make that byte change.
- C1 requires one red-before control per changed gate, while none of the eight prescriptions requires a gate change (defect 2 explicitly says “rather than widening K18”). The criterion is vacuous unless the new counter itself is treated as a changed gate.

## Do-nothing discrimination and axes

- Actual counter snapshot: do-nothing → `fixed=0/unresolved=8` (passes kill rule); forged marker fixture → `fixed=8/unresolved=0` (false green).
- `depth:verifiability` / C1: harmed by the fabricated 8/8 acceptance, mismatched subjects, and unbound baseline/count/control predicates.
- `coverage` / C2: not examined.

## Smallest safe correction

1. Bind each check to the defect's actual evidence or an explicitly named replacement; compare registry names to dispatch members; make report/pointer checks inspect the report/pointer themselves.
2. Add a negative forged-state test that rejects the marker-only fixture; current substring-removal mutants do not establish evidence grounding.
3. Pin `--baseline` to the frozen base ref/blob. Scope the human-readable defect count to §6.
4. Fix the control pointer and separate committed evidence from the working-tree-only `.tmp` check.

## Limitations and hygiene

- K18 was run standalone on a `git archive` export, not the full suite at a git worktree; K17 rejected a positional root argument, so its C1 blindness is from its documented rule and direct claims token scan, not a K17 execution.
- No R44 counter was committed. I tested snapshots only; it changed while inspected. The latest captured selftest errored as quoted above. Findings about counter predicates are snapshot-specific.
- No C2 work or verdict. No source edits, installs, or pacman invocation. No lane git/jj/index mutation. My scratch was removed. `HYAKU_SCRATCH` was unset; initial scratch used `$HOME/.cache/hyaku-scratch/kasegi-r44/R44Critic1/`, later `.scratch/kasegi-r44/R44Critic1/`; both cleaned.
