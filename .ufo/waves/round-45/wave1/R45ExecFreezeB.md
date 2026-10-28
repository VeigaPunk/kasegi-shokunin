VERDICT: DRAFT-READY

Seat R45ExecFreezeB, C1/R4 builder B. Draft only; nothing installed into corpus/instruments, nothing committed.

Draft: .ufo/waves/round-45/wave1/R45ExecFreezeB.draft/freeze-check.py (stdlib-only, python 3.14.8, executable bit set).
CLI: `--claims PATH --tool-root DIR --base DIR [--work DIR] [--timeout S]` and `--selftest [--work DIR] [--base DIR]`.
Tools installed/updated: none.

## Behavior
- Renders counter_cmd with {tool}=tool-root, {tree}={base}=base (each shell-quoted), runs `bash -c` in tool-root, stdout+stderr merged, child env R45_FREEZE_CHECK=1 and an explicit TMPDIR (the --work dir if given, else inherited TMPDIR), timeout 300 s (process group killed on timeout).
- Claim is `ok` only when: counter_cmd/expect_before/expect_after all present and non-blank; some output line, stripped, EQUALS expect_before (whole line, literal, not regex); no output line contains expect_after; expect_before != expect_after; counter_cmd mentions {tree} or {base}; id unique; the base tree is unchanged after the counter ran (relative path + size + mtime_ns snapshot). A nonzero counter exit is not a failure by itself.
- File-level: schema must be kasegi-round-claims-v2, claims list non-empty.
- Prints `claim <id> base_read=<matched line or last output line> verdict=ok|FAIL`, then `finding <id> <FINDING-ID> <detail>` lines under a FAIL, then `freeze-check claims=<n> base_ok=<k> exit=0|1`. Exit 0 only if n>0, k==n and no file-level finding.
- Finding ids: FC-SCHEMA FC-NO-CLAIMS FC-DUP-ID FC-MISSING-FIELD FC-BEFORE-EQ-AFTER FC-NO-TREE FC-NO-MATCH FC-AFTER-AT-BASE FC-TIMEOUT FC-BASE-MUTATED.
- Selftest fixtures: isolated subdir freeze-check-selftest-XXXX in --work (default mkdtemp under TMPDIR), removed at exit. The real base README comes from --base, else /fast/scratch/hyaku/kasegi-r45/L1/pure, else `git show dc5bb8c6...:corpus/README.md` (read-only). Only that one file is copied into the fixture.

