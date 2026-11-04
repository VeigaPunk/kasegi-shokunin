# ScopeF45 — Scoped Findings Receipt (Kasegi Round 67 Wave 1)

- **Seat:** `ScopeF45` (UFO-FSD connector, leaf member)
- **Lane Root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Base Revision:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`
- **Assigned Axes:** `depth:verifiability`, `coverage`
- **Milestone:** Predata multi-head SIGPIPE input-completeness repair + F45 PSIRT maturity screening
- **Report Trailer Path:** `.ufo/waves/round-67/w1/ScopeF45.md`

---

## 1. Executive Summary & Deliverables

This seat performed the read-only cross-surface sibling/consumer screen for Claim C2 (Frontier F45, FIRST's PSIRT Maturity document) and executed the UFO-FSD connector synthesis analyzing second-order effects across Claim C1 (multi-head SIGPIPE input-completeness gate repair) and Claim C2.

All checks were executed strictly read-only outside this seat's directories, adhering to leaf member invariants (zero subagent dispatch, zero production edits, zero git/jj mutations, zero fleet-root modifications, and scratch contained entirely within `/fast/scratch/hyaku/kasegi-r67/ScopeF45/`).

### Deliverables Written
1. `.ufo/waves/round-67/w1/ScopeF45.md` — This primary report.
2. `.ufo/waves/round-67/w1/ScopeF45/raw-sweep.txt` — Raw sweep receipt capturing every scanned hit across all 205 repository files.
3. `.ufo/waves/round-67/w1/ScopeF45/hit-evaluations.tsv` — Tab-separated database of all 59 hits with path, line number, matched terms, category, holding decision, and grounding justification.
4. `.ufo/waves/round-67/w1/ScopeF45/screen.md` — Extended sibling/consumer screen and candidate profile analysis.

---

## 2. Claim C2 Screen: Frontier F45 Candidate

### 2.1 Candidate Profile
- **Candidate Name:** FIRST PSIRT Maturity Document
- **Candidate URL:** `https://www.first.org/standards/frameworks/psirts/psirt_maturity_document`
- **Companion PDF:** `https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf`
- **Assigned Frontier ID:** `F45`
- **Proposed Source ID:** `S100` (registry highest row at base is S099)
- **Normalized Text Snapshot SHA256:** `cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f` (478 lines, 59,068 bytes, body L216–L464)
- **Companion PDF SHA256:** `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f` (644,190 bytes, 29 pages, creation date 2018-12-06)

---

### 2.2 Sibling / Consumer Sweep Results

A comprehensive sweep was conducted across all required surfaces:
- `corpus/knowledge/*.md` (81 files)
- `corpus/SOURCES.md` (1 file)
- `corpus/README.md` (1 file, including all frontier rows F01–F44)
- `SKILL.md` (1 file)
- `PROVINCE.md` (1 file)
- `corpus/source-snapshots/**` (120 files across 34 snapshot directories)

for the four specified terms:
`'maturity'`, `'PSIRT maturity'`, `'capability level'`, `'self-assessment'`.

**Total files scanned:** 205  
**Total matches found:** 59 hits  

#### Summary of Matches by Surface:
| Surface | Files Scanned | Total Hits | Holds Maturity-Level Ground? |
|---|---|---|---|
| `corpus/knowledge/` | 81 | 1 | **NO** (explicit boundary sentence in `first-psirt-services-framework.md:45`) |
| `corpus/SOURCES.md` | 1 | 2 | **NO** (L242 receipt note, L244 unadmitted lead annotation) |
| `corpus/README.md` | 1 | 0 | **NO** (zero matches across all frontier rows F01–F44) |
| `SKILL.md` | 1 | 0 | **NO** (zero matches) |
| `PROVINCE.md` | 1 | 0 | **NO** (zero matches) |
| `corpus/source-snapshots/` | 120 | 56 | **NO** (CVSS metrics, FIRST site navigation, Disclose.io, CSAF, CVE schemas, S098 glossary) |

---

### 2.3 Detailed Hit-by-Hit Ground Decisions

