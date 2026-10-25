# ConnClaims — Cross-Claim Pattern Check (Round 28 Wave 1)

**Seat**: ConnClaims (connector, read-only leaf)  
**Lane**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`  
**Base**: `c9f8b115a098c65356e4b3b6048af45a37ab8395` (claims freeze commit)  
**Report**: `.ufo/waves/round-28/wave1/ConnClaims.md` (no production edits)

---

## 1. Failing Controls Demanded by Kill Rules & Receipt Paths

Both claims share the principle of fail-closed verification: the claim is void if a control fails to demonstrate the required failure mode.

### C1 (depth:verifiability)
- **Kill Rule** (`claims.json:36`):
  > `"any counter misses its after value; or the do-nothing control (pre-change instrument bytes) reaches any after value; or the SKILL.md live run exits nonzero, its bad count moves, or its verdict-class counts move; or a selftest fixture is shown non-isolating (a fixture that fails a limb other than its own, or a limb with no failing fixture)"`
- **Failing Controls & Receipt Paths**:
  1. **Do-Nothing / Pre-change Control**: Unchanged committed `anchorcheck.py` bytes (`c2a9e6c6...`) executed against `.ufo/waves/round-27/c1-controls/bad-fixture.md` and `bounties-fixture.md`.
     - *Receipt Path (Before)*: `.ufo/waves/round-27/c1-controls/bad-fixture-before.txt` and `.ufo/waves/round-28/c1-controls/bad-fixture-before.txt` (shows `BASE-ABSENT`, `exit=0`).
     - *Fail Demand*: Under pre-change bytes, it must fail to reach after values (exits 0, 0 BOUNTIES lines). Under post-change bytes, bad-fixture MUST fail closed with `exit 1`.
  2. **Unverifiable Citation Bad-Fixture Control (Counter a)**:
     - *Control*: `.ufo/waves/round-27/c1-controls/bad-fixture.md` (cites nonexistent `zz-r27-anchorcheck-missing.md:99`, resolving to `BASE-ABSENT`).
     - *Receipt Path (Post-change)*: Counter (a) in `.ufo/waves/round-28/c1-receipt-index.txt` (and `.ufo/waves/round-28/receipts/ExecFixtureRun.txt`).
     - *Fail Demand*: Must fail closed with exit code `1` (previously exit 0).
  3. **Limb-Isolating Selftest Fixtures (Counter c)**:
     - *Control*: `anchorcheck.py --selftest` isolating fixtures for each limb (`MISSING-FILE`, `PAST-EOF`, `OUTSIDE-BASE`, `PIN-BROKEN`, `BASE-ABSENT`, `BOUNTIES-ABSENT`).
     - *Receipt Path*: `.ufo/waves/round-28/c1-receipt-index.txt` (and `.ufo/waves/round-28/receipts/ExecInstrSelftest.txt`).
     - *Fail Demand*: Every fixture must fail *only* its designated limb in isolation; any fixture failing another limb or any limb lacking a failing fixture triggers the kill rule.

### C2 (coverage)
- **Kill Rule** (`claims.json:65`):
  > `"a source row appended without an admitted entry citing it; census exit != 0 at round end; harness pass < entries; the entry's recheck --source ids differ from its declared source: ids; any manifest quote assertion not exactly-once (or anchor-broken)"`
- **Failing Controls & Receipt Paths**:
  1. **Do-Nothing Control**: The un-admitted baseline state without F12, S042, or the workflow entry.
     - *Receipt Path (Before)*: `.ufo/waves/round-27/c2-controls/before.txt` re-run at `.ufo/waves/round-28/c2-controls/before.txt` (`frontier_admitted=11`, `entries_citing_S042=0`, `sources_rows=41`, `entries=14 pass=14 exit=0`).
     - *Fail Demand*: The un-admitted tree cannot reach after values (must stay at 11 admitted, 0 citing, 41 rows, 14 entries).
  2. **Fail-Closed Manifest Quote Assertion Control**:
     - *Control*: `source-recheck.py` validating quote assertions in `corpus/source-snapshots/round-28/manifest.json` against `S041.txt` and `S042.txt`.
     - *Receipt Path*: `corpus/source-snapshots/round-28/manifest.json` checked via `source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041` and `--source S042`, receipted in `.ufo/waves/round-28/receipts/ExecManifest.txt`.
     - *Fail Demand*: If any quote is missing (`MISMATCH`, exit 1), unreadable (`UNAVAILABLE`, exit 2), not exactly-once, or anchor-broken, the check fails closed.
  3. **Assimilation Gate Reject Control**:
     - *Control*: Refusal candidate evaluated under QUALITY bar gates (e.g., `chinese-criminal-thresholds-and-authorisation.md` or `vendor-third-party-finding-coordination.md`).
     - *Receipt Path*: Round-28 lesson `## Gate` table (and `.ufo/waves/round-28/wave1/ScoutAssimilation.md`).
     - *Fail Demand*: C2 predicate explicitly demands `>=1 reject with inline <=25-word quotes`; absence of a measured, evidence-backed rejection fails the gate.

