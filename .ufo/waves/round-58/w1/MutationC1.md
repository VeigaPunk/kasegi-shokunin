VERDICT: C1's instrument-side kill rule reproduces exactly (pristine `selftest cases=6 failures=0` exit 0; committed battery `mutbat killed=2/2 survivors=0 controls=pass` exit 0; m4/m6 independently killed from extracted bytes) — but the instrument's own `--selftest` kills only 7 of the 15 one-limb mutants this seat built: 8 SURVIVE (ma, mc, md, mf, mh, mj, mk, mm), and 4 of those (ma, mc, md, mj) turn a red or harness-error audit into a green one on a real ledger. The battery's two listed limbs (m4, m6) are reproduced but cover none of the 13 new limbs this seat built; three gate holes (redirect write-through, self-truncation, `..` path traversal) are not expressible as single-limb mutants and are reported as text-only defects.

Seat: MutationC1. Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Implementation under test: 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b (lane HEAD). Scratch root S=/fast/scratch/hyaku/kasegi-r58/MutationC1 (deleted before yield; see E10). Host: Linux x64, python 3.14.8. No tool was installed or upgraded (pacman is host-paused; nothing was needed).

--------------------------------------------------------------------------------
E1. Target bytes are identical in the commit, the lane working tree, and scratch.

Command:
```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
sha256sum $S/pristine.py
git -C <lane> show 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b:corpus/instruments/figure-audit.py | sha256sum
git -C <lane> status --porcelain -- corpus/instruments corpus/knowledge
```
Output (exit 0 each):
```
18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  .../corpus/instruments/figure-audit.py
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  $S/pristine.py
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  -
(empty: no working-tree change under corpus/instruments or corpus/knowledge)
```
So the bytes I mutated are the bytes the committed battery grades (mutbat.py:20-21 resolves INSTR next to itself).

E2. Pristine extraction and baseline (`--selftest`).

Command (step 1):
```
git -C <lane> show 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b:corpus/instruments/figure-audit.py > $S/pristine.py   # exit 0, wc -l = 214
cd $S && TMPDIR=$S python3 pristine.py --selftest; echo EXIT=$?
```
Output (exit 0):
```
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
selftest cases=6 failures=0
EXIT=0
```
Baseline is green: a mutant's nonzero exit is attributable to the mutation, not to a broken baseline.

E3. The committed battery, run as specified (step 4).

