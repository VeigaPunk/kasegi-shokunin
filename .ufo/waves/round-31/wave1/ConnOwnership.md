# ConnOwnership — Integration Ownership & Sequencing Matrix

- **Round:** 31 (kasegi-shokunin)
- **Wave:** 1 (`kasegi-r31-build`)
- **Seat:** `ConnOwnership`
- **Role:** UFO-FSD connector / Integration ownership & sequencing matrix
- **Axes owned:** `depth:verifiability` (C1, held 4), `coverage` (C2, held 7)
- **Answering model:** `devin/deepseek-v4-1-flash` (config route table)
- **Report path:** `.ufo/waves/round-31/wave1/ConnOwnership.md`
- **Base commit:** `b374febbb33ccadade78a787279707fd5d2e6e1d`
- **Freeze commit:** `738a77999a00efbca129cfccb28a481037f6241f`

---

## 1. Executive Summary

This receipt establishes the authoritative integration ownership, sequencing matrix, and dependency graph for Wave 1 of Round 31.
Empirical audits over the 38 wave items in `.ufo/waves/round-31/wave1-spec.json` and the lane repository confirm:
1. **Zero Multi-Writer Collisions:** Every write target has exactly one assigned owner.
2. **Zero Unowned Required Writes:** Every required repository and instrument modification maps to a single designated executor or scribe.
3. **Strict DAG (Zero Cycles / Zero Unowned Waits):** The 29-node operational dependency graph is a cycle-free directed acyclic graph. Every wait condition targets a file owned and produced within the wave.
4. **QUALITY R6 Line Stability Enforced:** Every planned edit to line-anchored files (`SKILL.md`, `corpus/README.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `PROVINCE.md`, `corpus/instruments/README.md`, `corpus/knowledge/considerthese-proposals-ledger.md`) is append-only. A potential R6 violation in `ScribeProvince` (which was instructed to edit the Frontier section, threatening lines 45–52) was caught, messaged via agent IRC, and corrected: `ScribeProvince` will append at line 53+ to keep `PROVINCE.md:45-50` and `PROVINCE.md:52` stable.
5. **C1/C2 Causal Coupling Identified & Synthesized:** Live empirical testing demonstrated that creating the F15 entry temporarily flips `recheck-audit.py --quiet` from exit 0 to exit 1 (`unexpected=1`) until `ExecExpectedList` appends the entry to `knowledge-expected.txt`. An atomicity lockstep sequencing protocol is established to prevent race conditions during parallel execution.

---

## 2. File Ownership Verification

The table below verifies every write scope in the wave. No file has multiple writers; no planned write is unowned.

| Target Path | Owner Seat | Operation | Status / Collision Check |
|---|---|---|---|
| `corpus/instruments/limb-mutation-check.py` | `ExecCounter` | Write new | Clean (sole owner; stdlib only, scratch testing) |
| `corpus/instruments/recheck-audit.py` | `ExecRALimbs` | Edit in-place | Clean (sole owner; MutRAExisting uses scratch copies) |
| `corpus/instruments/source-recheck.py` | `ExecSRLimbs` | Edit in-place | Clean (sole owner; MutSRExisting uses scratch copies) |
| `corpus/instruments/frontier-recheck-count.py` | `ExecFRLimbs` | Edit in-place | Clean (sole owner; MutFRExisting uses scratch copies) |
| `corpus/instruments/limb-fixtures/sr/**` | `ExecSRLimbs` | Create new | Clean (isolated subfolder) |
| `corpus/instruments/limb-fixtures/fr/**` | `ExecFRLimbs` | Create new | Clean (isolated subfolder) |
| `.ufo/waves/round-31/wave1/ledger-fragments/ra.json` | `ExecRALimbs` | Write fragment | Clean (partitioned filename) |
| `.ufo/waves/round-31/wave1/ledger-fragments/sr.json` | `ExecSRLimbs` | Write fragment | Clean (partitioned filename) |
| `.ufo/waves/round-31/wave1/ledger-fragments/fr.json` | `ExecFRLimbs` | Write fragment | Clean (partitioned filename) |
| `corpus/instruments/limb-ledger.json` | `ExecLedgerMerge` | Assemble new | Clean (sole owner; merges fragments + controls) |
| `corpus/instruments/score-gap.py` | `ExecScoreGap` | Write new | Clean (sole owner; read-only reporter, proposal 2) |
| `corpus/instruments/README.md` | `ScribeInstrReadme` | Append-only | Clean (line 328+; waits on ExecLedgerMerge + ExecScoreGap) |
| `corpus/instruments/knowledge-expected.txt` | `ExecExpectedList` | Append/sort | Clean (line 44; waits on ExecEntryF15) |
| `corpus/source-snapshots/round-31/S048.txt` | `ExecCapManifest` | Capture new | Clean (sole owner; ScoutMSVR writes only to scratch) |
| `corpus/source-snapshots/round-31/manifest.json` | `ExecCapManifest` | Write new | Clean (sole owner; pins S048 assertions) |
| `corpus/knowledge/vendor-third-party-finding-coordination.md` | `ExecEntryF15` | Write new | Clean (sole owner; F15 MSVR knowledge entry) |
| `corpus/SOURCES.md` | `ExecRegistryAppend` | Append row | Clean (row S048; ExecCensusDry uses scratch mirror) |
| `corpus/README.md` | `ScribeReadmeF15` | Append-only | Clean (line 292+; F15 coverage row + admitted table) |
| `PROVINCE.md` | `ScribeProvince` | Append-only | Clean (line 53+; R6 preserved, existing lines 1–52 stable) |
| `SKILL.md` | `ScribeSkillGate` | Append-only | Clean (line 1058+; gates & probes registry append) |
| `corpus/QUALITY.md` | `ScribeQuality` | Append-only | Clean (line 90+; R16/R17 append; waits on ExecErratumCheck) |
| `LOG.md` | `ScribeLogR30` | Append-only | Clean (line 1468+; late round-30 entry) |
| `SCORECARD.md` | `ScribeErratum` | Append-only | Clean (line 836+; r31 erratum naming recheck-audit item) |
| `corpus/knowledge/considerthese-proposals-ledger.md` | `ScribeConsiderthese` | Append-only | Clean (line 21+; byte-identical recheck line) |
| `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` | `ExecErratumCheck` | Write receipt | Clean (sole owner; red-before capture) |
| `.ufo/waves/round-31/wave1/ExecErratumCheck-after.txt` | `ExecErratumCheck` | Write receipt | Clean (sole owner; green-after capture) |
| `.ufo/waves/round-31/wave1/ScoutMSVR-scratch/**` | `ScoutMSVR` | Scratch capture | Clean (wave-1 scratch dir only) |
| `.ufo/waves/round-31/wave1/ExecCensusDry/validate/**` | `ExecCensusDry` | Scratch mirror | Clean (dry validation mirror only) |
| `.ufo/waves/round-31/wave1/<SeatName>.md` | Each respective seat | Write receipt | Clean (every seat owns its own markdown receipt) |

### Non-Owned & Untouched Surfaces (Confirmed Frozen)
- `corpus/lessons/**`: Frozen for Wave 1. `ScribeGateDraft` drafts into `.ufo/waves/round-31/wave1/ScribeGateDraft.md` for L1 integration in Wave 2.
- `SHONEN.md`: Read-only this wave.
- `claims.json`: Frozen at commit `738a77999a00efbca129cfccb28a481037f6241f`.
- `.ufo/rounds/**`, `.ufo/prompts/**`, `.ufo/watchdog.log`, `MANIFEST.json`: Strictly untouched.

---

## 3. Dependency Order & Sequencing Matrix

The 38 seats operate across four parallel execution pipelines converging on final harness and ledger verification.

```
PIPELINE 1 (C2 Coverage — F15 MSVR):
  [ScoutMSVR, ScoutF15Sweep, ConnSibling]
          │
          ▼
    ExecCapManifest (captures S048.txt, writes manifest.json)
          │
          ▼
    ExecEntryF15 (writes knowledge/vendor-third-party-finding-coordination.md)
          │
    ┌─────┴──────────────────────────┬────────────────────────┬─────────────────────┐
    ▼                                ▼                        ▼                     ▼
ExecRegistryAppend             ScribeReadmeF15          ScribeProvince        ExecExpectedList
(waits on ExecCensusDry)       (appends README.md)      (appends PROVINCE)    (appends knowledge-expected)
    │                                │                        │                     │
    └────────────────────────────────┼────────────────────────┴─────────────────────┘
                                     │
                                     ▼
                               ExecHarnessC2
     (runs frontier-recheck-count 18/18, source-recheck S048, census validate)

PIPELINE 2 (C1 Depth:Verifiability — Mutation Ledger & Counter):
  [ScoutRALimbMap + MutRAExisting]   [MutSRExisting]   [MutFRExisting]   [ExecCounter]
               │                            │                 │                │
               ▼                            ▼                 ▼                │
          ExecRALimbs                  ExecSRLimbs       ExecFRLimbs           │
         (ra.json)                    (sr.json)         (fr.json)              │
               │                            │                 │                │
               └────────────────────────────┼─────────────────┴────────────────┘
                                            │
                                            ▼
                                     ExecLedgerMerge
                        (assembles limb-ledger.json, runs counter)
                                            │
                              ┌─────────────┴─────────────┐
                              ▼                           ▼
                       ScribeSkillGate             ScribeInstrReadme
                     (appends SKILL.md)       (appends instruments/README)
                                                          ▲
                                                          │
PIPELINE 3 (Non-Claim — Proposal 2 Score-Gap):             │
  ExecScoreGap (implements score-gap.py) ─────────────────┘
          │
          ▼
  ScribeConsiderthese (appends considerthese-proposals-ledger.md)

PIPELINE 4 (Non-Claim — Mistake M31-1 Closure):
  ExecErratumCheck (runs red-before check -> writes ExecErratumCheck-before.txt)
          │
          ▼
  ScribeErratum (appends r31 erratum to SCORECARD.md -> writes ScribeErratum.md)
          │
          ▼
  ExecErratumCheck (runs green-after check -> writes ExecErratumCheck-after.txt & ExecErratumCheck.md)
          │
          ▼
  ScribeQuality (appends R16/R17 to QUALITY.md -> writes ScribeQuality.md)

  [Independent]: ScribeLogR30 (appends round-30 entry to LOG.md)

PIPELINE 5 (Reviewers, Critics, Sentinel):
  - RevClaimsFreeze, CritC1Kill, CritC2Kill, RevSourceBar: read-only adversarial probes.
  - SentScopeW1: runs scope & credential sweep after >=15 wave-1 receipts land.
```

### Topological Graph Verification
- **Total Graph Nodes:** 29 active sequential milestones
- **Total Dependency Edges:** 33 directed causal dependencies
- **Topological Order:**
  1. `ExecErratumCheck_before`
  2. `MutFRExisting`
  3. `MutSRExisting`
  4. `ScoutMSVR`
  5. `ScoutF15Sweep`
  6. `ConnSibling`
  7. `ExecCensusDry`
  8. `ExecCounter`
  9. `ExecScoreGap`
  10. `ScoutRALimbMap`
  11. `MutRAExisting`
  12. `ScribeErratum`
  13. `ExecFRLimbs`
  14. `ExecSRLimbs`
  15. `ExecCapManifest`
  16. `ScribeConsiderthese`
  17. `ExecRALimbs`
  18. `ExecErratumCheck_after`
  19. `ExecEntryF15`
  20. `ScribeGateDraft`
  21. `ExecLedgerMerge`
  22. `ScribeQuality`
  23. `ExecRegistryAppend`
  24. `ScribeReadmeF15`
  25. `ScribeProvince`
  26. `ExecExpectedList`
  27. `ScribeSkillGate`
  28. `ScribeInstrReadme`
  29. `ExecHarnessC2`
- **Result:** Strict Directed Acyclic Graph (DAG). Zero cycles. Zero deadlocks. Zero unowned wait paths.

---

## 4. QUALITY R6 Line Stability Audit

Rule R6 mandates:
> *An edit to a file that other files cite by line number keeps every existing line at its number (append at the end, or a same-line suffix); anchorcheck before/after prints the same cited source lines.*

Every file undergoing modification was inspected for existing line count, trailing newline, and caller citations:

| File | Base Lines | Trailing Newline | Owner Seat | Append Plan & Line Anchor Check |
|---|---|---|---|---|
| `SKILL.md` | 1057 | Yes (`\n`) | `ScribeSkillGate` | Appends `## Round-31 Gates & probes registry addition` at lines 1058+. Preserves line citations (e.g. `SKILL.md:821`). |
| `corpus/README.md` | 291 | Yes (`\n`) | `ScribeReadmeF15` | Appends `## Round-31 admission — coverage map row and Frontier F15` at lines 292+. Keeps lines 1–291 intact. |
| `LOG.md` | 1467 | Yes (`\n`) | `ScribeLogR30` | Appends `## Round 30 — 2026-10-25 — late append` at lines 1468+. Preserves historical lines 1–1467. |
| `SCORECARD.md` | 835 | Yes (`\n`) | `ScribeErratum` | Appends `### Round-31 erratum to the round-30 section` at lines 836+. Preserves stale paragraph at lines 813–818 for check discrimination. |
| `corpus/QUALITY.md` | 89 | Yes (`\n`) | `ScribeQuality` | Appends `## Round-31 additions` (R16, R17) at lines 90+. Preserves existing Q1–Q10 and R1–R15 numbers. |
| `PROVINCE.md` | 52 | Yes (`\n`) | `ScribeProvince` | **CORRECTED:** Must append at lines 53+. Prevents shifting lines 45–50 and line 52 (cited by `ConnSibling.md:180,183`). |
| `corpus/instruments/README.md` | 327 | Yes (`\n`) | `ScribeInstrReadme` | Appends `## Round-31 additions` at lines 328+. Preserves existing instrument documentation. |
| `corpus/knowledge/considerthese-proposals-ledger.md` | 20 | Yes (`\n`) | `ScribeConsiderthese` | Appends `## Round-31 status flips` at lines 21+. Audited `recheck:` line at lines 5–6 stays byte-identical. |

### Contradiction Caught & Remediated: `ScribeProvince`
- **Issue:** The prompt for `ScribeProvince` stated: *"In the Frontier section PROVINCE.md names F01-F10 and an F11 line. Append one factual line for the F12-F15 admissions that PROVINCE.md does not yet name..."*
- **Risk:** Inserting the line inside `## Frontier` (around line 41–42) would insert into the middle of the 52-line file, shifting subsequent lines down by 1–2. Lines 45–50 and line 52 (`Live-target testing is refused; this corpus is documentation only.`) are actively cited by line number (including by `ConnSibling.md:180, 183` which landed in Wave 1). Shifting them violates R6.
- **Action Taken:** Message dispatched to `agent://ScribeProvince`:
  > *ConnOwnership notice: R6 requires append-only line stability. PROVINCE.md:45-50 and line 52 are cited by line number across the lane and wave-1 receipts (including ConnSibling.md:180, 183). To keep all existing lines 1-52 at their exact numbers, append your F12-F15 admission note at the END of PROVINCE.md (line 53+), rather than inserting mid-file into the Frontier section. Wait for ExecEntryF15 receipt before editing.*
- **Confirmation Received:** `ScribeProvince` acknowledged via IRC:
  > *ScribeProvince ack: I will append the F12-F15 admission note at the END of PROVINCE.md (new lines 53+), not mid-file in the Frontier section, so lines 1-52 keep their numbers (R6). The appended block will carry a `[r31 amendment, appended 2026-10-25]` header naming the Frontier section it amends...*

---

## 5. Non-Obvious Move / Synthesis Across Proposals and Axes

### Empirical Evidence
During live execution of Wave 1, an empirical probe was conducted at the exact moment `ExecEntryF15` created `corpus/knowledge/vendor-third-party-finding-coordination.md`:
```console
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=43 missing=0 unexpected=1 exit=1
exit_code: 1
```
Concurrently, `score-gap.py` was executed:
```console
$ python3 corpus/instruments/score-gap.py
recheck: lines=44 executes=20 gated=24 broken=0 exit=1
...
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

### Contradiction & Second-Order Effect
1. **False C1 Regression:** Claims C1 kill rule states:
   > *Fails if any of: ... OR the real corpus regresses (recheck-audit.py --quiet must still print `strict pass=N/N` with N equal to the committed expected-entry count and exit 0; source-recheck.py --selftest failures=0; frontier harness pass == entries, exit 0)*
   When `ExecEntryF15` lands, `recheck-audit.py` encounters `unexpected=1` and exits 1 until `ExecExpectedList` appends the entry to `knowledge-expected.txt`. Any C1 check run during this window falsely fails the kill rule.
2. **Score-Gap Reporting:** `score-gap.py` runs `recheck-audit.py --quiet` as a subprocess. During the in-flight window, it records `exit=1`.
3. **Synthesis Across Proposals:** Proposal 2 (`score-gap.py`) measures the distance to score 5 on `depth:verifiability`. The threshold for score 5 requires zero gated claims. Notice that C2's expansion (F15 MSVR) adds a *live, captured* source (S048), increasing `executes` from 19 to 20 and reducing the proportion of gated rechecks from 24/43 (55.8%) to 24/44 (54.5%). C2 directly improves the empirical substrate tracked by Proposal 2.

### Proposed Move: C2 Atomicity Lockstep & Quiescence Barrier
1. **Lockstep Staging:** `ExecExpectedList` must be treated as the immediate atomic pair to `ExecEntryF15`. Scribe seats and verifiers must not run recheck audits in the intermediate state.
2. **Quiescence Verification Gate:** C1's final verification command must be executed only when the tree is quiescent:
   - Pre-C2 Quiescent State: $N = 43$, harness $17/17$, exit 0.
   - Post-C2 Quiescent State: $N = 44$, harness $18/18$, exit 0.
   No verification command may run in the transient non-quiescent state ($N = 44$, expected $= 43$, exit 1).
3. **Subprocess Resilience:** `score-gap.py` parses `executes`, `gated`, and `broken` from `recheck-audit.py`. When run on quiescent bytes after `ExecExpectedList` lands, it prints `exit=0` and reflects the updated $24/44$ ratio cleanly.

### Risks
- **Race Condition:** If `ExecCounter` or `ExecLedgerMerge` runs real-corpus verification while `ExecExpectedList` is executing, a false failure could be recorded. Mitigated by strict sequencing (`ExecLedgerMerge` runs after its fragments land, and C1 counter runs scratch copies).
- **Format Divergence:** If `recheck-audit.py` stdout output format were altered, `score-gap.py` regex matchers would fail. Mitigated because `recheck-audit.py` output format is frozen by contract.

### Verification
```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
# 1. Post-quiescence recheck-audit
python3 corpus/instruments/recheck-audit.py --quiet
# Expected: strict pass=44/44, expected=44 missing=0 unexpected=0 exit=0

# 2. Frontier harness
python3 corpus/instruments/frontier-recheck-count.py
# Expected: PASS F15 ... ids=S048, entries=18 pass=18 exit=0

# 3. Score-gap output
python3 corpus/instruments/score-gap.py
# Expected: exit 0, recheck: lines=44 executes=20 gated=24 broken=0 exit=0

# 4. R6 Anchorcheck on PROVINCE.md
python3 corpus/instruments/anchorcheck.py PROVINCE.md
# Expected: exit 0, citations in range
```
