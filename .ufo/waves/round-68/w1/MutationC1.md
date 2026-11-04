# MutationC1 — round 68 w1: mutation test of the C1 repair's selftest coverage

**Verdict: VERIFIED. `killed=5/5 survivors=none equivalents=E1,E2 (both pass) invalid=X1`.** Every assigned one-limb mutant of the committed gate turns `--selftest` red and names the cases you would expect. Both equivalent controls stay green, and the syntax-error mutant is classed invalid, not killed. Two coverage residuals are below (section 4). They do not change the verdict. I made no edits to the lane gate, the counter or `claims.json`.

## 1. Subject and detector
- Gate: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 82b3b7d4704e914eb224e7bb24e57aa9cbd8603f:corpus/instruments/figure-audit.py`. Its sha256 is `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8`, which matches the claimed C1 gate pin and the lane working-tree file.
- M4 source bytes come from the base gate at `.ufo/waves/round-68/controls/base-gate-d0f48405.py`, sha256 `8147350c…7ad247`. The battery extracts the block from that file; it is not retyped.
- Detector: `python3 -B <mutant> --selftest`, with `TMPDIR`/`HYAKU_SCRATCH`/cwd set to `/fast/scratch/hyaku/kasegi-r68/MutationC1/tmp`. Python version is 3.14.8.
- Every mutant is also checked first with `ast.parse`. A mutant that fails to parse is INVALID. A mutant whose run prints no `selftest cases=` line is INCONCLUSIVE, never killed and never passed; this guard was added after run 1 (section 3).
- Battery: `MutationC1/battery.py` (sha256 `ac4f5edf9c37bc8a26a907b35ee0989000d950472d965fc33515dff61935c1fe`).
- Command: `cd /fast/scratch/hyaku/kasegi-r68/MutationC1 && python3 -B battery.py`. Wall time was 32 s.

## 2. Results (run 2, `MutationC1/battery.out`)
```
ANCHOR M4 cand_block=... sha=2b27751ec541d718adfd411d7349aa713a30fea0960e5ca6d240fa3402bc871a count_in_pristine=1
ANCHOR M4 base_block=b'DENIED_FLAGS = (\n    ("sort", ("-o", "--output")),\n    ("git show", ("--output", "--ext-diff")),\n)\n' sha=b8cc1d5496fdce307d381db5d6f8029166884bac13b4b7ee37e714677468d94a count_in_base=1
P0 pristine sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 parse=0 exit=0 ['selftest cases=77 failures=0'] failed=[]
M1 [drop --compress-program from sort] anchors=[1] sha256=2b84dd5803039624bd6a879b34e6b401531e443e7eeedf29b07a05820c49fd4d parse=0 exit=1 ['selftest cases=77 failures=3'] failed=['sort-compress-program-refused', 'sort-compress-program-space-refused', 'sort-compress-program-quoted-refused'] verdict=KILLED
M2 [drop --textconv from git show] anchors=[1] sha256=ba66183193d0c1c0993c93b967e9fd8ef7b954e76c674e5263e5e6cd41e6f099 parse=0 exit=1 ['selftest cases=77 failures=1'] failed=['git-show-textconv-refused'] verdict=KILLED
M3 [drop both] anchors=[1, 1] sha256=67dbb55667e55296407411f139120ffa24c0218d302b16b6073ded79fdc2f7c5 parse=0 exit=1 ['selftest cases=77 failures=4'] failed=[the 3 sort-compress cases + 'git-show-textconv-refused'] verdict=KILLED
M4 [restore pre-repair DENIED_FLAGS block byte-for-byte (base d0f48405)] anchors=[1] sha256=75d579d31c0dcd7f09afd79f3dea982246ae294969866acc2a8665325022a967 parse=0 exit=1 ['selftest cases=77 failures=4'] failed=[the 3 sort-compress cases + 'git-show-textconv-refused'] verdict=KILLED
M5 [weaken match to tok == flag] anchors=[1] sha256=f24007a468ed82953cd1bd9fe91e9d8f73455fbd396770a9ddf06c4714437338 parse=0 exit=1 ['selftest cases=77 failures=4'] failed=['git-show-output-flag-refused', 'git-quoted-output-refused', 'sort-compress-program-refused', 'sort-compress-program-quoted-refused'] verdict=KILLED
E1 [EQUIVALENT: comment-only edit] anchors=[1] sha256=854bc1e43aa5681ad49f51c670e57f72ec346dff1823ba9db0e1d22cca62c4f3 parse=0 exit=0 ['selftest cases=77 failures=0'] verdict=EQUIVALENT-PASS
E2 [EQUIVALENT: trailing whitespace on EXPECTED_CASES line] anchors=[1] sha256=affc7305cb9188a72de872e5c5e90a90e7264200efd6fe7b1b8b36fa248bfa7b parse=0 exit=0 ['selftest cases=77 failures=0'] verdict=EQUIVALENT-PASS
X1 [INVALID: syntax error in DENIED_FLAGS (unclosed tuple)] anchors=[1] sha256=83599b0b59be6fb6a5ce2a032f461c80091c198ab049f545d1db0315d1bb45ab parse=1 exit=1 ["SyntaxError: '(' was never closed"] verdict=INVALID
RESTORE committed-gate sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 pristine-copy sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 match=True
SUMMARY killed=5/5 survivors=none equivalents=E1:EQUIVALENT-PASS,E2:EQUIVALENT-PASS invalid=X1
```
- **Anchor uniqueness:** every edit anchor occurred exactly once (`anchors=[1]`; M3 is `[1, 1]`).
- **Size of each edit**, counted as `diff mutants/P0.py <m>` changed lines: M1, M2, M5, E1, E2 and X1 each change 2 lines; M3 changes 4. M4 changes 8: the 2 tuple lines change and the 4-line R68 comment is removed, so the file goes from 693 to 689 lines. The resulting block is byte-identical to the base block (sha `b8cc1d54…`). Unified diffs are kept as `MutationC1/<id>.diff`.
- **Why each mutant died.** These are the failing-case lines from `M*.selftest.out`, aggregated over all mutants:
  ```
  4 selftest case=sort-compress-program-refused exit=0 want=2 verdict=fail
  4 selftest case=sort-compress-program-quoted-refused exit=0 want=2 verdict=fail
  3 selftest case=sort-compress-program-space-refused exit=0 want=2 verdict=fail
  3 selftest case=git-show-textconv-refused exit=1 want=2 verdict=fail reasons=derive-exit-128
  1 selftest case=git-show-output-flag-refused exit=1 want=2 verdict=fail reasons=derive-exit-128
  1 selftest case=git-quoted-output-refused exit=1 want=2 verdict=fail reasons=derive-exit-128
  ```
- **The pin check never fired.** No mutant printed a `selftest pin` line, because no mutant removed a case. Every kill came from case verdicts.
- **M5 coverage:** M5 dies only on the `=`-spelling cases. Two older round-60 cases also catch it (`git-show-output-flag-refused`, `git-quoted-output-refused`). The space spelling (`sort-compress-program-space-refused`) and the bare `git show --textconv` stay green under M5, which is correct: exact-token match still refuses them.

## 3. Battery defect in run 1 (recorded, superseded)
Run 1 (`battery-run1.py` sha `be113b0c…bd17b`, output `battery-run1-defective.out`) reported `killed=4/5 survivors=M4`. **That M4 "survivor" was an artifact of my battery, not a coverage gap.**
- The bug: the anchor regex used `re.S`, so the `(?:# .*\n)*` comment group swallowed everything from `DENIED_FLAGS` to end of file.
- The result: the M4 file was truncated to 92 lines (sha `afba3d11…3ebce0`). It had no `main`, so `--selftest` exited 0 and printed nothing.
- The fix in run 2: the anchors are line-bounded (no `re.S`), and the no-summary INCONCLUSIVE guard was added.

The general point: a bare exit-code detector would have counted a silent truncated module as a "surviving" mutant, and in the equivalent role as a pass. Mutation batteries in this lane should require the `selftest cases=` line.

## 4. Coverage residuals (findings for L1; none defeats C1)
1. **The sort cases kill by refusal-exit difference, not by detecting execution.** When `--compress-program` is admitted (M1/M3/M4/M5), `sort --compress-program=/bin/false … g.txt` exits 0 with the right answer `35`. The 3-byte fixture never makes sort spill to a temp file, so `/bin/false` is never invoked. The case fails only because it wants 2 and gets 0. It therefore pins "refused at parse time", but the selftest alone does not show that the program would run. Observed execution (marker runs 18288) lives in the frozen counter's `sort-compress-refused` / `no-write-side-effect` measurements, not here.
2. **The textconv case passes or fails for an incidental reason.** When `--textconv` is admitted (M2/M3/M4), the case reads `derive-exit-128`: the selftest tmp root is not a git repository, so `git show HEAD` fails. No textconv driver is configured or run. The kill is sound (want 2, got 1), but if the fixture ever became a git repo the admitted case would still be red only because of the exit-code difference. Driver execution is covered by the counter's `git-textconv-refused` marker, not the selftest.

Neither residual changes `killed=5/5`. The selftest proves parse-time refusal; proof that the refused programs are actually not executed rests on the frozen counter. That matches the C1 predicate as frozen. I did not run the counter itself; it was outside this seat's assignment.

## 5. Restoration and bounds
- **Restoration:** the committed gate re-exported at the end of the run has sha256 `10c87100…74fee8`, the same as the pristine copy (`match=True`). The lane working-tree gate is also `10c87100…74fee8`, and the counter is `785e38fd…6b4b`; I re-ran `sha256sum` on both after the battery and both are unchanged.
- **Bounds:** all mutants lived only in `/fast/scratch/hyaku/kasegi-r68/MutationC1/mutants/`. I ran no mutating git or jj commands, built no fixture repos, started no subagents or background jobs, and installed no tools.
- **Receipts:** `MutationC1/` holds `battery.py`, `battery.out`, the run 1 script and output, `<id>.diff`, `<id>.selftest.out` for P0, M1–M5, E1, E2 and X1, and `SHA256SUMS`. The scratch directory is removed after the receipts are copied.
