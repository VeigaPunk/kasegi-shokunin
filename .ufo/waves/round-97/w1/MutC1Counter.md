# MutC1Counter — round-97 C1 control-set mutation probe

Seat: `MutC1Counter` (leaf; no subagents). Wave: round-97 attempt 1. Scratch:
`/fast/scratch/hyaku/kasegi-r97/MutC1Counter` (removed at seat close). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only). Candidate: the C1 landing
`75a471809cba265c8981ece1c0ed29c7895d9308`; base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`;
freeze `daf7fc6a627d615178c27594110e956e592e4cd9`.

## Verdict

**C1 P2 STANDS (re-derived).** At the landing the frozen harness prints
`C1-CONTROLS-RESULT pass controls=14` and `ATTRIBUTION pass fixtures=13`; the 14 CONTROL
lines are byte-identical to the frozen receipt's, and the candidate control reproduces
P1's limb lines exactly: M0 `base=1040/2041`, M1 `after=1043/2035`, M3
`same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5
`out_of_range=none`, M9 `rows=33 unbound=none`, M10 `labelled=33 want=33 mapped=33
kinds=qualify-lane=33 unknown=none unapplied=none unlabelled=none`, M6 the frozen map
sha `f4ed7387…`, `after_rev=75a47180…`. P3 was not probed by this seat.

**Coverage qualifier, no verdict change.** 17 single-point mutants were run through the
frozen harness: **7 killed, 10 survived**, including **7 of the 10 named probes**. The
frozen predicate asserts only that each fixture's observed FAIL set equals its declared
set; it does not assert that the fixture set isolates every rule. The survivors are
coverage findings, not permission to change the contract.

## Method

- Detector: a copy of the frozen harness with exactly one line parameterised —
  `meter = os.environ.get("MUT_METER") or (C1 + "/knowledge-meter.py")` (one hunk,
  receipt 07). The frozen harness file was never modified.
