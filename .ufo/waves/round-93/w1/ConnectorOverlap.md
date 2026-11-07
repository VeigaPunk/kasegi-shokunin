# ConnectorOverlap Report — Round 93 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 93, Attempt 1 (ONE v1 wave of 13 seats; count: 13 seats; L1 holds planner seat)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4), `coverage` (score 8 held)  
Base commit: `e15996bfd2f6eca4af39507a7c5973afbeca8347`  
Freeze commit: `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`  
C1 landing commit: `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`  
C2 landing commit: `9225954a6e3f177af46bdb9d811c062a4353a552`  
Scratch root: `/fast/scratch/hyaku/kasegi-r93/ConnectorOverlap` (purged prior to exit)  
Receipts: `.ufo/waves/round-93/w1/ConnectorOverlap-receipts/`

---

## Verdict

Verdict: lanes scanned=20 sibling lanes (21 total including kasegi), glpat detectors=0 bounded (1 unbounded substring detector in kagi; 2 if counting kumitate wave-93 sentinel), escape-aware=0.

- **Sibling-overlap scan**: Scanned all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (500,818 tracked files across the fleet). Active production credential scanners/pattern lists exist in 6 sibling lanes (`kagi`, `kengaku`, `chousa`, `tabi`, `souji`, `mado`), plus one wave-level sentinel scanner in `kumitate`.
  * **(a) `glpat-` with length bound**: **0** sibling lanes detect `glpat-` with a length bound. Only `kagi` checks `glpat-` in production, but uses unbounded SQL `LIKE '%glpat-%'` matching bare prefixes, <20-char tails, and >20-char tails without discrimination. `kumitate`'s wave sentinel checks `glpat-[A-Za-z0-9_-]{16,}` with a lower bound but no upper/exact bound.
  * **(b) GitHub token after escape terminator**: **0** sibling lanes implement escape-terminator left boundary awareness. `kengaku` and `kumitate` fail on escapes ending in alphanumeric characters (`\t`, `\r`, `\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xXX;`). `chousa`, `tabi`, and `souji` use unanchored substring regexes that match after escapes only degenerately while falsely matching letter-prefixed non-tokens (`xghp_`).
  * **(c) Round-92 GitHub shapes**: **0** sibling lanes detect both classic 36-base62 tokens with right boundary and stateless JWT tokens (`ghs_<digits>_<JWT>`).
- **Kasegi intake gate**: `corpus/instruments/capture-source.py:101-124` dynamically loads `corpus/instruments/capture-secret-scan.py` and evaluates `scan.patterns()` in `intake_gate()`. At landing `9225954a6e3f177af46bdb9d811c062a4353a552`, `patterns()` exports 14 shapes. Live test harness in scratch confirmed that `capture-source.py` inherits both `gitlab-pat` (refusing bare prefix, 19-char, 21-char, and letter-prefixed negatives while catching 20-char tokens and escape-preceded tokens) and escape-preceded `github-token` (catching `\t`, `\n`, `\r`, `\u0009`, `%20`, `&#32;`, `&#x20;` preceding tokens while rejecting letter-prefixed values). `capture-source.py --selftest` passes (rc=0).
- **Frozen claims verdict**: **STANDS** — C1 (meter 1007/2001 -> 1009/2000, 5 label edits, cell-repair + lane-root kinds) and C2 (`capture-secret-scan.py` sha256 `7d9d7309...`, capability row byte-identical, K1–K8 pass at 3 seeds) independently re-derived.

---

## 1. Sibling-Lane Credential Scanner & Pattern List Scan

