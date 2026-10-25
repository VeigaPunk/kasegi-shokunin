# Round-1 aggregator corpus audit — kasegi

Auditor: aggregator L1 (m_qwen) + one independent L2 `reviewer` lane
(m_composer, per `.ufo/prompts/aggregator-L1.md` routing map), 2026-09-28.
Method: re-executed the cited commands against
`/home/vgpnk/Projects/bounties` rather than trusting the entries.
Scope: `corpus/` only; `SKILL.md`/`LOG.md` are lane-owned and were **not**
edited — corrections are filed here as new entries, per the append-only
discipline `PROTOCOL.md` gives `LOG.md`.

Round evidence: `LOG.md` round-1 entry; commits `5a0188f` (skill+log) and
`49f5945` (corpus); lane report
`~/projects/shokunin/.ufo/reports/round-1/kasegi.md`.

## Verdict: conformant — pass with concerns

`corpus/README.md` + `knowledge/` (6 entries) + `lessons/round-1.md` present;
every README index row resolves to a real file; every knowledge entry carries a
`Source:` block; the lesson cites round, commit, LOG and report. No dangling
refs. No generic bounty-hunting filler: entries are host-specific (schema ids,
gate names, dollar amounts, verdict counts).

## Independently re-verified (12+ citations)

| Claim | Command | Observed |
|---|---|---|
| 1088 program records | `find bounty-map/programs -name '*.json' \| wc -l` | 1088 ✓ |
| verdict ledger 486 rows; 430 leave / 50 continue / 6 drop | `wc -l docs/review-verdicts.jsonl` + count by `verdict` | 486; 430/50/6 ✓ |
| continuation partition | `grep` class table in `docs/continuation-notes.md` | 438+19+26+3 = 486 ✓ |
| wrap-report verdicts | `grep '^- \*\*GO' docs/wrap-report.md` | 0 GO / 5 GO-WITH-FIX-NEEDED / 2 NO-GO ✓ |
| operator queue length | `grep -E '^\| [0-9]+ \|' docs/claim-ready-index.md \| wc -l` | 12 ✓ |
| EV formula + fail-closed | header of `ops/ev-report.mjs`; `node ops/ev-report.mjs __missing__` | formula matches; exit 2 + "program file missing" ✓ |
| schema fail-closed | `bounty-map/schema.json` | `additionalProperties:false`; required id/name/source_kind/official_url/freshness/lane/mission_state; `p_in_scope` min 0 max 1 ✓ |
| manifest schema id | `claims/cantina-pendle/ingestion-20260915/evidence/manifest.json` | `"evidence-manifest/v1"` ✓ |
| hard gates | `jq .claim_review.hard_gates claims/bugcrowd-seek/honest-zero/status.json` | written_scope, authorization, evidence_integrity, no_duplicate_or_prior_submission ✓ |
| honest-zero semantics | `claims/bugcrowd-seek/honest-zero/evidence/scope-snapshot.json` | `stop_reason` set; `in_scope_assets: []` ✓ |
| Cantina fee gate | `grep '\$100' claims/cantina-pendle/ingestion-20260915/claim_checklist.md` | $100 submission deposit ✓ |
| provenance pin | `claims/cantina-pendle/ingestion-20260915/provenance.json` | commit `f24265966bb53f75d834ad705decde8e479d3a33`; `policy_sha256` prefix `e92d529aa18f842e` ✓ |
| "~88% closed / default leave" | 430/486 | 88.5% ✓ (derived, falsifiable) |

## Defects filed (corrections, not rewrites)

1. **Package count is unreproducible as written.** `LOG.md`, `SKILL.md` and the
   lane report all say "275 claim packages under `claims/`". Observed 2026-09-28:
   `find claims -mindepth 1 -maxdepth 1 -type d | wc -l` = **274** program dirs;
   `find claims -mindepth 2 -maxdepth 2 -type d | wc -l` = **295** package dirs;
   `find claims -mindepth 3 -maxdepth 3 -name status.json | wc -l` = **281**.
   No counting rule yields 275. Fix direction: state the count *with* its
   command, or drop the number.
2. **Exemplar over-attribution.** `knowledge/claim-package-contract.md` and
   `SKILL.md` present `claims/cantina-pendle/ingestion-20260915/` as the
   `claim_review`/hard-gate exemplar; `grep claim_review` on that package's
   `status.json` returns nothing. The gate structure was verified on
   `claims/bugcrowd-seek/honest-zero/status.json` instead. Both packages are
   real; only the attribution is wrong.
3. **Autopsy count off by one.** Report says `docs/autopsies/` "(30 files)";
   `ls docs/autopsies/*.md | wc -l` = **31**.

## Gaps for the next round

- `ops/claim-check.mjs` gate **order** — currently known only from error strings
  and runbook prose; one line-by-line read closes it (the lane's own README
  already files this).
- Cantina sibling packages `claims/cantina-{dydx,morpho,immunefi-beanstalk}/
  ingestion-20260915/` unsampled for the same $100 fee/balance precondition —
  the "generalizes across Cantina" hypothesis in the lane report is untested.
- `vdp-disclosures/` and `vgn-bounty-lab/` unwalked (distinct disclosure
  corpus).
- `fleets/registry.json` lane→model routing: **cross-domain**, belongs to
  kumitate (orchestration & tooling). Reported, not absorbed, per `PROTOCOL.md`
  contested-scope invariant.
