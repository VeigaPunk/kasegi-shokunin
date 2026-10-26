# ScribeQualityRows — round 36 (kasegi-shokunin / hyaku run 9)

| field | value |
|---|---|
| seat | `ScribeQualityRows` (scribe, leaf — no dispatch) |
| item | draft two append-only `corpus/QUALITY.md` rows: R28 (quiescence / head-closure), R29 (exact-basename registration) |
| axes owned by the round | `depth:verifiability`, `coverage`; this seat judged on `depth:verifiability`, `calibration` |
| milestone | round-36 |
| lane head at work | `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze); base `cc692008b0cfd58d18275aa6c4aed79620120799` |
| worked at (UTC) | 2026-10-26 (local shell clock 12:37–12:41 -03:00) |
| lane writes | none — receipt only. `corpus/QUALITY.md` was read, never edited (sha256 unchanged across the seat: `d4f83bb1…d6e2b69`) |

Deliverable is draft text for the L1/integrator to append. Nothing below upgrades a contract-only
statement into a measurement: every prospective value is labelled, and the block itself says which
figure it does not own.

---

## 1. Deliverable — append block (verbatim, ready to append after line 250)

```markdown
## Round-36 additions — head closure and exact-basename registration (append-only)

R6 form: every line above keeps its number — this block is appended after line 250 (the file is
33731 bytes before it, `head -c 33731 corpus/QUALITY.md | sha256sum` →
`d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69`; `wc -l` → 250), and R22 (line
226), R23 (line 227), R26 (line 249) and R27 (line 250) are not edited. The landing commit re-runs
both commands immediately before writing: a byte figure measured at draft time is a stale premise
under R19 if an earlier append in the same round moved it.

