# R46bW2MutSelfC1 — battery `--counter c1` at the landed tree + formerly-uncaught mutant verification

VERDICT: HOLDS

Item: run the landed battery `--counter c1` against the landed tree; verify each formerly-uncaught
mutant is now caught (M06, M07, M08, M11, M12, M13, M14, M17, M18, M19), quoting per-mutant
extended-selftest failure lines or equivalence proof ids. Any mutant at `failures=0` without an
equivalence id would break C1.

## Tree identity

- Landed tree = lane commit `96379ae26ef9443097b860ddb33ef924b2cd5b5a` (wave-1 integration, HEAD),
  exported read-only via `git archive 96379ae | tar -x` to scratch. Freeze commit `fe0f56b` holds
  the pre-integration bytes; the battery at HEAD is v1.1 (E1 erratum adds F29 support; the frozen
  v1 sha256 f7a7cdf… in freeze.txt matches `git show fe0f56b:corpus/instruments/r46-mutbat.py`).
- The graded counter is UNCHANGED by the landing: `cmp` of `r46-c1-gate.py` between the 04af9bc
  export and the 96379ae export is byte-identical, so the only landing delta on this surface is
  the extended selftest (76 -> 83 cases) and the battery. My probe therefore attacks the claim
  "the extended selftest catches what the battery's C1 table throws at it".
- Pure input = byte-copy (`cp -a`) of the lane's own scratch
  `/fast/scratch/hyaku/kasegi-r46/L1/pure2`, the same pure the before-receipts used
  (`run-controls.sh` line 51: `PURE_SRC=/fast/scratch/hyaku/kasegi-r46/L1/pure2`).

## 1. Battery `--counter c1` at the landed tree — attack: claims.json C1 expect_after

Command (scratch cwd; TMPDIR inside scratch):

```
python3 -I corpus/instruments/r46-mutbat.py --root <scratch>/tree --pure <scratch>/pure2 \
  --work <scratch>/work/battery-landed --counter c1 --jobs 8
```

Quoted output (complete, 21 lines):

```
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=27 verdict=caught
mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=9 verdict=caught
mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M04-L2-one-reground baseline_failures=0 mutant_failures=26 verdict=caught
mutant=M05-L3-shape-loose baseline_failures=0 mutant_failures=3 verdict=caught
mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M08-L4-bytes-dropped baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M09-L4-planted-dropped baseline_failures=0 mutant_failures=4 verdict=caught
mutant=M10-L4-symlink-ok baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M11-L5-prefix-flip baseline_failures=0 mutant_failures=5 verdict=caught
mutant=M12-L5-restore-dropped baseline_failures=0 mutant_failures=3 verdict=caught
mutant=M13-L6-control-dropped baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M14-L6-exit-ignored baseline_failures=0 mutant_failures=0 verdict=equivalent
mutant=M15-L7-always-true baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M16-min-rows-5 baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M17-min-token-1 baseline_failures=0 mutant_failures=2 verdict=caught
mutant=M18-anchor-dirs-wide baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M19-L2-eq-relaxed baseline_failures=0 mutant_failures=1 verdict=caught
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=1 verdict=caught
mutbat counter=c1 mutants=20 caught=19 equivalent=1 uncaught=0 baseline_failures=0
```

`caught(19) + equivalent(1) == mutants(20)`, `uncaught=0`, `baseline_failures=0` — the C1
expect_after shape for counter c1 holds at the landed tree. No mutant is `failures=0` without an
equivalence verdict: M14 is the only zero-failure mutant and it carries the committed map entry
`corpus/instruments/r46-mutant-equivalents.json -> M14-L6-exit-ignored-receipt.txt`.

## 2. Per-mutant extended-selftest evidence (formerly-uncaught set + M08/M11/M12/M17)

