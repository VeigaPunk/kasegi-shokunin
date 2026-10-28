VERDICT: BROKEN

Scope: `corpus/QUALITY.md` rows R47, R48, R49 and the `## Round-45 additions` block, read from the export of `6662a4276b6f7bd61e23e12058414e09dd71b9e4` (round base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` exported read-only as the do-nothing control). Two of the three `enforced-by:` paths do not enforce the rule their row states (R48, R49); R47's before-value clause is enforced, its timing clause is not. The R6 head figures hold. Plus one counter hazard (F7) that bears on R47's control.

## F1 — R6 head line numbers: HOLDS
Attacked: the append-only claim in the block's preamble (`QUALITY.md:376`).
Commands and output:
```
$ git -C <lane> show dc5bb8c6…:corpus/QUALITY.md | head -c 78651 | sha256sum
dd753497f7138c395230df48443d3d356ca0d67c3d8a8cd24d9989103dd43d03  -
$ head -c 78651 base-QUALITY.md | wc -l
372
$ stat -c %s base-QUALITY.md   -> 78651 ; export (6662a42) -> 83252 bytes, 382 lines
$ cmp <(head -c 78651 exp/corpus/QUALITY.md) base-QUALITY.md && echo PREFIX-OK
PREFIX-OK
```
Row numbers R22=226 … R46=372 identical in base and export (grep -n "^| Rnn |" on both). The block starts at line 373 and R47/R48/R49 sit at lines 380/381/382.

## F2 — R47 (do-nothing before-value) enforced-by `corpus/instruments/freeze-check.py`: PARTIAL
What is enforced: the counter's output must contain a line EQUAL to `expect_before`, run on `--base`; a counter that reads 0 for a nonzero declared before fails.
- `python3 corpus/instruments/freeze-check.py --selftest --work <s>/tmp/fc1 --base <s>/base` → `case 2-round44-frozen-grep-real-readme PASS … table-aware admitted=26, frozen grep read 0 … | claim C base_read=0 verdict=FAIL` and `selftest cases=20 failures=0`, exit 0. The R47 mine (grep reads 0 where 26 is true) is caught.
- Replay of the frozen round-45 claims at the do-nothing base: `claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok`, `claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok`, `freeze-check claims=2 base_ok=2 exit=0`.
- Wrong control (treatment tree passed as `--base`): `claim C2 … fixed=7/7 exit=0 verdict=FAIL`, `finding C2 FC-NO-MATCH …` and `finding C2 FC-AFTER-AT-BASE counter output already contains expect_after`. So a treatment tree used as control is rejected through FC-AFTER-AT-BASE, not accepted.
Not enforced: "BEFORE data is read and before any seat scores". `freeze-check.py` has no record of ordering; the only timing check in the repo is R44's `frozen-at` vs `measured-at`. The clause is procedural. Overlap (not duplicate): R34 already requires a dry run of the frozen counting command before freeze, and R22/R25 require literal satisfiability against base before freeze. R47 is the narrower before-value predicate; it should cross-reference R22/R34 instead of restating the rule.

## F3 — R48 (presence-only) enforced-by `corpus/instruments/r45-routed-defects.py`: BROKEN
The rule ("every limb must bind content … a limb that only checks that a file, heading, row or word exists is void") is not enforced by the path named. `limb_r2` (lines 203-238) checks: the block heading count == 1, exactly one row per id, three cells, the substrings `do-nothing`/`before data`/`presence-only`/`capture method`/`reject` in the criterion text, `enforced-by:` path `isfile`, criterion length ≥300, and line refs in range. That is the presence-only pattern R48 forbids; the script does not bind any criterion's content.
Demonstration (`importlib` load of the export's script, then `limb_r2`):
```
E4a limb_r2(export, base)       -> (True, 'criteria=3')
E4b limb_r2(base, base)         -> (False, 'quality-not-append-only-or-unchanged')   [do-nothing control]
E4c limb_r2(adversarial, base)  -> (True, 'criteria=3')   [adversarial: R47-R49 rows carrying only the needle words plus padding, no rule]
```
The adversarial root is the base QUALITY bytes plus three placeholder rows; the r45 counter passes them. The R48 limbs that DO bind bytes (S072 sha pin, `PINS`) are in `limb_r1`/`limb_r3`/`limb_r4`/`limb_r5`, not in the criterion check that R48 names. Partial overlap: R48's "affirmative tokens read as whole values" restates R41 (QUALITY.md:353), and "located quotes by exact anchor" restates Q9 (QUALITY.md:64).
Fix direction: either drop `enforced-by` for R48 and state it as review-only, or add a check that each cited limb's counter reads the pinned bytes (not a text-presence check).

## F4 — R49 (capture-method parity) enforced-by `corpus/instruments/source-recheck.py`: BROKEN
`source-recheck.py` binds bytes and located quotes only. It never reads `capture_url`, `url`, `http.final_url` or `kind` (`grep -n -i "capture_url\|method\|admit\|reject\|kind" corpus/instruments/source-recheck.py` → only a comment at line 380). The only instrument reading `capture_url` is `capture-binding-check.py` (lines 452-460: capture_url == http.final_url), which has no admit/reject method logic. The registry has no capture-method column (`corpus/SOURCES.md:5`: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`).
Demonstration: copied the round-45 manifest, changed S072's `capture_url`, `url`, `http.final_url` to `https://example.invalid/js-shell` and `kind` to `html`, sha pin untouched:
```
--- original:
S072:sha256 OK
S072:Q1 OK normalized=markup-whitespace occurrences=1 anchor=148-ok
S072:Q2 OK normalized=markup-whitespace occurrences=1 anchor=1-ok
exit=0
--- tampered capture method fields:
(identical lines)  exit=0
```
Byte control (append `x` to S072.txt, same manifest): `S072:sha256 MISMATCH expected=364166c4… actual=ea3f6e4e…`, exit=1. So the script discriminates bytes but is blind to the capture method, which is exactly the parity rule R49 states.

