# MutC1Counter — mutation test of the frozen round-86 C1 counter

Seat: MutC1Counter (UFO-FSD mutation tester, wave w1, round 86 attempt 1). Scope: **one
mutation probe of `.ufo/waves/round-86/c1/knowledge-meter.py`**, nothing else. The frozen
counter, map, resolve.py and control script were never edited (hashes below).

## Verdict

- **30 single-point mutants**, **23 controls** (7 frozen + 16 extension), **713 cells**,
  0 missing. **Killed 24/30 = 80.0%**. Survived 6 (`m11`, `m12`, `m16`, `m17`, `m18`,
  `m29`) — every survivor is provably equivalent or dead at this base (proofs below), so
  none is a contract defect; they are dead weight in the meter.
- **The frozen 7-control suite alone kills only 6/30 = 20.0%** (`m04`, `m13`, `m14`,
  `m24`, `m25`, `m27`). It cannot see: a meter that compares only the numerator, a meter
  that reads no target at all, a meter that never checks anchor range, a meter that
  accepts any target path, a meter that drops M2 entirely.
- **Limbs individually self-protecting** (a control fails on that limb alone):
  **M1** (`tgt-den`, `tgt-lo`), **M3** (`prose`, `ghost`, `blank-line`), **M5**
  (`stale-lo`, `stale-range`), **M6** (`map-sha`, `mapsha-prefix`).
  **M2 and M4 never fail alone**: M2 is implied by M3, M4 is always coupled into M5 by
  `not m4bad`.

## Frozen inputs, measuring root, restoration

| item | value |
|---|---|
| counter | `.ufo/waves/round-86/c1/knowledge-meter.py` sha256 `03df491be611e8b9a3328cb7df673d9b54e93e4d1d1b856b5e678ad7949e50ee` |
| map | `.ufo/waves/round-86/c1/repair-map.json` sha256 `dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12` |
| resolve.py | `corpus/instruments/resolve.py` sha256 `db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667` |
| controls script | `.ufo/waves/round-86/controls/c1-controls-r86.sh` sha256 `7f1126c2a8f63d9029b9e69f1f89745f6e0ae1ae3a109aba8b073c2538362c4f` |
| base / freeze rev | `d7296645c2cd9f631329fa8e2f38328a4c9c89a5` / `252df0c90c066d83d229e3107811a6bc05e8feed` |

Root: per-control `git clone --shared <lane> <scratch>/trees/<name>` + `git checkout <base>`
(HEAD asserted equal to base). 15 clones. `python3 -B` throughout; no `__pycache__`.
**Restoration evidence:** all four hashes above re-checked after the run and identical; no
git/jj writes anywhere (read-only `clone/checkout/show/ls-files/ls-tree/cat-file` only);
no writes in the lane outside `.ufo/waves/round-86/w1/`; scratch root deleted. Pre-existing
lane state `M corpus/QUALITY.md, M corpus/SOURCES.md, M round-86/S122.txt,
M round-86/manifest.json, ?? .ufo/waves/round-86/l1/` was present before and after and is
not this seat's.

## Method and harness equivalence

The frozen driver was re-created exactly (`fresh`/`apply-map`/half/decite/pad/wrong-file/
map-sha) but with the counter path as a parameter, then **all 7 frozen controls reproduce
`c1-controls-r86.txt` line for line — `KNOWLEDGE-METER`, every `LIMB` detail string and
`RESULT` — 7/7 exact** (`compare_frozen.py`). Trees are built once and measured read-only
(each run writes only its own `kmeter-*` temp dir), which is byte-equivalent to the frozen
driver's per-control clones.

Kill rule used: a mutant is killed if any control's **verdict** changes (negative passes /
positive fails), the `KNOWLEDGE-METER-RESULT` line disappears, or an assertion-class
control's asserted line changes presence. Failures that leave the verdict unchanged do not
count as kills.

Mutants: 30 single-point edits, each `old` string asserted to occur exactly once in the
frozen source (hashes in `mutants-hashes.txt`). Mutant scratch copies live in
`receipts/mutants/`.

## Controls (23) — pristine behaviour and isolation

Frozen 7, re-created exactly:

| control | pristine | limbs FAIL | isolated limb |
|---|---|---|---|
| do-nothing | fail | M1,M2,M3 | no |
| positive | **pass** | – | – |
| partial | fail | M1,M2,M3 | no |
| decite | fail | M1,M3 | no |
| pad | fail | M1,M2,M3 | no |
| wrong-file | fail | M4,M5 | no (M5 fails only via `not m4bad`, `out_of_range=none`) |
| map-sha | fail | M6 | **M6** |

