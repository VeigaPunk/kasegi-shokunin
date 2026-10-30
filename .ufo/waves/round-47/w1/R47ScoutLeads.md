# R47ScoutLeads — future-round screen only

Axes: depth:verifiability (first-party fetched text and exact location); coverage (new ground rather than another F30 clock). No source rows, knowledge entries, frontier admissions, or production captures proposed for this round.

## Three screened leads

### 1. ZDI — How It Works (strongest broker-adjacent lead)
- URL: https://www.zerodayinitiative.com/about/benefits/
- Observed fetch: `read` of that URL returned `Content-Type: text/html`, `Method: native`, title “How It Works - TrendAI™ Zero Day Initiative™ (ZDI)”. Located via the registration page's raw navigation link, not a guessed route.
- Exact quote (10 words): **“Ownership remains with you until an offer is accepted.”** Location: **Program benefits → Researcher-first experience built on impact → Control over your work**, first sentence.
- Adds: pre-acquisition ownership boundary and the discovery → submission → validation → reward → notification sequence. The Submission subsection expressly places submission through the secure portal and assigns a case ID; the Validation subsection separates verification/valuation from offer acceptance.
- Why only a lead: F30's held S075 is the broker-to-vendor disclosure policy, not the researcher-to-broker acquisition workflow. The substantive held text at `corpus/source-snapshots/round-47/S075.txt:20-27` concerns vendor notification, escalation, patch windows and advisories. Its “How It Works” occurrences at lines 6, 13 and 51 are navigation, not this page's body. Future mining must pin and qualify this page's own statements; do not turn its marketing claims about validation into measured effectiveness.
- Confidence: high on observed wording and separate URL; medium-high on new conceptual ground, subject to future admission review.

### 2. HackerOne — Disclosure & Coordinated Vulnerability Disclosure (strongest platform contrast)
- URL: https://docs.hackerone.com/en/articles/8517457-disclosure-coordinated-vulnerability-disclosure
- Observed fetch: `read` returned the same canonical URL, `Content-Type: text/html`, `Method: native`, displayed date **June 3, 2026**.
- Exact quote (11 words): **“Explicit approval must be received regardless of report status.”** Location: **Part 2: Program Disclosure Settings**, table row **Disclosure Requiring Mutual Agreement**, Details cell, final sentence.
- Adds: separates declared CVD stance from platform disclosure settings. In the neighboring Disclosure row, the no-response public-disclosure default is 30 days for Resolved reports only; other closed states require mutual agreement. This provides a concrete contrast to F30's broker-to-vendor clock, not a universal disclosure deadline.
- Why only a lead: existing HackerOne holdings include safe harbor S006 (`corpus/SOURCES.md:12`) and standard program policy S043 (`:49`), neither is this settings guide. A later entry would need to preserve status/setting conditions and distinguish public disclosure from disclosure confined to private-program participants. It is not evidence for this round's S075/F30 admission.
- Confidence: high on fetched wording and setting distinction; medium-high on conceptual novelty.

### 3. ZDI — Sign Up (narrow researcher-onboarding lead)
- URL: https://www.zerodayinitiative.com/portal/register/
- Observed fetch: `read` returned `Content-Type: text/html`, `Method: native`, title “Sign Up - TrendAI™ Zero Day Initiative™ (ZDI)”. Public text only; no form submission, account creation, login, or vulnerability submission performed.
- Exact quote (16 words): **“You will have 7 days to activate your account before the link expires.”** Location: **Sign Up → Join the 19,000-strong global community advancing vulnerability research**, second prose paragraph, second sentence (confirmation-email paragraph).
- Adds: account-activation expiry and onboarding prerequisites, a different trigger and recipient from a vendor's acknowledgement or remediation deadline. The page also explicitly says JavaScript is needed to send the registration form; that is a published prerequisite, not a tested portal behavior.
- Why only a lead: no onboarding body is present in S075; its Sign Up occurrences at `S075.txt:10,17` are navigation. This is likely supporting ground for a later researcher-submission entry, not sufficient by itself to justify a new frontier. Do not inflate a form page into another disclosure-policy row.
- Confidence: high on quote; medium on eventual independent-entry value.

## Inventory discrimination and do-nothing control

Observed literal inventory check (`functions.grep`, case-insensitive):

```
pattern: zerodayinitiative.com/(portal/register|about/benefits)|8517457-disclosure-coordinated-vulnerability-disclosure
paths: corpus/SOURCES.md; corpus/knowledge; corpus/README.md
output: No matches found
```

A second conceptual screen used `Ownership remains|confirmation link|CVD Compliance Levels|Disclosure Requiring Mutual Agreement|valuation|payout offer|7 days to activate` on the same paths. Hits were unrelated evaluation/valuation substrings in existing entries; no displayed hit contained the candidate-specific ownership, activation or disclosure-setting phrases. This is literal evidence, not semantic proof of exhaustive novelty. No exported code contract is involved, so LSP definition/caller tracing is not applicable.

**Do-nothing control:** retain only the held S075 page and existing registry. It contains navigation labels but cannot supply any of the three located body quotes above. Fetching each candidate produces the specific new ownership / disclosure-setting / activation distinction; merely recounting links or adding candidate names would add no verified ground. No C1/C2 counter was run or claimed improved by this reconnaissance.

Relevant scope boundary: `corpus/README.md:211` defines F10 as vendor-side standing disclosure policies (S036–S040), whereas these leads concern broker acquisition, platform-controlled publication, and broker onboarding. They are deliberately outside this round's frozen F30 admission.

## Limits and handling

- Reader fetches establish inspectable public text, not recorded HTTP status, byte count, digest, snapshot identity, contractual enforceability, or operational portal behavior. No publication date was visible on the two ZDI reader pages. Re-fetch and pin in a future authorized round before citing them as admitted sources.
- Search-engine summaries were discovery only, not quote evidence. One constrained How It Works search returned unrelated results after relaxing the domain restriction; those were discarded. The actual process URL was recovered from ZDI's own raw navigation.
- No claim that F30 or C1 is closed; no battery, gate, selftest, or build run. The disclosed pre-freeze survivors remain unresolved by this seat.
- Only this findings file was written. No scratch directory or local downloaded capture was created, so no scratch artifacts remain to remove. No installation, git/jj mutation, delegation, or background job.

Self-evaluation: accuracy 4/5 (direct first-party reads; no byte-pinned receipts); completeness 4/5 (three leads, third intentionally supporting rather than frontier-ready); clarity 4/5 (explicit per-lead boundaries); actionability 4/5 (URLs/headings ready for future capture, admission still required); conciseness 4/5 (evidence and caveats retained). Overall 4.0/5. Highest-value future improvement: authorized byte-pinned captures, not expansion of round-47 scope. User-agreement check: this is reconnaissance only, not an admission or counter pass.
