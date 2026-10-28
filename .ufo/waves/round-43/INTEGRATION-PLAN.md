# round-43 L1 integration plan (KasegiR43)

Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; claims freeze commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`;
freeze record `.ufo/waves/round-43/freeze.txt`; one v2 wave `kasegi-r43-hyaku`, 73 seats, attack share 23/73 = 31.5 %.

This file states targets only. It deliberately carries no `closed=` or `selftest cases=` literals: every such value in a
round-43 record must be bound to a committed transcript (K18), and a plan is not a measurement.

## Landing order (ConnCrossClaims may revise; couplings named)

1. Instruments first, read-only over the current tree: `corpus/instruments/r43-closure.sh` (K1-K19),
   `corpus/instruments/claim-package-check.py` + its companion `corpus/instruments/claim-package-selftest.py`,
   `corpus/instruments/fixtures/claim-package/` (exemplar + `defect-1..9-<class>`).
2. The fixtures/exemplar depend on the captured source: `corpus/source-snapshots/round-43/S067.txt` + manifest record
   (CVE-2025-9086 capture, 109 lines, sha256 7e35413a...; the earlier CVE-2023-38545 capture was superseded by the seat).
3. The exemplar's prose depends on the capture; the `report.md` scope excerpt must quote captured bytes.
4. Corrections (append-only) change K14-K16's inputs; land them AFTER the limbs exist so each correction can name the
   token its limb greps for, and land the SCORECARD/LOG/lesson corrections in one commit so the K11 ledger stays coherent.
5. Declarations (`declared-blocks.txt`) must name every path any check reads AND every new corpus/instrument path —
   regenerate after every landing, then run K4.
6. `claims-erratum-1.md` (round 43) and `.ufo/waves/round-42/claims-erratum-5.md` (RD42-8) land before K17 is expected green.
7. `final-gates/r42-at-de09313.txt` (RD42-5) lands before K18 is expected green; it binds `closed=10/13` and the selftest
   tally the round-42 verifier quotes.
8. Only then: judged head J (every round-43 change except the receipt), then the receipt run at J -> Y.

## Two-way couplings to watch

- A new `Correction (round 43)` line raises the K11 correction ledger count AND supplies K14's supersede marker for the
  SCORECARD stale-literal cell — both measured in the same run.
- Adding `corpus/knowledge/claim-package-gate.md` changes `recheck-audit` expected (61 -> 62, `knowledge-expected.txt`
  must be appended) and K4's declarations.
- Adding `corpus/instruments/fixtures/claim-package/**` changes the lane's tracked footprint; `density.py` must stay
  byte-identical (K12 no-harm guard).
- The new registry rows change the census row count and the search log; capture-binding must move 56 -> 57, not 58.
- The gate's identity digest is cited by the fixtures' receipts: land the gate at its delivered bytes and ship the
  selftest as the companion file, never by pasting it into the gate.

## Verification (after all seats settle, one pass)

- the r43 suite over J: all nineteen checks closed, exit 0
- the suite's graded selftest over J: nineteen graded cases, no failures
- base and r41-head negative controls red; plain run exit 2; ref-not-found distinct
- `python3 corpus/instruments/claim-package-check.py --selftest`: ten graded cases, no failures
- the ten C2 counters per `claims.json`
- `git status --porcelain` empty (quiescence), scratch root removed
- misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain`

## Mined mistake so far (mine, this round)

M43-1 class `stale-premise`: the first C1 predicate draft declared the base export would print the "thirteen of nineteen"
figure with K1-K13 closed, but the do-nothing control (`c1-controls/do-nothing.txt`) measured the r42 stand-in at
`closed=12/13 exit=1` because the base carries commits after the r42 receipt and J8's receipt binding is red there.
Caught by R22/R25 (pre-freeze satisfiability) via the control receipt, before dispatch; fixed by freezing "at base every
one of K14-K19 is open and the run is short of nineteen closed", leaving the exact base figure to the measured report.
Able to fail: the control output contradicted the draft; had the draft been committed, the round would have frozen an
unsatisfiable base limb.
