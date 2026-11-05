# ConnectorTable — round-71 attempt 2: cross-source coordination-window table + ConnectorScope audit

Seat: ConnectorTable (connector, leaf). Lane tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`.
Committed bytes only (`git show`, captures, knowledge entries, SOURCES.md, README.md). No lane file
mutated except this report; scratch `/fast/scratch/hyaku/kasegi-r71/ConnectorTable/` created and removed.

Assignment: rebuild the cross-source comparison table making F49's distinctness checkable, mark
genuine disagreements and ZDI-only cells, name any F49 duplicate of an existing frontier row's ground,
and audit attempt-1's `w1/ConnectorScope.md` cell-by-cell against my own build.

## 0. Evidence base (committed bytes)

- `corpus/knowledge/coordinated-disclosure-timelines.md` (F02: S003/S004/S005 + rule)
- `corpus/knowledge/zdi-disclosure-policy.md` (F02 coordinator case: S075)
- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (F12: S041/S042)
- `corpus/knowledge/cert-guide-cvd-phases-and-validation.md` (F43: S095)
- `corpus/knowledge/cisa-cvd-program-stages.md` (F06: S023)
- `corpus/knowledge/multiparty-vulnerability-coordination.md` (F06: S018)
- `corpus/knowledge/first-psirt-services-framework.md` (F44: S098)
- `corpus/knowledge/first-psirt-maturity-document.md` (F45: S100/S101)
- `corpus/knowledge/github-advisory-database-curation-semantics.md` (F48: S105)
- `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` (F49: S106)
- `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` (F02 extension: S016)
- Captures: `round-24/S003.txt` `S004.txt` `S005.txt`; `round-47/S075.txt`;
  `round-30/S041.txt`; `round-28/S042.txt`; `round-62/S095.txt`; `round-40/S023.txt`;
  `round-65/S098.txt`; `round-67/S100.txt`/`S101.txt`; `round-70/S105.txt`; `round-71/S106.txt`.
  (`round-24` holds S003–S005; `round-28`/`round-30` hold the S041/S042 captures the F12 entry cites.)

## 1. Cross-source coordination-window table

Columns: party | window | shortening/escalation rule | who publishes | vendor-refusal consequence | entry + anchor.

| Party (source, frontier) | Window | Shortening / escalation rule | Who publishes | On vendor refusal / silence | Entry + anchor |
|---|---|---|---|---|---|
| **CISA supplier guide** (S003, F02) | No fixed interval; "a fixed period, a minimum or maximum, or a negotiated default starting point" (`round-24/S003.txt:202-203`) | Collaborative embargo adjustment ("Suppliers and researchers should work collaboratively to adjust embargo periods", `:204-205`); third-party coordinators named as collaborators (`:210-212`) | Supplier + researcher + coordinators, per negotiated VDP (`:209-212`) | Guidance warns long embargoes raise leak risk (`:207-208`); not an enforcement publisher | `coordinated-disclosure-timelines.md` Evidence bullets `:20-21`; `README.md:203` F02 |
| **CISA CVD program** (S023, F06) | Floor, not deadline: "may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made, regardless of the availability of a patch or update" (`round-40/S023.txt:151`) | Factor-based: disclosure status, potential impact, vendor responsiveness, mitigation availability (`:148-152`) | CISA Advisory + CVE record + CSAF (`:141-145`) | Vendor unresponsive or no reasonable remediation timeframe → earliest-disclosure floor (`:151`) | `cisa-cvd-program-stages.md` Claim 6 (`:74-76`, falsifiable rule `:93`) |
| **CISA BOD 20-01** (S021, F03-adjacent) | Agency-set targets only: ack/assessment/resolution targets, "not vulnerability resolution deadlines" (`cisa-bod-20-01-vdp-minimums.md` Claim ~`S021` L305 area); "45 to 90 days" is community expectation CISA quotes, "anything more than 90 days begins to veer away from what is reasonable" | Delay "may not be unreasonable" | Agency VDP + CyberScope metrics (10 metrics at 270d, `S021.txt:161-168`) | Reporter-facing clock exists only as agency target; no mandatory fix deadline | `cisa-bod-20-01-vdp-minimums.md:90,122,144` |
| **CERT/CC policy** (S004, F02) | **45 days** "after the initial report, regardless of the existence or availability of patches or workarounds" (`round-24/S004.txt:24-26`) | Earlier disclosure for exploitation/serious threats; later for standards/core-OS changes (`:26-29`, `:67-69`) | CERT/CC publishes Vulnerability Notes with reporter credit (`:29-30`, `:45`) | Publishes regardless of patch; "We may not publish every vulnerability" (`:70`); vendor disagreements posted alongside, not withheld (`:75-79`) | `coordinated-disclosure-timelines.md:22-23`; `README.md:203` |
| **Google Project Zero** (S005, F02) | **90 days**; early fix → public **30 days after fix** (90+30 rule, `round-24/S005.txt:18`); active exploitation → **7-day** deadline (`:44` exception list) | 14-day grace extension only on developer commitment to ship within it, max day-120 disclosure (`:21-23`); 1-week notice of report+deadline (`:19`); exceptions by Google (`:41-45`) | P0 derestricts issue-tracker entry (`:25-26`); `Deadline-Exceeded`/`Deadline-Grace` labels (`:27`) | Automatic derestriction at deadline; 95 historical unpatched disclosures (`:27`,`:29-30`) | `coordinated-disclosure-timelines.md:24-25`; `README.md:203` |
| **Anthropic CVD policy** (S016, F02 extension) | Default **90 days** or patch release, whichever first; compressed **7-day** target under active exploitation; post-patch **45-day** details buffer (`anthropic-cvd-provenance-and-pacing.md` Claims 1-3, L10-L16) | Maintainer-severity deferral except credible active exploitation; non-response 30 days → external coordinator, clock keeps running (L14); buffer can shorten/extend (L16) | Anthropic publishes report under its default; full technical details after 45-day buffer | "aim to escalate the finding to an external vulnerability coordinator" after 30-day non-response (L14) | `anthropic-cvd-provenance-and-pacing.md:24,40-54,94` |
| **JPCERT/CC + IPA** (S041, S042, F12/F11/F38) | 起算日 = first attempted contact per Ⅳ.4.2) (`round-30/S041.txt:340`); publication date **45日後を目安** from 起算日 — a guide, not a deadline (`round-30/S041.txt:648-653`); web-app path has no clock (`round-28/S042.txt:162-182`) | 4 adjustment factors (`S041.txt:649-653`); publication date changeable on developer request (`S041.txt:658-660`); call-off grounds (`S041.txt:662-671` per entry); 1-year non-disclosure-request withdrawal (`S041.txt:305-306`, `:430-431`) | IPA & JPCERT/CC jointly on JVN (`round-28/S042.txt:158-159`; `S041.txt` 図3/図4) | Unreachable developer listed on 連絡不能開発者一覧 (`S042.txt:142`); small-impact contact can close handling (`S042.txt:143`) — conditional, not automatic | `japanese-domestic-disclosure-workflow.md:19-27,43`; `README.md:213` F12 |
| **FIRST PSIRT Services Framework** (S098, F44) | No fixed interval; "negotiated disclosure plan" and "timelines … negotiated as soon as possible" (`round-65/S098.txt` ~L1203 area; entry C10/C11) | Finder-set embargo parameters honored (`S098.txt:478`); per-finder profiles inform pacing (`:893`) | Vendor PSIRT publishes advisories/release notes/CVE text with finder credit (`:599`,`:615`,`:623`) | "disclose the flaw before any agreed upon date" is the risk to manage (`S100.txt:305`); no stated consequence rule | `first-psirt-services-framework.md` C10/C11; `README.md` F44 |
| **FIRST PSIRT Maturity Document** (S100/S101, F45) | **No number**: the only interval is an unfilled template placeholder "triaged within [#] days" (`round-67/S100.txt:393`; `first-psirt-maturity-document.md` C16) | Multi-PSIRT "mutually agreeable time ('embargo period')" for simultaneous disclosure (`S100.txt:347`; `S101.txt:567`) | PSIRT publishes; template-level only | None stated — document is maturity guidance, not a policy | `first-psirt-maturity-document.md:30,52` |
| **FIRST multi-party guidelines** (S018, F06) | No number: "communicate and negotiate expectations and timelines" | Negotiated per party; lead-coordinator selection when multiple (`multiparty-vulnerability-coordination.md:27,30`) | Parties publish per negotiated plan | "negotiated communication rather than a universal automatic disclosure trigger" (`:46`) | `multiparty-vulnerability-coordination.md:11-13,27,46` |
| **CERT Guide phases** (S095, F43) | Conceptual 6-phase lifecycle (Submission→Deployment, `round-62/S095.txt:56-74`); no numerical window | Role-gated: Analyst/Vendor/Coordinator validate & prioritize (`:129-146`) | Vendor/Coordinator publish advisory in Awareness phase (`:69`) | Deferred to operational policies; a dash is not a prohibition (`cert-guide-cvd-phases-and-validation.md:36`) | `cert-guide-cvd-phases-and-validation.md`; `README.md:1031` F43 |
| **GitHub Advisory Database** (S105, F48) | No coordination window at all — curation semantics only: admission classes, feeds, GHSA id, CVSS/EPSS provenance (`round-70/S105.txt:568-643`) | Community contributions reviewed by GitHub Security Lab (`:642`) | GitHub publishes global advisories; Dependabot alerts only for reviewed class (`:599`,`:602`) | N/A — no vendor-coordination surface on the page | `github-advisory-database-curation-semantics.md:15-30` |
| **ZDI disclosure policy page** (S075, F02 case) | **120 days** ("four months") conditional on vendor response within the contact ladder (`round-47/S075.txt:24`); faulty-patch tiers **30/60/90** by severity+patch-efficacy (`:25`) | 5bd ack → +5bd second attempt → intermediary → "fifteen business days after the initial contact" → public advisory (`:23`); extensions at ZDI sole discretion (`:24`) | ZDI publishes on its website; only listed advisories are official (`:27`) | Refusal → "publish a limited advisory including mitigation" at deadline (`:24`); never "kept quiet" (`:26`) | `zdi-disclosure-policy.md:11-24`; `README.md:699` |
| **ZDI About page** (S106, F49) | **120-day standard coordination window** (`round-71/S106.txt:70`); shortened **30/60/90** "for flaws that result from incomplete or problematic security patches" (`:70`) | "may escalate to a limited public advisory" after **15 business days** of vendor non-response (`:70`) | ZDI publishes full advisory on patch (`:51`,`:71` joint advisory), limited advisory withholding exploit-enabling detail (`:52`), or full-or-limited on refusal (`:72`) | "may publish a full or limited advisory" on refusal/unresponsiveness (`:72`); no-backlog guarantee (`:62`) | `zdi-disclosure-process-and-vendor-coordination.md:84-111`; `README.md:1114` F49 |

## 2. Genuine disagreements (same dimension, different stated rule — not merely different scope)

Marked **[DISAGREE]** where two held sources state incompatible rules for the same quantity.

1. **120-day window conditionality — S075 vs S106 (same party, two pages).**
   S075: "If a vendor response is received within the timeframe outlined above, TrendAI™ ZDI will
   allow the vendor four months (120 days)…" (`S075.txt:24`) — the 120 days is gated on a timely
   vendor *response*. S106: "Vendors are given a standard coordination window of 120 days under
   TrendAI™ ZDI's disclosure policy." (`S106.txt:70`) — stated unconditionally as *the* standard
   window. These are not different scopes; they are two ZDI statements of the same window with
   different stated preconditions. The F49 entry itself flags this (its `ground:` line and the
   README erratum at `README.md:1129-1130`: "S075's 120 days is conditional on a vendor response
   while S106 states it as the standard window"). **Marked disagreement, intra-party.**

2. **15-business-day escalation product — S075 vs S106.**
   S075: "may issue a **public advisory disclosing its findings** fifteen business days after the
   initial contact" (`S075.txt:23`) — full findings. S106: "may escalate to a **limited** public
   advisory to protect users" (`S106.txt:70`), and "limited advisory … withholding information that
   could enable exploitation" (`S106.txt:52`). Same trigger, different disclosure content. README
   erratum names it (`README.md:1128-1129`). **Marked disagreement, intra-party.**

3. **15-business-day clock start — S075 vs S106.**
   S075's 15 business days runs after a 5bd-ack + 5bd-second-attempt + intermediary ladder
   ("If TrendAI™ ZDI exhausts all reasonable means in order to contact a vendor, then … fifteen
   business days after the initial contact", `S075.txt:23`). S106: "fails to respond within 15
   business days of first contact" (`S106.txt:70`) — no acknowledgement ladder named. Different
   stated trigger composition for the same number. **Marked disagreement, intra-party.** (The
   ZDI FAQ reportedly carries a 5/10-business-day ladder — ScoutF49 Lead C — but that page is not
   a held source; not counted here.)

4. **Shortened-window branch conditions — S075 vs S106.**
   S075 enumerates three distinct branches with stated conditions: 30d = critical-rated + active
   exploitation imminent; 60d = critical/high + partial patch protection + no imminent
   exploitation; 90d = all other faulty-patch reports (`S075.txt:25`). S106 compresses all three
   to "30, 60, or 90 days, **depending on multiple factors**" (`S106.txt:70`) with the only stated
   gate being "flaws that result from incomplete or problematic security patches". S106 also
   attaches the shortening to a *different stated class* ("incomplete or problematic security
   patches", `:70`) vs S075's "incomplete or otherwise faulty security patch" (`S075.txt:25`) —
   near-synonymous but not identical wording, and S106 names no severity/exploitation conditions.
   **Marked disagreement in stated conditions (information loss on the About page), intra-party.**

5. **CERT/CC 45-day vs JPCERT/CC 45-day — same number, different trigger AND different modality.**
   CERT/CC: 45 days "after the initial report" as a stated policy deadline (`S004.txt:24-26`).
   JPCERT/CC: 45 days is a 目安 (guide/target) measured from 起算日 = *first attempted contact*,
   adjustable on four stated factors and changeable on developer request
   (`S041.txt:340,648-660`). The lane's own F12 row already records this as a trigger difference
   (`README.md:213`), and the JPCERT entry states the modality difference ("目安 … not a deadline",
   `japanese-domestic-disclosure-workflow.md:25`). **Marked: same interval, genuinely different
   rule — not a contradiction of fact, but a reader must not merge them.** Flagged because a
   naive table would show "45 days" twice and imply agreement.

6. **CISA 45-day floor vs CERT/CC 45-day deadline vs ZDI 120-day — escalation asymmetry on vendor
   silence.** CISA: "may disclose … as early as 45 days after the initial attempt to contact the
   vendor" when unresponsive (`S023.txt:151`). CERT/CC: 45 days from report regardless of patch
   (`S004.txt:24`). ZDI/S075: 15 business days → *possible* public advisory only after exhausting
   contact means (`S075.txt:23`), then a further 120-day window if the vendor responds. These are
   three different stated consequences of vendor silence; they disagree as *rules* only if a reader
   generalizes one coordinator's number — which each entry forbids. **Not marked as factual
   disagreement** (different parties may legitimately differ), but noted: no two held sources state
   the same window for the same trigger with different outcomes, except the intra-ZDI pairs in
   items 1–4.

## 3. ZDI-only cells (F49/S106 is the sole holder of the statement)

Cells where **no other held source** states the proposition — these are F49's defensible novelty:

| Statement | Sole holder | Other-party nearest (does NOT state it) |
|---|---|---|
| Acquisition flow: validate → confirm severity → **formal monetary offer** → payment → vendor coordination (`S106.txt:60`) | S106/F49 only | S075 is the policy page; P0/S005 is researcher-side deadline; no entry states a buy-side payment step (`grep -rniE 'monetary offer\|payment is processed' corpus/knowledge/` → only the F49 entry) |
| "imposes no limit on the number of reports researchers can submit" (`S106.txt:60`) | S106/F49 only | — |
| Credit/anonymity/pseudonym choice in the advisory (`S106.txt:61`) | S106/F49 only | CERT/CC states reporter credit is default-on (`S004.txt:29-30`); P0/ZDI policy page state no anonymity option |
| No-backlog guarantee: "will not disappear into a backlog or remain undisclosed due to vendor inaction" (`S106.txt:62`) | S106/F49 only | S075's "never kept quiet" (`S075.txt:26`) is ZDI-policy-page ground held under F02 — **see §4 overlap note**: this is the same party's same guarantee restated, so it is ZDI-held twice, not twice-held ground |
| Vendor dossier contents: PoC, reproducible steps, severity assessment, exploitability insights (`S106.txt:69`) | S106/F49 only | FIRST S098 asks finders for quality reports but states no dossier hand-off list |
| Vendor-agnostic acquisition programme self-description (`S106.txt:28`,`:31`) | S106/F49 only | — |
| Joint advisory with credit + patch link on vendor patch (`S106.txt:71`) | S106/F49 only | S075 states advisories publish on ZDI's website (`:27`) but not the joint-advisory/credit form |
| "120-day standard coordination window" stated *without* a stated clock-start event | S106/F49 | S075 also leaves the start event unstated (`zdi-disclosure-policy.md` Scope) — same gap, second attestation |

**Clock-number cells are NOT ZDI-only**: 120 days, 30/60/90 days, and 15 business days are all
already held via S075/F02 (`zdi-disclosure-policy.md:17-24`). F49's table row above marks them;
they are second-party-page restatements with the §2 divergences, not new ground.

## 4. F49 duplicate-of-existing-ground check

Per the assignment: name any place F49 duplicates an existing frontier row's ground, with row id
and overlapping sentence; then SCOPE CLEAR or the overlap list.

**Overlap list (ground already held before F49):**

1. **Row F02 / entry `zdi-disclosure-policy.md` (S075).**
   - F49 ground sentence (README `:1114`): "the 120-day standard coordination window with its
     30/60/90-day shortening … escalation to a limited public advisory after 15 business days of
     vendor silence".
   - Overlapping held sentences:
     - "four months (120 days) to address the vulnerability" (`S075.txt:24`, held at
       `zdi-disclosure-policy.md:17`)
     - 30/60/90-day tiered timeline (`S075.txt:25`, held at `zdi-disclosure-policy.md:20-22`)
     - "fifteen business days after the initial contact" → public advisory (`S075.txt:23`, held
       at `zdi-disclosure-policy.md:16`)
     - "publish a limited advisory including mitigation" (`S075.txt:24`, held at
       `zdi-disclosure-policy.md:18`)
     - "In no cases will an acquired vulnerability be 'kept quiet'" (`S075.txt:26`, held at
       `zdi-disclosure-policy.md:24,42`) ≈ F49's "no-backlog guarantee" (`S106.txt:62`)
   - **The round-47 verdict already ruled on this shape**: `README.md:702` — "No F30 row is
     admitted: the proposed ZDI timeline frontier duplicates F02's existing
     coordinator/trigger/interval discipline." F49's clock numbers are the same discipline on a
     second ZDI page.

2. **Row F02 / entry `coordinated-disclosure-timelines.md` (S003/S004/S005).** F49's *comparison
   value* (a fourth coordinator column: broker/acquisition-side vs researcher-side P0 vs
   coordinator CERT/CC vs supplier-guidance CISA) instantiates F02's rule "name the policy or
   coordinator … do not describe one interval as the universal researcher deadline"
   (`coordinated-disclosure-timelines.md:7-8`). The row's *method* is held; the S106 column is
   new data under it.

3. **Row F12 (`japanese-domestic-disclosure-workflow.md`, S041/S042).** Not a duplicate — the
   45-day 目安 there is a different party's different trigger; F49 adds the ZDI column to the
   same comparison F12's `next` cell anticipates ("the Japanese column when comparing
   coordinator timelines against F02", `README.md:213`).

**Non-duplicate (genuinely new ground F49 adds):**
- The acquisition-side monetary flow (`S106.txt:60`) — validate → offer → payment → coordination.
- The no-limit submission statement, dossier contents, credit/anonymity/pseudonym, joint-advisory
  form, sanitized-intelligence sharing (`S106.txt:52`), and the About-page-specific wordings with
  their three measured divergences from S075 (§2 items 1–4).
- These are attested nowhere else in `corpus/knowledge/` (measured: `grep -rniE
  'monetary offer|formal monetary|vendor-agnostic|pseudonym|no limit on the number of reports'
  corpus/knowledge/` → only `zdi-disclosure-process-and-vendor-coordination.md`).

**Verdict: NOT SCOPE CLEAR as frozen** — the frozen C2 `declared` sentence lists the 120-day
window, the shortened window, the 15-business-day escalation and the full-vs-limited advisory
choice as F49 ground; all four are already held under F02/S075 (and the limited-advisory *form*
under S075's "limited advisory including mitigation"). The lane's own erratum
(`README.md:1122-1133`, appended after the w1 scout measured this) already narrowed F49's ground
to the acquisition-side flow plus the wording divergences, and states "A reader must not take the
clock numbers from this row as new ground; they are ZDI's numbers, first attested at S075."
**Overlap list stands as above; the surviving F49 ground is the acquisition flow + divergences +
About-page-only statements in §3.** Whether that residual ground justifies the frontier row is
the L1's adjudication, not this seat's; my table makes the overlap mechanically checkable.

## 5. Audit of attempt-1 `w1/ConnectorScope.md` §2 table

I rebuilt the table from committed bytes (§1 above). Cell-by-cell verdict on the attempt-1 table:

| Attempt-1 row | Verdict | Correction |
|---|---|---|
| **CISA (S003)** — "Flexible / negotiated default starting point; 2–3 business days acknowledgment; no universal deadline" | **Anchor wrong, substance right.** The "2–3 business days" (`S003.txt:232`) is the recommended *acknowledgement* mechanism ("Engage with the security researcher within a specified time frame, such as two to three business days"), not a coordination window; attempt-1 filed it under "Coordination Window & Clock Trigger". The window column should read: no fixed interval, "fixed period, minimum/maximum, or negotiated default starting point" (`S003.txt:202-203`). | Move 2–3bd to a separate acknowledgement cell or drop it; the window cell is correct only via the negotiated-starting-point quote. |
| **CERT/CC (S004)** — 45 days, earlier/later exceptions, Vulnerability Notes, publishes regardless | **Correct.** Verified `S004.txt:24-26,45,64-79`. Minor: "published regardless of patch availability" is right; the "We may not publish every vulnerability" (`:70`) discretion is worth one clause. | None material. |
| **Google P0 (S005)** — 90d, 30d post-fix, 7d active exploitation, 14-day grace max day-120, derestriction, Deadline-Exceeded | **Correct.** Verified `S005.txt:18-30,41-45`. | None. |
| **Japan IPA/JPCERT (S041/S042)** — 起算日 + 45日目安, JVN publication, unreachable-developer listing, conditional/no | **Substance right; two anchors unverifiable as cited.** Attempt-1 cites `S041.txt:340` for 起算日 — **wrong file**: that line is in `round-30/S041.txt`, not the round-28 capture; and `S042.txt:145` 起算日連絡 is `round-28/S042.txt:144-145` (verified). `S041.txt:648` 45-day 目安 verified at `round-30/S041.txt:648`. The "1-year withdrawal" cites `S041.txt:305-306,430-431` — verified at round-30 (`:305`,`:430`). | All S041 anchors must name `round-30/S041.txt` (the F12 entry's capture), not bare `S041.txt`; S042 anchors name `round-28/S042.txt`. Content otherwise correct. |
| **CERT Guide phases (S095)** — 6 phases, no fixed days, role matrix, vendor/coordinator publish | **Correct.** Verified `round-62/S095.txt:56-74,129-146`. | None. |
| **TrendAI ZDI (S106, S075)** — 120d, 30/60/90d, 15bd escalation, full-vs-limited advisory, publishes full/limited on refusal | **Conflates two sources into one row without marking the divergence.** The row merges S075's conditional 120 days and public-advisory escalation with S106's unconditional "standard window" and limited-advisory escalation. As written it implies one consistent ZDI rule; §2 items 1–4 show four real divergences. Also "guaranteed not to remain undisclosed" cites `S106.txt:62` (no-backlog guarantee) — accurate for S106 — but the same guarantee exists at `S075.txt:26`, which the row does not note. | Split into two rows (S075 policy page / S106 About page) or add a divergence column; the "vendor refusal" cell must distinguish S075's limited-advisory-with-mitigation at deadline vs S106's permissive "may publish a full or limited advisory" (`S106.txt:72`). |
| **Missing rows entirely** | **Coverage gap.** The assignment's party list includes CISA (S003/S004/S005 — note S004/S005 are CERT/CC and P0, not CISA; attempt-1 mislabeled the grouping but covered them), ISO 29147/30111 + JPCERT (covered), FIRST PSIRT (S098/S100/S101 — **absent**), CERT/CC phases S095 (covered), GitHub advisory curation S105 (**absent**), ZDI S106 (covered). FIRST PSIRT and GitHub curation hold **no coordination window** — verified: S098 states "negotiated disclosure plan"/"timelines negotiated" with no number (`first-psirt-services-framework.md` C10-C11); S105 is curation semantics with zero window vocabulary (`github-advisory-database-curation-semantics.md`; `S105.txt` grep for day/window/deadline → none). Their absence is defensible on "window" grounds but the assignment asked for every coordination-window statement the lane holds — a "no window stated" row is itself a checkable cell. | Add explicit "no numerical window held" rows for S098/S100/S101 (FIRST) and S105 (GitHub curation), plus optionally S018 (FIRST multiparty: negotiated timelines, no number) and S023 (CISA CVD program: the 45-day earliest-disclosure floor — a window statement attempt-1 **omitted entirely**). S023's 45-day floor is the most consequential omission: it is a held coordinator-side disclosure interval not in attempt-1's table. |
| **§3.1 overlap list** | **Correct and now superseded-but-consistent.** The four F02/S075 overlaps match my §4. The round-47 "No F30" citation (`README.md:702`) verified. | The table should also cite the README erratum (`README.md:1122-1133`) which already narrowed F49 post-scout; attempt-1's "SCOPE CLEAR iff acquisition-flow-only" conclusion agrees with the erratum's narrowing — consistent, not contradictory. |
| **§4 connector move (live figure derivation)** | Out of my audit scope (proposal, not a table cell); noted: it proposes binding live counters into `figure-audit-ledger.json` — interacts with C1's census work; flagged for L1, not judged here. | — |

**Unanchored/wrong cells summary for ConnectorScope.md:**
1. S003 "2–3 business days" misfiled under window (it's acknowledgement guidance).
2. All `S041.txt:` anchors ambiguous/wrong-capture — must be `round-30/S041.txt`.
3. ZDI row merges S075+S106 without marking four genuine divergences (§2 items 1–4).
4. S023 (CISA CVD 45-day floor), S018 (FIRST multiparty negotiated timelines), S098/S100/S101
   (FIRST PSIRT — no window), S105 (GitHub curation — no window) all absent; the "every
   coordination-window statement the lane holds" requirement is unmet.
5. Header grouping "CISA (S003/S004/S005)" in my assignment is itself loose — S004 is CERT/CC,
   S005 is Project Zero; attempt-1's table correctly separated them by party despite the loose
   grouping. Not an error in the artifact.

## 6. Second-order notes for the L1

- The three intra-ZDI divergences (§2.1–2.3) are the strongest verifiable content F49 adds beyond
  S075: they are *measured wording differences between two first-party ZDI pages*, checkable by
  `grep`/`source-recheck` on both captures. This is the narrowest defensible F49 ground and
  matches the README erratum's narrowing.
- S106's "120 days" appears exactly once (`S106.txt:70`) with no clock-start event — same gap as
  S075. Any package converting either into a date without a stated start fails both entries'
  falsifiable rules.
- No tool installs this round; no scratch residue (`/fast/scratch/hyaku/kasegi-r71/ConnectorTable/`
  created empty for contract compliance, removed on yield).
