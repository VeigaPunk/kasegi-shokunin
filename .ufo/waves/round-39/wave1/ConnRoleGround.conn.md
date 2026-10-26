# Cross-axis pattern check — round 39 (ConnRoleGround)

## 1. Artifact overlap: C1 suite × C2 capture

Directly shared paths (both claims touch the same lane file):

- `corpus/lessons/round-39.md` — C1 lesson rows (Mistakes, from round-38 verifier routed defects) and C2 lesson rows (Gate: S057 admission / S056-S059 rejections / spot-check readiness) both land in this file. C1's kill rule also reads it (`⟨pending` count must be 0 at filing). Content is disjoint sections; the L1 assembles the file.
- `SHONEN.md` — C1 R2 correction appends (overstate sweep) and C2 round-39 box lines (evidence pointers to F22/r39 suite) both land here. C1 G3 (quoted-run truth) and G5 (label drift) read this file post-integration.

Junction surfaces (one claim's artifact is read by the other's gate, but only as integration-time input):

- `.ufo/waves/round-39/declared-blocks.txt` (C1 G1 input) must enumerate every appended block at J — including all C2-added files: `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, `corpus/source-snapshots/round-39/S057.txt`, `corpus/source-snapshots/round-39/manifest.json`, `corpus/knowledge/cisa-when-to-issue-vex.md`, `corpus/lessons/round-39.md`, `SHONEN.md`. G1 is therefore a whole-tree gate, not a C1-local gate.
- `corpus/instruments/knowledge-expected.txt` — C2 audit data (`recheck-audit.py` default `--expect`). The C2 claim's `expected=51 missing=0 unexpected=0` cannot hold unless this list gains the new entry line. It sits in the same instruments directory where `r39-closure.sh` lands, but no C1 gate reads it.
- Knowledge count `ls corpus/knowledge/*.md` = 51 (C2) forbids any C1-side new file under `corpus/knowledge/`: C1 only modifies the existing ledger in place (`considerthese-proposals-ledger.md`, G7), which does not change the count.

Verified non-overlaps (code-inspected instrument inputs):

- `frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`, `recheck-audit.py` read only C2 surfaces (`corpus/README.md`, `corpus/knowledge/*.md`, `corpus/SOURCES.md`, `corpus/source-snapshots/*`). None opens `r39-closure.sh`, `declared-blocks.txt`, `final-gates/`, or the G-quoted files.
- C1's suite reads C2 content only through the declared-blocks whole-tail walk; it uses no C2 manifest field and no S057 line cite.

## 2. Role routing verification

- Wave context and every item prompt contain no model identifier (mercury/claude/gpt/llama/gemini/deepseek/qwen/mistral/anthropic/openai/inception all absent; "model" appears only as prose: fence-walk model, "never pass a model", "modelled on").
- The 49 spec items carry only the allowed roles: executor 27, scribe 11, reviewer 6, scout 2, connector 1, critic 2. No other role value exists in `wave1-spec.json`, `wave1-dispatch.json` (task `agent` fields), ready markers, plan output, or the swarm registry. Axes arrays carry axis names only.

## 3. Integration order (causally separable)

1. **Content** — land every seat deliverable byte-exactly; L1 assembles the lane-file appends (C2: SOURCES rows, README F22 block, PROVINCE line, knowledge entry, search-log bullet, Gate lesson; C1: suite, R2 corrections, SCORECARD distance-to-next-score, ledger round-39 dispositions, Mistakes lesson, SHONEN box lines) and performs the C-locale-correct `knowledge-expected.txt` insertion (+1 entry). No content edits after this point.
2. **Declaration** — generate `declared-blocks.txt` from the final diff (base..worktree), covering every appended block including the C2 files; commit J.
3. **Measurement** — run the r39 suite on J (green), base and r38 judged-head exports (red), and the graded selftest; produce the `final-gates/` transcripts. C2 counters (harness, source-recheck, binding, audit, census) run here — they need no receipt.
4. **Receipt** — write `all-gates.txt` (export-ref=J, suite-sha256, eight graded G lines, selftest summary); commit Y = J + the receipt only.
5. **Verification only** — suite on Y, quoted-run truth, label drift, scratch quiescence; no further writes.

Invariants that keep the claims from coupling:

- Nothing may edit content after J (G2: `git diff --name-only J Y` = receipt only).
- `declared-blocks.txt` must be (re)generated only after every append, including C2's (stale line counts red G1).
- The receipt is the last byte in the lane; it is the only self-referential artifact (it names J, which cannot contain it).
- C2 depends on zero C1 artifacts; C1 depends on C2 content only statically, via the whole-tail declaration at the commit boundary.
