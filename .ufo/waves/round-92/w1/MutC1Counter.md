# MutC1Counter — mutation test of the C1 knowledge-meter counter

Round-92 attempt 1, attack seat. Scope: the frozen C1 counter
`.ufo/waves/round-92/c1/knowledge-meter.py`, sha256
`631ad3dc291886dedd5e168f4ed05ff9e87af171f97b30deb88ee5093c0a2399`.
The lane file was never edited; the counter was copied into scratch and all
mutants are scratch-only. Findings below are coverage findings; the frozen
predicate was not changed and no claim is re-scored.

## Detector and kill rule

The detector is the frozen command itself:

```
python3 -B .ufo/waves/round-92/c1/knowledge-meter.py --lane LANE \
  --base-rev 0628fd247914555838a42c02ba5d4ac08b7e095d \
  --after-rev cb1ef2b9856df79c530f3ff1374fa9691ff56233 \
  --map .ufo/waves/round-92/c1/repair-map.tsv \
  --labels-rev d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d \
  --base-target 947/1947 --target 960/1944 \
  --map-sha256 6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772 \
  --work $S
```

(each run received the real map sha `6d87cafa…b772`; reproduced in
`receipts/reproduction.txt`). Each mutant was run on (a) the landing tree under
this command and (b) each of the eleven control variants of
`.ufo/waves/round-92/controls/c1-controls-r92.sh`, rebuilt once in a
scratch `git clone --shared` (toplevel asserted). **Killed** = the landing
verdict or any control verdict flips versus the pristine vector. A baseline
failure would be inconclusive; there was none.

Pristine vector (`P`/`F` over landing, candidate, no-work, partial-24-of-25,
partial-own-map, skip-qualify-59-own-map, excluded-437-applied,
no-edit-qualified, named-cell-155-token-only, drop-token-58-as-dash-cell,
wrong-key-column-86, working-tree-only):

```
P P F F F F F F F F F F
```

Reproduction checks (files in `receipts/`):

- landing: `base=947/1947 after=960/1944`, M0/M1/M3/M4/M5/M9/M10/M6 all pass.
- all eleven control contexts reproduce the `LIMB` and `KNOWLEDGE-METER` lines
  of `controls/c1-controls-r92.txt` **verbatim**, including the seven own-map
  sha256 lines. Variant commit ids differ from that receipt only because
  fixture commits embed wall-clock time; the trees and maps are the same bytes.
- the candidate-control tree differs from the landing tree only in C2 files
  (`corpus/SOURCES.md`, `corpus/source-snapshots/round-92/S136–S138` and the
  manifest); `corpus/knowledge/` is byte-identical, hence the same 960/1944.

29 mutants were built, one behavioral point each, as byte-level replacements of
the pristine source (`receipts/make_mutants.py`; unified diffs in
`receipts/mutants.diff`). Result: **7 killed by the existing control set, 22
survived. Of the 22, 15 are killed by a proposed control (each measured) and 7
are verdict-indistinguishable by any single-point control** (each proved
redundant/entailed in §C).

Full vectors and limb-level flips: `receipts/mutant-verdicts.tsv`,
`receipts/limb-flips.tsv`. Proposed-control recipes and measured outcomes:
`receipts/proposed-controls.tsv`. Fixture/harness sources:
`receipts/run_matrix.py`, `receipts/pc_matrix.py`.

## §A — killed by the existing detector set (7)

| mutant | mutated rule | flips |
|---|---|---|
| `m02_droptok_off` | drop-token branch disabled (`DROPTOK` test → `False`) | landing, candidate (M9 FAIL) |
| `m03_fixdash_off` | dash-cell branch disabled (`FIXDASH` test → `False`) | landing, candidate (M9,M10 FAIL) |
| `m04_lastcell_index` | `last_cell` returns `cells[-3]` | landing, candidate (M9 FAIL) |
| `m06_namedcell_as_named` | `"drop the"` test → `False` (named-cell as named) | landing, candidate (M9 FAIL) |
| `m07_named_as_namedcell` | `"drop the"` test → `True` (named as named-cell) | landing, candidate (M9 FAIL) |
| `m08_namedcell_prefix_off` | named-cell new drops the `MATCHES: ` prefix | landing, candidate (M9 FAIL) |
| `m09_m9_site_lookup` | `labels.get((site,key))` → `labels.get(site)` | landing, candidate (M9 FAIL) |

