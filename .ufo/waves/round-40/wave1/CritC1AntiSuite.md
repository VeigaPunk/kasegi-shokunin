# CritC1AntiSuite — round 40 wave 1 receipt (adversarial pre-build review)

Seat: `CritC1AntiSuite` (leaf; no subagents). Item: adversarial pre-build review of
the C1 counter (H1–H10) — enumerate concrete forgery tricks that must fail under
H1–H10, name the H-check that must stop each, and specify the graded selftest
mutant that must prove it. Axes touched: **depth:verifiability** (primary),
**coverage** (Count table only). No claim is authored, edited, judged or shipped
by this seat.

## Deliverable

- `CritC1AntiSuite.txt` (285 lines, 20 264 bytes, sha256
  `948ad9da20d7200e0f15d24031397033827ae9ed9791e26f06fefa16a1eee8dd`), landed at
  `.ufo/waves/round-40/wave1/CritC1AntiSuite.txt`.
- Content: §1 trick→check→mutant table (11 attack classes, 45 named mutants);
  §2 per-attack detail (attack, must-stop check, selftest mutant fixture +
  needle); §3 ExecSuiteBuild coverage checklist with minimum per-check set sizes
  and the freeze-gap note. The memo states that `ExecSuiteBuild` must not be
  considered done until every name in §3 is covered by a committed mutant.

## Inputs read (all read-only)

- `.ufo/waves/round-40/claims.json` (frozen) — C1 predicate/kill-rule/counting
  commands (`closed=10/10`, 10 graded `selftest case=H<n>` lines, base/r39-head
  reds, plain-run exit 2, H1–H10 definitions); C2 predicate; `judged_head_rule`.
- `.ufo/waves/round-40/c1-controls/before.txt` — R2/R5/R6 open, G2/G6 flaws
  standing, r39-l1 scratch leftover removed at round start.
- `.ufo/waves/round-40/c2-controls/before.txt`, `junk-decisions.md`, `census-before.txt` — C2 context (not operated on).
- `corpus/lessons/round-39-verifier-spotcheck.md` — R1–R7 routed defects
  (R1 attempt-1 future-dated forged receipt; R2 unmarked C1 overstatement; R4
  scratch survivor; R5 M39-2 criterion; R6 Gate rows lack URL/date/quote; R7 G2/
  G6 instrument findings).
- `corpus/lessons/round-39.md` — Mistakes M39-1..4; Gate rows for S056/S058/S059
  (currently reason+flip only, no URL/date/quote — R6); final measurement J1
  (`closed=7/8 exit=1`, selftest `failures=1`).
- `.ufo/waves/round-39/wave2/CritG2Exploit.md` — G2 shape-only parsing (F2 empty
  payloads/`mutants=0/0`/missing `mutants=`; F3 duplicate-id unobservable; F4
  indented ninth case invisible; F5 self-naming `export-ref`).
- `.ufo/waves/round-39/wave2/CritC1Kill.md` — G6 live-scratch dependence
  (default-root reds; exact-name-only scan, `kasegi-r39` only; R4), G8 pinned-r37
  live-worktree reads, K1–K6.
- `corpus/instruments/r39-closure.sh` (1793 lines) — header docs, `parse_args`,
  `make_work`, `prepare_export` (`git archive | tar -xf`; `rev-parse
  --verify ${want}^{commit}` accepts ref aliases/short hashes), `g1_path_safe`
  (existing path-safety precedent), `g2_graded`, `check_g6` (exact-name scan;
  realpath-based work-tolerance), `run_suite_report`, `judge_selftest_report`,
  selftest fixture machinery (`st_neg`, `st_verdict`, `g*_fixture`, `cases=`
  knobs), documented limits (G2 payload-value comparison "is not a limb").
- `corpus/QUALITY.md` — R32/R33/R34/R35/R36 append-only structure; M39-2 has no
  citing criterion (H3 target); R36 = the captured-by closure precedent.

## Findings (condensed; full memo in the deliverable)

1. Six named tricks mapped: verbatim cross-ref receipt → H7 (+H5)
   (`cases=receipt-cross-ref`); plausible-but-wrong payloads → H5 (5 mutants);
   injected/future-dated `run-utc` → H5+H7 (4 mutants); summary-only satisfying a
   graded case → H5 grading semantics (7 mutants); stray scratch under unrelated
   name → H6 (5 mutants + control); export path traversal → extraction guard,
   folded into H5 (3 mutants) + ref-validation mutants (3).
2. Live-lane-read class → every H-content limb; the dual-state fixture
   (`cases=live-lane-read` per check) pins it: fixture lane checked out at a
   different commit than the export ref with one differing byte.
3. Additional classes beyond the named six: receipt absent/renamed/extra (T8);
   suite-sha256 self-binding forgery (T9); declared-blocks gaming (T10, 6
   mutants); no-harm gaming (T11, 3 mutants: in-place edit preserving line count,
   deleted path, density instrument change).
4. Freeze-gap: T6 (export path traversal / ref resolution) is not enumerated in
   H1–H10 as frozen; it is mandatory harness hygiene and this memo folds it into
   H5's case set so it appears in the graded count. If the judge wants an
   eleventh check, `CHECK_IDS` and the frozen `closed=10/10` count would need an
   erratum.
5. H7 determinism requirements: one invocation, one clock, atomic tee (tmp +
   rename) after run completion, identical re-run args; a `tolerated=`/deviation
   line that varies between runs is a defect, not grounds to relax byte
   comparison.
6. H8's graded case must prove base/r39-head reds are genuine (same red limbs as
   the real negative controls), not a vacuous short-circuit.

## Controls / hygiene

- Disk guard green before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku` 26% (600.6G free).
- No tool installed or upgraded (no pacman — paused host-wide; no uv/npx needed;
  no network). No git/jj mutation anywhere. Fleet root and lane untouched except
  the two wave1 files.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/CritC1AntiSuite` removed before
  yield (deliverable copied to wave1 first), `trap 'rm -rf -- "$S"' EXIT` in
  effect. No `kasegi-r40*` sibling survives from this seat at filing.

Report: .ufo/waves/round-40/wave1/CritC1AntiSuite.md
