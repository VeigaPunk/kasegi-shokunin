# MutC1Counter — round-93 C1 counter, mutation probe (attempt 1, seat report)

Seat: leaf mutation tester for claim C1 (`depth:verifiability`). One probe wave: 19
single-change mutants of the frozen round-93 C1 counter, each run against the landed
state and against every control variant of the frozen suite, plus 8 purpose-built
fixtures for the survivors' proof inputs. Read-only on the lane's git/jj state; all
fixture commits live in scratch clones that are deleted at exit.

Pins re-derived before mutating (all match `.ufo/waves/round-93/claims.json`):

| artifact | sha256 |
|---|---|
| `git show 5bad9e5:.ufo/waves/round-93/c1/knowledge-meter.py` | `d9f9432d44f09154da95a03531ff8e5643e708bee0f4b067781819a8e57c4b92` |
| `git show 5bad9e5:.ufo/waves/round-93/c1/repair-map.tsv` | `7ab66a7fc8a90cf92d026d0ba1abaa23461b10a3bbd79d003ee4a33961eb3b76` |
| `git show 5bad9e5:.ufo/waves/round-93/c1/labels.tsv` | `51b4f3eb3ccc44c9138c29a1052dbb08f951001c9cc0f9dd2971c25f0b670dff` |

Baseline re-derivation on the pristine bytes: the frozen counter over
`--base-rev e15996bf --after-rev ae53b3c6 --labels-rev 5bad9e55` prints
`KNOWLEDGE-METER base=1007/2001 after=1009/2000 ... sites=5 labels=8` and
`LIMB M0/M1/M3/M4/M5/M9/M10/M6 all pass`, `KNOWLEDGE-METER-RESULT pass rc=0`; the frozen
control suite prints `C1-CONTROLS-RESULT pass controls=11`, rc=0. So the detector itself
is green before any mutation — no baseline failure.

## Verdict

killed=7 survivors=12 (19 mutants). Two routed predicate-integrity defects (R1, R2) and
one coverage hole (EXCLUDED empty) are reported below; neither re-scores C1's predicate at
the landing.

| mutant | area | verdict | detected by / proof |
|---|---|---|---|
| M01-cell-lastcell-last | cell-repair old derivation | killed | `candidate`: `LIMB M9 FAIL rows=5 unbound=triage-thresholds.md:437,triage-thresholds.md:438` (M3/M4 still pass) |
| M02-cell-new-eq-old | cell-repair new derivation | killed | `candidate`: same M9 unbind of 437/438 |
| M03-cell-iscell-false | cell-repair multi-value exemption | survived | equivalent on the frozen data; P01/P02 identical (is_cell is dead code) |
| M04-m3-union-knowledge-only | M3 labelled-file union | killed | `m3-labelled-file-scope`: `rc=0 want=1` (all limbs pass; the SKILL.md edit is invisible) |
| M05-m3-count-skip | M3 line-count equality | survived | R1 masks the limb; with R1 fixed, frozen `LIMB M3 FAIL bad_lines=1` vs mutant pass (P17/P18/P19) |
| M06-m4-bybase-nonunique | M4 basename uniqueness | survived | frozen `LIMB M4 FAIL bad=triage-thresholds.md:437` vs mutant pass (P03/P04) |
| M07-m4-laneroot-no-classify | M4 lane-root binding | survived | equivalent: classify is entailed by the tracked guard + M5's file-existence check |
| M08-m5-laneroot-no-hi-bound | M5 lane-root range | survived | frozen `LIMB M5 FAIL out_of_range=…:454` vs mutant pass (P05/P06) |
| M09-m5-laneroot-split | M5 lane-root range | survived | frozen `LIMB M5 FAIL` vs mutant pass on `SKILL.md:1252` (P07/P08) |
| M10-m10-drop-unknown | M10 pair completeness | survived | equivalent: unknown kinds stay in `want`, so `unapplied` catches them |
| M11-m10-unlabelled-emptied | M10 pair completeness | survived | equivalent: M9 rejects every mapped pair outside `want` (P12/P13) |
| M12-m10-excluded-not-subtracted | EXCLUDED empty set | survived | EXCLUDED={} in round 93; with a real pair the mutant rejects a valid tranche (P22/P23/P24) |
| M13-m10-excluded-membership | EXCLUDED empty set | survived | EXCLUDED={} makes the subset check vacuous (P15/P16) |
| M14-m6-prefix16 | M6 map-sha pin | survived | frozen `LIMB M6 FAIL` on a 16-hex-prefix pin vs mutant pass (P20/P21) |
| M15-m6-limb-omitted | M6 map-sha pin | killed | `wrong-map-sha`: `rc=0 want=1`, no M6 limb emitted |
| M16-labels-from-after-rev | labels rev pin | killed | `missing-labels` `rc=0 want=2` and `do-nothing` `rc=2 want=1` |
| M17-contentrepair-dash-disabled | content-repair kinds | survived | kind unexercised in r93; a valid round-92 drop-token row passes frozen, fails the mutant (P09/P10) |
| M18-m3-dup-not-counted | M3 duplicate rows | killed | `duplicate-map-row`: `rc=0 want=1`, `dup_rows=0` |
| M19-m10-mapped-drops-key | M10 pair identity | killed | `candidate` rc=1, but by a `ValueError` crash in `short(unlabelled)`, not a LIMB line (P25) |

