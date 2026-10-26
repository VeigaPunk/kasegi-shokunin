# MutCtrNonUniqueFind — wave 2 receipt (counter mutant: find-text-not-unique accepted)

Round 31 wave 2, seat `MutCtrNonUniqueFind`, dispatched by KasegiR31 (hyaku run 7).
Attack target: `corpus/instruments/limb-mutation-check.py` with the frozen
`mutants_of_the_counter` mutant `find-text-not-unique accepted`. All work in
mktemp scratch copies; the only lane write is this receipt. No tools installed
(operator 2026-10-19 channel unused). No pacman. No git/jj mutation (read-only
`rev-parse`, `status` only).

## Frozen kill rule (quote, <=25 words, exact location)

claims.json:27 `mutants_of_the_counter`: "Attack seats must show each of these
counter mutants fails the 3 controls or the LIMB-line clause" — and the same
value lists `find-text-not-unique accepted` as one of the four counter mutants.

## Environment, pristine hashes

- lane HEAD at attack time: `eecad59db166e0626ca2472e96ea48bc28a35153`
  (`git -C <lane> rev-parse HEAD`; wave 1 has landed, so HEAD is past base b374feb…)
- `sha256sum` (before):
  - `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  <lane>/corpus/instruments/limb-mutation-check.py`
  - `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  <lane>/corpus/instruments/limb-ledger.json`
  - identical hashes verified for both scratch copies (`cp -a <lane>/corpus`, 3.4M each)
- scratch lanes: `D1=/tmp/mutreal.dURgS6` (real counter), `D2=/tmp/mutmut.aRG2DA`
  (mutant counter), `D3=/tmp/mutprop.kleLgW` (proposal, real counter),
  `D4=/tmp/mutprop.UAMDOX` (proposal, mutant counter); each `mktemp -d` +
  `cp -a "$LANE/corpus" "$D/corpus"`.

## Ground fact: find occurrence counts (root cause of what follows)

Command (run from /tmp):

```
python3 - <<'EOF'
import json
lane='/home/vgpnk/Projects/shokunin/kasegi-shokunin'
led=json.load(open(lane+'/corpus/instruments/limb-ledger.json'))
for kind in ('limbs','controls'):
    for r in led[kind]:
        t=open(lane+'/'+r['instrument'],encoding='utf-8').read()
        print(kind, r['id'], r['instrument'].rsplit('/',1)[-1], 'find_count=%d' % t.count(r['find']))
EOF
```

Output (all 16 rows):

```
limbs RA-parse recheck-audit.py find_count=1
limbs RA-cwd recheck-audit.py find_count=1
limbs RA-paths recheck-audit.py find_count=1
limbs RA-cdroot recheck-audit.py find_count=1
limbs RA-instrument recheck-audit.py find_count=1
limbs RA-own recheck-audit.py find_count=1
limbs RA-completeness recheck-audit.py find_count=1
limbs RA-expect-missing recheck-audit.py find_count=1
limbs RA-expect-unexpected recheck-audit.py find_count=1
limbs SR-stem-mismatch source-recheck.py find_count=1
limbs SR-occurrence-not-unique source-recheck.py find_count=1
limbs FR-missing-entry frontier-recheck-count.py find_count=1
limbs FR-duplicate-entry frontier-recheck-count.py find_count=1
controls CTL-noop recheck-audit.py find_count=1
controls CTL-nocompile recheck-audit.py find_count=1
controls CTL-equivalent source-recheck.py find_count=1
```

No ledger row has a find text occurring more than once in its instrument.

## The mutant

One-point mutation at `evaluate_row`, counter line 428 (the `find`-count gate).
`text.replace(row["find"], row["replace"], 1)` on line 430 already applies to
the first occurrence, so relaxing the gate to "at least once" is exactly the
assigned mutation. `diff -u` (pristine D1 vs mutated D2):

