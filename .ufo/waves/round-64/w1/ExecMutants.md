# ExecMutants (round-64 w1) — command-aware upstream mutation battery

Seat: ExecMutants-4 (executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Base: master d74be00a82c8c2962a0b78442c5daea3af0adaae.
Run UTC of receipts: 2026-11-04T18:38Z–18:40Z. Final candidate pin (supersedes ca1015b2…): `.ufo/waves/round-64/w1/ExecPipeline/figure-audit.py` sha256 c233577dbf0517df29e2c7d938946bc9b06f9c4a8cf4af2654bc058c68c7df01, 503 lines; construct-only receipt `receipts/construct-only-candidate-c233577d.txt` (failures=0). Guard anchors verified exact-once at upstream_stale 79-86, heads 94/107, guard 119-120. Probe and mutant verdicts were NOT produced for either pin.

## Deliverable
- Battery: `.ufo/waves/round-64/w1/ExecMutants/figure-audit-mutbat-r64.py` (sha256 aba9f35b2f6acb03c42629c82fd6dce03aef059baff00c0304ca34f34fca4870, receipts/battery-sha256.txt).
- Control driver: `.ufo/waves/round-64/w1/ExecMutants/falsegreen-control-r64.py`.
- Receipts: `.ufo/waves/round-64/w1/ExecMutants/receipts/` (raw one-invocation outputs, run UTC printed).

## Layers (both through the real CLI)
1. Selftest layer: exact-once text mutants of the instrument, each run as `python3 INSTRUMENT --selftest`.
2. Probe layer: fixed fixture tree (g.txt, corpus/instruments/{fail,sigkill,sigterm}.py) and one-figure ledgers run as `python3 INSTRUMENT --ledger L --root R`. Probe verdicts do not read the instrument's selftest. Every m- mutant must be killed by the probe layer alone.
- Verdict classes: m- killable (must be probe-killed), e- equivalent and c- control (must be held), i- invalid control (must be rejected by exact-once anchoring). A probe run that yields neither FIGURE-AUDIT summary nor exit 0/1 is `invalid`, not a kill.
- Native fixture exits are checked before any instrument runs (fixture-valid gate).

## Probe set (21)
Upstream positive failures (candidate expects stale): cat missing, cat partial (g.txt + missing), cut/head/tail/sha256sum missing, ls/sort missing (exit 2), cat middle-stage missing, `&&`-preceding success then upstream failure.
Controls (candidate expects unchanged): grep no-match (first and middle stage), grep exit2 stale, pipe ok, `&&` concatenation, `&&` first-stage final failure, final exit1 stale, final-over-upstream precedence (derive-exit-7), python exit7 upstream stale, SIGKILL and SIGTERM upstream ignored.

## Construction receipts (pre-freeze; no candidate scoring)
- `receipts/construct-only-candidate-ca1015b2.txt`: anchors against ExecPipeline candidate sha256 ca1015b2488cb63c22f56e1118714c593be65f0e6bc9bea1a0121f6391984a5c (pinned at 18:37Z). Result: 14 native fixture exits all match; every anchor exact-once except the two invalid controls (sites 0 and 2, both rejected); all m-/e-/c- mutant texts compile; construct-only failures=0.
- `receipts/base-contract-master-15bcb6c4.txt`: base probe expectations run against the master instrument (sha 15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997): 21/21 met.
- `receipts/base-under-candidate-contract-falsegreen.txt`: the same master instrument scored against the candidate contract: 8/21 mismatch = falsegreens: p-cat-missing, p-cat-partial-missing, p-cut-missing, p-head-missing, p-tail-missing, p-sha256sum-missing, p-cat-middle-missing, c-and-success-then-upstream-fail. This is the r63 gap the probe layer is designed to surface.

## Mutant set (per limb >=3 exact-once, against candidate anchors)
- thresh: m-thresh-exit1-ignored, m-thresh-gt1-to-99, m-thresh-disabled
- grep exemption: m-grep-exempt-removed, m-grep-exempt-any-head, m-grep-gt1-exempt
- negative signal: m-neg-counted-nonzero, m-neg-below-minus1, m-neg-sigterm-only
- precedence/middle: m-final-disabled, m-final-only-gt1, m-middle-first-only
- equivalents: e-head-basename-dropped (argv[0] is always a literal admitted head, so basename is redundant under the grammar), e-heads-copy
- control: c-trailing-space
- invalid: i-anchor-absent (0 sites), i-anchor-duplicated (`p.wait(`, 2 sites)
Docstring is untouched by every mutant (prose-preserving), so kills must come from behaviour.

## Full scoring: NOT RUN (pending L1 freeze)
Candidate scoring is withheld per the lane rule. After freeze, L1 (or the main agent) runs once:
`python3 .ufo/waves/round-64/w1/ExecMutants/figure-audit-mutbat-r64.py --instrument <frozen figure-audit.py> --work <fresh scratch dir>`
Expected pass criteria: pristine selftest rc 0 and all 21 probes met; each limb >=3 m- mutants valid and probe-killed; both e-/c- held; both invalid controls rejected. Any `sites=` or `probe_invalid` output is a battery failure, not a kill.
Construction note: the run requires the frozen file's sha to match the pinned candidate; re-run construct-only first if the sha changed.

## Discrepancies found
- Spec says base greens are want0 except partial (want1). Measured on master: ls-missing and sort-missing are STALE with derive-upstream-exit-2 (the r63 `>1` rule catches exit 2). Only cat/cut/head/tail/sha256sum/middle-cat are base-green. The partial probe is base-green want1 as stated.
- Negative-signal handling: the r63 selftest has no signal case. Killing mutants for the signal limb come only from the new SIGKILL/SIGTERM probes, which is why probe-layer kill is required.
- Candidate's own selftest count (54 per ExecPipeline) was not verified by me; the battery does not depend on it.

## Tools
No installs or updates performed. Interpreter: python3 3.14.8 (existing).

## Scratch
/fast/scratch/hyaku/kasegi-r64/ExecMutants/ (ref, base, work trees, tmp). Removed on exit after receipts were copied.

## Coordination
- ExecPipeline-3: confirmed anchor list against sha ca1015b2… (no scoring).
- KasegiR64: progress acknowledgement sent.

## Verdict (scoped)
Battery authored and construction-verified pre-freeze. Full candidate kill verdict not produced (freeze gate). Control evidence: the base master is 8/21 falsegreen under the candidate contract, and 21/21 green under base expectations.
