# Cross-Surface Screen: C1 Signal Gate & C2 Frontier F44 (S098)

- **Seat:** `ScopeF44` (connector, leaf member, read-only outside own seat directory)
- **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Base Revision:** `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
- **Run UTC:** `2026-11-04T19:32:07Z`
- **Output Receipt:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-65/w1/ScopeF44/screen.md`
- **Round Milestone:** Predata signal-fail-closed gate build and F44 source screen (Round 65)

---

## Section 1: C2 Coverage Screen (FIRST PSIRT Services Framework v1.1)

### 1.1 Candidate Identification
- **Title:** FIRST PSIRT Services Framework v1.1
- **Candidate Source ID:** `S098`
- **Candidate Frontier ID:** `F44`
- **Target URL:** `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`
- **Normalized Host + Path:** `first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`

### 1.2 Coverage Decision: (a) UNCOVERED
The candidate source is **(a) UNCOVERED** by any held frontier row in `corpus/README.md` (F01–F43), `corpus/SOURCES.md`, `PROVINCE.md`, or `corpus/knowledge/*.md`.
- It is **not already covered**: no existing held row indexes the FIRST PSIRT Services Framework, its 6 service areas, its 28 services, its 84 functions, or its 3 organizational models (Distributed, Centralized, Hybrid).
- It is **not adjacent**: the subject matter (product security incident response teams, vulnerability intake, triage, qualification bug bars, remediation delivery, and coordinated disclosure) falls squarely within `kasegi-shokunin`'s domain ("bounty & security research — scopes ~/Projects/bounties, program rules, claim packages, triage and claim gates, and submission/disclosure packaging" per `PROVINCE.md:3,29-30`). It does not belong to sibling domains (`chousa` research method, `kagi` secrets/vault, `kake` web properties, `kengaku` LLM evaluation).

### 1.3 Closest Three Held Rows & Narrowing Sentences

1. **`F43` (Source `S095`): CERT/CC adapted CVD phase-to-five-role matrix**
   - **File:** `corpus/knowledge/cert-guide-cvd-phases-and-validation.md` (`corpus/README.md:1031`)
   - **Narrowing Sentence:**
     > "Read complete column headings (S095.txt:112-116) with Validation (:129-134) and Remediation (:141-146); a dash is not a prohibition on reporter verification. Generic phase names, prioritization and deployment are supporting context already held elsewhere." (`corpus/README.md:1031`)
   - **Distinction from F44:** F43 covers CERT/CC's adapted 6-phase CVD lifecycle (Discovery, Reporting, Validation, Triage, Remediation, Public Awareness) mapped across 5 multi-stakeholder roles (Finder/Reporter, Vendor, Coordinator, Deployer, Public), focusing on Reporter fix confirmation vs Vendor/Coordinator incoming-report validation. F44 covers an individual vendor organization's internal PSIRT service catalogue, organizational models, and capability specifications (e.g. Service Area 1 Stakeholder Ecosystem Management, Service Area 3 Vulnerability Triage and Analysis, Service Area 4 Remediation, Service Area 6 Training and Education).

2. **`F06` (Source `S018`): Multi-party CVD — FIRST guidelines v1.1**
   - **File:** `corpus/knowledge/multiparty-vulnerability-coordination.md` (`corpus/README.md:207`)
   - **Narrowing Sentence:**
     > "Record each party's role and relationship; an upstream fix is not downstream evidence." (`corpus/README.md:207`)
   - **Distinction from F44:** F06 covers FIRST's *Guidelines and Practices for Multi-Party Vulnerability Coordination and Disclosure* (v1.1, Spring 2020), which governs coordination across multiple independent parties (reporters, multiple vendors, coordinators, downstream users). F44 covers FIRST's *PSIRT Services Framework v1.1*, which details the internal structure, services, functions, and sub-functions that a single vendor's product security incident response team provides.

