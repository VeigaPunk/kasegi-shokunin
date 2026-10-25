# ConnClaims — Cross-Claim Pattern Check and UFO-FSD Connector Synthesis (Round 29, Wave 1)

- **Seat**: `ConnClaims-3` (role: `connector`, leaf member — no subagent dispatch)
- **Answering model**: `google-antigravity/gemini-3.8-flash` (workstation route; session default)
- **UTC Timestamp**: 2026-10-25T18:35:00Z
- **Lane**: `kasegi-shokunin` (repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- **Base revision**: `7a6591c1eb8a14f427297980a96fa8bb339f29ee`
- **Freeze revision**: `f28ff5d26b29270f93163117e7255e24f0b1d947`
- **Dispatch revision**: `46e07f6ae8f23debb10034164252e7027b4d9091`
- **Judged on**: `depth:verifiability`, `coverage`

---

## 1. Predicate Sentence Verification

> **Rule (1)**: Verify each claim's predicate sentence appears unchanged in the plan text, in the counter command semantics, and in the receipt label scheme.

### Claim C1 (`depth:verifiability`, held 4)
- **Frozen predicate sentence** (`claims.json:18`):
  `"anchorcheck --selftest reports limbs=9 covered=9 (every declared verdict limb has an isolating failing fixture) and prints selftest cases=12 failures=0, exits 0, and also exits 0 when run with PATH stripped of git (clean skip, no traceback)"`
- **Plan text consistency** (`wave1-spec.json`, `build-spec.py`):
  - **Verdict**: **PARTIAL / UNPACKED**
  - The exact predicate sentence string does not appear verbatim in `wave1-spec.json`. Its clauses are expanded into distinct requirements for `ExecImplC1` (completeness assertion `limbs=9 covered=9`, 12 cases, git-free hermeticity) and `ExecCanonC1`.
- **Counter command semantics**:
  - **Verdict**: **CONGRUENT**
  - Command 0 (`anchorcheck.py --selftest`) verifies exit code 0.
  - Command 1 (`anchorcheck.py --selftest | grep -E 'selftest cases=|limbs='`) emits the `cases=12 failures=0` and `limbs=9 covered=9` output lines.
  - Command 2 (`env -i "PATH=$T" ...`) verifies git-free execution emits `nogit_exit=0`.
- **Receipt label scheme** (`ExecCanonC1`):
  - **Verdict**: **ASYMMETRIC EXTENSION**
  - Labels in `ExecCanonC1`:
    - `(a)` `selftest` -> cases=12 failures=0, limbs=9 covered=9, exit 0 (matches predicate)
    - `(b)` git-free PATH run -> exit 0 (matches predicate)
    - `(c)` `anchorcheck.py SKILL.md` -> exit 0, bad=0, LOST-RECORDED=306 (NOT in predicate sentence; undeclared invariant guard)
    - `(d)` `instrument_sha256` line (in kill rule, NOT in predicate sentence)

### Claim C2 (`coverage`, held 7)
- **Frozen predicate sentence** (`claims.json:35`):
  `"frontier admitted rows increment 12 -> 13 (F13), exactly 1 knowledge entry cites a row first registered this round (S043/S044/S045), registry rows increment 42 -> 45, sources census exits 0, frontier-recheck-count harness entries=16 pass=16 exit=0, and source-recheck exits 0 for each of S043/S044/S045 on the round-29 manifest"`
- **Plan text consistency** (`wave1-spec.json`):
  - **Verdict**: **PARTIAL / DISTRIBUTED**
  - The exact predicate sentence does not appear verbatim. Tasks are distributed across `ExecEntryF13`, `ScribeSourcesGate`, `ScribeReadmeC2`, `ExecManifestC2`, and `ExecCanonC2`.
- **Counter command semantics**:
  - **Verdict**: **MISMATCH (M28-3 defect class)**
  - Predicate asserts: `"registry rows increment 42 -> 45"`.
  - Counter Command 2 executes: `grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md`.
    - This counts newly registered rows (`0 -> 3`), NOT the total registry row count (`42 -> 45`).
  - Counter Command 3 executes: `sources-census.sh validate ...; echo "census_exit=$?"`.
    - `validate` mode checks structure and emits warnings/ok, but does NOT emit total row count.
  - No command in C2's `counter_commands` emits `42` or `45`.
- **Receipt label scheme** (`ExecCanonC2`):
  - **Verdict**: **DISCREPANT (7 receipt labels vs 6 frozen commands)**
  - `ExecCanonC2.md` and `ExecCanonC2.txt` declare 7 numbered receipt items:
    1. frontier admitted awk (13)
    2. entries citing S04[3-5] (1)
    3. S043+S044+S045 rows (3)
    4. registry rows (census) (45) — **split out without a matching counter command**
    5. census validate exit (0)
    6. harness (entries=16 pass=16 exit=0)
    7. per-id rechecks S043/S044/S045 (exit 0 each)

---

## 2. Kill Rule and Failing Control Verification

> **Rule (2)**: Verify each kill rule names a failing control and that control's receipt path.

### Claim C1
- **Kill rule text** (`claims.json:24`):
  `"Fails if any of: selftest cases != 12; failures != 0; limbs != 9 or covered != 9; nogit_exit != 0; or the canonical c1-receipt-index.txt lacks an instrument_sha256 line matching the committed anchorcheck.py digest."`
- **Failing control & receipt path**:
  - Named in paired `do_nothing_control` (`claims.json:25`):
    `"Baseline bytes at base 7a6591c1 (...): grep -cE 'limbs=[0-9]+ covered=' -> 0 (no coverage assertion); git-free PATH run -> exit 1 with FileNotFoundError: 'git' traceback. Receipts in c1-controls/before.txt. Control cannot meet the target."`
  - **Verification of receipt path**:
    `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/c1-controls/before.txt` exists. Lines 8–9 record `0` (fails `covered=9`); lines 11–39 record `FileNotFoundError: 'git'` with `nogit_exit=1` (fails `nogit_exit=0`).
  - **Verdict**: **PASS (with field placement note)**. The failing control and its receipt path are fully specified in `do_nothing_control`, though not inside the `kill_rule` string itself.

### Claim C2
- **Kill rule text** (`claims.json:44`):
  `"Fails if any of: frontier admitted != 13; entries citing S04[3-5] != 1; S043+S044+S045 rows != 3; registry rows != 45; census_exit != 0; harness entries != 16 or pass != 16 or harness_exit != 0; recheck_exit != 0 or any manifest assertion not occurrences=1."`
- **Failing control & receipt path**:
  - Paired `do_nothing_control` (`claims.json:45`):
    `"Baseline at base 7a6591c1: frontier admitted 12, entries citing S04[3-5] 0, rows 42, no round-29 captures exist. Control cannot meet the target."`
  - **Omission**: C2's `do_nothing_control` **fails to name any receipt path**.
  - **On-disk state**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-29/c2-controls/before.txt` actually exists and contains the baseline outputs (12, 0, 1, 1, 42, harness 15/15), but it is omitted from `claims.json`.
  - **Verdict**: **FAIL / ASYMMETRY**. C2 fails to name its control receipt path in `claims.json`.

---

## 3. Counter Commands Syntax, Parsing, and Value Emission (M28-3 Audit)

> **Rule (3)**: Verify every frozen counter command parses (`bash -n` where shell) and can emit its own value — flag any command that cannot produce the number it claims to count (this is the M28-3 defect class).

All 9 frozen counter commands from `claims.json` were parsed via `bash -n -c "<cmd>"` and executed against baseline bytes:

| Claim | Cmd # | Command Summary | `bash -n` | Before Output | Target After | Defect Flag |
|---|---|---|---|---|---|---|
| **C1** | 0 | `python3 corpus/instruments/anchorcheck.py --selftest` | exit 0 | `selftest cases=9 failures=0` (exit 0) | `cases=12 failures=0` (exit 0) | Clean |
| **C1** | 1 | `python3 corpus/instruments/anchorcheck.py --selftest \| grep -E 'selftest cases=\|limbs='` | exit 0 | `selftest cases=9 failures=0` | `cases=12...` + `limbs=9 covered=9` | Clean |
| **C1** | 2 | `T=$(mktemp -d) ... env -i PATH=$T ... anchorcheck.py --selftest ... echo nogit_exit=$E` | exit 0 | `nogit_exit=1` | `nogit_exit=0` | Clean |
| **C2** | 0 | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | exit 0 | `12` | `13` | Clean |
| **C2** | 1 | `grep -lE '^source: S04[3-5] ' corpus/knowledge/*.md \| wc -l` | exit 0 | `0` | `1` | Clean |
| **C2** | 2 | `grep -cE '^\|[[:space:]]*S04[3-5][[:space:]]*\|' corpus/SOURCES.md` | exit 0 | `0` (with exit code 1) | `3` (exit 0) | **DEFECT (M28-3 class)**: Emits `0 -> 3`, cannot emit `42 -> 45`. Grep exits 1 on zero matches. |
| **C2** | 3 | `sources-census.sh validate --root ... kasegi; echo "census_exit=$?"` | exit 0 | `census_exit=0` | `census_exit=0` | **DEFECT (M28-3 class)**: Validates schema, does not emit row count `45`. |
| **C2** | 4 | `python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"` | exit 0 | `entries=15 pass=15 exit=0\nharness_exit=0` | `entries=16 pass=16 exit=0\nharness_exit=0` | Clean |
| **C2** | 5 | `python3 corpus/instruments/source-recheck.py ... S043 && ... S044 && ... S045; echo "recheck_exit=$?"` | exit 0 | `recheck_exit=2` (missing manifest) | `recheck_exit=0` | **STRUCTURAL GAP (CritC2Kill)**: Exits 0 on multi-occurrence unanchored quotes. |

### Detailed Defect Findings:
1. **M28-3 in C2 Counter Command 2 & Predicate Sentence**:
   - The predicate sentence requires `"registry rows increment 42 -> 45"`, and the kill rule requires `"registry rows != 45"`.
   - Command 2 filters for `S04[3-5]` and outputs `0` (before) or `3` (after).
   - Command 3 runs `sources-census.sh validate`, which outputs `census_exit=0` without total rows.
   - **Result**: No frozen command in `claims.json` can produce the number `45`.
2. **Grep Exit Code on Baseline in C2 Command 2**:
   - `grep -cE` exits with status `1` when 0 lines match. In pipelines or strict scripts, this produces an unexpected non-zero exit code during PRE-STATE evaluations.
3. **Unenforced Kill Rule Limb in C2 Command 5**:
   - The kill rule specifies `recheck_exit != 0 or any manifest assertion not occurrences=1`. As proven by `CritC2Kill`, `source-recheck.py` prints `occurrences=53 anchor=MISSING` and exits `0`. The counter command cannot enforce the occurrence constraint through `recheck_exit`.

---

## 4. Causal Separability of C1 and C2 Counters

> **Rule (4)**: Verify C1 and C2 counters are causally separable (C1 reads only anchorcheck.py and its receipts; C2 reads only README/SOURCES/entry/captures).

### Read and Write Footprint Analysis:
- **Claim C1 Execution**:
  - Commands 0, 1, 2 exclusively execute `corpus/instruments/anchorcheck.py --selftest`.
  - Hermetic isolation: `_selftest()` constructs a temporary scratch tree under `tempfile.mkdtemp()`, sets `KASEGI_LANE_ROOT`, `KASEGI_MIRROR`, `KASEGI_ORIGIN_ROOT`, and `KASEGI_BOUNTIES` to subdirectories inside that scratch directory, strips `GIT_*` environment variables, and removes the scratch tree on exit.
  - Zero reads against `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md`, or `corpus/source-snapshots/round-29/*`.
- **Claim C2 Execution**:
  - Commands 0 to 5 read exclusively: `corpus/README.md`, `corpus/knowledge/*.md`, `corpus/SOURCES.md`, `corpus/source-snapshots/round-29/manifest.json`, and snapshots.
  - Zero reads against `corpus/instruments/anchorcheck.py` or `.ufo/waves/round-29/wave1/c1-receipt-index.txt`.
- **Invariant Coupling Surface (`SKILL.md`)**:
  - In `ExecCanonC1`, receipt label `(c)` checks `anchorcheck.py SKILL.md`.
  - Seat `ScribeSkillGate` appends notes for both C1 and C2 to `SKILL.md`.
  - However, `anchorcheck.py SKILL.md` is **not** a frozen counter command in `claims.json` (it is an extra receipt check). Even if evaluated, `SKILL.md` additions are append-only text and do not invalidate C1's verdict classes.
- **Verdict**: **PASS**. C1 and C2 frozen counters are 100% causally separable.

---

## 5. Asymmetries L1 Must Reconcile

1. **Receipt Path Citation Asymmetry**:
   - C1 explicitly names its do-nothing control receipt path (`Receipts in c1-controls/before.txt.`) inside `claims.json`.
   - C2 completely omits its control receipt path from `claims.json`, despite `.ufo/waves/round-29/c2-controls/before.txt` being present on disk.
2. **Predicate Sentence vs. Counter Semantics Asymmetry**:
   - C1 counter commands directly check the exact conditions in its predicate sentence (`cases=12 failures=0`, `limbs=9 covered=9`, `nogit_exit=0`).
   - C2 predicate asserts total registry rows increment `42 -> 45`, but C2 counter command 2 checks new rows `0 -> 3`, leaving total row count uncounted by the frozen counter array.
3. **Receipt Label Scheme Asymmetry**:
   - `ExecCanonC1` introduces 2 extraneous labels `(c)` and `(d)` beyond the predicate sentence.
   - `ExecCanonC2` introduces a 7th item (`registry rows (census): rows=42 -> 45`) that does not map to any of the 6 frozen counter commands.
4. **Kill Rule Enforcement Rigor**:
   - C1 kill rule limbs are self-enforcing via exit code (`anchorcheck.py --selftest` exits 1 if limbs < 9 or cases != 12).
   - C2 kill rule limb `"any manifest assertion not occurrences=1"` is fail-open under `source-recheck.py`, which exits 0 on unanchored duplicate quotes.

---

## 6. UFO-FSD Connector Synthesis: One Non-Obvious Move

### Evidence
1. `claims.json` C2 has an M28-3 gap: Counter Command 2 counts only `S04[3-5]` (emitting 3), while Counter Command 3 runs `sources-census.sh validate` (emitting exit 0). Neither emits the total row count `45` demanded by the predicate sentence and kill rule.
2. `sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi` already exists, is committed, and emits `kasegi\trows\t42` (before) and `kasegi\trows\t45` (after).
3. `CritC2Kill` proved that `source-recheck.py` fails open on multi-occurrence unanchored quotes (exit 0), rendering C2's kill rule limb unfalsifiable via exit code alone.
4. C2's `do_nothing_control` in `claims.json` omitted the citation to `c2-controls/before.txt`.

### Affected Axes
- `depth:verifiability` (score 4): Improved. Resolves frozen counter value emission defect and closes the fail-open gap on capture quote assertions.
- `coverage` (score 7): Held. Maintains exact F13 admission boundaries and preserves registry growth.
- `depth:density` (score 9): Held. No prose-density dilution.

### Proposed Move
**Execute a Unified Claims-Erratum and Counter Re-binding via `sources-census.sh census` and `source-recheck.py` Hardening.**
The L1 should publish `.ufo/waves/round-29/claims-erratum-1.md` containing:
1. **Re-binding C2 Registry Counting**: Explicitly disambiguate C2 Counter 2 as counting *newly registered rows* (`S04[3-5] rows = 3`) and bind the total registry row assertion (`rows = 45`) to the canonical census command:
   ```bash
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi | awk '$1=="kasegi" && $2=="rows" {print $3}'
   ```
2. **C2 Control Path Citation**: Formally record `Receipts in c2-controls/before.txt` in the erratum to restore structural symmetry with C1.
3. **Closing the Q9 Occurrence Blind Spot**: In `corpus/instruments/source-recheck.py`, make unanchored multi-occurrence quotes exit 1 (or invoke `check_q9.py` in the canonical receipt), ensuring that `"any manifest assertion not occurrences=1"` strictly causes `recheck_exit != 0`.

### Risks and Second-Order Effects
- *Runtime*: Zero additional external dependencies; uses existing stdlib and repo scripts.
- *Contract*: Strictly aligns C2 execution with `corpus/QUALITY.md` R11 (counter discrimination) and Q9 (occurrence binding).
- *Substrate*: Eliminates the risk of a non-author verifier failing round 29 on M28-3 or M28-8 recurrence.

### Verification Protocol
1. Run `sources-census.sh census` on lane root; confirm output contains `kasegi\trows\t42` (pre-state) and `45` (post-state).
2. Run `source-recheck.py` against a synthetic multi-occurrence quote in scratch; verify exit code flips from 0 to 1.
3. Confirm all 7 labels in `ExecCanonC2.md` map 1:1 to reproducible, non-crashing command outputs.