```diff
--- /tmp/mutreal.dURgS6/corpus/instruments/limb-mutation-check.py	2026-10-25 21:00:20.176494491 -0300
+++ /tmp/mutmut.aRG2DA/corpus/instruments/limb-mutation-check.py	2026-10-25 21:26:33.651100160 -0300
@@ -425,7 +425,7 @@
         if live["exit"] != row["live_exit"] or not live["signal"]:
             return verdict_row(live_exit, yes_no(live["signal"]), "-", "-", "invalid:live-baseline")
         text = original.decode("utf-8")
-        if text.count(row["find"]) != 1:
+        if text.count(row["find"]) == 0:
             return verdict_row(live_exit, "y", "-", "-", "invalid:find-count")
         mutated = text.replace(row["find"], row["replace"], 1).encode("utf-8")
         if mutated == original:
```

## Real counter baseline — run twice (PRE-STATE n/a: wave 1 quiescent, both runs on these bytes)

Command (cwd = scratch lane root, run 1 then run 2):

```
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json --root /tmp/mutreal.dURgS6
```

Run 1: `EXIT=0`, `sha256(real1.out)=9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`
Run 2: `EXIT=0`, `sha256(real2.out)=9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`,
`cmp real1.out real2.out` → `CMP=identical`

Full output (run 1; run 2 byte-identical):

```
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
```

Baseline holds (exit 0, both frozen summary lines, 13 `LIMB …verdict=killed`
lines), so the mutant verdict below is conclusive — not a baseline failure.

## Mutant run

Command (cwd = D2): same as above with `--root /tmp/mutmut.aRG2DA`.

