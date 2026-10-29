VERDICT: BROKEN

# R46bMutSelfC1a — mutation-test of the extended C1 selftest draft against the 20 `C1_MUTANTS`

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only on the lane (verified:
`git status --porcelain -- corpus/` is empty; hashes in §1). All writes in my scratch
`/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/` (to be removed before this seat yields) and in
this Report file. No commits/pushes. No tools installed (stdlib only) — nothing to record under the
tooling directive.

## 1. Target bytes and the do-nothing control

* Selftest under test: `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/r46-counters-selftest-c1.py`
  sha256 `03079421b07639baabfc942ef4a022c9a8798ff8bc81f029d4b73c6a8b54e2fd` (764→843-line v1.4 draft;
  the committed sibling is `corpus/instruments/r46-counters-selftest-c1.py`, sha256
  `8b17164aadbd9c6925b5edd4111e3174936388e60e81e09465df0f00c04ec770`, 675 lines / 76 cases).
* Counter mutated: `corpus/instruments/r46-c1-gate.py`, sha256
  `95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7` — identical before and after
  every run (mutants are applied only to scratch copies, never to the lane).
* Mutant table: the frozen battery's own `C1_MUTANTS` (20 triples, `corpus/instruments/r46-mutbat.py`,
  sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`), imported — not
  re-typed — together with its own `apply_mutant`, so the "old-substring occurs exactly once" drift
  assertion is the committed one.
* Pure base: byte copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure2` (`diff -rq` → PURE-COPY-IDENTICAL).
  Hazard (recorded by the C2 sibling too): the selftest's built-in `PURE` default is
  `/fast/scratch/hyaku/kasegi-r46/L1/pure`, which does not exist; every invocation must pass
  `--pure .../L1/pure2` explicitly.
* Counter sanity read before grading (my `probe.py`, counter + tip built by the selftest's own
  `build_tip`): `gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64 … c1-gate fixed=7/7 exit=0`,
  `L2 read=base-gated=24 regrounded=2`. A counter that mis-reads here would invalidate every verdict.
* **Do-nothing control passed**: `driver.py` first runs the whole draft selftest against the
  PRISTINE counter and prints
  `BASELINE tree=/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/dtree failures=0`
  (83 cases). A dirty baseline would have made every mutant verdict inconclusive.

## 2. The decisive per-mutant evidence (7 runs I performed)

Command (one line per pair; the draft selftest is invoked with the battery's own mutant copy and
`--only <case>`, so the run executes exactly that case plus the 4 always-on tip/control/home
readings — the log shows `selftest cases=5`):

```
python3 /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/probe_cases.py \
  /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/dtree \
  /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/w-pc \
  /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/dtree/corpus/instruments/r46-counters-selftest-c1.py \
  M06-L3-home-dropped L3-home-path-in-trailing-comment \
  M07-L3-home-no-abs L3-absolute-home-path-in-trailing-comment \
  M13-L6-control-dropped L6-section-ids-not-unique \
  M14-L6-exit-ignored L6-section-ids-not-unique \
  M18-anchor-dirs-wide X-anchor-dir-outside-the-whitelist \
  M19-L2-eq-relaxed L2-newly-gated-entry-not-gated-at-base \
  M20-syntax-ignored L1-cd-target-is-not-valid-bash
```

Printed output (quote, `/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/probe-cases.log`):

