# ScoutF49 — round-71 reconnaissance: F49/S106 province & adjacency fit, sibling ownership, next-round leads

Seat: ScoutF49 (scout, leaf — no subagent dispatch). Base revision `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`.
FROZEN claims commit `0e260a54b0a670cee2915237ac403d37164c749d`.
Scratch: `/fast/scratch/hyaku/kasegi-r71/ScoutF49/` (removed on yield; receipts below are reproduced inline).
No lane production file was written except this report. No git/jj mutation, no commit, no push, no tool install.

---

## 0. Evidence base (measured)

### 0.1 The frozen claims, as read

`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60:corpus/source-snapshots/round-71/manifest.json`

C2's declared claim verbatim (claims.json, `claims[1].declared`):

> Frontier F49 admitted on S106 -- the TrendAI Zero Day Initiative's own disclosure-process and vendor-coordination statements (a 120-day standard coordination window, a shortened window for incomplete or problematic patches, escalation after 15 business days of vendor silence, the full-versus-limited advisory choice, and the validate -> monetary offer -> payment -> vendor coordination acquisition flow) -- with a new knowledge entry, its capture manifest and one mined registry row.

The manifest's own `note` (923 chars) says, in its final sentence:

> It is the acquisition-programme ground F13 (platform severity ladders and reward scales), S005 (Project Zero's 90-day policy), S004 (CERT/CC's own policy) and F11/F38 (the ISO 29147/30111 division of labour) do not hold; it is NOT a platform payout ladder, NOT a coordinator's statutory timeline and NOT any single advisory instance.

### 0.2 S106 capture integrity — verified

```
$ sha256sum S106.txt
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  S106.txt
$ wc -lc S106.txt
  148 15004 S106.txt
```

Matches the frozen values in the task statement exactly (sha256 `291f36c2…6cf59db`, 148 lines, 15004 bytes).

Manifest quote anchors re-derived by literal substring search over the 148-line capture:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106
S106:sha256 OK
S106:Q01-scope OK occurrences=2 anchor=28-ok
S106:Q02-acquisition OK occurrences=1 anchor=31-ok
S106:Q03-guarantee OK occurrences=1 anchor=47-ok
S106:Q04-validation OK occurrences=1 anchor=49-ok
S106:Q05-window OK occurrences=1 anchor=70-ok
S106:Q06-shortened OK occurrences=1 anchor=70-ok
S106:Q07-escalation OK occurrences=1 anchor=70-ok
S106:Q08-limited OK occurrences=1 anchor=52-ok
S106:Q09-full OK occurrences=1 anchor=51-ok
S106:Q10-offer OK occurrences=1 anchor=60-ok
S106:Q11-nobacklog OK occurrences=1 anchor=62-ok
S106:Q12-credit OK occurrences=1 anchor=61-ok
S106:Q13-dossier OK occurrences=1 anchor=69-ok
S106:Q14-refusal OK occurrences=1 anchor=72-ok
S106:Q15-nolimit OK occurrences=1 anchor=60-ok
EXIT=0
```

All 15 quotes land on their manifest anchors; 14 of 15 are exactly-once. **Q01-scope is the one exception**: the phrase "the world's largest vendor-agnostic vulnerability disclosure program" occurs twice — at L28 ("About TrendAI™ ZDI") and at L102 ("Earn rewards and contribute to the world's largest vendor-agnostic vulnerability disclosure program."). The lane's `source-recheck.py` accepts this under rule B2 (a non-unique quote passes when its anchor verifies), and it printed `occurrences=2 anchor=28-ok`. This is a *recorded* non-uniqueness, not a defect, but the F49 entry should cite L28 and not claim exactly-once for Q01.

### 0.3 Live cross-check of the capture against the served page

```
$ curl -sS -o zdi_about.html -w 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' \
    -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 … Chrome/120 Safari/537.36' \
    https://www.zerodayinitiative.com/about/
