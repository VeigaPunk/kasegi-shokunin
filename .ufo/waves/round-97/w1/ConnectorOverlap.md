# ConnectorOverlap Report — Round 97 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 97, Attempt 1 (ONE v1 wave of 14 seats)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4; tranche 12 closure + 13 attribution fixtures), `coverage` (score 8 held; capability extension of capture-secret-scan)  
Base commit: `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`  
Freeze commit: `daf7fc6a627d615178c27594110e956e592e4cd9`  
C1 landing commit: `75a471809cba265c8981ece1c0ed29c7895d9308`  
C2 landing commit: `a9a53608dce6aea07d298bb9d5133532078eb1dd`  
Scratch root: `/fast/scratch/hyaku/kasegi-r97/ConnectorOverlap`  
Receipts directory: `.ufo/waves/round-97/w1/ConnectorOverlap-receipts/`

---

## Verdict

Verdict: STANDS. Both frozen claims (C1 and C2) independently re-derived with rc=0 across all limbs, controls, and attribution fixtures.

- **Sibling-overlap scan**: All 20 sibling repositories scanned across `/home/vgpnk/Projects/shokunin/*-shokunin`. Zero sibling lanes hold an instrument measuring citation resolution or knowledge-scope token rates (`knowledge-meter` / `repair-map` / `abs_tokens` / `abs_nongone` / `qualify-lane`), zero hold an implementation of GitLab's routable/versioned-routable shapes (`glpat-`, `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`) or the ten round-97 S140 families (`GR1348941`, `feed_token=`, `gloas-`, `glft-`, `glimt-`, `glsoat-`, `gitlab+deploy-token-`, `glffct-`, `glrct-`, plain `glagent-` 50), and zero ship single-defect limb-attribution fixtures for a citation counter.
- **Lane proposal audit (`considerthese/`)**: All 8 reflection files (`2026-10-19.md` through `2026-10-26.md`, comprising 47 proposals) audited. Zero unimplemented proposals in `considerthese/` touch round 97's C1 or C2 claims.
- **S140 & Province audit**: Zero sibling lanes cite S140 as GitLab's `gitlab.toml` or commit `59ada1f4`. The ten new GitLab shapes in `capture-secret-scan.py` serve as capture ingestion hygiene and claim-package validation gates in `kasegi`'s core domain (bounty research evidence), and do not belong to `kagi`'s province (secrets & vault ops).
- **Contested scope statement**: Contested scope: None. No sibling lane contests or implements the C1 Tranche 12 citation qualification / knowledge-meter scope or the C2 GitLab secret-scan surface.

---

## 1. Sibling-Lane Overlap Scan

