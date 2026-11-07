# ConnectorOverlap Report — Round 99 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 99, Attempt 1 (ONE v1 wave of 13 seats)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4), `coverage` (score 8 held; capability extension of capture-secret-scan)  
Base commit: `b9411a6b530e486180cf14c72fccc46668dcf5ee`  
Freeze commit: `6195db307c1cb101eba1d268f8cbfc1578d2caf7`  
C2 landing commit: `a3db47e71fe292c03b00ba11f38cccbec45d3966`  
C1 landing commit: `35e3ab6041ff8690b00d831f27b93d08101fd16a`  
Scratch root: `/fast/scratch/hyaku/kasegi-r99/ConnectorOverlap`  
Receipts directory: `.ufo/waves/round-99/w1/ConnectorOverlap-receipts/`

---

## Verdict Summary

- **Sibling-Overlap Scan**: All 20 sibling repositories scanned across `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/`.
  - **(a) Revision-bound citation census with digests (`census-at-rev`, `citation-survival`, `header-sha256`, `body-sha256`)**: **0 hits of overlapping work**. Zero sibling lanes maintain a revision-bound citation extractor, a citation-survival census of record, or dual header/body sha256 binding. The historical matches in `tsukuroi` (.ufo round 47) refer to an OS package/driver testing shell script (`census-at-rev.sh`); matches in `kotoba` and `mori` are external citations pointing to `kasegi`'s instrument; matches in `kagi` (`quote-locate.py`) and `tabi` (`chain-repro.out`) verify source-capture and HTTP response body digests respectively, disjoint from citation censuses.
  - **(b) GitLab session-cookie or assignment-context credential shapes (`_gitlab_session`, `gitlab-session-cookie`, `assignmentContext`, `assignment-context`, `glcbt-`, `gliamrt-`, `gliamac-`, `gitlab.toml`, `S150`)**: **0 hits of overlapping work**. Zero sibling lanes define or scan for GitLab session-cookie patterns or assignment-context separator windows. Generic session-cookie references in siblings are historical receipt leaks (`kaidoku` GitHub session cookies in `f1.hdr`), curl man page options (`mori` `--junk-session-cookies`), or curl cookie-jar parsers (`tabi`). Every sibling lane defining `S150` defines an entirely disjoint local source (e.g. `chousa` Python `pathlib.Path.parents`, `kama` `llama.cpp` `top_n_sigma`, `mado` ghostty `AppDelegate.swift`, `tsukuroi` Linux `vm.rst`).
- **Contested Scope Statement**: **Contested scope: None.** No sibling repository contests or implements any portion of `kasegi`'s C1 revision-pinned citation census surface or C2 GitLab token/session scanning surface.
- **Kasegi Own-Corpus Discrepancy & Stale Sentence**:
  - In `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` lines 24-26, the text states:
    > *"A matcher built on a whitespace/quote/operator class refuses eight of the twelve real session values the round-98 sentinel measured (round 99)."*
  - This statement is **stale and factually contradictory** to:
    1. `corpus/instruments/capture-secret-scan.py:196-197`: *"Round 98 used a whitespace/quote/operator class, which refused the twelve real session values the round-98 sentinel measured"*;
    2. `.ufo/waves/round-99/claims.json:25`: *"round-98 used a whitespace/quote/operator class, which refused the twelve real 64-hex session values the round-98 sentinel measured"*;
    3. `SCORECARD.md:3416`: *"the gitlab-session-cookie separator class refused the twelve real session values the round-98 sentinel measured (probe 0/12, two boundary negatives over-detected)"*;
    4. `.ufo/waves/round-99/c2/session-cookie-probe.py` K3: execution of the round-98 instrument against the 12 MUSTFIX payloads prints `mustfix_hit=0/12` (all 12 refused, 0 hit).
  - The phrase *"refuses eight of the twelve"* is a stale draft number that failed to track the final 12/12 MUSTFIX payload set.
