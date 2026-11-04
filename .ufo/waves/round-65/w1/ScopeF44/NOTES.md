# NOTES — ScopeF44 (Kasegi Round 65 Wave 1)

- **Seat:** `ScopeF44` (connector, leaf member)
- **Lane Root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Base Master:** `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
- **Scratch Directory:** `/fast/scratch/hyaku/kasegi-r65/ScopeF44`
- **Assigned Axes:** `depth:verifiability`, `coverage`
- **Milestone:** Predata signal-fail-closed gate build and F44 source screen

---

## 1. Context and Environment

- Process cwd is `/home/vgpnk/Projects/shokunin` (fleet root).
- Scratch directory `/fast/scratch/hyaku/kasegi-r65/ScopeF44` was created and used for all intermediate script outputs and raw receipts.
- All actions strictly conformed to the leaf contract: read-only access across the repo, sibling lanes, and fleet root; zero tasks/spawns; zero git mutations; zero pacman transactions; zero production edits.
- Output files written solely under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-65/w1/ScopeF44/` and `.ufo/waves/round-65/w1/ScopeF44.md`.

---

## 2. C2 Screen: FIRST PSIRT Services Framework v1.1 (Frontier F44, Source S098)

### 2.1 Candidate Document Profile
- **Title:** FIRST PSIRT Services Framework v1.1 (Version 1.1)
- **URL:** `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`
- **Publisher:** Forum of Incident Response and Security Teams (FIRST)
- **Structure:**
  - 4-tier taxonomy spine: `SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS` (L227)
  - 6 Service Areas:
    1. Service Area 1: Stakeholder Ecosystem Management (L402)
    2. Service Area 2: Vulnerability Discovery (L674)
    3. Service Area 3: Vulnerability Triage and Analysis (L843)
    4. Service Area 4: Remediation (L941)
    5. Service Area 5: Vulnerability Disclosure (L1145)
    6. Service Area 6: Training and Education (L1309)
  - 28 Services and 84 Functions (verified by exact regex counts on `S098.candidate.txt`: `grep -c '^Service Area [0-9]'` = 6, `grep -c '^Service [0-9]'` = 28, `grep -c '^Function '` = 84).
  - 3 Core Organizational Models: Distributed, Centralized, Hybrid (L248–L271).
  - Core differentiators: distinguishes product security incident response (PSIRT) from infrastructure incident response (CSIRT) based on product focus (L244), and outlines intake, triage bug bars/quality gates (L853), established-finder bypass recommendations (L875), isolated reproduction environments (L918), and disclosure audience definition (L1231).

### 2.2 Coverage Classification: (a) UNCOVERED
1. **Uncovered:** Neither `corpus/README.md` (F01–F43) nor `corpus/SOURCES.md` (S001–S097) holds this framework.
2. **Not Covered by Closest Held Rows:**
   - **`F43` (S095, `cert-guide-cvd-phases-and-validation.md`):** Holds CERT/CC's 6-phase CVD matrix across 5 stakeholder roles (Finder, Vendor, Coordinator, Deployer, Public). Narrowed by: *"Read complete column headings (S095.txt:112-116) with Validation (:129-134) and Remediation (:141-146); a dash is not a prohibition on reporter verification. Generic phase names, prioritization and deployment are supporting context already held elsewhere."* F43 covers inter-role phase allocation in coordinated disclosure, whereas F44 covers an individual vendor's internal PSIRT operational architecture and service catalog.
   - **`F06` (S018, `multiparty-vulnerability-coordination.md`):** Holds FIRST's multi-party CVD guidelines v1.1. Narrowed by: *"Record each party's role and relationship; an upstream fix is not downstream evidence."* F06 covers cross-boundary coordination between finders, multiple vendors, coordinators, and downstream users. It does not define a vendor's internal PSIRT service taxonomy or organizational models.
   - **`F11` (S041, `iso-29147-and-30111-division-of-labour.md`):** Holds JPCERT/CC's division-of-labour guidance between ISO 29147 (disclosure) and ISO 30111 (handling). Narrowed by: *"Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names..."* F11 is a meta-analysis of ISO standard roles, not the FIRST community's concrete 6-area service framework.
   - **`F10` (S040, `vendor-disclosure-policy-commitments-crosswalk.md`):** Cisco's PSIRT policy states alignment with ISO/IEC 29147:2018 (S040.txt:58), but S040 is a single vendor's standing public policy, not the FIRST PSIRT Services Framework.
3. **Not Adjacent:** Fully inside `kasegi-shokunin`'s province ("program rules, scopes, claim packages, triage and claim gates, and submission/disclosure packaging"). Does not tread on `chousa` (research method), `kagi` (secrets), `kake` (web properties), or `kengaku` (benchmarks/LLM evaluation).

