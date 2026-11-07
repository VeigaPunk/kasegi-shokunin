# ConnectorOverlap Report — Round 87 Wave 1

Seat: `ConnectorOverlap`  
Lane: `kasegi`  
Round: 87, Attempt 1  
Declared Axes: `depth:verifiability` (lowest axis, score 4), `coverage` (score 7)  
Scratch root: `/fast/scratch/hyaku/kasegi-r87/ConnectorOverlap`  
Assimilation output: `.ufo/waves/round-87/assimilation/`  
Receipts: `.ufo/waves/round-87/w1/ConnectorOverlap-receipts/`

---

## 1. Sibling Overlap & Cross-Lane Secret/Credential Scanning

A read-only sweep was conducted across sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin/corpus/instruments/`, `*/tools/`, and `*/corpus/QUALITY.md`) for capture secret/credential scanning, credential-material rules, and redaction mechanisms.

### Sibling Survey

1. **`kagi-shokunin`**:
   - **Artifacts**: `corpus/transcript-scan.sh`, `corpus/QUALITY.md` (criterion QA5).
   - **What it scans**: Scans SQLite transcript databases (`opencode.db`) across all text-bearing columns (`data`, `prompt`, `content`, etc.) and credential tripwire tables (`account`, `credential`, `session_share`).
   - **Patterns scanned**:
     - `PATTERNS_HIT`: `op://` vault paths; PEM blocks; AWS access keys (`AKIA`, `ASIA`); GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, `github_pat_`); Slack tokens (`xoxb-`, `xoxp-`, `xoxs-`, `xoxa-`, `xoxr-`, `xoxc-`, `xapp-`); AI/provider keys (`sk-ant-`, `sk-proj-`, `sk-or-v1-`, `sk_live`, `sk_test`, `gsk_`, `xai-`, `csk-`); package/platform tokens (`glpat-`, `npm_`, `AIza`, `ya29.`); JWT headers (`eyJhbG`); daemon env tokens (`OP_SESSION_`, `OP_SERVICE_ACCOUNT_TOKEN`).
     - `PATTERNS_WARN`: generic field names (`access_token`, `refresh_token`, `api_key`, `secret_key`, `apikey`).
   - **Quality Rule (QA5)**: "No credential material, ever: no secret value, token, session id, vault/item/field name, or 1Password secret reference".
   - **Relation to kasegi**:
     - *Duplication*: Both check `op://`, PEM private keys, and `AKIA`/`ASIA` access keys.
     - *Differences & Missed Patterns*: kagi scans a relational DB rather than files/git revisions. However, kagi maintains an explicit catalog of high-signal provider prefixes (`ghp_`, `sk-ant-`, `xoxb-`, `ya29.`, `eyJhbG`) that `kasegi`'s regexes currently miss unless preceded by an explicit keyword like `api_key=` or `bearer `.

2. **`mado-shokunin`**:
   - **Artifacts**: `tools/mado-tripwire.py`, `corpus/QUALITY.md` (Rule 5 / 1065), `SKILL.md:2544`, Lesson `round-56.md` (M56-17).
   - **What it scans**: Inspects commands, evaluated shell bodies, and child process spawn arguments in real time before execution.
   - **Patterns scanned**:
     - URI Basic Authentication: `(?<=://)[^/\s:@]+:[^/\s@]+(?=@)` (e.g. `https://user:pass@host`).
     - AWS access keys: `AKIA[0-9A-Z]{16}`.
     - Generic long tokens: `[A-Za-z0-9_\-]{32,}`.
   - **Quality Rule (M56-17 / Credential-material rule)**: Prohibits dumping host environment variable channels or writing sensitive configuration files (e.g., notification daemon configs, EDID serial numbers) into receipts; asserts channel existence without printing values.
   - **Relation to kasegi**:
     - *Duplication*: Both check `AKIA` key IDs.
     - *Differences & Missed Patterns*: mado targets execution runtime and shell strings rather than persistent captures. Crucially, mado catches URI-embedded basic authentication (`user:password@domain`), which kasegi's `capture-secret-scan.py` does not detect.

