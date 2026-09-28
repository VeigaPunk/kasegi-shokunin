# Adjusted-EV model

Source: `~/Projects/bounties/ops/ev-report.mjs` (header + computation),
`bounty-map/schema.json` `ev_inputs` properties. Read 2026-09-28.

```
p_success    = p_in_scope × p_reproducible × p_unique × p_accepted
gross_value  = p_success × expected_reward
total_cost   = effort_hours × opportunity_rate
               + direct_cost + delay_cost + expected_risk_cost
adjusted_ev  = gross_value − total_cost
```

Facts:
- Inputs live in `bounty-map/programs/<id>.json` → `ev_inputs`; schema pins
  `p_*` to [0,1], `as_of` datetime, free-form `sources` for provenance.
- Missing inputs print `UNKNOWN` for the affected term, never 0/1; verdict
  degrades to `unknown` — fail-closed reporting.
- `ev-report.mjs` exits 0 always (reporting tool), 2 when the program file is
  absent.
- Cost fields beyond effort: `direct_cost` (e.g. Cantina $100 submission fee
  belongs here), `delay_cost`, `expected_risk_cost`, `duration_p90`,
  `submission_buffer`, `deadline`, `opportunity_rate`.

Usage: `node ops/ev-report.mjs <program-id>` prints every input with its basis
(source_url or estimate) + `as_of` timestamp.
