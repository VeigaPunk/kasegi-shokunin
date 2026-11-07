# ConnectorOverlap Report — Round 96 Wave 1

Seat: `ConnectorOverlap` (UFO-FSD connector, leaf member)  
Lane: `kasegi` (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`)  
Round: 96, Attempt 1 (ONE v1 wave of 13 seats)  
Declared Axes: `depth:verifiability` (lowest non-retired axis, score 4; tranche closure + control attribution), `coverage` (score 8 held; capability extension of capture-secret-scan)  
Base commit: `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`  
Freeze commit: `804e7bc344df0808c880815dde077c28be5db18a`  
C1 landing commit: `3c0581e2616df7a10af494a785b479d5e5293749`  
C2 landing commit: `7ef1d365eb523a83b2567342a6c0f585ab028ab0`  
Scratch root: `/fast/scratch/hyaku/kasegi-r96/ConnectorOverlap`  
Receipts directory: `.ufo/waves/round-96/w1/ConnectorOverlap-receipts/`

---

## Verdict

Verdict: STANDS. Both frozen claims (C1 and C2) independently re-derived with rc=0 across all limbs, controls, and attribution fixtures.

- **Sibling-overlap scan**: All 20 sibling repositories scanned across `/home/vgpnk/Projects/shokunin/*-shokunin`. Zero sibling lanes hold an instrument measuring citation resolution or knowledge-scope token rates (`knowledge-meter` / `abs_tokens` / `abs_nongone`), zero hold an implementation of GitLab's routable/versioned-routable shapes (`glpat-`, `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`), and zero ship single-defect limb-attribution fixtures for a citation counter.
- **Lane proposal audit (`considerthese/`)**: All 8 reflection files (`2026-10-19.md` through `2026-10-26.md`) audited. Zero unimplemented proposals in `considerthese/` touch round 96's C1 or C2 claims.
- **S140 & Province audit**: Zero sibling lanes cite S140 as GitLab's `gitlab.toml` or commit `59ada1f4`. The seven new GitLab shapes in `capture-secret-scan.py` serve as capture ingestion hygiene and claim-package validation gates in `kasegi`'s core domain (bounty research evidence), and do not belong to `kagi`'s province (secrets & vault ops).
- **Contested scope statement**: Contested scope: None. No sibling lane contests or implements the C1 Tranche 11 citation repair / knowledge-meter scope or the C2 GitLab routable/versioned secret-scan surface.

---

## 1. Sibling-Lane Overlap Scan

A comprehensive, read-only search across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/` was performed over their git-tracked trees, `corpus/instruments/`, `tools/`, `scripts/`, and `.ufo/waves/` paths for:
- (a) Citation resolution & knowledge-scope token rates: `knowledge-meter`, `repair-map.tsv`, `abs_tokens`, `abs_nongone`
- (b) GitLab token shapes: `glpat-`, `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`, `gitlab-pat-`, `gitlab-runner-auth`, `gitlab-deploy-token`, `gitlab-agent-token`, `gitlab-workspace-token`, `gitlab-pipeline-trigger`
- (c) Single-defect attribution fixtures: `single-defect`, `attribution`, `ATTRIBUTION pass`, `failing-limb`

Receipts: `sibling-gitgrep-knowledge-meter.txt`, `sibling-gitgrep-repair-map.txt`, `sibling-gitgrep-abs_tokens.txt`, `sibling-gitgrep-abs_nongone.txt`, `sibling-gitgrep-glrtr.txt`, `sibling-gitgrep-gldt.txt`, `sibling-gitgrep-glagent.txt`, `sibling-gitgrep-glwt.txt`, `sibling-gitgrep-glptt.txt`, `sibling-gitgrep-gitlab-pat.txt`, `sibling-gitgrep-gitlab-runner-auth.txt`, `sibling-gitgrep-gitlab-deploy-token.txt`, `sibling-gitgrep-gitlab-agent-token.txt`, `sibling-gitgrep-gitlab-workspace-token.txt`, `sibling-gitgrep-gitlab-pipeline-trigger.txt`, `sibling-grep-single-defect.txt`, `sibling-grep-attribution-tools.txt`, `sibling-gitgrep-single-defect.txt`, `sibling-gitgrep-attribution-pass.txt`, `sibling-gitgrep-failing-limb.txt`, `sibling-grep-glpat-clean.txt`.

### 1.1 Sibling Overlap Table

| Sibling | Path | What It Holds | Overlap with Kasegi C1/C2 |
|---|---|---|---|
| `kagi-shokunin` | `corpus/transcript-scan.sh:91`, `.ufo/waves/round-22` to `round-56` | Classic bare prefix checks (`'glpat-' 'npm_'`) in SQLite transcript hygiene script without length constraints, boundary discrimination, or versioned tail parsing. | **Zero overlap**. Bare prefix search in transcript text; does not model or implement the routable or versioned-routable GitLab shapes (`27-300` head, `2+7` or `2+2+7` tails, `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`). Zero overlap with C1. |
| `kama-shokunin` | `.ufo/waves/round-20/build/out/ConnectKagi/secret-shape-scan.py:45`, `.ufo/waves/round-35/w1/out/RevengerScope.md:67` | Loose lower-bound regexes (`(?<![A-Za-z0-9])(ghp_\|gho_\|...\|glpat-)([A-Za-z0-9_\-]{8,})`) in historical round artifacts. | **Zero overlap**. Unanchored lower-bound prefix scanner; does not implement versioned tails, runner partition tokens, or trigger shapes from S140. Zero overlap with C1. |
| `kotoba-shokunin` | `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:548884`, `.ufo/waves/round-82/build/Kb82E12Loader-omp-18.14.0-strings.txt:648504` | Static string dump from external `omp` binary v18.12.2 and v18.14.0 containing literal `["glpat-"]`. | **Zero overlap**. Third-party binary string dump only. |
| `kengaku-shokunin` | `.ufo/waves/round-52/w2/W2SentinelScope/report.md:60`, `.ufo/waves/round-78/w1/SentinelR78.md:179` | Broad sentinel regex list (`glpat-[A-Za-z0-9_-]{16,}`) checking workspace transcripts. | **Zero overlap**. Diagnostic scan pattern for bare 16+ character prefixes. Zero overlap with C1. |
| `chousa-shokunin` | `.ufo/waves/round-51/w2/R51W2SentFinal.md:18`, `tools/argv-witness.py:351` | Process argv trace attribution mechanism (`long_records`, `attribution`); sentinel bare prefix list. | **Zero overlap**. `argv-witness.py` traces process command-line arguments and kernel syscall witness records. Does not model secret shapes or citation resolution. |
| `kaidoku-shokunin` | `tools/round-50/selftest-r49-c2.py`, `tools/round-27/c2-xpin-check.py`, `tools/round-93/craft-citation-semantic.py` | (1) Single-defect selftest fixtures for `c2-mismatch.py` checking craft table atoms against `QUALITY.md` criteria; (2) Cross-pin evidence-ID attribution (`rea-agents 6.5.0 vs 6.7.0`); (3) Semantic craft citation linter. | **Disjoint domain**. Kaidoku's `selftest-r49-c2.py` tests that individual atom deletions in craft tables produce exactly one red cell in its internal validator. It does not test line-anchored path citation survival or knowledge-meter limbs. Zero overlap with C2. |
| `kake-shokunin` | `scripts/citation_lint.py`, `.ufo/waves/round-63/w1/SentinelFetchSecurity.md:70` | Git commit-hash hygiene gate over `{SCORECARD.md, LOG.md}`; sentinel bare prefix list. | **Zero overlap**. Commit object SHA validator; no token-level citation meter or GitLab secret pattern recognition. |
| `tsukuroi-shokunin` | `tools/check-section-citations.py` | Section-citation errata locator for bootloader documentation. | **Zero overlap**. Verifies section headings in markdown text; distinct domain. |
| `souji-shokunin` | `tools/souji-citation-reconcile.py`, `.ufo/waves/round-35/w1/SwarmSentinel35.md:24` | Test receipt value reconciler; sentinel bare prefix list. | **Zero overlap**. Reconciles test receipt numbers. |
| All 20 Sibling Lanes | `corpus/instruments/`, `tools/`, `.ufo/waves/` | Target patterns `glrtr-`, `gldt-`, `glagent-`, `glwt-`, `glptt-`, `knowledge-meter`, `repair-map.tsv`, `abs_tokens`, `abs_nongone`, `ATTRIBUTION pass`, `failing-limb`. | **Zero matches (0 hits)**. The S140 versioned/routable GitLab shapes, the `knowledge-meter.py` counter and repair map, and the 11 single-defect limb-attribution control fixtures exist exclusively in `kasegi-shokunin`. |

### 1.2 Contested Scope Determination

**Contested scope: None.**
No sibling repository implements or claims any portion of kasegi's round-96 C1 citation repair surface (Tranche 11 line repairs, prose-pointer M4 binding, 11 attribution fixtures) or C2 GitLab routable/versioned-routable secret-scan surface. The lane does not duplicate any sibling instrument and should not defer either capability.

---

## 2. Lane-Local Proposal Audit (`considerthese/`)

All 8 daily reflection files in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/` (`2026-10-19.md` through `2026-10-26.md`) were read and audited against round 96's claims:

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
All 47 proposals in `considerthese/` address historical concerns from rounds 18–35 (CNA Operational Rules 4.2.0, EU CRA Regulation 2024/2847 Article 14, `manifest.json` generation, anchorcheck regression testing, draft PR #1, wave receipt file bloat, and SHONEN box 2). None of the proposals addresses or implements C1 (Tranche 11 citation repairs, prose pointer M4 binding, 11 attribution fixtures) or C2 (GitLab secret scanner shapes from S140).

---

## 3. S140 and GitLab Rules File Citation Audit

### 3.1 Cross-Lane Citation Check for S140 and `gitlab.toml`
- S140 is defined in `kasegi-shokunin` as GitLab's `gitlab.toml` at commit `59ada1f4` under `corpus/source-snapshots/round-94/S140.txt`.
- A cross-lane search across all 20 sibling repositories for `gitlab.toml` and commit hash `59ada1f4` returned **zero hits (0 matches)**. Receipt: `sibling-grep-gitlab-rules.txt`.
- While `chousa-shokunin` contains an internal source labeled `S140`, it refers to a local Linux kernel `openat2` probe output (`openat2-probe.txt`) from round 62, completely disjoint from GitLab or secret scanning.

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
  python3 -B .ufo/waves/round-96/c1/knowledge-meter.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --base-rev d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6 \
    --after-rev 3c0581e2616df7a10af494a785b479d5e5293749 \
    --map .ufo/waves/round-96/c1/repair-map.tsv \
    --labels-rev 804e7bc344df0808c880815dde077c28be5db18a \
    --base-target 1030/2027 \
    --target 1032/2028 \
    --map-sha256 7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f \
    --work /fast/scratch/hyaku/kasegi-r96/ConnectorOverlap/c1-work
  ```
- **Observed Result**:
  - `KNOWLEDGE-METER base=1030/2027 after=1032/2028 base_target=1030/2027 target=1032/2028 sites=5 labels=5 after_rev=3c0581e2616df7a10af494a785b479d5e5293749 mirror_absent=True pinned=archive`
  - `HOST base abs_tokens=127 abs_nongone=23`
  - `HOST after abs_tokens=127 abs_nongone=23`
  - `LIMB M0 pass base=1030/2027`
  - `LIMB M1 pass after=1032/2028`
  - `LIMB M3 pass same_files=True bad_lines=0 old_not_once=0 dup_rows=0`
  - `LIMB M4 pass bad=none`
  - `LIMB M5 pass out_of_range=none`
  - `LIMB M9 pass rows=5 unbound=none`
  - `LIMB M10 pass labelled=5 want=5 mapped=5 kinds=part=4,range=1 unknown=none unapplied=none unlabelled=none`
  - `LIMB M6 pass sha256=7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f`
  - `KNOWLEDGE-METER-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c1-predicate-run.txt`

### 4.2 Claim C1 Controls & Attribution Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-96/controls/c1-controls-r96.py \
    /fast/scratch/hyaku/kasegi-r96/ConnectorOverlap/c1-landing-clone \
    804e7bc344df0808c880815dde077c28be5db18a \
    .ufo/waves/round-95/c1/knowledge-meter.py \
    /fast/scratch/hyaku/kasegi-r96/ConnectorOverlap/c1-ctl-work \
    /fast/scratch/hyaku/kasegi-r96/ConnectorOverlap/c1-ctl-out
  ```
- **Observed Result**:
  - Re-run against a clean checkout of C1 landing `3c0581e2616df7a10af494a785b479d5e5293749`.
  - Candidate control: `rc=0 want=0 PASS limbs=none declared=- attribution=PASS`
  - Do-nothing control: `rc=1 want=1 PASS limbs=M1,M3 declared=M1,M3 attribution=PASS`
  - Missing-labels control: `rc=2 want=2 PASS limbs=none declared=-`
  - Wrong-map-sha control: `rc=1 want=1 PASS limbs=M6 declared=M6 attribution=PASS`
  - Extra-unlisted-edit control: `rc=1 want=1 PASS limbs=M3 declared=M3 attribution=PASS`
  - R95-no-prose-branch control: `rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS`
  - Row-old-absent-only control: `rc=1 want=1 PASS limbs=M3 declared=M3 attribution=PASS`
  - Map-not-label control: `rc=1 want=1 PASS limbs=M9 declared=M9 attribution=PASS`
  - Snapshot-missing-only control: `rc=1 want=1 PASS limbs=M4,M5 declared=M4,M5 attribution=PASS`
  - Unknown-kind-row control: `rc=1 want=1 PASS limbs=M10 declared=M10 attribution=PASS`
  - Unlabelled-only control: `rc=1 want=1 PASS limbs=M10,M9 declared=M10,M9 attribution=PASS`
  - Unapplied-only control: `rc=1 want=1 PASS limbs=M10 declared=M10 attribution=PASS`
  - `ATTRIBUTION pass fixtures=11`
  - `C1-CONTROLS-RESULT pass controls=12`
  - Return code: `0`
- **Receipt**: `c1-controls-run.txt`

### 4.3 Claim C2 Re-derivation
- **Command**:
  ```bash
  python3 -B .ufo/waves/round-96/c2/capability-check.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --rev 7ef1d365eb523a83b2567342a6c0f585ab028ab0 \
    --work /fast/scratch/hyaku/kasegi-r96/ConnectorOverlap/c2-work \
    --instrument-sha256 71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9 \
    --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6
  ```
- **Observed Result**:
  - `CAPABILITY-CHECK-REV rev=7ef1d365eb523a83b2567342a6c0f585ab028ab0 seed=312480898`
  - `LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=128`
  - `LIMB K2 ok rc=0 scanned=2744 hits=0 allowed=27 unused_allow=0`
  - `LIMB K3 ok rc=1 hits=7 missing=none extra=none`
  - `LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none`
  - `LIMB K5 ok rows=1 last=87 named=True`
  - `LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential`
  - `CAPABILITY-CHECK-RESULT pass rc=0`
  - Return code: `0`
- **Receipt**: `c2-predicate-run.txt`

---

## 5. UFO-FSD Connector Move: Cross-Surface Synthesis

### 5.1 Evidence

1. **The Prose-Pointer M5 Verification Blindspot**:
   - In round 96, Claim C1 admitted prose-pointer `part` repairs (`(L1832-1833)` and `(L1834)` on `iso-29147-divergence-and-clause-crosswalk.md:36`) to fix off-by-one line citations pointing into `corpus/source-snapshots/round-30/S041.txt`.
   - To accept these non-backticked prose edits, `knowledge-meter.py:389-393` added an M4 branch:
     ```python
     if exp and exp[0] == "part" and not KEYFILE.match("`%s`" % key):
         if (old != key or new == old or PTR.sub("", old) != PTR.sub("", new)
                 or "`" in new):
             m4bad.append(tag)
         continue
     ```
   - **Contradiction**: Because this branch terminates with `continue`, the entire subsequent M5 range-checking loop (`lines 411-439`) is bypassed. The counter docstring asserts: *"every written value's anchor lies inside the entry (M5)"*. Yet `CriticClaimsC1` demonstrated in `06-prose-attacks.txt` that a mutant mutating `(L1834)` to `(L99999)` passes M4, M5, M9, M10 with `rc=0`, even though `S041.txt` has only 2,354 lines.
2. **Contextual Snapshot Disconnect**:
   - `resolve.py` only extracts backticked path-like tokens (e.g. `` `corpus/source-snapshots/round-30/S041.txt:1792-1867` ``). Inline prose pointers `(L1834)` carry no backticks and no file prefix, so they are invisible to `resolve.py`'s rate.
   - However, in `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`, lines 33–36 establish a local scope: line 33 explicitly cites `corpus/source-snapshots/round-30/S041.txt:1792-1867`, and line 36 lists sub-clauses a) through f) with their respective line ranges in that exact snapshot.
   - Currently, `knowledge-meter.py` has no mechanism to connect an inline prose pointer `(L1834)` to its enclosing section snapshot.
3. **Control Harness Coverage Gap**:
   - In `c1-controls-r96.py`, none of the 11 attribution fixtures tests an out-of-range prose pointer. The harness includes `snapshot-missing-only` and `r95-no-prose-branch`, but zero fixtures isolating M5 on prose pointers.

### 5.2 Affected Axes

- `depth:verifiability` (lowest non-retired axis, score 4): Closes the verification loophole where prose-pointer line numbers are unchecked strings that can point past EOF (`(L99999)`), elevating prose pointer repairs to the same verifiable standard as backticked line anchors.
- `coverage` (score 8 held): Bridges the gap between backticked citation metering (`resolve.py`) and granular prose line references, ensuring robust multi-tier evidence crosswalking.

### 5.3 Proposed Move

**Contextual Snapshot Anchoring and Range Verification for Prose Pointers in `knowledge-meter.py`:**

1. **Contextual Snapshot Resolution**:
   In `knowledge-meter.py`, when M4 encounters a prose pointer `part` row (`exp[0] == "part"` and `PTR.search(key)`), resolve the target snapshot by scanning preceding lines in `bfiles[rel]` up to the nearest section heading for a `corpus/source-snapshots/.../SNNN.txt` token. (Fallback to the entry's `source:` frontmatter header if no section snapshot exists).
2. **Enforce M5 Range Checks on Prose Pointers**:
   Remove the bare `continue` at `line 393`. Instead, extract `lo, hi` from `PTR.findall(new)`. Load the resolved snapshot from `A["tree"]`, determine `nlines = len(snapshot_text.splitlines())`, and verify:
   ```python
   if not (1 <= int(lo) <= (int(hi) if hi else int(lo)) <= nlines):
       m5bad.append(tag)
   ```
3. **Enforce Exact-Occurrence Line Binding**:
   Require `blines[n - 1].count(old) == 1` for prose pointer replacements in M3 to prevent occurrence bleed (e.g., preventing a replacement of `(L1835)` for item `e)` from also mutating item `f)`).
4. **Control Harness Isolation Fixture**:
   Add a 12th negative attribution fixture (`prose-pointer-out-of-range`) to `c1-controls-r96.py` that mutates `(L1834)` to `(L99999)` on line 36 of `iso-29147-divergence-and-clause-crosswalk.md` and asserts `limbs=M5 declared=M5 attribution=PASS`.

### 5.4 Risks & Mitigations

1. *Snapshot Resolution Ambiguity*:
   - *Risk*: A markdown file might cite multiple snapshots in one section.
   - *Mitigation*: Scan backwards strictly to the nearest line with a snapshot citation. In `iso-29147-divergence-and-clause-crosswalk.md`, line 33 is 3 lines above line 36 and uniquely specifies `S041.txt:1792-1867`.
2. *Performance Overhead*:
   - *Risk*: Reading and splitting snapshot texts on every row could slow down the meter.
   - *Mitigation*: Snapshot line counts are cached in memory by path during the run; cache lookup is $O(1)$.
3. *Non-line Parentheticals*:
   - *Risk*: Parenthetical text like `(RFC 2119)` or `(CVE-2026-...)` being misclassified.
   - *Mitigation*: Handled by `PTR = re.compile(r"\(L(\d+)(?:-(\d+))?\)")`, which strictly matches `(L...)` line pointers.

### 5.5 Verification

1. **Negative Fixture Verification**:
   In scratch, create a fixture with `iso-29147-divergence-and-clause-crosswalk.md:36` edited from `(L1834)` to `(L99999)`. Run `knowledge-meter.py` and assert:
   `LIMB M5 FAIL out_of_range=iso-29147-divergence-and-clause-crosswalk.md:36` and exit status `1`.
2. **Positive Landing Verification**:
   Run `knowledge-meter.py` against landing commit `3c0581e2616df7a10af494a785b479d5e5293749` and assert:
   `LIMB M4 pass bad=none`, `LIMB M5 pass out_of_range=none`, and `KNOWLEDGE-METER-RESULT pass rc=0`.
3. **Control Harness Pass**:
   Run `c1-controls-r96.py` and assert `ATTRIBUTION pass fixtures=12` and `C1-CONTROLS-RESULT pass controls=13`.

---

## Receipts

All command outputs cited in this report are preserved in `.ufo/waves/round-96/w1/ConnectorOverlap-receipts/`:

| Receipt File | Command / Test Executed | Observed RC | Output Summary |
|---|---|---|---|
| `c1-predicate-run.txt` | `python3 -B .ufo/waves/round-96/c1/knowledge-meter.py ...` | `rc=0` | All limbs M0–M10 pass; meter 1030/2027 -> 1032/2028. |
| `c1-controls-run.txt` | `python3 -B .ufo/waves/round-96/controls/c1-controls-r96.py ...` | `rc=0` | 12 controls PASS; ATTRIBUTION pass fixtures=11. |
| `c2-predicate-run.txt` | `python3 -B .ufo/waves/round-96/c2/capability-check.py ...` | `rc=0` | All limbs K1–K6 pass; cases=128; hits=7; seed=312480898. |
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
| `sibling-gitgrep-knowledge-meter.txt` | Sibling git-grep for `knowledge-meter` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-repair-map.txt` | Sibling git-grep for `repair-map.tsv` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-abs_tokens.txt` | Sibling git-grep for `abs_tokens` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-abs_nongone.txt` | Sibling git-grep for `abs_nongone` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-attribution-pass.txt` | Sibling git-grep for `ATTRIBUTION pass` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-failing-limb.txt` | Sibling git-grep for `failing-limb` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-gitgrep-single-defect.txt` | Sibling git-grep for `single-defect` across all 20 siblings | `rc=0` | 0 lines; 0 hits. |
| `sibling-grep-single-defect.txt` | Focused grep for `single-defect` in sibling tools | `rc=0` | 30 lines; `kaidoku-shokunin` round-50 craft atom selftest. |
| `sibling-grep-attribution-tools.txt` | Focused grep for `attribution` in sibling tools | `rc=0` | 240 lines; `kaidoku` cross-pin evidence ID, `chousa` argv witness. |
| `sibling-grep-gitlab-rules.txt` | Sibling git-grep for `gitlab.toml` and commit `59ada1f4` | `rc=0` | 0 lines; 0 hits. |
| `sibling-grep-glpat-clean.txt` | Clean git-tracked grep for `glpat-` across siblings | `rc=0` | 13 lines; bare prefix checks in 7 sibling lanes. |
| `considerthese-proposals.txt` | Extracted proposals from all 8 `considerthese/*.md` files | `rc=0` | 55 lines; 0 proposals touch C1 or C2. |
| `receipts-hygiene-scan.txt` | `capture-secret-scan.py --files ConnectorOverlap-receipts/*` | `rc=0` | 31 files scanned, 0 hits, 0 leaks. |
