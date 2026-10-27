# MutSuite — Round 41 falsify

## Result

The assigned requirement was not met: I did not demonstrate 12 killed byte-level mutants. The integrated suite's graded selftest at ref `ad7147532cb702b0d541d40499874552183d9132` is already red, so the required clean pristine baseline is absent and failures cannot be attributed to my mutations.

Pristine suite source SHA256: `3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`. Command: `bash r41-closure.sh --selftest --export-ref ad7147532cb702b0d541d40499874552183d9132 --lane <lane> --work <scratch>/work-base`; observed exit 1 and `selftest cases=12 failures=7`. Failing case details: I1 `mutants=1/2 positive=fail payload-match=0`; I2 `mutants=5/5 positive=fail payload-match=0` (payload reported `selftest-verdicts=9`, `i2-line=0`); I3 `mutants=0/1 positive=fail payload-match=0`; I6 `mutants=4/5 positive=fail payload-match=0` (`read=fail`, `unreadable-scratch-root rejected=0`). I4, I5, I7-I12 were green. I6's positive failed in this isolated seat scratch location; this run does not establish a defect independent of scratch-root setup.

## Byte-mutant outputs

| Limb / mutation | Mutated suite SHA256 | Observed result | Verdict |
|---|---|---|---|
| I3 token-boundary regex `[[:space:][:punct:]]` → `[[:space:]]` | `11e6c2aede8c239ce8842fb5622acf026a36bd9eb4bc3f5e5d6a8f1991dfd865` | exit 1; I3 `mutants=0/1 positive=fail payload-match=0 verdict=fail` | Inconclusive: baseline I3 already failed |
| I4 fence-state branch `if (in_fence)` → `if (0)` | `f76390f44c50921cb5c5f9ae1501ba9a270308e72723f9da799b6eec5347998f` | exit 1; I4 `mutants=0/2 positive=fail payload-match=0 verdict=fail` | Inconclusive: positive was broken; no isolated kill attribution |
| I10 negative acceptance default `R41_NEG_WEAK:-0` → `R41_NEG_WEAK:-1` | `2da00cd87cddafbdda00ae3ae8f3d5bc05461b3baa1f0645fd77b798944cb15fc1c` | exit 1; I10 `mutants=0/1 positive=fail payload-match=0 verdict=fail` | Inconclusive overall because pristine baseline is red; I10 output alone is not sufficient evidence |
| I2 receipt comparison replacement `cmp -s` → `true # cmp -s` | `d15a8ac77d5679339618142c561052c2001b0a3e1c172d1f14aff54dc9b12939` | exit 2, no graded I2 line | Invalid mutation (replacement not semantically/syntactically suitable); not scored |

Path canonicalization, case-fold, scan-depth, work-dir exclusion, and per-case isolation probes were not executed: my initial byte needles did not match the source and I did not misreport them as mutations. No survivor verdict is claimed.

## Evidence and cleanup

Actual baseline/mutant transcripts and hashes are in `MutSuite.findings.txt`; the raw working copies were kept only under the assigned scratch directory and removed before filing. No tools were installed. No final Y verification is claimed. Main follow-up is to establish the proper scratch-root environment and rerun a pristine accepted baseline, then repeat the planned matrix; until then this probe provides no coverage claim.