3. **`mori-shokunin`**:
   - **Artifacts**: `tools/mori-retention-gate.py`, `tools/mori-retention-reconcile.py`, `corpus/QUALITY.md` (Rules 51, 82).
   - **What it scans**: Scans all tracked blobs at a git revision against a strict policy schema (`mori-retention-policy-v1`) with regex classes R1–R9.
   - **Patterns scanned**: Session timestamps/UUIDs (`R1`), session store paths `\.omp/agent/sessions/` (`R2`), numbered tool log artifacts (`R3`), operator documents `~/Documents/` (`R4`), `.bash_history` (`R5`), `sudoers` (`R6`), operator config references (`R7`), routing table keys (`R8`), session record internal values (`R9`).
   - **Quality Rules**: Rule 51 requires zero unallowlisted hits at the measured revision; Rule 82 mandates pre-commit regex linting for host identifiers (`user-[0-9]{3,}\.slice`, `pid=`, `uid=`).
   - **Relation to kasegi**:
     - *Duplication*: Both implement git revision blob scanning and line/sha256 allowlisting.
     - *Differences & Missed Patterns*: mori focuses on host and operator privacy/retention rather than API secrets. kasegi focuses specifically on domain credential shapes and AWS STS session tokens.

4. **Other sibling lanes**:
   - `kake-shokunin`: QA rule bans credential values, session bodies, and raw journals; `prebuild_leak_check.py` validates JSON serializations.
   - `souji-shokunin`: Q46/Q49 redact cmd canaries and reason paths in process census outputs.

### Summary Comparison & Pattern Gaps

| Capability / Pattern | `kasegi` (`capture-secret-scan.py`) | `kagi` (`transcript-scan.sh`) | `mado` (`mado-tripwire.py`) | `mori` (`retention-gate.py`) |
|---|---|---|---|---|
| Target Surface | Captures (`corpus/source-snapshots/`, receipts) | SQLite DB transcript tables | Runtime exec/eval strings | Git blobs (all tracked files) |
| AWS STS Token (`X-Amz-Security-Token`) | **Yes** (strict, non-allowlistable) | No | No | No |
| AWS Access Keys (`AKIA`/`ASIA`) | **Yes** (with documentation example allowlist) | **Yes** (`AKIA`, `ASIA`) | Partial (`AKIA` only) | No |
| PEM Private Keys | **Yes** (`-----BEGIN ... PRIVATE KEY-----`) | **Yes** (`-----BEGIN`) | No | No |
| Provider Token Prefixes (`ghp_`, `sk-ant-`, `xoxb-`, `ya29.`) | No (requires `token=`, `api_key=`, or `bearer `) | **Yes** (dedicated prefix set) | No | No |
| URI Basic Auth (`://user:pass@`) | No | No | **Yes** | No |
| JWT Base64 Header (`eyJhbG`) | No | **Yes** | No | No |
| Host Identifiers / PID / UID / Sessions | No | No | No | **Yes** (R1–R9, Q82) |
| Allowlist Model | TSV (`path\tshape\tsha256\treason`) | Table row exclusion | None (direct redact) | JSON (`path`, `class`, `line_sha256`) |

**Patterns caught by siblings that kasegi misses**:
1. *Explicit vendor token prefixes without preceding keywords* (`ghp_`, `sk-ant-`, `ya29.`, `xoxb-`): In captures containing raw JSON arrays or URL query params where the key is not `api_key` or `token`, kasegi misses them; kagi catches them directly.
2. *URI-embedded basic authentication* (`user:password@domain`): Caught by mado; missed by kasegi.
3. *Base64 JWT headers* (`eyJhbG`): Caught by kagi; missed by kasegi.

---

## 2. Assimilation Check (§10 Commands & Guard Proof)