16 extension controls (all built from the same base clones; trees differ only as stated):

| control | mutation vs frozen set | class | pristine | limbs FAIL | isolated |
|---|---|---|---|---|---|
| tgt-den | `--target 596/1717` on positive tree | verdict | fail | M1 | **M1** |
| tgt-lo | `--target 595/1715` on positive tree | verdict | fail | M1 | **M1** |
| prose | positive tree + one prose word changed, no token touched | verdict | fail | M3 | **M3** |
| ghost | positive tree + extra zero-citation `corpus/knowledge/meter-ghost.md` | verdict | fail | M3 | **M3** |
| blank-line | positive tree + one trailing newline in a knowledge file | verdict | fail | M3 | **M3** |
| stale-lo | positive tree + `round-45/S071.txt` truncated to 100 lines (map anchor `:117`) | verdict | fail | M5 (`out_of_range=S071.txt:117`) | **M5** |
| stale-range | same file truncated to 371 lines (map anchor `:371-372`) | verdict | fail | M5 (`out_of_range=S071.txt:371-372`) | **M5** |
| uniq | frozen map with `S016.txt` swapped for `S029.txt:20` → one of its 41 snapshot copies | verdict | fail | M4 (`bad=S029.txt:20`),M5 | no |
| keym | frozen map with `S016.txt` swapped for a GONE **non-KEY** token (`!== sha256File(evidence/manifest.json)`) → `corpus/knowledge/citation-bases.md` | verdict | fail | M4,M5 | no |
| mapsha-prefix | correct sha with the last 56 hex chars zeroed | verdict | fail | M6 | **M6** |
| result-assert | wrong-file + assert a `KNOWLEDGE-METER-RESULT` line exists | assertion | fail | M4,M5 | no |
| anchor-mismatch | map value has no anchor while the key has `:20` (swap on `S016.txt`) | assertion | fail | M4 (`bad=S029.txt:20`),M5 | no |
| deleted-target | positive tree + `round-45/S071.txt` deleted from the worktree (still tracked) | assertion | pass-assert (`LIMB M4 FAIL` present) | M1,M4,M5 | no |
| assert-m2-donothing | assert `LIMB M2 FAIL` on do-nothing | assertion | pass-assert | M1,M2,M3 | no |
| assert-m2-pad | assert `LIMB M2 FAIL` on pad | assertion | pass-assert | M1,M2,M3 | no |
| assert-m5-wrongfile | assert `LIMB M5 FAIL` on wrong-file | assertion | pass-assert | M4,M5 | no |

Why each extension is needed: the swap maps keep **203 keys and exactly 596/1716** (M1, M2,
M3 all pass), so the only failing limb is the one under test. `stale-*` truncates a tracked
snapshot instead of editing the map, because **M4's anchor agreement forces a value's anchor
to equal its key's anchor** — no map at the frozen target can produce an out-of-range anchor.

## Mutants and kill matrix

| mutant | limb | verdict | killed by |
|---|---|---|---|
| m01_M1_true | M1 | killed | tgt-den, tgt-lo |
| m02_M1_numerator_only | M1 | killed | tgt-den |
| m03_M1_tuple_ge | M1 | killed | tgt-lo |
| m04_M1_base_rate | M1 | killed | positive |
| m05_M1_target_hardcoded | M1 | killed | tgt-den, tgt-lo |
| m06_M2_true | M2 | killed | assert-m2-donothing, assert-m2-pad |
| m07_M2_no_added | M2 | killed | assert-m2-pad |
| m08_M2_no_removed | M2 | killed | assert-m2-donothing |
| m09_M3_true | M3 | killed | prose, ghost, blank-line |
| m10_M3_no_line_equality | M3 | killed | prose, blank-line |
| m11_M3_no_hit_keys | M3 | **SURVIVED** | – |
| m12_M3_no_same_files | M3 | **SURVIVED** | – |
| m13_M3_no_forward_subst | M3 | killed | positive |
| m14_M4_true | M4 | killed | wrong-file, uniq, result-assert, assert-m5-wrongfile, deleted-target |
| m15_M4_no_uniqueness | M4 | killed | uniq |
| m16_M4_no_prefix | M4 | **SURVIVED** | – |
| m17_M4_no_endswith | M4 | **SURVIVED** | – |
| m18_M4_no_key_gone | M4 | **SURVIVED** | – |
| m19_M4_no_internal | M4 | killed | deleted-target |
| m20_M4_no_anchor_agreement | M4 | killed | anchor-mismatch |
| m28_M4_nonkey_skip | M4 | killed | keym |
| m21_M5_true | M5 | killed | stale-lo, stale-range, assert-m5-wrongfile |
| m22_M5_no_hi_vs_nlines | M5 | killed | stale-range |
| m23_M5_no_m4bad | M5 | killed | assert-m5-wrongfile |
| m24_M5_upper_strict | M5 | killed | positive |
| m25_M6_true | M6 | killed | map-sha, mapsha-prefix |
| m26_M6_prefix8 | M6 | killed | mapsha-prefix |
| m27_rate_internal_only | rate→M1 | killed | positive |
| m29_M4_no_tracked_nonempty | M4 | **SURVIVED** | – |
| m30_M3_no_linecount | M3 | killed | blank-line |

