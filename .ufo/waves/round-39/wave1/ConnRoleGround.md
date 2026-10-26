# ConnRoleGround — connector receipt (round 39, wave 1)

Seat: connector, leaf (no subagents). Claims assessed: C1 depth:verifiability (held 4), C2 coverage (held 7). Milestone round-39.

## Deliverable
- `ConnRoleGround.conn.md` (beside this receipt): 39 lines, sha256 `24156bedff99e62c93304a8b960e069d0806cb68552930c4d58f5b96edd8061b`.
- Landable text only (no validation tables); evidence is in this receipt.

## 1. Overlap (C1 suite × C2 capture)
Frozen input read: `.ufo/waves/round-39/claims.json` (C1 predicate w/ G1-G8, C2 predicate), `c1-controls/before.txt`, `c2-controls/before.txt`, `c2-controls/junk-f22.md`, `census-before.txt`; lane head `d65d823` (wave1 spec/dispatch), base `480b1a50…`, freeze `dcd31701…`.

Shared paths (both claims land text in the same lane file):
- `corpus/lessons/round-39.md` — C1 Mistakes rows (ExecMistakesDraft) + C2 Gate section (ScribeLessonGate, ScoutSiblingF22 ruling); C1 kill rule also monitors it (`⟨pending` = 0).
- `SHONEN.md` — C1 R2 correction appends (ExecCorrectionsR2) + C2 round-39 box lines (ScribeShonen); read by C1 G3/G5.
Junction surfaces:
- `declared-blocks.txt` (C1 G1) must cover every appended block at J, including all C2 files (`SOURCES.md`, `README.md`, `PROVINCE.md`, `S057.txt`, `manifest.json`, knowledge entry, lesson). G1 is a whole-tree gate.
- `corpus/instruments/knowledge-expected.txt` must gain the new entry (+1, C-locale-correct) or C2 `recheck-audit` cannot print `expected=51 missing=0 unexpected=0`.
- Knowledge count `ls corpus/knowledge/*.md` = 51 ⇒ C1 may not add a new knowledge file (it only edits the ledger in place, G7 — confirmed by ExecConsidertheseLedger deliverable shape).
Verified non-overlaps: `grep -nE "open\(|Path\(|glob\(…"` on `frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`, `recheck-audit.py` shows only C2-surface reads (README/knowledge/SOURCES/snapshots); none touches r39-closure.sh, declared-blocks.txt, final-gates/, or G-quoted files. C1 reads C2 content only via the whole-tail declaration.

## 2. Role routing verification
- `wave1-spec.json`: 49 items; roles exactly {executor 27, scribe 11, reviewer 6, scout 2, connector 1, critic 2}; no other role value.
- Token scan (case-insensitive mercury/claude/gpt/llama/gemini/deepseek/qwen/mistral/anthropic/openai/inception) over context (7033 B), all 49 prompts, `wave1-dispatch.json` (49 tasks; task `agent` field = role names only), `kasegi-r39-build.ready(.dispatched)`, `wave1-plan.out`, `wave1/swarm-registry.json`: 0 hits. "model" appears only as prose (fence-walk model, "never pass a model", "modelled on").
- Axes arrays carry axis names only.
Result: wave context passes no model; the spec carries roles only. No defect.

## 3. Proposed integration order (causally separable)
1. Content: land all seat deliverables; L1 assembles appends (C2 rows/entry/frontier/provenance/search-log/Gate; C1 suite/corrections/scorecard/ledger/Mistakes/SHONEN box) and syncs `knowledge-expected.txt` (+1). No content edits after.
2. Declaration: generate `declared-blocks.txt` from final diff base..worktree (includes C2 files); commit J.
3. Measurement: suite on J green, base/r38-head red, graded selftest; `final-gates/` transcripts; C2 counters run here (receipt-independent).
4. Receipt: write `all-gates.txt` (export-ref=J, suite-sha256, 8 graded G lines); commit Y = J + receipt only.
5. Verification only on committed bytes; no further writes.
Invariants: no edit after J (G2 diff J..Y = receipt only); declared-blocks regenerated after all appends; receipt last (only self-referential artifact; names J which cannot contain it); C2 depends on zero C1 artifacts; C1 depends on C2 only statically via declarations.

## Risks noted
- If L1 computes declared-blocks before C2 appends land, G1 reds (stale counts).
- If `knowledge-expected.txt` sync is skipped, C2 audit fails (`unexpected=1`) and score-gap/report inputs inherit the stale number.
- SHONEN/round-39.md multi-writer appends must be merged by the L1 (disjoint sections; no byte conflict).
- ExecJunkRecheck depends on ExecFrontierCapture.S057.txt existing in wave1 (polling per spec; internal to C2).
- `wave1-results.json` must exist and be tracked at J or G4 reds.
- G6 scratch quiescence requires every seat (both claims) to remove its scratch; kasegi-r39 holds only the L1's --work at filing.

## Tooling
No installs performed (no tooling needed; read-only analysis + two mandated writes).
