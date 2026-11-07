# MutC1Counter — round-95 C1 counter mutation test

**Seat:** MutC1Counter (mutation-tester). **Target:** frozen C1 counter
`.ufo/waves/round-95/c1/knowledge-meter.py` (sha256
`c0799f4c52441671b722ccdaa51b579a71c1e3f3c51074d062c7952606878db8`), read-only.
**Deliverable:** this report plus the campaign receipts already in
`.ufo/waves/round-95/w1/MutC1Counter-receipts/`.

**Compilation note (L1 request, 2026-11-07):** this report is compiled from the
campaign receipts already written during the round-95 run. **No new mutants or
controls were started for it**; every figure below is a transcription of a
receipt file named in-line. The campaign itself is complete: 18 of 18 manifest
mutants were run (receipt `08-run-log.txt`), **none is not-run**.

## Freeze, harness and baseline

| item | value | receipt |
|---|---|---|
| base rev | `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10` | `00-freeze-and-environment.txt` |
| freeze rev | `347519f21524d2bc13eb6c91cf3550930a4265b3` | `00-…` |
| C1 landing rev | `53ec479d71d25cf5be052db794a548a5904564b8` | `00-…` |
| C2 landing rev | `38e7319f44a9fab2978b59ffd43faf207cf62b32` | `00-…` |
| counter (working tree = freeze = landing) | `c0799f4c…` | `00-…`, `07-lane-integrity.txt` |
| repair map `repair-map.tsv` | `8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6` | `00-…` |
| labels `labels.tsv` | `cf73949702a569385e0c68390177f454f050f101659edc5ad89410973f0379d0` | `00-…` |
| frozen harness code `controls/c1-controls-r95.py` | `090deb24099fb39a5725e4cb5942117f5671e5c7ef1a6150faa29d9f26835ed2` | `00-…` |
| shipped control receipt at landing | `165e63e5…` committed / `bebac965…` live (fixture ids + work dir only; verdicts identical) | `02-provenance.txt` |

The probe executes the **frozen harness code** via a scratch copy
(`01-harness-copy.py`, sha `809173c1…`) with only `METER_PATH` parameterised —
not the receipt text (`02-provenance.txt`). Pinned candidate clone:
`/fast/scratch/hyaku/kasegi-r95/MutC1Counter/cand53`, `HEAD=53ec479…`, toplevel
asserted (`00-…`).

Baseline: the pristine counter passes **all 15 shipped controls** at both the
C1 landing rev and the wave head (`C1-CONTROLS-RESULT pass controls=15` in
`03-baseline-pristine-counter-at-c1-landing-controls.txt` and
`03b-baseline-pristine-counter-at-wave-head-d050e28-controls.txt`). Control
inventory and expected rcs (`02-shipped-c1-controls-r95-at-53ec479.txt`):
`candidate 0`, `do-nothing 1`, `partial-row-dropped 1`, `extra-unlisted-edit 1`,
`wrong-new 1`, `m5-out-of-range 1`, `snapshot-missing 1`, `missing-labels 2`,
`wrong-map-sha 1`, `unlabelled-row 1`, `part-as-cell 1`, `union-applied 0`,
`union-applied-before-r93 1`, `cell-repair-lane-root 1`, `two-cells-one-line 1`.
A mutant is **killed** when at least one control's verdict diverges from its
recorded `want` rc; limb deltas that do not change a control verdict are
recorded but do not count as kills (`05-limb-deltas.txt`).

## Result: 18 mutants, 8 killed, 10 survived

Source of the killed/survived column: `05-summary.tsv`; per-control limb deltas:
`05-limb-deltas.txt`; diffs: `04-mutants-manifest.json` and `06-mutants/`
(18 `.py` + 18 `.diff`); run order/rc: `08-run-log.txt`.

