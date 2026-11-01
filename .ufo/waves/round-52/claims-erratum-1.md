# round-52 claims erratum 1 — C1 selftest/audit figures vs the final instrument (2026-11-01)

Filed BEFORE the implementation commit; the freeze commit `29c4bd9dd0aa05a9276be6e3d6b35da7d9ecaa31`
pins the rev-1 instrument and its rev-1 receipts. While landing C1's receipts the instrument was
strengthened twice, each time because a receipt run exposed a real hole; the frozen C1 sentence's
selftest and audit figures are superseded as follows. Nothing else in the frozen claims changes; the
kill rule is unchanged and strictly stronger.

## What changed

1. **rev 2 — self-referential-span rule.** The rev-1 AFTER run flagged the round-51 Erratum's own text
   (`"(24 words by wc -w)"` quoting the stale figure) as an annotation and measured the annotation
   against itself (claimed=24 measured=5). A quoted span that contains the annotation match itself is a
   reference to an annotation, not a Gate locating a quote; such spans are now skipped and the nearest
   real quote wins. Found live, fixed, pinned as selftest case-h.
2. **rev 3 — erratum-acknowledgment check tightened.** The rev-2 acknowledgment ("rratum" + the bare
   measured figure anywhere in the file) wrongly acknowledged the PRE-erratum round-51 lesson, which
   discusses errata generally elsewhere — caught by the BEFORE-state re-derivation
   (`controls/quote-audit-before-recheck-r52.txt`, first run, exit 0 where exit 1 was expected). The
   rule now requires a SEPARATE occurrence of "<measured> words" within ±1000 chars of an erratum
   mention; a lesson that merely mentions erratum policy beside its own wrong annotation stays red.
   Pinned as selftest case-i.

## Superseded figures (frozen sentence → final state)

- "committed selftest (7 cases: …) prints selftest cases=7 failures=0" → **9 cases**
  (added case-h self-referential erratum, case-i erratum-mention-without-correction);
  final receipt `controls/quote-audit-selftest-r52.txt` prints `selftest cases=9 failures=0`, exit 0.
- "run over the committed lessons at the round tip it exits 0 with exactly one ERRATUM-ON-RECORD
  (round-51: 24 claimed, 17 measured)" → exit 0 with **two** ERRATUM-ON-RECORD rows — r51:39 (the
  original Gate figure) and r51:97 (the Erratum's own reference to it), both re-measuring the same
  quote at 17; final receipt `controls/quote-audit-after-r52.txt` prints
  `annotated=5 ok=5 erratum-on-record=2 failures=0`, exit 0.
- expect_after "the audit prints 4 annotated rows" → **5 annotated rows** (the fifth is the Erratum's
  annotation-shaped reference at r51:97).
- The BEFORE predicate is unchanged and re-derived with the final instrument:
  `controls/quote-audit-before-recheck-r52.txt` — pre-erratum lesson bytes (git show 29c4bd9) →
  r51:39 MISMATCH, erratum-on-record=0, LEDGER-ORPHAN on the unfiled row, exit 1.
  The rev-1 receipt `controls/quote-audit-before-r52.txt` (taken with rev 1 on the then-uncorrected
  tree, exit 1) is retained as history.

## Instrument pins

Rev-1 pin `75f0d5b1a42c8f96cb3c116c688b17efed6fd24721bdfe52a2a36cb02980bd82` superseded by the FINAL
instrument sha `396d720efa93fb38a1637f02f6b22da9eb2a0db03a0383e9ded78da7657b6896` (also recorded in
`freeze.txt` rev 1b). The C1 capability row enters the SCORECARD table pinned to the FINAL sha.

Erratum (round 53): the opening sentence claiming this erratum was filed before the implementation commit is superseded as to wording - it was authored before the implementation and COMMITTED WITH it (ride 227d3ede15e93191f737e4973e3274509bf4599f, the r52 implementation commit), a sequence freeze.txt rev 1b records transparently (instrument supersession, still pre-implementation); the supersession mechanism this erratum documents is unchanged, and the filed opening sentence stays byte-identical per R9.
