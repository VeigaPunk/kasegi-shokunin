# ExecLimbRAcompleteness — falsify ledger limb `RA-completeness` (round-31 wave 2)

Seat: ExecLimbRAcompleteness (leaf). Model actually run on: `opencode-go/deepseek-v4.1-flash`
(config route table decides; no model passed). Date 2026-10-25.
Scope: falsification only — this seat writes nothing but this receipt; all attack work in
`mktemp` scratch copies under `/tmp`.

## Bytes pinned (quiescent at measurement)

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
$ git status --porcelain corpus
(empty)
```

The same three hashes were taken before the first run and after the last run of this seat:
no lane byte moved. If wave 2's ExecCounterFix rewrites the counter or ledger, the numbers
below are pinned to `c660a95f…` / `c042adf6…` and must be re-run (never compare across bytes,
M30-3).

Row under test (verbatim from the ledger, `json.dumps`):

```
instrument = corpus/instruments/recheck-audit.py
find       = "    complete = len(entries) == total and total > 0\n    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)"
replace    = "    complete = True  # mutant: completeness limb disabled\n    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)"
kill       = python3 {inst} --selftest
live_exit  = 0
signal     = (?m)^selftest complete-empty\s+exit=1 want=1 lines=0/0 complete=False ok$[\s\S]*^selftest complete-missing-line\s+exit=1 want=1 lines=1/2 complete=False ok$
```

## 1. Counter line on the landed bytes

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
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

13 `LIMB ` lines, 3 `CONTROL ` lines, summaries exact. (Counted: `grep -c '^LIMB '` = 13,
`grep -c '^CONTROL '` = 3.) Wall time 16.2 s. `git status --porcelain corpus` empty afterwards:
the counter wrote nothing into the lane.

## 2. Hand re-derivation (no counter code reused)

Scratch lane = `tempfile.mkdtemp` copy of `corpus/`; kill command run with `cwd=<scratch>`,
`{inst}` = `<scratch>/corpus/instruments/recheck-audit.py`, `PYTHONDONTWRITEBYTECODE=1`;
find applied with `str.replace(find, replace, 1)` after asserting `count == 1`;
`py_compile` with `doraise=True`.

Script `/tmp/hand_racompleteness.py` (outside the lane, never committed):

```python
#!/usr/bin/env python3
"""Hand re-derivation of ledger row RA-completeness (no counter code used)."""
import difflib, json, os, re, shutil, subprocess, sys, tempfile, py_compile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
led = json.load(open(os.path.join(LANE, "corpus/instruments/limb-ledger.json")))
row = [r for r in led["limbs"] if r["id"] == "RA-completeness"][0]
scr = tempfile.mkdtemp(prefix="hand-racomp-")
shutil.copytree(os.path.join(LANE, "corpus"), os.path.join(scr, "corpus"),
                symlinks=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
inst = os.path.join(scr, row["instrument"])

def kill():
    env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = row["kill"].replace("{inst}", inst).replace("{root}", scr)
    p = subprocess.run(["bash", "-c", cmd], cwd=scr, env=env, capture_output=True)
    text = p.stdout.decode("utf-8", "replace") + "\n" + p.stderr.decode("utf-8", "replace")
    return p.returncode, re.search(row["signal"], text, re.MULTILINE) is not None, text

orig = open(inst, "rb").read()
assert orig == open(os.path.join(LANE, row["instrument"]), "rb").read()
rc0, sig0, t0 = kill()
print("KILL=%s" % row["kill"])
print("LIVE  exit=%d signal=%s" % (rc0, sig0))
text = orig.decode("utf-8")
print("find_count_lane_bytes=%d" % open(os.path.join(LANE, row["instrument"]), "rb").read().count(row["find"].encode()))
mut = text.replace(row["find"], row["replace"], 1)
print("noop=%s" % (mut.encode() == orig))
mutant_file = os.path.join(scr, "mutant.py")
open(mutant_file, "w").write(mut)
try:
    py_compile.compile(mutant_file, cfile=os.path.join(scr, ".c.pyc"), doraise=True)
    print("py_compile=ok")
except py_compile.PyCompileError as exc:
    print("py_compile=FAILED %s" % exc)
    sys.exit(1)
shutil.copy2(mutant_file, inst)
shutil.rmtree(os.path.join(scr, "corpus/instruments/__pycache__"), ignore_errors=True)
rc1, sig1, t1 = kill()
print("MUTANT exit=%d signal=%s" % (rc1, sig1))
print("verdict_hand=%s" % ("killed" if (rc1 != row["live_exit"] or not sig1) else "survivor"))
print("case_lines live=%d mutant=%d  ok live=%d mutant=%d  FAIL live=%d mutant=%d  traceback_mutant=%s" % (
    len([l for l in t0.splitlines() if l.startswith("selftest ")]),
    len([l for l in t1.splitlines() if l.startswith("selftest ")]),
    len([l for l in t0.splitlines() if l.endswith(" ok")]),
    len([l for l in t1.splitlines() if l.endswith(" ok")]),
    len([l for l in t0.splitlines() if l.endswith(" FAIL")]),
    len([l for l in t1.splitlines() if l.endswith(" FAIL")]),
    "Traceback" in t1))
print("--- stdout diff (live vs mutant) ---")
for line in difflib.unified_diff(t0.splitlines(), t1.splitlines(), "live", "mutant", lineterm="", n=0):
    print(line)
print("--- mutant FAIL lines ---")
for line in t1.splitlines():
    if line.endswith(" FAIL"):
        print(line)
shutil.rmtree(scr, ignore_errors=True)
```

Output:

```
$ python3 /tmp/hand_racompleteness.py; echo "script_exit=$?"
KILL=python3 {inst} --selftest
LIVE  exit=0 signal=True
find_count_lane_bytes=1
noop=False
py_compile=ok
MUTANT exit=1 signal=False
verdict_hand=killed
case_lines live=18 mutant=18  ok live=18 mutant=16  FAIL live=0 mutant=2  traceback_mutant=False
--- stdout diff (live vs mutant) ---
--- live
+++ mutant
@@ -32,3 +32,3 @@
-lines=0 total=0 pass=0 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
-expect=absent expected=0 missing=0 unexpected=0 exit=1
-selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok
+lines=0 total=0 pass=0 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
+expect=absent expected=0 missing=0 unexpected=0 exit=0
+selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL
@@ -39 +39 @@
-selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
+selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL
--- mutant FAIL lines ---
selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL
selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL
script_exit=0
```

Hand result vs counter line — identical, field for field:

| field | counter | hand |
|---|---|---|
| live exit / signal | `0` / `y` | `0` / `True` |
| mutant exit / signal | `1` / `n` | `1` / `False` |
| verdict | `killed` | `killed` |
| find occurrences | accepted (would be `invalid:find-count` otherwise) | `1` (in lane bytes and in scratch) |
| compile gate | accepted | `py_compile` ok |
| no-op gate | accepted | `noop=False` |

No difference → no counter defect on this row.

## 3. Isolation — the mutant is killed by completeness cases, not by a crash

From the same run (numbers above):

- live: 18 `selftest …` case lines, **18** end ` ok`, 0 ` FAIL`, exit 0.
- mutant: 18 `selftest …` case lines (all 13 per-entry fixtures, the auxiliary
  `selftest completeness lines=13 total=15 complete=False ok`, both expected-list cases),
  **16** ` ok`, exactly **2** ` FAIL`, `Traceback` absent.

Lines that differ (full unified diff above, 2 hunks): only the summary block emitted by
`main()` inside the `complete-empty` fixture run (`lines=0 … exit=1` → `exit=0`,
`expect=absent … exit=1` → `exit=0`) and the two completeness-through-main case lines:

```
-selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok
+selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL
-selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
+selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL
```

The auxiliary line `selftest completeness lines=13 total=15 complete=False ok` still prints
`ok` under the mutant (it recomputes its own local formula), which is exactly the wave-1
design claim: only the two `main()`-level cases can observe main()'s `complete`.

Every other case is byte-identical and `ok`; the harness exit 1 is `selftest()`'s own
`return 1 if failures else 0` for the two failing cases, not an import/exec crash
(`py_compile` ok, module level runs, all 13 per-entry fixtures execute and print).

## 4. Discrimination — second (and third …) mutants of the same limb

Script `/tmp/disc_racompleteness.py` applies six alternative one-limb patches to the same
scratch copy, each gate-checked (`find` count, no-op, `py_compile`) and then run through the
same kill command:

```
$ python3 /tmp/disc_racompleteness.py; echo "exit=$?"
LIVE exit=0 signal=True  (ledger live_exit=0)
VAR | find# | noop | compile | exit | sig | verdict | FAIL lines
MUT-B drop total>0 only              | 1 | False | ok      | 1 | False | KILLED    | ['selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL']
MUT-C drop complete consumption      | 1 | False | ok      | 1 | False | KILLED    | ['selftest complete-empty        exit=0 want=1 lines=0/0 complete=False FAIL']
MUT-D equivalent tightening          | 1 | False | ok      | 0 | True  | SURVIVOR  | []
MUT-E total>0 only                   | 1 | False | ok      | 1 | False | KILLED    | ['selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL']
MUT-F first conjunct always true     | 1 | False | ok      | 1 | False | KILLED    | ['selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL']
MUT-G total from collected entries   | 1 | False | ok      | 1 | False | KILLED    | ['selftest complete-missing-line exit=0 want=1 lines=1/1 complete=True FAIL']
restored_pristine=True
exit=0
```

Patch texts (find → replace, all on the lane bytes of `recheck-audit.py`):

```
MUT-B  "    complete = len(entries) == total and total > 0\n"
    -> "    complete = len(entries) == total\n"
MUT-C  "    ok = passed == len(entries) and complete and strict_passed == total and expect_ok\n"
    -> "    ok = passed == len(entries) and strict_passed == total and expect_ok\n"
MUT-D  "    complete = len(entries) == total and total > 0\n"
    -> "    complete = len(entries) == total and total > 0 and len(entries) >= 0\n"
MUT-E  "    complete = len(entries) == total and total > 0\n"
    -> "    complete = total > 0\n"
MUT-F  "    complete = len(entries) == total and total > 0\n"
    -> "    complete = len(entries) >= 0 and total > 0\n"
MUT-G  "    total = len(glob.glob(os.path.join(root, \"corpus/knowledge/*.md\")))\n"
    -> "    total = len(entries)\n"
```

Reading:

- **Five of six alternative shapes are killed**, at three distinct code sites
  (`complete` expression, its consumption in `ok`, and the `total` computation), so the
  fixture set is *not* keyed to one mutant shape. Shapes exercised: whole-expression
  collapse (ledger row), sub-conjunct drop (MUT-B), consumption drop (MUT-C), `total>0`-only
  (MUT-E), first-conjunct-always-true (MUT-F), `total`-site (MUT-G).
- Each of the two new cases carries a class no other case kills:
  `complete-empty` alone kills MUT-B and MUT-C (exit flip 0→1 with `complete=True`);
  `complete-missing-line` alone kills MUT-E, MUT-F, MUT-G (receipt `complete` field flip with
  `lines<total`); the ledger row's mutant is caught by both. So neither case is dead weight.
- **MUT-D is correctly a SURVIVOR**: `and len(entries) >= 0` is a provable tautology
  (`len` is non-negative), so the patch has no observable behaviour — the instrument does not
  manufacture a kill for an equivalent patch (mirrors `CTL-equivalent`).
- Kill mechanism per shape stays the limb's own cases: every mutant's only `FAIL` line is a
  completeness case, and no run shows a traceback.

## 5. Note-level imprecision (documentation only; row itself holds)

The ledger `note` says: "Only 'total > 0' is observable alone, because strict_passed == total
already implies len(entries) == total". Measured, that is true only inside the exit rule
(`ok`): the first conjunct is still independently observable through the receipt's `complete`
field in `complete-missing-line` — MUT-F keeps every fixture exit at its expected value
(`complete-empty exit=1`, `complete-missing-line exit=1`) yet flips `complete` to `True`
there and is killed. The note's own last clause ("complete-missing-line carries the receipt
complete=False flip") already records that mechanism, so the sentence is internally
inconsistent rather than wrong in effect. No behaviour defect; a note rewrite would be a
Scribe/ledger-owner edit, not this seat's (ledger is read-only here).

## Verdict

**`holds`.**

- Counter line reproduced byte-for-byte on the landed bytes: `LIMB RA-completeness live=0/y
  mutant=1/n verdict=killed`, inside `limbs=13 killed=13 survivors=0` / `controls=3
  rejected=3`, exit 0.
- Hand re-derivation (independent scratch copy, manual find/replace with count assert,
  `py_compile`) gives the same exit/signal/verdict — the closure kill-rule clause is satisfied.
- The limb is load-bearing and the kill is attributable: exactly two of 18 case lines differ,
  both completeness cases, no traceback, all 13 per-entry fixtures still `ok`.
- The instrument's cases are not shape-locked: 5 alternative one-limb mutants across 3 code
  sites are killed; 1 provably equivalent patch correctly survives.
- Residual risk: the two new `main()`-level cases are the *only* observation surface for
  `complete`; if a future edit drops either one, MUT-E/MUT-F/MUT-G (or MUT-B/MUT-C) classes
  go unobserved. That is a maintenance note for the instrument owner, not a defect today.

## Bounds / reproducibility

- Lane writes: this receipt only (`git status --porcelain corpus` empty before and after;
  `recheck-audit.py` sha unchanged `5d4842da…`).
- All attack work under `/tmp` (`hand-racomp-*`, `disc-racomp-*`, `racomp-*` scratch lanes,
  deleted at exit; `git status` never touched: no `git` mutation command was run at all).
- No network, no pacman, no tool install, no lane git/jj mutation, no subagent dispatch.
- Commands above are copy-paste runnable from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
  the two helper scripts are reproduced verbatim so the numbers can be re-derived from these
  bytes.
