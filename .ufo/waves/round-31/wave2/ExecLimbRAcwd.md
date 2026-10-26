# ExecLimbRAcwd — falsify C1 ledger limb `RA-cwd` (frozen limb (b), cwd)

Seat: ExecLimbRAcwd. Round 31, wave 2. Lane base b374febbb; wave-1 integration eecad59.
Answering model: `opencode-go/deepseek-v4.1-flash` (route-table default; no model passed).
Tool installs/upgrades: none (no pacman; no network fetch; no uv/npx needed).
Writes: this receipt only. Lane instruments read-only; all attack work in `mktemp -d` scratch copies.
No git/jj mutation was run (read-only `git status`/`git log` only).

## 0. Bytes under test

```
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```

Ledger row (read from the landed JSON, not retyped):

```json
{
  "id": "RA-cwd",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "lane_rc == foreign_rc and lane_digest == foreign_digest",
  "replace": "True",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest cwd\\.md .*\\bok$",
  "note": "frozen limb (b) cwd: lane-root vs foreign-cwd exit+digest equality collapsed to True; isolated by cwd.md (a relative corpus/instruments path runs from the lane root and fails from /)"
}
```

Code site in the instrument (`audit_entry`, lines 115-123):

```python
    try:
        lane_rc, lane_digest = run(line, root)
        foreign_rc, foreign_digest = run(line, foreign)
        limbs["cwd"] = lane_rc == foreign_rc and lane_digest == foreign_digest
```

Fixture that is supposed to isolate it (selftest `cases`, line ~215):

```python
"cwd.md": ("recheck: python3 corpus/instruments/tool.py corpus/knowledge/cwd.md", False, False),
```

## 1. Counter line on the landed bytes (lane, quiescent; counter is scratch-only)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
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
counter_exit=0
```

Counter's `RA-cwd` line under test: `LIMB RA-cwd live=0/y mutant=1/n verdict=killed` (wall 16.94 s).
Cross-check that the row's `find` is a one-limb patch site (no shared site with the other recheck-audit rows):

```
$ python3 - <<'EOF'   # prints every recheck-audit row's find from the landed ledger
RA-parse | 'capture_output=True).returncode == 0'
RA-cwd | 'lane_rc == foreign_rc and lane_digest == foreign_digest'
RA-paths | 'limbs["paths"] = named and not missing'
RA-cdroot | 'os.path.abspath(cd_target) == (cdroot or root)'
RA-instrument | 'strict["instrument"] = bool(instruments) or base_test'
RA-own | 'strict["own"] = own or sourced or base_state'
RA-completeness | '    complete = len(entries) == total and total > 0\n    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)'
RA-expect-missing | 'sorted(wanted - actual)'
RA-expect-unexpected | 'sorted(actual - wanted)'
```

## 2. Hand re-derivation of `RA-cwd` (independent of the counter)

(`<lane>` below = `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; `$LANE` in the script is the same path.)

```
$ S=$(mktemp -d /tmp/execlimbracwd.XXXXXX); cp -a <lane>/corpus "$S/corpus"
$ INST="$S/corpus/instruments/recheck-audit.py"
$ python3 - "$LANE/corpus/instruments/recheck-audit.py"   # byte-count of find on landed bytes
find_count= 1
orig_sha256= 5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
$ ( cd "$S" && python3 "$INST" --selftest > live.out 2>&1; echo "live_exit=$?" )
live_exit=0
signal `(?m)^selftest cwd\.md .*\bok$` -> signal_match= True
LINE: selftest cwd.md        pass want=False got=False | strict want=False got=False ok
$ python3 - "$INST"   # assert find==1, replace once, py_compile
mutant_sha256= 697ccd755fd4101918a18482cc0c18feeb838d378a38e9bc0a3d0ccf2c021f4e
py_compile=ok
$ ( cd "$S" && python3 "$INST" --selftest > mutant.out 2>&1; echo "mutant_exit=$?" )
mutant_exit=1
signal_match= False
LINE: selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL
```

Mutant determinism (mutant side re-run twice on my own scratch, same bytes):

```
mutant_exit_1=1   mutant_exit_2=1   signal=False/False   lines=39/39
```

Comparison with the counter's line:

| side | hand | counter | agree |
|---|---|---|---|
| live exit / signal | 0 / y | 0 / y | yes |
| mutant exit / signal | 1 / n | 1 / n | yes |
| verdict | killed | killed | yes |
| find occurrence count | 1 | 1 (else `invalid:find-count`) | yes |
| mutant compiles | ok | ok (else `invalid:nocompile`) | yes |

