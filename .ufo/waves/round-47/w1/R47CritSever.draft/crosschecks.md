# Cross-check constructions (static; not executed)

Axes: depth:verifiability; coverage.

Use a historical base export fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8, not the mutable lane working tree. Use counters/helpers/capture bytes from freeze 308a2cb2dc7bdce233461cc1ac49dd88e51c6193. Any executor's exports, fixtures and explicit counter --work directories must remain under that executor's assigned scratch root and be removed afterward. No git mutation is required: read-only git archive exports suffice.

The committed builders in corpus/instruments/r47-counters-selftest.py already specify the two constructions:

A = build_c2_green(base, own_work). Its file delta is S075 row + F30 README row + synthetic F30 entry + round-47 frozen snapshots/manifest (:320-342). It leaves SOURCES scaffold, F29 entry, and lessons unchanged. This is a mechanical synthetic fixture, not the production F30 draft or an admission decision.

B = build_c1_green(base, own_work). Its file delta is landed SOURCES bullets + REST lead + S076 row + S074 status/used-by edits; corrected F29 bytes; appended round-46 corrections; round-47 fixture lesson; frozen round-47 snapshots/manifest (:212-228). It does NOT add S075's registry row, F30's README row, or F30's entry. The helper's LANE constant must refer to the frozen export if using it in an executor probe, because the helper otherwise copies snapshots from the live lane (:223-227,337-341).

Evaluate BOTH frozen counters on A and B, with explicit --work under own scratch. Also evaluate historical base and unchanged freeze exports as negative controls. Preserve every limb line, process exit, source revision and fixture delta. Do not relabel the existing synthetic positive fixtures as do-nothing controls.

Predicted matrix, NOT new execution results:

| Tree | C1 | C2 |
|---|---|---|
| Historical base | 0/11, exit 1 | 1/7 (H7), exit 1 |
| Unchanged freeze | 0/11, exit 1 | 2/7 (H4,H7), exit 1 |
| A: only C2 | 0/11, exit 1; all L1-L11 red | 7/7, exit 0 |
| B: only C1 | 11/11, exit 0 | 2/7, exit 1; H1,H2,H3,H5,H6 red; H4,H7 green |

The builders' own-counter positive grades are independently recorded in the existing peer receipt .ufo/waves/round-47/w1/R47ExecSelftestReplay-selftest.txt:1,21. That receipt does not contain the reverse-counter cross-checks and must not be presented as their execution.

Semantic correction before using B as truthful provenance: its stock LESSON47_STUB says ZDI is admitted as F30 with S075 (:195-196), while B deliberately contains neither admission row nor entry. For the C1-only counterfactual replace that sentence with: 'ZDI reservation: preserve S075/F30 for the separately proposed C2 admission; C1 alone does not admit it.' L11 only requires ZDI + reservation and S068 + one GHSA advisory entry, so this removes the false admission statement without importing C2 into B. This is a proposed fixture correction, not an applied production change or a changed counter predicate.