A read-only pattern sweep was conducted across all 20 sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kasegi-shokunin`).
Receipt: `ConnectorOverlap-receipts/sibling-inventory.txt` and `ConnectorOverlap-receipts/sibling-scan.txt`.

### 1.1 Fleet Sibling Inventory

| # | Lane | Tracked Files | Production Secret Scanner / Pattern List | Wave Sentinel |
|---|---|---|---|---|
| 1 | `audio-shokunin` | 50,582 | None | Historical receipts only |
| 2 | `chousa-shokunin` | 21,852 | `tools/research-gate.sh:1086-1087` | Round wave controls |
| 3 | `game-dev-2d-shokunin` | 42,574 | None | Historical receipts only |
| 4 | `game-dev-3d-shokunin` | 23,570 | None | Historical receipts only |
| 5 | `kagi-shokunin` | 9,482 | `corpus/transcript-scan.sh:87,91` | Round wave controls |
| 6 | `kaidoku-shokunin` | 57,462 | None | Historical wave receipts |
| 7 | `kake-shokunin` | 28,361 | None | None |
| 8 | `kama-shokunin` | 45,237 | None | Round wave tests |
| 9 | `kengaku-shokunin` | 30,378 | `plans/stage_scan.py:67-68` | Round wave controls |
| 10 | `kotoba-shokunin` | 20,945 | None | Wave sentinels |
| 11 | `kotodama-shokunin` | 13,574 | None | None |
| 12 | `kumitate-shokunin` | 31,078 | None | `.ufo/waves/round-93/K93Sentinel/shape-scan.py:24,26` |
| 13 | `lore-shokunin` | 6,400 | None | None |
| 14 | `mado-shokunin` | 36,108 | `tools/mado-tripwire.py:301-305` | Wave sentinels |
| 15 | `mori-shokunin` | 15,286 | None | Historical receipts |
| 16 | `revenger-shokunin` | 5,887 | None | None |
| 17 | `souji-shokunin` | 20,716 | `tools/souji-proc-census.sh:219`, `tools/souji-receipt-run.py:104` | Wave sentinels |
| 18 | `tabi-shokunin` | 29,394 | `scripts/check-sources.mjs:347` | Historical sentinels |
| 19 | `tameshi-shokunin` | 27,522 | None | Historical receipts |
| 20 | `tsukuroi-shokunin` | 29,195 | None | None |

Across 20 sibling lanes, 6 lanes maintain production scanners/pattern lists (`kagi`, `kengaku`, `chousa`, `tabi`, `souji`, `mado`), 1 lane maintains a current wave sentinel scanner (`kumitate`), and 13 lanes maintain zero active secret scanners.

---

### 1.2 Per-Scanner Evaluation & Gap Classification

#### 1. `kagi-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/transcript-scan.sh:87,91`
- **Pattern Text**:
  ```bash
  PATTERNS_HIT=(
    ...
    'ghp_' 'gho_' 'ghu_' 'ghs_' 'ghr_' 'github_pat_'   # line 87: GitHub tokens
    ...
    'glpat-' 'npm_'                                     # line 91: GitLab PAT / npm token
  )
  ```
  Evaluated via: `SELECT count(*) FROM $t WHERE $c LIKE '%$(like_lit "$p")%' ESCAPE '\'`
- **(a) `glpat-` with length bound**: **NO**. Matches `LIKE '%glpat-%'`. Completely unbounded substring matching: bare `glpat-`, short 19-char tail, and long 21-char tail all trigger hits.
- **(b) Escape terminator awareness**: **NO**. SQL `LIKE '%ghp_%'` matches anywhere in text without boundary awareness. Preceding escape terminators hit degenerately, but letter-prefixed false positives (`xghp_`) also hit.
- **(c) Round-92 GitHub shapes**: **NO**. Checks prefixes only. No 36-char base62 check, no right-boundary lookahead, and no stateless JWT token shape (`ghs_<digits>_<JWT>`).
- **Gap Class**: Unbounded SQL substring matching; zero length bounds, zero boundary discrimination, missing stateless JWT tokens.

#### 2. `kengaku-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/stage_scan.py:67-68`
- **Pattern Text**:
  ```python
  ("github-pat", re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,}")),
  ("github-finepat", re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{22,}")),
  ```
- **(a) `glpat-` with length bound**: **NO**. `glpat-` is not present in `RULES`. Zero GitLab PAT detection.
- **(b) Escape terminator awareness**: **NO**. The negative lookbehind `(?<![A-Za-z0-9_])` fails when preceded by escape terminators ending in alphanumeric characters (`\t`, `\r`, `\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xXX;`). Tested: all 5 escape test cases missed.
- **(c) Round-92 GitHub shapes**: **PARTIAL / NO**. Uses loose `{36,}` length without upper bound, lacks right-hand boundary `(?![A-Za-z0-9_])`, and completely lacks stateless installation tokens (`ghs_<digits>_<JWT>`).
- **Gap Class**: Missing GitLab PAT, escape-blind left boundary, unconstrained right tail, missing stateless JWT format.

