# ScopeF44 — Scoped Findings Receipt (Kasegi Round 65 Wave 1)

- **Seat:** `ScopeF44` (connector, leaf member)
- **Lane Root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Base Master:** `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
- **Run UTC:** `2026-11-04T19:32:07Z`
- **Scratch Directory:** `/fast/scratch/hyaku/kasegi-r65/ScopeF44`
- **Assigned Axes:** `depth:verifiability`, `coverage`
- **Milestone:** Predata signal-fail-closed gate build and F44 source screen

---

## 1. Executive Summary & Deliverables

This seat executed the cross-surface screen for Claim C1 (signal-fail-closed derive gate) and Claim C2 (Frontier F44 on S098, FIRST PSIRT Services Framework v1.1). All checks were performed strictly read-only outside this seat's directories, adhering to the leaf member contract (zero spawns, zero commits, zero mutating git/jj verbs, zero production edits, zero pacman transactions).

Deliverables produced under `.ufo/waves/round-65/w1/`:
1. `.ufo/waves/round-65/w1/ScopeF44/screen.md` — The complete three-section screen:
   - Section 1: C2 coverage decision, narrowing sentences for closest held rows, and duplicate URL registry checks.
   - Section 2: Extended pre-freeze screen receipt (QUALITY R80) with UTC timestamps, `grep -ric` counts across README, SOURCES, PROVINCE, and knowledge files, plus the downstream-consumer sweep over `corpus/source-snapshots/`.
   - Section 3: C1 sibling lane scan across `kengaku-shokunin`, `kotodama-shokunin`, and `kumitate-shokunin`, plus verification of signal handling claims in held lane records (`SKILL.md` and `corpus/instruments/figure-audit.py`).
2. `.ufo/waves/round-65/w1/ScopeF44/NOTES.md` — Detailed investigative notes, taxonomy breakdown of S098, and the UFO-FSD connector synthesis.
3. `.ufo/waves/round-65/w1/ScopeF44.md` — This scoped findings report.

---

## 2. Claim C2 Screen: Frontier F44 & Source S098

### 2.1 Candidate Profile
- **Source:** FIRST PSIRT Services Framework v1.1
- **Target URL:** `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`
- **Assigned Frontier ID:** `F44`
- **Assigned Source ID:** `S098`

### 2.2 Coverage Decision: (a) UNCOVERED
FIRST PSIRT Services Framework v1.1 is **(a) UNCOVERED** by any held frontier row in `corpus/README.md` (F01–F43) or registry row in `corpus/SOURCES.md` (S001–S097). It defines an organization's internal PSIRT service taxonomy across 6 service areas, 28 services, 84 functions, and 3 organizational models (Distributed, Centralized, Hybrid), differentiating product incident response from infrastructure response (CSIRT). It is fully within `kasegi-shokunin`'s domain ("program rules, scopes, claim packages, triage and claim gates, and submission/disclosure packaging" per `PROVINCE.md:3,29-30`) and is not adjacent.

### 2.3 Closest Three Held Rows & Narrowing Sentences

1. **`F43` (Source `S095`): CERT/CC adapted CVD phase-to-five-role matrix**
   - **File:** `corpus/knowledge/cert-guide-cvd-phases-and-validation.md`
   - **Narrowing Sentence:**
     > "Read complete column headings (S095.txt:112-116) with Validation (:129-134) and Remediation (:141-146); a dash is not a prohibition on reporter verification. Generic phase names, prioritization and deployment are supporting context already held elsewhere." (`corpus/README.md:1031`)
   - **Distinction:** F43 covers inter-role phase allocation in coordinated disclosure across 5 multi-stakeholder roles (Finder, Vendor, Coordinator, Deployer, Public). F44 covers an individual vendor organization's internal PSIRT operational architecture, service catalog, and capability specifications.

2. **`F06` (Source `S018`): Multi-party CVD — FIRST guidelines v1.1**
   - **File:** `corpus/knowledge/multiparty-vulnerability-coordination.md`
   - **Narrowing Sentence:**
     > "Record each party's role and relationship; an upstream fix is not downstream evidence." (`corpus/README.md:207`)
   - **Distinction:** F06 covers cross-boundary coordination between finders, multiple vendors, coordinators, and downstream users. F44 defines the internal structure, services, functions, and sub-functions that a single vendor's product security incident response team provides.

3. **`F11` (Source `S041`): ISO/IEC 29147/30111 division-of-labour meta**
   - **File:** `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`
   - **Narrowing Sentence:**
     > "Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018)." (`corpus/README.md:212`)
   - **Distinction:** F11 covers the high-level division of labour between outward-facing disclosure (ISO 29147) and internal vulnerability handling (ISO 30111). F44 provides the operational, granular service catalog (28 services, 84 functions) and organizational models (Distributed, Centralized, Hybrid) defining how a PSIRT actually operates.

*(Note: `F10` / `S040` Cisco PSIRT policy cites ISO/IEC 29147:2018 alignment, but is a single vendor's standing public policy, not the FIRST community framework).*

### 2.4 Duplicate URL Registry Verification
- Exact URL: `grep -F 'https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md` -> Exit 1 (`0 matches`).
- Normalized Host+Path: `grep -F 'first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md` -> Exit 1 (`0 matches`).
- Path Slug: `grep -i 'psirt_services_framework' corpus/SOURCES.md corpus/README.md PROVINCE.md` -> Exit 1 (`0 matches`).
- The candidate URL is absent from the registry and entire repository.

