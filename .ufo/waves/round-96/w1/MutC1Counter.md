# MutC1Counter — round-96 C1 control-set mutation test

**Seat:** MutC1Counter (mutation-tester, leaf). **Target:** the frozen round-96
C1 counter `.ufo/waves/round-96/c1/knowledge-meter.py` (sha256
`fadd0ede47392ce0f15596377728415d8e5cc7906874debe1229ee17c8ad36db`) under the
frozen control harness `.ufo/waves/round-96/controls/c1-controls-r96.py`
(sha256 `d47328ae4384f07a92e11c7ad925f21d459ad8db298a230ca08b2454b9f7e7d2`).
**Deliverable:** this report plus the receipts in
`.ufo/waves/round-96/w1/MutC1Counter-receipts/`.

## Verdict

**C1's control-set predicate STANDS** — re-derived by this seat at the landed
revisions, not transcribed: the frozen counter at `--after-rev 3c0581e2` prints
every pinned limb (M0 `1030/2027`, M1 `1032/2028`, M3 `bad_lines=0
old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=5
unbound=none`, M10 `kinds=part=4,range=1`, M6 the frozen map sha) and
`KNOWLEDGE-METER-RESULT pass rc=0`; the frozen harness prints
`ATTRIBUTION pass fixtures=11` and `C1-CONTROLS-RESULT pass controls=12`
(receipt `02-baseline-pristine-r96-counter.txt`). The C1 landing diff shows the
five edits on four lines (the two `iso-29147:36` prose pointers share one line)
(receipt `11-c1-landing-diff.txt`).

**Mutation campaign: 6 of the 10 round-95 survivors are now killed; 4 survive.**
Two of the six kills are **attribution-only** (rc unchanged at 1; the failing-limb
set shrank), so the round-96 attribution fixtures are load-bearing — a
round-95-style rc-only control would have missed them. The four survivors are
coverage findings, not claim changes: one is an equivalent mutant, three are
fixture gaps (one of them a false fixture premise). No frozen file was modified.

## Pins and environment

| item | value | receipt |
|---|---|---|
| base | `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6` | `00-…` |
| freeze | `804e7bc344df0808c880815dde077c28be5db18a` | `00-…` |
| C1 landing (candidate) | `3c0581e2616df7a10af494a785b479d5e5293749` | `00-…` |
| frozen counter | `fadd0ede…` (unchanged after campaign) | `00-…`, `09-…` |
| frozen map | `7d9bb49f…` (unchanged) | `00-…`, `09-…` |
| frozen labels | `757894d1…` (unchanged) | `00-…`, `09-…` |
| frozen harness | `d47328ae…` (unchanged) | `00-…`, `09-…` |
| probe harness copy | `6c1f043fb721a37597eb08742fdd04541fc0b92e85372afa4a2be0316a65c489` | `01-…` |
| python / git | 3.14.8 / 2.56.0 | `00-…` |

The probe is a **scratch copy** of the frozen harness with exactly one line
changed — `meter = os.environ.get("C1_METER_PATH") or C1 + "/knowledge-meter.py"`
— so only the counter path is parameterised (`01-harness-copy.diff`, 1 hunk,
1 line). The frozen harness is read-only and its sha256 is unchanged.

The candidate is a `git clone --shared` of the lane pinned by
`git checkout --detach 3c0581e2` in scratch; the toplevel was asserted equal to
the clone before the checkout and after it, and a `--shared` clone of the clone
reports `HEAD=3c0581e2` (`00-…`). Every fixture is cloned from that pinned
candidate, never from the mutable live lane.

Provenance qualifier: the shipped control receipt prints
`candidate=f60c11a3… freeze=179deaaa…`; neither object exists in the lane
(`git cat-file -t` → fatal). My re-run at the **landed** objects
(`3c0581e2` / `804e7bc3`) reproduces the same 12 control verdicts and 11
attribution verdicts, so the shipped verdicts are reproducible from landed
history even though its printed shas are pre-landing scratch commits.

## Method

1. **Mutant reconstruction.** Each of the ten round-95 survivors was rebuilt as
   a single-point edit of the **round-96** counter from the round-95 manifest
   diff (`../round-95/w1/MutC1Counter-receipts/04-mutants-manifest.json`). The
   changed text of all ten is byte-identical to the round-95 manifest
   (`03c-r95-vs-r96-diff-equivalence.txt`: `identical=True` for all ten); each
   mutant is one hunk (`03-mutants-built.txt`), and all ten compile
   (`py_compile`). Full diffs: `03b-mutants-manifest-diffs.txt`; machine
   manifest with full sha256: `03-mutants-manifest.json`.
2. **Detector.** The frozen harness run unmodified except for the meter path.
   Baseline first (`02-…`, rc 0, 199 s), then the ten mutants in parallel, each
   with its own work/out dir (`04-<mutant>.txt`, 451–479 s each).
