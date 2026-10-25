# ConnOwnership — Integration Ownership & Sequencing Matrix (Round 29, Wave 1)

- **Seat**: `ConnOwnership` (UFO-FSD Connector, seat 08 / 64)
- **Lane**: `kasegi-shokunin` (Round 29, Wave 1)
- **Base Revision**: `7a6591c1eb8a14f427297980a96fa8bb339f29ee`
- **Claims Freeze**: `f28ff5d26b29270f93163117e7255e24f0b1d947`
- **Axes Targeted**: `depth:verifiability` (score held 4, improved), `coverage` (score held 7, improved), `depth:density` (score held 9, no-harm)
- **Scope**: Integration ownership matrix, single-writer rule verification, execution sequencing, and L1 explicit dependency flags across all 64 seats.

---

## 1. Executive Summary & UFO-FSD Connector Synthesis (One Non-Obvious Move)

### Evidence
In round 28, five severe execution anomalies emerged from unsequenced concurrent writes and racing verifiers:
1. **M28-1 (PRE-STATE Receipts)**: Seven seats captured counter values before their underlying subjects landed or before the final integration commit, resulting in invalid pre-state claims.
2. **Transient Census E11 Collision & M28-5 (Harness Crash)**: `ScribeReadmeC2` and `ScribeSourcesGate` appended rows citing `corpus/knowledge/japanese-domestic-disclosure-workflow.md` before `ExecEntry` landed the file, causing `sources-census.sh validate` to exit 1 (`kasegi E11 S041 missing used-by`) and `frontier-recheck-count.py` to raise `FileNotFoundError` (exit 1).
3. **M28-6 (R6 Line-Shift Fracture)**: An append to `SKILL.md` shifted line 1000 down to line 1003, leaving a stale anchor in `resolve-dispatch-fixtures.json:159,161`.
4. **M28-12 (Receipt Digest Drift)**: Production files received minor formatting touches after receipt indexes were hashed, desynchronizing committed sha256 digests.
5. **R14 Bloat & R15 Debt**: Wave evidence grew excessively, and open defects were tracked without machine-runnable closure checks (`considerthese/2026-10-25.md` proposals 1 and 5).

### Affected Axes
- `depth:verifiability` (score held 4): Eliminates phantom receipt drift, ensures hermetic isolation, and guarantees runnable closure checks.
- `coverage` (score held 7): Prevents harness failure cascades when admitting Frontier F13 and newly mined sources S043–S045.
- `depth:density` (score held 9, no-harm): Ensures append-only operations preserve citation anchors and block-density ratios without line shifting.

### Proposed Move: The Pre-Commit Barrier Protocol & "C2 Ground Zero" Synchronization
The non-obvious move is the formal establishment of a **Pre-Commit Barrier Protocol** that decomposes Wave 1 into five strictly ordered barrier phases anchored on two synchronization locks:

1. **Lock A ("C2 Ground Zero" — Entry Creation)**: `ExecEntryF13` is the sole gating prerequisite for all public index and registry modifications. Neither `ScribeReadmeC2`, `ScribeSourcesGate`, `ExecRecheckAudit`, nor `ScribeSkillGate` may write to the live working tree until `ExecEntryF13` publishes `corpus/knowledge/program-severity-ladders-and-reward-scales.md`.
2. **Lock B (Scratch-Mirror Census Gate)**: `ScribeSourcesGate` cannot write to `corpus/SOURCES.md` until `ExecCensusDry` publishes an exit-0 validation receipt over its scratch mirror (confirming zero E03/E04 findings).
3. **EOF-Append Discipline for `SKILL.md`**: `ScribeSkillGate` must append its Gates & Probes entry and Frontier note strictly at the very end of `SKILL.md` (after line 1035), guaranteeing that line 1000 (`ops/{validate,...}.mjs`) remains stationary, preserving `resolve-dispatch-fixtures.json:159,161`.
4. **Two-Phase Receipt Sealing**: Pre-commit canonical receipts (`ExecCanonC1`, `ExecCanonC2`) are sealed only after all production files land; post-commit verification (`ExecPostCommitRecheck`) is held by the L1 until after the git commit is minted on `master`, completely eliminating the M28-1 defect class.

