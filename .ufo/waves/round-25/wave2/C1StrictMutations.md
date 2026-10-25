# C1StrictMutations — limb-by-limb strict mutation test of the C1 counter (round 25, wave 2)

Seat: `L1Kasegi25.C1StrictMutations` (mutation tester, read-only on production; writes confined to
`.ufo/waves/round-25/wave2/`). Wave 2 — falsify wave-1 outputs.

Instrument under test: `corpus/instruments/recheck-audit.py`, sha256 `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f` (equals the pin in `.ufo/waves/round-25/c1-instrument-digest.txt`).

Strict limb set at this digest: `parse, cwd, paths, cdroot, instrument, own` (6 limbs; `STRICT_LIMBS` at `recheck-audit.py:73`). The wave-1 intermediate `artifact` limb is gone at the final digest.

## 0. Summary verdict

**The wave-1 C1 strict result `strict pass=35/35 exit=0` on the frozen 35-file surface STANDS.** No claim is falsified. Each of the six strict limbs is individually load-bearing on the frozen surface: a single-limb corpus mutation changes the control result in every case, and a corresponding instrument mutation (limb forced `True`) flips exactly its own mutation back. One provenance wrinkle is reported (§5): the committed receipt copy contains a *stale* interior instrument byte.

## 1. Base

