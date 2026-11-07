# MutC1Counter — round-85 C1 counter mutation test

**Seat:** MutC1Counter (leaf mutation-tester, no dispatch). **Probe:** one mutation
campaign against the frozen C1 counter `.ufo/waves/round-85/c1/skill-meter.py`
(read-only). **Scratch:** `/fast/scratch/hyaku/kasegi-r85/MutC1Counter`
(deleted at exit; receipts copied first). **Lane writes:** only this report and
`MutC1Counter-receipts/` under `.ufo/waves/round-85/w1/`.

**Verdict in one line:** 20 single-point mutants; the six frozen pre-freeze
controls kill **4/20** (`m09`, `m10`, `m19`, `m20`) and leave **16 survivors**;
ten added controls kill every survivor — seven exit-code controls (C1–C7) and
three named-limb assertions (C8–C10). Four survivors (`m04`–`m06`, `m08`) are
**verdict-equivalent by construction**: no exit-code control can ever kill them
(proof in §Equivalence); only limb-level assertions reach those rules.

## Frozen artifacts and oracle

| artifact | sha256 (before == after) |
|---|---|
| `.ufo/waves/round-85/c1/skill-meter.py` | `89c5d47b4dc04df90129d5a3bd443bb877f22ba9f1565008daa7024557634ed6` |
| `.ufo/waves/round-85/c1/repair-map.json` (18 entries) | `b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944` |
| base `SKILL.md` @ `bc722e540c93b48ff159454b65a0f9f4630db1ed` | `8df45d27e36e5dac62cdd7f56df6f6f2f85333d972be45fee0f751b8381b4104` |
| accepted after (`positive.md`, 18 repairs) | `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552` |
| `c1/apply-map.py` | `8eb22d7db99b820ab8209106f9db634bf5ef88aeb6dbb271e3ec514122b98c93` |

The oracle was **held fixed** for every mutant run: `--target 167/732` and
`--map-sha256 b575f147…`. A mutant that perturbs the meter must not be allowed
to re-derive its own target from its own output — the frozen control script
derives `T` with the counter under test, so mutants are run with the recorded
oracle instead. Base measure is `158/741`; positive-after measure is `167/732`.

**Reuse warning for round 86:** `c1-controls-r85.sh` derives
`T=$($M --measure positive)`, i.e. from the counter under test. That is sound at
freeze time (the frozen counter is trusted), but as a re-runnable mutation
detector it makes the oracle self-referential — a rate-perturbing mutant could
move the target it is judged against. Every control in §Proposed pins `T` and
the map sha explicitly.

## Baseline (pristine arm)

The six frozen controls were rebuilt in scratch with the frozen commands from
`controls/c1-controls-r85.sh` (same `git show`, same `apply-map.py` invocations,
same delete-gone python block, same pad line). Measured rates:
`base=158/741`, `pad=168/751`, `delgone=158/723`, `wrong=168/733`,
`partial=164/738`, `positive=167/732` — identical to the frozen receipt. All six
blocks (`SKILL-METER base=…`, five `LIMB` lines, `SKILL-METER-RESULT`) match
`controls/c1-controls-r85.txt` **line for line** (conformance PASS). Pristine rc:
five reject controls `1`, positive `0`. Every mutant run finished with `rc ∈ {0,1}`
and empty stderr (no crashes, no inconclusive runs).

## Mutants and results

20 mutants, each a single-point edit (one hunk; full diffs in
`MutC1Counter-receipts/mutants/*.diff`). The detector for every row is the frozen
six-control set (fixed oracle); `SURVIVED` means all six outcomes matched the
recorded expectations.