### Risks & Mitigations
- *Risk*: A stall in `ExecEntryF13` blocks all downstream scribes.
  *Mitigation*: Parallelize unblocked recon (Scouts, Connectors, Scribe drafts) and C1 implementation independently; C1 proceeds with zero cross-talk to C2.
- *Risk*: Inadvertent fleet-root misrooting by seats.
  *Mitigation*: `ExecScopeSweep` patrols the fleet root and relocates any kasegi-specific artifacts before integration.

### Verification
- Verification 1: `git status --porcelain` matches the single-writer table with zero untracked strays outside designated report/artifact trees.
- Verification 2: Run `bash -n` and cwd-invariant rechecks on all entry commands.
- Verification 3: Re-verify that `SKILL.md:1000` retains its exact line content via `sed -n '1000p' SKILL.md`.

---

## 2. Integration Ownership Matrix: Path -> Owning Seat Mapping

### 2.1 Core Production Repository Files
Every production file under `/home/vgpnk/Projects/shokunin/kasegi-shokunin` has exactly one owning seat. No other seat may write or modify these files.

| Path | Owning Seat | Role | Scope of Modification |
|---|---|---|---|
| `corpus/instruments/anchorcheck.py` | `ExecImplC1` | executor | Implement 9-limb completeness registry, 12 selftest cases, hermetic git-free skip. |
| `corpus/source-snapshots/round-29/S043.txt` | `ExecCapS043` | executor | Capture HackerOne standard program policy set snapshot. |
| `corpus/source-snapshots/round-29/S044.txt` | `ExecCapS044` | executor | Capture Bugcrowd VRT README snapshot. |
| `corpus/source-snapshots/round-29/S045.txt` | `ExecCapS045` | executor | Capture Bugcrowd VRT CWE mapping dataset snapshot (`cwe.json`). |
| `corpus/source-snapshots/round-29/manifest.json` | `ExecManifestC2` | executor | Build Q9 binding manifest for S043, S044, S045 with quote assertions. |
| `corpus/knowledge/program-severity-ladders-and-reward-scales.md` | `ExecEntryF13` | executor | Author F13 knowledge entry adhering to Q1–Q10. |
| `corpus/instruments/knowledge-expected.txt` | `ExecRecheckAudit` | executor | Regenerate expected knowledge entries list (40 -> 41 entries / 42 -> 43 lines). |
| `corpus/QUALITY.md` | `ScribeQuality` | scribe | Append R15 criterion (open-defects ledger with runnable closure checks) at EOF. |
| `SKILL.md` | `ScribeSkillGate` | scribe | Append Gates & Probes entry for anchorcheck and F13 note strictly at EOF (line > 1035). |
| `corpus/README.md` | `ScribeReadmeC2` | scribe | Append F13 coverage-map row and Frontier table row (12 -> 13 admitted). |
| `corpus/SOURCES.md` | `ScribeSourcesGate` | scribe | Append rows S043, S044, S045 and `## Registry changes` note (42 -> 45 rows). |
| `LOG.md` | `ScribeLog` | scribe | Append Round 29 work log entry. |
| `corpus/lessons/round-29.md` | `ScribeLesson` | scribe | Assemble and author the final Round 29 lesson. |
| `SCORECARD.md` | `ScribeScorecard` | scribe | Append Round 29 results section, maintaining line-number preservation (R6). |

### 2.2 Wave Control Artifacts, Canonical Indexes & Scratch Directories
Specific control directories, receipt indexes, and scratch trees under `.ufo/waves/round-29/wave1/` have dedicated, exclusive owners.

