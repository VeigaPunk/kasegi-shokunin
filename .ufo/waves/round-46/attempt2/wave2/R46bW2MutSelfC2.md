VERDICT: BROKEN

# R46bW2MutSelfC2 — c2 formerly-uncaught set (round 46 attempt 2, wave 2)

Item: for each of the 13 c2 mutants uncaught at the before-value (`controls/mutbat-before.txt`, c2 list:
G1c, G2a, G2b, G2c, G3a, G4b, G5c, G6a, G6b, G6c, G7a, G7b, G7c), quote the extended selftest's lines proving
it is now caught or equivalence-proven.

Attacked artifact: lane commit `96379ae` (HEAD, wave-1 integration). It contains `fe0f56b` (freeze) as an ancestor.
The extended c2 selftest (147 cases) exists only at `96379ae`; at `fe0f56b` the selftest is v1 (137 cases) and the
battery has no equivalence map. Corpus bytes at the live working tree equal `96379ae` for the three instruments
(`sha256` r46-c2-gate.py `29d50bf0…`, r46-counters-selftest-c2.py `9b13b6b3…`, r46-mutbat.py `99029667…`; `git status -- corpus` empty).

Scratch: `/fast/scratch/hyaku/kasegi-r46/R46bW2MutSelfC2/` (exports of 96379ae, 04af9bc, fe0f56b, 914ca0b corpus;
scratch-only repairs). Removed on exit. Nothing committed; no git/jj mutation (archive, show, log, status, rev-parse only).

## Result in one line

0 of 13 has a line in a runnable extended selftest at the landed commit. 10 are measurable only after scratch
repairs (below) and 3 (G6b, G7a, G7c) are equivalence claims whose committed proof is wrong for G6b. Details follow.

## F1 (blocking) — the extended c2 selftest does not import at 96379ae

Artifact: `corpus/instruments/r46-counters-selftest-c2.py` lines 68–69 (blob `9b13b6b3…`).

    $ cd <export 96379ae> && python3 -I corpus/instruments/r46-counters-selftest-c2.py --pure <pure>
    Traceback (most recent call last):
      File ".../r46-counters-selftest-c2.py", line 68, in <module>
        EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # ...
                         ^^^^^^^^^^
    NameError: name 'C1_ENTRIES' is not defined

`C1_ENTRIES` is defined on line 69, after its use on line 68. The same error occurs in the live working tree (same
bytes). Origin: the GatePinAmend draft (`wave1/R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py:63`) put the
`EXEMPT_ENTRIES` line above the set; the integration merged it. The lane's own untracked receipt
`controls/final-battery.txt` already shows `NameError: name 'C1_ENTRIES' is not defined`; its `exit=0` is the exit
status of `tail`, not of the selftest.

Battery at the landed tree (`--pure` = corpus export of 914ca0b, see F7):

    $ python3 corpus/instruments/r46-mutbat.py --root <96379ae> --pure <pure2> --work <w> --counter c2 --jobs 8
    mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1        (exit 1; no per-mutant line printed)

## F2 — with the import fixed, the committed selftest is red on the committed counter (junk conjunct)

Repair R1 (scratch only): move line 69 above line 68. Result:

    selftest cases=147 failures=101            (scratch R1, default counter = committed r46-c2-gate.py)
    FAIL control ctl-complete-tree fixed=6/7 failing=['G2']  <- control-not-7/7 failing=['G2']
        gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=7 xrefs=2/2

Cause: the v1.3 counter's g2 requires `junk == 0`, where `junk = table_lines - (2 + counted rows)`. The selftest's
complete-tree fixture has 8 three-cell table rows of which 7 carry a cite, so the uncited row is junk. Every control
and most mutant trees inherit this red G2. Removing only `and junk == 0` from a scratch copy of the counter and passing
it with `--counter` gives:

    selftest cases=147 failures=1
    FAIL control ctl-committed-tip-direct fixed=5/7 failing=['G1', 'G6']  <- control-not-7/7 failing=['G1', 'G6']

## F3 — the committed-tip control makes the c2 baseline unsatisfiable

