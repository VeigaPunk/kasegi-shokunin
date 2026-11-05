# ScoutNext — round-72 reconnaissance: C2 ground distinctness, sibling ownership, next-round leads, leads-section state

Seat: ScoutNext (scout, leaf — no subagent dispatch; no `task` calls issued).
Lane repo read-only: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`.
Scratch: `/fast/scratch/hyaku/kasegi-r71/ScoutNext/` (removed on yield; only HTTP status/byte counts and byte counts measured in it are reproduced below).
No git/jj mutation, no commit, no push, no tool install. Only this report file was written.

---

## 0. Evidence base (measured)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | head -8
 M LOG.md
 M SCORECARD.md
 M SKILL.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md
 M corpus/lessons/round-71.md
```

(The working tree carries sibling edits in flight; this seat read the tree as it stood and re-verified every cited line number at the end of the seat — F49 at `corpus/README.md:1114`, S106 at `corpus/SOURCES.md:118`, the `## Leads` heading at `corpus/SOURCES.md:168` — all unchanged.)

The round-71 C2 artefacts are **already committed at tip** (they are not untracked):

```
$ git -C … show 3cc8cd45:corpus/README.md | grep -cE '^\| F[0-9]+ \|'
49
$ git -C … show 3cc8cd45:corpus/README.md | grep -nE '^\| F49 \|' | cut -c1-120
1114:| F49 | TrendAI ZDI's own disclosure process and vendor coordination — the acquisition-programme flow (validation
$ git -C … show 3cc8cd45:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S106[[:space:]]*\|'
1
$ git -C … log --oneline -3 -- corpus/README.md
3cc8cd4 kasegi r71: late seat output (ScribeLesson round-71 lesson draft + report) after wrap-up; not a landed round
34faab9 kasegi r71: late seat output (ScribeRegistry registry-changes bullet + report) after wrap-up; not a landed round
453275f kasegi r71: preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)
```

`git log` on `corpus/README.md` shows its last content-bearing commit is `453275f` ("preserve in-flight work at hyaku run-15 wrap-up; **not a landed round**"). The tip commits `3cc8cd4`/`34faab9` are labelled "late seat output … **not a landed round**". **The F49 row and the S106 registry row therefore sit in the tree but were never landed as a round.** That is a fact about the lane's own commit labels, not a verdict on the claim.

The committed capture and entry are present and byte-intact:

```
$ sha256sum corpus/source-snapshots/round-71/S106.txt
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  S106.txt
$ ls corpus/knowledge/*.md | wc -l
87
```

Matching the frozen C2 predicate values (`knowledge 87`, `frontier 49`, `registry 106`).

---

## 1. Province fit of the round's C2 ground — per-row distinctness verdicts

Method: for each registry row named in the assignment, I took the row's **subject cell** and **teaches cell** from `corpus/SOURCES.md` (the compared line is quoted verbatim with its line number), then measured the S106 capture for that row's discriminating tokens. S106 capture = `corpus/source-snapshots/round-71/S106.txt` (148 lines, sha256 `291f36c2…6cf59db`).

### 1.1 Verdict table

| Row | Line compared | Verdict | Discriminating measurement on S106 |
|---|---|---|---|
| **S106** | `corpus/SOURCES.md:118` | **SELF — the claim's own row** | 120 days (L70), 15 business days (L70), 30/60/90 days (L70) — the only durations in the capture |
| **S003** | `:9` — "CVD program design for manufacturers and online service providers" | **DISTINCT** | S003 is *guidance for designing* a programme; S106 states *one programme's own* numbers. No design guidance in S106 |
| **S004** | `:10` — "CERT/CC's own disclosure schedule and exception practice" | **DISTINCT** | `grep -c "CERT/CC\|CERT Guide\|Coordinator"` → **0**. Different coordinator (CERT/CC vs ZDI), different interval (45 vs 120) |
| **S005** | `:11` — "Project Zero's own disclosure deadlines, patch uptake and exceptions" | **DISTINCT** | No "90 days" deadline of PZ's kind (the one `90 day` string in S106 is part of "30, 60, or 90 days", the faulty-patch tier). PZ = researcher-side programme disclosing its own findings; ZDI = acquisition programme disclosing bought findings |
| **S041** | `:47` — JPCERT/CC 2026 partnership guideline annex on ISO 29147/30111 conformance | **DISTINCT** | `grep -cE "ISO\|29147\|30111"` → **0**; `grep -cE "JPCERT\|Japan\|Japanese\|IPA \|JVN"` → **0**. S106 is a vendor-agnostic commercial programme, not a Japanese state-coordinated workflow; the 起算日 rule cannot apply to it |
| **S043** | `:49` — "HackerOne standard program policy set … what a program may authorise and the per-asset caps it sets" | **DISTINCT** | `grep -c "scope"` → **0**; `grep -c "in scope"` → **0**. S106 enumerates no in-scope asset class and states no per-asset cap. Its "no limit on the number of reports" (L60) is a submission-volume statement, not an authorisation boundary |
| **S044** | `:50` — "Bugcrowd VRT's own baseline technical severity ladder P1 to P5" | **DISTINCT** | `grep -cE "Critical\|High severity\|Medium\|Low\|Informational"` → **0**. No ladder, no severity label, no P1–P5 token |
| **S045** | `:51` — "The VRT's maintained crosswalk from VRT taxonomy ids to CWE ids" | **DISTINCT** | `grep -c "CWE-"` → **0**. No CWE id and no mapping anywhere in the capture |
| **S051** | `:57` — "Immunefi's own Web3 severity classification system v2.2 … the five levels Critical to None and the impact bullets each level lists for the Smart Contracts table" | **DISTINCT** | Same zero-severity-label measurement as S044. Nearest trap: S106 L49 "confirms its impact and severity" — a *validation step*, with **no label assigned**. No asset class, no impact bullet |
| **S095** | `:104` — "CERT/CC's adapted phase-to-five-role responsibility matrix … Reporter fix confirmation versus Vendor/Coordinator incoming-report validation" | **DISTINCT** | `grep -c "Coordinator"` → **0**. S106 L49 "Each submission begins with validation" is a *programme's own* step statement, not the CERT/CC role matrix. S095's four criteria (Reporter/Vendor/Coordinator/CNA) do not appear |

