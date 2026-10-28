# R44W2Exec05 — marker-only C1 probe

## Finding

**Axis attacked:** `depth:verifiability` / frozen C1. **The hypothesis holds for the strongest marker-only tree:** the committed counter printed `fixed=8 unresolved=0 exit=0` even though all round-44 binding files added for this probe were explicitly fabricated and no underlying measurement or repair operation was performed. Thus this probe falsifies the counter's ability to distinguish those fabricated assertions from genuine repair evidence. It does not establish that the committed lane evidence itself is false, nor by itself adjudicate C1's frozen kill rule.

## Inputs and construction

- Required frozen claims read: `.ufo/waves/round-44/claims.json` (C1 kill rule: a do-nothing replay against the frozen base reporting all 8 fixed kills C1).
- Routed-defect specification read: `corpus/lessons/round-43-verifier-spotcheck.md` §6, defects 1–8.
- Base export: `git archive 5ab3a60` extracted to scratch. `5ab3a60` is the observed commit `round-43 verifier spot-check (integrator, hyaku): non-author admit/reject`; the checked-out target instrument was at `8063547d0ce647d6f9eafc3c8d0a502616685218`.
- The committed instrument bytes were pinned before execution: `sha256sum` of `git show 8063547:corpus/instruments/r44-routed-defects.py` and its scratch copy both returned `7e7c145f831a04d4b094ce6fda228587368c2aee04baadbb8345404a8baca950`.
- Strongest tree construction: start from the 5ab3a60 export; append the matching prose markers to SCORECARD, round-43 lesson, LOG, SHONEN and instruments README; add marker-only round-43 erratum and round-44 lesson; fabricate a wave1-results JSON with 66 fake seats, a registry with 66 fake names, a nonfunctional registry-emitter stub, export-ref sidecar and missing-suite receipt. The receipt explicitly says no command was executed; the results explicitly say no seat ran. No real count, suite, wave, registry emission, or receipt measurement was performed. The base's `.tmp` leftover was absent in the exported tree. SHONEN was given a final blank line because D6 checks that byte property directly.

The probe therefore supplies assertion text and self-consistent fabricated structures—not the genuine committed repair evidence. Relevant instrument predicates: D1 checks correction/erratum tokens and existence (`r44-routed-defects.py:172-212`); D2 checks erratum tokens plus lesson vocabulary (`:215-243`); D3 checks correction strings (`:246-268`); D4 checks LOG prose against the results-file seat count (`:271-295`); D5 checks emitter substring, registry fields/count, and sidecar tokens (`:298-328`); D6 checks the final two newline bytes (`:331-341`); D7 checks README/SHONEN strings (`:344-358`); D8 checks erratum/receipt strings (`:361-378`). These are committed-file line references from the instrument read.

## Exact counter output — strongest marker-only tree

Command, run from the lane repo against the committed instrument:

```sh
python3 corpus/instruments/r44-routed-defects.py --root /fast/scratch/hyaku/kasegi-r44/R44W2Exec05/tree-strongest
```

```text
R44-D1 status=fixed detail=correction appended after the row; erratum carries 13/19 + superseded
R44-D2 status=fixed detail=.ufo/waves/round-43/claims-erratum-6.md matched by K17's own escape; mechanism named in the round-44 lesson
R44-D3 status=fixed detail=appended correction states 26 characters with the counting command; history kept
R44-D4 status=fixed detail=planner=L1, L2-floor and residual lines recorded; wave-1 seat count 66 cross-checks
R44-D5 status=fixed detail=leftover absent; emitter and a populated registry committed; export-ref sidecar present
R44-D6 status=fixed detail=final empty line restored; four boxes present
R44-D7 status=fixed detail=registry rows present in corpus/instruments/README.md; SHONEN pointer corrected by append
R44-D8 status=fixed detail=erratum separates the two exits; the 127 is backed by a committed receipt
routed-defects total=8 fixed=8 unresolved=0 exit=0
```

## Contrast: prose markers without newly created bound files

A less powerful tree (same base plus narrative markers, but no erratum-6, round-44 lesson/results, registry emitter/registry, sidecar, or receipt) yielded `fixed=3 unresolved=5 exit=1`: D3, D6, D7 fixed; D1, D2, D4, D5, D8 unresolved. Untouched base yielded `fixed=0 unresolved=8 exit=1`. These controls show the 8/8 result required the fabricated structures; they do not negate it.

## Limits

This is a scratch-tree falsification of the counter's evidence predicate: the counter accepted fabricated token-bearing artifacts and self-consistent fabricated seat counts. It does not show the real committed artifacts are fabricated. No production files were changed by the probe; the only lane write is this assigned report. No tools were installed. Scratch was removed before handoff.
