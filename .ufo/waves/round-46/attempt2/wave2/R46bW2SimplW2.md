# R46bW2SimplW2 — dead-weight pass over the landed instruments (wave 2)

VERDICT: BROKEN
(Scope of the verdict: the landed instrument set carries one landed-broken module and one
landed-incompatible guard, plus confirmed dead weight and docstring drift. Claim-relevant
consequence: C1's plain measure `python3 corpus/instruments/r46-counters-selftest-c2.py --pure
<pure> | tail -1` cannot print `cases=… failures=0` at the landed tree — the module dies at
import. All runs below: scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2SimplW2`, `TMPDIR` set to
it, `python3 -I`, read-only on the lane. Tree basis: landed instruments are identical in the
worktree and at integration commit 96379ae (dirty files are all `.ufo` bookkeeping; freeze
fe0f56b exported via `git archive` for comparison).

## F1 — r46-counters-selftest-c2.py: extension insert order kills the whole module (every added branch unreachable)

Artifact: `corpus/instruments/r46-counters-selftest-c2.py:68-69` (v1.3 ledger extension).

```
68: EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # the counter's CONTENT_EXEMPT: ...
69: C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}  # ...
```

Command: `python3 -I corpus/instruments/r46-counters-selftest-c2.py --help` (rc=1)

```
  File ".../r46-counters-selftest-c2.py", line 68, in <module>
    EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # ...
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
```

`C1_ENTRIES` is used at line 68 one line before its definition at line 69. `--help` never even
parses: the NameError fires at module level, so the ten `mut-g*` cases the extension adds (G1c,
G2a, G2b, G2c, G3a, G4b, G5c, G6a, G6c, G7b per the extension's own docstring block) are all
unreachable — no branch of the landed file executes at all.

Corroboration already committed by wave 1 — `.ufo/waves/round-46/attempt2/controls/final-battery.txt`:

```
== selftest c2 (extended+ledger):
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
exit=0
```

Control (discriminates against do-nothing): `python3 -I corpus/instruments/r46-counters-selftest-c1.py
--help` → rc=0. The v1.3 c1 extension imports cleanly; the crash is the c2 extension's own
statement order, not the harness. Minimal repair: move the line-69 definition above line 68 —
pure reorder, no behavior beyond making the file loadable.

## F2 — r46-selftest-f29.py build_positive: 28-row guard incompatible with the tree it landed on; the committed driver hits it

Artifact: `corpus/instruments/r46-selftest-f29.py` (`build_positive`), guard
`raise SystemExit("selftest: lane README carries %d frontier rows, expected 28" % len(frows))`.

Command: `python3 -I corpus/instruments/r46-selftest-f29.py --work $S/w-live` (default `--lane`
= the live lane), landed README `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `29`:

```
selftest: lane README carries 29 frontier rows, expected 28
```

The committed final driver `.ufo/waves/round-46/attempt2/controls/final-measure.sh` runs

```
[ -f corpus/instruments/r46-selftest-f29.py ] && run python3 -B corpus/instruments/r46-selftest-f29.py --work "$S/w-s3"
```

from `cd "$S/tip"` with no `--lane`, so the default (live lane, 29 rows) applies: the committed
final measurement's selftest step exits nonzero at the tip. (`-B` only suppresses `.pyc`
writing; the SystemExit path is identical — verified without `-B`.)

Narrow existing check proving the rest of the instrument is sound on 28-row material:
`python3 -I corpus/instruments/r46-selftest-f29.py --lane <fe0f56b export> --counter
<integ export>/corpus/instruments/r46-f29-gate.py --work $S/w-pair` →

```
ok   ctl     positive-cli           rc=0 gates=7 summary=['f29-gate fixed=7/7 exit=0']
selftest cases=30 failures=0
```

exit 0. So the 28-guard is the only blocker: the instrument can run only against a tree that
has the S074 capture AND 28 F-rows — exactly the freeze export fe0f56b — while its default and
the committed driver's effective lane is the landed tree (29 rows). Same guard in the
receipt-pinned builders, for the record: `f29-fixture.py --mode positive --lane <live lane>` →

```
  File ".../controls/f29-fixture.py", line 135, in build
    assert len(frows) == 28, len(frows)
AssertionError: 29
```

The builders are freeze-era receipt fixtures (sha-pinned), so their guard was correct for the
R50 pass; the live selftest inherited it and landed with the change that fires it.

## F3 — r46-mutbat.py v1.1: duplicated module-level constant block (second shadows first, values identical)

Artifact: `corpus/instruments/r46-mutbat.py` — the f29 wiring constants
`F29_DRAFT_SELFTEST / F29_CONTROLS_REL / F29_CONTROLS_ABS / F29_FIXTURE_MODES / F29_DEFECTS`
are defined twice: lines 141-147 ("# --- f29 grader wiring ---") and lines 181-187 ("# --- f29
grader: the selftest (preferred) or the R50 fixture corpus (fallback) ---").

Command: `sed -n '140,148p' … > blk1; sed -n '180,188p' … > blk2; diff blk1 blk2` →

```
1c1
< # --- f29 grader wiring -----------------------------------------------------------
---
> # --- f29 grader: the selftest (preferred) or the R50 fixture corpus (fallback) -----
```

Only the comment line differs; all five assignments are byte-identical. Identical-behavior
argument: Python executes both blocks in order, so the second assignment wins; since the values
are equal, deleting the first block (lines 140-148) changes no observable value, output, or
exit code. The two differing comment headers mark it as a merge/edit artifact, not intent.

## F4 — r46-mutbat.py v1.1: grader branches keyed on a selftest without `--counter` — unreachable for both existing graders

Artifacts: `f29_run_selftest`: `if counter_path and "--counter" not in flags: cmd += ["--root",
counter_path]`; `grade_f29`'s per-mutant else-branch ("the selftest grades a tree: put the
mutant gate into a tree copy and hand the copy over", a full `copytree` per mutant).

Command (flags of both graders):
`python3 -I <wave1 draft>/R46bExecSelftestF29.draft/r46-selftest-f29.py --help | grep -oE '\-\-[a-z-]+' | sort -u` →

```
--counter --do-nothing-control --help --jobs --keep --lane --pure --verbose --work
```

The committed `r46-selftest-f29.py` advertises the same set (its argparse: `--lane --counter
--work --pure --jobs --do-nothing-control --keep -v`). Neither accepts `--root`, both advertise
`--counter`, so `"--counter" not in flags` is False for every grader that exists in the tree →
both branches never execute; the dead else-branch would be the battery's most expensive path
(tree copy per mutant) if ever hit. Micro: `f29_find_selftest`'s `if p and os.path.isfile(p)` —
`p` is never falsy. Identical-behavior argument: removing both `--counter`-absent branches
leaves every reachable invocation (committed and draft grader, selftest and fixture modes)
byte-identical in output and exit code.

## F5 — r46-selftest-f29.py: vendored counter rule has drifted from the rule it claims to mirror

Artifacts: `live_lines` ("The counter's live-line rule (fenced and HTML-commented lines are not
live)") and `read_frontier` ("…read the way the counter reads them"). The landed gate v1.1
changed both rules (mid-line `<!-- … -->` stripped and the cleaned line kept; `frontier`
now lstrips); the selftest's vendored copies are the v1 rules.

Command (mechanical, importlib, sample `"text <!-- mid comment --> tail\n| F29 | x |\n   | F01 |
indented |\n"`): `st.live_lines(sample) == gate.live_lines(sample)` → `False`

```
gate v1.1:      ['text   tail', '| F29 | x |', '| F01 | indented |']
selftest copy:  ['text <!-- mid comment --> tail', '| F29 | x |', '   | F01 | indented |']
```

Identical-behavior boundary: grading always goes through `mod.GATES` (the real gate), so the
drift is observable only in `read_frontier`/`controlled_rows` (the clause-a-raw-once patch); no
committed fixture writes a mid-line HTML comment or an indented F-row into the README, so every
committed case is unaffected — but the docstring's "the counter's live-line rule" is now false,
and unlike the tree recipes this copy carries no provenance pin (BUILDER_PROVENANCE covers only
the two builders, both of which match:

```
52ea96939c62a71943838ca883d7914dd598f3e7eeb061266975ece7ccb26275  f29-fixture.py
2e95d4d4b6cf372a8464803bf82c7ae79d1612dc8060b5a9c18798cfbcbc07c2  f29-defects.py
```

equal to the selftest's pins, builders unchanged freeze→integration).

## F6 — docstring drift set (quotes vs landed behavior)

a. `r46-f29-gate.py:2` self-describes as `… C2 counter (coverage), v1.` while carrying the five
   v1.1 clause extensions (`frontier_anywhere` ghost-row clause, exact-entry-cell, `of <path>`
   locator binding, url canonicality, registry-sections); the integration commit names it
   "f29-gate v1.1"; the R50 receipt pins "v1" to the freeze sha. The landed bytes are not the
   pinned v1.
b. `r46-selftest-f29.py:1` "selftest for corpus/instruments/r46-f29-gate.py v1" — it grades the
   v1.1 file (F2's run: cases=30 failures=0 against the tip gate).
c. `r46-selftest-f29.py` USAGE advertises `[--jobs N]` (line 39); argparse parses it (line 798);
   it is used nowhere in the file — dead flag. Interaction: `r46-mutbat.py v1.1`
   `f29_run_selftest` passes `--jobs str(jobs)` whenever the selftest advertises the flag, so
   the battery believes parallelism is honored; the f29 selftest is silently serial. (`--pure`
   is the same parsed-never-used class but is self-declared "accepted for interface parity".)
d. `r46-selftest-f29.py` docstring case list names 7 clause cases; the landed file builds 8
   (`clause-c-cells-12` is omitted). "one defect tree per row of the R50 receipt's defect
   table": the receipt table has 20 pairing rows over 18 distinct defect trees; the selftest
   implements all 18 plus `src0740`-style derivation — the "per row" wording overcounts.
e. `r46-mutbat.py` docstring: "the f29 grader is the f29 selftest when one is present — the
   wave-1 draft at <draft>, else the committed corpus/instruments/r46-selftest-f29.py" —
   `f29_find_selftest` tries the tree's committed copy FIRST, the draft second. Reversed.

## F7 — extension branches checked and alive (no finding; stated to bound the pass)

- f29-gate v1.1 additions: the `clean.startswith("<!--")` skip is reachable (unterminated
  `<!--`), the lstrip+`frontier_anywhere` pair is reachable (indented / zero-width ghost rows),
  exact-entry-cell / locator-binding / url-canonicality / registry-sections are all
  input-reachable. No dead branch proven in the gate.
- c2-gate v1.3 junk-row clause: reachable and load-bearing — the entry under test is excluded
  from the content pin (`base_like = [n for n in everything if … != p]`), so a junk table row
  is the only red G5 can raise on such a tree (it kills the v1.1 "junk tolerated" mutant).
- counters-selftest-c1 v1.3 cases: module imports (rc=0); cases target the limbs the R50 table
  leaves uncovered.
- selftest-f29 defensive branches are NOT dead: `patch_pins`' no-PINS path and `patch_frontier`'s
  del path are exercised by `--do-nothing-control` (the stub counter has neither attribute).
  Control run (same pairing, `--do-nothing-control`): 29 `FAIL` case lines, positive stays `ok`,
  `selftest cases=30 failures=0` (failures counts only unexpected outcomes) — the case vectors
  discriminate against a do-nothing counter.

## Limitations

- Findings only; nothing edited, committed, or deleted (lane untouched; byte-identical check:
  instrument files are clean in `git status` and identical at 96379ae).
- I did not run the full battery (`--counter f29|all`) or the c1/c2 selftest suites end-to-end —
  that is the executors'/mutators' falsification surface; my runs were the narrow checks above.
  In particular F1 means no `mut-g*` c2 case has ever executed on the landed tree.
- The `run`-helper `exit=0` recorded beside the NameError in `final-battery.txt` is wave-1
  bookkeeping outside my item; quoted only as corroboration.
- Scratch removed after the report was written.
