# R46bW2MutBattery2 — battery v1.1 `--counter f29` end-to-end

VERDICT: BROKEN

Scope: run `corpus/instruments/r46-mutbat.py --counter f29` (v1.1, lane working copy = HEAD 96379ae bytes) against the
attempt-2 freeze tree fe0f56b, reconcile per-mutant lines with `controls/f29-r50-receipt.txt`, discriminate with a
do-nothing control. Nothing committed, nothing shared touched; scratch removed on exit.

## F1 — as specified, the f29 mode produces no per-mutant lines (BROKEN, blocks the item)

Command (exact, fe0f56b export at `$S/integ-fe0`, from `git archive fe0f56b corpus .ufo/.../controls`):

    python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-mutbat.py --root $S/integ-fe0 --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/work/fe0 --counter f29

Output (verbatim, exit 1):

    mutbat counter=f29 BASELINE-DIRTY baseline_failures=-1

Same on the landed tree (`git archive 96379ae`, `--root $S/integ-head`): verbatim identical line, exit 1.

Cause, reproduced by running the selftest the battery invokes (`python3 -I corpus/instruments/r46-selftest-f29.py`, cwd=tree):

    selftest: lane README carries 29 frontier rows, expected 28

- `r46-selftest-f29.py` has `LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"` (HEAD line 57) and
  `build_positive()` asserts 28 frontier rows in that README (HEAD line 188). The battery never passes `--lane`, so
  `--root` supplies only the counter bytes; the corpus graded is the live lane, which now has 29 rows
  (`grep -cE '^\| F[0-9]+ \|' corpus/README.md` = 29; fe0f56b export = 28; HEAD export = 29).
- The selftest is absent from the fe0f56b export; `f29_find_selftest()` falls back to an absolute path outside the
  export, `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`. `diff` against HEAD's
  `corpus/instruments/r46-selftest-f29.py` prints nothing (identical bytes).
- The committed selftest therefore cannot run on the tree it ships in. Live check, `python3 -I corpus/instruments/r46-selftest-f29.py`
  (default lane): rc=1, last line `selftest: lane README carries 29 frontier rows, expected 28`. The wave-1 commit
  message lists "selftest-f29" as landed; that claim does not hold at HEAD.
- The baseline sentinel `-1` (no `failures=` line) is what turns the whole mode into BASELINE-DIRTY; the battery
  never reaches a mutant.

## F2 — the gate is path-bound to the live lane (design defect that forced the diagnostic below)

`corpus/instruments/r46-f29-gate.py` line 72 `LANE_CD = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"`, used in
`RECHECK_LINE` (line 92) for H2. Any tree whose recheck text names another path reads H2 red; the export passes only
because its text names the live path. This is why `--root` cannot retarget the f29 mode. `--root <export> gate` on the
HEAD export reads `f29-gate fixed=7/7 exit=0` (verbatim gate lines: H1 `rows=29 admitted=29 F29=admitted`, H2
`recheck=1 ... table-rows=19 xrefs=7/7`, H5 `spans=45 located=45`, H6 `knowledge=66 entries=66 nested-md=66`, H7 `census-rc=0 ok-line=1`).

## F3 — diagnostic reconciliation (scratch-only; the lane-path constants patched in a scratch copy of fe0f56b)

To obtain per-mutant lines at all, I copied the fe0f56b export to a scratch tree and changed two constants IN THE SCRATCH
COPY ONLY: the selftest's `LANE_DEFAULT` and the gate's `LANE_CD` both set to that copy's path (the draft selftest bytes
copied in; the selftest's own provenance notes match). The copy's baseline is clean (`selftest cases=30 failures=0`,
`f29-gate fixed=7/7 exit=0` on the positive tree). Then the unmodified battery ran against it:

    python3 .../r46-mutbat.py --root $S/diag-fe0 --pure .../L1/pure2 --work $S/work/diag2 --counter f29

    mutant=H1a-counts-loose baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H1b-raw-loose baseline_failures=0 mutant_failures=0 verdict=uncaught
    mutant=H1c-src-boundary baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H2a-verified-loose baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H2b-wordfloor-low baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H2c-need-empty baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H3a-cells-loose baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H3b-scope-low baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H3c-kind-dead baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H4a-manifest-unpinned baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H4b-quotes-low baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H4c-distinct-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H5a-span-wide baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H5b-words-wide baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H5c-pass-low baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H6a-counts-loose baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H6b-pin-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H6c-size-low baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H7a-verdict-or baseline_failures=0 mutant_failures=0 verdict=uncaught
    mutant=H7b-symlink-dead baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=H7c-okline-loose baseline_failures=0 mutant_failures=0 verdict=uncaught
    mutbat counter=f29 mutants=21 caught=18 equivalent=0 uncaught=3 baseline_failures=0
    (exit 1)

Reconciliation against the R50 receipt (grading by mutant name; the receipt's pairing rows are fixture-level, the battery's
verdicts are selftest-level):

| receipt class | mutants | battery | result |
|---|---|---|---|
| FLIP (must be caught) | H1c, H2a, H2c, H3b, H3c, H4a, H5a, H5b, H6a, H6b, H7b | 11/11 caught | PASS |
| NOT-SHOWN (equivalent-or-caught) | H1a | caught | PASS (receipt (a) said shadowed; the selftest now catches it) |
| NOT-SHOWN | H2b, H3a, H4b, H4c, H5c, H6c | caught | PASS |
| NOT-SHOWN | H1b | uncaught, no proof | FAIL (see F4) |
| NOT-SHOWN | H7a, H7c | uncaught, no proof | FAIL (see F4) |