```
MUTANT=M06-L3-home-dropped CASE=L3-home-path-in-trailing-comment
  case L3-home-path-in-trailing-comment             L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN
  SUMMARY: selftest cases=5 failures=1
MUTANT=M07-L3-home-no-abs CASE=L3-absolute-home-path-in-trailing-comment
  case L3-absolute-home-path-in-trailing-comment    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN
  SUMMARY: selftest cases=5 failures=1
MUTANT=M13-L6-control-dropped CASE=L6-section-ids-not-unique
  case L6-section-ids-not-unique                    L1=1 L2=1 L3=0 L4=0 L5=1 L6=1 L7=1 fixed=5/7 exit=1 targets=L6 verdict=UNEXPECTED
  SUMMARY: selftest cases=5 failures=1
MUTANT=M14-L6-exit-ignored CASE=L6-section-ids-not-unique
  case L6-section-ids-not-unique                    L1=1 L2=1 L3=0 L4=0 L5=1 L6=0 L7=1 fixed=4/7 exit=1 targets=L6 verdict=OK
  SUMMARY: selftest cases=5 failures=0
MUTANT=M18-anchor-dirs-wide CASE=X-anchor-dir-outside-the-whitelist
  case X-anchor-dir-outside-the-whitelist           L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1,L2,L7 verdict=FALSE-GREEN
  SUMMARY: selftest cases=5 failures=1
MUTANT=M19-L2-eq-relaxed CASE=L2-newly-gated-entry-not-gated-at-base
  case L2-newly-gated-entry-not-gated-at-base       L1=0 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=6/7 exit=1 targets=L2 verdict=UNEXPECTED
  SUMMARY: selftest cases=5 failures=1
MUTANT=M20-syntax-ignored CASE=L1-cd-target-is-not-valid-bash
  case L1-cd-target-is-not-valid-bash               L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1 verdict=FALSE-GREEN
  SUMMARY: selftest cases=5 failures=1
```

Reading: M06/M07/M18/M20 read **FALSE-GREEN** (the mutated counter ACCEPTS the tree the case
plants — the dedicated v1.3 case discriminates), M13/M19 read **UNEXPECTED** (the mutated limb
reads green where the case demands red), and **M14 reads verdict=OK / failures=0 — the mutant is
NOT caught**. So the six formerly-uncaught mutants M06, M07, M13, M18, M19, M20 are now closed by
the draft, and **M14-L6-exit-ignored remains at `mutant_failures=0`**: a survivor. Under the
battery's own grading that is `verdict=uncaught` unless an `--equivalent` map entry names a
committed proof — and **no such proof exists in the lane today** (there is no c1 `--equivalent` map
file anywhere in the repo; the only `equiv.py` in the wave is the C2 sibling's). Without it the
battery will print `mutbat counter=c1 mutants=20 caught=19 equivalent=0 uncaught=1 …`, and the
frozen after-sentence `caught+equivalent=20 uncaught=0` fails its own kill rule.

## 3. Is M14 a real hole or an equivalent mutant?

M14 (r46-c1-gate.py:337) drops `p.returncode == 0 or` from the L6 survivor test. My clause
argument: `p.returncode == 0` means entry_mode returned 0, i.e. every row read ok=1, i.e.
`red == []`, which already makes `red != [r[0]]` true; the two predicates therefore agree on every
input, so M14 is an EQUIVALENT mutant — which is why no selftest case can kill it. Empirical
support: the dedicated-case probe above reads `verdict=OK … selftest cases=5 failures=0` (re-run
standalone it prints the full summary plus `residual-false-greens=0 … none`), i.e. the M14 counter
and the pristine counter behave identically on the draft's newest L6 case; and two sibling seats
reach the same verdict independently (`R46bExecSelftestC1/m14_equiv.py`;
`R46bScoutEquivalence.draft/COMPARISON.txt`: `cmp orig-tip vs M14-tip -> IDENTICAL` and identical
on T14/T6/T19).

**Disclosure — my own differential probe is inconclusive and is NOT evidence.** `m14_diff.py`
compared the pristine and M14 counters over 84 trees, but it shares one `base` copy across four
concurrent workers (`if not os.path.isdir(base): shutil.copytree(pure, base)` races), so the
pristine side of many trees read `base=0` / `fixed=1|2/7` against the M14 side's `base=64` /
`fixed=6/7`. Those DIFF lines are my harness's artifact, not a counter divergence, and I retract
them; a rerun with a pre-copied base is the follow-up. The conclusion I stand behind is the §2
probe plus the clause argument, not the differential.

**Consequence for the claim (coverage finding, not a contract change):** the extended selftest
closes 6 of the 7 formerly-uncaught mutants; the 7th (M14) can only be closed by the battery's
`--equivalent` map with a committed proof file (`elif mid in eq and os.path.isfile(eq[mid])`,
r46-mutbat.py:159-160). If the L1 lands the draft without that map entry, `uncaught=0` is not
reachable and the C1 after-sentence fails as written.

## 4. Full 20-mutant battery — 8 of 20 rows completed before the window closed

`driver.py` (reuses the frozen battery's `C1_MUTANTS` + `apply_mutant` + `run_selftest`, so the
drift assertion and the selftest invocation are the committed ones) ran the complete selftest per
mutant against the draft:

```
python3 /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/driver.py …/dtree …/pure …/work-draft …/draft-results.json 8 4
```

It printed (quote — the run was stopped at M08 when the wave was asked to settle):

```
BASELINE tree=/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC1a/dtree failures=0
mutant=M01-L1-target-24 failures=27 bad_cases=0
mutant=M02-L1-broken-ignored failures=9 bad_cases=0
mutant=M03-L1-floor-dropped failures=1 bad_cases=0
mutant=M04-L2-one-reground failures=26 bad_cases=0
mutant=M05-L3-shape-loose failures=3 bad_cases=0
mutant=M06-L3-home-dropped failures=2 bad_cases=1
mutant=M07-L3-home-no-abs failures=1 bad_cases=1
mutant=M08-L4-bytes-dropped failures=1 bad_cases=0
```

All eight read `failures>=1` → **caught**, and the two rows my §2 probes also cover agree exactly
(M06: failures=2 = the FALSE-GREEN case + one more; M07: failures=1 = the FALSE-GREEN case alone) —
that is the cross-check between the full-suite detector and the `--only` detector. `bad_cases` is
truncated to the last 2 kB of each run's stdout (mutbat's `run_selftest` returns only that tail),
so it is not evidence about which case failed; `failures=` is the battery's own grading number.

