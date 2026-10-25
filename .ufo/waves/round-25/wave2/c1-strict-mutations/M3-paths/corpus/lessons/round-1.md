# Round-1 lessons

Round: 1 (2026-09-28). Evidence: `LOG.md` round-1 entry, commit `5a0188f`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-1/kasegi.md`.

## What worked

- **Exemplar-first grounding.** Reading two complete packages end-to-end
  (`claims/cantina-pendle/ingestion-20260915/` positive-blocked,
  `claims/bugcrowd-seek/honest-zero/` terminal honest-zero) produced nearly all
  of SKILL.md's anatomy section — the live files teach more than
  `mission-template.md`'s prose because they show which contract fields
  actually get exercised (`resume_condition`, `claimability_blocker`,
  `not_granted` lists).
- **Verdict ledgers as triage data.** `docs/review-verdicts.jsonl` +
  `docs/continuation-notes.md` gave the decision table its real class weights
  (430/50/6; 438/19/26/3) instead of invented severity buckets.
- **`wrap-report.md` is the anti-patterns goldmine.** 0/7 clean GO — every
  fix was a disclosure defect. All 10 anti-patterns in SKILL.md trace to it.

## What failed / friction

- **`ls` + `find` sequencing.** The first probe guessed `/home/vgpnk/Projects/
  bounties` correctly but only by fallback `find`; capitalization differed
  from the prompt's `~/projects` convention. Cheap fix already in SKILL.md:
  cite absolute verified paths.
- **Claim slug naming is heterogeneous** — `ingestion-YYYYMMDD`, `honest-zero*`,
  vuln slugs; a skill reader must not assume one convention. Recorded as fact.
- **Tool boundary hit:** `head -N` inside `bash` calls got backgrounded by the
  harness mid-batch (jobs bg_7/bg_8/bg_9); results arrived fine, but batching
  reads via the `read` tool avoids the interjection entirely.

## Corpus additions this round

`corpus/knowledge/`: claim-package-contract, policy-access-playbook, ev-model,
terminal-classes, program-quirks — each cites its source path.

## Open gaps filed for next round

- `ops/claim-check.mjs` exact gate list (only error strings observed).
- Cantina fee-gate pattern may generalize — sample the other three
  `ingestion-20260915` Cantina packages.
- `vdp-disclosures/` and `vgn-bounty-lab/` directories unwalked.
