# TrendAI ZDI's own disclosure process and vendor coordination: what the acquisition programme states

source: S106 — https://www.zerodayinitiative.com/about/ — TrendAI™ Zero Day Initiative™ (ZDI), "About Us" page; capture corpus/source-snapshots/round-71/S106.txt (sha256 291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db, 148 lines, 15004 snapshot bytes, fetched 2026-11-05T01:27:03Z): the programme's self-description at S106.txt:28, the bounty model at S106.txt:31, the process guarantee at S106.txt:47, validation at S106.txt:49, the full-advisory rule at S106.txt:51, the limited-advisory rule at S106.txt:52, the researcher offer at S106.txt:60, vendor communication and credit at S106.txt:61, the case-tracking guarantee at S106.txt:62, the vendor dossier at S106.txt:69, the coordination windows and the 15-business-day escalation at S106.txt:70, and the refusal branch at S106.txt:72
verified-at: 2026-11-05
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-71/manifest.json --source S106   # 15 pinned quotes (Q01-Q15), each located at its anchor; the further spans quoted below are sub-spans of those same anchored lines and are located in the same capture
ground: F49 — what the ZDI acquisition programme says about its own disclosure process and vendor coordination: the validate → reward → private-share → vendor-coordination → advisory sequence; the 120-day standard coordination window and its shortened 30/60/90-day form for flaws from incomplete or problematic patches; ZDI's permissive 15-business-day escalation to a limited public advisory; the full-versus-limited advisory choice; the formal monetary offer and payment step; credit or anonymity; and the no-backlog guarantee. The ZDI policy-page timelines stay with F02/S075, platform severity ladders and reward scales stay with F13, Project Zero's own 90-day policy stays with S005, CERT/CC's own policy stays with S004, the ISO 29147/30111 division of labour stays with F11/F38, and any single published advisory instance stays with its own record.

## Scope and decision rule

