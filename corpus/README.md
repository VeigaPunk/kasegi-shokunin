# kasegi-shokunin corpus — index

Proprietary memory for the bounty & security research domain. Everything here
was read from `/home/vgpnk/Projects/bounties` on 2026-09-28; each entry names
its source. No generic filler.

## Coverage map

| Area | Entry | Source basis |
|---|---|---|
| Claim-package contract | `knowledge/claim-package-contract.md` | `fleets/mission-template.md` + live packages |
| Policy access per platform | `knowledge/policy-access-playbook.md` | `mission-template.md`, `docs/autopsies/`, `claims/bugcrowd-seek/` |
| Triage economics | `knowledge/ev-model.md` | `ops/ev-report.mjs`, `bounty-map/schema.json` |
| Mission outcome statistics | `knowledge/terminal-classes.md` | `docs/continuation-notes.md`, `docs/review-verdicts.jsonl`, `docs/wrap-report.md` |
| Program quirks | `knowledge/program-quirks.md` | `claims/cantina-pendle/…`, `docs/claim-ready-index.md`, `docs/claim-runbook.md` |
| Round-1 lessons | `lessons/round-1.md` | `LOG.md` round 1, commit `5a0188f`, report `.ufo/reports/round-1/kasegi.md` |

## Known gaps

- `ops/claim-check.mjs` gate list only known from error strings + runbook
  prose, not read line-by-line. Deep-dive if a round needs exact gate order.
- Cantina fee/precondition pattern observed on one package (Pendle); the other
  three `ingestion-20260915` Cantina packages not yet sampled for the same.
- `vdp-disclosures/` (one dir seen: `anthropic-plugin-dev-cmd-injection`) and
  `vgn-bounty-lab/` not yet walked — likely a distinct disclosure corpus.
- No entry yet on `fleets/registry.json` lane→model routing; fleet mechanics
  are arguably cross-domain, revisit if PROVINCE.md absorbs it.
