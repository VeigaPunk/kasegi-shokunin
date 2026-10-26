# ScoutF20Open — S054 source-open record + quote candidates (round 37, C2 / coverage)

Seat: leaf scout. Receipt only; no lane file written, no git command run against the lane except read-only `ls`/`rev-parse`.
Tooling installed: none. Scratch `/fast/scratch/hyaku/kasegi-r37/ScoutF20Open/` (removed before yield).

## 1. Open record (access 2026-10-26)

Fetched with the lane's own `corpus/instruments/capture-source.py` (UA `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`), plus `curl -L` with the same UA for headers.

| page | url | HTTP | redirects | fetched_bytes | snapshot_bytes | lines | snapshot sha256 | fetched_utc |
|---|---|---|---|---|---|---|---|---|
| HOME (frozen-claim literal) | `https://certcc.github.io/SSVC/` | 200 (HTTP/2, `text/html; charset=utf-8`, `last-modified: Fri, 23 Oct 2026 16:21:47 GMT`, etag `"6adb899b-19d4f"`, server GitHub.com) | 0 | 105807 (curl raw sha256 `60c00968563c688e4ffafb7a5b9fcedf097db8459114b92185c37cd4482112ed`) | 7730 | 286 | `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56` | 2026-10-26T17:12:14Z |
| OVERVIEW (erratum-1 primary) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 200 | 0 | 143053 | 32623 | 518 | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21` | 2026-10-26T17:12:36Z |
| CISA response how-to (supplementary) | `https://certcc.github.io/SSVC/howto/cisa_response/` | 200 | 0 | 126785 | 14896 | 656 | `4b3dfc9c4276ac2f516edd42dac932d89b87bb70b3736baa3fee8aaa0a67f0a6` | 2026-10-26T17:12:36Z |

Determinism: a second instrument capture of the HOME page was byte-identical to the first (sha above). The HOME and OVERVIEW sha256/byte values equal those recorded by `ExecC2QuoteOnce` (fetched 17:02:11Z), so the page content was stable across ≈10 min and two independent seats.
Hyperlinks from the home page (raw HTML hrefs): `tutorials/ssvc_overview/`, `howto/cisa_response/`, `topics/vulnerability_management_decisions/`, `reference/decision_points/…`.

**URL fact the L1 must hold:** the frozen claim C2 and this item name the HOME URL; `claims-erratum-1.md` (filed pre-score) moves the S054 row/manifest/capture URL to the OVERVIEW page because HOME alone fails (c) and (d) below. My measurement independently confirms the erratum is necessary.

## 2. Registry anchor (overview definition sentence)