#### 3. `chousa-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:1086-1087`
- **Pattern Text**:
  ```bash
  elif [[ $line =~ ghp_[A-Za-z0-9]{20,} ]]; then class=ghp_prefix
  elif [[ $line =~ github_pat_[A-Za-z0-9_]{10,} ]]; then class=github_pat
  ```
- **(a) `glpat-` with length bound**: **NO**. `glpat-` is not present in `scan_secrets()`.
- **(b) Escape terminator awareness**: **NO**. Regex `=~ ghp_[A-Za-z0-9]{20,}` has no boundary anchoring. Matches after escapes degenerately, but fails boundary discrimination (matches `xghp_`).
- **(c) Round-92 GitHub shapes**: **NO**. Detects only `ghp_` prefix (misses `gho_`, `ghu_`, `ghs_`, `ghr_`), uses loose `{20,}` length, and lacks stateless JWT tokens.
- **Gap Class**: Missing GitLab PAT, single-prefix `ghp_` only, loose length, zero boundary awareness.

#### 4. `tabi-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-sources.mjs:347`
- **Pattern Text**:
  ```javascript
  const credentialPatterns = [
    /op:\/\//,
    /BEGIN[\s\S]{0,100}PRIVATE KEY/,
    /ghp_[A-Za-z0-9]+/,
    /\bAKIA[A-Z0-9]+\b/,
    /xox[baprs]-[A-Za-z0-9-]+/,
  ];
  ```
- **(a) `glpat-` with length bound**: **NO**. `glpat-` is absent from `credentialPatterns`.
- **(b) Escape terminator awareness**: **NO**. Unanchored regex `/ghp_[A-Za-z0-9]+/` matches anywhere in text without boundary checking.
- **(c) Round-92 GitHub shapes**: **NO**. Checks only `ghp_`, uses unconstrained length `+`, misses `gho_`, `ghu_`, `ghs_`, `ghr_`, and lacks stateless tokens.
- **Gap Class**: Missing GitLab PAT, single-prefix `ghp_` only, unconstrained length, zero boundary awareness.

#### 5. `souji-shokunin`
- **Locations**:
  * `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-proc-census.sh:219`:
    `while [[ $value =~ (ghp_)[[:alnum:]_-]+ ]]; do`
  * `/home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-receipt-run.py:104`:
    `(re.compile(r"ghp_[A-Za-z0-9_-]+"), "[REDACTED]"),`
- **(a) `glpat-` with length bound**: **NO**. `glpat-` is not present in redaction patterns.
- **(b) Escape terminator awareness**: **NO**. Unanchored regexes match anywhere without boundary checking.
- **(c) Round-92 GitHub shapes**: **NO**. Checks only `ghp_`, uses unconstrained length `+`, misses other prefixes and stateless tokens.
- **Gap Class**: Output redaction only (not intake validator), missing GitLab PAT, single-prefix `ghp_`, unconstrained length.

#### 6. `mado-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:301-305`
- **Pattern Text**:
  ```python
  SECRET_PATTERNS = (
      re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
      re.compile(r"AKIA[0-9A-Z]{16}"),
      re.compile(r"[A-Za-z0-9_\-]{32,}"),
  )
  ```
- **(a) `glpat-` with length bound**: **NO**. A 26-char GitLab PAT (`glpat-` + 20 chars = 26 chars) is under 32 chars and is completely missed by `[A-Za-z0-9_\-]{32,}`.
- **(b) Escape terminator awareness**: **NO**. Generic string length check without token or escape boundary logic.
- **(c) Round-92 GitHub shapes**: **NO**. No dedicated GitHub token recognition.
- **Gap Class**: Arbitrary length threshold (>=32 chars); blind to 26-char GitLab PATs; zero dedicated token recognition.

#### 7. `kumitate-shokunin` (Round-93 Wave Sentinel)
- **Location**: `/home/vgpnk/Projects/shokunin/kumitate-shokunin/.ufo/waves/round-93/K93Sentinel/shape-scan.py:24,26`
- **Pattern Text**:
  ```python
  PREFIX = re.compile(
      r"(?:^|[^A-Za-z0-9])(sk-[A-Za-z0-9_-]{8,}|sk_live_[A-Za-z0-9]{8,}|"
      r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
      r"xox[abprs]-[A-Za-z0-9-]{8,}|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|"
      r"AIza[0-9A-Za-z_-]{20,}|glpat-[A-Za-z0-9_-]{16,}|hf_[A-Za-z0-9]{20,}|"
      r"pypi-[A-Za-z0-9_-]{20,}|npm_[A-Za-z0-9]{20,})"
  )
  ```