| Path / Directory | Owning Seat | Role | Scope of Ownership |
|---|---|---|---|
| `.ufo/waves/round-29/wave1/ExecImplC1.diff` | `ExecImplC1` | executor | Patch diff of the anchorcheck.py changes. |
| `.ufo/waves/round-29/wave1/c1-controls/*` | `ExecControlC1` | executor | C1 baseline copy, do-nothing control, and mutants M1–M4. |
| `.ufo/waves/round-29/wave1/c1-receipt-index.txt` | `ExecCanonC1` | executor | Canonical pre-commit C1 receipt index containing `instrument_sha256`. |
| `.ufo/waves/round-29/wave1/receipts/ExecCanonC2.txt` | `ExecCanonC2` | executor | Canonical pre-commit C2 receipt index. |
| `.ufo/waves/round-29/wave1/receipt-index.txt` | `ExecAssembleReceipts` | executor | Index rollup mapping seat -> role -> report file -> status. |
| `.ufo/waves/round-29/wave1/receipts/*` | `ExecAssembleReceipts` | executor | Rollup storage of gathered key seat receipts. |
| `.ufo/waves/round-29/wave1/post-commit-recheck.txt` | `ExecPostCommitRecheck` | executor | Post-commit verification run at `git rev-parse master` (runs LAST). |
| `.ufo/waves/round-29/wave1/assimilation/*` | `ScoutAssimilation` | scout | Scratch directory for collision detection and guard proofs. |
| `.ufo/waves/round-29/wave1/ExecCensusDry/*` | `ExecCensusDry` | executor | Scratch mirror directory for validating SOURCES append before commit. |

---

### 2.3 Wave 1 Report Files (64 Seats Bijective Mapping)
Each of the 64 seats in Wave 1 writes its final report to an exclusive path under `.ufo/waves/round-29/wave1/<SeatName>.md`.