| mutant | sha16 | single-point change | killed by (observed verdict flips) | manifest prediction | verdict |
|---|---|---|---|---|---|
| `m01_part_old_from_key` | 28bdd9f3324fdbf2 | part-kind `old` taken from key token | `candidate`, `union-applied` (M9 unbound on 5 part rows) | candidate | KILLED |
| `m02_lane_no_range_check` | 7c3e56ee4990b531 | M5 lane-root range check deleted | `m5-out-of-range` (M5 only limb; rc 1→0) | m5-out-of-range | KILLED |
| `m03_map_sha_inverted` | b1e5b7d1788ff41e | M6 runs only when `--map-sha256` absent | `wrong-map-sha` (M6 only; rc 1→0) | wrong-map-sha | KILLED |
| `m04_labels_read_swallowed` | c69291e2ec9d7232 | missing labels file tolerated as `{}` (rc 2→1) | `missing-labels` (rc 1 vs want 2) | missing-labels | KILLED |
| `m05_snapshot_key_dropped` | 8a31742b815e7531 | M4 snap-key acceptance deleted | `candidate`, `union-applied` (M4 FAIL on 5 snapshot rows) | candidate | KILLED |
| `m06_cell_multi_value_forbidden` | ed009d16cd0119f0 | one-value rule applied to cell rows | none — see routing | candidate (cell two-value fixture) | **SURVIVED** |
| `m07_m1_target_swapped` | fbba142c196754d4 | M1 compares after to base target | `candidate`, `union-applied` (M1 FAIL) | candidate | KILLED |
| `m08_m0_target_swapped` | a4a9d60b6ae99972 | M0 compares base to target | `candidate`, `union-applied` (M0 FAIL) | candidate | KILLED |
| `m09_part_kind_removed` | 6d2e1d299050fbd4 | part-kind branch never learned | `candidate`, `union-applied` (M10 unknown / M9 FAIL) | candidate | KILLED |
| `s01_old_absent_accepted` | 7c610366cfbcfb4a | M3 `old_not_once` check deleted | none — masked | unlabelled-row (predicted survivor) | **SURVIVED** |
| `s02_m9_ignores_new` | 5a0d01f1c3b7c65c | M9 new-value comparison deleted | none — masked | wrong-new (predicted survivor) | **SURVIVED** |
| `s03_missing_label_no_edit` | cdfe4e27e4e17a3a | redundant `lab is None` clause deleted | none — equivalent | unlabelled-row (predicted survivor) | **SURVIVED** |
| `s04_snapshot_existence_dropped` | e1dd3eb8769a06ab | M4 snapshot existence+range loop deleted | none — masked | snapshot-missing (predicted survivor) | **SURVIVED** |
| `s05_unknown_kind_allowed` | fa51a266274251a6 | M10 unknown-kind rejection deleted | none — unexercised | none shipped (predicted survivor) | **SURVIVED** |
| `s06_unlabelled_ignored` | ed035e811a2099e0 | M10 unlabelled rejection deleted | none — masked | unlabelled-row (predicted survivor) | **SURVIVED** |
| `s07_unapplied_ignored` | 40290e05f089a02b | M10 unapplied rejection deleted | none — masked | partial-row-dropped (predicted survivor) | **SURVIVED** |
| `s08_part_any_old` | 6513e36c70c370cd | M9 skips (old,new) compare for part kind | none — unexercised | none shipped (predicted survivor) | **SURVIVED** |
| `s09_skip_absent_label` | 103161932bf0a511 | M9 skips rows whose label is absent | none — masked | unlabelled-row (predicted survivor) | **SURVIVED** |

Kills cluster on the accepted-path controls: the five `candidate`/`union-applied`
kills (m01, m05, m07, m08, m09) come from controls that expect **rc 0**, while
the dedicated negative fixtures killed m02 (`m5-out-of-range`), m03
(`wrong-map-sha`) and m04 (`missing-labels`). In the recorded deltas no negative
fixture's verdict changed under any mutant: where a limb flipped, another limb
still produced the expected failure.

## Survivors → routed round-96 controls (not claim changes)

Each row names the fixture isolation the shipped set lacks. `observed` is from
`05-limb-deltas.txt`; `05-summary.tsv` carries the same residual in its last
column.

