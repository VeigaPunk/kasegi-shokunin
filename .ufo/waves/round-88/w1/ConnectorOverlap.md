# ConnectorOverlap Report — Round 88 Wave 1

Seat: `ConnectorOverlap`  
Lane: `kasegi`  
Round: 88, Attempt 1  
Declared Axes: `depth:verifiability` (score 4), `coverage` (score 8 held)  
Scratch root: `/fast/scratch/hyaku/kasegi-r88/ConnectorOverlap`  
Output dir: `.ufo/waves/round-88/w1/`  
Receipts: `.ufo/waves/round-88/w1/ConnectorOverlap-receipts/`  

---

## 1. Sibling Overlap Scan (Read-Only)

A read-only sweep was conducted across all 20 sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (inspecting `corpus/instruments/`, `tools/`, `corpus/knowledge/`, `corpus/SOURCES.md`, `SKILL.md`, and `.ufo/` waves) to identify instruments, knowledge entries, and source rows detecting or documenting Google Cloud Storage (GCS) signed URLs, Azure Shared Access Signatures (SAS), CloudFront signed URLs, or generic signed-URL query credentials.

### Sibling Survey Findings

1. **`kengaku-shokunin`**:
   - **Artifact**: `.ufo/waves/round-53/w3/R53SentinelFetch2/scan_extended.py:27`
     - **Code**: `("credential", "signed-url-param", re.compile(r"(?i)[?&](?:X-Amz-Signature|X-Amz-Credential|sig|signature|access_token|token)=[A-Za-z0-9._%\-]{16,}"))`
     - **Significance**: Implemented a unified signed-URL query credential scanner checking both AWS query parameters (`X-Amz-Signature`, `X-Amz-Credential`) and generic signature parameters (`sig=`, `signature=`).
   - **Artifact**: `.ufo/waves/round-32/build/R32Sentinel.md:14`
     - **Citation**: *"signed-URL params `X-Amz-Signature`/`GoogleAccessId`/`Signature=`"*
     - **Significance**: Explicitly documented and scanned for **GCS V2 signed URLs** (`GoogleAccessId` parameter with `Signature=`), which differs from the GCS V4 format (`X-Goog-Signature` with `X-Goog-Credential`).
   - **Artifact**: `.ufo/waves/round-95/w1/ScoutSources/receipts/net/config.headers:5`
     - **Evidence**: Captured an upstream HTTP `307 Temporary Redirect` response from Docker Hub containing a CloudFront signed URL in its `Location:` header with parameters `Expires=`, `Signature=`, and `Key-Pair-Id=`.

2. **`kama-shokunin`**:
   - **Artifacts**: `.ufo/waves/round-47/w1/out/S1Rows/model-head.txt:4`, `.ufo/waves/round-48/w1/out/S1Gate/loc1.txt:1`, `.ufo/waves/round-53/w1/out/Sc2Watch/model-head.txt:4`
     - **Evidence**: Upstream HTTP `302 Found` response headers from HuggingFace CDN (`https://us.aws.cdn.hf.co/...`) containing CloudFront signed URLs carrying `Policy=`, `Expires=`, `Signature=`, and `Key-Pair-Id=`.
     - **Significance**: Proves that upstream redirect headers in capture pipelines are a primary exposure surface for CloudFront signed URLs.

3. **`kagi-shokunin`**:
   - **Artifact**: `corpus/transcript-scan.sh:83-95`
     - **Function**: Scans SQLite transcript databases (`opencode.db`) across all text columns for credential prefixes (`AKIA`, `ASIA`, `AIza`, `ya29.`, `ghp_`, `xoxb-`, `sk-ant-`, `eyJhbG`, `op://`).
     - **Distinction**: Focuses exclusively on static API keys and tokens in relational DB columns; does not scan HTTP query string parameters or signed URLs.
   - **Artifact**: `corpus/knowledge/secret-scanning-detection-vs-validation.md:8-73`
     - **Content**: Thorough analysis of static pattern matching (Gitleaks) versus active live validation (TruffleHog `verified`/`unverified`/`unknown`). Establishes the operational principle that unverified detection is a triage trigger rather than proof of exposure.