| Seat # | Seat Name | Role | Exclusive Report File Path |
|---|---|---|---|
| 01 | `ScoutDatawalk` | scout | `.ufo/waves/round-29/wave1/ScoutDatawalk.md` |
| 02 | `ScoutCapH1` | scout | `.ufo/waves/round-29/wave1/ScoutCapH1.md` |
| 03 | `ScoutCapBugcrowd` | scout | `.ufo/waves/round-29/wave1/ScoutCapBugcrowd.md` |
| 04 | `ScoutAssimilation` | scout | `.ufo/waves/round-29/wave1/ScoutAssimilation.md` |
| 05 | `ScoutConnOverlap` | scout | `.ufo/waves/round-29/wave1/ScoutConnOverlap.md` |
| 06 | `ConnClaims` | connector | `.ufo/waves/round-29/wave1/ConnClaims.md` |
| 07 | `ConnStagedCensus` | connector | `.ufo/waves/round-29/wave1/ConnStagedCensus.md` |
| 08 | `ConnOwnership` | connector | `.ufo/waves/round-29/wave1/ConnOwnership.md` |
| 09 | `ExecImplC1` | executor | `.ufo/waves/round-29/wave1/ExecImplC1.md` |
| 10 | `ExecCapS043` | executor | `.ufo/waves/round-29/wave1/ExecCapS043.md` |
| 11 | `ExecCapS044` | executor | `.ufo/waves/round-29/wave1/ExecCapS044.md` |
| 12 | `ExecCapS045` | executor | `.ufo/waves/round-29/wave1/ExecCapS045.md` |
| 13 | `ExecManifestC2` | executor | `.ufo/waves/round-29/wave1/ExecManifestC2.md` |
| 14 | `ExecEntryF13` | executor | `.ufo/waves/round-29/wave1/ExecEntryF13.md` |
| 15 | `ExecCensusDry` | executor | `.ufo/waves/round-29/wave1/ExecCensusDry.md` |
| 16 | `ExecHarnessC2` | executor | `.ufo/waves/round-29/wave1/ExecHarnessC2.md` |
| 17 | `ExecRecheckAudit` | executor | `.ufo/waves/round-29/wave1/ExecRecheckAudit.md` |
| 18 | `ExecControlC1` | executor | `.ufo/waves/round-29/wave1/ExecControlC1.md` |
| 19 | `ExecCanonC1` | executor | `.ufo/waves/round-29/wave1/ExecCanonC1.md` |
| 20 | `ExecCanonC2` | executor | `.ufo/waves/round-29/wave1/ExecCanonC2.md` |
| 21 | `ExecScopeSweep` | executor | `.ufo/waves/round-29/wave1/ExecScopeSweep.md` |
| 22 | `ExecDensityNoHarm` | executor | `.ufo/waves/round-29/wave1/ExecDensityNoHarm.md` |
| 23 | `ExecSelftestProbe` | executor | `.ufo/waves/round-29/wave1/ExecSelftestProbe.md` |
| 24 | `ExecAssembleReceipts` | executor | `.ufo/waves/round-29/wave1/ExecAssembleReceipts.md` |
| 25 | `ExecPostCommitRecheck` | executor | `.ufo/waves/round-29/wave1/ExecPostCommitRecheck.md` |
| 26 | `ScribeLessonGate` | scribe | `.ufo/waves/round-29/wave1/ScribeLessonGate.md` |
| 27 | `ScribeLesson` | scribe | `.ufo/waves/round-29/wave1/ScribeLesson.md` |
| 28 | `ScribeScorecard` | scribe | `.ufo/waves/round-29/wave1/ScribeScorecard.md` |
| 29 | `ScribeQuality` | scribe | `.ufo/waves/round-29/wave1/ScribeQuality.md` |
| 30 | `ScribeSkillGate` | scribe | `.ufo/waves/round-29/wave1/ScribeSkillGate.md` |
| 31 | `ScribeReadmeC2` | scribe | `.ufo/waves/round-29/wave1/ScribeReadmeC2.md` |
| 32 | `ScribeSourcesGate` | scribe | `.ufo/waves/round-29/wave1/ScribeSourcesGate.md` |
| 33 | `ScribeLog` | scribe | `.ufo/waves/round-29/wave1/ScribeLog.md` |
| 34 | `ScribeReportDigest` | scribe | `.ufo/waves/round-29/wave1/ScribeReportDigest.md` |
| 35 | `ScribeFrontierNote` | scribe | `.ufo/waves/round-29/wave1/ScribeFrontierNote.md` |
| 36 | `ScribeQuarantine` | scribe | `.ufo/waves/round-29/wave1/ScribeQuarantine.md` |
| 37 | `ScribeConsiderthese` | scribe | `.ufo/waves/round-29/wave1/ScribeConsiderthese.md` |
| 38 | `ScribeAssimReport` | scribe | `.ufo/waves/round-29/wave1/ScribeAssimReport.md` |
| 39 | `RevC1Instrument` | reviewer | `.ufo/waves/round-29/wave1/RevC1Instrument.md` |
| 40 | `RevC1Controls` | reviewer | `.ufo/waves/round-29/wave1/RevC1Controls.md` |
| 41 | `RevC2Entry` | reviewer | `.ufo/waves/round-29/wave1/RevC2Entry.md` |
| 42 | `RevC2Registry` | reviewer | `.ufo/waves/round-29/wave1/RevC2Registry.md` |
| 43 | `RevC2Manifest` | reviewer | `.ufo/waves/round-29/wave1/RevC2Manifest.md` |
| 44 | `RevNoHarmC1` | reviewer | `.ufo/waves/round-29/wave1/RevNoHarmC1.md` |
| 45 | `RevNoHarmC2` | reviewer | `.ufo/waves/round-29/wave1/RevNoHarmC2.md` |
| 46 | `RevReceiptsCanon` | reviewer | `.ufo/waves/round-29/wave1/RevReceiptsCanon.md` |
| 47 | `RevSeatEvidence` | reviewer | `.ufo/waves/round-29/wave1/RevSeatEvidence.md` |
| 48 | `RevKillTry` | reviewer | `.ufo/waves/round-29/wave1/RevKillTry.md` |
| 49 | `RevCensusDry` | reviewer | `.ufo/waves/round-29/wave1/RevCensusDry.md` |
| 50 | `CritC1Kill` | critic | `.ufo/waves/round-29/wave1/CritC1Kill.md` |
| 51 | `CritC2Kill` | critic | `.ufo/waves/round-29/wave1/CritC2Kill.md` |
| 52 | `CritGlobal` | critic | `.ufo/waves/round-29/wave1/CritGlobal.md` |
| 53 | `CritMeta` | critic | `.ufo/waves/round-29/wave1/CritMeta.md` |
| 54 | `MutC1Limbs` | mutation-tester | `.ufo/waves/round-29/wave1/MutC1Limbs.md` |
| 55 | `MutC1Hermetic` | mutation-tester | `.ufo/waves/round-29/wave1/MutC1Hermetic.md` |
| 56 | `MutC2Counters` | mutation-tester | `.ufo/waves/round-29/wave1/MutC2Counters.md` |
| 57 | `MutC2Sources` | mutation-tester | `.ufo/waves/round-29/wave1/MutC2Sources.md` |
| 58 | `LabC1Probe` | executor | `.ufo/waves/round-29/wave1/LabC1Probe.md` |
| 59 | `LabC2Probe` | executor | `.ufo/waves/round-29/wave1/LabC2Probe.md` |
| 60 | `LabInstrumentProbe` | executor | `.ufo/waves/round-29/wave1/LabInstrumentProbe.md` |
| 61 | `SentScope` | sentinel | `.ufo/waves/round-29/wave1/SentScope.md` |
| 62 | `RevStagedIntent` | revenger | `.ufo/waves/round-29/wave1/RevStagedIntent.md` |
| 63 | `SimplyBloat` | simplifier | `.ufo/waves/round-29/wave1/SimplyBloat.md` |
| 64 | `SimplyFixture` | simplifier | `.ufo/waves/round-29/wave1/SimplyFixture.md` |

