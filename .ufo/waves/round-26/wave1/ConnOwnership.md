# Round 26 wave 1 ownership preflight

The detailed path matrix is in `c4-ownership.txt` in this directory. It maps concrete outputs to their sole assigned seats using the wave1-spec prompts, distinguishes read-only scouts from production writers, and asserts disjoint ownership at concrete-file granularity. The requested production files, snapshots, controls, and per-seat reports have a single owner each; directory globs are not treated as blanket write authorization.

## Findings

- The seat labels in the assignment are abbreviated/inconsistent with the actual spec: there are eight executor seats (e1–e8), not e1–e9; no e9 appears in wave1-spec.json or dispatch registry. The matrix covers all actual executor seats and does not invent an e9.
- s2's S040 capture is its explicit write exception; s4 and s5 are read-only on production assets. s3 is also a read-only scout and owns only its inventory report.
- The matrix separates overlapping abstract globs into per-seat concrete reports and restricts m1/m2/m3 to their named control receipts. m3 has one named receipt under each control directory.
- No production changes or tool installation were made. Ownership conclusions are based on the frozen wave specification/dispatch materials; runtime scope compliance remains an end-of-wave check for the sentinel.

Report: `.ufo/waves/round-26/wave1/c4-ownership.txt`
