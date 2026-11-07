# ExecC1Battery — round-84 attempt 1, independent C1 scoring

Seat: ExecC1Battery (leaf). Wave: 12 seats. Scope: score claim C1 over the frozen bytes at freeze
commit `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b` (base `a089ff3d601b4d53a5515e52720ba27e5ec72c3d`).
No lane bytes edited, no git writes. Scratch `/fast/scratch/hyaku/kasegi-r84/ExecC1Battery`
(deleted before yield; cited outputs copied to `ExecC1Battery-receipts/`).

## 0. Frozen-byte integrity (claims vs disk vs freeze tree)

`sha256sum` of the worktree files (receipt `hashes.txt`):

| file | worktree sha256 | claims | freeze blob |
|---|---|---|---|
| `.ufo/waves/round-84/c1/recheck-cwd-census.py` | `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e` | same | `f31f0e2b…` |
| `.ufo/waves/round-84/c1/mutbat.py` | `c67e6912ca52dcef6c1722882e3d3b725f40a56703d65bdee402a4c8e738d6ea` | same | `dfad6c0e…` |
| `.ufo/waves/round-84/c1/mutant-table.json` | `daf05baceae8efcdce8d3968a57472b86d92de224227d311f2047fc7b677aa9e` | same | `f8ac490a…` |
| `.ufo/waves/round-84/c1/build-table.py` | `4352368e28437e3826e34689a50e83b65d874f08aef60cfe92cb8f248f4a7516` | same | `3d01e6ca…` |
| `corpus/instruments/recheck-cwd-census.py` (base) | `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` | base as claimed | — |

`git hash-object` on the eight frozen files (four `c1/` + candidate/donothing/stub receipts +
counter driver) equals the blobs in `git ls-tree 7f76b7e .ufo/waves/round-84/{c1,controls}`, and
`git log --oneline 7f76b7e..HEAD -- .ufo/waves/round-84/c1 .ufo/waves/round-84/controls` is empty:
**the frozen bytes are byte-identical to the freeze commit and nothing has touched them since.**

## 1. Predicates, independently executed

### P1 — TRUE
`TMPDIR=$S python3 -B .ufo/waves/round-84/c1/recheck-cwd-census.py --selftest` → rc=0, last line
`selftest cases=33 failures=0` (`p1.out`).

### P2 — FALSE at freeze (landing-time predicate; candidate side TRUE)
`corpus/instruments/recheck-cwd-census.py` is still the base `343b21e4…` (27 cases) — the candidate
is not landed, exactly the state the freeze predicted. The frozen candidate's hash **is** the P2
value `e5f2e4bd…`, so P2 flips TRUE iff the L1 lands these bytes unchanged.

### P3 — TRUE
`python3 -B .ufo/waves/round-84/c1/mutbat.py --target .ufo/waves/round-84/c1/recheck-cwd-census.py --table .ufo/waves/round-84/c1/mutant-table.json --expect-cases 33 --work $S/p3` → rc=0; the line contains the predicate string verbatim:

```
MUTBAT target_sha256=e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e baseline=ok rows=79 killed=76 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=75/76
```

`grep -cE '^MUTANT [^ ]+ verdict=(KILLED|EXCEPTION-KILL) '` = **76**;
`grep -cE '^MUTANT H(0[1-9]|1[0-2]) verdict=KILLED '` = **12**. Each H row's `failed_cases` equals
its table-declared `kill_cases`, and each H row fails exactly one case (`counted=yes`):

| row | failed_cases (= declared) |
|---|---|
| H01, H02 | noprefix-only |
| H03, H04 | summary-fields |
| H05 | entry-bare-pass |
| H06, H07, H09, H10 | argv-values |
| H08 | verbose-order |
| H11, H12 | entry-set |

(`p3.out`, 81 lines; my run reproduces the committed `controls/c1-candidate-r84.txt` line for line.)

### P4 — TRUE
`mutbat --selftest --work $S/p4` → rc=0, `mutbat selftest ok … r84_limbs={'extra': True, 'dup': True, 'decoy_line': True} bad_tables=[True, True, True, True]` (`p4.out`).

### P5 — TRUE
`controls/c1-counter-mutants-r84.py --lane <lane> --work $S/p5` → rc=0, and exactly:

