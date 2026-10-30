# R47MutC1b — C1 set B mutation probe: limbs L7–L11, six fresh counter mutants

Lane kasegi round 47, wave 1. Frozen bytes only: every fixture, instrument and
detector run in this probe used scratch copies of the freeze-commit corpus
export (`git -C <lane> archive 308a2cb2 corpus`), verified against the freeze
record before and after. Lane repo read-only throughout; no git/jj command ran
anywhere except read-only `git archive`. No tools installed (nothing needed).
All receipts: `R47MutC1b.draft/` beside this file.

## Target

`corpus/instruments/r47-routed-defects.py` (sha256
`e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee`, equal in
lane working tree, freeze export, and `freeze.txt` pin). Limbs L7 (lesson-token
erratum, :226-230), L8 (S076 row + manifest pin + recheck, :241-273), L9
(re-anchored span locator + body bounds + uncited floor, :276-297), L10 (leads
bullet, :299-308), L11 (ZDI reservation + S068 precision, :310-318). Detector:
`r47-counters-selftest.py --counter c1` (sha
`4c7c0aab5b5eb3885965bd9e0ec3c1b8ddda7f3f393af6a3863c6eeea6347ec4`), graded by
the `r47-mutbat.py` rule: caught ⇔ selftest failures>0 under the mutant while
pristine failures=0. Six fresh single-edit mutants, none duplicating a
`C1_MUTANTS` id or old→new pair in `r47-mutbat.py:53-88`.

## Baseline and do-nothing control (all clean)

- Pristine detector run 3× on the 20-tree c1 fixture set: `selftest cases=20
  failures=0 exit=0` each; run 1 and run 2 stdout line-identical
  (`receipt.json: pristine_run1/2/3, pristine_stdout_identical`).
  `R47MutC1b.draft/pristine-{1,2,3}.txt`.
- Pristine counter on base export fc8e0af: `routed-defects total=11 fixed=0
  unresolved=11 exit=1` = claims `expect_before`. `counter-base.txt`.
- Pristine counter on freeze export 308a2cb: same summary — confirms claims
  C1 `freeze_tree_reading`. `counter-freeze.txt`.
- Pristine counter on the selftest's kept green tree:
  `routed-defects total=11 fixed=11 unresolved=0 exit=0` = claimed target state
  is reachable on the committed builders. `counter-green-pristine.txt`.
- All six mutants on green/base/freeze read 11/11, 0/11, 0/11 exactly as
  pristine (`receipt.json: mutants[].trees`) — the survivors diverge only on
  defect-shaped trees, i.e. they are false-green-class mutations.

## Mutants and verdicts

| id | edit (counter line) | verdict | evidence |
|---|---|---|---|
| L7d-lesson46-dropped | `for rel in (LESSON47, LESSON46):` → `for rel in (LESSON47,):` (:227) | **uncaught** (failures=0) | T-L7d demonstration below; `mut-L7d-…txt` |
| L8e-manifest-pin-dropped | manifest pin `… or sha(open(man,"rb").read()) != MAN_SHA:` → `if not os.path.isfile(man):` (:260) | **caught** (failures=1, case `c1-maninert ok=0 got=… fixed=11 … exit=0`) | `failing-cases.txt`, `div-c1-maninert-*.txt` |
| L9d-body-bounds-off-by-one | `rng[0] <= a <= b <= rng[1]` → `rng[0] - 1 <= a <= b <= rng[1] + 1` (:291) | **uncaught** (failures=0) | T-L9d low/high demonstrations below |
| L9e-uncited-masked | `ok = failed == 0 and uncited <= 0 and passed >= 20` → drops `uncited <= 0` (:296) | **caught** (failures=1, case `c1-nocite ok=0 got=… fixed=11 … exit=0`) | `failing-cases.txt`, `div-c1-nocite-*.txt` |
| L10d-lead-anywhere | `leads = section(raw, "Leads (unopened)")` → `leads = raw` (:302) | **uncaught** (failures=0) | T-L10d demonstration below |
| L11d-precision-phrase-wide | `b = "S068" in t and "one GHSA advisory entry" in t` → `b = "S068" in t and "GHSA advisory" in t` (:317) | **uncaught** (failures=0) | T-L11d demonstration below |

Mutant counter sha256s: L7d `976c51e5…`, L8e `a3d8894d…`, L9d `ebd279d3…`,
L9e `f11fea7d…`, L10d `a074aaca…`, L11d `42a64d7b…` (`receipt.json`).

## Coverage findings — four fresh survivors (not in the disclosed 34)

Each survivor was shown to be a real behavioral divergence, not an equivalent
mutant, on ad-hoc defect trees built from the kept `c1-green` fixture with one
scripted edit (`tdriver*.py`):

