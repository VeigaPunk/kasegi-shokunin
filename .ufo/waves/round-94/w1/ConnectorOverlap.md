# ConnectorOverlap Report — Round 94 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 94, Attempt 1 (ONE v1 wave of 13 seats; count: 13 seats; L1 holds planner seat)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4), `coverage` (score 8 held)  
Base commit: `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`  
Freeze commit: `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`  
C1 landing commit: `d51220aeb4a538b7b211bb2629e83210669cd56d`  
C2 landing commit: `996460861d4130ddb2da6b7554e905d3e47504a3`  
Scratch root: `/fast/scratch/hyaku/kasegi-r94/ConnectorOverlap` (purged prior to exit)  
Receipts: `.ufo/waves/round-94/w1/ConnectorOverlap-receipts/`

---

## Verdict

Verdict: lanes scanned=20 sibling lanes (21 total including kasegi). Sibling GitLab runner/deploy detectors=0; length-bounded custom instance prefix detectors=0. Citation meter overlap=0 (distinct scopes). Capability row duplicates=0.

- **Sibling-overlap scan**: Scanned all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin`. Active production credential scanners/pattern lists exist in 6 sibling lanes (`kagi`, `kengaku`, `chousa`, `tabi`, `souji`, `mado`), plus one wave-level sentinel scanner in `kumitate`.
  * **(a) `gitlab-pat` with custom instance prefix**: **0** sibling lanes detect `glpat-` with length-bounded custom prefix. Only `kagi` checks `glpat-` in production, using unbounded SQL `LIKE '%glpat-%'` which matches arbitrary substrings without length bounds, boundary discrimination, or prefix validation (false positives on bare prefix, 19-char, 21-char, and unhyphenated word-prefixed negatives). `kumitate`'s wave sentinel checks `glpat-[A-Za-z0-9_-]{16,}` (loose lower bound, no upper/exact bound, no custom instance prefix validation).
  * **(b) `gitlab-runner-auth-token` (`glrt-`/`glrtr-`, optional `t1_`/`t2_`/`t3_`)**: **0** sibling lanes detect runner authentication tokens.
  * **(c) `gitlab-deploy-token` (`gldt-`)**: **0** sibling lanes detect deploy tokens.
  * **(d) Citation / anchor verification gates**: 6 sibling lanes maintain citation or anchor verification instruments (`kaidoku`, `kagi`, `chousa`, `souji`, `tameshi`, `tsukuroi`). Every sibling citation instrument has a **distinct scope** (Ghidra session logs, registry quote location in fetched HTML/bodies, self-assessment test receipt quotes, limine bootloader adjacency anchors, or XML tag-stripped raw spans). **0** sibling gates verify token-level knowledge markdown citations (`corpus/knowledge/<name>.md:N-M` or `SKILL.md:N[-M]`).
  * **(e) Capability row duplication**: **0** sibling lanes duplicate the `capture-secret-scan` capability row in `SCORECARD.md`.
- **Kasegi intake gate inheritance**: `corpus/instruments/capture-source.py:101-124` dynamically loads `corpus/instruments/capture-secret-scan.py` and evaluates `scan.patterns()` in `intake_gate()`. At landing `996460861d4130ddb2da6b7554e905d3e47504a3`, `patterns()` exports 16 shapes (6 `SECRET_PATTERNS`, 2 AWS, 4 Cloud, 1 GitHub, 3 GitLab). Live test harness in scratch confirmed that `capture-source.py` inherits all 3 new GitLab shapes (`gitlab-pat` with custom instance prefix, `gitlab-runner-auth-token`, `gitlab-deploy-token`), refusing positives and passing negative controls without requiring any edits to `capture-source.py`. `capture-source.py --selftest` passes (rc=0).
- **Counter limbs duplication & sole guards**:
  * **C1 (`knowledge-meter.py`)**:
    - *Duplicated guard*: M1 and M3 both catch an unapplied tranche (`do-nothing`); M4 failure cascades directly into M5 (`not m5bad and not m4bad`).
    - *Sole guards*: M0 (base target resolve rate), M1 (after target resolve rate), M3 (unmapped git modifications, old token presence on base line, duplicate map rows), M5 (out-of-range line anchors on syntactically valid edits matching git commits, including embedded lane-roots in cell-repairs), M6 (map sha256), M9 (binding to `labels.tsv` and derived edit equality), M10 (completeness of mapped pairs).
  * **C2 (`capability-check.py`)**:
    - *Duplicated guard*: Forgeries that blank, drop, or loosen shapes (e.g. F1, F2, F3, F4, F6) trip multiple K limbs simultaneously (K1, K3, K4, K7, K8, K9).
    - *Sole guards*: K5 (SCORECARD table row), K6 (base discrimination against round-92), K9 (previous-landing regression against round-93 landing), K2 (historical S122 STS token), K3 (clean repository state at HEAD), K7 (dynamic seed pseudo-random generation vs static fixture literal keying), K1 (file digest pins and selftest), K8 (61-clause 1-to-1 mapping).
- **Frozen claims verdict**: **STANDS** — C1 (meter 1008/1999 -> 1009/2000, 19 repoints, 10 EXCLUDED) and C2 (`capture-secret-scan.py` sha256 `22ba32d1...`, capability row byte-identical, K1–K9 pass across runtime seed, seed 1, and seed 9191) independently re-derived.

---

## 1. Sibling-Lane Credential Scanner & Pattern List Scan

A read-only pattern sweep was conducted across all 20 sibling lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kasegi-shokunin`).
Receipts: `ConnectorOverlap-receipts/sibling-heads.txt`, `ConnectorOverlap-receipts/sibling-patterns-scan.txt`, `ConnectorOverlap-receipts/sibling-scanners-detail.txt`.