`ctl-committed-tip-direct` requires 7/7 on the committed tip. The tip reads 5/7 (G1 28→29, G6 65→66 after the F29
landing; errata E3 acknowledges this). So `baseline_failures >= 1` at every tip regardless of F1/F2. Under
`mutbat` a dirty baseline stops grading, and the caught predicate `mutant_failures >= 1` would count a no-op
mutant as caught on a dirty baseline. The unchanged control is the reason, not any mutant.

## F4 — the grader does not grade the tree under --root

`r46-mutbat.py` main: `baseline, tail = run_selftest(a.root, which, None, ...)` passes no `--counter`. The selftest
default is `os.path.join(a.lane, "corpus/instruments/r46-c2-gate.py")` with `LANE` hard-coded to
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (selftest line 53). So the baseline grades the live lane's counter, not
`--root`. Evidence: removing the junk conjunct in a scratch copy and running WITHOUT `--counter` left the count at
`failures=101`; only the `--counter` run changed it.

## F5 — per-mutant evidence for the 10 dedicated cases (scratch repairs, mutant applied to the counter named)

Selftest variants: R1 (import fixed) plus `--counter` pointing at a full instrument copy of the counter.
`C` = mutant of the committed counter. `J` = mutant of the same counter with `junk == 0` removed (scratch diagnostic).
`DN` = `--do-nothing-control`. Each line is the mutant's dedicated case, as printed.

| mutant | C (committed base) | J (junk-free base) |
|---|---|---|
| G1c | `FAIL mutant mut-g1c-f28-sources-cell-prefix fixed=6/7 failing=['G2'] <- ACCEPTED-targeted-gate-passes=['G1']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g1c-f28-sources-cell-prefix fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G1']; tree read 7/7` caught |
| G2a | `ok   mutant mut-g2a-verified-at-prefix fixed=6/7 failing=['G2']` **NOT caught** (G2 red for the junk reason) | `FAIL mutant mut-g2a-verified-at-prefix fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G2']; tree read 7/7` caught |
| G2b | `ok   mutant mut-g2b-limits-word-floor fixed=6/7 failing=['G2']` **NOT caught** | `FAIL mutant mut-g2b-limits-word-floor fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G2']; tree read 7/7` caught |
| G2c | `ok   mutant mut-g2c-overlap-xref-swapped fixed=6/7 failing=['G2']` **NOT caught** | `FAIL mutant mut-g2c-overlap-xref-swapped fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G2']; tree read 7/7` caught |
| G3a | `FAIL mutant mut-g3a-registry-row-cells fixed=5/7 failing=['G2','G7'] <- ACCEPTED-targeted-gate-passes=['G3']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g3a-registry-row-cells fixed=6/7 failing=['G7'] <- ACCEPTED-targeted-gate-passes=['G3']` caught |
| G4b | `FAIL mutant mut-g4b-manifest-quote-count fixed=6/7 failing=['G2'] <- ACCEPTED-targeted-gate-passes=['G4']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g4b-manifest-quote-count fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G4']; tree read 7/7` caught |
| G5c | `FAIL mutant mut-g5c-five-cores-two-spans fixed=5/7 failing=['G3','G4'] <- ACCEPTED-targeted-gate-passes=['G5']` caught | same shape, caught |
| G6a | `FAIL mutant mut-g6a-knowledge-file-symlink fixed=6/7 failing=['G2'] <- ACCEPTED-targeted-gate-passes=['G6']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g6a-knowledge-file-symlink fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G6']; tree read 7/7` caught |
| G6c | `FAIL mutant mut-g6c-entry-byte-floor fixed=6/7 failing=['G2'] <- ACCEPTED-targeted-gate-passes=['G6']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g6c-entry-byte-floor fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G6']; tree read 7/7` caught |
| G7b | `FAIL mutant mut-g7b-sources-md-symlink fixed=6/7 failing=['G2'] <- ACCEPTED-targeted-gate-passes=['G7']; collateral-unexpected=['G2']` caught | `FAIL mutant mut-g7b-sources-md-symlink fixed=7/7 failing=[] <- ACCEPTED-targeted-gate-passes=['G7']; tree read 7/7` caught |

