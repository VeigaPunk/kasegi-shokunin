# ConnectorOverlap — round 91, attempt 1: cross-claim & sibling-overlap scan

Seat: ConnectorOverlap (UFO-FSD connector, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`; freeze `53ab692a7b544c35141e2b19f7413cbdb767c1ad`;
C1 landing `8a1a00c639ba808a701d1f186aac9ebd0045deaa`; C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`;
landing receipts `bcbfbde63b83c9336e845001323b5c92419e526a`.
Wave: kasegi-r91-w1 (ONE v1 wave of 13 seats; L1 KasegiR91 holds planner seat).
Declared axes: **depth:verifiability** (score 4; citation repair, score not claimed to move) and **coverage** (score 8 held).
Receipts: `.ufo/waves/round-91/w1/ConnectorOverlap-receipts/`.

---

## 1. Sibling-lane scan (/home/vgpnk/Projects/shokunin/*-shokunin)

Searched 20 sibling lane repositories (read-only, no git writes, no sibling file modifications).
Search patterns: `X-Amz-Security-Token`, `Signature=`, `sig=`, `CloudFront`, `secret-scan`, `snapshot`, `capture`.
Receipt: `ConnectorOverlap-receipts/sibling-scan.txt`.

### Findings by lane and path

1. **Capture and snapshot writers in sibling lanes:**
   - `audio-shokunin`: `corpus/live/r75-scribe/fixture-snapshot-1640.py`, `corpus/live/r76-scout/capture_probe.py`, `corpus/live/r76-verifier/worktree-snapshot.py`, `corpus/live/r78-baseline/capture76_leg_diff.py`, `corpus/live/r79-scout/probe_b_capture.py`, `corpus/live/r79-author/exp_capture_ports.py` (hardware/audio stream probes and worktree snapshot utilities).
   - `chousa-shokunin`: `tools/capture-text.py` (OOXML/OLE compound file Word text extractor for captures), `tools/capture-fetch.py` (campaign curl GET re-fetch tool into `corpus/captures/`), wave scripts under `.ufo/waves/round-30/build/ExecD6Snapshot/` and `.ufo/waves/round-36/w1/ExecWitnessDirect/argv-witness-capture.py`.
   - `game-dev-2d-shokunin`: `corpus/live/frontier-pygame/capture_probe.py`, `corpus/live/r67-critic/seam_capture_probe.py`, `corpus/live/r71-reviewer/probe-snapshot-112817.py`, `corpus/live/r72-simplifier/snapshot_loop.sh`.
   - `game-dev-3d-shokunin`: `reports/round-107/mutations/w-cron-snapshot.sh`.
   - `kagi-shokunin`: `.ufo/waves/round-25/tools/capture-feeds.sh` (feed capture script); knowledge entry `corpus/knowledge/secret-scanning-detection-vs-validation.md` (documents Gitleaks vs TruffleHog semantics, not a tool).
   - `kaidoku-shokunin`: wave capture tools (`.ufo/waves/round-15/snapshot-inventory.py`, `.ufo/waves/round-22/tools/capture-probes.py`, `.ufo/waves/arc3-loop1-round2/claims/c3/VZ-3/vz3-independent-capture.sh`, `.ufo/waves/round-51/w1/CritTriV6/v5-source-snapshot.py`).
   - `kake-shokunin`: `scripts/live_snapshot.py`, `scripts/source_snapshot.py`, `scripts/response_snapshot.py`, `scripts/capture_delta.py` (retained HTTP GET response and page snapshot recorders; explicitly notes: "no cookies, credentials or request body").
   - `kama-shokunin`: `tools/test-snapshot.sh` (test harness verifying that `kama-probe snapshot` redacts forbidden fixture strings like `"user:pass"`, `"api_key"`, `"fixture-secret"`), `tools/round90-reason-capture.py`, `.ufo/waves/round-16/live/replay-captured-503.py`, `.ufo/waves/round-24/build/out/CaseWrongTypeCitation/capture_git_semantics.py`.
   - `kengaku-shokunin`: `.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/capture.py`, `.ufo/waves/round-83/w1/HistoryReceiptR83/capture_receipts.py`, `.ufo/waves/round-83/w1/SentinelR83/boundary_capture.py`.
   - `kotoba-shokunin`: `.ufo/round-46/evidence/w2/critic/capture_selftest.py`.
   - `kotodama-shokunin`: `tools/check-gate-captures.py` (verifies gate capture files against sha256 tokens), `reports/round-76/counters/capture-evidence.py`.
   - `kumitate-shokunin`: `.ufo/waves/round-70/build/K70ReviewCounterR7/c2-forgecapture.private.sh`, `.ufo/waves/round-79/w1/K79ScoutOpen/capture.sh`, `.ufo/waves/round-92/controls/ctl-captured.py`.
   - `lore-shokunin`: `.ufo/waves/round-97/seats/scratch-R1/capture.sh`.
   - `mado-shokunin`: `.ufo/waves/round-26/controls/K1SnapshotCache.py`, `.ufo/waves/round-40/w1/ExecCaptureStable/capture.sh`.
   - `mori-shokunin`: `.ufo/waves/round-26/capture/capture.sh`, `.ufo/waves/round-26/capture/capture-boots.sh`.
   - `souji-shokunin`: `tools/souji-wave-evidence-capture.sh` (census wave evidence capture script into `census/round-<N>/waves/`).
   - `tabi-shokunin`: `.ufo/waves/round-42/w1/RevC2Freeze/capture-git-evidence.sh`.
   - `tameshi-shokunin`: `tools/context-capture.py` (retained context receipt gate; explicitly notes "callers must select non-secret receipt/expected files. No credential probe is executed.").
   - `tsukuroi-shokunin`: `tools/check-review-snapshots.py` (review byte identity checker), `tools/capture-resume-facts-r84.py` (read-only /proc and /sys facts capture).

2. **Secret scanners in sibling lanes:**
   - **No sibling lane maintains an ongoing instrument or dedicated secret scanner tool** comparable to kasegi's `corpus/instruments/capture-secret-scan.py`.
   - One-time audit records / ad-hoc grep artifacts produced by Sentinel seats exist in wave receipts:
     * `souji-shokunin`: `census/round-18/transcript-secret-scan.json` (one-time `gitleaks dir --redact` run in round 18).
     * `kaidoku-shokunin`: `.ufo/waves/round-71/w1/SentinelScope/secret-scan.json` (Sentinel audit checking private keys, provider tokens, op URIs, session cookies).
     * `mado-shokunin`: `.ufo/waves/round-51/w2/SentinelC2Scope/receipts/secret-scan.txt` (Sentinel grep for gh tokens, AKIA, PRIVATE KEY).
     * `tameshi-shokunin`: `.ufo/waves/round-49/w2/T49W2SentinelScope.receipts/secret-scan.txt` (Sentinel grep for AKIA, token assignments).

3. **CloudFront signed cookies & skdutid SAS detection across siblings:**
   - **Zero sibling lanes detect CloudFront signed cookies or `skdutid` SAS.** Neither pattern appears in any sibling lane.
   - `CloudFront-Signature` occurs in **zero** files outside `kasegi-shokunin`.
   - `skdutid` occurs in **zero** files outside `kasegi-shokunin`.
   - `X-Amz-Security-Token` occurs in **zero** files outside `kasegi-shokunin`.
   - `CloudFront` appears in sibling lanes only in non-credential prose/docs (`game-dev-3d-shokunin` Linux UE download 403 note, `mori-shokunin` S579.html AWS docs export).
   - `Signature=` appears in sibling lanes exclusively as git configuration `log.showSignature=false` (`kama-shokunin`, `kengaku-shokunin`, `souji-shokunin`).
   - `sig=` appears in sibling lanes as Godot area signal names (`areasig`, `bodysig`, `SIGINT`).

---

## 2. Kasegi callers and importers of `capture-secret-scan.py` at 1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70

Receipt: `ConnectorOverlap-receipts/kasegi-callers.txt`.

At landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`, `capture-secret-scan.py` exports 12 shapes via `patterns()`:
`private-key`, `op-ref`, `bearer`, `authorization`, `credential`, `session-cookie`, `aws-sts-session-token`, `aws-access-key-id`, `gcs-signed-url-signature`, `azure-sas-signature` (widened to 2–7 letter parameter names, matching `skdutid`), `cloudfront-signed-url-signature`, `cloudfront-signed-cookie-signature` (new).

### Caller / Importer Inventory & Inheritance Analysis

| Caller / Importer | Path / Invocation | Mechanism | Inherits new shapes? |
|---|---|---|---|
| `capture-source.py` | `corpus/instruments/capture-source.py:102-113` | Dynamically loads `capture-secret-scan.py` via `importlib.util.spec_from_file_location("capture_secret_scan", path)` in `intake_gate()`; calls `scan.patterns()` and `scan.scan_bytes()`. | **YES.** Both new shapes (`cloudfront-signed-cookie-signature` and `skdutid` SAS) are dynamically loaded and enforced before any file write. Verified by live drive over loopback (refuses both with rc=3, zero byte leak). |
| `capture-secret-scan.py` (self) | `corpus/instruments/capture-secret-scan.py` | CLI entry points (`--files`, `--rev`, `--selftest`). | **YES.** Directly implements the regex patterns, docstring, and 53 passing selftest cases. |
| Round-91 C2 counter | `.ufo/waves/round-91/c2/capability-check.py` | Imports `corpus/instruments/capture-secret-scan.py` via `load_instrument()`. | **YES.** Limb K4 verifies plant hits/misses, K7 verifies seeded plants, K8 clause map verifies both positive and negative clauses for both new shapes. |
| Round-91 C2 controls | `.ufo/waves/round-91/controls/c2-controls-r91.sh` | Executes `python3 -B capture-secret-scan.py` directly. | **YES.** Evaluates F1–F8 forgeries and unpinned controls against the candidate scanner. |
| Round-90 C2 counter | `.ufo/waves/round-90/c2/capability-check.py` | Imports `capture-source.py` (which loads `capture-secret-scan.py`) and checks G0–G6. | **YES in runtime behaviour, but fails limb G0 by design.** G0 dynamically checks that the counter's plant shapes equal `scan.patterns()`. At the round-91 landing, `patterns()` returns 12 shapes, while round-90 counter planted 11 shapes (`missing=cloudfront-signed-cookie-signature`). This is expected counter staleness, not a runtime regression. |
| Practice package gate | `corpus/instruments/claim-package-check.py` | Defines its own static `SECRET_PATTERNS` (6 base shapes). Does **not** import `capture-secret-scan.py`. | **NO.** Does not inherit the AWS, GCS, Azure SAS, or CloudFront URL/cookie shapes. |
| Practice evidence | `corpus/practice/<pkg>/evidence/` | Scanned by `capture-secret-scan.py --rev REV` or `--files`. | **YES.** Line 17 of `capture-secret-scan.py` includes `corpus/practice/<pkg>/evidence/` in `is_capture_path()`. |
| Pre-commit L1 intake | `QUALITY.md` R138 / L1 script | Invokes `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>...`. | **YES.** Runs the CLI directly, enforcing all 12 shapes on all new captures and receipts before commit. |

---

## 3. Cross-claim pattern & QUALITY.md criteria review

Receipt: `ConnectorOverlap-receipts/c1-c2-binding-evidence.txt`.

### The Shared Pattern
Both C1 and C2 this round implement an identical epistemological pattern: **binding a claim's semantic assertions strictly to non-author or first-party source text, rejecting author-invented proxies:**
- **C1 (Citation Repair):** Tranche 6 binds every edit in `corpus/knowledge/triage-thresholds.md` strictly to the non-author hand labels established by `ReviewC1Sites` in round 90 (`round91-labels.tsv` at `e993fd18`). Counter limb M9 ("edit-equals-label") enforces that all 6/6 edits match the exact replacement named by the label, and M10 ("completeness") enforces that the mapped set equals the labelled set.
- **C2 (Capability Extension):** Capability additions are anchored strictly in first-party vendor documentation (S133 Microsoft user-delegation SAS; S134 Amazon CloudFront custom policy signed cookies). Counter limb K8 ("clause map") maps every semantic clause in the claim statement 1-to-1 to a positive or negative plant derived directly from S133/S134 line locations.

### Evaluation of QUALITY.md R138–R142

| Criterion | Rule Summary | Does it capture the C1/C2 pattern? | Reason |
|---|---|---|---|
| **R138** | Scans captures with `capture-secret-scan.py --files` before first commit. | **No** | Operational rule governing artifact intake scanning; does not govern claim statement formulation or semantic binding. |
| **R139** | Bounds landing commits to declared scope (`landing-scope-check.py`). | **No** | Git diff boundary enforcement; independent of source/label grounding. |
| **R140** | Requires non-author hand-labelled sample (>=15 keys) when keys are selected by a lexical proxy. | **No** | Only checks that a proxy-selected sample has no WRONG keys. Does not enforce that applied edits equal the label text (M9), does not enforce tranche completeness (M10), and does not cover capability statement clauses (K8). |
| **R141** | Counter plants must lie within `is_capture_path`. | **No** | Syntactic scan-scope check; does not enforce 1-to-1 mapping from statement clauses to source-anchored plants. |
| **R142** | Counter classifies against `git archive REV` extract and clean clone. | **No** | Environment isolation rule; does not govern statement binding. |

### Conclusion & Proposed New Criterion (R143)
A new criterion is warranted. R140 governs *admissibility* of proxy-derived keys, but neither R140 nor R138–R142 govern *statement-to-grounding congruence*.

**Draft Criterion R143:**
```markdown
| R143 | A claim that asserts a set of discrete semantic changes (citation-repair tranches or capability edge classes) binds each assertion bidirectionally to external non-author or first-party text before freeze:
  (a) For citation-repair maps: every map edit equals the replacement text specified by a committed non-author label file (M9 edit-equals-label), and the map's key set equals the labelled set without unlabelled additions or selective omissions (M10 completeness over `(site, key)` tuples);
  (b) For capability statements: every semantic clause (positive detection, negative limit, boundary exception) maps 1-to-1 to an explicit counter plant anchored in first-party source snapshot lines (K8 clause map).
Check before landing: the counter verifies M9 + M10 (C1) or K8 (C2) at rc 0; any unmapped clause or unlabelled edit fails the check. | `corpus/lessons/round-91.md` § Mistakes M91-1, M91-2; round-91 C1 limbs M9/M10, C2 limb K8; r90 closure defect 1 |
```

---

## 4. UFO-FSD Connector Move: Compatible Synthesis Across Proposals

Receipt: `ConnectorOverlap-receipts/proposal-synthesis-evidence.txt`.

### Evidence & Structural Contradiction
Reviewing the current round proposals and attack findings across all seats:
1. `ReviewC1Labels` generated 30 non-author labels for Round 92 (`round92-labels.tsv`) targeting bare GONE keys in `corpus/knowledge/*.md` (projected meter move: 891/1880 -> 905/1877).
2. `ReviewC2Scanner` Finding F1 identified that C2's landing in `capture-secret-scan.py` shifted **31+ explicit instrument line citations** across three knowledge entries (`cloud-signed-url-...md`, `capture-intake-gate.md`, `presigned-url-...md`) by 20–25 lines, leaving **4 sentences asserting false claims** (claiming CloudFront signed cookies are not detected).
3. `ReviewC2Scanner` Finding F2 established that `anchorcheck.py` is range-only (`line <= file_len`), exiting 0 (`86 in-range, 0 bad`) despite citing unrelated lines, and `resolve.py` / `knowledge-meter.py` classifies existing files as `INTERNAL` regardless of line correctness.
4. `CriticClaims` C1-F1 showed M10 is incomplete because it compares `{site}` rather than `{(site, key)}`, and C2-F1 showed K8 omitted 3 statement clauses.
5. **The Structural Contradiction:**
   - C2 improves `coverage` by expanding scanner capability, but because C2's predicate P3 strictly isolates its diff from `corpus/knowledge/`, it intentionally leaves the knowledge entries desynchronized.
   - The citation meter (`resolve.py`) and anchor gate (`anchorcheck.py`) are structurally blind to line drift within existing files.
   - `ReviewC1Labels` only harvests GONE tokens, completely missing the 31 invalid code line anchors.
   - As a result, every capability addition in C2 silently degrades `depth:verifiability`, which remains an unmeasured, permanently deferred externality across rounds.

### Affected Axes
- **depth:verifiability** (score 4; lowest axis): directly improved by repairing semantic truth and line citations in knowledge entries, preventing silent corruption.
- **coverage** (score 8 held): unharmed; scanner detection and intake gate remain fully intact.

### Proposed Non-Obvious Move: The "Complete Grounding Tranche" with Token-Bound Anchor Verification
Unify Round 92 C1 tranche around a single co-designed repair package that synthesizes ReviewC1Labels and ReviewC2Scanner into an integrated verifiability advance:
1. **Tranche Composition:** Combine ReviewC1Labels' 26 net GONE-token normalizations (the subset where `label != "No edit"`) with the 31 instrument line-anchor repoints from ReviewC2Scanner F1.
2. **Dual-Limb Verification:**
   - **Limb M10-R:** Tighten M10 to compare `{(site, key)}` tuples (closing CriticClaims C1-F1), matching the 26 net GONE edits.
   - **Limb M11 (Token-Bound Code Anchors):** Extend `anchorcheck.py` (or add counter limb M11) to enforce QUALITY.md R131: for any `path:line` cite to repo code (`corpus/instruments/*.py`), assert that the cited line(s) contain the token/identifier named in the citing sentence.
3. **Knowledge Consistency:** Rewrite the 4 contradictory sentences in `cloud-signed-url-credentials-in-captured-evidence.md` to accurately document the landed signed-cookie capability and Azure SAS window.

### Risks & Mitigations
- **Risk (Target Conflation):** Authors might expect the 31 instrument line-repoints to move the `resolve.py` rate.
  *Mitigation:* Explicitly declare in the claim that the rate move (891/1880 -> 905/1877) derives solely from the 26 GONE-to-INTERNAL conversions, while M11 verifies the 31 code anchor lines.
- **Risk (Predicate Scope Contamination):** Modifying knowledge entries inside C2 would violate C2 P3.
  *Mitigation:* Keep C2 diffs strictly isolated to instruments and scorecard; route all knowledge synchronizations to C1 in the immediately following round.

### Verification
- **C1 Meter:** `python3 -B .ufo/waves/round-92/c1/knowledge-meter.py --measure-rev <landing>` prints `891/1880 -> 905/1877`.
- **Anchor Gate:** `python3 -B corpus/instruments/anchorcheck.py --token-check corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` exits 0 with `0 bad`.
- **Consistency Check:** `grep -E 'CloudFront signed cookies.*are not detected' corpus/knowledge/*.md` prints 0 hits.

---

## 5. Routing lines for owners

- **To L1 (KasegiR91):** Both C1 and C2 landed cleanly on their frozen predicates; integrate wave receipts. For Round 92 planning, adopt the Complete Grounding Tranche (unifying ReviewC1Labels' 26 net GONE edits with ReviewC2Scanner's 31 line repoints).
- **To C1 Owner (Round 92):** Note that ReviewC1Labels' `round92-labels.tsv` contains 3 "No edit" rows and 1 input-file row; net actionable edits = 26. Tighten M10 to compare `(site, key)` pairs per CriticClaims C1-F1. Incorporate M11 token-bound anchor checks for code citations.
- **To C2 Owner (Round 92):** Expand `CLAUSES` in `capability-check.py` to cover the 3 missing clauses identified by CriticClaims C2-F1. In `capture-source.py` intake gate, address HTML `<a href>` attribute parsing (CriticHarm Q3) and colon-form object dump signatures (SentinelCookie F1).
- **To Sibling Lane Owners (`kake-shokunin`, `chousa-shokunin`, `souji-shokunin`):** Informational only (no edits): kake's snapshot writers and chousa's `capture-fetch.py` currently operate without pre-commit credential scanning; if they adopt capture scanning, note kasegi's `capture-secret-scan.py` pattern and allowlist architecture.

---

## Files written

- `.ufo/waves/round-91/w1/ConnectorOverlap.md` (this report)
- `.ufo/waves/round-91/w1/ConnectorOverlap-receipts/sibling-scan.txt`
- `.ufo/waves/round-91/w1/ConnectorOverlap-receipts/kasegi-callers.txt`
- `.ufo/waves/round-91/w1/ConnectorOverlap-receipts/c1-c2-binding-evidence.txt`
- `.ufo/waves/round-91/w1/ConnectorOverlap-receipts/proposal-synthesis-evidence.txt`

Scratch directory `/fast/scratch/hyaku/kasegi-r91/ConnectorOverlap` was used for temporary derivations, verified clean with `capture-secret-scan.py --files`, and completely removed before yielding (`rm -rf /fast/scratch/hyaku/kasegi-r91/ConnectorOverlap`). No lane files outside `.ufo/waves/round-91/w1/` were touched; no sibling lanes were modified.