Copy of the committed 35-file frozen surface: `.ufo/waves/round-25/c1-after-35/` (35 `corpus/knowledge/*.md`, byte-identical to the live tree minus C2's two additions; `cmp` verified 35/35, 0 differ). The instrument inside that copy is stale (`1ccee066…`, see §5); all runs below use the live pinned script `audit-pristine.py` (`c3c19adc…`) against `--root <copy> --cdroot <live lane>`, exactly the receipt's semantics.

Pristine control (`W/audit-pristine.py --root W/base --cdroot <lane> --json W/base.json`):

```
strict pass=35/35 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=35 total=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
EXIT=0
```

Field-for-field identical to the committed `c1-after-35.txt`. Baseline is live; a baseline failure would have made every verdict inconclusive.

## 2. Corpus-side single-limb mutations (each changes the control result)

All six mutate the same entry, `corpus/knowledge/authorised-testing-rules-of-engagement.md`, one `recheck:` line each (same file wave-1 M1–M4 used). Each is a one-line replacement; `diff -u` shows exactly one changed line per tree. Run with the pristine instrument, `--cdroot <lane>`:

| # | Mutant (one line, `recheck:` body) | Target limb | Entry strict vector | strict pass | exit | Changes control? |
|---|---|---|---|---|---|---|---|
| M1 | `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest <r24 manifest> --source S032 (` | parse | `frozen=011 strict=011111` | 34/35 | 1 | yes: 35→34, exit 0→1, `parse_fail 0→1` |
| M2 | `python3 corpus/instruments/source-recheck.py --manifest <r24 manifest> --source S032` (cd dropped) | cwd | `frozen=101 strict=101111` | 34/35 | 1 | yes: 35→34, exit 0→1, `cwd_fail 0→1` |
| M3 | `cd <lane> && … --manifest corpus/source-snapshots/round-99/manifest.json --source S032` | paths | `frozen=110 strict=110111` | 34/35 | 1 | yes: 35→34, exit 0→1, `paths_fail 0→1` |
| M4 | `cd /tmp && python3 corpus/instruments/source-recheck.py --manifest <r24 manifest> --source S032` | cdroot | `frozen=111 strict=111011` FROZEN-ONLY | 34/35 | 1 | yes: strict 35→34, exit 0→1, `cdroot_fail 0→1` (frozen pass stays 35) |
| M5 | `cd <lane> && test -e corpus/knowledge/authorised-testing-rules-of-engagement.md` | instrument | `frozen=111 strict=111101` FROZEN-ONLY | 34/35 | 1 | yes: strict 35→34, exit 0→1, `instrument_fail 0→1` |
| M6 | `cd <lane> && python3 corpus/instruments/anchorcheck.py corpus/knowledge/citation-bases.md` | own | `frozen=111 strict=111110` FROZEN-ONLY | 34/35 | 1 | yes: strict 35→34, exit 0→1, `own_fail 0→1` |

Every strict vector fails **exactly one** limb — the isolation is exact. M4–M6 are invisible to the frozen counter (`pass=35`) and are caught only by the strict counter and the exit rule.

Per-tree entry sha256:

| tree | `authorised-testing-rules-of-engagement.md` sha256 |
|---|---|
| base = do-nothing | `5533fc87…7e10e0` (== live lane file) |
| M1-parse | `c6d7511a…f0faa083` |
| M2-cwd | `fb0b4b09…ae4c2349e` |
| M3-paths | `5a8f92fb…d5b1456a022b8` |
| M4-cdroot | `318bca77…cdec125caad75` |
| M5-instrument | `957a0254…8dd5cb96355f043` |
| M6-own | `b7a42cf9…9f1741a949167970f6fb3045` |

## 3. Instrument-side limb mutants (each changes a control result; perfect diagonal)

Six copies of the pristine instrument, each with one strict limb forced to `True` in `audit_entry` (`audit-force-<limb>.py`):

| file | sha256 | forced line (`recheck-audit.py` source) |
|---|---|---|
| `audit-pristine.py` | `c3c19adc…ba2f6d7f` | — (verbatim lane bytes) |
| `audit-force-parse.py` | `5a0c18ae…8ad2f23` | `limbs["parse"] = parse_ok(line)` → `True` |
| `audit-force-cwd.py` | `123ed078…a8d7c2ec` | `limbs["cwd"] = lane_rc == foreign_rc and …` → `True` |
| `audit-force-paths.py` | `907a4660…ded4160b3` | `limbs["paths"] = named and not missing` → `True` |
| `audit-force-cdroot.py` | `d953dbf5…6b6827b2b2` | `strict["cdroot"] = …` → `True` |
| `audit-force-instrument.py` | `fc1a52ea…4ad025ad4d` | `strict["instrument"] = bool(instruments) or base_test` → `True` |
| `audit-force-own.py` | `7ae1e450…290c569c` | `strict["own"] = own or sourced or base_state` → `True` |

Run against the base tree and all six corpus mutants (`--root W/<tree> --cdroot <lane>`, real process exit captured):

| instrument mutant | base | M1-parse | M2-cwd | M3-paths | M4-cdroot | M5-instrument | M6-own |
|---|---|---|---|---|---|---|---|
| pristine | 35/35 e0 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 |
| force-parse | 35/35 e0 | **35/35 e0** | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 |
| force-cwd | 35/35 e0 | 34/35 e1 | **35/35 e0** | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 |
| force-paths | 35/35 e0 | 34/35 e1 | 34/35 e1 | **35/35 e0** | 34/35 e1 | 34/35 e1 | 34/35 e1 |
| force-cdroot | 35/35 e0 | 34/35 e1 | 34/35 e1 | 34/35 e1 | **35/35 e0** | 34/35 e1 | 34/35 e1 |
| force-instrument | 35/35 e0 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | **35/35 e0** | 34/35 e1 |
| force-own | 35/35 e0 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | 34/35 e1 | **35/35 e0** |

Reading: each limb mutation changes the control result **only** on the corpus mutant that fails exactly that limb (34/35 exit 1 → 35/35 exit 0), and changes nothing elsewhere — including on the all-pass base, so no instrument mutation manufactures a false pass on the honest surface. The strict counter is fully discriminating: 6/6 limbs kill their own mutant.

## 4. Built-in selftest coverage of the strict limbs

`--selftest` on each instrument byte (pristine = 0 failures; every forced limb ≥ 1 failure):

| instrument | selftest | failing case(s) |
|---|---|---|
| pristine | `cases=14 failures=0 exit=0` | — |
| force-parse | `failures=1 exit=1` | `parseonly.md` |
| force-cwd | `failures=1 exit=1` | `cwd.md` |
| force-paths | `failures=1 exit=1` | `ghost.md` |
| force-cdroot | `failures=1 exit=1` | `elsewhere.md` |
| force-instrument | `failures=2 exit=1` | `ownonly.md`, `instonly.md` |
| force-own | `failures=2 exit=1` | `selftesty.md`, `basetest.md` |

This supersedes the wave-1 `MutAuditLimbs` §5 finding (on the old `d07af435` bytes, the parse mutant "sailed through" selftest): at the final `c3c19adc` digest every strict limb is isolated by the selftest fixtures. (Wave-1's findings applied to the instrument bytes they measured; the instrument changed six times during wave 1.)

## 5. Provenance defect in the committed receipt copy (small correction, no claim falsification)

The committed frozen-surface copy `.ufo/waves/round-25/c1-after-35/corpus/instruments/recheck-audit.py` is **stale**: sha256 `1ccee066a50be51cd528e31810a1fee1cab178fdb84ea38c47026973ce341c82`, not the pinned `c3c19adc…`. The receipt `c1-after-35.json` is internally consistent (`instrument_sha256: c3c19adc…` — it ran the live script from the lane against `--root <copy>`), so the *receipt* is accurate, but anyone re-running `python3 <copy>/corpus/instruments/recheck-audit.py` would measure a different instrument. Smallest correction: either pin the interior copy's instrument bytes to `c3c19adc` (the scratch copies here were so pinned before running) or do not ship instruments inside receipt copies.

## 6. Reproduction

```
W=.ufo/waves/round-25/wave2/c1-strict-mutations
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
# build
for d in base do-nothing M1-parse M2-cwd M3-paths M4-cdroot M5-instrument M6-own; do
  cp -a .ufo/waves/round-25/c1-after-35 $W/$d
  cp corpus/instruments/recheck-audit.py $W/$d/corpus/instruments/recheck-audit.py
done
cp corpus/instruments/recheck-audit.py $W/audit-pristine.py
# corpus mutants: one-line replacements of the recheck: line in
# $W/M{1..6}/corpus/knowledge/authorised-testing-rules-of-engagement.md (see §2)
# instrument mutants: force each strict limb True in audit_entry (see §3)
# runs
python3 $W/audit-pristine.py --root $W/base --cdroot $LANE --json $W/base.json
for m in M1-parse M2-cwd M3-paths M4-cdroot M5-instrument M6-own; do
  python3 $W/audit-pristine.py --root $W/$m --cdroot $LANE --json $W/$m.json
done
for inst in parse cwd paths cdroot instrument own; do
  for tree in base M1-parse M2-cwd M3-paths M4-cdroot M5-instrument M6-own; do
    python3 $W/audit-force-$inst.py --root $W/$tree --cdroot $LANE --quiet
  done
done
```

## 7. Restoration / non-mutation evidence

- Production untouched: no file under `corpus/` or the lane root was written by this seat; `git status --porcelain` unchanged (only the pre-existing round-25 working-tree modifications). No VCS write, no pacman, no installs/upgrades performed or needed.
- Scratch copies disposable per tasking, left in place at `$W/` (trees `base`, `do-nothing`, `M1-parse`…`M6-own`; `audit-pristine.py`, `audit-force-<limb>.py`; receipts `base.txt/json`, `M*.txt/json`, `instrument-mutant-matrix.txt`).
- Base-tree restoration verified: `diff -r --brief <c1-after-35>/corpus/knowledge $W/base/corpus/knowledge` → no output; `do-nothing` identical to `base` (same entry sha). Mutant trees differ from base in exactly one line of one file (shown in §2 table + `diff -u`).
