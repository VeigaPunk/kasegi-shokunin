# Linux kernel security-bugs reporting process

source: S071 — https://docs.kernel.org/process/security-bugs.html — section anchors: Preparing your report (S071.txt:10-71); What qualifies as a security bug (S071.txt:73-107); Responsible use of AI to find bugs (S071.txt:174-252); Disclosure and embargoed information (S071.txt:299-327); RST capture at `corpus/source-snapshots/round-45/S071.txt`.
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d

## Scope and decision rule

This entry records one upstream project's reporting rule: the Linux kernel security team's page on how to report security bugs to the kernel. It governs reports sent to the kernel security list and to kernel maintainers. It is not a rule for distributions, for other projects, or for CVE handling beyond what the page itself states, and it is not general guidance on coordinated disclosure.

The page treats four items as required for any security bug report: “The following information are absolutely necessary in any security bug report” (`S071.txt:17-18`). Those four are the affected kernel version range, the problem description, a reproducer and the triggering conditions (listed at `S071.txt:20-47`).

Decision rule: a package may describe a Linux kernel report as complete for kernel intake only when all four items are present and the version is a stable identifier. A package may describe the embargo only in the terms of the table below. A package may not describe an issue that cannot be reproduced as a security bug.

| observed question | kernel text | package consequence |
|---|---|---|
| Does the report name a kernel version? | “with no version indication, your report will not be processed” (`S071.txt:20-22`) | Record the version field as missing and the report as not processable under this page; do not fill the field from a date, a branch name or a distro string. |
| Is a time-dependent label a version? | “A stable identifier such as a commit ID or an exact version is required” (`S071.txt:22-23`); the page also rejects a time-dependent version such as its latest-mainline example (`S071.txt:21-22`, paraphrased). | Accept only a commit ID or an exact version. A label that changes over time fails the field. |
| Does a distro kernel version satisfy the field? | “Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers” (`S071.txt:23-24`) | Keep the distro string as context only; the kernel.org identifier is still required. |
| May the reproducer be a binary? | “Binary-only executables are not accepted” (`S071.txt:39-40`) | The reproducer field must hold source code, a shell script, an instruction sequence or a file-system image (listed at `S071.txt:38-39`). A binary-only file fails the field. |
| Is an issue that cannot be reproduced a security bug? | “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug” (`S071.txt:41-43`) | Keep the item out of security-bug status while reproduction is absent; record it as an unconfirmed candidate. |
| Does an AI-assisted finding stay private? | “If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`) | Record the publication status as public. A package may not describe an AI-assisted finding as private-only. |
| Is the reproducer placed in the public body? | “do not publicly share a reproducer, as this could cause unintended harm” (`S071.txt:99`); “the reproducer should only be shared upon maintainers' request” (`S071.txt:210-211`) | State that a reproducer exists and is available on maintainer request; keep it out of the public text. |
| What starts the kernel's embargo clock? | “Once a robust fix has been developed, the release process starts” (`S071.txt:305`); “for the kernel security team occasional embargoes (as subject to a maximum allowed number of days) start from the availability of a fix” (`S071.txt:342-344`) | The clock starts at the release-process start after a fix exists. It does not start at the report date. |
| How long may publication of a fix be postponed? | “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`); “if it is agreed that the criticality of the bug requires more time” (`S071.txt:312`) | Record the release-process start date and a 7-day ceiling. The 14-day extension requires the agreement the page names. A longer deferral is unsupported by S071. |
| Which deferral reason is valid? | “The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA” (`S071.txt:312-314`) | Record QA or large-scale rollout coordination as the reason. Other reasons are not supported by this page. |
| When may linux-distros be contacted? | “a fix is accepted by the affected code's maintainers” (`S071.txt:350`) | Record linux-distros contact as not yet permitted until the maintainers accept the fix. |
| Who receives the report? | “If there are two or fewer recipients in your message” (`S071.txt:271-272`); “you must also always Cc: the Linux kernel security team” (`S071.txt:272-273`) | With two or fewer maintainer recipients, the security team must be Cc'd. Record the recipient count. |
| Is a CVE a required intake field? | “The security team does not assign CVEs, nor do we require them for reports or fixes” (`S071.txt:362-363`) | Do not list a CVE as a required field. Its absence is not a defect under this page. |

## Overlap and novelty

Already held in this corpus:

- F02 (`corpus/knowledge/coordinated-disclosure-timelines.md:7-17`) requires a timeline to name the policy, the clock-starting event, the stated interval, the patch/publication relationship and any documented extension, and forbids transplanting another coordinator's interval (line 17). This entry applies that rule to the kernel's own record. The 7-day and 14-day figures are S071's, bound to the release-process trigger. They must not be read into F02's CERT/CC 45-day row (`corpus/knowledge/coordinated-disclosure-timelines.md:22`) or its Project Zero 30-day and 14-day grace rows (`corpus/knowledge/coordinated-disclosure-timelines.md:24-25`).
- F04 (`corpus/knowledge/ai-assisted-finding-validation.md:7-8,15`) holds that an AI-originated finding stays a candidate until reproduction and an independent reviewer are recorded. S071 does not require a reviewer distinct from the producer. Its reporter-side check is that a reproducer which fails should lead to the report's validity being questioned: “the validity of the report should be seriously questioned” (`S071.txt:208-209`). F04's validation record and S071's intake duties are separate checks.
- F15 (`corpus/knowledge/vendor-third-party-finding-coordination.md:91-96`; `corpus/README.md:309`) holds the rule to record which party coordinates a multi-party finding. S071 places distro and vendor disclosure coordination with other groups: “other groups focus on fixing issues in distros and coordinating disclosure between operating system vendors” (`S071.txt:333-334`). For a kernel report, S071 therefore records no kernel-security-team coordination role for distro or vendor disclosure.

What is new here:

1. The kernel's required-fields intake contract. A maintainer-side list of four necessary fields, with a stated consequence for a missing version (`S071.txt:20-22`). F02 and F04 hold timelines and validation records, not an upstream intake gate.
2. The AI-assisted-report duties. The page requires a plain-text report with the four items, not Markdown decoration, a recipients section and a fix tested before reporting (`S071.txt:195-196`, `S071.txt:213-217`; the MUST list at `S071.txt:239-245`). The MUST wording itself is quoted: “Prepare a plain-text report explaining the problem. It must contain the four items listed at the top of this file as absolutely necessary” (`S071.txt:241-242`).
3. The 7/14-day ceiling as an upstream-maintainer rule. It caps postponement of a fix's publication, runs from the release-process start rather than the report date, and admits one valid reason. It is the maintainer's own ceiling, not a researcher deadline.

## Limits

- One project's rule: the Linux kernel security team's page. It is not law, not a general coordinated-disclosure standard and not guidance for other projects or distributions.
- The pinned capture was fetched 2026-10-28T20:52:44Z (`corpus/source-snapshots/round-45/manifest.json`). The assignment labels the page as versioned 7.3.0 at capture, but the capture carries no version string (no `7.3` match in `S071.txt`). This entry does not rely on that label.
- Quote checks are exact-text checks against the pinned capture, not a current online check. Re-open the live page before relying on the 7- and 14-day figures.
- Documentation only. The entry instructs no contact with the kernel security team, no submission and no probing of any kernel or system.

## Falsifiable package rule

When a package states the publication deferral for a kernel security fix, check it against S071 in this order. (1) The start date must be the release-process start, after a robust fix exists, not the report date (`S071.txt:305`; `S071.txt:342-344`). (2) The deferral must be at most 7 calendar days from that start (`S071.txt:310-311`). (3) A longer deferral, up to 14 days, needs the agreement the page names (`S071.txt:312`). A package that records a 21-day kernel embargo with no other source is unsupported by S071.

## Rejected over-generalizations

- Rejected claim: every Linux kernel report gets a 7-day embargo. S071 describes a postponement that may be requested by the reporter or an affected party, and caps it: “this may be postponed at the request of the reporter or an affected party” (`S071.txt:309-310`). It is a ceiling on requested postponement, not a default embargo for every report.
- Rejected claim: an AI-assisted finding may go only to the security list. S071 says to avoid a public list at this stage unless the issue is public or trivial to discover, and names “or use of AI-based tools” (`S071.txt:117`) as one such case. The page therefore does not route AI-assisted findings only to the security list.
- Rejected claim: the kernel security team coordinates disclosure with distributions. S071 says the security team “solely focuses on getting bugs fixed” (`S071.txt:332`) and attributes distro and vendor coordination to other groups (`S071.txt:333-334`).
