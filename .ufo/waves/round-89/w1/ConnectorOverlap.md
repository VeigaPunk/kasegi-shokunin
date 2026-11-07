# ConnectorOverlap — Round 89, Attempt 1

Seat: `ConnectorOverlap` (leaf member, UFO-FSD connector).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base: `090a46f89932324787e00ca20b1007f893934c9a`, Freeze: `94573d2573dc6cca83454cc65b787d37d96988f5`.
Landings: C1 `eb5f0df8eaceca617465e493c710e8626e9aa618`, C2 `c61c55868e6d28653f57413bac6a6de5a398d11f`.
Declared axes: **depth:verifiability** (C1) and **coverage** (C2).

---

## 1. Cross-Lane Pattern Scan (Sibling Lanes)

A read-only scan was conducted across all 20 sibling repositories (`/home/vgpnk/Projects/shokunin/*-shokunin`, excluding `kasegi-shokunin`) covering committed code, tools, knowledge entries, and wave artifacts.

### 1.1 CloudFront `Signature=`, `Key-Pair-Id=`, and Signed Cookies
- **Committed scanners / knowledge:** No sibling lane possesses committed scanners or knowledge documents for CloudFront signed URLs or signed cookies (`CloudFront-Policy`, `CloudFront-Signature`, `CloudFront-Key-Pair-Id`).
- **Real-world CloudFront Signed URL Receipts Discovered in Fleet:**
  1. `kengaku-shokunin`: `.ufo/waves/round-95/w1/ScoutSources/receipts/net/config.headers:5` (sha256 `ce05c1f0a5daf3252f3e6e3b1a57e791c97d64b80ac142561d7ee49e073d36c7`). Captured live Docker registry CDN URL (`production.cloudfront.docker.com/...`) carrying query parameters `Expires=...&Signature=...&Key-Pair-Id=K31B9XRZB58O8Z`.
  2. `kama-shokunin`: `.ufo/waves/round-47/w1/out/S1Rows/model-head.txt:4` (sha256 `74ccc8b54bd98f4b259b8de012f9337797e36b25341c0629d7b75ba7f4790896`). Captured live Hugging Face CDN URL (`us.aws.cdn.hf.co/...`) carrying `Expires=...&Policy=...&Signature=...&Key-Pair-Id=...`.
  - **Recheck with kasegi C2 scanner:** Running `capture-secret-scan.py --files` against both sibling receipts triggers un-allowlisted hits:
    - `HIT shape=cloudfront-signed-url-signature path=kengaku-shokunin/.../config.headers line=5` (exit 1)
    - `HIT shape=cloudfront-signed-url-signature path=kama-shokunin/.../model-head.txt line=4` (exit 1)
- **Reuse for Kasegi:** Kasegi C2 can ingest these two real-world CDN response headers as benchmark integration fixtures to verify that `cloudfront-signed-url-signature` discriminates live production telemetry alongside synthetic unit tests.

### 1.2 Azure SAS
- **Committed scanners:** No sibling lane maintains an Azure SAS regex detector.
- **Incidental mentions:** `kaidoku-shokunin/.ufo/waves/round-52/w1/SentSecrets/scan.md` and `souji-shokunin/census/round-31/waves/w2/SwarmSentinel30.md:70` mention `sig=` as a sensitive parameter token, but neither implements an inter-parameter separator regex or parameter-window validator.