Attribution of the 24 kills: frozen set 6, extension verdict-level controls 12,
assertion-class controls 6. Witness outputs in `witnesses.txt` (e.g. `m14` turns the
wrong-file control into a **pass**; `m20` crashes with
`AttributeError: 'NoneType' object has no attribute 'startswith'` and loses the RESULT line;
`m19` prints `LIMB M4 pass` on deleted-target; `m02` prints `LIMB M1 pass after=596/1716`
against `target=596/1717`).

## What the frozen suite structurally cannot see

1. **M1's tree reading is implied by M2∧M3.** Once the tokens and the per-line substitution
   match, `after` is a pure function of `(base scope, map)`, so its rate is forced. Only the
   *target comparison* is independent. `m01`/`m02`/`m03` change only the tree reading and no
   frozen control moves; `m02` (numerator-only) passes all seven. Only `tgt-den`/`tgt-lo`
   (wrong target, unchanged tree) kill them.
2. **M2 is implied by M3.** `after == base-with-`k`→`v`` gives `added ⊆ vals` and
   `removed == keys` (the substitution is the only edit). Every M2 clause mutant survives
   every verdict-level control; only output assertions on the `LIMB M2` line kill them.
3. **M5's range check is unreachable through the map.** M4 requires
   `path + anchor == v`, so a value's anchor is its key's anchor; every one of the 197
   anchored cited tokens is in range for its unique snapshot (0 out-of-range). The frozen
   wrong-file control shows `out_of_range=none` — its M5 failure is only the `not m4bad`
   coupling. A counter that never checks the range (`m21`, `m22`) is invisible to all seven
   frozen controls; it took a *tree* change (truncated snapshot → `stale-lo`/`stale-range`)
   to expose it. This is the sharpest verifiability gap.
4. **M4 sub-checks at this base:** uniqueness is live (89 of 292 cited GONE tokens were
   excluded for exactly that reason); KEY match is live (`keym`); anchor agreement guards a
   crash path (`anchor-mismatch`); classify-INTERNAL is reachable only when a tracked
   snapshot is missing from the worktree (`deleted-target`). Prefix is dead: of 292 cited
   GONE KEY tokens, 203 have a unique basename and **0** of those unique copies lie outside
   `corpus/source-snapshots/`. Endswith and key-GONE are implied/vacuous (below).
5. **`not m4bad` in M5 is redundant** with M4 (`m23` survives every verdict-level control;
   only the M5 line assertion kills it).

## Survivors — proof and the control that would kill each

