# ExecLimbRAexpectunexpected — falsify ledger limb `RA-expect-unexpected` (round 31, wave 2)

Seat: ExecLimbRAexpectunexpected (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`, wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`).

Files written: this receipt only. Every probe ran in `mktemp -d` scratch lanes under `/tmp`
(copied from the lane, deleted at the end). No git/jj mutation (read-only `git rev-parse`,
`git status`), no delegation, no background job, no network fetch, no credential material, no
tool install or upgrade (nothing needed; pacman not invoked). Answering model actually run on:
`opencode-go/deepseek-v4.1-flash` (harness route table; no model passed anywhere).

## 0. Bytes measured (identical at seat start and seat end)

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-ledger.json corpus/instruments/limb-mutation-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
$ git status --porcelain corpus/ | wc -l
0
```

No PRE-STATE label is needed: wave 1 had landed and was quiescent, and the hashes above are the same
before and after my work. While measuring, an ignored `corpus/instruments/__pycache__/recheck-audit.cpython-314.pyc`
appeared with mtime `21:20:58 -0300` from a concurrent seat's import: my first scratch copy (birth
`21:21:01`) already carried it, 13 s before my counter run (`21:21:11`), and every write of mine went
to `/tmp`. I left it untouched; no tracked file changed.

## 1. The row under test (verbatim, `corpus/instruments/limb-ledger.json:84-93`)

```json
{
  "id": "RA-expect-unexpected",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "sorted(actual - wanted)",
  "replace": "[]",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest expect-unexpected .*\\bok$",
  "note": "expected-list unexpected set collapsed to []: an extra tree entry no longer reds the audit; isolated by the expect-unexpected tree fixture (rc must be 1 and unexpected_entries must name extra.md)"
}
```

`find` is the second half of `expected_mismatch`'s return at `corpus/instruments/recheck-audit.py:194`
(`return sorted(wanted - actual), sorted(actual - wanted)`); it occurs exactly once in the instrument.

## 2. The counter's own line (lane run, scratch-only)

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

(The other 12 limb lines belong to sibling seats; kept only as the surrounding run. Wall time 19.3 s,
stderr empty.) The line under test: **`LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed`**.

## 3. Hand re-derivation on a scratch lane

```
$ S=$(mktemp -d /tmp/ra-ee.XXXXXX); cp -a corpus "$S/corpus"; cd "$S"
$ sha256sum corpus/instruments/recheck-audit.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09   # == landed instrument
$ python3 corpus/instruments/recheck-audit.py --selftest > live.out 2> live.err; echo "live_exit=$?"
live_exit=0
$ wc -l live.out live.err
39 live.out
 0 live.err
$ python3 -c "import re;t=open('live.out').read();m=re.search(r'(?m)^selftest expect-unexpected .*\bok$',t);print(bool(m), repr(m.group(0)))"
True "selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok"
```

The row's `live_exit=0` and `signal` therefore both hold on the unmutated bytes.

Mutation applied by hand with python (exactly-once assertion; decoded-UTF-8 semantics identical to the
counter's `text.count` + `text.replace(find, replace, 1)`):

```
$ python3 - <<'PY'
import json, pathlib
led = json.loads(pathlib.Path("corpus/instruments/limb-ledger.json").read_text())
row = next(r for r in led["limbs"] if r["id"] == "RA-expect-unexpected")
p = pathlib.Path("corpus/instruments/recheck-audit.py"); text = p.read_text()
print("find_count:", text.count(row["find"])); assert text.count(row["find"]) == 1
mut = text.replace(row["find"], row["replace"], 1); p.write_text(mut)
print("bytes_changed:", mut != text)
PY
find_count: 1
bytes_changed: True
$ stat -c '%s %n' corpus/instruments/recheck-audit.py
22859 corpus/instruments/recheck-audit.py            # pristine copy: 22880 B (21 B shorter: 23 chars -> "[]")
$ diff -u <pristine>/recheck-audit.py <mutant>/recheck-audit.py
@@ -191,7 +191,7 @@
     wanted = set(expected)
-    return sorted(wanted - actual), sorted(actual - wanted)
+    return sorted(wanted - actual), []
$ python3 -m py_compile corpus/instruments/recheck-audit.py; echo "compile_exit=$?"
compile_exit=0
$ python3 corpus/instruments/recheck-audit.py --selftest > mut.out 2> mut.err; echo "mut_exit=$?"
mut_exit=1
$ wc -l mut.out mut.err ; sha256sum corpus/instruments/recheck-audit.py
38 mut.out
 0 mut.err
