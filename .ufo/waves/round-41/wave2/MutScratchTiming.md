# MutScratchTiming — I6 scratch-scan probe

## Probe and detector

Target: committed `corpus/instruments/r41-closure.sh` at integrated ref `ad7147532cb702b0d541d40499874552183d9132`. Detector: that suite's export run and graded `--selftest --export-ref` using isolated `--scratch-root` and `--work` paths under `/fast/scratch/hyaku/kasegi-r41/MutScratchTiming`. Disk guard was checked before running.

The assigned environmental mutation was a family-named stray outside the configured scan root: `/tmp/kasegi_r41_outside_probe`. The request to create a family-named stray only after a scan was also considered: a completed scan cannot retrospectively detect a subsequent filesystem change; the committed I6 selftest checks static fixtures, not a concurrent timing race.

## Actual outputs and verdict

Pristine export run: exit 1; `I6 payload=strays=0,read=ok,scanned=0 closed=1`, overall `closed=11/12 exit=1`. This is an inconclusive baseline for whole-suite kills: I2 was open because this integrated ref does not contain the receipt, and the selftest had five failures (I1, I2, I3, I6? No: I6 passed; actual failed cases were I1, I2, I3 and I2's own positive accounting, with `selftest cases=12 failures=5`). The exact emitted transcript was retained in scratch during the probe; see the results below for all relevant lines.

External-stray mutated run: exit 1; despite `/tmp/kasegi_r41_outside_probe` existing, I6 remained `strays=0,read=ok,scanned=0 closed=1`, identical in substance to pristine I6. This is a surviving environmental escape: I6 scans only the configured root, so an outside-root object is not observed. It does not satisfy the frozen C1 kill rule's explicit committed-fixture condition (the stray was host state, not a committed fixture), nor is the out-of-root path within the stated scan contract. Verdict for the assigned outside-root challenge: **survived as expected for the configured-root boundary; not routed by the frozen kill rule**.

Selftest output included `selftest case=I6 mutants=5/5 positive=pass payload-match=1 verdict=pass`; its details were `family-stray`, `nested-family-stray`, `dot-prefixed-stray`, `case-separator-stray`, and `unreadable-scratch-root`, each `rejected=1`. The suite does not include either a post-scan race or an outside-configured-root fixture. Overall selftest exit 1, `selftest cases=12 failures=5`, and `selftest judge=own-report accepted=0`; therefore no claim that the whole suite is green is made.

## Restoration evidence

Suite bytes before and after probes had SHA-256 `3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd` (unchanged). No suite mutation was made. The trap removed the entire seat scratch directory and the `/tmp` stray on completion. No tools installed.