### 1.1 Fleet Sibling Inventory

| # | Lane | HEAD Commit | Tracked Files | Production Secret Scanner / Pattern List | Wave Sentinel |
|---|---|---|---|---|---|
| 1 | `audio-shokunin` | `f9da7ee9` | 50,582 | None | None |
| 2 | `chousa-shokunin` | `408ae68f` | 21,852 | `tools/research-gate.sh:1086-1087` (`b23301b6...`) | Round wave controls |
| 3 | `game-dev-2d-shokunin` | `1e033ef0` | 42,574 | None | Historical receipts only |
| 4 | `game-dev-3d-shokunin` | `39ca3973` | 23,570 | None | Historical receipts only |
| 5 | `kagi-shokunin` | `0085a5f7` | 9,482 | `corpus/transcript-scan.sh:87,91` (`2d60981b...`) | Round wave controls |
| 6 | `kaidoku-shokunin` | `0b518f56` | 57,462 | None | Historical wave receipts |
| 7 | `kake-shokunin` | `dd7a146d` | 28,361 | None | None |
| 8 | `kama-shokunin` | `e6f1dcce` | 45,237 | None | Round wave tests |
| 9 | `kengaku-shokunin` | `34b28c47` | 30,378 | `plans/stage_scan.py:67-68` (`cda552ad...`) | Round wave controls |
| 10 | `kotoba-shokunin` | `0344ddae` | 20,945 | None | None |
| 11 | `kotodama-shokunin` | `5fa04a9b` | 13,574 | None | None |
| 12 | `kumitate-shokunin` | `e4887850` | 31,078 | None | `.ufo/waves/round-93/K93Sentinel/shape-scan.py:24,26` (`ac86feeb...`) |
| 13 | `lore-shokunin` | `0f044aa7` | 6,400 | None | None |
| 14 | `mado-shokunin` | `8a0aadb0` | 36,108 | `tools/mado-tripwire.py:301-305` (`cd9da20c...`) | Wave sentinels |
| 15 | `mori-shokunin` | `7765969c` | 15,286 | None | Historical receipts |
| 16 | `revenger-shokunin` | `654d0929` | 5,887 | None | Wave receipts (`SentinelScope.md`) |
| 17 | `souji-shokunin` | `488956c4` | 20,716 | `tools/souji-proc-census.sh:219` (`3bc40344...`), `tools/souji-receipt-run.py:104` (`0ed30d44...`), `tools/souji-verify.sh:132` (`e6cb3f93...`) | Wave sentinels |
| 18 | `tabi-shokunin` | `ae2dc25f` | 29,394 | `scripts/check-sources.mjs:347` (`afd04787...`) | None |
| 19 | `tameshi-shokunin` | `87d1635c` | 27,522 | None | Historical receipts |
| 20 | `tsukuroi-shokunin` | `40efa4ea` | 29,195 | None | None |

Across 20 sibling lanes, 6 lanes maintain active production scanners/pattern lists (`kagi`, `kengaku`, `chousa`, `tabi`, `souji`, `mado`), 1 lane maintains a wave sentinel scanner (`kumitate`), and 13 lanes maintain zero active secret scanners.

---

### 1.2 Per-Scanner Evaluation on C2 GitLab Shapes

Receipt: `ConnectorOverlap-receipts/sibling-detection-matrix.txt`.

#### 1. `kagi-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/transcript-scan.sh:87,91`
- **Commit / SHA256**: HEAD `0085a5f76c9dc7e977f6606324e873d25b4fc44d` / `2d60981b198cef41b9263a1427b41f92d98b65eb26ff71c28057bea0ad823a23`
- **Pattern Text**:
  ```bash
  PATTERNS_HIT=(
    ...
    'ghp_' 'gho_' 'ghu_' 'ghs_' 'ghr_' 'github_pat_'   # line 87
    ...
    'glpat-' 'npm_'                                     # line 91
  )
  ```
  Evaluated via: `SELECT count(*) FROM $t WHERE $c LIKE '%$(like_lit "$p")%' ESCAPE '\'`
- **(a) `gitlab-pat` with custom instance prefix**: **NO**. Matches `LIKE '%glpat-%'`. Completely unbounded substring matching: bare `glpat-` and `acme-glpat-` hit only because they contain `glpat-`. However, short 19-char tail, long 21-char tail, and unhyphenated word prefix (`xglpat-`) all trigger false positives. Zero length bound, zero boundary discrimination.
- **(b) `gitlab-runner-auth-token` (`glrt-`/`glrtr-`)**: **NO** (0/4 detected).
- **(c) `gitlab-deploy-token` (`gldt-`)**: **NO** (0/2 detected).
- **Scope / Overlap**: Distinct scope (SQLite janitor transcript database scanner; unanchored substring matching; no length bounds, no runner/deploy token shapes).