Per §10 extraction commands, the 0-3-space ID extraction was run over `corpus/SOURCES.md` and `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` into `$A` (`.ufo/waves/round-87/assimilation/`).

### Output Inventory & Metrics

- Directory: `.ufo/waves/round-87/assimilation/`
- Files generated:
  - `reg-ids`: 125 lines (S001 through S125)
  - `staged-ids`: 94 lines (S031 through S124)
  - `collisions`: 94 lines (S031 through S124)
  - `guard-proof.sh`: Reproducible test script proving guard discrimination.
  - `guard-proof.txt`: Complete execution transcript.

### Line Counts & SHA-256 Digests

```
83361fccc2c80072a13459b43c00816c95bc216098158296bc274281eb1e6db1  reg-ids     (125 lines)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids  ( 94 lines)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  collisions  ( 94 lines)
```

*Finding*: Every staged ID in `SOURCES.append.md` (S031–S124) collides with an existing ID in `corpus/SOURCES.md` because kasegi's registry has grown to S125. The collision rate is 100% (94/94). Staged rows cannot be appended without an ID renumbering offset starting at `S126`.

### Guard Proof Execution

The failure-mode proof was run against a synthetic registry where `S002` is indented by two spaces (`  | S002 |`), testing the 0-3 leading space regex against a naive column-zero-only regex (`^\|`).

- **Guard pattern (`^ {0,3}\|[[:space:]]*S[0-9]{3,}`)**:
  - `a-reg-ids`: `S001 S002` (2 lines)
  - `a-staged-ids`: `S002 S003` (2 lines)
  - `a-collisions`: `S002` (1 line, NON-EMPTY)
- **Column-zero pattern (`^\|[[:space:]]*S[0-9]{3,}`)**:
  - `b-reg-ids`: `S001` (1 line — misses indented `  | S002 |`)
  - `b-staged-ids`: `S002 S003` (2 lines)
  - `b-collisions`: 0 lines (EMPTY — false negative)
- **Verdict**: PASS. The 0-3 space pattern reliably catches indented Markdown table rows, preventing silent collision misses.

---

## 3. Considerthese Analysis

Directory: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/` (8 files):
- `2026-10-19.md`
- `2026-10-20.md`
- `2026-10-21.md`
- `2026-10-22.md`
- `2026-10-23.md`
- `2026-10-24.md`
- `2026-10-25.md`
- `2026-10-26.md`

### Unimplemented Proposal Fitting C2 (Credential Hygiene / Capture Discipline)

- **File**: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-24.md`
- **Lines**: 49–52
- **Proposal**:
  > "2. **Fix snapshot capture to store clean text.** The deeper fix for #2 is upstream: re-capture `S030.txt` (and future snapshots) with markup stripped, or record a canonical "text" rendering beside the raw one, so quotes don't have to anticipate `<u>` boundaries. Otherwise every CNA-rules quote is fragile. One seat, mechanical."
- **Current Status**: Still unimplemented. While `capture-source.py` received an initial `html_to_text` helper, `S030.txt` was never re-captured and still contains 57 raw HTML `<u>` tags (`corpus/source-snapshots/round-23/S030.txt`), causing quote fragility. More importantly, the capture ingestion pipeline lacks upstream hygiene enforcement before writing snapshots to disk.

---

## 4. UFO-FSD Synthesis: One Non-Obvious Move

### Evidence

1. **Root Cause of Round 86 Defect (M86-2)**:
   In round 86, `capture-source.py` fetched `https://hackerone.com/reports/1997312.json` and saved it directly to disk. The JSON contained presigned profile URLs with live AWS STS session tokens (`X-Amz-Security-Token`). This file was committed in freeze `252df0c9` and pushed. As noted in `corpus/lessons/round-86.md`: *"no rule ran it over a capture before the freeze commit"*.
2. **Post-Hoc Gap in Round 87 C2**:
   Round 87's C2 introduces `capture-secret-scan.py`, but it operates exclusively as an *offline verifier* (`scan_rev` or `scan_files`). The producer tool (`capture-source.py`) remains completely unshielded: `capture()` performs HTTP fetch and immediately executes `fh.write(data)`.