The candidate map's own edits bind every kind once, so these seven are detected
by the landing run alone — the controls add nothing for them.

## §B — survived the scripted controls, killed by a proposed control (15, measured)

Each entry is the exact diff (context elided) and the control that flips the
verdict. "pristine fails" is the proposed control's verdict under the unmutated
counter; the mutant then returns `pass`, so the verdict flips (kill).

| mutant | exact diff (`-` pristine, `+` mutant) |
|---|---|
| `m01_qualify_key_equality` | `- if m and m.group(1) == key:` / `+ if m:` |
| `m05_lastcell_guard` | `- … if line.rstrip().endswith("|") and len(cells) >= 3 …` / `+ … if len(cells) >= 3 …` |
| `m11_m9_new_only` | `- … exp[1:] != (old, new):` / `+ … exp[2:] != (new,):` |
| `m13_m10_unapplied_off` | `- unapplied = sorted(want - mapped)` / `+ unapplied = []` |
| `m15_m10_excluded_subset_off` | `- … and set(EXCLUDED) <= set(kinds),` / `+ … and True,` |
| `m19_m4_bybase_member` | `- … bybase.get(name) == [path] and …` / `+ … name in bybase and …` |
| `m20_m4_key_in_old_off` | `- if len(vals) != 1 or ("\`%s\`" % key) not in old:` / `+ if len(vals) != 1:` |
| `m21_m3_oldcount_zero` | `- if b.count(old) != 1:` / `+ if b.count(old) < 1:` |
| `m22_m3_dup_off` | `- dup += 1` / `+ pass` |
| `m23_m3_samefiles_true` | `- same_files = set(bfiles) == set(afiles)` / `+ same_files = True` |
| `m24_m6_sha_off` | `- limbs.append(("M6", got == a.map_sha256.lower(), …))` / `+ limbs.append(("M6", True, …))` |
| `m25_m0_base_off` | `- ("M0", (bn, bm) == (bn0, bm0), …)` / `+ ("M0", True, …)` |
| `m26_m1_after_off` | `- ("M1", (an, am) == (tn, tm), …)` / `+ ("M1", True, …)` |
| `m27_m5_hi_off` | `- … not (1 <= lo <= hi <= len(text.splitlines())):` / `+ … not (1 <= lo <= len(text.splitlines())):` |
| `m28_m5_off` | `- if text is None or not (1 <= lo <= hi <= …):` / `+ if False:` |

Killing controls (all measured against the unmutated counter and the mutant;
pristine → mutant verdict):

- **PC-A** (m24): landing tree, frozen map, `--map-sha256` = 64 zeros →
  `fail / M6` → `pass`. (Existing controls flip M6 to pass in seven contexts
  but always alongside another failing limb.)
