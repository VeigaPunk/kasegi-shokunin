# ExecLimbRApaths — falsify C1 ledger limb `RA-paths` (round 31, wave 2)

Seat: ExecLimbRApaths (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze `738a77999a00efbca129cfccb28a481037f6241f`.
Lane HEAD at seat start: `eecad59 round-31: wave-1 integration (C1 limb ledger+counter, C2
F15/S048, score-gap, erratum, LOG r30), wave-2 spec`.
Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness-reported route; no model
was passed anywhere).
Tooling: nothing installed or upgraded this wave (no pacman, no uv/npx needed; stdlib python3 only).

Writes made by this seat: **this receipt only**. No file under `corpus/`, no registry/README/SKILL/
PROVINCE, no `.ufo/state`, no scratch inside the lane (all scratch under `mktemp -d` in `/tmp`), no
git/jj mutation (read-only `git log`/`git status` only). Verified: `git status --porcelain corpus/
SCORECARD.md SHONEN.md` → empty output (run after the counter run).

Subject bytes measured before and after all runs (identical, lane quiescent):

```
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```

Note (bounds 6): the counter hash is **not** the `eb9b87ff…` wave-1 cited; `limb-mutation-check.py`
is a wave-2 ExecCounterFix path, so its bytes are in flight. My hand replication below stands on the
instrument bytes only (`recheck-audit.py` + `limb-ledger.json`), both stable across the seat; the
counter line is quoted with its hash stamp.

## 1. The row under test (verbatim from the landed ledger)

```
$ python3 -c "import json;d=json.load(open('corpus/instruments/limb-ledger.json'));print(json.dumps([r for r in d['limbs'] if r['id']=='RA-paths'][0],indent=2))"
{
  "id": "RA-paths",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "limbs[\"paths\"] = named and not missing",
  "replace": "limbs[\"paths\"] = True",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest ghost\\.md .*\\bok$",
  "note": "frozen limb (c) paths: the named-and-exists conjunction collapsed to True; isolated by ghost.md (names an absent corpus/knowledge path while parse and cwd still pass)"
}
```

Code under mutation, `corpus/instruments/recheck-audit.py:130-132`:

```
    named = bool(tokens) or bool(HOME_BASE_RE.search(line))
    missing = [tok for tok in tokens if not os.path.exists(os.path.join(root, tok))]
    limbs["paths"] = named and not missing
```

Witness fixture, `corpus/instruments/recheck-audit.py:214`:

```
"ghost.md": ("recheck: cd %s && test -e corpus/knowledge/ghost-absent.md" % tmp, False, False),
```

## 2. Hand re-derivation on the LANDED bytes (independent of the counter)

Driver run in the session Python kernel: `tempfile.mkdtemp()`, `shutil.copytree(<lane>/corpus,
<scratch>/corpus)`, kill command `row["kill"].replace("{inst}", <scratch>/corpus/instruments/
recheck-audit.py)`, `bash -c` with `cwd=<scratch>`, `PYTHONDONTWRITEBYTECODE=1`, then
`src.count(find)` asserted, `src.replace(find, replace, 1)`, `python3 -m py_compile`, second run.

Printed output, verbatim:

```
scratch: /tmp/ralimb-paths-8fpmyb23
inst sha256: 5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
cmd: python3 /tmp/ralimb-paths-8fpmyb23/corpus/instruments/recheck-audit.py --selftest
live_exit=0 signal_match=True
```

```
find_count=1 expected 1
bytes_differ=True
mutant sha256: 84e7d82fc4683621a4cb922c0e8ebca0507759ff567e65e97334da69bdd8b65f
py_compile exit=0 stderr=''
mutant_exit=1 mutant_signal_match=False
--- differing lines (live vs mutant) ---
--- live
+++ mutant
@@ -4 +4 @@
-selftest ghost.md      pass want=False got=False | strict want=False got=False ok
+selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
mutant_ok_lines=17 total_lines=39
```

Hand result: `live=0/y mutant=1/n` → **killed**.