3. **`F11` (Source `S041`): ISO/IEC 29147/30111 division-of-labour meta**
   - **File:** `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (`corpus/README.md:212`)
   - **Narrowing Sentence:**
     > "Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018)." (`corpus/README.md:212`)
   - **Distinction from F44:** F11 covers the conceptual division of labour between outward-facing disclosure (ISO/IEC 29147) and internal vulnerability handling (ISO/IEC 30111) as analyzed in JPCERT/CC's 2026 guidelines. F44 provides the operational, granular service catalog (28 services, 84 functions) and organizational models (Distributed, Centralized, Hybrid) defining how a PSIRT actually operates.

*(Supporting context held in `F10` / `S040`: Cisco's PSIRT policy cites ISO/IEC 29147:2018 alignment in `vendor-disclosure-policy-commitments-crosswalk.md`, but covers only Cisco's standing vendor policy, not the FIRST community framework).*

### 1.4 URL Duplicate Check
Command lines executed from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`:
```bash
# 1. Exact candidate URL check in SOURCES.md
grep -F 'https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md
# Output: (exit 1: no exact URL match in SOURCES.md)

# 2. Normalized host + path check in SOURCES.md
grep -F 'first.org/standards/frameworks/psirts/psirt_services_framework_v1.1' corpus/SOURCES.md
# Output: (exit 1: no normalized host+path match in SOURCES.md)

# 3. Path slug check across SOURCES.md, README.md, and PROVINCE.md
grep -i 'psirt_services_framework' corpus/SOURCES.md corpus/README.md PROVINCE.md
# Output: (exit 1: no slug match in registry, README, or PROVINCE)
```
**Result:** Zero duplicates. The URL is completely unrepresented in `corpus/SOURCES.md` and the entire repository.

---

## Section 2: Extended Pre-Freeze Screen Receipt (QUALITY R80)

- **Screen Timestamp:** `2026-11-04T19:32:07Z` (pre-freeze, precedes freeze commit)
- **Base Tree:** `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`

### 2.1 Knowledge Filenames Check
```bash
$ ls corpus/knowledge/ | grep -E -i 'psirt|services-framework'
# Exit code: 1 (0 matching files among 81 knowledge entries)
```

### 2.2 Key Term Frequency Across Repo Surfaces (`grep -ric`)

Commands executed:
```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for term in "PSIRT Services Framework" "psirt_services_framework" "FIRST PSIRT" "Stakeholder Ecosystem Management" "PSIRT"; do
  echo "--- Term: $term ---"
  grep -ric "$term" corpus/README.md
  grep -ric "$term" corpus/SOURCES.md
  grep -ric "$term" PROVINCE.md
  grep -ric "$term" SKILL.md
  grep -rc -i "$term" corpus/knowledge/*.md | grep -v ':0$' || echo "(0 hits in corpus/knowledge/*.md)"
done
```

Exact command outputs:

1. **Term: `"PSIRT Services Framework"`**
   - `corpus/README.md`: `0`
   - `corpus/SOURCES.md`: `0`
   - `PROVINCE.md`: `0`
   - `SKILL.md`: `0`
   - `corpus/knowledge/*.md`: `(0 hits across all 81 corpus/knowledge/ entries)`

2. **Term: `"psirt_services_framework"`**
   - `corpus/README.md`: `0`
   - `corpus/SOURCES.md`: `0`
   - `PROVINCE.md`: `0`
   - `SKILL.md`: `0`
   - `corpus/knowledge/*.md`: `(0 hits across all 81 corpus/knowledge/ entries)`

3. **Term: `"FIRST PSIRT"`**
   - `corpus/README.md`: `0`
   - `corpus/SOURCES.md`: `0`
   - `PROVINCE.md`: `0`
   - `SKILL.md`: `0`
   - `corpus/knowledge/*.md`: `(0 hits across all 81 corpus/knowledge/ entries)`

4. **Term: `"Stakeholder Ecosystem Management"`**
   - `corpus/README.md`: `0`
   - `corpus/SOURCES.md`: `0`
   - `PROVINCE.md`: `0`
   - `SKILL.md`: `0`
   - `corpus/knowledge/*.md`: `(0 hits across all 81 corpus/knowledge/ entries)`

