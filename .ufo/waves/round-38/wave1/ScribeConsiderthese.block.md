## considerthese 2026-10-26 dispositions

Ledger: `corpus/knowledge/considerthese-proposals-ledger.md`. The seven are the items under
`considerthese/2026-10-26.md` § Self-improvement suggestions. Round 38 mines proposal 3 and leaves 1, 2,
4, 5, 6 as the ledger records them. The ledger's round-37 section
(`## Round-37 dispositions (appended 2026-10-26, R31 home)`, L37) landed as an empty heading at the
claims-freeze head `9a10b02f` — the L1-found defect D-F — and this round fills it under G7 with one row
per proposal, so each old → new below is the lesson half of an R31 disposition and that section the
durable half. The tracked path is also where the round-37 two-path conflict resolves: the freeze names
`corpus/knowledge/considerthese-proposals-ledger.md`, and `corpus/considerthese-ledger.md` is in no tree
(`git cat-file -e 9a10b02f:corpus/considerthese-ledger.md` → fatal, absent).

1. **Distance-to-next-score thresholds** — `open`, unchanged (the round-37 dispositions row for proposal
   1). Round 37 recorded the gap line (`gap: 24 of 47 rechecks still gated on a lost base; score 5 needs
   0 gated unsupported claims`); the static read this round is
   `grep -c 'Threshold for 8' SCORECARD.md` → `0` at `9a10b02f`, so §Saturation (`SCORECARD.md:309`)
   still declares the 9/10 line and no promotion threshold for either axis.
2. **End-to-end domain task round** — `open`, unchanged (row 2). `SHONEN.md:173-174` keeps box 2 at
   `[~]` with "no new end-to-end domain hunt ran"; this round again spends its work on a closure suite
   and one coverage admit, not on a priced claim package.
3. **Quiescence gate before `complete`** — `mined` round 36 → `mined` round 38, same class, wider check
   (row 3). What the proposal points at, opened this round: round 35 is `rejected-honest-stop` with both
   frozen kill rules firing at the judged revision and the missing bytes landed after `complete kasegi
   round=35` (04:00:34) and after filing — `8ce6fb4` 04:01:12, `5a25337` 04:02:21, `bb2dc8c` 04:04:46,
   `48e6053` 04:04:55 (`corpus/lessons/round-35-verifier-spotcheck.md:10-20`), which that spot-check
   names M35-1, wave writes after `complete`. Round 36 routes the same order again: `complete` 13:02:47,
   lane commit `c20300df` 13:41:37, erratum `1c43fd8f` 13:41:38
   (`corpus/lessons/round-36-verifier-spotcheck.md` §5 D3). Round 37 again: `complete` 15:02:47, lane
   commit `83975acc` 15:03:15 (`corpus/lessons/round-37-verifier-spotcheck.md` §5 D3), and §5 D-E finds
   `/fast/scratch/hyaku/kasegi-r37/build-spec.py` still present.

   Round 36 had landed the criterion (QUALITY R28) and a suite limb (`r36-closure.sh:93-108`, E9); round
   37 rewrote E9 fail-closed, added E14 to shape-check that the fail-closed status read stays in the
   committed bytes, and added E10 to bind the committed positive run. Both routed defects recurred
   anyway. Two faces were unchecked. E9 counted leftover *seat directories* — the read is
   `find "$sroot" -mindepth 1 -maxdepth 1 -type d` (`r36-closure.sh:475`) — so a leftover file reads
   quiescent. And nothing read the order, so a lane that is quiescent when the suite runs can commit
   afterwards.

   Round 38 puts both faces in the closure suite. G4: every `.ufo/waves/round-38/*-dispatch.json` in the
   export has a tracked sibling `*-results.json` that parses as JSON and lists exactly as many seats as
   the dispatch's `taskCall.tasks`, so the wave results are in the judged head before the report (D3,
   M38-4). G6: live scratch quiescence with the any-entry rule — `kasegi-r36` and `kasegi-r37` hold
   zero entries or are absent, and `kasegi-r38` holds nothing but the suite's own `--work` dir (D-E,
   M38-6). QUALITY **R33** (round-38 append-only block) records the criterion: the judged head carries
   every round artifact including the wave results, lane files name the judged head by reference to the
   gate receipt rather than by a hash they cannot contain, and the report is filed after the last lane
   commit. The status stays `mined`: a check binds the next round's evidence, not the intent of the lane
   that writes it.
4. **Cap or externalise wave evidence** — `open` (operator-owned), unchanged (row 4). Measured at
   `9a10b02f`: 7,352 tracked files, 7,069 of them under `.ufo/` (96.2 %); 121,114,796 tracked blob
   bytes, 115,132,709 under `.ufo/` (95.1 %); `.gitattributes` carries no LFS rule
   (`grep -c filter=lfs` → `0`). The round adds wave evidence; nothing in it externalises or prunes.
5. **Land the owed F18 `PROVINCE.md` amendment** — `mined`, unchanged (row 5): `PROVINCE.md:77`
   carries the F18 amendment appended in round 36 for the round-35 admission.
6. **Re-tune cadence and depth** — `open`, unchanged (row 6): no change is recorded for it in this
   lesson or in the ledger section the round fills.
7. **Proposal-status ledger** — `mined` at round 37 (QUALITY R31 plus the ledger itself), row 7. What
   round 37 left incomplete is the row set — the empty heading above — and G7 is its fill, not a new
   proposal.
