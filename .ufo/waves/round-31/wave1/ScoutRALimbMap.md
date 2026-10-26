# ScoutRALimbMap — C1 limb code map (round 31, wave 1)

Read-only scout. No instrument was edited. Instrument bytes mapped (sha256 at read time, `git status --short corpus/instruments/*.py` clean):

```
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  recheck-audit.py   (444 lines)
33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f  source-recheck.py  (403 lines)
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  frontier-recheck-count.py (228 lines)
```

Line numbers below are for those bytes; if an executor has already edited its file, re-grep the `find` text instead (every `find` below was verified `count == 1` against these bytes).

Method (evidence, not guess): a throwaway python prototype copied `corpus/` into `mktemp -d` scratch lanes, ran the kill command on the unmutated copy, applied find/replace to the scratch instrument, `py_compile`d it, re-ran the kill command. All predictions in the table are those measured results ("measured"), not inferences. Scratch dirs removed after each row; nothing written in the lane tree except this file.

Kill command for RA and SR rows: `python3 {inst} --selftest` (live_exit 0). FR has NO selftest and no fixture today — see FR section.

## Table

| # | limb id | implementing lines | `find` (exact once) | `replace` (compiles) | existing case that should catch it | measured today |
|---|---|---|---|---|---|---|
| 1 | RA-parse | recheck-audit.py:101-102 `parse_ok`; used :121 | `capture_output=True).returncode == 0` | `capture_output=True).returncode >= 0` | selftest case `parseonly.md` (:226; prose after a valid command, parse must fail; paths+cwd still pass so only parse can fail it). NOT `prose.md` — it is also killed by `paths` so it cannot isolate parse | **killed** (live 0, mutant 1) |
| 2 | RA-cwd | recheck-audit.py:122-128; verdict :125 (:128 is the TimeoutExpired branch, unreachable by selftest — not part of the limb) | `lane_rc == foreign_rc and lane_digest == foreign_digest` | `True` | selftest `cwd.md` (:213; relative path works from lane root, fails from `/`) | **killed** |
| 3 | RA-paths | recheck-audit.py:129-132; verdict :132 | `limbs["paths"] = named and not missing` | `limbs["paths"] = True` | selftest `ghost.md` (:214; names an absent corpus path) | **killed** |
| 4 | RA-cdroot | recheck-audit.py:135-137; verdict :137 | `os.path.abspath(cd_target) == (cdroot or root)` | `True` | selftest `elsewhere.md` (:216; `cd /tmp`, frozen pass, strict must fail) | **killed** |
| 5 | RA-instrument | recheck-audit.py:138-140; verdict :140 | `strict["instrument"] = bool(instruments) or base_test` | `strict["instrument"] = True` | selftest `instonly.md` (:227; own path named, cdroot ok, no instrument) | **killed** |
| 6 | RA-own | recheck-audit.py:141-147; verdict :147 | `strict["own"] = own or sourced or base_state` | `strict["own"] = True` | selftest `selftesty.md` (:218; instrument ok, own file not named). `basetest.md` also catches it | **killed** |
| 7 | RA-completeness | recheck-audit.py:350 `complete = ...`, :352 `ok = ... and complete and strict_passed == total ...` | ` and complete and strict_passed == total` (leading space; once, line 352) | `` (empty string) | **none.** selftest's `completeness` line (:244-254) recomputes its own formula (:248) and never calls `main()`'s expression; the two expect fixtures use complete, strict-clean trees | **SURVIVOR** (live 0, mutant 0) — see Strengthening A |
| 8 | RA-expect-missing | recheck-audit.py:188-194 `expected_mismatch` first return value; consumed :341, :351, :370-371 | `sorted(wanted - actual)` | `[]` | selftest label `expect-missing` (:259, :280-286; rc==1 and `missing_entries==["corpus/knowledge/ghost-absent.md"]`) | **killed** |
| 9 | RA-expect-unexpected | recheck-audit.py:194 second return value; consumed :341, :351, :372-373 | `sorted(actual - wanted)` | `[]` | selftest label `expect-unexpected` (:260, :287-293) | **killed** |
| 10 | SR-stem-mismatch | source-recheck.py:123-126 (B1) | `Path(path).stem != source_id` | `False` | selftest `stem-mismatch` (:342-351; id S901 over capture S900.txt) — mutant yields `S901:sha256 OK` exit 0 | **killed** |
| 11 | SR-occurrence-not-unique | source-recheck.py:186-200 (B2; verdict from `anchor_verdict` :85-114, "missing" at :107); fatal branch :192-198 (message `reason=occurrence-not-unique` at :194) | `anchor_verdict_result != "ok":` | `anchor_verdict_result != "ok" and anchor_verdict_result != "missing":` | selftest `double-occurrence` (:353-358; quote on lines 6 and 10, no anchor, exit 1 + substring) | **killed** (alt mutant `"missing": "reason=occurrence-not-unique"` -> `"missing": "reason=occurrence-unique"` also killed, by `expected_substr`) |
| 12 | FR-missing-entry | frontier-recheck-count.py:64-79 `entry_contract` returns None; :117-130 `evaluate` None branch; :132-134 second path resolution | `    if contract is None:\n` (4-space indent, trailing newline; the docstring mention at :71 has no `if`) | `    if False:\n` | **no selftest/fixture exists in this instrument.** With a fixture root (below) the mutant dies with `TypeError: cannot unpack non-iterable NoneType` — exit stays 1 (same as live), so the kill is by SIGNAL only | killed **given Fixture FR-1**; with no fixture there is no kill command at all (= survivor by the contract's rule) |
| 13 | FR-duplicate-entry | frontier-recheck-count.py:202-214 (realpath set), summary :215 | `if rp in seen_realpath:` | `if False:` | **none** (no selftest). With Fixture FR-2 the mutant flips exit 1 -> 0 | killed **given Fixture FR-2**; else survivor |

## Strengthening A — RA-completeness (ExecRALimbs; the only RA survivor)

Why it survives: `main()` computes `ok = passed == len(entries) and complete and strict_passed == total and expect_ok`. The selftest never reaches that expression with an incomplete or strict-failing tree; it only calls `audit_entry` per case and re-implements completeness inline at :248.

Measured mutants of line 350/352 against three throwaway trees run through `main()` (`--root D --cdroot D`, exit code shown):

```
mutant                 empty tree  missing-line tree  strict-only tree (frozen-pass, strict-fail entry)
live                       1             1                  1
drop ' and complete and strict_passed == total'   0   0   0      <- the limb mutant (row 7)
complete = True            0             1                  1
complete drops 'total > 0' 0             1                  1
drop ' and complete'       0             1                  1
drop ' and strict_passed == total'  1    1                  0
```

Reading: the two conjuncts are each individually redundant for the missing-line case (`strict_passed <= len(entries) <= total`, so `len(entries)==total` is implied by `strict_passed==total` — that half of `complete` is provably equivalent when `strict_passed == total` is kept). Distinct observable behavior:
- `total > 0` is observable only on an EMPTY `corpus/knowledge/` (entries 0 == total 0, strict_passed 0 == total 0).
- `strict_passed == total` is observable on a tree whose entries all pass the frozen limbs but one fails a strict limb (e.g. `cd D && true corpus/target.md` with `corpus/target.md` outside `corpus/knowledge/` so `total` stays equal to `len(entries)`; if the target file sits in `corpus/knowledge/`, `complete` goes False and masks the effect — I hit that bug in my first fixture).
- a recheck-less file is caught by either conjunct.

Smallest set of selftest additions that kills row 7 and both sub-mutants (each runs `main(["--root", T, "--cdroot", T, "--quiet"])`, wants rc==1; scratch tree T like the existing expect fixtures, one `good.md` per `corpus/instruments/tool.py` line `recheck: cd T && python3 corpus/instruments/tool.py corpus/knowledge/good.md`):
1. `complete-missing-line`: good.md + `corpus/knowledge/nol.md` containing `# no recheck`. rc must be 1.
2. `complete-strict-only`: good.md + `deg.md` (`recheck: cd T && true corpus/target.md`) + `T/corpus/target.md`. rc must be 1.
3. `complete-empty`: `T/corpus/knowledge/` with no files. rc must be 1.
Print one line each, e.g. `selftest complete-empty exit=1 want=1 ok`, and key the ledger `signal` on those three lines (use the combination regex or one limb signal per line; any missing line/FAIL makes the mutant fail).
Cleaner alternative: extract the expression to `def audit_ok(...)` used by both `main()` and the existing :248 formula so the selftest line stops being a copy. Either way the new cases must go through the code line the mutant edits.

Ledger entry shape for row 7: `find` = ` and complete and strict_passed == total`, `replace` = `` , `kill` = `python3 {inst} --selftest`, `signal` e.g. `selftest complete-empty\s+exit=1 want=1 ok[\s\S]*selftest complete-strict-only\s+exit=1 want=1 ok`.

## FR fixtures (ExecFRLimbs) — prototyped and measured

The instrument takes `--root DIR` and needs only `DIR/corpus/README.md` with a Frontier row `| F01 | title | admitted | knowledge/<entry> |` (FRONTIER_ROW :45) plus, for duplicates, the entry file and manifest.

**Scope trap (important): do NOT park fixture trees as `.md` files under `corpus/instruments/limb-fixtures/fr/**`.** `resolve.py:collect` (:303-313) `os.walk`s all of `corpus/` and reads every `*.md`, so a nested `corpus/README.md` + `knowledge/*.md` would enter the citation-survival census scope (`citation-survival.md/.tsv`, round-18 census of record) and change its counts. Existing convention for fixtures in this directory is a `.json` file (`mirror-containment-fixtures.json`, `resolve-dispatch-fixtures.json`) with trees generated at run time. Two safe options: (a) the kill command builds the tree in `$(mktemp -d)` (prototyped below, nothing stored); (b) store fixture bodies as `*.txt`/`*.in` under `limb-fixtures/fr/` and have the kill command `cp` them to `README.md` inside a mktemp dir.

Fixture FR-1 (row 12) — kill command prototype (placeholders `{inst}`; works verbatim):
```
D=$(mktemp -d) && mkdir -p "$D/corpus/knowledge" && printf '%s\n' '| F01 | ghost row | admitted | knowledge/ghost-absent.md |' > "$D/corpus/README.md" && python3 {inst} --root "$D"; rc=$?; rm -rf "$D"; exit $rc
```
live: exit 1, output
```
FAIL     F01  knowledge/ghost-absent.md                            ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
```
`live_exit` 1, `signal` `FAIL\s+F01\s+knowledge/ghost-absent\.md\s.*problems=missing-entry`. Mutant `if False:` -> exit 1 + `TypeError ... NoneType` traceback, signal no match -> killed (measured). Second one-limb mutant, `find` `"problems": ["missing-entry"],` `replace` `"problems": [],`, also killed by the same signal (exit 1 both; row prints without `problems=`).

Fixture FR-2 (row 13) — passing duplicate rows so the mutant flips the exit code (a failing-entry fixture would keep exit 1 and rely on the signal alone):
```
D=$(mktemp -d) && mkdir -p "$D/corpus/knowledge" && printf '%s\n' '| F01 | row one | admitted | knowledge/e.md |' '| F02 | row two | admitted | knowledge/e.md |' > "$D/corpus/README.md" && printf '%s\n' '{"schema_version":1,"sources":[{"id":"S900"}]}' > "$D/corpus/m.json" && printf '%s\n' '# e' 'source: S900' 'recheck: python3 -c 0 source-recheck.py --manifest corpus/m.json --source S900' > "$D/corpus/knowledge/e.md" && python3 {inst} --root "$D"; rc=$?; rm -rf "$D"; exit $rc
```
live: exit 1, output
```
PASS     F01  knowledge/e.md                                       ids=S900           exit=0
PASS     F02  knowledge/e.md                                       ids=S900           exit=0
DUPLICATE-ENTRY F01,F02 knowledge/e.md
entries=2 pass=2 exit=1
```
`signal` `DUPLICATE-ENTRY F01,F02 knowledge/e\.md`, `live_exit` 1. Mutant `if False:` -> `entries=2 pass=2 exit=0` (exit 0 != 1) -> killed (measured). Caveat: the recheck line `python3 -c 0 source-recheck.py ...` satisfies the harness' invocation test (`"source-recheck.py" in recheck`, :141) without calling the real instrument — it is a fixture for the duplicate-realpath limb only, not evidence about recheck behavior. If ExecFRLimbs prefers a real invocation, point the line at a copy of source-recheck.py inside the mktemp root (needs a `S900.txt` capture + manifest with sha256).

Note on `live_exit`: FR rows legitimately have `live_exit` 1 (fail-closed is the live behavior being protected); the counter's rule "exit != live_exit or signal mismatch" handles that.

## Counter-author notes (ExecCounter reads this too)

- Every `find` above was counted exactly once in the unmutated bytes. A near-miss: `complete = len(entries) == total and total > 0` occurs TWICE (:248 with 8-space indent, :350 with 4) because the 4-space form is a substring of the 8-space form — anchor it with a leading `\n` or choose the row-7 find above.
- `py_compile` should write its `cfile` into scratch (all rows compiled in my prototype; none needed a `__pycache__` in the lane). Skip `__pycache__` when copying `corpus/`.
- Keep `{inst}` absolute: the SR selftest resolves `Path(__file__)` and re-invokes itself; the RA selftest calls its own `main()`; both therefore exercise the mutated bytes.
- Regex signals: `%-13s` / `want=%-5s` padding in RA selftest lines means `True ` has a trailing space — use `\s+`. In JSON ledger every `\` is doubled.
- `.` in `re.search` does not cross newlines unless DOTALL; multi-line signals need `[\s\S]*`.
- SR `SELFTEST <case> PASS` lines are the clean per-case signal; the RA ones read `selftest <name> ... ok`.

## Raw measurement log (prototype, scratch dirs, deleted)

```
RA-parse             count 1 comp True live 0 True mut 1 False killed
RA-cwd               count 1 comp True live 0 True mut 1 False killed
RA-paths             count 1 comp True live 0 True mut 1 False killed
RA-cdroot            count 1 comp True live 0 True mut 1 False killed
RA-instrument        count 1 comp True live 0 True mut 1 False killed
RA-own               count 1 comp True live 0 True mut 1 False killed
RA-completeness      count 1 comp True live 0 True mut 0 True survivor
RA-expect-missing    count 1 comp True live 0 True mut 1 False killed
RA-expect-unexpected count 1 comp True live 0 True mut 1 False killed
SR-stem-mismatch     count 1 comp True live 0 True mut 1 False killed
SR-occurrence-not-unique count 1 comp True live 0 True mut 1 False killed
FR-missing-entry     count 1 live 1 True mut 1 False killed   (given Fixture FR-1)
FR-duplicate-entry   count 1 live 1 True mut 0 False killed   (given Fixture FR-2)
```
(columns: id, `find` occurrences, mutant compiles, live exit + signal match, mutant exit + signal match, verdict.)

Summary for the ledger: 10 of 13 limbs are killed by existing selftest cases with the `find`/`replace` above; RA-completeness is a real survivor needing selftest additions in recheck-audit.py; FR-missing-entry and FR-duplicate-entry have no existing case and are killed only once ExecFRLimbs lands a fixture-backed kill command (prototypes above). No limb is provably equivalent as a whole; one SUB-clause (`len(entries) == total` inside `complete`) is provably redundant given `strict_passed == total` and must not be used as a limb mutant.