#### 2. `kengaku-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/stage_scan.py:67-68`
- **Commit / SHA256**: HEAD `34b28c47bc38b4e0aa11f44f2dfe7c9470d551ac` / `cda552adc72b9aa493c803e2a05cff016947422ed279f87ae215adb33f803fc5`
- **Pattern Text**:
  ```python
  ("github-pat", re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,}")),
  ("github-finepat", re.compile(r"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9_]{22,}")),
  ```
- **(a) `gitlab-pat`**: **NO** (`glpat-` is completely absent from `RULES`).
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (pre-stage scanner for benchmark model outputs; GitHub tokens only; zero GitLab coverage).

#### 3. `chousa-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:1086-1087`
- **Commit / SHA256**: HEAD `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe` / `b23301b6dc141968edc33e838733df9cc3b3ecc2ab815e6d0acffd7efb546065`
- **Pattern Text**:
  ```bash
  elif [[ $line =~ ghp_[A-Za-z0-9]{20,} ]]; then class=ghp_prefix
  elif [[ $line =~ github_pat_[A-Za-z0-9_]{10,} ]]; then class=github_pat
  ```
- **(a) `gitlab-pat`**: **NO**.
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (research gate tripwire for literature claims; checks `ghp_` and `github_pat_` only).

#### 4. `tabi-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-sources.mjs:347`
- **Commit / SHA256**: HEAD `ae2dc25fe8b4db70d2ef8a83804bc5545fbc35ff` / `afd047874a1aa136efc252290bef8c76bb90d85f405d1ecf593e9d407125df77`
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
- **(a) `gitlab-pat`**: **NO**.
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (source check gate; checks `ghp_` only; zero GitLab coverage).

#### 5. `souji-shokunin`
- **Locations**:
  * `tools/souji-proc-census.sh:219`: `while [[ $value =~ (ghp_)[[:alnum:]_-]+ ]]; do`
  * `tools/souji-receipt-run.py:104`: `(re.compile(r"ghp_[A-Za-z0-9_-]+"), "[REDACTED]"),`
  * `tools/souji-verify.sh:132`: checks path names matching `*.env`, `*credential*`, `*secret*`, `id_*`, `*.pem`.
- **Commit / SHA256**: HEAD `488956c45166ed6edc21567e8588a8134413949e` / `3bc40344...`, `0ed30d44...`, `e6cb3f93...`
- **(a) `gitlab-pat`**: **NO**.
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (process census redaction and path safety verification; zero GitLab coverage).

#### 6. `mado-shokunin`
- **Location**: `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py:301-305`
- **Commit / SHA256**: HEAD `8a0aadb0727b7a753d837a49d37938400ce6c83d` / `cd9da20c2f562efbd30967e00c0c630026de6e6d06ef74399eb1a46ccf00ea84`
- **Pattern Text**:
  ```python
  SECRET_PATTERNS = (
      re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
      re.compile(r"AKIA[0-9A-Z]{16}"),
      re.compile(r"[A-Za-z0-9_\-]{32,}"),
  )
  ```
- **(a) `gitlab-pat`**: **NO** (bare 26-char PAT is under 32 chars and is missed).
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (tripwire for terminal output; generic 32+ length check; zero dedicated token recognition).

#### 7. `kumitate-shokunin` (Wave Sentinel)
- **Location**: `/home/vgpnk/Projects/shokunin/kumitate-shokunin/.ufo/waves/round-93/K93Sentinel/shape-scan.py:24,26`
- **Commit / SHA256**: HEAD `e4887850448c38172e12fcb220496d23f49e8121` / `ac86feebf8c1f9521ab970a1ff6c3c9b9245c52f09d8d2f7812773b0a5f7c348`
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
- **(a) `gitlab-pat`**: **PARTIAL / FALSE POSITIVES**. Uses `glpat-[A-Za-z0-9_-]{16,}` which has a lower bound of 16, but NO upper or exact length bound (matches 19-char and 21-char negatives). Matches custom prefix only degenerately by ignoring prefix characters.
- **(b) `gitlab-runner-auth-token`**: **NO**.
- **(c) `gitlab-deploy-token`**: **NO**.
- **Scope / Overlap**: Distinct scope (wave sentinel sweep over wave artifacts; loose lower bounds only; zero runner/deploy coverage).

---

### 1.3 Empirical Shape Detection Comparison Matrix

Tested empirically via `test_sibling_matrix.py` against all sibling scanners:

