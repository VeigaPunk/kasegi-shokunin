# MutCounter — round 82, attempt 1, wave 1 (C1 counter's new decoy limb)

Seat: MutCounter (leaf, no dispatch). Claim probed: **C1 depth:verifiability** — the round-82
counter's **new decoy limb** (`.ufo/waves/round-82/c1/mutbat.py`). 18 single-point mutants of
`run_decoy`, `rename_locals` and the decoy/hidden terms of the final `ok` expression, each run
through three independent detectors. **10 killed / 8 survived; no mutant makes a frozen predicate
false while surviving all three.**

Frozen bytes, hashed before and after this seat (identical):

| file | sha256 |
|---|---|
| `.ufo/waves/round-82/c1/mutbat.py` (mutated here, in scratch only) | `a7d4db43cdc8b2948af9c8c5f1baee827979fbb3d7dac0f39ecd46fad60ac55c` |
| `.ufo/waves/round-82/c1/recheck-cwd-census.py` = `corpus/instruments/recheck-cwd-census.py` (battery target) | `81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050` |
| `.ufo/waves/round-82/c1/mutant-table.json` (63 rows) | `045edc07c9edb24cb401b241e512745cc81e4d0f36eea26e5362b49e7cc5f26a` |
| `.ufo/waves/round-82/controls/c1-forgeries-r82.py` | `52cc6be5aa9d72c9d0644c1d97e252b215d792e5c00445417aa477d004d53908` |

Nothing outside `/fast/scratch/hyaku/kasegi-r82/MutCounter/` and this wave directory was
written; the lane instrument, table, driver and candidate were only read. No tool installs
(Python 3.14.8, `python3 -B`, no pacman/no network).

## Method

18 mutants, each **one** textual transform of a scratch copy (`m/base.py`, sha `a7d4db43…`).
Before writing each mutant the anchor was asserted to occur **exactly once** in the frozen bytes
(`occ=1`, recorded in `mutants.json`), and each mutant is compile-checked; the builder
(`make_mutants.py`) reproduces all 18 mutant hashes from the frozen bytes. Diffs:
`MutCounter-receipts/mutants.diff`.

Detectors, same three for every mutant (and for the pristine control):

- **P9** — the counter's own detector: `python3 -B <mutant> --selftest --work <scratch>`.
- **P4 r82 arm** — `controls/c1-forgeries-r82.py` copied to scratch with exactly one change:
  the `counter=r82` path is redirected to the mutant (`MUT_COUNTER`), the r81 arm left intact
  (`driver-patch.diff`). Kill signal: **F6-selfdiff or F7-wsnorm `counter=r82` rc=0** (a
  table-reading forgery that the frozen counter rejects now passes). F8-astembed rc=0 is the
  declared limit under both counters and is not a kill signal.
- **P3** — frozen candidate + frozen table, `--expect-cases 24`, `--work <scratch>`. Kill
  signals: **rc≠0** (`P3-rc`: the counter fails/accepts wrongly) or **rc=0 but the printed
  `MUTBAT` line does not end with the frozen P3 suffix** (`P3-line`: the counter's own exit code
  is 0, but the scored P3 predicate is still false because P3 pins `decoy=ok decoy_hidden=59/60`
  literally).

Control **MC00** (unmodified copy) reproduces the frozen receipt exactly: selftest rc=0; F6/F7
r82 rc=1, F8 r82 rc=0; P3 rc=0 with
`… neutral_ok=3/3 decoy=ok decoy_hidden=59/60` (`control-pristine.txt`). Costs: selftest
0.1–0.8 s, P3 74–81 s, driver 51–115 s; the 19-run batch took 651 s wall at 5 concurrent runs
(each job `TMPDIR`-isolated under scratch).

## Results