Command:
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=$S python3 corpus/instruments/figure-audit-mutbat.py; echo EXIT=$?
```
Output (exit 0):
```
PRISTINE selftest_exit=0 last='selftest cases=6 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=6 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=5 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=6 failures=1'
mutbat killed=2/2 survivors=0 controls=pass
EXIT=0
```
Battery shape, for the coverage statement: it lists exactly two mutants (mutbat.py:23-28) and one control (mutbat.py:29-31); a mutant is killed on returncode alone (mutbat.py:87 `k = 1 if rc != 0 else 0`), and the pristine gate is exit-only (mutbat.py:48-50: `rc, last = selftest_exit(INSTR, tmp)` then `if rc != 0`), so a pristine that prints a false summary still counts as pristine (see mf below).

E4. Fifteen one-limb mutants, each an exact-once edit with a recorded site count.

Builder commands (all exit 0):
```
cd $S && python3 mutate.py     # 11 specs
cd $S && python3 extra.py      # 2 specs
cd $S && python3 replay.py     # 2 committed limbs replayed independently
```
Output (every spec exact-once, every mutant byte-compiles):
```
SITES ma-python-prefix-allow-true sites=1 ... PYCOMPILE ma-... rc=0
SITES mb-compare-prefix-not-whole sites=1 ... PYCOMPILE mb-... rc=0
SITES mc-empty-derive-guard-off sites=1 ... PYCOMPILE mc-... rc=0
SITES md-derive-exit-not-failclosed sites=1 ... PYCOMPILE md-... rc=0
SITES me-cases-pin-raised-7 sites=1 ... PYCOMPILE me-... rc=0
SITES mf-summary-hides-failures sites=1 ... PYCOMPILE mf-... rc=0
SITES mg-allowlist-gains-echo sites=1 ... PYCOMPILE mg-... rc=0
SITES mh-cases-pin-check-off sites=1 ... PYCOMPILE mh-... rc=0
SITES mi-err-branch-counts-ok sites=1 ... PYCOMPILE mi-... rc=0
SITES mj-empty-figures-guard-off sites=1 ... PYCOMPILE mj-... rc=0
SITES mk-redirect-split-inert sites=1 ... PYCOMPILE mk-... rc=0
MUTANTS built=11 specs=11 rc=0
SITES ml-failures-init-removed sites=1 ... PYCOMPILE ml-... rc=0
SITES mm-good-always-true sites=1 ... PYCOMPILE mm-... rc=0
EXTRA built=2 rc=0
SITES ra-committed-m4-drop-stale-literal sites=1 ... PYCOMPILE ra-... rc=0
SITES rb-committed-m6-readonly-gate-off sites=1 ... PYCOMPILE rb-... rc=0
REPLAY built=2 rc=0
```
Mutant sha256 (from `sha256sum ma-*.py ... rb-*.py`):
```
0904d7a49f42f3c257256677eb4542d298c828d2e590e27a80629ca7009a4163  ma-python-prefix-allow-true.py
2d3499eb2f52331833ddffffc1120fef5b946a117e1b667f0d2f881fe8ad97c6  mb-compare-prefix-not-whole.py
a35a8ec965cd11ca8465c883eada49b0c2891345c9f48f55af7ae8f7ad658562  mc-empty-derive-guard-off.py
8fc0b1ee13b3c67fa96fda359db9b912aad682b28ff4cf00125f29e1b4b30280  md-derive-exit-not-failclosed.py
dc0a428d85c8e385b27ef8ed943820b9ff5f7a1a70369b6d611479c04fd23257  me-cases-pin-raised-7.py
c7a061ef2aa1e1bd05b2631c1e3e79cffea6049da0964527439e7740c0195828  mf-summary-hides-failures.py
b940d39a6484d1ec06493daf1c16925086b3f841515c8b9dd00e22e6d227c842  mg-allowlist-gains-echo.py
eece6eed3664f082ab3c08c31f83435a17771cc81a1054a54215ee70b0ab76a9  mh-cases-pin-check-off.py
6585031b4cec2b49982d160579f6f67710a91bdfd679a66a350dfabd6e131cd5  mi-err-branch-counts-ok.py
f06efe3f240b8f2aa58e2fee84751c78723b0d6ff809a15aa71b9646f0043a54  mj-empty-figures-guard-off.py
f6aab577097fc552460be00db74e3a56e57471e8b718aada78be900b149c1cfa  mk-redirect-split-inert.py
1ae987735196697578a575c9e7970a6fd8746693369e1db6648ad660268baaf4  ml-failures-init-removed.py
b7b9435030ff148df8d126e58e3995a953112ae8828fb9c3b4b5f67ae19773c6  mm-good-always-true.py
69f3ceaa64be9c2b4d6f0be7c9c54a85bf69fa6073fc7f6070249ad559c19398  ra-committed-m4-drop-stale-literal.py
42c42c007739ae89cec99f457df1952c41dc2cee4effc22557beb27c080d9681  rb-committed-m6-readonly-gate-off.py
```
Anchor line numbers in the extracted instrument (`grep -nF ... pristine.py`): case block 180-185 (ok-ledger 180, stale-literal 181, derive-fails 182, token 183, unreadable 184, not-read-only 185); pin value 53; pin check 192-194; summary print 195; empty-figures guard 98; fail-closed 71-72; empty guard 73-74; head split 79; python branch 80-83; READ_ONLY_HEADS allow-list 49; comparison 114; err branch 110-111; `failures = 0` 187; grader 175.

E5. Detector: the instrument's own `--selftest`, same command per mutant.

Command (consolidated; one line per mutant, exit code captured from the child):
```
cd $S && export TMPDIR=$S
for m in ma... rb...; do python3 "$m.py" --selftest > last-$m.txt 2>&1; rc=$?; ... done
```
Output (trimmed to the decisive field; each mutant was also run individually as `python3 <id>.py --selftest; echo EXIT=$?`):
```
DETECT ma-python-prefix-allow-true        selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT mb-compare-prefix-not-whole        selftest_exit=1 killed   last=selftest cases=6 failures=1
DETECT mc-empty-derive-guard-off          selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT md-derive-exit-not-failclosed      selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT me-cases-pin-raised-7              selftest_exit=1 killed   last=selftest cases=6 failures=1
DETECT mf-summary-hides-failures          selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT mg-allowlist-gains-echo            selftest_exit=1 killed   last=selftest cases=6 failures=1
DETECT mh-cases-pin-check-off             selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT mi-err-branch-counts-ok            selftest_exit=1 killed   last=selftest cases=6 failures=1
DETECT mj-empty-figures-guard-off         selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT mk-redirect-split-inert            selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT ml-failures-init-removed           selftest_exit=1 killed   last=UnboundLocalError: cannot access local variable 'failures' where it is not associated with a value
DETECT mm-good-always-true                selftest_exit=0 SURVIVES last=selftest cases=6 failures=0
DETECT ra-committed-m4-drop-stale-literal selftest_exit=1 killed   last=selftest cases=5 failures=1
DETECT rb-committed-m6-readonly-gate-off  selftest_exit=1 killed   last=selftest cases=6 failures=1
TALLY killed=7 survived=8 total=15
```
Killed-mutant detail (the case line that decided it, from the per-mutant runs):
```
mb: selftest case=token-boundary-34-vs-340 exit=0 want=1 verdict=fail
me: selftest pin cases=6 expected=7 verdict=fail ; selftest cases=6 failures=1
mg: selftest case=derive-not-read-only-refused exit=0 want=2 verdict=fail
mi: selftest case=derive-fails-fail-closed exit=0 want=1 verdict=fail
ra: selftest case=... (stale-literal dropped) ; selftest pin cases=5 expected=6 verdict=fail ; selftest cases=5 failures=1
rb: selftest case=derive-not-read-only-refused exit=0 want=2 verdict=fail
ml: predicate traceback, NO `selftest cases=` line at all (UnboundLocalError at the summary print, instrument line 195)
```

E5b. Table (mutant | limb and site | sites | py_compile | selftest exit | verdict).

| id | limb (instrument line) | sites | py_compile | selftest exit | verdict |
|---|---|---|---|---|---|
| ma-python-prefix-allow-true | python-prefix branch accepts any `python`/`python3` head (80-83) | 1 | 0 | 0 | **SURVIVES** |
| mb-compare-prefix-not-whole | whole-value equality → prefix test (114) | 1 | 0 | 1 | killed (token case) |
| mc-empty-derive-guard-off | exit-0-but-empty-stdout guard removed (73-74) | 1 | 0 | 0 | **SURVIVES** |
| md-derive-exit-not-failclosed | nonzero derive exit graded from its stdout (71-72) | 1 | 0 | 0 | **SURVIVES** |
| me-cases-pin-raised-7 | EXPECTED_CASES 6→7 (53) | 1 | 0 | 1 | killed (pin) |
| mf-summary-hides-failures | summary prints `failures=0` unconditionally (195) | 1 | 0 | 0 | **SURVIVES** |
| mg-allowlist-gains-echo | allow-list gains `echo ` (49) | 1 | 0 | 1 | killed (not-read-only case) |
| mh-cases-pin-check-off | `len(cases)!=EXPECTED_CASES` check removed (192-194) | 1 | 0 | 0 | **SURVIVES** |
| mi-err-branch-counts-ok | error branch counts `ok += 1` (110-111) | 1 | 0 | 1 | killed (derive-fails case) |
| mj-empty-figures-guard-off | `or not figs` removed (98) | 1 | 0 | 0 | **SURVIVES** |
| mk-redirect-split-inert | redirect split removed from the head (79) | 1 | 0 | 0 | **SURVIVES** (dead-limb probe) |
| ml-failures-init-removed | `failures = 0` removed (187) | 1 | 0 | 1 | killed-by-crash (traceback, not a grade) |
| mm-good-always-true | per-case grader forced True (175) | 1 | 0 | 0 | **SURVIVES** |
| ra-committed-m4-drop-stale-literal | stale-literal case dropped (181) — committed m4 | 1 | 0 | 1 | killed (pin) |
| rb-committed-m6-readonly-gate-off | allow-list branch returns True (84) — committed m6 | 1 | 0 | 1 | killed (not-read-only case) |

E6. Survivor probes: each survivor against a real ledger, pristine vs mutant, same command shape.

Probe fixtures written under $S/probes (`led-*.json`, root `g.txt`="35", `f.txt`="340"):
```
python3 <instrument> --ledger $S/probes/<ledger>.json --root $S/probes/root; echo EXIT=$?
```
(a) md — a derive that exits nonzero while printing the wanted value (`grep -c zzz f.txt` prints 0, exits 1):
```
pristine: FIG p-grep-nonzero recorded=0 derived=UNAVAILABLE reason=derive-exit-1 stale
          FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1                              EXIT=1
