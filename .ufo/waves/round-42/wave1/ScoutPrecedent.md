# ScoutPrecedent — round-42 wave-1 receipt (escape-class sweep)

Seat: `ScoutPrecedent` (scout, leaf — no subagent dispatch). Route chain at
spawn: L1 KasegiR42 (inline spawn handoff, hyaku run 10) -> ScoutPrecedent.
Axes touched: depth:verifiability (primary), coverage (the uncovered classes
X-01..X-04/X-06 are corpus-side). Frozen claims read first:
`.ufo/waves/round-42/claims.json` (sha256 of the file not recomputed; contents
quoted in work notes — C1 names the seven families F-EVID/F-TOKEN/F-TABLE/
F-DECL/F-SCAN/F-BIND/F-FLIP plus J8-J13; C2 admits F25 + S064).

## Item and scope

Sweep `round-39/wave2/`, `round-40/wave2/`, `round-41/wave2/` receipts for
escape classes that recur; name which r42 family covers each; flag classes
NOT covered by J1-J13 as wave-2 ammunition. Read-only sweep; no lane byte
outside this receipt and the deliverable was written.

## Deliverable

- `.ufo/waves/round-42/wave1/ScoutPrecedent.txt` — 156 lines, 10664 bytes,
  sha256 `6b3c3a7ba13fa248dbbe3a7dec2a73dedc575b3b0944065f8f5a693bed982908`.
  Landable bytes only: 19 recurring covered classes (EC-01..EC-19), 8
  uncovered/partial classes (X-01..X-08), one-round-only tail list.

## What was run (actual commands and output)

- `ls .ufo/waves/round-{39,40,41}/wave2/` — 46 + 58 + 26 files (r39 has 46
  receipt/artifact entries; r40 58; r41 26; counted by listing).
- `grep -rliE 'escape|bypass|forg|blind' <three wave2 dirs>` — 115 files;
  then class-keyed greps: substring 13, fence-family 79, forg/count 88,
  environment/UTC/TMPDIR 152, symlink 17, transcript/quote 99,
  scratch/stray 171 (raw signal counts; survivors list was then built by
  reading the attack receipts).
- `grep -rn -iE 'surviv' <three wave2 dirs>/*.md` — the master survivor
  ledger; every `survived`/`SURVIVED` verdict was read in context and mapped.
- Full reads: `round-40/wave2/CritKillRule.md` (7 escape states F1-F8),
  `CritReceiptForge.md` (7 forged-receipt variants), `RevC1Counters.md` +
  `.defeats.txt` (D1-D8), `round-41/wave2/CritC1KillRule.md`,
  `MutSkillTablePipes[.findings].md`, `MutScratchTiming`, `MutFrontierParser`,
  `CritDigestSelftest`, `CritDeclarationCoverage`, `CritI12Necessity`,
  `CritUpstreamAuthenticity`, `CritCommitTimestamp`, `CritReceiptBootstrap`,
  `CritC2Live`, `CritYDeltaClean`, `RevScanOwnership`,
  `RevCaptureNormalization`, `MutAncestorGuard`, `MutAuditUnexpected`,
  `MutBindingExistence`, `MutC2Chain`, `MutExportRecheck`,
  `MutExportRefReemit`, `MutFreshnessCensus`, `MutSuite[.findings]`,
  `RevC1Counters` (r41); r39: `CritC1Kill`, `CritG1Exploit`, `CritG2Exploit`,
  `CritG4Exploit`, `MutSelftestGrading`, `MutSuiteLimbs`, `CritMutantAssault`,
  `CritOverclaimScan`, `MutCorrectionBlocks`, `MutFixedPins`, `MutC2Row`,
  `MutJunk`, `MutFrontierRow`, `CritC2Kill` (b1-b5/c1-c2 tables);
  r40: `MutH1H5`, `MutH6H10`, `MutCountingCommands`, `MutEntries`,
  `MutRegistry`, `MutHarness`, `CritC2Fabricate`, `CritCounterSoup`,
  `CritCrossAxis`, `CritSourceTruth`, `LabExportClean` (survivor table).
