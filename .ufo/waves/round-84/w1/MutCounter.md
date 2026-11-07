# MutCounter — round-84 W1 mutation probe of the C1 counter

Seat: MutCounter (leaf, mutation-tester). Lane `kasegi-shokunin`, wave `.ufo/waves/round-84/w1/`.
Nothing outside this directory was edited; every mutant is a scratch copy under
`/fast/scratch/hyaku/kasegi-r84/MutCounter/` (deleted before yield). No delegation, no background
job opened by this seat beyond the two allowed concurrent P3 runs.

Frozen bytes attacked (sha256, re-measured after every run, unchanged):

| file | sha256 |
|---|---|
| `.ufo/waves/round-84/c1/mutbat.py` | `c67e6912ca52dcef6c1722882e3d3b725f40a56703d65bdee402a4c8e738d6ea` |
| `.ufo/waves/round-84/c1/recheck-cwd-census.py` | `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e` |
| `.ufo/waves/round-84/c1/mutant-table.json` | `daf05baceae8efcdce8d3968a57472b86d92de224227d311f2047fc7b677aa9e` |
| `.ufo/waves/round-83/c1/mutbat.py` (diff base) | `2f7c49d44bb1f21e8286d1a8b54d4c57bccc0be990fd7946a57813db0d81cb7d` |

r84 delta vs r83 is exactly the `r84_limbs` block in `selftest()` (mutbat.py:551-563) plus the
`r84_limbs` field in the verdict print (mutbat.py:575-580); `diff -u` shows no other hunk.

## 0. Baseline (the detector must be green before a kill counts)

| probe | command | observed |
|---|---|---|
| P4 | `python3 -B <counter> --selftest --work <scratch>` | `mutbat selftest ok … r84_limbs={'extra': True, 'dup': True, 'decoy_line': True}` rc=0 |
| P3 | `python3 -B <counter> --target <candidate> --table <table> --expect-cases 33 --work <scratch>` | rc=0, `rows=79 killed=76 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=75/76`, `target_sha256=e5f2e4bd…`, own per-row lines: 76 counting (`75×KILLED + 1×EXCEPTION-KILL`), 12 `H*` KILLED |
| P5 | `python3 -B controls/c1-counter-mutants-r84.py --lane . --work <scratch>` | `M09/M10/M12 counter=r83 rc=0 ok`, `counter=r84 rc=1 FAIL`, `COUNTER-MUTANTS-RESULT as-expected` rc=0 |

## 1. Mutants (16 single-site edits; budget was 10-15, one added, see §3)

Selftest verdict = `--selftest` on the mutant. "P3" = the frozen P3 command above over the frozen
candidate and 79-row table (run only where the selftest missed). "P5" = the control run against a
scratch lane whose r84 counter is the mutant. Site line numbers are in the frozen counter.

| id | single-site edit (site) | selftest | P3 | P5 | verdict |
|---|---|---|---|---|---|
| M01 | `apply_row` primary guard `!= 1` → `== 0` (278) | **ok rc0** | identical: rc0, `killed=76`, 76 counting, 12 H | as-expected | **SURVIVED all** |
| M02 | primary site never applied, `out = src` (280) | FAIL (`counted['T-KILL']='no'`) | not run — selftest kills | – | KILLED |
| M03 | extra guard `!= 1` → `== 0` (282) | FAIL (`r84 dup=False`) | not run | – | KILLED |
| M04 | extra loop over `()` (281) | FAIL (`r84 extra=False, dup=False`) | not run | – | KILLED |
| M05 | exception-class kill not counted (334) | FAIL (`counted['T-EXC']='no'`) | not run | – | KILLED |
| M06 | tally `killed += 1` → `survived += 1` (336) | FAIL (`r83_forgeries` legacy ok False ×3) | not run | – | KILLED |
| M07 | MUTBAT summary prints `survived` in the `killed` slot (350) | FAIL (selfdiff limb `killed=2`) | not run | – | KILLED |
| M08 | `hidden` counts every decoy, `[:2]` → all (301) | **ok rc0** | identical: `decoy_hidden=75/76`, rc0 | as-expected | **SURVIVED all** |
| M09 | battery ok `hidden >= 1` → `>= 0` (355) | **ok rc0** | identical, rc0 | as-expected | **SURVIVED all** |
| M10 | DECOY `nonce` field printed as `-` (347) | **ok rc0** | MUTBAT + all 79 per-row lines identical; only `DECOY … nonce=-` | control exits 2 (`anchor-count`) | survived semantically |
| M11 | D3 single decoy never appended (260) | FAIL (`r83_forgeries['count']=(True,True)`) | not run | – | KILLED |
| M12 | DECOY `keyed=` label always `yes` (347) | **ok rc0** | identical by construction (non-legacy path prints `yes` either way) | control exits 2 (`anchor-count`) | survived semantically |
| M13 | `r84_ok = all(r84.values())` → `True` (562) | **ok rc0** | unreachable (selftest-only code) | **unexpected rc1** | KILLED by P5 only |
| M14 | selftest `return 0 if okk else 1` → `return 1` (586) | prints `mutbat selftest ok`, rc=1 | unreachable (selftest-only) | as-expected | survived P3+P5; P4 kills |
| M15 | battery ok `killed == n_kill` → `killed >= 0` (354) | FAIL (`r83_forgeries['path']=(True,True)`) | not run | – | KILLED |
| M16 | keyed-decoy nonce `os.urandom(8).hex()` → `"0"` (297) | **ok rc0** | identical MUTBAT + per-row, rc0 (only `DECOY nonce=0`) | as-expected | **SURVIVED all** |
| | **totals** | 8 FAIL · 1 rc-only · 7 ok | 4 run, **0 detected** | 2 unexpected · 1 anchor-collision | **5 survive P3+P4+P5 semantics** |