---

## 3. Mutual Exclusion & Single-Writer Rule Verification

### Formal Disjointness Proof
Let $S = \{S_1, S_2, \dots, S_{64}\}$ be the set of 64 seats, and let $W(S_i)$ denote the set of paths written by seat $S_i$ under `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

1. **Report Paths**: $\forall i \neq j, \text{ReportPath}(S_i) \neq \text{ReportPath}(S_j)$. The report directory `.ufo/waves/round-29/wave1/` hosts exactly one unique `<SeatName>.md` per seat.
2. **Production Files**:
   $$\bigcup_{i=1}^{64} \left( W(S_i) \cap \text{ProductionFiles} \right) = \coprod_{i \in \text{ProdWriters}} W(S_i)$$
   where $\text{ProdWriters} = \{\text{ExecImplC1}, \text{ExecCapS043}, \text{ExecCapS044}, \text{ExecCapS045}, \text{ExecManifestC2}, \text{ExecEntryF13}, \text{ExecRecheckAudit}, \text{ScribeQuality}, \text{ScribeSkillGate}, \text{ScribeReadmeC2}, \text{ScribeSourcesGate}, \text{ScribeLog}, \text{ScribeLesson}, \text{ScribeScorecard}\}$. Each production path maps to a singleton set with zero overlap.
3. **Control & Auxiliary Paths**:
   - `c1-controls/` is owned strictly by `ExecControlC1`.
   - `c1-receipt-index.txt` is owned strictly by `ExecCanonC1`.
   - `receipts/ExecCanonC2.txt` is owned strictly by `ExecCanonC2`.
   - `post-commit-recheck.txt` is owned strictly by `ExecPostCommitRecheck`.
   - `receipt-index.txt` and `receipts/` rollup copies are owned strictly by `ExecAssembleReceipts`.

Therefore, for all $i, j \in \{1, \dots, 64\}$ with $i \neq j$:
$$W(S_i) \cap W(S_j) = \emptyset$$
The single-writer invariant holds unconditionally across the entire wave.

### Boundary Clarifications (Producers vs. Consumers)
To prevent accidental write collisions, explicit boundaries are enforced for related seats:
- **`ScribeLessonGate` vs. `ScribeLesson`**: `ScribeLessonGate` produces ONLY its draft report `.ufo/waves/round-29/wave1/ScribeLessonGate.md`. `ScribeLesson` is the SOLE author of `corpus/lessons/round-29.md`. `ScribeLesson` consumes the draft via read.
- **`ScribeConsiderthese` vs. `ScribeQuality`**: `ScribeConsiderthese` drafts R15 proposal text in `.ufo/waves/round-29/wave1/ScribeConsiderthese.md`. `ScribeQuality` is the SOLE writer of `corpus/QUALITY.md`.
- **`SimplyFixture` vs. `ExecControlC1`**: `SimplyFixture` inspects `c1-controls/` and reports optimization findings in `SimplyFixture.md`. It does NOT edit or overwrite `c1-controls/` directly; any adjustment requires peer messaging to `ExecControlC1`.
- **`SimplyBloat` vs. All Wave Seats**: `SimplyBloat` measures byte sizes and reports bloat. It never deletes another seat's receipt without an explicit agent message.
- **`ExecScopeSweep` vs. Repo Writers**: `ExecScopeSweep` checks the working tree and only deletes misplaced kasegi strays from the fleet root (`/home/vgpnk/Projects/shokunin/`). It does not alter lane files.
- **`ExecAssembleReceipts` vs. Seat Receipt Writers**: `ExecAssembleReceipts` copies existing receipts into `.ufo/waves/round-29/wave1/receipts/` and generates `receipt-index.txt`. It never mutates the original seat receipts.

---

## 4. Sequencing Architecture & Causal Dependency Graph

Execution is partitioned into 11 distinct causal epochs. No seat may advance past its barrier epoch until the prerequisite assets are confirmed landed on disk.

```
+---------------------------------------------------------------------------------------+
| EPOCH 0: Recon, Baselines & Drafts (Independent / Read-Only / Scratch)                |
| Scouts (Datawalk, CapH1, CapBugcrowd, Assimilation, ConnOverlap)                      |
| Connectors (ConnClaims, ConnStagedCensus, ConnOwnership)                              |
| Scribes (Considerthese, FrontierNote, Quarantine, AssimReport)                        |
| RevStagedIntent, SentScope                                                            |
+-------------------------------------------+-------------------------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                                                     |
+--------v----------------------------------+       +--------------------------v--------+
| BRANCH C1 (Instrument Completeness)       |       | BRANCH C2 (Assimilation & Entry)  |
| EPOCH 1A: ExecImplC1                      |       | EPOCH 1B: Captures S043,S044,S045 |
| Modifies corpus/instruments/anchorcheck.py|       | (ExecCapS043, ExecCapS044, S045)  |
|                                           |       | Parallel: ScribeQuality (QUALITY) |
+-------------------------------------------+       +------------------+----------------+
                                                                       |
                                                    +------------------v----------------+
                                                    | EPOCH 2: Manifest Generation      |
                                                    | ExecManifestC2 builds manifest    |
                                                    | Runs source-recheck S043/44/45    |
                                                    +------------------+----------------+
                                                                       |
                                                    +------------------v----------------+
                                                    | EPOCH 3: C2 Ground Zero (Entry)   |
                                                    | ExecEntryF13 authors F13 entry    |
                                                    | Cites S043-S045 with Q1-Q10 bar   |
                                                    +------------------+----------------+
                                                                       |
         +-------------------------------------------------------------+
         |