### 1.3 Citation Re-Anchor and Non-Author Label Binding Tooling
- **`tsukuroi-shokunin/tools/check-nonauthor-label-r85.py`:** Enforces `LEARNING.md §Discernment` by mechanically verifying that no lane seat is labelled as a "non-author reviewer". It reads the wave results census and flags any non-exempt line pairing a census seat with `non-author`.
- **`tsukuroi-shokunin/tools/check-anchor-coordinates-r83.py`:** Coordinates checker bound to `snapshot_sha256`. Verifies that quoted spans and cited line numbers `[a, b]` correspond byte-for-byte with raw lines in the pinned snapshot.
- **`kaidoku-shokunin/tools/round-93/craft-citation-semantic.py`:** Freezes keyword atoms that the cited criterion must contain, preventing syntax-valid citations from drifting to irrelevant sections.
- **`tameshi-shokunin/tools/anchor-drift-sweep.py`:** Manifest-driven anchor drift sweep over heading names and snapshot revisions.
- **`souji-shokunin/tools/souji-citation-reconcile.py`:** Binds citation anchors to committed receipt files with a TSV register schema.
- **Reuse for Kasegi:** Kasegi's C1 M9 binding (`labels.tsv` -> line in `ReviewC1Semantics.md`) is structurally unique in binding repoints directly to non-author review lines. However, `tsukuroi`'s digest-bound coordinate verification (`check-anchor-coordinates-r83.py`) offers a valuable pattern: binding citation line ranges directly to snapshot/target blob SHA-256 digests rather than relying on brittle post-hoc line offsets.

---

## 2. Reviewer-Named Correct Ranges Not Yet Applied at Master

A systematic review of rounds 85–88 wave reports (`ReviewC1Semantics.md`, `CriticClaims.md`, `CriticHarm.md`, `ConnectorOverlap.md`, `ExecReanchor.md`) and round 89 reviews (`ReviewC1Labels.md`, `ReviewWindow.md`) identified the following reviewer-named correct ranges that remain **bare or wrong** at master (`50e2632ea891bb080425f359d6a6115874cee61f`):

