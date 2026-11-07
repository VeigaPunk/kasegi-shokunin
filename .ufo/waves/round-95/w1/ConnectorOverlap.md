# ConnectorOverlap Report — Round 95 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 95, Attempt 1 (ONE v1 wave of 13 seats)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4), `coverage` (score 8 held)  
Base commit: `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`  
Freeze commit: `347519f21524d2bc13eb6c91cf3550930a4265b3`  
C1 landing commit: `53ec479d71d25cf5be052db794a548a5904564b8`  
C2 landing commit: `38e7319f44a9fab2978b59ffd43faf207cf62b32`  
Scratch root: `/fast/scratch/hyaku/kasegi-r95/ConnectorOverlap`  
Receipts directory: `.ufo/waves/round-95/w1/ConnectorOverlap-receipts/`

---

## Verdict

Verdict: STANDS. Both frozen claims (C1 and C2) independently re-derived with rc=0 across all limbs.

- **Sibling-overlap scan**: 20 sibling repositories scanned across `/home/vgpnk/Projects/shokunin/*-shokunin`. Zero sibling lanes hold an implementation of the 76-character `github-refresh-token`, zero hold the three-segment GitLab JWT family (`glcbt-`/`glsat-`/`gliamat-`), zero hold a `part`-edit counter pattern or `Replace part:` repair map, and zero maintain a markdown knowledge citation meter.
- **Lane proposal audit (`considerthese/`)**: All 8 reflection files (`2026-10-19.md` through `2026-10-26.md`) audited. Zero unimplemented proposals in `considerthese/` touch round 95's C1 or C2 claims.
- **Contested scope statement**: Contested scope: None; no sibling lane contests or implements the C1 citation repair / knowledge meter scope or the C2 76-character GitHub refresh token / three-segment GitLab JWT scanner scope.

---

## 1. Sibling-Lane Overlap Scan

