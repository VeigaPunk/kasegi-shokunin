# R46bW2RevSelftestW2 — diff-audit of the extended selftests at the integration tree

VERDICT: BROKEN

Seat item: diff-audit the extended selftests at the integration tree (freeze `fe0f56b`, landed tip
`96379ae` "wave-1 integration — … instruments (selftests 83/147 …)") against their committed wave-1
drafts; every case the L1 changed or dropped during integration is a finding unless a receipt shows
it failing identically; re-run the extended baselines and quote the tallies.

Trees used (read-only `git archive` exports under scratch, removed after the run):
base `04af9bc9`, freeze `fe0f56b`, tip `96379ae` (= lane HEAD; `git status --porcelain` on
`corpus/instruments` is empty). Pure base export for the selftests: the L1's own
`/fast/scratch/hyaku/kasegi-r46/L1/pure2`.

## Finding 1 — BLOCKING: the committed C2 selftest crashes at import; the L1's integration merge
introduced the crash and no receipt excuses it

Artifact attacked: `corpus/instruments/r46-counters-selftest-c2.py` at the integration tree.

The L1 changed the file after wave 1. Both source drafts are correct; the landed file is not:

- Executor draft `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/r46-counters-selftest-c2.py`
  (sha256 `0457a1926d766d73297aa07b2997a4fd79037bed5201501e1310de3cd869c281`): no LEDGER code,
  runs clean (its receipt `selftest-baseline-147.txt`: `selftest cases=147 failures=0`).
- Pin-amend draft `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py`
  (sha256 `37a723c0952af8523f17e79e949e2e3670783dc126dc1f35047d653b9c73814a`): has the LEDGER
  exemption with the CORRECT order — `C1_ENTRIES = …` (line 61), `LEDGER = …` (62),
  `EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}` (63).
- Landed file (sha256 `9b13b6b31b49e5f04339fa14177cc4c2f32c2620eb85289ae30f0aa4d5f04a3d`): the merge
  MOVED `C1_ENTRIES = …` to AFTER `EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}` (lines 67–69):

```
ALL = {f"G{i}" for i in range(1, 8)}
LEDGER = "considerthese-proposals-ledger.md"  # …
EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # …
C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}  # …
```

Re-run (mine, tip export):

```
$ python3 corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
    EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # …
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
RC=1
```

(The file parses — `ast.parse` succeeds — and dies only when the module body executes; a syntax
check alone does not catch it.)