| Key | Citing File:Line | Named Correct Range | Reviewer Source | Current State at Master | Basis / Ground Truth |
|---|---|---|---|---|---|
| `mission-control.md:42-46` | `corpus/knowledge/triage-thresholds.md:149` | `corpus/knowledge/mission-control.md:68` | `ReviewC1Semantics.md:114` (r88) | unapplied (`MATCHES: mission-control.md:42-46`) | Row 149 specifies `--sync` cadence ("every 10 ticks"), which is located at `L68`. Range `:42-46` is the commit message section. |
| `mission-control.md:43-46` | `corpus/knowledge/triage-thresholds.md:150` | `corpus/knowledge/mission-control.md:68-70` | `ReviewC1Semantics.md:64,153` (r88) | unapplied (`MATCHES: mission-control.md:43-46`) | Row 150 defines `SYNC_PATHS` allowlist (8 paths in entry), located at `L68-70`. Range `:43-46` is stale. |
| `claim-gates.md:21-23` | `corpus/knowledge/triage-thresholds.md:177` | DROP TIE (or re-anchor to contract) | `ReviewC1Semantics.md:35,155` (r88) | unapplied (`MATCHES: claim-gates.md:21-23`) | Row 177 is the package root `realpathSync(dir)` gate. `claim-gates.md:21-23` covers only artifact symlinks; row 177 has no supporting line in `claim-gates.md`. |
| `claim-gates.md:67-70` | `corpus/knowledge/triage-thresholds.md:278` | `corpus/knowledge/claim-gates.md:81-85` | `ReviewC1Semantics.md:81` (r88), `ReviewC1Labels.md:45` (r89) | unapplied (`MATCHES: claim-gates.md:67-70`) | Row 278 is the global duplicate scan; the actual gate in `claim-gates.md` is lines 81–85. |
| `claim-gates.md:70-71` | `corpus/knowledge/triage-thresholds.md:279` | `corpus/knowledge/claim-gates.md:86-87` | `ReviewC1Labels.md:63` (r89) | unapplied (`MATCHES: claim-gates.md:70-71`) | Row 279 specifies unresolved readiness blockers; located at lines 86–87 in `claim-gates.md`. |
| `claim-gates.md:71-74` | `corpus/knowledge/triage-thresholds.md:280` | `corpus/knowledge/claim-gates.md:88-91` | `ReviewC1Semantics.md:105` (r88) | unapplied (`MATCHES: claim-gates.md:71-74`) | Row 280 specifies nested readiness (`BLOCKED`, `claim_ready===false`). Lines 71–74 are reviewer bullets; the gate is lines 88–91. |
| `claim-gates.md:71-74` | `corpus/knowledge/triage-thresholds.md:281` | `corpus/knowledge/claim-gates.md:88-91` | `ReviewC1Semantics.md:105` (r88) | unapplied (`MATCHES: claim-gates.md:71-74`) | Row 281 specifies nested blockers (`blocker_codes`/`remaining_gates`); located at lines 88–91 in `claim-gates.md`. |
| `mission-control.md:20-21` | `corpus/knowledge/triage-thresholds.md:90` | `corpus/knowledge/mission-control.md:21` | `ReviewC1Semantics.md:112` (r88) | unapplied (`MATCHES: intake-surface.md:72, mission-control.md:20-21`) | Row 90 specifies `freshness.live ? 1 : 0`; supported specifically by line 21 in `mission-control.md`. |
| `ops-invariants.md:18` | `corpus/knowledge/triage-thresholds.md:390` | `corpus/knowledge/ops-invariants.md:18` | `ReviewC1Semantics.md:115` (r88) | unapplied (`MATCHES: ops-invariants.md:18, SKILL.md:525`) | Row 390 specifies `BANNED` provider tokens; supported by line 18 in `ops-invariants.md`. M8 excluded it due to a quoted mention in `citation-bases.md:14`. |
| `claim-package-contract.md:9-16, 28-38` | `corpus/knowledge/triage-thresholds.md:457` | `corpus/knowledge/claim-package-contract.md:9-16` (and `:52-53`) | `ReviewC1Labels.md:87` (r89 F1) | unapplied (bare composite) | Composite citation unparsed by `apply-map.py` and rejected by `resolve.py is_pathlike`; row 178 was repointed but row 457 was left bare. |
| `claim-gates.md:42-47` | `corpus/knowledge/triage-thresholds.md:249` | `corpus/knowledge/claim-gates.md:54-55` | `ReviewC1Labels.md:112` (r89 F3) | unapplied (`claim-gates.md:42-47 covers the regex only`) | Row 249 asserts the blanket symlink ban is uncovered; `claim-gates.md:54-55` explicitly states the blanket symlink ban. |
| `mission-control.md:37-38` | `corpus/knowledge/triage-thresholds.md:155` | `corpus/knowledge/mission-control.md:55-57` | `ReviewC1Labels.md:117` (r89 F4) | unapplied (`mission-control.md:37-38`) | Row 155 cites L37-38 for peak model routing; model routing is L55-57 (round-13 correction). L37-38 is the sweep. |
| `mission-control.md:37-38` | `corpus/knowledge/triage-thresholds.md:438` | `corpus/knowledge/mission-control.md:55-57` | `ReviewC1Labels.md:117` (r89 F4) | unapplied (`mission-control.md:37-38`) | Row 438 SUPERSEDES row repeats stale peak model attribution; correct model routing is L55-57. |

*Note on `japanese-domestic-disclosure-workflow.md:7`:* The round-88 defect (D88-H1 / R1) where line 7 was mistakenly repointed to cite itself was already cleanly resolved during round-88 integration commit `b8d25b9`, restoring line 7 to the bare file-name reference.

Full machine-readable table retained at `.ufo/waves/round-89/w1/ConnectorOverlap-receipts/candidate-reanchors-r90.tsv`.

---

## 3. SKILL.md Corpus/Knowledge Citation Audit

All citations in `SKILL.md` touching target knowledge entries modified by Round 89 C1 (`claim-gates.md`, `claim-package-contract.md`, `ops-invariants.md`) were audited against master:

1. **`SKILL.md:154`**:
   - `claim-check.mjs enforces all of it (authoritative list: \`corpus/knowledge/claim-gates.md\`): required-file presence, \`report.md\` ...`
   - **Status**: UNANCHORED, CARRIES FULL PREFIX.
   - **Verification**: Refers broadly to the entire claim-check gate suite (`claim-gates.md:10-91`). Already points to `corpus/knowledge/claim-gates.md`. Not modified or corrupted by C1 landing.
