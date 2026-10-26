# Round 34 — mistakes erratum 1 (M34-3 / M34-5 / M34-6 minted)

Filed by the L1 (`KasegiR34a2`) on 2026-10-26, per the round-34 lesson rule:
the frozen claims (`.ufo/waves/round-34/claims.json`) own the M34 numbering, so
rows marked provisional in `corpus/lessons/round-34.md` become canonical only
through this separate appended file. Field schema is round 33's: class ·
evidence pointer · captured-by · fix · fix shown able to fail.

## M34-3 — a post-freeze counting-literal erratum was filed against a criterion that cannot see it

- **Class:** freeze satisfiability.
- **Evidence:** `claims-erratum-1.md` mtime `2026-10-26T02:36:22` vs the freeze
  commit `29f606d` (`02:28:39`, `+7m43s`, `sha256 6a3cd99e…`); the base and
  freeze audit surfaces are byte-identical (`git diff --stat 7963976e 014ee2d
  -- corpus/source-snapshots corpus/instruments corpus/SOURCES.md` prints
  nothing), so `records=40` was true at base and false at the declared after-state
  (`records=41` once C2's own S051 manifest record lands).
- **Captured by:** `none` at freeze time — `QUALITY.md` R22 (pre-freeze
  satisfiability) existed but had no planned-state limb; first spotted by
  `wave1/CritMistakes.md` F5 (R22-vs-erratum-1 pairing) and
  `wave1/ScoutDatawalk.md` F-4a (harness literal).
- **Fix:** `QUALITY.md:229` **R25** now requires literals to be checked against
  base bytes **plus the round's declared after-adds**; this round's C1/C2
  after-list literals were reconciled to the printed column truth
  (`records=41`; the `PASS F17 ids=S051` line exists column-padded as
  `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0`).
- **Fix shown able to fail:** base-only R22 accepts `records=40` (empty diff),
  while the planned-state reading rejects it (`records=41`); `grep -c 'PASS F17
  ids=S051'` on the harness output prints 0 while the F17 line is present.

## M34-5 — one receipt declares "no git/jj mutation" while its own `jj log` calls created working-copy snapshots

- **Class:** overstatement (M34-1's class).
- **Evidence:** `wave1/SentScopeFinal.md` §2 B2–B3: four `snapshot working copy`
  ops (`3038db8e52bc` `ScoutQuarantine`, `1c80be616d4b` `ScoutDatawalk-2`,
  `497fe0c449c0` `RevErrata`, `2d099a7898ec` `RevClaimsFreeze-2`), all lacking
  `--ignore-working-copy`; `wave1/RevErrata.md:12,153` deny any jj mutation.
- **Captured by:** `wave1/SentScopeFinal.md` (§2 B2–B3).
- **Fix:** seats use `jj --ignore-working-copy` for read-only jj ops, or no jj
  at all; recipients that claim "no mutation" name the op-log check they ran.
- **Fix shown able to fail:** `jj --ignore-working-copy op log` shows the four
  ops against the L1's own `snapshot.auto-track="none()"` operations, and the
  seat's two reads at +5 min returned the same top op `3038db8e52bc`, so the
  check is stable.

## M34-6 — one seat wrote outside its write scope twice, by relative-path resolution

- **Class:** write-scope drift.
- **Evidence:** `wave1/CritC1Kill.md` "Seat hygiene (self-reported defect,
  corrected)": its first receipt write resolved against the session workspace
  root and landed at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-34/wave1/`
  (fleet root), copied byte-identically (`sha256 ab80628c…`) into the lane and
  the stray deleted. Separate strays: `baseline-plain.txt` at the fleet root
  (`850 B`, `sha256 56f08a92…`) and `selftest-baseline.txt` at the lane root
  (`1552 B`, `sha256 ca3759d1…`), both from one seat command captured in
  `~/.omp/agent/sessions/…/RevKillRule.jsonl` and attributed by
  `wave1/SentScopeFinal.md` §1 A1.
- **Captured by:** `wave1/SentScopeFinal.md` (and `wave1/CritOverclaim.md` F4 /
  `wave1/RevC1BeforeAfter.md` F5 for the lane-root file).
- **Fix:** seats use absolute paths under their scratch root; the L1 sweeps and
  deletes both stray classes before the integration commit.
- **Fix shown able to fail:** before removal, `git -C /home/vgpnk/Projects/shokunin
  status --porcelain` listed `?? baseline-plain.txt` and
  `git ls-files --error-unmatch selftest-baseline.txt` failed (not tracked);
  both read 0/none after removal (observed at integration: neither file exists on
  disk).
