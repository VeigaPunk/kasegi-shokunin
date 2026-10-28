VERDICT: BROKEN

# R45MutLimbR2 — C1 mutation test of limb R2 (QUALITY R47-R49 rows) in corpus/instruments/r45-routed-defects.py

Scope: read-only mutation probe of `limb_r2` (counter lines 150-179). Counter not edited. No commit, no git mutation, no shared file touched. Scratch removed on exit.

Counter identity: `sha256sum corpus/instruments/r45-routed-defects.py` = `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee`; `git show 8cf62c879e6e6b031e67412f8fac1fba0bd378cf:corpus/instruments/r45-routed-defects.py | sha256sum` = the same value (272 lines). The counter run was the frozen one.

Base: `/fast/scratch/hyaku/kasegi-r45/L1/pure` copied (never edited); `corpus/QUALITY.md` sha256 `dd753497f7138c395230df48443d3d356ca0d67c3d8a8cd24d9989103dd43d03` equals `git show dc5bb8c6e31efc4a6650819df85e79b72fd64bcd:corpus/QUALITY.md | sha256sum`, 372 lines, ends with newline. `git diff --stat dc5bb8c6… -- corpus/QUALITY.md` in the lane printed nothing (working copy = base).

## 1. Survivors (defect present, counter silent) — 4 of 8

Each row: the single edit applied to the satisfied tree, and the counter's own limb R2 line (quoted).

S1. **M2-R47-ground-missing-file** — R47 ground cell `corpus/lessons/round-44.md (M44-3/M44-8)` changed to `corpus/lessons/round-44.md.bak (M44-3/M44-8)`; the `.bak` file does not exist in the tree.
   Counter printed: `limb R2 fixed=1 read=criteria=3`.
   Why it survives: line 167 is `if "corpus/lessons/round-44.md" not in ground` — a substring test; the grounding file is never opened.

S2. **M3-R48-must-negated** — R48 criterion `so every predicate must bind the content it checks` changed to `so every predicate need not bind the content it checks`. This inverts the rule the R48 class names (presence-only predicates accept fabricated trees).
   Counter printed: `limb R2 fixed=1 read=criteria=3`.
   Why it survives: lines 169-170 test only that the class needle `presence-only` appears in the criterion cell (`re.search(nd, crit, re.I)`); no polarity or sense check.

S3. **M4-R48-enforced-by-unrelated** — R48 `enforced-by: \`corpus/instruments/r44-routed-defects.py\`` changed to `enforced-by: \`corpus/QUALITY.md\``; the target exists but does not enforce the class.
   Counter printed: `limb R2 fixed=1 read=criteria=3`.
   Why it survives: lines 172-177 test only `os.path.exists` of each backtick path; the target is not checked for relation to the criterion.

S4. **M7-unclosed-fence-before-heading** — the single line `` ```text `` inserted immediately before `## Round-45 additions` (the R47-R49 table is then inside an unclosed code fence and does not render as a table; the three rows are hidden from a markdown reader).
   Counter printed: `limb R2 fixed=1 read=criteria=3`.
   Why it survives: the heading check (line 156) and row checks (lines 159-161) are regexes over raw text; rendering is not modelled.

## 2. Discriminating mutants (counter rejects) — 4 of 8

- M1-drop-R47-row (delete the R47 row): `limb R2 fixed=0 read=R47-rows=0`
- M5-R49-enforced-by-typo (`capture-binding-check.py` → `capture-binding-chek.py`): `limb R2 fixed=0 read=R49-enforced-by-missing-corpus/instruments/capture-binding-chek.py`
- M6-R49-reject-to-deny (`used for reject rows` → `used for deny rows`): `limb R2 fixed=0 read=R49-missing-reject`
- M8-base-byte-edit (`71668 bytes before it` → `71669 bytes before it`, first occurrence in base text): `limb R2 fixed=0 read=quality-not-append-only-or-unchanged`

## 3. Controls (discriminate against a satisfied tree and do-nothing)

- control=satisfied-T0 (base + the hand-built R47/R48/R49 block below): `limb R2 fixed=1 read=criteria=3` — the target limb is satisfied, so mutant rejections are meaningful.
- control=do-nothing-base (root = base export): `limb R2 fixed=0 read=quality-not-append-only-or-unchanged` — RED, matches freeze-controls.txt intent.
- control=marker-only (heading present, no rows): `limb R2 fixed=0 read=R47-rows=0` — RED.

## 4. Hand-built satisfied R2 block (appended to base QUALITY.md; exact text)

```
## Round-45 additions

Round-45 C1 limb R2 criteria; appended after the round-44 block, each grounded in `corpus/lessons/round-44.md`.

| id | criterion | grounded in |
|---|---|---|
| R47 | A frozen counter is replayed on a do-nothing control before any data is graded: the do-nothing base must grade RED before data is read; enforced-by: `corpus/instruments/limb-mutation-check.py` | corpus/lessons/round-44.md (M44-3/M44-8) |
| R48 | Presence-only predicates accept denials and fabricated trees, so every predicate must bind the content it checks; enforced-by: `corpus/instruments/r44-routed-defects.py` | corpus/lessons/round-44.md (M44-4/M44-7/M44-10) |
| R49 | A capture method used for admit must also be used for reject rows, graded by the capture-binding check; enforced-by: `corpus/instruments/capture-binding-check.py` | corpus/lessons/round-44.md (this spot-check) |
```