| Case | Expected | `kasegi` (our lane) | `kagi` | `kumitate` | `kengaku` | `chousa` | `tabi` | `souji` | `mado` |
|---|---|---|---|---|---|---|---|---|---|
| `pos_pat_bare` | **HIT** | `gitlab-pat` | `LIKE '%glpat-%'` | `glpat-0123456789abcdefghij` | — | — | — | — | — |
| `pos_pat_custom` | **HIT** | `gitlab-pat` | `LIKE '%glpat-%'` | `glpat-0123456789abcdefghij` (trunc) | — | — | — | — | — |
| `neg_pat_19` | **CLEAN** | **CLEAN** | **FAIL** (`LIKE`) | **FAIL** (`glpat-0123...`) | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `neg_pat_21` | **CLEAN** | **CLEAN** | **FAIL** (`LIKE`) | **FAIL** (`glpat-0123...`) | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `neg_pat_letter` | **CLEAN** | **CLEAN** | **FAIL** (`LIKE`) | **CLEAN** | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `pos_runner_glrt` | **HIT** | `gitlab-runner-auth-token` | — | — | — | — | — | — | — |
| `pos_runner_glrtr` | **HIT** | `gitlab-runner-auth-token` | — | — | — | — | — | — | — |
| `pos_runner_t1` | **HIT** | `gitlab-runner-auth-token` | — | — | — | — | — | — | — |
| `pos_runner_custom` | **HIT** | `gitlab-runner-auth-token` | — | — | — | — | — | — | — |
| `neg_runner_21` | **CLEAN** | **CLEAN** | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `neg_runner_t4` | **CLEAN** | **CLEAN** | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `pos_deploy` | **HIT** | `gitlab-deploy-token` | — | — | — | — | — | — | — |
| `pos_deploy_custom` | **HIT** | `gitlab-deploy-token` | — | — | — | — | — | — | — |
| `neg_deploy_19` | **CLEAN** | **CLEAN** | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |
| `neg_deploy_21` | **CLEAN** | **CLEAN** | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN | CLEAN |

Conclusion: **ZERO** sibling lanes cover the shapes claimed in C2. No duplication exists; kasegi's scanner coverage is strictly disjoint from all sibling pattern lists.

---

## 2. Sibling-Lane Citation / Anchor Verification Gate Scan

Receipt: `ConnectorOverlap-receipts/sibling-citation-gates.txt`.

Committed citation and anchor verification gates across the fleet:

| # | Lane | Instrument Path | Commit HEAD | File SHA256 | Target Scope | Overlap with Kasegi C1 |
|---|---|---|---|---|---|---|
| 1 | `kaidoku-shokunin` | `.ufo/gates/citation-drift/citation-drift-probe.py` | `0b518f56` | `436ae13c...` | Pinned pointer table; extracted line numbers from sentences vs target text | **Distinct scope**: verifies line numbers stated in text against external REA carrier logs. |
| 2 | `kaidoku-shokunin` | `tools/round-97/craft-citation-v2.py` | `0b518f56` | `a50aa02d...` | `QUALITY <N>` citations parsed from craft manifest rows vs table | **Distinct scope**: verifies craft table criterion cells. |
| 3 | `kagi-shokunin` | `corpus/quote-locate.py` | `0085a5f7` | `68a33eeb...` | Byte offset verification of quotes in `corpus/quote-bodies.tsv` vs fetch bodies | **Distinct scope**: located byte offsets in HTTP bodies. |
| 4 | `kagi-shokunin` | `corpus/anchor-pins.sh` | `0085a5f7` | `abb9f9b2...` | SHA256 pins of `SOURCES.md` column 7 anchor cells | **Distinct scope**: registry column digest pins. |
| 5 | `chousa-shokunin` | `tools/quote-reopen.py` | `408ae68f` | `47a657e7...` | Re-opening located quotes against live source URLs in registry | **Distinct scope**: live web fetch quote re-derivation. |
| 6 | `chousa-shokunin` | `corpus/evidence/round53/pointer-anchor-check.py` | `408ae68f` | `0acf7287...` | `anchor: "<text>"` strings in `correction:` redirects | **Distinct scope**: exact substring search in redirect targets. |
| 7 | `souji-shokunin` | `tools/souji-citation-reconcile.py` | `488956c4` | `59f1e57d...` | Reconciles self-assessment quote after-values vs committed test receipts | **Distinct scope**: test receipt string matching. |
| 8 | `tameshi-shokunin` | `tools/anchor-drift-sweep.py` | `87d1635c` | `9905a2c9...` | `SOURCES.md` anchor headings vs snapshot headings | **Distinct scope**: markdown heading matching in source snapshots. |
| 9 | `tameshi-shokunin` | `tools/quoted-line-exists.py` | `87d1635c` | `6da61b7f...` | Quoted counter lines in records vs committed test receipt stdout | **Distinct scope**: receipt stdout verification. |
| 10 | `tsukuroi-shokunin` | `tools/check-adjacency-anchors.py` | `40efa4ea` | `588cc44f...` | Adjacency anchors in bootloader records | **Distinct scope**: UKI initramfs adjacency. |
| 11 | `tsukuroi-shokunin` | `tools/check-anchor-coordinates.py` | `40efa4ea` | `fedd45ce...` | Raw line coordinates of XML tag-stripped quotes | **Distinct scope**: XML tag stripping line coordinate reconciliation. |

Conclusion: **ZERO** sibling gates verify token-level markdown citations inside `corpus/knowledge/` (`corpus/knowledge/<name>.md:N-M` or `SKILL.md:N[-M]`). Kasegi's C1 knowledge citation meter (`knowledge-meter.py`) is unique in the fleet. No duplication exists; scopes are strictly disjoint.