### 1.2 The one row that is NOT distinct — and it is not on the assignment's list

The assignment asks about S106 + S003/S004/S005/S041/S043/S044/S045/S051/S095. All ten are distinct. But the **nearest neighbour of the C2 ground is not on that list**, and the lane already holds it:

**F02 / S075 — ZDI's own disclosure-policy page.** `corpus/SOURCES.md:81`:
> "TrendAI Zero Day Initiative (ZDI), Disclosure Policy — https://www.zerodayinitiative.com/advisories/disclosure_policy/ … ZDI's own stated disclosure policy for acquired vulnerabilities and product-vendor coordination; not individual advisory records, reward terms or researcher submission rules"

Measured overlap of the numbers themselves:

```
$ grep -oE "five business days|four months \(120 days\)|30 days|60 days|90 days|fifteen business days" corpus/source-snapshots/round-47/S075.txt | sort | uniq -c
      1 30 days
      1 60 days
      1 90 days
      1 fifteen business days
      2 five business days
      1 four months (120 days)
$ grep -oE "15 business days|120 days|30, 60, or 90 days" corpus/source-snapshots/round-71/S106.txt | sort | uniq -c
      1 120 days
      1 15 business days
      1 30, 60, or 90 days
```

S075 (F02 case study `corpus/knowledge/zdi-disclosure-policy.md`) already holds ZDI's 120-day window, its 30/60/90 faulty-patch tiers and its 15-business-day branch. S106 states the same three numbers again, on the About page. **The three "vendor-coordination numbers" that C2's declared claim leads with are therefore not new ground** — they are ZDI's numbers, already attested at S075, restated.

Three measured wording divergences exist between the two pages, and they are the genuine delta:

```
# advisory form
S075: "issue a public advisory disclosing its findings fifteen business days after the initial contact"
S075: "publish a limited advisory including mitigation in an effort to enable the defensive community to protect the user"
S106: "publishes a full advisory"
S106: "may publish a limited advisory to protect the broader public while withholding information that could enable exploitation"
```

- S075's escalation is a **public** advisory disclosing findings; S106's is a **limited** advisory withholding exploit-enabling detail (S106 L52).
- S075's 120-day branch is **conditional on a responsive vendor** ("If a vendor response is received within the timeframe outlined above…"); S106 states 120 days unconditionally as "a standard coordination window".
- S075's 15-business-day clock runs **after a 5 + 5-business-day acknowledgement ladder**; S106's runs from "first contact" and names no ladder. S075 names the *conditions* for 30/60/90 (critical-rated + active exploitation imminent / partial protection + exploitation not imminent); S106 compresses to "depending on multiple factors".

What S106 adds that the lane does **not** hold is the **acquisition-side flow**: validate → confirm severity → formal monetary offer → payment → vendor coordination → credit/anonymity/pseudonym, plus the "no limit on reports", the vendor dossier contents, and the no-backlog guarantee. Measured absence of that ground from the whole corpus:

```
$ grep -rniE 'monetary offer|reward points|pseudonym|remain anonymous' corpus/knowledge/ | cut -c1-200
(no output)
$ grep -rniE 'vendor-agnostic|vendor agnostic' corpus/knowledge/ | cut -c1-200
(no output)
```

Zero hits across all 87 knowledge entries. **This matches attempt-1's `ScoutF49` finding** (`.ufo/waves/round-71/w1/ScoutF49.md` §1.3, "the adjacency the manifest note does NOT name"). The round-71 manifest note names F13, S005, S004, F11/F38 as non-holders — it does **not** name F02/S075.

**Recommendation to the L1 (not an action by this seat):** the F49 row as landed currently lists the 120-day / 30-60-90 / 15-business-day numbers as the row's headline topic (`corpus/README.md:1114`) even though F02/S075 already holds them; the row's own *next* cell does say "F02/S075 keeps the ZDI policy body's conditional timeline", so the distinction is acknowledged but the topic cell leads with re-stated ground. The distinctive ground is the acquisition-side flow and the three wording divergences above.

### 1.3 F49 row and its neighbours — the frontier shape at tip

```
$ grep -nE '^\| F(4[5-9]) \|' corpus/README.md | cut -c1-150
1097:| F48 | GitHub Advisory Database curation semantics — the three class sub-headings (GitHub-reviewed vulnerability, unreviewed NVD import, malware) with their admission path, alerting consequence and what each record proves; …
1114:| F49 | TrendAI ZDI's own disclosure process and vendor coordination — the acquisition-programme flow (validation, formal monetary offer, payment, vendor coordination, credit or anonymity), the 120-day standard coordination window with its 30/60/90-day shortening for flaws from incomplete or problematic patches, escalation to a limited public advisory after 15 business days of vendor silence, and the full advisory after a patch against the limited advisory when no fix arrives | admitted | knowledge/zdi-disclosure-process-and-vendor-coordination.md | S106 | …
```

F48 (GitHub Advisory Database curation semantics, S105) and F49 (ZDI, S106) are adjacent in the frontier but share no surface — F48 is a database's admission-path semantics, F49 is a programme's disclosure process. **No overlap.** The gap between them is F47 (GitHub global security advisories REST API, S103) at `:1087`.