Driver: the battery's own `C1_MUTANTS` triples applied once to a scratch copy of the counter
(single-occurrence asserted by the battery's `apply_mutant`), then the landed
`r46-counters-selftest-c1.py` run against the mutated counter. Full logs were in scratch
(deleted on exit; key lines quoted here).

- **M06-L3-home-dropped** (`or HOME_RE.search(CD_RE.sub(...))` dropped) — caught:
  ```
  case L3-home-path-in-trailing-comment          ... L3=1 ... fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN
  case L3-absolute-home-path-in-trailing-comment ... L3=1 ... fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN
  selftest cases=7 failures=2
  ```
  Real verdict flip: with HOME_RE blind on the comment channel the counter reads a `~/notes`
  comment tree 7/7 exit=0; the unmutated counter rejects it.
- **M07-L3-home-no-abs** (`/home/` removed from HOME_RE) — caught:
  ```
  case L3-absolute-home-path-in-trailing-comment ... fixed=7/7 exit=0 targets=L3 verdict=FALSE-GREEN
  selftest cases=5 failures=1
  ```
- **M08-L4-bytes-dropped** (`and read(bp) == read(tp)` dropped) — caught:
  ```
  case L4-planted-anchor-in-place-edit ... fixed=7/7 exit=0 targets=L4 verdict=FALSE-GREEN
  selftest cases=5 failures=1
  ```
- **M11-L5-prefix-flip** (`t[:len(b)] != b` -> `== b`) — caught, but through the TIP case, not a
  dedicated false-green case: the flipped comparison reds the pristine tip itself,
  ```
  case TIP-7of7 ... L5=0 ... fixed=6/7 exit=1 targets=- verdict=UNEXPECTED
  selftest cases=10 failures=1
  ```
  every L5 case then also reads L5=0 fixed=6/7 verdict=OK (red for the mutated reason). Kill is
  real (mf=5) but it is a broken-grader kill, not a defect-detection kill.
- **M12-L5-restore-dropped** (`or rest_ok != [want]` dropped) — caught:
  ```
  case L5-restoration-recheck-dropped   ... fixed=7/7 exit=0 targets=L5 verdict=FALSE-GREEN
  case L5-restoration-comment-rewritten ... fixed=7/7 exit=0 targets=L5 verdict=FALSE-GREEN
  case L5-restoration-recheck-twice     ... fixed=7/7 exit=0 targets=L5 verdict=FALSE-GREEN
  selftest cases=7 failures=3
  ```
- **M13-L6-control-dropped** (`if c.returncode != 0:` -> `if False:`) — caught, but ONLY via the
  reason-string attribution the errata E2 discloses:
  ```
  case L6-anchor-escapes-the-scratch-copy ... L6=0 ... fixed=6/7 exit=1 targets=L6 verdict=UNEXPECTED
  reads=... L6:mutants=16 survivors=claim-package-contract.md:G1,...,G8
  selftest cases=5 failures=1
  ```
  Unmutated contrast run of the same case: `case L6-anchor-escapes-the-scratch-copy ... verdict=OK,
  selftest cases=5 failures=0`. The limb verdict (L6=0, fixed=6/7) is IDENTICAL under the mutant;
  what changes is only that the counter no longer says `unmutated-copy-not-green`. I could not
  construct an input where M13 flips the L6 pass/fail itself (on the case tree every row survives
  under both; a red control implies >= MIN_ROWS survivor rows either way), so this kill rests on
  the attribution sentence, exactly as E2 admits.
- **M14-L6-exit-ignored** — `failures=0`, equivalence verdict, and the proof checks out:
  - battery: `mutant=M14-L6-exit-ignored baseline_failures=0 mutant_failures=0 verdict=equivalent`
  - targeted run (`--only L6-`, i.e. all three dedicated L6 cases): `selftest cases=7 failures=0`
  - committed differential re-run by me against the same pure:
    `m14-equivalence trees=15 differing=0` (all 15 tree lines `identical=True`)
  - static argument verified in `r46-c1-gate.py`: `entry_mode` returns 0 only via
    `return 0 if good else 1` with `good => ok == len(rows)` and `ok` sums the printed row
    verdicts, so `p.returncode == 0` implies no ` ok=0 ` row line, i.e. `red == []`, which makes
    `red != [r[0]]` true for every row — the dropped disjunct is implied by the surviving operand
    on every input. Equivalence id: `M14-L6-exit-ignored-receipt.txt` (+ probe README). HOLDS.
- **M17-min-token-1** (`MIN_TOKEN = 8` -> `1`) — caught:
  ```
  case L4-token-shorter-than-8                    ... fixed=7/7 exit=0 targets=L1,L2 verdict=FALSE-GREEN
  case L4-token-shorter-than-8+stubbed-gate-copy  ... fixed=7/7 exit=0 targets=L1,L2 verdict=FALSE-GREEN
  selftest cases=6 failures=2
  ```
- **M18-anchor-dirs-wide** (`corpus/knowledge/` added to ANCHOR_DIRS) — caught:
  ```
  case X-anchor-dir-outside-the-whitelist ... fixed=7/7 exit=0 targets=L1,L2,L7 verdict=FALSE-GREEN
  selftest cases=5 failures=1
  ```
- **M19-L2-eq-relaxed** (`len(gt) == len(gb) - len(reg) and not (gt - gb)` -> `len(gt) <= len(gb)`)
  — caught with a real limb-verdict flip:
  ```
  case L2-newly-gated-entry-not-gated-at-base ... L2=1 ... fixed=6/7 exit=1 targets=L2 verdict=UNEXPECTED
  selftest cases=5 failures=1
  ```
  Unmutated contrast run: `case L2-newly-gated-entry-not-gated-at-base ... L2=0 ... fixed=5/7
  exit=1 targets=L2 verdict=OK`. L2 0 -> 1 under the mutant is a genuine verdict change.
- **M20-syntax-ignored** (`bash -n` check -> `if False:`) — caught with a real verdict flip:
  ```
  case L1-cd-target-is-not-valid-bash ... fixed=7/7 exit=0 targets=L1 verdict=FALSE-GREEN
  selftest cases=5 failures=1
  ```
  Unmutated contrast: `... L1=0 ... fixed=6/7 exit=1 ... verdict=OK`.

## 3. Do-nothing control — attack: kill_rule "before-value reproducible at the base export"

Same battery, `--root` = 04af9bc export (selftests untouched at base; counter identical, `cmp`
verified), same pure:

```
mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M13-L6-control-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M18-anchor-dirs-wide baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M19-L2-eq-relaxed baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=0 verdict=uncaught
mutbat counter=c1 mutants=20 caught=13 equivalent=1 uncaught=6 baseline_failures=0
```

All 20 per-mutant `mutant_failures` counts match `controls/mutbat-before.txt` line for line; the
only delta vs the before-receipt is M14 `uncaught -> equivalent`, which is the v1.1 `--equivalent`
map feature firing (the v1 battery had no map at all). The base selftest does NOT grade
uncaught=0 — the control discriminates, and the before-value reproduces.

## Findings (none kills the c1 claim)

1. Item-text mismatch: M08, M11, M12 and M17 were never formerly-uncaught —
   `controls/mutbat-before.txt` already grades them caught (mf=1, 5, 3, 2). The formerly-uncaught
   seven are M06, M07, M13, M14, M18, M19, M20. My run covers all eleven named mutants anyway.
2. M13's kill is attribution-only on the case tree (limb verdict identical; only the
   `unmutated-copy-not-green` sentence disappears) — disclosed in errata E2, confirmed here
   empirically. M11's kill is via the broken TIP case, not a dedicated defect case. Both are real
   kills under the battery predicate (`mutant_failures >= 1`) but weaker than the other seven.