### 2.3 Registry Duplicate Check
- Exact URL: `grep -F 'https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md` -> Exit 1 (no match).
- Normalized host+path: `grep -F 'first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md` -> Exit 1 (no match).
- Registry is clear; S098 is a unique addition.

### 2.4 QUALITY R80 Pre-Freeze Screen & Downstream Analysis
- **Receipt Date:** `2026-11-04T19:32:07Z`, prior to any freeze commit.
- **Term frequencies:**
  - `"PSIRT Services Framework"`: 0 in README, 0 in SOURCES, 0 in PROVINCE, 0 in SKILL, 0 across all 81 knowledge entries.
  - Downstream snapshot sweep found hits in `round-24/S001.txt`, `round-24/S002.txt`, and `round-36/S053.txt`.
  - **Critical Receipt Inspection:** In all three snapshot hits, `"PSIRT Services Framework"` occurs exactly at line 201 within the standardized FIRST.org website navigation menu banner (`Service FrameworksCSIRT Services Framework\nPSIRT Services Framework\nInformation Exchange Policy (IEP)...`). This is identical to line 201 of `S098.candidate.txt`. Zero substantive text or knowledge citations exist in the repository.

---

## 3. C1 Screen: Figure-Audit Sibling Scan & Signal Handling Claims

### 3.1 Sibling Lanes Scan (`kengaku-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`)
- Scanned for `figure-audit.py`, `run_derive`, `upstream_stale`, `derive-signal`.
- `kengaku-shokunin`: Contains standalone scratch derive scripts (`derive_spans.py`, etc.) and a single cross-reference in `.ufo/waves/round-78/w1/ConnectorR78.md:2334` noting kasegi's `figure-audit.py` as an external unrelated instrument.
- `kotodama-shokunin` & `kumitate-shokunin`: Zero derive-gate or figure-audit instruments. Neither lane has a `corpus/instruments/` directory.
- **Verdict:** `SCOPE CLEAR`.

### 3.2 Held Lane Records on Signal Handling
- Checked `SKILL.md` and `corpus/instruments/figure-audit.py`.
- **Findings:**
  - `SKILL.md:1224`: *"Negative upstream signal statuses remain ignored; a stale group stops later && groups."*
  - `SKILL.md:1236`: *"Negative-signal partial-output and PATH-shadowed grep residuals remain open."*
  - `corpus/instruments/figure-audit.py:44`: *"...negative signal statuses remain ignored."*
  - `corpus/instruments/figure-audit.py:82`: *"Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored."*
  - `corpus/instruments/figure-audit.py:449`: `run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))`
- **Verdict:** No held lane record claims signal handling for this gate. Current bytes explicitly document negative signal statuses as ignored and residual.

---

## 4. UFO-FSD Connector Move: Compatible Synthesis Across Round-65 Proposals

### 4.1 Evidence from Round Cache & Proposals
1. **The Intended C1 Spec (`w1-spec.json`):**
   - Assumes candidate fails closed on signal-terminated stages: SIGTERM/SIGKILL upstream stages become stale naming the signal, final-stage signal label becomes `derive-signal-N` (never `derive-exit--N`), and SIGPIPE non-final stays benign.
   - For `ExecSignalProbes`, specifies:
     - P1: `python3 kill.py | wc -l` (want 0)
     - P2: `python3 sigkill.py | wc -l` (want 0)
     - P3: `cat g.txt | python3 kill.py` (producer final stage, want "")
   - For `ExecDriver`, specifies Measurement 1:
     - `collector-base (the six-probe collector in base expectations on the committed production gate)`
2. **Empirical Falsification by `ExecSignalProbes` and `ExecSignalMutants`:**
   - In `probes-base.txt`: `c1-signal-probes.py --mode base` executed against base master `a283189b` reported:
     `PROBE P3 mode=base audit_exit=1 verdict=stale reason=derive-exit--15`
     `PROBES probes=6 failures=1` (Audit Exit = 1).
   - In `mutbat-base.txt`: `signal-mutbat.py` on base master observed:
     `BASE p3-final-signal verdict=stale reason=derive-exit--15`
3. **The Root Cause in Base Code (`figure-audit.py:116-121` at base):**
   ```python
   status = processes[-1].returncode
   if status != 0:
       out = b"".join(output).decode("utf-8", "replace").strip()
       return None, out, "derive-exit-%d" % status
   for p, head in zip(processes[:-1], heads[:-1]):
       if upstream_stale(head, p.returncode):
           ...
   ```
   For P3, the dying process (`kill.py`) is the **final stage** (`processes[-1]`). Its returncode is `-15`.
   Because `-15 != 0`, the final-stage check triggers immediately, returning `None, out, "derive-exit--15"`.
   Therefore, P3 was **never exit 0 (ok) at base**! It was already stale with exit 1, but carried the malformed label `derive-exit--15`.