- **Critical Second-Order Discovery on C1 (`depth:verifiability`)**:
  - Live execution of the exact frozen `--check` command (`python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <scratch>`) **currently FAILS with `rc=1` (`CENSUS-CHECK fail reason=body-mismatch rc=1`)**.
  - **Root Cause**: `census-at-rev.py:337` asserts `if body != mbody: return 1 ("body-mismatch")`. While the pinned rate (`skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76`) is completely stable and identical, `mbody` dynamically resolves host-owned external paths against the live host filesystem. The file `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` was cited at line 1490 and 1537; when the census was recorded at `a3db47e7`, `watchdog.log` had 3237 lines. During wave 1 execution, `watchdog.log` grew to 3238 lines. This single-line host log drift altered `mbody`'s line count column (`3237` -> `3238`), breaking `--check` on the landed commit.
- **UFO-FSD Connector Move**: Developed a bounded, cross-surface synthesis resolving (1) the live host file drift and extract-cache poisoning in `census-at-rev.py` (`depth:verifiability`), and (2) recovering Netscape/curl cookie-jar intake detection (+23 cells) via a bounded-whitespace union (`coverage`).

---

## 1. Sibling-Lane Overlap Scan

A comprehensive, read-only search across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/` was conducted for:
1. `census-at-rev`, `citation-survival`, `header-sha256`, `body-sha256`, and revision-bound citation censuses.
2. `_gitlab_session`, `gitlab-session-cookie`, `assignmentContext`, `assignment-context`, `gitlab.toml`, and the token shapes `glcbt-`, `gliamrt-`, `gliamac-`.
3. The source registration id `S150`.

Receipts: `sibling-scan-census.txt`, `sibling-scan-gitlab-tokens.txt`.

### 1.1 Revision-Bound Citation Census Scan

| Sibling Lane | Path:Line | Match Content | Classification | Overlap with Kasegi C1 |
|---|---|---|---|---|
| `tsukuroi-shokunin` | `.ufo/waves/round-47/w1-results.json:262` | `"declared_run": {"cmd": "python3 tools/score-census-identity-r46.py ...", ... "selftest_r46": ...}` (reports on `census-at-rev.sh`) | Historical test artifact | **Zero overlap**. References a round-47 shell development script testing OS systemd/package/driver states under a space TMPDIR. Disjoint domain. |
| `tsukuroi-shokunin` | `.ufo/waves/round-47/w1/C2ExecSelftest.md:48, 55` | `(source census-at-rev.sh:3473-3483...)` | Historical report citation | **Zero overlap**. Discusses system-state auditing under temporary directories. Disjoint domain. |
| `kotoba-shokunin` | `corpus/knowledge/sibling-citation-routing-round16.json:628, 2136` | `"token": "corpus/instruments/citation-survival.md"` | External routing pointer | **Zero overlap**. Historical routing index recording references across sibling repos; contains no census code or data. |
| `mori-shokunin` | `corpus/lessons/round-56.md:96` | `kasegi citation-survival records .ufo/watchdog.log GONE under a case-spelled path` | External citation | **Zero overlap**. Observational note discussing path casing; does not implement citation survival. |
| `kagi-shokunin` | `corpus/quote-locate.py:101` | `reason = "body-sha256-mismatch"` | Snapshot capture digest check | **Zero overlap**. Validates external URL source-snapshot HTML/text bodies against recorded sha256 sums in `SOURCES.md`. |
| `tabi-shokunin` | `corpus/evidence/w6-ver-b6/evidence/chain-repro.out:13, 27` | `body-sha256=cee3607e... body-bytes=308` | Benchmark response digest | **Zero overlap**. Records HTTP redirect chain response body hashes in automated browser testing. |
| All other 14 siblings | Full corpus regex sweep | 0 hits | Clean | **Zero overlap**. `census-at-rev.py` and `citation-survival.md` exist exclusively in `kasegi-shokunin`. |

### 1.2 GitLab Session-Cookie & Assignment-Context Shapes Scan

| Shape / Token Term | Sibling Lane Matches | Classification | Overlap with Kasegi C2 |
|---|---|---|---|
| `_gitlab_session` | 0 hits across 20 sibling corpora | Clean | **Zero overlap**. Does not exist outside `kasegi-shokunin`. |
| `gitlab-session-cookie` | 0 hits across 20 sibling corpora | Clean | **Zero overlap**. Does not exist outside `kasegi-shokunin`. |
| `assignmentContext` / `assignment-context` | 0 hits across 20 sibling corpora | Clean | **Zero overlap**. S150 generator semantics exist only in `kasegi-shokunin`. |
| `glcbt-`, `gliamrt-`, `gliamac-` | 0 hits across 20 sibling corpora | Clean | **Zero overlap**. GitLab token families exist only in `kasegi-shokunin`. |
| `gitlab.toml` | 0 hits across 20 sibling corpora | Clean | **Zero overlap**. Vendor ruleset capture exists only in `kasegi-shokunin`. |
| `session-cookie` (generic) | `kaidoku-shokunin` (`round-49.md:48, 56`, `round-50.md:52`) | Leaked HTTP header incident | **Zero overlap**. Notes unredacted GitHub session cookie headers in `f1.hdr` requiring operator purge. Not a scanner. |
| `session-cookie` (generic) | `mori-shokunin` (`corpus/evidence/sources-r32/S175.src:284`) | Curl man page source | **Zero overlap**. Documentation for curl's `-j, --junk-session-cookies` flag. |
| `session-cookie` (generic) | `tabi-shokunin` (`corpus/evidence/w9-tabi-b91/curl-control.sh:37`) | Cookie jar inspector | **Zero overlap**. Shell script evaluating Netscape cookie jar expiration timestamps. |

### 1.3 S150 Registry Allocation Scan

Every sibling lane defining `S150` uses it for a completely disjoint local domain document:
- `chousa-shokunin`: `corpus/SOURCES.md:160` — `pathlib` installed Python source (`/usr/lib/python3.14/pathlib/__init__.py`), `PurePath.parents`.
- `kama-shokunin`: `corpus/SOURCES.md:162` — `llama.cpp` `server-schema.cpp` line 101 (`top_n_sigma`).
- `kengaku-shokunin`: `corpus/SOURCES.md:165` — Terminal-Bench 2.0 `password-recovery/instruction.md`.
- `kotodama-shokunin`: `corpus/SOURCES.md:179` — Busnel & Classe 1976, *Whistled Languages*, Springer.
- `mado-shokunin`: `corpus/SOURCES.md:162` — ghostty `AppDelegate.swift` @ v1.3.1 (`setupSignals`).
- `mori-shokunin`: `corpus/SOURCES.md:156` — systemd v262 `OOMScoreAdjust=` manual page (`systemd.exec.xml`).
- `revenger-shokunin`: `corpus/SOURCES.md:165` — Microsoft published PDB/CodeView headers (`microsoft-pdb` README).
- `tabi-shokunin`: `corpus/SOURCES.md:164` — Node.js Crypto documentation (`nodejs.org/docs/latest-v24.x/api/crypto.html`).
- `tsukuroi-shokunin`: `corpus/SOURCES.md:156` — Linux v7.2 Documentation `vm.rst` (`vm.oom_kill_allocating_task`).
- `kagi`, `kaidoku`, `kake`, `kotoba`, `kumitate`, `lore`, `souji`, `tameshi`: `S150` unassigned.

### 1.4 Contested Scope Determination

**Contested scope: None.**  
No sibling repository implements, claims, or contests any portion of `kasegi`'s C1 revision-pinned citation census surface or C2 GitLab token/session scanning capability.

---

## 2. Kasegi Own-Corpus Audit & Discrepancies

### 2.1 The "8 vs 12" Session Values Discrepancy

In `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` lines 24-26, the text reads:
```markdown
- the assignment context is a *window*, not a separator list: the generator
  expands `assignmentContext` to `<keyword>.{0,8}[:=].{0,8}<value>` (S150), so
  `_gitlab_session => H`, `_gitlab_session%20=%20H`, `_gitlab_session,=H` and
  `_gitlab_session=cell--H` are all the shape. A matcher built on a
  whitespace/quote/operator class refuses eight of the twelve real session
  values the round-98 sentinel measured (round 99).