### 2.5 QUALITY R80 Pre-Freeze Screen & Downstream Analysis
- **Receipt Run UTC:** `2026-11-04T19:32:07Z` (pre-freeze).
- **Knowledge Filename Check:** `ls corpus/knowledge/ | grep -E -i 'psirt|services-framework'` returned 0 matches across 81 files.
- **Term Counts (`grep -ric`):**
  - `"PSIRT Services Framework"`: README=0, SOURCES=0, PROVINCE=0, SKILL=0, knowledge/*.md=0.
  - `"psirt_services_framework"`: README=0, SOURCES=0, PROVINCE=0, SKILL=0, knowledge/*.md=0.
  - `"FIRST PSIRT"`: README=0, SOURCES=0, PROVINCE=0, SKILL=0, knowledge/*.md=0.
  - `"Stakeholder Ecosystem Management"`: README=0, SOURCES=0, PROVINCE=0, SKILL=0, knowledge/*.md=0.
  - `"PSIRT"`: README=0, SOURCES=1 (Cisco S040), PROVINCE=0, SKILL=0, knowledge/*.md=4 files (all Cisco S040 or vendor disclosure policy crosswalks).
- **Downstream Consumer Sweep (`grep -rl` over `corpus/source-snapshots/`):**
  - `"PSIRT Services Framework"` matched `round-24/S001.txt`, `round-24/S002.txt`, and `round-36/S053.txt`.
  - **Verification:** Inspection confirms that in all three snapshots, `"PSIRT Services Framework"` appears exclusively at line 201 as part of FIRST.org's standard site-wide navigation menu (`Service FrameworksCSIRT Services Framework\nPSIRT Services Framework\nInformation Exchange Policy (IEP)...`), identical to line 201 of `S098.candidate.txt`. Zero substantive text or knowledge citations exist in any snapshot.

---

## 3. Claim C1 Screen: Sibling Lanes Scan & Signal Handling Claims

### 3.1 Sibling Lanes Scan (`kengaku-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`)
- Scanned for `figure-audit.py`, `run_derive`, `upstream_stale`, and `derive-signal`.
- `kengaku-shokunin`: Contains only one-off scratch scripts (`derive_spans.py`, etc.) and a reference in `.ufo/waves/round-78/w1/ConnectorR78.md:2334` pointing to kasegi's `figure-audit.py` as an external unrelated instrument.
- `kotodama-shokunin` & `kumitate-shokunin`: Contain zero derive-gate or figure-audit equivalents.
- **Verdict:** `SCOPE CLEAR`.

### 3.2 Held Lane Records on Signal Handling
- Grep for `signal` across `SKILL.md` and `corpus/instruments/figure-audit.py`:
  - `SKILL.md:1224`: *"Negative upstream signal statuses remain ignored; a stale group stops later && groups."*
  - `SKILL.md:1236`: *"Negative-signal partial-output and PATH-shadowed grep residuals remain open."*
  - `corpus/instruments/figure-audit.py:44`: *"...negative signal statuses remain ignored."*
  - `corpus/instruments/figure-audit.py:82`: *"Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored."*
  - `corpus/instruments/figure-audit.py:449`: `run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))`
- **Verdict:** No held lane record claims signal handling for this gate. Current bytes explicitly document negative signal statuses as ignored and residual.

---

## 4. UFO-FSD Connector Move: Compatible Synthesis Across Round Proposals

### 4.1 Identified Contradiction
The round specification assumes that all signal-killed probes at base master `a283189b` were "false greens" that read `ok`.
However, empirical measurements by `ExecSignalProbes` (`probes-base.txt`) and `ExecSignalMutants` (`mutbat-base.txt`) revealed:
```
BASE p3-final-signal verdict=stale reason=derive-exit--15
```
Because `kill.py` in Probe P3 (`cat g.txt | python3 corpus/instruments/kill.py`) is the **final stage**, base `figure-audit.py:116-118` executes:
```python
status = processes[-1].returncode
if status != 0:
    return None, out, "derive-exit-%d" % status
```
Since `status = -15 != 0`, the final-stage check fired immediately and returned `derive-exit--15` with exit 1!
Thus, **Probe P3 was ALREADY stale at base master**. It was never `ok` (exit 0). The defect on P3 was purely a malformed label (`derive-exit--15` instead of `derive-signal-15`).

### 4.2 Proposed Bounded Move
1. **Harmonize `c1-signal-probes.py` Mode Base:**
   Pin `--mode base` expectation for P3 to: `audit_exit=1, verdict=stale, reason=derive-exit--15`.
   This allows `c1-signal-probes.py --mode base` to exit 0 (`probes=6 failures=0`) against base master `a283189b`, reflecting observed base reality and preventing a false failure in the committed verification driver.
2. **Align Driver Measurements in `verify-r65.py`:**
   - Measurement 1 (`collector-base`): Asserts base behavior (P1/P2 = ok false-green; P3 = stale with malformed `derive-exit--15`; P4/P5/P6 = ok). Passes exit 0 on base master.
   - Measurement 2 (`collector-candidate`): Asserts candidate behavior (P1/P2 = stale with `derive-upstream-signal-N`; P3 = stale with `derive-signal-15`; P4/P5/P6 = ok). Passes exit 0 on candidate.
   - This cleanly separates the **status-flip discriminant** (P1/P2: ok -> stale) from the **label-format discriminant** (P3: `derive-exit--15` -> `derive-signal-15`).
3. **Selftest Case Renaming Documentation:**
   In `ExecSignalGate/figure-audit.py`, selftest case `upstream-python-signal-ignored` was flipped from `exit 0` to `exit 1` (`derive-upstream-signal-15`), but kept its now-contradictory name `"upstream-python-signal-ignored"`. Retain this id for lineage as noted by `ExecSignalGate`, but record the semantic flip explicitly in the lesson and scorecard.
4. **Substrate Requirement for Python SIGPIPE:**
   Document that Python subprocesses default to ignoring SIGPIPE, converting broken pipes into `BrokenPipeError` (exit code 1, which `upstream_stale` treats as stale `derive-upstream-exit-1`). Non-final Python producers must explicitly set `signal.signal(signal.SIGPIPE, signal.SIG_DFL)` (as done in `pipe.py` and `bigwriter.py`) to exhibit native SIGPIPE (-13) and test the benign non-final SIGPIPE branch.

### 4.3 Axes Impact & Verification
- **Improves `depth:verifiability` (Axis 1):** Resolves the base collector failure, ensuring `verify-r65.py` runs all measurements deterministically against committed bytes.
- **Protects `coverage` (Axis 2):** Preserves full 6-probe discrimination across both upstream and final-stage signal deaths.
- **Harms zero axes.**
- **Verification:**
  - `python3 c1-signal-probes.py --instrument corpus/instruments/figure-audit.py --mode base` -> exit 0.
  - `python3 c1-signal-probes.py --instrument .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py --mode candidate` -> exit 0.
  - `python3 signal-mutbat.py` on candidate -> 4/4 killed; on base -> 4/4 survivors (limb absent).
  - `verify-r65.py` -> 8/8 measurements pass.

---

## 5. Verification Commands Run by ScopeF44

All commands run directly on the host, producing receipts in `/fast/scratch/hyaku/kasegi-r65/ScopeF44`:
1. `git rev-parse HEAD` -> `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`.
2. Duplicate URL check against `corpus/SOURCES.md`: 0 matches.
3. Pre-freeze screen `grep -ric` counts across README, SOURCES, PROVINCE, SKILL, and 81 knowledge files.
4. Downstream-consumer sweep over `corpus/source-snapshots/` for candidate key terms.
5. Sibling scans across `kengaku-shokunin`, `kotodama-shokunin`, and `kumitate-shokunin` -> `SCOPE CLEAR`.
6. Held lane signal claims grep across `SKILL.md` and `corpus/instruments/figure-audit.py`.
7. Scratch directory `/fast/scratch/hyaku/kasegi-r65/ScopeF44` cleaned on exit.