HTTP 200 final=https://www.zerodayinitiative.com/about/ bytes=54328
```

All 15 manifest quotes were re-found in the tag-stripped live HTML. The capture is faithful to the page as served on 2026-11-04. No drift detected between the pinned capture and the live page for any quoted sentence.

**One capture-fidelity caveat for the scribe**: the capture retains HTML-comment residue from the page template at L2-L4 and L125 — `"(from the old blog.html shell)."`, `"Swap this in if the full responsive set above causes background styling issues."`, `"-->"`. Confirmed present in the live source HTML inside `<!-- HAND-SWAP FALLBACK: … -->`. This is not new to round 71: the same residue is present in the round-47 S075 capture (`corpus/source-snapshots/round-47/S075.txt:3-4` and `:37`), so it is a capture-source.py tag-stripping property, not a round-71 regression. The residue sits outside every quoted range, so no quote is affected.

---

## 1. Province and adjacency fit — per row

The question asked: is the ZDI About page's ground (a vendor-agnostic acquisition programme's own disclosure process and vendor-coordination windows) distinct from each row, or does one already hold it?

### 1.1 Summary table

| Row | Row's held ground (evidence line compared) | Verdict |
|---|---|---|
| F13 | Program severity ladders and reward scales; `corpus/README.md:264`; entry `knowledge/program-severity-ladders-and-reward-scales.md` over S043/S044/S045 | **DISTINCT** — S106 carries no severity level and no payout scale |
| F15 | A vendor's research programme as an intake route for other vendors' bugs; `corpus/README.md:309`; entry over S048 (Microsoft MSVR) | **DISTINCT** — ZDI is the coordinator/buyer, not a vendor's intake route |
| F17 | Immunefi VSCS v2.2 Web3/smart-contract severity classification; `corpus/README.md:361`; entry over S051 | **DISTINCT** — S106 states no severity level for any asset class |
| F18 | CISA KEV catalog, exploitation-status prioritization; `corpus/README.md:388`; entry over S052 | **DISTINCT** — S106 makes no exploitation-prioritization claim |
| S003 | CISA supplier guide, time-frame design; `corpus/SOURCES.md:9` | **DISTINCT** — S003 designs programs, S106 states one program's own numbers |
| S004 | CERT/CC's own disclosure policy, 45 days; `corpus/SOURCES.md:10` | **DISTINCT** — different coordinator, different interval |
| S005 | Project Zero's own 90-day deadline; `corpus/SOURCES.md:11` | **DISTINCT** — different coordinator, different interval, different subject |
| S022 | CVE CNA Operational Rules v4.1.0 — **status `rejected`**, superseded by S030; `corpus/SOURCES.md:28` | **DISTINCT and unusable** — S022 is a rejected row with no capture; S106 is not CNA-numbering ground |
| S043 | HackerOne standard program policy set (scope/assets, per-asset caps, DoS reward); `corpus/SOURCES.md:49` | **DISTINCT** — S106 states no scope list and no cap |
| S044 | Bugcrowd VRT P1-P5 baseline ladder; `corpus/SOURCES.md:50` | **DISTINCT** — no ladder in S106 |
| S045 | Bugcrowd VRT→CWE crosswalk dataset; `corpus/SOURCES.md:51` | **DISTINCT** — no CWE mapping in S106 |
| S051 | Immunefi VSCS v2.2 impact bullets; `corpus/SOURCES.md:57` | **DISTINCT** — no impact bullets in S106 |

### 1.2 Per-row evidence, as measured

**F13** (`corpus/README.md:264`) — cell 5 reads: *"Keep each platform's ladder as its own suggested baseline — distinct from CVSS-B and from other programs' reward ceilings; do not generalize a payout scale across programs."* The entry `corpus/knowledge/program-severity-ladders-and-reward-scales.md` holds HackerOne's per-asset DoS cap (`S043.txt:170`, "capped at the **Medium** severity bounty rate for the affected asset"), Bugcrowd's P1–P5 mapping (`S044.txt:33`), and the VRT→CWE crosswalk (`S045.txt:73`, `:91-94`).
Measured on S106:

```
$ grep -niE 'critical|high severity|medium|low severity|informational' S106.txt | cut -c1-260
28:…is the world's largest vendor-agnostic vulnerability disclosure program…
43:…Pwn2Own breakthroughs to coordinated disclosures across critical industries…
63:…across critical infrastructure, enterprise platforms, consumer technologies, and industrial systems…
93:…coordinated fixes that strengthen products, platforms, and critical systems worldwide…
```

All four hits are the adjective "critical" in prose; **zero severity labels** (Critical/High/Medium/Low/Informational as a ladder) occur. Payout figures:

```
$ grep -nE 'US\$|\$[0-9]|[0-9]+%|[0-9]+ ?(points|point)' S106.txt
96:73%
```

The single hit is `73% of all global disclosures in 2024` (L96-97) — a market-share statistic, not a reward scale. S106 states "issues a formal monetary offer" (L60) with **no amount, no band, no ceiling, no point multiplier**. Verdict: **DISTINCT**. The F13 next-cell's own instruction ("do not generalize a payout scale across programs") is satisfied — S106 names no ladder to generalize.

**F15** (`corpus/README.md:309`) — cell 5: *"Record which party coordinates a multi-vendor finding — the vendor itself, as S048's three intake routes and self-named coordinator role state, or an external centre, as F10's S039/S040 rows route it — and read no clock, contact or agreement into an intake route: the pinned capture states none."* F15's subject is Microsoft's MSVR as an **intake route for other vendors' bugs** (`corpus/knowledge/vendor-third-party-finding-coordination.md:17-39`, three routes at `S048.txt:32-34`, three-role sentence at `S048.txt:35`). S106's subject is ZDI acting as **acquirer and coordinator**: "TrendAI™ ZDI handles all communication with the affected vendor" (L61) and "a complete technical dossier, which includes proof of concept, reproducible steps, severity assessment" (L69). F15 is a *vendor* programme receiving other vendors' findings; S106 is a *third-party* programme buying from researchers and driving the vendor to a patch. The two directions of the flow differ. Verdict: **DISTINCT**. Note F15's cell 5 explicitly anticipates "an external centre" as a coordinator role — S106 is exactly that role, so the F49 entry should say so explicitly rather than treat F15 as a rival.

**F17** (`corpus/README.md:361`) — cell 5 reads a level "from Immunefi's own per-asset-class table", citing `S051.txt:52`, `:55-56`, `:75`, `:88`. F17's subject is a five-level Web3 severity taxonomy with per-asset impact bullets. S106 contains no level, no asset class, and no impact bullet (measured above: zero severity labels). The nearest severity-adjacent sentence is S106 L49 "confirms its impact and severity" — a *validation step*, not a taxonomy. Verdict: **DISTINCT**. This is the sharpest trap in the set: S106 says "confirms its impact and severity", which superficially resembles F13/F17 vocabulary but assigns no label to it.

**F18** (`corpus/README.md:388`) — cell 5: *"KEV listing is an exploitation-status signal, not a severity score — the feed carries no severity field."* F18's subject is a prioritized catalog of known-exploited vulnerabilities. S106 makes no prioritization-by-exploitation claim at all. Its only forward-looking protection sentence (L42, L79) is about ZDI deploying its own filters before vendor patches — a *mitigation* statement, not an exploitation-status ranking, and the page names no KEV-equivalent list. Verdict: **DISTINCT**.

**S003** (`corpus/SOURCES.md:9`) — "Establishing a Coordinated Vulnerability Disclosure Program to Work With Security Researchers", scope cell: "CVD program design for manufacturers and online service providers"; teaches cell: "Design a public policy and triage, remediation and identifier-assignment process, with a coordinator available when useful." S003 is **guidance on how to design a program** ("Establish Reasonable Time Frames for Remediation and Disclosure of Reported Vulnerabilities", PDF p. 6, quoted at `corpus/knowledge/coordinated-disclosure-timelines.md:26`). S106 is one program's **own stated numbers**. The two are of different logical type. Verdict: **DISTINCT**.

**S004** (`corpus/SOURCES.md:10`) — CERT/CC's own policy, 45 days after the initial report (`corpus/knowledge/coordinated-disclosure-timelines.md:28`). S004's coordinator is CERT/CC; S106's is ZDI; the intervals (45 vs 120) and triggers differ. Verdict: **DISTINCT**. The F02 rule that governs ("Do not transplant CERT/CC or Project Zero intervals into another policy record", `coordinated-disclosure-timelines.md:14`) is not violated by S106 because S106 speaks only for ZDI.

**S005** (`corpus/SOURCES.md:11`) — Project Zero's 90-day deadline and 14-day grace extension (`coordinated-disclosure-timelines.md:30-31`). Project Zero is a **researcher-side** programme disclosing *its own* findings; ZDI is an **acquisition** programme disclosing *bought* findings on a vendor's product. Different party, different clock, different subject. Verdict: **DISTINCT**.

**S022** (`corpus/SOURCES.md:28`) — status cell reads `rejected`; teaches cell: "REJECTED: superseded by S030 (CNA Rules v4.2.0 …); no lane capture of the v4.1.0 PDF exists." S022 is a **CVE-numbering** ruleset, not disclosure-timing ground, and it is a rejected row with no capture — it can hold nothing. Verdict: **DISTINCT and unusable**; S106 has no CVE-numbering content (no CVE id appears in the capture: `grep -c 'CVE-' S106.txt` → 0).

**S043** (`corpus/SOURCES.md:49`) — HackerOne's standard program policy record: Program Scope and Assets (In Scope/Out of Scope), the DoS reward cap, the same-finding rule. S106 states **no scope list** — it says the programme is vendor-agnostic (L28) and buys zero-days (L31) but enumerates no in-scope asset class. The "no limit on the number of reports" line (S106 L60, Q15) is a submission-volume statement, not an authorization boundary. Verdict: **DISTINCT**.

**S044** (`corpus/SOURCES.md:50`) — Bugcrowd VRT P1–P5 ladder with the P1-P5 override sentence at `S044.txt:11`. S106 has no ladder (measured above). Verdict: **DISTINCT**.

**S045** (`corpus/SOURCES.md:51`) — the VRT CWE crosswalk dataset. S106 contains no CWE id and no mapping. Verdict: **DISTINCT**.

**S051** (`corpus/SOURCES.md:57`) — Immunefi's five-level VSCS impact bullets for Smart Contracts. Same measurement as F17: zero severity levels in S106. Verdict: **DISTINCT**.

### 1.3 The adjacency the manifest note does NOT name — the material finding

The manifest note enumerates F13, S005, S004 and F11/F38 as the non-holders. Those all check out. But **neither the note nor the frozen claim names F02 or S075**, which is where the real overlap lives.

**F02 already holds ZDI's coordination windows.** `corpus/README.md:203` reads `| F02 | Coordinated-disclosure timelines | admitted | knowledge/coordinated-disclosure-timelines.md | S003, S004, S005 | Compare stated timelines while preserving each source's attribution. |`, and the F02 entry's own recheck line runs `source-recheck.py … --source S003 && --source S004 && --source S005`. **S075 is not in that entry's recheck list** — S075 lives in a *separate* F02 case-study entry, `corpus/knowledge/zdi-disclosure-policy.md`, whose `source:` line reads:

```
source: S075 — https://www.zerodayinitiative.com/advisories/disclosure_policy/ — … policy body lines 20-27 …
```

That entry already tabulates, with the same three numbers F49's About page now carries:

| Branch | S075 held text | S106 (new) text |
|---|---|---|
| Standard window | "four months (120 days) to address the vulnerability" (`S075.txt:24`) | "standard coordination window of 120 days" (`S106.txt:70`, Q05) |
| Faulty-patch tiers | 30 / 60 / 90 days (`S075.txt:25`) | "30, 60, or 90 days, depending on multiple factors" (`S106.txt:70`, Q06) |
| Vendor silence | "fifteen business days after the initial contact" (`S075.txt:23`) | "fails to respond within 15 business days of first contact" (`S106.txt:70`, Q07) |
| Advisory form | "publish a limited advisory including mitigation" (`S075.txt:24`) | "may publish a limited advisory" (`S106.txt:52`, Q08); "publishes a full advisory" (`S106.txt:51`, Q09) |

Measured overlap of the numbers themselves:

```
$ grep -c '120 days' corpus/source-snapshots/round-47/S075.txt   -> 1
$ grep -c '30 days\|60 days\|90 days' …/S075.txt                 -> 1
$ grep -c 'fifteen business days' …/S075.txt                     -> 1
$ grep -c '120' S106.txt ; grep -c '30, 60, or 90' S106.txt ; grep -c '15 business days' S106.txt
1 / 1 / 1
```