1. **`corpus/knowledge/first-psirt-services-framework.md:45` `[maturity, PSIRT maturity]`**
   - *Text:* `"- **Maturity is a glossary definition, not a level ladder.** S098's only maturity *definition* is the glossary entry at L1510... FIRST publishes a separate maturity document; it was opened only for boundary screening this round and is recorded as a lead, not admitted, so "FIRST defines PSIRT maturity levels" is not an F44 claim."`
   - *Decision:* **DOES NOT HOLD.** This is an explicit negative boundary rule confirming that F44/S098 does *not* claim maturity levels and designating the maturity document as an unadmitted lead.

2. **`corpus/SOURCES.md:242` `[maturity]`**
   - *Text:* Historical screening note for round-65 S098 recording 0 pre-existing held hits.
   - *Decision:* **DOES NOT HOLD.** Screening receipt text.

3. **`corpus/SOURCES.md:244` `[maturity, PSIRT maturity]`**
   - *Text:* `"- Lead added (round 65, not admitted): FIRST PSIRT Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document — opened only for boundary screening this round... A future admission needs its own source id, manifest and entry; S098 states no maturity levels."`
   - *Decision:* **DOES NOT HOLD.** Explicit lead note certifying that the document was opened *only* for boundary screening in round 65, was explicitly **not admitted**, and holds separate ground from S098.

4. **`corpus/source-snapshots/round-24/S001.txt` (6 hits) & `S002.txt` (10 hits)**
   - *Lines 122–124:* FIRST site navigation menu links to `"CTI Maturity model - Stage 1/2/3"`.
   - *Lines 362, 532, 536 (S001); 655, 668, 672, 679, 683, 1051, 1147 (S002):* CVSS v4 Exploit Maturity (E) threat metric.
   - *Decision:* **DOES NOT HOLD.** FIRST site chrome and vulnerability exploitability threat scoring metrics.

5. **`corpus/source-snapshots/round-24/S006.txt` (3 hits)**
   - *Lines 60, 64:* Safe harbor adoption as an indicator of organizational "cybersecurity maturity".
   - *Line 72:* Mention of Disclose.io / Bugcrowd "Bug Bounty Maturity Framework".
   - *Decision:* **DOES NOT HOLD.** External bug bounty context and generalized organizational security posture prose.

6. **`corpus/source-snapshots/round-24/S010.txt` (1 hit)**
   - *Line 245 `[capability level]`:* SWE-bench evaluation paper discussion of LLM reasoning vs. "true capability level of the models".
   - *Decision:* **DOES NOT HOLD.** Model benchmark evaluation context.

7. **`corpus/source-snapshots/round-36/S053.txt` (3 hits)**
   - *Lines 122–124:* FIRST site navigation menu links to CTI Maturity model.
   - *Decision:* **DOES NOT HOLD.** Site navigation chrome.

8. **`corpus/source-snapshots/round-37/S054.txt` (1 hit)**
   - *Line 175:* CERT/CC SSVC tutorial referencing CVSS "Exploit Maturity".
   - *Decision:* **DOES NOT HOLD.** Prioritization metric comparison.

9. **`corpus/source-snapshots/round-38/S055.txt` (2 hits)**
   - *Line 4206 `[capability level]`:* CSAF target profile capabilities ("single minimum capability level for every target").
   - *Line 5118:* JSON schema pointer `/vulnerabilities[]/scores[]/cvss_v3/exploitCodeMaturity`.
   - *Decision:* **DOES NOT HOLD.** Advisory document format target specification and CVSS schema pointer.

10. **`corpus/source-snapshots/round-42/S064.txt` (9 hits) & `round-49/S078.txt` (9 hits)**
    - Schema definitions for CVSS `exploitMaturityType` and `exploitCodeMaturityType`.
    - *Decision:* **DOES NOT HOLD.** Data format schema definitions.