**No difference between the hand result and the counter's `LIMB RA-cwd` line** — the kill-rule clause "closure re-derives any one ledger patch by hand … and the result differs from the counter's LIMB line" is **not** triggered.

## 3. Discrimination — a second, different one-limb mutant

Three probes, each its own fresh scratch copy of `<lane>/corpus`; `find_count=1` and `py_compile=ok` asserted for each.

### P1 — different code site: the foreign run is replaced by a lane-root run
`foreign_rc, foreign_digest = run(line, foreign)` → `foreign_rc, foreign_digest = run(line, root)`
(the cwd limb is tested only inside one cwd, so lane/foreign can never differ)

```
### foreign-site find_count=1
foreign-site live_exit=0
mutant_sha256= 738d41ade7445e5fefb41218f72342ac787ea243eb24237fab5d1fbde7f174a6
py_compile=ok
foreign-site mutant_exit=1
live_signal= True mutant_signal= False
live_banner_lines= 39 mutant_banner_lines= 39
MUT-ONLY: ['selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL']
LIVE-ONLY: ['selftest cwd.md        pass want=False got=False | strict want=False got=False ok']
```

Verdict: **killed**, and killed by the same single cwd.md line. So the instrument's cases are not tuned to one byte shape.

### P2 — inversion of the same expression
`lane_rc == foreign_rc and lane_digest == foreign_digest` → `lane_rc != foreign_rc and lane_digest != foreign_digest`

```
### invert find_count=1
invert live_exit=0
mutant_sha256= ec736fb5798dcdc2ccf8882f0966ccac2e02fc34d647ce87dc75716a7e607a17
py_compile=ok
invert mutant_exit=1
live_signal= True mutant_signal= False
live_lines 39 mut_lines 39 mut_only 19 live_only 19
selftest_lines 10
--- MUT-ONLY ---
selftest good.md       pass want=True  got=False | strict want=True  got=False FAIL
selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL
selftest degenerate.md pass want=True  got=False | strict want=False got=False FAIL
selftest elsewhere.md  pass want=True  got=False | strict want=False got=False FAIL
selftest ownonly.md    pass want=True  got=False | strict want=False got=False FAIL
selftest selftesty.md  pass want=True  got=False | strict want=False got=False FAIL
selftest sourced.md    pass want=True  got=False | strict want=True  got=False FAIL
selftest basetest.md   pass want=True  got=False | strict want=False got=False FAIL
selftest basestate.md  pass want=True  got=False | strict want=True  got=False FAIL
selftest instonly.md   pass want=True  got=False | strict want=False got=False FAIL
good.md                              frozen=101 strict=101111 lane=0   foreign=0   executes    FAIL
strict pass=0/1 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=1 total=1 pass=0 fail-closed=0 parse_fail=0 cwd_fail=1 paths_fail=0 exit=1
extra.md                             frozen=101 strict=101111 lane=0   foreign=0   executes    FAIL
good.md                              frozen=101 strict=101111 lane=0   foreign=0   executes    FAIL
strict pass=0/2 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=2 total=2 pass=0 fail-closed=0 parse_fail=0 cwd_fail=2 paths_fail=0 exit=1
strict pass=0/2 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=1 total=2 pass=0 fail-closed=0 parse_fail=0 cwd_fail=1 paths_fail=0 exit=1
--- LIVE-ONLY --- (the same 19 lines with `frozen=111`, `pass=1/…`, `cwd_fail=0`, `ok`/`PASS`)
```

19 lines differ (10 selftest case lines + 9 report lines: the `frozen=` bit string, the `pass=`/`cwd_fail=`
counts and the per-entry `ok`/`PASS` markers), i.e. the inversion is caught broadly, not by one case.

Verdict: **killed** (non-specifically — every cwd-independent fixture flips, as expected for an inversion).

### P3 — partial mutant: the digest half of the conjunction dropped
`lane_rc == foreign_rc and lane_digest == foreign_digest` → `lane_rc == foreign_rc`

```
### digestonly find_count=1
digestonly live_exit=0
mutant_sha256= 2da3cc22d10982352fe620571498318314c2dfb2ae7a4f919aab0a59ef5c656e
py_compile=ok
digestonly mutant_exit=0
live_signal= True mutant_signal= True
live_banner_lines= 39 mutant_banner_lines= 39
MUT-ONLY: []
LIVE-ONLY: []
```

