# R46bW2RevClaimC1 — end-to-end attack on the C1 verdict

VERDICT: BROKEN

Seat item: replay `controls/mutbat-before.txt` (before) against the integration values; audit the
equivalence entries used for the formerly-uncaught mutants (read the committed proof map);
falsify one proof by constructing the input class it claims impossible. Axis: depth:verifiability.
Tree under attack: lane `HEAD` = `96379ae26ef9443097b860ddb33ef924b2cd5b5a` ("wave-1
integration", the final lane revision; claims frozen at `fe0f56b`, byte-identical `claims.json`
verified by sha256 `ca73279f…`). Base `04af9bc9`, pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure2`.
All runs mine, in scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2RevClaimC1/` (removed at exit).
No installs (stdlib only). No git/jj mutation; lane instruments never written.

## F1 — BLOCKING: the c2 half of C1's after-value is unprintable at the final lane revision; the kill rule's `baseline_failures != 0` clause fires

Artifacts attacked: `corpus/instruments/r46-counters-selftest-c2.py` at the tip; the C1
after-value `mutbat counter=c2 mutants=21 caught+equivalent=21 uncaught=0 baseline_failures=0`;
control `controls/final-battery.txt`.

The committed c2 selftest crashes at import time at the tip. Lines 67–69 of the landed file:

```
LEDGER = "considerthese-proposals-ledger.md"  # …
EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # …
C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}  # …
```

`EXEMPT_ENTRIES` uses `C1_ENTRIES` one line before it is defined. Re-run (mine, tip export):

```
$ cd <tip export> && python3 corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
  File "…/corpus/instruments/r46-counters-selftest-c2.py", line 68, in <module>
    EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # …
                     ^^^^^^^^^^
NameError: name 'C1_ENTRIES' is not defined
exit=1
```

(`ast.parse` succeeds; the module body dies on execution. The defect was introduced by the L1's
integration merge — both source drafts are correct: `R46bExecSelftestC2.draft` has no LEDGER code
and a `selftest cases=147 failures=0` receipt; `R46bExecGatePinAmend.draft` has the correct order.
Corroborates peer `R46bW2RevSelftestW2` Finding 1; independently re-derived here.)

The battery therefore cannot grade c2 at the tip — the selftest prints no `failures=` line, the
battery's `run_selftest` returns its `-1` sentinel, and the c2 branch short-circuits. Exact
output of the committed battery (v1.1, default `--equivalent` = the committed map) at the tip:

```
$ python3 corpus/instruments/r46-mutbat.py --root <tip> --pure <pure2> --work w --counter c2 --jobs 4
mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1
```

The full `--counter both` run at the tip ends:

```
mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=1 verdict=caught
mutbat counter=c1 mutants=20 caught=19 equivalent=1 uncaught=0 baseline_failures=0
mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1
```

