# AttackA3 — Receipt index digest binding (C1 milestone)

Seat: L1Kasegi26.AttackA3 (leaf, read-only)
Date: 2026-10-25 UTC
Scope: verify receipt-index digest binding; report three values; confirm c1-live.json instrument hash.

## Values verified

| Source | Value |
|---|---|
| `.ufo/waves/round-26/c1-receipt-index.txt:2` `instrument_sha256=` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` |
| `.ufo/waves/round-26/c1-instrument-digest.txt:1` `instrument=` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` |
| `sha256sum corpus/instruments/recheck-audit.py` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` |
| `.ufo/waves/round-26/c1-live.json` `"instrument_sha256"` | `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` |

All four match the landed instrument `3fc0d751…` exactly (full 64-hex equality).

## Base control (pre-change)

- `.ufo/waves/round-26/c1-receipt-index.txt:3` `base_sha256_control=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`
- `.ufo/waves/round-26/c1-instrument-digest.txt:2` `base=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`
- Cross-check against round-25 pin: `.ufo/waves/round-25/c1-instrument-digest.txt:1` records `instrument=c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`; `.ufo/waves/round-25/c1-receipt-index.txt:1` matches. Therefore `base_sha256_control` == round-25 pinned digest `c3c19adc…` (= the pre-change control). ✓

## Assertions

1. Receipt index, instrument-digest file, and live `sha256sum` of `corpus/instruments/recheck-audit.py` are identical: `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` — matches landed instrument `3fc0d751…`.
2. `base_sha256_control` (both round-26 files) equals round-25 pinned digest `c3c19adc…` — verified against actual round-25 artifacts, not just comments.
3. `c1-live.json` `instrument_sha256` equals the same landed instrument digest.

Verdict: **C1 receipt-digest equality HOLDS.** No defect found in scope.

## Notes

- Round-26 index crossreference note (R25-2) is consistent with the actual round-25 receipt index (its line 4 is `executes=12 gated=0 broken=23`).
- No tools installed; no production edits (read-only seat).
- Residual risk: digests bind at file level; instrument content semantics covered by sibling seats, out of scope here.