### 4.2 The Contradiction & Second-Order Effects
- **Contradiction:** The prompt's informal premise treats all signal probes at base as "false greens" that read `ok`. If the collector's `--mode base` asserts `verdict=ok` on P3, the base collector fails (`failures=1`), and `verify-r65.py`'s Measurement 1 (`collector-base`) will exit 1 and fail the verification driver on committed production bytes.
- **Substrate Difference:**
  - Upstream signals (P1/P2) were false greens: `upstream_stale` checked only `status > 1` and `exit1 non-grep`, letting negative statuses pass through as benign, resulting in `verdict=ok` and `audit_exit=0`.
  - Final-stage signals (P3) were already fail-closed: `status != 0` caught `-15`, producing `verdict=stale` and `audit_exit=1`, but printed the invalid label `derive-exit--15`.
  - The C1 candidate change for P3 is **not** a status flip (`ok` -> `stale`); it is a **label formatting fix** (`derive-exit--15` -> `derive-signal-15`).

### 4.3 Proposed Move: Decouple P3 Label Invariant from Upstream Status Flip in Verification Architecture

**Specific Formulation:**
1. **Harmonize `c1-signal-probes.py` Mode Base:**
   Explicitly define `--mode base` expectation for P3 as:
   `audit_exit=1, verdict=stale, reason=derive-exit--15`.
   This allows `c1-signal-probes.py --mode base` to exit 0 (`probes=6 failures=0`) against base master `a283189b`, proving that the collector accurately characterizes the base state without failing.
2. **Align Driver Measurements in `verify-r65.py`:**
   - Measurement 1 (`collector-base`): Asserts base behavior (P1/P2 = ok false-green; P3 = stale with malformed `derive-exit--15`; P4/P5/P6 = ok). Passes exit 0.
   - Measurement 2 (`collector-candidate`): Asserts candidate behavior (P1/P2 = stale with `derive-upstream-signal-N`; P3 = stale with `derive-signal-15`; P4/P5/P6 = ok). Passes exit 0.
   - This cleanly separates the **status-flip discriminant** (P1: ok -> stale-15, P2: ok -> stale-9) from the **label-format discriminant** (P3: `derive-exit--15` -> `derive-signal-15`).
3. **Selftest Lineage Clarification in `figure-audit.py`:**
   In `ExecSignalGate/figure-audit.py`, selftest case `upstream-python-signal-ignored` was flipped from `exit 0` to `exit 1` (`derive-upstream-signal-15`), but kept its now-contradictory name `"upstream-python-signal-ignored"`.
   Recommend documenting this explicitly in the lesson and scorecard as an intentional lineage retention to avoid misleading future verifiers who read "signal-ignored" expecting an ignored signal.
4. **Substrate Interaction: Python SIGPIPE vs Native SIGPIPE:**
   In Python subprocesses, Python's runtime sets SIGPIPE to `SIG_IGN` by default, turning broken pipes into `BrokenPipeError` (exit code 1). For a Python producer in a pipeline to exhibit native SIGPIPE (-13) and test the benign non-final SIGPIPE branch, it must explicitly set `signal.signal(signal.SIGPIPE, signal.SIG_DFL)`. This substrate requirement (correctly handled by `ExecSignalGate`'s `pipe.py` and `ExecSignalProbes`'s `bigwriter.py`) must be documented in `figure-audit.py` docstrings so users understand why plain Python scripts fail closed with `derive-upstream-exit-1` on broken pipes.

### 4.4 Impact on Declared Axes
- **Improves `depth:verifiability` (Axis 1):** Eliminates a false-failure deadlock in `verify-r65.py` and establishes exact-match verifiability on committed bytes for both base and candidate states.
- **Protects `coverage` (Axis 2):** Preserves full discriminating coverage across all six probe configurations without loss of rigor or mutation sensitivity.
- **Harms zero axes.**

### 4.5 Risks and Verification Plan
- **Risk:** A reviewer might assume P3's base failure was an accidental regression rather than an existing property of `figure-audit.py`.
- **Verification:**
  1. Run `python3 c1-signal-probes.py --instrument corpus/instruments/figure-audit.py --mode base` -> exit 0, 6/6 match.
  2. Run `python3 c1-signal-probes.py --instrument .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py --mode candidate` -> exit 0, 6/6 match.
  3. Run `python3 signal-mutbat.py` on candidate -> 4/4 killed; on base -> 4/4 survivors (limb absent).
  4. Run `verify-r65.py` -> 8/8 measurements pass.
