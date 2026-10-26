# ExecLimbRAinstrument — falsify C1 ledger limb `RA-instrument` (strict limb (e), instrument)

Seat: ExecLimbRAinstrument. Round 31, wave 2. Lane base `b374febbb`; wave-1 integration `eecad59`.
Answering model: `opencode-go/deepseek-v4.1-flash` (route-table default; no model passed).
Tool installs/upgrades: none (no pacman — paused host-wide; no network fetch; no uv/npx needed).
Writes: this receipt only. Lane instruments/ledger read-only; every attack ran in a `mktemp -d` scratch copy of `corpus/`.
No git/jj mutation was run (read-only `git log`/`git status` only). No subagent, no background job, no network.

## 0. Bytes under test

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
$ git -C . log --oneline -1
eecad59 round-31: wave-1 integration (C1 limb ledger+counter, C2 F15/S048, score-gap, erratum, LOG r30), wave-2 spec
```

`recheck-audit.py` = `5d4842da…` is the landed wave-1 bytes (same digest recorded in
`wave1/ExecRALimbs.md:17`, `wave1/ExecExpectedList.md:33`, `wave1/CritC1Kill.md:14`).

Ledger row, read out of the landed JSON (not retyped):

```json
{
  "id": "RA-instrument",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "strict[\"instrument\"] = bool(instruments) or base_test",
  "replace": "strict[\"instrument\"] = True",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest instonly\\.md .*\\bok$",
  "note": "strict limb (e) instrument: the corpus/instruments-or-base-test requirement collapsed to True; isolated by instonly.md (own file named, cdroot ok, no instrument named)"
}
```

Code site (`audit_entry`, `recheck-audit.py:138-140`):

```python
    instruments = [tok for tok in INSTRUMENT_RE.findall(line) if os.path.exists(os.path.join(root, tok))]
    base_test = bool(BASE_TEST_RE.search(line))
    strict["instrument"] = bool(instruments) or base_test
```

Frozen limb text (`recheck-audit.py:28-29`, docstring):

```
  (e) instrument the command names an existing `corpus/instruments/<name>.py`, or
                 runs a `test -d/-e/-f ~/Projects/...` base test.
```

Fixture the note names (`selftest` `cases`, `recheck-audit.py:227`):

```python
"instonly.md": ("recheck: cd %s && ls corpus/knowledge/instonly.md corpus/knowledge/target.md" % tmp, True, False),
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

Two full runs, 2026-10-26 00:20:01Z and 00:21:24Z, byte-identical (`diff` empty), so the line is not a
one-shot artifact of concurrent wave-2 activity:

```
$ diff /tmp/ra_instr_counter.txt /tmp/ra_instr_counter2.txt && echo IDENTICAL
IDENTICAL
```

Line under test: `LIMB RA-instrument live=0/y mutant=1/n verdict=killed` (wall 20.9 s for the whole ledger).

## 2. Hand re-derivation (independent of the counter)

Fresh scratch copy of the whole `corpus/` tree, no lane bytes touched:

```
$ S=$(mktemp -d /tmp/rainstr.XXXXXX); cp -a <lane>/corpus "$S/corpus"
$ cd "$S" && python3 corpus/instruments/recheck-audit.py --selftest > live.out 2> live.err; echo live_exit=$?
live_exit=0
```

Signal on the unmutated run — exactly one matching line, so the row's regex is uniquely bound:

```
live signal matches 1
live run1 0 True run2 0 True identical True     # two consecutive live runs: stable (exit, signal, bytes)
```

Patch applied by hand with python (never `sed`), with the contract's three gates:

```
$ python3 - <<'EOF'   # reads the row from the landed ledger, patches the SCRATCH copy
...
$ find_count 1
$ mutated_equals_original False
$ python3 -m py_compile "$S/corpus/instruments/recheck-audit.py"; echo compile_exit=$?
compile_exit=0
```

