# Screen: FIRST PSIRT Maturity Document (Frontier F45 / S100 Candidate)

**Seat:** ScopeF45 (connector, leaf member)  
**Lane Root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`  
**Base Revision:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`  
**Date:** 2026-11-04  
**Assigned Axes:** `depth:verifiability`, `coverage`  

---

## 1. Sweep Methodology & Target Inventory

A read-only sweep was executed across the required repository surfaces for the four terms:
1. `'maturity'`
2. `'PSIRT maturity'`
3. `'capability level'`
4. `'self-assessment'`

### Targets Scanned (205 files total)
- `corpus/knowledge/*.md` (81 files)
- `corpus/SOURCES.md` (1 file)
- `corpus/README.md` (1 file, including all frontier rows F01–F44)
- `SKILL.md` (1 file)
- `PROVINCE.md` (1 file)
- `corpus/source-snapshots/**` (120 files across 34 snapshot directories)

Total hits across all surfaces: **59 hits**.

---

## 2. Path-by-Path Hit Evaluation

Every hit is documented below with path, line number, matched terms, and a decision on whether it holds maturity-level ground.

### 2.1 `corpus/knowledge/` (81 files scanned, 1 hit total)

#### `corpus/knowledge/first-psirt-services-framework.md` (1 hit)
- **Line 45** `[maturity, PSIRT maturity]`:
  > `- **Maturity is a glossary definition, not a level ladder.** S098's only maturity *definition* is the glossary entry at L1510 (how effectively an organization executes a particular capability); the capture also states once how maturity may be measured — L675: "Maturity of a PSIRT may be measured via the availability and efficiency of the difference services prescribed in this service area" (the source's own "difference" typo) — but names no maturity level and no level name (measured: `grep -cE 'Maturity Level|Level [123]'` over the capture = 0). FIRST publishes a separate maturity document; it was opened only for boundary screening this round and is recorded as a lead, not admitted, so "FIRST defines PSIRT maturity levels" is not an F44 claim.`
  - **Holds Maturity-Level Ground?** **NO.**
  - **Evaluation:** This entry is the knowledge document for Frontier F44 (S098, FIRST PSIRT Services Framework v1.1). Line 45 is an explicit boundary restriction stating that S098 does *not* define maturity levels or a maturity ladder. It explicitly references the separate FIRST PSIRT Maturity document as an unadmitted lead from round 65.

*(All other 80 files under `corpus/knowledge/` yielded 0 hits).*

---

### 2.2 `corpus/SOURCES.md` (1 file scanned, 2 hits total)

- **Line 242** `[maturity]`:
  > `...Screening: controls/prefreeze-screen-r65.txt finds 0 held-row/knowledge hits for 'PSIRT Services Framework', 'service area', 'sub-function', 'maturity' and 'bug bar')...`
  - **Holds Maturity-Level Ground?** **NO.**
  - **Evaluation:** Historical screening receipt notation from round 65 recording 0 pre-existing held hits.
- **Line 244** `[maturity, PSIRT maturity]`:
  > `- Lead added (round 65, not admitted): FIRST PSIRT Maturity document at https://www.first.org/standards/frameworks/psirts/psirt_maturity_document — opened only for boundary screening this round (HTTP 200, 82978 bytes, sha256 334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e; text carries "Maturity Level 1 (Basic)" through "Beyond Level 3"). A future admission needs its own source id, manifest and entry; S098 states no maturity levels.`
  - **Holds Maturity-Level Ground?** **NO.**
  - **Evaluation:** Explicit lead entry. It records that the document was opened *only* for boundary screening in round 65 and was explicitly **not admitted**. It confirms that S098 states no maturity levels and reserves admission for a future round with its own source id and manifest.

---

### 2.3 `corpus/README.md` (1 file scanned, 0 hits total)
- `grep -inE 'maturity|capability level|self-assessment' corpus/README.md` -> **0 matches**.
- Frontier rows F01–F44 hold zero maturity-level ground.

---

### 2.4 `SKILL.md` (1 file scanned, 0 hits total)
- `grep -inE 'maturity|capability level|self-assessment' SKILL.md` -> **0 matches**.
- Holds zero maturity-level ground.

---

### 2.5 `PROVINCE.md` (1 file scanned, 0 hits total)
- `grep -inE 'maturity|capability level|self-assessment' PROVINCE.md` -> **0 matches**.
- Holds zero maturity-level ground.

---

### 2.6 `corpus/source-snapshots/` (120 files scanned, 56 hits total)

#### `round-24/S001.txt` (CVSS v4.0 Specification, 6 hits)
- **Lines 122–124** `[maturity]`: FIRST site navigation sidebar links to "CTI Maturity model - Stage 1/2/3".
- **Lines 362, 532, 536** `[maturity]`: CVSS v4 Threat Metric Group metric ("Exploit Code Maturity renamed Exploit Maturity").
- **Holds Maturity-Level Ground?** **NO.** Site navigation chrome and CVSS vulnerability threat scoring metrics.