- Candidate: `git clone --shared` of the lane into scratch, then
  `git checkout --detach 75a47180…` in the scratch clone only (the lane's git/jj state
  was not mutated; the clone's HEAD is the landing and the base/freeze objects resolve).
- Each mutant: a copy of the frozen counter with exactly one hunk (17/17 one hunk,
  receipt 04), `python3 -m py_compile` clean, run through the same harness with
  `MUT_METER` pointing at the mutant and `TMPDIR` in scratch. The harness's 14 controls
  are unchanged.
- Baseline: the same detector with `MUT_METER` = a copy of the frozen counter
  (sha256 `a56198d0…`). Run before the sweep; every survivor was then diffed against it.
- No tool installs; system Python 3.14.8 and git 2.56.0 were sufficient. No pacman, no
  host mutation, no lane commit/checkout/reset.

## Baseline (re-derived)

Command: `MUT_METER=<scratch>/mutants/frozen.py python3 -B <scratch>/harness.py
<scratch>/cand daf7fc6a… <lane>/.ufo/waves/round-96/c1/knowledge-meter.py
<scratch>/base/work <scratch>/base/out` → rc=0.

Observed (receipt 00):

```
C1-CONTROLS candidate=75a47180… base=b06af5e0… freeze=daf7fc6a… r96=…/round-96/c1/knowledge-meter.py
CONTROL candidate rc=0 want=0 PASS limbs=none declared=- attribution=PASS
  LIMB M0 pass base=1040/2041
  LIMB M1 pass after=1043/2035
  LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0
  LIMB M4 pass bad=none
  LIMB M5 pass out_of_range=none
  LIMB M9 pass rows=33 unbound=none
  LIMB M10 pass labelled=33 want=33 mapped=33 kinds=qualify-lane=33 unknown=none unapplied=none unlabelled=none
  LIMB M6 pass sha256=f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c
  KNOWLEDGE-METER-RESULT pass rc=0
…
ATTRIBUTION pass fixtures=13
C1-CONTROLS-RESULT pass controls=14
```

The 14 CONTROL lines and the two summary lines are identical to the frozen receipt's
(receipt 14: only the header line differs — the frozen receipt was run at the pre-freeze
scratch candidate `f410e91f…` with freeze `2059fcba…`; this run is at the landing with
the freeze `daf7fc6a…`).

## Mutants

Each row is one single-point change to the frozen counter; the detector is the frozen
harness. "Killed" means at least one CONTROL line changed (rc flip or declared-set
mismatch); "survived" means every CONTROL line, and the whole receipt after normalising
the per-fixture commit revs, is identical to the baseline.

| # | probe | single-point change | observed | verdict |
|---|-------|---------------------|----------|---------|
| M01 | qualify-drop-tracked-internal | drop `target not in A["tracked"]` and `A["classify"](target) != "INTERNAL"` | `CONTROL qualify-target-missing rc=0 want=1 FAIL limbs=none declared=M4,M5` (all limbs pass, meter rc=0) | **KILLED** by qualify-target-missing |
| M02 | qualify-allow-separator-key | drop `"/" in key or ":" in key` | no CONTROL line differs | **SURVIVED** |
| M03 | qualify-accept-new-ne-label | drop `new != exp[2]` | no CONTROL line differs | **SURVIVED** |
| M04 | qualify-drop-old-eq-key | drop `old != "`key`"` | no CONTROL line differs | **SURVIVED** |
| M05 | qualify-accept-ufo-target | drop `target.startswith(".ufo/")` | no CONTROL line differs | **SURVIVED** |
| M06 | m3-drop-old-not-once | drop `missing == 0` from M3 | no CONTROL line differs | **SURVIVED** |
| M07 | m10-drop-unapplied | drop `not unapplied` from M10 | `CONTROL unapplied-only rc=0 want=1 FAIL limbs=none declared=M10` (M10 pass with `unapplied=cisa-bod-20-01-vdp-minimums.md:159/S021.txt` still printed) | **KILLED** by unapplied-only |
| M08 | m9-drop-new-comparison | `exp[1:] != (old, new)` → `exp[1] != old` | no CONTROL line differs | **SURVIVED** |
| M09 | drop-m6 | `got == a.map_sha256.lower()` → `True` | `CONTROL wrong-map-sha rc=0 want=1 FAIL limbs=none declared=M6` (M6 pass with the frozen sha) | **KILLED** by wrong-map-sha |
| M10 | m10-accept-unknown-kind | drop `not unknown` from M10 | no CONTROL line differs | **SURVIVED** |
| M11 | drop-m1 | `(an, am) == (tn, tm)` → `True` | `CONTROL do-nothing rc=1 want=1 FAIL limbs=M3 declared=M1,M3` | **KILLED** by do-nothing |
| M12 | drop-m0 | `(bn, bm) == (bn0, bm0)` → `True` | no CONTROL line differs | **SURVIVED** |
| M13 | m3-drop-dup-rows | drop `dup == 0` from M3 | `CONTROL duplicate-row rc=0 want=1 FAIL limbs=none declared=M3` (M3 pass with `dup_rows=1` still printed) | **KILLED** by duplicate-row |
| M14 | m5-drop-m4-propagation | `("M5", not m5bad and not m4bad, …)` → `("M5", not m5bad, …)` | four controls lose M5: `qualify-target-missing` (limbs=M4 declared=M4,M5), `qualify-key-not-bare` (same), `map-not-label` (limbs=M4,M9 declared=M4,M5,M9), `snapshot-missing-only` (limbs=M4 declared=M4,M5) | **KILLED** by those four |
| M15 | m4-range-drop-key-in-old | drop `("`key`") not in old` from the range branch | no CONTROL line differs | **SURVIVED** |
| M16 | m4-drop-internal-value-check | drop `A["classify"](v) == "INTERNAL"` on knowledge values | no CONTROL line differs | **SURVIVED** |
| M17 | m10-drop-unlabelled | drop `not unlabelled` from M10 | `CONTROL unlabelled-only rc=1 want=1 FAIL limbs=M9 declared=M10,M9` | **KILLED** by unlabelled-only |

### Killed — exact evidence

- **M01**: the qualify-target-missing fixture's target `corpus/instruments/quote-anchor-check.py`
  is untracked; with the tracked/INTERNAL clause gone the meter accepts it:
  `LIMB M4 pass bad=none`, `LIMB M5 pass out_of_range=none`, `KNOWLEDGE-METER-RESULT pass rc=0`
  against the control's `want=1`. The candidate control still passes, so the kill is
  specific to the fixture.
- **M07**: unapplied-only's label is in `want` but unmapped; with `not unapplied` gone M10
  passes and the meter exits 0. The detail line still prints
  `unapplied=cisa-bod-20-01-vdp-minimums.md:159/S021.txt`, i.e. the counter still computes
  the set but no longer enforces it.
- **M09**: wrong-map-sha passes `"0"*64`; with M6 forced true the meter prints
  `LIMB M6 pass sha256=f4ed7387…` and exits 0.
- **M11**: do-nothing's after rev is the base; M1 forced true leaves only M3 failing, so
  the observed set `{M3}` no longer equals the declared `{M1,M3}`.
- **M13**: duplicate-row appends the same `(site, key)` row; with `dup == 0` gone M3 passes
  (`dup_rows=1` still printed) and the meter exits 0.
- **M14**: M5's `not m4bad` is what makes the four M4-failing fixtures declare M5; with it
  gone those controls observe `{M4}` / `{M4,M9}` instead of `{M4,M5}` / `{M4,M5,M9}`.
- **M17**: unlabelled-only's no-op map row has no label; M9 still fails on it, but with
  `not unlabelled` gone M10 passes, so the observed set `{M9}` no longer equals
  `{M10,M9}`.

### Survived — why, and what would kill each

All ten survivor receipts are identical to the baseline after normalising the
per-fixture commit revs (receipt 12), so the mutant is behaviourally invisible to the
frozen harness.

Each suggested isolator below must also keep the after rate at 1043/2035 (or declare M1
as well); the frozen fixtures are rate-neutral by construction.

- **M02 (separator key)**: the qualify-key-not-bare fixture uses key
  `controls/plain-rows.sh` but its target `corpus/instruments/plain-rows.sh` is **not
  tracked** (receipt: `git ls-tree` over the three fixture targets lists only
  `corpus/instruments/resolve.py`). The tracked check therefore fires and masks the
  separator clause; the fixture's declared M4 failure is over-determined. A rate-neutral
  isolator is a **no-op** qualify-lane row whose key is a tracked path containing a
  separator, e.g. key = label = `corpus/instruments/resolve.py` on a line that already
  contains that path: `old == new`, M3/M1/M9/M10 stay green, and only the separator
  clause (plus M5, which follows M4) fails — the mutant would flip the control to
  `rc=0 want=1`.
- **M03 (`new != label`)**: M9's `(old, new)` equality still rejects any map row whose
  new differs from the label; no fixture has a qualify-lane row that disagrees only in
  `new`. A qualify-lane variant of map-not-label (same `old`, different tracked `new`)
  would make M4's clause the only extra failure and kill M03.
- **M04 (`old != key`)**: M9's equality and M3's forward composition both still reject a
  wrong `old`; no fixture has a qualify-lane row with a wrong `old`. A qualify-lane
  variant of map-not-label with `old` = "`key`," would kill M04.
- **M05 (`.ufo/` target)**: the guard is **unreachable**. `expected_edit` enters the
  qualify-lane branch only when `label.startswith("corpus/instruments/")`, and
  `target = exp[2]` is that label, so `target.startswith(".ufo/")` can never be true.
  No fixture can exercise it. The counter docstring's "(or any other tracked non-.ufo
  lane path)" is not implemented: only `corpus/instruments/` labels are qualify-lane.