2. **`SKILL.md:338`**:
   - `(\`[lost-tree] ops/shared.mjs:55\`, \`corpus/knowledge/ops-invariants.md:24\`).`
   - **Status**: ANCHORED, CARRIES FULL PREFIX.
   - **Verification**: Line 24 in `ops-invariants.md` is `| \`gitMutationBlocker\` | fail-closed preflight | ...`. The citation in `SKILL.md:338` specifically supports the missing `gitMutationBlocker` statement on lines 335–338. The line coordinate is exact and falls within the table range (`:17-25`) repointed in `triage-thresholds.md:455`.
3. **`SKILL.md:444`**:
   - `(\`/tmp/kasegi-r15/ev-smoke\`). Detail: \`corpus/knowledge/ops-invariants.md\`,`
   - **Status**: UNANCHORED, CARRIES FULL PREFIX.
   - **Verification**: General reference to ops invariants. Untouched by C1.
4. **`claim-package-contract.md`**:
   - **Status**: 0 occurrences in `SKILL.md`.

**Audit Conclusion:** No citations in `SKILL.md` were broken, altered, or invalidated by Round 89's C1 landing. All citations in `SKILL.md` to these entries already carried the canonical `corpus/knowledge/` prefix.

Receipt retained at `.ufo/waves/round-89/w1/ConnectorOverlap-receipts/skill-citations-audit.txt`.

---

## 4. UFO-FSD Synthesis: One Non-Obvious Move

### 4.1 Evidence & Cross-Claim Contradictions
1. **The C1 Grammar Contradiction (Global vs. Local Mapping):**
   - C1 operates via global string replacement (`repair-map.json`), mapping `old_token -> new_token`.
   - As proved by `ReviewC1Labels` (Finding F1), composite citations like `claim-package-contract.md:9-16, 28-38` in `triage-thresholds.md:457` cannot be processed by `apply-map.py` or counted by `knowledge-meter.py` because `resolve.py` rejects non-pathlike tokens (containing commas and spaces). Thus row 178 was repointed while row 457 remains bare, leaving an inconsistency in the very table being verified.
   - Furthermore (Finding F2), `claim-gates.md:35-36` occurs at three sites: two are already qualified and correct (lines 223, 224), while only bare site 225 needed `:36-37`. Global key replacement cannot distinguish among sites, risking collateral regression if applied naively.
2. **The C2 Parameter Boundary Contradiction:**
   - C2 expanded `capture-secret-scan.py` to recognize CloudFront signed URLs and handle Azure SAS separators.
   - However, as proved by `ReviewWindow.md`, Azure parameter matching restricts parameter names to `_PARAM = rb"[A-Za-z]{2,6}"`. Documented Azure SAS parameter `skdutid` (`signedKeyDelegatedUserTenantId`, 7 letters, API version 2025-07-05+) causes an immediate match termination. Any SAS URL containing `&skdutid=...` between `sv` and `sig` is completely missed.
   - Additionally, `ExecC2Corpus` identified that `%26` is accepted only at `_LB` (match start) and not in `_SEP` (inter-parameter separator).
3. **The Sibling Fleet Telemetry Evidence:**
   - Cross-lane scan revealed real production CloudFront signed URLs in `kengaku-shokunin` (Docker registry CDN receipt) and `kama-shokunin` (Hugging Face CDN receipt). Both trigger `capture-secret-scan.py` with `rc=1` exit code, confirming that C2's detector is active on live fleet data, but lacks integration tests validating standard Base64 characters (`+`, `/`, `=`) and encoded separators.

### 4.2 Proposed Move: Site-Indexed Citation Repair with Parameter Bound Generalization
For Round 90, execute a unified precision upgrade synthesizing the strengths of both claims:

