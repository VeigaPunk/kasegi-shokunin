# MutationCollector — round63 finite harness attack

Axes: depth:verifiability only; nominal score4 held under R58. No coverage, new ground, integration or sandbox claim. Read lane SKILL/PROVINCE, QUALITY R17/R50/R53/R58/R72/R82 and round62 verifier spotcheck. No installs, runtime substitution, delegation, production edits or git/jj mutations.

## Tested bytes and receipts

All receipt paths below are under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/MutationCollector/`. Each `.txt` is the unedited stdout+stderr tee of one driver invocation; full argv, expected verdicts and subprocess output are included. Drivers and the exact tested collector are retained alongside receipts.

- `collector-tested.py`: SHA256 `fd3f7875d9ffa644510ed4e6df27b3ec6dfec7ee1c73fce7c5e7cb26bd1dfa60`; exact proposed collector copied after ExecCollector widened its seat-only guard to round63 seat/subdirectory. No guard delta in tested bytes. The earlier relocated scratch draft was overwritten before execution.
- Base instrument extracted read-only from committed `fdccc6da803965234c1eff5a0fee38b97e6621c1`: SHA256 `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080`.
- `harness-attacks.txt`: five requested fault classes, pristine and restored controls.
- `same-mode.txt`: exact same base-mode detector on pristine / always-green counterfeit / restored bytes, removing candidate-mode baseline ambiguity.
- `tree-probes.txt`: independent finite defective-tree proposals on committed base, not a candidate validation.

## Harness fault outcomes

| Fault/control | Observed | Verdict |
|---|---|---|
| Pristine base | exit0, `HARNESS probes=8 failures=0 mode=base` | positive control |
| Missing instrument | exit2, `HARNESS-ERROR FileNotFoundError` | fails closed |
| Unusable work (regular file) | exit2, `HARNESS-ERROR FileExistsError`; sentinel unchanged | fails closed |
| Instrument under work | exit2, `HARNESS-ERROR ValueError: instrument-under-work`; instrument byte-identical afterward | fails closed |
| Always-green counterfeit, candidate mode | exit1, failures4/8 | rejected; alone not a killed-mutant proof because no passing real candidate control was run |
| Same counterfeit, base mode | pristine0/0 failures → mutant1/1 failure → restored0/0 failures | killed by retained final-failure case |
| Correct-looking success output but process exits7, base mode | exit1, failures8/8; baseline and restored each exit0/0 failures | killed |

Counterfeit SHA256 `6a3607bd89245a5cc029fe8a8a81720725d4bc4b24a7aadb359ae376a08d9a29`; exit7 counterpart SHA256 `7ec10bbf1f54044ba32a1a304d8395de240f0ebc2afa3cbc821d3c7828149cd8`. Both were temporary substitutions of the assigned scratch instrument, restored in `finally`. Restoration SHA256 equals the base digest above, and restored bounded detector passes. These deliberate fake-audit controls are not R17 exact-once single-edit instrument mutants or an R50 per-limb battery; no such compliance claim is made. No collector false-green was found in these five fault classes.

## Independent R53 tree proposals

Keep `claim.md` unchanged and retain each ledger's `id`, `record`, `recorded`, `derive`, `want`; alter the bound fixture reality instead of deleting prose. Base false-greens observed:

1. Missing `missing.txt` with `cat missing.txt | wc -l`, want0: green. This is an upstream exit1 boundary, **not** an error>1 repair target. The initial pre-correction receipt expected red; its expectation is superseded here, never edited. L1/ExecCollector subsequently explicitly retained this green control.
2. Invalid regex `grep '[' present.txt | wc -l`, want0: green despite upstream error>1.
3. Nonexistent Git target `git show refs/heads/MutationCollector-nonexistent:path | wc -l`, want0: green. My independent tree has no Git repository, so this measures masked Git failure, not specifically ref lookup. The collector's own minimal empty-repository fixture supplies the missing-ref shape; no commit/index command is invoked.
4. `python3 corpus/instruments/fail.py | wc -l`, with fail.py exiting7, want0: green.
5. Middle-stage invalid regex `cat present.txt | grep '[' | wc -l`, want0: green; tests inspecting only the first upstream stage miss this shape.
6. `python3 corpus/instruments/fail.py | wc -l && wc -l < empty.txt`, want `0\n0`: green; tests inspecting only the final && group miss this shape.

All six preserve prose SHA256 `1316f622f11ffb4d9dd0831c099c732baf15131758b922e404a143bd561d41d1`. The instrument hash also stayed unchanged throughout the tree receipt. Further observed boundary: `cat present.txt | cat missing.txt | wc -l` green is also upstream1, not an error>1 defect. Controls: grep no-match|wc exit0 and final invalid-regex exit1/stale, as expected. Items2/4/5/6 are directly within positive-error>1 scope; at least three independent tree-level probes are supplied without enlarging the contract.

These are pre-freeze base counterexamples/proposals, not evidence that a future candidate rejects every tree. L1 should bind candidate receipts for adopted tree shapes before freeze; this seat did not run broad tests or judge the candidate.

## Limits and disposition

All executions and mutations stayed under `/fast/scratch/hyaku/kasegi-r63/MutationCollector`; outputs stayed in this seat's named paths. No source-registry/lesson changes proposed here. No negative-signal, option-screen, side-effect or general-error inference. Scratch is deleted after receipts are saved; exact base bytes were restored before deletion.

Self-evaluation: accuracy4 (exact hashes/outputs, Git-fixture and cat-exit1 qualifications explicit); completeness4 (five faults and >=3 trees covered, candidate tree verdicts deliberately not claimed); clarity4 (fault rejection distinct from mutation kill); actionability4 (drivers and pinned collector retained); conciseness4 (raw logs external). Average4.0. Improvement priority: bind these trees to final candidate bytes, without describing this finite attack as broad R50 compliance. User-agreement check: findings support only bounded collector discrimination, not a shipped repair.
