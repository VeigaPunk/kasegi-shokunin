# ExecSkillRegistry — round 26, wave 1 (build)

Seat: `L1Kasegi26.ExecSkillRegistry` (executor). Lane base revision `1b076fa7f2fb5e7dd9d87449514eba526043421b` (claims freeze commit). Access: 2026-10-25 (UTC). Axes: depth:verifiability (C1).

## Scope

Sole owner of `SKILL.md` edits this round. Task: add a `## Gates & probes registry` section with an 8-column table and ONE row for `recheck-audit.py`, plus one sentence noting the expected-list contract (deletion = red audit). No other section touched.

## Files changed

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md` — only file changed; `git diff --stat`: 1 file changed, 9 insertions(+), 0 deletions(-). (Pre-edit `git status --porcelain -- SKILL.md` was empty.)

## Placement

Inserted immediately before `## Cited paths` (the trailing reference block), i.e. after the entire operational body — the checklists/instruments/gates material (Program-rule checklist, Ops integrity layer, Evidence-package anatomy, Triage economics, etc.) — and before the final reference sections (`## Cited paths` + `## Frontier decision table (round 22)`). This satisfies "after the instruments/checklists area, before the final tables".

## Diff lines added (verbatim)

```
+## Gates & probes registry
+
+| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
+|---|---|---|---|---|---|---|---|
+| recheck-audit.py | gate|probe | python3 corpus/instruments/recheck-audit.py [--json <out>] | 0 clean \| 1 failed \| undeclared nonzero -> could-not-evaluate | python3 corpus/instruments/recheck-audit.py --selftest | .ufo/waves/round-26/c1-receipt-index.txt | corpus/ read-only + its own receipt dir | kasegi |
+
+The audit is stateful against the committed expected list (the pinned receipt index): the present knowledge-entry set is compared to it, so deleting an entry is a red audit (exit 1 naming the missing entry), never a silent green pass.
```

(9 inserted lines including the separating blanks.)

## Retained evidence

- C1 registry-row counter, run from the lane root: `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → **1** (the row's type cell is the literal `gate|probe`, unescaped, as the counter requires).
- Self-test spelling in the row is exactly `--selftest` (verified against `corpus/instruments/recheck-audit.py` argparse: `--selftest`, action="store_true"; usage block `python3 corpus/instruments/recheck-audit.py --selftest`).
- Entry command matches the instrument's documented usage (`python3 corpus/instruments/recheck-audit.py [--json receipt.json]`).
- Verdict map matches the instrument's exit contract (`return 0 if ok else 1`; docstring: "Exit status: 0 when every line passes … 1 otherwise"). Escaped `\|` inside the verdict-map cell renders as literal pipes in one cell.
- Pinned-value path `.ufo/waves/round-26/c1-receipt-index.txt` is the C1(b) receipt index (owned by the ExecReceiptIndex seat; not created yet — not in this seat's scope).
- Expected-list sentence grounds the C1(d) contract (whole-entry deletion → audit exit 1 naming the missing entry; before: exit 0) and the round-25 completeness rule ("a deleted recheck line fails the audit instead of silently shrinking the set").

## Notes / risks

- The working-tree instrument does not yet implement the expected-list comparison (that is the ExecAuditFix/ExecExpectedList seats' work this wave). The registry row and sentence document the contracted behavior, not a claim that the current bytes already enforce it.
- The `gate|probe` type cell is intentionally unescaped to satisfy the frozen C1 counter regex; a strict markdown renderer therefore splits that one cell visually. This is the accepted trade for the judged counter.
- No tools installed/updated (none needed). No other lane/fleet files written. No git/VCS mutations performed (read-only git only).
