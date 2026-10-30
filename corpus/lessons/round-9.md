# Round-9 lessons

Round: 9 (2026-09-28). Evidence: `LOG.md` round-9 entry, commit `round-9`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-9/kasegi.md`.
L2 wave: 8 seats, one batched `task` call (reviewer/critic/connector/
sentinel/scout/revenger/executor/scribe) — all read-only.

## What I closed

- **Submitted-state / do-not-refile gap.** Merged the scattered set into
  `corpus/knowledge/submitted-registry.md`: 3 verified H1 filings (4002776 closed
  dup, 4002810 closed dup, 4002789 not_established), 3 archive-era filings
  (4028846 k8s, a169f309 launchdarkly, e4f41218-6036-… mattermost —
  owning mission claim-web1), 3 probable orphans (4028904/4028953 elastic,
  4ecbaf46-9548-… aiven), 1 VDP disclosure (DISCLOSED_FREE ledger row).
- **The receipts moved, not vanished.** `submission-review/` lives in the
  live sibling tree `~/Projects/origin-work/open-bug-bounties/
  claim-packages/` — receipts.csv (3 rows = the verified archive-era set),
  6 receipt JSONs, queue.json, CONTRADICTION.md. The 3 orphan receipts not
  in the CSV are exactly the probable set — matching claim-elastic's
  real-vs-orphan analysis.
- **Live hazard, proven by live run:** queued row 4
  (hackerone-anthropic/plugin-dev-…) = the identical finding already
  disclosed via VDP. `node ops/claim-check.mjs` on it → `OK`: the
  duplicate gate reads only `claims/*/*/status.json` fields
  `submitted_url`/`submission_performed`/`submission_state`; VDP,
  origin-work, and archive receipts are all outside.
- **Field-trap census (sentinel):** `submission_performed===true` occurs
  0× corpus-wide (vacuous checker leg); `no_submission_performed:false`
  on mozilla is a double-negative polarity trap; 19 distinct key-set
  signatures across producers (grok-4.6 b1k era → bare
  `no_submission_performed`; 2026-09-14/15 rewrap wave → fuller sets).
- **Hygiene:** 295 claim dirs / 280 status.json (PARKED 248, BLOCKED 16,
  DONE 15, SUBMITTED 2, OPERATOR_GATED 1); 15 status-less = 13
  ingestion-seeded stubs + stiltsoft partial + t-mobile BLOCKED.md-only.
  Root zips frozen ≤2026-09-15 09:45 — live tree has newer files absent
  from both. `claim-ready/*` ×3 tags peel to pre-submission `b3b1b7e3`;
  `claim-hold/*` ×9 exist alongside.

## Friction (real, repeated)

- **`edit` drift this round was severe**: five mid-range PUT/CUT ops
  duplicated rows, split paragraphs, and dropped content — caught only by
  re-reading the file after each op. Lesson: for a file under multi-seat
  correction, prefer whole-file `write` over chained surgical edits; the
  hashline anchor model punishes incremental patching of a moving target.
- My L1 draft asserted "alias marked only in receipt prose" — refuted by
  Probes + CiteAudit (alias `status.json` DOES carry `duplicate_of` +
  `submission_state:DUPLICATE_OF_SUBMITTED`; the prose mention lives in
  the *canonical* package's receipt). Two draft claims died on
  verification; that's the wave working as designed.

## Parked / open

- `fleets/registry.json` lane→model routing — still cross-domain.
- `george/` — still parked.
- Anthropic collision + origin-work blind spot reported upstream; fixes
  belong to the bounties repo owner (extend duplicate predicate to
  `vdp-disclosures/*/SUBMITTED.md` + archive-receipt index + origin-work
  corpus; compare commit+file+sha256+CWE, not title/slug alone).
- Critic seat yielded empty structured output; its transcript carried the
  real findings (origin-work discovery, CSV rows). Yield-shape failure —
  telemetry, not evidence loss.