Mutant run (measured through `subprocess.run`, so the raw exit code is captured verbatim):

```
$ python3 -c "... subprocess.run([sys.executable,'corpus/instruments/recheck-audit.py','--selftest'], cwd='$S') ..."
exit 1
stdout_len 3173 stderr_len 0
mutant_exit 1 signal_instonly False traceback False stderr_len 0
```

Three consecutive mutant runs are byte-identical (`sha256 79e00d54f7b1588d41d55c1cc11f334d00520faa75708ac354726d0ac8ed80a9`),
so the mutant side is stable too (`measure_runs` in the counter requires exactly this).

**Hand result vs counter line — identical:** `live=0/y mutant=1/n verdict=killed`. No difference, so no
defect under the item's clause (1).

Two measurement details that make the comparison honest:

- The counter does **not** reuse a scratch: `evaluate_row` runs both baseline runs on one scratch and the
  mutant runs on a second, untouched one (`measure_side`). My hand run mutated a single scratch in place.
  Same verdicts from both procedures, so the kill does not depend on scratch reuse or on run order.
- This harness shell aborts a command line when a child exits non-zero (errexit-like), which is why the
  mutant side above is measured through `subprocess.run`; the exit code `1` is recorded from the child,
  not inferred from the shell. Nothing in the instrument caused that: its two subprocess call sites are
  `subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, timeout=300)` at `:98` and
  `subprocess.run(["bash", "-n", "-c", cmd], capture_output=True)` at `:102`, and there is no
  `killpg`/`setsid`/`os.kill`/signal delivery anywhere in the file.

Causal attribution — importing pristine and mutant copies from `/tmp` (never from the lane, so no
`__pycache__` is written into `corpus/instruments/`) and calling `audit_entry` on the same fixture trees:

```
== ownonly.md
  pristine strict {"cdroot": true, "cwd": true, "instrument": false, "own": true, "parse": true, "paths": true} pass_strict False
  mutant   strict {"cdroot": true, "cwd": true, "instrument": true,  "own": true, "parse": true, "paths": true} pass_strict True
  frozen limbs equal: True | differing strict keys: ['instrument']
== instonly.md
  pristine strict {"cdroot": true, "cwd": true, "instrument": false, "own": true, "parse": true, "paths": true} pass_strict False
  mutant   strict {"cdroot": true, "cwd": true, "instrument": true,  "own": true, "parse": true, "paths": true} pass_strict True
  frozen limbs equal: True | differing strict keys: ['instrument']
== good.md
  ... differing strict keys: []
```

The collapse moves exactly one strict key, on exactly the two fixtures where `instrument` is the only
false limb; `good.md` (instrument named, own named) is untouched. The patch itself is minimal — one line,
one token:

```
140 -     strict["instrument"] = bool(instruments) or base_test
140 +     strict["instrument"] = True
line_delta True byte_delta -26
```

## 3. Discrimination — other one-limb mutants of the same limb

Three structurally different single-site mutants of the declared limb (e), each `find` asserted to occur
exactly once, each `py_compile`-clean, each run in its own fresh scratch copy, each also fed to the real
counter through a temp ledger outside the lane (`--ledger /tmp/ra-instr-probe/ledger-{A,B,C}.json --root <lane>`):

| probe | patch site | mutant exit / signal | hand verdict | counter verdict | changing lines |
|---|---|---|---|---|---|
| P1 invert | `bool(instruments) or base_test` → `not (bool(instruments) or base_test)` | 1 / n | killed | `LIMB RA-instrument-inverted live=0/y mutant=1/n verdict=killed` (exit 0) | 22 |
| P2 `or`→`and` | same expression, other operator | 1 / **y** | killed (exit only) | `LIMB RA-instrument-and live=0/y mutant=1/y verdict=killed` (exit 0) | 18 |
| P3 drop existence filter | `instruments = [tok for tok in INSTRUMENT_RE.findall(line) if os.path.exists(...)]` → `instruments = [tok for tok in INSTRUMENT_RE.findall(line)]` | 0 / y | **SURVIVOR** | `LIMB RA-instrument-filter live=0/y mutant=0/y verdict=survivor` / `limbs=1 killed=0 survivors=1` / `probe_B_exit=1` | 0 |

