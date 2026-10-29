VERDICT: DRAFT-READY

# R46bMutSelfC2a — mutation-test of `r46-counters-selftest-c2.py` against the 21 `C2_MUTANTS`

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Read-only on the lane; all writes under
`/fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/` (removed at exit) and this seat's draft dir
`.ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/`. No commits, no pushes, no mutating
git/jj. The counters and the frozen claims were not edited. No tools were installed (none needed).

## 0. What was attacked, and with what

**Target under test.** The C2 counter's selftest
`corpus/instruments/r46-counters-selftest-c2.py` (committed tip, sha256
`ff7104cfc891007160c6e474bf1f3b00a9e0b25e6ca9aed96559ea648c2b688f`, 619 lines, 137 cases).
The extended draft `wave1/R46bExecSelftestC2.draft/r46-counters-selftest-c2.py` (the seat that
extends it) had **not landed** at the time of this run, so the committed selftest is the target.

**Mutants.** The 21 `C2_MUTANTS` of the frozen battery
`corpus/instruments/r46-mutbat.py:69-91` (sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`,
the frozen v1). I imported that table and the battery's own `apply_mutant` (which asserts the
old-substring occurs **exactly once**, so a drifted counter fails loudly instead of mutating the
wrong line) rather than re-typing the mutants, so the mutant set cannot drift from the frozen one.

**Instrument bytes graded.** `corpus/instruments/r46-c2-gate.py` sha256
`647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909` — identical before and after
my run (`receipts/lane-hashes-before.txt` vs `receipts/lane-hashes-after.txt`); `git status --short corpus/`
is empty. The lane tree was never written.

**Base export.** `pure` = a byte copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure2` (never edited,
never written) — the round-45-shaped base the claims' canonical battery command uses.
Hazard worth recording: the selftest's built-in default `PURE` is `/fast/scratch/hyaku/kasegi-r46/L1/pure`,
which **does not exist**; every invocation must pass `--pure .../L1/pure2` explicitly.

## 1. Baseline — the committed selftest is clean

Command:
```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py \
    --pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure
```
Printed (tail):
```
ok   control ctl-c1-landed-two-entries fixed=7/7 failing=[]
ok   control ctl-committed-tip-direct fixed=7/7 failing=[]
probe       probe-entry-pad-is-garbage-bytes fixed=7/7 failing=[] (ACCEPTED) -- G6 floor is bytes, not content
selftest cases=137 failures=0
```
`failures=0`, exit 0. The battery's own baseline arm reproduces the same (`BASELINE ... baseline_failures=0`).
**A dirty baseline would have made every mutant verdict inconclusive**, so this is the precondition
for the whole table.

## 2. The table — `mutant -> failures`

Run (my own parallel driver, `draft/drv.py`; it reuses the frozen battery's mutant table and
`apply_mutant`, and runs the 21 mutants 7-at-a-time because the frozen runner is serial):

```
python3 /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/drv.py \
  --selftest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-counters-selftest-c2.py \
  --pure /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/pure \
  --work /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/work --jobs 7 \
  --out /fast/scratch/hyaku/kasegi-r46/R46bMutSelfC2a/receipts/c2-mutant-table-committed.txt
```

`failures` = the number of selftest cases that FAIL under that mutant (`failures=0` ⇒ the selftest
did not notice the counter's defect).

| mutant | failures | verdict | why (measured) |
|---|---|---|---|
| `G1a-counts-loose` | 2 | caught | caught by an existing case |
| `G1b-path-dropped` | 5 | caught | caught by an existing case |
| `G1c-src-boundary` | 0 | **failures=0** | LIVE on G1 — F28 sources cell says S0730 |
| `G2a-verified-prefix` | 0 | **failures=0** | LIVE on G2 — verified-at carries a trailing comment |
| `G2b-wordfloor-low` | 0 | **failures=0** | LIVE on G2 — a 9-word Limits section |
| `G2c-need-empty` | 0 | **failures=0** | LIVE on G2 — Overlap cites two NON-required knowledge files |
| `G3a-cells-loose` | 0 | **failures=0** | LIVE on G3 — 12-cell row, extra cell appended at the END (proved e2e) |
| `G3b-scope-words-low` | 1 | caught | caught by an existing case |
| `G3c-kind-dead` | 94 | caught | caught by an existing case |
| `G4a-manifest-unpinned` | 1 | caught | caught by an existing case |
| `G4b-quotes-low` | 0 | **failures=0** | LIVE on G4 — 7-quote manifest, grader-side repin |
| `G4c-distinct-dropped` | 2 | caught | caught by an existing case |
| `G5a-span-wide` | 1 | caught | caught by an existing case |
| `G5b-words-wide` | 2 | caught | caught by an existing case |
| `G5c-pass-low` | 0 | **failures=0** | EQUIVALENT by arithmetic (cores==5 implies passed>=5) |
| `G6a-guards-dead` | 0 | **failures=0** | LIVE on G6 — an exempt entry present but SHRUNK |
| `G6b-integrity-loose` | 0 | **failures=0** | EQUIVALENT by construction (nested==65 is implied) |
| `G6c-size-low` | 0 | **failures=0** | LIVE on G6 — the entry file is under the 3000-byte floor |
| `G7a-verdict-or` | 0 | **failures=0** | EQUIVALENT relative to the FLEET census contract (outside the lane) |
| `G7b-symlink-dead` | 0 | **failures=0** | LIVE on G7 — corpus/SOURCES.md is a symlink |
| `G7c-okline-loose` | 0 | **failures=0** | EQUIVALENT relative to the FLEET census contract (outside the lane) |

**Summary line** (my run):
```
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
SURVIVORS failures=0: G1c-src-boundary G2a-verified-prefix G2b-wordfloor-low G2c-need-empty G3a-cells-loose G4b-quotes-low G5c-pass-low G6a-guards-dead G6b-integrity-loose G6c-size-low G7a-verdict-or G7b-symlink-dead G7c-okline-loose
```

**Independent reproduction of the frozen before-value.** I diffed my per-mutant
`(baseline_failures, mutant_failures)` pairs against the frozen receipt
`.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (the L1's own battery run at
the freeze point): `DIFFERENCES (frozen, mine): NONE - my independent run reproduces
the frozen before-value exactly` (21/21 mutants compared). The claim's
`expect_before` (`caught=8 equivalent=0 uncaught=13 baseline_failures=0`) is therefore
reproduced by a run of my own, not merely quoted.

**Disclosure on the driver's own exit.** All 21 mutant lines above are the driver's own printed
output. The driver then raised `TypeError: not all arguments converted during string formatting`
on its *summary* line (a format-string arity bug in my driver, at `drv.py:97`, fixed afterwards);
the summary line shown above was recomputed from the 21 printed mutant lines by the same script
that produced the diff. No measurement is affected: every per-mutant number is the driver's
verbatim output, and the crash happened after the last one. `draft/drv.py` is shipped with the
bug fixed.

## 3. Control — the grading is not vacuous

Three independent controls, all in `draft/controls.txt`:

**(a) The selftest's own do-nothing control.** `--do-nothing-control` swaps in a stub counter that
always prints 7/7:
```
selftest cases=137 failures=118
```
118 of 137 cases fail against a counter that can never say red. The cases really do grade the
counter's own verdicts.

**(b) My own do-nothing control** (`draft/noop.py`) — a **byte-level** change to the counter with
**no behaviour change** (a trailing comment appended to a scratch copy):
```
control=no-op-append-comment counter_bytes_before=20598 counter_bytes_after=20659
mutant=NOOP-append-comment baseline_failures=0 mutant_failures=0 verdict=UNCAUGHT
mutant=PRISTINE baseline_failures=0 mutant_failures=0 verdict=UNCAUGHT
DO-NOTHING CONTROL OK: behaviour-neutral change graded failures=0 (grading is not vacuous)
```
So a "caught" verdict is caused by **behaviour**, not by the mere fact that the counter file's bytes
changed. (This is the discrimination the seat item asks for: without it, a selftest that flagged any
byte difference would look like full coverage.)

**(c) Probe power** (`draft/discriminating.py`) — the liveness probe's negative and positive arms:
```
NEGATIVE CONTROL (docstring-only edit): gates that differ = [] -> probe power OK
POSITIVE CONTROL (G1c on an S0730 sources cell): gates that differ = ['G1']
```
An inert edit flips no gate; a live edit flips exactly the gate it targets.

## 4. `failures=0` survivors — which are REAL holes and which are provably equivalent

`failures=0` alone does not say *why*. For each survivor I ran a **liveness probe**
(`draft/probe.py`): build the tree with the committed selftest's *own* builder, apply ONE isolating
defect, then run the **pristine** counter and the **battery-exact mutant** counter on the *same* tree.
A gate that is red under pristine and green under the mutant is an **observable** difference — a
selftest case targeting that gate (allowing the other red gates as collateral) would catch the mutant.
Full transcript: `draft/liveness-probes.txt`.

**Live differentials — the mutant changes a verdict that the selftest never grades.**
For each of these I built ONE isolating tree, ran the pristine counter and the battery-exact mutant
counter on it, and observed the target gate flip red→green. The verbatim probe output is in
`draft/liveness-probes.txt`.

| mutant | gate that flips | isolating defect (the tree the case must build) |
|---|---|---|
| `G1c-src-boundary` | G1 | F28's sources cell says `S0730` (pristine `\bS073\b` rejects it; the mutant's `S073` accepts it) |
| `G2a-verified-prefix` | G2 | the entry's provenance line is `verified-at: 2026-10-28 (reviewed)` (pristine wants equality, the mutant accepts a prefix) |
| `G2b-wordfloor-low` | G2 | the `## Limits` section carries 9 words (>= the mutant's floor 5, < the pristine floor 25) and keeps its `S073.txt` anchor |
| `G2c-need-empty` | G2 | Overlap's two `corpus/knowledge` cross-references name `claim-gates.md` and `claim-package-contract.md` instead of the two required files |
| `G3a-cells-loose` | G3 | a 12-cell S073 row with the extra cell appended at the END — proved end-to-end in §5 |
| `G4b-quotes-low` | G4 | the manifest keeps 7 quotes (Q1 removed) and a grader-side `R46_PINS_OVERRIDE` re-pins the edited manifest |
| `G6a-guards-dead` | G6 | `corpus/knowledge/claim-gates.md` is present but shrunk to 9 bytes (the names pin and content pin still hold) |
| `G6c-size-low` | G6 | the entry file is present but under the 3000-byte floor |
| `G7b-symlink-dead` | G7 | `corpus/SOURCES.md` is a symlink (pristine refuses a symlinked census input) |

Nine of the thirteen `failures=0` survivors are therefore **real coverage holes with a concrete
isolating input** — a new selftest case exists for each. The other four are the equivalence
arguments in §4.1.


### 4.1 Equivalence proofs (the survivors whose clause is DEAD, not merely uncovered)

**G5c-pass-low (`len(passed) >= 4` → `>= 1`) — EQUIVALENT by arithmetic.**
G5 requires `len(cores) == 5`. A located span is capped at 25 words (the pristine G5b limit), so the
minimum word count for one span to hold two of the five frozen cores, measured over the real capture
(all 10 pairs, `draft/equiv.py`):
```
enabled+form=185  enabled+ai=212  enabled+credit=278  enabled+merge=302
form+ai=35        form+credit=101 form+merge=125
ai+credit=70      ai+merge=94     credit+merge=30
```
Every pair exceeds 25 words ⇒ no two cores can share a span ⇒ `cores==5` implies `passed>=5` ⇒ the
`>=4` conjunct is implied by the `cores` conjunct and can never be the sole red limb. The mutant
cannot change any verdict on any input.

**G6b-integrity-loose (drops `nested == 65`) — EQUIVALENT by construction.**
`g6` computes `names` (top-level `.md` regular files), `everything` (all top-level entries, incl.
directories) and `nested` (`.md` files found recursively). The mutant keeps
`len(names)==65 and len(everything)==65`. If both hold then **all 65 top-level entries are `.md`
regular files**, so no subdirectory exists at the top level, so `os.walk` finds exactly those 65 and
`nested==65` follows. The dropped conjunct is implied by the two the mutant keeps.

**G7a-verdict-or / G7c-okline-loose — EQUIVALENT relative to the census contract (not isolable from inside the lane).**
Both grade the **census output**, and the census script lives **outside** the lane
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`; the counter hardcodes that absolute path
in `CENSUS`), so the committed selftest cannot redirect it. Measured on three trees (clean, an
E-code tree, a W-code tree):
```
### clean     G7a pristine_G7=1 mutant_G7=1 | mutant read='census-rc=0 ok-line=1'
             G7c pristine_G7=1 mutant_G7=1 | mutant read='census-rc=0 ok-line=1'
### E-code   G7a pristine_G7=0 mutant_G7=0 | mutant read='census-rc=1 ok-line=0'
             G7c pristine_G7=0 mutant_G7=0 | mutant read='census-rc=1 ok-line=0'
### W-code   G7a pristine_G7=1 mutant_G7=1 | mutant read='census-rc=0 ok-line=1'
             G7c pristine_G7=1 mutant_G7=1 | mutant read='census-rc=0 ok-line=1'
```
On every input I could construct `rc==0 <=> ok_line`, so `rc==0 or ok_line` ≡ `rc==0` ≡ the
original, and the census's only ok emission is `file<TAB>ok<TAB><path>`, which matches both regexes.
Byte note: the G7c mutant's replacement pattern is `r"^\S+\tok"` — **TAB** + `ok`, a valid escape,
not `\o`; I checked the raw bytes of both the battery line and the counter line to be sure.

## 5. One disagreement with the sibling gap analysis, resolved by execution

The sibling scout (`wave1/R46bScoutSelftestC2Gap.md`, E1) classes **G3a-cells-loose** as
"equivalent-by-construction", on the argument that a row with ≥12 cells "shifts the mined/date/
recheck/used-by literals off positions 7-10". My probe contradicts that: appending the extra cell at
the **END** of the row leaves positions 0..10 untouched. Verified on the actual builder's row:
```
cells: 11     0 S073  1 <url>  2 docs  3 A  4 scope  5 anchor  6 teaches  7 mined  8 2026-10-28  9 180d  10 <used-by>
after append-at-end cells: 12   ...  7 mined  8 2026-10-28  9 180d  10 corpus/knowledge/github-private-vulnerability-reporting.md  11 extra
row[10] = 'corpus/knowledge/github-private-vulnerability-reporting.md'   used-by still at index 10? True
```
The counter reads `row[7]` (status), `row[8]` (opened), `row[9]` (recheck) and `row[10]` (used-by)
(`corpus/instruments/r46-c2-gate.py:263,266,267,270`), so all four stay satisfied. My probe measured:
```
pristine: c2-gate fixed=5/7 exit=1  gates={'G1': 1, 'G2': 1, 'G3': 0, ... 'G7': 0}
mutant:   c2-gate fixed=6/7 exit=1  gates={'G1': 1, 'G2': 1, 'G3': 1, ... 'G7': 0}
```
G7 is collateral-red in both (the extra cell also breaks the census's 13-field contract), but **G3
itself flips**, which is what a case targeting G3 (with G7 allowed as collateral) grades.

**End-to-end proof** (`draft/g3a-e2e.txt`): I copied the committed selftest to scratch, added ONE case,
and ran it against both counters.

```
scratch selftest written: .../g3a-uz0yider/selftest-ext.py
EXTENDED selftest vs PRISTINE counter: failures=0
    ok   mutant  mut-s073-row-twelve-cells-extra-at-end fixed=5/7 failing=['G3', 'G7']
EXTENDED selftest vs G3a MUTANT counter: failures=1
    FAIL mutant  mut-s073-row-twelve-cells-extra-at-end fixed=6/7 failing=['G7']  <- ACCEPTED-targeted-gate-passes=['G3']

VERDICT: the new case CATCHES the G3a mutant (failures 0 -> 1)
```

The case (one line, existing selftest symbols only):
```python
add(Case("mut-s073-row-twelve-cells-extra-at-end", "mutant",
    lambda r: sub(r, SOURCES, line_of(r, SOURCES, "| S073 |"),
                   line_of(r, SOURCES, "| S073 |")[:-1] + " | extra |"), {"G3"}, allow={"G7"}))
```

So **G3a-cells-loose is FIXABLE with a new case, not equivalent** — this corrects the sibling's E1
classification. Practical consequence for the wave: if G3a is banked as an equivalence proof, the
counter keeps a real hole (a registry row with a trailing extra cell passes the C2 registry limb).


## 6. Limitations

1. **The extended C2 selftest draft had not landed** when this run finished. The table is the
   committed selftest's coverage. When `wave1/R46bExecSelftestC2.draft/r46-counters-selftest-c2.py`
   lands, the same driver re-runs against it unchanged (`drv.py --selftest <draft path>`); the
   survivors' *fixability* (the isolating defects in §4) is what carries over, not the failure counts.
2. **The battery's `equivalent` arm was not exercised.** `r46-mutbat.py` accepts an
   `--equivalent` map of id → committed proof file. No such map exists yet, and the claim's kill rule
   requires the proof files to be **committed**. My equivalence arguments in §4.1 are written out in
   this report and in `draft/equiv.py`, but they are **not yet committed proof files**, so under the
   battery's predicate G5c, G6b, G7a and G7c still read `uncaught` until they are.
3. **G7a/G7c equivalence is relative to the fleet census, not to the lane.** The census script lives
   at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane; the lane cannot
   change it, and I did not. If that script's ok-line contract changes, both mutants become live
   again. This is a coupling to an external file, and I flag it rather than claiming a lane-local proof.
4. **The load.** The host ran at load 160–270 on 32 cores during this window (dozens of sibling
   seats running their own batteries), so a single selftest run took ~8–25 minutes and the whole
   21-mutant table took hours of wall time. The measurement is unaffected — each mutant run is
   independent and its `failures` count is exact — but I could not run the extended-selftest arm or
   additional mutant sets beyond the 21.
5. **My liveness probes use the selftest's builder, so a probe verdict is only as good as that
   builder's fidelity to the real tree.** I cross-checked it with the negative/positive controls in
   §3(c) and with the end-to-end run in §5.
6. **I did not test the F29 counter or the f29 selftest** — outside this seat's item (the C2 counter's
   selftest vs the C2 battery table).

## 7. Report file

Findings and receipts: this file, plus the draft dir
`.ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/` (receipts `c2-mutant-table-committed.txt`,
`liveness-probes.txt`, `controls.txt`, `lane-hashes-before.txt`, `lane-hashes-after.txt`, and the
driver/probe scripts `drv.py`, `probe.py`, `noop.py`, `equiv.py`, `discriminating.py`, `g3a_e2e.py`).
