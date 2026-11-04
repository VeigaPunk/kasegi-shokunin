# ScoutF45 — FIRST's PSIRT Maturity Document: capture, structure, quote table, novelty screen, province check

- **Seat:** `ScoutF45` (scout, leaf member — zero spawns, zero commits, zero mutating git/jj verbs, zero production edits, zero pacman transactions)
- **Lane root:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- **Base revision:** `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0` (read-only; no git/jj mutation was performed)
- **Seat directory:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScoutF45/`
- **Scratch (deleted on exit):** `/fast/scratch/hyaku/kasegi-r67/ScoutF45/`
- **Assigned axes:** `depth:verifiability`, `coverage`
- **Milestone:** predata multi-head SIGPIPE input-completeness repair + F45 PSIRT maturity screening
- **Run UTC:** 2026-11-04T20:51:58Z (first fetch) → 2026-11-04T21:0xZ (last measurement)
- **Tooling:** no install, no upgrade, no pacman transaction. `pdftotext`, `pdfinfo`, `pdftoppm` (poppler) and `tesseract` were already present on the host (`/usr/bin/`), used read-only.

---

## 0. Summary of findings for the L1

1. **The document is capturable and its ground is real.** HTTP 200, three maturity levels with named
   sub-sections, a per-level service listing (as artwork), a per-level sample checklist (64 items),
   five operational annexes, and an explicit *exclusion* of capacity and of SIM3. This is **new ground
   the lane does not hold** — `maturity level` appears **0 times** in every lane corpus file except
   `corpus/knowledge/first-psirt-services-framework.md`, and that file says only that S098 has *no* levels.
2. **It is a different document from S098 (F44), and it does not replace it.** The maturity document
   defers to the Services Framework for the catalogue itself (Annex 1, L356–L357). F45's scope is the
   *level ladder and the per-level capability expectations*, not the service catalogue.
3. **A verifiability defect in the round-65 lead row — for the L1 to correct.** The round-65 lead row
   (`corpus/SOURCES.md:244`) pins the maturity document by its **raw-HTML sha256**
   `334aeb01b20a8704fa35bbdc594277e0c212f42908c5ce3a940d8f2e4c77cf8e` (82978 bytes). That digest is
   **not reproducible**: the served HTML carries a **per-response CSP nonce**, so every distinct response
   is a distinct digest at an identical byte length. Measured: 6 raw fetches → 5 distinct nonces → 5
   distinct raw digests, one identical byte length (82978), one identical nonce-normalized digest, one
   identical `capture-source.py` text digest. The r65 digest is **not** reproduced by any of my 6 fetches
   nor by any of 10 normalizations I tested. **A registry row must not be pinned on that raw digest.**
   The two stable pins are the normalized text digest `cf834a65…` and the companion PDF digest
   `f217c446…` — the latter **reproduces round-65's own recorded PDF digest exactly** (644190 bytes).
4. **The PDF is the byte-stable artifact** and it is *older* than the corpus's S098: it points at
   `FIRST_PSIRT_Services_Framework_v1.0.pdf` while the corpus holds the **v1.1** framework (S098).
   F45's ladder is therefore keyed to the v1.0-era service catalogue — a real scope boundary to state.
5. **The document's own PDF table of contents is wrong in 8 of 11 checked entries** (including the
   Level 2 heading: TOC says page 19, actual page 10). Cite by HTML capture line, never by TOC page.

---

## 1. What was captured (durable receipts)

Written into the seat directory (no production file touched):

| file | what it is | bytes | sha256 |
|---|---|---|---|
| `ScoutF45/S100.txt` | the `capture-source.py` **text snapshot** (candidate capture) | 59068 | `cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f` |
| `ScoutF45/manifest.json` | candidate manifest, 12 pinned quotes, `body_lines [216,464]` | 4879 | — |
| `ScoutF45/raw-82978bytes-nonce1.html` | the raw served HTML (one nonce instance) | 82978 | `fce2d8307e9e17c2c2d8ba605954e37289f584081ac44634d8554cb9609dd678` |
| `ScoutF45/http-headers.txt` | the response headers | 1228 | — |
| `ScoutF45/FIRST_PSIRT_Maturity_Document.pdf` | the companion PDF (byte-stable) | 644190 | `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f` |
| `ScoutF45/receipts-measurements.txt` | every measurement quoted in this report | 9615 | — |

**Commands run** (from the seat scratch; `TMPDIR` passed explicitly on every instrument call):

```
python3 -B corpus/instruments/capture-source.py --id F45-maturity \
  --url https://www.first.org/standards/frameworks/psirts/psirt_maturity_document \
  --out <scratch>/S045.candidate.txt --kind html
