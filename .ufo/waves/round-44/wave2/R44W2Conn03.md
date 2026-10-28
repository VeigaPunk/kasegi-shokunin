# R44W2Conn03 — cross-lane naming/CLI scan

**Axes:** `depth:verifiability` (C1) and `coverage` (C2), from `.ufo/waves/round-44/claims.json:9-24`. This scan makes no claim verdict.

## Finding

**One bounded CLI-adjacency risk; no exact name or receipt-path collision found.** The other-lane routed-defect counter I found is `kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py`. Its CLI requires `--root DIR --rev REV`; `--root` means a Git repository and `--rev` pins a commit (`kaidoku…/routed-defects.py:1394-1405`). Kasegi's `corpus/instruments/r44-routed-defects.py` instead takes `--root` as a tree to grade, with optional `--baseline`, `--selftest`, and `--work` (`corpus/instruments/r44-routed-defects.py:525-543`); the frozen C1 invocation explicitly supplies an exported lane tree and baseline (`.ufo/waves/round-44/claims.json:14`). Both tools also expose `--selftest`. Thus the `--root`/`--selftest` overlap could mislead a generic fleet reader who omits the full path, but the required flags and semantics differ; invoking the wrong tool with the other's documented arguments fails or measures a different input. Their basenames are distinct (`routed-defects.py` vs `r44-routed-defects.py`).

Other routed-defect-like candidates are not conflicting CLIs: Tabi's round-38/39 counters are Node `.mjs` tools using `--rev`/`--repo` (and round 39 `--claims`/`--json`; `tabi-shokunin/.ufo/waves/round-38/counters/c1-routed-defects.mjs:37-39`, `round-39/counters/c2-routed-defects-v2.mjs:30-33`). Tameshi's `corpus/routed-defects.json` is a `tameshi-routed-defects-v1` ledger, not an executable counter; Kengaku's sibling-ledger scan identifies it as the sole exact `corpus/routed-defects.json` hit (`kengaku-shokunin/.ufo/waves/round-51/w1/C2ScoutSiblingLedgers.md:17-24`). Chousa has a distinct `corpus/evidence/round40/routed-defect-dispositions.json`, also data rather than a counter.

Exact-name/path scan across visible `*-shokunin` repos: `wave-registry.py`, `r44-routed-defects.py`, `r44-frontier-count.py`, and `wave-registry.txt` each occur only under kasegi; the only `routed-defects.py` basename hit is kaidoku's round-18 tool. Other lanes have separate `.ufo/waves/round-44/` directories, but none has the same `wave-registry.txt` filename. Kasegi's own `corpus/instruments/README.md:992-993` documents the C1 counter and emitter; the emitter writes the lane-local `.ufo/waves/round-44/wave-registry.txt`.

## Proposed move

Keep the round-prefixed Kasegi filename. Add one short phrase to its registry row/docstring clarifying that `--root` is an exported filesystem tree (not a Git root; this tool has no `--rev` mode). That closes the only discovered flag-semantics ambiguity without changing the frozen CLI or counter behavior.

**Risk/tradeoff:** Documentation-only; no observed shared dispatcher invokes counters by basename. A generic reader may still confuse similarly named tools if it discards lane/path context. No evidence that this ambiguity changed a C1/C2 result.

## Verification / limits

Read-only checks performed:

- `find . -name 'wave-registry.py' -o -name 'r44-routed-defects.py' -o -name 'r44-frontier-count.py' -o -name 'routed-defects.py'` from fleet root: exact results as described above; `find` for `wave-registry.txt` found only `kasegi-shokunin/.ufo/waves/round-44/wave-registry.txt`.
- `grep -nE 'add_argument|def main|argv|Usage|--' tabi-shokunin/.ufo/waves/round-38/counters/c1-routed-defects.mjs tabi-shokunin/.ufo/waves/round-39/counters/c2-routed-defects-v2.mjs`: confirms Node CLI flags above.
- `grep -rn 'r44-routed-defects\\|r44-frontier-count\\|wave-registry\\.py'` outside kasegi: no fleet-root reference found.
- `grep -rnE 'routed-defect\\*|routed-defects?\\*|glob.*registry|\\*REGISTRY|registry\\*'` over code found no fleet-level routed-defect discovery. The only relevant registry glob inspected was kaidoku `tools/round-30/settle-gate.py:91-93`, which reads `*/swarm-registry.json` (JSON, different basename/format), not Kasegi's text registry.

No instruments were executed and no other lane was modified. Limits: this is a filesystem scan of visible working trees, not a census of unreachable/history-only branches or external tools; no exact cross-lane shared receipt path or basename collision was observed. No tools installed.