Battery-level totals, selftest `failures=` per run: committed-base mutants 101 for all except G5c (102); the committed
baseline (R1, no mutant) is 101. So under the committed counter G2a/G2b/G2c would be "caught" by the baseline noise,
not by their own case. J-base runs: `failures=2` for every mutant against a baseline of `failures=1` (the tip
control); the target case adds exactly one. Do-nothing control: `selftest cases=147 failures=128` with 134
`ACCEPTED` lines, including the same `FAIL mutant … ACCEPTED-targeted-gate-passes=[Gx]` line for all 10 targeted cases,
so the cases do reject a stub that accepts everything.

Outcome for the 10 dedicated cases: caught by their own line when the junk conjunct is removed (J). Under the committed
counter, G2a, G2b and G2c are not caught by their own line (C reads `ok`); the other seven are caught only together
with junk-induced collateral G2 failures.

## F6 — G6b equivalence proof argues a clause that does not exist; the mutant is equivalent for a different reason

Artifacts: `corpus/instruments/r46-mutant-equivalents/README.md` (section G6b) and
`corpus/instruments/r46-mutant-equivalents/G6b-G7a-G7c-equivalence-probe.txt`; map `r46-mutant-equivalents.json`.

- The proof says the mutant is `base_ok = base_ok and cont == PINS[...] and ledger_ok`. The gate has no `ledger_ok` in g6.
  Actual line 351: `base_ok = base_ok and (PINS["base-knowledge-content"] is None or cont == PINS["base-knowledge-content"])`.
- The battery's G6b (`r46-mutbat.py` C2_MUTANTS) drops `len(everything) == 65 and nested == 65` from the g6 return:
  `return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized),` ->
  `return (len(names) == 65 and base_ok and sized),`. The content pin is not touched.
- The battery accepts "equivalent" when `mid in eq and os.path.isfile(eq[mid])`; it never checks that the proof argues
  the mutant. So the verdict rests on the file's existence.

Independent argument (not committed; equivalence holds): `PINS["base-knowledge-names"]` = `bf3044814698b31b…` equals the
sha of exactly the 64 pure base names (checked on the 914ca0b export: `sha256("\n".join(sorted(names))+"\n")` =
`bf304481…`). `base_like` = knowledge entries minus the F28 entry `p`, and `p` is a regular non-symlink directly in
`corpus/knowledge` (`entry_path`). So `base_ok and sized` forces `everything` = 65 entries. `names == 65` with the
symlink guard (`if links or not grown: return False` runs before the return) forces all 65 to be regular `.md` files and
no subdirectories, so `nested == 65`. Both dropped conjuncts are implied on every tree.

Differential over 8 constructed trees (script `g6/g6diff.py` in scratch; `frozen` = head gate, `G6b` = mutant):

    base                       frozen=1 ... | G6b=1 ... | same
    subdir-md                  frozen=0 knowledge=65 entries=66 nested-md=66 base-intact=0 | G6b=0 ... | same
    extra-txt                  frozen=0 ... | G6b=0 ... | same
    extra-md                   frozen=0 knowledge=66 ... | G6b=0 ... | same
    dir-symlink                frozen=0 symlinks=1 ... | G6b=0 ... | same
    content-edit-pinned-exempt-no frozen=1 ... | G6b=1 ... | same
    pinned-file-moved-to-subdir frozen=0 ... | G6b=0 ... | same
    entry-replaced-by-dir      frozen=0 ... | G6b=0 ... | same
    differing readings: 0

So the equivalence is probably right, but the committed proof does not prove the battery's mutant. The C1 claim's
kill rule ("proof falsified by a constructed input") is not triggered; the "committed proof" condition is nominal for G6b.

## F7 — G7a / G7c equivalence: the argument holds on the census code but is conditional on an unpinned external script