The amendment paragraph under F49 (`corpus/README.md:1116-1118`) already carries the F02/S075 distinction:
> "the F02/S075 entry holds ZDI's policy body (a broker acquisition-disclosure timeline with an unstated clock start), not the About page's process and coordination statements."

**Verdict on the C2 ground's province fit: IN PROVINCE, and distinct from all ten named rows.** The single correction the L1 should consider is that the *numbers* in the F49 topic cell are F02/S075 ground restated, and the *new* ground is the acquisition-side flow.

---

## 2. Sibling ownership scan

### 2.1 The requested scan, verbatim

```
$ cd /home/vgpnk/Projects/shokunin && grep -lEi "acquisition[- ]programme|acquisition program|bug[- ]?bounty|disclosure[- ]polic|coordinated[- ]vulnerability[- ]disclosure|coordinated disclosure|bounty" */PROVINCE.md
chousa-shokunin/PROVINCE.md
kake-shokunin/PROVINCE.md
kasegi-shokunin/PROVINCE.md
kengaku-shokunin/PROVINCE.md
kotoba-shokunin/PROVINCE.md
revenger-shokunin/PROVINCE.md
```

Six of twenty-one lanes hit the pattern. **Every hit is a refusal, a report-out, or a bounded training module — none holds programme ground.** Per lane, with the line that decides it:

**kasegi-shokunin** (`kasegi-shokunin/PROVINCE.md:3`):
> `**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages`

The owner. Its `## Frontier` section lists F01–F10 (round-25 state) and the append-only amendments carry it to **F49 at round 71** (`PROVINCE.md` last amendment line, `[r71 Frontier amendment, appended 2026-11-05] F49 - TrendAI ZDI's own disclosure process …`). Its `## Adjacent` section names chousa (research method), kagi (secrets), kake (web properties), kengaku (LLM evaluation) — none touches programme rules. The same file's `## Refuses` line: "Live-target testing is refused; this corpus is documentation only."

**chousa-shokunin** (`chousa-shokunin/PROVINCE.md:10`):
> `**Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality`

Explicit refusal naming kasegi as the owner. Domain is "deep-research method (調査)".

**kengaku-shokunin** (`kengaku-shokunin/PROVINCE.md:31`):
> `- **kasegi:** bounty ledger mission-state / dispatcher semantics.`

Report-out, not absorption. Domain is "LLM/model research & evaluation".

**kake-shokunin** (`kake-shokunin/PROVINCE.md:291`):
> `of province: report intake, triage, remediation, disclosure timing, bounty and`

Full sentence at `:290-292`: "Vulnerability handling itself stays out of province: report intake, triage, remediation, **disclosure timing, bounty** and policy operation, and whether any named contact channel works, are not kake's ground". Kake disclaims exactly the two things F49 holds. Domain is "web properties & publishing".

**kotoba-shokunin** (`kotoba-shokunin/PROVINCE.md:67`):
> `| kasegi | adjacent | a155310d1ee9aacc07c3ce62328105a46c0392b4 | kasegi owns bounty and security research (programs, rules, claim packages; SKILL.md:3) and states no split with kotoba; …`

An adjacency ledger row that names kasegi the owner. Domain is "prompt & skill craft".

**revenger-shokunin** (`revenger-shokunin/PROVINCE.md:9-12`):
> `Bounty and coordinated-disclosure triage enters only through`
> `corpus/training/bounty-triage/MODULE.md: a written scope record gates access`
> `… activity, exploitation, third-party testing and disclosure outside the program`

The **only sibling that touches this ground at all**, and it holds it as an explicitly *gated training module*, not a corpus entry. `revenger-shokunin/corpus/training/bounty-triage/MODULE.md:1-4` states: "Status: **instruction**, not a knowledge entry. It fills no coverage-map row, carries no Evidence ID and claims no capability." Its subject is *bounty/coordinated-disclosure triage of a shipped artifact* — reverse-engineering triage, not programme rules. Domain is "reverse engineering of shipped artifacts".

### 2.2 Fleet-wide ownership confirmation and verdict

```
$ grep -rl -i 'zerodayinitiative\|zero day initiative' /home/vgpnk/Projects/shokunin/*-shokunin/ | grep -v '/\.git/' | grep -v 'kasegi-shokunin'
(no output)
```

Zero occurrences of ZDI ground in any sibling lane outside kasegi. The 15 lanes not in the §2.1 hit list (audio, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kotodama, kumitate, lore, mado, mori, souji, tabi, tameshi, tsukuroi) hold none of this ground by construction. The scan's initial narrow pattern (`acquisition|bug[- ]?bounty|disclosure[- ]policy`) matched only kaidoku, kasegi and mori — and the kaidoku/mori hits are false positives (`kaidoku-shokunin/PROVINCE.md:239` "acquisition capability" = signal/hardware acquisition; `mori-shokunin/PROVINCE.md:136` "slot acquisition" = dispatch-slot acquisition). Widening the pattern to the actual ground vocabulary produces the six refusals/report-outs listed above.

**Ownership is clean: F49/S106 is kasegi's alone.**

---

## 3. Next-round leads — five+ candidates the registry does NOT hold

Every URL below was **fetched and measured** on 2026-11-05 with the lane's instrument UA, and every one was confirmed **absent** from the registry and from the knowledge corpus:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for u in "security.apple.com/bounty" "cert.europa.eu" "knvd.krcert.or.kr" "twcert.org.tw" \
         "zerodayinitiative.com/about/benefits" "zerodayinitiative.com/about/faq" \
         "zdi_researcher_agreement" "6625378258649088" "single-reporting-platform" \
         "zerodayinitiative.com/advisories/upcoming"; do
  printf '%-46s SOURCES=%s README=%s\n' "$u" "$(grep -cF "$u" corpus/SOURCES.md)" "$(grep -cF "$u" corpus/README.md)"