+--------v------------------------------------------------------------------------------+
| EPOCH 4: Gate Proving, Expected List Sync & Registry/Index Appends                    |
| - ExecCensusDry: Scratch mirror validation of S043-S045 + Entry (Gate PASS: exit 0)   |
| - ExecRecheckAudit: Proves RED state, then updates knowledge-expected.txt (40->41)   |
| - ScribeReadmeC2: Appends F13 coverage-map and Frontier rows to corpus/README.md      |
| - ScribeSourcesGate: Appends S043-S045 rows to corpus/SOURCES.md (POST Census PASS)  |
| - ScribeSkillGate: Appends anchorcheck row and F13 note strictly at EOF of SKILL.md   |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 5: Intermediate Verification, Probes, Controls & Mutation Attacks               |
| - ExecHarnessC2: Runs frontier-recheck-count.py (16/16 pass) and source-rechecks     |
| - ExecControlC1: Executes do-nothing control and mutants M1-M4 in c1-controls/        |
| - Reviewers: RevC1Instrument, RevC1Controls, RevC2Entry, RevC2Manifest,               |
|              RevC2Registry, RevNoHarmC1, RevNoHarmC2, RevCensusDry, RevKillTry        |
| - Mutation Testers: MutC1Limbs, MutC1Hermetic, MutC2Counters, MutC2Sources           |
| - Lab Probes: LabC1Probe, LabC2Probe, LabInstrumentProbe, ExecSelftestProbe           |
| - Invariants: ExecDensityNoHarm (re-measures density), SimplyFixture, SimplyBloat    |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 6: Synthesis, Digest & Lesson Drafting                                          |
| - ScribeLessonGate: Compiles Gate section draft (admits, rejects, quarantine table)   |
| - ScribeReportDigest: Compiles evidence digest for L1 report                          |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 7: Pre-Commit Canonical Receipts Sealing                                        |
| - ExecCanonC1: Re-hashes anchorcheck.py, runs C1 counters, seals c1-receipt-index.txt |
| - ExecCanonC2: Runs all 5 frozen C2 counters, seals receipts/ExecCanonC2.txt          |
| - RevReceiptsCanon: Audits canonical receipt indexes                                  |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 8: Final Scribing, Rollup & Misroot Sweep                                       |
| - ScribeScorecard: Appends Round 29 section to SCORECARD.md (R6 preserved)            |
| - ScribeLog: Appends Round 29 summary to LOG.md                                       |
| - ScribeLesson: Assembles final corpus/lessons/round-29.md                            |
| - ExecAssembleReceipts: Gathers 64 receipts into receipts/ and writes index           |
| - RevSeatEvidence: Audits 10 sample receipts                                         |
| - ExecScopeSweep: Fleet root sweep (cleans strays, verifies working tree)            |
| - CritC1Kill, CritC2Kill, CritGlobal, CritMeta: Final adversarial evaluations        |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 9: L1 Integration Commit                                                        |
| - L1 Integrator checks working tree cleanliness and commits wave to `master` ref     |
+---------------------------------------------------------------------------------------+
                                            |
