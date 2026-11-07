# MutC2Counter — mutation test of the frozen C2 counter (round 87, attempt 1, wave w1)

Seat: leaf mutation tester. Target: `.ufo/waves/round-87/c2/capability-check.py`,
sha256 `4fba0cbe98fff8524efaf9f8ccd8879a133632260820ee611b7253f3fccfead7`
(frozen bytes; nothing in the lane was edited).

Method: 19 single-point mutants, each one contiguous replacement of the frozen
source (each verified as exactly one `@@` diff hunk), scored against a scratch
re-implementation of the 12 scenarios of
`.ufo/waves/round-87/controls/c2-controls-r87.sh` (the 11 named controls plus
`scopewide-corpus`, which the frozen script also carries; `pin` reuses the
positive clone with a zeroed instrument pin). The frozen counter was run on the
same scratch clones first: its verdict vector reproduces the recorded
`controls/c2-controls-r87.txt` on 12/12 scenarios (`MISMATCHES=0`,
receipts/`baseline-vs-frozen-controls.txt`).

A **verdict** is the full observable result of one counter run: the printed
`CAPABILITY-CHECK-RESULT` line, the process exit code, and the five LIMB
pass/FAIL statuses. A mutant is **killed** when any scenario's verdict differs
from the frozen counter's on the identical clone. Kills are classified by level:
`exit` (process status flips: strong), `limb` (a LIMB status flips, exit
unchanged), `printed` (only the printed verdict line flips). Survivors are
routed defects below; they do not re-score C2.

## Results — 19 mutants, 12 killed, 7 survived

| # | clause mutated | verdict | killed by (scenario: frozen → mutant) | level |
|---|---|---|---|---|
| M01 | `HISTORY_EXPECTED` widened by one path | KILLED | positive: K2 pass → FAIL, rc 0 → 1 | exit |
| M02 | `HISTORY_EXPECTED` emptied | KILLED | positive: K2 pass → FAIL, rc 0 → 1 | exit |
| M03 | `ORACLE_RE` token floor `{20,}` → `{1,}` | SURVIVED | — | — |
| M04 | K2 `sts == oracle` → `sts <= oracle` | KILLED | gate-only: K2 FAIL → pass | limb |
| M05 | K3 `unused_allow == 0` conjunct dropped | KILLED | stale-row: K3 FAIL → pass, rc 1 → 0 | exit |
| M06 | K3 `allowed >= 1` conjunct dropped | SURVIVED | — | — |
| M07 | K4 exact hit set → `PLANT_EXPECT ⊆ hits` | KILLED | scopewide-corpus, whole-tree: K4 FAIL → pass | limb |
| M08 | K4 STS-refusal `rc2 == 2` dropped | KILLED | refusal-disabled: K4 FAIL → pass, rc 1 → 0 | exit |
| M09 | K5 last-cell `== "87"` dropped | SURVIVED | — | — |
| M10 | K1 selftest rc/string check dropped | KILLED | gate-only, path-only, scopewide, whole-tree: K1 FAIL → pass | limb |
| M11 | printed verdict polarity inverted | KILLED | all 12: printed `pass rc=0` ↔ `fail rc=1`; exit unchanged | printed |
| M12 | K2 `oracle == HISTORY_EXPECTED` dropped | SURVIVED | — | — |
| M13 | K1 both sha256 pins dropped | KILLED | wrong-pin: K1 FAIL → pass, rc 1 → 0 | exit |
| M14 | K3 `not hits` conjunct dropped | SURVIVED | — | — |
| M15 | K4 planted-run `rc == 1` check dropped | KILLED | always-clean: K4 FAIL → pass | limb |
| M16 | K5 `len(rows) == 1` → `>= 1` | SURVIVED | — | — |
| M17 | process exit polarity inverted | KILLED | all 12: exit flips (0 ↔ 1) | exit |
| M18 | `all(ok …)` → `any(ok …)` aggregation | KILLED | 10 negative controls: rc 1 → 0 | exit |
| M19 | `ORACLE_RE` collapsed to the bare header name | SURVIVED | — | — |

Full matrix (19 × 12, compact cells `verdictword|exit|K1P…K5P`), per-mutant
flip records, and mutant digests: receipts/`mutant-matrix.tsv`,
`mutant-detail.json`, `mutant-shas.txt`.

## What the kills show