This is a change made by the L1 during integration (errata E2 admits the merge: "the latter merged
with ExecGatePinAmend's v1.3 mirror"), and the excusing condition does not hold: no accompanying
receipt shows the draft "failing identically" — both drafts' receipts show `failures=0`, and the
L1's own integration receipt `controls/final-battery.txt` records the crash, not a pre-existing
failure:

```
== selftest c2 (extended+ledger):
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
exit=0
```

Note that receipt's `exit=0`: it comes from a `| tail` pipeline masking the crash's real exit 1.
The claims' own plain c2 command (`python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1`)
therefore prints a traceback tail and pipeline-exits 0 — the expected `cases=147 failures=0` line
never appears, and an adjudicator running the plain measures gets no tally and no error.

Consequence (claim-level): C1's after-condition "the extended selftests … keep `failures=0`
baselines at the final revision" is FALSE for c2 as landed, and the c2 battery grading is
unreachable: `r46-mutbat.py` `run_selftest` parses `failures=(\d+)` from stdout and returns -1 when
absent (lines 162–164), and `main` then prints `mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1`
and `continue`s (lines 395–401). So `expect_after`'s c2 line (`uncaught=0 baseline_failures=0`)
cannot be produced by the committed instruments at the tip.

Also in the same merge, the landed docstring misdescribes the harness: it says "The base's two C1
entries are the BASE bytes; `land_c1` swaps in the lane's re-grounded bytes" while the merged code
runs `for fn in sorted(EXEMPT_ENTRIES)` (three files, incl. the ledger). Cosmetic next to the crash,
but it shows the merge was not re-run.

## Finding 2 — BLOCKING even with Finding 1 fixed: the extended C2 selftest baseline cannot reach
`failures=0` against the committed v1.3 counter (101/147 fail, all on G2's new junk conjunct)

Artifact attacked: the compatibility of the extended selftest (either draft — the NameError is not
the cause) with the committed counter `corpus/instruments/r46-c2-gate.py` v1.3 (errata E3: adds
`junk == 0` to g2, line 246, "every table-shaped line must be a header, a separator, or a counted
row").

Discrimination runs (same draft file `0457a192…`, same pure export; only `--lane` differs):

```
$ python3 R46bExecSelftestC2.draft/r46-counters-selftest-c2.py --pure …/L1/pure2 --lane <fe0f56b export>
selftest cases=147 failures=0        # RC=0, 251 s — reproduces the executor receipt exactly

$ python3 R46bExecSelftestC2.draft/r46-counters-selftest-c2.py --pure …/L1/pure2 --lane <96379ae export>
selftest cases=147 failures=101      # RC=1, 360 s
```

`fe0f56b` and `96379ae` differ for this purpose only in the counter (both lanes' C1 entries are
byte-identical: `fe0f==tip claim-gates.md claim-package-contract.md`; the S073 capture is the
freeze capture). Verdict-token tally of the tip run: `101 FAIL / 46 ok`; every one of the 101
failures includes G2, e.g.:

```
FAIL control ctl-complete-tree fixed=6/7 failing=['G2']  <- control-not-7/7 failing=['G2']
       gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=7 xrefs=2/2
```

All G2 sub-reads are green yet the gate is red — exactly the v1.3 `junk == 0` conjunct firing on
the selftest's own synthetic entries (their quote tables contain rows the conjunct does not
"account": e.g. the cite-less `| {q} | no response time is stated | {c} |` row and rows with <2
word-cells or out-of-range cites; under v1.2 the same trees were fine because g2 only required
`tbl >= 6`). The wave-1 drafts were built and receipted against the v1.2 counter; errata E3 landed
the junk conjunct at integration and errata E2 nonetheless asserts "Baselines stay failures=0" —
that sentence is falsified for c2. No wave-1 c2 selftest draft (neither `0457a192…` nor the
pin-amend `37a723c0…`, same v1.2-era synthetic entries) can pass against the committed v1.3 counter.

## Non-findings / verified-clean items

- **C1 selftest: no case changed or dropped.** The committed file is byte-identical to the
  ExecSelftestC1 draft: sha256 `03079421b07639baabfc942ef4a022c9a8798ff8bc81f029d4b73c6a8b54e2fd`
  for both `R46bExecSelftestC1.draft/r46-counters-selftest-c1.py` and the tip export;
  `diff -u` is empty; the registered case-name lists are identical.
- **C2 selftest: no case dropped or renamed.** `add(Case("…"` registration names are identical
  between draft `0457a192…` and the landed file; the only landed delta vs the drafts is the
  LEDGER/EXEMPT_ENTRIES merge of Finding 1 (and the docstring merge quoted there).
- **C1 extended baseline re-run (mine, tip export):**
  `python3 corpus/instruments/r46-counters-selftest-c1.py --pure …/L1/pure2 --work $S/w-c1 --jobs 8`
  → `residual-false-greens=1 (…R-claim-text-unrelated-to-anchor)` / `selftest cases=83 failures=0`,
  real RC 0, 289 s. Matches the L1's `controls/final-battery.txt` ("selftest cases=83 failures=0")
  and the draft receipt `02-after-extended-selftest.txt`. Do-nothing discrimination is intact on
  both sides: c1 `CONTROL-do-nothing` reads `fixed=1/7 exit=1` and c2
  `null-pure-base-unmodified fixed=1/7 failing=['G1'…'G6']` in the same runs, while the synthetic
  tips read 7/7 — the new cases did not loosen the harnesses.
- **Draft C2 baseline against the freeze-era counter reproduces:** `cases=147 failures=0` (quoted
  above), matching `selftest-baseline-147.txt`.

## Secondary observations (not my item's primary surface)

- `controls/final-battery.txt` (374 bytes) ends mid-receipt at `== battery c1:` — it contains the
  c1 selftest tally and the c2 NameError, and NO battery output at all. The C1 after-value battery
  pair (`uncaught=0` both counters) has no committed receipt; the battery seats / L1 must produce
  it. As landed, the c2 battery leg will print `BASELINE-DIRTY baseline_failures=-1` (code path
  quoted in Finding 1), not `uncaught=0`.
- The claims' plain case-count measure `grep -c 'def case_'` prints `0` for both selftests at base
  and tip (cases are tuple-list/`add(Case(…))` registrations, not `def case_` functions), so that
  line of `claims.json plain` does not measure the "case-count move behind the tallies". Tallies
  themselves (83/147) are reproducible as quoted above.
- `r46-mutant-equivalents.json` values are repo-root-relative and `r46-mutbat.py` checks them with
  bare `os.path.isfile(eq[mid])` (CWD-relative): the equivalent verdicts for M14/G6b/G7a/G7c only
  resolve when the battery is invoked from the lane root. The proof files themselves exist and are
  non-empty (M14 receipt 682 B; G6b/G7a/G7c probe 3560 B).
- Equivalence-proof context for C1's "equivalent verdict names a committed proof" leg: the four
  proof files are committed under `corpus/instruments/r46-mutant-equivalents/`; content matches the
  wave-1 receipts (15-tree M14 differential, `differing=0`; G6b/G7a/G7c probe batteries). I did not
  re-execute those probes (they are the battery/equivalence seats' surface).

## Limitations

- I did not run the full `r46-mutbat.py --counter both` battery (41 full selftest invocations; the
  battery seats own that). The BASELINE-DIRTY consequence for c2 is established from the battery's
  own code plus the observed crash output, not from a battery run.
- The 101-failure diagnosis names the G2 junk conjunct via the gate read strings (all sub-reads
  green, `pass=0`, failing set always containing G2) and the conjunct's code; I did not bisect
  individual synthetic rows.
- No live-target testing, no writes outside this report and my scratch; scratch
  `/fast/scratch/hyaku/kasegi-r46/R46bW2RevSelftestW2` removed at yield. No tools installed.
