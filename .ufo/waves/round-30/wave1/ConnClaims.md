# ConnClaims — Frozen Claims Reconciliation & UFO-FSD Connector Synthesis (Round 30, Wave 1)

- **Seat**: `ConnClaims-4` (role: `connector`, leaf member — no subagent dispatch)
- **Answering model**: `google-antigravity/gemini-3.8-flash` (session workstation route)
- **UTC Timestamp**: 2026-10-25T19:05:00Z
- **Lane**: `kasegi-shokunin` (repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- **Base revision**: `a94871315cafa368f79c17d8c62d71fddd967986`
- **Claims-freeze commit**: `3c5573541300ba0fd3d89372dda3d841172eaa3f`
- **Judged on**: `depth:verifiability`, `coverage`
- **Milestone**: `round-30`

---

## 1. Frozen Claim Chains (Predicate → Counter → Kill Rule → Receipts)

The frozen claims declared in `.ufo/waves/round-30/claims.json` map into end-to-end verification chains from predicate to before/after receipts:

### Claim C1 (`depth:verifiability`, score held 4)
- **Surface**: Instrument conformance for frontier recheck harness (`frontier-recheck-count.py`) and captured-source checker (`source-recheck.py`), addressing M29-4 (uncaught `FileNotFoundError` traceback on missing entry; duplicate admitted row targets undetected) and M29-3 (Q9 stem != id and non-unique quote without anchor).
- **Predicate Sentence** (`claims.json:25`):
  > "On four committed fixtures: (A1) a frontier row naming a missing entry makes the harness exit 1 with a message naming the row, not a FileNotFoundError traceback; (A2) two admitted rows naming the same entry realpath make the harness exit 1 naming the duplicate; (B1) a source-recheck manifest record whose id != capture file stem exits 1 (reason=stem-mismatch); (B2) a quote occurring twice without a verified anchor exits 1 (reason=occurrence-not-unique)"
- **Counter Commands** (`claims.json:26-31`):
  1. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1; echo "a1_exit=$?"`
  2. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a2; echo "a2_exit=$?"`
  3. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043; echo "b1_exit=$?"`
  4. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045; echo "b2_exit=$?"`
- **Kill Rule** (`claims.json:32`):
  > "Fails if any of: a1_exit != 1 or the A1 stderr/stdout does not name the row id F98; a2_exit != 1 or the A2 output does not name the duplicate entry; b1_exit != 1 or the B1 output lacks reason=stem-mismatch; b2_exit != 1 or the B2 output lacks a failure reason; OR the real corpus regresses (frontier-recheck-count.py on the lane must still pass every admitted row as of the round's final state, and every real manifest recheck that passed at base must still pass)."
- **Before Receipt File**: `.ufo/waves/round-30/c1-controls/before.txt`
  - Digest baseline: `frontier-recheck-count.py` sha256 `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261`; `source-recheck.py` sha256 `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96`.
  - Baseline measurements: A1 exits 1 with `FileNotFoundError` traceback and no row marker; A2 exits 0 with `entries=2 pass=2 exit=0`; B1 exits 0 (`S043:sha256 OK / S043:Q1 OK`); B2 exits 0 (`S045:Q1 OK occurrences=2 anchor=MISSING`).
- **Expected After Files / Evidentiary Artifacts**:
  - Landed instrument digests: `corpus/instruments/frontier-recheck-count.py` (`aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`), `corpus/instruments/source-recheck.py` (`33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`).
  - Seat implementation and mutant reports: `.ufo/waves/round-30/wave1/ExecImplFrontierHarness.md`, `.ufo/waves/round-30/wave1/ExecImplSourceRecheck.md`, `.ufo/waves/round-30/wave1/ExecMutantsC1.md`.
  - Canonical after receipts: `.ufo/waves/round-30/c1-controls/before-run-2.txt`, `.ufo/waves/round-30/wave1/c1-receipt-index.txt`.

---

### Claim C2 (`coverage`, score held 7)
- **Surface**: Frontier F14 "Japanese severity vocabulary and the handling-priority model" (assimilated from `/home/vgpnk/Projects/shokuknow/merge/kasegi`), admitted with entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` citing newly registered S046 (IPA JVN activity report PDF) and S047 (IPA JVN quarterly report HTML/tables) plus registered S041 (JPCERT/CC 2026 guideline), with captures pinned in `corpus/source-snapshots/round-30/manifest.json`.
- **Predicate Sentence** (`claims.json:44`):
  > "frontier admitted rows increment 13 -> 14 (F14); exactly 1 knowledge entry cites a row first registered this round (S046/S047); registry rows increment 45 -> 47; sources census exits 0; frontier-recheck-count harness entries=17 pass=17 exit=0 including PASS F14 ids=S046,S047,S041; source-recheck exits 0 for each of S046/S047/S041 on the round-30 manifest"
- **Counter Commands** (`claims.json:45-52`):
  1. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md`
  2. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l`
  3. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\\|[[:space:]]*S04[6-7][[:space:]]*\|' corpus/SOURCES.md`
  4. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"`
  5. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"`
  6. `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S047 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S041; echo "recheck_exit=$?"`
- **Kill Rule** (`claims.json:53`):
  > "Fails if any of: frontier admitted != 14; entries citing S04[6-7] != 1; S046+S047 rows != 2; registry rows != 47; census_exit != 0; harness entries != 17 or pass != 17 or harness_exit != 0; recheck_exit != 0 or any round-30 manifest assertion not exactly-once (occurrences=1) with stem == id."
- **Before Receipt Files**:
  - `.ufo/waves/round-30/c2-controls/before.txt`
  - `.ufo/waves/round-30/census-before.txt`
  - Baseline measurements: `frontier_admitted=13`, `entries_citing_s046_047=0`, `registry_rows=45`, `census_exit=0`, `harness=entries=16 pass=16 exit=0`.
- **Expected After Files / Evidentiary Artifacts**:
  - `corpus/README.md` (Frontier table: +F14 row; admitted total = 14)
  - `corpus/SOURCES.md` (Registry table: +S046, +S047 rows; registry total = 47)
  - `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (F14 entry)
  - `corpus/source-snapshots/round-30/manifest.json` + `S041.txt`, `S046.txt`, `S047.txt`
  - `corpus/instruments/knowledge-expected.txt` (updated expected entry inventory)
  - Verification reports: `.ufo/waves/round-30/wave1/ExecEntryF14.md`, `.ufo/waves/round-30/wave1/RevC2Registry.md`, `.ufo/waves/round-30/harness-after.txt`, `.ufo/waves/round-30/post-commit-recheck.sh`.

---

## 2. Predicate vs. Counter Congruence & L1 Executable Command List

### Congruence Audit

| Claim | Target Clause | Counter Command | Result on Landed Bytes | Congruence Verdict |
|---|---|---|---|---|
| **C1** | (A1) Missing entry exits 1 naming row F98 | Command 1 (`--root .../harness-root-a1`) | `FAIL F98 knowledge/zz-missing.md ... a1_exit=1` | **CONGRUENT** |
| **C1** | (A2) Duplicate realpath exits 1 naming duplicate | Command 2 (`--root .../harness-root-a2`) | `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md ... a2_exit=1` | **CONGRUENT** |
| **C1** | (B1) Stem != id exits 1 (`reason=stem-mismatch`) | Command 3 (`--manifest .../manifest-b1.json`) | `S043:manifest MISMATCH reason=stem-mismatch ... b1_exit=1` | **CONGRUENT** |
| **C1** | (B2) Double-occurrence exits 1 (`reason=occurrence-not-unique`) | Command 4 (`--manifest .../manifest-b2.json`) | `S045:manifest MISMATCH reason=stem-mismatch ... b2_exit=1` | **DISCREPANT (Stem trips before quote check; see §3)** |
| **C2** | Frontier admitted rows increment 13 -> 14 | Command 1 (`awk ... corpus/README.md`) | `14` | **CONGRUENT** |
| **C2** | Exactly 1 entry cites S04[6-7] | Command 2 (`grep -lE ... \| wc -l`) | `1` | **CONGRUENT** |
| **C2** | Newly registered S046+S047 rows == 2 | Command 3 (`grep -cE ...S04[6-7]...`) | `2` | **CONGRUENT** |
| **C2** | Registry rows increment 45 -> 47 | **NONE** (Omitted from frozen commands) | N/A | **DEFECT (M29-2 class recurrence; see §3)** |
| **C2** | Sources census exits 0 | Command 4 (`sources-census.sh validate`) | `census_exit=0` | **CONGRUENT** |
| **C2** | Harness entries=17 pass=17 exit=0 (incl. F14) | Command 5 (`frontier-recheck-count.py`) | `entries=17 pass=17 exit=0\nharness_exit=0` | **CONGRUENT** |
| **C2** | Source-recheck exits 0 for S046/S047/S041 | Command 6 (`source-recheck.py ...`) | `recheck_exit=0` | **CONGRUENT** |

### Complete L1 Executable Command List for Kill Rules

To evaluate the kill rules of both claims, the L1 executes this unified sequence:

```bash
# === C1 Kill Rule Evaluation Commands ===

# 1. A1 missing-entry fixture check (must exit 1, output must name F98)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1; echo "a1_exit=$?"

# 2. A2 duplicate-target fixture check (must exit 1, output must name duplicate entry)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a2; echo "a2_exit=$?"

# 3. B1 stem-mismatch fixture check (must exit 1, output must contain reason=stem-mismatch)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043; echo "b1_exit=$?"

# 4. B2 double-occurrence fixture check (must exit 1, output must contain failure reason)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045; echo "b2_exit=$?"

# 5. C1 no-regression guard on live lane corpus (must exit 0, all admitted entries pass)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"

# 6. C1 no-regression guard on historical source manifests (must exit 0 for rounds 24, 25, 26, 28, 29)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json; \
  echo "past_manifests_exit=$?"

# === C2 Kill Rule Evaluation Commands ===

# 7. Frontier admitted rows count (must equal 14)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md

# 8. Entries citing newly registered rows S046/S047 (must equal 1)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l

# 9. Newly registered rows S046+S047 count (must equal 2)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S04[6-7][[:space:]]*\|' corpus/SOURCES.md

# 10. Total registry rows count (RESOLVES M29-2; must equal 47)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md

# 11. Sources census schema and validation (must exit 0)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"

# 12. Full frontier harness recheck (must print entries=17 pass=17 exit=0 and exit 0)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"

# 13. Round-30 source-recheck for S046, S047, S041 (must exit 0, assertions exactly-once or anchored-ok)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046 && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S047 && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S041; \
  echo "recheck_exit=$?"
```

---

## 3. Defect Analysis: M29-2 Recurrence & B2 Isolation Defect

### A. M29-2 Class Recurrence in Claim C2 (Unsatisfiable Total Row Counting)
- **Defect Class**: Unsatisfiable instrument in frozen counter array (exact recurrence of `corpus/lessons/round-29.md:193-195` M29-2 / M28-3).
- **Evidence**:
  - The frozen predicate sentence demands: `"registry rows increment 45 -> 47"`.
  - The frozen kill rule demands: `"registry rows != 47"`.
  - C2 Counter Command 2 runs: `grep -cE '^\\|[[:space:]]*S04[6-7][[:space:]]*\\|' corpus/SOURCES.md`. This counts only the newly added rows, emitting `0` (before) and `2` (after).
  - C2 Counter Command 3 runs: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate ...; echo "census_exit=$?"`. In `validate` mode, this script emits validation diagnostics and `census_exit=0`; it does not emit the row count.
  - **No command in the frozen `counter_commands` array produces `47`.**
- **Impact**: Any automated harness or L1 evaluation strictly iterating through the frozen `counter_commands` list cannot observe the scalar value `47` demanded by the kill rule.
- **Resolution**: Command 10 in the L1 command list (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` or `sources-census.sh census`) must be formally recorded in a claims erratum to close the measurement gap.

### B. Compound Defect in C1 B2 Control Fixture (Q9 Isolation Failure)
- **Defect Class**: Non-isolating fixture / Compound mutant failure (violates `corpus/QUALITY.md` R10 and R13).
- **Evidence**:
  - The committed fixture `.ufo/waves/round-30/c1-controls/q9/manifest-b2.json` contains:
    ```json
    { "id": "S045", "path": "B2.txt", "quotes": [ { "id": "Q1", "quote": "vulnerability rating taxonomy crosswalk node" } ] }
    ```
  - The capture path is `B2.txt`, whose stem is `"B2"`. The record id is `"S045"`.
  - Therefore, `manifest-b2.json` contains a **stem mismatch** (`"B2" != "S045"`).
  - In `corpus/instruments/source-recheck.py`, the B1 stem check runs immediately upon loading the record:
    ```python
    if Path(path).stem != source_id:
        emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch")
        return 1
    ```
  - Because the stem mismatch is detected first, execution terminates with exit code 1 and emits `reason=stem-mismatch`. It **never reaches quote occurrence evaluation**.
  - As a result:
    1. The output fails to emit `reason=occurrence-not-unique` (diverging from the predicate sentence).
    2. The required isolating mutant `mutant-B2` (which removes the occurrence check) **cannot flip the fixture to exit 0**, because the mutant still trips the stem check and exits 1 with `reason=stem-mismatch`.
- **Mitigation & Demonstration**:
  - The executor seat `ExecImplSourceRecheck` and mutation seat `ExecMutantsC1` established a clean isolating control under `.ufo/waves/round-30/wave1/ExecImplSourceRecheck-b2/` and `mutants/b2iso/`, where the double-occurrence file is named `S045.txt` (stem == id). Under this isolating fixture, the landed instrument outputs `reason=occurrence-not-unique` (exit 1), and `mutant-B2` flips to exit 0.

---

## 4. Causal Separability of C1 and C2

C1 and C2 are **strictly causally separable** across both working-tree writes and execution paths:

### Footprint Disjointness Matrix

| Surface | Claim C1 Boundary | Claim C2 Boundary | Overlap / Shared State |
|---|---|---|---|
| **Production Code** | `corpus/instruments/frontier-recheck-count.py`<br>`corpus/instruments/source-recheck.py` | None | None |
| **Domain Corpus** | None | `corpus/SOURCES.md`<br>`corpus/README.md`<br>`corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`<br>`corpus/instruments/knowledge-expected.txt` | Disjoint |
| **Source Snapshots** | None | `corpus/source-snapshots/round-30/{manifest.json, S041.txt, S046.txt, S047.txt}` | Disjoint |
| **Control Fixtures** | `.ufo/waves/round-30/c1-controls/{harness-root-a1, harness-root-a2, q9/*}` | None | Disjoint |
| **Receipt Files** | `.ufo/waves/round-30/c1-controls/before.txt`<br>`.ufo/waves/round-30/wave1/c1-receipt-index.txt` | `.ufo/waves/round-30/c2-controls/before.txt`<br>`.ufo/waves/round-30/census-before.txt` | Disjoint |

### Execution Separability Analysis
1. **C1 Runs Independently of C2**:
   - C1 counter commands 1 and 2 operate against isolated mock roots (`--root .../harness-root-a1` and `--root .../harness-root-a2`). They inspect only their contained mock `corpus/README.md` and mock entries (`dup-entry.md`), without touching the live lane corpus or round-30 entries.
   - C1 counter commands 3 and 4 operate against fixture manifests under `c1-controls/q9/`, completely decoupled from live snapshots.
   - C1 can be 100% verified even if F14, S046, and S047 are completely absent.
2. **C2 Uses C1 Instruments Cleanly**:
   - C2 counter commands 5 and 6 execute the instruments modified by C1.
   - The modifications introduced by C1 (named missing row, duplicate realpath prohibition, stem == id binding, and unanchored duplicate quote prohibition) are fully satisfied by C2's landed work:
     - All 17 entries have distinct realpaths and existing markdown files.
     - All round-30 sources have stems matching their record ids (`S041.txt` -> `S041`, `S046.txt` -> `S046`, `S047.txt` -> `S047`).
     - In `corpus/source-snapshots/round-30/manifest.json`, duplicate quotes carry verified line anchors (`S047:Q1` anchor=123-ok, `S047:Q3` anchor=130-ok), so no assertion fails the B2 gate.
   - Therefore, while C2 depends on the correctness of the instruments, the claims do not interfere with or invalidate each other's verification boundaries.

---

## 5. UFO-FSD Connector Synthesis: One Non-Obvious Move

### Evidence
1. **M29-2 Re-emergence**: `claims.json` frozen counter array for C2 omits any command emitting the scalar `47` for total registry rows, while `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` and `sources-census.sh census` already evaluate cleanly to 47.
2. **B2 Isolation Defect**: The committed `manifest-b2.json` fixture has an unanchored compound defect (`B2.txt` != `S045`), meaning the B2 limb is masked by the B1 stem check. An isolating fixture `mutants/b2iso/` already exists and demonstrates clean mutant flipping.
3. **Q10 Conformance Friction on Mined Proposal 4**: In this round, `considerthese/2026-10-25.md` proposal 4 was successfully mined into durable knowledge entry `corpus/knowledge/considerthese-proposals-ledger.md`. However, its recheck line was written with a leading prose cadence (`recheck: 180d — cd /home/...`), causing `corpus/instruments/recheck-audit.py` to fail closed with exit code 1 (`strict pass=42/43 ... FROZEN-ONLY`). Under Q10, recheck commands must be directly executable, with human notes following a `#`.

### Affected Axes
- `depth:verifiability` (score 4): **Improved**. Eliminates the uncounted total registry row gap (M29-2), repairs fixture isolation for the Q9 occurrence limb (R10/R13), and enforces strict Q10 recheck syntax compliance across all 43 knowledge entries.
- `coverage` (score 7): **Held**. Preserves the admission of F14 (`japanese-severity-vocabulary-and-impact-model.md`), S046, and S047, while keeping proposal-4 ledger registered.
- `depth:density` (score 9): **Held**. Zero dilution of existing density or table structures.

### Proposed Move
**Promote an Integrated Claims-Erratum & Recheck Syntax Realignment (`claims-erratum-r30.md`).**

The L1 should append `.ufo/waves/round-30/claims-erratum-r30.md` incorporating three co-dependent alignments:
1. **Disambiguate C2 Registry Counters**: Record that frozen C2 Counter 2 measures *newly registered rows* (`S046+S047 = 2`), and officially append the canonical census counter:
   ```bash
   cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
   ```
   yielding `47`, satisfying the kill rule's `registry rows != 47` clause.
2. **Adopt the Isolating B2 Fixture**: Formally document the supplementary fixture `.ufo/waves/round-30/c1-controls/mutants/b2iso/manifest.json` (where capture stem is `S045.txt`) as the isolating control for mutant-B2, establishing compliance with `corpus/QUALITY.md` R10/R13 while explaining why the frozen fixture trips B1 first.
3. **Align `considerthese-proposals-ledger.md` with Q10**: Format the recheck line in `corpus/knowledge/considerthese-proposals-ledger.md` to:
   ```markdown
   recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -f considerthese/2026-10-25.md && test -f corpus/QUALITY.md && test -f corpus/lessons/round-29.md && test -f corpus/lessons/round-28.md # 180d
   ```
   This immediately flips `recheck-audit.py` from `strict pass=42/43 exit=1` to `strict pass=43/43 exit=0`.

### Risks and Second-Order Effects
- *Runtime*: Zero runtime overhead; relies strictly on existing Python instruments and POSIX shell utilities.
- *Contract*: Enforces strict adherence to `corpus/QUALITY.md` Q9 (occurrence binding), Q10 (recheck line executable formatting), and R13 (isolating mutants).
- *Substrate*: Eliminates the risk of a non-author verifier spot-check flagging M29-2 recurrence, B2 mutant masking, or recheck-audit failure.

### Verification Protocol
1. Re-run `recheck-audit.py`: verify that all 43 knowledge entries pass strict evaluation (`expect=present expected=43 missing=0 unexpected=0 exit=0`).
2. Run the 13-command L1 sequence in §2; verify that all exit codes match the required zero/non-zero targets and that total registry rows emit `47`.
3. Execute `python3 corpus/instruments/source-recheck.py` on `mutants/b2iso/manifest.json` with `mutant-b2.py`; confirm exit code flips cleanly from 1 to 0.