| id | criterion | grounded in |
|---|---|---|
| R28 | A round's claims rest on committed paths at the quoted head, and the run that carries them is made against that head, not the worktree: the counter/harness runs a claim cites are recorded over a `git archive <final lane commit>` export (an `--export-ref <hash>` run), and the lane is quiescent before filing — `git status --porcelain` empty and no leftover scratch seat dirs under `/fast/scratch/hyaku/kasegi-rNN/`. A run made while wave seats still write, or over a worktree that differs from the quoted head, is not a closure run and cannot carry a claim. | `corpus/lessons/round-35-verifier-spotcheck.md:127-129` (§5.1 — "Quiesce the wave, commit every path the claims rest on, then file; record the suite and harness run over `git archive <final lane commit>`, not the worktree. Append a lesson/QUALITY row citing this spot-check."), the same spot-check's verdict `:13-19` (M35-1 recurrence — the r35 bytes landed 04:01:12–04:04:55 after the 04:00:34 `complete`, "while wave seats were still writing"), `:140-141` (§5.6 — "Two untracked seat receipts and four modified files after `48e6053`"), `corpus/lessons/round-35.md:282-290` (M35-7 — class landing/closure-order on cleanup: a receipt printed `scratch-absent` while `live-selftest.txt` 03:42:59, `.git/objects/…` 03:43:36 and `green.txt` 03:43:43 re-created the tree, so the durable record was a prediction rather than output; its re-runnable form is `find /fast/scratch/hyaku/kasegi-r35 -mindepth 1 -maxdepth 1 -type d`), and `considerthese/2026-10-26.md:31` proposal 3 (2026-10-26 — "Add a quiescence gate before `complete`. Require `git status --porcelain` to be empty … before a lane may signal done"). No row above states this: R14 caps wave-evidence size in git; R15, R16 and R18 bind a closure check to a filed paragraph's bytes; none binds the run a claim cites to an export of a committed head. Runnable form: `test -z "$(git status --porcelain)"` → exit 0 and `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d` → prints nothing at filing, then `bash corpus/instruments/r36-closure.sh --export-ref <final-lane-hash>` → `closed=9/9 exit=0`. First measurement is the round-36 post-integration run: at the round-36 freeze `ls corpus/instruments/r36-closure.sh` → exit 2, so this row claims none. |
| R29 | An instrument is registered at the `SKILL.md` § Gates & probes registry under its exact basename — one row whose name cell is exactly the file name (`r36-closure.sh`) — not under a name of which it is a substring. A near-name sibling row (the `r-defect-closure.sh` row for `r35-defect-closure.sh`) does not satisfy the registry requirement, and a registry count reached by a substring literal is a false green even when it prints non-zero. | M36-3 (`corpus/lessons/round-36.md` § Mistakes, minted this round; anchor text `.ufo/waves/round-36/build-spec.py:123`) — class counter-discrimination, captured-by R17 limb / R11 discrimination; re-derived on the frozen round-36 head: `git show b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6:SKILL.md \| grep -cF 'r35-defect-closure.sh'` → 0 while the instrument is tracked (`git ls-tree --name-only cc692008b0cfd58d18275aa6c4aed79620120799:corpus/instruments/ \| grep -cF 'r35-defect-closure.sh'` → 1) and the near-name row sits at `SKILL.md:1097`. The old literal is substring-shaped: `corpus/instruments/r35-defect-closure.sh:192` measures `grep -c -F -- 'r-defect-closure' SKILL.md`, which the near-name row satisfies — the mention/negation class the spot-check already routes at `corpus/lessons/round-35-verifier-spotcheck.md:132-134` (§5.3). Exact-cell check (`grep -cE '^\| *r35-defect-closure[.]sh *\|' SKILL.md`; pass value 1, measured 0 at the freeze) is the form C1's E3 asserts for `r35-defect-closure.sh` and `r36-closure.sh`; the 0 is the before-state, not a defect of this row. |
```

Two cell-internal pipes are written `\|`, the escape `SKILL.md:1097` (`gate\|probe`) already uses;
`corpus/QUALITY.md` carries three such lines today, so the convention is in-file, not new.

---

## 2. Grounding re-derived (read-only, commands as run from the lane root)

| # | fact | command | observed |
|---|---|---|---|
| G1 | spot-check routes closure-order defect #1 | `nl -ba corpus/lessons/round-35-verifier-spotcheck.md \| sed -n '127,129p'` | `127 1. **Close against one head (M35-1 recurrence).** Quiesce the wave, commit every path the claims` / `128 rest on, then file; record the suite and harness run over `git archive <final lane commit>`, not` / `129 the worktree. Append a lesson/QUALITY row citing this spot-check.` |
| G2 | M35-1 recurrence stated in the verdict | `nl -ba … \| sed -n '13,19p'` | "the D3 registry rows are absent from `SKILL.md`"; "landed the missing bytes *after* the `complete` line … (8ce6fb4 04:01:12, 5a25337 04:02:21, bb2dc8c 04:04:46, 48e6053 04:04:55) … while wave seats were still writing. That is M35-1 … recurring." |
| G3 | dirty-tree limb (§5.6) | `nl -ba … \| sed -n '140,141p'` | `6. **Dirty tree at closure.** Two untracked seat receipts and four modified files after `48e6053`;` / `commit or record them as discarded.` |
| G4 | proposal 3 on its own line | `nl -ba considerthese/2026-10-26.md \| sed -n '31p'` | `3. **Add a quiescence gate before `complete`.** Require `git status --porcelain` to be empty, plus the D1 placeholder grep from `r35-defect-closure.sh`, before a lane may signal done.` |
| G5 | no R28/R29 yet; highest id is R27 | `grep -cE '^\| R[0-9]+ \|' corpus/QUALITY.md`; `grep -cE '^\| R2[89] \|' corpus/QUALITY.md` | `27`; `0` |
| G6 | exact basename absent at base and at freeze | `git show cc692008…:SKILL.md \| grep -cF 'r35-defect-closure.sh'`; `git show b47f2cdf…:SKILL.md \| grep -cF 'r35-defect-closure.sh'` | `0`; `0` |
| G7 | instrument exists, registration does not | `git ls-tree --name-only cc692008…:corpus/instruments/ \| grep -i closure` | `r-defect-closure.sh` and `r35-defect-closure.sh` both tracked |
| G8 | near-name row exists | `grep -cE '^\| *r-defect-closure\.sh *\|' SKILL.md` | `1` (the row itself at `:1097`; `grep -cF 'r-defect-closure.sh' SKILL.md` → `3`, the row plus its notes at `:1102`/`:1104`) |
| G9 | exact-cell form measured at freeze | `grep -cE '^\| *r35-defect-closure\.sh *\|' SKILL.md`; `… r36-closure\.sh …` | `0`; `0` |
| G10 | old D3 literal is a substring count | `sed -n '192p' corpus/instruments/r35-defect-closure.sh` | `    rdc=$(grep -c -F -- 'r-defect-closure' SKILL.md 2>/dev/null); rdc=${rdc:-0}` |
| G11 | suite under test absent at freeze | `ls -l corpus/instruments/r36-closure.sh` | `No such file or directory` (exit 2) |
| G12 | QUALITY anchors at draft time | `wc -l -c corpus/QUALITY.md`; `head -c 33731 corpus/QUALITY.md \| sha256sum` | `250 33731`; `d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69` |
| G13 | R6-convention precedents not disturbed | `grep -nF 'supersedes R22' corpus/QUALITY.md`; `… 'supersedes R23' …` | present at `:249`/`:250`; the draft block adds neither literal (`python3` substring check on the block: both `False`) |
| G14 | M35-7 minted, cleanup-ordering limb | `nl -ba corpus/lessons/round-35.md \| sed -n '282,290p'` | `M35-7 (provisional) — a receipt asserted its scratch tree was absent while a later write re-created it, making the durable record a prediction.` Class landing/closure-order (M35-1's class, on cleanup); evidence `wave1/ExecClosureSuite.md` printed `scratch-absent` while `live-selftest.txt` (03:42:59), `.git/objects/…` (03:43:36), `green.txt` (03:43:43) were written after it; able-to-fail form `find /fast/scratch/hyaku/kasegi-r35 -mindepth 1 -maxdepth 1 -type d` |
| G15 | R28/R29 do not duplicate an existing row (cross-seat check, re-derived here) | `grep -ci -- <term> corpus/QUALITY.md` for `quiesc`, `porcelain`, `export-ref`, `exact basename`, `near-name`, `basename` | `0` for all six; `grep -cE '^\| R2[89] \|'` → `0`. Adjacent rows are distinct in mechanism: R14's `git archive` is tarball regeneration (evidence economy), R18's `scratch` is mutant-control copies, R4 is round-existence credit with no quiescence limb, R16 binds paragraphs, R19 binds specimen figures, R11/R17 bind instrument discrimination, not registry identity |
| G16 | closure-order lineage cells (own re-read of the sibling's correction) | `grep -n porcelain corpus/lessons/round-{30,31,32,33,34}-verifier-spotcheck.md` | r30`:15` DEFECT (8 untracked entries); r31`:17` empty; r32`:32` empty; r33`:31` reads status; r34`:30` "Empty at closure start. At 06:21:40Z: ` M …`" (D4). So 3 of the last 6 closure checks (r30, r34, r35) carried the defect, non-monotonically — the calibration argument for a standing gate rather than per-round vigilance |

Before-state of R28's own gate, measured while the wave runs (this is the before, not an after):

| probe | command | observed |
|---|---|---|
| lane quiescence | `test -z "$(git status --porcelain)"` | exit `1`; `git status --porcelain \| wc -l` → `9` (round-36 wave artifacts, pre-existing) |
| scratch seat dirs | `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d \| wc -l` | `49` (includes this seat's dir; all wave seats live) |

---

## 3. What this draft deliberately does not claim

- **R28 owns no run.** `corpus/instruments/r36-closure.sh` does not exist at the freeze (G11), so the
  row's `closed=9/9 exit=0` is written as the criterion's pass value and labelled "first measurement
  is the round-36 post-integration run". C1's suite build is a sibling executor's work.
- **R29 owns no landing.** The exact-cell counts are `0`/`0` (G9) — the before-state. The pass value
  `1` belongs to C1's E3 check after integration; this receipt does not assert it.
- **No E7 interference.** The block contains neither `supersedes R22` nor `supersedes R23`, so the
  strings `r35-defect-closure.sh:250-251` count to close E7 are unchanged by the append.
- **Byte/sha anchors are draft-time** (G12). The block instructs the landing commit to re-measure
  immediately before writing; reusing `33731`/`d4f83bb1…` after another append would be the R19
  stale-literal class.
- **Grounded-in file line numbers were re-derived, not copied**: §5.1 `:127-129`, verdict `:13-19`,
  §5.6 `:140-141`, §5.3 `:132-134`, M35-7 `:282-290`, considerthese proposal 3 `:31`.
- **Amendment after cross-seat review (ConnPatterns, IRC):** R28's grounded-in cell gained the M35-7
  citation (G14) for the scratch-cleanup limb. The criterion text is byte-identical to the first
  draft; no other wording changed, and the row still owns no run.

## 4. Composition checks run on the draft

- Table form: 4 row lines (header, separator, R28, R29); every row has exactly 4 pipe characters
  after removing `\|` escapes → 3 columns, matching the file's `| id | criterion | grounded in |`.
- Forbidden literals: `filled by the L1` → absent; `<LANE_HASH>` → absent (the R28 text uses the
  metavariable `<final-lane-hash>` so C1's E1 literal stays 0 in any file it greps).
- R6: append-only, no renumbering; the block names the lines it appends after and the four rows it
  must not touch.
- No-harm: `corpus/QUALITY.md` sha256 before and after this seat is
  `d4f83bb1…d6e2b69`; no lane file was created or modified by this seat.

## 5. Findings (for the L1, no lane edit made)

- **F1 — the r35 D3 row is a registry miss, not a wording miss.** The instrument was tracked at the
  base (G7) and the suite's own D3 limb counted the near-name substring (G10), so the r35 round could
  print a green registry limb while the exact basename was absent at its judged head (G6). R29 is the
  row that names this; C1's E3 is its counter. Both are needed: the row states the bar, E3 measures it.
- **F2 — the quiescence gate has two independent limbs and the round-36 claim uses both.** Proposal 3
  supplies `git status --porcelain`; the scratch-dir limb is grounded in the lane's own M35-7
  (G14 — `scratch-absent` asserted before later writes re-created the tree, so the durable record was
  a prediction) and is the same limb the frozen C1 E9 literal measures. The draft attributes them
  accordingly rather than crediting proposal 3 with the scratch clause.
- **F3 — R28 is the lesson/QUALITY row §5.1 asks for.** The spot-check's own text ("Append a
  lesson/QUALITY row citing this spot-check") makes this row and the round-36 lesson the pair that
  closes routed defect 1; landing one without the other leaves the routed item half-closed.
- **F4 — no R28/R29 collision.** Highest prior id is R27 (G5); no supersession arises, so neither row
  carries a `supersedes` clause.
- **F5 — duplication confirmed independently.** Six-term grep returns `0` for every candidate term
  (G15), and the nearest neighbours differ in mechanism rather than wording; the sibling's sweep and
  this seat's re-run agree.
- **F6 — closure-order lineage is non-monotonic, so vigilance is not the fix.** Re-read of the
  spot-check cells gives r30 defect, r31/r32 empty, r34 D4, r35 recurrence — 3 of the last 6 closure
  checks carried the class (G16). That is the calibration argument for a standing gate (R28 / C1 E9)
  rather than another per-round reminder. Cite this count, not "six consecutive".

## 6. Out of scope (not done by this seat)

- Appending the block to `corpus/QUALITY.md` (L1/integrator lands it).
- Building or running `corpus/instruments/r36-closure.sh`; E1–E9 measurement; `--selftest`.
- SKILL.md registry rows (C1's E3 target), lesson text, SCORECARD, SHONEN, LOG, PROVINCE.
- Any git mutation anywhere; any write outside this receipt and the scratch dir.

## 7. Paths and hygiene

- Receipt: `.ufo/waves/round-36/wave1/ScribeQualityRows.md` (this file).
- Scratch: `/fast/scratch/hyaku/kasegi-r36/ScribeQualityRows/` (block draft + lint), removed before
  yield.
- Tooling: none installed or upgraded; system `git 2.56.0`, `GNU bash 5.3.20(1)-release`, `grep
  (pi-uu-grep) 0.2.0`, `python3` — all pre-existing.
- Rule read: `/home/vgpnk/.omp/agent/RULES.md` not needed beyond the operator authorization quoted in
  the assignment (no install was performed).
