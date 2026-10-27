# MutAncestorGuard — round 41 wave 2

## Scope and detector

Attacked I2's `export-ref` ancestor/ref-not-found boundary in the archived integrated tree at `ad7147532cb702b0d541d40499874552183d9132`. Detector: the exported `corpus/instruments/r41-closure.sh --selftest --export-ref REF` (I2 graded case and payload) plus the export suite, with `--lane` explicitly set to the lane repository. No lane source was mutated. Scratch: `/fast/scratch/hyaku/kasegi-r41/MutAncestorGuard/`, removed by shell `trap` after each probe. Disk guard status returned the usage report, but its call timed out after 30 seconds.

## Baseline

The baseline probe at `ad7147532cb702b0d541d40499874552183d9132` exercised the detector but was **inconclusive**, not a clean baseline: full selftest output reported `selftest cases=12 failures=7`; I2 positive reported `ancestor=1` but `digest=0`, `selftest-verdicts=9`, `i2-line=0`. The suite reported `closed=10/12 exit=1`, with I2 red and I6 `read=fail` (the scratch-root layout was invalid for I6). This probe is not represented as a killed mutant. The detector's failures are environmental/fixture-related and distinct from the I2 ref limbs under test.

## Mutations and actual results

Mutation targets were generated in scratch by substituting the receipt `export-ref` with:

1. **Valid non-ancestor:** `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (resolves to a commit, but is not an ancestor of the current verification ref).
2. **Nonexistent:** `0000000000000000000000000000000000000001` (unresolvable in the lane repository).

The valid-ref case is the I2 `foreign-ref` fixture already embedded in the committed selftest: its actual output was `selftest detail=I2 mutant=foreign-ref rejected=1 limb=ancestor=0`. The I2 case ended `mutants=5/5`, but its positive failed and the overall case was graded `verdict=fail`; therefore this is **inconclusive** evidence for a mutation kill under the requested baseline rule, despite the foreign-ref limb producing the expected rejection. Its export-suite output was `I2 payload=receipt=0,...ancestor=0... closed=0` and `closed=3/12 exit=1`; that suite invocation used the non-receipt export tree, so it did not contain a mutated receipt and is not counted as a kill.

For the nonexistent ref, actual output from the export suite was `I2 payload=ref-not-found,ref=0000000000000000000000000000000000000001 closed=0` and `closed=0/12 exit=1` (exit 1). This distinctly identifies the ref-not-found path rather than an ordinary ancestor failure. The selftest exited 1 with `selftest cases=0 failures=0`: it cannot run the I2 fixture grading when export preparation fails. This is **inconclusive** for selftest mutation killing, but the suite's ref-not-found behavior is observed directly.

## Verdict and restoration

No mutant was killed conclusively because the required baseline detector failed. The ancestor rejection limb did produce the expected `ancestor=0`; nonexistent ref produced the distinct `ref-not-found` payload. This is a coverage observation, not a contract change. No committed or lane bytes were changed: probes used `git archive` into the isolated scratch directory, and the `trap` removed that directory after each process. No tools were installed.
