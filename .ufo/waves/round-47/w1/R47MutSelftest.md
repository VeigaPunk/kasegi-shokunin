# R47MutSelftest — mutation test of the round-47 counter selftest's fixture builders

- Seat: `R47MutSelftest` (round 47, wave 1, mutation-tester). Date: 2026-10-30.
- Target under test: `corpus/instruments/r47-counters-selftest.py` (kasegi lane repo).
- Target bytes: sha256 `4c7c0aab5b5eb3885965bd9e0ec3c1b8ddda7f3f393af6a3863c6eeea6347ec4`;
  byte-identical to freeze commit `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`
  (`git diff --stat 308a2cb… -- corpus/instruments/r47-counters-selftest.py` empty) and clean at lane HEAD `82a8bd7`
  (`git status --porcelain` on the file: empty).
- Axes: depth:verifiability (hash-pinned pristine/mutated/restored protocol) + coverage (can a broken builder read green?).
- Tools installed: none (stdlib python3 only). Pacman pause respected; no installs, no service restarts.

## Question

Can a fixture-builder mutation produce a fixture tree that reads green but carries a defect, without the
selftest's own assertions noticing? Detection criterion per tasking: selftest reports `failures >= 1`.

## Protocol (pristine → mutated → restored)

Per mutation-tester role: the lane source was never modified. All mutations were applied to separate scratch
copies under `/fast/scratch/hyaku/kasegi-r47/R47MutSelftest/` (removed before this report; receipts preserved in
`R47MutSelftest.draft/`). Detector = the selftest itself, run from each (pristine or mutated) instruments copy
against the pure base export `git archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus`; the counters it
drives are the committed `r47-routed-defects.py` (sha256 `e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee`)
and `r47-f30-gate.py` (sha256 `563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b`) from the same
pristine copy — the builders are the only mutated component in every run. Per KNOWN LIMITS the full 56-mutant
counter battery was NOT rerun; the 34 disclosed survivors are out of scope here and no equivalence claim is made.

Baseline (pristine bytes): `selftest cases=43 failures=0 exit=0` — `R47MutSelftest.draft/baseline.out` (10.3 s).
This is the do-nothing control for the harness; a baseline failure would have made every verdict inconclusive.

## Control (comment-only mutation) — PASS, no signal

- Site `:61-62`: inert comment line added after the builders header (`mutctl.diff`).
- Mutated sha256 `93d44160951f41a693a4177d34e6e21d1e155659a27f0703a8655d41de984688`.
- Output: `selftest cases=43 failures=0 exit=0` (`ctl.out`) — identical to baseline.
- Function: proves the four kills below are caused by builder behavior changes, not by running from a scratch
  copy, work-dir placement, or harness noise.

## Mutants — 4/4 KILLED, 0 survived, 0 inconclusive

| id | site (source :line) | builder mutation | expected detector | actual output | verdict |
|----|---------------------|------------------|-------------------|---------------|---------|
| M1 | `build_c1_green` :220 | skips the F29 entry fix (base false sentences stay) | c1-green case fails: green tree carries the D6 defect | `case c1-green ok=0 want=routed-defects total=11 fixed=11 unresolved=0 exit=0 got=routed-defects total=11 fixed=7 unresolved=4 exit=1`; `selftest cases=20 failures=1 exit=1` | killed |
| M2 | `mut_manifest_fewquotes` :438 | c2-fewquotes defect tree self-heals (`[:3]`→`[:10]`, all ten quotes kept) | c2-fewquotes case fails: defect tree reads green | `case c2-fewquotes ok=0 want=H4 red + exit!=0 got=f30-gate fixed=7/7 exit=0`; `selftest cases=23 failures=1 exit=1` | killed |
| M3 | `c1_defects` :247 | c1-s1left defect tree self-heals (mutator replaced by no-op) | c1-s1left case fails: defect tree reads green | `case c1-s1left ok=0 want=L1 red + exit!=0 got=routed-defects total=11 fixed=11 unresolved=0 exit=0`; `selftest cases=20 failures=1 exit=1` | killed |
| M4 | `build_c2_green` :330 | green F30 frontier row lands with status `queued` instead of `admitted` (green-but-defective row) | c2-green case fails | `case c2-green ok=0 want=f30-gate fixed=7/7 exit=0 got=f30-gate fixed=6/7 exit=1`; `selftest cases=23 failures=1 exit=1` | killed |