So the *clock numbers* F49's About page carries are the same numbers the lane already holds from ZDI's own disclosure-policy page. The About page is a **second, marketing-shaped statement of the same ZDI policy**, and it differs from S075 in wording and in one substantive way:

- **S075's escalation is a *public* advisory disclosing findings; S106's is a *limited* advisory withholding exploit-enabling detail.** S075 L23: "may issue a public advisory disclosing its findings fifteen business days after the initial contact." S106 L70 (Q07): "may escalate to a **limited** public advisory to protect users." S106 L52 (Q08): "may publish a limited advisory … while withholding information that could enable exploitation."
- **S075's 120-day branch is conditional on a responsive vendor** ("If a vendor response is received within the timeframe outlined above, TrendAI™ ZDI will allow the vendor four months (120 days)…"). S106 states the 120 days unconditionally as the "standard coordination window". A reader who merges the two pages could wrongly conclude S106 states a flat 120-day rule with no responsiveness condition, or that S075's rule is unconditional.
- **S075's 15-business-day clock starts after the acknowledgement ladder** (5 business days to acknowledge, +5 to a second attempt, then an intermediary, then "exhausts all reasonable means"). S106's 15 business days runs from "first contact" with no acknowledgement ladder named on the About page. The About page does not carry the 5+5-day ladder; S075 does.
- **S075 names a 30-day branch condition S106 omits** (critical-rated with active exploitation imminent) and the 60-day condition (partial protection, exploitation not imminent). S106 compresses all three to "depending on multiple factors".

**Consequence for the round.** The frozen C2 claim's declared ground lists four of five items that are *already held by the lane* through S075/F02 — the 120-day window, the 30/60/90 shortening, the 15-business-day escalation, and the full-vs-limited advisory choice. What S106 adds that the lane does **not** hold is the **acquisition-side flow**: validate → confirm severity → **formal monetary offer** → payment → vendor coordination → credit/anonymity/pseudonym, plus the "no limit on reports", the dossier contents, and the "never swept under the rug / no backlog" guarantee. Measured confirmation that this ground is unheld:

```
$ grep -rniE 'monetary offer|reward points|pseudonym|remain anonymous' corpus/knowledge/ | cut -c1-200
(no output)
$ grep -rniE 'vendor-agnostic|vendor agnostic' corpus/knowledge/ | cut -c1-200
(no output)
```

Zero hits in all 86 knowledge entries. The frozen claim's own framing — "the validate -> monetary offer -> payment acquisition flow" — is the genuinely new ground; the coordination windows are re-statements.

**Recommendation to the L1 (not an action by this seat):** the F49 entry must not present the 120/30-60-90/15-business-day numbers as new ground; it must carry them as ZDI's numbers already attested at S075, and hang the F49 admission on the acquisition-side flow and on the two wording divergences measured above. Whether F49 as a *frontier row* survives this is the L1's call — the frozen claim's predicate names `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`, so the entry's file name and the row's scope limit should carry the distinction.

### 1.4 Adjacency check against F10 and F43 (not asked, but adjacent)