The census is `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (outside the lane; not sha-pinned by the gate).
Code: `emit "$lane<TAB>ok<TAB>$f"` runs only when `lane_errors = 0` (line 745); the exit logic is
`[ missing_error = 1 ] && exit 2; [ findings = 1 ] && exit 1; exit 0` (lines 804–806). In `--file` mode the lane label
is the constant `file` (`resolve_targets`). Direct runs:

    $ bash sources-census.sh validate --file <96379ae>/corpus/SOURCES.md ; echo rc=$?
    ...
    file	ok	/fast/scratch/.../head/corpus/SOURCES.md
    rc=0            (ok-strict=1 ok-loose=1)

    $ (tier mutated to Z in a copy) bash sources-census.sh validate --file <copy>/corpus/SOURCES.md ; echo rc=$?
    file	E06	S001 tier=Z
    ...
    rc=1            (ok-strict=0 ok-loose=0)

`rc == 0 <=> ok line` holds on every reachable output, so G7a (`or`) and G7c (loose anchor) cannot change a verdict on
any input the lane builds. The committed proof says it "would require mutating the fleet census script", which is not
the argument. The real limit: the equivalence depends on a file outside the lane that the gate does not pin.
A later census edit (for example a different ok format) would silently make G7a/G7c non-equivalent.

## F8 — the selftest's --pure default and baseline are not reproducible from the stated base

- `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` (selftest line 54) does not exist (`ls` fails).
- With `--pure <04af9bc export>` the selftest fails its C1 precondition:
  `AssertionError: claim-gates.md` (selftest line 543). At 04af9bc the two C1 entries are byte-identical to the lane's
  (`sha256 93be63b0…` and `6f445bc3…` in both), so base cannot serve as its own pure.
- A pre-round corpus export (914ca0b, `pure2`; 64 knowledge files, F27 row present, no F28 row, C1 entries `06e2bd5c…` /
  `2233cd06…`) satisfies the precondition. The wave-1 scout recorded the same (`wave1/R46bScoutPureRecipe.md`).
- `controls/selftest-baselines.txt` ("cases=137 failures=0 at base") does not record the `--pure` it used.

## Recipes for L1 (scratch-built, none landed)

- R1: move `C1_ENTRIES = {...}` above `EXEMPT_ENTRIES` (selftest lines 68 and 69).
- R2: reconcile fixture and counter. Either the uncited 8th table row is not junk in the counter, or the fixture carries
  it as a counted row. Replace or re-base `ctl-committed-tip-direct` (5/7 at the F29-era tip); it can never read 7/7.
- R3: make the battery baseline grade `--root`: pass `--counter <root>/corpus/instruments/r46-c2-gate.py` and a
  root-relative `--lane` (the selftest hard-codes `LANE`).
- R4: rewrite the G6b proof around the pin arithmetic in F6; pin the census script sha (or record it in the proof) for G7a/G7c.
- R5: after R1–R3, the battery's c2 counts for G1c, G2a, G2b, G2c, G3a, G4b, G5c, G6a, G6c, G7b should each show the
  targeted `ACCEPTED-targeted-gate-passes` line (F5, J column).

## Limitations

- The selftests were run with `--pure` = 914ca0b corpus export (my own export), not the landed default (which does not
  exist). LANE-dependent parts (S073 snapshot/manifest, C1 entries, recheck line) read the live lane, whose corpus bytes
  equal 96379ae.
- All repairs (R1, junk-free counter, placement of counter copies with full instrument trees) were scratch-only
  diagnostics. Placing a counter copy without `source-recheck.py` beside it turned G4 red (TOOL_ROOT); that run was
  discarded and redone.
- The full battery could not run to completion on any repaired tree, because the committed-tip control keeps the
  baseline at 1 (F3). Per-mutant verdicts come from per-case lines, not from the battery summary.
- G6b / G7a / G7c equivalence: hand argument plus an 8-tree differential (G6b) and direct census runs (G7). Not exhaustive.
- The very first battery run (before I set `HYAKU_SCRATCH`) let the selftest use the shared seat directory
  `/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC2`; it crashed at import, so it created nothing I know of there.
- Tooling: no installs or updates; `python3`, `bash`, `git` read-only (archive, show, log, status, rev-parse).