done
security.apple.com/bounty                SOURCES=0 README=0
cert.europa.eu                            SOURCES=0 README=0
knvd.krcert.or.kr                        SOURCES=0 README=0
twcert.org.tw                             SOURCES=0 README=0
zerodayinitiative.com/about/benefits      SOURCES=0 README=0
zerodayinitiative.com/about/faq           SOURCES=0 README=0
zdi_researcher_agreement                  SOURCES=0 README=0
6625378258649088                          SOURCES=0 README=0
single-reporting-platform                 SOURCES=0 README=0
zerodayinitiative.com/advisories/upcoming SOURCES=0 README=0
$ grep -rlE "twcert|cert\.europa\.eu|knvd|security\.apple\.com" corpus/knowledge/ | wc -l
0
```

Measured reachability (`curl -sS -o /dev/null -A '<instrument UA>' -w 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' -L`):

```
https://www.zerodayinitiative.com/documents/zdi_researcher_agreement.pdf    HTTP 200 final=…/zdi_researcher_agreement.pdf bytes=330832
https://www.zerodayinitiative.com/about/benefits/                          HTTP 200 final=…/about/benefits/ bytes=51197
https://www.zerodayinitiative.com/about/faq/                               HTTP 200 final=…/about/faq/ bytes=92613
https://www.zerodayinitiative.com/advisories/upcoming/                     HTTP 200 final=…/advisories/upcoming/ bytes=2375636
https://bughunters.google.com/rest/v1/articles/about/rules/6625378258649088/…  HTTP 200 bytes=44048
https://security.apple.com/bounty/categories/                              HTTP 200 bytes=130105
https://security.apple.com/bounty/guidelines/                              HTTP 200 bytes=27751
https://www.twcert.org.tw/en/dl-45-75e0a2e1be7b42c99bbc2c11377e796b.html HTTP 200 bytes=589288
https://knvd.krcert.or.kr/overview/operation                               HTTP 200 bytes=749
https://cert.europa.eu/coordinated-vulnerability-disclosure-policy         HTTP 200 bytes=16996
https://www.enisa.europa.eu/…/single-reporting-platform-srp/frequently-asked-questions HTTP 200 bytes=84407
```

### Lead 1 — ZDI Researcher Agreement (the acquisition contract itself) — **ACQUISITION-PROGRAMME PRIMARY**
- **URL:** `https://www.zerodayinitiative.com/documents/zdi_researcher_agreement.pdf`
- **Programme/document:** Trend Micro's "ZERO DAY INITIATIVE RESEARCHER AGREEMENT" (PDF, 4 pages, dated **August 2017**).
- **Ground added:** the *legal* layer of the acquisition programme, which no held entry has. Measured from the PDF: §4.3 "Trend Micro Offer" — the offer amount, "Any time prior to your acceptance of a Trend Micro Offer, Trend Micro may withdraw such Trend Micro Offer"; on acceptance "you agree to convey, assign, transfer, and deliver to Trend Micro all of your right, title, and interest in and to all intellectual property in the Vulnerability Information". §4.4 "Trend Micro will use reasonable efforts to pay you within two weeks of your request" and the IRS Form 1099 / Form W-9 machinery. §5.1 confidentiality "shall not apply … after one year following the disclosure thereof to Trend Micro, and Trend Micro will have the specific right to disclose the vulnerability if you provide no response to Trend Micro for over a year". §6.1 attribution, and the **right to withhold credit** if the researcher republishes before disclosure. §6.2 the republication right after disclosure, verbatim-only. §7 the anti-scraping clause. §10 liability capped at "the DOLLAR AMOUNT Trend Micro PAYS YOU IN THE 12 MONTHS PRIOR TO THE ACTION GIVING RISE TO LIABILITY". §12 export-law compliance on Vulnerability Information.
- **Why a triager/VR analyst needs it:** this is the instrument that makes "the researcher receives their reward" (F49/S106 L49) *legally* true or false — offer mechanics, IP transfer, payment timing, credit withholding, republication limits, the one-year non-response escape. It is the acquisition counterpart to S075's vendor-side policy and to S106's About-page description, and it is the one document that states the **one-year** disclosure right that neither S075 nor S106 mentions.
- **Province:** **IN.** It is a programme's own rules document — kasegi's domain verbatim ("program rules, claim packages"). Sibling ownership clean per §2.
- **Caveat to carry:** the PDF is dated **August 2017** and names "Trend Micro", not "TrendAI"; the About page and the live site are now TrendAI-branded. A future entry must record that date and that branding difference rather than presenting it as current.

