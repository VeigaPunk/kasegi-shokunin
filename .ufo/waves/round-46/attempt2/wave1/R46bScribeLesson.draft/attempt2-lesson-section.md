# Round 46 (attempt 2) — lesson section DRAFT (append-only skeleton)

Target of the append: `corpus/lessons/round-46.md` (append a new `## Attempt 2 (2026-10-29, L1 KasegiR46)`
section at the end of the file; the attempt-1 section above it is NOT edited — R6-style append-only).
This file is a DRAFT produced by seat `R46bScribeLesson`; the L1 owns the committed bytes.

---

## Attempt 2 (2026-10-29, L1 KasegiR46)

Attempt 2 re-dispatches round 46 after the attempt-1 honest-stop (operator wrap-up, run 11). Attempt 1's
claims (`.ufo/waves/round-46/claims.json`, frozen `9f23aab`) landed their work but were never adjudicated;
attempt 2 declares NEW claims against the post-attempt-1 tree.

Round-open base: `04af9bc92229232ea5cce8b32bfe59dd969eb26d`. Attempt-2 freeze commit:
`fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`. Frozen claims: `.ufo/waves/round-46/attempt2/claims.json`
(sha256 `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`, per
`.ufo/waves/round-46/attempt2/freeze.txt`). Neither the counters nor the claims file is edited by any seat:
amendments happen only at L1 integration as logged errata.

### Claims (one line each)

- **C1 — depth:verifiability (measured).** Every mutant of the frozen mutation battery
  (`corpus/instruments/r46-mutbat.py` v1, 20 c1 mutants and 21 c2 mutants) is graded by the committed
  selftests: the battery prints `mutbat counter=c1 mutants=20 caught=<k1> equivalent=<e1> uncaught=0
  baseline_failures=0` and `mutbat counter=c2 mutants=21 caught=<k2> equivalent=<e2> uncaught=0
  baseline_failures=0` at the final lane revision, and every `equivalent` verdict names a written proof file.
  Before-value (frozen receipt `controls/mutbat-before.txt`, sha256
  `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`, `BATEXIT=1`): `c1 … caught=13
  equivalent=0 uncaught=7 baseline_failures=0` and `c2 … caught=8 equivalent=0 uncaught=13
  baseline_failures=0`. The round's work is the selftests and the battery; the two counters' limb
  semantics are untouched.
- **C2 — coverage (measured).** Frontier **F29 = GitHub repository security advisories** (the
  maintainer-side advisory lifecycle: draft advisory, temporary private fork, credit, CVE request through
  GitHub as a CNA, publication, fix-version duty) is admitted with one new tier-A mined source row
  **S074** (sha-pinned 42-line capture, 9 located manifest quotes) and one new knowledge entry
  (`corpus/knowledge/github-repository-security-advisories.md`): 29 admitted frontier rows, 66 knowledge
  entries, ≥74 SOURCES rows; the reporter-side flow stays F28.

### Frozen-counter lineage

