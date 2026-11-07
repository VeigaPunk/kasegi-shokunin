# MutC2Counter — mutation probe of the frozen C2 counter (.ufo/waves/round-85/c2/e2e-check.py)

Seat: MutC2Counter (mutation-tester, leaf). Round 85 attempt 1, wave w1.
Frozen bytes probed: `.ufo/waves/round-85/c2/e2e-check.py`
sha256 `a6f238022d0d263403b46221fa9ca959b91c8941157c3275eb0ae5ae76a6814d`
(equals `claims.json` instruments block). Freeze commit
`4a2d34f203519a87078f21a896dc8679137ff675`; base `bc722e54…`.

## Method and integrity

- 20 single-point mutants were generated from one copy of the frozen counter
  (`$S/base.py`, sha asserted) by unique-string replacement; each mutant differs
  in exactly one behaviour-bearing expression. Mutant sha256s are in
  `MutC2Counter-receipts/hashes.txt`.
- Detector 1 (the freeze's own): `controls/c2-controls-r85.sh` rebuilt verbatim as
  11 invocations (package-absent, exemplar-copy, positive pricing, 8 forgeries).
  The pristine counter reproduced `controls/c2-controls-r85.txt` exactly:
  **11/11 rc and limb-status matches**.
- Detector 2 (new, this probe): 16 probes — 1 positive anchor and 15 negative
  probes that put the counter in front of a package or report that satisfies a
  limb. 13 of them map one-to-one to the 13 survivors; the other 2 (`outside_lane`,
  `reward_currency`) cover guards outside my 20-mutant budget.
- Candidate package `w1/ExecC2Package-candidate/curl-h1-1913733` (9 files, as it
  stood at probe time; not edited by me) was also run against all 21 counters.
- Writes: scratch only (`/fast/scratch/hyaku/kasegi-r85/MutC2Counter/`, removed on
  exit) and the two paths named under "Files written". Frozen counter, gate,
  snapshots and candidate shas before/after: **unchanged**
  (`MutC2Counter-receipts/hashes.txt`; counter sha re-measured after the run).

## Result: 6 killed, 13 survived (each detected by a routed probe), 1 equivalent

"Killed" = at least one frozen control changes its limb verdict / rc against the
mutant, i.e. the pre-freeze suite is a live detector. "Survived" = the frozen
suite prints the identical signature for pristine and mutant; a new probe below
does flip it.

| # | mutant | single point | verdict | detector |
|---|--------|--------------|---------|----------|
| 1 | `sev_case_sensitive` | `if g.lower() != w` → `if g != w` (E3 severity) | **killed** | positive-pricing E3 pass→FAIL; forged-quote E3 pass→FAIL |
| 2 | `fields_drop_cve` | `cve` dropped from `FIELDS` | **killed** | forged-cve E3 FAIL→pass |
| 3 | `flag_always_true` | platform flag hardwired `"true"` | **killed** | positive-pricing E3 pass→FAIL; forged-platform-flag FAIL→pass; forged-quote pass→FAIL |
| 4 | `kev_reverse_prefix` | `if not w.startswith(g)` (kev predicate reversed) | **killed** | positive-pricing E3 pass→FAIL; forged-quote E3 pass→FAIL |
| 5 | `e4_ignore_missing` | E4 drops `not miss` | **killed** | forged-quote E4 FAIL→pass |
| 6 | `e4_pool_s119_only` | quote pool loses S120/S121 | **killed** | 8 controls flip; positive-pricing E4 pass→FAIL |
| 7 | `e1_rc_only` | E1 drops `"verdict=WELL-FORMED"` | survived | probe `gate_rc0_bad` |
| 8 | `e1_verdict_only` | E1 drops `p.returncode == 0` | survived | probe `gate_rc3_good` |
| 9 | `e2_drop_recorded_sha` | E2 drops the package-recorded digest | survived | probe `bogus_recorded_sha` |
| 10 | `e2_drop_manifest_binding` | E2 drops `h == rec[sid]` (round-85 manifest) | survived | probe `manifest_lie` |
| 11 | `e2_one_source` | E2 accepts `"S119" in found` | survived | probe `one_source` |
| 12 | `e2_symlink_evidence` | E2 follows symlinked evidence | survived | probe `symlink_evidence` |
| 13 | `sev_ignore_s120` | severity from S119 without the S120 agreement | survived | probe `s120_disagrees` |
| 14 | `reward_case_insensitive` | reward compared `.lower()` both sides | survived | probe `reward_case` |
| 15 | `e4_threshold_1` | E4 quote threshold `>= 3` → `>= 1` | survived | probe `two_quotes` |
| 16 | `e4_raw_no_norm` | E4 compares raw text (no whitespace collapse) | survived | probe `ws_quote` (pristine pass → mutant FAIL) |
| 17 | `e4_pool_includes_kev` | E4 pool gains the S052 KEV capture | survived | probe `kev_quote` |
| 18 | `e5_or` | E5 accepts `LOG or SHONEN` | survived | probe `log_only` |
| 19 | `allok_ignores_e1` | overall verdict ignores limb E1 | survived | probe `only_e1_fails` |
| 20 | `kev_dead_guard` | deletes `(w == "listed" and g.startswith("not-listed"))` | **equivalent** | none can exist (proof below) |

## Killed — what actually killed them

The frozen suite's only positive control is the pricing-only report; every
package control is a failure. So kills come from the pricing forgeries and from
positive-pricing's strictness:

- `sev_case_sensitive` and `flag_always_true` are caught twice over: the positive
  control demands `Medium`/`false`, and the matching forgery demands the opposite.
- `e4_ignore_missing` is caught by exactly one line (`forged-quote` E4) —
  `e4_pool_s119_only` by eight. Both quote-limb guards are covered, but only
  through the pricing path, never through a package.

## Survived — coverage findings and the routed control for each

None of the 13 flips a frozen control because the frozen suite never hands the
counter a package or report that *passes* E1/E2/E5 (and never a passing E3/E4
case other than the exact positive pricing). Each survivor is a real loosening:
it makes the counter accept a package the claim says it must reject. Routed
control names are the `PROBE` names printed by
`MutC2Counter-receipts/c2-probe-controls.py`; each prints the pristine verdict
shown and exits non-zero when the mutant is substituted.

| survivor | why the frozen suite is blind | routed control (pristine verdict) |
|---|---|---|
| `e1_rc_only` | no control has a gate that exits 0 while printing a non-WELL-FORMED verdict | `gate_rc0_bad`: stub gate prints `verdict=DEFECT exit=0` → E1 must FAIL |
| `e1_verdict_only` | no control has a gate that prints WELL-FORMED and exits non-zero | `gate_rc3_good`: stub prints `verdict=WELL-FORMED exit=3` → E1 must FAIL |
| `e2_drop_recorded_sha` | no package control reaches the E2 body with correct bytes | `bogus_recorded_sha`: real snapshot bytes, recorded sha256 `0…0` → E2 must FAIL |
| `e2_drop_manifest_binding` | frozen snapshots and manifest agree, so a hash-only check is indistinguishable | `manifest_lie`: scratch-lane manifest declares S119 sha256 `f…f`, package records the true sha → E2 must FAIL |
| `e2_one_source` | no package control carries even one snapshot | `one_source`: valid S119 artifact only → E2 must FAIL |
| `e2_symlink_evidence` | no package control uses a symlink | `symlink_evidence`: `evidence/S119.txt` → symlink to the lane snapshot → E2 must FAIL |
| `sev_ignore_s120` | S119 (`medium`) and S120 (`Severity: Medium`) agree in the frozen snapshots, so dropping the agreement is unobservable on frozen bytes | `s120_disagrees`: scratch lane with `Severity: High`, pricing says `medium` → E3 must FAIL |
| `reward_case_insensitive` | the positive value is already canonical (`2400 USD`) and the forgery differs numerically | `reward_case`: `2400 usd` → E3 must FAIL |
| `e4_threshold_1` | every frozen pricing control carries exactly 3 quotes | `two_quotes`: two valid quotes → E4 must FAIL |
| `e4_raw_no_norm` | all frozen quotes are single-space exact substrings | `ws_quote`: `Severity:  Medium` / `Bug bounty:  2400 USD` (double space) → E4 must **pass** (over-strict mutant turns it red) |
| `e4_pool_includes_kev` | no frozen quote is drawn from S052 | `kev_quote`: adds `> "vendorProject": "Arista",` (S052 only) → E4 must FAIL |
| `e5_or` | no frozen case names the package in only one of LOG.md/SHONEN.md | `log_only`: lane stub names it in LOG.md only → E5 must FAIL |
| `allok_ignores_e1` | no frozen case passes every limb but one (the exemplar also fails E2/E3/E4/E5) | `only_e1_fails`: gate stub exits 1, E2–E5 pass → `E2E-RESULT fail`/rc 1 |

Two more guards the 20-mutant budget did not mutate are also covered by the
suite, because they sit on the same success path:
`outside_lane` (a package outside the lane whose `../…` relpath is nonetheless
named in both LOG.md and SHONEN.md → E5 must FAIL) and `reward_currency`
(`2400 EUR` → E3 must FAIL, i.e. the reward comparison is verbatim including
currency).

## Equivalent mutant (not a coverage finding)

`kev_dead_guard` deletes the second conjunct of
`if not g.startswith(w) or (w == "listed" and g.startswith("not-listed")):`.
It is dead: when `w == "listed"`, `not g.startswith("listed")` is already true for
any `g` starting `not-listed`, so the second conjunct can never change the value
(truth table over 16 plausible `(g, w)` pairs: 0 differences). No control can
distinguish it. Routed as dead code for cleanup, **not** as a contract defect.
The full probe suite still reports `16/16 exit=0` against this mutant — the
positive evidence that the suite has no false-positive probe.

## The candidate package as a detector

Candidate as it stood at probe time: 9 files, evidence S119/S120/S121
byte-identical to the committed snapshots (sha256 match), package-recorded
digests match the round-85 manifest. Pristine signature:

```
LIMB E1 pass gate_rc=0
LIMB E2 pass bound=S119,S120
LIMB E3 pass section=True bad=none
LIMB E4 pass quotes=4 missing=0
LIMB E5 FAIL rel=.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733 log=False shonen=False
E2E-RESULT fail limbs=5 rc=1
```

It flips only 3 of the 20 mutants (`flag_always_true`, `kev_reverse_prefix`,
`e4_pool_s119_only`). That is expected and is the point: a *positive* package
catches over-strictness and wrong-pool mutants, but it cannot see any loosening —
pristine and loosening mutants both pass. Negative packages are required, and the
frozen controls have none that reach E2/E5 success paths.

## Routed defect (one, concrete)

**R85-C2-MUT-1 — the C2 pre-freeze control set does not test the success paths it
freezes.** `controls/c2-controls-r85.sh` contains no package that satisfies E1,
E2 or E5 and no report that varies the E3/E4 comparisons except through the
single canonical positive. Result: 13/20 single-point loosening mutants leave the
frozen suite's output byte-identical, including every guard that separates a real
package from a fabricated one (gate verdict/rc pair, recorded digest, manifest
binding, source set, symlinks, LOG/SHONEN conjunction, overall `all`).
Route: adopt `MutC2Counter-receipts/c2-probe-controls.py` as a pre-freeze control
(`controls/c2-probes-r85.py` after L1 integration), require `PROBE-RESULT
pass=16/16 exit=0` at freeze, and keep the mutant matrix (mutate-harness.py) as
the freeze-time evidence that each loosening goes red. No frozen byte is changed
by this routing; it adds a control, not a contract change.

Reproduce (lane reads only; writes under `$S`):

```bash
S=/fast/scratch/hyaku/kasegi-r85/MutC2Counter
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
# oracle suite on the frozen counter: 16/16, exit 0
python3 -B .ufo/waves/round-85/w1/MutC2Counter-receipts/c2-probe-controls.py \
  --lane . --counter .ufo/waves/round-85/c2/e2e-check.py --scratch "$S/probe-run"
# 20-mutant matrix + candidate run (regenerates $S/mut/*.py from the frozen bytes)
python3 -B .ufo/waves/round-85/w1/MutC2Counter-receipts/mutate-harness.py
# e.g. the E5 mutant: suite names the probe and exits 1
python3 -B .ufo/waves/round-85/w1/MutC2Counter-receipts/c2-probe-controls.py \
  --lane . --counter "$S/mut/e5_or.py" --scratch "$S/probe-e5_or"
```

Measured suite behaviour on substitution: `e1_rc_only`, `e2_one_source`, `e5_or`
each `15/16 exit=1` naming exactly their probe; `kev_dead_guard` `16/16 exit=0`
(equivalent). Transcripts in `MutC2Counter-receipts/probe-suite-mutant-*.txt`.

## Files written

- `.ufo/waves/round-85/w1/MutC2Counter.md` (this report)
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/c2-probe-controls.py`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/mutate-harness.py`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/mutation-results.json`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/probe-suite-frozen.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/probe-suite-mutant-e1_rc_only.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/probe-suite-mutant-e2_one_source.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/probe-suite-mutant-e5_or.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/probe-suite-mutant-kev_dead_guard.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/candidate-state.txt`
- `.ufo/waves/round-85/w1/MutC2Counter-receipts/hashes.txt`