### Lead 2 — ZDI "How It Works" (payout criteria + reward-tier ladder) — **ACQUISITION-PROGRAMME PRIMARY**
- **URL:** `https://www.zerodayinitiative.com/about/benefits/`
- **Programme/document:** TrendAI ZDI, "How It Works" page (title "How It Works - TrendAI™ Zero Day Initiative™ (ZDI)").
- **Ground added:** the **payout-offer criteria** and the **reward-point tier mechanism** — exactly the ground F49's own entry declares absent ("No severity tiers, no payout amounts … the platform ladder and the reward scale live with F13"). Measured: "TrendAI™ ZDI applies consistent criteria to determine payout offers. Each submission is evaluated based on product deployment, privilege gained, exploitability under default configuration, and the product's relevance across industry environments." The six valuation criteria are printed separately: **Product deployment, Privilege gained, Default exposure, Product importance, User interaction, Exploit reliability, Attack surface**. The tier ladder: "Accepted submissions earn reward points equal to the payout value. These points accumulate toward **Bronze, Silver, Gold, and Platinum** tiers" — Bronze 15,000 points (US$2,000 one-time bonus, 10% submission bonus, 10% point multiplier), Silver 25,000 (US$5,000 / 15% / 15%), Gold 45,000 (US$10,000 / 20% / 25%), Platinum 65,000 (US$25,000 / 25% / 50%). "For every accepted vulnerability, you earn one reward point for every dollar paid." Plus the referral programme (2,500 points after the referred researcher's first acquisition) and the ownership boundary "Ownership remains with you until an offer is accepted."
- **Why it matters here:** it quantifies the "formal monetary offer" F49 names but does not price, and it gives ZDI a **programme-specific ladder** — which F13's own next-cell demands be kept separate ("Keep each platform's ladder as its own suggested baseline … do not generalize a payout scale across programs"). **This is the ground that would make F49's declared scope limit ("no severity tiers, no payout amounts") untrue as a statement about the programme.**
- **Province:** **IN.** Acquisition-programme rules, kasegi's domain; F13-shaped but a different programme.
- **Note:** this exact URL was already proposed as a lead in **round 47** (`.ufo/waves/round-47/w1/R47ScoutLeads.md:8-13`, quote "Ownership remains with you until an offer is accepted.") and **never opened as a registry row**. It is a one-round-stale unfired lead.

### Lead 3 — Google and Alphabet VRP (VRP) Rules — **ACQUISITION-PROGRAMME PRIMARY**
- **URL:** `https://bughunters.google.com/rest/v1/articles/about/rules/6625378258649088/google-and-alphabet-vulnerability-reward-program-vrp-rules`
- **Programme/document:** Google Bug Hunters, "Google and Alphabet Vulnerability Reward Program (VRP) Rules" (article `documentId` 6625378258649088, JSON via the same article API the lane already uses for S070/S072).
- **Ground added:** the **reward-decision mechanics** of a first-party acquisition programme, in a form the lane has never held: the **Domain Tier × Information Tier (IT0/IT1/IT2) × Action Criticality (Critical/Impactful/Moderate)** reward matrix with its dollar table, and the **report-quality multiplier** "we adjust the final rewards by a factor, based on the quality of the report [0.8x, 1x, or 1.2x]" with a dimension table (vulnerability description, attack preconditions, impact analysis, reproduction steps/PoC, target info, reproduction output, researcher responsiveness). Also: the **appeal window** "you can appeal the decision within 1 month of the reward notification"; the **six-month acquisition blackout**; the **"first found, first dressed"** duplicate rule; the **broker-report exclusion** — "We believe that it is against the spirit of the program to privately disclose the flaw to third parties for purposes other than actually fixing the bug. Consequently, such reports will typically not qualify"; the **sanctions/eligibility carve-out** naming Russia and Belarus; the 18+ age bar; and the "This is not a competition, but rather an experimental and discretionary rewards program" disclaimer.
- **Why it matters here:** this is the **only held-adjacent source that states the rule ZDI's own About page quietly conflicts with** — ZDI *is* a third-party buyer, and the Google rules say a report privately disclosed to a third party for a purpose other than fixing the bug "will typically not qualify". A package comparing acquisition programmes needs both statements side by side, attributed separately. S069 holds the **Google Cloud** VRP rules and S070/S072 hold the rules *directory*; the Google-and-Alphabet VRP's own reward matrix is unheld.
- **Province:** **IN.** HackerOne/Bugcrowd/Immunefi programme rules are already kasegi-held (S043/S044/S045/S051); a fourth programme's own reward matrix is the same class of ground.
- **Note:** `S069` and `S070` already name `bughunters.google.com` — a screen must show the *specific article* `6625378258649088` is not covered, which it is: `grep -cF "6625378258649088" corpus/SOURCES.md` → 0.

### Lead 4 — TWCERT/CC Coordinated Vulnerability Disclosure Policy v2.2 — **REGION-SPECIFIC (Taiwan)**
- **URL:** `https://www.twcert.org.tw/en/dl-45-75e0a2e1be7b42c99bbc2c11377e796b.html` (PDF, 12 pages, **Version 2.2, March 18, 2025**)
- **Programme/document:** TWCERT/CC (Taiwan Computer Emergency Response Team/Coordination Center, operated by NICS under the Ministry of Digital Affairs), Coordinated Vulnerability Disclosure Policy.
- **Ground added:** a **national CNA coordinator's** own disclosure clock and handling process — a region the lane has **no** Taiwan ground for (`grep -cF "twcert.org.tw" corpus/SOURCES.md` → 0; the lane's Japanese ground is S041/S042, its Korean and Taiwanese ground is nil). Measured: §3.2 "Vulnerabilities reported to TWCERT/CC will be disclosed to the public within **90 calendar days from the date the report is confirmed to be complete**", with the right "to postpone the disclosure schedule and adjust the level of detail disclosed"; §3.4 the six-step Vulnerability Handling Process (submit → initial assessment → TVN ID assigned → **basic information disclosed on the TVN platform within 90 calendar days** → forwarded to the vendor → public disclosure once all parties confirm resolution); §3.3 the **Taiwan Vulnerability Note (TVN)** platform and its field set (reporting date, detected date, affected product, description, solution, CVE ID, reference, reporter); §3.5 four **CVE Counting Rules** with Rule 4's four sub-rules (public availability, no duplicate, user-controlled version, publicly available and legally licensed product) — the CNA-scope escalation to the Root CNA; §3.6 the reporter's **name disclosure** rule, including "If the reporter does not wish to disclose their name, they may request anonymity at any time" and the consent gate before a vendor receives a reporter's contact details.
- **Why it matters here:** it is the **clock-start observation** the F02 rule demands and the ZDI entries lack. S075 explicitly leaves ZDI's 120-day start event unstated; TWCERT/CC names its own start event ("the date the report is confirmed to be complete") and its own deadline (90 calendar days) — a **third** coordinator with a **different, named** trigger, directly comparable to CERT/CC's 45 days (S004) and Project Zero's 90 days (S005). It is also the first held-candidate document carrying a **CVE-counting** rule set at coordinator level, which F07 (CNA assignment rules) does not cover for a *national coordinator's* application of them.
- **Province:** **IN.** Programme/coordination rules, kasegi's domain. Distinct from F11/F38 (ISO publisher records — normative text paywalled), from F43 (CERT/CC's phase matrix), and from F12/S041 (Japanese workflow). It is **region-specific (Taiwan)**, satisfying the assignment's requirement.