| instrument | attempt-1 state | attempt-2 state | evidence |
|---|---|---|---|
| `corpus/instruments/r46-c1-gate.py` | v1.2 (errata E1/E2) | **UNCHANGED this round** | sha256 `95f2eb7933841d6c…` identical at base `04af9bc9` and at freeze `fe0f56b7` |
| `corpus/instruments/r46-c2-gate.py` | v1.2 (errata E1/E2) | **UNCHANGED by this wave so far** (v1.2 at the freeze; the attempt-2 errata logs a **conditional** v1.3 ledger-exemption amendment, E3, that lands only if the wave's own verification succeeds) | sha256 `647bd5b7b6268551…` identical at base and freeze; attempt-2 errata §E3 |
| `corpus/instruments/r46-counters-selftest-c1.py` | v1.1 harness, `cases=76 failures=0` | **extended by this round** (the round's C1 surface) | sha256 `8b17164aadbd9c69…` identical at base and freeze; the extension lands at integration |
| `corpus/instruments/r46-counters-selftest-c2.py` | v1.1 harness, `cases=137 failures=0` | **extended by this round** (the round's C1 surface) | sha256 `ff7104cfc8910071…` identical at base and freeze; the extension lands at integration |
| `corpus/instruments/r46-mutbat.py` | did not exist at base | **new at the attempt-2 freeze** (the battery, v1) and logged for a **v1 → v1.1 extension** at integration (attempt-2 errata E1-a/E1-b: the `F29_MUTANTS` table and `--counter f29`; the c1/c2 predicate is untouched, so every v1 reading stays reproducible) | base blob `e3b0c442…` (absent) → freeze `f7a7cdfa187ef6f2…`, matching `freeze.txt: mutbat-sha256-v1` |
| `corpus/instruments/r46-f29-gate.py` | did not exist at base | **new at the attempt-2 freeze** (the C2 counter, v1) | base blob `e3b0c442…` (absent) → freeze `a1091e246a51c1c1…`, matching `freeze.txt: f29-gate-sha256-v1` |

Lineage statement for the committed lesson: the two round-46 counters are **v1.2 at the attempt-2 freeze
and are not edited by this wave's seats**; the attempt-1 hardening (v1 → v1.1 → v1.2) is recorded in
`.ufo/waves/round-46/counter-errata.md` (decision E1/E2) and is not re-opened here; this round extends
the **selftests** that grade the counters and adds the **battery** that measures their mutation coverage.
The attempt-2 errata file is **`.ufo/waves/round-46/attempt2/counter-errata.md`** (frozen at
`fe0f56b7`, same claims sha256 `ca73279f…`); it classifies the round's changes as an erratum, not a
changed rule, and logs three items: **E1** the battery `v1 → v1.1` extension (the `F29_MUTANTS` table and
`--counter f29`; the c1/c2 predicate is untouched, so the before-value stays reproducible under v1
bytes), **E2** the two selftest extensions (baselines stay `failures=0`; each new dedicated case must
fail under its targeted mutant), and **E3 — CONDITIONAL** a `r46-c2-gate.py` `v1.2 → v1.3` ledger
exemption that lands **only if the wave's own verification succeeds**, otherwise E3 is struck and the
`considerthese` ledger append is deferred again with the reason. If E3 lands, this lesson's lineage
table must record the counter as v1.3 at the landing commit with the erratum pointer — a counter byte
change is only admissible as a logged erratum with a plain re-derivation that does not use the changed
instrument; the counters' limb sentences are frozen for the whole wave.

### Frozen readings (before-values, re-derived at the freeze)

- `controls/mutbat-before.txt` — `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7
  baseline_failures=0`; `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13
  baseline_failures=0`; `BATEXIT=1`.
- `controls/selftest-baselines.txt` — `selftest cases=76 failures=0` (`c1-exit=0`); `selftest cases=137
  failures=0` (`c2-exit=0`); one disclosed mechanical limit, `residual-false-greens=1`
  (`R-claim-text-unrelated-to-anchor`), not counted as a failure.
- `controls/f29-gate-at-base.txt` — `f29-gate fixed=1/7 exit=1` at the base export `04af9bc9`
  (`gate H7 pass=1 read=census-rc=0 ok-line=1`; H1-H6 red).
- `controls/f29-r50-receipt.txt` — the R50 pre-freeze mutant pass over the f29 gate: 21 mutants
  (3 per limb H1-H7), 11 defect-tree flips shown, 10 NOT-SHOWN and disclosed.
- `controls/sources-census-before.txt` — `W04 S028`, `W04 S029`, `W04 S072`, `kasegi ok`, exit 0.

### Mistakes

Round-45 spot-check dispositions (`corpus/lessons/round-45-verifier-spotcheck.md` §6) were answered in
attempt 1 as M46-2 (not reproduced) and M46-3 (scope overclaims); M46-1 (the v1 counters' cheap controls)
was answered in attempt 1 and is **carried, not re-mined**: the attempt-1 hardening (v1 → v1.2) is the
closure of M46-1 and the two counters are unchanged this round. The mined mistakes below are the ones
attempt 2 can already evidence from its own frozen receipts.

| ID | Class | Error | Evidence pointer | Captured by | Fix | Evidence the fix can fail |
|---|---|---|---|---|---|---|
| M46-4 | unmeasured-verification | The round-46 selftests were shipped on a **case-count baseline** (`cases=76 failures=0`, `cases=137 failures=0`): that number counts the harness's own cases, not the coverage of the counters' clauses. The frozen battery then showed **7 of 20 c1 mutants and 13 of 21 c2 mutants uncaught** — clauses M06/M07/M13/M14/M18/M19/M20 (c1) and G1c/G2a/G2b/G2c/G3a/G4b/G5c/G6a/G6b/G6c/G7a/G7b/G7c (c2) were exercised by no failing case, so `failures=0` was compatible with a counter that reads green on a defective tree. | `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` — per-mutant lines `verdict=uncaught` for `M06-L3-home-dropped`, `M07-L3-home-no-abs`, `M13-L6-control-dropped`, `M14-L6-exit-ignored`, `M18-anchor-dirs-wide`, `M19-L2-eq-relaxed`, `M20-syntax-ignored` and the 13 `G*` mutants; summaries `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`, `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`, `BATEXIT=1` (red-before receipt; sha256 `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`) | QUALITY R50 (the pre-freeze mutant pass that produced `controls/f29-r50-receipt.txt` applied the same discipline to the two attempt-1 counters and exposed the gap before the freeze) | Extend the committed selftests so that every mutant of the frozen battery is graded: each new dedicated case must FAIL under its targeted mutant, and a mutant with neither a failing case nor a committed proof stays red. An uncaught mutant may be discharged only by an `--equivalent` entry naming a written proof file (no silent exemption). The battery must print `uncaught=0` and `baseline_failures=0` for both counters. | The battery summary itself (`uncaught>0` or `baseline_failures != 0` ⇒ C1 red) and the per-mutant receipt (a dedicated case whose own mutant yields `mutant_failures=0` proves nothing and must be rejected at review). | 
| M46-5 | shadowed-clause | 10 of the 21 f29-gate mutants are **NOT-SHOWN at gate level**: H1a/H1b (counts / one-live-row) are shadowed by the later `dup` and `entry-shared` clauses; H2b (per-section word floor) is shadowed by the section's own ≥6-row table; H3a (11-cell → ≥9) is closed by construction (a 9-cell row fails the positional literals); H4b/H4c (quote-count and distinctness floors) are shadowed by the manifest byte-pin H4a; H5c (≥4 located spans) is shadowed by `failed == 0` plus the H2 table-rows conjunct; H7a/H7c grade the census **output shape**, and the census script lives at the fleet root, outside this lane, so no lane-side defect tree isolates them. | `.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt` — the defect-tree pairing table (21 mutants, `defect-flips shown=11`, `not-shown=10`) and the `## Disclosures` paragraphs (a)-(f) | QUALITY R50 | The wave-1 selftest `corpus/instruments/r46-selftest-f29.py` grades clauses (a), (b), (d), (e) on synthetic trees (it rebuilds `PINS` for its trees); the battery extension `r46-mutbat.py --counter f29` reaches `uncaught=0` for the f29 gate with the same caught-or-equivalent predicate as C1's counters; H7a/H7c stay disclosed as census-dependent. | The battery's f29 summary (`uncaught>0` ⇒ red) and, per mutant, a dedicated case that fails under its own mutant; a selftest case that passes under its own mutant proves nothing. |

L1 integration note: M46-4 and M46-5 are written from the frozen receipts; the *fix* columns describe
work that lands in the wave's own commits, so the closing evidence for both rows is the wave's final
battery receipt, not this draft.

<!-- END OF (a) DRAFT -->
