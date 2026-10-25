# ScribeScorecard — round 28 wave 1

Scope: append `## Round 28 — frozen claims C1/C2 (2026-10-25)` to `SCORECARD.md`; write nothing
else except this report and `.ufo/waves/round-28/receipts/ScribeScorecard.txt`. Lane base
`c9f8b115a098c65356e4b3b6048af45a37ab8395`; worktree HEAD `94f387cbeb71a532a51ce075f01701a557231e85`.
Measurements 2026-10-25T17:22Z–17:33Z. No VCS write, no subagent, no background job, no tool
install.

## Behavior

`SCORECARD.md` grew from 607 to 727 lines; no pre-existing line was edited. The appended section
(lines 609–727) carries: the claim provenance, a measurement-state paragraph (including the
instrument's in-place rewrite history and the one still-pending limb), the three-row table
(C1 / C2 / depth:density), the C1 corpus-disclosure correction, the resolved transient-gate
observation, an L1 close-out command block, the capabilities statement (no row added), and the
unchanged saturation paragraph.

## Measured result

| Claim | Before | After (measured) | Verdict |
|---|---|---|---|
| C1 | bad-fixture exit 0; bounties 0 lines; `--selftest` absent; SKILL exit 0 / bad 0 / LOST 306; instrument `c2a9e6c6…` | at landed digest `95333e29…` (523 lines): bad-fixture exit **1**; bounties **1** `BOUNTIES-ABSENT` line; `selftest cases=9 failures=0` exit **0**; SKILL exit 0 / bad 0 / LOST 306 / all fail classes 0 | counters met in the default environment; **kill-rule attack reproduced** (`pin-broken` non-isolating under an inherited `GIT_DIR`) — L1 adjudicates |
| C2 | frontier 11; entries 0; rows 41 census exit 0; harness 14/14 | frontier **12**; entries **1**; S042 row **1**; rows **42** census exit **0**; harness **15/15** exit **0**; `source-recheck` exit 0 on S041+S042, six quotes each `occurrences=1` | improved, score held 7 |
| depth:density | 9 | 9 | held; no credit claimed |

Instrument digest was checked before and after every counter run and never moved during a run; each
counter was run twice with identical results. A final re-verification at 17:33Z reproduced every
value at the same digests (`anchorcheck.py` `95333e29…`, `SKILL.md` `125be37d…`); the only open
item is the C1 receipt index.

## Findings

1. **The instrument was rewritten in place during measurement.** Nine digests were observed in
   ~8 minutes (`c2a9e6c6…` → `2f707046…` → `0a24a173…` → `7adfc847…` → `982d7207…` → `5f5f725c…` →
   `29aba084…` → `c3629229…` → `95333e29…`). Intermediate states were rejected as evidence: the
   early ones still exited 0 on the bad fixture and had no `--selftest`; one raised
   `NameError: name '_selftest' is not defined`; one matched the bounties cite but resolved it
   under the mirror prefix (`the-bounty-hunter/~/Projects/bounties/…`) as `BASE-ABSENT`. A digest
   stable within one run was *not* sufficient — it moved between the stability probe and the run
   once. The L1 must confirm the executor's report has landed and re-run at the final commit.
2. **C1's disclosure cell does not reproduce as frozen, and the correction is already filed.**
   The four named provenance lines are plain prose trailers, not backticked tokens, so
   `LOST-RECORDED` counts stay 0/0/0/15, not 1/1/1/16. `.ufo/waves/round-28/claims-erratum-1.md`
   (appended by the L1) states the corrected cell — zero backticked anchored bounties citations
   lane-wide, no verdict-class movement anywhere — and this seat's independent measurement agrees.
   A `/tmp` control shows the arm itself works for a properly backticked marked bounties cite.
3. **C1(c)'s receipt-index limb is still open.** `.ufo/waves/round-28/c1-receipt-index.txt` did not
   exist at 17:29Z, so the frozen counter's `selftest cases=` + `instrument_sha256=` pair is not
   produced. Owner: ExecReceiptCanonC1 / L1. Named in the scorecard and the receipt.
4. **Stale density comparand reconciled.** r24–r26's 154.0 / 19 blocks / 652 is the r22-byte
   figure; the same instrument measures 150.3 / 20 / 652 on the r26+ bytes because round 26 added
   the `Gates & probes registry` block (dens 80.0). After ScribeSkillGate's append the file reads
   160.2 / 20 / 656 at sha256 `125be37d…`, with no-harm intact (exit 0, bad 0, LOST 306). The row
   names both byte states and claims no density credit.
5. **Frozen counter command (d)'s `bad=` sed never fires** — the summary is `N bad; K distinct …`,
   so `s/^== .*bad; \([0-9]*\) bad.*/` prints nothing. The value is read from the same summary
   line instead. Recorded for the L1's counter hygiene; not repaired (no owned file).
6. **Capabilities: no row added.** Nothing beyond the frozen predicates was demonstrated; C1
   extends `anchorcheck.py` and C2 uses the already-recorded `source-capture`,
   `source-capture-pdf` and `frontier-recheck-harness` capabilities. The r22 stagnation window
   continues.
7. **C1 kill-rule attack reproduced (critic `CritC1Kill`).** With an inherited `GIT_DIR` pointing
   at a temp repo carrying a ref named `deadbeef` and a `pinned.md` blob, `--selftest` prints
   `selftest FAIL pin-broken: PIN-BROKEN: want 1, got 0; IN-RANGE: want 0, got 1; exit: want 1,
   got 0` and `selftest cases=9 failures=1` (exit 1); without the perturbation the same bytes give
   `9 failures=0` exit 0. The `pin-broken` fixture is therefore non-isolating under ambient git
   state — the killer clause of `claims.json` C1. The instrument's own verdicts are unaffected;
   the scorecard records the hit and leaves the score to the L1.
8. **C2 critic limit, confirmed textually, not a kill.** `CritC2Admission` finds the staged
   pre-publication user-notification step absent from the landed entry; this seat confirms the
   staged entry carries it (`→ 7 必要なら公表前の利用者通知 →`, line 20) and the landed entry has
   zero `利用者` occurrences. The frozen C2 predicate still measures met, so this is recorded as a
   completeness limit in the entry owner's file, not as an admission failure.

## Out of scope / not done

- No production file besides `SCORECARD.md` was written: no instrument, entry, registry, manifest,
  README, QUALITY, LOG, lesson or SKILL edit by this seat.
- No claim of a receipt-index pass, and no density gain claimed.
- Transient census exit 1 / harness `FileNotFoundError` observed at 17:24Z (entry absent) are
  recorded as landing-order artifacts and are superseded by the 17:29Z measured passes.

## Artifact paths (absolute under the lane repo)

- `SCORECARD.md:609-727` — appended section.
- `.ufo/waves/round-28/receipts/ScribeScorecard.txt` — receipt (counters verbatim, §8 mid-write log,
  §9 final measurements, close-out block).
- `.ufo/waves/round-28/wave1/ScribeScorecard.md` — this report.
- Cited peer evidence: `.ufo/waves/round-28/receipts/{ExecFixtureRun,ExecInstrSelftest,ExecNoHarmC1,ExecC2Counters,ExecCaptureS041,ExecCaptureS042,ExecManifest}.txt`;
  `.ufo/waves/round-28/wave1/ExecImplC1.diff`; `.ufo/waves/round-28/claims-erratum-1.md`;
  `.ufo/waves/round-28/c1-controls/*-before.txt`; `.ufo/waves/round-28/c2-controls/before.txt`;
  `.ufo/waves/round-28/census-before.txt`; `corpus/source-snapshots/round-28/manifest.json`.

## Checks the main agent / L1 should run at close

The block in `SCORECARD.md` § "L1 close-out block" and receipt § 6/§ 9. Required: C1 bad-fixture
exit 1, BOUNTIES-ABSENT 1, `selftest cases=N failures=0` at the final digest, the receipt-index
pair, SKILL exit 0 / bad 0 / LOST 306 / fail classes 0; C2 frontier 12, entries 1, S042 row 1,
census exit 0 with 42 rows, harness 15/15 exit 0, `source-recheck` exit 0; density re-measured at
whatever `SKILL.md` bytes close the round.