---

## 3. SCORECARD Capability Row Duplication Audit

Receipt: `ConnectorOverlap-receipts/sibling-scorecards.txt`.

All 20 sibling `SCORECARD.md` files were parsed for `## Capabilities` tables.
- Zero sibling lanes list `capture-secret-scan` or duplicate its capability.
- Sibling capabilities that mention "scan", "secret", or "capture" are:
  * `kagi`: `release-clock observation`, `differential feed-token agreement gate`, `located-quote gate over committed capture bodies`, `stated-clock offline replay`.
  * `kake`: `GET snapshot + canonical receipt replay`, `Capture-to-capture drift gate`, `Capture-once / audit-offline re-derivation chain`.
  * `souji`: `souji-verify`, `process-residue observations`.
  * `tsukuroi`: `boot-chain-audit`.
All are dedicated to domain-specific concerns (registry clocks, HTML header diffs, process argv leaks, UKI bootloader images) with zero overlap with kasegi's `capture-secret-scan`.

---

## 4. Kasegi Intake Gate Inheritance at Landing `996460861d4130ddb2da6b7554e905d3e47504a3`

Receipt: `ConnectorOverlap-receipts/intake-gate-test.txt`.

### 4.1 Inheritance Mechanism
In `corpus/instruments/capture-source.py:101-124`:
```python
def load_scanner():
    path = os.path.join(HERE, "capture-secret-scan.py")
    spec = importlib.util.spec_from_file_location("capture_secret_scan", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def intake_gate(data, out, allow_path):
    try:
        scan = load_scanner()
        allow = scan.load_allow(allow_path or os.path.join(HERE, "capture-secret-allow.tsv"))
        found, _ = scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)
        return found
    except Exception as e:
        return [("gate-error:%s" % type(e).__name__, 0)]
```
`intake_gate()` dynamically executes `capture-secret-scan.py` and calls `scan.patterns()`.
At landing `996460861d4130ddb2da6b7554e905d3e47504a3`:
- `patterns()` in `capture-secret-scan.py:236-237` returns 16 shapes:
  `gate_patterns()` (6) + `AWS_PATTERNS` (2) + `CLOUD_PATTERNS` (4) + `GITHUB_PATTERNS` (1) + `GITLAB_PATTERNS` (3).
- `GITLAB_PATTERNS` exports `gitlab-pat`, `gitlab-runner-auth-token`, and `gitlab-deploy-token`, all using `_GL_PREFIX = rb"(?:[A-Za-z0-9]{1,20}-)?"` and `_GL_LB`.
Because `capture-source.py` invokes `scan.patterns()` generically, it **automatically inherits protection against custom-instance-prefixed PATs, runner tokens, and deploy tokens without requiring any code edit to `capture-source.py`**.

### 4.2 Live Validation of `intake_gate`
A live Python test harness executed against committed code evaluated 12 test cases:
- `valid-gitlab-pat-bare` (`glpat-` + 20) -> refused as `[('gitlab-pat', 1)]` [PASS]
- `valid-gitlab-pat-custom` (`acme-glpat-` + 20) -> refused as `[('gitlab-pat', 1)]` [PASS]
- `valid-gitlab-runner-glrt` (`glrt-` + 20) -> refused as `[('gitlab-runner-auth-token', 1)]` [PASS]
- `valid-gitlab-runner-glrtr` (`glrtr-` + 20) -> refused as `[('gitlab-runner-auth-token', 1)]` [PASS]
- `valid-gitlab-runner-t1` (`glrt-t1_` + 20) -> refused as `[('gitlab-runner-auth-token', 1)]` [PASS]
- `valid-gitlab-runner-custom` (`prod-glrt-` + 20) -> refused as `[('gitlab-runner-auth-token', 1)]` [PASS]
- `valid-gitlab-deploy-bare` (`gldt-` + 20) -> refused as `[('gitlab-deploy-token', 1)]` [PASS]
- `valid-gitlab-deploy-custom` (`ops-gldt-` + 20) -> refused as `[('gitlab-deploy-token', 1)]` [PASS]
- `neg-gitlab-pat-19` (19 chars) -> allowed `[]` [PASS]
- `neg-gitlab-pat-21` (21 chars) -> allowed `[]` [PASS]
- `neg-gitlab-runner-21` (21 chars) -> allowed `[]` [PASS]
- `neg-gitlab-deploy-19` (19 chars) -> allowed `[]` [PASS]
`python3 -B corpus/instruments/capture-source.py --selftest` exited 0 (`intake-refuse=ok existing-kept=ok`).

---

## 5. Counter Limbs: Duplication Analysis and Sole Guards

Receipt: `ConnectorOverlap-receipts/c1-limb-forgery-matrix.txt`.

### 5.1 C1 Counter (`knowledge-meter.py`)

C1 evaluates limbs M0, M1, M3, M4, M5, M6, M9, M10.

