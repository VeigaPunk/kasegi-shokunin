# Round 27 — kasegi

Lane: kasegi-shokunin. Round base `744a0d87e04445c3525c861194c0792e0d5ed39c` (round-26 verifier
spot-check commit; lane clean at round start). Two claims frozen in
`.ufo/waves/round-27/claims.json` before any dispatch: C1 depth:verifiability (anchorcheck.py
gate soundness: exit nonzero on unverifiable verdicts, `~/Projects/bounties/` CITE arm,
`--selftest`) and C2 coverage (F12 Japanese state-coordinated disclosure workflow, adopted from
the staged package entry `japanese-domestic-disclosure-workflow.md`, staged S042 → lane S042).
Before-measurements and do-nothing receipts were committed for both claims; then the operator
ended the run (orchestrator wrap-up, 2026-10-25): **no wave was dispatched, no production byte
changed, and both claims land NOT VERIFIED.** This lesson records the honest stop, the one
verified fix made before the freeze, and the carry-forward.

## Gate — the assimilation set

No source was opened this round; no SOURCES.md row was added, touched, or rejected. The
assimilation package (`/home/vgpnk/Projects/shokuknow/merge/kasegi`, read-only) was surveyed
only at the planning level: the staged entry `japanese-domestic-disclosure-workflow.md` and its
staged rows S042 (IPA process page, free in the lane registry) and S043 (= lane S041, registered
round 26) were read from the package bytes; the staged row `| S042 |` carries a prose-flavoured
`teaches` cell that the lane's census grammar would need re-checking before append. Planned
admits/rejects for the frozen C2 (≥1 admit: staged workflow entry re-grounded on round-27
captures; ≥1 reject: re-confirm the standing `chinese-criminal-thresholds` refusal and evaluate
`vendor-third-party-finding-coordination`, whose `ground: F20` names no lane frontier row) were
NOT executed. Status: adoption closed; re-opens under a fresh freeze in round 28.

## Mistakes

**M27-1 · a fixture designed against a stale premise (caught before freeze).** Class:
stale-premise. Evidence: the C1 bad-fixture was first drafted expecting a `MISSING-FILE`
verdict for a fabricated `corpus/knowledge/zz-r27-anchorcheck-missing.md:99` citation; run
against the pre-change instrument it reported `BASE-ABSENT (base tree absent: …/the-bounty-hunter/…)`
with exit 0 — on this host the mirror root has been ABSENT since 2026-10-12, so any unresolved
`'/'`-carrying citation falls through to the absent mirror base, and `MISSING-FILE` cannot fire
for it at all (`.ufo/waves/round-27/c1-controls/bad-fixture-before.txt`). Captured-by: none at
design time — the premise "a fabricated lane citation yields MISSING-FILE" was assumed, not
measured. Fix (shown able to fail): the fixture was RUN before the freeze and the frozen claim
was written against the observed verdict class (`BASE-ABSENT`, exit 0) instead of the assumed
one; the fix fails if the fixture ever prints `MISSING-FILE` for this citation on the landed
instrument — the round-28 wave-1 data-walk re-runs it first. House rule going forward: every
frozen counter's fixture is executed and its observed verdict text committed BEFORE the claims
file freezes (this round: `c1-controls/*-before.txt` committed with the freeze).

**M27-2 · round wrapped by the operator with zero waves dispatched.** Class: landing (external).
Evidence: orchestrator wrap-up message 2026-10-25 ("start no new waves… land NOW with what you
have"); no `task` swarm call was ever sent for round 27 (no `.ufo/waves/round-27/wave1/`
registry; the §3 L2 floor and the 32–64 wave band were never exercised). Captured-by: none —
operator directive, out of lane control. Fix: land the freeze + receipts + this lesson honestly;
record both claims NOT VERIFIED; re-declare under a fresh freeze next round (carry-forward
below); never claim verification for after-values no seat and no L1 run produced.

## Frozen claims — status at wrap-up (honest)

| Claim | Axis | Before (measured, committed) | After | Verdict |
|---|---|---|---|---|
| C1 | depth:verifiability (4) | bad-fixture exit 0 (BASE-ABSENT printed); bounties-fixture 0 BOUNTIES lines; `--selftest` absent (FileNotFoundError, exit 1); SKILL.md exit 0, bad=0 (`.ufo/waves/round-27/c1-controls/`) | not reached — instrument unchanged | **NOT VERIFIED** (no dispatch, no edit) |
| C2 | coverage (7) | frontier admitted 11; entries citing S042: 0; census exit 0 rows 41; harness `entries=14 pass=14 exit=0`; expected-list 41 lines (`.ufo/waves/round-27/c2-controls/before.txt`, `census-before.txt`) | not reached — no capture, no entry, no row | **NOT VERIFIED** (no dispatch, no edit) |

Do-nothing controls: the committed before-receipts ARE the do-nothing receipts — unchanged
bytes cannot reach any after value (e.g. pre-change instrument: fixture exit 0 and 0 BOUNTIES
lines; no adoption: frontier 11, entries 0, harness 14/14).

## Carry-forward for round 28

1. Re-freeze C1/C2 (new `claims.json`; fixtures and before-receipts already committed at
   `.ufo/waves/round-27/c1-controls/`, `c2-controls/` — re-run, do not re-create). Add the
   wave-band dispatch and the routed-defect items: reviewer seats inside the build wave
   (round-26 routed defect 2), inline ≤25-word Gate quotes (defect 3), single canonical receipt
   at the landed digest, no mid-wave receipt artifacts (defect 4).
2. C1 implementation notes for the executor seat: `FAIL_CLASSES = MISSING-FILE, PAST-EOF,
   OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT`; LOST-RECORDED stays recorded-not-fail;
   derive the bounties root like MIRROR/ORIGIN (`KASEGI_BOUNTIES` override + canonical
   `~/Projects/bounties`); selftest fixtures must isolate limbs under the absent-bases host
   (env-override a temp mirror root to reach MISSING-FILE; PAST-EOF needs a real temp file).
3. C2 implementation notes: source-recheck resolves capture paths only inside the manifest's
   own directory — a round-27 manifest cannot reference the round-26 S041 capture, so F12 needs
   a round-27 re-capture of the JPCERT PDF plus the new IPA page capture; header declares both
   S041 and S042; recheck `--source S041 --source S042 --manifest corpus/source-snapshots/round-27/manifest.json`.
4. `knowledge-expected.txt` stood at 41 lines at round start (`wc -l`); the r26 integration
   recorded 39 entries — reconcile the count basis when the F12 entry lands (recheck-audit
   `--expect` regeneration, not arithmetic).

## Compliance

Claims frozen before any dispatch (R25-1): `claims.json` commits with the freeze commit;
corrections would land as appended files — none were needed. Census at round start: exit 0,
41 rows, only the pre-existing W04 S028/S029 (`.ufo/waves/round-27/census-before.txt`); the
registry was not touched, so the round-end census gate is trivially unchanged (same bytes,
same exit) — re-run at round-28 close. No tool installed; no pacman transaction attempted
(host-wide pacman pause still in force).