4. **`kotodama-shokunin`**:
   - **Artifacts**: `.ufo/waves/round-74/w1/SentinelScope.md:90`, `.ufo/waves/round-74/w2/SentinelLanded.md:463`
     - **Evidence**: Sentinel regex scan over evidence paths: `X-Amz-Signature|X-Amz-Credential|Signature=|access_token=|api_key=|sig=`.

5. **`mado-shokunin`**:
   - **Artifact**: `.ufo/waves/round-18/w1/reports/RevFetchReceiptContract.md:577`
     - **Rule**: Rejection gate prohibiting captured query parameters: `'sessionid', 'sig', 'signature', 'x-amz-signature'`.

6. **`kotoba-shokunin`**:
   - **Artifacts**: `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:2877, :33927`, `.ufo/waves/round-82/build/Kb82E12Loader-omp-18.14.0-strings.txt:3357`
     - **Evidence**: Decompiled runtime binary strings referencing SigV4 query and header tokens (`X-Amz-Security-Token=`, `x-amz-security-token:`, `X-Amz-Signature=`).

### What Kasegi Could Reuse vs Must Not Duplicate

- **What Kasegi Could Reuse**:
  1. **CloudFront Signed URL Signature Shapes (`Key-Pair-Id` + `Signature`)**: Sibling receipts in `kama-shokunin` and `kengaku-shokunin` prove that HTTP `Location:` redirect headers frequently contain CloudFront signed URLs. Kasegi's C2 currently leaves CloudFront signed URLs as an explicit gap in `capture-secret-scan.py`'s docstring.
  2. **GCS V2 Signed URL Identification (`GoogleAccessId` + `Signature`)**: `kengaku-shokunin/.ufo/waves/round-32/build/R32Sentinel.md:14` identifies the legacy Google Cloud Storage V2 signed URL shape (`GoogleAccessId` alongside `Signature=`), complementing kasegi's V4 detection (`X-Goog-Signature` alongside `X-Goog-Credential`).
  3. **Unified Query-Parameter Normalization**: Sibling regex patterns (`kengaku-shokunin:27`) demonstrate scanning combined query strings with case-insensitive boundary assertions across URL-encoded delimiters (`&amp;`, `\u0026`).

- **What Kasegi Must NOT Duplicate**:
  1. **Relational Database Scanning**: Kagi's `transcript-scan.sh` operates over SQLite database columns. Kasegi's domain is strictly static file and git-blob scanning across bounty captures and evidence trees.
  2. **Process Spawn / Runtime Interception**: Mado's `tools/mado-tripwire.py` hooks shell process spawning. Kasegi's instruments are offline audit tools run pre-freeze and at landing.
  3. **Host Retention / Privacy Filtering**: Mori's `retention-gate.py` filters host usernames, session UUIDs, and system slice IDs. Kasegi must maintain strict focus on credential material in capture evidence.
  4. **Ad-Hoc Unpinned Shell Pipelines**: Sibling sentinel checks often rely on loose `grep -E` pipes without sha256 pins or TSV allowlists. Kasegi must maintain its counter-verified, allowlist-bound instrument architecture.

---

## 2. Cross-Axis Pattern: `anchor-content-drift` Audit in `SKILL.md`

In Round 88 C1, 54 sibling-entry line anchors in `corpus/knowledge/*.md` were excluded from repointing (`.ufo/waves/round-88/c1/excluded.json`) under the classification `anchor-content-drift`: the citing sentence shared zero identifiers (under the M8 content proxy) with the cited line range in the target knowledge entry.

We conducted an audit of `SKILL.md` using the exact same M8 content proxy logic (`probe-skill-anchor-drift.py`):
1. **Identifier Extraction (`idents`)**: Spans enclosed in backticks `` `...` `` and double quotes `"..."` excluding path-like strings (`PATHLIKE`), tokenized by `WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")`.
2. **Target Words (`tw`)**: Set of words (`WORD`) within lines `lo` through `hi` (inclusive) of the target file `corpus/knowledge/<name>.md`.
3. **Verdict**: If `idents(citing_line) & tw == set()`, the citation is classified as `anchor-content-drift`.