## Run 1 - selftest (re-run by me): `python3 freeze-check.py --selftest --work $S/w` with TMPDIR set, exit 0
```
case 1-good-claim-red-counter-exit1 PASS exit want=0 got=0 ids want=[] got=[] verdict=ok | claim C base_read=T fixed=0 exit=1 verdict=ok
case 2-round44-frozen-grep-real-readme PASS exit want=1 got=1 ids want=['FC-NO-MATCH'] got=['FC-NO-MATCH'] table-aware admitted=26, frozen grep read 0 (readme /fast/scratch/hyaku/kasegi-r45/L1/pure/corpus/README.md) | claim C base_read=0 verdict=FAIL
case 3-do-nothing-green-only-after-line PASS exit want=1 got=1 ids want=['FC-AFTER-AT-BASE', 'FC-NO-MATCH'] got=['FC-AFTER-AT-BASE', 'FC-NO-MATCH'] | claim C base_read=T fixed=1 exit=0 verdict=FAIL
case 3b-after-line-present-beside-before-line PASS exit want=1 got=1 ids want=['FC-AFTER-AT-BASE'] got=['FC-AFTER-AT-BASE'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 4-missing-expect_before PASS exit want=1 got=1 ids want=['FC-MISSING-FIELD'] got=['FC-MISSING-FIELD'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 4b-empty-expect_before PASS exit want=1 got=1 ids want=['FC-MISSING-FIELD'] got=['FC-MISSING-FIELD'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 4c-missing-expect_after PASS exit want=1 got=1 ids want=['FC-MISSING-FIELD'] got=['FC-MISSING-FIELD'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 4d-missing-counter_cmd PASS exit want=1 got=1 ids want=['FC-MISSING-FIELD'] got=['FC-MISSING-FIELD'] | claim C base_read=n/a verdict=FAIL
case 5-counter-crash-no-matching-line PASS exit want=1 got=1 ids want=['FC-NO-MATCH'] got=['FC-NO-MATCH'] base_read=last line | claim C base_read=RuntimeError: boom verdict=FAIL
case 6-substring-suffix-fixed=0x PASS exit want=1 got=1 ids want=['FC-NO-MATCH'] got=['FC-NO-MATCH'] | claim C base_read=fixed=0x verdict=FAIL
case 6b-substring-prefix-xfixed=0 PASS exit want=1 got=1 ids want=['FC-NO-MATCH'] got=['FC-NO-MATCH'] | claim C base_read=xfixed=0 verdict=FAIL
case 7-before-equals-after PASS exit want=1 got=1 ids want=['FC-AFTER-AT-BASE', 'FC-BEFORE-EQ-AFTER'] got=['FC-AFTER-AT-BASE', 'FC-BEFORE-EQ-AFTER'] | claim C base_read=T 0 verdict=FAIL
case 8-counter-timeout PASS exit want=1 got=1 ids want=['FC-TIMEOUT'] got=['FC-TIMEOUT'] | claim C base_read=<no-output> verdict=FAIL
case 9-duplicate-claim-id PASS exit want=1 got=1 ids want=['FC-DUP-ID'] got=['FC-DUP-ID'] | claim C1 base_read=T fixed=0 exit=1 verdict=ok // claim C1 base_read=T fixed=0 exit=1 verdict=FAIL
case 10-counter-reads-no-tree-placeholder PASS exit want=1 got=1 ids want=['FC-NO-TREE'] got=['FC-NO-TREE'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 11-wrong-schema PASS exit want=1 got=1 ids want=['FC-SCHEMA'] got=['FC-SCHEMA'] | claim C base_read=T fixed=0 exit=1 verdict=ok
case 11b-no-claims PASS exit want=1 got=1 ids want=['FC-NO-CLAIMS'] got=['FC-NO-CLAIMS'] | 
case 12-counter-mutates-base PASS exit want=1 got=1 ids want=['FC-BASE-MUTATED'] got=['FC-BASE-MUTATED'] | claim C base_read=T fixed=0 exit=1 verdict=FAIL
case 13-env-tmpdir-cwd-contract PASS exit want=0 got=0 ids want=[] got=[] | claim C base_read=env=1 tmp=<work>/freeze-check-selftest-<rand>/tmp cwd=<tool-root>... (path elided here; printed in full by the tool)
case 14-mixed-ok-and-fail PASS exit want=1 got=1 ids want=['FC-NO-MATCH'] got=['FC-NO-MATCH'] claims=2 base_ok=1 | claim A base_read=T fixed=0 exit=1 verdict=ok // claim B base_read=nope verdict=FAIL
selftest cases=20 failures=0
```
(case 13 line paths abbreviated in this report only; the random fixture dir suffix differs per run.) Case 2 is the round-44 defect: the real base README holds 26 admitted rows by table-aware count (not 25: the round-44 lesson's 25 is the pre-F26 count; the pure base is post-F26), the frozen `grep -cE '^\| F[0-9]+ \| admitted \|'` read 0 (exit 1, grep -c with no matches), expect_before=26 -> FAIL FC-NO-MATCH.

## Run 2 - the real claims file (read-only), exit 0
Command: `python3 .../R45ExecFreezeB.draft/freeze-check.py --claims /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-45/claims.json --tool-root /home/vgpnk/Projects/shokunin/kasegi-shokunin --base /fast/scratch/hyaku/kasegi-r45/L1/pure`
```
claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok
claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok
freeze-check claims=2 base_ok=2 exit=0
```
(rc=0 printed by my wrapper.)

## Discrimination (do-nothing / mutation controls, all re-run by me)
- Control: empty base dir with the real claims -> `claim C2 base_read=c2-gate fixed=0/7 exit=1 verdict=FAIL`, `finding C2 FC-NO-MATCH ...`, `freeze-check claims=2 base_ok=1 exit=1`. (C1 still reads ok on an empty tree: r45-routed-defects.py prints fixed=0 there too, a counter property, see limitations.)
- Mutant 1, substring match instead of whole-line: selftest `cases=20 failures=2` (cases 6, 6b FAIL: `got=0 ... base_read=fixed=0x verdict=ok`).
- Mutant 2, after-check removed: `failures=3` (cases 3, 3b, 7 FAIL).
- Mutant 3, nonzero counter exit counted as failure: `failures=1` (case 1 FAIL `got=1 ids ... got=['FC-NO-MATCH']`).
So the selftest is not vacuous: each core rule is held by at least one case that goes red when the rule is removed.
- `--selftest --base /nonexistent` falls back to `git show` of the frozen base README: `selftest cases=20 failures=0`.

## Limitations
- A base-only replay cannot catch a counter that is wrong in the round-44 way but reads the same at base as claimed (e.g. expect_before `0` for the broken grep, expect_after `26`): it would print ok. It catches only claim/counter mismatch at the base; reaching expect_after is the R44 controls' job.
- expect_before is a literal whole-line string, not a regex; an expect_before copied with different internal whitespace than the counter prints FAILs (intended, strict).
- expect_after is checked as a substring of any output line (stricter than whole-line, so a line like `... fixed=5 exit=0 extra` at base still FAILs).
- FC-BASE-MUTATED uses size+mtime_ns, so a counter that rewrites identical bytes and resets mtime is not seen; large bases would slow the double snapshot (the pure export is small: whole run ~2 s).
- FC-NO-TREE heuristic: a counter that reaches the base via an absolute path rather than {tree}/{base} is flagged.
- Replay is single-run: nondeterministic counters are not detected. Counter commands run via bash with shell=True semantics: claims are trusted data from the L1 freeze.
- --work in check mode is used only as the children's TMPDIR (not cleaned by the tool).
- Selftest case 2 depends on the real base README being obtainable (--base / pure export / git show of the frozen rev inside the repo containing the script); otherwise it reports `real base README not found` and counts a failure.
- Scratch dir /fast/scratch/hyaku/kasegi-r45/R45ExecFreezeB removed on exit (trap). No git/jj mutation, no labrat spawned.