- On HOME: **L203** `SSVC stands for A Stakeholder-Specific Vulnerability Categorization.` (occ 1) with **L204** the methodology sentence (occ 1).
- On OVERVIEW (the pinned page): the definition-plus-contrast sentence is **L247**; the categorisation/priority sentence **L259**. Recommended registry anchor for the overview-pinned row: **L247** (the page's definition of what SSVC rates and how it differs from severity/exploitability), with L259 as the mechanism anchor. HOME L203–L205 is the only place the "SSVC stands for…" expansion appears (0 occurrences on OVERVIEW).

## 3. Verification of the five required statements

| # | statement | HOME (`S054` frozen URL) | OVERVIEW (erratum-1 URL) | CISA how-to |
|---|---|---|---|---|
| a | what SSVC is | **YES** L203–L204 | not needed (L247 "SSVC rates vulnerabilities on risk to the concerned stakeholder") | — |
| b | stakeholder-tailored | **YES** L204 ("based on the needs of the stakeholders…"), L205 (finders, vendors, coordinators, deployers) | **YES** L247 ("not … one-size-fits-all", "stakeholder-defined decision model"), L259 ("risk that varies among stakeholders") | — |
| c | decision-point / outcome mechanism | **NO** — only nav labels (L107 "Decision Points", L178 "Outcomes", L183 "Decision Tables"); no prose | **YES** L259 (series of questions → priority categories, Decision Trees), L277 (decision points / outcomes explainable; decision point values determine how risky) | L211/L217: 4 binary decision points → 4 outcomes |
| d | prioritization vs severity/likelihood | **PARTIAL** — L204 "methodology for prioritizing vulnerabilities" but no severity/exploitability contrast anywhere on HOME (terms `severity`, `likelihood` appear only as nav label L58/L139 "Qualitative Severity"; `likelihood` count 0) | **YES** L247 contrasts "technical severity (how bad it could be…)" and "exploitability (how likely it is that there will be an exploit)" with stakeholder risk; L259 "categorizes … by priority" | — |
| e | BOD 26-04 response model | **NAV LABEL ONLY** — L48 `CISA BOD 26-04 Response Model` (1 occurrence; no description text) | **NAV LABEL ONLY** — `BOD 26-04` count 1 (nav, L68); no description | **YES** (separate page): L205–206 "tool support implementers of CISA BOD 26-04"; L211 four binary decision points (InKEV, Publicly Exposed, Automatable, Technical Impact L212–L215); L217 four outcomes; L219–L238 outcome group `cisa:BOD2604:1.0.0` with values FSU / 60D / 14D / 3D / 3DF (L224–L238) |

Conclusion: a single page grounds (a),(b),(d) only partially on HOME and (c) not at all; OVERVIEW grounds (a)–(d); (e) is grounded on neither pinned page — only on the CISA how-to (`howto/cisa_response/`, a different URL). A row that cites exactly one `https://` token (capture-binding B5) cannot ground (e); any (e) statement in the knowledge entry must be limited to "the site lists a CISA BOD 26-04 Response Model" (nav label, HOME L48 / OVERVIEW L68) or carry a second captured source. I did not verify BOD 26-04 against CISA itself; BOD 26-04 existence rests only on the CERT/CC page text.

## 4. Quote candidates (≤25 words; exact line numbers; occurrences = `source-recheck.py normalize()` whole-snapshot `str.count`; raw = un-normalized count)

OVERVIEW snapshot (`ff3f3b2c…`, pinned URL):

| id | line | occ | raw | words | quote | grounds |
|---|---|---|---|---|---|---|
| QA | L247 | 1 | 1 | 22 | `Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability` | d (contrast with severity/exploitability) — HOME occ 0 |
| QB | L259 | 1 | 1 | 12 | `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders.` | b, d, c (priority output) — HOME occ 0 |
| QC | L247 | 1 | 1 | 21 | `or exploitability (how likely it is that there will be an exploit), SSVC rates vulnerabilities on risk to the concerned stakeholder.` | a, b, d (completes the QA contrast: likelihood vs stakeholder risk) |
| QD | L259 | 1 | 1 | 15 | `Decision Trees are used when asking the series of questions to categorize a vulnerability's priority.` | c (mechanism) |
| QE | L277 | 1 | 1 | 14 | `All decision points and decision outcomes (priority categories) must be explainable to the non-expert.` | c (decision-point/outcome) |
| (alt) | L247 | 1 | 1 | 12 | `SSVC follows a stakeholder-defined decision model to make these determinations of risk.` | b |
| (alt) | L259 | 1 | 1 | 22 | `SSVC categorizes vulnerabilities by priority based on risk that varies among stakeholders. These categories reflect the timeliness of action to be taken.` | prioritization = timeliness |

HOME snapshot (`a6613315…`, frozen URL; each occ 1, raw 1, OVERVIEW occ 0):

| id | line | words | quote |
|---|---|---|---|
| QH1 | L203 | 7 | `SSVC stands for A Stakeholder-Specific Vulnerability Categorization.` |
| QH2 | L204 | 20 | `It is a methodology for prioritizing vulnerabilities based on the needs of the stakeholders involved in the vulnerability management process.` |
| QH3 | L205 | 21 | `SSVC is designed to be used by any stakeholder in the vulnerability management process, including finders, vendors, coordinators, deployers, and others.` |

CISA how-to snapshot (`4b3dfc9c…`, supplementary, **not** the pinned URL): `The CISA Response Timeline has 4 binary decision points:` L211 occ 1; `These 4 decision points are combined to yield 4 outcomes for vulnerability` L217 occ 1 (line-wrapped; whitespace-normalises across L217–L218); `The CISA BOD 26-04 outcome group of remediation timelines for agencies to follow.` **occ 2** (L220, L245 JSON copy — would need an anchor; avoid); `Remediate within 3 days and carry out a forensic triage…` occ 2 (L238, L271 — avoid).

Recommended set for the OVERVIEW-pinned row: QA (L247), QB (L259), QD (L259), QE (L277) — all occ 1, ≤25 words, mapping (b),(c),(d), with (a) from QC. This matches the four quotes `ExecC2QuoteOnce` already pinned (Q1=QA, Q2=QB), so no conflict.

## 5. Gaps / non-claims

- (e) not groundable on either pinned URL beyond a nav label (see §3); decide wording or add a captured source before the entry claims BOD 26-04 content.
- Pages are live-fetched; this proves the captured bytes at 2026-10-26T17:12Z, not that SSVC is current beyond that date (`last-modified` 2026-10-23).
- Normalized snapshot line numbers are the instrument's (`collapse()` drops blank lines); raw-HTML line numbers differ.

Report: .ufo/waves/round-37/wave1/ScoutF20Open.md
