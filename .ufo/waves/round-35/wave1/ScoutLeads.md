# ScoutLeads — standing leads state check (round 35)

Seat: ScoutLeads (leaf, scout). Read-only probes under the instrument UA; no lead adopted; no lane file edited other than this receipt.
UA (corpus/instruments/capture-source.py:32): `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`
Probe time: 2026-10-26 ~06:37–06:45Z. curl 8.23.0, `curl -sS -L -m 45 -A "$UA"`.

## Report

### Lead registry state (unopened)
corpus/SOURCES.md (sha256 `510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`) `## Leads (unopened)` L79 holds exactly three bullets:
- L81 Google Big Sleep (tracker https://goo.gle/bigsleep "was not opened"; DeepMind blog URL 404 in the earlier pass)
- L82 ISO/IEC 29147 + 30111 records (https://www.iso.org/standard/72311.html, https://www.iso.org/standard/69725.html)
- L83 UK AISI blog (https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing)
Remain unopened in the registry sense: `grep -rn -E "goo\.gle/bigsleep|iso\.org/standard/(72311|69725)|aisi\.gov\.uk"` over corpus/SOURCES.md, corpus/knowledge, corpus/README.md, corpus/QUALITY.md, SKILL.md hits only SOURCES.md:81-83 (no S-row, no knowledge entry, no snapshot capture of any lead). Only incidental URL occurrence in a snapshot: corpus/source-snapshots/round-24/S003.txt:94 and :457 (sha256 `b659e385f873799a…`) cite the 72311 URL as a footnote/bibliography entry of S003 (CISA CVD doc) — a citation, not an opening of the lead. No S-row in the registry carries any of the three URLs. Nothing added to corpus/ by this seat (no capture written into source-snapshots).

### Probes (HTTP, instrument UA, redirects followed)
| # | URL | final status | final URL | notes |
|---|-----|--------------|-----------|-------|
| 1 | https://goo.gle/bigsleep | 200 (curl exit 0) | https://issuetracker.google.com/savedsearches/7155917 (1 redirect: 302) | body 83238 B (second fetch 83239), `<title>Google Issue Tracker</title>`, visible text only "Google Issue Tracker Sign in"; 0 occurrences of "Big Sleep" in the HTML. JS-rendered shell, unauthenticated: no report list readable. |
| 2 | https://www.iso.org/standard/72311.html | **intermittent** 200 / 403 (curl exit 0 both) | same (no redirect) | 6 retry trials: 200,403,403,200,200,403 (a further run 200 at try 1). 403 body = Cloudflare "Just a moment… Enable JavaScript and cookies to continue" (5597 B). 200 body 89224 B sha256 `134bcdd1c6bcff47c35dd70bf3dbe2ab50e51652a903fc755eb5ca756ee158f3`. |
| 3 | https://www.iso.org/standard/69725.html | **intermittent** 200 / 403 | same | 6 trials: 403,200,200,200,403,200. 200 body 88105 B sha256 `d1a31ecdda29900f146ecc6ce8e2956ed659b085d204cc9ef1d03f7cb6fea6fa`. |
| 4 | https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing | 200 (curl exit 0, stable on 2 fetches) | same | body 33476 B sha256 `c671775158b6feea9231bad4f98c0c32feb6e15c5805e42b8b58e6a67c30fe19`; title "How fast is autonomous AI cyber capability advancing? \| AISI Work"; 11610 chars of readable text. |

### Content seen and whether it is a substantive new source
1. **Big Sleep tracker — not usable.** The short link resolves to a Google Issue Tracker saved search that serves a sign-in/JS shell with no entries in the static HTML. A static capture (capture-source.py) would record "Google Issue Tracker Sign in" only; no dated findings, so no Q-bar-passing text. Status: remains a lead; would need an authenticated/JS-rendering route or the Project Zero page that links it (S-row-level source, not this URL). The earlier DeepMind-blog 404 was not re-tested (not in this assignment's URL list).
2. **ISO/IEC 29147:2018 (72311) and 30111:2019 (69725) — catalogue records only; low marginal value.** Observed from the 200 bodies:
   - 72311: "ISO/IEC 29147:2018 — Information technology — Security techniques — Vulnerability disclosure", Edition 2, 2018-10, Published; "This publication was last reviewed and confirmed in 2024. Therefore this version remains current."; CHF 179 (PDF+ePub / Paper). Abstract opens "This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services." and lists guidelines on receiving reports / disclosing remediation; "Coordinated vulnerability disclosure is especially important when multiple vendors are affected."
   - 69725: "ISO/IEC 30111:2019 — … Vulnerability handling processes", Edition 2, 2019-10, Published; "last reviewed and confirmed in 2025. Therefore this version remains current."; CHF 135; 13 pages; JTC 1/SC 27; ICS 35.030; stage 90.92 "International Standard to be revised"; previously ISO/IEC 30111:2013 (withdrawn). Abstract: "requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service… applicable to vendors involved in handling vulnerabilities."
   - Verdict: both are paywalled standards; the pages expose status/edition/abstract/price only, no clause text. Existing corpus ground already covers the standards' division of labour without buying them (corpus/knowledge/iso-29147-and-30111-division-of-labour.md, iso-29147-divergence-and-clause-crosswalk.md; S041). What the pages could add is the current-edition/lifecycle fact (29147:2018 current, confirmed 2024; 30111:2019 current, confirmed 2025, stage 90.92 to be revised) — a dated currency check on the editions the existing entries already name, not a new capability. Operational blocker for a capture: intermittent Cloudflare 403 under the instrument UA (about 40–50% of requests in 12 trials), so a capture-source.py run would need retry logic or it would store the challenge page. Not a source this round could have needed (no claim or frontier item depends on it); not adopted.
3. **UK AISI blog — substantive and fetchable, topically adjacent to existing AI entries.** Dated May 13, 2026, AISI (research organisation within DSIT). Stated claims (first-party, text read): doubling time of the length of cyber tasks AI models complete at 80% reliability estimated 4.7 months (Feb 2026) vs 8 months (Nov 2025) estimate; Claude Mythos Preview and GPT-5.5 "substantially exceeded both doubling rate trends"; 2.5M tokens/task cap; narrow cyber suite with human baselines on only about a third of tasks; cyber range "The Last Ones" solved 6/10, "Cooling Tower" 3/10 by newer Mythos checkpoint; explicit caveats ("not a future prediction, nor a fixed law", six tasks over eight hours). It is a capability-trend measurement for frontier AI, not a vulnerability-reporting/disclosure-program source. Fit to the lane: it would sit beside the AI-finding-validation ground (corpus/knowledge/ai-assisted-finding-validation.md; S010–S012, S025) as context on how fast AI discovery capability moves, but it contains no triage/validation/report-quality method — the lane's topic. Verdict: a real, new, openable source (the only one of the three that returns a stable 200 with readable text) that a coverage frontier item *could* have used as a Tier-A first-party AI-capability source, but this round's claims C1/C2 and the non-claim items do not need it (C2 is F18/CISA KEV). Lead stays a lead; not adopted.

### Summary table
| lead | HTTP (instrument UA) | readable content | substantive new source usable this round? | lead state after this seat |
|------|----------------------|------------------|-------------------------------------------|----------------------------|
| Big Sleep goo.gle/bigsleep | 200 via 302 to issuetracker.google.com/savedsearches/7155917 | none (auth/JS shell) | no | unopened (unchanged) |
| ISO 29147 / 72311 | 200 or 403 intermittent (Cloudflare) | catalogue record, no clause text | no (currency fact only; covered by existing entries) | unopened (unchanged) |
| ISO 30111 / 69725 | 200 or 403 intermittent | catalogue record, no clause text | no | unopened (unchanged) |
| AISI blog | 200 stable | full first-party article, 2026-05-13 | yes in principle, not needed by C1/C2 | unopened (unchanged) |

Observation for the L1 (not an edit): SOURCES.md L79-L83 lists three bullets (four URLs); the bullet at L83 (AISI) is present in the lane copy. Leads were not edited by this seat; if the L1 records this probe, a one-line dated note per lead beside L81-L83 would carry the status above.

### Checks run / environment
- Commands: grep over corpus (above), `curl` ×~40 (4 URLs, repeated for the ISO pair), python3 html stripping. No installs, no tool changes (no tooling update needed).
- Scratch: /fast/scratch/hyaku/kasegi-r35/ScoutLeads/ created per command with `trap 'rm -rf -- "$S"' EXIT`; absent at yield.
- Lane writes: only this file.
