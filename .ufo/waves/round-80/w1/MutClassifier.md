# MutClassifier — round-80 w1, C1 classifier probe

Seat: MutClassifier (mutation tester). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch `S=/fast/scratch/hyaku/kasegi-r80/MutClassifier` (TMPDIR=$S explicitly; no /tmp; no
git/jj writes; no installs; lane tree untouched).

**Verdict on the assigned hypothesis: CONFIRMED** — both conjuncts hold on the frozen bytes:
(1) under the frozen counter an assertion-class row is scored `EXCEPTION-KILL` (`counted=no`)
only on a FAIL detail beginning `exception=`; (2) the only two detail expressions in the frozen
candidate that begin `exception=` are the `gate-consume` and `gate-negpolarity` exception
branches (`recheck-cwd-census.py:523`, `:532`). The carve-out is *reachable* by an
assertion-shaped transform (probe 3), which is a routed r81 finding, not a verdict change: the
frozen 28-row table scores `killed=28/28` and none of its 27 assertion rows emits an
`exception=` FAIL.

## Frozen bytes (read-only; hashes as frozen, re-checked after all probes)

| file | sha256 |
|---|---|
| `.ufo/waves/round-80/c1/recheck-cwd-census.py` | `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698` |
| `.ufo/waves/round-80/c1/mutbat.py` | `b47276d1f96795d8b430de0be195f26122ffa6d673fb4b25e88250d8fcb7d450` |
| `.ufo/waves/round-80/c1/mutant-table.json` | `08d7f3cebc5b40dfb6a03a0ba5caa1f1aa848b3bbc3d9e0b6b969497098ea418` |
| `.ufo/waves/round-80/c1/build-table.py` | `e0a8c714c6941cb70b5b2a2436409dcbd75c3614455ff4b558593bccb9ee0ef3` |

Table composition confirmed from the frozen JSON: 27 rows `class=assertion`, 1 row
`class=exception` (K-M3).

## Probe 1 — every live `check(...)` detail expression in the candidate

AST walk over `check` calls with 3 args (`ast.Call`, `func.id == "check"`, `len(args) >= 3`),
with the `% (...)` BinOp peeled to its literal head. 20 live calls (the strings at :468-472 and
the `def check` at :291 are not calls):

| # | line | case | detail head | begins `exception=` |
|---|---|---|---|---|
| 1 | 315 | prefix-census | `got=%s want=%s` | no |
| 2 | 328 | result-main | `nonconformant ret=%d conformant ret=%d` | no |
| 3 | 350 | tmpdir-parent | `calls=%d dirs=%s` | no |
| 4 | 356 | scratch-cleanup | `calls=%d leftover=%d` | no |
| 5 | 368 | first-line | `got=%s want=%s` | no |
| 6 | 383 | restoration-only | `got=%s want=%s marker_present=%s` | no |
| 7 | 410 | both-headers | `got=%s want=%s first_ran=%s restoration_ran=%s` | no |
| 8 | 433 | relabel-detection | `unpatched got=%s want=%s; patched got=%s want=%s` | no |
| 9 | 460 | tmpdir-refusal | `ret=%d stdout=%r stderr=%r` | no |
| 10 | 502 | gate-predicates | `rows=%d expect=%d bad=%s` | no |
| 11 | 512 | gate-wiring | `findings=%s` | no |
| 12 | 515 | gate-regs | `registered=%s` | no |
| 13 | 542 | gate-checkids | `missing=%s extra=%s side_logs=%r` | no |
| 14 | 537 | gate-consume | `no-registration` | no |
| 15 | 538 | gate-negpolarity | `no-registration` | no |
| 16 | 526 | gate-consume | `clean_ok=%r limb_log=%r` | no |
| 17 | **523** | **gate-consume** | **`exception=%r`** | **YES** |
| 18 | 524 | gate-negpolarity | `not-evaluated-after-exception` | no (prefix is `not-`) |
| 19 | 534 | gate-negpolarity | `neg_ok=%r neg_ret_ok=%r` | no |
| 20 | **532** | **gate-negpolarity** | **`exception=%r`** | **YES** |

No other detail can begin `exception=`: every other head is a distinct literal prefix
(`got=`, `nonconformant`, `calls=`, `ret=`, `rows=`, `findings=`, `registered=`, `missing=`,
`no-registration`, `clean_ok=`, `not-evaluated-`, `neg_ok=`), and no `%s`/`%r` payload occupies
the head position. `:453` sets a local `out13 = "exception=%r" % (exc13,)` but "tmpdir-refusal"
(`:460`) interpolates it into `stdout=%r` — the FAIL head is `ret=`, not `exception=`; and since
`ret13 == 2` is false on that branch, it fails on an assertion (the `tmpdir-refusal` mutant
K-T1 receipt below shows exactly this head).

Counter side (frozen `mutbat.py:41-42, 58-66, 95`): `EXC_RE = ^selftest case=\S+ FAIL exception=`,
`FAIL_RE = ^selftest case=\S+ FAIL`; `verdict()` returns `EXCEPTION-KILL` iff rc!=0, no
`Traceback`, `fails>0`, `EXC_RE.search(out)`; `counted = (v=="KILLED") or (v=="EXCEPTION-KILL"
and class=="exception")`. So conjunct 1 is the code path, and it is anchored.

