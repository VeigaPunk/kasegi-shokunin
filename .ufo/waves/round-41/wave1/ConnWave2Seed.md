# ConnWave2Seed — wave-1 receipt (round 41, build wave 1)

**Seat:** `ConnWave2Seed`  
**Role:** UFO-FSD connector / Wave-2 Seeding  
**Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`  
**Base commit:** `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (corrected 40-char; freeze literal 38-char erratum noted)  
**Claims-freeze commit:** `fbba3d96cdf8d37c1ea41304a1ba35691329684b`  
**Judged on:** `depth:verifiability`, `coverage`  
**Milestone:** round-41 build wave 1 (fresh-start)

---

## 1. Deliverable Verification

- **Deliverable file:** `.ufo/waves/round-41/wave1/ConnWave2Seed.txt`
- **Line count:** 40 lines (within required 35–45 range)
- **Format:** strictly one item per line, no prose, adhering exactly to `attack <what> with <method> because <finding>`
- **SHA256:** `df3bc52e104f91b594885cbf67eb35fc2d5b5ec062a2849422b8af17097399be`
- **Bytes:** 6,507 bytes

---

## 2. Polling Method & Attack-Seat Coverage

### 2.1 Polling Method
The wave1 output directory `.ufo/waves/round-41/wave1/` was monitored via regular directory scans and read inspections alongside real-time transcript tracking via `history://<seat>` across all 21 dispatched attack seats (`Crit*`, `Mut*`, `Rev*`). As seats executed empirical probes and drafted their findings, receipts and probe outputs were read directly upon landing.

### 2.2 Coverage Across 21 Attack Seats
All 21 attack seats were tracked and their core findings distilled into the 40 seeded wave-2 attack lines:

1. **`CritClaims`**: Evaluated whether C1 predicate can be satisfied by a trivially-printing suite, fake registry row, or self-grading selftest. Verified root directory resolution and base hash verification.
2. **`RevSuitePlan`**: Mapped `r40-closure.sh` H1–H10 checks to r41 I1–I12 successors. Verified inheritance of all wave-2 fixes (W1–W21), retirement of H4, and defense-in-depth on I6/I11.
3. **`MutDesign`**: Mutation-tested the CLAIM-to-CHECK mapping. Discovered that D4, D5, D6 are orphan defects (unowned by any I1–I12 suite check), I12 is an orphan check, and identified dual ownership of scratch scan between I6 and I11.
4. **`CritC2`**: Adjudicated RFC 9116 in-province boundaries against sibling `kake` S078. Verified fetch stability (UTF-8 BOM present, 45,129 bytes, `79d19ce7...`), located quote fidelity, and harness 27/27 entry requirements.
5. **`RevC2Shape`**: Ran C2 counting commands across base and control exports. Demonstrated that `capture-binding-check.py` rule B does not enforce row→record presence (so row-only twins bind green) and verified maximal twin (variant-F) greens every frozen counter.
6. **`MutC2Counters`**: Mutated each C2 after-state value on scratch copies; constructed junk twin mutations and verified which kill-rule clauses fire.
7. **`RevD4D5D6`**: Produced exact landed repairs for routed records: `RevD4D5D6.lesson-erratum.txt` (D4 duplicated Gate heading + garbled census), verified tally non-propagation in SHONEN.md (zero-byte fix), and `RevD4D5D6.skill-table-fix.txt` (D6 table repair).
8. **`CritI2Receipt`**: Attacked I2 receipt design, testing committer date self-assertion, the fixed-point convergence of receipt verification, and the absence of a committed selftest transcript in the receipt.
9. **`RevFreshStart`**: Verified fresh-start discipline across r38 (self-referential predicate avoided via external Y supply), r39 (unbacked quotes avoided via teed transcript), and r40 (fixtures verified against frozen kill rule).
10. **`MutKillRule`**: Discovered 10 fresh kill-rule escape states beyond the committed CritKillRule set, including unverified suite digest (E1), selftest line injection (E2), late scratch creation (E4), out-of-root scratch strays (E5), undeclared appends (E6), and overdue census suppression (E7).
11. **`RevLessonShape`**: Evaluated structural defects from `round-40.md` to prevent recurrence in round 41: duplicated headings, mangled parentheticals, tally arithmetic errors (dispatch JSON 25/35 vs lesson 33/35), and narrowing frozen clauses after landing.
12. **`CritReceiptUtc`**: Analyzed `time-basis=ref-commit`. Proved `%ct` epoch derivation is timezone-immune, confirmed receipt `run-utc` binds to named `export-ref` (J7), and validated ancestor/diff-clean guards.
13. **`RevRegistry`**: Verified Markdown table blank-line rule (D6 repair), required logical 8-column table structure, escaped alternation pipes (`\|`), and exact first-cell naming (`r41-closure.sh`).
14. **`MutScan`**: Constructed extensive mutant matrix for I6 scanner, testing case folding, dotfile inclusion, nested recursion, non-breaking hyphens, and unreadable root fail-closed handling.
15. **`RevCorrections`**: Pre-reviewed `Correction (round 41)` blocks against spotcheck D1/D2 requirements: mandatory "not verified" grading, naming exact firing paths, and stating receipt truth values.
16. **`CritSync`**: Tested C2 instrument synchronization across 4 failure scenarios: unlisted knowledge files (audit unexpected=1), manifest hash mismatch (binding unbound), mismatched F24 entry name (harness FAIL), and duplicate registry rows.
17. **`RevQualityCriterion`**: Formulated criterion row `R38` in `corpus/QUALITY.md` capturing the M41-1 overclaim class (grading verified while frozen kill rule fires on committed evidence).
18. **`MutPredicates`**: Executed cheat probes against frozen predicates in scratch fixtures, demonstrating how naive suites trip kill-rule clauses.
19. **`RevC2Entry`**: Evaluated `ScribeC2Entry.entry.md` against QUALITY.md admission bars: verified provenance trio, quote accuracy against RFC 9116 §2.4, and flagged deliverable hash tracking.
20. **`CritInstruments`**: Proved `source-recheck.py` validates quotes only against local capture files (self-referential) and that `capture-binding-check.py` checks manifest-to-row binding without verifying live upstream content.
21. **`RevReceiptPath`**: Reconstructed the 6-step round-40 receipt production sequence (mint at J7, commit as Y, re-verify at Y), demonstrating that H5 baseline was synthetically generated and that selftest transcripts were never committed in the receipt.

---

## 3. UFO-FSD Connector Synthesis: One Non-Obvious Move

### 3.1 Synthesis Context & Evidence
Synthesis across the round's proposals reveals three critical structural findings:
1. **The Suite Digest & Declared-Blocks Blind Spot:** `MutKillRule` showed that K10 checks receipt byte-identity but nowhere binds the receipt's recorded `suite-sha256` to the exported suite file digest, permitting silent suite revisions between J and Y. Furthermore, `r40-closure.sh` H9 only iterates *over declared lines in `declared-blocks.txt`* rather than checking that *all paths modified between base and Y are declared*.
2. **The Orphaned D4–D6 Repair Verification:** `MutDesign` proved that while D1–D3 and wave-2 findings are mechanistically closed by checks I1–I11, D4 (lesson heading/census syntax), D5 (tally arithmetic), and D6 (SKILL.md table formatting) have *no owning check* in I1–I12. They exist purely as landed documentation and table text, requiring manual closure re-derivation.
3. **The Local Consistency vs Upstream Truth Asymmetry:** `CritInstruments` and `RevC2Shape` proved that C2 counters measure only internal coherence (capture ↔ manifest ↔ row ↔ entry). A maximal twin (variant-F) greens all 9 counters without touching upstream network truth.

