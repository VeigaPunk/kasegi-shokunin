# ExecLimbRAown — falsification of ledger limb `RA-own` (C1, strict limb (f) own)

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (leaf seat; only this receipt written in the lane).
Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a77999a00efbca129cfccb28a481037f6241f`;
observed integration HEAD `eecad59db166e0626ca2472e96ea48bc28a35153` (`git log --oneline -1`), tracked tree clean
(`git status --porcelain | grep -v '^??'` printed nothing). All attack work ran in `mktemp -d` scratch copies; the
lane instruments were never edited.

## 0. Bytes actually tested (sha256)

```
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
```

`cmp -s corpus/instruments/recheck-audit.py <scratch>/raown.pristine.py` → `identical` (the hand baseline is the landed
instrument byte-for-byte).

## 1. The row under test (verbatim, ledger lines 54-64)

```json
{
  "id": "RA-own",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "strict[\"own\"] = own or sourced or base_state",
  "replace": "strict[\"own\"] = True",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest selftesty\\.md .*\\bok$",
  "note": "strict limb (f) own: the own/sourced/base-state disjunction collapsed to True; isolated by selftesty.md (instrument ok, the entry's own file not named)"
}
```

Instrument site (landed bytes, line 147): `strict["own"] = own or sourced or base_state`, fed by line 141
`own = "corpus/knowledge/" + entry in tokens`, line 142 `sourced = "--source" in line and "corpus/source-snapshots/" in line`,
line 146 `base_state = base_test and not tokens`.

## 2. Hand re-derivation on the landed bytes

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
S=$(mktemp -d /tmp/raown.XXXXXX); cp -a "$LANE/corpus" "$S/corpus"
cd "$S"; PYTHONDONTWRITEBYTECODE=1 python3 "$S/corpus/instruments/recheck-audit.py" --selftest > live.out 2>&1
```

```
live_exit=0
selftest_lines=18
8:selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
signal_match=True        # re.search(r'(?m)^selftest selftesty\.md .*\bok$', live.out)
```

Mutation applied by hand (not by the counter), then compiled:

```
find_count=1
bytes_written=22856 changed=True
py_compile_exit=0
mutant_exit=1
8:selftest selftesty.md  pass want=True  got=True  | strict want=False got=True  FAIL
signal_match=False
```

Hand result: `live=0/y`, `mutant=1/n` → the limb is killed by the row as written.

## 3. The counter's line for the same row (run in the lane, scratch-only)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
timeout 900 python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
counter_exit=0
```

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

(wall 14.32 s)

Hand vs counter for `RA-own`:

| side | hand | counter | agree |
|---|---|---|---|
| live exit/signal | 0 / y | 0 / y | yes |
| mutant exit/signal | 1 / n | 1 / n | yes |
| verdict | killed | killed | yes |

No difference → no defect in the row, the mutation text, or the counter's report for this limb. The counter's run was
on the same quiescent bytes (HEAD `eecad59`, tree clean), so it is comparative, not PRE-STATE.

## 4. Isolation: which lines change, and is the kill limb-specific?

`diff -u live.out mutant.out` (whole run) changed exactly four lines (two removals, two additions):

```diff
 selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
-selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
+selftest selftesty.md  pass want=True  got=True  | strict want=False got=True  FAIL
 selftest sourced.md    pass want=True  got=True  | strict want=True  got=True  ok
-selftest basetest.md   pass want=True  got=True  | strict want=False got=False ok
+selftest basetest.md   pass want=True  got=True  | strict want=False got=True  FAIL
 selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
```

- Both flipped lines are limb-(f) decisions and nothing else: `selftesty.md` (`cd <tmp> && python3 … --selftest`) and
  `basetest.md` (`… && test -d ~/Projects/bounties && python3 … corpus/knowledge/target.md`) are the two fixtures whose
  `strict.own` is False *only* because of this disjunction. The ledger signal is keyed on `selftesty.md`, the fixture whose
  own=False does not ride on the base_test conjunction.
- The mutant does **not** crash and the run is otherwise intact: `mutant_selftest_lines=18`, `mutant_ok_lines=16`,
  `mutant_fail_lines=2`, `grep -c Traceback mutant.out` → `0`, no `SyntaxError|NameError|TypeError`, and the whole tail
  (completeness sanity, `complete-empty`, `complete-missing-line`, `strict pass=1/2 …`, `executes=1 gated=0 broken=0`,
  `lines=1 total=2 …`, `expect=absent …`) is byte-identical to the live run. The exit 1 is the selftest's own
  `return 1 if failures else 0` with `failures == 2`, not an unrelated failure mode.

## 5. Discrimination: second, different one-limb mutants of limb (f)

Each applied to its own fresh `cp -a corpus` scratch; `find` asserted to occur exactly once; `py_compile` run before
`--selftest`; signal = the ledger regex.

| mutant | code site | find → replace | compile | exit | signal | killed? |
|---|---|---|---|---|---|---|
| M1 (ledgered) | line 147 | `strict["own"] = own or sourced or base_state` → `strict["own"] = True` | ok | 1 | n | **killed** |
| M2a | line 141 | `own = "corpus/knowledge/" + entry in tokens` → `own = True` | ok | 1 | n | **killed** |
| M2b | line 142 | `sourced = "--source" in line and "corpus/source-snapshots/" in line` → `sourced = "--source" in line` | ok | 0 | y | **SURVIVOR** |
| M2c | line 147 (inversion) | `strict["own"] = own or sourced or base_state` → `strict["own"] = not (own or sourced or base_state)` | ok | 1 | n | **killed** |
| M2d | line 146 | `base_state = base_test and not tokens` → `base_state = base_test` | ok | 1 | y | killed (by exit only) |

FAIL lines per mutant (verbatim):

```
M2a: selftest selftesty.md … strict want=False got=True  FAIL
     selftest basetest.md  … strict want=False got=True  FAIL