## Probe 2 — the 28 frozen rows, executed on the frozen candidate

Command (exactly the counting command, with `--keep` added for receipts):

```
TMPDIR=$S python3 -B .ufo/waves/round-80/c1/mutbat.py \
  --target .ufo/waves/round-80/c1/recheck-cwd-census.py \
  --table  .ufo/waves/round-80/c1/mutant-table.json \
  --expect-cases 15 --work $S/work --keep $S/keep
```

Summary line (rc 0): `MUTBAT target_sha256=420151fd…5698 baseline=ok rows=28 killed=28
survived=0 dirty=0 notderived=0`. All 28 rows rc=1. `FAIL_RE` matched every row (1-3 lines
each); `EXC_RE` matched **exactly one line in the whole 28-row set**:

```
K-M3 (class=exception)  selftest case=gate-consume FAIL exception=NameError("name 'out6' is not defined")
```

`exc_fails=0` for all 27 assertion-class rows. First FAIL line per row (from `$S/keep/*.out`):

| id | class | fails | first FAIL (after `selftest case=`) |
|---|---|---|---|
| K-M1 | assertion | 3 | `gate-regs FAIL registered=[]` (+ `gate-consume FAIL no-registration`) |
| K-M2 | assertion | 1 | `gate-negpolarity FAIL neg_ok=True neg_ret_ok=True` |
| K-M3 | exception | 2 | `gate-consume FAIL exception=NameError("name 'out6' is not defined")` (+ `gate-negpolarity FAIL not-evaluated-after-exception`) |
| K-M4 | assertion | 2 | `gate-predicates FAIL rows=28 expect=28 bad=[4, 5]` |
| K-M5 | assertion | 2 | `gate-wiring FAIL findings=['F3:both-headers']` |
| K-X1 | assertion | 1 | `gate-consume FAIL clean_ok=True limb_log=[]` |
| K-X2a | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[1]` |
| K-X2b | assertion | 2 | `gate-wiring FAIL findings=['F1:gate-consume:526', 'F2:gate-consume:526', 'F3:gate-consume']` |
| K-M8 | assertion | 2 | `gate-wiring FAIL findings=['F1:relabel-detection:433']` |
| K-W1 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[24, 26, 27]` |
| K-W2 | assertion | 1 | `gate-checkids FAIL missing=[] extra=[] side_logs=[[True], [], [True]]` |
| K-N1 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[15]` |
| K-P1 | assertion | 1 | `gate-checkids FAIL missing=[] extra=[] side_logs=[[True], [True], [False]]` |
| K-P2 | assertion | 2 | `gate-wiring FAIL findings=['F1:gate-predicates:502', …]` |
| K-G1 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[9, 10, 11, 13]` |
| K-C1 | assertion | 1 | `gate-wiring FAIL findings=['F1:gate-checkids:542', …]` |
| K-NP | assertion | 2 | `gate-wiring FAIL findings=['F1:gate-negpolarity:534', …]` |
| K-CL | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[26]` |
| K-T1 | assertion | 1 | `tmpdir-refusal FAIL ret=-99 stdout="exception=FileNotFoundError(2, 'No such file or directory')" stderr=''` |
| N10 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[26]` |
| N11 | assertion | 1 | `gate-predicates FAIL rows=27 expect=28 bad=[]` |
| N21 | assertion | 1 | `prefix-census FAIL got=entries=6,…,exit_other=0,…` |
| N25 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[11]` |
| N26 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[13]` |
| N27 | assertion | 1 | `gate-predicates FAIL rows=28 expect=28 bad=[21]` |
| N30 | assertion | 1 | `prefix-census FAIL got=entries=6,…,exit0_foreign=2,…` |
| T1 | assertion | 2 | `gate-wiring FAIL findings=['F4:gate-consume:526']` |
| T2 | assertion | 1 | `gate-negpolarity FAIL neg_ok=False neg_ret_ok=True` |

Two receipts matter for the classifier:

* **K-T1** is the substring-vs-anchor discriminator: its detail *contains* `exception=` but the
  FAIL head is `ret=`, so `EXC_RE` does not match and the row is `KILLED` `counted=yes`. (The
  counter's selftest T-KILL/T-EXCA toy pins the same distinction.)
* **K-M3** is the only `exception=` line in the set; it is the one row declared
  `class=exception`, and it is `counted=yes`. Its second FAIL
  (`gate-negpolarity FAIL not-evaluated-after-exception`) is an ordinary assertion FAIL and is
  *not* the reason for the verdict.

Independent cross-check: `grep -rh "selftest case=.* FAIL exception="
.ufo/waves/round-80/w1/ExecC1Battery-mutants` (the battery seat's kept outputs, read-only)
returns that same single K-M3 line, so the result is not an artifact of my scratch rerun.

Counter self-control (P8) re-executed: `TMPDIR=$S python3 -B …/mutbat.py --selftest --work $S`
→ `mutbat selftest ok got={'T-KILL': 'KILLED', …, 'T-EXCA': 'EXCEPTION-KILL'}
counted={…, 'T-EXCA': 'no'}, rc=0`.

## Probe 3 — an assertion mutant whose FAIL detail begins `exception=`

Both probes are single literal transforms on an exact scratch copy of the frozen candidate
(`pristine/recheck-cwd-census.py`, sha `420151fd…5698`), declared `class=assertion` in a
one-row scratch table, and scored by the **frozen** counter:

* **P3DEL** — delete the case-6 capture line `out6, ret6 = capture(main, …)` (the K-M3
  transform; mutant sha `81adb2300e61d3427ebb176823be4ff0772d7280d4ad1c88967f474c1bf23d20`).
* **P3RAISE** — neuter the registered RESULT predicate by making it raise:
  `ret == 1 and …` → `(1 / 0) == 1 and …` (mutant sha
  `9a5f2348210673f88b7cd12e1a1b8661ca6713483022378708b5934936b42868`).

Mutant selftests (direct, `TMPDIR=$S`):

```
P3DEL   : selftest case=gate-consume FAIL exception=NameError("name 'out6' is not defined")
          selftest case=gate-negpolarity FAIL not-evaluated-after-exception
          selftest cases=15 failures=2      rc=1
P3RAISE : selftest case=gate-consume FAIL exception=ZeroDivisionError('division by zero')
          selftest case=gate-negpolarity FAIL not-evaluated-after-exception
          selftest cases=15 failures=2      rc=1
```

Frozen counter on each (`--target pristine/… --table tableA|B.json --expect-cases 15`):

```
MUTANT P3DEL   verdict=EXCEPTION-KILL rc=1 fails=2 counted=no
MUTBAT target_sha256=420151fd…5698 baseline=ok rows=1 killed=0 survived=0 dirty=1 notderived=0   rc=1

MUTANT P3RAISE verdict=EXCEPTION-KILL rc=1 fails=2 counted=no
MUTBAT target_sha256=420151fd…5698 baseline=ok rows=1 killed=0 survived=0 dirty=1 notderived=0   rc=1
```

So the two `exception=` branches are reachable by an assertion-shaped transform, and the
counter's verdict there is `EXCEPTION-KILL` → `counted=no` for `class=assertion`. Both probes
also exhibit the "any line" property: each has a genuine assertion FAIL
(`not-evaluated-after-exception`) *and* the exception-marked FAIL, and `EXC_RE.search(out)`
over the whole output decides the verdict from the latter alone.

## Interpretation / routed finding (r81, NOT a verdict change)

* The classifier is prefix-anchored and searches the whole output, not per-check. Consequence:
  any mutant that trips `recheck-cwd-census.py:523` (or `:532`) is `EXCEPTION-KILL` regardless
  of what else failed; declared `class=assertion` it lands `counted=no` (and is tallied in
  `dirty`, because `mutbat.py`'s `else` branch counts every non-counted non-`SURVIVED` verdict
  as dirty — so the summary `dirty=` is not a count of `DIRTY` verdicts).
* The frozen table is immune only because its sole transform of that shape (K-M3) is declared
  `class=exception`; the class label is assigned from the observed FAIL shape, so it is not an
  independent predicate over the transform. A future row with the same shape declared
  assertion would show a real kill as `counted=no`.
* This does not touch C1's predicate P3 on the frozen bytes: all 28 frozen rows count killed
  (`killed=28/28`, rc 0), and no frozen assertion row emits an `exception=` FAIL. Per the
  frozen kill rule this is a routed defect for round 81 (per-check attribution of the exception
  marker, or requiring every FAIL detail to be exception-marked), never a verdict change.

## Restoration evidence

Pristine, mutated and restored bytes were run through the same bounded detector
(`--selftest` / the frozen battery):

| state | bytes | sha256 | detector |
|---|---|---|---|
| pristine (frozen) | `…/c1/recheck-cwd-census.py` | `420151fd…5698` | `selftest cases=15 failures=0`, rc 0; battery 28/28, rc 0 |
| mutant A (P3DEL) | `$S/mutA/…` | `81adb230…3d20` | rc 1, `fails=2`, 1 `exception=` FAIL |
| mutant B (P3RAISE) | `$S/mutB/…` | `9a5f2348…2868` | rc 1, `fails=2`, 1 `exception=` FAIL |
| restored (re-copy of frozen) | `$S/restored/…` | `420151fd…5698` | `selftest cases=15 failures=0`; battery `killed=28/28`, rc 0 |

The frozen candidate, counter, table and builder were never opened for write; their hashes
after all probes equal the frozen hashes above. Scratch `$S` was removed at yield time
(`D=/fast/scratch/hyaku/kasegi-r80/MutClassifier`), including every mutant, table, kept
output and battery run.

## Files written

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/MutClassifier.md` (this report).

No other lane or wave file was created or modified; no tools installed (pacman paused, none
needed).