- **F10** (`corpus/README.md:211`) — vendor-side disclosure policies as corpus objects, over S036–S040 (Cybozu, GMO Pepabo, Hitachi) and the Cisco crosswalk. Measured: `grep -niE 'zdi|zeroday|trend' corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` → **no output**. ZDI is absent from the F10 crosswalk, and S106 is a *programme* page, not a vendor's own product-policy page — the same "a policy page is not a programme" line F10 draws for Japanese vendors (`vendor-disclosure-policies-as-corpus-objects.md`, "Rejected over-generalizations" #1). Distinct, and the F10 precedent supports F49's framing.
- **F43** (`corpus/README.md:1031`) — CERT/CC's phase-to-five-role matrix, Validation rows at `S095.txt:129-134`. S106 L49 "Each submission begins with validation" is a *programme's own* step statement, not the CERT/CC role matrix. Distinct.

---

## 2. Sibling ownership — chousa / kengaku / kagi / kake

**Verdict: no sibling holds this ground. All four explicitly route it away from themselves, and one explicitly refuses it to kasegi.**

### 2.1 chousa — explicit refusal, points at kasegi

`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md:10`:
> **Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku); …

`/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md:60`:
> **Refuses bounty-program scope** — that is kasegi (program rules, claim packages).

`chousa-shokunin/SKILL.md:10`:
> verified against its source. Not the bounty programs (kasegi) and not model

Chousa holds *research method* (question framing, source hierarchy, citation chaining). It refuses program scope **and names kasegi as the owner**. Corpus sweep: `grep -rliE 'coordinated vulnerability disclosure|vendor coordination|bug bounty program|disclosure window|advisory deadline' chousa-shokunin/corpus/knowledge/` → **0 files**.

### 2.2 kengaku — LLM/model evaluation; reports bounty ground to kasegi

`/home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md:1`:
> **Domain:** LLM/model research & evaluation …

`kengaku-shokunin/PROVINCE.md:31`:
> - **kasegi:** bounty ledger mission-state / dispatcher semantics.

`kengaku-shokunin/PROVINCE.md:76` records the `~/Projects/bounties/` loss as a **report-out to kasegi**, not a kengaku absorption. Corpus sweep → **0 files**; `grep -niE 'zeroday|hackerone|bugcrowd|immunefi|bug.bounty' kengaku-shokunin/corpus/SOURCES.md` → **0 hits** across 265 registry rows.

### 2.3 kagi — secrets and vault ops; no disclosure ground

`/home/vgpnk/Projects/shokunin/kagi-shokunin/PROVINCE.md:3`:
> **Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence

`grep -niE 'zeroday|disclosure polic|coordinated vulnerability|bounty|bug bounty|severity ladder|reward scale' kagi-shokunin/PROVINCE.md kagi-shokunin/SKILL.md` → **0 hits**. Corpus sweep → **0 files**; 88 registry rows, **0** hits for any bounty-platform name.

### 2.4 kake — web properties; explicitly disclaims the ground

`/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:3`:
> **Domain:** web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys

`/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:291-293` — the decisive line:
> Vulnerability handling itself stays out of province: report intake, triage, remediation, **disclosure timing, bounty and policy operation**, and whether any named contact channel works, are not kake's ground …

Kake disclaims exactly the two things F49 holds (disclosure timing; programme rules). Corpus sweep → **0 files**; 207 registry rows, **0** hits for bounty-platform names.

### 2.5 Fleet-wide confirmation

```
$ grep -rl -i 'zerodayinitiative\|zero day initiative' /home/vgpnk/Projects/shokunin/*-shokunin/ \
    | grep -v '/\.git/' | grep -v 'kasegi-shokunin'
(no output)
```

**Zero occurrences of ZDI ground in any sibling lane outside kasegi.** Kasegi's own PROVINCE.md confirms the adjacency list (`## Adjacent`: chousa — research method; kagi — secrets; kake — web properties; kengaku — LLM evaluation) and none of those four touches programme rules. **Ownership is clean: F49/S106 is kasegi's alone.**

---

## 3. Next-round leads — the registry does not hold these

The `## Leads (unopened)` section (`corpus/SOURCES.md:167-169`) currently names exactly one item:

> - Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.

Five candidate sources a bounty triager would need, all verified absent from the registry and reachable on 2026-11-04. **None of the five is in the registry** (measured: `grep -c` over `corpus/SOURCES.md`, `corpus/README.md` and `corpus/knowledge/` → 0 for every candidate path).

### Lead A — ZDI "How It Works" (benefits) — the reward-offer criteria and tier ladder
- **URL:** `https://www.zerodayinitiative.com/about/benefits/`
- **Programme/document:** TrendAI™ ZDI, "How It Works" page (page title "How It Works - TrendAI™ Zero Day Initiative™ (ZDI)")
- **Ground added:** the **payout-offer criteria and the reward-tier mechanism**, which no held entry has. Measured from the live page: "TrendAI™ ZDI applies consistent criteria to determine payout offers. Each submission is evaluated based on **product deployment, privilege gained, exploitability under default configuration**, and the product's relevance across industry environments." Plus: "Accepted submissions earn reward points equal to the payout value. These points accumulate toward **Bronze, Silver, Gold, and Platinum** tiers"; "For every accepted vulnerability, you earn **one reward point for every dollar paid**"; "a Platinum researcher receiving a US$4,000 valuation would receive US$5,000 (25% bonus) and 6,000 reward points (50% multiplier)"; and "**Ownership remains with you until an offer is accepted.**"
- **Why it matters here:** this is the acquisition-side ground S106 gestures at ("issues a formal monetary offer", L60) but does not quantify. It is **F13-adjacent** — F13 holds HackerOne/Bugcrowd ladders, and this would be ZDI's own ladder under F13's own rule ("keep each platform's ladder as its own suggested baseline").
- **Province:** IN. Sibling ownership: clean per §2.
- **Already screened before:** `.ufo/waves/round-47/w1/R47ScoutLeads.md` §1 proposed this exact URL as "the strongest broker-adjacent lead" with the quote "Ownership remains with you until an offer is accepted." and the same reasoning ("F30's held S075 is the broker-to-vendor disclosure policy, not the researcher-to-broker acquisition workflow"). It was never opened as a registry row. This is a **one-round-old unfired lead**, and it is the single highest-value item on this list.
- **Reachability measured:** `HTTP 200 … bytes=51197`.

