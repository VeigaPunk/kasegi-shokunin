VERDICT: BROKEN

Seat R45W2MutC1R1R2 (mutation-tester), C1 limbs R1 and R2 of `corpus/instruments/r45-routed-defects.py` v1.1. Attacked: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (tip), round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd (base). Counter bytes unchanged; no git mutation; scratch removed on exit. Installs: none.

Method: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive <tip|base> | tar -x -C <scratch>/{tip,base}`, then `python3 recipe/mutate_c1_r1r2.py` (env `S=<scratch>`, `TMPDIR=<scratch>/tmp`). Each mutant = a fresh copy of tip, ONE edit (count asserted == 1), counter run from the copy (its own tool root) with `--root <copy> --baseline <base>`. `rejected=1` means the targeted limb printed `fixed=0`; `rejected=0` means the limb stayed green while the defect is present. The recipe ran twice; both runs gave identical rejected values for all 13 cases.

Controls (discriminate the counter from a do-nothing pass):
```
control-tip-unmodified-vs-base: tip exit=0 R1=1 R2=1
mutant=CTRL-base-do-nothing rejected=1 target=R1+R2 exit=1
    R1 fixed=0 read=row-S072=absent
    R2 fixed=0 read=quality-not-append-only-or-unchanged
mutant=CTRL-tip-unmodified rejected=0 target=R1+R2 exit=0
mutant=CTRL-R2-line-ref-out-of-range rejected=1 target=R2 exit=1
    R2 fixed=0 read=R47-line-refs-absent-or-out-of-range
```
The counter discriminates: the base do-nothing tree is red on both limbs, the tip is green, and a single out-of-range line reference is caught.

## Findings: survivors (counter green while the defect is present), 9 of 10 mutants

Every survivor edits a file the PINS do not cover (PINS at r45-routed-defects.py:67-74 cover only S072.txt, freeze-check.py, r44-frontier-count.py, r44-routed-defects.py, the refiled body and claims.json). SOURCES.md, QUALITY.md, round-44.md and manifest.json are unpinned.

**S1 — R2 / table inside a code fence accepted.** Edit to `corpus/QUALITY.md` (tail, `## Round-45 additions`): a line "```" inserted before the header `| id | criterion | grounded in |` and another after the R49 row. Output: `mutant=R2-01-table-in-code-fence rejected=0 target=R2 exit=0`, then `R2 fixed=1 read=criteria=3`.
Cause: limb_r2 reads rows with `lines = [ln for ln in tail.splitlines() if re.match(...)]` (r45-routed-defects.py:213). It does no fence or HTML-comment stripping. The fence stripping at registry_lines (lines 90-106) covers only SOURCES.md. The v1 falsifier's "row inside a code fence" is fixed for the SOURCES registry but not for the QUALITY criteria.

**S2 — R2 / R48 inverted to license presence-only limbs.** `corpus/QUALITY.md` R48 row: `so every limb must bind content:` → `so a limb may check presence alone:`. Output: `mutant=R2-02-R48-licenses-presence-only rejected=0 target=R2 exit=0`, `R2 fixed=1 read=criteria=3`.
Cause: the class check is a keyword presence test on the criterion text (CLASS_RX at lines 196-200; `re.search(nd, crit, re.I)` at line 223). A negated or inverted criterion that keeps the keyword passes.

**S3 — R2 / R49 negated.** `corpus/QUALITY.md` R49 row: `The capture method used to ADMIT a source is also the capture method used to REJECT one:` → `... The capture method used to ADMIT a source need not be the capture method used to REJECT one:`. Output: `mutant=R2-03-R49-negated rejected=0 target=R2 exit=0`, `R2 fixed=1 read=criteria=3`.
Cause: same keyword-presence predicate (line 223). The criterion text is never read for meaning.

**S4 — R2 / R47 `enforced-by` points at an unrelated existing file.** `corpus/QUALITY.md` R47: `enforced-by: \`corpus/instruments/freeze-check.py\`` → `enforced-by: \`corpus/README.md\``. Output: `mutant=R2-04-R47-enforced-by-unrelated-file rejected=0 target=R2 exit=0`, `R2 fixed=1 read=criteria=3`.
Cause: the enforced-by check is `os.path.isfile(...)` only (lines 228-230). It does not check that the target enforces the criterion. The v1.1 "directory targets" fix blocks directories but not irrelevant files.

**S5 — R2 / R47 line reference moved to an unrelated in-range line.** `corpus/QUALITY.md` R47: `corpus/lessons/round-44.md:126` → `corpus/lessons/round-44.md:1` (line 1 is `# Round 44 — Kasegi`). Output: `mutant=R2-05-R47-line-ref-unrelated-line rejected=0 target=R2 exit=0`, `R2 fixed=1 read=criteria=3`.
Cause: the line-reference check is a range test only (lines 233-235). A grounding citation is not checked against its content.