md:       FIG p-grep-nonzero recorded=0 derived=0 ok
          FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0                              EXIT=0
```
(b) mc — exit-0 empty stdout (`sed -n '/^zzz$/p' f.txt`, want ""):
```
pristine: FIG p-empty-stdout recorded= derived=UNAVAILABLE reason=derive-empty stale
          FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1                              EXIT=1
mc:       FIG p-empty-stdout recorded= derived= ok
          FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0                              EXIT=0
```
(c) ma — arbitrary python code in a ledger (`python3 -c 'print(35)'`):
```
pristine: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=p-py-arbitrary    EXIT=2
ma:       FIG p-py-arbitrary recorded=35 derived=35 ok
          FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0                              EXIT=0
```
(d) mj — an emptied ledger (`{"figures": []}`):
```
pristine: FIGURE-AUDIT: UNAVAILABLE reason=ledger-shape want=figures-array        EXIT=2
mj:       FIGURE-AUDIT figures=0 ok=0 stale=0 exit=0                              EXIT=0
```
(e) mk — dead limb: the redirect probe ledger (`cat g.txt > written.txt`) gives the identical verdict under pristine and mk (`stale`, exit 1), but the command **wrote** `written.txt` (3 bytes, sha256 90d7ec0f… equals `g.txt`). The `>` split at line 79 never changes a verdict, and the gate never sees the redirect it stripped.

E7. Composition probes (labelled two-limb; NOT counted as mutants). Builders `compose.py` / `compose2.py` printed `sites=1`, `py_compile=0`, `rc=0` for each edit; then `python3 <composed>.py --selftest; echo EXIT=$?`.
```
c1-mh-after-m4  (m4 dropped case + mh pin check removed):
  ... selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
  selftest cases=5 failures=0                                        EXIT=0