**Rows NOT re-run by me: M09, M10, M11, M12, M15, M16, M17 (7 mutants).** For them the frozen
before-value receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` records
`mutant_failures=4, 2, 5, 3, 1, 2, 2` against the COMMITTED selftest, and the draft only ever ADDS
cases plus one marker conjunct (diffed: six new cases, a `--only` flag, a `marked = …` conjunct,
and `BASE_LINE_ALL` bookkeeping — no case removed), so a committed-caught mutant cannot read
uncaught under the draft. The residual risk the remaining sweep would close is a baseline-dirty
regression of the draft itself, and the draft's own baseline is clean (§1).

## 5. Limitations

* The full 20-row sweep did not finish in the window (host contention: ~30 sibling selftest
  processes, load 150-260 on 32 cores). My own re-runs cover the baseline, M01-M08 (full-suite
  numbers, all caught) and the 7 decisive mutants of §2 (M06/M07 appear in both); M09, M10, M11,
  M12, M15, M16, M17 were not re-run and rest on the frozen receipt plus the add-only diff, as
  stated in §4.
* M14's equivalence rests on the clause argument plus the §2 probe (identical readings on the
  draft's dedicated L6 case) and two sibling seats' independent probes; my own differential was
  inconclusive (harness race) and is retracted in §3, so I did not complete an exhaustive
  input-space proof.
* The draft selftest bytes were a moving target during the wave (v1.3 `d3578f28…` → v1.4
  `03079421…` at 19:37); every number above is against the v1.4 bytes named in §1. If the executor
  seat changes the file again, §2 and §4 must be re-run.
* My scratch dir was removed on exit, so the §4 battery log lives only in this report and the
  session record; the receipts were not copied out before the L1 asked the wave to settle.
* No package was installed or upgraded for this seat (stdlib only); nothing to record under the
  tooling directive.
