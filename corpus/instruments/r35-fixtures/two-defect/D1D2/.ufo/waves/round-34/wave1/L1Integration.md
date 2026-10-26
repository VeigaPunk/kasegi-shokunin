# Round-34 L1 integration — fixture payload (not the lane receipt)

Committed test fixture for the C1 closure check D6. The live file is
`.ufo/waves/round-34/wave1/L1Integration.md` at the lane root; bytes here are pinned.

## Notes

- The round-33 regression battery is covered by the L1 re-run plus
  `wave1/ExecRDefectClosureSuite.md` §5 (base `closed=0/9`, exit 1) and the wave receipts.

<!-- limb D6 fixed: the stale dead-seat note is superseded, and the stale sentence is not quoted here -->
**Correction (round 35) — stale dead-seat note.** An earlier revision of this file said a round-33
summary seat had filed no receipt. That sentence was stale: `wave1/ExecRegressionC1.md` is committed
at `c1c6a5f` and this correction supersedes the stale note. The round-33 summary seat did file a
receipt.