11. **`corpus/source-snapshots/round-65/S098.txt` (11 hits)**
    - *Lines 122–124:* FIRST site navigation menu links to CTI Maturity model.
    - *Lines 274, 403:* Colloquial prose ("continue to mature and scale", "maturity lifecycle of the PSIRT").
    - *Line 675:* General measurement note ("Maturity of a PSIRT may be measured via the availability and efficiency of the difference services prescribed in this service area").
    - *Line 1499:* Glossary definition of Actions ("at varying levels of detail / maturity").
    - *Line 1510:* Glossary definition: `"Maturity - how effectively an organization executes a particular capability within the mission and authorities of the organization. It is a level of proficiency attained either in actions or tasks or in an aggregate of functions or services."`
    - *Lines 1553, 1554, 1568 `[maturity, PSIRT maturity]`:* Site footer navigation links to external documents ("PSIRT Maturity, HTML", "PSIRT Maturity, PDF Format").
    - *Decision:* **DOES NOT HOLD.** S098 contains zero maturity levels (measured `grep -cE 'Maturity Level|Level [123]'` = 0), no capability tiers, and no self-assessment framework.

12. **`corpus/source-snapshots/round-65/manifest.json:3` (1 hit)**
    - Note recording that S098's only maturity definition sits at glossary line 1510.
    - *Decision:* **DOES NOT HOLD.** Snapshot manifest metadata.

---

### 2.4 Ground Status: Genuinely New (Uncovered)

**Definitive Finding:** F45's ground is **GENUINELY NEW and UNADMITTED**.
Not a single line of held knowledge, index, or source snapshots holds PSIRT maturity levels, evolutionary progression models, or maturity-level assessment checklists.

The FIRST PSIRT Maturity Document introduces:
1. **The 3-Tier PSIRT Operational Maturity Model:**
   - **Level 1 (Basic):** Establishing core foundational viability — executive sponsorship, budget, initial policies referencing ISO 29147/30111, dedicated intake channels (email/PGP/web form), baseline qualification, basic analysis/triage, remediation facilitation, and advisory publication with finder credit.
   - **Level 2 (Intermediate):** Internally-focused, trained reactive operations — formal "Bug Bar" qualification thresholds, repeat-finder tracking databases, internal isolated reproduction capabilities, comprehensive product Bill of Materials (BOM) tracking, SDLC integration hooks, CWE weakness tagging, and cross-industry advance coordination.
   - **Level 3 (Advanced):** Proactive operations and continuous adaptation — predicting issues based on historical metrics, KPIs (CSAT, Net Promoter Score, patch SLOs/SLAs), external stakeholder engagement, upstream component governance, active variant hunting, priority triage bypass for proven finders, secure reproduction sandboxes, and developer training.
   - **Beyond Level 3:** Continuous maturity evolution and community leadership.
2. **Operational Capability Progression:** Concrete guidance on transforming a team from ad-hoc reactive firefighting into proactive prevention and variant hunting.
3. **Maturity Checklists (Annex 7):** Concrete checklists for Level 1, Level 2, and Level 3 across Operational Foundations, Stakeholder Ecosystem Management, Vulnerability Discovery, Vulnerability Triage, Remediation, Vulnerability Disclosure, and Training & Education.
4. **Organizational Governance Templates (Annexes 3–6):** Real-world PSIRT mission statements from industry exemplars (Microsoft MSRC, IBM, Dell, Brocade, Red Hat, Honeywell) and templates for charters and policies.

---

### 2.5 Consumer Confusion Analysis & Narrowing Sentences

To prevent researcher and downstream consumer confusion, F45 must be differentiated from adjacent held entries:

1. **`F44` (Source `S098`): FIRST PSIRT Services Framework v1.1**
   - *File:* `corpus/knowledge/first-psirt-services-framework.md`
   - *Why Confused:* Both are FIRST standards documents governing PSIRTs and sharing the same six service area names.
   - *Narrowing Sentence:*
     > "Read F44 as the horizontal service catalogue defining *what* a PSIRT does across 28 services and 84 functions without levels; read F45 as the vertical developmental maturity ladder defining *when* and *in what evolutionary order* (Level 1 Basic, Level 2 Intermediate, Level 3 Advanced) a team selects, operationalizes, and benchmarks those services."