### Lead 5 — KISA/KNVD 신고포상제 joint-operation bug-bounty scheme — **REGION-SPECIFIC (Korea)**
- **URL:** `https://knvd.krcert.or.kr/overview/operation` (Korean-language; the same page's content was read in full via the reader's jina backend)
- **Programme/document:** KNVD (KISA 인터넷 보호나라 & KrCERT) — "공동 운영 제도" / 공동운영사 (joint-operation scheme) of the 신고포상제 (reporter-reward system).
- **Ground added:** **the only acquisition-programme *operating model* the lane has never seen**: a **national CERT running a bug bounty on a company's behalf and then handing the whole operation over to the company in four stages.** Measured, the four stages split intake / verification-analysis / assessment / reward-payment across KISA and the company: stage 1 = KISA does all four; stage 2 = KISA does intake + verification + analysis, the company does assessment + payment; stage 3 = the company does everything; stage 4 = the company does everything including intake. The agreement procedure is five steps (KISA briefing meeting → the company's internal decision and reward-budget allocation → signed joint-operation agreement → **quarterly evaluation committee participation in the second week of March, June, September and December** → the company pays the reporter after the final evaluation). The four "버그바운티 구축 시 고려사항" (considerations for building a bug bounty) are: 지정 대상범위(제품) — pick the in-scope product; 예산, 포상기준 마련 — set the budget and the reward criteria "취약점 보급도, 공격 유형별" (by vulnerability prevalence and by attack type); 입수체계 구축 — build the intake web page; and split the roles of verification/evaluation/budget payment. Plus MITRE CVE issuance, portal promotion and a cloud analysis platform as the supporting services.
- **Why it matters here:** F13 holds *platform* ladders (HackerOne/Bugcrowd) and F16 holds *crowdsourced-testing platform* scope (CNVD/360SRC); neither holds a **national-CERT-as-bug-bounty-operator** ground, and this document's four-stage handover answers a question no held entry can: **what does a programme look like when the coordinator and the sponsor are the same body, and how is the reward decided when two parties share the assessment?** A bounty triager deciding where to file a report needs to know which body assesses and which pays.
- **Province:** **IN.** Programme rules and reward determination, kasegi's domain. **Region-specific (Korea)**.
- **Caveat to carry:** the page is Korean-language; a future capture must pin the Korean text and any translation separately (the lane's own precedent for Japanese text is S041's 付録6 pinning).

### Lead 6 — CERT-EU coordinated vulnerability disclosure policy — **REGION-SPECIFIC (EU institutions)**
- **URL:** `https://cert.europa.eu/coordinated-vulnerability-disclosure-policy`
- **Programme/document:** CERT-EU (the CSIRT of the EU institutions), "Coordinated vulnerability disclosure policy".
- **Ground added:** a **coordinator with a three-stage disclosure ladder and an explicitly named clock trigger**. Measured: "The deadlines mentioned in the different phases below will start when we have established a contact that can reasonably be considered as appropriate to receive vulnerability information. When no such contacts have been established after reasonable attempts are made by CERT-EU, the deadlines below will also be considered started." Then: **limited disclosure to constituents** if unfixed at 30 days from notification; **limited disclosure to cybersecurity communities** (EGC, EU CSIRTs Network) at 60 days; **public disclosure normally 90 days** from first notification, extendable "if a sound justification and explanation for any delay can be produced"; and public disclosure by CERT-EU if the vendor neither responds nor offers a plan nor asks for an extension.
- **Why it matters here:** the **"clock start" sentence is exactly what S075 leaves unstated** for ZDI, and it is a third distinct start-trigger formulation alongside CERT/CC's 45-day and Project Zero's 90-day. It also adds a **two-tier limited disclosure** (constituents at 30 days, the wider security community at 60 days) that no held entry has, and which sits against S075's single "publish a limited advisory including mitigation" at the 120-day boundary.
- **Province:** **IN.** Coordinator policy, kasegi's domain (same class as S003/S004/S005). **Region-specific (EU institutions)**.
- **Caveat:** the lane already holds S024/S029 (the CRA regulation) and S104 (ENISA EUVD API, **status rejected**) — so the screen must show this is CERT-EU's own policy, distinct from the CRA's statutory reporting duties and from ENISA's database service. `grep -cF "cert.europa.eu" corpus/SOURCES.md` → 0.

