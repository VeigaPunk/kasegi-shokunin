# ScopeF48 — Round-70 Wave-1 Scope & Sibling-Overlap Report

**Seat:** ScopeF48 (connector, leaf)  
**Round:** kasegi round-70 wave 1  
**Base revision:** `e7c02bddaa32a4a70afb2e6278f108e03dca067c`  
**C2 landing:** `b4afd8a0206b23a69d8cd65d92070cdfcd4680a7`  
**C1 implementation commit:** `c1051749571caf6a0383b15187fc02cdd21785b5`  
**FROZEN claims commit:** `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`  
**Target:** Frontier F48 (GitHub Advisory Database curation semantics, S105)  
**Verdict:** **SCOPE CLEAR**

---

## 1. Held-Ground Overlap Scan (In-Lane)

Scanned `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, and `corpus/knowledge/` for the required terms: `advisory database`, `GHSA`, `reviewed`, `unreviewed`, `malware advisory`, `substitution attack`, `EPSS`, `OSV`.

### Scanned Rows and Held Knowledge Entries

| Identifier | Subject / Scope | Class Taxonomy | Review Gate | Feed List | Field Provenance | Holding or Disclaiming Sentence |
|---|---|---|---|---|---|---|
| **S068** (`SOURCES.md:74`) | Rejected row: single advisory instance `GHSA-v676-f8gm-92r9` (CVE-2025-9086) | No | No | No | No | "REJECTED: screened out on primary-of-record and record completeness — the page republishes NVD's record of the CVE, self-labelled Unreviewed at L64 and L68... flip: re-open only if the entry becomes Reviewed..." (Exemplifies an unreviewed instance; carries no taxonomy, review gate, or feed list). |
| **S073 / F28** (`github-private-vulnerability-reporting.md`) | Reporter-side private reporting flow | No | No | No | No | `PROVINCE.md:171` & `SOURCES.md:78`: "scope limit: reporter flow only — maintainer handling, the GHSA database and CVE assignment stay out." |
| **S080 / F31** (`osv-affected-range-events.md`) | OpenSSF OSV format spec (`affected[].ranges[].events`) | No | No | No | No | `PROVINCE.md:178` & `osv-affected-range-events.md:17`: "the format's range/event semantics only — the osv.dev service API, the JSON Schema validation artifact, individual database exports and per-database database_specific values stay out." (F48 references OSV as GitHub's export format, but S080 specifies the schema format itself). |
| **S086 / F35** (`openssf-scorecard-checks.md`) | OpenSSF Scorecard check documentation | No | No | No | No | `openssf-scorecard-checks.md:40`: "pins Scorecard's USE of OSV only — the OSV format's range/event semantics stay F31/S080." Carries no GitHub advisory database semantics. |
| **S087 / F36** (`github-repository-security-advisories-rest-api.md`) | Repository-level advisories REST API (12 routes) | No | No | No | No | `github-repository-security-advisories-rest-api.md:45-46`: "'published' here is the advisory's own state on the source repository, not the global GitHub Advisory Database entry (global advisories are a separate reference page outside this capture)." |
| **S103 / F47** (`github-global-security-advisories-rest-api.md`) | Global security advisories REST read interface (`GET /advisories`, `GET /advisories/{ghsa_id}`) | No | No | No | No | `github-global-security-advisories-rest-api.md:76-78`: "- **No database semantics.** What 'reviewed' requires, how malware advisories are curated and how unreviewed advisories enter are deferred to 'About the GitHub Advisory database' (`S103.txt:276`), which was not opened." |

### Core Curation Elements Breakdown

1. **Class taxonomy** (*GitHub-reviewed vulnerability*, *unreviewed NVD import*, *malware*):
   - S103 lists `type` filter parameters (`reviewed`, `malware`, `unreviewed`) but defines neither their semantics nor their curation origins.
   - S068 mentions `Unreviewed` only as a page-label on a rejected single record.
   - None of the held rows or entries carries the three-class curation taxonomy.
2. **Review gate** (Allow-list of 12 supported package registries: Composer, Erlang, Go, Actions, Maven, Npm, NuGet, Pip, Pub, RubyGems, Rust, Swift):
   - Not present in any held row or knowledge entry. S103 enumerates 13 query values for `ecosystem`, but establishes no review-admission gate.
3. **Feed list** (9 imported sources: GitHub security advisories, NVD, npm security advisories, FriendsOfPHP, Go Vulncheck, Python Packaging, Ruby, RustSec, community contributions):
   - Not present in any held row or entry.
4. **Field provenance** (GHSA ID shape/charset `23456789cfghjmpqrvwx`; CVSS versions 3.0/3.1/4.0 provenance; EPSS daily sync vs percentile on-change updates; Security Lab community review gate):
   - F19 (`epss-exploit-prediction-scoring.md`) holds FIRST's model and definition, but not GitHub's ingestion or synchronization guarantees.
   - F47 holds query filter keys (`epss_percentage`, `epss_percentile`), but not field authoring or sync rules.

### Closest Overlap and Exact Differing Sentence

The closest held overlap is **F47 / S103** (`corpus/knowledge/github-global-security-advisories-rest-api.md`).

- **F47 explicitly disclaims and defers the curation ground (`github-global-security-advisories-rest-api.md:76-78`):**
  > "- **No database semantics.** What "reviewed" requires, how malware advisories are curated and how unreviewed advisories enter are deferred to "About the GitHub Advisory database" (`S103.txt:276`), which was not opened."

- **F48 opens and bounds that exact deferred ground (`github-advisory-database-curation-semantics.md:10-13`):**
  > "F47 could say "an unfiltered list returns reviewed, non-malware advisories" but not *what reviewed means*, *where the unreviewed and malware classes come from*, or *which fields GitHub authored versus imported*. This entry answers those three questions from the database's own documentation page, so a reader can decide what a GHSA record proves before treating it as a finding, a fix version or a score."

---

## 2. Sibling Lane Scan (Read-Only)

Searched `corpus/SOURCES.md` and `PROVINCE.md` across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin/`:
- `audio-shokunin`
- `chousa-shokunin`
- `game-dev-2d-shokunin`
- `game-dev-3d-shokunin`
- `kagi-shokunin`
- `kaidoku-shokunin`
- `kake-shokunin`
- `kama-shokunin`
- `kengaku-shokunin`
- `kotoba-shokunin`
- `kotodama-shokunin`
- `kumitate-shokunin`
- `lore-shokunin`
- `mado-shokunin`
- `mori-shokunin`
- `revenger-shokunin`
- `souji-shokunin`
- `tabi-shokunin`
- `tameshi-shokunin`
- `tsukuroi-shokunin`