- **(a) `glpat-` with length bound**: **NO**. Uses `glpat-[A-Za-z0-9_-]{16,}` which has a lower bound of 16, but NO upper or exact length bound. Tested: 19-char, 20-char, and 21-char tails all match.
- **(b) Escape terminator awareness**: **NO**. Left boundary `(?:^|[^A-Za-z0-9])` fails when preceded by escape terminators whose last character is alphanumeric (`\n`, `\t`, `\r`, `\uXXXX`, `%XX`). Tested: all escape test cases missed.
- **(c) Round-92 GitHub shapes**: **PARTIAL / NO**. Checks `gh[pousr]_` with loose `{20,}` length, no right boundary, and misses stateless JWT tokens.
- **Gap Class**: Loose lower bound only for GitLab PAT, escape-blind left boundary, unconstrained right tail, missing stateless JWT format.

---

### 1.3 Overlap Matrix

| Lane | Scanner Path | Detects `glpat-` with length bound? | Detects GitHub token after escape terminator? | Detects round-92 GitHub shapes? | Intake gate before capture write? |
|---|---|---|---|---|---|
| **`kasegi` (our lane)** | `corpus/instruments/capture-secret-scan.py` | **YES** (`glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])`) | **YES** (`_ESC_LB` / `_GH_LB`) | **YES** (classic 36-base62 + stateless JWT) | **YES** (`capture-source.py` intake gate) |
| `kagi` | `corpus/transcript-scan.sh` | NO (unbounded `LIKE '%glpat-%'`) | NO (degenerate match; no boundary) | NO (prefixes only) | NO |
| `kengaku` | `plans/stage_scan.py` | NO (absent) | NO (misses alphanumeric escapes) | PARTIAL (loose 36+, no stateless) | NO |
| `chousa` | `tools/research-gate.sh` | NO (absent) | NO (degenerate match; no boundary) | NO (`ghp_` only, loose 20+) | NO |
| `tabi` | `scripts/check-sources.mjs` | NO (absent) | NO (degenerate match; no boundary) | NO (`ghp_` only, unconstrained) | NO |
| `souji` | `tools/souji-proc-census.sh` | NO (absent) | NO (degenerate match; no boundary) | NO (`ghp_` only, unconstrained) | NO |
| `mado` | `tools/mado-tripwire.py` | NO (blind to 26-char PAT) | NO (generic 32+ length check) | NO (generic 32+ length check) | NO |
| `kumitate` | `.ufo/waves/round-93/K93Sentinel/shape-scan.py` | NO (loose 16+, no exact bound) | NO (misses alphanumeric escapes) | PARTIAL (loose 20+, no stateless) | NO |
| 13 other lanes | — | NO (no scanner) | NO (no scanner) | NO (no scanner) | NO |

---

## 2. Kasegi Intake Gate Inheritance at Landing `9225954a6e3f177af46bdb9d811c062a4353a552`

Receipts: `ConnectorOverlap-receipts/kasegi-intake-gate-test.txt`, `ConnectorOverlap-receipts/kasegi-selftest.txt`, `ConnectorOverlap-receipts/kasegi-callers.txt`.

### 2.1 Mechanism of Inheritance

In `corpus/instruments/capture-source.py:101-124`:
```python
def load_scanner():
    path = os.path.join(HERE, "capture-secret-scan.py")
    spec = importlib.util.spec_from_file_location("capture_secret_scan", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def intake_gate(data, out, allow_path):
    """Return [(shape, line)] that refuse these bytes at --out; [("gate-error", 0)] if the scanner cannot run."""
    try:
        scan = load_scanner()
        allow = scan.load_allow(allow_path or os.path.join(HERE, "capture-secret-allow.tsv"))
        found, _ = scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)
        return found
    except Exception as e:  # fail closed: a gate that cannot run refuses
        return [("gate-error:%s" % type(e).__name__, 0)]
```
`intake_gate()` dynamically imports `capture-secret-scan.py` and calls `scan.patterns()`.
At landing `9225954a6e3f177af46bdb9d811c062a4353a552`:
- `patterns()` in `capture-secret-scan.py:212-213` returns 14 shapes:
  `gate_patterns()` (6) + `AWS_PATTERNS` (2) + `CLOUD_PATTERNS` (4) + `GITHUB_PATTERNS` (1) + `GITLAB_PATTERNS` (1).
