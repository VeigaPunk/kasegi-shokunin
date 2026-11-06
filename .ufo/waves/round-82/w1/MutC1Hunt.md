# MutC1Hunt — r82 C1 candidate: 22 mutants outside the frozen table

Seat: mutation-tester (leaf). Round 82, attempt 1, ONE v1 wave of 12 seats. Scope: the frozen
C1 candidate `.ufo/waves/round-82/c1/recheck-cwd-census.py` (sha256 `81677e9d…e050`), hunting
single-point mutants **outside** the frozen 63-row table, concentrated on the round-82 code:
`conform_ok`, the bucket-sum and main-default checks, `main()`'s conform/result path and
`census()`'s bucket increments. No lane file was written; every mutant ran on a copy in
`/fast/scratch/hyaku/kasegi-r82/MutC1Hunt/`.

## 1. Frozen bytes, invocation, baseline

| object | sha256 |
|---|---|
| c1/recheck-cwd-census.py (target) | `81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050` |
| c1/mutbat.py (frozen counter) | `a7d4db43cdc8b2948af9c8c5f1baee827979fbb3d7dac0f39ecd46fad60ac55c` |
| c1/mutant-table.json (frozen 63 rows) | `045edc07c9edb24cb401b241e512745cc81e4d0f36eea26e5362b49e7cc5f26a` |
| my hunt table (22 rows) | `984933a4940ed33e344bd40bffeacebe2cfe985179835a25d0529565628e6cdf` (`MutC1Hunt-rows.json`) |

Command (exactly the seat command; `$S=/fast/scratch/hyaku/kasegi-r82/MutC1Hunt`):

```
TMPDIR=$S python3 -B .../c1/mutbat.py --target .../c1/recheck-cwd-census.py \
  --table $S/hunt.json --expect-cases 24 --work $S/w --keep $S/keep
```

Counter summary (verbatim, `MutC1Hunt-receipts/hunt.out`):

```
MUTBAT target_sha256=81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050 baseline=ok rows=22 killed=14 survived=7 miskilled=0 dirty=0 notderived=0 neutral_ok=1/1 decoy=ok decoy_hidden=21/21
```

`rc=1` is the counter correctly refusing a hunt table with survivors (its `ok` requires every
non-neutral row killed); baseline, neutral and decoy limbs are green and no row was
NOT-DERIVED. Predictions (class, kill_cases, expected outcome) were written **before** the run
into `MutC1Hunt-receipts/predictions.json` (sha256 `96eb455d…f2cc`). Target sha256 before and
after the hunt is identical; the counter ran only on scratch copies.

## 2. Verbatim MUTANT lines

```
MUTANT H01-BK-NO-EXIT0 verdict=KILLED rc=1 fails=4 failed_cases=bucket-sum,gate-negpolarity,result-main,usage-guards counted=yes
MUTANT H02-BK-EXIT0-TWICE verdict=KILLED rc=1 fails=4 failed_cases=bucket-sum,gate-negpolarity,result-main,usage-guards counted=yes
MUTANT H03-BK-NORE-AS-REST verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H04-BK-NORE-AS-EXITOTHER verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H05-BK-GE verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H06-MAIN-WORD-SWAP verdict=KILLED rc=1 fails=5 failed_cases=bucket-sum,conform-limbs,gate-consume,result-main,usage-guards counted=yes
MUTANT H07-MAIN-RET-ZERO verdict=KILLED rc=1 fails=5 failed_cases=bucket-sum,conform-limbs,gate-consume,main-default,result-main counted=yes
MUTANT H08-MAIN-CONFORM-COPY verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H09-MAIN-TMPDIR-RET3 verdict=KILLED rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=yes
MUTANT H10-VERBOSE-FLAG-OFF verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H11-EXIT2-INC-ZERO verdict=KILLED rc=1 fails=2 failed_cases=first-line,prefix-census counted=yes
MUTANT H12-EXIT0-INC-ZERO verdict=KILLED rc=1 fails=10 failed_cases=both-headers,bucket-sum,gate-checkids,gate-negpolarity,prefix-census,prefix-literal,relabel-detection,restoration-only,result-main,usage-guards counted=yes
MUTANT H13-EXIT1-INC-ZERO verdict=KILLED rc=1 fails=3 failed_cases=bucket-sum,prefix-census,prefix-literal counted=yes
MUTANT H14-NORE-INC-ZERO verdict=KILLED rc=1 fails=3 failed_cases=conform-limbs,gate-checkids,relabel-detection counted=yes
MUTANT H15-REST-INC-ZERO verdict=KILLED rc=1 fails=3 failed_cases=gate-checkids,relabel-detection,restoration-only counted=yes
MUTANT H16-NOPREFIX-INC-ZERO verdict=KILLED rc=1 fails=3 failed_cases=first-line,prefix-census,prefix-literal counted=yes
MUTANT H17-BS-SWAP-SHORT verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT H18-MD-VERBOSE-INJECT verdict=KILLED rc=1 fails=1 failed_cases=main-default counted=yes
MUTANT H19-MD-NEG-WEAK verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H20-BS-SUM21-NOPREFIX verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT H21-BS-IDENT-NOT-TRUE verdict=SURVIVED rc=0 fails=0 failed_cases=- counted=no
MUTANT H22-NEU-DOC verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
```