---

## 2. sha256 Binding Sentences Comparison: C1 Counter (c) vs C2 Counter (3)

### C1 Counter (c) Binding Sentence
In `claims.json`:
- **Predicate Limb (c)** (`claims.json:12`):
  > `"(c) anchorcheck.py --selftest runs one isolating fixture per limb and prints selftest cases=N failures=0, committed in the round receipt index at the instrument's own sha256;"`
- **After State** (`claims.json:25`):
  > `"selftest_receipt_lines": "1 at instrument_sha256 matching sha256sum corpus/instruments/anchorcheck.py, selftest cases=N failures=0 exit=0"`
- **Counter Command (c)** (`claims.json:33`):
  > `"grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt && grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt && sha256sum corpus/instruments/anchorcheck.py | awk '{print \"instrument_sha256=\"$1}' && python3 corpus/instruments/anchorcheck.py --selftest >/dev/null 2>&1; echo selftest_exit=$?"`

### C2 Counter (3) Sentence
In `claims.json`:
- **Counter Command (3)** (`claims.json:62`, index 2 of `counter_commands`):
  > `"grep -cE '^\\|[[:space:]]*S042[[:space:]]*\\|' corpus/SOURCES.md ; /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?"`
- **After State** (`claims.json:56`):
  > `"sources_rows": "42, census exit 0, S042 row present"`
- **Predicate sha256 Reference** (`claims.json:46`):
  > `"the manifest pins both captures (path stem equals id, sha256, Q9-conformant quote assertions) and source-recheck exits 0 on both ids"`

### Shape Confirmation & Contradiction Finding
**The binding sentence is NOT the same shape in both.**
- For C1, counter (c) explicitly binds a receipt file (`.ufo/waves/round-28/c1-receipt-index.txt`) to the tool's live hash (`instrument_sha256=[0-9a-f]{64}` matching `sha256sum corpus/instruments/anchorcheck.py`).
- For C2, counter (3) does **not** bind a receipt to a sha256; it only greps `SOURCES.md` and validates census syntax.
- The sha256 binding in C2 exists only in the **predicate** and inside `manifest.json` (`"sha256": "..."`), which is checked by `source-recheck.py`. But `source-recheck.py` is not among C2's 4 frozen `counter_commands` (it is invoked only indirectly via `frontier-recheck-count.py`).

---

## 3. Asymmetries the L1 Must Reconcile Before Canonical Receipts Land

1. **Receipt Index Asymmetry**:
   - C1 has a dedicated, frozen-counter-checked canonical receipt index file: `.ufo/waves/round-28/c1-receipt-index.txt`.
   - C2 has no independent canonical receipt index file (`c2-receipt-index.txt` does not exist in `claims.json`).
   - In `assemble-receipts.py`, C2 counters are appended into `c1-receipt-index.txt`, but only counts (`frontier_admitted`, `entries citing S042`, `s042_rows`, `frontier harness`).
2. **Missing Manifest Quote & Capture sha256 in Canonical Index**:
   - `assemble-receipts.py` omits `source-recheck.py` output and capture sha256 checks (`S041:sha256 OK`, `S042:sha256 OK`, Q1-Q6 assertion tallies).
   - Although C2's kill rule kills the round if any manifest quote is not exactly-once or anchor-broken, the assembled canonical receipt index currently records zero manifest quote verification lines!
3. **Control Fixture Asymmetry**:
   - C1 has negative control fixtures checked in under `.ufo/waves/round-28/c1-controls/` (`bad-fixture.md`, `bounties-fixture.md`).
   - C2 has only an aggregate before receipt in `c2-controls/before.txt`; negative mutation fixtures (e.g. broken quote, mutated sha256) exist only as wave-1 subagent scratch (`MutQuoteC2`, `MutManifestC2`) rather than committed controls.