#### `round-24/S002.txt` (CVSS v4.0 User Guide, 10 hits)
- **Lines 122–124** `[maturity]`: FIRST site navigation sidebar links to "CTI Maturity model".
- **Lines 655, 668, 672, 679, 683, 1051, 1147** `[maturity]`: CVSS v4 Exploit Maturity (E) metric guidance and scoring examples.
- **Holds Maturity-Level Ground?** **NO.** Threat scoring guidance and site navigation.

#### `round-24/S006.txt` (Disclose.io Safe Harbor, 3 hits)
- **Lines 60, 64** `[maturity]`: Prose stating that standardized safe harbor adoption signals "cybersecurity maturity".
- **Line 72** `[maturity]`: Mention of external "Bug Bounty Maturity Framework".
- **Holds Maturity-Level Ground?** **NO.** Colloquial posture description and external bug bounty context, not PSIRT operational maturity levels.

#### `round-24/S010.txt` (SWE-bench / Model Capability Evaluation, 1 hit)
- **Line 245** `[capability level]`: Discussion of expert human vs. LLM "true capability level".
- **Holds Maturity-Level Ground?** **NO.** LLM benchmark performance context.

#### `round-36/S053.txt` (FIRST EPSS, 3 hits)
- **Lines 122–124** `[maturity]`: FIRST site navigation sidebar links to "CTI Maturity model".
- **Holds Maturity-Level Ground?** **NO.** Site navigation chrome.

#### `round-37/S054.txt` (CERT/CC SSVC Overview, 1 hit)
- **Line 175** `[maturity]`: Mention of CVSS "Exploit Maturity" in vulnerability prioritization discussion.
- **Holds Maturity-Level Ground?** **NO.** Vulnerability prioritization comparison.

#### `round-38/S055.txt` (OASIS CSAF v2.0 Standard, 2 hits)
- **Line 4206** `[capability level]`: CSAF target profile capabilities ("single minimum capability level for every target").
- **Line 5118** `[maturity]`: JSON schema path pointer `/vulnerabilities[]/scores[]/cvss_v3/exploitCodeMaturity`.
- **Holds Maturity-Level Ground?** **NO.** Advisory document target format and CVSS metric pointers.

#### `round-42/S064.txt` (CVE JSON 5.1 Format Schema, 9 hits)
- **Lines 1283, 1669, 1670, 2008, 2345, 2346, 2563, 2900, 2901** `[maturity]`: Schema definitions for `exploitMaturityType` (CVSS v4) and `exploitCodeMaturityType` (CVSS v3).
- **Holds Maturity-Level Ground?** **NO.** Data format schema definitions for CVSS metrics.

#### `round-49/S078.txt` (CVE Services API Specification, 9 hits)
- **Lines 7464, 7580, 7581, 7712, 7769, 7770, 7871, 7927, 7928** `[maturity]`: Schema definitions for CVSS exploit maturity metrics.
- **Holds Maturity-Level Ground?** **NO.** API request/response schema definitions.

#### `round-65/S098.txt` (FIRST PSIRT Services Framework v1.1, 11 hits)
- **Lines 122–124** `[maturity]`: FIRST site navigation sidebar links to "CTI Maturity model".
- **Line 274** `[maturity]`: Colloquial use ("As a PSIRT continues to mature and scale...").
- **Line 403** `[maturity]`: Colloquial use ("throughout the lifecycle of an incident or the maturity lifecycle of the PSIRT").
- **Line 675** `[maturity]`: Service area measurement note ("Maturity of a PSIRT may be measured via the availability and efficiency of the difference services prescribed in this service area"). Names no levels or criteria.
- **Line 1499** `[maturity]`: Glossary entry for Actions ("at varying levels of detail / maturity").
- **Line 1510** `[maturity]`: Glossary entry ("Maturity - how effectively an organization executes a particular capability within the mission and authorities of the organization. It is a level of proficiency attained either in actions or tasks or in an aggregate of functions or services.").
- **Lines 1553, 1554, 1568** `[maturity, PSIRT maturity]`: Site footer navigation links to external documents ("PSIRT Maturity, HTML", "PSIRT Maturity, PDF Format").
- **Holds Maturity-Level Ground?** **NO.** As measured in round 65, S098 has `grep -cE 'Maturity Level|Level [123]'` = 0. It contains no maturity levels, no capability ladders, no self-assessment framework, and no level-specific checklists.

#### `round-65/manifest.json` (1 hit)
- **Line 3** `[maturity]`: Manifest note recording that S098's only maturity definition sits at glossary line 1510.
- **Holds Maturity-Level Ground?** **NO.** Snapshot capture metadata note.

---

## 3. Ground Status: Genuinely New & Unadmitted