### Search Terms & Results
- `about-the-github-advisory-database`: **0 hits** across all 20 sibling lanes.
- `advisory-database`: **0 hits** across all 20 sibling lanes.
- `Unreviewed advisories`: **0 hits** across all 20 sibling lanes.
- `type:malware`: **0 hits** across all 20 sibling lanes.
- `GHSA-xxxx`: **0 hits** across all 20 sibling lanes.

*(Note on broader pattern `GHSA`: The only hit across all siblings is `mori-shokunin:corpus/SOURCES.md:18` (S012: `GHSA-652q-wxr6-h5j6`), which captures a specific `systemd-oomd` vulnerability advisory for Linux memory pressure/OOM handling. It holds no general advisory database ground or curation semantics).*

**Conclusion:** No sibling lane holds `about-the-github-advisory-database` or its curation semantics.

---

## 3. Proposal Sweep (`considerthese/`)

Audited all 8 reflection files in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/` (`2026-10-19.md` through `2026-10-26.md`):
- `2026-10-19.md`: Anchorcheck prefix regression tests; rubric calibration; public source re-grounding (HackerOne, Bugcrowd, Google VRP); Saturation line pre-draft.
- `2026-10-20.md`: Live-source rechecker; rubric Frontier integration; owed-corrections ledger; CRA Art. 14 pre-screening.
- `2026-10-21.md`: Daily recheck runner; pre-admission quote validation; CNA 4.2.0 & CRA Art. 14 rubric integration.
- `2026-10-22.md`: Single-seat r23 close dossier; branch scanning; idleness tracking; CVSS v4 platform severity lens.
- `2026-10-23.md`: Quote uniqueness/location contract; r23 close dossier; quote checks on F06/F07.
- `2026-10-24.md`: Rechecker normalization and pinning; clean text capture; r23 close dossier.
- `2026-10-25.md`: Capping wave evidence bloat; distance-to-next-score metrics; bounty craft (SHONEN box 2); proposal ledger.
- `2026-10-26.md`: Verifiability 5 criteria; SHONEN box 2 domain task; quiescence gate; externalizing wave receipts; F18 PROVINCE amendment.

**Finding:** No still-unimplemented proposal in `considerthese/` is served by F48 / S105, and F48 / S105 does not implement any unimplemented proposal from `considerthese/`.

---

## 4. Verdict & Recommendation

**Verdict: SCOPE CLEAR.**

1. F48 / S105 introduces novel ground (three-class curation taxonomy, review allow-list of 12 package registries, 9 aggregator feeds, and field provenance rules) not held by any existing row or entry in `kasegi-shokunin`.
2. F48 respects the established boundary with F47 / S103 (F47 = REST query/filters, F48 = curation/admission semantics), S068 (rejected single record instance), and S080 (OSV spec format).
3. No sibling lane holds or claims this ground.

**Recommendation:** Maintain the two-way boundary in `corpus/README.md` and both entries (`github-global-security-advisories-rest-api.md` and `github-advisory-database-curation-semantics.md`): query filters stay with F47, curation semantics stay with F48.

---

## 5. Connector Synthesis: Non-Obvious Move Across Round Proposals

### Context & Evidence
- **Axis C1 (`depth:verifiability`):** `figure-audit.py` was extended in Round 70 (`c1051749`) to admit Python heads under `corpus/instruments/` with read-only arguments, while refusing write/exec/ingress flags (`PY_DENIED_FLAGS = ("--root", "--out", "--output", "--json", "--scratch", "--url", "--work")`).
- **Axis C2 (`coverage`):** F48 admits S105 with 19 located quotes validated by `corpus/instruments/source-recheck.py`.
- **Substrate Friction:** In `corpus/knowledge/*.md`, 76 of 86 entries hardcode absolute path prefixes in their `recheck:` header:
  `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py ...`
  This breaks in isolated scratch clones, git exports, and alternate roots (e.g. `ReviewC2`, `ScoutS105`, and verifier harnesses). Furthermore, `figure-audit-ledger.json` audits file/line counts, but contains zero figures verifying quote integrity for knowledge entries.
- **`considerthese` Link:** Reflective proposals in `2026-10-20.md` ("Become the live-source rechecker") and `2026-10-21.md` ("Run every recheck: line daily") noted that rechecks are documented per-entry but never audited as continuous, fail-closed figures.

### Proposed Move
Synthesize C1's newly admitted Python-head derive capability with C2's source-recheck verification by adding continuous source-recheck quote figures directly into `figure-audit-ledger.json`:

```json
{
 "id": "s105-recheck-quotes",
 "record": "corpus/knowledge/github-advisory-database-curation-semantics.md recheck '19 pinned quotes (Q01-Q19)'",
 "recorded": "19",
 "derive": "python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-70/manifest.json --source S105 | grep -c \"occurrences=1 anchor=\"",
 "want": "19"
}
```

### Second-Order Effects & Verification
1. **Verifiability (Improved):** Elevates S105 quote-check verification from an unmonitored per-file comment into an automated, fail-closed committed-byte audit executed on every `figure-audit.py` run.
2. **Path Portability:** Because `figure-audit.py` executes derive commands with `cwd=root`, the command eliminates the fragile `cd /home/vgpnk/...` wrapper entirely, making rechecks root-portable across scratch environments.
3. **Gate Compliance:**
   - Command uses admitted head `python3 corpus/instruments/source-recheck.py`.
   - Arguments `--manifest` and `--source` are clean of `PY_DENIED_FLAGS`.
   - Pipeline uses allowed `grep -c`.
   - Evaluated mechanically with `figure_audit.py`: `check_read_only` returns `True`, and `run_derive` yields exact output `('19', '19', None)` with return code 0.
4. **Coverage & Density (Unharmed):** No new rows added, no word counts mutated, no non-claims perturbed.