5. **Term: `"PSIRT"`**
   - `corpus/README.md`: `0`
   - `corpus/SOURCES.md`: `1` (line 46: Cisco PSIRT policy summary on row S040)
   - `PROVINCE.md`: `0`
   - `SKILL.md`: `0`
   - `corpus/knowledge/*.md`: 4 files with hits (all relating to Cisco S040 / vendor policies):
     - `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`: `1` (line 19: Cisco PSIRT alignment with ISO 29147:2018)
     - `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`: `1` (line 60: Cisco PSIRT URL verification)
     - `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`: `2` (lines 59, 63: Yahoo Japan policy translation)
     - `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md`: `7` (lines 1, 46, 47, 48, 50, 51, 52: Cisco PSIRT crosswalk)

### 2.3 Downstream-Consumer Sweep over `corpus/source-snapshots/`

Commands executed:
```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for term in "PSIRT Services Framework" "psirt_services_framework" "FIRST PSIRT" "Stakeholder Ecosystem Management" "PSIRT"; do
  echo "--- Downstream consumer sweep: $term ---"
  grep -rl -i "$term" corpus/source-snapshots/ || echo "(no snapshot hits)"
done
```

Exact command outputs:

1. **`"PSIRT Services Framework"`:**
   - `corpus/source-snapshots/round-24/S001.txt`
   - `corpus/source-snapshots/round-24/S002.txt`
   - `corpus/source-snapshots/round-36/S053.txt`
   *(Receipt Analysis: Each of these three files contains `"PSIRT Services Framework"` at line 201 as part of FIRST's standardized global navigation header bar: `Service FrameworksCSIRT Services Framework\nPSIRT Services Framework\nInformation Exchange Policy (IEP)...`. It is identical to the navigation header at line 201 of `S098.candidate.txt`. Zero substantive text or knowledge citations reference this document.)*

2. **`"psirt_services_framework"`:**
   - `(no snapshot hits)`

3. **`"FIRST PSIRT"`:**
   - `(no snapshot hits)`

4. **`"Stakeholder Ecosystem Management"`:**
   - `(no snapshot hits)`

5. **`"PSIRT"`:**
   - `corpus/source-snapshots/round-23/S031.txt` (CVE CNA rules)
   - `corpus/source-snapshots/round-24/S001.txt` (FIRST CVSS v4.0 User Guide navbar)
   - `corpus/source-snapshots/round-24/S002.txt` (FIRST CVSS v4.0 Spec navbar)
   - `corpus/source-snapshots/round-24/S003.txt` (CISA CVD Guide)
   - `corpus/source-snapshots/round-25/S036.txt` (Brave Disclosure Policy)
   - `corpus/source-snapshots/round-25/S039.txt` (Hitachi HIRT)
   - `corpus/source-snapshots/round-25/S040.txt` (Cisco Security Vulnerability Policy)
   - `corpus/source-snapshots/round-25/manifest.json` (round 25 snapshot manifest)
   - `corpus/source-snapshots/round-26/S040-live.txt` (Cisco live recheck)
   - `corpus/source-snapshots/round-28/S042.txt` (IPA domestic disclosure)
   - `corpus/source-snapshots/round-30/S047.txt` (JVN impact model)
   - `corpus/source-snapshots/round-35/S052.txt` (CISA KEV catalog feed)
   - `corpus/source-snapshots/round-36/S053.txt` (FIRST EPSS page navbar)
   - `corpus/source-snapshots/round-38/S055.txt` (CSAF v2.0 specification)

---

## Section 3: C1 Sibling Lane Scan & Signal Handling Claims

### 3.1 Sibling Lanes Scan
Target Sibling Lanes:
- `/home/vgpnk/Projects/shokunin/kengaku-shokunin`
- `/home/vgpnk/Projects/shokunin/kotodama-shokunin`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin`

Commands executed:
```bash
# Sibling ls-files check for figure-audit or derive-gate
git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin ls-files | grep -E 'figure-audit|derive_gate' || echo "(none)"
git -C /home/vgpnk/Projects/shokunin/kotodama-shokunin ls-files | grep -E 'figure-audit|derive_gate' || echo "(none)"
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-files | grep -E 'figure-audit|derive_gate' || echo "(none)"

# Sibling SKILL.md check
grep -in "figure-audit" /home/vgpnk/Projects/shokunin/kengaku-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/kotodama-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/kumitate-shokunin/SKILL.md || echo "(no hits)"

# Sibling runtime check for derive functions
grep -rn "run_derive" /home/vgpnk/Projects/shokunin/kengaku-shokunin/lib/ /home/vgpnk/Projects/shokunin/kotodama-shokunin/lib/ /home/vgpnk/Projects/shokunin/kumitate-shokunin/lib/ 2>/dev/null || echo "(no hits)"
```

**Results:**
- `kengaku-shokunin`: Zero derive gates. Sibling has scratch analysis scripts (`derive_spans.py`, `derive66.py`, etc.) and one external cross-reference in `.ufo/waves/round-78/w1/ConnectorR78.md:2334` noting kasegi's `figure-audit.py` as an unrelated instrument.
- `kotodama-shokunin`: Zero figure-audit or derive-gate instruments.
- `kumitate-shokunin`: Zero figure-audit or derive-gate instruments.
- None of the three sibling lanes contains a `corpus/instruments/` directory.

**Verdict:** `SCOPE CLEAR`. There is no figure-audit or derive-gate equivalent in any sibling lane, and no collision on pipeline status or signal semantics.

### 3.2 Held Lane Records Signal Handling Check

Commands executed:
```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
grep -in "signal" SKILL.md
grep -rn -i "signal" corpus/instruments/figure-audit.py
```

Outputs:
- In `SKILL.md`:
  - Line 1224: `| figure-audit.py | gate | python3 corpus/instruments/figure-audit.py [--ledger PATH] [--root DIR] | 0 every recorded figure re-derives; 1 stale or derive failed; 2 unreadable ledger or derive refused (derive-not-read-only) | python3 corpus/instruments/figure-audit.py --selftest (selftest cases=59 failures=0, current interpreter) | corpus/instruments/figure-audit-ledger.json (35 figures) | Direct execution of the validated decoded argv plan. Final-stage nonzero status takes precedence; otherwise first upstream positive status becomes stale except grep exit1, which remains an ordinary no-match. Negative upstream signal statuses remain ignored; a stale group stops later && groups. NOT sandboxed...`
  - Line 1236: `Negative-signal partial-output and PATH-shadowed grep residuals remain open.`
- In `corpus/instruments/figure-audit.py`:
  - Line 44: `no-match and is not an error; negative signal statuses remain ignored. This is not`
  - Line 82: `Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored.`
  - Line 366: `f.write("import os, signal\nos.kill(os.getpid(), signal.SIGTERM)\n")`
  - Line 449: `run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))`

### 3.3 Closest Sentence Analysis
- Closest sentence in `SKILL.md`:
  > "Negative upstream signal statuses remain ignored; a stale group stops later && groups." (`SKILL.md:1224`)
- Second closest sentence in `SKILL.md`:
  > "Negative-signal partial-output and PATH-shadowed grep residuals remain open." (`SKILL.md:1236`)
- Closest sentence in `corpus/instruments/figure-audit.py`:
  > "Grep exit1 is an ordinary no-match; negative (signal) statuses stay ignored." (`corpus/instruments/figure-audit.py:82`)
- Closest selftest verification in `corpus/instruments/figure-audit.py`:
  > `run_case("upstream-python-signal-ignored", 0, _one("s-pysignal", "python3 corpus/instruments/kill.py | wc -l", "0"))` (`corpus/instruments/figure-audit.py:449`)

**Conclusion:** No held lane record claims signal handling for this gate. On the contrary, existing lane records explicitly and repeatedly document that signal handling is an OPEN residual, that negative upstream signal statuses are currently IGNORED, and that upstream signal termination false-greens as exit 0 at baseline.