- `GITHUB_PATTERNS` uses `_GH_LB = _ESC_LB` (`\t`, `\r`, `\n`, `\uXXXX`, `%XX`, `&#NN;`, `&#xXX;`).
- `GITLAB_PATTERNS` uses `_GL_LB` and matches `glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])`.

Because `capture-source.py` calls `scan.patterns()` without hardcoding pattern names, `capture-source.py` **automatically inherits both new shapes at landing without requiring any code edit to `capture-source.py`**.

### 2.2 Live Drive of `intake_gate` in Sandbox

A live Python test harness executed against the committed `capture-source.py` and `capture-secret-scan.py` evaluated 19 positive and negative cases:

```
Total patterns returned by scan.patterns(): 14
Shape names: ['private-key', 'op-ref', 'bearer', 'authorization', 'credential', 'session-cookie', 'aws-sts-session-token', 'aws-access-key-id', 'gcs-signed-url-signature', 'azure-sas-signature', 'cloudfront-signed-url-signature', 'cloudfront-signed-cookie-signature', 'github-token', 'gitlab-pat']
[OK] valid gitlab-pat                         -> got [('gitlab-pat', 1)], expected [('gitlab-pat', 1)]
[OK] tab-escaped gitlab-pat                   -> got [('gitlab-pat', 1)], expected [('gitlab-pat', 1)]
[OK] newline-escaped gitlab-pat               -> got [('gitlab-pat', 1)], expected [('gitlab-pat', 1)]
[OK] unicode-escaped gitlab-pat               -> got [('gitlab-pat', 1)], expected [('gitlab-pat', 1)]
[OK] percent-escaped gitlab-pat               -> got [('gitlab-pat', 1)], expected [('gitlab-pat', 1)]
[OK] bare prefix glpat- (neg)                 -> got [], expected []
[OK] 19-char tail glpat- (neg)                -> got [], expected []
[OK] 21-char tail glpat- (neg)                -> got [], expected []
[OK] letter-prefixed glpat- (neg)             -> got [], expected []
[OK] valid classic github-token               -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] tab-escaped github-token                 -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] newline-escaped github-token             -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] carriage-return-escaped github-token     -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] unicode-escaped github-token             -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] percent-escaped github-token             -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] html-numeric-escaped github-token        -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] html-hex-escaped github-token            -> got [('github-token', 1)], expected [('github-token', 1)]
[OK] letter-prefixed github-token (neg)       -> got [], expected []
[OK] stateless jwt github-token               -> got [('github-token', 1)], expected [('github-token', 1)]

Final Intake Gate Inheritance Verification: ALL TESTS PASSED
```

Additionally, `python3 -B corpus/instruments/capture-source.py --selftest` was executed directly:
```
selftest normalize=ok deterministic=ok
INTAKE-REFUSED SELFTEST shape=credential line=1 out=/tmp/capture-source-selftest-880aku8s/out.txt written=no
INTAKE-REFUSED SELFTEST shape=aws-sts-session-token line=1 out=/tmp/capture-source-selftest-880aku8s/out.txt written=no
selftest intake-refuse=ok existing-kept=ok
EXIT_CODE: 0
```
Verdict: **PASS** (exit code 0).

---

## 3. UFO-FSD Connector Synthesis & Non-Obvious Move Proposal