# -> F45-maturity status=200 fetched_bytes=82978 snapshot_bytes=59068
#    sha256=cf834a652560bb8e230917299d8ea58c245a0c8715101280115c2508318bff9f
#    utc=2026-11-04T20:51:58Z
python3 -B corpus/instruments/capture-source.py --selftest
# -> selftest normalize=ok deterministic=ok   RC=0
python3 corpus/instruments/source-recheck.py \
  --manifest .ufo/waves/round-67/w1/ScoutF45/manifest.json --source S100
# -> S100:sha256 OK ; 12 x "OK" (11 with occurrences=1, M01 with occurrences=2 anchor=1-ok) ; RC=0
```

**HTTP record** (from `http-headers.txt`): `HTTP/2 200`; `last-modified: Mon, 26 Jan 2026 14:43:46 GMT`;
`content-type: text/html; charset=UTF-8`; `content-length: 82978`; served via `varnish`
(`x-cache: MISS, HIT`, `x-served-by: cache-gig2250041-GIG`). The `Last-Modified` value is **identical to
the one round 65 recorded for the sibling S098 page** — it is a *site publish* timestamp, not a document
revision date. The page states **no publication or revision date of its own** (the only four-digit year
in the whole capture is `2013`, at L220, in the Preface's account of when FIRST began the Services
Frameworks work).

**Capture reproducibility — measured, and the reason the raw digest is unusable as a pin:**

| fetch | raw bytes | raw sha256 | CSP nonce | `capture-source.py` text digest |
|---|---|---|---|---|
| 1 (`raw-r67.html`) | 82978 | `fce2d830…` | `tSpAxu6OKaKmpw9JA1x55w` | `cf834a65…` |
| 2 (`raw-r67b.html`) | 82978 | `fce2d830…` | same instance (cache hit) | `cf834a65…` |
| 3 (`raw-ua.html`, browser UA + query) | 82978 | `ecfd1de8…` | `sLyrtimmd54Xq0SpEEtYWg` | `cf834a65…` |
| 4 (`cb1.html`, cache-busted) | 82978 | `e4e55651…` | `RrotW3s4Sl05J9Cnf9dAkw` | `cf834a65…` |
| 5 (`cb2.html`, cache-busted) | 82978 | `346f2a84…` | `j4OjrE94o23oP5kZBF4EYw` | `cf834a65…` |
| 6 (`cb3.html`, cache-busted) | 82978 | `59299ab2…` | `q2Y-cxWktd2bURUPS7Hg6w` | `cf834a65…` |

- The nonce occupies **4 positions** in the script tail; the two cache-busted fetches differ from each
  other in **exactly 80 bytes across 8 ranges**, every one of them inside a nonce value.
- Length-preserving nonce normalization (all 6 fetches → `nonce="AAAAAAAAAAAAAAAAAAAAAA"`) yields
  **one** digest, `d3e932ee880493643827e0a40fa68fa3f72af061e9eb94d716059bbff79db6a1`.
- The **round-65 lead digest `334aeb01…` is not reproducible** by any of the 6 fetches, nor by any of 10
  normalizations (`raw`, `no-nonce-attr`, `no-script-tags`, `no-script-nonce`, `nonce22`,
  `nonce22+ts`, `ts-only`, `head-body-split`, `trailing-strip`, `lf-strip`). Since the nonce is the only
  per-response variable and the byte length is identical (82978), the r65 digest is a **nonce-bound
  instance digest**: it was true of one response and cannot be re-derived from the page.
- The **PDF digest is stable**: two consecutive fetches were byte-identical (`cmp`: no differences), and
  the digest `f217c446b4f422d1288d6836467f6acccc58a5b3027fef67866c9f392059a31f` **reproduces round-65's
  own recorded value** at `.ufo/waves/round-65/w1/ScoutS098/NOTES.md:91` (644190 bytes, 29 pages).

**Consequence for the L1 (a proposed correction, not an edit):** the round-65 lead row at
`corpus/SOURCES.md:244` should be superseded by a real registry row whose pin is either the normalized
text digest `cf834a65…` (with the manifest's sha256 over `S100.txt`) or the PDF digest `f217c446…`.
**Do not carry `334aeb01…` into a committed row.** The lead row is not a registry row (it lives under
"Registry changes", not in the `| id | source | … |` table), so nothing in the committed registry
currently depends on the unreproducible digest — but the lead row is the text a future reader will
copy from.

---

## 2. The document's own structure

### 2.1 Identity and layout

- **Title (L1, repeated at L216 as the `<h1>`):** "Product Security Incident Response Team (PSIRT)
  Maturity Document". The same string at L1 and L216 → M01 occurs **twice**; the manifest pins it with
  `anchor: 1`.
- **Chrome vs body:** L2–L215 = FIRST site navigation; **L216–L464 = document body**; L465–L478 = the
  site Standards/Publications navigation column and the copyright footer. The manifest declares
  `body_lines: [216, 464]`.
- **Level structure** (from the HTML heading tree, `<h2>`/`<h3>`/`<h4>`):

```
h1  Product Security Incident Response Team (PSIRT) Maturity Document
h2  PSIRT Maturity Levels to demonstrate Operational Capability and Maturity
h3  Maturity Level 1 (Basic) - The Beginning is a very fine place to start
      Preface: · Introduction: · Getting Started - Operational Foundations ·
      PSIRT Entrypoint - Vulnerability Discovery · The Next Step - Vulnerability Triage and Analysis ·
      Fixing the thing - Remediation · The Final Countdown -Vulnerability Disclosure · Conclusion
