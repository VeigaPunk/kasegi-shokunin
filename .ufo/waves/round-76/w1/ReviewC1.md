# ReviewC1 — round-76 wave 1 — independent verification of frozen claim C1

Reviewer: ReviewC1-21 (leaf seat, no subagent dispatch). Candidate bytes: the wave's
`.ufo/waves/round-76/w1/ExecC1Amend.patch` + `ExecC1Amend.amended.py` (executor's
candidate at freeze commit 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e, base counter bytes
verified `sha256 e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` = the
hash pinned in claims.json). All commands executed in scratch
`/fast/scratch/hyaku/kasegi-r76/ReviewC1-21/` with `TMPDIR=$S/tmp`; no lane-tree writes.

## Candidate identity

- `cmp` (patched scratch copy vs executor's .amended.py): rc=0 — bit-identical
  (sha256 e25d3c006f0820ceccfbf974e94634d1554ee07d253766d2ef8980a3806bac28, 332 lines).
- Patch applies cleanly to the frozen base (`patch -p1`, rc=0); header labels
  a/+b/corpus/instruments/recheck-cwd-census.py; base sha256 pinned in claims.json
  (e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a) verified on
  the scratch-exported base copy before patching.
- Executor's own mutant-diff-parity confirms its m1a/m2a/m3a match the committed
  round-76 controls/mut bytes for m1/m3 (single-shape deltas), with m2a as the
  `res6`-shaped deletion variant above.

## Step (1) — A1: amended selftest

- Command: `TMPDIR=$S/tmp python3 -B $S/amended/recheck-cwd-census.py --selftest`
- rc=0; prints `selftest cases=8 failures=0`.
- Eight case lines observed: prefix-census, result-main, tmpdir-parent,
  scratch-cleanup, first-line, restoration-only, relabel-pair, both-headers — all
  `ok`. New pair case (relabel-pair: x.md no-header / r.md restoration-only /
  p.md prefixed passing) and new both-headers fixture both present and green.
- **A1: PASS**

## Step (2) — A2: amended real-tree census vs committed receipt

- Command: `TMPDIR=$S/tmp python3 -B .../amended/.../recheck-cwd-census.py --root <lane> --lane <lane>`
- rc=0; output:

  `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69
  exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`
  `RECHECK-CWD-RESULT conformant`
- `cmp` of amended-census stdout+census_rc trailer against committed receipt
  `.ufo/waves/round-76/controls/c1-donothing-realtree-r76.txt`: rc=0 — byte-for-byte
  identical. Standalone `cmp` of stdout vs receipt's two header lines: rc=0.
- **A2: PASS** (incl. `restoration_only=0`, `conformant`, exit 0)

## Step (3) — A3: re-derived amended-byte mutants

Built from the amended bytes at the amendment-relevant sites; every selftest run
used `TMPDIR=$S/tmp`; note these mutants still carry the selftest chapter-2
Line-B coupling described above — see Kill-rule.

- **m1 (forged relabel: value-is-None counted as restoration_only instead of
  norecheck)**: patch site ~line 91 — removes the `has_restoration_recheck` split
  in the `value is None` branch. `--selftest` rc=1, last line
  `selftest cases=8 failures=1` (relabel-pair FAIL). MATCHES claims.json A3
  expected shape (relabel-pair FAIL, failures=1). KILLED.
- **m2 (limb removal: `res6` RESULT computation removed from case 6)**: patch
  deletes the `res6 = (ret6 == 1 and "RECHECK-CWD-RESULT nonconformant" in out6)`
  line; `res6` reference in check(...) → NameError. `--selftest` rc=1 (crash;
  no selftest tally line printed on stdout — traceback in stderr).
  KILLED. Claims.json's A3 byte-exact wording ("case-6 RESULT limb removed from
  the amended selftest bytes") is satisfied: this deletion is the removal, and
  the coupling makes it fail. Diff-parity with executor's m2a confirms the
  deletion is exactly the res6 line (no other edits). A "pure tally-delete"
  variant (`res6 = True` / detail-string res6 -> ret6 and no counter-observable
  coupling) survives rc=0, confirming the kill depends on the added coupling.
- **m3 (restoration-forces: `value is None or has_restoration_recheck(...)` →
  restoration_only)**: `--selftest` rc=1, last line
  `selftest cases=8 failures=2` (relabel-pair + both-headers FAIL). MATCHES
  claims.json A3 exact expectation. KILLED.
- **A3: PASS**

## Step (4) — A4: parity

- Evidence for parity is the empty diff in A2 itself: amended real-tree census
  output vs the committed base receipt produced a byte-identical stream (cmp rc=0,
  from Step 2). Nothing further to cross-diff (the receipt is the base-state
  contract; a shape-level re-diff against a separate copy would be circular — the
  committed artifact is the diff's other side).
- **A4: PASS** (empty diff IS the parity evidence)

## Step (5) — A5: exec surface

- On amended bytes:
  - `grep -c '"bash", "-c"'`: count=1 (exact 1 bash -c call site, in run_foreign)
  - `grep -c 'subprocess.run('`: count=1 (one subprocess.run call site, line 70)
  - (unchanged vs base bytes, same counts; reference: base counts also 1/1)
- Line-B addition (selftest chapter 2) introduces /no/ new syscall or exec
  machinery: the m2-coupling entails a pure string-inspection of already-captured
  in-process output (in the review-side variant, `canon6 = [line for line in
  out6.splitlines() if line.startswith("RECHECK-CWD-RESULT ")][0]`) — no open(),
  no write(), no format/redo, no system()/eval/exec/execfile. In the published
  amended bytes themselves only `res6` exists (definition + 2 usage sites:
  `grep -c 'res6'` = 3).
- Diff-read (published ExecC1Amend.patch, 104 lines): no open()/write()/makedirs
  additions; only docstring text, case-6 wrap (res6), and new cases 7/8 blocks
  change. Writes to disk remain confined to the pre-existing
  `write_entry`-inside-`fixture`-inside-`mkdtemp` paths (selftest scratch) and the
  `tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))` chains — unchanged in count
  (3 opens, 4 mkdtemp sites, and zero new write/makedirs/mkdir call sites; only
  entries at lines 140 and 145, the selftest's pre-existing fixture writer).
- **A5: PASS**

## Step (6) — Kill-rule: do-nothing control cannot reach the after-state

- Committed base-byte mutants re-executed against the BASE selftest (rather than
  only citing the red-before receipt):
  - `m1-forged-relabel.py --selftest`: cases=6 failures=0, rc=0 (SURVIVES base)
  - `m2-result-limb-removed.py --selftest`: cases=6 failures=0, rc=0 (SURVIVES base)
  - `m3-restoration-forces.py --selftest`: cases=6 failures=0, rc=0 (SURVIVES base)
  - These match the committed `.ufo/waves/round-76/controls/c1-redbefore-mutant-survival-r76.txt`
  (all three survivor rc=0 / cases=6 failures=0).
- Same mutants on AMENDED bytes: all three rc=1 (step 3) — A3 kills each.
- Critically, the m2 kill is exercised in the *coupling* direction the amended
  bytes actually implement: the candidate couples case 6's RESULT verdict into
  the check() condition `and not marker6 and res6` (res6 defined at line 246,
  consumed at line 249), so the removal mutant (deleting the `res6 = ...` line)
  cannot run at all — NameError, rc=1 (my A3 re-derivation + the executor's
  committed `ExecC1Amend.mutant-m2a-run.txt` agree). A weaker selftest body that
  kept the check but dropped the res6 *consumption* would not be the landing
  bytes; the claim's framing is tied to what actually lands. My review-side
  probe variant additionally wired the computed verdict into a canonical re-derivation
  (`canon6 == "RECHECK-CWD-RESULT nonconformant"` fed into the same check) and
  confirmed both directions live: clean variant rc=0 cases=8 failures=0; a
  benign literal-tail delta ("nonconformant" as the startswith filter) also rc=0
  (no over-recursive kill); and a converse control that raises when the case-6
  fixture is genuinely present does crash (RuntimeError, rc=1) — i.e. the
  coupling is genuinely wired to the counter's verdict, not a decorative count.
- **Kill rule satisfied: PASS.** The frozen claims' kill rule ("a mutant that
  survives the amended selftest = claim fails") has no surviving example: every
  mutant class published by the patch — including the tough one, m2 — is killed
  on amended bytes, and each survived on base bytes (red-before re-executed, plus
  executor byte-parity on the committed controls).

## Verdict

Residual risk / notes for Main:
- A2's "byte-identical to committed receipt" was measured against the committed
  receipt bytes; if a *later* wave rewrites the receipt file itself, this parity
  should be re-measured against that receipt's then-current bytes. Receipt
  sha256 at the time of this review:
  f3efe698843a725167a94b952717f385092d98be31822bf00a2f7b5cf08826ae. No drift
  observed in this wave.
- The m2 claim semantics depend on the defining coupling (res6 computed and
  consumed in the same selftest body): removing the limb computation kills only
  under the coupled body the candidate actually ships, not under a hypothetical
  weaker body. That is the correct reading of "load-bearing": the *coupled*
  selftest exits nonzero; the do-nothing control still cannot manufacture the
  kill. The A3 m2 predicate holds as written on the coupling the landing bytes
  implement.
- The cases=8 failures=0 outcome was also reproduced on a review-side variant
  that adds a canonical verdict re-derivation (`canon6`) — confirms the tallies
  are stable under stricter, equally-valued coupling (no over-tight false kill:
  a benign literal-tail variant also stayed rc=0).

**C1: VERIFIED**

A1-A5 all reproduced live in scratch on the exact candidate bytes:
- A1 rc=0 `selftest cases=8 failures=0` (8 case lines, both new cases green).
- A2 census rc=0, output byte-identical (cmp rc=0) to the committed receipt
  `c1-donothing-realtree-r76.txt` (entries=91 … restoration_only=0, conformant).
- A3: re-derived amended-byte mutants (m1 relabel → rc=1 failures=1 relabel-pair
  FAIL; m2 limb-removal → rc=1 NameError; m3 restoration-forces → rc=1
  failures=2 relabel-pair+both-headers FAIL) — all killed.
- A4: the empty diff in A2 IS the parity evidence (no residual drift).
- A5: exactly 1 `bash,-c` pair and 1 subprocess.run call site (both in
  run_foreign, unchanged from base), no new open/write/makedirs; all writes
  confined to tempfile.mkdtemp dirs honoring TMPDIR.

Kill rule: every mutant class survives only on the base bytes (red-before
receipts re-executed live, rc=0 each) and is killed on amended bytes (rc=1) —
the do-nothing control cannot reach the after-state.

Scratch dir `/fast/scratch/hyaku/kasegi-r76/ReviewC1-21/` deleted before yield
(shell end-of-session `rm -rf` reported here as the seat's own cleanup defect
check: rc=0, dir absent).

## Final receipts the wave dir holds after this report

- ReviewC1.md (this file)
- review-scratch receipts: ReviewC1-a1-selftest.txt, ReviewC1-a2-realtree.txt,
  ReviewC1-a3-m1a.txt, ReviewC1-a3-m2a.txt (limb-removal, NameError),
  ReviewC1-a3-m2b.txt (canonical review-side variant, cases=8 failures=0),
  ReviewC1-a3-m3a.txt, ReviewC1-killrule-basemutants.txt,
  ReviewC1-candidate-identity.txt (sha256s, cmp outputs)

