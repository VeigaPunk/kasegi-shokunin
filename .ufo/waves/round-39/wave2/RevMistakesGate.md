# RevMistakesGate — round 39, wave 2 (falsify) — receipt

Seat: RevMistakesGate (leaf, reviewer). Item: verify the round-39 lesson `## Mistakes` rows — each row has
class, evidence pointer (resolvable at the cited commit), captured-by, and fix; each fix shown able to fail
(named red state exists, or the G-limb rejects the mutant); no placeholder tokens; QUALITY criteria
R34/R35/R36 cite their lesson rows and the lesson rows cite the criteria. Receipt only; non-author.

State audited: lane HEAD = Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`; J = `46c66c268502abd1b2c342fc71bf88ccf721845b`
(receipt `export-ref=`); base `480b1a505a2dfc14a4f718d16d63808247214d0a`; freeze `dcd31701720a6a4929a32471a62011ed87103421`.
`git diff --name-only J Y` → `.ufo/waves/round-39/final-gates/all-gates.txt` only (measured). sha256 of
`corpus/instruments/r39-closure.sh` = `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b`
= the receipt's `suite-sha256` (measured). Lesson committed at J (blob `e90c0daf0037bb128b6d962084c9f1295b2a54b5`).
Tracked tree clean; untracked = wave-2 runtime only (incl. `final-gates/reds.txt`, see F2).

## 1. Row-by-row verdicts

Table shape verified: header `| id | class | event | evidence | captured-by | fix | able to fail |`; all four
rows (M39-1..M39-4) have every cell filled. Placeholder scan over the whole lesson:
`grep -nE '⟨pending|⟨TBD|TODO|FIXME|lorem|PLACEHOLDER|<pending>|<TBD>' corpus/lessons/round-39.md` → no matches
(the C1 kill-rule token `⟨pending` count = 0).

### M39-1 (stale-premise / claim hygiene) — evidence resolves; fix landed; able-to-fail red state confirmed (count figure imprecise, F3)

- Evidence resolves. r38 `claims.json` C1 predicate (frozen at `9a10b02`, last commit touching the file):
  "prints `closed=8/8 exit=0` on the round-38 judged head J". r38 receipt
  `.ufo/waves/round-38/final-gates/all-gates.txt`: `:2` `export-ref=66703acaaff50529a35be49aa8759d04140720ad`,
  `:8` `export-ref-run: G2 payload=receipt=0,… closed=0`, `:15` `export-ref-run: closed=7/8 exit=1` — exactly
  the row's quote. Verifier R1 exists at `corpus/lessons/round-38-verifier-spotcheck.md:155-160` (file
  unchanged base..Y, measured).
- Captured-by accurate: no QUALITY criterion existed at r38; R34 minted this round (see §2).
- Fix landed: erratum E4 (verification ref Y = J + receipt; measured `git diff --name-only J Y` = the receipt
  alone); suite header "GREEN WINDOW" (r39-closure.sh :56-70) documents the same.
- Able-to-fail: the named red state EXISTS — first-hand run over J (isolated `--scratch-root`/`--work` under
  my scratch):
  ```
  $ bash corpus/instruments/r39-closure.sh --export-ref 46c66c268502abd1b2c342fc71bf88ccf721845b \
      --work $S/iso-j/work --scratch-root $S/iso-j
  G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,…,graded-cases=0,… closed=0
  G8 payload=pin-ref=2387dcf6…,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=0,r37-exit=1 closed=0
  closed=6/8 exit=1      (EXIT=1)
  ```
  G2 `receipt=0` confirmed structurally. But the cell says "prints 7/8"; at the final head it prints **6/8**
  (G8 also red — see F3). The 7/8 figure is the HEAD==J overlay value (wave-1 build results recorded
  `overlay_run_at_J_head_J: closed=7/8`, `overlay_run_at_J_head_Y: closed=6/8` — my run matches the latter).

### M39-2 (evidence-record) — evidence resolves at base; fix substance landed 5/5; **frozen verification command fails on LOG.md (F1, the item's medium finding)**

- Evidence resolves at base `480b1a50` (all read; each overstates as claimed):
  - `corpus/lessons/round-38.md:21` — frozen C1 row: "`closed=8/8 exit=0` and `selftest cases=8 failures=0`
    over the judged head are the receipt".
  - `:94` — Gate readiness item 8: "`--export-ref J` → `closed=8/8 exit=0`".
  - `SHONEN.md:185` — "r38 suite run + selftest over the judged head: export-ref of …all-gates.txt (raw
    transcript committed there)".
  - `LOG.md:1698` — "Run and selftest over the judged head: `.ufo/waves/round-38/final-gates/all-gates.txt`".
  - `SCORECARD.md:1517` — "the run over the round-38 head the receipt names, and its `--selftest`, are
    committed in …all-gates.txt".
  The r38 receipt contradicts each (J-run 7/8, G2 `receipt=0`; the 8/8 + 8/0 are over `run-ref=7dd2fcd6…`).
- Fix substance landed and committed at J, content accurate (each block names the receipt's actual values):
  `corpus/lessons/round-38.md:311` (covers both :21 and :94, cites receipt :2/:8/:15/:26/:73/:4, "retained as
  history"), `LOG.md:1704` + summary `:1711`, `SCORECARD.md:1560` + `:1579` (f06148c6 report-only),
  `SHONEN.md:190`. No existing bytes rewritten (suite G1 `pure-append=1,corrections-declared=1` in my Y-run).
- **Able-to-fail command FAILS on the landed bytes.** The row's named command (also erratum E5 item 7, "at
  least 1 per file at the judged head"):
  ```
  $ grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
  corpus/lessons/round-38.md:1
  LOG.md:0            ← required >= 1
  SCORECARD.md:2
  SHONEN.md:1
  ```
  Same at J via `git grep -c '^Correction (round 39)' 46c66c2… -- …` → SCORECARD 2, SHONEN 1, round-38.md 1,
  **LOG.md absent (= 0)**. Cause: the LOG correction is bullet-prefixed — `LOG.md:1704` starts
  `- **Correction (round 39):**` — so the anchored pattern cannot see it (unanchored grep finds it; content
  is accurate). The named red state fires on the honest delivered state: the fix is unverifiable by its own
  frozen command for LOG.md. This is the same frozen-command-vs-landed-bytes class the round itself minted
  (M39-1/R34). At base the command shows 0 in all four files (red state before the fix — verified, exit 1).

### M39-3 (evidence-record) — evidence resolves; fix landed; G-limb rejects the mutants (first-hand)

- Evidence resolves. The r38 report is the fleet file `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md`:
  `:37` quotes `--export-ref f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` (tip = J + receipt only) →
  `closed=8/8 exit=0` + `selftest … cases=8 failures=0`, "Run by the L1 at 19:1xZ" — with no committed
  transcript. "Commit grep 0 hits" reproduced first-hand:
  `git grep -c f06148c6 f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` → no output, exit 1 (a commit cannot carry
  its own run). Verifier R3 at spotcheck `:168-171` ✓.
- Fix landed: G3 in the suite; receipt committed at Y (`all-gates.txt` blob `fa41b999…`, added at the Y
  commit — `git ls-tree J -- …/final-gates/` is empty, at HEAD exactly one blob). SCORECARD `:1579` carries
  the `report-only` label for the f06148c6 quote.
- Able-to-fail (G-limb), first-hand selftest rerun at Y:
  ```
  selftest detail=G3 control=quoted-run-transcribed accepted=1 payload=added-quotes=1,covered=1,uncovered=0,…
  selftest detail=G3 mutant=quote-without-transcript rejected=1 limb=uncovered=1
  selftest detail=G3 mutant=transcript-outside-final-gates rejected=1 limb=uncovered=1
  selftest case=G3 positive=pass mutants=2/2 verdict=pass
  ```
  Exactly the cell's claim: a quoted run without transcript (and the transcript-outside-final-gates variant)
  reds G3. (Caveat on the fix cell's "receipt + reds committed at Y": reds.txt is NOT committed — F2.)

### M39-4 (evidence-record) — evidence resolves; fix landed; able-to-fail shown both directions

- Evidence resolves: at base, `git grep -cE 'M38-5|M38-7' 480b1a50 -- corpus/QUALITY.md` → no output, exit 1
  (0 hits — the row's "QUALITY.md greps (0 hits)"); verifier R4 at spotcheck `:172-174` ✓; base
  `corpus/lessons/round-38.md:287` and `:289` are the M38-5 / M38-7 rows (read).
- Fix landed: R36 row (QUALITY.md:309) cites M38-5 and M38-7 with the base measurements
  (`grep -c 'M38-5'` → 0, `grep -c 'M38-7'` → 0, against M38-1/2/4 → 1 each) and states the executable form.
  `grep -cE 'M38-5|M38-7' corpus/QUALITY.md` at Y → 1 ✓ (≥1 per E5 item 8).

## 2. QUALITY criteria ↔ lesson rows (bidirectional) — VERIFIED

- R34 (QUALITY.md:307) "grounded in" = **M39-1** (`corpus/lessons/round-39.md` § Mistakes, minted this
  round) — the r38 G2/J contradiction, routed as R1 (spotcheck :155-160 quoted in the row).
- R35 (QUALITY.md:308) = **M39-3** — routed as R3 (spotcheck :168-171 quoted; base measurement
  `git grep -c f06148c6 f06148c6` → 0 recorded in the row).
- R36 (QUALITY.md:309) = **M39-4** — routed as R4 (spotcheck :172-174 quoted); the row also cites M38-5 and
  M38-7 and cross-states "R34 cites M39-1 and R35 cites M39-3".
- Lesson rows cite the criteria: M39-1 fix cell "R34 criterion added this round (pre-freeze dry-run over a
  stand-in head)"; M39-3 captured-by "none — R35 criterion added (committed transcript or report-only label)";
  M39-4 captured-by "none — R36 criterion added". ✓
- M39-2 carries no QUALITY criterion; its captured-by cell states the reason ("none — corrections sweep this
  round (R2)"). Consistent with R36's own text ("…or the round states in the lesson why not"); noted, not a
  defect.

## 3. First-hand suite runs (isolated scratch root; suite prints `deviation=non-default --scratch-root`)

- J-run: `closed=6/8 exit=1` — G1,G3,G4,G5,G6,G7 `closed=1`; G2 `receipt=0…closed=0`; G8
  `r37-closed=0,r37-exit=1 closed=0`.
- Y-run: `closed=7/8 exit=1` — G2 fully green (`receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,
  digest-match=1,export-suite=1,run-lines=8,distinct-ids=8,closed-line=1,graded-cases=8,ungraded-cases=0,
  selftest-summary=1,…closed=1`); G8 red (`r37-closed=0,r37-exit=1`) — environmental: G8 executes the pinned
  r37 suite whose E9 needs live HEAD == exported ref and a clean tree (suite comment :1625: "a ref that is
  not the lane HEAD breaks the r37 suite's E9 head limb"); HEAD=Y≠J for the J-run, and 5+ untracked wave-2
  entries dirty the tree for the Y-run. The committed receipt's `closed=8/8 exit=0` + `selftest cases=8
  failures=0` (run-utc 21:35Z, pre-wave-2, clean tree) remain the canonical green evidence; my Y-run
  reproduces every G2 graded limb but cannot reproduce G8's live limb mid-wave.
- Selftest at Y: 8 cases run; G1 4/4, G2 8/8, G3 2/2, G4 6/6, G5 4/4, G6 4/4, G7 3/3 — all `positive=pass
  verdict=pass`; G8 `positive=fail mutants=3/3 verdict=fail` (same environmental live limb);
  `selftest cases=8 failures=1`; forged judges 6/6 rejected; `selftest judge=own-report accepted=0`
  (fail-closed given G8's environmental fail). Exit 1 — environmental, not a suite defect.

## 4. Findings by severity

- **F1 (medium — M39-2 fix verification).** The frozen able-to-fail command
  `grep -c '^Correction (round 39)' …` (erratum E5 item 7: ≥1 per file at the judged head) returns **0 for
  LOG.md** at J and Y: the LOG correction landed as a bullet (`- **Correction (round 39):**`, LOG.md:1704,
  committed at J, content accurate). The correction substance is real (5/5 records swept) but the fix's own
  named measurement cannot turn green on the delivered bytes — an honest verifier following the frozen
  command false-reds LOG.md. Same class as M39-1 itself. Route to round 40 (per the frozen-rule discipline:
  a rule changed after scoring is not the claim's rule): either an anchored `Correction (round 39):` line in
  LOG.md in a post-Y commit, or an erratum restating the command unanchored.
- **F2 (low — M39-3 fix cell).** "receipt + reds committed at Y": the receipt IS committed at Y (diff J..Y =
  the receipt alone); **reds.txt is not committed** — untracked (`?? …final-gates/reds.txt` in
  `git status --porcelain=v1 -uall`), absent from the index and from the J and Y trees, no commit history,
  not gitignored (`git check-ignore -v` exit 1). Committing it AT Y is impossible under the frozen
  judged-head rule (diff J..Y must be the receipt only), so the cell overstates. The reds evidence that IS
  committed: `wave1/ExecSuiteBuild.md:107` (base run `closed=1/8 exit=1`) and the full transcript
  `wave1/ExecSuiteBuild.overlay/run-at-base-live-scratch.txt` (G1-G6,G8 red, G3 vacuous-green, G6 red on live
  scratch). Also `final-gates/reds.txt` on disk lists only the G7/G8 payload lines per ref while printing
  `closed=1/8` — a partial record; the full red payloads live in the wave-1 transcripts.
- **F3 (low — M39-1 able-to-fail cell precision).** "`--export-ref J` on the final head prints 7/8": measured
  **6/8** at the final head (G2 `receipt=0` AND G8 red — G8's live limb needs HEAD==exported-ref + clean
  tree; HEAD=Y≠J). 7/8 holds only in the HEAD==J overlay (wave-1 build results: `overlay_run_at_J_head_J:
  closed=7/8`, `overlay_run_at_J_head_Y: closed=6/8` — my run matches). The structural red the cell exists to
  prove (G2 `receipt=0` at J) is confirmed; the stated count is unattainable once Y exists. Symmetrically, the
  Y-run at wave-2 runtime prints 7/8 (G8 environmental) vs the receipt's committed 8/8.
- **F4 (low — E4 wording vs receipt).** E4: the J-run is "expected and documented in the receipt". The
  committed receipt v3 carries **no J-run line** (`grep -E 'receipt=0|closed=7/8|export-ref-run'
  .ufo/waves/round-39/final-gates/*` → no matches). The documentation lives in the erratum, the lesson's
  M39-1 able-to-fail cell, and the suite header — not in `all-gates.txt`.
- **Observation (out of item scope).** The r38 receipt header (:5) cites "round-38 lesson, M38-8"; no M38-8
  row exists at base (`git grep -c 'M38-8' 480b1a50 -- corpus/lessons/round-38.md` → 0, exit 1) — a dangling
  citation in the r38 receipt, not captured by any M39 row. Suggest routing with the round-40 fixtures.

## 5. Do-nothing controls verified (base-state reds)

- Corrections at base: `git grep -c '^Correction (round 39)' 480b1a50 -- <4 files>` → no output, exit 1
  (0 everywhere — the red state the fix had to move).
- QUALITY citations at base: `M38-5|M38-7` → 0 (exit 1).
- f06148c6 commit-grep at the r38 tip → 0 hits (exit 1) — reproduced.

## 6. Residual risk / verification gaps

- G8's live limb makes any first-hand suite/selftest count state-dependent while wave-2 seats hold scratch
  and untracked files exist; the committed receipt (clean-tree, 21:35Z) stays the canonical 8/8 + 8/0
  evidence. I did not rerun the base/r38-head red exports (C1 counting commands 3-4 — RevC1Receipt's item);
  the landed red evidence is untracked `reds.txt` + the committed wave-1 transcripts (F2).
- My first `git status --porcelain=v1` read listed 5 untracked entries and omitted `final-gates/reds.txt`;
  the scoped `-uall` re-read shows it. Recorded as a transient read anomaly; the current state is
  authoritative and is what F2 uses.
- Filing-time cleanliness (kill rule) is the L1's concern: reds.txt and the wave-2 receipts are untracked at
  audit time and must be committed or removed before filing.

## 7. Tooling / scratch

No tools installed or upgraded (read-only audit; pacman pause respected). Scratch
`/fast/scratch/hyaku/kasegi-r39/RevMistakesGate/` (suite work dirs under it) removed before yield.
