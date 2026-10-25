# ScribeLesson — round 29 wave 1 (final lesson receipt)

- Seat: `ScribeLesson` (scribe, leaf; no subagent dispatch). Round: kasegi-shokunin 29, wave 1.
- Answering model: `inception/mercury-3` (config route table; no model passed by this seat).
- Date: 2026-10-25. Lane base `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims freeze
  `f28ff5d26b29270f93163117e7255e24f0b1d947`; dispatch HEAD `46e07f6ae8f23debb10034164252e7027b4d9091`.
- Assigned deliverable: `corpus/lessons/round-29.md` (final lesson, assembled after the scribe
  sections and canonical receipts landed).

## File receipt

| item | value |
|---|---|
| lesson file | `corpus/lessons/round-29.md` |
| sha256 | `78ae8080fc3653b2f7291df7fd229ff4aeccc9965db2042c1825ca1f5aa52f5b` |
| lines | 263 |

- `## Frozen claims` — before/after with measured values and seat digests: C1 (instrument
  `23818c1204…` → `68e1bdc6…`; selftest 9/0 → `cases=12 failures=0`, `limbs=9 covered=9`;
  nogit exit 1 traceback → exit 0 clean skip; SKILL no-harm 7/0/306 unchanged; `c1-receipt-index.txt`
  digest line present), C2 (frontier 12→13; entries citing S04[3-5] 0→1; rows 0→3; registry
  42→45; census exit 0; harness 15/15→16/16; rechecks exit 0 each; frozen manifest `910608e6…`
  — all 12 assertions exactly-once (stems==ids; S043 anchors 31/40/170/92 verified; mid-wave
  `79b32d50` occurrences=12 state resolved by the record-scoped S043 re-capture `d3b815ed…`),
  claimed; verdict classes unmoved).
- `## Gate` — assimilation set, by-document id map (S031→S043/S032→S044/S033→S045), collision
  list + guard proof, quarantine slice 7-row verdicts (none adopted), admits, rejects with flip
  conditions, and the **spot-check result**: non-author reviewer `RevC2Entry` re-opened the admit
  (partial agree — Q8/Q10 stand) and a refusal (agree — Q4 universalization).
- `## Mistakes` — nine rows, each with class · evidence pointer · captured-by · fix (M29-1…M29-9).
- `## Registry changes` — S043/S044/S045 old→new cells; S041/S042 untouched.
- `## considerthese` — proposal 5 mined → `QUALITY.md` R15 (citing `considerthese/2026-10-25.md`,
  2026-10-25); proposals-status ledger.
- `## Compliance` — freeze discipline, ownership, census before/after (45 rows), scope/safety,
  tooling, close-out ledger (post-integration recheck, C2 occurrence-limb decision, scorecard,
  final swept).

## Known limits of this receipt

- All after values are measured at the landed **working-tree bytes**; the integration commit had
  not landed at assembly. `ExecPostCommitRecheck` re-verifies at the commit (owed).
- The C2 kill-rule clause "any manifest assertion not occurrences=1" is satisfied at the frozen
  bytes (`910608e6…`: 12/12 exactly-once); the mid-wave `79b32d50` state that tripped it, and the
  still-uncommitted Q9 reader (M29-3), are recorded as defects rather than hidden.
- Writes by this seat: `corpus/lessons/round-29.md` and this receipt only. No tool installed; no
  pacman transaction; no git/jj commands.