- **M06 (M3 `old_not_once`)**: no fixture has `old_not_once > 0`; do-nothing,
  extra-unlisted-edit and duplicate-row fail M3 on `bad_lines`/`dup_rows`. A map row
  whose `old` is absent from the base line, with a label that agrees, would make M3's
  `missing` counter the sole guard and kill M06.
- **M08 (M9 new comparison)**: map-not-label changes `old` as well, so M9 still fails on
  `old`; no fixture isolates `new`. A range row whose `old` matches the label and whose
  `new` is a different valid range of the same file (M4 passes on the same file, M5 on a
  valid range, M3 on the edited line) would kill M08.
- **M10 (M10 unknown)**: the clause is redundant. An unknown-kind pair is either
  unmapped — then it is in `want` and in `unapplied`, so M10 still fails — or mapped —
  then `exp is None` and M9 fails. No fixture can make `unknown` the sole failing limb.
- **M12 (M0)**: structurally unexercised. The harness hardcodes `BASE_TARGET` and passes
  the frozen base rev; no fixture can change the base reading. A control that passes a
  wrong `--base-target` (e.g. `1041/2041`) and expects M0 FAIL would be needed.
- **M15 (range key-in-old)**: for a labelled row M9 requires `old == "`key`"`, which
  already implies the check; an unlabelled row fails M9 anyway. A labelled range row
  whose `old` lacks "`key`" (so M4 and M9 both fail) would make the clause the extra
  failure and kill M15.
