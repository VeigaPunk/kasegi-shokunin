# round-53 claims erratum 1 — two misderived after-literals in the frozen sentences (2026-11-01)

Filed BEFORE the round's final measurement receipts and SCORECARD row: two numeric literals inside
the frozen `expect_after` fields of `.ufo/waves/round-53/claims.json` (freeze commit `23448a2`) are
misderived and are superseded by this erratum. Both errors are arithmetic in the L1's derivation of
the after-state, not in the landed tree: each corrected figure is the figure the frozen sentence's
OWN cited control printed. Nothing else in the frozen claims changes; both claims verify on the
corrected readings, and the verdicts are unaffected.

## 1. C1 `expect_after`: the selftest completeness line reads total=15, not 14

Frozen: "plus 'selftest completeness lines=13 total=14 complete=False ok'".
Actual (receipt `controls/c1-after-selftest-r53.txt:16`, one run): `selftest completeness
lines=13 total=15 complete=False ok`. The derivation missed that the selftest's tmp knowledge dir
holds the separately pre-written `target.md` beside the 13 case fixtures and `missing-line.md`
(13 + 1 + 1 = 15), and `lines=13` because `target.md` carries no recheck line. The verdict the case
keys on — `complete=False`, red — is unchanged, and the C1 receipt printed it.

## 2. C2 `expect_after`: 33 inherited entry FAIL records, not 34

Frozen: "all 34 inherited entry FAIL records carry exactly problems=recheck-exit-1". Actual: **33**
— `entries=37 pass=4` leaves 33 FAIL entry records (37 − 4), and the do-nothing control the same
sentence cites had already printed the matching 33 (`controls/do-nothing-c2-r53.txt` footer:
"all 33 FAIL entry records carry problems=recheck-exit-1"; the final receipt
`controls/c2-counter-final-r53.txt` re-derives `FAIL_entry_records=33 not_recheck-exit-1=0`). The
frozen sentence therefore contradicted its own cited control in the exact R43 before-cell shape, on
the after side, and this erratum is filed before the round's results land on it. Both class counts
(33 = 33 across baseline and final, all `recheck-exit-1`; 30 = 30 row records, all
`missing-pass-line`) are unchanged, which is the substantive predicate.

## Also on record (kill-rule reading, not a supersession)

The C2 kill rule says "any FRONTIER-FAIL record on F34". The FIRST counter run over the DRAFT entry
(before this round's implementation commit) printed `FRONTIER-FAIL F34 ... problems=missing-pass-line`
twice over: the draft entry's Limits bullet "- S066 (the rejected row for this URL) ..." parsed as an
evidence-list source declaration (the counter's EVIDENCE_LINE limb), adding S066 to the declared set
the recheck line must cover. The bullet was reworded so no list item begins with an S-id; the
counter's verdict over the SHIPPED bytes — the state every receipt and the SCORECARD row measure —
is `FRONTIER-PASS F34 ids=S085` with no F34 FAIL record anywhere in its output
(`controls/c2-counter-final-r53.txt`, raw output captured in full at receipt time). The landing catch
is mined in `corpus/lessons/round-53.md` as the round's own worked example of the counter working as
designed; it is not a kill-rule firing on the landed state.

## What was NOT caught before the freeze, and why that is the mistake

R25 (pre-freeze satisfiability of literal constants against the declared after-adds) existed and was
not applied to these two derivation literals — the round dry-ran the state literals (rows/registry/
entries/expected counts, sha equality) but not the derived count-of-FAIL-records and the selftest
tmp-dir file count. The class and the fix are mined in the round-53 lesson's Mistakes.
