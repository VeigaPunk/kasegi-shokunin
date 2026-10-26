# Anthropic's coordinated-disclosure policy for Claude-discovered vulnerabilities — AI-origin labelling, maintainer-sustainable pacing, and a discoverer-side clock with a post-patch details buffer

source: S016 — https://www.anthropic.com/coordinated-vulnerability-disclosure — capture corpus/source-snapshots/round-40/S016.txt (32 lines, 4,481 bytes; sha256 91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b): title L5, "Last updated Mar 6, 2026" L6, Purpose Statement L7, Scope L8, General L9, Target Vulnerability Disclosure Timelines L10-L15, Patch Details L16, Vulnerability Disclosure Reporting and Coordination L17; L1-L4 and L18-L32 are site chrome
verified-at: 2026-10-26 (re-opened by me this day: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` on the URL returned HTTP 200, text/html; charset=utf-8, 164,307 raw bytes, raw sha256 d7dbc1766f4b7cc3d600b42d87f1f140c44679d3495eb902434861d8a1110ded at 2026-10-26T21:16:37Z; converting that body with the lane's `corpus/instruments/capture-source.py html_to_text()` gave 32 lines / 4,550 bytes / sha256 7070a3635a04e209340a70382b682825144c6c431a03a9e2a78594fb57ea13b8 — the footer mission sentence at L28 came back in a different wording that day, and body lines L5-L17 were byte-identical to the landed capture, which is what every quote below cites)
ground: F02 — extends the coordinated-disclosure timeline item (S003/CISA's 45-day, S004/CERT-CC's 45-day, S005/Project Zero's 90+30 with a 14-day grace) with a discoverer-side policy that adds a distinct post-patch *details* buffer, an AI-origin label on the report itself, and a submission-pacing rule that no coordinator row states
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S016   # prints S016:sha256 OK then one S016:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved — a pinned-capture comparison under whitespace collapse, not a fresh network check

## Attribution

This is Anthropic's own operating policy for vulnerabilities Anthropic's tooling discovers, published on Anthropic's site, and the page says so twice: the purpose ties the document to Anthropic's own tooling — "Anthropic is building AI tools that find software vulnerabilities faster and cheaper" (L7) — and the scope clause bounds who the rules cover.

> "These operating principles apply to vulnerabilities Anthropic discovers in open-source software" — S016.txt:L8

> "It does not generally cover reports to Anthropic by external researchers, which are governed by Anthropic’s Responsible Disclosure Policy." — S016.txt:L8

Two consequences a reader must carry: this capture says nothing about how a researcher should report *to* Anthropic (that is a different, uncaptured policy), and nothing it says is a rule for other AI-assisted finders. It is a first-party statement of one discoverer's outbound practice, "Last updated Mar 6, 2026" (L6) — the revision every quote below belongs to.

## Claim 1 — the default clock is 90 days or patch release, whichever comes first

> "Anthropic aims to follow the industry standard 90-day disclosure deadline" — S016.txt:L9

> "we aim to share details publicly with defenders after 90 days, or after a patch is released, whichever comes first" — S016.txt:L10

The second quote is the operative default and it is a disjunction with a "first" rule: a vendor that ships a patch on day 10 shortens the public-details date to day 10, not day 90. That is a different branch from the Project Zero model F02 already holds, where the 90-day deadline is followed by a separate 30-day patch-adoption window when a fix lands early (`corpus/knowledge/coordinated-disclosure-timelines.md:24`, S005). Same 90-day default; different meaning for an early patch.

## Claim 2 — the departures are enumerated, each with a named trigger

> "making progress toward a fix as the 90-day deadline approaches, we may grant a 14-day extension on request" — S016.txt:L11

> "For actively exploited critical vulnerabilities, we target a 7-day timeline for a patch or mitigation." — S016.txt:L12

> "If the maintainer is actively working on a fix and requests more time, we may grant a further 7-day extension." — S016.txt:L12

> "When a finding reflects an ecosystem-wide pattern affecting many projects at once, we aim to notify affected parties" — S016.txt:L13

> "Where we and a maintainer disagree on the severity of a finding, we would generally defer to the maintainer's assessment." — S016.txt:L14

> "the compressed 7-day target timeline would apply regardless of how the maintainer classifies the bug" — S016.txt:L14

> "a maintainer does not respond to our initial report within 30 days, we will aim to escalate the finding to an external vulnerability coordinator" — S016.txt:L14

> "In extenuating circumstances—such as events beyond our reasonable control or findings requiring exceptional remediation complexity—we reserve the right to adjust deadlines" — S016.txt:L15

Read as a set, the page names five triggers — engaged maintainer (L11), active exploitation (L12, L14), ecosystem-wide pattern (L13), non-response (L14), extenuating circumstances (L15) — and every one is a trigger, not a discretion in the abstract: the page says what fact moves the clock. The severity rule is the one that cuts both ways: Anthropic defers to the maintainer's severity *except* where it holds "credible evidence of active exploitation" (L14), and then the 7-day target applies "regardless of how the maintainer classifies the bug" (L14). Silence has its own clock: 30 days without a response escalates to an external coordinator and the default timeline still runs out into disclosure (L14).

## Claim 3 — the post-patch buffer is 45 days, and it protects *details*, not the status

> "Once a patch is available, we would generally wait 45 days before publishing full technical details." — S016.txt:L16

> "give downstream users time to deploy the fix before detailed exploitation information is public" — S016.txt:L16

> "We may shorten this buffer if the details are already publicly known through other channels" — S016.txt:L16

The buffer starts when a patch exists and covers "full technical details" only; the report itself is disclosed under Claim 1's default (90 days or patch release, whichever comes first) and the buffer governs when the *detailed* record follows. L16 states that the buffer can move in both directions — shortened when the details are public elsewhere, extended "when patch deployment is unusually complex or the affected footprint is unusually broad" (L16). Do not merge this 45 with F02's 30: Project Zero's 30 days is when the *report* becomes public after an early fix, Anthropic's 45 days is how long *technical detail* waits after a patch. Different number, different object, both first-party.

## Claim 4 — provenance is attached to the report: human review, AI-origin label, patch label

> "Every report we send generally reflects a finding that a human security researcher has reviewed and confirmed." — S016.txt:L17

> "Reports originating from AI-powered discovery are clearly labeled as such." — S016.txt:L17

> "we include it, labeled by provenance and offer to collaborate with the maintainer on a production-quality fix" — S016.txt:L17

The label is on the outbound report, so a maintainer can tell a model-origin report from a human-only one without asking, and a candidate patch carries its own origin label. This is a different claim from F04's validation ground (S009-S012: what a finder should do before reporting); it is what the delivered report *says about itself*. Note the hedge in the first two statements — "generally" (L17) and "where we can" (L9) — so neither human review nor an included patch is an unconditional promise.

## Claim 5 — volume is a negotiated term, and active exploitation outranks the negotiation

> "provide human-reviewed reports with suggested fixes where we can, and pace our submissions to what maintainers can actually absorb." — S016.txt:L9

> "We do not submit large volumes of findings to a single project" — S016.txt:L17

> "without first reaching out in an effort to agree on a pace the maintainer can sustain" — S016.txt:L17

> "Actively exploited vulnerabilities are exempt from pacing and typically follow the compressed timeline above." — S016.txt:L17

This is the row's most transferable rule, and the one no F02 coordinator row states: automated finding volume is paced by agreement with the receiving project, and the exception is exploitation. The rule is expressed as Anthropic's own practice ("We do not submit…"), not as an industry obligation, and "large volumes" is never quantified — a maintainer can quote it to start a pace conversation, not to compute a limit.

## What the policy does not say

- **No coordinator requirement for the normal path.** An external coordinator appears only in the non-response case (L14); engagement does not route through one.
- **No CVE/identifier, reward, or breach clock.** The words do not appear in the body lines (L5-L17).
- **No quantification.** Neither "large volumes" (L17) nor "ecosystem-wide pattern" (L13) carries a count.
- **No promise that the 45-day buffer holds.** L16 names shortening and extension conditions.
- **Nothing about inbound reports.** L8 hands them to a separate policy this capture does not contain.

## How a bounty or security researcher uses it

1. **Quote the default branch, not just the number.** The public-details date is min(90 days, patch release) (L10) — a patched-but-undisclosed finding is late by this policy's own terms.
2. **Map the trigger before arguing about the clock.** Which of the five triggers is in play (L11-L15) decides which interval applies; there is no single Anthropic deadline.
3. **Use the severity exception narrowly.** Deference to the maintainer (L14) holds except on credible active exploitation, where the compressed target overrides the maintainer's classification (L14).
4. **Start the 45-day buffer at the patch, not the report.** It covers technical detail (L16); shortening is allowed when the details are already public elsewhere (L16).
5. **Read the AI-origin label as provenance, not as a quality signal.** A labelled report is one a human reviewed and confirmed (L17); the label says where the finding came from.
6. **Negotiate pace before volume.** Reach out to agree a sustainable rate (L17) — and expect no pacing for actively exploited findings (L17).
7. **Track escalation as a date, not a threat.** Non-response for 30 days moves the finding to an external coordinator with the timeline still running (L14).
8. **Do not cite this page for a programme's inbound terms.** L8 sends those elsewhere.

## Sources overlap — F02 (clocks), F04 (AI-finding validation), F10 (vendor policies), F15 (vendor programme intake)

`grep -oF` on the capture gives `90-day=2`, `45 days=1`, `7-day=3`, `14-day=1`, `AI=4`, `labeled=2`, `pacing=1`, `coordinator=1`; `90+30`, `patch gap`, `upstream`, `trial` are 0. Lane analysis, not a quote: F02 holds the coordinator clocks (S003, S004, S005) and this entry is a fourth, discoverer-side column for that item; F04 holds what a finder should verify before reporting (S009-S012) while L17 is about what the delivered report declares; F10's vendor policies govern reports *into* a vendor, the opposite direction from this outbound policy; F15's S048 describes a vendor research programme as an intake route for other vendors' bugs, and S016 names no intake route at all. None of those rows carries a pacing rule, an AI-origin label, or a post-patch details buffer.

## Falsifiable rule and checks

**Falsifiable rule.** A statement about Anthropic's policy is falsified by any of: (a) naming one Anthropic disclosure deadline, when the page sets 90 days, a 7-day compressed target and a 45-day details buffer on different objects (L10, L12, L16); (b) saying an early patch delays disclosure to day 90, when the default is "whichever comes first" (L10); (c) saying the maintainer's severity always governs, when active exploitation overrides it (L14); (d) saying reports are sent unreviewed or unlabelled, when human review and the AI-origin label are stated (L17); (e) saying bulk submission is permitted at the finder's discretion, when pace is agreed first and only exploitation is exempt (L17); (f) saying the 45-day buffer is fixed, when L16 shortens and extends it; (g) treating this page as Anthropic's inbound disclosure policy, which L8 excludes.

**FC-1 — every block-quoted span is verbatim, ≤25 words, and starts on its declared line.** Each `> "…" — S016.txt:Lnn` span was matched under the instrument's normalization (whitespace collapsed, `<u>` markup removed) against `S016.txt`; observed `spans=22 words_max=24 occurrences=1 each anchors_ok=22 of 22`. No span is a paraphrase and no two spans are the same text.

**FC-2 — revision.** `grep -n 'Last updated' S016.txt` returns L6 ("Last updated Mar 6, 2026"), matching the registry row's `last updated 2026-03-06`; every line reference above is a line of that revision's capture.

**FC-3 — the body is L5-L17.** L1-L4 and L18-L32 are navigation, footer and legal chrome; `grep -c 'Coordinated vulnerability disclosure'` returns 2 (L1 title tag, L5 heading), so no claim quotes chrome as policy.

**FC-4 — the trigger vocabulary is finite and each term is present.** `grep -oF` gives `14-day=1`, `7-day=3`, `45 days=1`, `90-day=2`, `coordinator=1`, `pacing=1`; there is no `30-day` token (the 30-day non-response window is written "within 30 days", L14), so a claim about a 30-day *disclosure* deadline is unsupported here.

**FC-5 — the outbound direction.** `grep -n 'Responsible Disclosure Policy'` returns L8 alone: the page's only pointer to inbound reports, and the reason this row cannot be used as an intake policy.

## Rejected over-generalizations

1. **"Anthropic discloses 90 days after reporting, always."** Rejected: the default is "after 90 days, or after a patch is released, whichever comes first" (L10), and five triggers at L11-L15 move it.
2. **"A patched finding stays private for 90 more days."** Rejected: the patch starts the 45-day *details* buffer (L16), not a fresh disclosure clock; the report's own disclosure is governed by L10, and the buffer delays only the detailed technical record.
3. **"The maintainer decides severity, so nothing moves without them."** Rejected: with credible evidence of active exploitation the 7-day target applies "regardless of how the maintainer classifies the bug" (L14).
4. **"45 days and Project Zero's 30 days are the same patch-adoption window."** Rejected: PZ's 30 days is when the report becomes public after an early fix (F02/S005); Anthropic's 45 days withholds full technical details after a patch exists (L16).
5. **"AI-discovered reports are sent as the model produced them."** Rejected: "Every report we send generally reflects a finding that a human security researcher has reviewed and confirmed" (L17).
6. **"Volume is fine because each finding is valid."** Rejected: "We do not submit large volumes of findings to a single project" before agreeing a pace (L17), with only actively exploited findings exempt (L17).
7. **"Anthropic routes every report through a coordinator."** Rejected: the coordinator appears only when a maintainer has not responded within 30 days (L14).
8. **"This is Anthropic's bug-bounty or inbound disclosure policy."** Rejected: L8 excludes external researchers' reports and points at a different policy.

## Honest limit

- **One page, one instant.** This is the "Last updated Mar 6, 2026" revision (L6) as captured on 2026-10-26; the footer sentence at L28 came back in a different wording between two fetches about a minute apart (2026-10-26T21:15:52Z and 21:16:37Z), so a later revision is a new pin, not a correction of this one. Line numbers are lines of this capture, not rendered page positions.
- **Anthropic's own practice only.** The page describes what Anthropic says it does; none of it is audited here, and "generally"/"we aim to"/"where we can" make several commitments explicitly non-absolute (L9, L15, L16, L17).
- **No inbound policy, no other vendor's practice.** The only inbound pointer is L8, and the page names no other discoverer's policy.
- **Quotes are whitespace-normalized.** Sentences run long in the capture (L7, L8, L17 are single paragraphs), so a quote matches under collapsed whitespace; typographic apostrophes and the em dashes at L15 and L17 are preserved as captured.
- Documentation only: the capture holds public policy text, no credential, session or private URL, and this entry quotes none.