| id | change (one point each) | selftest rc | F6 r82 | F7 r82 | P3 rc | hidden | verdict |
|---|---|---|---|---|---|---|---|
| MC00 | pristine control | 0 | 1 | 1 | 0 | 59/60 | control ok (exact P3 line) |
| MC01 | `for decoy in (d1, d2)` → `(d1,)` (drop D2 execution) | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC02 | `for decoy in (d1, d2)` → `(d2,)` (drop D1 execution) | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC03 | `return ok, [d1, d2]` → `[d1, d1]` (return D1 twice) | 0 | 1 | 1 | 0 | 39/60 | killed: P3-line |
| MC04 | `hidden >= 1` → `hidden >= 0` | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC05 | final `ok`: `decoy_ok` conjunct → `True` | 1 | **0** | **0** | 0 | 59/60 | killed: P9 + P4 |
| MC06 | `run_decoy` returns `True` unconditionally | 1 | **0** | **0** | 0 | 59/60 | killed: P9 + P4 |
| MC07 | arg guard inverted (`if arg is None:`) → crash | 1 | 1 | 1 | 1 | – | killed: P9 + P3-rc |
| MC08 | rename excludes `module_names`? dropped (`- module_names`) | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** (equivalent) |
| MC09 | rename excludes call keywords? dropped (`- keywords`) | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** (equivalent) |
| MC10 | except-as handler renamed with `""` (no rename) | 0 | 1 | 1 | 1 | 59/60 | killed: P3-rc |
| MC11 | hidden comprehension drops `class != "neutral"` filter | 1 | 1 | 1 | 0 | 61/60 | killed: P9 + P3-line |
| MC12 | `hidden >= 1` → `hidden >= 2` | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC13 | hidden `any(... for d in decoy_src)` → `decoy_src[:1]` | 0 | 1 | 1 | 0 | 39/60 | killed: P3-line |
| MC14 | decoy accumulator `ok = ok and …` → `ok = ok or …` | 1 | **0** | **0** | 0 | 59/60 | killed: P9 + P4 |
| MC15 | D2 built without `rename_locals` | 0 | 1 | 1 | 0 | 39/60 | killed: P3-line |
| MC16 | decoy parse failure `return False, None` → `True, None` | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC17 | `clean_pass` drops `"Traceback" not in out` | 0 | 1 | 1 | 0 | 59/60 | **SURVIVED** |
| MC18 | arg seeding skipped cleanly (`local.add(arg.arg)` → `pass`) | 0 | 1 | 1 | 0 | 57/60 | killed: P3-line |

Kill attribution: **P9 kills 5** (MC05, MC06, MC07, MC11, MC14), **P4 kills 3** (MC05, MC06,
MC14 — all already P9-killed), **P3 kills 7** (rc: MC07, MC10; line: MC03, MC11, MC13, MC15,
MC18), **union 10**. P9 and P4 have **no unique kill** on this mutant set; the only detector
that catches MC03/MC10/MC13/MC15/MC18 is P3 — and for four of those, only through P3's literal
`decoy_hidden=` value, the counter itself exiting 0.

## Findings (routed, not verdict changes)

1. **The executed decoy set is unverified (MC01, MC02).** Dropping either decoy's *execution*
   leaves all three detectors green: `hidden` is computed from the **generated** sources
   (`decoy_src`), not from what ran, and both forgeries fail under **either** decoy (proved by
   MC01 rc=1 under D1-only and MC02 rc=1 under D2-only). So the docstring's "runs each" property
   — the whole reason for two decoys — is generated, not observed. A counter that runs one decoy
   passes P9, P4 and P3 with the exact frozen line.
2. **`hidden >= 1` is never exercised (MC04).** `decoy_hidden=0` is accepted by every control:
   no selftest toy and no frozen target has all anchors surviving both decoys. Removing the guard
   is invisible. The guard is the limb's only defence against a table whose anchors are all
   unparse-stable.
3. **The hidden count's value is pinned only by P3's literal line (MC03, MC13, MC15, MC18).**
   Replacing `[d1, d2]` with `[d1, d1]` (39/60), counting only `decoy_src[:1]` (39/60), building
   D2 without the rename (39/60), or skipping parameter seeding (57/60) all leave selftest and
   forgery control green and the counter's own exit code 0; only the frozen P3 suffix
   (`… decoy_hidden=59/60`) fails. The counter never self-asserts the count.
4. **The except-as renaming is pinned only by the frozen candidate (MC10).** The counter's TOY
   never executes an except body, so `name += "_d"` → `name += ""` passes P9; the candidate's
   `except SystemExit as exc19` body does run and the renamed decoy dies with
   `NameError: name 'exc19_d' is not defined` (`mc10-decoy-nameerror.txt`), so only P3 sees it
   (`decoy=broken`, rc 1).
5. **The two enforcement points are double-pinned, with different observability (MC05, MC06).**
   Removing the final `decoy_ok` conjunct makes F6/F7 rc=0 while the forgery's own summary still
   reads `decoy=broken` — the mutant *detects* but does not *enforce*. Forcing `run_decoy`'s
   return makes the same forgeries pass with `decoy=ok` — the mutant is blind. Both are killed by
   P9 (`selfdiff_forgery_exit=True`) **and** by P4; these are the only mutants that invert the
   frozen P4 limb, and none survives.