3. **Verdict rule.** A mutant is **killed** when at least one `CONTROL` line
   prints `FAIL` — i.e. its rc diverges from `want`, or (round-96 addition) its
   failing-limb set diverges from `declared`. Limb deltas that do not change a
   control verdict are recorded but do not count as kills.
4. **Restoration.** The frozen counter was never edited (mutants are separate
   files). After the campaign the frozen shas were re-checked (`09-…`) and the
   baseline was re-run on the pristine bytes (`07-…`): rc 0, and the `CONTROL`
   and `LIMB` lines are **identical** to the pre-campaign baseline.

## Kill table

Source: `05-summary.tsv`; per-mutant logs `04-<mutant>.txt`; limb deltas
`05-limb-deltas.txt`. Baseline: all 12 controls PASS, attribution 11/11.

| mutant | verdict | kill kind | killing control | observed (mutant vs want/declared) |
|---|---|---|---|---|
| `m06_cell_multi_value_forbidden` | **SURVIVED** | — | — | no control verdict differs from baseline |
| `s01_old_absent_accepted` | **SURVIVED** | — | — | no control verdict differs from baseline |
| `s02_m9_ignores_new` | **KILLED** | rc-flip | `map-not-label` | rc=0 want=1, fails=none, declared=M9 |
| `s03_missing_label_no_edit` | **SURVIVED** | — | — | no control verdict differs from baseline |
| `s04_snapshot_existence_dropped` | **KILLED** | rc-flip | `snapshot-missing-only` | rc=0 want=1, fails=none, declared=M4,M5 |
| `s05_unknown_kind_allowed` | **SURVIVED** | — | — | no control verdict differs from baseline |
| `s06_unlabelled_ignored` | **KILLED** | attribution-only | `unlabelled-only` | rc=1 want=1, fails=M9, declared=M10,M9 |
| `s07_unapplied_ignored` | **KILLED** | rc-flip | `unapplied-only` | rc=0 want=1, fails=none, declared=M10 |
| `s08_part_any_old` | **KILLED** | rc-flip | `map-not-label` | rc=0 want=1, fails=none, declared=M9 |
| `s09_skip_absent_label` | **KILLED** | attribution-only | `unlabelled-only` | rc=1 want=1, fails=M10, declared=M10,M9 |

Per-mutant limb deltas vs the pristine baseline (`05-limb-deltas.txt`); every
unlisted control is unchanged, so each kill is attributable to exactly one
control:

| mutant | control delta |
|---|---|
| `s02_m9_ignores_new` | `map-not-label`: rc 1→0, fails M9 → none |
| `s04_snapshot_existence_dropped` | `snapshot-missing-only`: rc 1→0, fails M4,M5 → none |
| `s06_unlabelled_ignored` | `unlabelled-only`: rc 1→1, fails M10,M9 → M9 |
| `s07_unapplied_ignored` | `unapplied-only`: rc 1→0, fails M10 → none |
| `s08_part_any_old` | `map-not-label`: rc 1→0, fails M9 → none |
| `s09_skip_absent_label` | `unlabelled-only`: rc 1→1, fails M10,M9 → M10 |
| `m06`, `s01`, `s03`, `s05` | (no limb or rc delta on any of the 12 controls) |

## Does the round-96 set change the round-95 outcome?

**Yes, for 6 of 10.** Round-95 recorded 8 killed / 10 survived of 18; under the
round-96 fixtures the same ten mutants give 6 killed / 4 survived, i.e.
**14/18 killed, 4 alive** overall. The change is not only rc: `s06` and `s09`
keep rc=1 and are killed solely because their failing-limb set no longer equals
the declared set (`unlabelled-only` declared `M10,M9`; the mutant leaves only
`M9`, resp. only `M10`). That is the round-96 attribution mechanism doing work
the round-95 rc-only verdict could not do.

## Survivors and why (coverage findings, not claim changes)