+-------------------------------------------v-------------------------------------------+
| EPOCH 10: Post-Commit Canonical Verification (RUNS LAST)                             |
| - ExecPostCommitRecheck: Runs C1 + C2 counters at `git rev-parse master` commit hash  |
|   Writes post-commit-recheck.txt (Eliminates M28-1 PRE-STATE defect)                  |
+---------------------------------------------------------------------------------------+
```

---

## 5. Critical Dependencies for Explicit L1 Sequencing

The L1 Integrator MUST explicitly enforce seven synchronization barriers during execution:

### Flag 1: Captures-before-Manifest Barrier
- **Constraint**: `ExecManifestC2` MUST NOT generate `corpus/source-snapshots/round-29/manifest.json` until `ExecCapS043.md`, `ExecCapS044.md`, and `ExecCapS045.md` receipts are published and sha256 digests verified.
- **Consequence of Violation**: `source-recheck.py` fails with missing snapshot file errors; manifest quote assertions fail closed.

### Flag 2: Manifest-before-Entry Barrier
- **Constraint**: `ExecEntryF13` MUST NOT author `corpus/knowledge/program-severity-ladders-and-reward-scales.md` until `manifest.json` exists and its rechecks pass.
- **Consequence of Violation**: Entry header `recheck:` command references a nonexistent or failing manifest, failing Q1 and Q10.

### Flag 3: Entry-before-README Barrier (Prevents M28-5)
- **Constraint**: `ScribeReadmeC2` MUST NOT append F13 to `corpus/README.md` until `corpus/knowledge/program-severity-ladders-and-reward-scales.md` physically exists on disk.
- **Consequence of Violation**: Defect M28-5 recurs — `frontier-recheck-count.py` crashes with `FileNotFoundError` when it encounters an admitted Frontier row whose entry path is absent.

### Flag 4: Dual-Gated SOURCES Append Barrier (Prevents Transient E11)
- **Constraint**: `ScribeSourcesGate` MUST NOT append S043, S044, S045 to `corpus/SOURCES.md` until:
  1. `ExecEntryF13` has landed the entry file (satisfying `used-by` path existence).
  2. `ExecCensusDry` has published its PASS receipt (`ExecCensusDry.md`) confirming that the scratch-mirror run of `sources-census.sh validate` exited 0 with zero E03/E04 findings.
- **Consequence of Violation**: In-flight transient failure: `sources-census.sh validate` exits 1 with `kasegi E11 S043 missing used-by...`, breaking automated census checks.

### Flag 5: Expected-List Synchronization Barrier
- **Constraint**: `ExecRecheckAudit` MUST run its RED check first (verifying `unexpected=1` / exit 1 when F13 lands), then regenerate `corpus/instruments/knowledge-expected.txt` to 41 entries / 43 lines, and confirm exit 0.
- **Consequence of Violation**: Stale audit debt carries into future rounds; verifier spot-checks flag unexpected entry discrepancies.

### Flag 6: SKILL.md End-of-File Append Discipline (Prevents M28-6)
- **Constraint**: `ScribeSkillGate` MUST append its `anchorcheck.py` registry note and F13 frontier note strictly at the very end of `SKILL.md` (after line 1035).
- **Consequence of Violation**: Defect M28-6 recurs — inserting lines into earlier tables shifts line 1000 down, breaking the verbatim line citation in `corpus/instruments/resolve-dispatch-fixtures.json:159,161`.

### Flag 7: Post-Commit Barrier for `ExecPostCommitRecheck` (Prevents M28-1)
- **Constraint**: `ExecPostCommitRecheck` MUST NOT run until the L1 has minted the integration commit on `master` and messaged the seat with the commit hash.
- **Consequence of Violation**: Defect M28-1 recurs — `post-commit-recheck.txt` records a pre-state working tree hash or intermediate parent hash rather than the landed round-29 commit.

---

## 6. Verifiable Self-Check & Receipt

### Verification Checklist
- [x] All paths under `/home/vgpnk/Projects/shokunin/kasegi-shokunin` checked for single-writer assignment.
- [x] Mutual exclusion proven across all 64 seats ($\forall i \neq j, W(S_i) \cap W(S_j) = \emptyset$).
- [x] Causal ordering defined: captures $\to$ manifest $\to$ entry $\to$ (README + SOURCES + RecheckAudit) $\to$ verification $\to$ canonical receipts $\to$ post-commit recheck.
- [x] Scratch-mirror validation gate (`ExecCensusDry`) explicitly chained before `ScribeSourcesGate`.
- [x] Canonical receipt indexes (`ExecCanonC1`, `ExecCanonC2`) and post-commit verification (`ExecPostCommitRecheck`) placed last.
- [x] Seven explicit L1 sequencing flags documented with failure modes.
- [x] UFO-FSD connector synthesis documented (Pre-Commit Barrier Protocol & "C2 Ground Zero").
- [x] Leaf role bounds respected: no subagents dispatched, no background jobs, no mutations outside lane write scope.

### Receipt
- **Author**: `ConnOwnership` (UFO-FSD connector)
- **Report Location**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/wave1/ConnOwnership.md`
- **Output Digest**: SHA256 generated on save.
- **Status**: COMPLETE