Selftest survivors are M01, M08, M09, M10, M12 (and M16 run later), plus M13/M14 which are
invisible to P3 by construction: `main()` never calls `selftest()`, so a mutation inside
`selftest()` cannot reach a P3 run.

## 2. P3's three limbs — what they actually bind

P3's declared limbs are (a) the full MUTBAT line (incl. `target_sha256`, `baseline`, `rows`,
`killed/survived/miskilled/dirty/notderived`, `neutral_ok`, `decoy`, `decoy_hidden`), (b) the
counter's own per-row `MUTANT … verdict=` lines (76 counting, 12 `H0*`/`H1[0-2]` KILLED), (c)
`target_sha256`. Measured P3 impact of every mutant that reached it:

- M01, M08, M09, M16: byte-identical MUTBAT line and per-row lines, rc 0 — **all three limbs
  blind**. M08 is blind because `decoy_hidden=75/76` is unchanged (`decoy_src[:2]` vs all decoys
  coincides on this table: D3's chosen row was already hidden by D1/D2 in all nine observed runs —
  6 P3 runs here plus the three committed r84 control receipts).
- M10: identical MUTBAT + per-row; the only difference is the `DECOY` line, which P3 does not read.
- M07 (killed by selftest) *would* have been caught by limb (a) (`killed=0`), M05 by limb (a)
  (`killed=75`), M02/M03/M04 by limb (a)+(b), M15 by rc≠0. So P3's limbs are strong on the
  summary/per-row surface and blind on the decoy/nonce surface and on guard weakening that the
  79-row table happens not to exercise (the table has zero duplicate primary anchors — verified:
  all 79 rows have `src.count(anchor)==1`).

## 3. P5 attack — can an r84 mutant pass the control?

Control re-run on the frozen lane: `COUNTER-MUTANTS-RESULT as-expected`, rc 0 (P5 holds).
Then the same control over scratch lanes whose **r84 counter is a mutant** (`c1-counter-mutants-r84.py
--lane <scratch lane>`; r83 counter pristine in each lane):

| r84 counter in lane | control result | meaning |
|---|---|---|
| pristine | as-expected rc0 | control is green at freeze |
| M01 | as-expected rc0 | control blind |
| M08 | as-expected rc0 | control blind |
| M09 | as-expected rc0 | control blind |
| M16 | as-expected rc0 | control blind — and this one re-opens a forgery class (§4) |
| M14 | as-expected rc0 | control blind; P5 never runs the *unmutated* r84 counter, so a permanently-red selftest is green here (P4 catches it) |
| M13 | **unexpected rc1** | control kills `r84_ok = True` through its own M09/M10/M12 composition |
| M10, M12 | control **rc=2 `anchor-count`** | detected only as *format coupling*: both mutants rewrite the exact two-line `lines.append("DECOY …)` block that the control's M12 anchor quotes |

So: **yes, an r84 mutant can pass P5** — four demonstrated (M01, M08, M09, M16), and M14 passes P5
when P4 is not run. P5's DECOY-line pinning is anchor identity, not value checking: a value-only
change to `nonce` (M10) or to the `keyed=` expression (M12) is invisible, and the equivalent
edit expressed *off* the quoted block (M16, the nonce source) leaves the control fully green.

## 4. Routed defects (counter coverage, not claim falsification)

All predicates P3/P4/P5 are **true** on the frozen bytes (baseline above). These are the coverage
holes a mutation probe finds; each is a routed defect with a re-runnable command.

**D1 (Major) — nothing pins keyed-decoy nonce freshness; a constant nonce restores the round-82
hash-whitelist forgery that r83 claims closed.** Mutant M16 (line 297) survives P3, P4 and P5.
Kill-power demonstration (`MutCounter-receipts/demo-hashwl.txt`): a `FORGERY_SELFDIFF` variant that
whitelists the sha256 of its own D1, D2 **and D3** decoy cores is
`decoy=broken`, `battery_ok=False` under the pristine random-nonce counter and
`decoy=ok`, **`battery_ok=True`** under M16. Reproduce:

```
python3 -B .ufo/waves/round-84/c1/mutbat.py --selftest --work <scratch>            # green
python3 -B <scratch>/M16.py --target .ufo/waves/round-84/c1/recheck-cwd-census.py \
    --table .ufo/waves/round-84/c1/mutant-table.json --expect-cases 33 --work <scratch>  # rc0, killed=76
python3 -B .ufo/waves/round-84/controls/c1-counter-mutants-r84.py --lane <scratch-lane> --work <scratch>  # as-expected
```

