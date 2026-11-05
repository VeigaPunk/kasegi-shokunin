# Round-76 red-before mutants (base counter bytes e666ae11…a21a)

Each file is the base `corpus/instruments/recheck-cwd-census.py` with exactly one patch:

- `m1-forged-relabel.py` — neither-header knowledge files are counted as
  `restoration_only` (the M75-3 forged relabel of the base norecheck bucket).
- `m2-result-limb-removed.py` — the case-6 RESULT limb
  (`ret6 == 1 and "RECHECK-CWD-RESULT nonconformant" in out6`) removed
  (the M-P4 removal shape from round-75 MutAuditC1).
- `m3-restoration-forces.py` — any file carrying a `restoration-recheck:` line is
  classified restoration_only even when a `recheck:` line exists.

All three pass the BASE selftest (`selftest cases=6 failures=0`, rc=0 —
`../c1-redbefore-mutant-survival-r76.txt`) because the base fixture set has no
case that discriminates them. The frozen C1 A3 requires each to fail the
AMENDED selftest.
