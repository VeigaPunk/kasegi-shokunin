# R44Review5 — C1 routed defect 5

## Findings

- **Registry `names=` defect remains evidenced in committed round-43 artifact.** `git show HEAD:.ufo/waves/round-43/w1-REGISTRY.txt` prints `counts={"spawn": 73, "resume": 0, "total": 73}`, `seats=73`, and final `names=` with no values. Roles and seat totals are populated but the advertised names inventory is empty. This is a concrete traceability failure, not proof that seats were absent.
- **Missing export-ref is confirmed in committed selftest transcript.** `git show HEAD:.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt` contains J1–J13 case records and `selftest cases=13 failures=3`, but no `export-ref` or `de09313` identity token. Its case text alone cannot establish which exported revision the transcript tested.
- **Aborted temp has no current closure residue at this working tree.** `git status --short -- .ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp` returned empty; filesystem test returned `absent`. This is consistent with removal, but not sufficient to prove safe lane-helper deletion or committed deletion: the original reported `.tmp` was untracked and its prior content/path history is not represented by a commit. Do not claim a specific cleanup mechanism from this evidence.

## Do-nothing discrimination / limitations

Frozen control `.ufo/waves/round-44/controls/do-nothing.txt` lines 1–2 fixes the base at `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; the round-43 spot-check §6 lines 97–105 routes all three hygiene issues. The current committed round-43 artifacts above still exhibit the first two defects, so do-nothing cannot satisfy the routed item. The absent temp alone is not credit for a verified remediation. This audit did not execute or validate a round-44 emitter/helper or any cleanup workflow, and did not inspect an L1 closure record; therefore safe closure remains unproven.

No tools installed or updated.