#### Duplicated Limbs / Cascades in C1
1. **M4 failure cascades directly into M5**:
   Line 407: `limbs.append(("M5", not m5bad and not m4bad, "out_of_range=%s" % ...))`.
   Because M5 requires `not m4bad`, **any syntax or structural binding violation that fails M4 automatically fails M5 as well**. M4 never fails alone.
2. **M1 and M3 co-fail on an unapplied tranche**:
   In the `do-nothing` control (where `after_rev = base_rev`), M1 fails (`after=1008/1999` vs target `1009/2000`) and M3 simultaneously fails (`bad_lines=18`). Both limbs duplicate detection of a missing landing.
3. **M10 and M9 co-fail on an excluded label being mapped**:
   In `m10-excluded-mapped`, M9 fails (`unbound=triage-thresholds.md:88`) and M10 fails (`unlabelled=triage-thresholds.md:88/SKILL.md:113-114`).

#### Sole Guards in C1
- **`M0`**: **SOLE GUARD** for the base resolve rate (`(bn, bm) == (bn0, bm0)`). No other limb checks the base rate.
- **`M1`**: **SOLE GUARD** for target resolve rate when an edit is syntactically well-formed, line-exact, and within range, but fails to move the resolve meter to the target.
- **`M3`**: **SOLE GUARD** for:
  (a) *Unmapped git modifications*: Any edit in `afiles` that is not declared in `repair-map.tsv` produces `bad_lines > 0` in M3. M4 and M5 only iterate over `rows` from the map and never inspect unmapped git diffs. Proven in `m3-union-unmapped` (M3 FAIL, M4 pass, M5 pass).
  (b) *Missing old tokens*: If `b.count(old) < 1` on the base line, M3 fails with `old_not_once > 0`.
  (c) *Duplicate map rows*: `dup_rows > 0` fails M3.
  (d) *Collateral file changes*: `set(bfiles) != set(afiles)` fails M3.
- **`M5`**: **SOLE GUARD** for out-of-range line references (`1 <= lo <= hi <= len(text.splitlines())`) when the edit is syntactically valid and matched in git. Proven in `m5-out-of-range` (M5 FAIL, M3 pass, M4 pass) and `m5-cell-repair-lane-root` (M5 FAIL, M3 pass, M4 pass).
- **`M6`**: **SOLE GUARD** for map file integrity (`got == a.map_sha256`). Proven in `wrong-map-sha` (M6 FAIL, all other limbs pass).
- **`M9`**: **SOLE GUARD** for verifying that the map's `(old, new)` matches the derived edit from `labels.tsv` (`exp[1:] == (old, new)`). Proven in `m9-wrong-new` (M9 FAIL, M3 pass, M4 pass, M5 pass).
- **`M10`**: **SOLE GUARD** for complete coverage of all non-excluded label rows (`mapped == want`).

---

### 5.2 C2 Counter (`capability-check.py`)

C2 evaluates limbs K1, K2, K3, K4, K5, K6, K7, K8, K9 across three random seeds.

#### Duplicated Limbs in C2
1. **Generic scanner failure / Always-clean forgery (`F6-always-clean`)**:
   Fails K1 (selftest_rc=1), K2 (sts_files=0), K3 (unused_allow=23), K4 (missing all plants), K7 (missing all generated), K8 (61 clauses failing), K9 (`lost=39`).
2. **Dropping a token family (`F3-drop-github`)**:
   Fails K1 (selftest_rc=1), K4 (missing 11 github plants), K7 (missing 4 github generated), K8 (11 clauses failing), K9 (`lost=11`).
3. **Loosening token boundary (`F4-loose-runner`)**:
   Fails K1 (selftest_rc=1), K3 (`hits=1` on real tree), K4 (extra hits on negative plants), K7 (extra hit on generated negative), K8 (negative clauses failing).

#### Sole Guards in C2
- **`K5`**: **SOLE GUARD** for `SCORECARD.md` capabilities table row integrity (verifying row cell 1 is `capture-secret-scan`, score is `87`, and required shapes are named). Proven in `row-round93` (K5 FAIL, K1-K4 and K6-K9 pass).
- **`K6`**: **SOLE GUARD** for baseline discrimination vs round-92 base (`BASE_REV`). Verifies that the round-92 scanner does not catch any of the new shapes.
- **`K9`**: **SOLE GUARD** for regression against the previous round landing (`PREV_REV`, round-93 landing). Verifies that (a) previous landing catches none of the round-94 shapes, and (b) candidate loses no shape previously caught (`lost=none`).
- **`K2`**: **SOLE GUARD** for historical regression against the S122 STS token in `HISTORY_REV` (round-86 freeze).
- **`K3`**: **SOLE GUARD** for real working-tree hygiene at `--rev REV` (0 unallowed secrets in tracked files, 0 stale allowlist rows).
- **`K7`**: **SOLE GUARD** against fixture literal keying. A detector hardcoding the static fixture strings of K4 passes K4 and K8, but fails K7 because K7 draws pseudo-random token values from `random.Random(seed)` at run time.
- **`K1`**: **SOLE GUARD** for file digest pins of `capture-secret-scan.py` and `claim-package-check.py`, and `--selftest` execution.
- **`K8`**: **SOLE GUARD** for explicit 1-to-1 mapping of all 61 frozen statement clauses to plant verification outcomes.