**D2 (Minor) — the primary-anchor uniqueness guard is unpinned (mutbat.py:278).** M01
(`!= 1` → `== 0`) survives the selftest (the r84 `dup` limb only exercises the *extra* guard, 282),
P3 (no table row has a duplicate anchor) and P5. A table row whose primary anchor occurs twice
would then be "derived" and silently applied to the first occurrence.

**D3 (Minor) — the `hidden >= 1` decoy-power gate is unpinned (355) and M08 makes it weaker.**
M09 (`>= 0`) and M08 (`decoy_src[:2]` → all decoys) both survive everything. M08 additionally lets
the D3 single decoy satisfy `decoy_hidden >= 1`, so a table that D1/D2 hide nothing in would pass
the decoy-power gate that P3's `decoy_hidden=75/76` is supposed to certify.

**D4 (Minor) — the DECOY line's field values are unpinned.** M10 (nonce → `-`) and M12 (keyed label
always `yes`, so a legacy run is misreported) pass the selftest, P3 and (as values) P5; only the
control's anchor quoting notices, and it reports rc=2 rather than the defect. The r84 limb tests
`startswith("DECOY keyed=yes nonce=")` and `" d3_row="`, i.e. field *presence*, not content.

**D5 (Info) — selftest rc and verdict string are never paired.** M14 prints
`mutbat selftest ok` with rc=1; P5 reads only the stdout substring and stays green. P4's exit code
is the only killer, and P4 is not part of P5.

## 5. Cheapest killing assertions (each validated: pristine green, mutant red)

`MutCounter-receipts/probe-limb.py` injects candidate limbs into `r84` (dict is extensible; printed
as extra keys). Measured, `pristine rc0 ok` / each mutant `rc1 FAIL` on its intended key only:

| limb (added inside `selftest()`, before `r84_ok = all(r84.values())`) | kills | receipt |
|---|---|---|
| `r84.update({"primary_dup": apply_row("a\nb\na\n", {"anchor": "a\n", "replacement": "c\n", "class": "assertion", "kill_cases": ["a"]}) is None})` | M01 | `probe2-M01.txt` (`primary_dup=False`) |
| 6-line `vsrc` target (`GOOD = True` … `sys.exit(1 if _fails else 0)`) + row set `[T-VIS(GOOD=True→False, kill_cases=["b"]), T-NV(neutral)]` + `ok_vis, lines_vis = battery(vpath, vis, 1, d, nonce="00000000000000a1")` + `"hidden_src": (not ok_vis) and "decoy_hidden=0/1" in lines_vis[-1]` | M08, M09 | `probe2-M08.txt`, `probe2-M09.txt` (`hidden_src=False`) |
| `_okn, _ln = battery(toy, good, 2, d, nonce="00000000000000a1")` + `"nonce_field": "nonce=00000000000000a1" in _ln[-2]` | M10 | `probe2-M10.txt` |
| `_okl, _ll = battery(toy, good, 2, d, legacy=True)` + `"legacy_keyed": "keyed=no" in _ll[-2]` | M12 | `probe2-M12.txt` |
| `_o1, _l1 = battery(toy, good, 2, d)` / `_o2, _l2 = battery(toy, good, 2, d)` + compare the `nonce=` field of `_l1[-2]` and `_l2[-2]` (`nonce_fresh`) | **M16 (D1)** | `probe3-M16.txt` (`nonce_fresh=False`), `probe3-PRISTINE.txt` (True) |

M13 (`r84_ok=True`) needs no new limb: P5's existing three mutants already kill it (§3). M14 needs
P4's exit code, or one line pairing rc with the verdict string in `main()`/`selftest()`.
The `hidden_src` limb doubles as the kill for M08 and M09; the `nonce_fresh` limb is the only
cheap detector found for the D1 forgery class.

## 6. Limits of this probe

- The probe covers the counter only; the candidate's 33-case selftest and the 79-row table's
  row-level quality are other seats' items. P3 was run 5× over frozen bytes, always rc0.
- M12's P3 impact is a code-path argument (non-legacy always prints `yes`), not an executed run;
  M13/M14 are unreachable from `main()` (`selftest()` is not called there).
- The hash-whitelist demonstration uses the counter's own `FORGERY_HASHWL_BASE` and the selftest's
  `good` row set; it is a kill-power probe of the decoy limb, not a new target forgery class.
- Two P3 runs at a time at most; all scratch under `/fast/scratch/hyaku/kasegi-r84/MutCounter/`,
  deleted at yield.

## 7. Receipts

Beside this file in `MutCounter-receipts/`: `hashes.txt`, `mutants.json` (all 16 edits + sha256),
`selftest-M0[1-9]/M1[0-6].txt`, `p3-base.txt`, `p3-M01/M08/M09/M10/M16.txt`, `p5-*.txt`
(pristine, M01, M08, M09, M10, M12, M13, M14, M16), `probe-limb.py`, `probe2-*.txt`,
`probe3-*.txt`, `demo-hashwl.txt`, `p5-attack.sh`, `apply.py`.