- Model kills (M05, M08, M13): a negative control flips the whole verdict to
  pass, i.e. the battery's stated expectation is protected at the exit-code
  level by exactly one control each (stale row; refusal-disabled; wrong pin).
- M01/M02: the positive control flips to fail, so K2's expected set is
  protected at exit level.
- M04, M07, M10, M15 are killed only at the LIMB level: the control that
  observes the weakened clause also fails another limb, so `rc` stays 1. The
  frozen script records the per-limb expectation in prose ("expected fail
  K2,K4", …) but `check()` only echoes `rc=$?`; a gate that reads only the exit
  code would not stop these weakenings (routed as R8).
- M11 and M17 are the two single-point halves of "verdict polarity". M11
  inverts only the printed line (exit unchanged); M17 inverts only the return
  (print unchanged) and is caught by every control. Nothing in the battery ties
  the printed `rc=` field to the process exit, so M11 survives an exit-code
  reading while printing `fail` on the positive control (routed as R7).
- M18 (aggregation all→any) is caught by ten negative controls; the four that
  stay failing already have all limbs failing.

## Survivors and executed isolating controls (routed defects)

All mutants and fixtures stayed in scratch; the receipts carry only digests and
the scanner's HIT/summary lines. Five survivors were killed by purpose-built
controls run in scratch (`receipts/demonstrations.txt`); two are structural.

| survivor | clause removed | why the 12 controls cannot see it | isolating control (executed) | route |
|---|---|---|---|---|
| M06 | K3 `allowed >= 1` | the only `allowed=0` control (empty allowlist) also has `hits=4`, so K3 fails earlier on rc/hits | D1: clean capture scope (the four allowlisted values removed) + empty allowlist → `hits=0, allowed=0, unused_allow=0, rc=0`; frozen K3 FAIL/rc 1, M06 pass/rc 0 | R1 |
| M09 | K5 last cell `== "87"` | no control writes a row with a non-87 last cell | D2: same positive tree with row last cell `86`; frozen K5 FAIL/rc 1, M09 pass/rc 0 | R2 |
| M16 | K5 single-row requirement | no control writes two capability rows | D3: rows `…|87|` and `…|86|`; frozen K5 FAIL (rows=2)/rc 1, M16 pass/rc 0 | R3 |
| M14 | K3 `not hits` | no control produces an instrument that prints a HIT line while its summary says `hits=0` | D4: forged instrument prints one HIT line on a zero-hit scan, summary `hits=0 rc=0`; frozen K3 FAIL/rc 1, M14 pass/rc 0 | R4 |
| M12 | K2 `oracle == HISTORY_EXPECTED` | the oracle is computed at hardcoded `HISTORY_REV`; every control clones the same object store, so `oracle == HISTORY_EXPECTED` always holds | D5: oracle drift (PATH shim returns 1 history path for the `git grep` call) + scanner under-reporting to the same 1 file; frozen K2 FAIL (`oracle_matches_expected=False`), M12 pass/rc 0 — the clause is load-bearing under drift | R5 |
| M03, M19 | `ORACLE_RE` shape (token floor; `=`+value class; whole value) | any regex that keeps the file set at `HISTORY_REV` is indistinguishable; `{20,}`, `{1,}`, and the bare header name all return the same two files | not constructible with the frozen interface (no `--history-rev`); a regex-preserving weakening is invisible by construction | R6 |

Additionally, M11 shows the battery never asserts printed verdict == exit status.
Route R7: one assertion in the control harness.

### Routed defects (re-runnable recipes)

- **R1 — missing `allowed >= 1` control.** Add to `c2-controls-r87.sh`: clone
  base, place candidate scanner + an empty allowlist + row 87, then
  `git rm .ufo/waves/round-85/w1/ExecC1Hunt-receipts/{gone,hunt2}.json
  corpus/source-snapshots/round-49/S078.txt` and remove the placed
  `corpus/source-snapshots/round-87/S124.txt`, commit, run the counter: the
  frozen counter must print `LIMB K3 FAIL … allowed=0` and `fail rc=1`.
  Observed for D1 (clone rev `2afab637…`): frozen `fail rc=1`, M06 `pass rc=0`.
- **R2 — missing round-marker control.** Add: positive tree with the capability
  row's last cell `86`; frozen `K5 FAIL rows=1`, `fail rc=1` (D2, rev
  `40ec5093…`).