| survivor | why it survives (observed) | evidence |
|---|---|---|
| `m06_cell_multi_value_forbidden` | No fixture or label contains a `cell-repair` row: `grep -c cell-repair` is 0 in the frozen labels, map and harness, and every control's `kinds=` tally is part/range only (`part=4,range=1`; `part=5,range=1`; `part=4,range=2`). The round-95 routed control `cell-two-values` was **not shipped**. | `08-fixture-premises.txt`, `02-…` |
| `s01_old_absent_accepted` | `row-old-absent-only`'s map row is `(L1819) → (L1820)`; `(L1819)` occurs **once** on base line 36 (the `a)` item), so the fixture fails via M3 `bad_lines=1` (an edit the file does not carry), **not** `old_not_once`. Both baseline and mutant print `M3 FAIL … bad_lines=1 old_not_once=0`, so the deleted clause is never exercised. | `08-…`, `04-s01…`, `06-…` |
| `s03_missing_label_no_edit` | Equivalent mutant: `exp = expected_edit(...) if lab else None`, so `lab is None` already implies `exp is None`; the deleted disjunct is redundant. Zero limb deltas on all 12 controls. | `05-limb-deltas.txt` |
| `s05_unknown_kind_allowed` | `unknown-kind-row`'s unknown pair is also **unapplied** (`want` includes it, `mapped` does not), so M10 still FAILs via `unapplied` after the `unknown` clause is deleted. In the other direction a *mapped* unknown pair fails M9 (`exp is None`), so the `unknown` clause is shadowed both ways and no shipped fixture isolates it. | `04-s05…` |

Supplementary probe for `s01` (`06-probe-s01-absent-old.txt`): a fixture whose
old is **genuinely absent** (`(L9999)`, 0 occurrences on base line 36) with
everything else clean gives pristine `M3 FAIL … old_not_once=1` rc=1 and the
mutant `M3 pass` rc=0. So `s01` is killable by the fixture shape the harness
comment claims `row-old-absent-only` is; the shipped fixture does not realize
that shape.

## Routed findings (defects/qualifiers, not verdict changes)

* **F1 — false fixture premise (harness defect).** `row-old-absent-only` is
  documented as "a prose part row whose old is not on its line (M3's
  `old_not_once`)" but its old `(L1819)` occurs on base line 36; it exercises
  M3's unapplied-edit clause instead. The declared limb set `{M3}` still matches,
  so the attribution check passes and the defect is invisible at limb level.
  Fix: use an old that does not occur (the `(L9999)` probe above), or rename the
  fixture. This is the one round-95 routed control that was shipped with the
  wrong shape.
* **F2 — `unknown-kind-row` is multi-clause inside M10.** The unknown pair is
  simultaneously unapplied; removing `not unknown` leaves M10 FAIL. Fix: declare
  `{M9,M10}` for a mapped unknown pair, or accept that the `unknown` clause is
  shadowed and drop it.
* **F3 — no cell fixture.** `m06` remains alive because the round-95 routed
  `cell-two-values` control was not shipped. Add a `cell-repair` row writing two
  values (pristine M4 green, mutant M4 red).
* **F4 — equivalent clause.** `s03` cannot be killed; the `lab is None` disjunct
  in M9 is redundant with `exp is None`. Document or drop it (round-95 already
  routed this).
* **F5 — receipt provenance.** The shipped control receipt's
  `candidate=f60c11a3… freeze=179deaaa…` are not lane objects; the verdicts
  reproduce at the landed `3c0581e2` / `804e7bc3`. Not a predicate failure.

## Integrity and restoration

* **Frozen inputs unchanged after the campaign** (`09-lane-integrity.txt`):
  counter `fadd0ede…`, map `7d9bb49f…`, labels `757894d1…`, harness
  `d47328ae…` all equal the `00-…` pins.
* **Restored bytes re-run** (`07-restored-pristine-rerun.txt`): harness rc=0,
  `ATTRIBUTION pass fixtures=11`, `C1-CONTROLS-RESULT pass controls=12`; the
  `CONTROL` and `LIMB` lines are byte-identical to the pre-campaign baseline
  (diff empty). Fixture commit ids differ per run (each fixture is a fresh
  commit), which is the only expected variance.
* **Lane state:** the live lane advanced during the campaign
  (`7ef1d365` → `6299582b`, L1 integration/amendments). All my runs were pinned
  to the scratch clone at `3c0581e2`, so the advance cannot affect the results.
  My only lane writes are this report and the receipts directory; the lane's
  `git status` shows `?? .ufo/waves/round-96/w1/MutC1Counter-receipts/` (and this
  report once written). No commit/add/checkout/reset/stash was run in the lane.
* **Scratch:** `/fast/scratch/hyaku/kasegi-r96/MutC1Counter` measured 29 G
  before removal; it is deleted at the end of the seat (every cited output is
  already copied into the receipts).

## Manifest of diffs

One hunk each, against the frozen round-96 counter; full unified diffs in
`03b-mutants-manifest-diffs.txt`, machine manifest in `03-mutants-manifest.json`.