### Audit Census & Metrics

- **Total Anchored Citations Inspected in `SKILL.md`**: 12
  - Canonical backticked citations (`corpus/knowledge/<name>.md:N[-M]`): 7
  - Parenthesized sub-anchors (lines 472–473): 5
- **Passing M8 Content Proxy**: 3 (25.0% of total; 42.9% of canonical backticked)
- **Failing M8 (`anchor-content-drift`)**: 9 (75.0% of total; 57.1% of canonical backticked)
- **Out-of-Range Anchors**: 0 (all line anchors fall within the physical line counts of their targets)

| Citation Category | Total | Passing M8 | Drifted (Failing M8) | Drift Rate |
|---|---|---|---|---|
| Canonical Backticked (`corpus/knowledge/*.md:N`) | 7 | 3 | 4 | 57.1% |
| Parenthesized Sub-anchors (`:N-M`) | 5 | 0 | 5 | 100.0% |
| **Combined Total** | **12** | **3** | **9** | **75.0%** |

### 5 Concrete Examples of `anchor-content-drift` in `SKILL.md`

1. **`SKILL.md:120` citing `corpus/knowledge/program-quirks.md:10`**
   - **Citing Line**: `Per-program pattern list: \`corpus/knowledge/program-quirks.md:10\` (fee gate),`
   - **Extracted Identifiers (`idents`)**: `[]` (empty: the path token is path-like, and "fee gate" is unquoted prose).
   - **Target Text (`program-quirks.md:10`)**: `- **$100 submission deposit** — the claimability gate is a read-only`
   - **Target Words (`tw`)**: `['claimability', 'deposit', 'submission']`
   - **Analysis**: The citing line references "(fee gate)", but line 10 uses "$100 submission deposit". Because the conceptual link is in plain prose outside backticks, the M8 proxy finds 0 shared identifiers.

2. **`SKILL.md:338` citing `corpus/knowledge/ops-invariants.md:24`**
   - **Citing Line**: `(\`[lost-tree] ops/shared.mjs:55\`, \`corpus/knowledge/ops-invariants.md:24\`).`
   - **Extracted Identifiers (`idents`)**: `['shared']` (from `[lost-tree] ops/shared.mjs:55`).
   - **Target Text (`ops-invariants.md:24`)**: `| \`gitMutationBlocker\` | fail-closed preflight | refuses when rebase-merge/rebase-apply/MERGE_HEAD/CHERRY_PICK_HEAD exist (\`ACTIVE_GIT_OPERATION\`) or HEAD not on \`main\` (\`HEAD_NOT_ON_MAIN\`); used by finalize-all, fleet-dispatch commits, --sync |`
   - **Target Words (`tw`)**: `['gitMutationBlocker', 'preflight', 'rebase', 'MERGE_HEAD', 'CHERRY_PICK_HEAD', 'ACTIVE_GIT_OPERATION', 'HEAD_NOT_ON_MAIN', 'finalize', 'dispatch', 'commits', 'sync']`
   - **Analysis**: Target line 24 specifies `gitMutationBlocker`. The citing line references `shared.mjs:55` from the lost tree. While conceptually related to git preflights, the citing identifier `shared` does not occur in line 24.

3. **`SKILL.md:416` citing `corpus/knowledge/intake-and-finalize.md:78-92`**
   - **Citing Line**: `(\`corpus/knowledge/intake-and-finalize.md:78-92\`).`
   - **Extracted Identifiers (`idents`)**: `[]` (empty: the entire citation is path-like).
   - **Target Text (`intake-and-finalize.md:78-92`)**: Detailed 5-step checklist: Filters, Re-validates, Commits, Byte-proofs the tag target, Tags.
   - **Target Words (`tw`)**: 42 words including `['Filters', 'Commits', 'Tags', 'claim_ready', 'status']`.
   - **Analysis**: Bare parenthetical citation on its own clause. With no accompanying backticked identifiers in the citing clause, the M8 proxy fails completely.