`EXIT=0`, `sha256(mut1.out)=9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`
— byte-identical to both real-counter runs. Full output: identical line-for-line
to the run-1 block above (same sha256; 13 LIMB killed lines, 3 CONTROL ok=y
lines, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`).

## Verdict: SURVIVOR — coverage hole in the frozen counter design

The mutant prints both `limbs=13 killed=13 survivors=0` and
`controls=3 rejected=3` with exit 0 and is byte-identical to the real counter,
so it fails NEITHER the LIMB-line clause NOR any of the 3 controls
(CTL-noop → `invalid:noop` ok=y, CTL-nocompile → `invalid:nocompile` ok=y,
CTL-equivalent → `survivor` ok=y). Under the frozen rule this mutant is
**not killed**: a hole.

Why it survives: every find text occurs exactly once in its instrument (table
above), so `text.count(row["find"]) != 1` and `== 0` are extensionally the same
predicate on this ledger, and the replace was always first-occurrence. The
`invalid:find-count` gate is exercised by the counter's own `--selftest` but by
no frozen ledger row or control.

## Smallest closing proposal (verified in scratch; NOT landed)

ExecCounterFix owns both files. A ledger row alone does not work: `validate_row`
restricts control `expect` to `CONTROL_EXPECTS = ("invalid:noop",
"invalid:nocompile", "survivor")` (counter line 88), so a row with
`expect: "invalid:find-count"` makes the counter exit 2. Minimal two-part fix:

1. counter `limb-mutation-check.py`:
   - line 88: `CONTROL_EXPECTS = ("invalid:noop", "invalid:nocompile", "survivor", "invalid:find-count")`
   - `CONTROL_ID_EXPECTS`: add `"CTL-find-count": "invalid:find-count",`
2. ledger `limb-ledger.json`, append control (find occurs exactly twice in
   recheck-audit.py, replace is a comment-only compile-clean no-op):

```json
    {
      "id": "CTL-find-count",
      "instrument": "corpus/instruments/recheck-audit.py",
      "find": "    if expect_path is None:",
      "replace": "    if expect_path is None:  # non-unique find control: comment only, no behavior change",
      "kill": "python3 {inst} --selftest",
      "live_exit": 0,
      "signal": "(?m)^selftest parseonly\\.md .*\\bok$",
      "expect": "invalid:find-count",
      "note": "proposed control (MutCtrNonUniqueFind r31w2): find occurs exactly twice in recheck-audit.py, so the honest verdict is invalid:find-count; a counter that accepts a non-unique find (first-occurrence replace) proceeds to a comment-only survivor here and fails this control."
    }
```

Measured discrimination (D3 = real counter + fix, D4 = mutant counter + fix,
both in scratch):

D3 command: same counter command with `--root /tmp/mutprop.kleLgW` →
`EXIT=0`, `sha256(prop_real.out)=7d10baad8f5b7a9c20f372e935b135ea00fbd04e88f53fb3ac31ccdd1f4cfd45`:

```
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
CONTROL CTL-find-count verdict=invalid:find-count expected=invalid:find-count ok=y
limbs=13 killed=13 survivors=0
controls=4 rejected=4
```

(13 LIMB killed lines identical to baseline; proposal keeps the real counter green.)

D4 command: same with `--root /tmp/mutprop.UAMDOX` → `EXIT=1`,
`sha256(prop_mut.out)=a225ab12da171d8956c0c767dca110013f45cd2a9d11d95c94f5d0a5e1c4ec27`:

```
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
CONTROL CTL-find-count verdict=survivor expected=invalid:find-count ok=n
limbs=13 killed=13 survivors=0
controls=4 rejected=3
```

The mutant is then **killed by the controls clause** (`rejected != controls`,
exit 1) — note it still prints `limbs=13 killed=13 survivors=0`, so the
LIMB-line clause alone never catches it; the fourth control is required.

Claim coupling: with the fourth control the summary line becomes
`controls=4 rejected=4`, while frozen C1 says `controls=3 rejected=3`. Claims
are frozen, so landing this proposal needs an L1 claims amendment (appended
erratum file), not a silent ledger bump. Message sent to ExecCounterFix with
the mutant diff; decision and landing are theirs/L1's.

## Restoration evidence

- D2 counter restored from pristine D1 bytes before deletion:
  `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  /tmp/mutmut.aRG2DA/corpus/instruments/limb-mutation-check.py`
- scratch removed: `removed /tmp/mutreal.dURgS6`, `removed /tmp/mutmut.aRG2DA`,
  `removed /tmp/mutprop.kleLgW`, `removed /tmp/mutprop.UAMDOX` (each verified
  absent with `[ ! -e ]`)
- lane bytes after (unchanged):
  - `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py`
  - `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json`
- lane HEAD after: `eecad59db166e0626ca2472e96ea48bc28a35153` (unchanged)
- `git -C <lane> status --porcelain -- corpus/instruments` → empty (clean)

## Bounds kept

Writes: this receipt only (plus mktemp scratch under /tmp, all removed). No
lane instruments/entries/registry/README/SKILL.md/PROVINCE.md touched, no git/jj
mutations, no fleet-root or shokuknow writes, no live bounty contact, no tool
installs. Peer traffic: one coordination message to ExecCounterFix (survivor
finding + mutant diff), as tasked; their reply and this seat's afterword follow
below.

## Afterword — post-probe fix report (per ExecCounterFix message; not re-verified by this seat)

After this receipt was filed, ExecCounterFix reported closing the hole WITHOUT a
fourth control, so the frozen C1 summary stays `controls=3 rejected=3` and no
claims amendment is needed: the counter now runs three implicit guard fixtures
on every ledger run (throwaway probe lane, 1 s cap) — baseline losing its
signal must be `invalid:live-baseline`, find occurring twice must be
`invalid:find-count`, a never-returning kill must be `invalid:timeout` — and
folds their result into the exit status. Guard lines are `guard <name> …` plus
`guard cases=3 failures=0`; they are not limbs/controls and never enter the two
counts. Per their replay of this seat's exact one-line mutant against the
patched counter: `guard invalid-find-count verdict=killed want=invalid:find-count FAIL`,
`guard cases=3 failures=1`, exit 1, with LIMB lines and both summaries
unchanged (`limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`); pristine
patched counter: `guard failures=0`, same two summary lines, exit 0,
`--selftest cases=20 failures=0`.

This seat made no further probe (assigned mutation probe was closed before the
fix landed; ExecCounterFix marked no action needed). All hashes and outputs
above were captured on the PRE-FIX counter bytes
(`c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f`), which
stand as the red-before evidence for their fix. My earlier "claim coupling"
paragraph described only my 4th-control proposal, which was not the landed
design; its caveat is therefore moot.