## 3. Row ledger

`predicted` = kill_cases declared before the run; `actual` = FAIL cases observed.

| id | single point | predicted | verdict | actual | classification |
|---|---|---|---|---|---|
| H01 | bucket sum drops `exit0_foreign` | bucket-sum | KILLED | bucket-sum,gate-negpolarity,result-main,usage-guards | detector fired |
| H02 | bucket sum doubles `exit0`, drops `exit1` | bucket-sum | KILLED | same as H01 | detector fired |
| H03 | bucket-sum `norecheck` term -> `restoration_only` | bucket-sum | SURVIVED | — | **equivalent** |
| H04 | bucket sum drops `exit_other` (doubles `norecheck`) | bucket-sum | SURVIVED | — | **real gap G1** |
| H05 | `buckets == entries` -> `>=` | bucket-sum | SURVIVED | — | **real gap G2** |
| H06 | `RECHECK-CWD-RESULT` words swapped | result-main | KILLED | bucket-sum,conform-limbs,gate-consume,result-main,usage-guards | detector fired |
| H07 | main nonconformant exit 1 -> 0 | result-main | KILLED | bucket-sum,conform-limbs,gate-consume,main-default,result-main | detector fired |
| H08 | main conform line: `conform_ok(dict(counts))` | bucket-sum | SURVIVED | — | **equivalent** |
| H09 | main TMPDIR-refusal exit 2 -> 3 | tmpdir-refusal | KILLED | tmpdir-file,tmpdir-refusal | detector fired |
| H10 | `--verbose` parser sets `verbose = False` | main-default/output-lines | SURVIVED | — | **real gap G3** |
| H11 | `exit2_foreign` increment +0 | prefix-census | KILLED | first-line,prefix-census | detector fired |
| H12 | `exit0_foreign` increment +0 | prefix-census | KILLED | 10 cases incl. bucket-sum,result-main | detector fired |
| H13 | `exit1_foreign` increment +0 | prefix-census | KILLED | bucket-sum,prefix-census,prefix-literal | detector fired |
| H14 | `norecheck` increment +0 | relabel-detection | KILLED | conform-limbs,gate-checkids,relabel-detection | detector fired |
| H15 | `restoration_only` increment +0 | restoration-only | KILLED | gate-checkids,relabel-detection,restoration-only | detector fired |
| H16 | `noprefix` increment +0 | prefix-census,main-default | KILLED | first-line,prefix-census,prefix-literal | detector fired (main-default miss explained below) |
| H17 | case-21 census swap returns `bal` not `short` | bucket-sum | KILLED | bucket-sum | detector fired |
| H18 | case-22 main call gains `--verbose` | main-default | KILLED | main-default | detector fired |
| H19 | main-default negative limb -> `len(out22) > 0` | main-default | SURVIVED | — | **real gap G4** |
| H20 | case-21 `sum21` reads `noprefix` for `exit0` | bucket-sum | KILLED | bucket-sum | detector fired |
| H21 | `conform_ok(short) is False` -> `is not True` | bucket-sum | SURVIVED | — | **equivalent** |
| H22 | conform_ok docstring shortened | (neutral) | NEUTRAL-OK | — | neutral control |

Prediction note: H16 declared `main-default` as an intended kill case, but the ENTRY line prints
the **local** `noprefix` variable, not `counts["noprefix"]`; output text therefore stays correct
under the mutation and only the summary/scored counts move. The row was still counted on its
declared `prefix-census`. H01/H02/H06/H07/H12 additionally trip `result-main`/`usage-guards`/
`gate-*` because their fixtures are conformant trees whose result string or exit code moves —
collateral, not mis-kills (miskilled=0).

## 4. Survivors: 3 equivalent, 4 real gaps

Probe: `MutC1Hunt-receipts/probe_survivors.py`, output `probe.out`. It loads pristine and mutant
copies from scratch and compares only the changed functions; nothing is run against the lane
tree.

**Equivalents (must not be added as kill rows):**

- **H03** — exhaustive comparison of `conform_ok` over the 0..3^8 counts domain (65,536
  mappings): `conform_ok_diffs=0`. The `norecheck` and `restoration_only` sum terms are masked
  by the `counts["norecheck"] == 0 and counts["restoration_only"] == 0` conjuncts: when either
  is non-zero the predicate is already False, and when both are zero the substituted term
  equals the dropped one.
- **H08** — `conform_ok(dict(counts))` vs `conform_ok(counts)`: `conform_ok_diffs=0`;
  `conform_ok` only reads the mapping.
- **H21** — `conform_ok` returns only real booleans (domain values `['False','True']`), so
  `x is False` and `x is not True` agree on every reachable value
  (`isFalse_eq_isNotTrue=True`).

