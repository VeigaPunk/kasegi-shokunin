L1 correction delivered to the dispatched seats at 17:53 -03 (wave taken at 17:51:46).

MEASURED FACT: `wc -l big.txt missing.txt | head -n 1` (P10) is FLAKY at native level on this host. Five repeats gave stage0 = -13 five times in one pass; an earlier pass gave stage0 = 1. wc's per-file write races the downstream close, so its status is not stable.

Required handling (the wave payload's original text said "P10 -> rc0" at base and "P10 -> derive-upstream-signal-13" at candidate):
- Do NOT freeze a single reason for P10 and do NOT put P10 in the frozen repair set.
- Record five repeats with their native stage0 and the gate's verdict for each.
- The candidate must read stale for P10 under BOTH outcomes (derive-upstream-exit-1 or derive-upstream-signal-13); base reads green only in the runs where stage0 is -13.
- The frozen repairs are cut (P9) and grep (P11), both measured -13 on five of five repeats.

Receipts: .ufo/waves/round-67/controls/native-statuses-r67.txt (one pass, P10 = 1) and the L1 repeat probe (five passes, P10 = -13). Both are L1 evidence, not seat evidence.

## L1 base matrix (measured on production at base 8e2a8fe, receipt controls/base-matrix-r67.txt)

Production at base ALREADY carries round-66's cat repair, so cat multi-operand SIGPIPE is stale at base:

| probe | base verdict |
|---|---|
| P1, P2 | stale `derive-upstream-signal-13` |
| P5 | stale `derive-exit-1` |
| P15 | stale `derive-upstream-exit-1` |
| P3, P4, P6, P7, P8, P9, P10, P11, P12, P13, P14, P16, P17 | ok |
| P10 | FLAKY (green when native stage0 is -13; stale `derive-upstream-exit-1` when it is 1) |

Candidate (after the repair): P9 and P11 join P1/P2 as stale `derive-upstream-signal-13`; P10 stale under either outcome; every other row keeps its base verdict.
The wave payload's "P1/P2 base rc0" and "P8 candidate signal-13" lines are superseded by this measured matrix.