2. **`F10` (Source `S040`): Cisco PSIRT Policy & Vendor-Side Disclosure Commitments**
   - *File:* `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
   - *Why Confused:* Both cover vendor PSIRT policies and reference ISO/IEC 29147.
   - *Narrowing Sentence:*
     > "Read F10 as one vendor's outward-facing public policy commitments; read F45 as the community-standard maturity model and internal charter/policy drafting framework across organizational development stages."

3. **`F13` (Sources `S043`, `S044`): Program Severity Ladders & Reward Scales**
   - *File:* `corpus/knowledge/program-severity-ladders-and-reward-scales.md`
   - *Why Confused:* Both define tiered levels or hierarchical ladders.
   - *Narrowing Sentence:*
     > "Read F13 as vulnerability impact and payout scales (bug severity tiers Critical through Low); read F45 as team operational capability tiers (operational maturity levels Basic through Advanced), not bug severity."

4. **`F43` (Source `S095`): CERT/CC CVD Phase-to-Role Matrix**
   - *File:* `corpus/knowledge/cert-guide-cvd-phases-and-validation.md`
   - *Why Confused:* Both structure vulnerability handling across sequential phases.
   - *Narrowing Sentence:*
     > "Read F43 as inter-organizational phase allocation across five stakeholder roles (Finder, Vendor, Coordinator, Deployer, Public); read F45 as intra-organizational operational maturity progression within a single vendor's product security team."

---

### 2.6 Province Coverage Analysis

Under `PROVINCE.md`:
- **Domain (lines 3, 29–30):** *"bounty & security research — scopes ~/Projects/bounties, program rules, claim packages... The line-3 domain comprises program rules, scopes, and claim packages; the core also covers triage and claim gates, and submission/disclosure packaging."*
- **Frontier (lines 37–40):** *"General practice that governs every program is indexed in corpus/README.md under Frontier F01–F10... F11–F44."*

**Verdict: IN PROVINCE.**
The FIRST PSIRT Maturity Document directly governs receiving-side triage gates, bug bars (Level 2), report qualification criteria (Level 1), repeat-finder trust channels (Level 2), and expedited analysis paths (Level 3 priority bypass for proven researchers). This operational capability architecture directly dictates the requirements for valid, claimable bounty submissions and claim packaging. It is documentation only; live-target testing remains refused.

---

## 3. UFO-FSD Connector Synthesis: Bounded Move Across Round Proposals

### 3.1 Observed Contradictions Across Wave Evidence

#### Contradiction 1: Native Substrate Race Condition on Multi-Input SIGPIPE
- **Claim Premise:** "the stage dies of SIGPIPE before reaching a later named operand, so a green FIG line reports success on a world where a named input was never read."
- **Host Measurement (`RevengerMultiHead` & `ExecMultiHeadGate`):**
  1. For `wc -l big.txt missing.txt | head -n 1`, `wc` opens both operands, attempts to read `missing.txt`, outputs its error message to `stderr`, and only then dies of `SIGPIPE` when writing totals to the closed pipe.
  2. The process returncode races natively between `1` (if error exit wins) and `-13` (if SIGPIPE wins).
  3. In reversed operand order (`cut missing.txt big.txt | head -n 1`), `cut` reports `missing.txt` on `stderr` and *then* dies of `SIGPIPE` (`-13`).
  4. For `grep x xlines.txt missing.txt | head -n 1` (P11), `ExecMultiHeadGate` observed that grep can also race between `-13` and `1` (missing operand error winning the race).
  5. In all cases, `figure-audit.py:run_derive` redirects `stderr` to an anonymous `tempfile.TemporaryFile()` that is never read or checked; therefore, any `-13` returncode completely masks whatever error was logged to `stderr`.

#### Contradiction 2: Web Substrate Volatility on F45 Candidate Capture
- **Screening & Lead Record:** `corpus/SOURCES.md:244` recorded a raw HTML digest `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e` from a single round-65 fetch.
- **Empirical Measurement (`ScoutF45`):** `first.org` injects dynamic per-response CSP nonces into the raw HTML of `psirt_maturity_document`. Raw HTML SHA256 varies on every live fetch (5 fetches yielded 3 distinct nonces and 5 distinct raw digests, despite identical 82,978 byte length).
- In contrast, the normalized text snapshot extracted by `capture-source.py` (`S100.txt`) produces a 100% stable SHA256 (`cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f`, 478 lines, 59,068 bytes), and the official companion PDF (`FIRST_PSIRT_Maturity_Document.pdf`) is completely byte-identical and byte-stable with SHA256 `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`.

---

### 3.2 The Proposed Bounded Move

**Move:** Unify the verification and integrity contract across both Claim C1 and Claim C2 around deterministic, race-immune criteria:

1. **For Claim C1 (Driver & Probe Verification):**
   - Bind all verification oracles (`figure-audit.py` selftest, `probes.py`, and `verify.py`) to an **any-of stale reason set** for racing multi-input probes (`P10` `wc` and `P11` `grep`):
     - `P10` accepts either `derive-upstream-exit-1` or `derive-upstream-signal-13`.
     - `P11` accepts either `derive-upstream-exit-1` or `derive-upstream-signal-13` (or `derive-upstream-exit-2` depending on grep implementation).
   - The discriminant that falsifies the base gate and proves candidate correctness is the **binary status flip**:
     - At base: `cut`, `wc`, `grep` read `ok` (rc 0) while operands are unread or errors are masked.
     - On candidate: all multi-operand stages read `stale` (rc 1) under both race faces.
   - This decouples test suite stability from host kernel scheduler timing without relaxing the safety invariant.

2. **For Claim C2 (Source Integrity & Registry Pinning):**
   - In `corpus/SOURCES.md`, `manifest.json`, and `corpus/README.md`, anchor S100's durable integrity pin to:
     - The normalized text snapshot SHA256 (`cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f`), which is completely reproducible across tools and fetches.
     - The official companion PDF SHA256 (`f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f`), which serves as the byte-stable upstream distribution artifact.
   - Document the raw HTML CSP nonce variance as web-substrate behavior in the manifest note, explicitly preventing false-positive integrity check failures in future re-harvest verification scripts.

---

### 3.3 Affected Axes & Second-Order Effects

- **Improves `depth:verifiability` (Axis 1):**
  - Eliminates intermittent test suite flakiness in C1 committed verification driver runs caused by kernel pipe scheduling races on multi-input `wc` and `grep`.
  - Ensures C2 source integrity checks reproduce deterministically across independent fetches, protecting the lane against false-positive hash drift alarms.
- **Protects `coverage` (Axis 2):**
  - Confirms F45 is completely unheld and eligible for admission as S100, expanding the lane's frontier with a comprehensive PSIRT operational maturity model.
  - Maintains strict boundary narrowing against F44, F10, F13, and F43.
- **Harms Zero Axes:**
  - Does not weaken the derive gate: every masked multi-input pipeline is strictly refused (rc 1 stale) under candidate.
  - Does not weaken provenance: both normalized text and companion PDF are cryptographically pinned.

---

### 3.4 Verification Commands Run

All checks were executed directly on the host from scratch `/fast/scratch/hyaku/kasegi-r67/ScopeF45/`:
1. `python3 -B sweep.py` — Scanned 205 repository files for the 4 terms; identified 59 hits.
2. `python3 -B generate_tsv.py` — Formatted and evaluated all 59 hits into `ScopeF45/hit-evaluations.tsv` and copied `ScopeF45/raw-sweep.txt`.
3. Verified zero matches for terms in `corpus/README.md`, `SKILL.md`, `PROVINCE.md`.
4. Verified F44 knowledge boundary in `corpus/knowledge/first-psirt-services-framework.md:45`.
5. Checked candidate manifest and capture in `.ufo/waves/round-67/w1/ScoutF45/manifest.json`.
6. Verified candidate gate selftest: `cases=71 failures=0, exit 0` on candidate `figure-audit.py`.
7. Scratch directory `/fast/scratch/hyaku/kasegi-r67/ScopeF45/` cleaned up prior to yield.