### 3.2 The Non-Obvious Move
**"Bidirectional Declared-Blocks & Suite-Digest Anchor Gate"**

Instead of treating `declared-blocks.txt` validation as a one-way walk of declared lines, make I12 bidirectional:
1. **Forward check:** Every declared line is an exact whole-tail append with zero deletions and canonical root resolution (I5 + I12).
2. **Reverse check:** Every path changed in `git diff --name-only base..Y` (excluding only the receipt `.ufo/waves/round-41/final-gates/all-gates.txt`) MUST be present in `declared-blocks.txt`.
3. **Suite-Digest Pin:** In I2's verification, explicitly assert that `receipt.suite-sha256 == sha256(export/corpus/instruments/r41-closure.sh)`.
4. **Tie D4–D6 Repairs to Declared Tails:** Because D4, D5, and D6 are append-only repairs to `round-40.md` and `SKILL.md`, requiring their paths in the bidirectional declared-blocks check guarantees their repair blocks cannot be omitted without tripping I12.

### 3.3 Trace of Second-Order Effects
- **Runtime Surface:** Adding the reverse diff check (`git diff --name-only base..Y`) requires a single read-only git command in I12, adding <10ms to suite runtime while completely closing E6 (undeclared appends).
- **Contract Surface:** Resolves `MutDesign`'s finding that I12 was an orphan check with no routed defect, directly tying I12 to the safe verification of D4–D6 and preventing silent unmonitored file mutations.
- **Substrate Surface:** Binds the receipt to the exact exported instrument bytes at ref Y, closing `MutKillRule` E1 (suite-digest unbound) and `RevReceiptPath`'s synthetic baseline hazard.
- **Verification Surface:** External verifiers can mathematically verify that no out-of-band files were slipped into the commit beyond what the declared-blocks manifest explicitly covers.

### 3.4 Explicit Contradictions Stated
1. **Claims-Freeze Hash Typos:** `claims.json` line 5 specifies `5b29ea1439450b712581edf5f0bf98dfb262ab` (38 characters, missing `f0`), which resolves to no git object. Ground truth is the 40-character commit `5b29ea1439450b712581edf5f0f0bf98dfb262ab`.
2. **CritKillRule Escape Count:** Claims text references "seven CritKillRule escape states", whereas the committed `CritKillRule.md` carries 8 `### F` headings (F1–F8). I11 must grade 8 escapes.
3. **Binding Rule Asymmetry:** `capture-binding-check.py` Rule B binds manifest records to rows, but does not enforce that mined rows have manifest records. A mined row without a manifest record passes binding checks with `unbound=0`.

### 3.5 Risks and Verification
- **Risk:** If a wave-2 artifact or scratch file is inadvertently tracked in git between base and Y, bidirectional I12 will immediately red.
- **Mitigation:** Ensure the L1 commit for J contains only intentional deliverables and documentation appends.
- **Verification:** Run `git diff --name-only <base> <Y>` and compare the set difference against `cut -d' ' -f1 declared-blocks.txt`; the set difference must contain only `.ufo/waves/round-41/final-gates/all-gates.txt`.

---

## 4. Scratch & Host Hygiene

- **Scratch Directory:** Created at `/fast/scratch/hyaku/kasegi-r41/ConnWave2Seed/` at session start.
- **Scratch Cleanup:** Completely removed via `rm -rf /fast/scratch/hyaku/kasegi-r41/ConnWave2Seed` prior to yield. No temporary files left in `/tmp` or `/fast/scratch`.
- **Write Scope:** Written only to:
  1. `.ufo/waves/round-41/wave1/ConnWave2Seed.txt` (deliverable bytes)
  2. `.ufo/waves/round-41/wave1/ConnWave2Seed.md` (this receipt)
- **Git & Tooling Integrity:** No mutating git or jj commands were executed. No packages were installed or upgraded. Fleet root and source repositories remained strictly read-only.