```
COUNTER-MUTANT M09 counter=r83 rc=0 selftest=ok
COUNTER-MUTANT M10 counter=r83 rc=0 selftest=ok
COUNTER-MUTANT M12 counter=r83 rc=0 selftest=ok
COUNTER-MUTANT M09 counter=r84 rc=1 selftest=FAIL
COUNTER-MUTANT M10 counter=r84 rc=1 selftest=FAIL
COUNTER-MUTANT M12 counter=r84 rc=1 selftest=FAIL
COUNTER-MUTANTS-RESULT as-expected
```

Extra attribution I ran on the three r84 mutants (`limb/M09,10,12.py`, `m12.out`): each fails
**only** its own limb — M09 `r84_limbs={'extra': False, 'dup': True, 'decoy_line': True}`, M10
`{'extra': True, 'dup': False, 'decoy_line': True}`, M12
`{'extra': True, 'dup': True, 'decoy_line': False}`. The three r84 limbs are load-bearing
individually, not as a bundle.

### P6 — TRUE on the frozen bytes (landing-time path)
Frozen candidate with `--root <lane> --lane <lane>`: `RECHECK-CWD entries=98 noprefix=0
exit2_foreign=0 exit0_foreign=76 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` /
`RECHECK-CWD-RESULT conformant`, rc=0 (`p6conf.out`). Base bytes give the identical summary (so the
six new checks do not change census behaviour on the real tree). `entries=98` because the 98th
`corpus/knowledge/*.md` is the **uncommitted** C2 draft (`osv-gcs-data-dump-layout.md`); tracked
count is 97, matching the freeze.

### P7 — TRUE
Committed freeze receipts, read directly: `controls/c1-donothing-r84.txt` tail `rc=1` and 12 lines
matching `^MUTANT H(0[1-9]|1[0-2]) verdict=SURVIVED`; `controls/c1-stub-r84.txt` tail `rc=1` and
12 such lines. Independent reproduction of both controls:

- do-nothing: exact copy of the base bytes (`343b21e4…`) through the r84 counter → rc=1,
  `MUTBAT target_sha256=343b21e4… baseline=bad rows=79 killed=64 survived=12 miskilled=0 dirty=0
  notderived=0 neutral_ok=0/3 decoy=broken decoy_hidden=75/76`, H01–H12 all `verdict=SURVIVED`
  (`dn.out`). The 64 kills are the r83 64/64 set: the 79-row table preserves r83 kill power.
- stub: rebuilt with `controls/c1-stub-r84.py` → sha256 `e77bd5f6dd8df60df39e90e9e2d4f1c6a05cb26ab9da272baf55da98541a83c2`
  (matches the receipt header) and `selftest cases=33 failures=0` rc=0 — the stub satisfies P1's
  *shape*. Through the r84 counter it is rc=1 with
  `MUTBAT target_sha256=e77bd5f6… baseline=ok rows=79 killed=64 survived=12 miskilled=0 dirty=0
  notderived=0 neutral_ok=3/3 decoy=ok` and H01–H12 all `verdict=SURVIVED` (`stub.out`). Because
  this control's `baseline=ok`, the twelve survivors — not a bad baseline — are the sole
  differentiator between the stub and the candidate.

### P8 — FALSE at freeze (landing edit pending)
`SKILL.md:982` and `corpus/instruments/README.md:354` still pin `selftest cases=27 failures=0`
(base state, as the claim says). The L1 must rewrite both to `cases=33` at landing; the claim's P8
is then TRUE. This is the only predicate whose truth depends on a *text* edit rather than the
frozen candidate.

## 2. Corroborating checks (not predicates)

- **Table provenance**: the r84 table's first 67 rows are dict-identical to
  `.ufo/waves/round-83/c1/mutant-table.json` (0 diffs), and rows 68–79 are H01–H12 in order.
- **H rows are the r83 survivors verbatim**: each H row's `anchor`+`replacement` is byte-identical
  to one of the twelve r83 `MutC1Hunt` survivors (H01←MUT-CF-noprefix-ge, H02←MUT-CF-noprefix-ne1,
  H03←MUT-SUM-swap-exit1-other, H04←MUT-SUM-other-as-norecheck, H05←MUT-MV-drop-noprefix-pass,
  H06←MUT-AP-root-no-value, H07←MUT-AP-lane-no-value, H08←MUT-AP-verbose-as-lane,
  H09←MUT-AP-root-no-abspath, H10←MUT-AP-selftest-last, H11←MUT-MV-extra-nonzero,
  H12←MUT-MV-timeout-label). All 21 hunt rows were present in
  `.ufo/waves/round-83/w1/MutC1Hunt-rows.json`; the 9 killed ones are not re-admitted.