Counts: receipt tallies 11 flips + 10 NOT-SHOWN = 21 (H6c added by the receipt's correction). The task text says
"the 9 disclosed"; the receipt says 10. Mismatch recorded; 7 of the 10 NOT-SHOWN read caught.

## F4 — 3 uncaught mutants, all with a provable-equivalence argument, none with a committed proof

`corpus/instruments/r46-mutant-equivalents.json` (tracked at HEAD) maps only C1/C2 ids (4 entries: M14, G6b, G7a, G7c). No
F29 entry and no F29 proof file exist. Per the C1 kill rule (uncaught>0 keeps the claim red) the battery correctly exits 1.
Arguments the lead can commit as proofs (I did not commit anything):

- H1b (`if len(raw) != 1` -> `if len(raw) > 1`): `frontier()` keeps lines with `^\| F\d+ \|` after lstrip and
  `f29 = [r for r in rows if r[0] == "F29"]` is non-empty only if a live line matches `^\| F29 \|`; `raw` is exactly the
  live lines matching `^\| F29 \|` after lstrip over the same `live_lines()`. The clause `if not f29 ... return False`
  runs first, so any input reaching the raw check has len(raw) >= 1; `!= 1` and `> 1` then agree on every reachable
  input. Equivalent. (The receipt's disclosure (a) said "belt-and-braces"; this is the reason.)
- H7a (`rc == 0 and ok_line` -> `rc == 0 or ok_line`) and H7c (`\tok\t` -> `\tok`): the census script
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, lines 700-806) sets `findings=1` only on an E-line
  (line 740), which also sets `lane_errors=1`, which suppresses the `ok` emit (line 745, `emit "$lane\tok\t$f"`); exit 1
  only when `findings=1` (line 805). Probes: clean SOURCES -> `rc=0` plus `file\tok\t...`; SOURCES with one malformed
  row -> `rc=1` and no ok line; empty registry and header-only registry -> `rc=0` plus ok line. So rc!=0 never coexists
  with an ok line, and rc=0 always does. The second field of every census line is `ok`, an E/W code, or a FLEET tag,
  so no non-`ok` line begins with `ok`. Equivalent under the census's emitter grammar.
  CAVEAT: the census script is fleet-root, outside this lane, and the gate pins neither its bytes nor its grammar
  (PINS has no census entry). The equivalence holds only for the census as read; a committed proof should pin its sha.

Direct checks that the uncaught verdicts are not battery artifacts:
- `python3 -I $S/diag-fe0/corpus/instruments/r46-selftest-f29.py --counter <H7a mutant>` -> `selftest cases=30 failures=0`, rc=0.
- `--counter <H1c mutant>` -> `FAIL defect  defect-src0740  fixed=7/7 failing=[] <- expected-red=['H1'] actual-red=[]; tree read 7/7`
  and `selftest cases=30 failures=1`, rc=1 (the H1c catch is the real src0740 defect: the mutant regex `S074` without `\b` accepts the `S0740` cell).

## F5 — do-nothing discriminator (selftest level; the battery itself has no do-nothing mode)

`python3 -I <diag selftest> --do-nothing-control` (stub counter reads 7 green limbs everywhere): rc=0, `selftest cases=30 failures=0`,
with 29 `FAIL` lines, i.e. every red-expecting case reports the stub's unexpected green. The case set discriminates a no-op
counter; the unmutated diag baseline reads `failures=0`. The battery has no do-nothing control of its own; the receipt's
"before" line for f29 does not exist (`controls/mutbat-before.txt` carries only the c1/c2 pair).

## F6 — hygiene and hermeticity (no effect on the verdicts above)

- `r46-mutbat.py` defines `F29_DRAFT_SELFTEST`, `F29_CONTROLS_REL/ABS`, `F29_FIXTURE_MODES`, `F29_DEFECTS` twice (lines 141-149 and 181-189).
- The fixture fallback (`grader == "fixture"`) is unreachable whenever a selftest is found, and no run here exercised it.
- `--equivalent` defaults to the lane's working map, not the `--root` tree's map.
- A selftest discovered outside `--root` (the draft path) silently grades an export that lacks its own selftest. Non-hermetic.
- Tree-identity: the spec calls fe0f56b "integration of wave 1"; fe0f56b is the freeze commit. The wave-1 integration is 96379ae (HEAD). Both were tested; both give F1.

## Limitations

- Per-mutant lines exist only in the patched scratch copy (F3); the spec's exact command produces no mutant lines on either tree (F1). The patch is a path-constant change in scratch, not a fix.
- Equivalence arguments are reasoned from source plus probes, not machine-checked. The census argument depends on an unpinned fleet-root script.
- Grading by mutant name against the receipt; receipt pairing rows are fixture-level, battery verdicts are selftest-level.
- Not run: the battery's fixture fallback; the other counters (c1/c2 were out of scope); live-target or credential work (none).
- Tooling: no installs or updates were made by this seat.

## Requested fixes (for the planner; not applied)

1. Selftest: read the corpus from `--lane` (default to `--root`) and drop the hard-coded 28-row assertion, or assert 29 for the landed tree; re-land with a green HEAD run.
2. Gate: derive `LANE_CD` from the tree (or the recheck check against `--lane`) so `--root` retargets H2.
3. Battery: pass `--lane <tree>` to the selftest; refuse a selftest outside `--root`; name the pinned selftest sha.
4. Proofs: commit F29 equivalence files for H1b (argument above) and H7a/H7c (census grammar argument, with the census sha pinned), add the three ids to `r46-mutant-equivalents.json`, or add selftest cases that kill them.