Verdict: **SURVIVOR** — byte-identical output, identical exit. Recorded as a finding, not relabelled as killed.

**Finding F1 (report-only; instrument is out of my write scope).** The frozen limb (b) predicate is exit-equality **and** digest-equality (`recheck-audit.py` docstring, limb (b)). The instrument's fixtures kill the whole-expression mutants (P1, P2 and the ledger's collapse) but no fixture ever produces *equal exit status with different output bytes*, so the digest conjunct is not independently load-bearing in the selftest. The limb is therefore killed on exit-status discrimination only. The gap is closable with one fixture whose lane-root run and foreign run both exit 0 while printing different bytes — e.g. a relative-path line that fails from `/` but is not allowed to set the exit status, `recheck: python3 corpus/instruments/tool.py corpus/knowledge/digest.md; true` (foreign run prints the python error to stderr, exit 0 both sides, digests differ) — expected `(False, False)`; P3's mutant would then print `digest.md ... got=True FAIL`. No such fixture exists today (`cases` holds only `cwd.md`, whose foreign run exits 2). Same class of gap is visible in the strict `elsewhere.md` case, which is `cd`-pinned and therefore digest-blind.

Note on granularity: within the instrument's selftest, `cwd.md` is the only case whose verdict depends on the cwd limb at all; `parseonly.md` (parse), `ghost.md` (paths), `elsewhere.md` (cdroot), `instonly.md` (instrument), `ownonly.md`/`selftesty.md` (own) isolate their own limbs. So the cwd limb has exactly one decisive case — sufficient for this row (plus P1 as a second shape), but one case is the whole budget.

## 4. Isolation — the kill is case-specific, not an unrelated crash

```
$ diff -u live.out mutant.out
--- live.out
+++ mutant.out
@@ -1,6 +1,6 @@
 selftest good.md       pass want=True  got=True  | strict want=True  got=True  ok
 selftest prose.md      pass want=False got=False | strict want=False got=False ok
-selftest cwd.md        pass want=False got=False | strict want=False got=False ok
+selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL
 selftest ghost.md      pass want=False got=False | strict want=False got=False ok
 selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
 selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
```

Both runs print 39 lines (`live_banner_lines= 39 mutant_banner_lines= 39`); the banner and all other cases are byte-identical, including:

```
selftest completeness lines=13 total=15 complete=False ok
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok
selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
```

No traceback, no truncated run: the mutant executes every fixture and both `main()` blocks, then exits 1 through the instrument's own `return 1 if failures else 0`. The single differing line is the one whose `want` encodes the frozen cwd limb (`cwd.md → (False, False)`), so the kill is attributable to the limb itself, not to collateral damage.

## 5. Cleanliness / bounds

```
$ sha256sum <lane>/corpus/instruments/recheck-audit.py <lane>/corpus/instruments/limb-ledger.json   # after all runs
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-audit.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-ledger.json
$ git -C <lane> status --porcelain=v1 -- corpus/instruments      # (empty: instruments unchanged)
```

Counter scratch discipline observed: `/tmp/limb-mutation-*` dirs seen during the wave are in-flight copies from concurrently running seats, not leaks — every one created before a 20 s wait was gone afterwards (`after 20s: none`; `persisted across 20s` = empty). The counter's `evaluate_row`/`measure_side` each `shutil.rmtree` in a `finally`, and `build_scratch` copies only `corpus/` (plus `ledger.copy`, absent here) into `tempfile.mkdtemp`.

My own scratch (`/tmp/execlimbracwd.*`) is outside the lane and was removed after the receipt was written.

## 6. Verdict

**`holds`.** `RA-cwd` is a real, one-limb, exactly-once patch site; on the landed bytes its mutant exits 1 with the discriminating signal gone while the live baseline exits 0 with it present; the hand derivation reproduces the counter's line exactly (`live=0/y mutant=1/n verdict=killed`); the kill is isolated to the single `cwd.md` fixture line and a second, structurally different mutant (foreign run replaced by a lane run) is killed by the same case.

Recorded, non-blocking: **finding F1** — the digest conjunct of frozen limb (b) is not independently exercised by the instrument's fixtures (partial mutant P3 survives; suggested fixture above). This limits the limb's discrimination to exit-status equality but does not falsify the ledger row, whose declared patch is the whole-expression collapse and is killed.

Routed defects: none (nothing in the counter, the ledger or the isolation was found wrong). F1 is an instrument-fixture depth gap for the L1 to route (instrument edits were outside this seat's write scope).