8f06f2999ee91cd899ac9967b0682a239999f757f3b751f75608bb4b478e8ce5  corpus/instruments/recheck-audit.py
$ # signal check, re.MULTILINE, on stdout+stderr
live_signal_match=True   mut_signal_match=False (no line matches; the case line ends "FAIL")
```

Determinism (the counter runs each side twice and requires agreement):

```
$ python3 corpus/instruments/recheck-audit.py --selftest > live2.out  # pristine copy
live_second_run_exit=0 ; cmp live.out live2.out -> LIVE_RUN_STABLE=yes
$ python3 corpus/instruments/recheck-audit.py --selftest > mut2.out   # mutant copy
mut_second_run_exit=1 ; cmp mut.out mut2.out -> MUTANT_RUN_STABLE=yes
```

Running the kill through the absolute `{inst}` path from the scratch cwd (exactly the counter's
expansion) reproduces both runs byte-for-byte (`cmp` equal), so the relative-path form used above is
not a confound.

Hand result vs counter line — **no difference**:

| field | hand | counter |
|---|---|---|
| live | `0/y` | `0/y` |
| mutant | `1/n` | `1/n` |
| verdict | `killed` | `killed` |

## 4. Isolation: killed by the `expect-unexpected` case, not by a crash

`diff -u live.out mut.out` (pristine 39 lines → mutant 38 lines; `difflib` matching blocks: **35
identical lines**, 1 removed, 3 replaced). Every differing line belongs to the `expect-unexpected`
block; `expect-missing`, the 13 per-entry lines, the `complete-*` lines and the completeness sanity
line are byte-identical:

```diff
@@ -21,12 +21,11 @@
 selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
 extra.md                                                   frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
 good.md                                                    frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
-unexpected=corpus/knowledge/extra.md
 strict pass=2/2 cdroot_fail=0 instrument_fail=0 own_fail=0
 executes=2 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
-lines=2 total=2 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
-expect=present expected=1 missing=0 unexpected=1 exit=1
-selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
+lines=2 total=2 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
+expect=present expected=1 missing=0 unexpected=0 exit=0
+selftest expect-unexpected exit=0 want=1 missing=[] unexpected=[] FAIL
 strict pass=0/0 cdroot_fail=0 instrument_fail=0 own_fail=0