---

## 6. UFO-FSD Connector Synthesis & Non-Obvious Move Proposal

### 6.1 Grounding Evidence in Round-94 Local Artifacts
1. **`CriticHarm.md` (§The named harm)**:
   The C2 landing expanded `corpus/instruments/capture-secret-scan.py` (+33 lines, 458 -> 491), shifting line numbers from line 98 onwards. Consequently, **65 of the 102 full-path citations** across 5 `corpus/knowledge/` entries now point at shifted lines (35 distinct cited lines). For example, `capture-intake-gate.md:69,71` quotes docstring sentences at `:122-123` which now sit at `:141-143`.
2. **`CriticHarm.md` (§Q1) & `ReviewC1Labels.md` (Meter Blindness)**:
   `resolve.py` resolves internal citations by path existence only (`os.path.exists`), stripping line ranges (`:NNN`). The knowledge meter reads `1009/2000` at the C2 landing tip, completely blind to the fact that 65 citations point at incorrect lines.
3. **`ReviewC2Scanner-receipts/vendor-vs-instrument.txt`**:
   `capture-secret-scan.py` handles hex entity escape terminators (`\u0026`) via `_ESC_LB` / `_GL_LB` that vendor regex does not directly parse.
4. **`ScoutGitLabRules-receipts/05-lead-shape-probes.txt`**:
   Four fixed-length GitLab shapes documented in S140 remain unmined and scan clean (NO HIT) on the landed scanner:
   - `glagent-[A-Za-z0-9_-]{50}` (Kubernetes Agent Token, S140 line 213)
   - `glsoat-[A-Za-z0-9_-]{20}` (SCIM Token, S140 line 278)
   - `glffct-[A-Za-z0-9_-]{20}` (Feature Flag Client Token, S140 line 392)
   - `gloas-[A-Za-z0-9_-]{64}` (OAuth Application Secret, S140 line 174)
   Additionally, S141 documents the GitHub `ghr_` 76-character refresh token (line 72).
5. **`claims.json` (§P3 Invariant Contradiction)**:
   C1 predicate P3 restricts changes to the two knowledge files; C2 predicate P3 restricts changes to `capture-secret-scan.py` and `SCORECARD.md`. Neither claim landing can repair the citation drift caused by the other without failing its frozen predicate P3.

### 6.2 Stated Contradictions
- **The Cross-Landing Citation Drift Trap**: Any capability expansion of `capture-secret-scan.py` in C2 shifts line numbers. Because C2's predicate P3 forbids touching knowledge files, C2 cannot update the citing entries. And because C1's predicate P3 forbids touching the scanner, C1 cannot synchronize with C2 during landing. This guarantees citation drift at every C2 landing unless resolved outside the claim landings (e.g. in the integration commit).
- **The Resolve Meter Line-Blindness Contradiction**: `resolve.py` classifies `INTERNAL` based purely on file existence. A citation pointing to shifted, invalid, or even nonexistent lines inside an existing file scores as `INTERNAL`. The citation meter rate (+1/+1) measures token-set churn, not citation truth.

### 6.3 Affected Axes
- **`depth:verifiability`** (lowest non-retired axis, score 4): 65 citations into `capture-secret-scan.py` drifted; resolve meter is blind to line coordinates; 10 label rows remain EXCLUDED as prose rewords.
- **`coverage`** (score 8 held): Currently blind to four S140 fixed-length GitLab tokens (`glagent-`, `glsoat-`, `glffct-`, `gloas-`) and S141 `ghr_` refresh tokens.

### 6.4 Proposed Bounded Move for Round 95

A dual, compatible synthesis uniting citation verifiability and scanner coverage:

1. **On `depth:verifiability`**:
   - **Integration Re-Anchor**: In the Round-94 integration commit (or Round-95 C1), apply the mechanical re-anchoring of the 35 shifted lines across the 5 knowledge entries using `CriticHarm-receipts/scanner-cite-drift.tsv` (and `ReviewC2Scanner-receipts/knowledge-citation-reanchor.txt`), restoring verbatim citation truth without violating any frozen claim predicate.
   - **Tranche 10 Prose Rewords**: In Round 95 C1, map the 10 label rows frozen in `EXCLUDED` (`triage-thresholds.md` lines 88, 89, 90, 356, 396, 433, 434, 435) with their explicit reword descriptions already codified in `knowledge-meter.py:104-115`, advancing the resolve meter towards 100% completion.
   - **Line-Coordinate Verifiability Gate**: Introduce an automated line-coordinate audit for citations into lane instruments, checking that every quoted block in `corpus/knowledge/` exists verbatim at its cited lines, bridging the gap between `resolve.py`'s file-existence check and actual text grounding.