- **M16 (INTERNAL value check)**: the `bybase` uniqueness check already requires the
  value's file to be tracked at `corpus/knowledge/<name>`, and `resolve.classify` strips
  the anchor and reports any path present in the archive INTERNAL. No fixture has a
  tracked-but-GONE knowledge value. A tracked broken symlink at
  `corpus/knowledge/<name>` (present in `bybase`, absent for `exists_any`) would kill
  M16.

## Harness forgeries

### F1 — a declared set that hides a real FAIL

Forgery: the harness copy's per-control check and `att` string use
`fails <= set(declared)` instead of `fails == set(declared)`. Probe: M14 (M5's
`not m4bad` removed), which the frozen harness kills on four fixtures.

- **F1 partial** (only `ok` and `att` weakened; `attribution.append` still equality):
  the four affected controls print PASS with a strict subset —
  `qualify-target-missing … PASS limbs=M4 declared=M4,M5`,
  `qualify-key-not-bare … PASS limbs=M4 declared=M4,M5`,
  `map-not-label … PASS limbs=M4,M9 declared=M4,M5,M9`,
  `snapshot-missing-only … PASS limbs=M4 declared=M4,M5` — and the result line says
  `C1-CONTROLS-RESULT pass controls=14` with rc=0, but the aggregate line says
  `ATTRIBUTION fail fixtures=13` (receipt 08). **Caught by the ATTRIBUTION aggregate**
  (the third equality site) and by the visible `limbs=` vs `declared=` mismatch.
- **F1b full** (all three sites weakened): `ATTRIBUTION pass fixtures=13`,
  `C1-CONTROLS-RESULT pass controls=14`, rc=0, while the same four CONTROL lines still
  show `limbs` ⊊ `declared` (receipt 09). **Caught only by the printed
  `limbs=`/`declared=` fields** — the declared set hides the missing M5 FAIL — and by
  re-running the frozen harness, which prints `FAIL … attribution=FAIL`. Once all three
  sites are weakened, nothing inside the forged harness catches it.

Note: the harness's exit code ignores the ATTRIBUTION aggregate
(`verdict = all(results)`, `att_ok` is printed only). In the frozen harness every
control's `ok` already includes the equality, so the aggregate is redundant; under a
weakened per-control check the aggregate can fail while the result line and rc say pass.

### F2 — a fixture that edits the meter

Forgery: a new `meter-selfedit` fixture clones the candidate, edits
`.ufo/waves/round-97/c1/knowledge-meter.py` line 1 to `sys.exit(0)`, and also makes the
unlisted `triage-thresholds.md:143` edit the real meter flags as M3. The control expects
rc=0.