### Lead 7 — ENISA CRA Single Reporting Platform FAQ — **REGION-SPECIFIC (EU), platform ground**
- **URL:** `https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp/frequently-asked-questions` (updated 15 October 2026)
- **Programme/document:** ENISA, "Frequently Asked Questions | Single Reporting Platform (SRP)".
- **Ground added:** the **operational clock mechanics of a statutory reporting platform**: the 24-hour early warning, the 72-hour notification, the 14-day final report for actively exploited vulnerabilities and the 1-month final report for severe incidents; the **72-hour counter** implementation (displayed 48 hrs after submission of the 24-hour early warning, with the known false-overdue behaviour); the **CDaC selection rule** (report to the CSIRT designated as coordinator of the Member State of main establishment, with the ordered fallbacks for no EU main establishment); the Primary/Secondary AR model (one Primary per manufacturer, up to 20 Secondary) and the validation-parallel-to-processing rule with a 20-notification allowance; the **Particularly Exceptional Circumstances** regime under Art. 16(2) and the 11 December 2025 Delegated Act; and "no Application Programming Interface (API) will be provided at the initial release of the SRP".
- **Why it matters here:** the lane holds S024/S029 (the CRA text) and S104 (EUVD API — rejected). What it does **not** hold is the **platform's own operational contract**: how the 72-hour counter is actually computed, what a report must contain at each stage, and which coordinator gets the report. For a triager deciding "where do I file this in the EU, and what will they demand of me", this is the ground.
- **Province:** **IN**, but **adjacent** to F08 (CRA manufacturer reporting duties) — the F08 next-cell already distinguishes manufacturer statutory tracks from researcher disclosure. A future admission must state that it is the *platform's operational* contract, not the *regulation's* duties. `grep -cF "single-reporting-platform" corpus/SOURCES.md` → 0.

### Lead 8 — ZDI upcoming advisories list — **ACQUISITION-PROGRAMME PRIMARY (the clock as dates)**
- **URL:** `https://www.zerodayinitiative.com/advisories/upcoming/`
- **Programme/document:** TrendAI ZDI's public upcoming-advisories list.
- **Ground added:** the **only public surface where the coordination window is visible as a date pair**. Measured over the fetched HTML: the table header is `['ZDI CAN', 'Affected Vendor(s)', 'Severity', 'Reported', 'Deadline']`; **706 rows carry ≥2 dates and the reported→deadline delta is exactly 120 days on all 706** (`Counter` → `[(120, 706)]`, zero exceptions). The same FAQ page states the semantic of a row: "Each upcoming advisory includes the vendor name and **the date the vendor was notified**."
- **Why it matters here:** it is a candidate **clock-start observation** for the very branch S075 leaves unstated. **Caution to carry:** the column header says `Reported` while the FAQ says "the date the vendor was notified" — these are not obviously the same event and a future entry must record both wordings without equating them. The list is a live, mutating surface (2,375,636 bytes at fetch time) and needs a date-stamped pin.
- **Province:** **IN.**
- **Note:** this was already proposed in attempt-1's `ScoutF49` (§3, Lead B) with the same 706/120 measurement; it remains unopened as a registry row.

### Lead 9 — Apple Security Bounty categories + guidelines + Target Flags — **ACQUISITION-PROGRAMME PRIMARY**
- **URLs:** `https://security.apple.com/bounty/categories/`, `https://security.apple.com/bounty/guidelines/`, `https://security.apple.com/bounty/target-flags/`
- **Programme/document:** Apple's own Apple Security Bounty programme pages.
- **Ground added:** the **outcome-based (not severity-ladder) reward model** of a first-party vendor programme: a reward table keyed by *entry point → end point* (network attack no interaction → kernel US$2,000,000 / user space US$350,000; wireless proximity → application processor US$1,000,000; physical access → sensitive data US$500,000; app sandbox escape → kernel US$500,000 / sensitive data US$100,000; browser attack → kernel US$1,000,000 / WebContent sandbox escape US$300,000 / Web Content code execution US$10,000) plus a services table (iCloud account data US$1,000,000 down to domain takeovers US$5,000), macOS-only rewards (Gatekeeper bypass US$100,000 down to US$1,000), Private Cloud Compute rewards (US$1,000,000 down to US$50,000), and bonus multipliers (beta software 50%, Lockdown Mode 100%, both 150%). The **Target Flags** mechanism is new ground entirely: the Commpage Target Flag and the TCC Target Flag, the three control levels (register control / arbitrary read-write / arbitrary code execution), the `_COMM_PAGE_ASB_TARGET_VALUE` / `_COMM_PAGE_ASB_TARGET_ADDRESS` registers, the requirement that a PoC **crash and produce a crash log**, and the "accelerated awards … processed immediately after the research is received and confirmed, even before a fix is available".
- **Why it matters here:** F13 holds **platform** severity ladders; Apple's is a **vendor's own** acquisition programme whose reward is keyed by *demonstrated capability*, with no severity tier at all — which is precisely the axis F13's next-cell warns against generalising across. The Guidelines page adds the triage-relevant rules: "Only the first complete and actionable report we receive for an issue is eligible for a reward"; "Publicly disclosing security issues before a fix is available makes you ineligible for all Apple Security Bounty rewards"; the 180-day pause for repeated ineligible reports; the three-week reassessment window; and the "most reports are resolved within 90 days".
- **Province:** **IN.** Programme rules and reward scale, kasegi's domain. `grep -cF "security.apple.com" corpus/SOURCES.md` → 0.

### Out-of-province markers on the lead set

**None of the nine is out of province.** CERT-EU (Lead 6) is a coordinator receiving *researcher* reports; TWCERT/CC (Lead 4) is a national CNA coordinator receiving researcher reports; KISA/KNVD (Lead 5) is a national CERT operating a *reporter-reward system* on behalf of private companies — all three sit on the researcher-facing side. **ENISA's SRP FAQ (Lead 7) is the one whose admissibility turns on a scope argument rather than a domain fit**: ENISA is an EU agency operating a **statutory** reporting platform for **manufacturers and open-source stewards**, not a bug-bounty programme a researcher reports to. It is IN only under F08's "manufacturer statutory tracks" limb, and it must not be filed as a researcher-facing programme.

---

## 4. State of the `## Leads (unopened)` section