```

**Discrepancy**:
- Line 25 asserts: *"refuses eight of the twelve real session values"*.
- However, the round-98 whitespace/quote/operator regex `_GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[\s\"'=:;]+(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])"` was tested against all 12 MUSTFIX payloads from `SentinelShapes-receipts/final-checks.txt:15-26`:
  1. `ck-len-cookie-cell0` (`_gitlab_session=cell--<hex>`): MISSED (refused due to `cell--`)
  2. `ck-ruby-hash-rocket` (`_gitlab_session => <hex>`): MISSED (refused due to `>`)
  3. `ck-pct20-eq` (`_gitlab_session%20=%20<hex>`): MISSED (refused due to `%`)
  4. `ck-pct20-colon` (`_gitlab_session%20:%20<hex>`): MISSED (refused due to `%`)
  5. `ck-pct20-after-eq` (`_gitlab_session=%20<hex>`): MISSED (refused due to `%`)
  6. `ck-paren-eq` (`_gitlab_session(=<hex>)`): MISSED (refused due to `(`)
  7. `ck-paren-gap` (`_gitlab_session ( = ) <hex>`): MISSED (refused due to `(` and `)`)
  8. `ck-comma-eq` (`_gitlab_session,=<hex>`): MISSED (refused due to `,`)
  9. `ck-pipe-eq` (`_gitlab_session|=<hex>`): MISSED (refused due to `|`)
  10. `ck-plus-eq` (`_gitlab_session+=<hex>`): MISSED (refused due to `+`)
  11. `ck-rocket-nospace` (`_gitlab_session=> <hex>`): MISSED (refused due to `>`)
  12. `ck-geo-pct20` (`_gitlab_session_geo_<hex>%20=%20<hex>`): MISSED (refused due to `%`)
- Observed Hit Count: **`0 / 12` hits, `12 / 12` refused** (Receipt: `corpus-discrepancy-eight-vs-twelve.txt`).
- This matches `capture-secret-scan.py:196-197` (*"refused the twelve real session values"*), `.ufo/waves/round-99/claims.json:25` (*"refused the twelve real 64-hex session values"*), and `session-cookie-probe.py` K3 (*"prints `mustfix_hit=0/12`"*).
- **Finding**: Line 25 of `gitlab-iam-ci-build-and-session-token-shapes.md` is a stale sentence that must be corrected from *"refuses eight of the twelve"* to *"refuses all twelve"*.

### 2.2 Live Host Log Drift Breaking C1 `--check`

When evaluating the landed revision (`35e3ab60`) with a fresh scratch directory:
```bash
$ python3 -B corpus/instruments/census-at-rev.py \
    --lane . --check corpus/instruments/citation-survival.md --work /fast/scratch/hyaku/kasegi-r99/ConnectorOverlap/fresh_check
CENSUS-CHECK fail reason=body-mismatch rc=1
```
**Observation**: Return code is `1`, indicating failure!

**Diagnostic Tracing**:
- In `census-at-rev.py`:
  - `check()` loads `citation-survival.md`, verifies `measured-at` is an ancestor, verifies header digest (`ddad8766...`), verifies body digest against `body-sha256: 0375a382...` (PASS).
  - It runs `measure(..., cache_ok=False)` to generate fresh `rates` and `mbody`.
  - Pinned rate lines are compared:
    `file: pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2569/7624 = 33.70% | lane 2607/8026 = 32.48%`
    `rev : pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2569/7624 = 33.70% | lane 2607/8026 = 32.48%`
    Exact match! All 5 header lines match!
  - At line 337: `if body != mbody: print("CENSUS-CHECK fail reason=body-mismatch rc=1")`.
  - A unified diff between `body` and `mbody` reveals:
    ```diff
    @@ -174,8 +174,8 @@
     | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md:37` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md` | 37 | 87 | in range |
     | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md:32` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-40/kasegi.md` | 32 | 65 | in range |
     | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/kasegi.md:115` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/kasegi.md` | 115 | 128 | in range |
    -| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1490` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1490 | 3237 | in range |
    -| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1537` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1537 | 3237 | in range |
    +| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1490` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1490 | 3238 | in range |
    +| `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1537` | RESOLVES | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` | 1537 | 3238 | in range |
     | `/home/vgpnk/Projects/shokunin/CORPUS.md:101-104` | RESOLVES | `/home/vgpnk/Projects/shokunin/CORPUS.md` | 101-104 | 184 | in range |
    ```
- **Analysis**:
  - `resolve.py` resolves host-owned absolute citations (`/home/vgpnk/...`) against the live host filesystem.
  - The live `.ufo/watchdog.log` was 3237 lines long when `a3db47e7` was recorded.
  - As soon as a process on the workstation appended a single line to `watchdog.log` (bringing it to 3238 lines), the dynamic line-count column changed from `3237` to `3238`.
  - Because `check()` demands verbatim equality (`body == mbody`), **live host log activity breaks revision verification of a committed commit**.
  - This demonstrates that verbatim `body == mbody` comparison contradicts the claim of revision-stability whenever host-owned files exist in the corpus.

### 2.3 Extract Directory Cache Poisoning in `census-at-rev.py:extract()`

In `census-at-rev.py:extract()` lines 78-80:
```python
    d = os.path.join(work, "extract-" + rev[:12], "tree")
    if os.path.isfile(os.path.join(d, RESOLVE)):
        return d, None
```
- **Vulnerability**: `extract()` checks whether `corpus/instruments/resolve.py` exists in `<work>/extract-<rev12>/tree`. If so, it returns `d` immediately without executing `git archive` or verifying content integrity.
- **Exploitation**: An attacker who can write to `<work>` can plant a fabricated `resolve.py` that outputs arbitrary census counts and markdown. When `--check` runs with that `--work`, it executes the planted script under the verifier's interpreter (`subprocess.run([sys.executable, ...])`) and passes with `rc=0` (Receipt: `c1-extract-cache-poisoning.txt`).
- **Second-Order Effect**: Passing `cache_ok=False` to `measure()` bypasses the JSON cache under `<work>/cache/`, but does NOT bypass the extract cache under `<work>/extract-<rev12>/tree/`. This violates the claim that `--check` never reads unauthenticated cached measurements.

---

## 3. UFO-FSD Connector Move: Cross-Surface Synthesis

### 3.1 Evidence

1. **Intake Format Regression in C2 (`coverage`)**:
   - The round-99 landing replaced `[\s"'=:;]+` with S150's generator pattern `[^\n]{0,8}[:=][^\n]{0,8}`.
   - SentinelCookie audited 192 matrix cells and identified **23 regressions** against the round-98 scanner (`SentinelCookie.md:94-123`).
   - Specifically, standard Netscape/curl cookie jars (tab-separated: `.gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t<H64>`) and space-separated cookies have NO `:` or `=` operator. Round 98 detected them; round 99 misses them completely (`cli-checks.txt:111-114`).
   - S150's merge request generated code for assignment expressions in source code, but `capture-secret-scan.py` is an intake gate for *captured bounty evidence*, which frequently consists of exported browser cookie jars and HTTP header dumps.
   - SentinelCookie evaluated Candidate B (`remedy.py`):
     ```python
     B = re.compile(LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
                    rb"(?:[^\S\n\"'=:;]{1,8}|[^\n]{0,8}[:=][^\n]{0,8})" + TAIL)
     ```
     Candidate B achieves `mustfix=12/12 negatives=0/10`, recovers `jar-tab` and `jar-space`, and preserves all 10 boundary negatives without catastrophic backtracking (Receipt: `c2-candidate-b-verification.txt`).

2. **Verification Brittleness in C1 (`depth:verifiability`)**:
   - `census-at-rev.py:check()` demands `body == mbody`.
   - `mbody` embeds the current line count of live host files (e.g. `.ufo/watchdog.log`). A single log append on the host breaks `--check` with `body-mismatch rc=1`, even though all revision-pinned rates and internal extract citations are perfectly stable and verified.
   - Furthermore, `extract()` trusts existing directories in `--work`, creating a code-execution and spoofing bypass (ReviewC1Instrument F1).

### 3.2 Affected Axes

- **`depth:verifiability`** (lowest non-retired axis, score 4): Restores deterministic revision-stability to `--check` by eliminating false failures from live host log drift, and achieves true tamper-evidence by closing the extract-directory cache bypass.
- **`coverage`** (score 8 held): Recovers the 23 lost cookie-jar detection cells without introducing false positives on the 10 boundary negatives, ensuring capture intake hygiene covers real-world browser and curl artifacts.

### 3.3 Proposed Move

**Hermetic Archive Extraction, Host-Stat Masking, and Dual-Intake Session Boundary Synthesis**

1. **Hermetic Fresh Extraction in `census-at-rev.py:extract()`**:
   Update `extract()` to accept `fresh=False`. When `cache_ok=False` (as called by `--check`), pass `fresh=True` to wipe any pre-existing extract tree and unconditionally unpack from `git archive <rev>`:
   ```python
   def extract(lane, rev, work, fresh=False):
       d = os.path.join(work, "extract-" + rev[:12], "tree")
       if not fresh and os.path.isfile(os.path.join(d, RESOLVE)):
           return d, None
       shutil.rmtree(d, ignore_errors=True)
       os.makedirs(d)
       ...
   ```
   *Second-Order Effect*: Guarantees that `--check` never runs untrusted code or relies on leftover files in `--work`.

2. **Host-Owned Live Stat Masking in `census-at-rev.py:check()`**:
   In `check()`, when comparing `body` against `mbody`, normalize or mask dynamic line counts for `RESOLVES` rows that point outside the extract (host-owned rows):
   ```python
   def normalize_host_rows(text):
       # Mask live line counts on external host-owned RESOLVES rows
       return re.sub(r'(\| `[^`]+` \| RESOLVES \| `[^`]+` \| \d+ \|) \d+ (\| in range \|)',
                     r'\1 <masked> \2', text)

   if normalize_host_rows(body) != normalize_host_rows(mbody):
       print("CENSUS-CHECK fail reason=body-mismatch rc=1")
       return 1
   ```
   *Second-Order Effect*: The body is still strictly verified against hand-edits via `body-sha256` and all internal citation rows must match `mbody` verbatim. Only non-revision-stable host file line counts (such as `watchdog.log`) are normalized, making `--check` 100% revision-stable across time and host activity.

3. **Dual-Intake Session Boundary in `capture-secret-scan.py` (Candidate B)**:
   Update the `gitlab-session-cookie` pattern to SentinelCookie's Candidate B:
   ```python
   ("gitlab-session-cookie", re.compile(
       _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
       rb"(?:[^\S\n\"'=:;]{1,8}|[^\n]{0,8}[:=][^\n]{0,8})"
       rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),
   ```
   *Second-Order Effect*: Recovers detection of Netscape/curl cookie jars (tab and space separated) while maintaining strict S150 parity for code assignment expressions, hitting 12/12 MUSTFIX and 0/10 NEGATIVES.

4. **Harmonize Knowledge Entry**:
   Update line 25 of `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` from *"refuses eight of the twelve"* to *"refuses all twelve"*, restoring consistency across code, scorecard, and knowledge.

### 3.4 Risks & Mitigations

1. *Risk of masking internal citation tampering*:
   - *Mitigation*: The regex mask applies strictly to lines matching `\| RESOLVES \|` where the target path is outside the repository. All `INTERNAL` rows (which constitute the revision-stable numerator and denominator) remain strictly unmasked and checked verbatim.
2. *Risk of Candidate B introducing false positives on boundary negatives*:
   - *Mitigation*: Empirically verified against all 10 boundary negatives (including `n-gap-9`, `n-gap-newline`, and `n-left-word`); all 10 produce 0 hits (`c2-candidate-b-verification.txt`).
3. *Performance impact of fresh re-extraction*:
   - *Mitigation*: `git archive` and tar extraction of the repository take ~0.40s. Total `--check` runtime moves from 2.23s to ~2.65s, well within the 60s / 1 GiB threshold.

### 3.5 Verification

1. **Candidate B Verification** (`c2-candidate-b-verification.txt`):
   - `MUSTFIX`: 12/12 hits.
   - `NEGATIVES`: 0/10 hits.
   - `jar-tab` (`.gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t<hex>`): True.
   - `jar-space`: True.
2. **Hermetic Extraction Verification** (`c1-extract-cache-poisoning.txt`):
   - Wiping extract tree when `cache_ok=False` eliminates the planted `resolve.py` bypass and guarantees execution of committed code only.
3. **Host-Stat Masking Verification** (`c1-body-mismatch-live-watchdog-drift.txt`):
   - Normalizing live line counts on external `watchdog.log` rows allows `--check` to pass deterministically on the committed revision regardless of background log writes.

---

## Receipts Index & Hygiene

All supporting verification artifacts are preserved under `.ufo/waves/round-99/w1/ConnectorOverlap-receipts/`:

| Receipt File | SHA-256 Digest | Description |
|---|---|---|
| `sibling-scan-census.txt` | `b99e7ebc...` | Census and digest search results across all 20 sibling corpora |
| `sibling-scan-gitlab-tokens.txt` | `1da0119b...` | GitLab token shapes and S150 search results across 20 sibling corpora |
| `corpus-discrepancy-eight-vs-twelve.txt` | `4859f776...` | Empirical evidence of 12/12 MUSTFIX refusal vs knowledge line 25 "refuses eight" |
| `c1-body-mismatch-live-watchdog-drift.txt` | `d7f6ebca...` | Live reproduction of `watchdog.log` growth breaking `--check` with `body-mismatch rc=1` |
| `c1-extract-cache-poisoning.txt` | `05e94b26...` | Reproduction of extract directory cache poisoning in `census-at-rev.py` |
| `c2-candidate-b-verification.txt` | `8c642145...` | Execution proof of Candidate B (12/12 MUSTFIX, 0/10 NEGATIVES, cookie jars recovered) |
| `receipts-hygiene-scan.txt` | `c970428d...` | Output of `capture-secret-scan.py --files` over all receipts (0 hits, rc=0) |

A full hygiene scan with `python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-99/w1/ConnectorOverlap-receipts/*` confirmed **0 leaks, 0 hits across all receipt files** (`receipts-hygiene-scan.txt`).

---

## Verdicts

VERDICT: sibling-overlap-census — NONE  
VERDICT: sibling-overlap-gitlab-tokens — NONE  
VERDICT: contested-scope — NONE  
VERDICT: kasegi-corpus-session-cookie-separator — STALE-DISCREPANCY (corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:25 states "refuses eight of the twelve", contradicting capture-secret-scan.py:196 and claims.json:25 which state twelve, verified 0/12 by session-cookie-probe.py K3)  
VERDICT: depth:verifiability — UNSTABLE-ON-HOST-DRIFT (watchdog.log line growth 3237->3238 breaks frozen --check with body-mismatch rc=1; extract() trusts unauthenticated resolve.py in --work)  
VERDICT: coverage — REGRESSION-RECOVERABLE (23 cells lost by requiring [:=], recoverable via Candidate B bounded-whitespace union)  
VERDICT: connector-move — FEASIBLE (hermetic fresh extraction + host log masking + Candidate B recovers coverage and verifiability without regressions)  
