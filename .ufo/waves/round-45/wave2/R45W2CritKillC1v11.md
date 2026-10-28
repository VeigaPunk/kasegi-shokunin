VERDICT: BROKEN

Seat: R45W2CritKillC1v11. Attacked: C1 counter `corpus/instruments/r45-routed-defects.py` v1.1 at lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4, exported with `git archive` (read-only) to scratch; round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd exported the same way as `--baseline`. Pins checked with sha256sum against the PINS dict: S072.txt 364166c4…a025, freeze-check.py a38d8dc1…5888, r44-frontier-count.py 2409d240…f0d4, r44-routed-defects.py d5438c67…ca7ba90, claims.json bbe40503…c6206 — all match. No git mutation, no install, no shared file touched. Scratch removed on exit.

## Controls (re-run)

- Genuine export, tool=export, root=export, baseline=base:
  `routed-defects total=5 fixed=5 unresolved=0 exit=0`
  (limbs: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`, `limb R2 fixed=1 read=criteria=3`, `limb R3 fixed=1 read=selftest-cases=43`, `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`, `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`)
- Do-nothing control, root=base, baseline=base:
  `limb R1 fixed=0 read=row-S072=absent` … `routed-defects total=5 fixed=0 unresolved=5 exit=1`

Every construction below is the genuine export with ONE named edit (fixture trees t1..t9 in scratch). Each prints `fixed=5` for a tree whose routed defect is still present. The tool root is always the genuine export unless stated.

## Findings

F1 R1 (S072 row, `flip:` clause). Attacked: corpus/SOURCES.md row S072, the `flip:` clause, predicate counter line 158 `re.search(r"flip:\s*\S", teaches)`. Edit: `flip: a fresh article-API capture states a program-specific scope or boundary rule that the program's linked rules page does not state` replaced by `flip: tbd`.
  Command: `python3 <export>/corpus/instruments/r45-routed-defects.py --root t1 --baseline base`
  Printed: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`
  Defect present: spot-check §6 item 1 requires "Replace the vacuous flip condition with a checkable one". This is wave-1's own falsification (`flip: tbd`). Erratum E1 says v1.1 binds content; the flip predicate is byte-for-byte the v1 token check, so it was not closed.

F2 R2 (QUALITY R47/R48/R49 criteria). Attacked: corpus/QUALITY.md lines 380-382, counter lines 203-238 (keyword substring, length ≥300, `enforced-by:` path must be a file, one `round-44.md:N` in range). Edit: each criterion cell replaced by a ≥300-char keyword placeholder with `enforced-by: \`README.md\`` (an existing file that enforces nothing) and a grounding line ref.
  Command: `… --root t2 --baseline base`
  Printed: `limb R2 fixed=1 read=criteria=3` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`
  Row printed (line 380): `| R47 | Replay the frozen counter on the do-nothing control BEFORE data is read; … Placeholder: the criterion text carries the class keywords and states no procedure beyond them, so the row is accepted on keywords alone; enforced-by: \`README.md\`. …`
  Defect present: §6 item 2 asks for criteria that name the mistake classes grounded in round-44.md. The predicate reads keywords, length and file existence only; no class content is checked.

F3 R3 (SKILL.md round-45 registry rows; README row). Attacked: SKILL.md appended section, counter lines 255-265 (regex on the name, cell count == 8, empty cells count), and corpus/instruments/README.md, counter lines 266-268 (regex anywhere in file).
  F3a Edit: the three rows (`r44-frontier-count.py`, `r44-routed-defects.py`, `wave-registry.py`) replaced by `| name |  |  |  |  |  |  |  |`. Command `… --root t3 --baseline base`. Printed: `limb R3 fixed=1 read=selftest-cases=43` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`. Rows at t3 SKILL.md lines 1150-1152 print `| r44-frontier-count.py |  |  |  |  |  |  |  |`.
  F3b Edit: genuine README row (line 994) deleted, bare `| r44-frontier-count.py |` appended at file end (t7). Printed: `limb R3 fixed=1 read=selftest-cases=43` … `fixed=5`.
  Defect present: §6 item 3 asks for a registry row describing the probe at its home. Empty cells and a bare line pass.

F4 R4 (freeze-check replay). Attacked: counter lines 272-289 run `freeze-check.py` from the GRADED tree (`fc = root/corpus/instruments/freeze-check.py`), so the pinned script's sys.path[0] is the tree's `corpus/instruments/`. Fixture t4 ships `corpus/instruments/shlex.py`, a shadow that loads the real stdlib shlex and makes `quote()` route any directory containing `corpus/instruments/r45-routed-defects.py` to a tree-local stub printing the two expect_before lines.
  Discriminator (same genuine export, baseline = empty dir `empty/`):
  genuine: `limb R4 fixed=0 read=replay-rc=1`; t4: `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`.
  Full run t4 at genuine base: `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`, total `fixed=5`.
  Defect present: the replay is not a replay: the counter that prints the expect_before line is a tree-supplied stub, so R4 is satisfied by content the tree chose. The pins cover freeze-check.py and claims.json bytes only; imports are not pinned.

F5 R5 (refiled receipt). Attacked: `.ufo/waves/round-44/controls/final-attempt3-refiled.txt`, counter lines 292-318. The body pin covers only lines between the single invocation line and the first `exit=0`; the only other check is "no line starting `usage:` and no line containing `error:`". Edit (t5): prepend `$ python3 corpus/instruments/r44-routed-defects.py --selftest` and `exit=2` (the failed bare call, usage text omitted).
  Command: `… --root t5 --baseline base`
  Printed: `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged` … `fixed=5`.
  File head printed: `$ python3 corpus/instruments/r44-routed-defects.py --selftest` / `exit=2`.
  Defect present: §6 item 5 asks to re-file "without the failed call"; the failed bare call is still listed.

F6 All-limb forged tree (tall = F1 + F2 + F3a + F4 shadow + F5 together; tool = genuine export, baseline = genuine base).
  Printed:
  `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`
  `limb R2 fixed=1 read=criteria=3`
  `limb R3 fixed=1 read=selftest-cases=43`
  `limb R4 fixed=1 read=selftest-cases=20 replay=base_ok=2`
  `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`
  `routed-defects total=5 fixed=5 unresolved=0 exit=0`
  Items 1-5 are all still present in this tree (F1-F5). The counter cannot distinguish it from the genuine tree.

F7 TOOL_ROOT trust (source-recheck.py is not pinned; counter line 171 runs it from TOOL_ROOT). Fixture t6: `corpus/instruments/source-recheck.py` replaced by a stub printing `S072:sha256 OK`, `S072:Q1 OK`, `S072:Q2 OK`, exit 0; manifest S072 gains an unlocated quote Q9 ("this sentence is not in the captured snapshot at all anywhere").
  Control, genuine tool root (export): `limb R1 fixed=0 read=recheck-rc=1-quotes=2` … `routed-defects total=5 fixed=4 unresolved=1 exit=1` (the unlocated quote is caught).
  Tree-run, `python3 t6/corpus/instruments/r45-routed-defects.py --root t6 --baseline base`: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`.
  The graded command template uses `{tool}`, so the grader is safe; any seat or CI step that runs the counter from inside the tree is not.

F8 R1 lesson correction wording. Attacked: corpus/lessons/round-44.md line 205 (the `Correction (round 45` line), counter lines 186-192 (prefix `Correction (round 45`, contains `S072`, contains `10029`, one straight-quoted span ≥30 chars and ≥6 words located in S072). Edit (t8): the whole line replaced by a correction asserting the opposite ("S070 stands as rejected; … does not change the reason, which still reads "Welcome to the VRP rules section! Here, you'll find an overview of the different…" as the reject ground") with those tokens and that located quote kept.
  Printed: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1` … `fixed=5`.
  The genuine line 205 says the reverse. The counter binds tokens and one quote, not the claim.

F9 Pins can be switched off from the environment. Attacked: counter lines 75-77 `if os.environ.get("R45_PINS_OVERRIDE"): PINS.update(json…)`. The docstring says "selftests only", the code does not enforce it. Fixture t9: `r44-frontier-count.py` replaced by `print("selftest cases=8 failures=0")`; override JSON pins that file to the stub's sha.
  Without env: `limb R3 fixed=0 read=r44-frontier-count-not-the-pinned-bytes` (`fixed=4`).
  With `R45_PINS_OVERRIDE=<json>`: `limb R3 fixed=1 read=selftest-cases=8` … `routed-defects total=5 fixed=5 unresolved=0 exit=0`.
  Environment-dependent; a grader shell that inherited the variable from a selftest run would accept this.

F10 Re-entrancy / hang when baseline contains the counter stack (robustness, grader hazard). `timeout 20 python3 <export>/corpus/instruments/r45-routed-defects.py --root <export> --baseline <export>` → exit=124, no output in 20 s; the same run with the base tree completes in 2.2 s. Mechanism (from code, [INFERENCE] for the exact recursion depth): the R4 replay runs the counter at `{tree}`=baseline; when that tree contains the counter, the nested counter re-enters R4. A background run of the same command was cancelled at 300 s (bg_20770).

F11 Registry rows point at self-tests that do not exist (SKILL.md, genuine tree, not caught by any limb). SKILL.md r45-routed-defects.py row: "run `corpus/instruments/r45-counters-selftest-c1.py` with --selftest"; r45-c2-gate.py row: "run `corpus/instruments/r45-counters-selftest-c2.py`". `ls exp/corpus/instruments/r45-counters-selftest-c1.py` → `No such file or directory`; the c2 file is absent from the instruments listing too. R3 checks only the three r44/wave-registry names.

## Controls file

Controls file `.ufo/waves/round-45/controls/freeze-controls.txt` records `control c1-marker-only … fixed=0 … got=RED`. No marker-only tree is committed and I did not reproduce it. The recorded controls do not cover F1-F9: those trees are richer than a marker-only tree and grade fixed=5.

## Reading against the frozen kill rule

The three literal kill conditions are not met by the genuine tree: it prints fixed=5, and the recorded controls are RED. The "after" claim is still falsified in substance: "5 of those 5 are resolved … as read by the committed counter" is not what fixed=5 measures. F1-F6 print fixed=5 with items 1-5 present.

Smallest candidate corrections (errata, predicate-preserving per the rule): F1 require a non-vacuous flip (a located reference to S069 Q5 or a checkable path); F2 require the enforced-by target to contain the grading logic, not any file; F3 require eight non-empty cells and rows outside fences; F4 run every subprocess with `python3 -I` (or `-P`) so the tree's directory is never on sys.path, and pin the imports; F5 forbid any line naming the bare `--selftest` call; F7 pin source-recheck.py and the manifest; F8 bind the correction to the S072 teaches text; F9 drop the env override; F10 refuse a baseline that contains the counter. F11 make the registry-row targets existence-checked.

## Limitations

- Each construction is one edit to the genuine export in scratch; the constructions are my own and were run once in this session; the printed lines above are the exact output.
- Kill-rule clause 3 (predicate change after scoring) was not tested.
- C2 and the wave-1 falsification files were not re-read beyond what the counter reads.
- The recorded control outputs in freeze-controls.txt were not regenerated.
- No marker-only tree was built; F1-F6 are stronger than marker-only, so they falsify the predicate set but not the recorded control.
- Baseline=export (F10) was observed to hang, but the recursion depth was not instrumented.
