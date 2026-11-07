# ConnectorOverlap Report — Round 92 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 92, Attempt 1 (ONE v1 wave of 13 seats; L1 `KasegiR92` holds planner seat)  
Declared Axes: `depth:verifiability` (lowest axis, score 4), `coverage` (score 8 held)  
Base commit: `0628fd247914555838a42c02ba5d4ac08b7e095d`  
Freeze commit: `9e4f0d6830dcc9a30c6f524c48d074ec8979f040`  
C1 landing commit: `cb1ef2b9856df79c530f3ff1374fa9691ff56233`  
C2 landing commit: `58c0c115342877ee556cae19928d69839b0b29f0`  
Landing receipts commit: `ee830069af1255043aeb39f1d324e6b3e5d69dbd`  
Scratch root: `/fast/scratch/hyaku/kasegi-r92/ConnectorOverlap` (purged prior to exit)  
Receipts: `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/`

---

## 1. Sibling-Lane Scan for Secret Scanners and Capture Writers

A read-only pattern scan was executed across all 20 sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kasegi-shokunin`).
Search patterns: `ghp_`, `github_pat_`, `secret-scan`, `SECRET_PATTERNS`, `capture-source`.
Receipt: `ConnectorOverlap-receipts/sibling-scan.txt`.

### 1.1 Secret Scanners in Sibling Lanes
1. **`kagi-shokunin`** (`corpus/transcript-scan.sh:87`):
   - **Mechanism**: Substring matching in `PATTERNS_HIT` array against: `'ghp_' 'gho_' 'ghu_' 'ghs_' 'ghr_' 'github_pat_'`.
   - **GitHub token detection**: Detects GitHub tokens via simple prefix substring matching. Does not enforce the 36-character tail length, base62 charset, delimiter boundaries, or stateless JWT token structure.
2. **`kengaku-shokunin`** (`plans/stage_scan.py:67-68`):
   - **Mechanism**: Regex rules:
     * `github-pat`: `(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,}`
     * `github-finepat`: `(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{22,}`
   - **GitHub token detection**: Detects classic 36+ base62 prefixed tokens (`gh[pousr]_`) and fine-grained PATs. Does **not** detect the stateless installation token format `ghs_<digits>_<3 dot-separated base64url segments>`.
3. **`chousa-shokunin`** (`tools/research-gate.sh:1086-1087`):
   - **Mechanism**: Regex checks: `ghp_[A-Za-z0-9]{20,}` (class `ghp_prefix`) and `github_pat_[A-Za-z0-9_]{10,}` (class `github_pat`).
   - **GitHub token detection**: Partial only. Detects `ghp_` and fine-grained `github_pat_`. Does **not** detect `gho_`, `ghu_`, `ghs_`, `ghr_`, or stateless installation tokens.
4. **`tabi-shokunin`** (`scripts/check-sources.mjs:347`):
   - **Mechanism**: Regex in `credentialPatterns`: `/ghp_[A-Za-z0-9]+/`.
   - **GitHub token detection**: Minimal. Detects `ghp_` only. Does **not** detect `gho_`, `ghu_`, `ghs_`, `ghr_`, `github_pat_`, or stateless tokens.
5. **`mado-shokunin`** (`tools/mado-tripwire.py:301-305`):
   - **Mechanism**: Generic regex: `SECRET_PATTERNS = (... re.compile(r"[A-Za-z0-9_\\-]{32,}"))`.
   - **GitHub token detection**: Indirect only. Collaterally matches arbitrary 32+ alnum/dash/underscore strings; has no dedicated GitHub token recognition.
6. **Remaining 15 Sibling Lanes**:
   - Zero active secret scanners. Historical Sentinel grep receipts from past waves exist in `souji-shokunin`, `kaidoku-shokunin`, `mado-shokunin`, and `tameshi-shokunin`, but no maintained instrument.

### 1.2 Capture Writers in Sibling Lanes
1. **`chousa-shokunin`**: `tools/capture-fetch.py` (HTTP curl GET fetcher into `corpus/captures/`), `tools/capture-text.py` (OOXML/OLE docx/doc text extraction into captures). Neither performs pre-write secret scanning.
2. **`kumitate-shokunin`**: `scripts/source-capture.mjs` (offline byte-persistence gate validating opened `SOURCES.md` rows against committed captures; does not fetch).
3. **`souji-shokunin`**: `tools/souji-wave-evidence-capture.sh` (census wave artifact capture). Pre-write secret scan: NO.
4. **`kake-shokunin`**: `scripts/live_snapshot.py`, `scripts/response_snapshot.py` (page and response snapshot fetchers), `scripts/capture_delta.py` (drift checker). Pre-write secret scan: NO.
5. **`tabi-shokunin`**: `corpus/evidence/tabi-a1-r2b-capture/capture.mjs`, `tabi-r2-1-capture/capture.mjs` (loopback test runners). Pre-write secret scan: NO.
6. **`kama-shokunin`**: `tools/round90-reason-capture.py` (reasoning trace capture). Pre-write secret scan: NO.
7. **`tameshi-shokunin`**: `tools/context-capture.py` (receipt gate; callers select non-secret files). Pre-write secret scan: NO.
8. **`tsukuroi-shokunin`**: `tools/capture-resume-facts-r84.py` (/proc and /sys facts capture). Pre-write secret scan: NO.
9. **`audio-shokunin`**: Hardware/audio stream capture probes in `corpus/live/`. Pre-write secret scan: NO.

### 1.3 Overlap Finding
Zero sibling lanes implement pre-write secret scanning on network capture ingestion. Sibling lanes with capture fetchers (`chousa-shokunin`, `kake-shokunin`) operate without intake credential screening. Sibling secret scanners lack the dual classic-base62 and stateless-JWT recognition defined in kasegi round 92.

---

## 2. Kasegi Callers & Importers of `capture-secret-scan.py` at 58c0c115342877ee556cae19928d69839b0b29f0

Receipt: `ConnectorOverlap-receipts/kasegi-callers.txt`.

At C2 landing `58c0c115342877ee556cae19928d69839b0b29f0`, `corpus/instruments/capture-secret-scan.py` (sha256 `04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e`) exports 13 shapes: the 6 gate patterns, 2 AWS shapes (`aws-sts-session-token`, `aws-access-key-id`), 3 cloud signed-URL/cookie shapes (`gcs-signed-url-signature`, `azure-sas-signature`, `cloudfront-signed-url-signature`, `cloudfront-signed-cookie-signature`), and the new `github-token`.

### 2.1 Caller & Importer Inventory

| Caller / Importer | Location & Invocation | Mechanism | Inherits `github-token`? |
|---|---|---|---|
| **`capture-source.py` (Intake Gate)** | `corpus/instruments/capture-source.py:101-124` | Dynamically imports `capture-secret-scan.py` via `importlib.util.spec_from_file_location("capture_secret_scan", path)`. In `intake_gate()`, calls `scan.patterns()` and `scan.scan_bytes()`. | **YES.** Both classic `gh[pousr]_` (36 base62) and stateless `ghs_<digits>_<JWT>` forms are enforced before any file write. Verified by live drive in `$S` (intake gate returned `[("github-token", 1)]`, `written=no`). |
| **`capture-secret-scan.py` (Self / CLI)** | `corpus/instruments/capture-secret-scan.py` | Direct CLI entry point (`--files`, `--rev`, `--selftest`). Enforced by L1 under `QUALITY.md` R138 before committing new captures or wave receipts. | **YES.** Native pattern definitions and passing selftest cases 47–52. |
| **Practice Evidence Scope** | `corpus/practice/<pkg>/evidence/` | Evaluated by `capture-secret-scan.py` `--rev` or `--files` via `is_capture_path()` (line 17). | **YES.** |
| **Practice Tooling: `claim-package-check.py`** | `corpus/instruments/claim-package-check.py` | Defines static `SECRET_PATTERNS` (6 base shapes). Does **not** import `capture-secret-scan.py`. | **NO.** `claim-package-check.py` is the upstream provider of `gate_patterns()` to `capture-secret-scan.py`, not an importer. |
| **Round-92 C2 Counter** | `.ufo/waves/round-92/c2/capability-check.py` | Dynamically imports scanner via `load_instrument()`. | **YES.** Directly tests K1–K8 (K4 plants, K6 base discrimination, K7 runtime seeded plants, K8 29 clauses). |
| **Round-92 C2 Controls** | `.ufo/waves/round-92/controls/c2-controls-r92.sh` | Executes `c2-forgeries.py` against candidate scanner and verifies unpinned controls. | **YES.** |
| **Round-90 C2 Counter** | `.ufo/waves/round-90/c2/capability-check.py` | Evaluates capability `capture-intake-gate`. | **YES at runtime, but fails G0 by design.** Runtime intake gate protects against `github-token`. However, limb G0 verifies shape set equality against round 90's 11 expected shapes; receiving 13 shapes from round 92 fails G0 (expected cross-round counter staleness). |
| **Other Core Instruments** | `anchorcheck.py`, `resolve.py`, `census-freshness-check.py`, `figure-audit.py`, `source-recheck.py` | Tracked in `corpus/instruments/`. | **NO.** None of these instruments import or execute `capture-secret-scan.py`. |

### 2.2 Execution of `capture-source.py --selftest` in Git Archive Sandbox
An isolated extract of `58c0c115342877ee556cae19928d69839b0b29f0` was staged in `$S/archive` and verified:
```
$ cd /fast/scratch/hyaku/kasegi-r92/ConnectorOverlap/archive
$ python3 -B corpus/instruments/capture-source.py --selftest
selftest normalize=ok deterministic=ok
INTAKE-REFUSED SELFTEST shape=credential line=1 out=/tmp/capture-source-selftest-ltjzrzph/out.txt written=no
INTAKE-REFUSED SELFTEST shape=aws-sts-session-token line=1 out=/tmp/capture-source-selftest-ltjzrzph/out.txt written=no
selftest intake-refuse=ok existing-kept=ok
EXIT_CODE: 0
```
Verdict: **PASS** (exit code 0).

---

## 3. Cross-Claim Pattern Analysis & `corpus/QUALITY.md` Review

Receipt: `ConnectorOverlap-receipts/c1-c2-patterns-and-quality.txt`.

### 3.1 The Shared Pattern Across C1 and C2 in Round 92
Both claims in Round 92 operationalize the principle of **preserving semantic truth by explicitly accounting for and verifying exclusions/boundaries where mechanical or naive application would induce falsehoods or false positives**:
- **C1 (`depth:verifiability`):**
  Tranche 7 applied 25 label-named edits from `ReviewC1Labels`'s 30 labelled pairs.
  Crucially, 2 pairs (`triage-thresholds.md:437` and `:438`) were **explicitly EXCLUDED** from repointing. Line 437 quotes historical superseded text ("reward.min present on 48", which existed at historical `intake-surface.md:76` at commit `fb9ac8e`). Repointing line 437 to live lines 89–90 would violate quote truth, because lines 89–90 state the corrected text ("reward object on 48 but numeric reward.min on only 14"). Repointing under that quote would create a false attribution.
  In addition, 3 pairs were identified as no-edit CORRECT pairs (counter-examples in `citation-bases.md` and an external merge input in `japanese-domestic-disclosure-workflow.md`).
  Counter limb M10 was tightened to enforce completeness over the exact set of 30 `(site, key)` tuples (25 edits + 3 no-edit + 2 EXCLUDED = 30).
- **C2 (`coverage`):**
  Capability extension adds `github-token`.
  Rather than naive prefix matching (`gh[pousr]_.*` or matching `github_pat_` without distinguishing fine-grained structure), C2 explicitly bounds the shape:
  1. Classic tokens require exactly 36 base62 characters after the 5 classic prefixes.
  2. Stateless tokens require `ghs_<digits>_<3 dot-separated base64url segments>`.
  3. Negative boundaries prevent false matches embedded in alphanumeric strings.
  4. Documentation placeholders (`ghs_APPID_JWT`) are verified NOT to match.
  5. Fine-grained PATs (`github_pat_`) are explicitly excluded as a named known limit ("neither opened nor claimed").
  Counter limb K8 maps every positive clause and negative boundary/exclusion 1-to-1 to a plant.

### 3.2 Evaluation of Existing Criteria in `corpus/QUALITY.md`
A systematic audit of criteria R1 through R143 in `corpus/QUALITY.md` was conducted:
- **R10:** Governs fixture matrices stating covered/unpinned escape classes, but does not govern citation-repair tranches or quote preservation.
- **R108:** Requires knowledge entries to attribute only what anchors state, but does not provide an operational rule preventing citation-repair tranches from repointing quotes of superseded text.
- **R131:** Requires code citations (`path:line`) to name lines holding the cited token, but does not prevent citation maps from repointing quotes of superseded prose.
- **R135:** Requires falsifiable rules not to contradict Limits or assert what quotes do not state.
- **R137:** Defines citation-for-citation qualification for planned tranches, but says nothing about handling quotes of superseded text.
- **R140:** Requires a non-author hand-labelled sample (>=15 keys) when keys are selected by a lexical proxy, but does not specify how to handle labelled pairs that quote superseded text.
- **R141:** Governs capability counter plants lying within scan scope.
- **R142:** Governs environment isolation via `git archive REV` in clean clones.
- **R143:** Requires re-anchoring knowledge citations when an instrument's line layout shifts.

### 3.3 Recommendation: Proposed Criterion R144
`corpus/QUALITY.md` currently lacks a criterion governing citation repair exclusions for quotes of superseded text.

**Proposed Rule R144:**
```markdown
| R144 | A citation-repair tranche that encounters an anchor whose citing cell quotes superseded or historical text MUST NOT repoint the anchor if the quoted text is absent from the repointed range (preserving quote fidelity under R108/R131). The pair must either:
  (a) be explicitly declared as an EXCLUDED pair with the historical text and revision cited in the counter docstring, and verified unchanged by completeness checks (M10 over (site, key) tuples); or
  (b) be repaired by a whole-cell rewrite that cites the live anchor and updates the quote via an explicit erratum. Check before landing: every mapped repoint is verified to contain the cell's quoted text at the target range; any repoint that separates a quote from its text fails the landing gate. | `corpus/lessons/round-92.md` § C1 tranche 7 exclusion of rows 437/438; ReviewC1Sites round-92 findings |
```

---

## 4. UFO-FSD Connector Synthesis: Proposed Round-93 Claim Pair

Receipt: `ConnectorOverlap-receipts/round93-proposals.txt`.

### 4.1 Grounding in Routed Defects & Round-92 Evidence
1. **`round-91-verifier-spotcheck.md` §6**:
   - *Defect 1*: Row 454 second token (`triage-thresholds.md:454` cites `SKILL.md:494-506`, which lacks EV formula) + D2/D3 rows 367/369/370 and SKILL.md token drift.
   - *Defect 6* (carried from r90): `capture-source.py` crashes on `file://` (status=None); missing explicit `--allow` file silently loads as empty instead of failing closed.
2. **`ReviewC1Sites` Round 92 Findings (this wave)**:
   - *High-severity WRONG landings at lines 58 and 144*: Dropping `mission-control.md:20-21` left `SKILL.md:117` as the surviving tie in both cells. At `cb1ef2b`, line 117 is a provenance string (`provenance.json:29`). The actual termination condition is at `SKILL.md:191` (`attempts()>=2`).
   - *Stale root-level citations*: Line 153 (`SKILL.md:14-15` -> `:265-266`), line 390 (`SKILL.md:525` -> `:322`), line 90 (`SKILL.md:113-114,175-176` -> `:182-185`).
   - *Residual defect on row 438*: Historical target is `mission-control.md:52`, not `:37-38`.
   - *Systemic Verifiability Blind Spot*: Root-level references (`SKILL.md:N`) bypass `knowledge-meter.py` M4/M5 because they are absolute root refs (HOST abs_tokens=127).
3. **Round 92 C2 Scanner Frontier**:
   - S136 documents fine-grained personal access tokens (`github_pat_`), which round 92 explicitly left as a named known limit ("neither opened nor claimed").

### 4.2 Proposed Round-93 Claim 1 (C1): Axis `depth:verifiability` (score 4)
- **Statement**:
  Tranche 8: of the flagged citation defects in `corpus/knowledge/triage-thresholds.md`,
  (a) the 2 WRONG survivor ties at lines 58 and 144 are repointed from `SKILL.md:117` to `SKILL.md:191` (the actual `attempts()>=2` termination condition);
  (b) line 454 second token is repointed from `SKILL.md:494-506` to the live EV formula anchor in `SKILL.md`;
  (c) lines 90, 153, 390 are repointed to their live `SKILL.md` anchors (182–185, 265–266, 322);
  (d) row 438 historical reference is corrected to `mission-control.md:52`, preserving the quoted text;
  and the counter verifies:
  - M9: edit-equals-label for all tranche 8 repairs;
  - M10: completeness over the repaired `(site, key)` tuples;
  - M11 (New Limb: Root-Token Anchor Verification): for each repaired `SKILL.md:N` cite, verifies that line N in `SKILL.md` contains the cited identifier/formula, closing the HOST token verification gap.
- **Counter Idea**:
  `python3 -B .ufo/waves/round-93/c1/knowledge-meter.py --lane . --base-rev <base> --after-rev <landing> --map .ufo/waves/round-93/c1/repair-map.tsv` (Limbs M0, M1, M9, M10, M11).
- **Do-Nothing Control**:
  Running counter against base revision fails M9 and M10 (unrepaired rows) and fails M11 because `SKILL.md:117` contains zero occurrences of `attempts` or `MAX_ATTEMPTS`.

### 4.3 Proposed Round-93 Claim 2 (C2): Axis `coverage` (score 8 held)
- **Statement**:
  Capability extension of `capture-source.py` intake gate and `capture-secret-scan.py`:
  (a) `capture-source.py` intake gate fails closed (`INTAKE-REFUSED shape=gate-error:FileNotFoundError`) when an explicit `--allow` path is provided but does not exist on disk, rather than silently falling back or loading empty (defect 6);
  (b) `capture-source.py` fetch handles non-HTTP schemes (`file://`) without crashing on status=None (defect 6);
  (c) `capture-secret-scan.py` extends `github-token` detection to cover fine-grained tokens: `github_pat_` followed by 22 base62 characters, an underscore, and 59 base62 characters (total 93 characters; S136:163), closing the round-92 named known limit.
- **Counter Idea**:
  `python3 -B .ufo/waves/round-93/c2/capability-check.py --lane . --rev <rev> --work <scratch>` (Limbs K1–K6).
- **Do-Nothing Control**:
  Running counter against base revision fails K2 (base silently accepts missing `--allow`), fails K3 (base crashes on `file://`), and fails K4 (base misses fine-grained `github_pat_` plants).

### 4.4 Second-Order Effects Across Surfaces
- **Runtime Surface**: Fast sub-second counter execution; zero network I/O; clean scratch isolation under `$TMPDIR`.
- **Contract Surface**: Directly resolves four numbered defects from `round-91-verifier-spotcheck.md` §6 (Defects 1 & 6) and cures the 2 high-severity WRONG survivor ties identified by `ReviewC1Sites` in round 92.
- **Substrate Surface**: Hardens `capture-source.py` intake gate against silent allowlist bypasses and scheme crashes.
- **Verification Surface**: Closes the unmeasured HOST token gap in `knowledge-meter.py` via limb M11, preventing root reference drift from escaping future citation tranches.

---

## 5. Route Table

| # | Finding | Recommended Owner |
|---|---|---|
| 1 | Sibling lanes (`chousa-shokunin`, `kake-shokunin`) operate capture writers without pre-write secret scanning | Informational to Sibling Lanes |
| 2 | Sibling secret scanners (`kengaku-shokunin`, `kagi-shokunin`, `chousa-shokunin`, `tabi-shokunin`) lack stateless JWT token recognition | Informational to Sibling Lanes |
| 3 | `capture-source.py` intake gate in kasegi inherits `github-token` and passed `--selftest` at `58c0c11` | C2 Owner (Round 92 verified) |
| 4 | Tranche 7 EXCLUDED pairs 437/438 preserve quote truth against superseded text; `QUALITY.md` lacks rule for this pattern | ScribeQuality / Round 93 (Proposed R144) |
| 5 | Tranche 7 lines 58 and 144 left WRONG survivor ties (`SKILL.md:117` provenance line instead of `:191` termination condition) | C1 Owner (Round 93 Tranche 8) |
| 6 | Systemic stale root citations in `triage-thresholds.md` (lines 90, 153, 390, 454) bypass M4/M5 citation meter | C1 Owner / Limb M11 (Round 93) |
| 7 | `capture-source.py` intake gate silently loads empty allowlist on missing `--allow` and crashes on `file://` | C2 Owner (Round 93) |
| 8 | S136 fine-grained PATs (`github_pat_`) remain a named known limit | C2 Owner (Round 93) |

---

## 6. Files Written & Scratch Accounting

Files written:
- `.ufo/waves/round-92/w1/ConnectorOverlap.md` (this report)
- `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/sibling-scan.txt`
- `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/kasegi-callers.txt`
- `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/c1-c2-patterns-and-quality.txt`
- `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/round93-proposals.txt`

Scratch accounting & credential hygiene:
- Scratch root `/fast/scratch/hyaku/kasegi-r92/ConnectorOverlap` was used for temporary archive extractions and derivation.
- Every file in `.ufo/waves/round-92/w1/ConnectorOverlap-receipts/` and this report was verified with `python3 -B corpus/instruments/capture-secret-scan.py --files`: output `hits=0 files=0 rc=0`.
- The scratch directory `/fast/scratch/hyaku/kasegi-r92/ConnectorOverlap` is purged prior to completion (`trap 'rm -rf -- "$S"' EXIT` / explicit removal).