Lane run of the real counter (same invocation the L1's C1 predicate uses):

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

Counter's `LIMB RA-paths live=0/y mutant=1/n verdict=killed` is **identical** to my hand row
(`live=0/y mutant=1/n killed`). No difference → no counter defect on this row. The counter also
reported nothing else changed under my hands: `corpus/` stayed git-clean after the run (§ top).

## 3. Isolation — the kill is limb-specific, not a crash

The mutant's stdout differs from pristine on **exactly one line** (unified diff in §2, `n=0`
context: one hunk, one line). The mutant run still prints all 17 other `… ok` selftest lines, both
`complete-*` lines (`ok`), the per-tree gauge lines (`frozen=… strict=… lane=… foreign=… executes`),
and the expected-list lines; exit 1 comes from the `failures` counter, not from an exception
(`py_compile exit=0`, no traceback in output).

The witness itself is limb-isolated. Rebuilding the ghost fixture by hand and auditing it with the
instrument's own `audit_entry()` (pristine bytes, private tmp tree):

```
line: recheck: cd /tmp/ghostfixture-w9kapzln && test -e corpus/knowledge/ghost-absent.md
limbs: {'parse': True, 'cwd': True, 'paths': False}
strict: {'parse': True, 'cwd': True, 'paths': False, 'cdroot': True, 'instrument': False, 'own': False}
pass: False pass_strict: False class: gated missing: ['corpus/knowledge/ghost-absent.md']
```

parse and cwd are already True on the pristine bytes, so `pass` is False **only** because
`paths` is False; under the mutant `paths` alone flips, `pass` flips, and `strict` stays False
(unchanged) — which is why the FAIL line reads `strict want=False got=False FAIL`. The signal
`(?m)^selftest ghost\.md .*\bok$` matches the pristine line and stops matching the mutant line, as
the ledger requires.

## 4. Discrimination — three further one-limb mutants of the same limb

Each on its own fresh scratch copy of the landed corpus; same kill command, same baseline check
(`live_exit=0`, signal matches) already established in §2.

