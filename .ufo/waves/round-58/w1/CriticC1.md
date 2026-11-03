SURVIVES — C1 holds at 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b: every counting command reproduces the frozen `after`, m4/m6 are killed for exactly the claimed reasons, the case-substitution attack against the count pin is caught by the committed battery, and the non-equivalent-control attack is caught by battery grading. Two caveats recorded as observations, neither green-lighting a defect inside the frozen rules: (a) the EXPECTED_CASES pin is count-only — a case substitution reads green on the selftest limb alone and is caught only by the battery limb; (b) the d53-1 red control is record-anchored, not commit-anchored — a one-line edit to the r53 receipt literal flips it to ok, and only the kill_rule file-set clause (receipt not in the tolerated set) prevents that. Smallest safe corrections in OBS-1/OBS-2.

Adversarial review of claim C1 (claims.json:11-31, frozen 543cac1) at implementation 18ddb054. Lane L read-only; all mutations in scratch S=/fast/scratch/hyaku/kasegi-r58/CriticC1 (clone via `git clone --shared`, toplevel verified, HEAD 18ddb054, status clean). No tool installs or upgrades were performed (python 3.14.8 + git present; RULES.md read). Scratch deleted before yield; no leftovers.

## A. Frozen after-state reproduction (all five counting commands)

1. Pristine selftest.
   Command: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=/fast/scratch/hyaku/kasegi-r58/CriticC1 python3 corpus/instruments/figure-audit.py --selftest`
   Output: six case lines, all `verdict=pass` — `ok-ledger exit=0`, `stale-literal exit=1`, `derive-fails-fail-closed exit=1`, `token-boundary-34-vs-340 exit=1`, `unreadable-ledger-exit-2 exit=2`, `derive-not-read-only-refused exit=2` — last line `selftest cases=6 failures=0`. EXIT=0.
   Matches claims.json:17 limb 1 and kill_rule clauses 1 and 7 (all five prior case exit codes 0,1,1,1,2 unchanged; figure-audit.py:180-185).

2. Mutant battery.
   Command: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=/fast/scratch/hyaku/kasegi-r58/CriticC1 python3 corpus/instruments/figure-audit-mutbat.py`
   Output: `PRISTINE selftest_exit=0 last='selftest cases=6 failures=0'`; `CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held`; `MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=5 failures=1'`; `MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=6 failures=1'`; `mutbat killed=2/2 survivors=0 controls=pass`. EXIT=0.
   Matches claims.json:17 limb 2 exactly (mutbat.py:23-32, exact-once guard :53, py_compile guard :78-84, kill grading :87).

3. Red fixture.
   Command: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json | grep d53-1` → `FIG d53-1-trailer recorded=34 derived=33 want=34 stale`, pipe exit 0.
   Unpiped exit check: same command without the pipe → `FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1`, EXIT=1. Matches claims.json:17 limb 3 (derived=33, not UNAVAILABLE, not 34, exits 1). Critic note: the pinned counting command pipes to grep, which masks the audit's exit; the kill_rule's "or exits 0" clause is only checkable unpiped — done here.

4. Ledger audit: `python3 corpus/instruments/figure-audit.py` → 35 `ok` lines ending `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, EXIT=0. Matches claims.json:17 limb 4.
5. Entry count: `grep -c '"id"' corpus/instruments/figure-audit-ledger.json` → 35. Matches claims.json:17 limb 5.

## B. Attack 1 — count-pin substitution (add a case, drop a case, count stays 6)

Named edit: in figure-audit.py replace line 185 `run_case("derive-not-read-only-refused", 2, SELFTEST_LEDGER_NOT_RO)` with `run_case("ok-ledger-again", 0, SELFTEST_LEDGER_OK)` (scratch copy S/attackA/figure-audit.py; the only m6-killing case removed, replaced by a duplicate pass-through).
Result, command `TMPDIR=$S python3 figure-audit.py --selftest` in S/attackA: all six case lines pass (`ok-ledger-again exit=0 want=0 pass`), last line `selftest cases=6 failures=0`, EXIT=0. The selftest limb of the kill_rule is SATISFIED while m6 limb coverage is gone — the pin at figure-audit.py:192 (`len(cases) != EXPECTED_CASES`) is a count check, not an identity check.
Same tree, battery: `TMPDIR=$S python3 figure-audit-mutbat.py` → `MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=0 killed=0 last='selftest cases=6 failures=0'`, `mutbat killed=1/2 survivors=1 controls=pass`, EXIT=1. The battery DETECTS the substitution (m6 survives because its only killer was dropped). Verdict: SURVIVES as a composite — the frozen after-state does not read green (counting command 2 fails) — but the selftest limb alone is falsifiable by substitution; the defense rests on the battery limb, and mutbat.py itself is inside the kill_rule's tolerated file set (see OBS-3).