---

## 4. Scan of Prior Defects (Lessons Round-25 & Round-26) & Round-28 Closures

### Lesson Evidence & Lines
1. **Defect R25-2 (Receipt Cross-Reference & Pre-Change Trap)**:
   - *Lesson 26 Evidence* (`corpus/lessons/round-26.md:82-84`, **M26-1**):
     `"M26-1 · the receipt index was written before the instrument change landed (R25-2's own trap). Class: pinned-value path written against pre-change bytes. Evidence: c1-receipt-index.txt pins instrument_sha256=c3c19adc… and selftest cases=14 failures=0 while the landed instrument is 3fc0d751… with selftest cases=15..."`
   - *Lesson 26 Compliance* (`corpus/lessons/round-26.md:101-102`):
     `"| R25-2 · selftest tally not in the committed receipt ... | Fixed and measured: c1-receipt-index.txt now carries a selftest cases=… failures=0 line and an explicit cross-reference correction note..."`
   - *Lesson 26 Fix Control* (`corpus/lessons/round-26.md:110`):
     `"2. Selftest receipt in c1-receipt-index.txt (C1(b); R25-2, M26-1). Control: grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt → 1, AND the index's instrument_sha256 must equal sha256sum corpus/instruments/recheck-audit.py at commit..."`
2. **Defect 4 (Canonical Receipt Index at Landed Digest / No Mid-Wave Artifacts)**:
   - *Lesson 26 Verifier Spot-Check* (`corpus/lessons/round-26-verifier-spotcheck.md:78`):
     `"4. Note only: mid-wave e1-selftest-live.txt shows a completeness meta-line (lines=13 total=15 complete=False) while the regenerated index claims 15/0/0; keep the canonical receipt at the landed digest and prune stale receipt artifacts to avoid ambiguity."`
   - *Lesson 27 Carry-Forward* (`corpus/lessons/round-27.md:68-69`):
     `"...single canonical receipt at the landed digest, no mid-wave receipt artifacts (defect 4)."`

### Round-28 Dispatch Requirements Closure
In `claims.json:78`:
> `"one canonical receipt index at the landed instrument digest; no mid-wave receipt artifacts (round-26 routed defect 4)"`

**How Round-28 Closes Them**:
1. **No Mid-Wave Canonical Artifacts**: Per `build-wave1-spec.py:342-355`, executor seats (`ExecReceiptCanonC1`, `ExecReceiptCanonC2`) are strictly instructed to output draft text blocks or write to `receipts/<SeatName>.txt`. No leaf seat writes `.ufo/waves/round-28/c1-receipt-index.txt`.
2. **Post-Landing Assembly by L1**: `assemble-receipts.py` is invoked once after all production edits land. It dynamically reads `sha256sum corpus/instruments/anchorcheck.py` on disk and runs `--selftest` live, eliminating the pre-change digest trap (M26-1).
3. **Counter (c) Enforces Integrity**: Counter (c) in `claims.json:33` directly couples `grep -oE 'instrument_sha256=...'` from the index to `sha256sum corpus/instruments/anchorcheck.py`. Any mismatch or stale receipt fails the counter.

---

## 5. Non-Obvious Move (Synthesis & Proposal)

- **Evidence**: `assemble-receipts.py` assembles C1's instrument sha256, selftest, and fixtures alongside C2's counting checks, but completely omits `source-recheck.py` verification of the round-28 manifest captures (`S041.txt`, `S042.txt`) and their 12 quote assertions.
- **Affected Axes**: `depth:verifiability` (score 4 held), `coverage` (score 7 held).
- **Proposed Move**:
  Extend `assemble-receipts.py` to execute:
  ```bash
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
  ```
  and append their `:sha256 OK` and `:Q[0-9]+ OK` verdicts into the canonical receipt index before final commit.
- **Risks**: Modifying the receipt assembler during wave execution. Mitigation: Leaf seats do not edit `assemble-receipts.py`; this recommendation is handed off to L1 for the final post-wave assembly.
- **Verification**: Run `assemble-receipts.py`, inspect `.ufo/waves/round-28/c1-receipt-index.txt`, and confirm that both `instrument_sha256` and manifest `source-recheck.py` lines are present and exit 0.