**S6 — R1 / vacuous flip clause back.** `corpus/SOURCES.md` S072 row, teaches cell: `flip: a fresh article-API capture states a program-specific scope or boundary rule that the program's linked rules page does not state` → `flip: tbd`. Output: `mutant=R1-01-flip-vacuous rejected=0 target=R1 exit=0`, `R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`.
Cause: the flip check is `re.search(r"flip:\s*\S", teaches)` (line 158), which accepts any non-space token. Lesson §6 item 1 names the vacuous flip as the defect, and the v1 falsifiers (`flip: tbd`, per the counter's own docstring lines 40-42) reintroduced it. v1.1 did not fix it.

**S7 — R1 / denied readable body.** `corpus/SOURCES.md` S072 teaches: `the body is readable through the article API (10029 characters)` → `the body is not readable through the article API (10029 characters)`. Output: `mutant=R1-02-readable-denied rejected=0 target=R1 exit=0`, `R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`.
Cause: `re.search(r"\breadable\b", teaches)` (line 162) is presence-only. A denial ("not readable") passes. That is the R48 class the counter claims to cover.

**S8 — R1 / lesson correction reverses its own conclusion.** `corpus/lessons/round-44.md` line 205: `so the JavaScript-shell reason does not hold` → `so the JavaScript-shell reason holds`. Output: `mutant=R1-03-correction-reversed rejected=0 target=R1 exit=0`, `R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`. The line still says "the S070 body is readable through the article API", so the corrected line now contradicts itself and the counter does not notice.
Cause: the correction is accepted on three tokens (starts with "Correction (round 45", contains S072, contains 10029) plus one located span of at least six words (lines 185-193). The assertion the correction makes is never read.

**S9 — R1 / manifest quote replaced by a generic located phrase.** `corpus/source-snapshots/round-45/manifest.json` S072 Q2: `an overview of the different vulnerability reward programs Google maintains` (anchor 1) → `Welcome to the VRP rules section!` (the same anchor-1 window; snapshot line 2 begins with it). Output: `mutant=R1-04-manifest-located-generic rejected=0 target=R1 exit=0`, `R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`.
Cause: manifest.json is not in PINS. source-recheck.py (invoked at lines 171-175) verifies only that quotes are located, not that they support the row's teaches. The R1 limb reads `oks=2` and passes.

## Caught (the counter bites here)

**C1 — R1 / fabricated located quote in the correction.** `corpus/lessons/round-44.md` line 205: `Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data` → `... that handles all user data`. Output: `mutant=R1-05-correction-quote-fabricated rejected=1 target=R1 exit=1`, `R1 fixed=0 read=lesson-correction-absent-or-quotes-no-located-S072-span`. The located-span check works for a span that is not in the snapshot.

## Observations on the tip (state, not mutants)

**O1 — R1 is green while the defective S070 reason stays live in the registry.** The S070 row is required byte-identical to base (lines 164-167), and no pointer to S072 is required. Probe on the tip export: `probe S070-row-count=1 mentions-JavaScript-shell=True mentions-S072=False`. So the registry row still states "REJECTED: the page's accessible body is a JavaScript shell", with no supersession marker. Lesson §6 item 1 asks for a correction "to corpus/SOURCES.md S070". The counter certifies the fix while the wrong reason remains in S070.

**O2 — the correction's own "true reason" is not located, and the limb does not require it to be.** Probe: `probe true-reason-span located-in-S072=False span='overview, no program-specific rule beyond S069 Q5'`. The limb passes on `any(...)` (line 189) because the other span (the Q1 quote) is located. The reason the correction asserts is therefore unverified by the counter.

**O3 — the snapshot is not a JavaScript shell, and S072 nowhere says so.** Probe: `probe JS-shell-claim-in-S072=False`. This is consistent with the correction, so O1 and O2 are the defects, not the correction's direction.

## Limitations
- Ten mutants, one edit each, chosen by me from the lesson §6 defect statements and the counter's predicates. Survivors are a lower bound on the counter's gaps, not an exhaustive list. I did not test combined edits, and I did not test R3-R5.
- Only the export of 6662a42 (tip) and dc5bb8c (base) was used. I did not run the L1 pure copy at /fast/scratch/hyaku/kasegi-r45/L1/pure.
- I read only the first 120 lines of source-recheck.py (anchor logic and docstring); R1-04's survival rests on the counter's own output (`recheck-quotes=2`), not on a full read of that tool.
- The probes (O1-O3) use a small reimplementation of the counter's `norm` (r45-routed-defects.py:84-87); they are not the counter's own output.
- Survivor severity is my judgment: S1-S5 and S7 are predicate-level gaps the counter's own docstring claims to close (R48 binding content); S6 and S9 are gaps against the lesson's explicit defect statements.
- Scratch dir removed on exit. No file in the lane, the fleet repo or shared production files was modified.
