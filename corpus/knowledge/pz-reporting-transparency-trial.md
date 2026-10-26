# Project Zero's 2025 reporting-transparency trial — a one-week public notice ahead of an unchanged 90-day deadline, and the "upstream patch gap" it is meant to shrink

source: S017 — https://projectzero.google/2025/07/reporting-transparency.html — capture corpus/source-snapshots/round-40/S017.txt (39 lines, 5,058 bytes; sha256 3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe): title L12, date "2025-Jul-29" L13, byline L14-L15, "90+30" model and patch gap L16, upstream patch gap L17-L19, trial announcement L20, "The Trial: Reporting Transparency" L21-L28, rationale L29-L32, "Will this help attackers?" L33-L34, acknowledged cost L35-L36, trial status L37
verified-at: 2026-10-26 (re-opened by me this day: the URL returned HTTP 200, text/html, 14,764 raw bytes, raw sha256 6addf3baff5f61ff7a6a8750007cc2b0d4aa2153a317ed2a8974412bbce2cfb3 at 2026-10-26T21:16:38Z; converting that body with the lane's `corpus/instruments/capture-source.py html_to_text()` reproduced the landed capture byte for byte — 39 lines / 5,058 bytes / sha256 3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe, `cmp` clean)
ground: F02 — a fourth disclosure-timeline shape: the 90-day deadline unchanged, a new ~1-week public-notice milestone inserted before it, and a definition that separates the earlier "upstream patch gap" from the user-side "patch gap" that F06's downstream-role ground (S018) presumes but does not name
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S017   # prints S017:sha256 OK then one S017:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved — a pinned-capture comparison under whitespace collapse, not a fresh network check

## Attribution

Project Zero's own policy announcement, first-party and dated: "Policy and Disclosure: 2025 Edition" (L12), "2025-Jul-29" (L13), "Posted by Tim Willis, Google Project Zero" (L15). It is presented as a change to Project Zero's own process, and it is explicitly a pilot — "trial" occurs 7 times in the capture, twice as a self-description of the policy itself (L20, L37).

> "To address this, we're announcing a new trial policy: Reporting Transparency." — S017.txt:L20

> "This is a trial, and we will be closely monitoring its effects." — S017.txt:L37

One named collaborator joins it, and only one:

> "Google Big Sleep, a collaboration between Google DeepMind and Google Project Zero, will also be trialling this policy" — S017.txt:L28

So this post is authoritative for Project Zero's and Big Sleep's reporting practice, and for nothing else — not for Google, and not for other coordinators.

## Claim 1 — the trial adds a notice milestone; the 90-day deadline is unchanged

> "Our core 90-day disclosure deadline will remain in effect." — S017.txt:L22

> "However, we're adding a new step at the beginning of the process." — S017.txt:L22

> "within approximately one week of reporting a vulnerability to a vendor, we will publicly share that a vulnerability was discovered" — S017.txt:L23

> "This trial maintains our existing 90+30 policy, meaning vendors still have 90 days to fix a bug before it is disclosed" — S017.txt:L27

> "with a 30-day period for patch adoption if the bug is fixed before the deadline" — S017.txt:L27

Lane reading: the trial moves a *milestone*, not a deadline. The clock still starts at reporting to the vendor (L23) and still runs 90 days (L22, L27); what is new is a disclosure-of-existence at about day 7. Read against F02, none of its three rows (S003, S004, S005) has a finder announcing a pending report: S005's Project Zero FAQ gives the 90+30 figure and the 14-day grace, and this post keeps the same figures while adding an earlier publication event.

## Claim 2 — the notice is an enumeration of three facts and nothing else

> "The vendor or open-source project that received the report." — S017.txt:L24

> "The affected product." — S017.txt:L25

> "The date the report was filed, and when the 90-day disclosure deadline expires." — S017.txt:L26

The post introduces the list with "We will share:" (L23) and then gives exactly these three lines (L24-L26). No vulnerability class, no component, no severity and no fix are among them. A reader who infers more from a Project Zero notice is inferring beyond the policy's own content list.

## Claim 3 — the disclosure limit for the whole trial

> "no technical details, proof-of-concept code, or information that we believe would materially assist discovery will be released until the deadline" — S017.txt:L34

> "Reporting Transparency is an alert, not a blueprint for attackers." — S017.txt:L34

The section is headed "Will this help attackers?" and opens "No —" (L34); the limit is temporal — "until the deadline" — and the post states it once, for the trial as a whole, rather than report by report. This is also the sentence that separates this row from `vendor-disclosure-policies-as-corpus-objects.md` (F10): the notice discloses existence while the technical record waits.

## Claim 4 — the target is the earlier gap, defined against the user-side one

> "Many consider the patch gap to be the time between a fix being released for a security vulnerability and the user installing the relevant update." — S017.txt:L17

> "an upstream vendor has a fix available, but downstream dependents, who are ultimately responsible for shipping fixes to users, haven’t yet integrated it" — S017.txt:L17

> "this upstream gap significantly extends the vulnerability lifecycle" — S017.txt:L18

> "a vulnerability isn't fixed when a patch is released from Vendor A to Vendor B" — S017.txt:L19

> "The primary goal of this trial is to shrink the upstream patch gap by increasing transparency." — S017.txt:L30

> "By providing an early signal that a vulnerability has been reported upstream, we can better inform downstream dependents." — S017.txt:L30

Lane reading: two different delays, and the trial targets the first. The user-side gap (L17) is deployment lag after a fix exists; the upstream gap (L17) is integration lag between an upstream fix and a downstream product. The F06 frontier row already teaches the downstream caution in its own words — "an upstream fix is not downstream evidence" (`corpus/README.md:207`) — and S017 supplies the mechanism behind that caution: the downstream party may not know a fix exists, which is why the post's intervention is a report-existence signal.

## Claim 5 — the rationale is stated as expectation, and the cost is admitted

> "Our goals were to drive faster yet thorough patch development, and improve patch adoption." — S017.txt:L16

> "We hope that this trial will encourage the creation of stronger communication channels between upstream vendors and downstream dependents" — S017.txt:L31

> "make it easier for researchers and the public to track how long it takes for a fix to travel" — S017.txt:L32

> "for some vendors without a downstream ecosystem, this policy may create unwelcome noise and attention for vulnerabilities that only they can address" — S017.txt:L35

> "We believe the benefits of a fair, simple, consistent and transparent policy outweigh the risk of inconvenience to a small number of vendors." — S017.txt:L35

The benefit claims are hopes and beliefs (L31, L35), and the measurable claim is about tracking (L32), not about outcomes: the post announces a data source before the trial produces data. The cost side is not denied — vendors whose bugs only they can fix get attention they did not ask for — and the post's answer is a judgement about a minority ("these vendors now represent the minority of vulnerabilities reported by Project Zero", L35), not an exemption for them. This is a self-reported, first-party expectation and must be labelled as such (Q4).

## What the post does not say

- **No end date and no results.** It announces the trial (L20) and promises monitoring (L37); nothing here reports an effect.
- **No coverage beyond Project Zero and Big Sleep.** L28 is the only second participant named.
- **No change to 90+30 and no new grace.** The 14-day extension F02 records from S005 is not mentioned in this capture; the trial is additive to the deadline model.
- **No technical content in the notice.** L24-L26 is the complete content list.
- **No exploitation data.** There is no reference to exploitation status, severity scoring or a catalogue: `CVSS`, `KEV`, `EPSS`, `SSVC` and `CSAF` each occur 0 times.

## How a bounty or security researcher uses it

1. **Read a Project Zero pre-notice as existence, not as a bug.** The notice is the three facts at L24-L26, published about a week after the report (L23).
2. **Do not date the disclosure from the notice.** The 90-day deadline still runs from the report (L27); the notice is day ~7 of it.
3. **Quote the limit if you are asked whether PZ is dropping 0-days early.** "an alert, not a blueprint" (L34) and the "until the deadline" rule (L34) are the policy's own answer.
4. **Use the notice date as the downstream signal it is meant to be.** The target audience is "downstream dependents" (L30), not end users.
5. **Do not generalize the practice.** It is a trial (L20, L37) and covers Project Zero and Big Sleep (L28); the post itself notes other vendors may find it noisy (L35).
6. **Do not claim the trial was evaluated.** The post is prospective; the outcome figures would have to come from a later publication.
7. **Do not confuse the two gaps when attributing delay.** An upstream patch and a shipped fix are different events (L17-L19).

## Sources overlap — F02 (timelines), F06 (multi-party roles), F10 (vendor policy objects)

`grep -oF` on the capture gives `trial=7`, `upstream=9`, `patch gap=4`, `downstream=4`, `90+30=2`, `90-day=2`, `CVSS=0`, `KEV=0`, `EPSS=0`, `SSVC=0`, `CSAF=0`. Lane analysis, not a quote: F02 holds the published clocks (S003, S004, S005) and this entry adds the notice milestone to that item; F06's S018 is the lane's multi-party role ground and this post defines the delay those roles imply; F10 collects vendor policies as corpus objects and the disclosure rules of those policies govern inbound reports, whereas this post governs what a finder publishes about its own pending report. The post defines no scoring system and no exploitation catalogue, so no F18/F19/F20/F21 row is in scope.

## Falsifiable rule and checks

**Falsifiable rule.** A statement about this trial is falsified by any of: (a) saying Project Zero shortened or extended its 90-day deadline, when the post says the deadline "will remain in effect" (L22) and restates 90+30 (L27); (b) saying technical details are published at notice time, when L34 withholds them "until the deadline"; (c) saying the notice itself describes the vulnerability, when its content list is three facts (L24-L26); (d) saying the trial is Google-wide or industry practice, when the only other participant named is Big Sleep (L28) and the post calls it a trial (L20, L37); (e) equating the upstream patch gap with the user-side patch gap, when L17 defines them separately; (f) saying the trial has demonstrated a benefit, when the benefit is stated as a hope or belief (L31, L35) and the post promises monitoring rather than results (L37).

**FC-1 — every block-quoted span is verbatim, ≤25 words, and starts on its declared line.** Each `> "…" — S017.txt:Lnn` span was matched under the instrument's normalization (whitespace collapsed, `<u>` markup removed) against the landed capture; observed `spans=24 words_max=25 occurrences=1 each anchors_ok=24 of 24`.

**FC-2 — date and byline.** `grep -n '2025-Jul-29'` returns L13 and `grep -n 'Posted by Tim Willis'` returns L15; the registry row's anchor ("The Trial: Reporting Transparency; 2025-07-29") matches both the section heading L21 and the date L13.

**FC-3 — the notice content list is exactly three items.** L23 ends with "We will share:" and L24-L26 are the three following lines, each a complete sentence; L27 resumes the policy statement, so no fourth item exists between them.

**FC-4 — the deadline model is restated, not replaced.** `grep -oF '90+30'` returns 2 occurrences (L16 and L27) and `grep -oF '90-day'` returns 2 (L22 and L26); there is no `120-day` or `60-day` token, so a claim of a shortened or lengthened clock is unsupported by this capture.

**FC-5 — the trial vocabulary is the capture's own.** `grep -oF 'trial'` returns 7 hits, including the self-description at L20 and the status statement at L37; a claim that the post presents a permanent policy contradicts its own wording.

## Rejected over-generalizations

1. **"Project Zero now publishes technical details when it reports a bug."** Rejected: no technical detail, PoC or materially assisting information "will be released until the deadline" (L34).
2. **"The trial shortens Project Zero's deadline."** Rejected: "Our core 90-day disclosure deadline will remain in effect" (L22) and the 90+30 restatement (L27).
3. **"The public notice contains the report."** Rejected: the notice is the three facts at L24-L26.
4. **"This is Google's disclosure policy."** Rejected: the post is Project Zero's, with Big Sleep added (L28); no other Google team is named.
5. **"The upstream patch gap is just the patch gap."** Rejected: L17 defines the user-side gap (fix released → user installs) and the earlier upstream gap (upstream fix → downstream integration) as different periods.
6. **"The trial has been shown to speed patching."** Rejected: the benefit is a hope (L31) and a belief (L35); the post commits to monitoring (L37), not to results.
7. **"Vendors without downstream ecosystems are exempt from the notice."** Rejected: L35 says the policy "may create unwelcome noise and attention" for exactly those vendors, which is a cost accepted, not an exemption granted.

## Honest limit

- **One post, one date.** This is the 2025-07-29 announcement (L13) as captured on 2026-10-26; whether the trial continued, changed or ended after that post is not stated in these bytes, and a later status page is a new pin, not a correction of this entry.
- **Prospective, not evaluative.** The post describes an intention and a measurement plan (L32, L37); no outcome data exists in the capture, so nothing here supports a claim about the trial's effect.
- **Project Zero and Big Sleep only.** The post speaks for two reporting teams (L15, L28); treating it as a statement by Google or by the industry over-reads it.
- **Quotes are whitespace-normalized.** The post's paragraphs run long in the capture, so quotes match under collapsed whitespace; the typographic apostrophe in "haven’t" (L17) and the straight ones elsewhere are preserved as captured.
- Documentation only: the capture holds public policy text, no credential, session or private URL, and this entry quotes none.
