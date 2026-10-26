# ExecLimbRAparse — falsify ledger limb `RA-parse` (round 31, wave 2)

Seat: ExecLimbRAparse (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`, wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`).

Files written: this receipt only. The lane is otherwise read-only for this seat; every probe ran in
`mktemp -d` scratch copies, all of which were deleted (`ls -d /tmp/r31*` → no such file). No git/jj
mutation (read-only `git rev-parse`, `git status`), no delegation, no background job, no network
fetch, no credential material touched, no tool install/upgrade (nothing needed; pacman not invoked).
Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness route; no model passed).

Measured bytes (landed, unchanged at seat start and at seat end — same three hashes both times):

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ python3 -c "import hashlib; [print(p, hashlib.sha256(open(p,'rb').read()).hexdigest()) for p in ['corpus/instruments/recheck-audit.py','corpus/instruments/limb-ledger.json','corpus/instruments/limb-mutation-check.py']]"
corpus/instruments/recheck-audit.py        5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
corpus/instruments/limb-ledger.json        c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be
corpus/instruments/limb-mutation-check.py  c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f
```

No PRE-STATE label is needed: wave 1 had landed and quiescent, and nothing in the lane changed
between my first and last read (hashes above). The C1 claims file was not edited.

## 0. The row under test (verbatim, `corpus/instruments/limb-ledger.json:3-13`)

```json
{
  "id": "RA-parse",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "capture_output=True).returncode == 0",
  "replace": "capture_output=True).returncode >= 0",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest parseonly\\.md .*\\bok$",
  "note": "frozen limb (a) parse: the bash -n gate is defeated, so every returncode (including the syntax-error 2) counts as parseable; isolated by parseonly.md, the only fixture whose frozen verdict depends on parse alone"
}
```

`find` occurs exactly once in the landed instrument (`grep -c 'capture_output=True).returncode == 0'
corpus/instruments/recheck-audit.py` → `1`, at `corpus/instruments/recheck-audit.py:102`).

## 1. The counter's own line (lane run, scratch-only)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "EXIT=$?"
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
EXIT=0
```

(The other 12 limb lines belong to sibling seats; recorded here only as the surrounding run.)

## 2. Hand re-derivation of `RA-parse` on a scratch lane

```
$ S=$(mktemp -d /tmp/r31-raparse-XXXXXX); cp -a corpus "$S/corpus"; rm -rf "$S/corpus/instruments/__pycache__"
$ sha256sum "$S/corpus/instruments/recheck-audit.py"
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09   # == the lane instrument
$ python3 "$S/corpus/instruments/recheck-audit.py" --selftest > live.out 2> live.err; echo "LIVE_EXIT=$?"
LIVE_EXIT=0
$ wc -l live.out live.err
39 live.out
 0 live.err
$ python3 -c "import re;t=open('live.out').read();m=re.search(r'(?m)^selftest parseonly\.md .*\bok$',t);print(bool(m), repr(m.group(0)))"
True "selftest parseonly.md  pass want=False got=False | strict want=False got=False ok"
```

Mutant, applied by hand with python (exactly-once assertion, `py_compile`, byte identity check):

```
$ python3 - <<'PY'   # args: the scratch instrument path
find  = b"capture_output=True).returncode == 0"
repl  = b"capture_output=True).returncode >= 0"
data  = open(p,'rb').read(); n = data.count(find)
print("find_count=%d" % n); assert n == 1
mut = data.replace(find, repl); assert mut != data; open(p,'wb').write(mut)
PY
find_count=1
mutated_bytes_identical=False
orig_sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
mut_sha256=2eaf92f2ce10170568dfc8c2624c62a7d78a1e2110af731047e9ea2529b88ff9
CHANGED_LINE_OLD=b'    return subprocess.run(["bash", "-n", "-c", cmd], capture_output=True).returncode == 0'
CHANGED_LINE_NEW=b'    return subprocess.run(["bash", "-n", "-c", cmd], capture_output=True).returncode >= 0'
$ python3 -m py_compile "$S/corpus/instruments/recheck-audit.py"; echo "COMPILE_EXIT=$?"
COMPILE_EXIT=0
$ rm -rf "$S/corpus/instruments/__pycache__"
$ python3 "$S/corpus/instruments/recheck-audit.py" --selftest > mut.out 2> mut.err; echo "MUT_EXIT=$?"
MUT_EXIT=1
$ # signal check on stdout+stderr, python re.search:
live_signal_match=True  match='selftest parseonly.md  pass want=False got=False | strict want=False got=False ok'
mut_signal_match=False  match=None
```

Hand verdict: `live=0/y mutant=1/n verdict=killed`, i.e. **byte-for-byte the counter's line**
(`LIMB RA-parse live=0/y mutant=1/n verdict=killed`). Difference at step (1): **none** — no defect.

## 3. Isolation: the kill is case-specific, not a crash

`diff live.out mut.out` on the two 39-line stdout streams:

```
12c12
< selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
---
> selftest parseonly.md  pass want=False got=True  | strict want=False got=True  FAIL
```

Exactly one line of 39 differs; all 12 other per-entry case lines still print `ok`; both tree-level
expected-list lines, both `complete-*` lines, the three `main()` summary blocks and every entry print
line are unchanged; `mut.err` is empty (0 bytes), so the mutant did not crash — the instrument ran
its whole selftest and failed only the `parseonly.md` assertion (`corpus/instruments/recheck-audit.py:234`).
The mutant's `exit=1` therefore comes from that single `failures += 1`.