**Decision: F45's ground is GENUINELY NEW (UNCOVERED).**

Zero held rows, zero knowledge entries, and zero source snapshots in `kasegi-shokunin` hold PSIRT maturity-level ground.
The candidate document (`https://www.first.org/standards/frameworks/psirts/psirt_maturity_document`):
1. Establishes the 3-tier PSIRT operational maturity ladder:
   - **Maturity Level 1 (Basic):** Establishing operational foundations (executive mandate, budget, basic policies referencing ISO 29147/30111), core intake channels, initial report qualification, analysis, remediation facilitation, and advisory disclosure with researcher acknowledgement.
   - **Maturity Level 2 (Intermediate):** Internally-focused, trained reactive operations, repeatable automated builds, internal vulnerability discovery, formal "Bug Bar" qualification, repeat-finder tracking, isolated reproduction capability, product Bill of Materials (BOM) inventory, SDLC hooks, CWE tagging, and cross-industry advance coordination.
   - **Maturity Level 3 (Advanced):** Proactive and consistent operations, predicting issues based on historical trends, KPIs and metrics (CSAT, Net Promoter Score, patch SLOs/SLAs), external stakeholder engagement, upstream component governance, active variant hunting, priority triage bypass for proven finders, secure reproduction sandbox, and developer training.
   - **Beyond Level 3:** Continuous evolution and community leadership.
2. Provides actionable implementation checklists (Annex 7) segmented by maturity level.
3. Provides sample charters, mission statements from major industry teams (Microsoft MSRC, IBM, Dell, Brocade, Red Hat, Honeywell), and policy templates.

---

## 4. Consumer Confusion & Narrowing Sentences

A downstream consumer or researcher would most likely confuse F45 with the following held entries:

### 1. `F44` (Source `S098`): FIRST PSIRT Services Framework v1.1
- **File:** `corpus/knowledge/first-psirt-services-framework.md`
- **Why Confused:** Both documents originate from FIRST, focus specifically on PSIRTs, and organize activities around the same six service areas (Foundations, Stakeholders, Discovery, Triage/Analysis, Remediation, Disclosure).
- **Distinction & Narrowing Sentence:**
  > "Read F44 as the horizontal service catalogue defining *what* a PSIRT does across 28 services and 84 functions without levels; read F45 as the vertical developmental maturity ladder defining *when* and *in what evolutionary order* (Level 1 Basic, Level 2 Intermediate, Level 3 Advanced) a team selects, operationalizes, and benchmarks those services."

### 2. `F10` (Source `S040`): Cisco PSIRT Policy & Vendor-Side Disclosure Commitments
- **File:** `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
- **Why Confused:** Both address vendor PSIRT policies and cite ISO/IEC 29147.
- **Distinction & Narrowing Sentence:**
  > "Read F10 as one vendor's outward-facing public policy commitments; read F45 as the community-standard maturity model and internal charter/policy drafting framework across organizational development stages."

### 3. `F13` (Sources `S043`, `S044`): Program Severity Ladders & Reward Scales
- **File:** `corpus/knowledge/program-severity-ladders-and-reward-scales.md`
- **Why Confused:** Both describe hierarchical "ladders" or tiered levels.
- **Distinction & Narrowing Sentence:**
  > "Read F13 as vulnerability impact and payout scales (bug severity tiers Critical through Low); read F45 as team operational capability tiers (operational maturity levels Basic through Advanced), not bug severity."

### 4. `F43` (Source `S095`): CERT/CC CVD Phase-to-Role Matrix
- **File:** `corpus/knowledge/cert-guide-cvd-phases-and-validation.md`
- **Why Confused:** Both describe phased or staged processes in vulnerability handling.
- **Distinction & Narrowing Sentence:**
  > "Read F43 as inter-organizational phase allocation across five stakeholder roles (Finder, Vendor, Coordinator, Deployer, Public); read F45 as intra-organizational operational maturity progression within a single vendor's product security team."

---

## 5. Province Coverage Analysis

Under `PROVINCE.md`:
- **Domain (lines 3, 29–30):** *"bounty & security research — scopes ~/Projects/bounties, program rules, claim packages... The line-3 domain comprises program rules, scopes, and claim packages; the core also covers triage and claim gates, and submission/disclosure packaging."*
- **Frontier (lines 37–40):** *"General practice that governs every program is indexed in corpus/README.md under Frontier F01–F10... F11–F44."*

**Coverage Verdict: IN PROVINCE.**
The FIRST PSIRT Maturity document directly governs how vendor product security teams establish triage thresholds, bug bars (Level 2), report qualification criteria (Level 1), repeat-finder trust channels (Level 2), and expedited analysis paths (Level 3 priority bypass for proven researchers). This receiving-side capability architecture directly dictates the requirements for valid, claimable bounty submissions and claim packaging. It is documentation only; live-target testing remains refused.