- **R3 — missing duplicate-row control.** Add: positive tree with two capability
  rows (`…|87|` then `…|86|`); frozen `K5 FAIL rows=2`, `fail rc=1` (D3, rev
  `911d8c08…`).
- **R4 — missing HIT/summary consistency control.** Add: an instrument that on a
  zero-hit scan prints one `HIT` line and a summary `hits=0 … rc=0`; frozen
  `K3 FAIL`, `fail rc=1` (D4, forged scanner sha256 `405251a1…`).
- **R5 — K2's oracle is untestable as parameterized.** The counter hardcodes
  `HISTORY_REV`; no control can drift the oracle. Add `--history-rev`
  (and, if a fixture lane is used, `--history-expected`) so a fixture history
  can exercise the `oracle == HISTORY_EXPECTED` guard. D5 proves the guard is
  load-bearing: with drift + an under-reporting scanner, the frozen counter
  fails K2 while M12 passes.
- **R6 — `ORACLE_RE` shape is unpinned.** With `--history-rev`, add a fixture
  history containing a 19-char token value and a header occurrence without a
  value; the oracle must exclude both. Today `ORACLE_RE` can be reduced to the
  bare header name (M19) and all 12 controls still pass; `K2`'s
  `oracle == HISTORY_EXPECTED` only bounds drift that changes the file set.
- **R7 — printed verdict vs exit status.** The recorded controls show both
  `CAPABILITY-CHECK-RESULT … rc=N` and `rc=$?`, but nothing compares them. Add
  `assert printed_rc == exit` to the control harness: M11 then fails every
  scenario instead of only being visible to a reader.
- **R8 — limb-level kills are not exit-code-visible.** M04 (gate-only K2), M07
  (scopewide/whole-tree K4), M10 (four controls' K1), M15 (always-clean K4) do
  not change any control's exit code. If the freeze gate reads only `rc`, add
  isolating controls: an under-reporting history scanner (K2), a planted repo
  with an extra flagged hit but a clean K3 (K4 exactness), a scanner that fails
  selftest while scanning correctly (K1 selftest), and a scanner that reports
  the exact planted set while exiting 0 (K4 rc).

## Claim impact (not a re-score)

C2's predicate P1 is evaluated at the landing commit against these exact frozen
counter bytes, whose sha256 is pinned in `claims.json`; no survivor changes the
C2 verdict at the landing commit. The survivors are pre-freeze battery coverage
gaps: a future counter edit that drops these conjuncts would pass the frozen
battery, and the only post-freeze guard is the sha256 pin, not behaviour.
Qualifier: the M04, M07, M10 and M15 weakenings are observed only through a
limb status while the harness records `rc` as the verdict, so "expected fail"
in `c2-controls-r87.txt` is not machine-asserted at that level.

## Reproduction and run ledger

Commands (scratch, absolute; receipts hold the exact clone revisions):

```
S=/fast/scratch/hyaku/kasegi-r87/MutC2Counter
# baseline (frozen counter, 12 scenarios, parallel -P 8)
bash run-battery.sh $S/base/capability-check.py base
# each mutant
bash run-battery.sh $S/mutants/<Mnn-name>.py <Mnn-name>
python3 -B score.py ; python3 -B verify-baseline.py
```

Counts: 12 baseline runs + 19 × 12 = 228 mutant runs + 10 demonstration runs
(5 controls × frozen/mutant) = 250 scored counter invocations. Wall clock:
baseline 33 s; 19 mutant batteries 3 m 10 s + 30 s at `-P 4` outer / `-P 8`
inner on 32 cores; demonstrations 21 s. The whole-tree-scope control ran once
per mutant (26.5 s each). Tooling: none installed; `python3 -B` and read-only
`git`; fixture repos created with `git init` inside scratch only, toplevel
asserted before every commit.

Restoration evidence: the frozen counter's sha256 is unchanged before and after
(`4fba0cbe…`, re-checked at yield); every mutant and fixture lived under
`/fast/scratch/hyaku/kasegi-r87/MutC2Counter` and that tree was removed at
exit; the lane tree received only this report and its receipts.

## Files written

- `.ufo/waves/round-87/w1/MutC2Counter.md` (this file)
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/mutant-matrix.tsv`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/mutant-detail.json`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/mutant-shas.txt`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/baseline-vs-frozen-controls.txt`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/demonstrations.txt`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/scenario-revisions.txt`
- `.ufo/waves/round-87/w1/MutC2Counter-receipts/hygiene.txt`