## F5 — R49 contradicts the landed R1 handling of the S070 row: BROKEN (decision needed)
R49 says a reason the second capture contradicts "is corrected in the registry row and in the lesson that recorded it, not left standing." The landed state leaves the S070 row as it was:
```
$ git show dc5bb8c6…:corpus/SOURCES.md > base-SOURCES.md
$ diff <(grep "^| S070 " base-SOURCES.md) <(grep "^| S070 " exp/corpus/SOURCES.md) && echo "S070 row identical to base"
S070 row identical to base
$ grep -c "JavaScript shell" exp/corpus/SOURCES.md
1
```
The S070 row still reads `REJECTED: the page's accessible body is a JavaScript shell …`. R1's limb (`corpus/instruments/r45-routed-defects.py:164-167`) requires `old == new` for that row, so the counter enforces the opposite of R49's wording. The correction is instead a new superseding row S072 plus an appended line at `corpus/lessons/round-44.md:205`, which says "the S070 reject reason above (`## Gate` and the S070 row) was wrong". The lesson therefore says the S070 row is wrong while the row stands. Also, `round-44-verifier-spotcheck.md:79` (§6 item 1) asked to "Append (never rewrite) a correction to `corpus/SOURCES.md` S070", which the landed design did not do. The frozen C1 `after` text does accept "superseded by a sha-pinned row S072", so the defect is in R49's wording, not in the frozen claim. Either reword R49 to "corrected in a superseding row and in the lesson", or append a correction to the S070 row and change R1. Pick one; as written R49 and R1 cannot both hold.
Minor citation gap: R49's grounded column cites spotcheck §6 item 1 (line 79); the capture-method class itself is named at `round-44-verifier-spotcheck.md:80` (item 2), which is not cited.

## F6 — Citation check (lessons say what is claimed): HOLDS, with the minor gap in F5
Each cited line was printed with `sed -n` and checked:
- R47: `round-44.md:15` (M44-3, "command prints 0 in base and after"), `:126` (M44-8, "a counter must be re-derived on a do-nothing control before data"; "`frontier rows=25 admitted=25`"). Controls `.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt` (prints `0`, `0`) and `c2-do-nothing.txt` ("Correct diagnostic counts at base: admitted frontier 25") exist and match.
- R48: `round-44.md:16` (M44-4, marker-only tree → all 8 fixed), `:125` (M44-7), `:167` (denials, stub, fabricated seat names), `:189` (M44-10, `fixed=8 unresolved=0` on fabricated tree). `.ufo/waves/round-44/wave2/R44W2Rev09.md` exists; line 41 "D5 accepts a nonfunctional emitter and fabricated seat names".
- R49: `round-44.md:22`, `:24` (S069 via article API), `:131` (S070 reject from "JavaScript shell"); `round-44-verifier-spotcheck.md:65-66` (S069 agree; S070 "10 029-char body") and `:79`. Manifest S072 `capture_url` exists.

## F7 — Hazard in the r45 counter's R4 limb (affects R47's control): BROKEN for same-tree baseline, defined for the L1 command
`limb_r4` replays `.ufo/waves/round-45/claims.json` through `freeze-check.py`, whose C1 `counter_cmd` is the r45 counter itself. Passing the same tree as root and baseline recurses without a guard:
```
(exp, base)  → exit=0 secs=3.2   (5/5 limbs fixed)
(base, base) → exit=1 secs=0.1   routed-defects total=5 fixed=0 unresolved=5 exit=1   [do-nothing]
(exp, exp)   → STILL RUNNING after 90s (killed process group)
```
When I killed the (exp, exp) run, `pgrep -f` showed 424 nested `r45-routed-defects.py`/`freeze-check.py` processes. These were all children of my scratch export; I removed them with `pkill -9 -f R45W2RevQualityRows/exp` and confirmed `remaining=0`. The wrong-control replay in F2 also ended as `FC-TIMEOUT counter exceeded 280 s` for C1. R47's control must print its before-value; a control that hangs prints nothing and cannot satisfy it. Fix: a recursion guard (e.g., skip R4 when `--baseline == --root`, or refuse when the claims sha is the one under replay).

## Limitations
- Scope limited to QUALITY.md R47-R49 and the block. Other seats cover C1 counter and C2 gate; I did not re-judge R1-R5 beyond the R1 S070 rows and R4 freeze-check behavior needed for F2 and F7.
- F2 timing clause: not tested by a counter; judged from code absence (`freeze-check.py` has no ordering check).
- F4: the demonstration altered only the manifest fields; I did not check `capture-binding-check.py` with a consistent mismatch (it accepts matching `capture_url`/`final_url`), so I am claiming only that `source-recheck.py` is blind to method, not that no instrument checks it.
- Self-inflicted artifacts: my `importlib` load of `r45-routed-defects.py` wrote `__pycache__` into my scratch export while a background replay ran, so the `FC-BASE-MUTATED` line in the E6 output is caused by my import, not by the counter. It is not a finding.
- One early E5 attempt failed (variables were not set in a temporary shell); the reported E5 numbers are from the rerun with absolute paths.
- Nothing was committed or mutated in the lane; scratch removed on exit.
