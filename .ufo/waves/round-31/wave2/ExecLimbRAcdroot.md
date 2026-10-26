# ExecLimbRAcdroot — falsification of ledger limb `RA-cdroot` (C1, strict limb (d))

Round 31, wave 2, lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze `738a77999a00efbca129cfccb28a481037f6241f`.
Seat: ExecLimbRAcdroot (leaf; no dispatch, no background job, no subagent).
Answering model actually used: `opencode-go/deepseek-v4.1-flash` (route table decided; no model flag passed by me).
Lane writes by this seat: this receipt only. Every experiment ran in a `mktemp -d` copy of `corpus/`; the lane's `corpus/instruments/*` bytes were never edited (`git status --porcelain corpus/instruments/` empty before and after; hashes below).

Subject bytes (read-only, `sha256sum`, recorded before and after all runs, identical):

```
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
```

## Verdict

**`weak`** — the row itself holds exactly (hand re-derivation reproduces the counter line bit-for-bit, the mutant is killed by a case specific to this limb, and the mutant run still prints every other line), but the limb's discrimination is **shape-narrow**: the instrument's 17 selftest cases kill only the "ignore the cd target entirely" mutant shape. Three other non-equivalent one-limb mutants of the same limb — including one in the *documented* `--root <scratch> --cdroot <lane>` invocation mode — **survive** with byte-identical output. No defect against the frozen C1 contract (which asks only that the row be killed); the gap is in `recheck-audit.py`'s fixtures, which is not this seat's write scope. Details and the two fixtures that would close it are in §4.

## 1. Ledger row as landed (`limb-ledger.json`, single occurrence)

```json
{"id":"RA-cdroot","instrument":"corpus/instruments/recheck-audit.py",
 "find":"os.path.abspath(cd_target) == (cdroot or root)","replace":"True",
 "kill":"python3 {inst} --selftest","live_exit":0,
 "signal":"(?m)^selftest elsewhere\\.md .*\\bok$",
 "note":"strict limb (d) cdroot: the 'cd <path> &&' target is no longer compared with the audited root; isolated by elsewhere.md"}
```

Production site (`corpus/instruments/recheck-audit.py:137`):

```python
strict["cdroot"] = True if cd_target is None else os.path.abspath(cd_target) == (cdroot or root)
```

The mutant therefore becomes `strict["cdroot"] = True if cd_target is None else True` (line 137, verified after mutation).

## 2. Step 1 — hand re-derivation on the UNMUTATED copy, then my own mutation

Scratch: `S=$(mktemp -d /tmp/limb-cdroot-XXXXXX)` → `/tmp/limb-cdroot-AwMB6x`; `cp -a corpus "$S/corpus"`; `rm -rf "$S/corpus/instruments/__pycache__"`.
Kill command run as written in the row, cwd = scratch, same environment the counter uses (`PYTHONDONTWRITEBYTECODE=1`):

```
cd /tmp/limb-cdroot-AwMB6x
python3 corpus/instruments/recheck-audit.py --selftest > live.txt 2>&1; echo "LIVE_EXIT=$?"
LIVE_EXIT=0
LIVE_SIGNAL_MATCH= True
LIVE_LINES= 39
FIND_COUNT= 1
```

Find count asserted by hand before mutating: `"os.path.abspath(cd_target) == (cdroot or root)"` occurs **exactly once** in the 483-line instrument.

Mutation applied by python, then compiled, then the same kill command re-run:

```
MUTATED_LINE= ['    strict["cdroot"] = True if cd_target is None else True']
python3 -m py_compile <scratch>/corpus/instruments/recheck-audit.py  -> COMPILE=ok(exit=0)
python3 <scratch>/corpus/instruments/recheck-audit.py --selftest > mutant.txt 2>&1; echo "MUTANT_EXIT=$?"
MUTANT_EXIT=1
MUTANT_SIGNAL_MATCH= False
```

Determinism re-checked in a *second, fresh* scratch (`/tmp/limb-cdroot-live-*`), three live runs and two mutant runs:

```
live_run1 exit=0
live_run2 exit=0
live_run3 exit=0
LIVE_DETERMINISTIC=same(3/3)
py_compile=exit0
mut_run1 exit=1
mut_run2 exit=1
MUTANT_DETERMINISTIC=same(2/2)
v1.txt signal_matches= True  lines= 39 FAIL= 0
m1.txt signal_matches= False lines= 39 FAIL= 1
```

(Recorded self-error: in the first scratch I re-ran the "live" command after the file had already been mutated; `live2.txt` from that directory is a *mutant* run and is excluded. The fresh-scratch triple above is the authoritative determinism evidence.)

