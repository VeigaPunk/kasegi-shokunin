# R46bSimplifierDrafts — receipts

The findings live in `../R46bSimplifierDrafts.md`. This directory holds the raw transcripts of the
re-runs that back it (the scratch tree itself was removed on exit, as the seat card requires).

* `f29-orig-*.txt` / `f29-cut-*.txt` — the frozen F29 gate and the cut copy on the base, positive,
  junk and fabricated trees (byte-identical per pair).
* `list-orig.txt` / `list-cut.txt` — the mutation battery's `--list` output (frozen vs cut copy).
* `mutbat-stub-orig.txt` / `mutbat-stub-cut.txt` — the whole battery flow (41 mutants) on a tree
  whose two selftests are stubs; frozen vs cut copy (byte-identical).
* `mutbat-real-c1-PARTIAL-timeout.txt` — the real battery run I attempted; it was killed by the
  1800 s cap after one mutant (its one line reproduces the frozen receipt's first line).
* `c1selftest-orig.txt` / `c1selftest-cut.txt` — the committed C1 selftest, frozen vs cut copy
  (76 cases, byte-identical).
* `c2selftest-orig.txt` / `c2selftest-cut.txt` — the committed C2 selftest, frozen vs cut copy
  (137 cases, byte-identical).
* `deadnames.py` / `unusedimports.py` — the two AST probes (read-only; they print, they do not
  write).
