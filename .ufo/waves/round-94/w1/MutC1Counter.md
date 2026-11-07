# MutC1Counter — round-94 C1 counter, mutation probe (attempt 1, seat report)

Seat: leaf mutation tester for claim C1 (`depth:verifiability`). One v1 wave, 13 seats
(count from the round-94 w1 spec; no other number). Probe: 17 single-change mutants of the
frozen round-94 C1 counter, each run against the landed state (`d51220a`) and against the
control fixtures rebuilt from `.ufo/waves/round-94/controls/c1-controls-r94.txt`, plus six
purpose-built fixtures introduced only because a mutant's kill needed an input the frozen
suite does not contain. Read-only on the lane's git/jj state; every fixture commit lives in
a scratch clone under `/fast/scratch/hyaku/kasegi-r94/MutC1Counter` that is deleted at exit.

Pins re-derived before mutating — all three match `.ufo/waves/round-94/claims.json`:

| artifact | sha256 (observed) |
|---|---|
| `git show 96b5033:.ufo/waves/round-94/c1/knowledge-meter.py` | `03947734a0a01160b37eb1891b05561520ac4c1c9210d1ec627a109492161f67` |
| `git show 96b5033:.ufo/waves/round-94/c1/repair-map.tsv` | `11de45a74337b945b5179645e18e0f710a2f9ec54935450806a0e4bda7a78847` |
| `git show 96b5033:.ufo/waves/round-94/c1/labels.tsv` | `41bc438b04b0531a74bb9e52550fb968c0c818fee3aa315ad7ba99cd527a556b` |

HEAD copies of the same three paths hash identically (the C1 landing and C2 landing touch
neither file).

## Verdict

**STANDS — re-derived, no survivor.** The frozen counter at the freeze bytes, run exactly as
C1's P1 command with `--after-rev d51220a`, prints
`KNOWLEDGE-METER base=1008/1999 after=1009/2000 ... sites=19 labels=29 after_rev=d51220a…`,
`LIMB M0/M1/M3/M4/M5/M9/M10/M6 pass`, `KNOWLEDGE-METER-RESULT pass rc=0`
(`baseline-landed.txt`). Seventeen mutants, one contiguous change each, were run against
that run plus 9 rebuilt frozen controls and 6 purpose-built fixtures (16 detectors):
**17 killed, 0 survivors**. Ten kills come from the frozen detector set (seven from the
landed P1 run itself, three from rebuilt frozen controls), including the `after_rev` field
and the two-occurrence replace-all on
`considerthese-proposals-ledger.md:156`); seven mutants are invisible to the frozen suite and
were killed only by fixtures this seat had to build. Two qualifiers (R1, R2) and seven
frozen-suite coverage gaps are routed below; none of them re-scores C1 at the landing.

## Baseline (pristine bytes, no mutant)

| detector | observed |
|---|---|
| landed (lane, after=`d51220a`, labels=`96b5033`, map+sha pinned) | rc=0; `M0 pass base=1008/1999`, `M1 pass after=1009/2000`, `M3 pass bad_lines=0`, `M4 pass bad=none`, `M5 pass out_of_range=none`, `M9 pass rows=19 unbound=none`, `M10 pass labelled=29 want=19 mapped=19 kinds=excluded=10,range=19`, `M6 pass` |
| do-nothing (after=base) | rc=1; `LIMB M1 FAIL after=1008/1999`, `LIMB M3 FAIL bad_lines=18` |
| m3-union-applied (rebuilt) | rc=0; `sites=20 labels=30`, all limbs pass |
| m3-union-unmapped (rebuilt) | rc=1; `LIMB M3 FAIL bad_lines=1` |
| m5-cell-repair-lane-root (rebuilt) | rc=1; `LIMB M5 FAIL out_of_range=triage-thresholds.md:440` |
| m5-out-of-range (rebuilt) | rc=1; `LIMB M5 FAIL out_of_range=r94-ctl3.md:1` |
| m9-wrong-new (rebuilt) | rc=1; `LIMB M9 FAIL unbound=r94-ctl4.md:1` |
| m10-excluded-mapped (rebuilt) | rc=1; `LIMB M9 FAIL unbound=triage-thresholds.md:88`, `LIMB M10 FAIL unlabelled=triage-thresholds.md:88/SKILL.md:113-114` |
| missing-labels (rebuilt) | rc=2 |
| wrong-map-sha (rebuilt) | rc=1; `LIMB M6 FAIL sha256=11de45a7…` |