| mutant | expected limb | why it survives | control that would kill it |
|---|---|---|---|
| m11_M3_no_hit_keys | M3 | **Equivalent.** M2's `removed == keys` plus `after == fwd(base)` (M3's own `bad == 0`) imply every key occurred backticked in a base line, i.e. `hit == keys`. The clause is dead code inside the conjunction. | **None exists.** No tree can satisfy M2 and `bad==0` while missing a `hit` key. Fix is to delete `hit == keys` (or keep as an assertion of intent); a control cannot distinguish it. |
| m12_M3_no_same_files | M3 | **Equivalent.** The same `same_files` value also gates the line loop (`if same_files:`); when the file sets differ, `hit` stays empty and `hit == keys` fails M3. Removing the verdict conjunct leaves the guard doing the same work. | **None exists** while the guard is present. (If the guard were removed, `ghost` would already kill it — it kills `m09` today.) |
| m16_M4_no_prefix | M4 | **Dead at this base.** 0/203 unique-basename cited GONE tokens have their only tracked copy outside `corpus/source-snapshots/`, so no admissible map value can fail the prefix test while passing uniqueness/endswith. | **Recipe, currently unreachable:** cite a bare `S068.txt` (its only tracked copy is `.ufo/waves/round-29/wave1/assimilation/fetch/S068.txt`), then swap it in for a droppable frozen key (203 keys, 596/1716). Pristine would fail only M4 (prefix); the mutant passes → killed. Verified today: bare `S068.txt`/`S070.txt`/`S072.txt` occur 0 times backticked in the base knowledge scope (`git grep <base> -- corpus/knowledge/`). |
| m17_M4_no_endswith | M4 | **Equivalent.** `bybase.get(name) == [path]` means `path` is the unique tracked file whose basename is `name`, so `path.endswith("/" + name)` always holds given the prefix check. | **None exists.** Delete the conjunct (or keep as belt-and-braces). |
| m18_M4_no_key_gone | M4 | **Vacuous.** A bare `S<digits>.txt` relative token can only resolve at the lane root; the base tree has **0** files matching `^S[0-9]{3,}\.txt$` at the root, so `bcls.get(k)` is GONE for every KEY-matching key. | **None without a contract change:** a committed lane-root `S###.txt` (the wave contract forbids copying snapshots into w1 for exactly this reason). |
| m29_M4_no_tracked_nonempty | M4 | **Vacuous in the harness.** `tracked` comes from `git ls-files` in a base checkout (16310 entries); a non-empty checkout always satisfies `bool(tracked)`. | **None:** the falsifier is a lane clone with an empty index, which is not a valid lane and would fail everything else. |

## Recommendations (routed, not applied)

Controls worth freezing alongside the seven (all cheap; each isolates a limb the frozen set
cannot reach): `tgt-den`, `tgt-lo`, `prose`, `ghost`, `blank-line`, `stale-lo`,
`stale-range`, `uniq`, `keym`, `mapsha-prefix`, plus assertion-class `anchor-mismatch`,
`deleted-target`, `assert-m2-*`, `assert-m5-wrongfile`. If the contract wants the frozen
seven kept as-is, treat those 16 as the r86 verifiability extension rather than as
replacements.

Dead/redundant clauses that a 6-month reader will trip on: M2 as a whole (implied by M3),
M1's tree reading (implied by M2∧M3), M3's `hit == keys` and the duplicated `same_files`,
M4's `endswith`/`INTERNAL`/`GONE`/`bool(tracked)` and the prefix test on this corpus, and
M5's `not m4bad`. Either delete them or state in the docstring that they are forward-looking
guards (prefix and key-GONE become live only if a knowledge file cites a bare name whose
unique copy lives outside the snapshot tree / at the lane root).

## Reproduction

```
S=/fast/scratch/hyaku/kasegi-r86/MutC1Counter   # recreate (printf path is deleted)
mkdir -p $S; cp <lane>/.ufo/waves/round-86/c1/knowledge-meter.py $S/knowledge-meter.orig.py
python3 -B $S/gen_mutants.py                    # 30 mutants, each edit asserted unique
python3 -B $S/build_controls.py                 # frozen 7 + 9 verdict extension controls, pristine checks
python3 -B $S/add_controls.py; python3 -B $S/add_blank.py; python3 -B $S/add_deleted.py
python3 -B $S/run_matrix.py --controls all --counters all --jobs 6 --report
python3 -B $S/compare_frozen.py                 # 7/7 exact vs c1-controls-r86.txt
```

## Files written by this seat

- `.ufo/waves/round-86/w1/MutC1Counter.md` (this report)
- `.ufo/waves/round-86/w1/MutC1Counter-receipts/`: `facts.txt`, `witnesses.txt`,
  `mutants-hashes.txt`, `matrix-grid.txt`, `table_controls.md`, `table_mutants.md`,
  `results.json` (713 cells, full stdout), `controls.json`, `knowledge-meter.orig.py`
  (frozen bytes), harness scripts (`gen_mutants.py`, `build_controls.py`, `add_controls.py`,
  `add_blank.py`, `add_deleted.py`, `run_matrix.py`, `compare_frozen.py`, `pick_tokens.py`,
  `scan_anchors.py`), the generated maps (`half.json`, `wrongfile.json`, `uniq.json`,
  `keym.json`, `anchor-mismatch.json`) and `mutants/` (30 mutant files).

No `S<digits>.txt` was copied into the wave dir. No lane file outside `w1/` was written.