3. **Capture Hygiene Debt (2026-10-24 Proposal)**:
   `considerthese/2026-10-24.md:49-52` explicitly identified that downstream gates are brittle when raw captures contain unnormalized or contaminated bytes, proposing upstream normalization in `capture-source.py`.
4. **Scope Creep in C1 Landing (`d87b1b55`)**:
   Frozen predicate P3 failed in `d87b1b55` because wave-scaffold files were swept into the commit alongside `corpus/knowledge/` (`changed=8 outside=3 verdict=FAIL`). This demonstrates that relying on post-commit gates invites human and path-scoping errors.

### Affected Axes

- **`depth:verifiability`** (current score: 4): Guarantees that snapshot citations are grounded in clean, deterministic, unpolluted text, preventing quote mismatches caused by markup or volatile credential signatures.
- **`coverage`** (current score: 7): Closes the structural capability loop between capture ingestion (`capture-source.py`) and capture validation (`capture-secret-scan.py`).

### Proposed Move

**Synthesize an Upstream Intake Gate in `capture-source.py`**:
Connect `capture-secret-scan.scan_bytes()` and canonical text normalization directly into `corpus/instruments/capture-source.py:capture()` before snapshot bytes are written to disk.

Specifically:
1. When `capture(source_id, url, out, kind)` receives fetched bytes, after decoding and stripping markup (fulfilling the 2026-10-24 capture discipline proposal), it calls:
   ```python
   hits, allowed = scan_bytes(data, patterns(), path=out, allow=load_allow(ALLOWLIST_PATH))
   ```
2. If `hits` is non-empty (or if an `aws-sts-session-token` is detected), `capture()` prints:
   `REFUSED: secret shape detected at intake (shape=<shape> line=<line>)`
   and immediately aborts with exit code 1 without creating or overwriting `out`.
3. The allowlist (`capture-secret-allow.tsv`) is consulted for known documentation examples, but `aws-sts-session-token` remains strictly non-allowlistable.

### Second-Order Effects Across Surfaces

- **Runtime Surface**: Zero performance overhead on regular operations. Prevents live credential material or volatile presigned session tokens from ever touching the worktree, eliminating emergency token revocations, secret leaks, and `jj abandon` recovery procedures.
- **Contract Surface**: Reuses `capture-secret-scan.py`'s `patterns()` and allowlist logic as a single authoritative specification. Producer and auditor share the exact same pattern definitions without code duplication.
- **Substrate Surface**: Prevents tainted git blobs from entering the local object database (`.git/objects`) or git reflogs, guaranteeing clean commit histories.
- **Verification Surface**: Closes M86-2 structurally at point-of-entry. Turns capture security from a post-freeze audit into a fail-closed pre-freeze intake contract.

### Risks & Mitigations

- **Risk**: False positive lock-out on documentation sources discussing API keys or security terminology.
  - *Mitigation*: Legitimate documentation shapes are allowlisted via `capture-secret-allow.tsv` with path and SHA-256 bindings, while `aws-sts-session-token` is permanently refused.
- **Risk**: Circular dependency or drift between instruments.
  - *Mitigation*: `capture-source.py` imports `scan_bytes`, `patterns`, and `load_allow` directly from `capture-secret-scan.py` in the same directory (`corpus/instruments/`).

### Verification

The move is verified by a two-leg deterministic test in scratch:
1. **Negative / Denial Control**: Ingest a synthetic mock HTTP response containing an `X-Amz-Security-Token=...` parameter into a scratch destination. Assert that `capture-source.py` terminates with exit 1, prints the refusal reason, and asserts that the target snapshot file does NOT exist on disk.
2. **Positive Control**: Ingest a mock HTTP response containing the standard AWS documentation example `AKIAIOSFODNN7EXAMPLE`. Assert exit 0, snapshot file written, and SHA-256 correctly reported.