A reader deciding what a "ZDI disclosure timeline" claim may assert should treat this page as a
first-party statement of one acquisition programme's own process, and should carry exactly three
things out of it: the sequence ZDI states, the numbers ZDI states with the conditions ZDI attaches
to them, and the boundaries of those statements (a permissive escalation, a shortened window
confined to a named class of flaws, and a guarantee about ZDI's own case tracking). Every sentence
below is attributed to ZDI as the stating party; this entry verifies what the page says, not that
the conduct happened.

Decision rule for "what does this page establish?":

1. **The programme ZDI describes.** ZDI prints its own self-description as "the world's largest
   vendor-agnostic vulnerability disclosure program" (`corpus/source-snapshots/round-71/S106.txt:28`) — a first-party claim about ZDI,
   not a comparative ranking this entry establishes. ZDI also prints an acquisition model:
   "A vendor-agnostic bug bounty program where researchers are financially incentivized
   to submit vulnerabilities." (`corpus/source-snapshots/round-71/S106.txt:31`).
2. **The policy that governs an acquired finding.** ZDI states that "TrendAI™ ZDI's disclosure
   process is designed to ensure that vulnerabilities are handled responsibly, and not resold,
   redistributed, or censored." (`corpus/source-snapshots/round-71/S106.txt:47`), and that "Every vulnerability acquired through the
   program is managed according to the TrendAI™ ZDI disclosure policy" (`corpus/source-snapshots/round-71/S106.txt:47`).
3. **The sequence ZDI states.** ZDI states that "Each submission begins with validation."
   (`corpus/source-snapshots/round-71/S106.txt:49`), and that "Once validated, the researcher receives their reward, and the issue
   is privately shared with the affected vendor" (`corpus/source-snapshots/round-71/S106.txt:49`) — validation, then reward, then
   private sharing with the vendor.
4. **The numbers ZDI states, with their conditions.** ZDI states that "Vendors are given a standard
   coordination window of 120 days under TrendAI™ ZDI's disclosure policy." (`corpus/source-snapshots/round-71/S106.txt:70`); that
   "For flaws that result from incomplete or problematic security patches" (`corpus/source-snapshots/round-71/S106.txt:70`) ZDI
   "shortens the window to 30, 60, or 90 days, depending on multiple factors" (`corpus/source-snapshots/round-71/S106.txt:70`); and
   that "If a vendor fails to respond within 15 business days of first contact, TrendAI™ ZDI may
   escalate to a limited public advisory to protect users." (`corpus/source-snapshots/round-71/S106.txt:70`).
5. **The advisory choice.** ZDI states that "When the vendor releases a patch, TrendAI™ ZDI
   publishes a full advisory." (`corpus/source-snapshots/round-71/S106.txt:51`); that "TrendAI™ ZDI may publish a limited advisory
   to protect the broader public while withholding information that could enable exploitation."
   (`corpus/source-snapshots/round-71/S106.txt:52`); and that where a vendor refuses to patch or stays unresponsive ZDI "may
   publish a full or limited advisory" (`corpus/source-snapshots/round-71/S106.txt:72`).
6. **The researcher-side flow.** ZDI states that "Once your report is received, TrendAI™ ZDI
   validates the vulnerability, confirms its severity, and issues a formal monetary offer."
   (`corpus/source-snapshots/round-71/S106.txt:60`), and that "When you accept the offer, payment is processed, and the case enters
   the vendor coordination phase" (`corpus/source-snapshots/round-71/S106.txt:60`).

## What the acquisition programme states about itself

| item | what ZDI states | location |
|---|---|---|
| programme self-description | "the world's largest vendor-agnostic vulnerability disclosure program" | `corpus/source-snapshots/round-71/S106.txt:28` |
| acquisition model | "A vendor-agnostic bug bounty program where researchers are financially incentivized to submit vulnerabilities." | `corpus/source-snapshots/round-71/S106.txt:31` |
| submission volume | ZDI states "TrendAI™ ZDI imposes no limit on the number of reports researchers can submit" | `corpus/source-snapshots/round-71/S106.txt:60` |
| process guarantee | "TrendAI™ ZDI's disclosure process is designed to ensure that vulnerabilities are handled responsibly, and not resold, redistributed, or censored." | `corpus/source-snapshots/round-71/S106.txt:47` |
| acquired-finding scope | "Every vulnerability acquired through the program is managed according to the TrendAI™ ZDI disclosure policy" | `corpus/source-snapshots/round-71/S106.txt:47` |

The self-description row is a first-party claim printed by ZDI about itself. This entry records the
claim and does not test it; no independent ranking is asserted here.

## The disclosure sequence ZDI states

ZDI prints the flow as: submission → validation → reward → private sharing with the vendor →
vendor coordination → advisory. The individual steps are located as follows.

| step | what ZDI states | location |
|---|---|---|
| validation | "Each submission begins with validation." | `corpus/source-snapshots/round-71/S106.txt:49` |
| reward and private share | "Once validated, the researcher receives their reward, and the issue is privately shared with the affected vendor" | `corpus/source-snapshots/round-71/S106.txt:49` |
| formal monetary offer | "Once your report is received, TrendAI™ ZDI validates the vulnerability, confirms its severity, and issues a formal monetary offer." | `corpus/source-snapshots/round-71/S106.txt:60` |
| payment and coordination phase | "When you accept the offer, payment is processed, and the case enters the vendor coordination phase" | `corpus/source-snapshots/round-71/S106.txt:60` |
| vendor-side dossier | "TrendAI™ ZDI provides the vendor with a complete technical dossier, which includes proof of concept, reproducible steps, severity assessment" | `corpus/source-snapshots/round-71/S106.txt:69` |
| vendor communication | "TrendAI™ ZDI handles all communication with the affected vendor, including root cause clarification, patch feasibility questions, patch timelines, and disclosure scheduling." | `corpus/source-snapshots/round-71/S106.txt:61` |

The dossier row describes what ZDI says it hands to the vendor. It is not an instruction to probe,
scan or test any target, and no target, host or credential appears here.

## The coordination windows ZDI states

ZDI states one standard window and one shortened form, and states an escalation branch that is
permissive rather than automatic.

| branch | condition ZDI states | interval ZDI states | location |
|---|---|---|---|
| standard | vendors are given a standard coordination window under ZDI's disclosure policy | "Vendors are given a standard coordination window of 120 days under TrendAI™ ZDI's disclosure policy." | `corpus/source-snapshots/round-71/S106.txt:70` |
| shortened | "For flaws that result from incomplete or problematic security patches" | "TrendAI™ ZDI shortens the window to 30, 60, or 90 days, depending on multiple factors" | `corpus/source-snapshots/round-71/S106.txt:70` |
| escalation | "If a vendor fails to respond within 15 business days of first contact" | ZDI "may escalate to a limited public advisory to protect users." | `corpus/source-snapshots/round-71/S106.txt:70` |

Two limits are load-bearing. The shortened window is confined by ZDI to the stated class of flaws —
"flaws that result from incomplete or problematic security patches" (`corpus/source-snapshots/round-71/S106.txt:70`) — and the page
names no factor, threshold or severity band that selects between 30, 60 and 90 days; it says only
"depending on multiple factors" (`corpus/source-snapshots/round-71/S106.txt:70`). The escalation branch is written as a permission
("may escalate to a limited public advisory", `corpus/source-snapshots/round-71/S106.txt:70`), not as an automatic publication, and
the page names no clock-start event for the 120-day window: the capture contains "120 days" once
(`corpus/source-snapshots/round-71/S106.txt:70`) and no line of the capture states when that window starts.

## The advisory choice ZDI states

| situation ZDI states | outcome ZDI states | location |
|---|---|---|
| "When the vendor releases a patch" | "TrendAI™ ZDI publishes a full advisory." | `corpus/source-snapshots/round-71/S106.txt:51` |
| what a full advisory carries | "The advisory includes technical details, credit to the submitting researcher (unless they choose to remain anonymous), and links to the vendor's patch." | `corpus/source-snapshots/round-71/S106.txt:51` |
| no fix, or the vendor declines to address the issue within the coordination timeline | ZDI "may publish a limited advisory to protect the broader public while withholding information that could enable exploitation." | `corpus/source-snapshots/round-71/S106.txt:52` |
| the vendor refuses to patch or remains unresponsive | ZDI "may publish a full or limited advisory" | `corpus/source-snapshots/round-71/S106.txt:72` |
| sanitized sharing beyond the programme's own customers | ZDI "may also share sanitized information with other security vendors and researchers to extend protection beyond Trend customers." | `corpus/source-snapshots/round-71/S106.txt:52` |

The two "may publish" rows are not interchangeable with the full-advisory row: ZDI states the full
advisory for a released patch, and states a permissive limited-or-full choice for the refusal and
unresponsive branches. Nothing on the page states that a particular advisory exists or that any
branch was taken in any case.

## Credit, anonymity, and the no-backlog guarantee

ZDI states that "You can choose to be publicly credited in the advisory, remain anonymous, or use
a pseudonym." (`corpus/source-snapshots/round-71/S106.txt:61`). ZDI also states a guarantee about its own case handling: "TrendAI™
ZDI guarantees that your work will not disappear into a backlog or remain undisclosed due to
vendor inaction." (`corpus/source-snapshots/round-71/S106.txt:62`), and that "Every case is tracked, managed under a defined
timeline, and disclosed according to our disclosure policy even if a vendor declines to issue a
patch." (`corpus/source-snapshots/round-71/S106.txt:62`).

Both sentences are ZDI's own guarantee about ZDI's own tracked cases, not a property of
coordinated disclosure in general and not an observation of any individual case.

## Scope limits

This entry is one acquisition programme's own process statement. It is **not** F13's platform
severity ladder and reward scale (that comparison stays with `corpus/knowledge/program-severity-ladders-and-reward-scales.md`);
it is **not** S005's Project Zero 90-day policy; it is **not** S004's CERT/CC own disclosure policy;
it is **not** F11/F38's ISO 29147/30111 division of labour between requester and coordinator; and
it is **not** any single published advisory instance. Where another entry already owns a
programme's policy page, that entry keeps it: the ZDI policy-page timelines and their branch
conditions stay with F02/S075 (`corpus/knowledge/zdi-disclosure-policy.md`). Where a number below
is ZDI's own statement about its own programme, a package that restates it as a general rule, as
another coordinator's deadline, or as a severity-tiered window has left this page; the
severity-selected shortened-window tiers ZDI states on its own policy page stay with F02/S075
(`corpus/source-snapshots/round-47/S075.txt:25`).

## Falsifiable rule

A reader can check any package that asserts a ZDI disclosure deadline or ZDI disclosure outcome
against this entry with three checks, each answerable from the capture alone:

1. **The stating party.** The package must name TrendAI™ ZDI as the party whose policy states the
   window; the window ZDI states is "a standard coordination window of 120 days under TrendAI™
   ZDI's disclosure policy" (`corpus/source-snapshots/round-71/S106.txt:70`), so a package that attributes the figure to a vendor,
   to Project Zero, to CERT/CC or to ISO fails this check.
2. **The condition attached to a shortened window.** If the package states 30, 60 or 90 days it
   must carry ZDI's own condition "For flaws that result from incomplete or problematic security
   patches" (`corpus/source-snapshots/round-71/S106.txt:70`); a package that applies the shortened windows to ordinary reports
   fails this check. The check binds packages that state the figure on this page's authority;
   where a package cites F02/S075's policy-page tiers, S075's severity and exploitation conditions
   apply instead (`corpus/source-snapshots/round-47/S075.txt:25`).
3. **The modality of the escalation.** If the package states the 15-business-day branch it must
   say ZDI "may escalate to a limited public advisory to protect users" (`corpus/source-snapshots/round-71/S106.txt:70`); a package
   that says ZDI publishes after 15 business days of silence fails this check.

A package that fails any of the three checks is not falsified by this entry's judgement; it is
falsified by the located quote at the cited anchor. The fifteen pinned spans are re-verified by the
`recheck:` command above; each further span quoted here is a sub-span of the same anchored line and
is located in the same capture.

## Rejected over-generalizations

Each proposition below is this entry's own phrasing of a claim a reader might make; none of them
is a sentence from the capture, and each is rejected with the located quote that falsifies it.

1. **"120 days is the disclosure deadline for vulnerabilities."** Rejected: the figure is ZDI's own
   statement of a standard *coordination* window under ZDI's disclosure policy (`corpus/source-snapshots/round-71/S106.txt:70`), the
   same line states a shorter window for a named class of flaws, and the capture states no
   clock-start event for the 120 days.
2. **"ZDI publishes 30, 60 or 90 days after a submission, by severity."** Rejected: this page
   states the shortened window for "flaws that result from incomplete or problematic security
   patches" (`corpus/source-snapshots/round-71/S106.txt:70`) and names no severity band, only "depending on multiple factors"
   (`corpus/source-snapshots/round-71/S106.txt:70`); severities do select the shortened length on ZDI's policy page, which stays
   with F02/S075 (`corpus/source-snapshots/round-47/S075.txt:25`).
3. **"A vendor that goes silent for 15 business days is automatically published."** Rejected: ZDI
   writes a permission — "may escalate to a limited public advisory to protect users"
   (`corpus/source-snapshots/round-71/S106.txt:70`) — and the refusal branch is likewise "may publish a full or limited advisory"
   (`corpus/source-snapshots/round-71/S106.txt:72`).
4. **"ZDI's no-backlog guarantee is a property of coordinated disclosure generally."** Rejected: it
   is ZDI's guarantee about ZDI's own cases — "Every case is tracked, managed under a defined
   timeline" (`corpus/source-snapshots/round-71/S106.txt:62`).
5. **"ZDI's reward structure is a platform severity ladder."** Rejected: F13 holds platform
   severity ladders and reward scales; this page states only a formal monetary offer
   (`corpus/source-snapshots/round-71/S106.txt:60`), points in a rewards program, and that ZDI "imposes no limit on the number of
   reports researchers can submit" (`corpus/source-snapshots/round-71/S106.txt:60`).
6. **"ZDI's window is the same as Project Zero's 90-day policy or CERT/CC's policy."** Rejected:
   those are S005's and S004's own statements, and this page is ZDI's own; no page here states a
   comparison.

## Gate

Admitted 2026-11-05 (round 71) on S106, opened this round (`capture-source.py --kind html`, HTTP
200, fetched 2026-11-05T01:27:03Z). Located quote (≤25 words, `corpus/source-snapshots/round-71/S106.txt:70`): "Vendors are given a
standard coordination window of 120 days under TrendAI™ ZDI's disclosure policy." Fifteen quotes
are pinned in `corpus/source-snapshots/round-71/manifest.json`; the longest pinned quote is 25
words. The `recheck:` command above prints one `S106:<quote-id> OK occurrences=<n> anchor=<n>-ok`
line per pinned quote and exits 0; `Q01-scope` is the only pinned span that occurs twice in the
capture, and the manifest pins it at its first occurrence.

Pinned spans and their `wc -w` counts (measured with `wc -w` on the quoted text):

| pin | anchor | words | span |
|---|---|---|---|
| Q01-scope | `corpus/source-snapshots/round-71/S106.txt:28` | 7 | programme self-description |
| Q02-acquisition | `corpus/source-snapshots/round-71/S106.txt:31` | 13 | bounty model |
| Q03-guarantee | `corpus/source-snapshots/round-71/S106.txt:47` | 19 | process guarantee |
| Q04-validation | `corpus/source-snapshots/round-71/S106.txt:49` | 5 | validation first |
| Q05-window | `corpus/source-snapshots/round-71/S106.txt:70` | 15 | 120-day standard window |
| Q06-shortened | `corpus/source-snapshots/round-71/S106.txt:70` | 15 | 30/60/90-day shortening |
| Q07-escalation | `corpus/source-snapshots/round-71/S106.txt:70` | 25 | 15-business-day escalation |
| Q08-limited | `corpus/source-snapshots/round-71/S106.txt:52` | 19 | limited advisory |
| Q09-full | `corpus/source-snapshots/round-71/S106.txt:51` | 12 | full advisory on a patch |
| Q10-offer | `corpus/source-snapshots/round-71/S106.txt:60` | 19 | formal monetary offer |
| Q11-nobacklog | `corpus/source-snapshots/round-71/S106.txt:62` | 19 | no-backlog guarantee |
| Q12-credit | `corpus/source-snapshots/round-71/S106.txt:61` | 16 | credit, anonymity, pseudonym |
| Q13-dossier | `corpus/source-snapshots/round-71/S106.txt:69` | 19 | vendor technical dossier |
| Q14-refusal | `corpus/source-snapshots/round-71/S106.txt:72` | 18 | refusal branch |
| Q15-nolimit | `corpus/source-snapshots/round-71/S106.txt:60` | 13 | no limit on submissions |

Further spans quoted above, each a sub-span of an anchored line, with their `wc -w` counts:

| anchor | words | span |
|---|---|---|
| `corpus/source-snapshots/round-71/S106.txt:47` | 15 | acquired findings managed under ZDI's disclosure policy |
| `corpus/source-snapshots/round-71/S106.txt:49` | 17 | reward, then private sharing with the vendor |
| `corpus/source-snapshots/round-71/S106.txt:51` | 22 | what a full advisory carries |
| `corpus/source-snapshots/round-71/S106.txt:52` | 19 | sanitized sharing beyond the programme's customers |
| `corpus/source-snapshots/round-71/S106.txt:60` | 16 | payment, then the vendor coordination phase |
| `corpus/source-snapshots/round-71/S106.txt:61` | 21 | ZDI handles all vendor communication |
| `corpus/source-snapshots/round-71/S106.txt:62` | 25 | every case tracked, managed, disclosed |
| `corpus/source-snapshots/round-71/S106.txt:70` | 10 | the condition on the shortened window |

## Limits

- **First-party statements only.** Every rule here is what ZDI prints about ZDI's own programme.
  Nothing on the page is evidence that any advisory was published, that any window was honoured, or
  that any vendor behaved as described; the page's own assurance about its case tracking
  (`corpus/source-snapshots/round-71/S106.txt:62`) is a policy statement, not proof of conduct.
- **No clock-start event.** The capture states no start event for the 120-day coordination window:
  the string "120 days" occurs once (`corpus/source-snapshots/round-71/S106.txt:70`), and no line states when the window begins. A
  reader must not convert the window into a date by supplying a start event the page does not give.
- **The factors behind 30/60/90 are not enumerated on this page.** The page states "depending on
  multiple factors" (`corpus/source-snapshots/round-71/S106.txt:70`) and does not list them, so a package cannot select a shortened
  length for a given finding from this page; the policy page's severity and exploitation tiers stay
  with F02/S075 (`corpus/source-snapshots/round-47/S075.txt:25`).
- **No severity tiers, no payout amounts.** The page states a formal monetary offer
  (`corpus/source-snapshots/round-71/S106.txt:60`), and the same line says yearly point totals unlock "bonus multipliers, higher
  payout tiers" (`corpus/source-snapshots/round-71/S106.txt:60`) — but it names no monetary amount, no tier value and no severity
  band, so the platform ladder and the reward scale live with F13
  (`corpus/knowledge/program-severity-ladders-and-reward-scales.md`), not here.
- **One programme, one page.** The page also carries general programme claims (founding year,
  researcher counts, disclosure counts, protection-filter deployment). None is pinned by the
  manifest's fifteen quotes, so none is asserted here; the entry covers only the disclosure
  process and vendor coordination statements listed above.
- **Documentation only.** This entry records a captured public page. It instructs no probing,
  scanning, logging in or submission against any target, carries no credential material, and names
  no private URL or vault reference.
- **The recheck verifies pinned bytes, not the live page.** The `recheck:` command compares the
  pinned capture's digest and the located quotes; it does not re-fetch the network and does not
  establish that the page still reads this way.
