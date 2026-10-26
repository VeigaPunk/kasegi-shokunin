# Round 39 — claims erratum 1 (append-only; freeze text stands as written)

Author: L1 KasegiR39. Date: 2026-10-26. Supersedes the corresponding numbers in
`.ufo/waves/round-39/claims.json` (commit `dcd31701`) for measurement and closure
purposes; the frozen predicate sentences otherwise stand unchanged.

## E1 — registry after-count is 59, not 58 (C2)

`claims.json` C2 counts `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58`
reflected an arithmetic slip in the L1's freeze draft: the round appends FOUR rows —
S057 (mined) plus S056/S058/S059 (rejected) — so 55 → **59**. The kill-rule row
`registry != 58` reads as `registry != 59`. Every instrument that reads the registry
(census, audit, harness) counts the four rows; the spot-check list labels the
measured 59 versus the as-frozen 58 and cites this erratum.

## E2 — r38 judged-head hash corrected to the full 40-char form (C1)

The freeze text and the wave-1 prompts truncated the r38 judged head to
`66703aca50529a35be49aa8759d04140720ad` (37 chars, invalid object name). The real
r38 judged head J is `66703acaaff50529a35be49aa8759d04140720ad` (40 chars) per
`.ufo/waves/round-38/final-gates/all-gates.txt` `export-ref=` and the round-38
verifier spot-check. All `--export-ref 66703aca…` control runs (base-red proof for
C1, CritBaseControl do-nothing control) MUST use the 40-char hash; the suite's own
kill rule is unchanged (r38 judged-head export red).

## E3 — measured values recorded at erratum time

- Registry rows at base: 55 (S001–S055, unique).
- Intended after-state: 59 rows (S056–S059 added), frontier 22, knowledge 51.
- r38 judged head: `66703acaaff50529a35be49aa8759d04140720ad`.
