# R47MutC2b — C2 set B mutation findings

Axes: depth:verifiability (pristine/mutated/restored evidence), coverage (H5–H7 discrimination).

## Result

Six fresh counter-source mutants: **0 killed, 6 survived, 0 inconclusive**. All 18 detector runs printed `selftest cases=23 failures=0 exit=0` with process exit 0. These are disclosed selftest coverage findings, not an equivalence proof or a claim that malformed production content passes the integrated gate. No full battery was rerun.

## Detector and do-nothing control

Detector: freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193` copies of `corpus/instruments/r47-counters-selftest.py` and `r47-f30-gate.py`; base exported read-only with `git archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus`. Each receipt records the complete command, stdout, stderr and return code. Invocation: `python3 -I <scratch>/instruments/r47-counters-selftest.py --base <scratch>/base --work <explicit-scratch-work> --counter c2 --gate <mutant-copy>`. Source-recheck sibling copied from freeze.

The named do-nothing controls are each `B*-pristine` run; exact restored-byte controls are `B*-restored`. The same 23-case C2 detector runs at all three stages. Expected killing signal: valid pristine/restored controls plus a mutated `selftest failures>0`; an unchanged `failures=0` is survival under this detector. This matches the frozen selftest contract at `corpus/instruments/r47-counters-selftest.py:24-26` and battery grading at `corpus/instruments/r47-mutbat.py:168-191`.

| Mutant | Frozen counter line | Smallest defect | Actual pristine / mutant / restored failures | Verdict |
|---|---:|---|---|---|
| B1-H5-lower-bound-omitted | 339 | Drop lower body bound `a >= BODY[0]` | 0 / 0 / 0 | survived |
| B2-H5-upper-bound-omitted | 339 | Drop upper body bound `b <= BODY[1]` | 0 / 0 / 0 | survived |
| B3-H6-name-pin-bypassed | 359 | Bypass base knowledge-name SHA pin (content pin retained) | 0 / 0 / 0 | survived |
| B4-H6-link-verdict-omitted | 368 | Ignore knowledge symlinks in H6 verdict (counts/pins retained) | 0 / 0 / 0 | survived |
| B5-H7-census-exit-ignored | 382 | Ignore census process return code; require only ok-line | 0 / 0 / 0 | survived |
| B6-H7-SOURCES-link-guard-omitted | 374 | Drop SOURCES.md symlink guard; retain corpus guard | 0 / 0 / 0 | survived |

All line references in that table are to `corpus/instruments/r47-f30-gate.py` at freeze. Mutation strings, each mutant hash, exact command receipts and restoration evidence are under `.ufo/waves/round-47/w1/R47MutC2b.draft/`. See `results.json` for the six complete records; the 18 `B*-{pristine,mutated,restored}.txt` files contain the actual 23-case outputs.

## Restoration and isolation

Each pristine and restored counter SHA256 equals `563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b`; each mutated SHA differs (all six values in `results.json`). Each record has `exact_restore: true`. Entire scratch `/fast/scratch/hyaku/kasegi-r47/R47MutC2b` was removed in Python `finally`; `cleanup.json` records `exists_after_cleanup: false`. No production source, sibling files, index, or git history was changed; no commits or installs. Only read-only git archive/show used. Disk guard printed `/fast/scratch/hyaku 53% 378.0G free`; its subsequent top-consumer scan timed out after 30 seconds, so no completed disk-guard success is asserted.

## Interpretation and limits

- H5: existing `widespan` attacks both body bounds together; removing either bound alone still lets the other reject it. The detector does not discriminate these independent guards. More focused future fixture candidates: a located body quote cited as `1-24` (lower-only violation) or `24-60` (upper-only violation), rather than both bounds violated. These candidates were not executed here.
- H6 name-pin bypass retains the content hash, which also incorporates names. Survival alone cannot establish this mutant is non-equivalent. No equivalence adjudication performed. H6 link verdict likewise remains partly constrained by counts and byte pins; an equal-byte symlink fixture is absent from the selected frozen cases.
- H7 source symlink fixture is a dangling `etc/hostname` relative link (`r47-counters-selftest.py:428`), so later Registry checks can still make it red after the guard is removed. This is masking, not evidence the guard is tested. A valid-target symlink fixture would isolate the guard.
- Ignoring census exit status survives because the present fixtures do not independently produce an ok-line plus a failing process status. Census remains a fleet-root external dependency (`r47-f30-gate.py:379-382`); no external helper was changed or substituted.
- These six are distinct from the 21 frozen C2 mutation substitutions (`r47-mutbat.py:90-111`), including the broader H7b removal of the entire symlink guard. The known pre-freeze totals (C1 16 survivors, C2 18 survivors) remain disclosed and are not replaced or closed by this bounded result. Wave-2 integrated-tree behavior was not tested.

## Self-evaluation

Accuracy 4/5: full outputs and hashes retained; no equivalence adjudication. Completeness 5/5: six mutations, triplets, controls, restoration and cleanup recorded. Clarity 4/5: source-mutant survival distinguished from artifact false-green; overlapping guards need careful reading. Actionability 4/5: specific fixture gaps identified, not implemented under this probe-only seat. Conciseness 4/5: detailed receipts separate from summary. Overall 4.2/5. Highest-impact next measurement: isolate one bound and a valid-target symlink. User agreement self-check: results are bounded, reproducible and do not claim uncaught=0.