h3  Maturity Level 2 (Intermediate) - I am reactive, but I've trained for it!
      Introduction: · Back to Basics - Organizational Foundations ·
      (Not a) Communications Breakdown - Stakeholder Ecosystem Management ·
      Jinkies! A Clue! - Vulnerability Discovery · A word on SDLC ·
      Just the facts, ma'am - Vulnerability Triage and Analysis · Remediation ·
      I promise to tell you the truth, the whole truth… - Vulnerability Disclosure · Training · Conclusion
h3  Maturity Level 3 (Advanced) - Proactive...we're ready for anything (mostly)
      Introduction · Rock-solid Foundations · Putting the Stake into Stakeholder...mmmm...steak ·
      Discovering the Unknown (or at least it wasn't known to you to start out with) ·
      What's the Diagnosis, Doc? · Fixing the Thing ·
      Hark! I bring tidings of …. broken stuff (but I'm also going to tell you how to fix it!) ·
      Teach me, Sensei · Conclusion
h4  Beyond "Level 3"
h2  Annex 1: Supporting Resources
h2  Annex 2: Illustrations
h2  Annex 3: PSIRT Charter
h2  Annex 5: Charter Template
h2  Annex 6: Policy Template
h2  Annex 7: Sample Checklist
```

- **Markup defect in the source HTML:** *Annex 4: Examples of Mission Statements* is **not** a heading
  — it is a bare `<p>` (L372), so the `<h2>` sequence skips 4. The PDF does carry it as a TOC entry
  ("ANNEX 4 · EXAMPLES OF MISSION STATEMENT · 23"). A heading-tree extractor over the HTML alone would
  lose Annex 4 entirely.

### 2.2 What each level covers

**Level 1 (Basic)** — the founding sequence, walked end to end: Operational Foundations (executive
sponsorship L230–L232, stakeholders L233–L234, budget L235–L236, policies and procedures L237–L244,
with ISO/IEC 29147 and 30111 named at L239) → Vulnerability Discovery / intake (L245–L251) → Triage and
Analysis (L252–L255) → Qualification (L256–L267, naming CVRF, CSAF, VDO, ISO 30111, CVE) → Analysis
(L268–L271, "choose your yardstick", CVSS) → Remediation (L272–L276) → Disclosure (L277–L282,
finder acknowledgement) → Conclusion (L283–L284).

**Level 2 (Intermediate)** — the internal-facing expansion (L288: "we view PSIRTs in this middle-stage
of maturity as internally-focused"): organizational foundations incl. charter and organizational model
(L291–L292), stakeholder ecosystem management (L293–L295), discovery incl. a **product manifest / BOM**
(L296–L298), **SDLC** integration (L299–L300), triage incl. the **bug bar** and **security champions**
(L301–L307), remediation (L308–L309), disclosure incl. multi-party coordination and **embargo**
(L310–L312), training (L313–L315).

**Level 3 (Advanced)** — the proactive, externally-engaged PSIRT (L323: "proactive and consistent
behaviors"): rock-solid foundations (L327–L328), stakeholder engagement and **KPIs** (L329–L333, with
"Net Promoter Score" and "Service Level Objectives/Agreements" at L331), proactive discovery (L334–L336),
triage with a **reproduction system** and established-finder treatment (L337–L341), remediation with a
**standardized release window** (L342–L344), disclosure with **upstream/third-party coordination**
(L345–L347), training (L348–L350), conclusion (L351–L352).

**"Beyond Level 3" is a stub.** HTML L353 is the heading, L354 is one sentence ("What? …. Sounds
Impossible…. but it is NOT!"), and **L355 is already Annex 1**. In the PDF, page 19 ends with the same
two lines and **page 20 contains only the folio "20"** (`pdftotext -f 20 -l 20` → `20`). The ladder
therefore **ends at Level 3** in both renderings; there is no fourth level and no "beyond" content.

### 2.3 Self-assessment or evidence requirement — measured: **none**

| probe (body L216–L464) | count |
|---|---|
| `self-assess` / `self assess` | **0** |
| `certif*` | **0** |
| `rubric` | **0** |
| `audit` | **0** |
| `pass` / `fail` (as gate words) | **0** / **0** |
| `weight` / `grade` / `threshold` / `mandatory` | **0** / **0** / **0** / **0** |
| `criteria` | 1 (L270 — about documenting *scoring* criteria, not about level assessment) |
| `evaluat*` | 2 (L302 "a quantifiable process for evaluating these incoming reports"; L307 "proficient in evaluating the security vulnerability") |
| `shall` | **0** |
| `must` | 13 (L229, L238, L250, L257, L269, L270, L271, L292, L303, L328, L344, L392, L393) |
| `should` | 23 |

Annex 7's **Sample Checklist** (L397–L464) is the only self-assessment-shaped artefact: **19 items**
for Level 1 (L399–L417), **26** for Level 2 (L419–L444), **19** for Level 3 (L446–L464) — **64 items**
total, each a plain action line ("Establish budget", "Create baseline metrics", "Train development
teams"). **No scoring rule, no weighting, no pass/fail, no evidence-to-submit, no assessor, no
certification.** It is a to-do list, not an assessment instrument.

The register is advisory, not obliging: `shall` = 0; the strongest single sentence is L292's
"these key things **MUST** be in place" (Level 2, Organizational Foundations) and L328's rhetorical
"You must be this tall to ride the ride"; L392–L393 ("must be submitted", "must be triaged within
[#] days") sit inside the **Annex 6 policy template**, where the `[#]` is a literal placeholder.

### 2.4 The document's own exclusions — an unusually citable boundary

L221, the Preface: the framework "does not cover topics such as **capacity** — the number of
vulnerabilities and incidents a team can manage simultaneously, or **a maturity model such as SIM3**
which indicates how well a team governs, documents, performs and measures their function(s)." The
rendered HTML links "SIM3" to `https://opencsirt.org/maturity/sim3/` (an **external** maturity model,
outside this lane's corpus — a naming boundary for the entry). Level 3's KPIs (L331) are *examples the
PSIRT "could"* track, not a scheme.

### 2.5 What the document does **not** state (measured absences)

- **No numeric interval of its own.** The only interval-shaped text is the Annex 6 template's
  placeholder `[#] days` (L393). `deadline`, `SLA` (as a stated number), `within N days` — none.
  Disclosure timing is expressed as a negotiated embargo (L347), not a deadline.
- **No security research method.** Nothing about finding, reproducing or reporting vulnerabilities as
  research; the subject is the *receiving* organization's program.
- **No tier-A regulatory or legal obligation.** No `shall`, no `safe harbor`, no statutory duty.
- **No reproduction/evidence standard.** Reproduction appears as a Level 2/3 *capability* (L306, L340)
  and as an Annex-7 checklist line (L436), with no method, isolation rule or retention rule attached.
- **The figure content is artwork, not text.** "Figure 1/2/3: Listing of Maturity Level N desired
  Service Areas and Services" are **PNG images**
  (`PSIRT-maturity/figure1.png` 32448 B, `figure2.png` 103995 B, `figure3.png` 162903 B — all HTTP 200).
  The text capture holds **only the three caption lines** (L225, L290, L325) and the three figure-listing
  lines in Annex 2 (L359–L361). **Any claim about which service areas/services a level lists cannot be
  anchored in the text capture.** For the L1's information only (OCR of the PDF's rendered pages 6/11/16
  and of the three PNGs — *lossy, not quote-anchored, not evidence*): Level 1's figure shows
  Sponsorship / Stakeholders / Budget / Policies / Triage / Vulnerability Qualification / Vulnerability
  Analysis / Remediation / Intake of Vulnerability Reporting / Disclosure; Level 2 adds Charter,
  Organizational Model, Established Finders, Management & Stakeholder Support, Security Remedy Management
  Plan, Identifying Unreported Vulnerabilities, Vulnerability Metrics, Training & Education; Level 3 adds
  the Service Area 1–6 labels, Incident Handling, Incident Communication Coordination, Vulnerability
  Discovery Metrics, Training the Development Team, Staff, Resources & tools, Coordination. **This is
  OCR, explicitly not a quote, and the L1 should not admit it as a claim without a figure capture of its
  own.**
- **The PDF's table of contents is wrong in 8 of 11 checked entries** — measured against the rendered
  PDF (printed footer == PDF page index here): Level-1 *Introduction* TOC 3 → actual 5; *Getting Started*
  TOC 3 → actual 6; *PSIRT Entrypoint* TOC 7 → actual 8; *The Next Step* TOC 7 → actual 8; *The Final
  Countdown* TOC 9 → actual 10; **Level 2 heading TOC 19 → actual 10**; Annex 1 TOC 20 → actual 21;
  Annex 7 TOC 27 → actual 28. Only *Fixing the thing* (9), the Level 3 heading (15) and *Beyond "Level 3"*
  (19) are right. **Cite the HTML capture's line numbers, never a TOC page.**
- **The maturity document is older than the framework the corpus holds.** PDF `CreationDate`
  2018-12-06, cover says 2019; Annex 1 (L356–L357) points at
  `https://www.first.org/education/FIRST_PSIRT_Services_Framework_v1.0.pdf` — **v1.0** — while S098 is
  the **v1.1** framework page. F45's level ladder is therefore keyed to the **v1.0-era** service
  catalogue. Its prose references to the Services Framework (L227, L234, L246, L292, L312) are to that
  document, not to S098's v1.1 page. **This is the cleanest statement of the F44/F45 boundary.**

---

## 3. The quote table — 12 located quotes, each ≤ 25 words

Every quote is verbatim from the seat capture `ScoutF45/S100.txt` (sha256 `cf834a65…`, 478 lines), each
carries its line number, and every one is pinned in `ScoutF45/manifest.json` and verified by the lane's
own `source-recheck.py` (`RC=0`, all 12 `OK`). Word counts are whitespace tokens of the quote as pinned.

| id | line | words | quote (verbatim) |
|---|---|---|---|
| **M01** | 1 | 8 | Product Security Incident Response Team (PSIRT) Maturity Document |
| **M02** | 217 | 9 | PSIRT Maturity Levels to demonstrate Operational Capability and Maturity |
| **M03** | 221 | 21 | These referenced use cases cover a spectrum of developmental levels from a newly-established PSIRT, through a more advanced Incident Response team |
| **M04** | 221 | 21 | The framework does not cover topics such as capacity - the number of vulnerabilities and incidents a team can manage simultaneously |
| **M05** | 224 | 20 | The use of the term "maturity" in this document is intended to describe a profile of a product security team |
| **M06** | 218 | 14 | Maturity Level 1 (Basic) - The Beginning is a very fine place to start |
| **M07** | 285 | 13 | Maturity Level 2 (Intermediate) - I am reactive, but I’ve trained for it! |
| **M08** | 318 | 10 | Maturity Level 3 (Advanced) - Proactive...we’re ready for anything (mostly) |
| **M09** | 353 | 3 | Beyond “Level 3” |
| **M10** | 354 | 8 | What? …. Sounds Impossible…. but it is NOT! |
| **M11** | 397 | 4 | Annex 7: Sample Checklist |
| **M12** | 363 | 15 | PSIRTs should have a defined charter that describes what the PSIRT does, and its scope. |

**Anchoring notes (measured by `source-recheck.py`):**

- M01 occurs **twice** (L1 site `<title>`, L216 `<h1>`) → carries `anchor: 1`; recheck reports
  `occurrences=2 anchor=1-ok`.
- M03, M04 are two sentences of the **same line L221**; both are unique in the capture
  (`occurrences=1`).
- M09 and M10 are the entire "Beyond Level 3" section; their adjacency to M09/M10 is the measurement
  that the section is a stub (L355 is Annex 1).
- All 12 quotes carry the source's own wording, including its typographic apostrophes (L285, L318) and
  its ellipsis (L354). No quote was silently corrected.

**Additional located lines the L1 may want** (measured, and each verified as a substring of the named
line, but **not** pinned in the manifest — pin them if they are used):
L220 (Preface: CSIRT-vs-PSIRT distinction, "In 2013 FIRST initiated efforts on creating Services
Frameworks"); L227 ("In the PSIRT Services Framework, we have a concept of Operational Foundations");
L230–L232 (executive sponsorship); L239 (ISO/IEC 29147 and 30111 named); L262–L266 (CVRF, CSAF, VDO,
ISO 30111, CVE); L270–L271 ("choose your yardstick", CVSS); L282 (ISO 29147 for vulnerability
disclosure); L288 (Level 2 "internally-focused"); L292 ("these key things MUST be in place"); L298
(product manifest / BOM); L299–L300 (SDLC); L302 (bug bar); L307 (CVSS, CWE, security champions);
L317; L323 ("proactive and consistent behaviors"); L331 (KPIs, "Net Promoter Score"); L340 (reproduction
system); L347 (embargo); L352 (closing sentence); L356–L357 (Annex 1 → the **v1.0** Services Framework
PDF); L363–L371 (Annex 3 PSIRT Charter: mission statement, stakeholders, affiliation and sponsoring
organization, scope); L372–L386 (Annex 4: six named mission statements — Microsoft, IBM, Brocade,
Dell EMC, Red Hat, Honeywell); L388–L389 (Annex 5 charter template); L391–L396 (Annex 6 policy
template, including the `[#] days` placeholder at L393); L397–L464 (Annex 7 checklist, 64 items);
L478 (copyright footer).

---

## 4. Novelty screen against F44 / S098 (the PSIRT Services Framework v1.1)

**Method.** `corpus/source-snapshots/round-65/S098.txt` (1573 lines, sha256 `cfa42e23…`, digest
re-verified by me at base) was term-counted against the maturity capture's body (L216–L464). Counts are
case-insensitive occurrences.

### 4.1 What the maturity document holds that S098 does **not** (the new F45 ground)

| term | S098 | maturity | note |
|---|---|---|---|
| `maturity level` | **0** | 16 | the ladder itself — S098 has no level vocabulary at all |
| `level 1` / `level 2` / `level 3` | **0** / **0** / **0** | 5 / 4 / 5 | same |
| `Annex 7` / `Sample Checklist` / `checklist` | **0** / **0** / **0** | 1 / 1 / 1 | the 64-item per-level checklist is unique to F45 |
| `Charter Template` / `Policy Template` | **0** / **0** | 1 / 1 | Annexes 5–6 are unique to F45 |
| `Net Promoter` / `Key Productivity Indicator` | **0** / **0** | 1 / 1 | Level 3 KPI examples are unique to F45 |
| `reactive` | **0** | 3 | the reactive→proactive arc is F45's axis |
| `SIM3` / `capacity` (as an exclusion) | **0** / (not an exclusion) | 1 / 1 | the document's own scope carve-out |
| `SDLC` | **0** | 5 | Level 2's SDLC-connection expectations |
| `BOM` / `product manifest` | **0** | 1 / 1 | Level 2's component-inventory expectation |
| `security champions` | **0** | 1 | Level 2's delegated-scoring practice |

**In words:** S098 (F44) holds *what a PSIRT's services are* — six service areas, 28 services,
84 functions, the three organizational models, the Operational Foundations tiers, and a single Glossary
*maturity definition* (its own L1510). The maturity document holds *what a PSIRT looks like at each
stage of growth*: three named levels with per-level expectations (what changes at Level 2: charter,
organizational model, product manifest, SDLC, bug bar, security champions, embargo, training; what
changes at Level 3: KPIs, proactive discovery, reproduction system, standard release window, upstream
coordination), a per-level checklist, and operational templates (charter, mission statements, policy).
The two documents are **complementary, not duplicative** — and the maturity document says so itself
(Annex 1 defers to the Services Framework for the catalogue and glossary).

### 4.2 What the maturity document **repeats** (do not re-admit as new)

| term | S098 | maturity | what is repeated |
|---|---|---|---|
| `service area` | 23 | 7 | the same six service-area names, cited by reference (L246, L292, L367) |
| `CVSS` | 36 | 6 | CVSS as the yardstick — already held by F44 and F01 |
| `reproduction` | 13 | 3 | reproduction as a Level 2/3 capability; the *method* stays S098's |
| `executive sponsorship` | 3 | 4 | Operational Foundations item — S098's L316–L322 holds it |
| `budget` | 5 | 5 | Operational Foundations item |
| `ISO/IEC 29147` | 5 | 3 | the standards references stay F11's ground |
| `bug bar` | 7 | 1 | quality-gate/bug-bar concept stays F44's (S098 L853) |
| `embargo` | 5 | 1 | embargo coordination stays F06/S018-adjacent multi-party ground |
| `multi-party` | 7 | 3 | the multi-party guidelines stay F06's ground (S098 L1531 links v1.0) |
| `charter` | 4 | 9 | the charter *requirement* is S098's L332–L338; F45 adds the *template* |
| `Microsoft`, `IBM`, `Brocade`, `Dell`, `Red Hat`, `Honeywell` | 2, 0, 0, 3, 3, 1 | 6, 8, 4, 5, 2, 4 | **S098's six hits are the Acknowledgements author list (L1452–L1465), not mission statements.** F45's Annex 4 is six *actual mission statements* — new content, but it is illustrative vendor self-description, **not** a policy rule, and must not be read as a vendor commitment. |

### 4.3 Overlap with the other held rows

- **F43 (S095, CERT/CC phase-to-role matrix)** — CERT/CC's *roles across a CVD episode*; F45 is a
  *vendor team's internal capability stages*. No overlap.
- **F06 (S018, FIRST multi-party coordination guidelines)** — F45 *names* the guidelines (L311) and
  the embargo (L347) as things a Level 2+ PSIRT does; the coordination rules stay F06's.
- **F11 (S041, ISO 29147/30111 division of labour)** — F45 *cites* both standards (L239, L241, L265,
  L282); the division stays F11's.
- **F01 (S001/S002, CVSS)** and **F20/F19 (SSVC/EPSS)** — F45 mentions CVSS/CWE only as scoring advice;
  the scoring systems stay F01/F19/F20's.
- **F10 (S040, Cisco PSIRT policy)** — F45 is framework-agnostic best practice, not a vendor policy.

### 4.4 Corpus-side screen (read-only, at base)

- `grep -cE '^\| F45 \|' corpus/README.md` → **0** (no F45 row exists).
- Frontier rows in `corpus/README.md` = **44**, all `admitted`. F45 is the next free frontier id.
- `grep -cE '^\| S100 ' corpus/SOURCES.md` → **0**. The registry's highest id is **S099**; S100 is free.
- `psirt_maturity_document` appears in `corpus/SOURCES.md` **exactly once** — the round-65 **lead** row
  (line 244), not a registry row. `corpus/README.md`, `PROVINCE.md`, `SKILL.md` → **0 hits**.
- `corpus/knowledge/`: only `first-psirt-services-framework.md` mentions "Maturity Level", and only to
  state that **S098 contains no levels** (its §Maturity). **No knowledge entry holds the ladder.**
- **Sibling lanes:** `maturity level` matches only `kasegi-shokunin` (4 files) and `revenger-shokunin`
  (`corpus/SOURCES.md:402`, Hex-Rays' decompiler "maturity levels" — unrelated). No sibling holds this
  ground.

---

## 5. Province check against `PROVINCE.md`

**Province (`PROVINCE.md:3`, `:24–25`, `:29–30`):** domain *"bounty & security research — scopes
~/Projects/bounties, program rules, claim packages"*; owns *"the domain knowledge, playbooks, error
patterns, and checklists"*; the Core covers *"program rules, scopes, and claim packages… triage and
claim gates, and submission/disclosure packaging"*.

**In province — yes.** The maturity document is a **vendor-side program document** in exactly the class
the lane already holds: F10 (vendor-side disclosure policies), F43 (CERT/CC's phase/role matrix), F44
(S098, the PSIRT Services Framework). It describes how a *receiving team's own program* — its intake,
qualification, triage, remediation and disclosure gates — matures. That is the "triage and claim gates,
and submission/disclosure packaging" surface, on the receiving side. It is documentation only; the
lane's standing refusal of live-target testing is untouched.

**Adjacency, not absorption (named so the L1 does not over-claim):** chousa (research method and source
hierarchy) — F45 is *not* a research method; kengaku (LLM evaluation) — F45's KPIs are program
management, not model evaluation; kagi (secrets) and kake (web properties) — untouched.

### 5.1 Rejection arguments — readings I refuse, and why

1. **Refuse: "FIRST defines a four-level maturity ladder (Basic, Intermediate, Advanced, and beyond)."**
   *Rejected.* "Beyond 'Level 3'" (M09) is followed by exactly one sentence (M10) and then Annex 1
   (L355); the PDF's page 20 carries only a folio. There is **no fourth level**.
2. **Refuse: "the maturity document is a certification scheme with a self-assessment and a score."**
   *Rejected on measurement:* `self-assess` 0, `certif*` 0, `rubric` 0, `audit` 0, `pass`/`fail` 0/0,
   `weight`/`grade`/`threshold`/`mandatory` 0/0/0/0. Annex 7 is an unscored 64-item checklist (M11).
3. **Refuse: "Level 3 requires the PSIRT to track Net Promoter Score / SLO / SLA."** *Rejected.* L331
   says these "**could be**" KPI examples; `must` at L331 is absent (the 13 `must` hits are at L229,
   L238, L250, L257, L269, L270, L271, L292, L303, L328, L344, L392, L393, and L392–L393 are template
   text with a `[#]` placeholder).
4. **Refuse: "the maturity document mandates a triage/disclosure deadline."** *Rejected.* No numeric
   interval; the only one is the Annex-6 template's literal `[#] days` (L393). Disclosure timing is a
   negotiated embargo (L347).
5. **Refuse: "this can be folded into F44 / the S098 entry can carry the level ladder."** *Rejected.* The
   documents are distinct artifacts; S098's body has **0** occurrences of `maturity level` and of
   `level N` (measured by me at base over the committed 1573-line capture). The r65 S098 entry already
   says so, and its "Maturity rule" package rule #2 correctly routes level ground to the separate
   document. F45 is a new row.
6. **Refuse: "the maturity document supersedes or replaces the Services Framework."** *Rejected by the
   document itself:* Annex 1 (L356–L357) defers to the Services Framework for the supporting resources
   and glossary. Note also the version skew: the maturity document points at the **v1.0** framework PDF
   while the corpus holds **v1.1** (S098).
7. **Refuse: "the maturity document's figure shows which service areas each level covers" as a text
   claim.** *Rejected as unanchorable:* the figures are PNG artwork; the text capture holds only the
   three caption lines. Any such claim needs the figure asset captured and quoted separately. (My OCR of
   the figures is recorded in §2.5 as **not evidence**.)
8. **Refuse: "the maturity document is dated 2019 / 2018-12-06."** *Rejected as a property of the HTML
   page:* the HTML states no date; `2019` and the PDF `CreationDate` belong to the **PDF artifact**
   (whose cover says 2019, `CreationDate 2018-12-06`), and the HTTP `Last-Modified` (2026-01-26) is the
   *site's* publish stamp, identical to the one S098's page carries. A row that says "dated 2019" must
   say so **of the PDF**, with the PDF digest as its pin.
9. **Refuse: "the level ladder is verifiable against the PDF's table of contents."** *Rejected:*
   8 of 11 checked TOC page numbers are wrong (Level 2 heading: TOC 19, actual 10). Cite HTML capture
   lines only.
10. **Refuse: "the round-65 lead digest `334aeb01…` identifies the document."** *Rejected:* it is a
    nonce-bound instance digest (§1) — not reproducible from the page, and not the digest of any
    artifact the corpus can hold. The corpus-stable pins are `cf834a65…` (text) and `f217c446…` (PDF).
11. **Refuse: "the maturity document is a vendor commitment."** *Rejected:* Annex 4's six mission
    statements are illustrative examples of what a charter may say (Microsoft, IBM, Brocade, Dell EMC,
    Red Hat, Honeywell). They are *not* program rules, deadlines or safe harbours, and no F45 sentence
    may treat them as obligations.

---

## 6. What the L1 needs from this seat (all L1-production)

Nothing here is landed by this seat. The L1 owns every production byte. Recommended inputs:

1. **Registry row** for the maturity document. Proposed id **S100** (S099 is the highest); proposed
   frontier id **F45** (F44 is the highest admitted). Suggested `kind=docs`, `tier=A`,
   `status=mined`, `opened=2026-11-04`, `recheck=180d` (matching the sibling S098 cadence for a
   page with no publication date).
2. **The capture** must be committed under `corpus/source-snapshots/round-67/` with a manifest whose
   sha256 is the **text** digest `cf834a65…` and whose `path` stem equals the source id (the lane's
   `source-recheck.py` enforces `stem-mismatch`).
3. **The pin to use: `cf834a65…` (text snapshot) or `f217c446…` (PDF).** Do **not** carry
   `334aeb01…`. If the L1 wants the PDF as a second source (recommended — it is byte-stable and
   reproduces round-65's own PDF digest), it needs its own id and manifest.
4. **The round-65 lead row at `corpus/SOURCES.md:244`** should be superseded or annotated so the
   unreproducible raw digest is not copied forward.
5. **Scope limits for the F45 row**, from §5.1: the three levels and what changes at each; the
   per-level checklist as an *unscored* to-do list; the templates; the document's own exclusion of
   capacity and SIM3; and the **v1.0-vs-v1.1** version skew against F44.
6. **`body_lines [216, 464]`** for the text capture, with L1–L215 and L465–L478 declared as chrome —
   and note that L1 is the title as well as L216, so a title quote needs `anchor: 1` (M01, `occurrences=2`).
7. **Known residuals to name in the entry's Limits section** (all measured, none hidden): the figures
   are artwork (no text claim about them); the PDF's TOC page numbers are unreliable; "Beyond Level 3"
   is a stub; the HTML states no date; the PDF is the dated artifact; the raw HTML digest is not stable.

**Reproducibility note for the L1:** every measurement in this report is in
`.ufo/waves/round-67/w1/ScoutF45/receipts-measurements.txt` (140 lines), and the 12 quotes are
re-verifiable with the lane's own instrument:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py \
  --manifest .ufo/waves/round-67/w1/ScoutF45/manifest.json --source S100
# -> S100:sha256 OK ; 12 OK lines ; RC=0
```

---

## 7. Compliance

- **Production untouched.** No file under `corpus/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`
  or `corpus/instruments/figure-audit.py` was created, edited or deleted. No `git`/`jj` command other
  than reads; no commit, push, stash, checkout or index write; no `task` dispatch; no `agent://all`
  message; no pacman transaction and no tool install (poppler and tesseract were already present).
- **Scope respected.** This seat wrote only inside
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-67/w1/ScoutF45/` and its own report
  file. No sibling lane was written to.
- **Scratch.** `/fast/scratch/hyaku/kasegi-r67/ScoutF45/` was the only scratch area (every instrument
  call passed it explicitly as `TMPDIR`/output path), and it was **removed on exit** — verified absent
  after the durable receipts were copied into the seat directory. No file under `/tmp` was written.
- **Honesty.** Every number in this report was measured in this run and the command or receipt is named.
  The only non-capture-derived material is the OCR of the three figure assets, which is labelled as
  lossy and **not** evidence; no sandbox, semantic-emulator or general-correctness property is claimed.

Report: .ufo/waves/round-67/w1/ScoutF45.md
