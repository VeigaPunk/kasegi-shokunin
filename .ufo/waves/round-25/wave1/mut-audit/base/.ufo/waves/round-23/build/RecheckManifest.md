# RecheckManifest — scoped interface review

## Scope and verdict

Read-only review of frozen C2 in `.ufo/waves/round-23/claims.json`, `corpus/QUALITY.md` Q3/Q7, and the current `corpus/instruments/source-recheck.py`. No production edits, tests, `--selftest`, or network access. The mounted tool catalog exposed no LSP device, so caller/definition/diagnostic queries were unavailable; the literal reference search was not treated as semantic proof.

**Finding — High for C2/Q3 acceptance: the quote locator is decorative, not verified.** C2 requires “exact located quotes”; Q3 requires each load-bearing quote to have an exact location. In `source-recheck.py:82-97`, the manifest check requires a nonempty quote but does not require or validate `location`. At `:127-132`, success is based solely on `assertion["quote"] in source_text`, with no location read. The selftest has a location field (`:177-181`) but its clean case checks only exit status and output IDs (`:213`), so it does not catch a false locator.

## Concrete acceptance condition

For every quote, require a machine-checkable locator in the pinned snapshot (minimal form: one-based inclusive `line_start`/`line_end`). Emit quote `OK` only if the exact quote occurs wholly within that specified span, after the snapshot SHA-256 matches. A correct digest and quote paired with a wrong span must fail. Report success only as a check of the captured snapshot; it must not assert that the upstream source is current.

## Counterexample

Use the existing selftest payload `Captured fixture supports a verifiable local rule.\n` (`source-recheck.py:164`) and its matching `snapshot_digest` (`:165`). Its Q1 quote is `verifiable local rule` (`:177-180`), which occurs on line 1. Change only the location to `fixture line 999` (or a structured span for line 999): current control flow still emits `S900:Q1 OK` and returns success, because only substring membership is tested. This is falsifiable by adding that wrong-location control; it is a deduction from the inspected branches, not an observed test run.

## Residual risk and verification gaps

The tool's own boundary is correctly stated at `source-recheck.py:7-9`: it reads local files and checks captured bytes, not upstream availability or freshness. A digest binds bytes to the declared manifest pin; it does not authenticate the manifest or make a jointly changed manifest and snapshot current. At inspection, `corpus/source-snapshots/round-23/` listed S018.txt, S029.txt, and S030.txt but no manifest.json, so actual C2 quote rows could not be checked. No runtime outcomes are claimed.

Report: .ufo/waves/round-23/build/RecheckManifest.md