### 3.1 Grounding Evidence in Round-93 Local Artifacts
1. **`ScoutGitLab.md` (§4 L4-L5)**: GitLab's authoritative secret detection rules repository (`gitlab-org/security-products/secret-detection-rules`, commit `59ada1f4`) and first-party documentation (`…/security/tokens/`, lines 344–364; `…/api/admin/token/`, line 176) document that GitLab Personal Access Tokens permit an **optional custom instance prefix** of 1 to 20 alphanumeric characters followed by a hyphen: `(?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20}`. GitLab's test suite includes `acme-glpat-REDACTED-r93`. Because the round-93 landed scanner enforces `(?<![A-Za-z0-9_-])` as its left boundary, any hyphenated prefix immediately preceding `glpat-` triggers the lookbehind negative, causing all custom-prefixed GitLab tokens to be **silently missed**.
2. **`ReviewC2Scanner.md` (Defect D3)**: The frozen C2 statement and scanner docstring name seven escape terminators, including hex HTML entities (`&#xXX;`). However, `&#x` appears 0 times in `.ufo/waves/round-93/c2/capability-check.py` and 0 times in selftest cases. The hex entity escape is **unpinned** by the verification counter.
3. **`ReviewC2Scanner.md` (Defects D1, D2) & `ReviewC1Labels`**: The C2 landing inserted lines and docstrings into `capture-secret-scan.py`, shifting 60 out of 82 citation ranges across 5 knowledge entries. Furthermore, `corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md` contains 3 falsified measurement statements (selftest case count 68 vs 90; 15 vs 26 `SELFTEST gh-` lines; and the assertion that matches preceded by `[A-Za-z0-9_]` are refused, which was made false by alphanumeric-ending escapes).
4. **Sibling Scanner Sweep**: Sibling lanes completely lack pre-write capture intake screening and boundary-aware token recognition.

### 3.2 Affected Axes
- **`coverage`** (score 8 held): Currently blind to custom-prefixed GitLab tokens (`acme-glpat-...`).
- **`depth:verifiability`** (lowest non-retired axis, score 4): The hex entity escape terminator is unpinned in verification; knowledge citations and measurement assertions drifted after the landing.

### 3.3 Proposed Bounded Move for Round 94

A single, compatible synthesis uniting C1 citation-truth repair and C2 scanner-completeness:

1. **On `coverage`**:
   Extend `capture-secret-scan.py`'s `gitlab-pat` pattern to recognize the documented optional custom instance prefix:
   ```python
   _GL_PREFIX = rb"(?:[A-Za-z0-9]{1,20}-)?"
   ("gitlab-pat", re.compile(_GL_LB + _GL_PREFIX + rb"glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"))
   ```
   This closes the miss on instance-prefixed tokens (`acme-glpat-...`) documented in GitLab's rules repo and `…/security/tokens/`, while preserving the exact 20-character tail length and negative boundaries against bare prefixes, unhyphenated words (`xglpat-`), and trailing characters.
2. **On `depth:verifiability`**:
   - Add explicit regression pins for the unpinned `&#xXX;` hex entity escape in both `--selftest` and `capability-check.py` limb K4/K8 (closing D3).
   - Re-anchor the 60 shifted knowledge citations using `ReviewC2Scanner`'s `reanchor-r93.tsv` and repair the 3 falsified measurements in `github-prefixed-tokens-in-captured-evidence.md` (closing D1).
   - Correct the docstring citation anchor from line 86 to line 87 (closing D2).

### 3.4 Second-Order Effects Across Surfaces
- **Runtime Surface**: Sub-second execution; zero performance degradation. Regex evaluation of `(?:[A-Za-z0-9]{1,20}-)?glpat-` remains strictly deterministic and bounded to 20 prefix characters.
- **Contract Surface**: Preserves the 20-character tail contract and right-hand lookahead. Does not alter allowlist format or require allowlist modifications.
- **Substrate Surface**: `capture-source.py` intake gate automatically inherits protection against custom-prefixed GitLab tokens without requiring changes to `capture-source.py`.
- **Verification Surface**: Eliminates the unpinned escape terminator gap (D3); aligns knowledge base measurements with landed reality under `QUALITY.md` R108/R143.

### 3.5 Risks & Mitigations
- **Risk**: False positives from arbitrary words ending in `-glpat-`.
  * **Mitigation**: The prefix is strictly alphanumeric (`[A-Za-z0-9]{1,20}`), must be followed immediately by `-glpat-`, and must be followed by exactly 20 characters of `A-Za-z0-9_-` with negative right lookahead `(?![A-Za-z0-9_-])`. Unhyphenated words (`myglpat-`) remain non-hits.
- **Risk**: Line-layout drift recurrence when updating docstring.
  * **Mitigation**: Apply the re-anchor table (`reanchor-r93.tsv`) in the same round as the docstring repair, verified by an automated anchor check pass.

### 3.6 Verification Plan
- Counter limb K4 adds plants for `acme-glpat-<20ch>` and `myorg123-glpat-<20ch>`; verifies non-matches for `glpat-` with 19/21 chars, `xglpat-`, and bare prefix.
- Selftest adds test cases for `gl-pat-custom-prefix` and `gh-escape-hex-entity`.
- Citation anchor verification (`anchorcheck.py`) confirms all 60 re-anchored citations resolve cleanly.

