# kasegi — round 43

Lane `kasegi-shokunin`. Round shape: **one v2 wave declared and dispatched — `kasegi-r43-hyaku` (hyaku
run 11), 73 seats; no second wave.**

- Wave `kasegi-r43-hyaku` — **73 seats** (`counts={"spawn": 73, "resume": 0, "total": 73}`,
  `.ufo/waves/round-43/w1-dispatch.json`), registry `.ufo/waves/round-43/w1-REGISTRY.txt`, handoff
  `.ufo/waves/round-43/w1.ready` (l1 `KasegiR43`), policy `ufo-wave-policy-v2.json` (wave band 64–128,
  hard ceiling 256). Results `.ufo/waves/round-43/kasegi-r43-hyaku-results.json`; dead seats
  `<pending: seat>`.
- Role mix: executor 23, reviewer 11, scribe 10, scout 9, critic 7, mutation-tester 5, connector 2,
  sentinel 2, revenger 2, simplifier 2 — attack roles (reviewer + critic + mutation-tester)
  **23/73 = 31.5 %**.
- Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; claims freeze
  `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (`.ufo/waves/round-43/claims.json`, `freeze.txt`).
  **Judged head J = `<pending: commit>`**; **verification ref Y = `<pending: commit>`** (J + the receipt
  only). Lane tip and remote `master` = `<pending: commit>`.

## Work performed

Declared claims (frozen `.ufo/waves/round-43/claims.json`, freeze commit `4cb6d4ae`; controls committed
before any round-43 data):

- **C1 — depth:verifiability (4, held).** `corpus/instruments/r43-closure.sh` runs in export mode only
  (`--export-ref <hash>` extracts `git -C <lane> archive <hash> | tar -x` into a work dir outside the
  lane; a plain run refuses exit 2; an unresolvable ref prints its distinct `ref-not-found` red and exits
  1) and prints one `K<n> payload=… closed=0|1` line per check K1–K19, then `closed=19/19 exit=0` at Y.
  `--selftest --export-ref Y` prints nineteen graded `selftest case=K<n> … positive=pass … verdict=pass`
  lines and `selftest cases=19 failures=0`. K1–K13 carry the r42 J1–J13 payload grammar and replay limbs
  unchanged; K14–K19 are the new narrative-evidence checks (correction literals, wave-dispatch narrative
  vs results files, the round-42 placeholder promise, claims `before` literals vs their controls, quoted
  `closed=` values vs committed transcripts, freeze-record ordering). The frozen predicate fixes the
  negative-control rule — base `ab98fac9` and round-41 judged head
  `1f7464612ac4c44e39886b82e812610d3c039b13` each print `closed<19/19 exit=1` and at base every one of
  K14–K19 is open — and requires the exact base figure to be **measured during integration and quoted in
  this report, never pre-declared**.
- **C2 — coverage (8, held; capability acquisition).** The six-file claim-package contract, documentation
  only since the `ops/*` executables were lost, gains an executable gate:
  `corpus/instruments/claim-package-check.py <package-dir>` prints one `RULE <id> verdict=pass|fail` line
  for each of R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS, R-REPORT, R-NOSECRET
  and a `package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED|DEFECT exit=0|1` summary; the
  committed exemplar `corpus/instruments/fixtures/claim-package/exemplar/` must print
  `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`; nine committed defect fixtures each print
  `verdict=DEFECT exit=1` with their own rule failing; `--selftest` prints a graded line per case and
  `selftest cases=10 failures=0`, the ten cases being the nine defect classes plus the degenerate
  always-pass control, which it must reject. The exemplar is built from one public disclosed report
  captured this round as a new mined registry row, documented by `corpus/knowledge/claim-package-gate.md`;
  `claimable` stays false and the operator gates are named in the exemplar's `claim_checklist.md`.

Work items, in wave order. Each seat's receipt is `.ufo/waves/round-43/w1/<Name>.md`; the landed outcome of
each item is `<pending: seat>` until the integration pass reads its receipt.

- **ExecSuiteSkeleton** (executor) — byte-exact suite forking `corpus/instruments/r42-closure.sh` into the
  export-mode-only r43 instrument. Deliverables `ExecSuiteSkeleton.r43-closure.sh`,
  `ExecSuiteSkeleton.usage.txt`. Outcome `<pending: seat>`.
- **ExecK14Corrections** (executor) — sourceable `check_k14`: every `corrections=<n>` literal in
  SCORECARD.md/LOG.md/SHENON.md against the suite's own re-derivation, or named superseded by a committed
  `Correction (round 43)` line (RD42-1). Deliverables `ExecK14Corrections.sh`,
  `ExecK14Corrections.transcript.txt`. Outcome `<pending: seat>`.
- **ExecK15WaveNarrative** (executor) — sourceable `check_k15`: every `kasegi-rNN-<word>` dispatch
  sentence and round-total sentence in LOG.md and `corpus/lessons/*.md` against
  `.ufo/waves/round-NN/<wave>-results.json` (RD42-2/RD42-3). Deliverables `ExecK15WaveNarrative.sh`,
  `ExecK15WaveNarrative.transcript.txt`. Outcome `<pending: seat>`.
- **ExecK16Placeholder** (executor) — sourceable `check_k16`: the placeholder shape (a `## ` section body
  promising content `when the … reports`/`to be filled`/`TBD`/`placeholder`/`pending the … wave`) must be
  named unfulfilled by a `Correction (round 43)` line (RD42-4). Deliverables `ExecK16Placeholder.sh`,
  `ExecK16Placeholder.transcript.txt`. Outcome `<pending: seat>`.
- **ExecK17ClaimsBefore** (executor) — sourceable `check_k17`: whole-token `closed=`/`failures=`/`cases=`
  literals in each claims.json `before`/`after` cell against the control receipt the cell cites, or a
  committed claims erratum (RD42-8, R41 token boundary). Deliverables `ExecK17ClaimsBefore.sh`,
  `ExecK17ClaimsBefore.transcript.txt`. Outcome `<pending: seat>`.
- **ExecK18Transcript** (executor) — sourceable `check_k18`: every `closed=<n>/<m>` and
  `selftest cases=<n> failures=<k>` quoted in round-42/43 lane records must appear as a whole token in a
  committed transcript, or be marked `report-only`, or be named superseded (RD42-5). Deliverables
  `ExecK18Transcript.sh`, `ExecK18Transcript.transcript.txt`,
  `ExecK18Transcript.de09313-tee.txt`. Outcome `<pending: seat>`.
- **ExecK19Freeze** (executor) — sourceable `check_k19`: one `measured-at=` line per control receipt, the
  freeze record's `frozen_at_utc` not earlier than the latest of them nor earlier than the claims `base`
  commit (RD42-6). Deliverables `ExecK19Freeze.sh`, `ExecK19Freeze.transcript.txt`,
  `ExecK19Freeze.freeze-format.txt`. Outcome `<pending: seat>`.
- **ExecCarryChecks** (executor) — integration owner for the thirteen carried checks: proves the r42 suite
  green over a scratch export of base `ab98fac9` before copying J1–J13 function bodies into the suite as
  K1–K13, and emits the r43 declaration list. Deliverables `ExecCarryChecks.report.md`,
  `ExecCarryChecks.declared-blocks.txt`, `ExecCarryChecks.transcript.txt`. Outcome `<pending: seat>`.
- **ExecSelftest19** (executor) — the graded selftest runner block: nineteen cases, K1–K13 reusing the r42
  mutants and the r41 defeat artifacts without weakening them, K14–K19 each with a positive case, a
  mutant built from committed r42 defeat bytes, and a missing-correction negative. Deliverables
  `ExecSelftest19.sh`, `ExecSelftest19.cases.txt`. Outcome `<pending: seat>`.
- **ExecNegCtlReceipt** (executor) — the negative controls (base and round-41 head exports red, plain run
  exit 2, ref-not-found distinct) and the receipt writer: one unedited tee of one run+selftest at Y.
  Deliverables `ExecNegCtlReceipt.sh`, `ExecNegCtlReceipt.spec.txt`,
  `ExecNegCtlReceipt.transcript.txt`. Outcome `<pending: seat>`.
- **ExecTranscriptDe0931** (executor) — byte-exact teed transcript of the r42 suite over
  `de09313e8edb98280b19767d0094bb2dd8031d73`, landed at
  `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` as K18's citation substrate. Deliverable
  `ExecTranscriptDe0931.txt`. Outcome `<pending: seat>`.
- **ScribeCorrections** (scribe) — three end-of-file append blocks closing RD42-1, RD42-2, RD42-3 and
  RD42-4: each `Correction (round 43)` line names the superseded statement by file:line. Deliverables
  `ScribeCorrections.scorecard.txt`, `ScribeCorrections.log.txt`, `ScribeCorrections.lesson42.txt`.
  Outcome `<pending: seat>`.
- **ScribeClaimsErratum** (scribe) — the round-43 claims erratum naming round-42 C1's `before` literal
  `closed=10/12` superseded by the control's `closed=8/12`, and round-42 `frozen_at_utc` superseded by the
  disclosed mtime (RD42-8/RD42-6). Deliverable `ScribeClaimsErratum.claims-erratum-1.md`, landed at
  `.ufo/waves/round-43/claims-erratum-1.md`. Outcome `<pending: seat>`.
- **ScribeLessonDraft** (scribe) — the round-43 lesson in the shape of `corpus/lessons/round-42.md`: frozen
  claims table, mistake table, gate block, Y-rule references (never a hash the file cannot contain).
  Deliverable `ScribeLessonDraft.round-43-lesson.md`, landed at `corpus/lessons/round-43.md`. Outcome
  `<pending: seat>`.
- **ScribeLogEntry** (scribe) — the `## Round 43` LOG append in the round-42 entry's shape, with one bullet
  per work item, the seat and role counts taken from `w1-dispatch.json`, and no wave-dispatch sentence
  that lacks its results file (K15's input). Deliverable `ScribeLogEntry.log-entry.md`. Outcome
  `<pending: seat>`.
- **ScribeScorecardRound43** (scribe) — the `## Round 43 result` table (depth:verifiability, coverage, the
  depth:density non-target guard), move-log rows, and axis verdict wording that never says `verified`
  unless the round's own kill rule is re-derived. Deliverable `ScribeScorecardRound43.append.md`. Outcome
  `<pending: seat>`.
- **ScribeShonenLines** (scribe) — four `[~]` SHONEN evidence lines, no `## Round N evidence` heading, one
  indented evidence line per box (RD42-9). Deliverable `ScribeShonenLines.append.md`. Outcome
  `<pending: seat>`.
- **ScribeQualityRows** (scribe) — the `corpus/QUALITY.md` append block with the R6 byte/lines preamble
  freshly measured and one row per criterion the round mints. Deliverable `ScribeQualityRows.append.md`.
  Outcome `<pending: seat>`.
- **ScribeReportSkeleton** (scribe) — this report; landed at `.ufo/reports/round-43/kasegi.md`. Deliverable
  `ScribeReportSkeleton.report.md`. Outcome is the landed report itself.
- **ExecGateCore** (executor) — the gate CLI and dispatcher for the eight rules plus the `package=…`
  summary. Deliverables `ExecGateCore.claim-package-check.py` (landed as
  `corpus/instruments/claim-package-check.py`), `ExecGateCore.rules.txt`. Outcome `<pending: seat>`.
- **ExecGateManifest** (executor) — sourceable `rule_files`, `rule_manifest`, `rule_redact` to the contract
  text (six files; per-artifact sha256 recomputed, never trusted; polarity enum; relative paths).
  Deliverables `ExecGateManifest.rules.py`, `ExecGateManifest.transcript.txt`. Outcome `<pending: seat>`.
- **ExecGateChain** (executor) — `rule_custodian` and `rule_status`: non-empty decision chain,
  `NO_SCOPE_OBJECTION` scope signal, `head_sha256` chained to the manifest's expected head, and
  `claim_review` hard gates with a reviewer distinct from every producer. Deliverables
  `ExecGateChain.rules.py`, `ExecGateChain.transcript.txt`. Outcome `<pending: seat>`.
- **ExecGateProvReport** (executor) — `rule_provenance`, `rule_report`, `rule_nosecret`: the provenance
  trio, the literal `No submission performed`, cited artifact digests, and the secret-shape scan.
  Deliverables `ExecGateProvReport.rules.py`, `ExecGateProvReport.transcript.txt`. Outcome
  `<pending: seat>`.
- **ExecGateFixtures** (executor) — nine full six-file defect packages, one defect class each (missing
  sixth file, wrong digest, negative-only polarity, path escape, empty redactions, custodian head
  mismatch, reviewer identity collision, report marker/digest defect, secret-shaped token).
  Deliverables `ExecGateFixtures.defect-<k>/` payloads and `ExecGateFixtures.index.txt`. Outcome
  `<pending: seat>`.
- **ExecGateSelftest** (executor) — the ten graded cases of the gate selftest, including rejection of the
  degenerate always-pass control. Deliverables `ExecGateSelftest.selftest.py`,
  `ExecGateSelftest.transcript.txt`. Outcome `<pending: seat>`.
- **ExecExemplarPackage** (executor) — the six exemplar files built from the round's captured public
  disclosed report, `claimable` false. Deliverables `ExecExemplarPackage.report.md`,
  `ExecExemplarPackage.claim_checklist.md`, `ExecExemplarPackage.manifest.json`,
  `ExecExemplarPackage.custodian-receipts.json`, `ExecExemplarPackage.provenance.json`,
  `ExecExemplarPackage.status.json`. Outcome `<pending: seat>`.
- **ExecSourceCapture** (executor) — the complete capture of one public, first-party, login-free disclosed
  report with its normalization, manifest record and provenance. Deliverables
  `ExecSourceCapture.<id>.txt` (landed as `corpus/source-snapshots/round-43/S067.txt`),
  `ExecSourceCapture.manifest.json`, `ExecSourceCapture.provenance.txt`. Outcome `<pending: seat>`.
- **ExecRegistryRows** (executor) — the S067 registry row plus the screened reject row, eleven columns
  each, and the search-log note. Deliverables `ExecRegistryRows.rows.txt`,
  `ExecRegistryRows.searchlog.txt`. Outcome `<pending: seat>`.
- **ScoutSourceHunt** (scout) — 4–6 candidate public disclosed reports/advisories a six-file claim
  package could be built around, screened for public, first-party, login-free, no-live-target.
  Deliverable `ScoutSourceHunt.md`. Outcome `<pending: seat>`.
- **ScoutSiblingOverlap** (scout) — read-only sibling-lane and shokuknow corpus scan for overlap with the
  claim-package gate and its source. Deliverable `ScoutSiblingOverlap.md`. Outcome `<pending: seat>`.
- **ScoutR42Defects** (scout) — inventory of RD42-1..RD42-9 from `corpus/lessons/round-42-verifier-spotcheck.md`
  §7/§9.6 with each defect's committed location. Deliverable `ScoutR42Defects.md`. Outcome
  `<pending: seat>`.
- **ScoutInstrumentInventory** (scout) — the lane's committed instrument conventions (export-mode contract,
  argument names, `all-gates` header versions, selftest grading, receipt grammar). Deliverable
  `ScoutInstrumentInventory.md`. Outcome `<pending: seat>`.
- **ScoutClaimContract** (scout) — the six-file claim-package contract and the package shapes the lane
  already records, as the gate's specification input. Deliverable `ScoutClaimContract.md`. Outcome
  `<pending: seat>`.
- **ScoutCorpusCensus** (scout) — pasteable census measurements: registry rows and status histogram,
  frontier rows and admitted count, queued rows, knowledge files, captures. Deliverable
  `ScoutCorpusCensus.md`. Outcome `<pending: seat>`.
- **ScoutConsiderthese** (scout) — the one still-unimplemented `considerthese/` proposal this round can
  carry, or the refusal with reason. Deliverable `ScoutConsiderthese.md`. Outcome `<pending: seat>`.
- **ScoutAssimilation** (scout) — the §10 id-collision check in its own scratch (never writing
  shokuknow): registry ids against the assimilation package. Deliverable `ScoutAssimilation.md`. Outcome
  `<pending: seat>`.
- **ScoutQuiescenceScan** (scout) — scratch-discipline audit of every committed instrument and tool
  (hardcoded `/tmp` roots, `mkdtemp(dir=` defaults, inherited `TMPDIR`). Deliverable
  `ScoutQuiescenceScan.md`. Outcome `<pending: seat>`.
- **RevSuiteContract** (reviewer) — receipt-only review of the suite skeleton against the recorded
  conventions and the r42 instrument. Receipt `RevSuiteContract.md`. Outcome `<pending: seat>`.
- **RevK14** (reviewer) — receipt-only attack on `check_k14`: stale literal in a fenced block, two
  literals on one line, a literal inside quoted defect evidence, an unappended correction marker.
  Receipt `RevK14.md`. Outcome `<pending: seat>`.
- **RevK15** (reviewer) — receipt-only attack on `check_k15`: round number disagreeing with the path,
  hyphenated wave names, a sentence split across lines, a results file that exists but is empty. Receipt
  `RevK15.md`. Outcome `<pending: seat>`.
- **RevK16** (reviewer) — receipt-only attack on `check_k16`: a promise reworded without trigger words, a
  promise in a table cell, a correction marker placed before the promise. Receipt `RevK16.md`. Outcome
  `<pending: seat>`.
- **RevK17** (reviewer) — receipt-only attack on `check_k17`: a token in an `after` cell, a token in an
  uncited control, nested claims files, a supersede line without the token. Receipt `RevK17.md`. Outcome
  `<pending: seat>`.
- **RevK18** (reviewer) — receipt-only attack on `check_k18`: trailing punctuation, a value inside a fenced
  transcript, a transcript containing the token in a filename only. Receipt `RevK18.md`. Outcome
  `<pending: seat>`.
- **RevK19** (reviewer) — receipt-only attack on `check_k19`: forged claims digest, two `measured-at`
  lines, a missing `measured-at`. Receipt `RevK19.md`. Outcome `<pending: seat>`.
- **RevGateRules** (reviewer) — rule-by-rule review of the gate and the three rule modules against the
  contract text. Receipt `RevGateRules.md`. Outcome `<pending: seat>`.
- **RevGateFixtures** (reviewer) — per-fixture review: does each defect fixture fail for its own rule and
  not another, and is it a full six-file package. Receipt `RevGateFixtures.md`. Outcome `<pending: seat>`.
- **CritKillRule** (critic) — clause-by-clause re-derivation of C1's frozen kill rule against committed
  bytes, attempting to fire each clause. Receipt `CritKillRule.md`. Outcome `<pending: seat>`.
- **CritC2DoNothing** (critic) — C2 do-nothing controls (always-pass gate stand-in, gate reading bytes
  outside the package, degenerate selftest) scored with the frozen counters. Receipt `CritC2DoNothing.md`.
  Outcome `<pending: seat>`.
- **CritReceiptForge** (critic) — receipt-forgery battery: extra payload line, plausible unprinted value,
  a second `all-gates` header, an edited run line. Receipt `CritReceiptForge.md`. Outcome
  `<pending: seat>`.
- **CritBaselineEscape** (critic) — attack on the base-red requirement: can any K14–K19 limb go green at
  base through a degenerate path. Receipt `CritBaselineEscape.md`. Outcome `<pending: seat>`.
- **CritExemplarReal** (critic) — fabrication audit of the exemplar and its source: does the captured
  document say what the manifest claims. Receipt `CritExemplarReal.md`. Outcome `<pending: seat>`.
- **CritProvinceScope** (critic) — province check that a claim-package gate sits inside kasegi's core.
  Receipt `CritProvinceScope.md`. Outcome `<pending: seat>`.
- **CritTokenRead** (critic) — whole-token (R41) audit over every new counter: near-token mutants for
  K14–K19 and the gate's rule ids. Receipt `CritTokenRead.md`. Outcome `<pending: seat>`.
- **RevC1Freeze** (reviewer) — pre-freeze satisfiability (R22/R25) of C1: every literal and regex in the
  predicate and kill rule run against the base tree. Receipt `RevC1Freeze.md`. Outcome `<pending: seat>`.
- **RevC2Counters** (reviewer) — pre-freeze satisfiability of C2's counting commands at base, each observed
  value against the claim's `before` cell. Receipt `RevC2Counters.md`. Outcome `<pending: seat>`.
- **MutK14K15** (mutation-tester) — mutation battery on the K14 and K15 limbs (drop the stale-literal
  comparison, drop the fenced-block exclusion, and siblings). Receipt `MutK14K15.md`. Outcome
  `<pending: seat>`.
- **MutK16K17** (mutation-tester) — the same battery for K16 and K17 (drop the whole-token boundary, accept
  a supersede line without the token). Receipt `MutK16K17.md`. Outcome `<pending: seat>`.
- **MutK18K19** (mutation-tester) — the same battery for K18 and K19 (drop the report-only exception,
  accept a filename-only token, skip the claims-digest check). Receipt `MutK18K19.md`. Outcome
  `<pending: seat>`.
- **MutGateRules** (mutation-tester) — gate mutations one rule at a time (trust the recorded digest, allow
  `..` paths, accept an empty chain, accept a producer-identical reviewer). Receipt `MutGateRules.md`.
  Outcome `<pending: seat>`.
- **MutSelftestDegenerate** (mutation-tester) — degenerate-selftest battery for both instruments:
  summary-only line, forged case lines, all-pass without fixtures, summary printed after a failing case.
  Receipt `MutSelftestDegenerate.md`. Outcome `<pending: seat>`.
- **ConnCrossClaims** (connector) — cross-claim ordering and interaction map over every deliverable both
  claims read. Deliverable `ConnCrossClaims.txt`. Outcome `<pending: seat>`.
- **ConnSiblingPattern** (connector) — read-only scan of sibling-lane instruments and contracts for
  patterns to reuse rather than reinvented. Deliverable `ConnSiblingPattern.txt`. Outcome
  `<pending: seat>`.
- **SentinelScope** (sentinel) — scope watch over `.ufo/waves/round-43/w1` at start and at least three
  times, recording every out-of-scope write. Receipt `SentinelScope.md`. Outcome `<pending: seat>`.
- **SentinelMisroot** (sentinel) — misroot watch: fleet-root `git status --porcelain` at start and at
  least twice more. Receipt `SentinelMisroot.md`. Outcome `<pending: seat>`.
- **RevengerReceipt** (revenger) — reverse-engineering of how
  `.ufo/waves/round-42/final-gates/all-gates.txt` was produced, as the receipt-shape input. Receipt
  `RevengerReceipt.md`. Outcome `<pending: seat>`.
- **RevengerKillRule** (revenger) — reconstruction of why the last three closures (r40, r41, r42) died,
  as the kill-rule input. Receipt `RevengerKillRule.md`. Outcome `<pending: seat>`.
- **SimplifierSuite** (simplifier) — YAGNI review of the nineteen checks: overlap between K14 and K11's
  correction ledger, K18 and K1's transcript rule, and siblings. Receipt `SimplifierSuite.md`. Outcome
  `<pending: seat>`.
- **SimplifierGate** (simplifier) — YAGNI review of the eight gate rules and ten selftest cases.
  Receipt `SimplifierGate.md`. Outcome `<pending: seat>`.
- **ScribeKnowledgeGate** (scribe) — the knowledge entry for the new gate, with H1, the provenance trio
  (`source: S067 …`), the rule table and a real `recheck:` line. Deliverable
  `ScribeKnowledgeGate.entry.md`, landed at `corpus/knowledge/claim-package-gate.md`. Outcome
  `<pending: seat>`.
- **ScribeExemplarReport** (scribe) — the exemplar's two prose files: `report.md` with the verbatim
  `Scope excerpt` from the capture and the literal `No submission performed`, and `claim_checklist.md`
  naming `claimable` false and the operator gates. Deliverables `ScribeExemplarReport.report.md`,
  `ScribeExemplarReport.claim-checklist.md`. Outcome `<pending: seat>`.
- **ExecEntryGateRecheck** (executor) — proof that the knowledge entry's `recheck:` line is a real
  recheck: one `bash -n`-parseable, `cd`-prefixed command, exit 0 on the delivered tree and nonzero on a
  mutated gate. Deliverables `ExecEntryGateRecheck.transcript.txt`,
  `ExecEntryGateRecheck.entry-fix.txt`. Outcome `<pending: seat>`.
- **ExecC2Counters** (executor) — the ten C2 counting commands as one runnable script, each printing its
  command and its observed value. Deliverables `ExecC2Counters.bundle.sh`,
  `ExecC2Counters.transcript.txt`. Outcome `<pending: seat>`.
- **ExecCoverageMapNote** (executor) — the `corpus/README.md` append note recording that the six-file
  contract moved from documentation-only to an instrumented surface, naming the instrument, exemplar and
  fixtures. Deliverables `ExecCoverageMapNote.append.md`, `ExecCoverageMapNote.transcript.txt`. Outcome
  `<pending: seat>`.

## Landed changes

Tied to `LOG.md` §Round 43 (appended by `ScribeLogEntry`) and the commit carrying each change. Base
`ab98fac9dce87130bc4f66de89e30650d63943dc`; freeze `4cb6d4ae`.

| Change | Commit |
|---|---|
| Frozen claims, both controls (`c1-controls/do-nothing.txt`, `c2-controls/before.txt`), census-before, freeze record, wave spec/dispatch/registry (73 seats) | `4cb6d4ae` |
| `corpus/instruments/r43-closure.sh` (K1–K19) with its graded selftest, negative controls and receipt harness | `<pending: commit>` |
| `corpus/instruments/claim-package-check.py`, the three rule modules, nine `corpus/instruments/fixtures/claim-package/defect-*` packages and its selftest | `<pending: commit>` |
| `corpus/source-snapshots/round-43/S067.txt` + manifest record; `corpus/SOURCES.md` S067 row and screened reject row; `corpus/knowledge/claim-package-gate.md` | `<pending: commit>` |
| `corpus/instruments/fixtures/claim-package/exemplar/` six files (gate-clean, `claimable` false) | `<pending: commit>` |
| Append-only corrections closing RD42-1..RD42-4 (`SCORECARD.md`, `LOG.md`, `corpus/lessons/round-42.md`), claims erratum 1 (RD42-5/RD42-8/RD42-6 inputs) and `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` | `<pending: commit>` |
| `corpus/lessons/round-43.md`, `LOG.md` §Round 43, `SCORECARD.md` round-43 append, `SHONEN.md` lines, `corpus/QUALITY.md` rows, `corpus/README.md` coverage-map note, `corpus/instruments/knowledge-expected.txt` sync (61 → 62) | `<pending: commit>` |
| **Judged head J** — every round-43 change except the receipt | `<pending: commit>` |
| **Receipt Y** — `.ufo/waves/round-43/final-gates/all-gates.txt`, one unedited tee of run + selftest at J | `<pending: commit>` |

## Before → after measurements

Every command below is run from the lane root; the suite runs in export mode with a private `--work` and
`--scratch-root` outside the lane. **Before** values were re-measured by this seat at a bare export of base
`ab98fac9` (`git -C <lane> archive ab98fac9 | tar -x` into scratch) or, where the base instrument is
absent, cited from the committed control receipt with its `measured-at` line.

**C1 — depth:verifiability (4 held → 4 held).**

| # | Counting command | Before (base `ab98fac9`) | After |
|---|---|---|---|
| 1 | `bash corpus/instruments/r43-closure.sh` | instrument absent — the control's `ls` probe prints `No such file or directory`, exit 2; invoked, the absent script exits 127 (`c1-controls/do-nothing.txt`, `measured-at=2026-10-28T16:32:23Z`) | `<pending: seat>` — frozen: plain run refuses **exit 2** |
| 2 | `bash corpus/instruments/r43-closure.sh --export-ref <Y> --work <scratch>/w --scratch-root <scratch>` | r43 suite absent; the do-nothing stand-in (r42 suite, `suite-sha256=fca5ae62…`, `run-utc=2026-10-28T16:27:52Z`) over the same base export prints **`closed=12/13 exit=1`** — J8 red only because the base carries commits after the r42 receipt | `<pending: seat>` — frozen: **`closed=19/19 exit=0`** |
| 3 | `bash corpus/instruments/r43-closure.sh --selftest --export-ref <Y> …` | r43 suite absent (r42 stand-in's selftest is not this instrument's) | `<pending: seat>` — frozen: nineteen graded `verdict=pass` lines and **`selftest cases=19 failures=0`** |
| 4 | `bash corpus/instruments/r43-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc …` | — | `<pending: seat>` — the exact base figure is **measured during integration**, never pre-declared; frozen rule: `closed<19/19 exit=1` with every one of K14–K19 open |
| 5 | `bash corpus/instruments/r43-closure.sh --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13 …` | — | `<pending: seat>` — frozen: `closed<19/19 exit=1` |
| 6 | `bash corpus/instruments/r43-closure.sh --export-ref deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` | — | `<pending: seat>` — frozen: distinct `ref-not-found` red, **exit 1** (never a vacuous `closed=0/19`) |

The six routed r42 defects are present in base bytes and no check among the thirteen grades any of them
(`c1-controls/do-nothing.txt` §C): `SCORECARD.md:1634` carries `corrections=33` against the suite's own
live `corrections=34`; `LOG.md:1804` claims `wave 2 kasegi-r42-falsify 36 seats dispatched` with no
`.ufo/waves/round-42/wave2-results.json`; `corpus/lessons/round-42.md:11-16` repeats the dispatch and its
`## Wave-2 falsification` section (line 52) promises verdicts "when the round-42 falsify wave reports";
`corpus/lessons/round-42-verifier-spotcheck.md:65` and `.ufo/waves/round-42/claims-erratum-4.md:9` quote
`closed=10/13` with no committed transcript printing it; round-42 claims C1 `before` says `closed=10/12`
while its own control prints `closed=8/12`.

**C2 — coverage (8 held → 8 held; capability row enters).**

| # | Counting command | Before (base `ab98fac9`) | After |
|---|---|---|---|
| 1 | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` | instrument absent (`ls`: `No such file or directory`; `c2-controls/before.txt` records `instrument-basenames-matching-claim: 0`) | `<pending: seat>` — frozen: **`rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`** |
| 2 | `python3 corpus/instruments/claim-package-check.py --selftest` | instrument absent | `<pending: seat>` — frozen: **`selftest cases=10 failures=0`**, exit 0 |
| 3 | `grep -c '^RULE ' <(python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar)` | no instrument | `<pending: seat>` — frozen: 8 |
| 4 | `ls corpus/instruments/fixtures/claim-package/ \| grep -c '^defect-'` | directory absent | `<pending: seat>` — frozen: 9 |
| 5 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **66** | `<pending: seat>` — frozen: `>=68` (S067 mined plus one screened reject) |
| 6 | `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | **0** | `<pending: seat>` — frozen: 1 |
| 7 | `ls corpus/knowledge/*.md \| wc -l` | **61** | `<pending: seat>` — frozen: 62 |
| 8 | `python3 corpus/instruments/capture-binding-check.py` | **`records=56 bound=56 unbound=0`**, exit 0 (`AUDIT` line: `with_url=56 with_fetched_utc=18 with_archival=38 snapshot_dirs=18 manifest_dirs=18 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt`) | `<pending: seat>` — frozen: 57/57 |
| 9 | `python3 corpus/instruments/recheck-audit.py --quiet` | `lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; `expect=present expected=61 missing=0 unexpected=0 exit=0` (`c2-controls/before.txt`, in-repo run) | `<pending: seat>` — frozen: `expected=62` |
| 10 | `python3 corpus/instruments/frontier-recheck-count.py` | **`entries=28 pass=28 exit=0`** (last two rows `PASS F24 … ids=S063`, `PASS F25 … ids=S064`) | `<pending: seat>` — claim declares no frontier row change |
| 11 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **exit 0** with `W04 S028`, `W04 S029`, `kasegi ok …/corpus/SOURCES.md` | `<pending: seat>` — frozen: exit 0 |

Do-nothing control: `c1-controls/do-nothing.txt` and `c2-controls/before.txt` reach none of the after
values; the r43 suite is absent at base and the r42 stand-in is red at base. Limit on row 9: a bare
`git archive` export has no repository root, so the `cd`-prefixed rechecks fail closed there
(`strict pass=1/61 cdroot_fail=60`); the `expected=61` figure is therefore cited from the in-repo control
receipt, not from the bare-export run.

## Sources & frontier

Census command, run at round start and at round end:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

- **before** (`.ufo/waves/round-43/census-before.txt`; reproduced by this seat at base `ab98fac9`):

  ```text
  kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
  kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
  kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
  ```

  **exit 0**. Both `W04` lines are the standing duplicate-URL warnings carried since earlier rounds.
- **after**: `<pending: seat>` — the same command at Y, with its exit code and every `W`/`E` line quoted.

Counting command and its before output (this seat, base `ab98fac9`):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
```

```text
kasegi	rows	66
kasegi	tier.A	61
kasegi	tier.B	3
kasegi	tier.C	2
kasegi	status.mined	54
kasegi	status.rejected	12
FLEET	rows	66
FLEET	tier.A	61
FLEET	tier.B	3
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	0
FLEET	status.mined	54
FLEET	status.rejected	12
FLEET	status.invalid	0
FLEET	missing	0
```

**exit 0**. After: `<pending: seat>`.

- Rows **66 → `<pending: seat>`**; added by tier `<pending: seat>`. The declared addition is the mined
  S067 row (tier fixed by its first-party status: a vendor advisory or the disclosing party's own write-up
  is A, a news piece or aggregator is B) plus at least one screened reject row with reason + flip.
- Rows touched old→new: `<pending: seat>` — the declared target is that no pre-existing
  S001–S066 status/recheck/used-by cell changes.
- Frontier rows advanced: **none.** No `F` row enters this round; the harness measured
  `entries=28 pass=28 exit=0` at base and the claim declares no change, so F25 remains the newest
  frontier entry. `<pending: seat>` for the Y tick.
- Assimilation: `<pending: seat>` — `ScoutAssimilation.md` must name the audited package path and state
  whether anything was adopted; nothing in `corpus/` is written from shokuknow.

## Trend verdicts

- **expansion — `<pending: seat>`.** Deciding evidence: the registry row delta (66 → `<pending: seat>`)
  and the capability row `claim-package-gate` entering `SCORECARD.md` with the gate command as its
  evidence pointer. Expansion here is a capability acquisition, not a frontier admission: the harness
  entry count stays 28 (`entries=28 pass=28 exit=0` measured at base), and the coverage score stays held
  at 8.
- **quality — `<pending: seat>`.** Deciding evidence: the C1 counter moved from an absent instrument at
  base to `<pending: seat>` at Y with nineteen graded selftest cases, while the r42 stand-in is
  `closed=12/13 exit=1` over the base export; the C2 gate must print `rules=8 pass=8 fail=0` on the
  exemplar and `verdict=DEFECT exit=1` on each of nine defect packages with its own rule failing, and
  `selftest cases=10 failures=0`. The six routed r42 defects are quoted above with their file:line
  locations; the corrections that name them are `<pending: seat>`.
- **discernment — `<pending: seat>`.** Deciding evidence: the round's claims were frozen with committed
  controls before any data, and the negative-control limbs are declared as literals rather than measured
  after the fact. A concrete move already visible at freeze: round 42's C2 after-state quoted
  `measure 45/45 = 1.000`, which round-42's own critics found asserted and uncommanded
  (`wave1/RevC2Shape.md:152`: "No measure (45/45 = 1.000) command was exercised: it is not in the nine
  counting commands and its tool is not named"); round 43's C2 after-state carries ten named counting
  commands instead and no measure literal, and this report's measurement section therefore runs only
  counters that exist as commands. Whether the non-author sampling closes the claim is `<pending: seat>`.

## SHONEN

- `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence: the
  `r43-closure.sh` registry row and the re-measured no-harm limb; at base `density.py SKILL.md` prints mean
  **234.2** over 30 blocks (1134 lines, 782 path-citation instances, exit 0, `density.py` sha256
  `ee803726a322…`) and `anchorcheck.py SKILL.md` exits 0 with `16 in-range cite instances, 0 bad;
  LOST-RECORDED=306 PIN-BROKEN=0`; the post-append row check and re-measurement at J are
  `<pending: seat>`. No non-author check.
- `[~]` At least one end-to-end domain task executed and logged in LOG.md — evidence: no live end-to-end
  hunt ran; the executed work is instrument construction and corpus curation (the S067 capture with its
  manifest and `source-recheck`, the gate and its exemplar, the C1 suite). The LOG pointer is
  `LOG.md` §Round 43, whose entry is `<pending: seat>` until `ScribeLogEntry` lands.
- `[~]` Instructions executable by an agent without oral context — evidence: every counter runs from
  committed bytes with no oral context; the frozen before-state is committed at `4cb6d4ae` with both
  controls, and the base measurements in this report were produced by bare-export runs. The after-state
  (Y `closed=19/19 exit=0`, `selftest cases=19 failures=0`, gate `rules=8 pass=8`, `selftest cases=10`,
  the ten C2 counters, census exit 0) is `<pending: seat>`; pointer
  `.ufo/waves/round-43/final-gates/all-gates.txt`. No non-author check.
- `[~]` No cross-domain bleed (PROVINCE.md still accurate) — evidence: `PROVINCE.md` is 165 lines, sha256
  `8deea5ea1c58…`, and carries no round-43 amendment at base; the claim-package gate sits in the core
  already occupied by the claim-package contract, and its only province question is whether the gate
  widens that core (`CritProvinceScope.md`, `<pending: seat>`). `ScoutSiblingOverlap.md` is
  `<pending: seat>`. No province edit is claimed beyond whatever that ruling requires.

## Extras

- **Stale-lane:** respawn-per-round driver; no other mission of this lane is open.
- **Tool installs:** none this round — no `pacman` transaction (host-wide pause), no `uv tool install`,
  `npx` package or release binary was installed or upgraded by any seat.