### Hand result

| side | exit | signal `(?m)^selftest elsewhere\.md .*\bok$` | verdict |
|---|---|---|---|
| unmutated | 0 | matches | — |
| one-limb mutant | 1 | no match | **killed** |

## 3. Counter's line on the landed bytes — identical

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
counter_exit=0
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

Comparison: counter `live=0/y mutant=1/n verdict=killed` vs hand `exit 0 / signal match` then `exit 1 / no match` → **equal**, no defect. Exit 0 and both frozen summary lines (`limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`) reproduce.

Quiescence (rule 6): the counter was run twice, 18 s of wall time apart, with instrument/ledger/audit hashes identical before and after both runs (`INSTRUMENT_BYTES_STABLE_ACROSS_RUN=yes`) and byte-identical output (`COUNTER_OUTPUT_IDENTICAL_RERUN=yes`). No in-flight comparison is being cited.

## 4. Step 2 — discrimination: a second (third, fourth) one-limb mutant of the SAME limb

Each mutant in its own fresh scratch copy of the whole `corpus/`, `find` count asserted `== 1`, `py_compile` clean, then the row's kill command `python3 corpus/instruments/recheck-audit.py --selftest` (cwd = scratch):

| id | mutation of limb (d) | find count | compile | selftest exit | signal | killed? | changed lines vs live |
|---|---|---|---|---|---|---|---|
| landed `RA-cdroot` | `os.path.abspath(cd_target) == (cdroot or root)` → `True` | 1 | ok | 1 | no | **killed** | 1 |
| M2 cdroot-override-ignored | `(cdroot or root)` → `root` (an explicit `--cdroot` is ignored) | 1 | ok | 0 | yes | **SURVIVOR** | 0 (39 vs 39 lines, byte-identical) |
| M3 cdroot-no-abspath | `os.path.abspath(cd_target) == (cdroot or root)` → `cd_target == (cdroot or root)` (normalization dropped) | 1 | ok | 0 | yes | **SURVIVOR** | 0 |
| M4 cdroot-plumbing (different code site: `main()`, line 367) | `cdroot = os.path.abspath(args.cdroot) if args.cdroot else None` → `cdroot = None` | 1 | ok | 0 | yes | **SURVIVOR** | 0 |
| M5 cdroot-inversion | `... == ...` → `... != ...` | 1 | ok | 1 | no | **killed** | 10 |

```
== M2-cdroot-override-ignored   exit=0 signal_match=True  killed=False  baseline_lines=39 mutant_lines=39 changed_pairs=0
== M3-cdroot-no-abspath         exit=0 signal_match=True  killed=False  baseline_lines=39 mutant_lines=39 changed_pairs=0
== M4-cdroot-plumbing           exit=0 signal_match=True  killed=False  baseline_lines=39 mutant_lines=39 changed_pairs=0
== M5-cdroot-inversion          exit=1 signal_match=False killed=True   changed_pairs=10
```

### The three survivors are NOT equivalent mutants — they are uncovered code

Proven with fixtures that the instrument's own cases never build, driven through `audit_entry`/`main` exactly as production calls them (fixture tree A = audited root, directory B = a *different* cdroot; all commands inert `test -e`):

```
root A = /tmp/fixtureA-7o5e9qft   cdroot B = /tmp/fixtureB-vv54v8zx
== pristine
   ovr.md (cd->B, root=A, cdroot=B):  cdroot=True
   rel.md (cd '.', root=A, cdroot=None): cdroot=True
== M2-cdroot-override-ignored
   ovr.md: cdroot=False          <-- M2 distinguishable
   rel.md: cdroot=True
== M3-cdroot-no-abspath
   ovr.md: cdroot=True
   rel.md: cdroot=False          <-- M3 distinguishable
== M4-cdroot-plumbing (through main(["--root", A, "--cdroot", B, "--json", ...]))
pristine  exit=1  receipt cdroot= /tmp/fixtureB-no35q__f  stdout: strict pass=0/1 cdroot_fail=0 instrument_fail=1 own_fail=1
M4        exit=1  receipt cdroot= /tmp/fixtureA-t07hsuat  stdout: strict pass=0/1 cdroot_fail=1 instrument_fail=1 own_fail=1
                                  <-- M4 distinguishable (cdroot_fail 0→1, receipt cdroot B→A)
```

So the semantic content of limb (d) has three observable sub-behaviours and the selftest covers exactly one of them:

- covered: a cd target that is **not the default root** is rejected (`elsewhere.md`, `cd /tmp`);
- uncovered: an explicit `--cdroot` override that **is** the cd target is accepted (this is the round-26 documented control shape `--root <scratch-tree> --cdroot <lane-root>`, `corpus/lessons/round-26.md:12`, `:109`);
- uncovered: a **relative** cd target is normalized with `abspath` before comparison.

Cause: all 17 selftest cases either pass `cdroot=None` to `audit_entry` (13 per-entry fixtures, lines 224-243) or call `main(["--root", tree, "--cdroot", tree, ...])` with `cdroot == root` (4 tree-level fixtures, lines 274 and 317). No case ever separates `--root` from `--cdroot`, and no case uses a relative cd target.

## 5. Step 3 — isolation: the kill is specific to this limb, not an unrelated crash

Unified diff of the two 39-line runs (landed mutant), whole output:

```
--- v1.txt (live)
+++ m1.txt (mutant)
@@ -3,7 +3,7 @@
 selftest cwd.md        pass want=False got=False | strict want=False got=False ok
 selftest ghost.md      pass want=False got=False | strict want=False got=False ok
 selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
-selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
+selftest elsewhere.md  pass want=True  got=True  | strict want=False got=True  FAIL
 selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
 selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
 selftest sourced.md    pass want=True  got=True  | strict want=True  got=True  ok
```

- Exactly **one** line differs; the other 38 lines are byte-identical, including all 12 other per-entry case lines, the `selftest completeness ... ok` line, the four tree-level fixture lines, and every `main()` summary line (`strict pass=… cdroot_fail=…`, `executes=… gated=… broken=…`, `lines=… total=… pass=…`, `expect=…`). No traceback, no import error, no banner loss: number of output lines is 39 on both sides, ` ok` lines 18 → 17, `FAIL` 0 → 1.
- The flipped case is the one the row names, and `elsewhere.md` isolates this limb: on pristine bytes `audit_entry` returns `limbs = {'parse': True, 'cwd': True, 'paths': True}` (all frozen limbs pass, so `pass=True`) and `strict = {'parse': True, 'cwd': True, 'paths': True, 'cdroot': False, 'instrument': True, 'own': True}` — `cdroot` is the **only** false strict component, with `cd_target = /tmp` vs `root = /tmp/fx-_55hul3w`. So only limb (d) can decide that case.
- M5 (inversion) flips 5 case lines plus 5 summary lines — a *non*-isolating shape, listed only to show the row's chosen mutant is the precise one, not the blunt one.

## 6. Routing note (no write performed — instruments are outside this seat's scope)

To make limb (d) shape-discriminating (kills M2, M3, M4 as well) `recheck-audit.py`'s `selftest()` needs two fixtures; both are cheap and use only the tree it already builds:

1. **override case**: a tree where the recheck line's `cd` target is a *different* directory than `--root`, run as `main(["--root", tree_with_entry, "--cdroot", other_dir, "--json", receipt])`, asserting `cdroot_fail == 0` / `receipt["cdroot"] == other_dir` for a passing entry (kills M2 and M4).
2. **relative case**: an entry whose line is `cd . && …`, audited with `audit_entry(..., root, foreign, None)` while the process cwd is `root`, asserting `strict["cdroot"] is True` (kills M3).

Owner: whoever holds `recheck-audit.py` (not ExecCounterFix — the counter and ledger are correct as landed; the survivor is a *fixture* gap, not a ledger defect). Wave-1 `MutRAExisting.md` tested the broader shape `strict["cdroot"] = True` on the then-29-line selftest; this receipt re-derives the narrower landed shape on the current 39-line selftest, and extends it with the three same-limb survivors that neither wave-1 receipt reports.

## 7. Integrity and cleanup

- `git status --porcelain corpus/instruments/` → empty (both before and after all runs); lane `corpus/` never written. All mutants and scratch trees were `mktemp -d` copies under `/tmp` and were removed, except the fixture/copy trees named above which hold no lane data. No `git`/`jj` mutation was run in the lane (read-only `git status`, `git log`, `sha256sum` only).
- The counter was run in the lane exactly as specified (`--ledger corpus/instruments/limb-ledger.json`, no `--root`) and is scratch-only by construction; it created no lane files (`git status` clean apart from pre-existing wave artefacts owned by other seats).
- Tool installs/upgrades: **none** (python3 stdlib, `sha256sum`, `diff` sufficed).
- Scratch output of the first counter run was staged under `.ufo/waves/round-31/wave2/_limbcdroot/counter-run.txt` while collecting evidence; its full text is reproduced in §3 and the directory has been deleted so wave2 holds only seat receipts.