### Lead B — ZDI "Upcoming Advisories" — the coordination window as *observable dates*
- **URL:** `https://www.zerodayinitiative.com/advisories/upcoming/`
- **Programme/document:** TrendAI™ ZDI, public upcoming-advisories list (the same surface the FAQ describes: "TrendAI™ ZDI already provides visibility into upcoming advisories through its public upcoming advisories list")
- **Ground added:** the **only public surface where the 120-day window is visible as a date pair**. The table carries columns `ZDI CAN | Affected Vendor(s) | Severity | Reported | Deadline | Discovered By`. Measured over the live page: 706 dated rows parsed, **and the reported→deadline delta is exactly 120 days on all 706 rows** (`Counter` → `[(120, 706)]`, zero exceptions). Example: `ZDI-CAN-36787 | Autodesk | CVSS: 7.8 | reported 2026-11-04 | deadline 2027-03-04`. 162 distinct vendors.
- **Why it matters here:** the F02 rule (`coordinated-disclosure-timelines.md:11`) demands "the clock trigger and its date are stated". S075 explicitly leaves the 120-day clock's **start event unstated** ("its clock's start event is unstated: receipt of a timely vendor response selects this branch without explicitly identifying the date from which the interval runs", `corpus/knowledge/zdi-disclosure-policy.md`, Scope and decision rule). The upcoming list supplies a per-row `Reported` date and a `Deadline` date 120 days later — **a candidate clock-start observation the lane currently lacks**, and the ZDI FAQ states the semantic of the row: "Each upcoming advisory includes the vendor name and **the date the vendor was notified**."
- **Caution to record:** the column header is `Reported`, the FAQ says "the date the vendor was notified". Those are not obviously the same event. A future entry must not silently equate them; it must record both wordings. Also note the list is a **live, mutating** surface — a future capture needs a date-stamped pin, exactly as round 47 did for S075.
- **Province:** IN. **Reachability measured:** `HTTP 200 … bytes=2368941`.

### Lead C — ZDI FAQ — acquisition criteria, exclusivity, duplicate-report rule
- **URL:** `https://www.zerodayinitiative.com/about/faq/`
- **Programme/document:** TrendAI™ ZDI, FAQ page
- **Ground added:** the **programme's own acceptance and exclusivity rules**, which no held entry has. Measured from the live page: "TrendAI™ ZDI accepts **previously unpatched** vulnerabilities in a wide range of products, including … operating systems, browsers, enterprise and consumer software, industrial control systems, and products listed in Pwn2Own tracks"; "TrendAI™ ZDI evaluates findings based on **exploitability and real-world impact, clarity and reproducibility** of the submission, security relevance, affected vendor or product coverage, and our disclosure policy. Submissions that cannot be reproduced or verified will not be acquired."; the duplicate rule "the **first researcher** who provides information that can be verified by the TrendAI™ ZDI team will be compensated … Subsequent researchers submitting the same vulnerability will not."; the exclusivity rule and its sanction "If researchers violate exclusivity, they will be **prohibited from participating** in TrendAI™ ZDI."; the residency limit "under US law, we are unable to accept researchers who reside in **Cuba, Iran, North Korea, Sudan, or Syria**."; and the vendor-contact ladder "If the vendor does not respond within **five business days**, TrendAI™ ZDI follows up with another attempt. A lack of response after **10 business days** prompts us to reach the vendor through alternative channels, including industry partners, or the national or local CERT."
- **Why it matters here:** the 5 / 10-business-day ladder here is a **third** statement of the acknowledgement ladder, and it corroborates S075's 5 + 5 + intermediary shape in the FAQ's own wording — a useful cross-check on the F49 entry's escalation wording, and the "acquisition criteria" is exactly the missing half of the acquisition-side ground.
- **Province:** IN. **Reachability measured:** `HTTP 200 … bytes=92613`.

