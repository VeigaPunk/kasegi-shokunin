# ExecSelftest — round 42, wave 1 (kasegi-shokunin)

Seat: `ExecSelftest` (executor, instrument QA — **not acceptance**).
Axes: `depth:verifiability`, `coverage`.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `5053a7f46de35784cff4b56756906e9014a38276`; round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13`;
lane tip at read time `0566bd66e93d429b2df8b6751cf10cbdc391e79b`.
Frozen claims read first (`.ufo/waves/round-42/claims.json`), not edited.

Deliverables written (this seat's only writes besides this receipt):

| file | lines | sha256 |
|---|---:|---|
| `.ufo/waves/round-42/wave1/ExecSelftest.transcript.txt` | 71 | `078ea73eedcf8451be4ebd13dc0c5bf312ed34bade796d752d58edf78d83d5ea` |
| `.ufo/waves/round-42/wave1/ExecSelftest.mutants.txt` | 214 | `bb5d49e12ac20a617ea45e3adea32dd6fb84a78f72db65bff049425fb466df4a` |

---

## 1. Headline: two routed families are STILL OPEN in the landed wave-1 bytes

Both are measured, not inferred. These are in-family escapes of the shape the
frozen C1 kill rule fires on.

### 1.1 F-FLIP — the frontier row status-flip is still silently dropped

The committed `corpus/instruments/frontier-recheck-count.py` (sha256
`1be79af6…8249`) enumerates **only `admitted` rows**. A row whose status is
flipped away from `admitted` leaves the denominator instead of failing, so the
counter prints a clean green. Measured, verbatim:

```
$ python3 corpus/instruments/frontier-recheck-count.py --root <scratch>/ft   # PRISTINE
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0
exit=0
flipped F01: admitted -> explored
$ python3 corpus/instruments/frontier-recheck-count.py --root <scratch>/ft   # MUTANT: one row flipped
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=26 pass=26 exit=0
exit=0
```

`entries` drops 27 → 26 and the run stays green at exit 0: the flipped row is
**silently dropped**. This reproduces the committed r41 wave-2 artifact
`MutC2Chain.md` mutation A exactly, and the frozen C1 predicate names this as a
family the J7 check must close. The lane's own `ExecJ7Flip.frontier-recheck-count.py`
deliverable had **not landed** when this seat closed, so the repair is not in
the wave-1 bytes yet.

### 1.2 F-BIND — the landed deliverable is a byte copy of the committed instrument

`.ufo/waves/round-42/wave1/ExecJ6Bind.capture-binding-check.py` is **byte-identical**
to the committed `corpus/instruments/capture-binding-check.py`:

```
landed:    3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa      892  40556
committed: 3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa      892  40556
IDENTICAL — the deliverable is a byte copy of the committed instrument
```

It therefore carries the same rule set as the unpatched instrument
(`rule=url-mismatch`, `rule=no-row`, `rule=dup-record`, …) and **no**
existence rule. Measured, verbatim: the committed r41 wave-2
`MutBindingExistence.md` defeat — a manifest record whose capture file is
ABSENT, the record's `path` kept — is still accepted:

```
$ python3 inst.py --root <scratch>/bt   # PRISTINE
records=55 bound=55 unbound=0
exit=0
$ rm corpus/source-snapshots/round-41/S063.txt   # MUTANT: capture file deleted, record path kept
$ python3 inst.py --root <scratch>/bt   # MUTANT
records=55 bound=55 unbound=0
exit=0
```

The sibling shape the instrument *does* reject, for contrast — a URL case-flip —
is killed correctly:

```
$ python3 inst.py --root <scratch>/bt2   # MUTANT: url case-flipped
FAIL rule=url-mismatch record=S063 row=S063 dir=round-41
records=55 bound=54 unbound=1
exit=1
```

So F-BIND is **partially** closed: the URL variant is already rejected (it was
killed even before the wave-2 probe — `MutBind.md` recorded it as KILLED), and
the **missing-capture existence variant remains open**. `MutBind.md` classified
exactly this case as `B1 … SURVIVED`. If the wave-1 landing takes this byte
copy as-is, J6 will not close the family the frozen claim names.

---

## 2. What I could NOT run, and why (the honest limit)

**The r42 suite deliverable never landed.** `.ufo/waves/round-42/wave1/ExecSuiteCore.r42-closure.sh`
was polled continuously for ~2 hours and was absent when this seat closed;
`ExecSuiteCore-2` confirmed at 11:2x UTC that it was still being written and
promised a ping. Consequently these two assigned runs were **not executed**:

* `bash corpus/instruments/r42-closure.sh --selftest --export-ref <lane-tip>`
* `bash corpus/instruments/r42-closure.sh --export-ref <base>`

No claim is made about the r42 suite's graded case lines, `selftest cases=13
failures=0`, or `closed=13/13 exit=0`. **I do not fabricate a transcript for a
suite I never executed.**

What I did instead, so the seat is not empty: I measured every mutant against
the **landed J-limbs** — the same `check_jN` entry points the r42 suite sources
(`ExecJ11Corr.sh`, `ExecJ12J13.sh`, `ExecJ5Scan.sh`, `ExecJ8Receipt.sh`,
`ExecJ9NegCtl.sh`), each sourced and called with its own env contract. Those
verdicts are in `ExecSelftest.mutants.txt`.

---

## 3. The harness (built, validated, and reusable the moment the suite lands)

`/fast/scratch/hyaku/kasegi-r42/ExecSelftest/` (removed before yield).

* `build-mirror.sh` — a scratch git fixture that carries the lane's **real**
  commit objects, so `--export-ref` resolves to the exact hashes the frozen
  claims name. Asserts `git rev-parse --show-toplevel` equals the fixture dir
  before any commit, and hash-verifies all three refs:

  ```
  toplevel-asserted: /fast/scratch/hyaku/kasegi-r42/ExecSelftest/mirror
  hash-preserved: 5053a7f46de35784cff4b56756906e9014a38276
  hash-preserved: 1f7464612ac4c44e39886b82e812610d3c039b13
  hash-preserved: 0566bd66e93d429b2df8b6751cf10cbdc391e79b
  ```

  The lane repo is only ever **read** (`git fetch` from it, `git archive` from
  it). No mutating git/jj command ran in the lane, the fleet root, or any
  sibling repo. The mirror's base blob still resolves to the pinned density
  digest `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`,
  so J12's `base-density` limb is satisfiable against it.
* `drive.sh` — the suite-level driver: 6 baseline runs (selftest at the tip, run
  at tip/base/r41-head, plain-run refusal, unresolvable-ref red) and 7 mutants,
  each run with its **own** `--scratch-root` and `--work`, baselines in
  parallel, mutants each with a private git index so their fixtures cannot
  contaminate one another.
* `limb-qa.sh` — the fallback driver used for the evidence in §4.
* `mutants/MUT-*.sh` — the seven defeat scripts, each self-documenting with the
  committed artifact it reproduces.

**Harness proof.** The driver was validated end-to-end against the r41 suite
(the r42 suite's proven ancestor): the export harness, the `--selftest`
machinery, the payload table and the nested negative controls all ran here.
The verbatim payload table is in `ExecSelftest.transcript.txt`.

**Isolation fix found by measurement.** The r41-shaped scanner's outside limb
counts family-shaped entries **recursively under the scope parent**, so a
shared scope parent makes every run read red. Each run therefore gets
`--scratch-root = <label>/root`, making its outside scope `<label>` — isolated.
This matters for whoever runs the real suite: a shared `--scratch-root` parent
containing another seat's tree will produce a spurious `outside=<n>` red.

---

## 4. Per-mutant verdicts against the landed limbs

Fixture = a fresh mirror commit over the suite tip; the limb is then run over
the **pristine** fixture and over the **mutant** fixture. `REJECTED` = the limb
went red on the mutant (repair holds). `ACCEPTED` = the limb stayed green (an
in-family escape). Full output in `ExecSelftest.mutants.txt`.

| mutant | family / J limb | limb | pristine | mutant | verdict |
|---|---|---|---|---|---|
| `MUT-J5-F-SCAN-outside` | F-SCAN / J5 | ExecJ5Scan.sh | exit 0, `strays=0,outside=0,read=ok,scanned=0,scope=on closed=1` | exit 1, `strays=2,outside=1,read=ok,scanned=4,scope=on closed=0` | **REJECTED** |
| `MUT-J11-F-CORR-duplicate` | F-CORR / J11 | ExecJ11Corr.sh | exit 1, `records=3,corrections=31,distinct=27,dups=4,dup-lines=4,dup-records=1` | exit 1, `records=3,corrections=57,distinct=27,dups=5,dup-lines=30,dup-records=2` | **detected** — the duplication raises `corrections` 31→57, `dups` 4→5, `dup-lines` 4→30, `dup-records` 1→2 |
| `MUT-J1-F-EVID-union` | F-EVID / J1 | — | — | — | **limb not landed**; the union defeat (SCORECARD's correction lines lose every evidence path while LOG.md/SHONEN.md keep theirs) is planted and ready |
| `MUT-J2-F-TOKEN-mangled` | F-TOKEN / J2 | — | — | — | **limb not landed**; `closed=<n>/<m>` → `closed=<n>/<m>0` planted in every correction line of all three records |
| `MUT-J3-F-TABLE-split` | F-TABLE / J3 | — | — | — | **limb not landed**; registry table split + bare pipe + leading whitespace + a split `r42-closure.sh` row planted |
| `MUT-J7-F-FLIP-status` | F-FLIP / J7 | instrument | pristine `entries=27 pass=27 exit=0` | mutant `entries=26 pass=26 exit=0` | **ACCEPTED (ESCAPE)** — see §1.1 |
| `MUT-J12-J13-tracked-deletion` | F-NOARM / J12 | ExecJ12J13.sh | exit 1, `deleted=0,renamed=0,density=1,base-density=1,missing=0,diff-read=fail` | exit 1, same payload | **INCONCLUSIVE** — the limb is red on the pristine fixture too (`diff-read=fail`), so the mutant cannot be attributed; the planted `D` row for `corpus/source-snapshots/round-41/S063.txt` is in the commit diff |

Two mutants (J5, J11) are decisive; the F-FLIP one is a measured escape; the
J12 one is inconclusive for an environmental reason I state rather than
paper over.

### 4.1 Why J12's limb is inconclusive here

`ExecJ12J13.sh`'s `check_j12` reads the base blob and the changed-path set from
the **lane repository** it is given. Driven standalone against a scratch mirror
it reports `diff-read=fail` on the pristine fixture too, so the limb is red
before and after the mutation and the mutant cannot be attributed. It needs the
assembled suite's `--lane` binding to be meaningful. This is a limitation of my
standalone driver, **not** evidence that J12 is weak.

### 4.2 J5 — the mutant is rejected, and the shape matters

The first version of the mutant planted the outside stray one level too high and
J5 reported `outside=0` — my probe was wrong, not the limb. Measured
correction: J5's outside scope is the **parent of the outside root**, so the
stray must be a **sibling of the configured root**. With the stray placed
correctly, J5 goes `strays=0,outside=0 … closed=1` → `strays=2,outside=1 …
closed=0`, exit 0 → exit 1. The mutant also plants a case/separator variant
(`Kasegi_R40_stray`), a family-named **regular file** (`kasegi-r42-ready` — the
r41 file-as-stray false-red class), and a stray in the `--work` area.

---

## 5. Risk notes for the L1

1. **F-FLIP and F-BIND are open in the wave-1 bytes as they stand.** §1.1 and
   §1.2 are measurements on the current lane/instrument bytes. If the landing
   takes them unchanged, the C1 kill rule's "the CURRENT suite bytes accepting
   an input within one of the seven named repair families" clause is at risk
   for J6 and J7.
2. **`ExecJ6Bind.capture-binding-check.py` being a byte copy of the committed
   instrument** is worth a glance on its own: the seat spec asks for a
   *patched* file, and this one carries no patch. Either the seat has not
   written yet, or the file was copied early.
3. **The J5 outside limb scans recursively.** Any run whose outside scope
   contains another seat's export tree (which carries tracked
   `.ufo/waves/round-4*/kasegi-r4*-*.ready` files) reads red. Measured:
   `outside=82` on a pristine fixture whose scope held a sibling export tree.
   The r42 suite should bind its outside scope to a directory it owns, or the
   counting command in the frozen claim will read red for environmental reasons.
4. **The `--selftest` cost.** RevSuitePlan measured the r41 shape at
   `real 5m47s, user 32m30s` at base. The r42 suite should keep the nested
   negative controls to one nested pass per control with a depth guard, or the
   receipt's selftest run will dominate the round's wall time.

## 6. Hygiene

* Scratch: `/fast/scratch/hyaku/kasegi-r42/ExecSelftest/` — **removed before
  yield** (verified gone).
* Disk guard green before the read pass and before the heavy runs
  (`/fast/scratch/hyaku` 27% used, 592.6G free at start; 28% / 585.5G later).
* `TMPDIR` bound to the seat scratch dir for every command that writes a
  relative path; no inherited TMPDIR relied on.
* **No tool installs** (curl, python3, git, coreutils, tar, awk, sed all
  already present). `pacman` not touched. `~/.omp/agent/RULES.md` read.
* No mutating git/jj command in the lane repo, the fleet root, or any sibling
  repo. The lane was only read (`git fetch`/`git archive`/`git log`/
  `git show-ref`). The only git writes were inside the seat's own scratch
  mirror, whose toplevel was asserted before every commit.
* No network fetches performed by this seat (none needed).
* Fleet-root tracked files untouched; the only lane writes are the two
  deliverables and this receipt, all under
  `.ufo/waves/round-42/wave1/`.

Report: `.ufo/waves/round-42/wave1/ExecSelftest.md`