1. **C1 (depth:verifiability) — Site-Indexed Repair Map with Composite Splitting:**
   - Upgrade the repair map schema from flat `key -> value` to site-indexed triples `(citing_file, citing_line, replacement_token)`. This adopts C2's allowlist architecture `(file, shape, line)` and `tsukuroi`'s `check-anchor-coordinates-r83.py` model.
   - Ingest the 39 Tranche-5 keys (46 citing sites) catalogued in `ReviewC1Labels-receipts/tranche5-labels.tsv` and the unapplied candidate ranges from Section 2.
   - Split composite citations into individually qualified sub-ranges (e.g. repoint `triage-thresholds.md:457` to `corpus/knowledge/claim-package-contract.md:9-16, 28-38`), eliminating the F1 blind spot and preventing F2 site-collision hazards.
2. **C2 (coverage) — Parameter Name Width Expansion:**
   - Widen `_PARAM` in `capture-secret-scan.py` from `[A-Za-z]{2,6}` to `[A-Za-z]{2,8}` (or `[A-Za-z0-9_-]{1,32}` matching `_CF_PARAM`).
   - This directly closes the `skdutid` (7-char) false negative identified in `ReviewWindow.md` without degrading scan performance.
   - Incorporate the `kengaku-shokunin` and `kama-shokunin` real-world CloudFront response headers into C2's integration regression suite.

### 4.3 Second-Order Effects & Surface Impact
- **Runtime Surface:** Widening `_PARAM` to length 8 adds negligible regex state transitions (bounded repeat); runtime on large repositories remains strictly sub-second.
- **Contract Surface:** Eliminates the contradiction in `resolve.py` where composite citations are ignored. Re-anchors all drifted `triage-thresholds.md` rows to exact entry lines.
- **Substrate Surface:** No filesystem or repo mutations outside wave output directories. Fully backward-compatible with existing K1–K8 and M1–M9 control suites.
- **Verification Surface:** Site-indexed TSV allows line-level verification without global string replacements, preventing accidental mutation of comments, quoted examples, or already-correct citations.

### 4.4 Risks and Mitigations
- **Risk:** Widening `_PARAM` to length 8 might match non-Azure parameters in random query strings.
  *Mitigation:* The match is still strictly anchored to `sv=YYYY-MM-DD` and `sig=[A-Za-z0-9%]{40,}` within a 20-parameter window. Random query strings lack that co-occurrence.
- **Risk:** Site-indexed line replacements in `triage-thresholds.md` could shift line numbers if lines are inserted or deleted.
  *Mitigation:* Apply repairs bottom-to-top (descending line order) or enforce line-preserving single-line edits.

### 4.5 Verification Plan
1. **C1 Verification:** Run `knowledge-meter.py` with site-indexed labels against Tranche 5 candidates. Verify that `triage-thresholds.md:457` resolves both ranges under `resolve.classify` and that M9 passes for all 46 sites.
2. **C2 Verification:** Execute `capture-secret-scan.py --files` over a fixture containing `?sv=2025-07-05&skdutid=...&sig=...`. Confirm `HIT shape=azure-sas-signature` (rc=1). Run over existing K1–K8 controls to confirm zero regression.

---

## 5. Tooling, Credentials, and Scratch Disposal

- **Tooling authorization:** No tools installed or upgraded. Read-only commands only.
- **Credential hygiene:** Zero credential values recorded. All receipts carry SHA-256 digests, file paths, line numbers, and scanner summary lines only.
- **Scratch:** Scratch directory `/fast/scratch/hyaku/kasegi-r89/ConnectorOverlap` was removed via `trap 'rm -rf -- "$S"' EXIT`.
- **Files written:**
  - `.ufo/waves/round-89/w1/ConnectorOverlap.md` (this report)
  - `.ufo/waves/round-89/w1/ConnectorOverlap-receipts/sibling-scan-receipts.txt`
  - `.ufo/waves/round-89/w1/ConnectorOverlap-receipts/candidate-reanchors-r90.tsv`
  - `.ufo/waves/round-89/w1/ConnectorOverlap-receipts/skill-citations-audit.txt`