### Lead D — ZDI faulty-patch blog post — the *reason* behind 30/60/90
- **URL:** `https://www.zerodayinitiative.com/blog/2022/8/11/new-disclosure-timelines-for-bugs-from-faulty-patches`
- **Programme/document:** TrendAI™ ZDI blog, "New Disclosure Timelines for Bugs Resulting from Incomplete Patches"
- **Ground added:** the **derivation** of the tiered windows, which S075 names but does not contain ("For additional details on this portion of our disclosure policy, please refer to this blog entry", `S075.txt:25`) and which S106 points at but does not contain ("The details of our failed patch disclosure policy can be found here.", `S106.txt:70`). Measured from the live page: "Our standard 120-day disclosure timeline for most vulnerabilities remains, but for bug reports that result from faulty or incomplete patches, we will use a shorter timeline. Moving forward, the ZDI will adopt a tiered approach based on the **severity of the bug and the efficacy of the patch**"; and the historical datum "our disclosure timeline **used to be 180 days**".
- **Why it matters here:** it is the **primary document behind both** the S075 tier table and the S106 Q06 sentence, and it is the natural answer to the branch-condition loss measured in §1.3 (S106 compresses three distinct branches into "depending on multiple factors"). It also carries the one historical figure no held entry has (the prior 180-day timeline).
- **Province:** IN. **Reachability measured:** `HTTP 200 … bytes=87537`.