1. **L7d — the LESSON46 acceptance branch of l7 is unpinned.** A tree with the
   seat names only in `corpus/lessons/round-46.md` grades L7 green pristine
   (`read=dropped-findings-named in=corpus/lessons/round-46.md`, 11/11) and L7
   red under the mutant (10/11) — `t-T-L7d-*.txt`. The suite never exercises
   this branch: its only related case `c1-nolesson47` maps to limb L11 and
   passes with L7 either green or red (mutant on that tree: 9/11 vs pristine
   10/11, both `exit=1` with L11 red — `div-c1-nolesson47-*.txt`). An erratum
   landed only in the round-46 lesson — the natural home for round-46 dropped
   findings — is accepted by the frozen counter but pinned by no case.
2. **L9d — body-window bounds accepted at ±1 line.** Citing `S076.txt:557`
   (chrome "Repository security advisories", one line before `body_lines`
   [558,600]) or `S076.txt:601` ("Back to top", one line after) reds L9
   pristine (10/11) and greens it under the mutant (11/11) — `t-T-L9d-*.txt`,
   boundary line words in `boundary-scout.txt`. The suite's only out-of-body
   probe (`c1-badspan`, `S076.txt:1`) is far enough outside that the widened
   window still fails it, so the exact 558/600 edges are pinned nowhere.
3. **L10d — the lead bullet is not pinned to the Leads section.** The exact
   REST-API lead bullet displaced into `## Search log` reds L10 pristine
   (10/11) and greens it under the mutant (11/11) — `t-T-L10d-*.txt`. The
   suite probes removal (`c1-nolead`) but never displacement, so
   `section(raw, "Leads (unopened)")` scoping is unpinned.
4. **L11d — the precision phrase width is unpinned.** Replacing
   "one GHSA advisory entry" with "the GHSA advisory row class" (imprecise
   wording, still S068+GHSA) reds L11 pristine (`s068-precision=0`, 10/11) and
   greens it under the mutant (11/11) — `t-T-L11d-*.txt`. The suite's
   `c1-noprecision` swaps the whole phrase for "a row class", which fails
   pristine and mutant alike, so it does not discriminate phrase width.

Cross-check vs disclosure: `mutbat-receipt.txt` L-set survivors are L7a/L7b
(name count, keyword class), L8a/L8c/L8d (supersede cell, recheck rc, cell
count), L9a/L9b/L9c (old-cite check, whole range condition, pass floor), L10a/
L10b (URL specificity, bullet marker), L11a (reservation token). My four
survivors hit different bytes and different sub-checks (lesson-file fallback,
bound edges, section scoping, phrase width); none is one of the disclosed
edits. Per claims `mechanical_limits` these are selftest-coverage gaps, not
claims of equivalence; they do not weaken C1's kill rule — they widen what
wave 2 and the L1 should know is mechanically unpinned.

## Caught mutants (consistent with the frozen standard)

- L8e shows the manifest sha pin at :260 is load-bearing: with it amputated,
  the `maninert` tree (manifest note altered, bytes rewritten) false-greens
  11/11 — `source-recheck.py` does not itself pin manifest bytes, so the
  counter's own comparison is the only guard, and case `c1-maninert` catches
  the amputation.
- L9e shows the `uncited <= 0` floor at :296 is load-bearing: dropping it
  false-greens the `nocite` tree (one citation removed → its quote uncited,
  47→46 spans, uncited=1) at 11/11, caught by case `c1-nocite`.

## Limitations

- Bounded probe, per seat rules: 6 mutants × the c1 fixture set (20 trees) +
  5 crafted demonstration trees; the full 56-mutant battery was not re-run
  (its 34 disclosed survivors stand as receipted, not re-verified here).
- Mutants are counter-side single-edit weakenings only; no content-side
  mutants of lane docs were made (wave 2's attack scope).
- The c2 counter (f30-gate) was not probed — out of this seat's set.
- `divergent_cases` arrays in `receipt.json` are empty due to a parser bug in
  my driver (the selftest's `want=` field contains spaces my case-line regex
  didn't span); the per-case flips were read directly from the saved
  selftest stdout (`mut-*.txt`, `failing-cases.txt`) — verdicts unaffected.
- The frozen selftest copies snapshots from the live lane
  `corpus/source-snapshots/round-47/` (read-only); captures were not
  re-verified against the live web — out of scope.

## Restoration evidence

- Lane counter sha256 before and after every run:
  `e6ede7b668155fc173ad9a1c0f83168f173d6c31b12ecb85da406e1660424aee`
  (`hashes-before.txt`, `receipt.json: restoration.lane_unchanged=true`);
  freeze-export counter and selftest sha equal their `freeze.txt` pins.
- Mutants existed only as scratch copies under
  `/fast/scratch/hyaku/kasegi-r47/R47MutC1b/`; pristine detector rerun after
  all mutants: `cases=20 failures=0` (`pristine-3.txt`).
- Scratch dir removed after receipt copy (`COPY_OK`; 37 files in
  `R47MutC1b.draft/`).