- Routed-defect anchors re-read: `corpus/lessons/round-41-verifier-spotcheck.md`
  §5 (I1/I3/I7/I5-I12/I6 outside-root/capture-binding/frontier-flip queue +
  D-r41-1..5) and `corpus/lessons/round-40-verifier-spotcheck.md` §5 (D1-D7).
- Spot-verification greps before landing: `grep -n 'evidence=' r41 RevC1Counters`
  (I1 union at lines 902-906 confirmed); `grep -n 'b3 ' r39 CritC2Kill`
  (PASS ids=S054 confirmed); `grep -n '1 of 41' MutEntries` (40 survivors
  confirmed); `grep -n 'SURVIVED' MutC2Chain` (status-flip survived
  confirmed).

## Findings summary (detail in the deliverable)

19 recurring covered classes mapped: EC-01 substring/value (J2 F-TOKEN),
EC-02 fence-blindness (J1 F-EVID), EC-03 count-relative forgery (J8+J9),
EC-04 environment-dependence (J5+J13), EC-05 symlink escapes (J4+J5+J13),
EC-06 missing-transcript quotes (J8), EC-07 shape-only grading (J8+J10),
EC-08 union-aggregation (J1 F-EVID), EC-09 declaration completeness (J4
F-DECL), EC-10 name-family normalization (J5 F-SCAN), EC-11 fail-open root
(J5+J13), EC-12 literal-marker spelling (J5/I11 lineage), EC-13 foreign-ref
games (J8+J9), EC-14 status-flip blind spot (J7 F-FLIP), EC-15 binding
granularity (J6 F-BIND), EC-16 selftest-attribution/isolation (J10), EC-17
duplicated corrections (J11), EC-18 corpus-deletion blindness (J12), EC-19
scratch quiescence/stale work (J13).

8 uncovered or partial classes flagged for wave 2: X-01 lane-bound `cd` in
`recheck:` lines (recheck validates the lane, not the export — demonstrated
r39 C-ESC and r41 MutExportRecheck); X-02 entry-content drift (40/41 mutant
survival on the three gates; r39 b3/b4 swaps PASS); X-03 registry-row
orphan acceptance (S999 stays bound+census-clean); X-04 registry-cell drift
below E/W granularity (kind/status/tier/second-URL silent); X-05
dispatch/results identity binding (r39 G4 — surface retired, verify no
unbound wave-accounting limb); X-06 quote-evasion counting (hyphen-join +
URL-colon location) on the <=25-word rule — partial; X-07 duplicated
scanner-implementation drift (I6 in-suite vs standalone) — design risk, not
a family; X-08 committed-defeat-replay absent — the meta-class the kill
rule already names (any skipped J1-J7 replay limb is ammunition by the
freeze's own wording).

## Confidence and remaining unknowns

High confidence on the class-to-family mapping (each mapping cites the
receipt file and, where useful, the payload string). Unknowns: whether the
r42 suite (not yet landed at sweep time) replays the QUALITY.md
criterion-row-in-fence variant under F-EVID, and whether the C2-side
screened-reject gate enforces a hyphen/URL-safe word counter (X-06) — both
noted inline.

## Hygiene / tooling / network

- Disk guard `status` run before the pass: `/fast/scratch/hyaku` 27% used,
  591.7G free — green.
- No tools installed or upgraded; no pacman (paused); bash 5.x + coreutils +
  grep sufficed (tooling record: none installed, authorization unexercised).
- No network fetches. No mutating git/jj command anywhere (read-only
  `git archive`-free sweep; not even a fixture repo was needed — every claim
  was verified against committed receipts by `grep`/`sed`/read).
- Writes: only this receipt and `ScoutPrecedent.txt` in
  `.ufo/waves/round-42/wave1/`; scratch
  `/fast/scratch/hyaku/kasegi-r42/ScoutPrecedent/` removed before yield
  (explicit `rm -rf` after the deliverable was copied out).

Report: .ufo/waves/round-42/wave1/ScoutPrecedent.md
