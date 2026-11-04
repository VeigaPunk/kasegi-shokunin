# ExecCollector — round 63 predata proposal

Axes: depth:verifiability nominal, score4 held; no coverage/new-ground claim. No production edits, Git mutations, tools/config changes, installations, delegation, builds, linters or lane-wide gates.

## Deliverables

All artifacts below are under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/ExecCollector/`:

- `c1-probes-r63.py`: CLI `--instrument ABS --work ABS --mode base|candidate`; eight finite end-to-end probes; compares return code and complete stdout/stderr, including complete figure finding and figures/ok/stale/exit trailer. Missing instrument/dependencies or unusable scratch return2. Instrument-under-work rejected before fixture creation. Never clears existing work; deletes only its fresh temporary run. TMPDIR owned; shell-free subprocess argv. Requires only Python stdlib and PATH python3/cat/grep/wc/git.
- `base-figure-audit.py`: exact committed blob from `fdccc6da803965234c1eff5a0fee38b97e6621c1:corpus/instruments/figure-audit.py`.
- `base-receipt.txt`, `candidate-receipt.txt`: each the untouched merged stdout+stderr from one collector invocation, written once. Each preserves actual CLI argv, derive strings, expected tuples, actual exits/stdout/stderr and PASS/FAIL records.
- `base-command.json`, `candidate-command.json`: exact invoking argv and observed collector exit0, separate from raw receipts.

## Observed results

Both receipts end `HARNESS probes=8 failures=0` with their respective modes. Base SHA256 `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080`; candidate SHA256 `e557d2f0ceea9866b40b7b99dd53864a00330ae7481f32e7eeefca2fbf2431e8` from `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/ExecPipeline/figure-audit.py`, available without polling.

| Probe | Base | Candidate |
|---|---|---|
| cat missing / wc | exit0 figures1 ok1 stale0 derived0 | same |
| invalid grep regex / wc | exit0 figures1 ok1 stale0 derived0 | exit1 figures1 ok0 stale1 reason derive-upstream-exit-2 |
| nonexistent git ref / wc | exit0 figures1 ok1 stale0 derived0 | exit1 figures1 ok0 stale1 reason derive-upstream-exit-128 |
| python fail.py exit7 / wc | exit0 figures1 ok1 stale0 derived0 | exit1 figures1 ok0 stale1 reason derive-upstream-exit-7 |
| grep no-match / wc | exit0 clean derived0 | same |
| success cat / wc | exit0 clean derived1 | same |
| final grep no-match | exit1 stale reason derive-exit-1 | same |
| successful cat && cat | exit0 clean derived `35\n35` | same |

**Explicit L1 correction:** `cat missing` exits1, outside positive upstream>1. L1 directed retaining this as green boundary/residual control (M63-4), not inventing a fourth >1 repair. Original request's four-stale formulation is therefore not asserted. Three named >1 repairs are observed.

## Limits and process evidence

Read lane SKILL/PROVINCE, QUALITY R17/R50/R53/R58/R72/R82, and round-62 verifier spotcheck. Minimal empty Git fixture written directly under private scratch, without git init, index, commit or other mutation command. No shell, live target, credentials, private URL or external source claim. No LSP interface is mounted; symbol navigation used read/grep, not an empty LSP response.

Base invocation preceded a preflight-only portability revision: work guard now accepts `/fast/scratch/hyaku/kasegi-r63/SEAT/SUBDIR` rather than only this seat, enabling falsifier-owned scratch. Probe tables/assertion logic unchanged; candidate receipt runs the delivered revision. No base rerun was performed. Caller must select its own seat; guard enforces round root/depth, not caller identity. Runtime binaries/PATH are host dependencies, not hermetic or sandbox claims.

MutationCollector received the exact source/interface for independent fault probes. No mutation breadth/compliance claim is made here; R50/R53 freeze readiness remains L1's integration decision. Proposed collector is not itself proof against arbitrary fabricated audit output, signal statuses or side effects.

All private probe directories and this seat's empty scratch directories were removed after receipts were saved. Parent should run delivered collector on final committed export and integrate falsifier evidence before freeze. No final gate run by this seat.

Self-evaluation: accuracy4 (raw exact receipts; base guard revision explicitly distinguished); completeness4 (requested probes and controls, L1-corrected cat boundary); clarity4 (full tuples retained outside concise summary); actionability4 (absolute source/interface and receipts supplied; final committed gate belongs to L1); conciseness4 (raw evidence linked, not duplicated). Average4.0. Highest-impact improvement: bind final freeze bytes to parent export run; user agreement depends on preserving the explicit three-repair scope.

Report: .ufo/waves/round-63/w1/ExecCollector.md