## 5. Run evidence (recipe `mutate_r2.py` in scratch; output verbatim, `R45_SCRATCH=…/R45MutLimbR2 TMPDIR=…/tmp python3 mutate_r2.py`, exit 0)

```
base_quality_sha256=dd753497f7138c395230df48443d3d356ca0d67c3d8a8cd24d9989103dd43d03
control=satisfied-T0 fixed=1 read=criteria=3 counter_rc=1
control=do-nothing-base fixed=0 read=quality-not-append-only-or-unchanged counter_rc=1
control=marker-only fixed=0 read=R47-rows=0 counter_rc=1
mutant=M1-drop-R47-row rejected=1
  edit: delete the R47 row line
  counter: limb R2 fixed=0 read=R47-rows=0 (counter_rc=1)
mutant=M2-R47-ground-missing-file rejected=0
  edit: R47 ground `corpus/lessons/round-44.md` -> `corpus/lessons/round-44.md.bak` (file absent)
  diff: +| R47 | … enforced-by: `corpus/instruments/limb-mutation-check.py` | corpus/lessons/round-44.md.bak (M44-3/M44-8) |
  counter: limb R2 fixed=1 read=criteria=3 (counter_rc=1)
mutant=M3-R48-must-negated rejected=0
  edit: R48 criterion 'every predicate must bind' -> 'every predicate need not bind'
  diff: +| R48 | Presence-only predicates accept denials and fabricated trees, so every predicate need not bind the content it checks; enforced-by: `corpus/instruments/r44-routed-defects.py` | corpus/lessons/round-44.md (M44-4/M44-7/M44-10) |
  counter: limb R2 fixed=1 read=criteria=3 (counter_rc=1)
mutant=M4-R48-enforced-by-unrelated rejected=0
  edit: R48 enforced-by `corpus/instruments/r44-routed-defects.py` -> `corpus/QUALITY.md` (exists, unrelated)
  diff: +| R48 | … enforced-by: `corpus/QUALITY.md` | corpus/lessons/round-44.md (M44-4/M44-7/M44-10) |
  counter: limb R2 fixed=1 read=criteria=3 (counter_rc=1)
mutant=M5-R49-enforced-by-typo rejected=1
  edit: R49 enforced-by `capture-binding-check.py` -> `capture-binding-chek.py`
  counter: limb R2 fixed=0 read=R49-enforced-by-missing-corpus/instruments/capture-binding-chek.py (counter_rc=1)
mutant=M6-R49-reject-to-deny rejected=1
  edit: R49 criterion 'used for reject rows' -> 'used for deny rows'
  counter: limb R2 fixed=0 read=R49-missing-reject (counter_rc=1)
mutant=M7-unclosed-fence-before-heading rejected=0
  edit: insert line '```text' immediately before '## Round-45 additions'
  diff: +```text
  counter: limb R2 fixed=1 read=criteria=3 (counter_rc=1)
mutant=M8-base-byte-edit rejected=1
  edit: append-only breach: base token '71668 bytes before it' -> '71669 bytes before it' (first occurrence, in base text)
  counter: limb R2 fixed=0 read=quality-not-append-only-or-unchanged (counter_rc=1)
survivors=4 M2-R47-ground-missing-file,M3-R48-must-negated,M4-R48-enforced-by-unrelated,M7-unclosed-fence-before-heading
base_quality_sha256_unchanged=True
```

(Diff lines abbreviated with `…` where identical to §4; full text is in the run log quoted in §4. The recipe asserted each edit matched exactly once before applying it, so every mutant is a single, exact edit.)

## 6. Repair notes for the L1 (not implemented here; the counter is frozen and edits are the L1's call)

Per C1 kill rule, a predicate change after a seat has scored is a freeze violation; tightening that keeps the predicate's intent is a counter erratum to be logged, not a new rule. Candidate tightenings, each closing one survivor:
- S1: resolve the ground path `corpus/lessons/round-44.md` as a whole token (`(?<![\w./-])corpus/lessons/round-44\.md(?![\w.-])`) and require that file to exist under root.
- S2: require each class criterion to match its class sentence (e.g. R48 must contain `must bind` or equivalent) rather than a bare needle; a negated polarity word (`need not`, `not a defect`) fails.
- S3: require each `enforced-by` target to be a file whose path or content names the class (e.g. `r44-routed-defects.py` for R48), or at minimum to not equal the QUALITY file itself.
- S4: require the heading line to be the first non-blank line of the tail and no fence opener to be open at the heading (track ``` parity over the tail).

## 7. Limitations

- Survivor list is for limb R2 only, as asked. Not exhaustive: 8 single edits chosen to span rows, needles, ground, enforced-by, append-only and layout; other single edits may survive.
- The satisfied tree sets R2 only; the full counter prints `rc=1` on it because limbs R1, R3-R5 are unsatisfied there. The R2 `read=` token is the signal used; the other limbs' results are not claimed.
- The counter's ground check and needle checks are substring/regex over raw text; I did not test whether the cited lesson actually supports each class (the limb never opens it), so a row grounded in a real but unrelated lesson section is not covered by this probe.
- Markdown rendering was reasoned about (S4), not rendered; the counter does not model it.
- One run, deterministic (no timing or randomness in the limb). Scratch base copy (159 MB) and all mutant trees were removed after the run.
- No installs, no tool upgrades (none needed); no pacman; no git mutation; no commit; no edit to the counter, claims, controls, QUALITY.md, or any shared file.