| mutant | sha256 of mutant file | single-point change |
|---|---|---|
| `m06_cell_multi_value_forbidden` | `751a8b20e7a7edb5d9571108afdcd348deb09d88900923964090d03d813d8ccc` | M4 drops `and not is_cell` from the one-value rule |
| `s01_old_absent_accepted` | `9bb9bb92eaeda0d7dd4ca657d3aa38772c588ab4e4c5f9eea0664e7f68792186` | M3 replaces the `old`-occurrence check with an unconditional `replace` |
| `s02_m9_ignores_new` | `57146753a1dc4325a50de49109088211e73ed2ca6ef9d73d9871c18ba089bfba` | M9 drops `exp[1:] != (old, new)` |
| `s03_missing_label_no_edit` | `f5fe5ba990588d741bc88d4a460a008872b6b8bc3c3724d21c47a2b4218000a2` | M9 drops the redundant `lab is None` disjunct |
| `s04_snapshot_existence_dropped` | `9581686e3413be9ab63ac217100ca73e07e49108122f9fd0c62ede1f2ec572a4` | M4 deletes the snapshot existence/range loop |
| `s05_unknown_kind_allowed` | `c06bdaeb7f19202173452cf22b61d7eabec370919567d743977c6aca46b1dd53` | M10 drops `not unknown` |
| `s06_unlabelled_ignored` | `66e6abf53689276f7e3172ad4db3fd53d122d51f7078590439e7d27f85d3e6c7` | M10 drops `not unlabelled` |
| `s07_unapplied_ignored` | `bea2d33161d9f7aa23a9f6acc6aef4574fa1b62f6d9f83252f225f08f0d97ab6` | M10 drops `not unapplied` |
| `s08_part_any_old` | `68a5fca5c66bad74d7d30d4e522c48206117223f0a984c87c69738681f247c6a` | M9 skips the `(old,new)` compare for `part` |
| `s09_skip_absent_label` | `834f3b26e9aa2078d335e17ebcb60796b8f3ce8d14a7df3ffbb0252925a52870` | M9 skips rows whose label is absent |

## Receipts

Commands run (all from the lane root or the scratch dir; `TMPDIR` set to the
scratch; outputs in `.ufo/waves/round-96/w1/MutC1Counter-receipts/`):

| # | command (abridged) | observed |
|---|---|---|
| 1 | `sha256sum .ufo/waves/round-96/c1/{knowledge-meter.py,repair-map.tsv,labels.tsv} .ufo/waves/round-96/controls/c1-controls-r96.py` | counter `fadd0ede…`, map `7d9bb49f…`, labels `757894d1…`, harness `d47328ae…` — all equal the pins (`00-…`) |
| 2 | `git cat-file -t f60c11a3… ; git cat-file -t 179deaaa…` | both `fatal: could not get object info` (not lane objects) |
| 3 | `cp` frozen harness → scratch; replace the `meter = …` line; `diff -u` | 1 hunk, 1 line; copy sha `6c1f043f…` (`01-…`) |
| 4 | `git clone -q --shared <lane> $S/cand; git -C $S/cand checkout -q --detach 3c0581e2` after `rev-parse --show-toplevel` assert | toplevel = `$S/cand`; `HEAD=3c0581e2`; `--shared` clone of it reports `HEAD=3c0581e2` (`00-…`) |
| 5 | `python3 make-mutants.py` | 10 mutants, 1 hunk each, `py_compile` clean (`03-…`) |
| 6 | compare each mutant's changed lines to the round-95 manifest | `identical=True` for all ten (`03c-…`) |
| 7 | `python3 -B harness.py $S/cand 804e7bc3 …/round-95/c1/knowledge-meter.py $S/work/baseline $S/out/baseline` | rc=0, 199 s; `ATTRIBUTION pass fixtures=11`; `C1-CONTROLS-RESULT pass controls=12` (`02-…`) |
| 8 | same harness with `C1_METER_PATH=$S/mutants/<name>.py`, one run per mutant (parallel) | rc=0 for `m06,s01,s03,s05`; rc=1 for `s02,s04,s06,s07,s08,s09`; the `CONTROL … FAIL` lines in the kill table (`04-…`) |
| 9 | direct counter run on a probe fixture with old `(L9999)` (0 occurrences on base line 36) | pristine `M3 FAIL … old_not_once=1` rc=1; `s01` `M3 pass` rc=0 (`06-…`) |
| 10 | re-run baseline harness on the pristine bytes after the campaign | rc=0, 312 s; `CONTROL`/`LIMB` lines identical to step 7 (`07-…`) |
| 11 | `sha256sum` frozen inputs; `git -C <lane> status --porcelain`; `du -sh $S` | all four pins unchanged; only `?? …/MutC1Counter-receipts/` is mine; scratch 29 G (`09-…`) |
| 12 | `git diff d8a2bb0 3c0581e2 -- corpus/knowledge/{triage-thresholds,iso-29147-…}.md` | 4 changed lines carrying the 5 edits (the two `iso-29147:36` pointers share one line) (`11-…`) |

Tooling: none installed or upgraded (python 3.14.8, git 2.56.0 as shipped); no
pacman/uv/npm transaction, no host mutation.