A comprehensive, read-only search across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/` was performed over their `corpus/instruments/` and `.ufo/waves/` paths for:
- `ghr_`
- `github-refresh-token`
- `glcbt`
- `glsat`
- `gliamat`
- `gitlab-jwt-token`
- `Replace part:`
- `citation-premise`
- `repair-map`

Receipts: `sibling-grep-ghr-.txt`, `sibling-grep-github-refresh-token.txt`, `sibling-grep-glcbt.txt`, `sibling-grep-glsat.txt`, `sibling-grep-gliamat.txt`, `sibling-grep-gitlab-jwt-token.txt`, `sibling-grep-Replace-part-.txt`, `sibling-grep-citation-premise.txt`, `sibling-grep-repair-map.txt`.

### 1.1 Sibling Overlap Table

| Sibling | Path | What It Holds | Overlap with Kasegi C1/C2 |
|---|---|---|---|
| `kagi-shokunin` | `corpus/transcript-scan.sh:87`, `.ufo/waves/round-27` to `round-33` | Classic GitHub prefix check (`'ghp_' 'gho_' 'ghu_' 'ghs_' 'ghr_' 'github_pat_'`) in SQLite transcript janitor script without length bounds or boundary discrimination. | **Zero overlap**. Unanchored bare prefix search in transcript text; does not implement or recognize the 76-character `github-refresh-token` shape or GitLab JWT shapes. Zero overlap with C1. |
| `kama-shokunin` | `.ufo/waves/round-20/build/out/ConnectKagi/secret-shape-scan.py:42`, `.ufo/waves/round-35/w1/out/RevengerScope.md:67` | Loose regular expressions (`(?<![A-Za-z0-9])(ghp_\|gho_\|ghu_\|ghs_\|ghr_\|github_pat_...)([A-Za-z0-9_\-]{8,})`) in historical round artifacts. | **Zero overlap**. Loose lower-bound prefix scanner (>= 8 chars); does not model or enforce the 76-character length constraint from S141/S142, nor GitLab JWT shapes. Zero overlap with C1. |
| `kotoba-shokunin` | `.ufo/waves/round-82/build/Kb82E12Loader-omp-18.14.0-strings.txt:648519,1118310` | Static string dump from external `omp` binary v18.14.0 containing literal list `["gho_", "ghp_", "ghu_", "ghs_", "ghr_", ...]`. | **Zero overlap**. Third-party diagnostic strings dump only. |
| `mado-shokunin` | `.ufo/waves/round-20/w1/reports/SentinelFixtures.md:49`, `.ufo/waves/round-30/w1/reports/SentScope.md:314` | Round-20 diagnostic report quoting external `gitleaks dir` default rule name (`6 github-refresh-token`); round-30 note mentioning classic prefixes. | **Zero overlap**. Diagnostic observation of external tool run; no instrument implementing the shape. Zero overlap with C1. |
| `souji-shokunin` | `.ufo/waves/round-17/w1/SentinelTranscripts.md:18` | Sentinel transcript hygiene table row checking bare prefixes `ghp_ gho_ ghu_ ghs_ ghr_ github_pat_`. | **Zero overlap**. Bare prefix hygiene audit in transcripts. Zero overlap with C1. |
| `kaidoku-shokunin` | `tools/round-93/craft-citation-semantic.py`, `tools/round-97/craft-citation-v2.py` | Semantic citation verification gate for `SKILL.md` craft tables, validating `QUALITY <N>` citations against keyword atoms in `corpus/QUALITY.md`. | **Disjoint domain**. Kaidoku checks internal craft rows against `QUALITY.md` criteria. Kasegi C1 (`knowledge-meter.py`) is an anchor-repair and citation-survival meter for knowledge markdown (`triage-thresholds.md`, `iso-29147-crosswalk.md`) against `SKILL.md`, `mission-control.md`, and snapshot captures (`S041.txt`). Zero overlap with C2. |
| `kake-shokunin` | `scripts/citation_lint.py` | Commit-citation hygiene gate over `{SCORECARD.md, LOG.md}`, checking git commit hashes against git revs. | **Zero overlap**. Git commit object hygiene gate; no token-level path citation or secret scan capability. |
| `kama-shokunin` | `tools/citation-provenance.py`, `tools/round77-citation-baseline.py` | Revision-qualified digest tags `cite(<rev>, <path>, sha256=...)` verified against git blobs. | **Zero overlap**. Git blob digest validation; distinct from markdown token line-anchor citation metering. |
| `tsukuroi-shokunin` | `tools/check-section-citations.py` | Section-citation errata gate for `section-citation-errata-r16.json` checking headings and row substrings. | **Zero overlap**. Heading and row substring locator in bootloader records. |
| `souji-shokunin` | `tools/souji-citation-reconcile.py` | Self-assessment citation cell reconciler checking after-values and commit pins against test receipts. | **Zero overlap**. Test receipt value reconciler. |
| All 20 Sibling Lanes | `corpus/instruments/`, `.ufo/waves/` | Target patterns `glcbt`, `glsat`, `gliamat`, `gitlab-jwt-token`, `Replace part:`, `repair-map`, `citation-premise`. | **Zero matches (0 hits)**. The 3-segment GitLab JWT shapes, the `Replace part:` repair mechanism, and the knowledge-meter repair map exist exclusively in `kasegi-shokunin`. |

### 1.2 Contested Scope Determination

**Contested scope: None.**
No sibling repository implements or claims any portion of kasegi's round-95 C1 citation repair surface or C2 GitHub refresh token / GitLab JWT secret-scan surface. The integrator does not need to partition or negotiate ownership of either capability.

---

## 2. Lane-Local Proposal Audit (`considerthese/`)

All files in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/` were inspected:
- `2026-10-19.md` (7 suggestions: anchorcheck regression test, claim-package rubric calibration, CVSS/VRT severity sources, Saturation line pre-draft, PR #1 decision, craft-vs-meta ratio, change-driven reflections)
- `2026-10-20.md` (6 suggestions: live-source rechecker, rubric Frontier folding, owed-corrections ledger, pre-screening Frontier sources, metric redefinition flagging, anchorcheck carry-overs)
- `2026-10-21.md` (6 suggestions: daily recheck lines, pre-admission snapshot string matching, CNA 4.2.0/CRA Art. 14 in rubric, C1 resolver second review, infrastructure tracking, carry-overs)
- `2026-10-22.md` (5 suggestions: single-seat close-r23 dossier, branch scanner, wall-clock idleness counter, CVSS v4 rubric lens, event reflections)
- `2026-10-23.md` (5 suggestions: quote uniqueness in rechecker contract, close-r23 dossier with diffs, F06/F07 quote checks, idle cadence downshifting, README branch pruning)
- `2026-10-24.md` (5 suggestions: normalization in rechecker contract, clean snapshot capture, close-r23 dossier, idle downshift, PR #1 pruning)
- `2026-10-25.md` (6 suggestions: wave-evidence bloat cap, distance to next score, bounty craft / SHONEN box 2, proposal status ledger, open-defects ledger, event reflections)
- `2026-10-26.md` (7 suggestions: explicit distance to next score, SHONEN box 2 end-to-end domain task, pre-complete quiescence gate, wave evidence capping, F18 PROVINCE amendment, cadence retuning, proposal status ledger)

Receipt: `considerthese-proposals.txt`.

**Finding**: No file or proposal in `considerthese/` addresses or touches round 95's C1 (`triage-thresholds.md` rows / Tranche 10 / S041 crosswalk citations / `knowledge-meter.py`) or C2 (`github-refresh-token` 76 chars / GitLab JWT shapes / `capture-secret-scan.py`). The proposals in `considerthese/` address historical rounds 18–35 concerns and procedural workflow improvements.

---

## 3. Independent Re-derivation of Frozen Claims

### 3.1 Claim C1 Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-95/c1/knowledge-meter.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --base-rev 9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10 \
    --after-rev 53ec479d71d25cf5be052db794a548a5904564b8 \
    --map .ufo/waves/round-95/c1/repair-map.tsv \
    --labels-rev 347519f21524d2bc13eb6c91cf3550930a4265b3 \
    --base-target 1007/1998 \
    --target 1008/1994 \
    --map-sha256 8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6 \
    --work /fast/scratch/hyaku/kasegi-r95/ConnectorOverlap/c1-work
  ```
- **Observed Result**:
  - `KNOWLEDGE-METER base=1007/1998 after=1008/1994 base_target=1007/1998 target=1008/1994 sites=16 labels=16 after_rev=53ec479d71d25cf5be052db794a548a5904564b8 mirror_absent=True pinned=archive`
  - `LIMB M0 pass base=1007/1998`
  - `LIMB M1 pass after=1008/1994`
  - `LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0`
  - `LIMB M4 pass bad=none`
  - `LIMB M5 pass out_of_range=none`
  - `LIMB M9 pass rows=16 unbound=none`
  - `LIMB M10 pass labelled=16 want=16 mapped=16 kinds=cell-repair=4,part=5,range=7 unknown=none unapplied=none unlabelled=none`
  - `LIMB M6 pass sha256=8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6`
  - `KNOWLEDGE-METER-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c1-predicate-run.txt`

### 3.2 Claim C2 Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-95/c2/capability-check.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --rev 38e7319f44a9fab2978b59ffd43faf207cf62b32 \
    --work /fast/scratch/hyaku/kasegi-r95/ConnectorOverlap/c2-work \
    --instrument-sha256 66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707 \
    --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
  ```
- **Observed Result**:
  - `CAPABILITY-CHECK-REV rev=38e7319f44a9fab2978b59ffd43faf207cf62b32 seed=1241966984`
  - `LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=115`
  - `LIMB K2 ok rc=0 scanned=2477 hits=0 allowed=26 unused_allow=0`
  - `LIMB K3 ok rc=1 hits=6 missing=none extra=none`
  - `LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none`
  - `LIMB K5 ok rows=1 last=87`
  - `LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential`
  - `CAPABILITY-CHECK-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c2-predicate-run.txt`

---

## 4. UFO-FSD Connector Move: Cross-Surface Synthesis

### 4.1 Evidence
1. **Intake vs Packaging Gate Asymmetry**:
   - `corpus/instruments/capture-source.py:101-124` dynamically loads `capture-secret-scan.py` and evaluates `scan.patterns()` in `intake_gate()`. In round 95, it automatically inherits all 16 secret patterns (including C2's `github-refresh-token` and `gitlab-jwt-token`).
   - Conversely, `corpus/instruments/claim-package-check.py:34-41` (which enforces rule `R-NOSECRET` over the six-file claim-package contract defined in `corpus/knowledge/claim-package-contract.md`) defines a static, unextended tuple of only 6 baseline patterns:
     ```python
     SECRET_PATTERNS = (
         ('private-key', ...),
         ('op-ref', ...),
         ('bearer', ...),
         ('authorization', ...),
         ('credential', ...),
         ('session-cookie', ...),
     )
     ```
   - In fact, `capture-secret-scan.py:228-233` imports `claim_package_check.SECRET_PATTERNS` as its `gate_patterns()`, but `claim-package-check.py` never imports `capture-secret-scan.patterns()`.
2. **Second-Order Effect**:
   - A newly ingested capture or wave receipt in `corpus/source-snapshots/` or `*-receipts/` is strictly audited against all 16 patterns (including 76-character `ghr_` tokens and GitLab JWT forms).
   - However, a claim package submitted under `corpus/practice/` (e.g. `curl-ibb-h1-1997312`) being audited by `claim-package-check.py` is checked against only the 6 baseline patterns. If a package contains a modern 76-character GitHub refresh token or a 3-segment GitLab JWT token, `claim-package-check.py` evaluates `RULE R-NOSECRET verdict=pass` (`claim-package-check-practice.txt`).
3. **Allowlist Asymmetry**:
   - `capture-secret-scan.py` supports `capture-secret-allow.tsv` with path, shape, and SHA-256 digest binding (`HEX64`).
   - `claim-package-check.py` has no digest-bound allowlist mechanism; any positive match on its patterns causes an unconditional `RULE R-NOSECRET verdict=fail` exit 1.

### 4.2 Affected Axes
- `coverage` (score 8 held): Expands secret-scanning coverage to the lane's submission gate (`claim-package-check.py`), eliminating the gap where claim packages could leak token classes that the ingestion scanner already detects.
- `depth:verifiability` (score 4): Aligns the claim package verification gate with the same verified provider tokens (S140, S141, S142) established in C2, removing divergence between the capture gate and the package submission gate.

### 4.3 Proposed Move
**Synthesize the secret-scanning substrate across intake and packaging gates:**
1. Extract or expose the unified pattern suite from `capture-secret-scan.patterns()` into a shared definition callable by `claim-package-check.py`'s `R-NOSECRET` rule.
2. Introduce package-relative digest-bound allowlisting in `claim-package-check.py` (analogous to `capture-secret-allow.tsv`) for documented, non-credential placeholders (such as synthetic documentation tokens in practice reports).
3. Update `claim-package-check.py --selftest` to assert coverage across all 16 patterns, including `github-refresh-token` and `gitlab-jwt-token`.

### 4.4 Risks
1. *Circular import dependency*: `capture-secret-scan.py` already imports `claim_package_check.py`. Moving to a bidirectional import will cause an `ImportError` unless patterns are factored into a standalone module (e.g., `corpus/instruments/secret_patterns.py`) or imported lazily within `rule_nosecret()`.
2. *Practice package regression*: Existing packages under `corpus/practice/` might contain example strings matching AWS, Cloud, GitHub, or GitLab patterns. Live test of `corpus/practice/curl-ibb-h1-1997312` (`claim-package-check-practice.txt`) confirmed 0 hits under baseline patterns, but full 16-pattern sweep must be validated prior to landing.
3. *Contract synchronization*: `corpus/knowledge/claim-package-contract.md` specifies the rules of the package. Modifying `R-NOSECRET` requires updating documentation to state that provider-specific token shapes (GitHub, GitLab, AWS, Azure, GCS) are included.

### 4.5 Verification
1. Run `python3 -B corpus/instruments/claim-package-check.py --selftest` and verify all 16 pattern checks pass.
2. Run `python3 -B corpus/instruments/claim-package-check.py corpus/practice/curl-ibb-h1-1997312` and verify `package=... rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.
3. Construct a fixture package containing a synthetic `ghr_` + 76 string and assert `RULE R-NOSECRET verdict=fail detail=hits=1,shape=github-refresh-token exit=1`.

---

## Receipts

All command outputs cited in this report are preserved in `.ufo/waves/round-95/w1/ConnectorOverlap-receipts/`:

| Receipt File | Command / Test Executed | Observed RC | Output Summary |
|---|---|---|---|
| `c1-predicate-run.txt` | `python3 -B .ufo/waves/round-95/c1/knowledge-meter.py ...` | `rc=0` | All limbs M0–M10 pass; meter 1007/1998 -> 1008/1994. |
| `c2-predicate-run.txt` | `python3 -B .ufo/waves/round-95/c2/capability-check.py ...` | `rc=0` | All limbs K1–K6 pass; cases=115; seed=1241966984. |
| `sibling-grep-ghr-.txt` | Sibling grep for `ghr_` across all 20 siblings | `rc=0` | 21 lines; bare prefix checks in `kagi`, `kama`, `kotoba`, `mado`, `souji`. |
| `sibling-grep-github-refresh-token.txt` | Sibling grep for `github-refresh-token` across all 20 siblings | `rc=0` | 2 lines; diagnostic gitleaks report reference in `mado`. |
| `sibling-grep-glcbt.txt` | Sibling grep for `glcbt` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-glsat.txt` | Sibling grep for `glsat` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-gliamat.txt` | Sibling grep for `gliamat` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-gitlab-jwt-token.txt` | Sibling grep for `gitlab-jwt-token` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-Replace-part-.txt` | Sibling grep for `Replace part:` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-citation-premise.txt` | Sibling grep for `citation-premise` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `sibling-grep-repair-map.txt` | Sibling grep for `repair-map` across all 20 siblings | `rc=0` | 1 line (`rc=0`); 0 hits. |
| `find-citation-premise-meter.txt` | Find `*citation*`, `*premise*`, `*meter*` files in siblings | `rc=0` | 74 lines; lists citation tools in `kaidoku`, `kake`, `kama`, `tsukuroi`, `souji`. |
| `sibling-citation-tools-head.txt` | Python inspection of sibling citation tool heads | `rc=0` | Examines `kaidoku`, `kake`, `kama`, `tsukuroi`, `souji`, `mado` scripts. |
| `considerthese-proposals.txt` | Proposal extraction from all 8 `considerthese/*.md` files | `rc=0` | 55 lines; 0 proposals touch C1 or C2. |
| `receipts-hygiene-scan.txt` | `capture-secret-scan.py --files ConnectorOverlap-receipts/*` | `rc=0` | 14 files scanned, 0 hits, 0 leaks. |
| `claim-package-check-selftest.txt` | `python3 -B corpus/instruments/claim-package-check.py --selftest` | `rc=0` | 10 cases, 0 failures. |
| `claim-package-check-practice.txt` | `python3 -B corpus/instruments/claim-package-check.py corpus/practice/curl-ibb-h1-1997312` | `rc=0` | 8 rules pass, verdict=WELL-FORMED exit=0. |
