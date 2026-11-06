# ExecC1Battery — C1 scored receipt (round-82 attempt 1)

Seat: ExecC1Battery (leaf; single-labrat allowance unused; no other seat spawned).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Freeze commit under test: b9589300810a477f4d6794bfabc24b22fb50b846 (== HEAD at run time); base 1a50638edabb9bd1a4a4784774fc984cb5f2360f.
Scratch: /fast/scratch/hyaku/kasegi-r82/ExecC1Battery (TMPDIR passed explicitly; removed before yield).
Tooling: none installed or upgraded. Lane tree not edited; no git/jj writes anywhere. All work is read-only over the frozen bytes plus the wave-dir report/receipts.

Assignment: score C1 with the frozen r82 counter (the scored receipt). Items (1)-(6) below.

## 1. Frozen-byte hash conformance (claims.json C1 candidate/counter fields)

`sha256sum` over .ufo/waves/round-82/c1/* and the forgery driver, compared with the C1 claim text:

| artefact | observed sha256 | claimed in claims.json | match |
|---|---|---|---|
| c1/recheck-cwd-census.py | 81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050 | 81677e9d…e050 (candidate) | MATCH |
| c1/mutbat.py | a7d4db43cdc8b2948af9c8c5f1baee827979fbb3d7dac0f39ecd46fad60ac55c | a7d4db43…c55c (counter) | MATCH |
| c1/mutant-table.json | 045edc07c9edb24cb401b241e512745cc81e4d0f36eea26e5362b49e7cc5f26a | 045edc07…f26a | MATCH |
| c1/build-table.py | 07727196c26cd83b2f016d3d976fa2ffaaaf26b54e14c701a0a5957ca9885785 | 07727196…5785 | MATCH |
| controls/c1-forgeries-r82.py | 52cc6be5aa9d72c9d0644c1d97e252b215d792e5c00445417aa477d004d53908 | 52cc6be5…3908 | MATCH |

Freeze-commit blob identity (read-only git): `git ls-tree -r b9589300 -- …` yields
83cdb5ef build-table.py, 57fd2c24 mutant-table.json, 33163024 mutbat.py, b2ffa055 recheck-cwd-census.py, eefb59c8 c1-forgeries-r82.py; `git hash-object` on the five worktree files yields the same five blob ids, and `git status --porcelain` over those paths is empty. HEAD prints b9589300810a477f4d6794bfabc24b22fb50b846.
=> P2 true; no frozen byte differs from the freeze commit.

## 2. P3 — frozen counter, two runs

Command (both runs, cwd = lane root):

    TMPDIR=$S python3 -B .ufo/waves/round-82/c1/mutbat.py \
      --target .ufo/waves/round-82/c1/recheck-cwd-census.py \
      --table .ufo/waves/round-82/c1/mutant-table.json \
      --expect-cases 24 --work $S/w1   (run 1; run 2 uses $S/w2)

Run 1: rc=0. Every MUTANT line and the MUTBAT line, verbatim:

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 failed_cases=gate-consume,gate-negpolarity,gate-regs counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=gate-consume,gate-negpolarity counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 failed_cases=gate-negpolarity,gate-predicates counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-X1 verdict=KILLED rc=1 fails=1 failed_cases=gate-consume counted=yes
MUTANT K-X2a verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-X2b verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-M8 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-W1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-W2 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-N1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-P1 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-P2 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-G1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-C1 verdict=KILLED rc=1 fails=1 failed_cases=gate-wiring counted=yes
MUTANT K-NP verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-CL verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-T1 verdict=KILLED rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=yes
MUTANT N10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N21 verdict=KILLED rc=1 fails=2 failed_cases=prefix-census,timeout-bucket counted=yes
MUTANT N25 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N26 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N27 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N30 verdict=KILLED rc=1 fails=1 failed_cases=prefix-census counted=yes
MUTANT T1 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT T2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT M1 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-file counted=yes
MUTANT M2 verdict=KILLED rc=1 fails=1 failed_cases=timeout-bucket counted=yes
MUTANT S01 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S02 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S04 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S05 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S37 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S07 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S19 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S20 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S21 verdict=KILLED rc=1 fails=2 failed_cases=main-default,output-lines counted=yes
MUTANT S22 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S08 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S09 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S41 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S40 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S12 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S13 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S14 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S16 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S15 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S43 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S25 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-unset counted=yes
MUTANT S30 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S31 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S39 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT NT1 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT2 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT3 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT J1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT S07M verdict=KILLED rc=1 fails=1 failed_cases=main-default counted=yes
MUTANT B1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT B2 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTBAT target_sha256=81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050 baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60
```

Run 2: rc=0. Every MUTANT line and the MUTBAT line, verbatim:

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 failed_cases=gate-consume,gate-negpolarity,gate-regs counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=gate-consume,gate-negpolarity counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 failed_cases=gate-negpolarity,gate-predicates counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-X1 verdict=KILLED rc=1 fails=1 failed_cases=gate-consume counted=yes
MUTANT K-X2a verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-X2b verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-M8 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-W1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-W2 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-N1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-P1 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-P2 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-G1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-C1 verdict=KILLED rc=1 fails=1 failed_cases=gate-wiring counted=yes
MUTANT K-NP verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-CL verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-T1 verdict=KILLED rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=yes
MUTANT N10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N21 verdict=KILLED rc=1 fails=2 failed_cases=prefix-census,timeout-bucket counted=yes
MUTANT N25 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N26 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N27 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N30 verdict=KILLED rc=1 fails=1 failed_cases=prefix-census counted=yes
MUTANT T1 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT T2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT M1 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-file counted=yes
MUTANT M2 verdict=KILLED rc=1 fails=1 failed_cases=timeout-bucket counted=yes
MUTANT S01 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S02 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S04 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S05 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S37 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S07 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S19 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S20 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S21 verdict=KILLED rc=1 fails=2 failed_cases=main-default,output-lines counted=yes
MUTANT S22 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S08 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S09 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S41 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S40 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S12 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S13 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S14 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S16 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S15 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S43 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S25 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-unset counted=yes
MUTANT S30 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S31 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S39 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT NT1 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT2 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT3 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT J1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT S07M verdict=KILLED rc=1 fails=1 failed_cases=main-default counted=yes
MUTANT B1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTANT B2 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes
MUTBAT target_sha256=81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050 baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60
```

Per-row agreement: `diff -u` of the two full transcripts rc=0 (zero lines of difference; receipts/ExecC1Battery-receipts/p3-diff.txt is empty). Both runs: 63 MUTANT lines, 59 KILLED + 1 EXCEPTION-KILL + 3 NEUTRAL-OK; 63 unique row ids; 60 counted kills; `diff` covers the MUTBAT line too.
MUTBAT suffix: both lines end exactly with `baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60` (checked with `str.endswith`).
Independent cross-check against the table: every counted row's `failed_cases` intersects its declared `kill_cases` (60/60), every neutral row is rc=0/fails=0/`-`, no row has an unexpected verdict (`bad=[]`).
K-M3 is the one EXCEPTION-KILL; the table row's class is `exception`, so the counter's `counted` rule accepts it (mutbat verdict(), lines 103-114). It contributes to killed=60.
=> P3 true (baseline=ok, killed=60, survived=0, miskilled=0, dirty=0, notderived=0, neutral_ok=3/3, decoy=ok, decoy_hidden=59/60).

Note on the declared limit: decoy_hidden is 59/60, not 60/60 - matching the claim (decoy_hidden >= 1) and the frozen control; the known AST-embedding forgery F8 is the limit, not a P3 condition.

## 3. P1 — candidate selftest

    TMPDIR=$S python3 -B .ufo/waves/round-82/c1/recheck-cwd-census.py --selftest

rc=0. Cases line, verbatim:

```
selftest cases=24 failures=0
```

FAIL lines: none (`^FAIL` count = 0 across all 24 case lines). The two new r82 cases are present and pass: `selftest case=bucket-sum ok entries=3 buckets=3 main_ret=0 short_ret=1` and `selftest case=main-default ok lines=7 ret=1`.
=> P1 true.

## 4. P9 — counter selftest

    TMPDIR=$S python3 -B .ufo/waves/round-82/c1/mutbat.py --selftest --work $S/self

rc=0. Output line, verbatim:

```
mutbat selftest ok got={'T-KILL': 'KILLED', 'T-MIS': 'MISKILLED', 'T-SURV': 'SURVIVED', 'T-ABSENT': 'NOT-DERIVED', 'T-EXC': 'EXCEPTION-KILL', 'T-EXCA': 'EXCEPTION-KILL', 'T-NEU': 'NEUTRAL-OK', 'T-NEUBAD': 'NEUTRAL-BROKEN'} counted={'T-KILL': 'yes', 'T-MIS': 'no', 'T-SURV': 'no', 'T-ABSENT': 'no', 'T-EXC': 'yes', 'T-EXCA': 'no', 'T-NEU': 'yes', 'T-NEUBAD': 'no'} all_killed_exit=True location_forgery_exit=False baseline_forgery_exit=False selfdiff_forgery_exit=False bad_tables=[True, True, True]
```

Line begins `mutbat selftest ok`, contains `selfdiff_forgery_exit=False`; rc=0.
=> P9 true.

## 5. Named rows vs declared kill_cases

All four are non-neutral assertion rows; each verdict is KILLED on a case that is in its declared `kill_cases` list.

| row | MUTANT line (run 1 and run 2 identical) | declared kill_cases (table) | matches declaration |
|---|---|---|---|
| J1 | `MUTANT J1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes` | ["bucket-sum"] | YES - failed case = bucket-sum |
| S07M | `MUTANT S07M verdict=KILLED rc=1 fails=1 failed_cases=main-default counted=yes` | ["main-default"] | YES - failed case = main-default |
| B1 | `MUTANT B1 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes` | ["bucket-sum"] | YES - failed case = bucket-sum |
| B2 | `MUTANT B2 verdict=KILLED rc=1 fails=1 failed_cases=bucket-sum counted=yes` | ["bucket-sum"] | YES - failed case = bucket-sum |

(J1 = r81 junk edit that the r81 counter passed, now killed on bucket-sum; S07M = r81 main()-site verbose survivor, now killed on main-default; B1 = conform_ok loses the bucket-sum conjunct; B2 = main() ignores the bucket sum. Table rows read from c1/mutant-table.json: J1 anchor `counts["entries"] += 1`, S07M anchor `root, lane, verbose = ".", DEFAULT_LANE, False`, B1 anchor `and buckets == counts["entries"])`, B2 anchor `conform = conform_ok(counts)`.)

## 6. Table rebuild against the frozen table

    python3 .ufo/waves/round-82/c1/build-table.py .ufo/waves/round-82/c1/recheck-cwd-census.py $S/t.json \
      && cmp $S/t.json .ufo/waves/round-82/c1/mutant-table.json

Output, verbatim:

```
build-table rows=63 neutral=3 new=4 reanchored=2
build_rc=0
cmp_rc=0
```

The builder regenerates 63 rows with 3 neutral, 4 new (J1 S07M B1 B2) and 2 re-anchored (S04 S05), and the rebuild is byte-identical to the frozen table (`cmp` rc=0). Consistent with the claim's 63-row description and the freeze blob 57fd2c24.

## Rolling status of C1 predicates exercised by this seat

| predicate | exercised | result |
|---|---|---|
| P1 | yes | cases=24 failures=0, rc=0 -> true |
| P2 | yes | candidate hash 81677e9d…e050 = claim; worktree = freeze blobs -> true |
| P3 | yes (x2) | baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60, rc=0 -> true |
| P4-P8 | no | out of this seat's assignment (attack/other seats); not scored here |
| P9 | yes | mutbat selftest ok … selfdiff_forgery_exit=False, rc=0 -> true |

## Findings / risks / blockers

- No defect found in the frozen C1 scoring path as exercised: (1) all five frozen artefacts match claims.json and the freeze commit; (2) the counter twice returns the exact declared receipt over the 63-row table with 60 counted kills (59 KILLED + 1 EXCEPTION-KILL) and 3 neutral; (3) candidate selftest 24/24; (4) counter selftest ok with selfdiff_forgery_exit=False; (5) J1, S07M, B1, B2 each die on their declared case; (6) the table rebuilds byte-identically.
- Risk / recorded limit (routed, not a P3 failure): decoy_hidden=59/60, i.e. one of the 60 counted rows is not hidden by the counter-owned decoy limb; the claim declares only decoy_hidden >= 1 and the F8 AST-embedding forgery is the declared limit for P4. Round-83 routing material only.
- Risk: EXCEPTION-KILL row K-M3 is counted via its table `class: exception`; if a future table mislabels a row's class, the counter's counted rule (mutbat.py:103-114, 241) would flip. Not exercised as a fault here; table's K-M3 class is `exception`.
- No tool installs; no host changes; no scratch residue (scratch removed before yield). No blockers.

## Files written by this seat

- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery.md (this report)
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery-receipts/p1.txt
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery-receipts/p9.txt
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery-receipts/p3-run1.txt
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery-receipts/p3-run2.txt
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/ExecC1Battery-receipts/p3-diff.txt (empty: runs byte-identical)