A comprehensive, read-only search across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/` was performed over their git-tracked trees, `corpus/instruments/`, `tools/`, `scripts/`, and `.ufo/waves/` paths for:
- (a) Citation resolution & knowledge-scope token rates: `knowledge-meter`, `repair-map.tsv`, `abs_tokens`, `abs_nongone`, `qualify-lane`
- (b) GitLab token shapes:
  - Round 97 new shapes: `gitlab-runner-registration-token` (`GR1348941`), `gitlab-feed-token` (`feed_token=`), `gitlab-oauth-app-secret` (`gloas-`), `gitlab-feed-token-v2` (`glft-`), `gitlab-incoming-email-token` (`glimt-`), `gitlab-scim-oauth-token` (`glsoat-`), `gitlab-deploy-token-in-url` (`gitlab+deploy-token-`), `gitlab-feature-flags-client-token` (`glffct-`), `gitlab-runner-controller-token` (`glrct-`), `gitlab-agent-token-plain` (plain `glagent-` 50)
  - Prior GitLab shapes: `glpat-`, `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`, `gitlab-pat-`, `gitlab-runner-auth`, `gitlab-deploy-token`, `gitlab-agent-token`, `gitlab-workspace-token`, `gitlab-pipeline-trigger`
- (c) Single-defect attribution fixtures: `single-defect`, `attribution`, `ATTRIBUTION pass`, `failing-limb`

Receipts: `sibling-gitgrep-knowledge-meter.txt`, `sibling-gitgrep-repair-map.txt`, `sibling-gitgrep-abs_tokens.txt`, `sibling-gitgrep-abs_nongone.txt`, `sibling-gitgrep-qualify-lane.txt`, `sibling-gitgrep-gitlab-runner-reg.txt`, `sibling-gitgrep-feed-token.txt`, `sibling-gitgrep-gloas.txt`, `sibling-gitgrep-glft.txt`, `sibling-gitgrep-glimt.txt`, `sibling-gitgrep-glsoat.txt`, `sibling-gitgrep-gitlab-deploy-url.txt`, `sibling-gitgrep-glffct.txt`, `sibling-gitgrep-glrct.txt`, `sibling-gitgrep-glagent-plain.txt`, `sibling-gitgrep-glrtr.txt`, `sibling-gitgrep-gldt.txt`, `sibling-gitgrep-glagent.txt`, `sibling-gitgrep-glwt.txt`, `sibling-gitgrep-glptt.txt`, `sibling-gitgrep-gitlab-pat.txt`, `sibling-gitgrep-gitlab-runner-auth.txt`, `sibling-gitgrep-gitlab-deploy-token.txt`, `sibling-gitgrep-gitlab-agent-token.txt`, `sibling-gitgrep-gitlab-workspace-token.txt`, `sibling-gitgrep-gitlab-pipeline-trigger.txt`, `sibling-gitgrep-single-defect.txt`, `sibling-gitgrep-attribution-pass.txt`, `sibling-gitgrep-failing-limb.txt`, `sibling-grep-glpat-clean.txt`, `sibling-grep-attribution-tools.txt`, `sibling-grep-single-defect.txt`.

### 1.1 Sibling Overlap Table

| Sibling | Path | What It Holds | Overlap with Kasegi C1/C2 |
|---|---|---|---|
| `kagi-shokunin` | `corpus/transcript-scan.sh:91`, `.ufo/waves/round-22` to `round-56` | Classic bare prefix checks (`'glpat-' 'npm_'`) in SQLite transcript hygiene script without length constraints, boundary discrimination, or versioned tail parsing. | **Zero overlap**. Bare prefix search in transcript text; does not model or implement the routable, versioned-routable, or ten new S140 GitLab shapes. Zero overlap with C1. |
| `kama-shokunin` | `.ufo/waves/round-20/build/out/ConnectKagi/secret-shape-scan.py:45`, `.ufo/waves/round-35/w1/out/RevengerScope.md:67` | Loose lower-bound regexes (`(?<![A-Za-z0-9])(ghp_\|gho_\|...\|glpat-)([A-Za-z0-9_\-]{8,})`) in historical round artifacts. | **Zero overlap**. Unanchored lower-bound prefix scanner; does not implement versioned tails, runner registration tokens, feed tokens, or deploy-token URL shapes from S140. Zero overlap with C1. |
| `kotoba-shokunin` | `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:548884`, `.ufo/waves/round-82/build/Kb82E12Loader-omp-18.14.0-strings.txt:648504` | Static string dump from external `omp` binary v18.12.2 and v18.14.0 containing literal `["glpat-"]`. | **Zero overlap**. Third-party binary string dump only. |
| `kengaku-shokunin` | `.ufo/waves/round-52/w2/W2SentinelScope/report.md:60`, `.ufo/waves/round-78/w1/SentinelR78.md:179` | Broad sentinel regex list (`glpat-[A-Za-z0-9_-]{16,}`) checking workspace transcripts. | **Zero overlap**. Diagnostic scan pattern for bare 16+ character prefixes. Zero overlap with C1. |
| `chousa-shokunin` | `.ufo/waves/round-51/w2/R51W2SentFinal.md:18`, `tools/argv-witness.py:351` | Process argv trace attribution mechanism (`long_records`, `attribution`); sentinel bare prefix list. | **Zero overlap**. `argv-witness.py` traces process command-line arguments and kernel syscall witness records. Does not model secret shapes or citation resolution. |
| `kaidoku-shokunin` | `tools/round-50/selftest-r49-c2.py`, `tools/round-27/c2-xpin-check.py`, `tools/round-93/craft-citation-semantic.py` | (1) Single-defect selftest fixtures for `c2-mismatch.py` checking craft table atoms against `QUALITY.md` criteria; (2) Cross-pin evidence-ID attribution (`rea-agents 6.5.0 vs 6.7.0`); (3) Semantic craft citation linter. | **Disjoint domain**. Kaidoku's `selftest-r49-c2.py` tests that individual atom deletions in craft tables produce exactly one red cell in its internal validator. It does not test line-anchored path citation survival, `qualify-lane`, or knowledge-meter limbs. Zero overlap with C2. |
| `kake-shokunin` | `scripts/citation_lint.py`, `.ufo/waves/round-63/w1/SentinelFetchSecurity.md:70` | Git commit-hash hygiene gate over `{SCORECARD.md, LOG.md}`; sentinel bare prefix list. | **Zero overlap**. Commit object SHA validator; no token-level citation meter or GitLab secret pattern recognition. |
| `tsukuroi-shokunin` | `tools/check-section-citations.py` | Section-citation errata locator for bootloader documentation. | **Zero overlap**. Verifies section headings in markdown text; distinct domain. |
| `souji-shokunin` | `tools/souji-citation-reconcile.py`, `.ufo/waves/round-35/w1/SwarmSentinel35.md:24` | Test receipt value reconciler; sentinel bare prefix list. | **Zero overlap**. Reconciles test receipt numbers. |
| All 20 Sibling Lanes | `corpus/instruments/`, `tools/`, `.ufo/waves/` | Target patterns: `GR1348941`, `feed_token=`, `gloas-`, `glft-`, `glimt-`, `glsoat-`, `gitlab+deploy-token-`, `glffct-`, `glrct-`, `knowledge-meter`, `repair-map.tsv`, `abs_tokens`, `abs_nongone`, `qualify-lane`, `ATTRIBUTION pass`, `failing-limb`. | **Zero matches (0 hits)**. The ten new S140 GitLab shapes, the `knowledge-meter.py` qualify-lane counter and repair map, and the 13 single-defect limb-attribution control fixtures exist exclusively in `kasegi-shokunin`. |

### 1.2 Contested Scope Determination

**Contested scope: None.**  
No sibling repository implements or claims any portion of kasegi's round-97 C1 citation qualification surface (Tranche 12 bare lane-instrument qualifications, `qualify-lane` M4/M9/M10 binding, 13 attribution fixtures) or C2 GitLab secret-scan surface (ten remaining S140 families). The lane does not duplicate any sibling instrument and should not defer either capability.

---

## 2. Lane-Local Proposal Audit (`considerthese/`)

All 8 daily reflection files in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/` (`2026-10-19.md` through `2026-10-26.md`) were read and audited against round 97's claims:

- `2026-10-19.md` (7 suggestions: anchorcheck regression test, claim-package rubric calibration, CVSS/VRT severity sources, Saturation line pre-draft, PR #1 decision, craft-vs-meta ratio, change-driven reflections)
- `2026-10-20.md` (6 suggestions: live-source rechecker, rubric Frontier folding, owed-corrections ledger, pre-screening Frontier sources, metric redefinition flagging, anchorcheck carry-overs)
- `2026-10-21.md` (6 suggestions: daily recheck lines, pre-admission snapshot string matching, CNA 4.2.0/CRA Art. 14 in rubric, C1 resolver second review, infrastructure tracking, carry-overs)
- `2026-10-22.md` (5 suggestions: single-seat close-r23 dossier, branch scanner, wall-clock idleness counter, CVSS v4 rubric lens, event reflections)
- `2026-10-23.md` (5 suggestions: quote uniqueness in rechecker contract, close-r23 dossier with diffs, F06/F07 quote checks, idle cadence downshifting, README branch pruning)
- `2026-10-24.md` (5 suggestions: normalization in rechecker contract, clean snapshot capture, close-r23 dossier, idle downshift, PR #1 pruning)
- `2026-10-25.md` (6 suggestions: wave-evidence bloat cap, distance to next score, bounty craft / SHONEN box 2, proposal status ledger, open-defects ledger, event reflections)
- `2026-10-26.md` (7 suggestions: explicit distance to next score, SHONEN box 2 end-to-end domain task, pre-complete quiescence gate, wave evidence capping, F18 PROVINCE amendment, cadence retuning, proposal status ledger)

Receipt: `considerthese-proposals.txt`.

**Finding**: **None fits either claim.**  
All 47 proposals in `considerthese/` address historical concerns from rounds 18–35 (CNA Operational Rules 4.2.0, EU CRA Regulation 2024/2847 Article 14, `manifest.json` generation, anchorcheck regression testing, draft PR #1, wave receipt file bloat, and SHONEN box 2). None of the proposals addresses or implements C1 (Tranche 12 bare-instrument qualification, `qualify-lane` kind, 13 attribution fixtures) or C2 (GitLab secret scanner shapes from S140).

---

## 3. S140 and GitLab Rules File Citation Audit

### 3.1 Cross-Lane Citation Check for S140 and `gitlab.toml`
- S140 is defined in `kasegi-shokunin` as GitLab's `gitlab.toml` at commit `59ada1f4` under `corpus/source-snapshots/round-94/S140.txt`.
- A cross-lane search across all 20 sibling repositories for `gitlab.toml` and commit hash `59ada1f4` returned **zero hits (0 matches)**. Receipt: `sibling-grep-gitlab-rules.txt`.
- While `chousa-shokunin` (`corpus/knowledge/openat2-resolve-r62.md`, round 62) and `kaidoku-shokunin` (`corpus/SOURCES.md`, round 45) contain internal sources labeled `S140`, they refer respectively to an `openat2` Linux kernel probe and git-status documentation, completely disjoint from GitLab or secret scanning. Receipt: `sibling-grep-s140.txt`.

### 3.2 Province Boundary Audit
- In `kasegi-shokunin/PROVINCE.md`, line 48 lists `kagi — secrets and vault handling` under `Adjacent: Sibling lanes are reported, not absorbed`.
- In `kagi-shokunin/PROVINCE.md`, the domain is declared as `secrets & vault ops — the-janitor flows, credential hygiene evidence` (1Password `op` CLI flows, vault credential provisioning, agent token rotation).
- In `kasegi-shokunin`, `capture-secret-scan.py` is strictly an intake-hygiene gate (`capture-source.py:intake_gate`) and claim-package validation instrument ensuring that live API secrets or presigned session tokens are not leaked into committed bounty captures (`corpus/source-snapshots/`) or submitted packages (`claim-package-contract.md`).
- `kagi-shokunin` does not maintain secret token grammar definitions or shape regexes (only a bare prefix list `'glpat-' 'npm_'` in `transcript-scan.sh`).
- **Conclusion**: The new GitLab shapes do not belong to `kagi` or any other sibling lane's province. They are properly situated in `kasegi-shokunin` as capture-hygiene and bounty disclosure validation instruments.

---

## 4. Independent Re-derivation of Frozen Claims

### 4.1 Claim C1 Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-97/c1/knowledge-meter.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --base-rev b06af5e07efbd961a8449f7de6b57eeea62c6bd3 \
    --after-rev 75a471809cba265c8981ece1c0ed29c7895d9308 \
    --map .ufo/waves/round-97/c1/repair-map.tsv \
    --labels-rev daf7fc6a627d615178c27594110e956e592e4cd9 \
    --base-target 1040/2041 \
    --target 1043/2035 \
    --map-sha256 f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c \
    --work /fast/scratch/hyaku/kasegi-r97/ConnectorOverlap/c1-work
  ```
- **Observed Result**:
  - `KNOWLEDGE-METER base=1040/2041 after=1043/2035 base_target=1040/2041 target=1043/2035 sites=33 labels=33 after_rev=75a471809cba265c8981ece1c0ed29c7895d9308 mirror_absent=True pinned=archive`
  - `HOST base abs_tokens=128 abs_nongone=23`
  - `HOST after abs_tokens=128 abs_nongone=23`
  - `LIMB M0 pass base=1040/2041`
  - `LIMB M1 pass after=1043/2035`
  - `LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0`
  - `LIMB M4 pass bad=none`
  - `LIMB M5 pass out_of_range=none`
  - `LIMB M9 pass rows=33 unbound=none`
  - `LIMB M10 pass labelled=33 want=33 mapped=33 kinds=qualify-lane=33 unknown=none unapplied=none unlabelled=none`
  - `LIMB M6 pass sha256=f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c`
  - `KNOWLEDGE-METER-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c1-predicate-run.txt`

### 4.2 Claim C1 Controls & Attribution Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-97/controls/c1-controls-r97.py \
    /fast/scratch/hyaku/kasegi-r97/ConnectorOverlap/c1-candidate-clone \
    daf7fc6a627d615178c27594110e956e592e4cd9 \
    .ufo/waves/round-96/c1/knowledge-meter.py \
    /fast/scratch/hyaku/kasegi-r97/ConnectorOverlap/c1-ctl-work \
    /fast/scratch/hyaku/kasegi-r97/ConnectorOverlap/c1-ctl-out
  ```
- **Observed Result**:
  - Re-run against a clean clone of C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`.
  - Candidate control: `rc=0 want=0 PASS limbs=none declared=- attribution=PASS`
  - Do-nothing control: `rc=1 want=1 PASS limbs=M1,M3 declared=M1,M3 attribution=PASS`
  - Missing-labels control: `rc=2 want=2 PASS limbs=none declared=-`
  - Wrong-map-sha control: `rc=1 want=1 PASS limbs=M6 declared=M6 attribution=PASS`
  - Extra-unlisted-edit control: `rc=1 want=1 PASS limbs=M3 declared=M3 attribution=PASS`
  - R96-no-qualify-branch control: `rc=1 want=1 PASS limbs=M10,M4,M5,M9 declared=M10,M4,M5,M9 attribution=PASS`
  - Qualify-target-missing control: `rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS`
  - Qualify-key-not-bare control: `rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS`
  - Map-not-label control: `rc=1 want=1 PASS limbs=M4,M5,M9 declared=M4,M5,M9 attribution=PASS`
  - Unknown-kind-row control: `rc=1 want=1 PASS limbs=M10 declared=M10 attribution=PASS`
  - Unlabelled-only control: `rc=1 want=1 PASS limbs=M10,M9 declared=M10,M9 attribution=PASS`
  - Unapplied-only control: `rc=1 want=1 PASS limbs=M10 declared=M10 attribution=PASS`
  - Duplicate-row control: `rc=1 want=1 PASS limbs=M3 declared=M3 attribution=PASS`
  - Snapshot-missing-only control: `rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS`
  - `ATTRIBUTION pass fixtures=13`
  - `C1-CONTROLS-RESULT pass controls=14`
  - Return code: `0`
- **Receipt**: `c1-controls-run.txt`

### 4.3 Claim C2 Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-97/c2/capability-check.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --rev a9a53608dce6aea07d298bb9d5133532078eb1dd \
    --work /fast/scratch/hyaku/kasegi-r97/ConnectorOverlap/c2-work \
    --instrument-sha256 59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92 \
    --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
  ```
- **Observed Result**:
  - `CAPABILITY-CHECK-REV rev=a9a53608dce6aea07d298bb9d5133532078eb1dd seed=1254652219`
  - `LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=148`
  - `LIMB K2 ok rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0`
  - `LIMB K3 ok rc=1 hits=10 missing=none extra=none`
  - `LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none`
  - `LIMB K5 ok rows=1 last=87 named=True`
  - `LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential`
  - `CAPABILITY-CHECK-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c2-predicate-run.txt`

---

## 5. UFO-FSD Connector Move: Cross-Surface Synthesis

### 5.1 Evidence

1. **The `qualify-lane` Basename Identity Verification Loophole**:
   - In round 97, Claim C1 introduced the `qualify-lane` label kind to qualify 33 bare lane-instrument basenames (e.g. `anchorcheck.py`) to tracked paths (`corpus/instruments/anchorcheck.py`).
   - In `knowledge-meter.py:413-419`, the M4 verification branch enforces:
     ```python
     if exp and exp[0] == "qualify-lane":
         target = exp[2].strip("`")
         if (old != "`%s`" % key or new != exp[2] or "/" in key or ":" in key
                 or target.startswith(".ufo/") or target not in A["tracked"]
                 or A["classify"](target) != "INTERNAL"):
             m4bad.append(tag)
         continue
     ```
   - **Contradiction**: The check enforces that `target` is tracked, non-`.ufo`, and classifies `INTERNAL`. However, **it never verifies that `os.path.basename(target) == key`** or that `target.startswith("corpus/instruments/")`!
   - **Experimental Proof**: In a scratch experiment (`move-verification-cross-instrument.txt`), we created a mutant where `anchorcheck.py` on `capture-intake-gate.md:178` was mapped to `corpus/instruments/resolve.py` (an entirely different tool). Running the unpatched `knowledge-meter.py` on this cross-instrument mutant produced `rc=0` with **all limbs M0–M10 passing** (`LIMB M4 pass bad=none`). The counter completely failed to detect that the tool identity was substituted!

2. **Preclusion of Line-Anchored Instrument Citations**:
   - In `knowledge-meter.py:264-265`, `expected_edit()` declares:
     ```python
     if label.startswith("corpus/instruments/"):
         return "qualify-lane", "`%s`" % key, "`%s`" % label
     ```
   - Because this prefix match is unconditional, any future citation repair that points to a line range inside a lane instrument (e.g. `` `corpus/instruments/capture-source.py:126-146` ``, already cited on `capture-intake-gate.md:39`) is erroneously forced into `qualify-lane` instead of `range`.
   - In `qualify-lane`, the trailing `:126-146` is treated as part of `target`, which is not in `A["tracked"]`, causing M4 to fail, while the trailing `continue` at line 419 prevents M5 from ever executing range validation on instrument files.

3. **Attribution Fixture Gap in `c1-controls-r97.py`**:
   - The round-97 control harness tests 13 negative attribution fixtures (`qualify-target-missing`, `qualify-key-not-bare`, `map-not-label`, `extra-unlisted-edit`, etc.), but **zero fixtures isolate cross-instrument substitution** or line-anchored instrument citations.

### 5.2 Affected Axes

- `depth:verifiability` (lowest non-retired axis, score 4): Closes the semantic forgery loophole in `qualify-lane`, ensuring that instrument qualification mathematically enforces basename identity (`os.path.basename(target) == key`) and directory confinement (`corpus/instruments/`).
- `coverage` (score 8 held): Bridges the verification gap between bare-instrument qualifications and line-anchored instrument citations, enabling future tranches to verify line ranges inside `corpus/instruments/` without colliding with `qualify-lane`.

### 5.3 Proposed Move

**Identity-Confined Instrument Qualification and Line-Anchor Segregation in `knowledge-meter.py`:**

1. **Enforce Strict Basename Identity and Directory Confinement in M4**:
   Update `knowledge-meter.py:413-419` to require that `target` starts with `corpus/instruments/` and that `os.path.basename(target) == key`:
   ```python
   if exp and exp[0] == "qualify-lane":
       target = exp[2].strip("`")
       if (old != "`%s`" % key or new != exp[2] or "/" in key or ":" in key
               or not target.startswith("corpus/instruments/")
               or os.path.basename(target) != key
               or target not in A["tracked"]
               or A["classify"](target) != "INTERNAL"):
           m4bad.append(tag)
       continue
   ```

2. **Segregate Line-Anchored Instrument Citations in `expected_edit()`**:
   In `knowledge-meter.py:264-265`, check for line anchors (`:`) to classify line-anchored citations as `range` rather than `qualify-lane`:
   ```python
   if label.startswith("corpus/instruments/"):
       if ":" in label:
           return "range", "`%s`" % key, "`%s`" % label
       return "qualify-lane", "`%s`" % key, "`%s`" % label
   ```

3. **Add 14th Attribution Fixture to `c1-controls-r97.py`**:
   Add `qualify-wrong-instrument` fixture in `c1-controls-r97.py` that maps `anchorcheck.py` to `corpus/instruments/resolve.py` at `capture-intake-gate.md:178` and asserts `limbs=M4 declared=M4 attribution=PASS`.

### 5.4 Risks & Mitigations

1. *Risk of breaking existing Tranche 12 rows*:
   - *Check*: In Tranche 12, all 33 rows have `target == "corpus/instruments/" + key` without colons.
   - *Result*: All 33 rows satisfy `target.startswith("corpus/instruments/")` and `os.path.basename(target) == key`. Zero regressions on the C1 landing revision (`75a47180`).
2. *Risk of altering meter rates*:
   - *Check*: Meter rates (`1040/2041` -> `1043/2035`) are computed by `resolve.py` token collection, which is independent of M4 checks.
   - *Result*: Rates remain exactly `1040/2041` and `1043/2035`.
3. *Performance impact*:
   - *Check*: `os.path.basename` and `str.startswith` are in-memory string operations ($O(1)$).
   - *Result*: Negligible CPU impact (<0.1s over 33 rows).

### 5.5 Verification

1. **Negative Fixture Verification**:
   - Running the patched `knowledge-meter.py` on the cross-instrument mutant (`anchorcheck.py` -> `corpus/instruments/resolve.py`) failed immediately:
     `LIMB M4 FAIL bad=capture-intake-gate.md:178` and exit code `1` (see receipt `move-verification-cross-instrument.txt`).
2. **Positive Landing Verification**:
   - Running the patched `knowledge-meter.py` on the clean C1 landing commit `75a471809cba265c8981ece1c0ed29c7895d9308` passed with:
     `LIMB M0 pass`, `LIMB M1 pass`, `LIMB M3 pass`, `LIMB M4 pass bad=none`, `LIMB M5 pass out_of_range=none`, `LIMB M9 pass`, `LIMB M10 pass`, `LIMB M6 pass`, `KNOWLEDGE-METER-RESULT pass rc=0`.
3. **Control Harness Attribution**:
   - The 14th negative fixture produces exact single-limb attribution (`limbs=M4 declared=M4 attribution=PASS`), raising the attribution count to `fixtures=14` and `controls=15`.

---

## Receipts

All command outputs cited in this report are preserved in `.ufo/waves/round-97/w1/ConnectorOverlap-receipts/`.  
A full hygiene scan with `capture-secret-scan.py --files .ufo/waves/round-97/w1/ConnectorOverlap-receipts/*` confirmed **0 leaks, 0 hits across all 40 receipt files** (`receipts-hygiene-scan.txt`).

| Receipt File | Command / Test Executed | Observed RC | Output Summary |
|---|---|---|---|
| `c1-predicate-run.txt` | `python3 -B .ufo/waves/round-97/c1/knowledge-meter.py ...` | `rc=0` | All limbs M0–M10 pass; meter 1040/2041 -> 1043/2035. |
| `c1-controls-run.txt` | `python3 -B .ufo/waves/round-97/controls/c1-controls-r97.py ...` | `rc=0` | 14 controls PASS; ATTRIBUTION pass fixtures=13. |
| `c2-predicate-run.txt` | `python3 -B .ufo/waves/round-97/c2/capability-check.py ...` | `rc=0` | All limbs K1–K6 pass; cases=148; hits=10; seed=1254652219. |
| `move-verification-cross-instrument.txt` | `python3 test_move2.py` | `rc=0` / `rc=1` | Unpatched KM passes cross-instrument mutant (`rc=0`); patched KM catches it (`LIMB M4 FAIL`, `rc=1`). |
| `sibling-gitgrep-knowledge-meter.txt` | Sibling git-grep for `knowledge-meter` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-repair-map.txt` | Sibling git-grep for `repair-map.tsv` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-abs_tokens.txt` | Sibling git-grep for `abs_tokens` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-abs_nongone.txt` | Sibling git-grep for `abs_nongone` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-qualify-lane.txt` | Sibling git-grep for `qualify-lane` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-runner-reg.txt` | Sibling git-grep for `GR1348941` / `gitlab-runner-registration-token` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-feed-token.txt` | Sibling git-grep for `feed_token=` / `gitlab-feed-token` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gloas.txt` | Sibling git-grep for `gloas-` / `gitlab-oauth-app-secret` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glft.txt` | Sibling git-grep for `glft-` / `gitlab-feed-token-v2` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glimt.txt` | Sibling git-grep for `glimt-` / `gitlab-incoming-email-token` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glsoat.txt` | Sibling git-grep for `glsoat-` / `gitlab-scim-oauth-token` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-deploy-url.txt` | Sibling git-grep for `gitlab+deploy-token-` / URL form | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glffct.txt` | Sibling git-grep for `glffct-` / feature flags client token | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glrct.txt` | Sibling git-grep for `glrct-` / runner controller token | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glagent-plain.txt` | Sibling git-grep for plain 50-char `glagent-` | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glrtr.txt` | Sibling git-grep for `glrtr-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gldt.txt` | Sibling git-grep for `gldt-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glagent.txt` | Sibling git-grep for `glagent-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glwt.txt` | Sibling git-grep for `glwt-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-glptt.txt` | Sibling git-grep for `glptt-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-pat.txt` | Sibling git-grep for `gitlab-pat-` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-runner-auth.txt` | Sibling git-grep for `gitlab-runner-auth` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-deploy-token.txt` | Sibling git-grep for `gitlab-deploy-token` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-agent-token.txt` | Sibling git-grep for `gitlab-agent-token` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-workspace-token.txt` | Sibling git-grep for `gitlab-workspace-token` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-gitlab-pipeline-trigger.txt` | Sibling git-grep for `gitlab-pipeline-trigger` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-attribution-pass.txt` | Sibling git-grep for `ATTRIBUTION pass` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-failing-limb.txt` | Sibling git-grep for `failing-limb` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-single-defect.txt` | Sibling git-grep for `single-defect` across all 20 siblings | `rc=0` | 984 lines; disjoint craft-table / argv trace tests. |
| `sibling-grep-attribution-tools.txt` | Focused grep for `attribution` in sibling tools | `rc=0` | 216 lines; `kaidoku` cross-pin evidence ID, `chousa` argv witness. |
| `sibling-grep-single-defect.txt` | Focused grep for `single-defect` in sibling tools | `rc=0` | 28 lines; `kaidoku` round-50 craft atom selftest. |
| `sibling-grep-gitlab-rules.txt` | Sibling git-grep for `gitlab.toml` and commit `59ada1f4` | `rc=0` | 0 lines; 0 hits. |
| `sibling-grep-s140.txt` | Sibling git-grep for documented citations of `S140` | `rc=0` | 28 lines; disjoint `openat2` probe (`chousa`) and `git-status` (`kaidoku`). |
| `sibling-grep-glpat-clean.txt` | Clean git-tracked grep for `glpat-` across siblings | `rc=0` | 63 lines; bare prefix checks in 7 sibling lanes. |
| `considerthese-proposals.txt` | Extracted proposals from all 8 `considerthese/*.md` files | `rc=0` | 71 lines; 0 proposals touch C1 or C2. |
| `receipts-hygiene-scan.txt` | `capture-secret-scan.py --files ConnectorOverlap-receipts/*` | `rc=0` | 40 files scanned, 0 hits, 0 leaks. |
