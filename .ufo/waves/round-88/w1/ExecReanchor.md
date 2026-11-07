# ExecReanchor — round 88 attempt 1

Wave: ONE v1 wave of 14 seats. Axes: depth:verifiability and coverage.

## Result

Generated an advisory candidate for all 54 excluded `anchor-content-drift` keys at base `6beead9148945fa695cf3139e8fc9d8e91cc5fd0`: **4 unique best, 8 ties, 42 none**. No corpus edits or frozen-claim re-scoring.

The search shifts each original range start by at most three lines in either direction, preserves its exact span length, and rejects out-of-entry ranges. Score is the sum of distinct identifier intersections across citing lines. Citing identifiers use the frozen meter's exact `idents()` definition; target identifiers use its `WORD` matcher over the entire cited range, as M8 does. Equal scores remain ties, without a proximity tie-break. `none` means no positive overlap anywhere in this bounded window, not no possible anchor elsewhere in the entry.

Of the 12 keys with positive overlap, 8 have at least one best range sharing an identifier with **every** citing line. The remaining 4 do not satisfy M8 across all citing lines. Each candidate records that distinction, every tied best range, per-line intersections, and every citing location with an excerpt capped at 120 characters. Long opaque spans are redacted before excerpts are retained. Ties have top-level `proposed: none` rather than an arbitrary chosen anchor; their actual alternatives remain in `best_candidates`.

## Retained evidence

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecReanchor-receipts/reanchor-candidate.json` — full key mapping; SHA256 `d1118362b9097dc9ad103258ecebe6165aed83459e169c4b1509cfac097ebc56`.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecReanchor-receipts/summary.json` — counts, method, and digests of the script, excluded map, frozen meter, candidate and base knowledge files.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecReanchor-receipts/reanchor.py` — generator; extracts only the frozen identifier definitions through AST, never copies the counter.

Executed once, exit 0:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && mkdir -p /fast/scratch/hyaku/kasegi-r88/ExecReanchor && trap 'rm -rf -- /fast/scratch/hyaku/kasegi-r88/ExecReanchor' EXIT; TMPDIR=/fast/scratch/hyaku/kasegi-r88/ExecReanchor python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecReanchor-receipts/reanchor.py
```

Observed output: `keys=54; unique=4; ties=8; none=42; keys_with_m8_passing_best_candidate=8`.

## Qualifications and handoff

Identifier overlap is a proxy, not semantic support. Round-89 intake should inspect tied ranges and partial-line failures before choosing any replacement; changing anchors is outside round-88's frozen M4 predicate. No build, lint, formatter, tests, full census, scanner, or landing gate was run. Parent owns the wave-file credential scan and any subsequent gates. Scratch was removed by EXIT trap. No tools installed. No LSP interface was mounted; this was a new advisory generator, with no existing symbols refactored. No blockers.

Self-evaluation (advisory, not claim judging): accuracy 4 (lexical support only); completeness 4 (bounded window deliberately leaves 42 unmatched); clarity 4 (ties require reading nested alternatives); actionability 4 (semantic selection remains parent's decision); conciseness 4 (per-citing-line evidence intentionally increases JSON size). Overall 4.0. Highest-value next step is semantic review of positive-overlap ranges, not broadening this frozen-wave candidate.

Files written: this report and the three receipt files named above. All writes are inside the assigned wave directory.