c2-mf-after-mb  (mb prefix comparison + mf lying summary):
  selftest case=token-boundary-34-vs-340 exit=0 want=1 verdict=fail
  selftest cases=6 failures=0                                        EXIT=1
c3-mm-after-mb  (mb prefix comparison + mm grader forced True):
  selftest case=token-boundary-34-vs-340 exit=0 want=1 verdict=pass
  selftest cases=6 failures=0                                        EXIT=0
```
c1 shows mh is load-bearing only in combination (with the check present, a dropped case is caught — ra). c2 shows mf makes the last line lie while the exit code stays honest. c3 is the deepest: a broken per-case grader prints `verdict=pass` for a case that returned exit 0 against want 1 and exits 0, so **no** verdict printed by `--selftest` can be trusted if the grader itself is mutated — only an external oracle (the battery) can see it, and the battery's m6 kill would also be masked by mm if both limbs were present.

E8. Gate defects not expressible as single-limb mutants (text only; no claim is edited).

1. Redirect write-through. `check_read_only` strips everything after `>` before matching (instrument line 79), so an allow-listed head with a redirect is accepted **and the redirect executes**:
```
derive "cat g.txt > written.txt"  -> FIG ... derived=UNAVAILABLE reason=derive-empty stale, EXIT=1
                                     ls -l written.txt -> 3 bytes, created by the audit