Full row data (sha, suite rc, failing controls, killing limb text, proof receipt, note):
`MutC1Counter-receipts/mutants.tsv`. Suites: `receipts/suites/M*-controls.txt`,
`receipts/suites/M*-summary.txt`. Probes: `receipts/probes/P*.txt`.

## Routed defects

### R1 (counter, high) — the M3 labelled-file walk crashes; its control passes on the traceback

`knowledge-meter.py:282` rebinds the argparse namespace:

```
            b, a = file_at(B["tree"], rel), file_at(A["tree"], rel)
```

so any label whose *citing* file is outside `corpus/knowledge` (or absent at one rev)
turns `a` into a `str`, and `if a.map_sha256:` (line 399) raises
`AttributeError: 'str' object has no attribute 'map_sha256'`. The crash happens **before**
the LIMB print loop, so the counter emits no `LIMB`/`KNOWLEDGE-METER-RESULT` line and
exits 1.

Consequences, all observed:
* the frozen control `m3-labelled-file-scope` records `rc=1 want=1 PASS` — a crash read as
  a detection (`receipts/01-controls-frozen.txt`; reproduction
  `receipts/02-r1-shadow-repro.txt`, `probes/P17-fx7-frozen.txt`);
* the claim's sentence "M3 walks every labelled file, not only corpus/knowledge" is
  inoperative: the walk cannot complete on the input it exists for;
* M3 defects behind the union (M05, M18-class line-count/dup drift on a non-knowledge
  labelled file) are invisible to the frozen detector.
* `variants/r1fix.py` (rename `a` → `a_txt` in both lines) makes the limb work:
  `LIMB M3 FAIL same_files=True bad_lines=1` on a SKILL.md append (`probes/P18`), and the
  M05 mutant then passes (`probes/P19`).

Not a re-score of P1: the landing's 8 labels cite only `corpus/knowledge` files, so the
union set is empty there and every limb passes honestly. The defect is a qualifier on the
counter's stated generality and on the controls receipt, not on the base/after readings.

### R2 (predicate wording) — M5 does not cover lane-root tokens inside a cell replacement

M4/M5 extract a lane-root value only when the whole `new` field is `` `SKILL.md:N[-M]` ``
(`LANEVAL` is `^…$`). A `cell-repair` replacement is prose, so the lane-root token it
carries is neither bound nor range-checked. Probe F1 rewrites 437's second token
`SKILL.md:176-178` to `SKILL.md:9999-10000` (past EOF of the 1251-line `SKILL.md`): the
frozen counter prints `LIMB M5 pass out_of_range=none` and `rc=0` (`probes/P01`).
`is_cell` is dead code on this data (M03) because `VALANY` finds exactly one value per
cell. On the landing the token is `SKILL.md:176-178`, which is in range, so no limb's
verdict changes; the sentence "every written value's anchor lies inside the entry" is
simply broader than the implementation.

### EXCLUDED is empty in round 93 (three survivors, one real defect)

`EXCLUDED = {}` — the two errata pairs round 92 excluded became the round-93
`cell-repair` edits. The r92 counter carried two entries and the r92 controls carried
`excluded-437-applied` (`git show 5bad9e5:.ufo/waves/round-92/controls/c1-controls-r92.txt`);
the r93 control set has no excluded pair, and the r93 M10 tally prints
`kinds=cell-repair=2,no-edit=3,range=3` — no `excluded=` bucket. M11/M12/M13 therefore
cannot be distinguished by any frozen input. M12 is a genuine latent defect: with an
excluded pair that is correctly left unmapped, the mutant puts it in `want` and fails M10
(`unapplied=…58/SKILL.md:117`) where the correct counter passes
(`probes/P23` vs `P24`, and `P22` shows the frozen counter's rc=1 is due to EXCLUDED
being empty, not to the mutant).

## Survivors with a reachable proving input (proposed controls in `PROPOSED-CONTROLS.md`)

* **M05** — M3 line-count equality. Frozen: traceback (R1). R1-fixed: `bad_lines=1`
  rc=1; M05: rc=0. Input: `SKILL.md` entering the walk via a `CORRECT / No edit` label
  row plus one appended line (`probes/P17–P19`).