**Real gaps (behaviour changes the selftest does not observe):**

- **G1 / H04 — the `exit_other` term of the bucket sum is never pinned in the accepting
  direction.** Witness: `conform_ok({entries:2, noprefix:0, exit2:0, exit0:1, exit1:0,
  exit_other:1, norecheck:0, restoration_only:0})` is `True` pristine and `False` mutant — a
  conformant tree with one passing and one timed-out recheck entry is refused. The only fixture
  carrying `exit_other` is case 1, and `main()` sees it only in case 22 where `exit2_foreign`
  already forces nonconformant; `timeout-bucket` (case 17) inspects `census()` counts only and
  never `conform_ok`/`main`.
- **G2 / H05 — `>=` accepts over-accounted counts.** Witness: counts `{entries:1, exit0:1,
  exit_other:1, …}` are `False` pristine and `True` mutant (buckets 2 >= entries 1). No fixture
  has `buckets > entries`; J1-style *under*-count edits are still caught, but a
  bucket-doubling edit would no longer be.
- **G3 / H10 — the documented `--verbose` flag path is unasserted end-to-end.** On a fixture
  with one prefixed passing entry, pristine `main(..., "--verbose")` prints `ENTRY p.md`
  (`entries=1`, rc 0); the mutant prints none (`entries=0`, rc 0). The selftest has 13
  `capture(main, …)` sites and none passes `--verbose` (`main_calls=13 with_verbose_flag=0`);
  `census(verbose=True)` is likewise never called by a check. S07M pins the main()-site
  *default*, not the flag.
- **G4 / H19 — the main-default negative limb can be replaced by a non-constant tautology.**
  `"ENTRY a-prefixed.md" not in out22` -> `len(out22) > 0` survives the whole battery, because
  `gate-wiring` F1 refuses only a literal `True` or a BoolOp with a literal-True operand.
  Decisive witness: a copy carrying **H19 + S07M** (verbose default True, the exact defect
  main-default was added to kill) runs `selftest cases=24 failures=0`, rc 0 — the negative limb
  is the sole detector of S07M and it can be neutered while the battery stays green.

## 5. Kill accounting and coverage

14/21 non-neutral rows KILLED, 7 SURVIVED (3 equivalent, 4 real gaps); 0 MISKILLED, 0 DIRTY,
0 NOT-DERIVED; 1/1 neutral NEUTRAL-OK; decoy=ok with hidden anchors 21/21. The 14 kills span
every round-82 site except the conform-line copy: `conform_ok` sum terms (H01, H02), main
result string/exit code (H06, H07), TMPDIR refusal through main (H09), all six census bucket
increments (H11–H16), the bucket-sum main-swap limb (H17), the main-default positive limb
(H18) and the case-21 structural sum (H20). Only H03/H04/H05 touch the `norecheck` /
`restoration_only` / `exit_other` terms of the sum; only H05 touches the comparison operator;
only H10/H19 touch the verbose-path assertions.

Routed to round 83 (fresh coverage, not a contract change): (1) add a fixture with one
`exit_other` entry plus one passing entry and require `main()` rc 0 (G1); (2) require
`conform_ok` to refuse buckets > entries, or a double-counting census edit (G2); (3) assert
`main --verbose` prints ENTRY for a prefixed passing entry and `census(verbose=True)` does too
(G3); (4) make `gate-wiring` / main-default robust to a tautological negative limb (or add a
row that pairs H19 with S07M) (G4). Equivalents H03/H08/H21 are recorded, not routed.

## 6. Hygiene and restoration

- Target sha256 `81677e9d…e050` before and after; all mutants are byte-replacements of scratch
  copies under `$S/w`/`$S/keep`; no lane file was edited, none of `corpus/`, `SKILL.md`,
  `PROVINCE.md`, `SCORECARD.md`, `LOG.md` or any instrument was touched.
- No git/jj write; no fixture repo created; no host/sysctl change; no tool installed
  (python3 only; nothing to record).
- Scratch `$S` is deleted before yield.

## 7. Files written

- `.ufo/waves/round-82/w1/MutC1Hunt.md` (this report)
- `.ufo/waves/round-82/w1/MutC1Hunt-rows.json` — 22 rows, standard counter format
  (sha256 `984933a4…6cdf`)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/hunt.json` (same bytes as the rows file)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/hunt.out` — verbatim counter output
  (sha256 `b856f98d…29eb`)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/predictions.json` — pre-run predictions
  (sha256 `96eb455d…f2cc`)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/verdicts.json` — per-row verdict/classification
  ledger (sha256 `3a13a5f6…f622`)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/probe.out` — survivor probe output
  (sha256 `f4123f14…65d8`)
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/probe_survivors.py` — probe driver
- `.ufo/waves/round-82/w1/MutC1Hunt-receipts/h19_plus_s07m.py` — H19+S07M witness copy
  (sha256 `edbe9214…8cb0`)
