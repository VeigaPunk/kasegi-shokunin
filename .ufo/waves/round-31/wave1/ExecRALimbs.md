# ExecRALimbs — C1 recheck-audit limbs (round 31, wave 1)

Seat: ExecRALimbs (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base
`b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze `738a77999a00efbca129cfccb28a481037f6241f`).
Owned paths written: `corpus/instruments/recheck-audit.py` and
`.ufo/waves/round-31/wave1/ledger-fragments/ra.json` (plus this receipt). Nothing else in the
lane, nothing outside it, no git/jj mutation (read-only `git show`/`git diff` only).
Answering model actually run on: `devin/deepseek-v4-1-flash` (harness-reported route; no model
was passed anywhere). Tooling: none installed or upgraded this wave (no pacman, no uv/npx need).

Instrument bytes: before `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`
(444 lines) → after `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`
(483 lines), measured:

```
$ sha256sum corpus/instruments/recheck-audit.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
$ wc -l corpus/instruments/recheck-audit.py
483 corpus/instruments/recheck-audit.py
```

## 1. PRE-STATE label (bounds 6, M30-3)

`corpus/instruments/limb-mutation-check.py` and `corpus/instruments/limb-ledger.json` are owned by
ExecCounter / ExecLedgerMerge and did not exist at seat start
(`ls corpus/instruments/` then: no `limb-mutation-check.py`; both landed at 23:39–23:40Z, §4a runs them). **Every number in §4 is
PRE-STATE with respect to the merged ledger** at seat start: it is a hand-run replica of the
counter semantics stated in the L1 interface contract (fresh `mkdtemp`, `cp -r corpus`, live kill
run → exit+signal, exact-once find/replace on the scratch instrument, `py_compile`, second kill run).

The counter landed mid-seat (2026-10-25T23:39–23:40Z) and §4a re-runs the rows through it, so the
§4 replica numbers are superseded by counter output for the same rows; the replica stays in the
receipt because it is the only measurement that predates the counter bytes. §4a's merged-ledger run
is a snapshot: ExecLedgerMerge still owns that file, so treat it as in-flight (bounds 6) until the
L1 freezes the wave.

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```

## 2. What changed in the instrument (diff)

Only `selftest()` changed; `main()`, `audit_entry()`, `collect()`, `expected_mismatch()`, the
regexes and every exit rule are untouched. `git diff -- corpus/instruments/recheck-audit.py`:

```diff
@@ -226,9 +226,6 @@ def selftest():
             "instonly.md": ("recheck: cd %s && ls corpus/knowledge/instonly.md corpus/knowledge/target.md" % tmp, True, False),
         }
-        for name, (line, _, _) in cases.items():
-            with open(os.path.join(tmp, "corpus/knowledge", name), "w") as handle:
-                handle.write("# fixture\n\n" + line + "\n")
         for name, (line, want_pass, want_strict) in cases.items():
             with open(os.path.join(tmp, "corpus/knowledge", name), "w") as handle:
                 handle.write("# fixture\n\n" + line + "\n")
@@ -297,9 +294,51 @@ def selftest():
                 "selftest %-15s exit=%d want=1 missing=%s unexpected=%s %s"
                 % (label, rc, receipt["missing_entries"], receipt["unexpected_entries"], "ok" if ok else "FAIL")
             )
-        # 13 per-entry fixtures + 2 tree-level expected-list fixtures (completeness
-        # is an auxiliary sanity line above, not counted as a case)
-        total_cases = len(cases) + 2
+        # completeness through main(): the exit rule's own `complete` conjunct must red
+        # an empty knowledge dir (total == 0) and a dir carrying a recheck-less file
+        # (lines < total). The auxiliary line above recomputes its own formula, so it
+        # cannot catch a `complete` verdict that main() never consumes.
+        for label, extra, want_lines, want_total in (
+            ("complete-empty", (), 0, 0),
+            ("complete-missing-line", ("nol.md",), 1, 2),
+        ):
+            tree = os.path.join(tmp, label)
+            os.makedirs(os.path.join(tree, "corpus/knowledge"))
+            os.makedirs(os.path.join(tree, "corpus/instruments"))
+            open(os.path.join(tree, "corpus/instruments/tool.py"), "w").close()
+            if extra:
+                line = "recheck: cd %s && python3 corpus/instruments/tool.py corpus/knowledge/good.md" % tree
+                with open(os.path.join(tree, "corpus/knowledge/good.md"), "w") as handle:
+                    handle.write("# fixture\n\n" + line + "\n")
+                for name in extra:
+                    with open(os.path.join(tree, "corpus/knowledge", name), "w") as handle:
+                        handle.write("# no recheck\n")
+            receipt_path = os.path.join(tree, "receipt.json")
+            rc = main(["--root", tree, "--cdroot", tree, "--quiet", "--json", receipt_path])
+            with open(receipt_path, encoding="utf-8") as handle:
+                receipt = json.load(handle)
+            ok = (
+                rc == 1
+                and receipt["complete"] is False
+                and receipt["lines"] == want_lines
+                and receipt["total_knowledge_files"] == want_total
+            )
+            if not ok:
+                failures += 1
+            print(
+                "selftest %-21s exit=%d want=1 lines=%d/%d complete=%s %s"
+                % (
+                    label,
+                    rc,
+                    receipt["lines"],
+                    receipt["total_knowledge_files"],
+                    receipt["complete"],
+                    "ok" if ok else "FAIL",
+                )
+            )
+        # 13 per-entry fixtures + 4 tree-level main() fixtures (2 expected-list, 2
+        # completeness; the completeness sanity line above is not counted as a case)
+        total_cases = len(cases) + 4
         return 1 if failures else 0
```

The deleted hunk is a byte-for-byte duplicate of the write loop that follows it (both wrote
`"# fixture\n\n" + line + "\n"` for every case). Removing it is the only non-fixture change; §6
proves the selftest stdout is additions-only.

## 3. The 13 fixtures kept, and what the new cases are

All 13 per-entry fixture lines (`good.md` … `instonly.md`) and both expected-list case lines print
byte-identically to the pre-edit bytes (§6 diff: additions only). The two added cases are
tree-level and call `main()` — the same path `main()` uses on the live lane — so the exit rule is
exercised, not re-implemented:

| new case | tree | asserts |
|---|---|---|
| `complete-empty` | `corpus/knowledge/` with no files | `rc == 1`, `receipt.complete is False`, `lines=0/0` |
| `complete-missing-line` | `good.md` (valid recheck line) + `nol.md` (`# no recheck`) | `rc == 1`, `receipt.complete is False`, `lines=1/2` |

Why both: `main()`'s `complete = len(entries) == total and total > 0` has two conjuncts and only one
of them is observable alone. `strict_passed <= len(entries) <= total`, so `strict_passed == total`
(kept in the same `ok` expression) already implies `len(entries) == total` — a deleted recheck line
reds the audit whether or not `complete` is consumed. The `total > 0` half is observable only on an
empty knowledge dir, and that is the case where the mutant flips the *exit code* (1 → 0). The
missing-line case is the one that flips the *receipt field* (`complete` False → True), which is the
documented purpose of the rule ("a deleted recheck line therefore fails the audit instead of
silently shrinking the set", `corpus/instruments/recheck-audit.py:41-42`). Neither case fails under
any of the other eight limb mutants (§4 FAIL-line lists: no `complete-*` line appears).

## 4. Per-limb verdicts (hand-run replica of the counter semantics, pre-counter)

Every row: `find` occurs exactly once in the landed bytes, the mutated file compiles, the mutated
bytes differ from the original, the unmutated kill run exits `live_exit` and matches the row's
signal, and the mutant run differs (exit or signal). Kill for all nine rows is
`python3 {inst} --selftest` with `live_exit 0`.

| limb | find count | live exit | mutant exit | verdict | isolating fixture (the only case that decides it) |
|---|---|---|---|---|---|
| RA-parse | 1 | 0 | 1 | killed | `parseonly.md` |
| RA-cwd | 1 | 0 | 1 | killed | `cwd.md` |
| RA-paths | 1 | 0 | 1 | killed | `ghost.md` |
| RA-cdroot | 1 | 0 | 1 | killed | `elsewhere.md` |
| RA-instrument | 1 | 0 | 1 | killed | `instonly.md` |
| RA-own | 1 | 0 | 1 | killed | `selftesty.md` |
| RA-completeness | 1 | 0 | 1 | killed | `complete-empty` + `complete-missing-line` (added this round) |
| RA-expect-missing | 1 | 0 | 1 | killed | `expect-missing` |
| RA-expect-unexpected | 1 | 0 | 1 | killed | `expect-unexpected` |

Mutant patches (each applied to a fresh scratch copy of the landed bytes; `find` → `replace`):

```
RA-parse               capture_output=True).returncode == 0                      -> capture_output=True).returncode >= 0
RA-cwd                 lane_rc == foreign_rc and lane_digest == foreign_digest    -> True
RA-paths               limbs["paths"] = named and not missing                    -> limbs["paths"] = True
RA-cdroot              os.path.abspath(cd_target) == (cdroot or root)            -> True
RA-instrument          strict["instrument"] = bool(instruments) or base_test     -> strict["instrument"] = True
RA-own                 strict["own"] = own or sourced or base_state              -> strict["own"] = True
RA-completeness        complete = len(entries) == total and total > 0            -> complete = True   (with the following
                       (two-line find including the `expect_ok = ...` line)         `expect_ok = ...` line kept verbatim)
RA-expect-missing      sorted(wanted - actual)                                   -> []
RA-expect-unexpected   sorted(actual - wanted)                                   -> []
```

The two-line find for RA-completeness is required for uniqueness: the bare line
`complete = len(entries) == total and total > 0` also matches the selftest oracle at 8-space indent
(`recheck-audit.py:245`), so the 4-space production line is found only together with the following
`expect_ok` line (`:389-390`).

Kill evidence — the `FAIL` line(s) each mutant prints (verbatim; every other line of every mutant run
stayed `ok`):

```
RA-parse               selftest parseonly.md  pass want=False got=True  | strict want=False got=True  FAIL
RA-cwd                 selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL
RA-paths               selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
RA-cdroot              selftest elsewhere.md  pass want=True  got=True  | strict want=False got=True  FAIL
RA-instrument          selftest ownonly.md    pass want=True  got=True  | strict want=False got=True  FAIL
                       selftest instonly.md   pass want=True  got=True  | strict want=False got=True  FAIL
RA-own                 selftest selftesty.md  pass want=True  got=True  | strict want=False got=True  FAIL
                       selftest basetest.md   pass want=True  got=True  | strict want=False got=True  FAIL
RA-completeness        selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL
                       selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL
RA-expect-missing      selftest expect-missing  exit=0 want=1 missing=[] unexpected=[] FAIL
RA-expect-unexpected   selftest expect-unexpected exit=0 want=1 missing=[] unexpected=[] FAIL
```

RA-instrument also reds `ownonly.md` and RA-own also reds `basetest.md`; the ledger signals are keyed
on the isolating case (`instonly.md`, `selftesty.md`), which is the one fixture whose verdict depends
on that limb alone.

Ledger signals (as written in `ra.json`, each verified to match the unmutated run and to stop
matching under its mutant):

```
RA-parse              (?m)^selftest parseonly\.md .*\bok$
RA-cwd                (?m)^selftest cwd\.md .*\bok$
RA-paths              (?m)^selftest ghost\.md .*\bok$
RA-cdroot             (?m)^selftest elsewhere\.md .*\bok$
RA-instrument         (?m)^selftest instonly\.md .*\bok$
RA-own                (?m)^selftest selftesty\.md .*\bok$
RA-completeness       (?m)^selftest complete-empty\s+exit=1 want=1 lines=0/0 complete=False ok$[\s\S]*^selftest complete-missing-line\s+exit=1 want=1 lines=1/2 complete=False ok$
RA-expect-missing     (?m)^selftest expect-missing .*\bok$
RA-expect-unexpected  (?m)^selftest expect-unexpected .*\bok$
```

## 4a. The real counter on the same rows (counter bytes `eb9b87ff…`)

Counter: `corpus/instruments/limb-mutation-check.py` sha256
`eb9b87ff7fe97d70e93a29c0d36a8e6c23480837085a1da5c4a14665c439e6b8` (ExecCounter's, not mine).
First, my 9 rows alone in a temp ledger outside the lane
(`/tmp/ra-mut/ra-only-ledger.json`, `{"version":1,"limbs":[9],"controls":[]}`), 2026-10-25T23:41Z:

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger /tmp/ra-mut/ra-only-ledger.json; echo "counter_exit=$?"
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
limbs=9 killed=9 survivors=0
controls=0 rejected=0
counter_exit=0
```

Second, the merged fleet ledger as it stood at 2026-10-25T23:41Z
(`corpus/instruments/limb-ledger.json` sha256
`83aecf3fd3d566045462a713e6e83d35631763ef900038ff1419353ec1288077`, 13 limbs + 3 controls) — my 9
rows are in it unchanged and the C1 predicate lines are printed:

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

This is a snapshot of a file ExecLedgerMerge still owns (bounds 6: in-flight, non-comparative until
the L1 freezes the wave). It is recorded because it is the only measurement in this receipt that is
the real counter's own output rather than my replica.

## 5. The one survivor and the strengthening that kills it

**Pre-fix bytes (`3fc0d751…`, extracted with `git show HEAD:corpus/instruments/recheck-audit.py`).**
RA-completeness was a real survivor: the mutant compiled, the find occurred once, the selftest
exited 0, and the mutant's stdout was **byte-identical** to pristine.

```
$ cd /tmp/ra-mut/pre && sha256sum recheck-audit.py
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  recheck-audit.py
$ python3 recheck-audit.py --selftest > pristine.txt 2>&1; echo "pristine_exit=$?"
pristine_exit=0
$ python3 -m py_compile mutant.py && echo "compiles=yes"; python3 mutant.py --selftest > mutant.txt 2>&1; echo "pre_fix_mutant_exit=$?"
compiles=yes
pre_fix_mutant_exit=0
$ diff pristine.txt mutant.txt && echo "OUTPUT_IDENTICAL_TO_PRISTINE=yes"
OUTPUT_IDENTICAL_TO_PRISTINE=yes
```

That is the survivor, and it is not a labelling question: the limb had no failing fixture, so the
strengthening (not a relabel) is the work. The selftest's existing `completeness` line recomputes its
own formula inline (`recheck-audit.py:245`) and never reaches `main()`'s `complete`, and both
expected-list trees are complete and strict-clean, so `complete` was masked.

**Post-fix bytes (`5d4842da…`).** Same mutant, fresh scratch copy, same find/replace:

```
$ python3 corpus/instruments/recheck-audit.py --selftest; echo "post_fix_mutant_exit=$?"
...
selftest complete-empty        exit=0 want=1 lines=0/0 complete=True FAIL
selftest complete-missing-line exit=1 want=1 lines=1/2 complete=True FAIL
post_fix_mutant_exit=1
$ grep -c 'selftest complete-.*FAIL' post-mutant.txt
2
```

Red on the mutant (exit 0 → 1, two FAIL lines, no other case moved), green on the real bytes (§6).
Both new cases are load-bearing under the chosen mutant: `complete-empty` flips the exit code,
`complete-missing-line` flips the receipt's `complete` field.

**Contract-semantics run of the final fragment** (fresh `mkdtemp` per row, live baseline first,
then patch+compile+rerun), which is the exact sequence the counter is specified to perform:

```
rows=9 ids=RA-parse,RA-cwd,RA-paths,RA-cdroot,RA-instrument,RA-own,RA-completeness,RA-expect-missing,RA-expect-unexpected
RA-parse live_baseline=ok
RA-cwd live_baseline=ok
RA-paths live_baseline=ok
RA-cdroot live_baseline=ok
RA-instrument live_baseline=ok
RA-own live_baseline=ok
RA-completeness live_baseline=ok
RA-expect-missing live_baseline=ok
RA-expect-unexpected live_baseline=ok
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
limbs=9 killed=9 survivors=0 invalid=0
```

## 6. No-harm evidence

**(a) Selftest: additions only.** Pristine (`3fc0d751…`) vs landed (`5d4842da…`) `--selftest`
stdout, `diff pristine.txt selftest-after.txt` — 10 added lines, zero changed or removed, so the
deleted duplicate write loop and the new cases leave every existing fixture line intact:

```
29a30,39
> strict pass=0/0 cdroot_fail=0 instrument_fail=0 own_fail=0
> executes=0 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
> lines=0 total=0 pass=0 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
> expect=absent expected=0 missing=0 unexpected=0 exit=1
> selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok
> strict pass=1/2 cdroot_fail=0 instrument_fail=0 own_fail=0
> executes=1 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
> lines=1 total=2 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
> expect=absent expected=0 missing=0 unexpected=0 exit=1
> selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
```

**(b) Live selftest green on the landed bytes** (`selftest_exit=0`), isolating lines:

```
$ python3 corpus/instruments/recheck-audit.py --selftest; echo "selftest_exit=$?"
selftest cwd.md        pass want=False got=False | strict want=False got=False ok
selftest ghost.md      pass want=False got=False | strict want=False got=False ok
selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
selftest complete-empty        exit=1 want=1 lines=0/0 complete=False ok
selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok
selftest_exit=0
```

**(c) Live lane audit at my landing: unchanged, 43/43 exit 0.** Measured immediately after the edit,
before the C2 entry landed:

```
$ python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
audit_exit=0
```

**(d) A/B neutrality on identical quiescent corpus bytes.** Two scratch copies of `corpus/` with the
in-flight C2 entry removed; copy B's instrument replaced by the HEAD bytes; both audited with
`--root <copy> --cdroot <lane>` (the documented scratch mode). Summaries identical, both exit 0:

```
=== A: landed instrument (5d4842da6103)
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
exit=0
=== B: HEAD instrument (3fc0d751f2a5)
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
exit=0
=== summary diff A vs B (expect none)
IDENTICAL
```

**(e) Mid-flight state at receipt time, cause pinned (bounds 6).** A sibling seat landed
`corpus/knowledge/vendor-third-party-finding-coordination.md` (C2's F15 entry) while this seat was
writing; the live audit is therefore red *for that reason only*:

```
$ git status --porcelain corpus/knowledge/
?? corpus/knowledge/vendor-third-party-finding-coordination.md
$ python3 corpus/instruments/recheck-audit.py 2>/dev/null | grep -E '^(unexpected|missing)='
unexpected=corpus/knowledge/vendor-third-party-finding-coordination.md
$ tail -3 corpus/instruments/knowledge-expected.txt
corpus/knowledge/vdp-disclosure-packages.md
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

`corpus/instruments/knowledge-expected.txt` (ExecExpectedList's path, not mine) still lists 43 names,
so the live audit reports `total=44 … exit=1`. I did not touch that file. My rows are unaffected by
it: every RA kill command is `--selftest`, which builds its own temporary trees and never reads the
live lane.

## 7. Risks, limits, notes

- **Signal/format coupling.** Each RA signal keys on a selftest case line. A later reformat of those
  `print` statements makes the row `invalid:live-baseline` (loud, exit non-zero), not silently
  passing; the ledger row must then be re-derived with the new bytes.
- **RA-completeness find is two lines by necessity** (§4). A merge that re-sorts or de-duplicates
  rows must keep the `expect_ok` continuation, or the find count becomes 2 and the row goes
  `invalid:find-count`.
- **`len(entries) == total` is not independently observable** while `strict_passed == total` stays in
  the same `ok` expression; the note in `ra.json` states the proof rather than claiming a second
  kill. This is recorded as a measured redundancy, not hidden.
- **No limb was relabelled.** Eight rows were already killed by existing fixtures; the ninth was a
  proven survivor and the fixtures in §3 are the fix.
- Hand-run scratch dirs lived under `mktemp -d` and `/tmp/ra-mut/` (outside the lane) and were
  removed; nothing was written into `corpus/` except the instrument itself.

## 8. Handoff

Written and final:

- `corpus/instruments/recheck-audit.py` — sha256 `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`
- `.ufo/waves/round-31/wave1/ledger-fragments/ra.json` — `{"limbs":[9 rows]}`, 9/9 killed by the real
  counter (§4a), ExecLedgerMerge notified by id with the merge caution about the two-line find.

State at hand-off (2026-10-25T23:41Z, in-flight): the merged `limb-ledger.json` carries all 13 limbs
and prints `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` / exit 0; the live audit is red
only because `knowledge-expected.txt` still lists 43 while the tree holds 44 (C2's entry landed,
ExecExpectedList owns the list).

Checks the main agent should run after the wave is quiescent (not run by me):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/recheck-audit.py --selftest; echo "selftest_exit=$?"          # 0
python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"               # 0 once ExecExpectedList lists 44
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```