- **PC-B** (m25): landing tree, `--base-target 948/1947` → `fail / M0` → `pass`.
- **PC-C** (m26): landing tree, `--target 961/1944` → `fail / M1` → `pass`.
- **PC-E** (m13): the `partial-24-of-25` commit, its own map, own sha, and
  `--target 959/1944` (from that control's printed rate) → `fail / M10
  (unapplied)` → `pass`.
- **PC-F** (m15): labels rev = frozen labels minus the row for
  `triage-thresholds.md:437`; landing after-rev + frozen map/sha/targets →
  `fail / M10 (EXCLUDED subset)` → `pass`.
- **PC-G** (m19): candidate edits plus a tracked non-scope file
  `corpus/other/mission-control.md` (basename collision) → `fail / M4,M5` →
  `pass`. The repo currently has no duplicate basename involving
  `corpus/knowledge/` (checked at the landing rev), so only a fixture can test
  this.
- **PC-H** (m22): candidate after-rev + frozen map with the row for
  `triage-thresholds.md:86` duplicated, own sha → `fail / M3 (dup_rows=1)` →
  `pass`.
- **PC-I** (m23): candidate edits plus a tracked, uncited
  `corpus/knowledge/zz-extra.md` → `fail / M3 (same_files=False)` → `pass`.
- **PC-J** (m11): BASE + 24 frozen edits, and row 86 applied as
  old `MATCHES: \`intake-surface.md:71\`,` → new
  `\`corpus/knowledge/intake-surface.md:83-88\`` (label-correct new,
  non-label old), own sha → `fail / M9` → `pass`.
- **PC-K** (m20): labels rev adds `(triage-thresholds.md:437,
  mission-control.md:37-38)` as a content-repair whose fix carries "drop the"
  (a named-cell whose base line cell lacks the key); after replaces 437's last
  cell with `MATCHES: \`corpus/knowledge/mission-control.md:56-57\``; own sha;
  `--target 959/1942` (measured) → `fail / M4,M5` → `pass`.
- **PC-L** (m01): labels rev changes row 59's qualify target to
  `corpus/knowledge/mission-control.md:19-21` (different from the label key);
  landing after-rev + frozen map/sha/targets → `fail / M9,M10` → `pass`.
  (Note: `m01` alone leaves the derived edit using `key`, so the map must keep
  the key-derived value; only the label's fix target is changed.)
- **PC-M** (m27, m28): labels rev repoints row 90 to
  `corpus/knowledge/mission-control.md:1-9999` (past EOF), after applies that
  edit, own sha, `--target 961/1945` (measured; the new distinct anchor shifts
  the rate) → `fail / M5` → `pass` for both mutants.
- **PC-N** (m05): synthetic lane fixture. `x.md` line 3 is
  `a | b \`x.md:1\` | tail` (contains pipes, does not end in `|`); a
  named-cell label (fix carries "drop the") maps old `b \`x.md:1\`` to
  `MATCHES: \`corpus/knowledge/x.md:2\``; base-target 0/1, target 1/1 →
  `fail / M9` → `pass`.
- **PC-O** (m21): synthetic lane fixture. `x.md` line 3 contains `x.md:1`
  twice; a range label repoints to `corpus/knowledge/x.md:1`; the after tree
  replaces the first occurrence; base-target 0/1, target 1/2 →
  `fail / M3 (old_not_once=1, bad_lines=1)` → `pass`.

Both synthetic fixtures carry the two frozen EXCLUDED label rows so M10's
EXCLUDED-subset limb can pass; their labels blob is their base commit.

## §C — survived; no single-point control distinguishes them (7)

Each is a real behavioral change, but the verdict is already determined by
another limb in every possible control, so no mutation of the control suite can
flip it. These are redundancy findings, not licence to change the predicate.

1. **`m10_m9_excluded_off`** — drops `(site, key) in EXCLUDED` from M9's
   reject condition.
   diff: `- if lab is None or (site, key) in EXCLUDED or exp is None or exp[1:] != (old, new):`
   / `+ if lab is None or exp is None or exp[1:] != (old, new):`
   A mapped EXCLUDED pair that matches its label now passes
   M9, but M10's `unlabelled` limb still fails; one that does not match fails
   M9 on the `exp[1:]` comparison anyway. Measured: PC-D (excluded-437 applied,
   own sha, `--target 961/1944`) gives pristine `fail / M9,M10`; `m10` gives
   `fail / M10`. No flip.
2. **`m12_m10_unlabelled_off`** — disables M10 `mapped - want`.
   diff: `- unlabelled = sorted(mapped - want)` / `+ unlabelled = []`
   Every mapped
   pair outside `want` is kind `excluded` or `no-edit`; M9 rejects mapped
   EXCLUDED pairs outright and mapped no-edit pairs through `exp is None`.
   Hence M10's unlabelled limb is implied by M9. Measured: same PC-D; `m12`
   gives `fail / M9`. No flip. (`m10` and `m12` are mutually redundant: either
   guard can be deleted alone with no verdict change, but not both.)
3. **`m14_m10_unknown_off`** — removes `not unknown`.
   diff: `- … not unlabelled and not unknown and set(EXCLUDED) <= set(kinds)`
   / `+ … not unlabelled and set(EXCLUDED) <= set(kinds)`
   An unknown-kind pair is
   in `want`; if mapped it fails M9 (`exp` is `(kind, None, None)` and the map
   strings can never be `None`), if unmapped it fails M10 `unapplied`. Measured:
   labels rev with a `content-repair` / fix `Repoint later.` row (unknown kind,
   unmapped) gives pristine `fail / M10`; `m14` also `fail / M10` (unapplied
   remains). No flip.
4. **`m16_m10_want_nonempty_off`** — removes `bool(want)`.
   diff: `- bool(want) and not unapplied and not unlabelled …`
   / `+ not unapplied and not unlabelled …`
   If `want` is empty,
   every label pair is excluded/no-edit; `rows` non-empty (else M3/M4/M9 fail
   `bool(rows)`) implies `mapped` non-empty, so `unlabelled = mapped - want` is
   non-empty and M10 fails regardless. If `rows` is empty, M3/M4/M9 fail. No
   flippable control exists.
5. **`m17_m4_bare_off`** — disables M4's removal-row BARE check.
   diff: `- if len(BARE.findall(old)) != 1 or BARE.findall(old)[0] != key:`
   / `+ if False:`
   M4's removal
   branch runs only for `new` in `{—, ""}`; the M9-bound edit for those rows is
   exactly `("MATCHES: \`key\`", "—")` or `(", \`key\`", "")`, on which
   `BARE.findall(old) == [key]` always holds. Measured limb evidence: in the
   `drop-token-58-as-dash-cell` control M4/M5 flip to pass, but M9 (and M6)
   still fail, so the verdict does not move.
6. **`m18_m4_valany_any`** — relaxes M4's `len(vals) != 1` to `< 1`.
   diff: `- if len(vals) != 1 or ("`%s`" % key) not in old:`
   / `+ if len(vals) < 1 or ("`%s`" % key) not in old:`
   Every
   non-removal edit M9 accepts writes exactly one backticked
   `corpus/knowledge/<name>.md:N-M` value, so the check can never fire on an
   M9-passing row. No flippable control exists.
7. **`m29_m4_internal_off`** — drops the `resolve.classify(...) == "INTERNAL"`
   test.
   diff: `- … bybase.get(name) == [path] and A["classify"](vals[0]) == "INTERNAL":`
   / `+ … bybase.get(name) == [path]:`
   `bybase.get(name) == [path]` means the `corpus/knowledge/<name>.md`
   path is tracked at the after-rev, hence present in the archive extract, and
   `classify` returns INTERNAL for any existing lane-relative token. No
   flippable control exists (the check is already covered by M4's
   tracked-basename test).

## Control-suite gap

The eleven scripted controls are all `fail` verdicts except the candidate. A
disabled limb is therefore masked whenever another limb already fails, which is
why 22/29 mutants survive: `receipts/limb-flips.tsv` shows `m12` flipping M10
to pass in two controls, `m13` in two, `m17`/`m20` flipping M4–M5, `m24`
flipping M6 in seven, and `m26` flipping M1 in eight — with no verdict change.
The low-cost repair is to add isolating controls that pin their own map sha and
a target equal to their own measured rate, so the exercised limb is the only
failing one. The fifteen PC recipes above are exactly that; three of them
(PC-A/B/C) are single invocations of the landing command with one argument
mutated.

## Hand-off notes

- Counter bytes unchanged in the lane; re-checked `sha256` equals
  `631ad3…a2399` after the run (`receipts/hashes.txt`). The frozen map sha and
  labels blob are recorded there too.
- All mutant fixtures, clones and synthetic lane repos lived only in scratch
  `/fast/scratch/hyaku/kasegi-r92/MutC1Counter/`; that scratch root has been
  deleted (`test ! -e` verified) and no fixture bytes or credential-shaped
  values were written into the lane.
- Scratch harnesses are receipts, not lane instruments: `make_mutants.py`
  regenerates the mutant files and diffs, `run_matrix.py` runs the landing +
  control matrix, `pc_matrix.py` builds and runs the proposed controls. They
  hardcode the scratch root and expect the frozen map/labels at the frozen
  paths.
- These findings route defects/qualifiers only; they do not re-score C1 depth
  or C2 coverage.

## Files written

- `.ufo/waves/round-92/w1/MutC1Counter.md` (this report)
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/mutant-verdicts.tsv`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/limb-flips.tsv`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/proposed-controls.tsv`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/mutants.diff`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/reproduction.txt`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/hashes.txt`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/make_mutants.py`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/run_matrix.py`
- `.ufo/waves/round-92/w1/MutC1Counter-receipts/pc_matrix.py`