- **Candidate is base + six checks**: `diff` vs base removes **9** lines, all docstring text and the
  `REQUIRED_CHECKS` id tuple; no existing assertion is weakened or removed. The six added cases
  (26–31) assert observable behaviour — `conform_ok` in both polarities, the exact `RECHECK-CWD`
  field string on exit1=2/exit_other=1, default-mode `ENTRY` lines for prefix-less passers, the
  argv traps (trailing `--root`/`--lane` rc=2 + usage, relative root reported absolute, `--selftest`
  in any position), `--verbose` before `--root`, and the exact ENTRY set incl. `foreign_exit=-1`
  for a timeout.
- **Builder determinism**: `build-table.py <frozen candidate> $S/t.json` → `cmp` with the frozen
  table rc=0 (`build-table rows=79 neutral=3 new=12`). The table is derived, not hand-edited.

## 3. Findings routed to the L1 (none falsifies a predicate)

1. **D1 (claims text, minor)** — `claims.json` names the candidate receipt
   `.ufo/waves/round-84/controls/c1-candidate-r84.raw`; no `.raw` exists. The committed file is
   `c1-candidate-r84.txt` (blob `e4d555e7`, 7273 B), and it is exactly the receipt my P3 run
   reproduces. Fix the reference at landing (or note `.raw` = raw stdout form).
2. **D2 (counter usability, minor)** — `mutbat.py` exits 2 with
   `mutbat: --work … is not a directory` when `--work` does not pre-exist; the docstring/usage does
   not say so. Three of my first invocations died this way (P3, P4 and the do-nothing run each cost
   one failed start). Cheap fix: `os.makedirs(a.work, exist_ok=True)` or a usage line.
3. **N1 (binding strength)** — P3's "binds target_sha256" is *textual*: the predicate requires the
   hash inside the MUTBAT line, but `mutbat.py` has no `--expect-target-sha256` and never refuses a
   wrong target. Any target that passes all 79 rows would exit 0 and print its own hash. A
   `--expect-target-sha256 HEX` option (rc=2 on mismatch) would make the binding mechanical.
4. **N2 (maintainability)** — three of the six new checks lean on fixtures created in earlier
   cases (`_t1` case 1, `_t23` case 23, `ret25` case 25). A reorder of `selftest()` breaks
   `entry-bare-pass`, `entry-set` and `verbose-order` without any behaviour change. Local fixtures
   would decouple them.
5. **N3 (control shape)** — the do-nothing control runs `--expect-cases 33` against 27-case base
   bytes, so its rc=1 is over-determined (`baseline=bad` *and* 12 survivors). It still demonstrates
   H01–H12 surviving, but `--expect-cases 27` would isolate the survivor signal from the baseline
   signal. Non-blocking (the committed control claims only the survivors and rc=1).

## 4. Verdict

C1 as frozen: **P1 P3 P4 P5 P6 P7 TRUE on the frozen bytes; P2 P8 FALSE only because the candidate
is not landed / the two pin rows still say `cases=27`.** With the candidate landed byte-identical
and the two pins rewritten to `cases=33`, all eight predicates hold on this evidence. The claim's
"76/76 non-neutral kills, 12/12 r83 survivors closed, r84 limbs extra/dup/decoy_line load-bearing"
is reproduced independently: the candidate kills all 76 non-neutral rows with case-matched faults,
while the base bytes and the name-only stub each leave exactly H01–H12 alive (rc=1; the stub has
`baseline=ok`, so its nonzero exit comes only from those twelve survivors).

Files written by this seat:
- `.ufo/waves/round-84/w1/ExecC1Battery.md` (this report)
- `.ufo/waves/round-84/w1/ExecC1Battery-receipts/`: `hashes.txt`, `p1.out`, `p3.out`, `p4.out`,
  `p5.out`, `p6.out`, `p6conf.out`, `dn.out`, `m12.out`, `M09.out`, `M10.out`, `stub.out`
  (stub battery), `stub-hash.txt`.

No tool installed or upgraded; no host-state change; scratch removed before yield.
