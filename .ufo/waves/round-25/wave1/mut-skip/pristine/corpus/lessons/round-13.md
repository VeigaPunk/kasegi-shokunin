# Round 13 lessons — the full-set audit round

1. **Late commits break protocol traceability.** Round 12 ended without a
   commit in either repo (kasegi HEAD was still round-11; the r12 report sat
   untracked in the main repo). Discovered only at r13 start via `git log`.
   A round ends when the push is verified, not when the work is done.
2. **Repair markers don't protect against regressions elsewhere.** r12 fixed
   `ufo-archive-2026.md:5` (19→20 missions) but left `:11` and `SKILL.md:385`
   at 19. When repairing a falsified fact, grep EVERY occurrence of the wrong
   value — the audit found one site, the fact lives in many.
3. **Unbounded negatives are the most fragile claim class.** "rank.mjs never
   ran post-refresh" was falsified at the margin: it ran ≥2× on 2026-09-04
   (2 RANKED ledger lines in its exact append shape; one artifact sha matches
   `rankings-2026-09-04.json`); what never happened is PERSISTENCE (held by
   state guard + S3). Date-bound negatives and name the mechanism verified.
4. **Universals die on census; record distributions.** "Every reroute cause
   is grok/xai" → 23/121 non-grok. "Targets are devin/swe-2:max" → 88/121.
   The distributions were the real content all along.
5. **Grep-tally claims must carry the pattern.** The same file yields 4/16/20
   hits for `submission_performed:true` under strict/`.ufo`-wide/separator-
   tolerant variants — and none yields the recorded 9. Event censuses need
   `"event"\s*:\s*` line-matching or they undercount `attempt_reset` by 92%
   (7065 compact vs 143 spaced lines in one JSONL).
6. **"Read-only" fleet tooling is not write-free.** `check-freshness.mjs:61`
   appends a telemetry line per run (the r12 AND r13 audits both mutated
   `ledger/telemetry.jsonl`); `claim-index.mjs:124` regenerates a doc.
   The sentinel's safety gate — prove zero writes from full source BEFORE
   executing — is the right protocol; run it for every live-run claim.
7. **Scripted artifacts outlive failed agents.** CitationsReviewer degraded
   into incoherent fabricated totals ("108 modules") and exited without
   yielding — but its `citations.json` (1100 tokens) + extraction script were
   on disk, letting L1 finish the audit deterministically (classify5.py).
   Design L2 tasks so raw artifacts land early; reject the narrative, keep
   the data.
8. **Measure the premise before planning the move.** SCORECARD's r13 plan
   called the finding-triage table "the thinnest re-verification margin";
   the density census ranks it #14/18. The real thin cohort (Program-rule
   checklist 28.6, anti-patterns 29.7) was invisible until measured.
9. **Three-way independent derivation works.** L1 full-source read ×
   executor draft × reviewer derivation agreed on the entire gate/threshold
   model with ZERO disagreement; every conflict was corpus-text vs source,
   never derivation vs derivation. Triple-derive the load-bearing models.
10. **Field-name precision survives rounds only by luck.** "`submitted_url`
    on queued rows is a route URL" was wrong at audit time r10 AND r12 —
    the field is null on all 12; routes live in `submission_url`/`claim_url`/
    payload. Verification that re-reads the same sentence, not the same
    field, re-verifies nothing.
11. **Dangling citations can be the fact.** The `.ufo/missions/…` refs are
    cited BECAUSE they dangle (invisible to every gate). An audit classifier
    must distinguish "broken citation" from "citation of brokenness" —
    context adjudication, not pure path resolution.
12. **Denominator transparency beats denominator stability.** The 18-item
    coverage proxy survived re-walk, but "3 root files" undercounts 26;
    recorded as a transparency note instead of silently redefining the proxy.
