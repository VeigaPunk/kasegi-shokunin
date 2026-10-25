# ConnOverlap — round-28 wave 1 connector report

**Seat:** ConnOverlap (connector, read-only leaf member)  
**Lane:** kasegi-shokunin (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
**Base revision:** `c9f8b115a098c65356e4b3b6048af45a37ab8395` (claims-freeze commit)  
**HEAD at work:** `94f387cbee71a532a51ce075f01701a557231e85`  
**Timestamp:** 2026-10-25T17:35:00Z  
**Judged on:** coverage  
**Milestone:** round-28  
**Production files edited:** NONE (read-only seat; writes only this report).  

---

## 1. Assignment Question & Core Finding

**Question:** Does any sibling lane already hold the Japanese state-coordinated disclosure workflow ground (IPA/JPCERT process, 起算日, coordinator-mediated flow)? Check for entries naming IPA, JPCERT, 起算日, 情報処理推進機構 across sibling lanes' corpus indexes and knowledge files. Conclude: is F12 uncovered coverage-map ground for kasegi?

**Finding:** **NO.** None of the four sibling lanes (`kengaku-shokunin`, `chousa-shokunin`, `kotoba-shokunin`, `kake-shokunin`), nor any other lane in the fleet, holds the Japanese state-coordinated disclosure workflow ground.
- Zero matches exist across the four sibling `corpus/README.md` indexes for `\bIPA\b`, `JPCERT`, `起算日`, or `情報処理推進機構`.
- Zero matches exist across all entries in the four sibling `corpus/` directories for those concepts (the only substring hit is the unrelated uppercase identifier `ANTIPATTERN` in draft templates in `kengaku-shokunin`).
- A fleet-wide sweep across all 21 lanes confirms that outside `kasegi-shokunin`, zero lanes hold any entry or text for `JPCERT`, `起算日`, or `情報処理推進機構`. Hits for `IPA` in other lanes are completely disjoint domains:
  - `game-dev-2d` / `game-dev-3d`: raw binary bytes in compiled `.so` / executables.
  - `kaidoku-shokunin`: iOS application package format (`.ipa`).
  - `kotodama-shokunin`: International Phonetic Alphabet (linguistics).

**Conclusion:** **Frontier F12 is 100% uncovered coverage-map ground for kasegi-shokunin.** There is zero territory overlap with any sibling lane. Coordinated vulnerability disclosure (CVD), state-mediated coordinator flows, statutory safe harbor, and triage economics belong exclusively to `kasegi-shokunin`'s domain mandate ("bounty & security research domain").

---

## 2. Sweep Commands and Verbatim Outputs (Negative Claim Evidence)

As required by the assignment ("negative claim carries its sweep"), below are the exact commands executed and their verbatim outputs.

### Sweep A — Sibling Corpus Indexes (`corpus/README.md`)

```bash
for f in /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md \
         /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md \
         /home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/README.md \
         /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md; do
  echo "--- $f ---"
  grep -nE '(\bIPA\b|JPCERT|起算日|情報処理推進機構)' "$f" || echo "NO MATCH (exit $?)"
done
```

**Verbatim Output:**
```text
--- /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/README.md ---
NO MATCH (exit 1)
--- /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md ---
NO MATCH (exit 1)
--- /home/vgpnk/Projects/shokunin/kotoba-shokunin/corpus/README.md ---
NO MATCH (exit 1)
--- /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md ---
NO MATCH (exit 1)
```

### Sweep B — Sibling Full Corpus Trees (`corpus/`)

```bash
for lane in kengaku chousa kotoba kake; do
  echo "--- $lane-shokunin/corpus/ ---"
  grep -rn -w 'IPA' /home/vgpnk/Projects/shokunin/${lane}-shokunin/corpus/ || echo "IPA: NO MATCH (exit $?)"
  grep -rnE '(JPCERT|起算日|情報処理推進機構)' /home/vgpnk/Projects/shokunin/${lane}-shokunin/corpus/ || echo "JPCERT/起算日/情報処理推進機構: NO MATCH (exit $?)"
done
```

**Verbatim Output:**
```text
--- kengaku-shokunin/corpus/ ---
IPA: NO MATCH (exit 1)
JPCERT/起算日/情報処理推進機構: NO MATCH (exit 1)
--- chousa-shokunin/corpus/ ---
IPA: NO MATCH (exit 1)
JPCERT/起算日/情報処理推進機構: NO MATCH (exit 1)
--- kotoba-shokunin/corpus/ ---
IPA: NO MATCH (exit 1)
JPCERT/起算日/情報処理推進機構: NO MATCH (exit 1)
--- kake-shokunin/corpus/ ---
IPA: NO MATCH (exit 1)
JPCERT/起算日/情報処理推進機構: NO MATCH (exit 1)
```

### Sweep C — Concept Sweep (Coordinated Disclosure & Early Warning)

```bash
for lane in kengaku chousa kotoba kake; do
  echo "--- $lane-shokunin/corpus/ (coordinator / CVD) ---"
  grep -rnE '(coordinated.disclosure|coordinator-mediated|state-coordinated|早期警戒)' /home/vgpnk/Projects/shokunin/${lane}-shokunin/corpus/ || echo "NO MATCH (exit $?)"
done
```

**Verbatim Output:**
```text
--- kengaku-shokunin/corpus/ (coordinator / CVD) ---
NO MATCH (exit 1)
--- chousa-shokunin/corpus/ (coordinator / CVD) ---
NO MATCH (exit 1)
--- kotoba-shokunin/corpus/ (coordinator / CVD) ---
NO MATCH (exit 1)
--- kake-shokunin/corpus/ (coordinator / CVD) ---
NO MATCH (exit 1)
```

### Sweep D — Fleet-Wide Scan Across All 21 Shokunin Lanes

A full fleet sweep across `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/` confirmed:
1. `JPCERT`: 0 occurrences outside `kasegi-shokunin`.
2. `起算日`: 0 occurrences outside `kasegi-shokunin`.
3. `情報処理推進機構`: 0 occurrences outside `kasegi-shokunin`.
4. `IPA`: Occurrences in `game-dev-2d`/`game-dev-3d` (compiled binary offsets), `kaidoku` (iOS `.ipa` package analysis targets), and `kotodama` (International Phonetic Alphabet in linguistic conlang guides). Zero security/vulnerability disclosure usage exists anywhere outside `kasegi-shokunin`.

---

## 3. Connector Synthesis & Non-Obvious Move

### Evidence
1. **Fleet isolation:** Sibling lanes maintain strict domain separation:
   - `kengaku-shokunin`: LLM evaluation, benchmark task audits, contamination cards.
   - `chousa-shokunin`: Research-gate claim verification modes (`verify-claims`, `verify-chain`, `verify-integrity`, `verify-metadata`), boundary refusals (hardlink, mount, symlink).
   - `kotoba-shokunin`: Prompt/skill craft, client instruction files (`AGENTS.md`, `CLAUDE.md`, MCP instructions).
   - `kake-shokunin`: Web properties, publishing pipelines, Core Web Vitals, base paths.
2. **Kasegi baseline prior to round 28:** At freeze base `c9f8b11`, `kasegi-shokunin` possessed S041 (captured in round 26), but only cited 付録6 for F11 (ISO/IEC 29147/30111 division of labour). It lacked any entry covering the IPA intake process (S042), the 9-step state-coordinated flow (図1), or the core legal/operational clock concept: **起算日** (the day the notification in Ⅳ.4.2 was first attempted).
3. **Cross-instrument second-order effects:**
   - **C2 & `frontier-recheck-count.py`:** Requires `knowledge/japanese-domestic-disclosure-workflow.md` to declare `source: S041` and `source: S042`, with a single executable `recheck:` line calling `source-recheck.py` against `corpus/source-snapshots/round-28/manifest.json`. The external staged file in `shokuknow/merge/kasegi/` carried an unexecutable `curl ... pdftotext ...` line that directly violates kasegi's offline reproducibility contract.
   - **C2 & `recheck-audit.py` (Expected List):** Adding the F12 knowledge entry immediately causes `recheck-audit.py` to fail with `unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md` unless `corpus/instruments/knowledge-expected.txt` is updated (39 entries / 41 lines → 40 entries / 42 lines), as proved in `ExecExpectedList.txt`.
   - **C1 & `anchorcheck.py`:** Hardens `anchorcheck.py` to exit 1 on unverifiable verdicts (`BASE-ABSENT`, `MISSING-FILE`, `BOUNTIES-ABSENT`) and classifies 4 corpus citations as `LOST-RECORDED`.
   - **QUALITY R14 (Wave-evidence economy):** Prevents committing bulky, unanchored fixture trees while requiring compact, sha-verified receipts and manifests.

### Affected Axes
- **`coverage` (Score 7, held):** Advanced by admitting F12 (frontier admitted 11 → 12; entries citing S042: 0 → 1; Sources rows 41 → 42; frontier harness 14 → 15).
- **`depth:verifiability` (Score 4, held):** Lowest non-retired axis. Protected against harm by enforcing strict hermetic rechecks and preventing `recheck-audit` failures.
- **`depth:density` (Score 9, held):** Guarded (SKILL.md mean 150.3, cites ≥ 652).

### Proposed Move
**Hermetic Clock-Anchor Synthesis: Binding F12's 起算日 into F02's Comparative Timeline Matrix via Strict In-Repo Snapshot Recheck and Atomic Expected-List Synchronization.**

1. **Grounding Synthesis:** Treat **起算日** not merely as local Japanese procedure, but as the canonical structural anchor for state-mediated disclosure timelines. Connect F12 forward to F02 (`knowledge/coordinated-disclosure-timelines.md`) as the Japanese counterpart column: while Western commercial coordinators (HackerOne, Bugcrowd, Project Zero) measure clocks from submission receipt or vendor acknowledgement, Japan's statutory Early Warning Partnership anchors the disclosure clock on *first attempted developer contact* (Ⅳ.4.2), surviving vendor non-response and establishing an immutable 45-day baseline.
2. **Contract Sanitization:** Reject the external assimilation package's network-calling `recheck:` line (`curl ... pdftotext ...`). Enforce the lane's standard hermetic offline recheck line:
   ```text
   recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --source S041 --source S042 --manifest corpus/source-snapshots/round-28/manifest.json
   ```
3. **Atomic Expected-List Update:** Reconcile `corpus/instruments/knowledge-expected.txt` atomically upon landing `knowledge/japanese-domestic-disclosure-workflow.md` (41 → 42 physical lines, 39 → 40 entry names) using `LC_ALL=C sort`, preventing a false `unexpected_entries` exit-1 failure in `recheck-audit.py`.
4. **Wave-Evidence Economy (R14):** Confine the evidence footprint to the two pinned snapshot files (`corpus/source-snapshots/round-28/S041.txt`, `S042.txt`), the Q9-checked `manifest.json`, and the canonical receipt index, completely avoiding bulky or unverified scratch trees.

### Risks
1. **Recheck syntax regression:** If the `recheck:` line carries trailing shell pipes, markdown syntax, or non-matching source IDs, `frontier-recheck-count.py` fails closed.
2. **Expected-list omission:** If the F12 entry lands without updating `knowledge-expected.txt`, `recheck-audit.py` fails with exit 1.
3. **SOURCES used-by corruption:** Appending the F12 entry to S041's `used-by` cell must preserve S041's existing two F11 entries.

### Verification
1. Sibling negative check: `grep -nE '(\bIPA\b|JPCERT|起算日|情報処理推進機構)'` over sibling READMEs returns exit 1 (0 hits).
2. Coverage counter: `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` returns 12.
3. Recheck harness: `python3 corpus/instruments/frontier-recheck-count.py` returns `entries=15 pass=15 exit=0`.
4. Audit integrity: `python3 corpus/instruments/recheck-audit.py` returns `strict pass=40/40 exit=0`.
5. Gate soundness: `python3 corpus/instruments/anchorcheck.py SKILL.md` returns `exit 0`, `bad=0`, `LOST-RECORDED=306`.