| # | mutant (site) | exit | signal | verdict by counter rules |
|---|---|---|---|---|
| B1 | `missing = []` (line 131 — the *existence* computation nulled) | 1 | n | killed (ghost.md FAIL) |
| B2 | `limbs["paths"] = named or not missing` (line 132, `and`→`or` inversion) | 1 | n | killed (ghost.md FAIL) |
| B3 | `named = True` (line 130 — the *other* conjunct's probe forced) | **0** | **y** | **survivor** |
| B4 | existence checked against `/` instead of `root` (line 131) | 1 | y | killed, but by 11 unrelated lines (not isolated) |

Verbatim output:

```
== B1 missing=[] at line 131
   bytes_differ=True py_compile=0 exit=1 signal_match=False ok_lines=17
   FAIL: selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
   verdict_by_counter_rules=killed
== B2 and->or at the same line
   bytes_differ=True py_compile=0 exit=1 signal_match=False ok_lines=17
   FAIL: selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
   verdict_by_counter_rules=killed
== B3 named=True (other conjunct)
   bytes_differ=True py_compile=0 exit=0 signal_match=True ok_lines=18
   verdict_by_counter_rules=survivor
== B4 existence checked against foreign root
   bytes_differ=True py_compile=0 exit=1 signal_match=True ok_lines=10
   FAIL: selftest good.md       pass want=True  got=False | strict want=True  got=False FAIL
   … (10 more FAIL lines: degenerate/elsewhere/ownonly/selftesty/sourced/basetest/instonly + 3 tree gauges)
   verdict_by_counter_rules=killed
```

Confirmed by the real counter on a scratch ledger outside the lane
(`/tmp/ralimb-paths-ledger/rows.json`, rows A + B3 only, `--ledger` pointed there):

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger /tmp/ralimb-paths-ledger/rows.json; echo "counter_exit=$?"
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-paths-named live=0/y mutant=0/y verdict=survivor
limbs=2 killed=1 survivors=1
controls=0 rejected=0
counter_exit=1
```

**So the instrument's own cases kill exactly one mutant shape for this limb: the collapse delivered
by the ledger row (and the `missing`/`and` variants behind it). They do not kill the `named` half.**
B3 is *not* provably equivalent: forcing `named` True makes a tokenless, home-base-free recheck line
report `paths=True` instead of `False`. The masking reason is the fixture roster: the only fixture
with no corpus path token is `prose.md` (`recheck-audit.py:212`), and its expected verdict is already
False via `parse` (its prose is not `bash -n`-clean), so `paths` is unobservable there. Every other
fixture tokenizes at least one `corpus/…` path or names a `~/Projects/…` base.

Live-corpus scope of B3 today: all 44 `corpus/knowledge/*.md` recheck lines were re-audited with the
instrument's own helpers; 42 tokenize ≥1 corpus path, and the 2 tokenless rows (`repo-git-state.md`,
`root-loss-2026-10-12.md`) are `named=True` through `HOME_BASE_RE` (`test -d ~/Projects/bounties`
forms). So B3 is behaviorally silent on the current live corpus and on the current selftest — it is a
**future-line** hole in the limb assertion, not a live mis-verdict.

## 5. Strengthening that would kill B3 (proved in scratch; lane instrument NOT edited)

Proposed fixture, inserted into the scratch copy's `cases` dict after `prose.md`
(`recheck-audit.py:212`), a line that parses, runs identically from the lane and from `/`, names no
corpus artifact and no home base — so `paths` is the only limb that can decide it:

```python
"pathless.md": ("recheck: cd %s && true" % tmp, False, False),
```

Scratch experiment (fresh copy per arm, kill command `python3 {inst} --selftest`):

```
== strengthened pristine exit=0 fail_lines=0
   selftest pathless.md   pass want=False got=False | strict want=False got=False ok
== strengthened + B3 named=True exit=1 fail_lines=1
   FAIL: selftest pathless.md   pass want=False got=True  | strict want=False got=False FAIL
== strengthened + ledger A mutant exit=1 fail_lines=2
   FAIL: selftest pathless.md   pass want=False got=True  | strict want=False got=False FAIL
   FAIL: selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
```

So the added case is green on pristine, reds B3, and does not disturb the ledger row's own kill. This
is a proposal for the L1 to route to the instrument's owner (recheck-audit.py is outside this seat's
single-writer paths and outside wave-2 write scope); I did not apply it.

## 6. Verdict

**`weak`.**

- Faithfulness of the row: **holds on every checkable axis.** `find` occurs exactly once, mutated
  bytes differ, `py_compile` passes, pristine run exits 0 and matches the signal, mutant exits 1 and
  breaks the signal, the killing line is exactly the `ghost.md` fixture, and my hand result
  (`live=0/y mutant=1/n killed`) equals the counter's line character-for-character. No defect found
  in the ledger row, the signal, or the counter's handling of this row.
- Why not `holds`: the limb is only half-witnessed. A one-limb mutant of the same limb at the *other*
  conjunct (`named = True`, line 130) survives the row's kill command with exit 0 and a byte-identical
  signal match, and the counter agrees (`survivor`). The limb declares a `named and not missing`
  conjunction; the fixtures only prove the `not missing` half. That is a discriminating gap, not a
  labelling question: §5 gives a one-case strengthening that closes it.

Risks / hand-off notes:
1. Add the `pathless.md` case (or equivalent) to the `recheck-audit.py` selftest by its owner, then
   re-run the C1 counter; RA-paths stays killed and B3 becomes killable. Without it, the ledger's
   claim "the paths conjunction is load-bearing" rests on one conjunct only.
2. `limb-mutation-check.py` bytes moved between wave 1 (`eb9b87ff…`) and this seat (`c660a95f…`);
   the C1 predicate line should be re-measured by the owning wave-2 fixer on final bytes. My hand
   replication is independent of the counter's bytes.
3. `B4` (existence checked against `/`) shows that a broader root-scoping error is caught only by
   collateral fixtures, not by an isolating case; not a defect of this row (it is not the declared
   limb), recorded so the L1 knows the limb set has no root-scoping witness.