- **F2 control** (frozen meter path `C1 + "/knowledge-meter.py"`, the lane's read-only
  counter): the fixture's meter edit is inert; the real meter reports M3 →
  `CONTROL meter-selfedit rc=1 want=0 FAIL limbs=M3 declared=- attribution=FAIL`,
  `C1-CONTROLS-RESULT fail controls=15` (receipt 10). **Caught by the frozen meter
  path**: the harness never runs a counter from inside the fixture.
- **F2 forged** (the same harness plus `if counter == meter: counter =
  os.path.join(lane, ".ufo/waves/round-97/c1/knowledge-meter.py")`): the counter is read
  from the run's lane (the fixture clone), the self-edited meter exits 0 →
  `CONTROL meter-selfedit rc=0 want=0 PASS limbs=none declared=- attribution=PASS`,
  `ATTRIBUTION pass fixtures=14`, `C1-CONTROLS-RESULT pass controls=15`, rc=0
  (receipt 11). **Caught only externally**: the claim pins
  `counter_sha256 a56198d0…`, but the harness never hashes the counter; a verifier must
  hash the meter actually executed (or note that the frozen harness's meter path is the
  lane's frozen file). The meter's M3 does not compare `.ufo/` files, so the self-edit is
  invisible to the meter itself.

## Routed observations (no re-score)

1. `claims.json` C1 `surface` says "33 bare lane-instrument basenames in 12
   corpus/knowledge files"; the statement, P3 and the wave goal say sixteen. The map has
   **16 distinct citing files** (receipt 01), 9 distinct keys, 33 rows (receipt 02). The
   "12" is stale text; P1/P2/P3 do not use it.
2. The qualify-lane `.ufo/` guard is dead code (unreachable, see M05), and the docstring's
   "(or any other tracked non-.ufo lane path)" is not implemented.
3. The harness's rc ignores the ATTRIBUTION aggregate (see F1).
4. For fixture controls the harness passes the **fixture's own** map sha (`sha` is
   recomputed after the fixture commit), so M6 is tautological for fixtures; the frozen
   map is pinned only by the candidate and wrong-map-sha controls. By design, but the
   fixture M6 lines are not map-integrity evidence.
5. The qualify-key-not-bare fixture is over-determined (untracked target), so it does not
   isolate the separator clause (M02 survives).
6. M0 is structurally unexercised (no fixture can vary the base reading).
7. M10's `unknown` clause is redundant (unmapped → unapplied; mapped → M9).
8. M03/M04/M15 are implied by M9 whenever M9 passes; a qualify-lane/range variant of
   map-not-label would isolate them.
9. M16's INTERNAL check is near-redundant with the `bybase` tracked check.

## Receipts

All paths under `.ufo/waves/round-97/w1/MutC1Counter-receipts/`. Frozen pins observed
(receipt 03): counter `a56198d00505cb81cb971b959aa32f4c917c74c48bf1f482521d7c50e8bb57da`,
map `f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c`, labels
`5155959d4cea88bde7f44c0590f007731700a3072faa93f8ecbbd16410ffc853`, harness
`471feda7032ffb28c666c6c6c1b22e4e0a0d9fd9052dcdb7dea386bd88cbe1fb`, receipt
`9cff921f850eaebc03453faeeb3d8a296ca0dbde7dac526203e7d0f08d253179`.

Commands and observed rc/lines:

1. `sha256sum .ufo/waves/round-97/c1/{knowledge-meter.py,repair-map.tsv,labels.tsv}
   .ufo/waves/round-97/controls/c1-controls-r97.py …` → the five pins above; `git
   rev-parse HEAD` → `a9a53608…` (lane HEAD, read only). Receipt `03-frozen-pins.txt`.
2. `diff -u <frozen harness> <scratch>/harness.py` → one hunk (the `MUT_METER` line).
   Receipt `07-harness-diffs.txt`.