| # | mutant | single-point change | frozen controls killing it | new control killing it |
|---|---|---|---|---|
| m01 | `m01-m1-numerator-only` | M1 `(an,am)==(tn,tm)` → `an==tn` | **SURVIVED** | C1 |
| m02 | `m02-m1-limb-dropped` | M1 limb never appended | **SURVIVED** | C1 |
| m03 | `m03-m1-ge` | M1 `==` → `an >= tn` | **SURVIVED** | C1 |
| m04 | `m04-m2-drop-added` | M2 drops `and added<=vals` | **SURVIVED** | C8† |
| m05 | `m05-m2-keys-subset` | M2 `removed==keys` → `keys<=removed` | **SURVIVED** | C9† |
| m06 | `m06-m2-any-overlap` | M2 `removed==keys` → `bool(removed&keys)` | **SURVIVED** | C9† |
| m07 | `m07-m3-skip-linecount` | M3 `len(base)==len(after)` → `True` | **SURVIVED** | C2 |
| m08 | `m08-m3-drop-hit` | M3 `bad==0 and hit==keys` → `bad==0` | **SURVIVED** | C10† |
| m09 | `m09-m3-self-replace` | M3 replaces key with key | positive | — |
| m10 | `m10-m3-hit-from-after` | M3 looks for keys in `al`, not `fwd` | positive | — |
| m11 | `m11-m4-drop-ufo` | M4 drops `.ufo/` exclusion | **SURVIVED** | C4 |
| m12 | `m12-m4-drop-endswith` | M4 drops `endswith("/"+key)` | **SURVIVED** | C5 |
| m13 | `m13-m4-drop-internal` | M4 drops `classify==INTERNAL` | **SURVIVED** | C6 |
| m14 | `m14-m4-drop-base-gone` | M4 drops `bcls.get(k)=="GONE"` | **SURVIVED** | C7 |
| m15 | `m15-m5-ignored` | M5 `if a.map_sha256:` → `if False and …` | **SURVIVED** | C3 |
| m16 | `m16-m5-prefix` | M5 full sha → 8-hex prefix | **SURVIVED** | C3 |
| m17 | `m17-verdict-ignores-m4` | verdict skips `M4` | **SURVIVED** | C4, C5, C6, C7 |
| m18 | `m18-verdict-ignores-m5` | verdict skips `M5` | **SURVIVED** | C3 |
| m19 | `m19-rc0-on-fail` | `return 0 if allok else 1` → `return 0` | donothing, pad-resolving-cites, delete-gone-cites, wrong-target, partial-9-of-18 | any reject (C1–C7) |
| m20 | `m20-m3-zip-swapped` | M3 walks `zip(after_lines, base_lines)` | positive | — |

† limb-level control (asserts a named `LIMB` line, not the exit code).

## What the frozen controls do and do not pin

* **Killed (4/20).** `m09`/`m10`/`m20` are killed by the positive control
  because they corrupt the *accepted* after. `m19` (blanket `rc=0`) is killed by
  all five reject controls. Within this 20-mutant set the five reject controls
  kill nothing else: none of them isolates a limb the positive control does not
  already guard.
* **M1 is unpinned (m01–m03).** No frozen control ever presents an after whose
  numerator matches the oracle while the denominator does not, and none presents
  a rate above the target. `positive` (167/732) and every reject case pass under
  `an==tn`, `an>=tn`, and no-M1-at-all. C1 fixes this.
* **M2 is unpinned (m04–m06) — and structurally unreachable by rc.** See
  §Equivalence. C8/C9 assert the M2 limb directly; no exit-code control can.
* **M3 line-count is unpinned (m07).** `pad` changes line count but also the
  meter and token set, so other limbs mask it; `delete-gone` has equal line
  counts. No frozen input is meter-identical with unequal line counts. C2 is.
* **M3 hit rule is unreachable by rc (m08).** See §Equivalence. C10 asserts the
  M3 limb.
* **M4 sub-rules are unpinned (m11–m14).** Every frozen control hands the counter
  the *well-formed* frozen map and varies the after instead; all four M4
  conditions pass in all six runs (`LIMB M4 pass bad=none`), so all four
  single-point weakenings survive. C4–C7 supply one malformed map each.
* **M5 is unpinned (m15, m16) and the verdict blind spot is unpinned (m18).**
  No frozen control passes a `--map-sha256` that differs from the map bytes.
  C3 corrupts the last nibble of the otherwise-correct sha.
* **Verdict blind spot (m17).** No frozen control ever fails M4, so a verdict
  that ignores M4 is invisible; C4–C7 (which fail only M4) kill it.

## Proposed round-86 controls (all re-runnable, all tested here)

Common prefix (lane root, scratch `$S`): inputs rebuilt as in the frozen script;
runner is `python3 -B $W/c1/skill-meter.py --lane $L --work $S/w` plus
`--base $S/base.md --after <AFTER> --map <MAP> --target <T> --map-sha256 <SHA>`.
For C4/C5/C10 the target is measured from the *intended* after with the pristine
counter (as the frozen positive control derives its target); for C1 it is the
deliberately wrong denominator. All controls expect `rc=1` (`fail`) and were
confirmed to fail for the intended limb and to be green (`rc=0`) only under the
targeted mutant.