Mechanism, why this case and only this case: `parseonly.md`
(`corpus/instruments/recheck-audit.py:226`) is the one fixture whose line is a bash *syntax error*
(`... test -d ~/Projects/bounties (fails closed today)` → `bash -n` exits 2). With the real gate
(`:102`) that is `parse=False`; under `>= 0` every exit code is `True`, so `pass` flips and only that
line reds. Every other fixture line parses cleanly, so `== 0` and `>= 0` agree on all of them.

## 4. Discrimination: other one-limb mutants of the same limb

Each row is a fresh scratch lane from the landed bytes, one find/replace, `py_compile`, then the same
kill command `python3 {inst} --selftest`. Baseline (pristine scratch): `exit=0 signal=True
stdout_lines=39 stderr_bytes=0`.

| mutant | site | find count / compiles | mutant exit | signal | selftest output | FAIL cases | verdict |
|---|---|---|---|---|---|---|---|
| M1-ledger (`>= 0`) | `:102` comparison | 1 / 0 | 1 | n | 1 line differs | `parseonly.md` | killed |
| M2-invert (`!= 0`) | `:102` comparison, inverted | 1 / 0 | 1 | n | 19 of 39 lines differ (13 `FAIL`) | 10 case lines (`good`, `degenerate`, `elsewhere`, `ownonly`, `selftesty`, `sourced`, `basetest`, `basestate`, `parseonly`, `instonly`) + 3 `main()` entry prints (`frozen=011 … FAIL`) | killed |
| M3-rc-except-2 (`!= 2`) | `:102` comparison, rc domain | 1 / 0 | 0 | y | **byte-identical** | none | **survivor** |
| M4-class-site (`"gated" if True`) | `:162` class projection | 1 / 0 | 0 | y | **byte-identical** | none | **survivor** |
| M5-parse-field (`limbs["parse"] = True`) | `:121` assignment | 1 / 0 | 1 | n | 1 line differs | `parseonly.md` | killed |

So the instrument kills three distinct mutant shapes on the parse→`pass` path (gate disabled, gate
inverted, parse field hardcoded) — not merely the ledger's one shape.

**M3 (`returncode != 2`) is equivalent within the reachable exit-code domain, not a coverage hole.**
`parse_ok` consumes only `bash -n -c`'s exit code. Probing 40 inputs (valid lines, unterminated quote,
bare `if`/`then`/`&&`, unbalanced `#`/`$(`/`((`, `exec 9>&-`, `coproc`, `function f {`, …) yields only
two distinct codes:

```
rc=0 count=15 examples=['true', '', ':', 'cd /tmp && true']
rc=2 count=25 examples=["echo 'unterminated", 'if', 'foo(', 'cd /tmp && test -d ~/Projects/bounties (fails closed today)']
distinct_rc=[0, 2]
```

On `{0, 2}`, `rc != 2` ⟺ `rc == 0`, so no fixture (and no corpus line) can distinguish M3 from the
real gate. I state this as equates-on-observed-domain `{0,2}` plus the arithmetic identity, not as a
proof about every input bash's parser could ever reject — no distinguishing input was found.

**M4 is a real, observably different survivor — a coverage gap at the parse limb's *class*
projection.** The mutated line `:162` (`else ("gated" if limbs["parse"] else "broken")`) is the parse
limb's other consumer; `:234` asserts only `record["pass"]` and `record["pass_strict"]`, never
`record["class"]`. M4's selftest output is byte-identical to pristine and its exit is also 0, yet it
is not equivalent — a tree with one syntax-broken entry shows it (`main()` on
`corpus/knowledge/broken.md` = `recheck: cd <tree> && test -d ~/Projects/bounties (fails closed today)`):

```
pristine      exit=1 complete=True entry_class='broken' broken=1 gated=0
M4-class-site exit=1 complete=True entry_class='gated'  broken=0 gated=1
```

Both runs print identical summary stdout, but the JSON receipt's per-entry `class`, and the
`broken`/`gated` counts (`corpus/instruments/recheck-audit.py:385-386`), disagree. The same gap
covers `failing_limbs["parse"]` and the printed `parse_fail=` counter, none of which any selftest
case reads.

## 5. Verdict

**holds** for the ledger row `RA-parse`.

- (1) hand result == counter line == `live=0/y mutant=1/n verdict=killed`; find exactly once,
  mutated bytes differ, mutant compiles, live run matches the row's signal. No defect.
- (2) discrimination: the row's shape is not a lone special case (M2, M5 also killed on the same
  limb); M3 is equivalent on the reachable `bash -n -c` code domain `{0,2}`.
- (3) isolation: the kill is one case line (`parseonly.md`), one differing line of 39, empty stderr,
  normal selftest run — not an unrelated crash.

**Finding for the L1 to route (not a row defect; this seat is read-only on instruments):** the
instrument's selftest pins the parse→`pass` projection only. A single-line mutant at
`corpus/instruments/recheck-audit.py:162` survives with byte-identical output, so the parse limb's
`class`/`broken`/`gated` and `failing_limbs["parse"]` projections are unpinned. Concrete
strengthening (for the owning executor, not applied here): in the fixture loop, also assert
`record["class"] == ("gated" if ... )` — simplest is to add to the `parseonly.md` case an expectation
`class == "broken"` (its line is a syntax error with a non-zero lane exit), or add one `main()`-level
case over a syntax-broken entry asserting `receipt["entries"][0]["class"] == "broken"`,
`receipt["broken"] == 1`, `receipt["gated"] == 0`. Both fail under M4 and pass on the landed bytes.
This does not weaken the frozen claim: C1's predicate is the 13 `LIMB` lines plus summary, which the
row satisfies as measured.

Blockers: none. Scratch directories and temp scripts removed after measurement
(`ls -d /tmp/r31*` → `no_r31_tmp_left`).