---

## 4. Route Table

| # | Finding | Recommended Owner |
|---|---|---|
| 1 | Sibling lanes (`chousa`, `kake`) operate capture writers with zero pre-write secret screening | Informational to Sibling Lanes |
| 2 | Sibling secret scanners (`kengaku`, `kagi`, `chousa`, `tabi`, `souji`) lack escape-aware boundaries and stateless JWT token shapes | Informational to Sibling Lanes |
| 3 | `capture-source.py` intake gate in kasegi inherits `gitlab-pat` and escape-aware `github-token` and passed `--selftest` at `9225954a` | C2 Owner (Round 93 verified) |
| 4 | Landed scanner misses custom instance-prefixed GitLab PATs (`acme-glpat-...`, S139 rules repo) | C2 Owner / Round 94 proposed move |
| 5 | Unpinned hex entity escape `&#xXX;` in `capture-secret-scan.py` (Defect D3) | C2 Owner / Round 94 proposed move |
| 6 | 60 knowledge citation ranges shifted; 3 falsified measurements in `github-prefixed-tokens...` (Defect D1) | ScribeEntry / C1 Owner / Round 94 |
| 7 | Citation off-by-one in scanner docstring line 108 (S139 line 86 vs 87, Defect D2) | C2 Owner / Round 94 |

---

## ## Receipts

1. `python3 -B -c "..."` (sibling lane pattern search across all 20 sibling lanes):
   - Command: Scanned 500,818 tracked files across 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin`.
   - Result: 6 sibling lanes with production tools (`chousa-shokunin`, `kagi-shokunin`, `kengaku-shokunin`, `mado-shokunin`, `souji-shokunin`, `tabi-shokunin`); 1 lane with current wave sentinel (`kumitate-shokunin`); 13 lanes with zero scanners.
   - Receipt: `ConnectorOverlap-receipts/sibling-inventory.txt` (21 lines, rc=0).
2. `python3 -B -c "..."` (sibling scanner behavioral test harness):
   - Command: Tested 7 sibling scanners/sentinels against 15 positive/negative test cases covering bounded `glpat-`, escape terminators, negative boundaries, and stateless tokens.
   - Result: 0/7 detect bounded `glpat-`; 0/7 are escape-aware; 0/7 detect all round-92 GitHub shapes.
   - Receipt: `ConnectorOverlap-receipts/sibling-scan.txt` (137 lines, rc=0).
3. `python3 -B corpus/instruments/capture-source.py --selftest`:
   - Command: Ran `--selftest` on the landed `capture-source.py` at `9225954a6e3f177af46bdb9d811c062a4353a552`.
   - Result: `normalize=ok deterministic=ok intake-refuse=ok existing-kept=ok`, exit code 0.
   - Receipt: `ConnectorOverlap-receipts/kasegi-selftest.txt` (4 lines, rc=0).
4. `python3 -B -c "..."` (kasegi intake gate live drive):
   - Command: Evaluated `capture-source.py` `intake_gate()` against 19 test cases in scratch sandbox.
   - Result: `Total patterns returned by scan.patterns(): 14`; `ALL TESTS PASSED`. Both `gitlab-pat` and escape-aware `github-token` inherited and verified.
   - Receipt: `ConnectorOverlap-receipts/kasegi-intake-gate-test.txt` (23 lines, rc=0).
5. `git grep -n "capture-secret-scan"`:
   - Command: Enumerated all occurrences and callers of `capture-secret-scan` in `kasegi-shokunin`.
   - Result: 1,535 occurrences across history and active instruments; primary callers are `capture-source.py`, C2 capability check counter, and quality gates.
   - Receipt: `ConnectorOverlap-receipts/kasegi-callers.txt` (174 lines, rc=0).
6. `python3 -B corpus/instruments/capture-secret-scan.py --files ...`:
   - Command: Credential hygiene check over all 5 files in `.ufo/waves/round-93/w1/ConnectorOverlap-receipts/`.
   - Result: `CAPTURE-SECRET-SCAN mode=files scanned=5 hits=0 files=0 allowed=0 unused_allow=23 rc=0`. Clean: 0 credential hits.