| control | input | map | target | map sha | pristine failing limb | kills |
|---|---|---|---|---|---|---|
| C1 wrong-denominator-target | `positive.md` | frozen | **167/741** | `b575f147…` | `M1 FAIL after=167/732` | m01, m02, m03 |
| C2 blank-line-appended | `positive.md` + one `\n` | frozen | 167/732 | `b575f147…` | `M3 FAIL linecount_equal=False` | m07 |
| C3 mapsha-tail-corrupt | `positive.md` | frozen | 167/732 | `b575f147…ab1945` (last nibble 4→5) | `M5 FAIL` | m15, m16, m18 |
| C4 map-value-under-ufo | forged map → `c4-ufo-value.md` | `resolve.py` → `.ufo/waves/round-25/c1-after-35/corpus/instruments/resolve.py` | 168/733 | `91bb1f18…` | `M4 FAIL bad=resolve.py` (only `.ufo/` fails) | m11, m17 |
| C5 map-value-wrong-basename | forged map → `c5-wrong-basename.md` | `resolve.py` → `corpus/instruments/test_resolve.py` | 168/733 | `6b977c87…` | `M4 FAIL bad=resolve.py` (only `endswith` fails) | m12, m17 |
| C6 map-value-missing-worktree | fixture clone lane, `positive.md` | frozen | 166/732 | `b575f147…` | `M4 FAIL bad=S073.txt` (only `INTERNAL` fails) | m13, m17 |
| C7 base-key-resolving | fixture clone lane + `$CL/resolve.py`, `positive.md` | frozen | 167/732 | `b575f147…` | `M4 FAIL bad=resolve.py` (only base-GONE fails) | m14, m17 |
| C8 wrong-target-M2 † | `wrong.md` (the frozen reject input) | frozen | 167/732 | `b575f147…` | assert `LIMB M2 FAIL` (`stray_added=1`) | m04 |
| C9 extra-decite-M2 † | `positive.md` with `` `corpus/knowledge/claim-gates.md` `` de-cited | frozen | 167/732 | `b575f147…` | assert `LIMB M2 FAIL` (`removed=19 keys=18`) | m05, m06 |
| C10 ghost-key-M3hit † | `positive.md` | frozen + `ghost-key-r85.md` → `corpus/knowledge/ghost-key-r85.md` | 167/732 | `4e87a9c6…` | assert `LIMB M3 FAIL` (`bad_lines=0 keys_hit=18/19`) | m08 |

Notes for the integrator:

* **C4/C5 targets are 168/733, not 167/732.** The base already cites
  `corpus/instruments/resolve.py` on another line, so the forged value adds one
  more resolving token to the intended after (measured, not guessed). M1 stays
  green so the only failing limb is M4.
* **C6/C7 need a fixture lane.** `git clone --shared --quiet $L $CL`, assert
  `git -C $CL rev-parse --show-toplevel` equals `$CL` and `.git` exists; then a
  **worktree-only** perturbation (no git writes): C6 removes
  `$CL/corpus/source-snapshots/round-46/S073.txt` (tracked, so still in
  `ls-files`, but now classifies GONE) and restores it byte-identically
  (`66c96a61…`, verified); C7 creates an empty `$CL/resolve.py` (a bare base key
  now classifies INTERNAL) and removes it after. `--lane $CL` is passed to the
  counter; `resolve.py` import and `ls-files` both come from the clone.
* **C8/C9/C10 are limb-level.** They parse the `LIMB M2` / `LIMB M3` line that
  the counter already prints; no counter change is needed. They are the only
  control class that can reach M2 and the M3 hit rule (§Equivalence).

Exact construction of the forged inputs is in
`MutC1Counter-receipts/harness/driver.py` (`forge`, `proposed`),
`clone_controls.py` and `limb_controls.py`; the built inputs are in
`MutC1Counter-receipts/inputs/` (the base, positive, pad, delgone, wrong,
partial, extradecite and positive-blankline afters, the frozen map and the three
forged maps; the C4/C5 afters are rebuilt with
`apply-map.py <forged-map> base <after>`).

## Equivalence findings (why rc-only detection cannot cover M2 / M3-hit)

Two implications of the frozen code (no mutant involved):