```

```
$ grep -c FAIL live.out mut.out ; grep -c '^selftest ' live.out mut.out
live:     0 FAIL, 18 selftest lines
mutant:   1 FAIL, 18 selftest lines
$ wc -c mut.err
0
```

The instrument still prints its whole selftest (all 18 `selftest ` lines, both entry-tree blocks, both
`complete-*` cases), stderr is empty, and exactly one case reds — so the `exit=1` comes from that one
`failures += 1`, not from an unrelated exception or an argparse/usage failure.

Mechanism, why this case and only this case. The fixture's nested `main()` run on the
`expect-unexpected` tree
(`corpus/instruments/recheck-audit.py:257`, assertions at `:285-290`) reports `pass=2/2`, `strict
pass=2/2`, `complete=True`, `missing=0` in both runs; the **only** failing conjunct on pristine bytes
is `expect_ok = not expect_active or (not missing_entries and not unexpected_entries)` (`:390`), which
is false solely because `unexpected_entries == ['corpus/knowledge/extra.md']`. Collapsing the
unexpected set to `[]` makes `expect_ok` true, so the nested audit exits 0, and the fixture's
`rc == 1 … unexpected_entries == [...]` assertion fails. The sibling `expect-missing` fixture is
untouched because the `wanted - actual` half of `:194` is intact.

Production path (non-fixture) on a scratch tree with `good.md` (listed) + `extra.md` (not listed) in
`corpus/instruments/knowledge-expected.txt`:

```
pristine instrument: exit=1   unexpected=['corpus/knowledge/extra.md'] missing=[]
mutant   instrument: exit=0   unexpected=[]                            missing=[]
both: strict pass=2/2, complete=True, pass=2/2   (identical except the unexpected conjunct)
```

That is the limb's stated effect (`note`: "an extra tree entry no longer reds the audit"), measured on
the real audit path rather than only through the fixture.

## 5. Discrimination: other one-limb mutants of the same limb

Each row is a fresh scratch lane from the landed bytes, one find/replace (count asserted = 1),
`py_compile`, then the row's kill command `python3 {inst} --selftest`. Baseline: `exit=0`,
signal=True, 39 stdout lines, 0 stderr bytes.

| mutant | site | find/compile | mutant exit | signal | selftest output | verdict |
|---|---|---|---|---|---|---|
| M1 (ledger row) `sorted(actual - wanted)` → `[]` | `:194` producer, collapse | 1 / ok | 1 | n | 4 lines (see §4) | killed |
| A1 consumer drop: `expect_ok = … (not missing_entries and not unexpected_entries)` → `expect_ok = … or not missing_entries` | `:390` consumer | 1 / ok | 1 | n | 3 lines: nested `exit=1→0`, `unexpected=1 exit=1 → unexpected=1 exit=0`, case `ok → FAIL` | killed |
| A2 wrong-but-nonempty: `sorted(actual - wanted)` → `sorted(actual & wanted)` | `:194` producer, value | 1 / ok | 1 | n | 4 lines replaced + 1 inserted across the `expect-missing` and `expect-unexpected` blocks (`unexpected=['corpus/knowledge/good.md']` in both) | killed |
| A3 display of names: `for name in unexpected_entries:` → `for name in ():` | `:411` stdout printer | 1 / ok | 0 | y | **1 line removed** (`unexpected=corpus/knowledge/extra.md`); receipt and exit unchanged | **survivor** |
| A4 display of count: `len(unexpected_entries),` → `0,` in the `expect=… unexpected=%d` print | `:471` stdout printer | 1 / ok | 0 | y | `expect=… unexpected=1 exit=1 → unexpected=0 exit=1`; receipt and exit unchanged | **survivor** |

A2 matters for shape discrimination: the fixture does not merely require a non-empty list — it asserts
exact membership, so a wrong nonempty set (`actual & wanted`) is killed as well. So the instrument
kills three distinct semantic shapes of this limb (collapse to `[]`, consumer-term drop, wrong
nonempty set), not one special-cased mutation.

A3/A4 are the honest boundary, and they are **not** the limb this row names: in both the unexpected
*set* is computed and consumed correctly, and only its human-readable stdout projection changes. They
show the fixture asserts the JSON receipt (`unexpected_entries`, `missing_entries`, `expect`, `rc`) but
never the printed `unexpected=<path>` lines or the printed `unexpected=<n>` count. A row targeting the
reporting projection would therefore survive today.

## 6. Verdict

**holds** for the ledger row `RA-expect-unexpected`.

- (1) Hand result == counter line == `live=0/y mutant=1/n verdict=killed`; `find` exactly once,
  mutated bytes differ (22880 → 22859 B), mutant compiles (exit 0), live run matches the row's signal.
  No defect.
- (2) Discrimination: killed for three distinct mutant shapes of this limb (producer collapse,
  consumer-term drop, wrong nonempty set). Two shape-invariant survivors exist only on the stdout
  display projection (§5 A3/A4), which is outside this row's semantics.
- (3) Isolation: the kill is one fixture case (`expect-unexpected`, `recheck-audit.py:257` + `:390`),
  4 differing output lines of 39, 35 identical, all 18 `selftest ` lines still printed, empty stderr,
  and a production-path run where only the unexpected conjunct changes.

**Finding for the L1 to route (not a row defect; this seat is read-only on instruments):** the
instrument's selftest pins the unexpected set in the receipt and the exit code, but not the two
stdout lines that report it (`recheck-audit.py:411` per-name print, `:466`/`:471` count print); A3 and A4
survive with `exit=0`, signal matching, and unchanged receipt. Concrete strengthening for the owning
executor (not applied here): in the `expect-unexpected` branch of the fixture loop, capture the nested
`main()` stdout with `contextlib.redirect_stdout` and assert it contains
`unexpected=corpus/knowledge/extra.md` and a summary line `missing=0 unexpected=1`; both assertions
pass on the landed bytes and fail under A3 / A4 respectively. This does not weaken the frozen claim:
C1's predicate is the 13 `LIMB` lines plus the two summary lines, which this row satisfies as measured.

Blockers: none. Cleanup: every `/tmp/ra-ee*`, `/tmp/altm`, `/tmp/a4-*` scratch lane removed after
measurement (`ls -d /tmp/ra-ee* /tmp/altm /tmp/a4-* 2>/dev/null` → nothing); the lane moved no bytes.
