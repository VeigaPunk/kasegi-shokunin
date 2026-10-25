# Round-28 claims erratum 1 (appended, never an in-place edit; R25-1, R9)

Filed by L1 after ExecInstrReadme's non-reproduction report (verified by the L1
against committed bytes). Frozen `claims.json` is unchanged; this note corrects
one cell in it.

## What does not reproduce

`claims.json` C1 `corpus_disclosure` asserted: "after the CITE bounties arm, 4
corpus marked bounties citations (claim-gates.md, intake-and-finalize.md,
mission-control.md, source-tree-loss-2026-09-28.md) newly classify
LOST-RECORDED instead of being silently skipped".

Observed truth (ExecInstrReadme scratch CITE-arm probe + L1 verification):

- The 4 named citations are `source:` header lines in appended `## Provenance`
  blocks (e.g. `corpus/knowledge/claim-gates.md:123`), written as plain text
  without backticks around the `[lost-tree] ~/Projects/bounties/...:NN` token.
  `TOK` extracts only backticked spans, so CITE never reaches these lines —
  before AND after the arm they are invisible to anchorcheck.
- A corpus+SKILL sweep for backticked anchored bounties citations
  (`` `[lost-base|lost-tree] ~/Projects/bounties/...:NN` ``) returns **0 hits**
  (`grep -rno '`\[lost-\(base\|tree\)\] ~/Projects/bounties/[^`]*:[0-9][0-9]*`' corpus/ SKILL.md | wc -l` → 0).
- ExecInstrReadme's scratch run of the CITE-arm instrument over 43 corpus files
  shows **0 LOST-RECORDED movement**.

## Correction

The disclosure cell is superseded by: **after the CITE bounties arm lands,
there are zero backticked anchored `~/Projects/bounties/` citations anywhere in
the lane tree; no verdict-class count moves on any file, corpus or SKILL.md.**
This is a *stronger* no-harm result than the frozen cell asserted — the arm is
strictly invisible to all existing bytes. The 4 named provenance headers remain
documentation of record, never anchorcheck-verified citations.

## Effect on the claim

- C1 counters (a)–(d) are unchanged; the disclosure cell was evidence
  annotation, not a counter.
- No axis is harmed; the correction strengthens the no-harm evidence.
- ScribeSkillGate's SKILL.md note must read "zero backticked anchored bounties
  citations exist; no verdict-class movement anywhere" (steered directly).

Evidence pointers: ExecInstrReadme seat report, L1 grep receipts in
`.ufo/waves/round-28/receipts/` at close.

## Erratum 2 — selftest isolation (2026-10-25)

`CritC1Kill.md` found that the `pin-broken` selftest inherited `GIT_DIR` and could
resolve a deliberately missing blob from the caller's repository. The L1
reproduced the failure before the fix:

```text
GIT_DIR="<temp-repo>/.git" python3 corpus/instruments/anchorcheck.py --selftest
selftest FAIL pin-broken: PIN-BROKEN: want 1, got 0; IN-RANGE: want 0, got 1; exit: want 1, got 0
selftest cases=9 failures=1
```

The fixture runner now removes inherited `GIT_*` variables from each child
environment before setting its isolated roots. After the fix, the same
perturbation prints `selftest cases=9 failures=0`, exit 0. This corrects the
selftest's isolation implementation; the frozen predicate/counter is unchanged.
The final landed digest and outputs are in the canonical receipt and final
round lesson.

## Erratum 3 — disclosure scan scope

Erratum 1's phrase "zero backticked anchored bounties citations anywhere in the
lane tree" was too broad after the C1 selftest implementation added literal
fixture strings to `anchorcheck.py`. Correct scope: **zero such tokens in the
Markdown files that anchorcheck is measured against** (`SKILL.md`, `corpus/*.md`,
`corpus/knowledge/*.md`, `corpus/lessons/*.md`). Python test-fixture literals
are source code, not Markdown inputs scanned by `TOK`; they do not affect the
four named corpus files or the SKILL.md no-harm measurement. The no-movement
claim is therefore scoped to anchorcheck's actual Markdown input surface,
not every file type in the repository.