3. `counter-errata.md` E2 says "Both dead `--pure` defaults now point at the committed map
   pattern (`--pure` required, no dead absolute default)" — FALSE at the landed tree:
   `r46-counters-selftest-c1.py` lines 57/649 still carry `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"`
   as the `--pure` default (path does not exist). Doc/instrument mismatch; harmless when `--pure`
   is passed, as the battery always does.
4. Battery crash-path mislabels grader failure as a coverage hole: `run_selftest` returns -1 when
   the selftest prints no `failures=` line (e.g. a selftest crash), and -1 is not `>= 1`, so a
   crashing grader grades the mutant `uncaught`, not `error`. Conservative for kills, but it would
   misdiagnose a broken selftest as a mutation-coverage gap.
5. Ambiguity in the kill_rule wording "reproducible at the base export": a literal base-commit
   export (04af9bc corpus) is NOT usable as the selftest's `--pure` — the selftest crashes with
   `AssertionError: mutation was a no-op on corpus/knowledge/claim-gates.md` because claim-gates
   at 04af9bc already carries the attempt-1 `## Re-ground (round 46)` table (25 G-rows), so the
   case builders' first `| G1 |` matches a historical row with a range anchor. The faithful base
   reading (base tree + the lane's pure2, as run-controls.sh does) reproduces the before-value
   exactly; but a reviewer following the literal wording hits a crash, not a receipt.

## Limitations

- Host was heavily contended (loadavg up to ~107, dozens of sibling selftests); each full
  battery took ~2 h wall-clock instead of minutes. All 20 mutants completed in both runs; no
  timeouts or partial results. The landed battery's exit code was not captured (wrapper omitted
  on the detached relaunch); by the tool's own accounting (`bad` incremented only on
  baseline-dirty or uncaught, neither of which occurred) it is 0, and the summary line carries the
  claim.
- M13's "no limb-flip class constructible" is a failure-to-construct, not a proof; the static
  argument is in Finding 2. M14's equivalence is verified on the committed differential's 15 trees
  plus the static implication argument; a counterexample outside that class would falsify it.
- The pure used is a byte-copy of the lane scratch `L1/pure2` (same bytes; `cp -a`), not a git
  object — matching what the before-receipts actually used.
- Scratch dir (exports, work dirs, logs) deleted after this report; quoted outputs are
  self-contained above. No lane file was written except this report; no git/jj/index mutation.

Restoration evidence: all mutations were applied to scratch copies only
(`apply_mutant` into `<scratch>/work/...`); the lane tree and both git exports were never edited.
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status` untouched by me apart from this
report file; scratch removed with `rm -rf` before yielding.