1. **M3 passing implies M2 passing.** M3 requires equal line counts, `bad==0`
   (every after line equals its base line with each backticked map key replaced
   by its value) and `hit==keys` (every key occurs backticked in base). Then the
   collected token set of after is exactly the base token set with the key
   tokens removed and only map values inserted, i.e. `removed == keys` and
   `added ⊆ values`. Caveat: values must collect verbatim — true for all 18
   frozen values and every value these controls use (they are clean tracked
   paths; a value ending in `.,;:` would be the only way to break it, and M4's
   tracked-file binding excludes that in practice).
2. **M2 passing plus `bad==0` implies `hit==keys`.** `removed==keys` makes every
   key a *collected* base token; tokens are only collected from backticked
   spans, so every key occurs as `` `key` `` on some base line and the M3 loop
   adds it to `hit`.

Consequences, confirmed empirically (C8/C9/C10 kill exactly these four):

* `m04`–`m06` (weakened M2) never change the verdict: when pristine M2 passes the
  mutants pass, and when pristine M2 fails the pristine verdict already fails
  through M3 (implication 1's contrapositive). So they are verdict-equivalent;
  C1–C7 cannot kill them by exit code. C8 (`wrong-target`, original M2 fails via
  `stray_added=1`, m04's M2 passes) and C9 (`extra-decite`, original fails via
  `removed=19`, m05/m06 pass) kill them at limb level.
* `m08` (M3 without `hit==keys`) can only differ when `bad==0` and a key is not
  hit; by implication 2 that input already fails M2 in both counters, so the
  verdict is identical. C10 (map key that occurs on no base line: `bad_lines=0`,
  `keys_hit=18/19`) makes the pristine M3 fail while m08's M3 passes — a limb
  kill.

If round 86 wants exit-code controls for these rules, the counter needs a
limb-isolation mode (run one named limb on a hand-built input). Otherwise the
honest position is: M2 and M3's hit rule are diagnostic/redundant given M3/M2,
and the controls must assert the `LIMB` lines (C8–C10) if those rules are to be
load-bearing. Deleting them would be a contract change, not a test fix.

## Evidence and restoration

* **Frozen bytes never written.** The counter and map were only read
  (`cp`/`git show` into scratch). Hashes at start and after the whole campaign:
  counter `89c5d47b…` (identical), map `b575f147…` (identical); base and positive
  as tabulated above. No `__pycache__` writes: `python3 -B` on every counter /
  apply-map call, and `find corpus -name '*.pyc' -newermt 2026-11-06` returns 0
  (the one delete-gone helper run without `-B` in the frozen style reused the
  pre-existing 2026-11-04 `resolve.cpython-314.pyc`, whose source predates it). No git/jj
  writes anywhere; the only repository created was `git clone --shared` inside
  scratch, toplevel asserted; its perturbations were worktree-only and restored
  (S073.txt sha before == after == `66c96a61…`, `resolve.py` removed).
* **Baseline conformance.** All six frozen control outputs match the frozen
  receipt line for line; pristine rc 1/1/1/1/1/0 as recorded.
* **No crashes / no inconclusive rows.** All 20 mutants ran clean
  (`rc ∈ {0,1}`, empty stderr) on all six frozen controls and all ten new
  controls.
* **Tooling:** nothing installed (no pacman — host-paused —, no uv/npx/official
  binary); no host or lane mutation beyond the report/receipts named here.
* **Scratch deleted** at exit (`trap 'rm -rf -- "$S"' EXIT`) after receipts were
  copied; `MutC1Counter-receipts/` holds 65 files with `SHA256SUMS`
  (`frozen_matrix.json`, `proposed_matrix.json`, `clone_matrix.json`,
  `limb_matrix.json`, four run logs, 20 mutants + 20 diffs, 12 inputs, 4 harness
  scripts).

## Files written

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter.md`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/SHA256SUMS`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/{frozen_matrix.json,proposed_matrix.json,clone_matrix.json,limb_matrix.json}`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/logs/{frozen.log,proposed.log,clone.log,limb.log}`
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/mutants/*.py` and `*.diff` (20 + 20)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/inputs/*` (base, positive, pad, delgone, wrong, partial, extradecite, positive-blankline, frozen map, three forged maps)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/MutC1Counter-receipts/harness/{driver.py,clone_controls.py,limb_controls.py,summarize.py}`