2. **On `coverage`**:
   - Extend `capture-secret-scan.py`'s `GITLAB_PATTERNS` to cover the remaining S140 fixed-length shapes:
     ```python
     ("gitlab-agent-token", re.compile(_GL_LB + _GL_PREFIX + rb"glagent-[A-Za-z0-9_-]{50}(?![A-Za-z0-9_-])")),
     ("gitlab-scim-token", re.compile(_GL_LB + _GL_PREFIX + rb"glsoat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])")),
     ("gitlab-feature-flag-token", re.compile(_GL_LB + _GL_PREFIX + rb"glffct-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])")),
     ```
   - All three shapes use exact length boundaries (`{50}`, `{20}`), support optional custom instance prefixes (`_GL_PREFIX`), and were verified clean by `ScoutGitLabRules`.
   - Update S140 status in `corpus/SOURCES.md` from `queued` to `mined`.

### 6.5 Second-Order Effects Across Surfaces
- **Runtime Surface**: Sub-second execution; zero regex backtracking overhead (fixed length quantifiers with negative lookahead). `intake_gate()` automatically inherits protection without code edits to `capture-source.py`.
- **Contract Surface**: Preserves the exact length contract, right lookahead `(?![A-Za-z0-9_-])`, and allowlist schema.
- **Substrate Surface**: S140 row flips to `mined`, resolving Qualifier Q2 from `CriticHarm`.
- **Verification Surface**: `capability-check.py` gains K4/K7/K8 regression clauses for the three new shapes; K9 checks candidate non-regression against round-94 landing; knowledge citations match exact line numbers.

### 6.6 Risks & Mitigations
- **Risk**: Line drift recurrence on future scanner edits.
  * *Mitigation*: In the knowledge entries, cite named functions/blocks (e.g. `load_allow()`, `patterns()`, `Known limits`) in addition to line ranges, and apply re-anchor tables in the integration commit of any round modifying `capture-secret-scan.py`.
- **Risk**: False positives on arbitrary 50-character strings.
  * *Mitigation*: `glagent-` prefix is mandatory, followed by exactly 50 base64-safe characters and bounded by `(?![A-Za-z0-9_-])`.

### 6.7 Verification Plan
1. Run `python3 -B .ufo/waves/round-94/c1/knowledge-meter.py --measure-rev HEAD` to verify meter movement on Tranche 10.
2. Run `python3 -B corpus/instruments/capture-secret-scan.py --selftest` to verify selftest pass with new shapes.
3. Run `capability-check.py` across three seeds to verify K1-K9 pass.
4. Verify all 65 re-anchored citation spans against committed `capture-secret-scan.py` bytes.

---

## Receipts

All commands executed from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (or scratch `$S`); outputs stored in `.ufo/waves/round-94/w1/ConnectorOverlap-receipts/`.

| Command | Observed rc / Output Summary | Receipt Path |
|---|---|---|
| `python3 -B .ufo/waves/round-94/c1/knowledge-meter.py ...` (C1 landing) | rc 0; base=1008/1999, after=1009/2000, M0-M10 pass | `c1-counter-run.txt` |
| `python3 -B .ufo/waves/round-94/c2/capability-check.py ...` (runtime seed) | rc 0; seed=1366489368, nonce=994f788e, K1-K9 pass | `c2-counter-run-default.txt` |
| `python3 -B .ufo/waves/round-94/c2/capability-check.py ... --seed 1` | rc 0; seed=1, nonce=33a1d0a4, K1-K9 pass | `c2-counter-run-seed1.txt` |
| `python3 -B .ufo/waves/round-94/c2/capability-check.py ... --seed 9191` | rc 0; seed=9191, nonce=2c0dc8ca, K1-K9 pass | `c2-counter-run-seed9191.txt` |
| `sha256sum` over 7 frozen artifacts | rc 0; all digests match `claims.json` byte-for-byte | `frozen-pins-check.txt` |
| `git diff --stat dff5a0a..d51220a` | rc 0; C1 landing: 2 files changed, 18 insertions, 18 deletions | `c1-landing-diffstat.txt` |
| `git diff --stat 96b5033..9964608` | rc 0; C2 landing: 2 files changed, 47 insertions, 14 deletions | `c2-landing-diffstat.txt` |
| `python3 scan_siblings.py` | rc 0; 20 sibling lane repositories located and HEAD commits pinned | `sibling-heads.txt` |
| `python3 check_scorecards.py` | rc 0; 0 sibling capabilities duplicate `capture-secret-scan` | `sibling-scorecards.txt` |
| `python3 deep_scan_siblings.py` | rc 0; deep grep for glpat/glrt/gldt and citation/anchor scripts across 20 sibling repos | `sibling-patterns-scan.txt` |
| `python3 inspect_sibling_scanners.py` | rc 0; detailed pattern inspection of 6 sibling scanners | `sibling-scanners-detail.txt` |
| `python3 inspect_citation_gates.py` | rc 0; detailed inspection of 11 sibling citation/anchor gates | `sibling-citation-gates.txt` |
| `python3 test_sibling_matrix.py` | rc 0; 15-case positive/negative matrix evaluated across all scanners | `sibling-detection-matrix.txt` |
| `python3 test_intake_gate.py` | rc 0; 12 positive/negative cases; `capture-source.py --selftest` rc 0 | `intake-gate-test.txt` |
| `python3 test_c1_limbs.py` | rc 0; analysis of C1 control suite limb outcomes | `c1-limb-forgery-matrix.txt` |