## C. Attack 2 — m6 kill-reason attribution

Command: py_compile + `TMPDIR=$S python3 S/attackB/figure-audit.py --selftest` where attackB is the committed instrument with figure-audit.py:84 `return head.startswith(READ_ONLY_HEADS)` → `return True` (the battery's own m6 patch, mutbat.py:26-27).
Output: `selftest case=derive-not-read-only-refused exit=0 want=2 verdict=fail` — the ONLY failing case; the five prior cases all pass; `selftest cases=6 failures=1`, EXIT=1, py_compile OK.
So m6 is killed precisely because the non-allow-listed head (`echo 35`, SELFTEST_LEDGER_NOT_RO at figure-audit.py:147-151) is no longer refused with exit 2 — the reason the frozen sentence (claims.json:15) names, and no other reason. Cross-check m4 (attackB4, stale-literal run_case line deleted): `selftest pin cases=5 expected=6 verdict=fail`, `selftest cases=5 failures=1`, EXIT=1 — killed by the count pin, exactly as claimed. Verdict: attribution CORRECT for both mutants.

## D. Attack 3 — red fixture receipt-edit attack

Fixture: scratch layout S/attackC with a copy of .ufo/waves/round-53/controls/c2-counter-final-r53.txt and a copy of red-d53-ledger.json; same derive string (red-d53-ledger.json:9: `grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2`), run with `--root S/attackC`.
Pre-edit: `FIG d53-1-trailer recorded=34 derived=33 want=34 stale`, EXIT=1 (receipt line 8 holds `FAIL_entry_records=33`; the receipt has exactly one FAIL_entry_records occurrence, so `head -1` is not masking a second value).
One-line edit: receipt line 8 `FAIL_entry_records=33` → `FAIL_entry_records=34`. Post-edit run: `FIG d53-1-trailer recorded=34 derived=34 ok` — the red control flips to ok.
Verdict: the control is real on a clean tree (derived=33 vs want=34, discriminating filed-vs-derived) but it is RECORD-anchored: the derive greps the live working-tree file; the d53-1 entry carries no `rev` key (verified: grep '"rev"' over red-d53-ledger.json → none), so committed-byte anchoring (the instrument's own optional rev mechanism, figure-audit.py docstring) is not used. The edit path is blocked only because c2-counter-final-r53.txt is NOT in the kill_rule's tolerated file set (claims.json:18) — any such edit trips the changed-file clause. SURVIVES inside the frozen rules; OBS-2 records the correction.

## E. Attack 4 — battery miss / control misclassification

Equivalent-vs-not, concrete runs in scratch:
1. Committed control is genuinely equivalent: patch is `return head.startswith(READ_ONLY_HEADS)` → same + two trailing spaces (mutbat.py:30-31); trailing whitespace after a return statement is semantically inert; battery prints `must_not_be_killed=held`, selftest output identical to pristine (item A.2).
2. Non-equivalent patch called a control — caught: scratch battery S/attackD2 with an added control `("c-non-eq-gate-true", "return head.startswith(READ_ONLY_HEADS)", "return True")` → `CONTROL c-non-eq-gate-true selftest_exit=1 must_not_be_killed=KILLED`, `mutbat killed=2/2 survivors=0 controls=fail`, EXIT=1. Output-based grading cannot bless a behaviour-changing control.
   (First D2 attempt crashed FileNotFoundError because I had copied only the battery, not the instrument, into the fixture dir — my fixture error, corrected by copying figure-audit.py beside it; the traceback was not a lane defect.)
3. Missed equivalent-class mutant — real gap, bounded by the claim: scratch mutant `return head.lower().startswith(READ_ONLY_HEADS)` (case-insensitive gate; admits `CAT f1.txt`) — py_compile OK, selftest `cases=6 failures=0` EXIT=0. A py_compile-valid, behaviour-changing patch invisible to the selftest and absent from the battery's two mutants. Verdict: the battery proves only what it lists; the frozen sentence claims exactly m4+m6, so this is not a falsification — recorded as OBS-4.

## F. Attack 5 — weakening of an existing limb

Command: `git -C S/clone diff 1e5c8f2cdc1c9d14672444c6fca0e67414366494 18ddb054... -- corpus/instruments/figure-audit.py` → 13 insertions, 0 deletions: the EXPECTED_CASES constant (:53), SELFTEST_LEDGER_NOT_RO (:147-151), the new run_case line (:185), the pin check (:192-194). No existing case, no READ_ONLY_HEADS entry, no audit/derive code touched — the five prior case verdicts re-verified green in item A.1. File set of the whole round diff (543cac1→18ddb05): red-d53-ledger.json, PROVINCE.md, corpus/README.md, corpus/SOURCES.md, figure-audit-mutbat.py, figure-audit.py, knowledge-expected.txt, aisi-...md — all inside the tolerated set (C2 files + named docs). Verdict: no existing limb weakened.

## G. Kill-rule walk (claims.json:18), clause by clause

1. Pristine selftest exit / last line — item A.1: `selftest cases=6 failures=0`, exit 0 → holds.
2. Battery exit / survivors / control — item A.2: exit 0, survivors=0, control held → holds.
3. m4/m6 killed by own selftest exit — item A.2 (killed=1 each) and item C (exit 1 each, py_compile OK) → holds.
4. Red fixture UNAVAILABLE / derived=34 / exit 0 — item A.3: derived=33, exit 1 → holds.
5. Ledger audit / entry count — items A.4-A.5: 35/35/0/exit 0 and 35 → holds.
6. Changed files outside tolerated set — item F: none → holds.
7. Five prior case verdicts changed — item A.1: 0,1,1,1,2 all as frozen → holds.
Kill-rule verdict: C1 SURVIVES all seven clauses.

## H. Observations (report-only; no rule or file changed)

- OBS-1 (pin is count-only): the EXPECTED_CASES pin kills drops (m4) but not substitutions; substitution is caught only by the battery replay (item B). Smallest safe correction if the canonical judge wants the selftest limb standalone: pin the sorted tuple of case ids (e.g. hash the `cid` list) instead of the count. Not required for C1 as frozen.
- OBS-2 (red fixture record-anchored): d53-1-trailer flips ok under a one-line receipt edit (item D) and would also flip if the receipt were regenerated. Smallest safe correction: add `"rev": "<r53 commit sha>"` to the entry and prefix the derive with `git show <rev>:` (head `git show ` is allow-listed, figure-audit.py:47-53); the red then reads committed bytes and becomes tamper-evident against working-tree edits. The lane working tree is clean w.r.t. the receipt today, so the frozen after-state reads as claimed.
- OBS-3 (battery bytes unpinned): figure-audit-mutbat.py is inside the tolerated file set, so an attacker free to co-edit instrument + battery could re-label a weakening as a control-adjacent mutant while keeping printed lines shaped right; the counting commands pin the printed tokens but not the battery's bytes. Within this round's frozen rules (the diff is the impl commit, clean tree) this path is closed; a sha pin on the battery would close it prospectively.
- OBS-4 (gate head-only, pre-existing): check_read_only (figure-audit.py:78-84) inspects only the first `|`/`>`-split segment's head; `&&`/`;`/backtick tails are unexamined. The committed ledger already uses `git cat-file -e ... && git show ...` (figure-audit-ledger.json:123,131) — benign, allow-listed heads both — and a scan found no `;`, `||`, backtick or `$(` derives, so the shipped after-state is safe; the gate design predates C1 and is not weakened by it. Correction would be to split on compound operators before the head check (both existing compound derives still pass).
- OBS-5 (counting-command exit masking): the red-fixture counting command pipes through grep, so its printed exit is grep's 0; the kill_rule's "or exits 0" clause needs the unpiped run, recorded in item A.3.

Evidence set: this file; commands as printed per item; scratch S=/fast/scratch/hyaku/kasegi-r58/CriticC1 (deleted before yield; no leftovers outside it; nothing written under L except this file).