### 4.1 The section is in `corpus/SOURCES.md`, **not** in `corpus/README.md`

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -c "^## Leads" corpus/README.md
0
$ grep -c "unopened" corpus/README.md
0
$ grep -n "^## Leads" corpus/SOURCES.md
168:## Leads (unopened)
```

`corpus/README.md` has **no** `## Leads (unopened)` section and **zero** occurrences of the word "unopened". The section lives in the registry file, `corpus/SOURCES.md`, at line 168. `git log -S "## Leads (unopened)" -- corpus/README.md` returns nothing — it never existed in the README.

### 4.2 Its exact lines at tip

```
$ awk 'NR>=167 && NR<=171 {printf "%d:%s\n", NR, $0}' corpus/SOURCES.md
167:
168:## Leads (unopened)
169:
170:- Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.
171:
```

**Yes — it names only the Fuzzilli primary documentation, and nothing else.** One heading (L168), one blank line, one bullet (L170).

### 4.3 The bullet is byte-identical to the round-71 base, and the round-71 registry bullet says so

The round-71 registry-changes bullet at `corpus/SOURCES.md:262` asserts:
> "…the cited SOURCES.md lines 137, 142, 157, 246 and the `## Leads (unopened)` Fuzzilli lead line 169 are byte-identical at base 4e33119 and at tip (exact-line sha256 dbd3f08e97adf982, 01ba4719c80b6fe9, 01ba4719c80b6fe9, 01ba4719c80b6fe9 and **0dd9b02c6cbc9c9a** respectively, base line N now at tip line N+1), and the `## Leads (unopened)` Fuzzilli line is **NOT retired**: the Fuzzilli primary documentation was not opened this round, so it stays an unopened lead."

Verified independently:

```
$ sed -n '170p' corpus/SOURCES.md | sha256sum | cut -c1-16
0dd9b02c6cbc9c9a
$ git show 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60:corpus/SOURCES.md | sed -n '169p' | sha256sum | cut -c1-16
0dd9b02c6cbc9c9a
```

Both halves match the bullet's own recorded digest. The line moved from 169 to 170 exactly because the S106 registry row insert at tip line 118 pushed everything below down by one — as the bullet states.

### 4.4 Is the Fuzzilli bullet's *substance* still current?

The bullet's deferral condition is "defer unless its tool-technique ground clears PROVINCE and sibling ownership". Two measured facts bear on that:

**(a) The Fuzzilli ground was never opened by this lane.** `grep -rl "googleprojectzero/fuzzilli" corpus/source-snapshots/` → no output; `grep -rn "googleprojectzero/fuzzilli" corpus/knowledge/` → no output. The URL appears only in the S106/S093 neighbourhood, never as a capture.

**(b) The document itself, fetched, contains no programme ground.** The README was fetched (HTTP 200, 23,894 bytes, 249 lines) and measured:

```
$ grep -icE "bounty|disclosure|reward|vulnerabilit" fuzzilli_readme.md
3
$ grep -icE "policy|timeline|deadline|coordinator" fuzzilli_readme.md
0
$ grep -icE "program" fuzzilli_readme.md
16   # every hit is "generated programs" / "FuzzIL program" / "mutated program" — the fuzzer's input programs
```

The only bounty-adjacent sentences are the README's request to send a note to a Project Zero address "possibly including a CVE number … so it can be included in the bug showcase" and "you can of course claim any bug bounty, CVE credits, etc." — a *tool-technique* document's aside, not a programme rule, timeline, disclosure policy, coordinator statement or reward scale. The sibling scan confirms no sibling holds fuzzer ground either (`grep -lEi "fuzzer|fuzzing" */PROVINCE.md` → no output across all 21 lanes).

**Assessment:** the section is **current as written** — it names exactly one lead, the Fuzzilli primary documentation, and that document is genuinely unopened. The bullet's own deferral condition ("unless its tool-technique ground clears PROVINCE and sibling ownership") now has measured evidence pointing the other way: the README carries no programme-rule, timeline, disclosure-policy, coordinator or reward-scale ground, and no sibling lane holds fuzzer ground. **The lead is not stale — it is a correctly-recorded item whose province test now looks likely to fail.** Whether to retire it is the L1's call, not this seat's.

**The gap the section does not record:** the registry's own search log and the round-47 scout file name several *unopened* documents that were never promoted into the `## Leads (unopened)` section — the ZDI "How It Works" benefits page (`corpus/SOURCES.md` round-47 lead, and `.ufo/waves/round-47/w1/R47ScoutLeads.md:8`) and HackerOne's disclosure-settings guide (`.ufo/waves/round-47/w1/R47ScoutLeads.md:16`). Both are still absent from the registry (measured §3: `SOURCES=0` for both). The round-61 reconciliation bullet (`corpus/SOURCES.md:245`) retired several older leads as opened but did not add these two back. **The section is therefore accurate but incomplete** — one recorded lead where the search log records more.

---

## 5. What I did not do, and cleanup (stated so the L1 does not over-read this)

- No C1 or C2 re-verification was attempted: this seat's assignment was reconnaissance for round 72 and the coverage frontier. The C2 counters, the S106 recheck and the census exit code are **not** measured here; only the artefacts' presence, byte identity and row/entry counts are.
- No lead URL above was captured into the lane, quoted in a knowledge entry, or registered as a row. All nine remain **leads**.
- No lane production file was written except this report. No git or jj command mutated any repository. No package was installed (no tool was needed for this seat). The `## Leads (unopened)` bullet was **not** edited — the recommendation in §4.4 is for the L1.
- Scratch tree `/fast/scratch/hyaku/kasegi-r71/ScoutNext/` held the fetched HTML/PDF/Markdown for the nine leads and the Fuzzilli README; it is removed on yield. No citable receipt was written under `/tmp` — every status code and byte count quoted above was printed by the fetch commands themselves and is reproduced inline.
