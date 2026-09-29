# Adjusted-EV model

Source: `~/Projects/bounties/ops/ev-report.mjs` (header + computation),
`bounty-map/schema.json` `ev_inputs` properties. Read 2026-09-28.
**Round-15 anchor base:** `~/Projects/bounties` is GONE
(`corpus/knowledge/source-tree-loss-2026-09-28.md`). Every `ev-report.mjs`
line number in this file was re-verified this round against the frozen
2026-09-05 mirror `~/Projects/the-bounty-hunter` HEAD `1cfbd86`
(`ops/ev-report.mjs`, 92 lines, sha256 `ba5485ed6a5d`) and resolves at 0
offset — anchor-compatible, not proven byte-identical. Live-census counts
(0/1088 and friends) are corpus-attested as-of 2026-09-28T23:32Z.

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
- `ev-report.mjs` exits 0 on a report; exit **2** both for a missing
  program-id argument AND a missing program file; an unparseable file →
  `WARNING` + all terms UNKNOWN + exit 0 — fail-closed on values, not on
  parse (round-13 correction: earlier text named only the file-missing 2).
- Verdict is strict: `positive_adjusted_ev: true` only when
  `adjusted_ev > 0` (ev-report.mjs:91); `false` at ≤0, `unknown` when any
  term is non-finite (round-13 addition).
- The basis column (`source_url`/`estimate`/`unknown`) is never exercised
  live: 0/1088 records carry any `sources[].basis`, so every live program
  prints basis `unknown` for all 10 inputs (round-13 census).
- `adjusted_ev` is derived-only, never persisted: schema `ev_inputs` has no
  such property (`additionalProperties:false` at `bounty-map/schema.json:34`,
  block `bounty-map/schema.json:32-52` — round-15 correction: the close is one
  line later than the `:32-51` this line previously cited) and 0/1088
  records carry the key; `fleet-dispatch.mjs:200` reads it for telemetry
  anyway — every `mission_dispatched` line logs `adjusted_ev:"unknown"` and
  the negative-EV `ev_note` branch (:204) is dead code (round-13
  three-way-verified derivation).
- Ranking-artifact defaults are a separate machine (`rank.mjs:55-58`
  DEFAULTS, never used by ev-report): p_in_scope .7, p_reproducible .7,
  p_unique .25, p_accepted .6, effort_hours 60, opportunity_rate 25,
  direct_cost 0, delay_cost 0, expected_risk_cost 250 → default p_success
  .0735 (round-13 addition).
- Cost fields beyond effort: `direct_cost` (e.g. Cantina $100 submission fee
  belongs here), `delay_cost`, `expected_risk_cost`, `duration_p90`,
  `submission_buffer`, `deadline`, `opportunity_rate`.

Usage: `node ops/ev-report.mjs <program-id>` prints every input with its basis
(source_url or estimate) + `as_of` timestamp.