* **M06** — M4 basename uniqueness. Input: the 437 cell edit with frozen labels/map plus
  `notes/intake-surface.md` (`P03/P04`).
* **M08** — M5 `hi` bound. Input: 454 → `` `SKILL.md:827-9999` `` (`P05/P06`).
* **M09** — M5 `split("\n")` counts the trailing empty element. Input: 454 →
  `` `SKILL.md:1252` `` on a 1251-line file (`P07/P08`).
* **M14** — M6 pin is a full-file compare; a 16-hex prefix pin is accepted
  (`--map-sha256 7ab66a7fc8a90cf9` + 48 zeros; `P20/P21`).
* **M17** — the round-91/92 `content-repair` kinds (dash-cell / drop-token / named /
  named-cell) are not re-exercised by the r93 labels; a valid round-92-style `drop-token`
  row passes the frozen counter and fails the mutant with `kinds=unknown=1` (`P09/P10`).
* **M03** — equivalent on the frozen inputs; its survival is the evidence that `is_cell`
  is dead and that the cell's lane-root token is unchecked (R2).

## Equivalent mutants (no control proposed; redundancy, not coverage)

* **M07** — for a bare lane-root value, `classify()` is `INTERNAL` iff `SKILL.md` exists,
  which the `"SKILL.md" not in A["tracked"]` guard and M5's `file_at(...) is None` check
  already require.
* **M10** — `"unknown"` is not in the `("excluded","no-edit")` filter, so an unknown pair
  is always in `want` and always caught by `unapplied`; `not unknown` is redundant.
* **M11** — M9's condition rejects a mapped pair when the label is absent, the edit is
  `no-edit`/`unknown` (`exp is None`), or the pair is in `EXCLUDED`; `unlabelled` can
  never change the verdict (P12/P13 show M9 failing in both).

## Not a claim re-score

C1's P1 still holds at the landing on the frozen bytes (rc=0, base 1007/2001, after
1009/2000, all limbs incl. M6 on the pinned map sha). R1/R2 are routed counter/predicate
defects; the survivors are coverage findings for round 94, not permission to change the
contract or the map.

## Receipts

All under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-93/w1/MutC1Counter-receipts/`.

| command (working dir `/fast/scratch/hyaku/kasegi-r93/MutC1Counter`, `TMPDIR` set to it) | observed |
|---|---|
| `git -C lane show 5bad9e5:<counter>` > `art/knowledge-meter.py`; `sha256sum` | `d9f9432d…` = frozen counter pin |
| `git -C lane show 5bad9e5:<map|labels>`; `sha256sum` | `7ab66a7f…`, `51b4f3eb…` = frozen pins |
| `python3 -B art/knowledge-meter.py --lane lane --base-rev e15996bf --after-rev ae53b3c6 --map art/repair-map.tsv --labels-rev 5bad9e55 --base-target 1007/2001 --target 1009/2000 --map-sha256 7ab66a7f… --work work` | rc=0; `base=1007/2001 after=1009/2000`; M0,M1,M3,M4,M5,M9,M10,M6 pass (`00-frozen-baseline.txt`) |
| `python3 -B art/c1-controls-r93.py lane e15996bf ae53b3c6 art/knowledge-meter.py art/repair-map.tsv art/labels.tsv work/ctl-frozen out/ctl-frozen` | rc=0; `C1-CONTROLS-RESULT pass controls=11` (113 s) (`01-controls-frozen.txt`) |
| `python3 -B art/mkmutants.py` | 19 mutants, one unique textual change each, all `compile()` clean (`mutants-index.txt`) |
| `bash art/run-all-suites.sh` (each mutant cloned into `fx/<id>`, mutant meter installed and committed, 11 controls run, clone deleted) | 19 suites: 7 killed / 12 survived (`suites/`) |
| `python3 -B art/mkfixtures.py` + `art/mkfx8.py` | fixtures fx1–fx8 committed in `fx/build/lane`, rates measured for `--base-target/--target` (`fixtures.tsv`) |
| `bash art/run-all-probes.sh` + the fx8 trio | P01–P25: frozen-vs-mutant limb differentials (`probes/`) |
| `python3 -B art/mkreceipt.py` | `mutants=19 killed=7 survived=12`; asserts each mutant's observed failing-control set equals the verdict mapping |
| `python3 -B art/mutants/M19-… --lane lane …` (direct) | `ValueError: too many values to unpack` in `short()`; rc=1 (`probes/P25`) |
| `python3 -B art/variants/r1fix.py` on fx7 | `LIMB M3 FAIL bad_lines=1`, rc=1 (`P18`) |
| `python3 -B art/variants/excl-base.py` / `-m12` on fx8 | rc=0 / rc=1 `unapplied=…58/SKILL.md:117` (`P23/P24`) |

Tooling: no installs or upgrades were made (python3 and git already present); no pacman
transaction was run.