| survivor | why it survived (observed) | round-96 control to add |
|---|---|---|
| `m06_cell_multi_value_forbidden` | `cell-repair-lane-root` flips M4 pass→FAIL but the control stays rc 1 (receipt: "still rc1 via M5"; M4/M5 attribution not isolated); no candidate fixture writes two values in a cell row | `cell-two-values`: cell row writing two values, pristine accepts (M4 green), M5 green; pristine rc 0, mutant rc 1 |
| `s01_old_absent_accepted` | `unlabelled-row` flips M3 `old_not_once` 1→0 but still fails via M9 unbound + M10 unlabelled | `row-old-absent-only`: one row's old not on its line, everything else clean; pristine rc 1 via M3 only; mutant rc 0 |
| `s02_m9_ignores_new` | `wrong-new`/`snapshot-missing`/`two-cells-one-line` flip M9 FAIL→pass but each control still returns its expected failure through other limbs (receipt: `wrong-new` still rc1 via M3 `bad_lines=1`) | `wrong-new-only`: one wrong new value, M3 line diff green; pristine rc 1 via M9; mutant rc 0 |
| `s03_missing_label_no_edit` | equivalent mutant: zero limb deltas (`lab is None` ⇒ `exp is None`) | none (equivalent); document or drop the redundant clause |
| `s04_snapshot_existence_dropped` | `snapshot-missing` flips M4 FAIL→pass and M5 FAIL→pass, but the control still fails via M1 `after=1007/1994` + M9 unbound | `snapshot-missing-only`: missing snapshot path with M1 rate and M9 green; pristine rc 1 via M4; mutant rc 0 |
| `s05_unknown_kind_allowed` | no fixture yields an unknown kind (`kinds=… unknown=none` on every control) | `unknown-kind-row`: label whose kind is unknown/excluded, M3/M9 green; pristine rc 1 via M10 unknown; mutant rc 0 |
| `s06_unlabelled_ignored` | `unlabelled-row` flips M10 FAIL→pass but still fails via M3 `old_not_once=1` + M9 unbound | `unlabelled-only`: applied map row with no label, M3 `old_not_once=0`, M9 green; pristine rc 1 via M10 unlabelled; mutant rc 0 |
| `s07_unapplied_ignored` | `partial-row-dropped` and `part-as-cell` flip M10 FAIL→pass but each still fails via M3 `bad_lines` (partial-row-dropped: `bad_lines=1`) | `unapplied-only`: labelled row not applied, M3 `bad_lines=0`; pristine rc 1 via M10 unapplied; mutant rc 0 |
| `s08_part_any_old` | no fixture perturbs a part row's old; zero limb deltas | `part-old-wrong`: part row with wrong old, M3/M10 green; pristine rc 1 via M9; mutant rc 0 |
| `s09_skip_absent_label` | `unlabelled-row` flips M9 FAIL→pass but still fails via M3 `old_not_once=1` + M10 unlabelled | `absent-label-only`: label absent, M3 `old_not_once=0`, M10 unlabelled=0; pristine rc 1 via M9; mutant rc 0 |

The masked survivors (s01, s02, s04, s06, s07, s09, m06) show that the shipped
negative fixtures are **multi-defect**: they still fail for a reason other than
the rule under test, so their verdict cannot attribute the failure. The unexercised
survivors (s05, s08) need a fixture shape the set does not contain. Neither class
is a claim change; both are routed controls.

## Coverage, integrity and restoration

* **Coverage:** manifest 18 = summary 18 = 18 distinct `=== RUN` lines in
  `08-run-log.txt` (+ `pristine53`); no mutant is not-run. `06-mutants/` holds
  18 `.py` + 18 `.diff`.
* **Frozen C1 inputs unchanged:** counter `c0799f4c…`, map `8545eba2…`, labels
  `cf739497…` all equal the `00-…` freeze values after all 18 runs
  (`07-lane-integrity.txt`).
* **Lane modification recorded:** the only C1-path `git status` entry is
  ` M .ufo/waves/round-95/controls/c1-controls-r95.txt`; `02-provenance.txt`
  records that the live-vs-committed diff is fixture commit ids and work dir
  only and that control verdicts are identical, and that the probe executes the
  harness code sha `090deb24…`, not the receipt text.
* **Scratch:** `/fast/scratch/hyaku/kasegi-r95/MutC1Counter` was left in place
  with `cand53` and `mutants/` (`07-lane-integrity.txt` inventory: 19 mutant
  files); every output cited here is already copied into
  `MutC1Counter-receipts/`, so the scratch is disposable.
* **Tooling:** none installed (`00-…`: python 3.14.8, git 2.56.0; no
  pacman/uv/npm transaction).
* **This report** adds no executions: it transcribes `00`–`08`.

## Files written

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-95/w1/MutC1Counter.md`
  (this report; the `MutC1Counter-receipts/` set was written during the campaign
  and is unchanged by this report)