Kill rule, clause 1: "C1 fails if either battery summary at the final revision prints uncaught>0
or baseline_failures!=0". The c2 summary at the final revision is not printed at all; the printed
c2 result is `baseline_failures=-1` (≠ 0). The claim's own control receipt agrees the after-run
never completed: `controls/final-battery.txt` is untracked, stops at line 10 mid-header
(`== battery c1:`), and records this same NameError above an unexplained `exit=0` (the `run()`
helper's `$?` after the crashed command cannot be 0; the receipt is internally inconsistent).
No committed revision contains a completed after-battery
(`git cat-file -e <rev>:.ufo/waves/round-46/attempt2/controls/final-battery.txt` is absent at
`fe0f56b` and at `96379ae`).

## F2 — MAJOR: the frozen before-value is not reproducible at the base export today (c2 half); the frozen c2 selftest grades the live lane

Artifact attacked: `controls/mutbat-before.txt` (sha256 `13c21fcd…`, verified) as the
do-nothing/before control; command: the frozen v1 battery bytes
(`git show fe0f56b:corpus/instruments/r46-mutbat.py`, sha256 `f7a7cdfa…`, verified) over a base
export:

```
$ python3 mutbat-v1.py --root <base 04af9bc9 export> --pure <pure2> --work w-before --counter both --jobs 8
```

c1 half — reproduced BYTE-IDENTICAL. `diff` of my lines 1–21 against receipt lines 1–21 prints
nothing; both read `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`
with all 20 per-mutant lines equal (M01=26 … M20=0 uncaught).

c2 half — NOT reproducible. My run prints:

```
mutbat counter=c2 BASELINE-DIRTY baseline_failures=1
```

with the base selftest's own tail showing the single failure (all 137 cases ran, exactly one):

```
FAIL control ctl-committed-tip-direct fixed=5/7 failing=['G1', 'G6']  <- control-not-7/7 failing=['G1', 'G6']
       gate G1 pass=0 read=rows=29 admitted=29 dup=0
       gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
selftest cases=137 failures=1
```

Root cause (read from the frozen base selftest, `base/corpus/instruments/r46-counters-selftest-c2.py`):
line 537 `add(Case("ctl-committed-tip-direct", "control", direct=True, …))` runs the counter on
`--lane` itself, whose default (line 46) is the hardcoded LIVE lane path
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. When `mutbat-before.txt` was generated the live
lane still read the freeze-era state (28 rows / 65 entries → this control passed 7/7). Today the
live lane is `96379ae` (29 rows / 66 entries — moved by THIS round's landing, exactly the two
limbs erratum E3 names), so the era counter reads 5/7 there and the battery's c2 baseline is
dirty. The receipt was honest when written but is time-dependent: the before-value does not "stay
reproducible at the base export" (kill-rule parenthetical). The battery invokes the selftest
with no `--lane`, so no rerun of the frozen battery can grade the c2 mutants at base while the
live lane is past the freeze.

Discriminator against a do-nothing control: it does NOT grade uncaught=0 — c1 at base reads
uncaught=7 (exact replay above) and c2 cannot grade at all. The after-value is not a do-nothing
artifact; it is broken for the separate reason in F1.

## F3 — the equivalence entries for the formerly-uncaught mutants survive falsification (proof map sound)

Artifact attacked: `corpus/instruments/r46-mutant-equivalents.json` (4 entries: M14 →
`M14-L6-exit-ignored-receipt.txt`; G6b, G7a, G7c → `G6b-G7a-G7c-equivalence-probe.txt`) and the
claims' kill clause "a reviewer who builds an input class where the mutated clause changes a
verdict kills that equivalence". All four proof files exist, are non-empty, and match the
battery's actual triples. I attempted to falsify each by constructing the claimed-impossible
input class; every attempt failed, and in three cases I proved impossibility from the code:

- **M14-L6-exit-ignored** (`r46-c1-gate.py:337` drops `p.returncode == 0 or`). Claimed-impossible
  class: a tree where the L6 re-run exits 0 while `red == [r[0]]` (would make the unmutated
  predicate True and M14's False). Impossible: `entry_mode` returns 0 only when
  `ok == len(rows)` (its printed per-row `ok=0` set is then empty), so `rc==0 ⟹ red==[]`, and
  `[] != [r[0]]` is true for every row — the two survivor tests coincide on every input.
  Empirical differential (mine, battery-style mutant copy at `<dir>/corpus/instruments/` run with
  `--root <tip export> --baseline <pure2>`): frozen and M14 outputs are byte-identical,
  `c1-gate fixed=7/7 exit=0` both. (An early mis-laid mutant copy — two directory levels instead
  of three — mis-resolved `TOOL_LANE` and flipped every limb; that is a scratch-layout artifact,
  not a verdict difference; the battery's own `apply_mutant` copies the whole instruments tree
  precisely to avoid this.)

- **G6b-integrity-loose** (the battery's real triple edits the g6 return, dropping
  `len(everything) == 65 and nested == 65`). Claimed-impossible class: names==65 ∧ base_ok ∧
  sized ∧ (everything≠65 ∨ nested≠65). Impossible: `base_ok` includes a sha pin over the sorted
  FULL listdir minus the entry, so any extra/missing/renamed/nested item breaks the name pin
  first (both gates reject); given names==65 ∧ everything==65 ∧ no symlinks ∧ grown, every item
  is a regular `.md` and `os.walk` sees exactly those 65 files, so nested==65 follows. Constructed
  differential (pure base tree + `corpus/knowledge/zz-extra.md`): frozen and G6b-mutant gates
  both read `gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 …` —
  identical. NB documentation defect: the proof dir `README.md` describes G6b as dropping "the
  v1.3 gate's content-pin and ledger-floor conjuncts" — that is NOT the battery's triple; had it
  been, a one-byte flip of any pinned knowledge file would flip the verdict and the equivalence
  would be dead. The map's target file (the probe) and my differential both match the actual
  triple; the README prose is wrong and should be corrected, but no proof the claim relies on is
  falsified.

- **G7a-verdict-or / G7c-okline-loose** (`rc == 0 and ok_line` → `or`; `^\S+\tok\t` → `^\S+\tok`).
  Claimed-impossible class: a census run with rc==0 but no ok line, or rc!=0 with one. I read the
  fleet script `scripts/sources-census.sh` (806 lines) validate path: with `--file` the lane
  field is the literal `file`; a clean lane always emits `file\tok\t<f>` (`emit "$lane\tok\t$f"`
  only when `lane_errors=0`) and exits 0; any E finding prints only E/W lines (no ok line) and
  exits 1; `die` paths exit 2 with an `ERROR: …` stderr line that never matches `^\S+\tok` even
  though the gate's `run()` merges stderr into the regexed text; the gawk-failure path discards
  partial output before dying. So ok-line ⟺ rc==0 on every reachable output, and the ok line
  always carries the strict tab shape, making the loose regex coextensive with the strict one.
  Constructed differential (my own trees): a SOURCES.md with a 10-cell registry row
  (`census-rc=1 ok-line=0`, G7=0 both gates); the real lane's warning-bearing SOURCES.md
  (`census-rc=0 ok-line=1`, G7=1 both); a header-only registry (`rc=1 ok-line=0`, G7=0 both) —
  frozen vs a double G7a+G7c mutant copy read identically on all three.

## F4 — the c1 half of the after-value HOLDS (for completeness of the end-to-end attack)

Tip battery, c1 (quoted in full in F1's block): all six formerly-uncaught mutants now read
caught with the extended selftest (M06=2, M07=1, M13=2, M18=1, M19=1, M20=1 — matching the
dedicated-case receipts `wave1/R46bExecSelftestC1.draft/receipts/03-mutant-*.txt` and the kill
clause "a case that passes under its own mutant tests nothing" in the negative), the 13 old
catches regress cleanly (counts ≥ the before values: M01 27≥26, M02 9≥8, M04 26≥25, M15 2≥1,
rest equal), M14 reads `equivalent` via the committed map, summary
`caught=19 equivalent=1 uncaught=0 baseline_failures=0`. The extended c1 selftest is
byte-identical to its wave-1 draft (diff empty) whose receipt reads `selftest cases=83 failures=0`;
a dirty c1 baseline would have printed BASELINE-DIRTY and skipped grading, as the c2 branch
demonstrates — so the graded c1 run itself attests a clean 83-case baseline.

## Minor (not claim-killing, listed for the L1)

- The claims' plain measure `grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py
  corpus/instruments/r46-counters-selftest-c2.py` prints `0 0` at base, freeze, and tip — the
  extended selftests enumerate a `CASES` tuple table, not `def case_` functions. The measure is
  vacuous as committed (the real tallies come from each selftest's own `cases=N` line).
- `claims.json` names `.ufo/waves/round-46/attempt2/controls/freeze-controls.txt` as the C1/C2
  control; that file was never committed (`git ls-files .ufo/waves/round-46/attempt2/controls/`
  lists nine files, `freeze-controls.txt` not among them; only the wave-1 executor's draft copy
  exists). The after-receipt `controls/final-battery.txt` is likewise uncommitted and truncated.

## Limitations

- F2's c2 before-grading could not be re-derived today because of the live-lane drift; the
  drift's mechanism is pinned by the frozen selftest's own printed tail (137 cases ran, exactly
  one failure, the live-lane control). The c2 before-lines stand as a historical receipt only.
- The G6b/G7a/G7c probe script is not committed (only its output txt); my differentials
  independently reproduce its frozen-vs-mutant readings on trees I constructed.
- I did not re-run the c1 selftest standalone (host at >110 load from sibling seats); the clean
  c1 baseline is entailed by the battery's grading behaviour and corroborated by the
  byte-identical draft receipt quoted in F4.
- The M14/G7 mutant copies for my differentials were built by hand in battery layout
  (`<dir>/corpus/instruments/`); a first mis-laid copy mis-resolved `TOOL_LANE` and was
  discarded (recorded in F3).