M2b: (none — all 18 selftest lines end " ok")
M2c: good.md, selftesty.md, sourced.md, basetest.md, basestate.md  (5 FAIL: the disjunction inverted)
M2d: basetest.md only  (selftesty.md still " ok", so only the exit 0→1 carries this kill; the signal stays y)
```

M2b is **not** an equivalent mutant — proof, pristine vs M2b instrument on a synthetic one-entry tree
(`$T/corpus/knowledge/probe.md` = `recheck: cd $T && python3 corpus/instruments/tool.py --source S999`, i.e. `--source`
with no `corpus/source-snapshots/` path):

```
pristine exit=1  probe.md strict_own=False  strict={'parse': True, 'cwd': True, 'paths': True, 'cdroot': True, 'instrument': True, 'own': False}  pass_strict=False
M2b      exit=0  probe.md strict_own=True   strict={'parse': True, 'cwd': True, 'paths': True, 'cdroot': True, 'instrument': True, 'own': True}   pass_strict=True
--- diff (pristine vs M2b) ---
-probe.md  frozen=111 strict=111110 lane=0 foreign=0 executes FROZEN-ONLY
-strict pass=0/1 cdroot_fail=0 instrument_fail=0 own_fail=1
+probe.md  frozen=111 strict=111111 lane=0 foreign=0 executes PASS
+strict pass=1/1 cdroot_fail=0 instrument_fail=0 own_fail=0
-lines=1 total=1 pass=1 fail-closed=0 … exit=1
+lines=1 total=1 pass=1 fail-closed=0 … exit=0
```

So M2b drops a real gate (the `sourced` disjunct accepts `--source` with no manifest) and the instrument's own cases do
not see it. It is invisible on the current corpus too: all 18 entries whose first `recheck:` line uses `--source` also name
`corpus/source-snapshots/` (loop over `grep -l '^recheck:.*--source' corpus/knowledge/*.md` printed no offender), and
pristine vs M2b `--quiet --json` receipts on the landed corpus are identical apart from `instrument_sha256`
(`receipts_identical=True`, `strict_failing_own=0/0`, both `audit_exit=1`).

Conclusion on discrimination: the selftest kills the *specific mutant shape* the ledger names — collapse of the
own/sourced/base-state disjunction to a constant, whether `True` (M1) or its inversion (M2c) — and also the `own`
sub-term (M2a) and the `base_state` conjunction (M2d). It does **not** discriminate the `sourced` sub-term's manifest
requirement (M2b survives), and M2d is killed by the exit code while the `selftesty.md`-keyed signal still matches.

## 6. Verdict: `holds`

- Hand re-derivation on the landed bytes reproduces the counter's `LIMB RA-own live=0/y mutant=1/n verdict=killed`
  exactly (find count 1, compiles, live exit 0 with signal y, mutant exit 1 with signal n).
- The kill is isolated and limb-specific: exactly the two limb-(f) fixture lines flip, the remaining 16 selftest lines
  and every downstream summary line are byte-identical, and there is no traceback or unrelated crash.
- Recorded weakness (coverage, not a C1 violation): discrimination is narrow. `sourced = "--source" in line and
  "corpus/source-snapshots/" in line` → `sourced = "--source" in line` is a non-equivalent one-limb mutant (proved above)
  that the instrument's cases leave alive. Suggested fixture for the owning executor (I am read-only on instruments and
  did not apply it): add case `sourced-nomanifest.md` with line
  `recheck: cd %s && python3 corpus/instruments/tool.py --source S999` and want `(True, False)`, which reds M2b only
  (`strict.own` False→True) and leaves M1/M2a/M2c/M2d verdicts unchanged. A second narrowness note: for a `base_state`
  mutant the row would be killed on exit alone, since the `selftesty.md` signal is blind to that sub-term.

## 7. Bounds / hygiene

- Writes: this receipt only, under the lane. No edits to instruments, entries, registry, README, SKILL.md, PROVINCE.md,
  `.ufo/state/`, `MANIFEST.json`; no writes to the fleet root, siblings or `shokuknow`. All mutant copies live under
  `/tmp/raown*` and were deleted after the runs (`rm -rf /tmp/raown.* /tmp/raown-* /tmp/raown-synth.* /tmp/raown-real.*`;
  the counter's own scratch lives in its internal `mkdtemp` and is removed by the counter).
- Git/jj: read-only only (`git status`, `git log`, `git rev-parse`). No add/commit/checkout/reset/stash, no jj verb.
- No tool installs (nothing needed); no pacman. No background jobs, no delegation.
- No live bounty target contacted; no credential or session material read or written.
- Answering model: `opencode-go/deepseek-v4.1-flash` (runtime route; this item's evidence does not depend on model choice).