9 of the 12 frozen control rows were rebuilt as fixtures; the `candidate` row was reproduced
with the real C1 landing commit `d51220a` instead of the harness's throwaway candidate clone
`e7adac6`; every limb value and both rates equal the frozen receipt's candidate row. The two
`-before-r93` rows were not rebuilt: they invoke the round-93 counter and score the
predecessor, not the frozen instrument under mutation.

## Mutants (17, one change each; sha256 and unified diffs in `mutant-index.tsv`, `mutant-diffs.txt`)

| mutant | frozen target | the one change | verdict | killed by — observed limb delta |
|---|---|---|---|---|
| MU1-lane-split-semicolon | `lane_specs`, comma-combined value | `split(",")` → `split(";")` | killed | landed: `M4 pass bad=none` → `M4 FAIL bad=triage-thresholds.md:459` (the map's `SKILL.md:224-226,335-338` value stops parsing), rc 0→1 |
| MU2-lane-malformed-continue | `lane_specs`, malformed part | malformed part `return None` → `continue` | killed | fixture `cell_malformed_lane2`: pristine `M4 FAIL bad=triage-thresholds.md:440` → mutant all limbs pass, rc 1→0 |
| MU3-lane-loose-regex | `lane_specs`, malformed part | per-part regex end-anchor dropped (`5-` parses as 5) | killed | fixture `cell_malformed_lane2`: pristine `M4 FAIL` → mutant rc 1→0 |
| MU4-lane-first-part-only | M5 lane-root loop | `for lo, hi in lane:` → `lane[:1]` | killed | fixture `multi_part_oor`: pristine `M5 FAIL out_of_range=r94-ctl5.md:1` → mutant `M5 pass`, rc 1→0 |
| MU5-lane-hi-unchecked | M5 lane-root range | lane check `1<=lo<=hi<=len` → `1<=lo<=len` | killed | fixture `token_hi_oor`: pristine `M5 FAIL out_of_range=r94-ctl6.md:1` → pass, rc 1→0 |
| MU6-m3-replace-one | M3 replace-all | `fwd.replace(old,new)` → `replace(old,new,1)` | killed | landed: `M3 pass bad_lines=0` → `M3 FAIL bad_lines=1` (second `SKILL.md:1163` on ledger:156 survives), rc 0→1 |
| MU7-m3-first-row-per-site | per-site edit list | `setdefault((f,n),[]).append(...)` → `setdefault((f,n),[(old,new)])` | killed | landed: `M3 FAIL bad_lines=1` (triage:397's second row drops); `M9`/`M10` still pass, rc 0→1 |
| MU8-m3-old-not-once | M3 old-occurrence check | `if b.count(old) < 1:` → `if False:` | killed | fixture `old_absent2`: pristine `M3 FAIL old_not_once=1` → mutant `M3 pass`, rc 1→0 |
| MU9-excluded-drop-pair | EXCLUDED set | drop `("…triage-thresholds.md:356","SKILL.md:522")` | killed | landed: `M10 pass want=19 kinds=excluded=10` → `M10 FAIL want=20 kinds=excluded=9 unapplied=triage-thresholds.md:356/SKILL.md:522`, rc 0→1 |
| MU10-excluded-site-keyed | EXCLUDED membership | `(site,key) in EXCLUDED` → `site in EXCLUDED` | killed | landed: `M10 FAIL want=29 kinds=range=28,unknown=1 unknown=triage-thresholds.md:435/SKILL.md:10-11` and 10 `unapplied` pairs, rc 0→1 |
| MU11-m3-union-off | M3 labelled-file union | `labelled_files = {…} \| {…}` → `set()` | killed | control `m3-union-unmapped`: pristine `M3 FAIL bad_lines=1` → mutant `M3 pass`, rc 1→0 |
| MU12-m10-site-only | M10 completeness on (site,key) | `mapped = {(site,key)}` → `{site}` | killed | landed, by crash: `ValueError: too many values to unpack (expected 2)` in the M10 detail formatter, rc 0→1, no LIMB lines emitted |
| MU13-after-rev-prints-base | `after_rev` print | measurement line prints `a.base_rev` | killed | landed: `after_rev=d51220a…` → `after_rev=dff5a0a…` with every limb still `pass` and rc=0 — caught only by P1's printed-revision assertion |
| MU14-m6-always-pass | M6 map-sha pin | `got == a.map_sha256.lower()` → `True` | killed | control `wrong-map-sha`: pristine `M6 FAIL sha256=11de45a7…` → `M6 pass`, rc 1→0 |
| MU15-m9-excluded-allowed | M9 label binding | drop the `(site,key) in EXCLUDED` rejection | killed | control `m10-excluded-mapped`: pristine `M9 FAIL unbound=triage-thresholds.md:88` → `M9 pass` (M10 still fails, rc stays 1; the M9 line is the kill) |
| MU16-corpus-hi-unchecked | M5 corpus-value range | value check `1<=lo<=hi<=len` → `1<=lo<=len` | killed | fixture `corpus_hi_oor`: pristine `M5 FAIL out_of_range=r94-ctl8.md:1` → pass, rc 1→0 |
| MU17-dup-basename-allowed | M4 basename uniqueness | `bybase.get(name)==[…]` → `name in bybase` | killed | fixture `dup_basename`: pristine `M4 FAIL bad=r94-ctl9.md:1` → pass, rc 1→0 |

Kill counts per mutant across the 16 valid detectors are in `summary.json`; e.g. MU1 dies
on 13 detectors and MU6/MU7 on 12 (every fixture whose line diff depends on the same edit
path). A kill on one detector is sufficient; the extra ones are incidental.

## What the kills say about the claim's limbs

* **Comma-combined lane-root values (C1's "comma-combined" clause) are exercised at the
  landing, not only in fixtures.** MU1 dies on the landed P1 run at
  `triage-thresholds.md:459`, whose map value is `SKILL.md:224-226,335-338`.
* **Replace-all is exercised.** `considerthese-proposals-ledger.md:156` carries two
  occurrences of `SKILL.md:1163`; MU6 leaves the second one, M3 reports `bad_lines=1`.
* **The per-site edit list is exercised.** `triage-thresholds.md:397` has two map rows on
  one line; MU7 keeps only the first and M3 reports `bad_lines=1` while M9/M10 stay green.
* **M5 genuinely binds a lane-root token inside a cell replacement.** The rebuilt
  `m5-cell-repair-lane-root` control fails on pristine and passes when the loop skips later
  parts (MU4) or drops the `hi` bound (MU5), so the limb is live on that input.
* **EXCLUDED is non-empty and load-bearing.** Ten pairs; removing one or keying it on the
  site breaks M10 at the landing.
* **`after_rev` has no limb.** MU13 changes the printed revision while every limb and the
  exit code stay correct. The kill exists only because P1 names
  `after_rev=<C1 landing>` in the printed line; any consumer that trusts rc alone would miss
  a forged revision print.

## Baseline-failure discipline (two first-cut fixtures, discarded)

Two of my first fixtures had `rc=0` on the pristine counter, so their mutants were
"survivors" only against a broken baseline; both were rebuilt before being counted:

* `old_absent` put the label on `notes/r94-ctl7.md`, a file that exists only at the after
  rev. Pristine printed `rc=0`, `M3 pass same_files=True bad_lines=0`
  (`inconclusive-baseline-old_absent.txt`), because the M3 union only compares files present
  at **both** revs. Rebuilt as `old_absent2` on `corpus/QUALITY.md` (present at both revs):
  pristine `M3 FAIL old_not_once=1`, MU8 then passes → kill.
* `cell_malformed_lane` used `SKILL.md:5-9x`. Pristine printed `rc=0`
  (`inconclusive-baseline-cell_malformed_lane.txt`) because `LANE_VAL`'s character class
  never extracts that token. Rebuilt as `SKILL.md:5-` (matched by `LANE_VAL`, rejected by
  the per-part regex): pristine `M4 FAIL bad=triage-thresholds.md:440`, MU2/MU3 then pass →
  kills.

Both discarded baselines are also the evidence for R1 and R2.

## Routed qualifiers (not a claim re-score)

**R1 (counter, medium) — M3 silently skips a labelled file absent at `--base-rev`.**
The union adds a file only when `bf is not None and af is not None`
(`knowledge-meter.py`, `for rel in sorted(labelled_files - set(bfiles))`). A map row on a
file added at the after rev is therefore never compared, emits no limb and cannot fail.
Observed: a label/map pair claiming `` `SKILL.md:7` → `SKILL.md:8` `` on a one-line file
`notes/r94-ctl7.md` containing `no tokens here` prints `rc=0` and `M3 pass
same_files=True bad_lines=0` (`inconclusive-baseline-old_absent.txt`). The docstring's
"Every file named by a label or a map row is compared, including non-knowledge files" is
broader than the implementation for after-only files. C1's landing edits two files present
at both revs, so P1 is unaffected; route a fixture to round 95.

**R2 (counter, low) — a lane-root-looking token with a non-`[0-9,\- ]` character is
invisible to M4/M5.** `LANE_VAL` matches only `` `SKILL.md:([0-9][0-9,\- ]*)` ``, so a cell
replacement carrying `` `SKILL.md:5-9x` `` beside one valid `corpus/knowledge/…` value has
no lane value to bind: `lane=[]`, `vals=[…]`, `is_cell=True`, and the row passes every limb
(`rc=0`; `inconclusive-baseline-cell_malformed_lane.txt`). This is not the R2 class the
round-93 seat routed (that one was about a *well-formed* token inside a cell); here the
value is not parsed at all. No such token exists in the frozen map, so no verdict changes.

**Observation (not a defect of frozen bytes).** MU12 is killed by a `ValueError` inside
`short()`, the M10 detail formatter, before any limb line is printed. rc goes 0→1, so the
kill is real, but it is the same crash-as-detection shape round 93 routed as R1: a future
refactor of the M10 `mapped` set type would turn a bad counter into a traceback rather than
a named limb.

## Coverage gaps in the frozen control set (routed for round 95)

Seven mutants die only on fixtures the frozen 12-row suite does not contain; the harness
(`c1-controls-r94.py`) has no occurrence of `5-9x`, `99999`, `SKILL.md:5,`,
`mirror/triage` or `old_not_once`, and its only out-of-range token is the single-part
`SKILL.md:9999`:

1. multi-part lane token with an out-of-range **second** part (`SKILL.md:5,9999`) — MU4;
2. lane-range `hi` past EOF with `lo` in range (`SKILL.md:5-9999`) — MU5;
3. malformed lane part that `LANE_VAL` matches but the part regex rejects (`SKILL.md:5-`) —
   MU2, MU3;
4. corpus/knowledge value whose `hi` is past EOF — MU16 (the frozen `m5-out-of-range` only
   plants lane-root tokens);
5. duplicate basename outside `.ufo/` for a value's target file — MU17 (the round-93 seat's
   M06 was the same class and also had no control);
6. map `old` absent from its base line while `old`/`new` still match the label's derived
   edit — MU8;
7. (from R1) a labelled file that exists only at the after rev.

## Not a claim re-score

C1's P1/P2 still hold on the frozen and landed bytes: rc=0, `base=1008/1999`,
`after=1009/2000`, `sites=19 labels=29`, `M10 kinds=excluded=10,range=19`, M6 on the pinned
map sha, `after_rev=d51220a…`; the counter, map and labels hashes equal the claim pins. No
mutant changes that; R1/R2 and the seven gaps are instrument/coverage findings for round 95,
not permission to change the contract, the map or the labels.

## Receipts

All under `.ufo/waves/round-94/w1/MutC1Counter-receipts/` in the lane. Scratch root
`/fast/scratch/hyaku/kasegi-r94/MutC1Counter` (TMPDIR set to it; deleted at exit).

| command | observed |
|---|---|
| `git show 96b5033:…{knowledge-meter.py,repair-map.tsv,labels.tsv} \| sha256sum`; `sha256sum` on the HEAD copies | three hashes = the claim pins (`pins-r94-mutc1.txt`) |
| `python3 -B pristine-meter.py --lane <lane> --base-rev dff5a0a --after-rev d51220a --map .ufo/…/repair-map.tsv --labels-rev 96b5033 --base-target 1008/1999 --target 1009/2000 --map-sha256 11de45a7… --work <scratch>` | rc=0; M0..M6 pass, `base=1008/1999 after=1009/2000` (`baseline-landed.txt`) |
| `python3 -B driver.py` (builds 13 fixture clones + 1 mirror clone with `git clone --shared` from the lane, asserts each clone's `rev-parse --show-toplevel`, commits only inside scratch; runs pristine + 17 mutants × 16 detectors, 8-way) | `PRISTINE valid detectors: 14/16`; run 1: 14 mutants killed, MU2/MU3/MU8 inconclusive-baseline (driver stdout in the seat log) |
| `python3 -B driver2.py` (two corrected fixtures; pristine must fail before counting) | `PRISTINE2 old_absent2 rc=1 (M3 FAIL old_not_once=1)`, `cell_malformed_lane2 rc=1 (M4 FAIL bad=triage-thresholds.md:440)`; MU2, MU3, MU8 then `rc 1→0` (`baseline-old_absent2.txt`, `baseline-cell_malformed_lane2.txt`, `kill2-*.txt`) |
| `python3 -m py_compile mutants/*.py` | clean for all 17; one hunk each (`mutant-index.tsv`) |
| `for pat in 9999 5-9x 99999 mirror/triage 'SKILL.md:5,' QUALITY.md:537 old_not_once; do grep -c -F "$pat" .ufo/waves/round-94/controls/c1-controls-r94.py; done` | `0` for `5-9x`, `99999`, `mirror/triage`, `SKILL.md:5,`, `old_not_once`; `4` for `9999` (single-part only), `2` for `QUALITY.md:537`; frozen control names are the 12 in `c1-controls-r94.txt` |
| per-mutant killing runs | `kill-*.txt` (frozen detectors) and `kill2-*.txt` (purpose-built fixtures); exact limb deltas quoted in the table above |
| `python3 -B assemble.py` | 40 receipt files written, plus `pins-r94-mutc1.txt` (41 total: `summary.json`, `mutant-diffs.txt`, `mutant-index.tsv`, 18 baselines, 2 inconclusive baselines, 17 kill receipts) |

Tooling: no installs or upgrades; `python3 3.14.8`, `git 2.56.0`; no pacman transaction
(pacman is paused host-wide). Fixture commits stayed in the scratch clones; the lane's git
and jj state was only read (`show`, `ls-tree`, `archive` via the counter's own
`git -C <lane> archive`, `clone --shared`).