6. **MC07 is a crash mutant, not a verdict** (`rename-args-guard-inverted`): `arg.arg` is read
   while `arg` is `None` (vararg/kwarg), so `rename_locals` raises `AttributeError`, selftest
   rc=1 and P3 rc=1 with no `MUTBAT` summary. It fails closed (P3 has no line) but as an
   uncaught internal exception. MC18 is the non-crashing form of "rename skips args" and is
   caught only by P3-line.
7. **MC08 and MC09 are equivalent mutants on the frozen inputs** — not live defects. The
   candidate has **no** function-local name that collides with a module-level binding
   (`loc ∩ module_names = ∅`), and its only keyword/local collisions (`env`, `prefix`) are
   call-site keyword names of external callees (`subprocess.run(env=…)`, `mkdtemp(prefix=…)`), so
   renaming those locals is harmless. The two exclusions are untested by every control.
8. **The neutral filter in `hidden` is pinned exactly once (MC11).** The selftest's TOY catches
   `hidden` counting neutral rows only because T-NEU's anchor contains the parameter `x`, which
   D2 renames: the counter prints `decoy_hidden=3/2` and the `"decoy_hidden=2/2"` assertion fails.
   Without that single string assertion, P3's line (61/60) would be the only detector.
9. **Unexercised thresholds/branches (MC12, MC16, MC17).** `hidden >= 2` (tightening) is
   invisible; the `SyntaxError/ValueError` branch of `run_decoy` is unreachable (its `True, None`
   variant would count all 60 rows and print 60/60); the `"Traceback" not in out` clause of
   `clean_pass` (shared by baseline and both decoys) is never reached by a clean-exit traceback.

## Routed defects (round 83; no predicate edit, no verdict change)

- **RD-1 (from MC01/MC02)** decoy-execution set unobserved. Control shape: a toy whose anchor
  vanishes under exactly one of D1/D2, plus an assertion that names *which* decoy failed (or a
  run counter), so that a counter running one decoy fails P9.
- **RD-2 (from MC04)** `hidden >= 1` unexercised. Control shape: a toy whose anchors survive both
  decoys (hidden=0) and the counter must exit 1.
- **RD-3 (from MC03/MC13/MC15/MC18)** the hidden count is not self-asserted; the value is pinned
  only by P3's literal. Control shape: a toy with a known mixed anchor set and an assertion of
  the exact `hidden` value, so the count is a property, not a constant.
- **RD-4 (from MC10)** except-as renaming only observable via the frozen candidate. Control
  shape: a TOY case whose except body executes (deliberate raise), exercising handler renaming
  inside P9.
- **RD-5 (from MC12/MC16/MC17)** threshold, parse-failure branch and Traceback clause are
  unexercised (fail-closed today).
- **RD-6 (from MC08/MC09)** the `module_names` and `keywords` exclusions are untested; harmless
  on the frozen inputs (equivalent mutants).

## Verdict for C1's counter

Within the probed mutant set the decoy limb is **not inverted**: every mutant that disables the
limb's *enforcement* (MC05, MC06, MC14) is killed twice (P9 and P4), and every mutant that
weakens the *generated inputs* is killed by P3. The residual is detector coverage, not a false
pass: the **executed** decoy set and the `hidden >= 1` guard are unobserved by any control
(RD-1/RD-2), and four rename/count transforms are pinned only by P3's literal count (RD-3). None
of this contradicts P1–P9 at the freeze bytes; all six items are routed to round 83.

## Evidence

`MutCounter-receipts/`: `summary-table.md` (the table above), `results.json` (per mutant:
selftest/driver/P3 rc, F6/F7/F8 r82 rc and the raw F6 r82 line, timings), `raw/<id>/`
(`selftest.txt`, `p3.txt`, `driver.txt`, `counter.sha256` for all 19 runs), `mutants.diff`,
`mutants.json` (anchors, `occ=1`, mutant sha256), `make_mutants.py`, `harness.py`,
`driver-patch.diff` (the single redirect of the r82 arm), `control-pristine.txt`,
`mc10-decoy-nameerror.txt`, `mc07-crash.txt`, `frozen-hashes-before.txt`,
`frozen-hashes-after.txt`.

Restoration: the mutants exist only in scratch; the frozen counter, candidate, table, builder and
forgery driver hash identically before and after (tables above, `frozen-hashes-*.txt`), scratch
deleted at exit. Sibling seats wrote other files in this tree during the wave (`LOG.md`,
`SCORECARD.md`, `corpus/lessons/round-82.md`, `l1/`); none of those writes are this seat's.