### Lead E — HackerOne's platform disclosure-settings article — the platform-side contrast
- **URL:** `https://docs.hackerone.com/en/articles/8517457-disclosure-coordinated-vulnerability-disclosure`
- **Programme/document:** HackerOne Docs, "Disclosure & Coordinated Vulnerability Disclosure" (HackerOne's own platform settings)
- **Ground added:** the **platform-controlled publication setting** as distinct from a coordinator's own clock. Measured from the live page (2026-11-04, HTTP 200, 133273 bytes): "**Explicit approval must be received** regardless of report status." as the Details cell of the "Disclosure Requiring Mutual Agreement" setting; and a no-response public-disclosure default of 30 days for Resolved reports only, with other closed states requiring mutual agreement.
- **Why it matters here:** the lane holds HackerOne's safe-harbor (S006-equivalent, `corpus/SOURCES.md:12`) and its standard program policy (S043, `:49`) but **not** its disclosure-settings guide. This is the direct platform-side contrast to F49's broker-side clock, and it separates "the platform's setting" from "the coordinator's policy" — the distinction F02's rule ("the policy or coordinator is named") turns on.
- **Also already screened before:** `.ufo/waves/round-47/w1/R47ScoutLeads.md` §2 proposed it as "the strongest platform contrast" with the same quote and the same reasoning. Never opened as a registry row.
- **Province:** IN (HackerOne programme rules are kasegi's own domain; S043/S044/S044 are already held there). Sibling ownership: clean per §2.

### Out-of-province markers on the lead set

- **Lead A is the only one that could tempt a sibling lane.** Its reward-tier language ("Bronze, Silver, Gold, Platinum", point multipliers) is a **programme rules** object → kasegi, not chousa's method, not kake's web properties. It is IN.
- **A sixth candidate considered and marked OUT OF PROVINCE:** ZDI's **researcher portal registration page** `https://www.zerodayinitiative.com/portal/register/` (HTTP 200, 36987 bytes). The only program-rule content is an account-activation expiry ("You will have 7 days to activate your account before the link expires"), i.e. **onboarding, not disclosure or programme rules**. It was already screened as a lead in round 47 (`R47ScoutLeads.md` §3, "likely supporting ground for a later researcher-submission entry, not sufficient by itself to justify a new frontier"). Recommend **not** opening it as a frontier row; if opened at all, mark it tier C and supporting.
- **A seventh candidate considered and marked OUT OF PROVINCE:** the ZDI **PGP key** `https://www.zerodayinitiative.com/documents/zdi-pgp-key.asc` (HTTP 200, 8543 bytes). Cryptographic key material is `kagi`'s subject (secrets & vault custody) and is not programme-rule ground. Do not open in kasegi.
- **Pwn2Own contest rules** (`https://www.trendmicro.com/en_us/zero-day-initiative/pwn2own.html`, HTTP 200, 413708 bytes) are **adjacent but out of scope for F49's ground**: a contest with cash prizes and "Master of Pwn" points is a reward structure, not a disclosure-process or vendor-coordination window. If the lane ever wants it, it belongs to the F13 reward-scale line, not to a disclosure frontier row.

### Note on the existing Fuzzilli lead (no change proposed)

The one lead the registry already carries, `https://github.com/googleprojectzero/fuzzilli`, remains a **tool-technique** lead — it is the F41/F42 family (Project Zero's fuzzer comparisons, `corpus/README.md` F41/F42 rows, sources S093/S094). It is **not** a bounty triager document: it does not state a programme rule, a disclosure window, or a reward scale. Its existing disposition ("defer unless its tool-technique ground clears PROVINCE and sibling ownership") stands; this seat proposes no change and does not recommend opening it for a triager need.

---

## 4. Residual unknowns and limits

1. **I did not open a byte-pinned capture of any lead.** All lead-page content in §3 comes from live HTML fetched on 2026-11-04 with a browser UA (recorded byte counts above), read via tag-stripping in a scratch script. None of it is a lane capture, has a sha256, or is admissible as a registry row. Every lead needs a `capture-source.py` capture, a manifest with located quotes, and a recheck before it can be cited.
2. **The published-advisories index** `https://www.zerodayinitiative.com/advisories/published/` (HTTP 200, 2748393 bytes; 875 table rows; header `ZDI ID | ZDI CAN | Vendor/Product | CVE | CVSS | Published | Updated`) was fetched and inspected while screening, and **deliberately not proposed as a lead**: round 43 already screened this surface and refused ZDI-26-811 as a claim-package exemplar ("no fix commit and no scope or reward sentence", `.ufo/waves/round-43/w1/ScoutSourceHunt.md:60`, `:126`). Re-proposing the same surface risks re-opening a closed decision. It is listed here only so the L1 knows it was examined and why it was dropped.
3. **The 706-row 120-day uniformity in Lead B is a single-day observation** (2026-11-04). Whether the "Reported" column is a report-received date, a vendor-notification date, or a can-id-open date is **not resolved** by the pages I read; the FAQ's "the date the vendor was notified" and the table's `Reported` header are different wordings. A future entry must not equate them without a locating quote.
4. **The C1 side of round 71 was not examined** by this seat — the assignment is scoped to C2's province/adjacency fit and the round-and-next-round reconnaissance. C1's gate behaviour is other seats' scope (`ReviewerC1`, `CriticC1`, `MutationC1`, `SentinelGate`, `ExecRerun`, `ExecSelftest`).
5. **No sibling repo was written to.** All sibling reads were `grep`/`cat`/`sed -n` over `/home/vgpnk/Projects/shokunin/{chousa,kengaku,kagi,kake}-shokunin/`. The one write outside my scratch was this report file.
6. **No tools installed**, so no tool/version/channel/reason entry is required.
7. **Quiescence note for the L1 (R110).** `corpus/QUALITY.md` gained an R110 row in the working tree during this wave (a one-line append by another seat, not by me), requiring `git status --porcelain` to print nothing at round close. This report file is untracked under `.ufo/waves/round-71/w1/` and will need the L1's commit together with the other wave-1 reports; the sibling authoring seats' `corpus/QUALITY.md` edit must also land or be reverted before the quiescence gate can pass. I did not touch `corpus/QUALITY.md` and did not commit anything.

---

## 5. What I ran, and what it printed

Commands are reproducible from the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; the live-URL fetches ran from `/fast/scratch/hyaku/kasegi-r71/ScoutF49`.

```
git show 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60:corpus/source-snapshots/round-71/manifest.json
git show 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60:corpus/source-snapshots/round-71/S106.txt > S106.txt
sha256sum S106.txt                      -> 291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db
wc -lc S106.txt                          -> 148 15004
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106   -> 16 OK lines, EXIT=0
grep -nE '^\| F(13|15|17|18) \|' corpus/README.md
grep -nE '^\|[[:space:]]*S(003|004|005|022|043|044|045|051|106)[[:space:]]*\|' corpus/SOURCES.md
grep -nE '^\| F(02|10|11|38|43|48) \|' corpus/README.md
grep -rniE 'monetary offer|reward points|pseudonym|remain anonymous' corpus/knowledge/     -> 0
grep -rniE 'vendor-agnostic|vendor agnostic' corpus/knowledge/                           -> 0
grep -niE 'zdi|zeroday|trend' corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md   -> 0
grep -rcE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
grep -cE '^\| F[0-9]+ \|' corpus/README.md
for r in chousa kengaku kagi kake: grep -niE 'zeroday|disclosure polic|coordinated vulnerability|bounty|bug bounty|severity ladder|reward scale' $r-shokunin/PROVINCE.md $r-shokunin/SKILL.md
grep -rliE 'coordinated vulnerability disclosure|vendor coordination|bug bounty program|disclosure window|advisory deadline' $r-shokunin/corpus/knowledge/
grep -rl -i 'zerodayinitiative|zero day initiative' /home/vgpnk/Projects/shokunin/*-shokunin/ | grep -v kasegi-shokunin   -> 0
curl -sS -o zdi_about.html  -w 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://www.zerodayinitiative.com/about/
curl -sS -o zdi_faq.html    … https://www.zerodayinitiative.com/about/faq/
curl -sS -o zdi_benefits.html … https://www.zerodayinitiative.com/about/benefits/
curl -sS -o zdi_faulty.html … https://www.zerodayinitiative.com/blog/2022/8/11/new-disclosure-timelines-for-bugs-from-faulty-patches
curl -sS -o zdi_upcoming.html … https://www.zerodayinitiative.com/advisories/upcoming/
curl -sS -o zdi_published.html … https://www.zerodayinitiative.com/advisories/published/
```

Scratch tree `/fast/scratch/hyaku/kasegi-r71/ScoutF49/` held `S106.txt`, `manifest-r71.json`, `note.txt` and the eight fetched HTML files; it is removed on yield. Nothing under it is cited as evidence in this report except the three byte counts and two status codes that the fetch commands printed.