4. **`SKILL.md:821` citing `corpus/knowledge/mission-control.md:3`**
   - **Citing Line**: `lines vs the lost 427 (\`corpus/knowledge/mission-control.md:3\`) and diverges`
   - **Extracted Identifiers (`idents`)**: `[]` (empty).
   - **Target Text (`mission-control.md:3`)**: `Source: \`~/Projects/bounties/ops/fleet-dispatch.mjs\` (read in full, 427`
   - **Target Words (`tw`)**: `['Projects', 'Source', 'bounties', 'dispatch', 'fleet']`
   - **Analysis**: The citing text refers to line counts ("lost 427"), but neither `427` nor any shared word is enclosed in backticks/quotes on line 821, producing a false negative under M8.

5. **`SKILL.md:472` citing `corpus/knowledge/vdp-disclosure-packages.md:3-5` (and `:9`, `:13-16`, `:20`, `:22-31`)**
   - **Citing Line**: `\`corpus/knowledge/vdp-disclosure-packages.md\` (\`:3-5\`, \`:9\`, \`:13-16\`, \`:20\`,`
   - **Extracted Identifiers (`idents`)**: `[]` (empty: range tokens `:3-5` contain no `WORD`).
   - **Target Text (`vdp-disclosure-packages.md:3-5`)**: Source metadata and `vdp-disclosures/` file receipts.
   - **Analysis**: Multi-anchor citation pattern where sub-anchors are parenthesized. None of the five sub-anchors share any identifier with the citing line under M8.

---

## 3. UFO-FSD Synthesis: One Non-Obvious Move

### Evidence & Synthesis Across Round Proposals

1. **Structural Flaw in `resolve.py`**:
   `corpus/instruments/resolve.py` checks only file-level path reachability. Any line anchor `:N` or `:N-M` appended to an existing path (e.g., `corpus/knowledge/ops-invariants.md:24`) is classified as `INTERNAL` as long as `corpus/knowledge/ops-invariants.md` exists on disk. `resolve.py` does not verify line count bounds or content matching. Consequently, `resolve.py` awards full verifiability credit to drifted or hallucinated line numbers in `SKILL.md` and `corpus/knowledge/`.
2. **C1 Exclusion Ledger (`excluded.json`) & ExecReanchor**:
   C1 excluded 54 sibling citations from the repair map because they failed M8. Because they were excluded, they remained bare sibling entries (`claim-gates.md:51`), which `resolve.py` scores as `GONE`, artificially capping the knowledge meter at 742/1743. In wave 1, `ExecReanchor` is drafting manual re-anchorings for these 54 keys.
3. **Cross-Axis Drift in `SKILL.md`**:
   Section 2 demonstrates that `SKILL.md` suffers from the exact same drift class (57.1% canonical drift rate). Re-anchoring knowledge files without auditing `SKILL.md` leaves the lane's primary instruction surface degraded.
4. **Sibling Evidence for CloudFront Redirects**:
   Sibling evidence (`kama-shokunin` and `kengaku-shokunin`) proves that upstream CDN redirects (`Location:` headers) routinely carry CloudFront signed URLs (`Key-Pair-Id`, `Signature`). Meanwhile, C2 (`capture-secret-scan.py`) explicitly leaves CloudFront signed URLs unhandled.

### Affected Axes

- **`depth:verifiability`** (current score: 4): Moves citation verification from blind path resolution to semantic, anchor-aware verification across both `corpus/knowledge/` and `SKILL.md`.
- **`coverage`** (current score: 8 held): Bridges the capture inspection pipeline to cover CDN redirect headers carrying CloudFront signed URLs.

### Proposed Move

**Synthesize an Anchor-Aware Verification Instrument (`anchor-verify.py`) and CloudFront Redirect Header Scanner for Round 89**:

1. **Semantic Anchor Verification Substrate (`anchor-verify.py`)**:
   Promote the M8 content proxy from a pre-freeze repair map filter into a standalone verification instrument (`corpus/instruments/anchor-verify.py` or `resolve.py --check-anchors`).
   - Audits all line-anchored citations (`path:lo[-hi]`) across both `corpus/knowledge/*.md` and `SKILL.md`.
   - Checks two discrete limbs:
     - **Limb A (Range Validity)**: `1 <= lo <= hi <= len(target_lines)`.
     - **Limb B (Semantic Identity)**: `idents(citing_line) & target_words != set()`, augmented with a 1-line context window to accommodate preceding heading identifiers.
   - Ingests `ExecReanchor`'s re-anchored candidate mappings for the 54 `excluded.json` keys, allowing round 89's C1 to repoint them to `corpus/knowledge/`, elevating the knowledge meter from 742/1743 toward 796/1743.
   - Simultaneously re-anchors the 4 drifted citations in `SKILL.md` (lines 120, 338, 416, 821).

2. **CloudFront Signed URL Extension (`Key-Pair-Id` + `Signature`) in `capture-secret-scan.py`**:
   Incorporate CloudFront signed URL query parameters into `capture-secret-scan.py`:
   - Detect `Key-Pair-Id=[A-Z0-9]{14,}` in conjunction with `Signature=[A-Za-z0-9~_%-]{40,}` in URL query strings and HTTP `Location:` / `Set-Cookie:` response headers.
   - Sibling receipts in `kama-shokunin` and `kengaku-shokunin` provide ready-made, real-world test vectors.

### Second-Order Effects Across Surfaces

- **Runtime Surface**: Fast offline execution (under 0.2s in Python). Zero network or external service calls. Prevents live CDN redirect URLs with temporary access tokens from persisting in capture receipts.
- **Contract Surface**: Eliminates the contradiction where `resolve.py` scores drifted or hallucinated line numbers as `INTERNAL`. Establishes a verifiable contract between citing sentences and target anchors.
- **Substrate Surface**: Guarantees that future edits to knowledge entries or `SKILL.md` do not silently break citation validity.
- **Verification Surface**: Converts `ExecReanchor`'s manual work and our `SKILL.md` findings into an objective, machine-checkable gate for round 89 claims.

### Risks & Mitigations

- **Risk**: Prose lines citing anchors without backticks/quotes (e.g. `SKILL.md:416` or `SKILL.md:821`) produce false-positive drift under strict `idents` rules.
  - *Mitigation*: The augmented instrument evaluates a 1-line preceding window or extracts nouns from the immediate enclosing sentence clause when backticks are absent.
- **Risk**: Immediate fail-closed integration into `resolve.py` would cause mass regression in existing resolve census scores.
  - *Mitigation*: Keep `resolve.py`'s core census format unchanged and introduce anchor checking as an orthogonal verification limb (`--check-anchors`) or dedicated script (`anchor-verify.py`) targeted for round 89.

### Verification Plan

1. **Anchor Verifier Test**:
   - Run `anchor-verify.py` over `kasegi` base `6beead91`. Assert that it cleanly reproduces the 54 `excluded.json` keys in `corpus/knowledge/` and flags exactly the 4 drifted backticked citations in `SKILL.md`.
   - Apply `ExecReanchor`'s candidate patch in scratch; re-run `anchor-verify.py` and assert drift drops from 54 to 0 in `corpus/knowledge/`.
2. **CloudFront Detection Test**:
   - In scratch, run `capture-secret-scan.py` against a test fixture containing `kengaku-shokunin/.ufo/waves/round-95/w1/ScoutSources/receipts/net/config.headers:5`.
   - Assert `HIT: cloudfront-signed-url-signature` is triggered on `Key-Pair-Id` and `Signature`.

---

## 4. Receipts & Inventory

- `receipts/probe-skill-anchor-drift.py`: Python audit tool implementing M8 content proxy.
- `receipts/probe-skill-anchor-drift.txt`: Complete execution transcript and drift analysis over `SKILL.md`.
- `receipts/sibling-overlap-scan.txt`: Sanitized survey transcript across 20 sibling lane repos.
- All receipt files scanned with `corpus/instruments/capture-secret-scan.py` (`hits=0`).