Raw P3 evidence — byte-identical output, so no case the instrument ships can see it:

```
$ diff live.out mut.out ; echo differing=$(...)
    (no output)
differing lines: 0
P3: mutant_exit 0 stderr_len 0 signal_instonly True
```

**So yes, the instrument's own cases kill only some shapes:** they kill the whole-expression collapse
(the ledger's row), the inversion, and the operator swap — every shape that changes the *result* of the
limb on a fixture that names no instrument. They cannot kill a mutant of the limb's **existence
qualifier**, because no fixture in `recheck-audit.py`'s `cases` names an absent `corpus/instruments/*.py`.

P3 is not an equivalent mutant — it is observable, and only outside the fixture set. Attribution first,
via `audit_entry` on the same synthetic line:

```
# synthetic entry line `recheck: cd <tmp> && ls corpus/instruments/typo.py` (typo.py absent)
pristine strict {"cdroot": true, "cwd": true, "instrument": false, "own": false, "parse": true, "paths": false} pass_strict False
p3       strict {"cdroot": true, "cwd": true, "instrument": true,  "own": false, "parse": true, "paths": false} pass_strict False
differing strict keys ['instrument']
```

The same flip reaches the instrument's own non-selftest report. `STRICT_LIMBS` (`recheck-audit.py:89`) is
`("parse","cwd","paths","cdroot","instrument","own")`, so `instrument` is the 5th bit of the 6-bit
`strict=` string, and `instrument_fail=` counts the same limb. Pristine vs P3 on a one-entry synthetic
root whose line names an absent `corpus/instruments/typo.py`:

```
$ python3 /tmp/ra_pristine2/pristine.py --root "$R" > pri.txt
$ python3 /tmp/ra_pristine2/p3.py       --root "$R" > p3.txt
--- pristine
absentinst.md    frozen=110 strict=110100 lane=2 foreign=2 gated FAIL
strict pass=0/1 cdroot_fail=0 instrument_fail=1 own_fail=1
lines=1 total=1 pass=0 fail-closed=1 parse_fail=0 cwd_fail=0 paths_fail=1 exit=1
--- p3
absentinst.md    frozen=110 strict=110110 lane=2 foreign=2 gated FAIL
strict pass=0/1 cdroot_fail=0 instrument_fail=0 own_fail=1
lines=1 total=1 pass=0 fail-closed=1 parse_fail=0 cwd_fail=0 paths_fail=1 exit=1
```

The 5th strict bit goes `0 → 1` and `instrument_fail` goes `1 → 0`; `pass_strict` stays False because
`paths` already fails, so only the per-limb breakdown can see it. No selftest case names an absent
instrument, hence the survivor. The counter is honest about it: it prints `verdict=survivor` and exits 1
rather than counting the row as a kill.

## 4. Isolation — the kill is case-specific, not an unrelated crash

```
$ diff live.out mut.out
7c7
< selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
---
> selftest ownonly.md    pass want=True  got=True  | strict want=False got=True  FAIL
13c13
< selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
---
> selftest instonly.md   pass want=True  got=True  | strict want=False got=True  FAIL
```

Two lines differ out of 39, and both are strict-verdict lines whose only differing strict key is
`instrument` (§2). The mutant keeps the instrument's whole banner:

```
live case lines present True FAIL lines 0 exit lines 12
mutant case lines present True FAIL lines 2 exit lines 12
```

i.e. all 13 per-entry case lines, the `completeness` oracle, both expected-list cases and both `main()`
blocks print normally; `stderr` is empty (`stderr_len 0`), no traceback, and exit `1` is the instrument's
own `return 1 if failures else 0` — not a crash. The row's kill therefore comes from the fixture verdicts,
not collateral damage.

The note says the limb is "isolated by instonly.md"; it is actually decided by **two** fixtures
(`instonly.md` and `ownonly.md` — wave 1 already disclosed this at `wave1/ExecRALimbs.md:194`). Ablating
`ownonly.md` from the fixture dict proves the note's named case is sufficient on its own:

```
ownonly_fixture_lines 1
ablated pristine: exit 0 instonly_sig True
ablated mutant: exit 1 instonly_sig False fail_lines ['selftest instonly.md   pass want=True  got=True  | strict want=False got=True  FAIL']
```

(Observation for the L1, not a defect of this row: `ownonly.md` and `instonly.md` are strict-limb
equivalent — same `strict` dict, same single false key — so `ownonly.md` contributes no discriminating
case that `instonly.md` does not already provide for any of the 13 limbs. It is fixture redundancy, not
missing coverage.)

## 5. Cleanliness / bounds

```
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json   # after all runs
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
$ git -C <lane> status --porcelain | grep -v '^??'
(no tracked modifications)
```

Unchanged before/after: every probe ran on `/tmp` copies; the only lane reads were `read`/`grep` and the
read-only `git log`/`status`. `corpus/instruments/__pycache__/` is gitignored and holds a
`recheck-audit.cpython-314.pyc` written by a concurrent seat importing in-lane; my imports used `/tmp`
copies named `pristine.py`/`mutant.py` with `sys.dont_write_bytecode=True`, so no pyc of mine can exist
(`ls __pycache__` shows no `pristine`/`mutant`/`p3` entries). Counter scratch discipline is the counter's
own: `build_scratch` copies `corpus/` into `tempfile.mkdtemp(prefix="limb-mutation-")` with
`shutil.ignore_patterns("__pycache__", "*.pyc")`, and `evaluate_row`/`measure_side` `rmtree` it
in `finally`. My scratch dirs are outside the lane and were removed after this receipt was written
(`ls -d /tmp/rainstr* /tmp/ravariant* /tmp/rav2* /tmp/raablate* /tmp/rastable* /tmp/ra_pristine*
/tmp/rap3root* /tmp/ra-instr-probe` → 0 hits).

## 6. Verdict

**`holds`.** `RA-instrument` is a real single-line, exactly-once patch site (`recheck-audit.py:140`,
−26 B); on the landed bytes `5d4842da…` the live baseline exits 0 with the row's signal present, the
mutant compiles, exits 1 and loses that signal; my hand derivation reproduces the counter's line exactly
(`live=0/y mutant=1/n verdict=killed`), twice over, on both sides stable. The kill is isolated: 2 of 39
lines differ, both strict-`instrument` verdicts, full banner intact, empty stderr, and the flip is
attributable to the `instrument` key alone (`differing strict keys: ['instrument']`). A second
(inversion) and a third (`or`→`and`) mutant of the same limb are killed as well, and the counter labels
all three shapes correctly when fed through a temp ledger.

Recorded, non-blocking — **finding F1 (report-only; `recheck-audit.py` is outside this seat's write
scope):** the limb's declared **existence qualifier** (`:138`, "names an *existing* … .py") has no
fixture. Dropping the `os.path.exists` filter is a genuine (observable in the strict bit string and
`instrument_fail`) one-limb mutant that survives byte-identically, and the counter rightly reports it
`survivor`. The ledger row's declared patch is the whole-expression collapse and that is killed, so the
claim is not falsified; the gap is closable with one case naming an absent `corpus/instruments/*.py`
(e.g. `recheck: cd <tmp> && ls corpus/instruments/typo.py`) whose expected `strict` bit is
`instrument=False`.

Routed defects: none found in the counter, the ledger row, or the isolation claim. F1 is an
instrument-fixture depth gap for the L1 to route.