```
2. Destructive self-truncation. Same gate, `derive "cat copy.txt > copy.txt"`:
```
before: wc -c probes/trunc/copy.txt = 3
after : wc -c probes/trunc/copy.txt = 0
```
The audit truncated a file in its own root while claiming the command is read-only.
3. Prefix test is lexical, not resolved. With the `..` component resolvable, `python3 corpus/instruments/../probes/evil.py` passes the `corpus/instruments/` prefix test and executes a script outside the instruments tree:
```
FIG p-traversal recorded=35 derived=35 ok ; FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0   EXIT=0
```
(NB: the same command exits 2 when `corpus/instruments/` does not exist in the root, because the literal path cannot resolve — the check passes either way; resolution failures are caught only by derive-exit.)

E9. Survivor list and the limb each leaves unguarded.

| survivor | unguarded limb | audit consequence (probe) |
|---|---|---|
| ma | python-prefix allow-list (instrument:80-83) | any `python3 -c …` in a ledger runs and can grade `ok` (E6c) |
| mc | empty-stdout guard (73-74) | exit-0 silent command grades `ok` when want is empty (E6b) |
| md | nonzero-exit fail-closed (71-72) | failed derive that printed the wanted value grades `ok` (E6a); real shape: `grep -c` exits 1 on zero matches but prints 0 |
| mf | summary failure count (195) | last line reports `failures=0` while a case line reads `verdict=fail` (E7 c2) |
| mh | count-pin check (192-194) | pin value is inert; only the pin check's presence matters (E7 c1) |
| mj | non-empty figures guard (98) | `{"figures": []}` reads `figures=0 ok=0 stale=0 exit=0` (E6d) — vacuous green for the lane's counting command |
| mk | redirect split (79) | dead code; removing it changes no verdict, and the gate never rejects redirects (E6e, E8) |
| mm | per-case grader (175) | a real red case prints `verdict=pass`, exit 0 (E7 c3) |

Severity ordering for repair: mm > md > mj > ma > mc > mf > mh > mk.

Proposed fixtures (text only, for the owner of the instrument; not applied):
1. Case `derive-exit-nonzero-with-want-on-stdout`: ledger `{"derive": "grep -c zzz f1.txt", "want": "0"}`, expect exit 1 and the line containing `reason=derive-exit-1`. Kills md.
2. Case `derive-empty-stdout-exit0`: ledger `{"derive": "sed -n '/^zzz$/p' f1.txt", "want": ""}`, expect exit 1 with `reason=derive-empty`. Kills mc.
3. Case `python-head-outside-instruments-refused`: ledger `{"derive": "python3 -c 'print(35)'", "want": "35"}`, expect exit 2. Kills ma.
4. Case `empty-figures-array-rejected`: ledger `{"figures": []}`, expect exit 2 with `reason=ledger-shape`. Kills mj.
5. Meta case `grader-must-fail-a-red-ledger`: inside `selftest`, run the instrument on a ledger known stale and assert the printed case verdict is `fail` (or assert the summary's `failures` field equals the number of `verdict=fail` lines). Kills mm; this is the only shape that does not depend on the grader it is testing.
6. Battery additions (in `figure-audit-mutbat.py`): append ma, mc, md, mh, mj, mm to `MUTANTS`; require each killed mutant's last line to match `^selftest cases=\d+ failures=[1-9]` so a crash (ml) is not counted as a kill; and assert the PRISTINE last line equals `selftest cases=6 failures=0`, not merely exit 0.
7. Battery control: add a second `must_not_be_killed` control that is a semantically equivalent rewrite (e.g. `code = 1 if stale else 0` → `code = int(stale > 0)`), since the current control (mutbat.py:30-31) only appends trailing whitespace.
8. Gate hardening (defect proposals, not claim changes): reject a derive whose command text contains an unquoted redirect or a `..` path component before the allow-list match; or run the derive under a read-only sandbox. Fixtures: `derive "cat g.txt > written.txt"` → exit 2; `derive "python3 corpus/instruments/../x.py"` → exit 2.

E10. Restoration and lane integrity.

Command:
```
cd $S && git -C <lane> show 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b:corpus/instruments/figure-audit.py > restored.py
sha256sum pristine.py restored.py <lane>/corpus/instruments/figure-audit.py
cmp pristine.py restored.py && echo "RESTORE_CMP=identical exit=$?"
git -C <lane> status --porcelain -- corpus
```
Output:
```
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  pristine.py
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  restored.py
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  <lane>/corpus/instruments/figure-audit.py
RESTORE_CMP=identical exit=0
 M corpus/QUALITY.md
?? corpus/lessons/round-58.md
```
All mutations were applied to scratch copies only; the lane file was never opened for writing (the two `corpus/` status entries above are not this seat's writes — this seat wrote nothing under L except this evidence file). Scratch S was removed with `rm -rf -- $S` before yield; no probe, clone, mutant or temp file is left behind, and TMPDIR was set to S for every run.

E11. Tooling. Installed/upgraded: none (nothing needed; pacman is host-paused and not used). python3 = 3.14.8 (system). The committed battery writes only to its `tempfile.mkdtemp` under TMPDIR and removes it (`mutbat.py:45`, `:97`).