3. Baseline: `MUT_METER=<scratch>/mutants/frozen.py python3 -B <scratch>/harness.py
   <scratch>/cand daf7fc6a… <lane>/.ufo/waves/round-96/c1/knowledge-meter.py
   <scratch>/base/work <scratch>/base/out` → rc=0; `C1-CONTROLS-RESULT pass controls=14`;
   `ATTRIBUTION pass fixtures=13`; 14 CONTROL lines identical to the frozen receipt
   (receipt 14 shows only the header difference). Receipt
   `00-baseline-frozen-harness-frozen-counter.txt`.
4. Mutant generation: `python3 <scratch>/gen_mutants.py` → 17 WROTE lines, 17/17 anchors
   unique; `python3 -m py_compile` → 17/17 COMPILE-OK; `diff -u` per mutant → 17/17
   one hunk. Receipts `04-mutant-diffs.txt`, `05-mutant-shas.txt`.
5. Sweep: `printf '%s\n' <scratch>/mutants/M*.py | xargs -P 4 -I{} sh -c '… MUT_METER=
   <scratch>/mutants/{}.py python3 -B <scratch>/harness.py <scratch>/cand daf7fc6a… <r96>
   <scratch>/runs/{}/work <scratch>/runs/{}/out …'` → 17 "done … rc=" lines (7 rc=1, 10
   rc=0); summary: 7 KILLED, 10 SURVIVED (receipt `06-mutant-summary.txt`); per-mutant
   receipts in `mutants/`.
6. Survivor identity: `sed -E 's/after_rev=[0-9a-f]+/after_rev=X/g'` on each survivor and
   the baseline, then `diff -q` → 10/10 identical (receipt `12-survivor-identity.txt`).
7. Killed evidence: the CONTROL/LIMB snippets in `13-killed-snippets.txt`.
8. F1 partial: `MUT_METER=<scratch>/mutants/M14-m5-drop-m4-propagation.py python3 -B
   <scratch>/harness-f1-subset.py …` → rc=0; four controls PASS with `limbs` ⊊
   `declared`; `ATTRIBUTION fail fixtures=13`; `C1-CONTROLS-RESULT pass controls=14`.
   Receipt `08-forgery-f1-partial.txt`.
9. F1b full: `MUT_METER=<scratch>/mutants/M14-…py python3 -B
   <scratch>/harness-f1b-subset-all.py …` → rc=0; `ATTRIBUTION pass fixtures=13`;
   `C1-CONTROLS-RESULT pass controls=14`; same four `limbs` ⊊ `declared` lines. Receipt
   `09-forgery-f1b-full.txt`.
10. F2 control: `MUT_METER=<scratch>/mutants/frozen.py python3 -B
    <scratch>/harness-f2-control.py …` → rc=1; `CONTROL meter-selfedit rc=1 want=0 FAIL
    limbs=M3 declared=- attribution=FAIL`; `C1-CONTROLS-RESULT fail controls=15`. Receipt
    `10-forgery-f2-control.txt`.
11. F2 forged: `MUT_METER=<scratch>/mutants/frozen.py python3 -B
    <scratch>/harness-f2-forged.py …` → rc=0; `CONTROL meter-selfedit rc=0 want=0 PASS
    limbs=none declared=- attribution=PASS`; `ATTRIBUTION pass fixtures=14`;
    `C1-CONTROLS-RESULT pass controls=15`. Receipt `11-forgery-f2-forged.txt`.
12. Map counts: `awk -F'\t' … repair-map.tsv | sort -u | wc -l` → 16 files; distinct
    keys → 9; rows → 33; label rows → 33. Receipts `01-map-distinct-files.txt`,
    `02-map-distinct-keys.txt`.
13. Restoration evidence: post-probe `sha256sum` of the four frozen inputs → all four
    equal the pins above; `diff` of the hash list against the pin list →
    `FROZEN-INPUTS-UNCHANGED` (receipt 16). The mutants were scratch copies; the frozen
    counter, map, labels and harness were never written. The scratch tree was removed at
    seat close.

No credential values appear in any receipt; the C1 meter output carries only file:line
tags, limb details and digests.