All runs exit 1 with `failures >= 1`; each kill is assertion-caught (no harness crash, no traceback). Full
outputs: `R47MutSelftest.draft/mut{1,2,3,4}.out`; exact byte-level diffs: `mut{1,2,3,4}.diff`.

Mutated selftest sha256s (scratch copies, never propagated):
- M1 `90446661a601b99925418488725925ff23f3923f75baeb11cb139f7d80df0406`
- M2 `2712da71f554396de290b86469bc1fe82e7af59ba20287900f6bbce8081f6f5e`
- M3 `b924fa281b54067f20b80598e25ee5a620a8d10ab72f207d779a279e380dd3fe`
- M4 `08ff9409787a2522eec231efdb81cb5149716502e464d293fa5f52ec47078653`

## Restoration evidence

- Lane source sha256 before all work == after all work: `4c7c0aab…347ec4`; `git status --porcelain` on the file
  empty before and after; no commit, push, index, or worktree mutation anywhere (only read-only
  `git archive` / `git diff` / `git rev-parse` / `git status`).
- The pristine `instr/` scratch copy (the only copy the control and baseline ran from) was never edited:
  hash `4c7c0aab…` re-verified post-run. Mutants lived in separate `mut1..4`, `mutctl` dirs and were never
  copied back. Wave-1 rule "restore exact bytes" satisfied trivially: nothing shared was ever mutated.

## Coverage findings (not defects; for wave 2 / L1 information)

1. **Fix-omission detection rests entirely on the green case.** Under M1, all 19 c1 per-limb defect cases still
   pass (`ok=1`): each asserts only `rc != 0 and limb_red(...)` (`:509`, `:525`) on its own limb, and inherited
   defects keep every individual limb red. The single point that catches "a fix was skipped" is the exact-string
   green summary comparison (`:500`, `:515`). That line is sound (exact match, not a substring), but any future
   refactor that loosens it would silently open the whole fix-omission class.
2. **Defect-case verdicts cannot distinguish "limb red" from "counter crash".** `ok = rc != 0 and limb_red(...)`
   (`:509`, `:525`): a counter that exits nonzero with a traceback (no `limb`/`gate` lines) satisfies both
   clauses — `limb_red` returns True because the expected pass-line is absent. Run-level detection still fires
   via the green case (built and run first, same gate), so a counter mutant that is green on green trees but
   crashes on defect trees would read `failures=0` — a plausible survivor shape for the wave-2 counter-mutant
   battery. Code-grounded observation only; I did not mutation-test it (counter mutants are mutbat's lane, and
   the battery rerun is out of my scope per KNOWN LIMITS).
3. **M4 design note:** mutating the row-insertion statement out of `build_c2_green` (rather than a cell value)
   would crash downstream defect-builders (`[ln for ln in ... if ln.startswith("| F30 |")][0]` → IndexError)
   before the verdict pass — a loud but non-assertion detection. The committed defect-case builder family is
   structurally dependent on the green builder succeeding; a builder mutation can therefore also manifest as a
   harness crash rather than `failures >= 1`. M4 was deliberately shaped as a cell-value defect to stay inside
   the assertion-catch criterion.

## Limitations

- Bounded per-seat probe: 4 builder mutants + 1 inert control, as tasked. Untested builder surface remains:
  the S075/S076 snapshot copy loops, `LESSON46/47` writers, `entry29_fixed` (reads sibling
  `entry29-fixed-bytes.md`), `add_leads_bullet`, `edit_row_cells`, and the c2 README row-insert mechanics.
- No counter-source mutants were run here; the pre-freeze battery receipt (c1 35/19/16, c2 21/3/18,
  baseline_failures=0, 34 disclosed survivors) is cited as ground truth, not re-measured.
- Detector runs are fast (2.4–10.3 s each) but single-environment (this host, python3 `-I`); no cross-platform
  claim is made.

## Receipts

`.ufo/waves/round-47/w1/R47MutSelftest.draft/`: `baseline.out`, `ctl.out`, `mut1.diff`, `mut1.out`, `mut2.diff`,
`mut2.out`, `mut3.diff`, `mut3.out`, `mut4.diff`, `mut4.out`, `mutctl.diff`.
Scratch `/fast/scratch/hyaku/kasegi-r47/R47MutSelftest/` removed after receipt copy.
