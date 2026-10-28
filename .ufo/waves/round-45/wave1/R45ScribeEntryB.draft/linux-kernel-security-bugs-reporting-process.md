# Linux kernel security-bugs reporting process

source: S071 — https://docs.kernel.org/process/security-bugs.html — sections Preparing your report; What qualifies as a security bug; Identifying contacts; Responsible use of AI to find bugs; Disclosure and embargoed information; pinned RST capture `corpus/source-snapshots/round-45/S071.txt`.
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d

## Scope and decision rule

This entry records one upstream project's reporting process: the Linux kernel security team's page, as pinned in S071. It states what a report must contain, which reports the security list is for, how AI-assisted reports are handled, and when publication of a fix may be deferred. It is that project's own rule for reports sent to its security list and maintainers. It is not law, not guidance for other projects, and not authorisation to test any target.

The page's scope test is narrow. The security list is for “urgent bugs that grant an attacker a capability they are not supposed to have on a correctly configured production system” (`S071.txt:89-90`). The page also says most reports it receives do not meet that test: “the majority of the bugs reported via the security team are just regular bugs” (`S071.txt:82-83`). Ordinary bugs go through the normal reporting channels (`S071.txt:85-87`, paraphrased, not quoted).

Decision rule for a package: first confirm the issue crosses the trust boundary the page describes, then check the required items in the table below. A package that fails either check is not supported for the security channel by this entry.

## Observed questions

| observed question | kernel text | package consequence |
|---|---|---|
| Does the report name a version the maintainers can use? | “with no version indication, your report will not be processed” (`S071.txt:20-21`) | A report with no version field is unprocessable under the page. Record the field as missing; do not present the package as submission-ready. |
| Is a time-dependent or distro-kernel label an acceptable version? | “A stable identifier such as a commit ID or an exact version is required” (`S071.txt:22-23`); “Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers” (`S071.txt:23-24`) | Name a commit ID or an exact upstream version. A "latest mainline" label, or a distro kernel string, does not satisfy the field. |
| Has the code been checked against a recent tree? | “it is extremely important that vulnerabilities are verified on recent versions” (`S071.txt:26-27`) | Record a check on a recent tree, or that the code is unchanged since the version where the bug was detected (`S071.txt:27-29`). The detected version alone does not establish currency. |
| Is a binary-only reproducer acceptable? | “Binary-only executables are not accepted.” (`S071.txt:39-40`) | The reproducer must be in a reviewable form the page lists: source code, a shell script, an instruction sequence or a file-system image (`S071.txt:38-39`). A binary alone fails the reproducer field. |
| Does a bug that cannot be reproduced count as a security bug? | “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.” (`S071.txt:41-43`) | Record a non-reproducing candidate as unconfirmed. Do not file it as a security bug or make a severity claim from it. |
| Which items are required, and which are only desirable? | “The following information are absolutely necessary in any security bug report” (`S071.txt:17-18`); “the following information are highly desirable” (`S071.txt:49`) | Required: version range, description, reproducer and conditions (`S071.txt:20`, `31`, `35`, `45`). Desirable only: suspected location, a proposed fix and mitigations (`S071.txt:51`, `57`, `69`). The page attaches no stated consequence to omitting the desirable items; that absence is an observation, not a rule. |
| May an AI-found bug be sent to a public list, and must it be treated as public? | “If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`); “consider the issue as being public or trivial to discover” (`S071.txt:114-115`), whose examples include “or use of AI-based tools” (`S071.txt:116-117`) | Treat the finding as public for channel purposes. The page does not bar a public-list route at first contact for an issue it considers public, so record the channel choice and the reason for it. |
| Is an AI-found bug's reproducer published? | “do not publicly share a reproducer, as this could cause unintended harm” (`S071.txt:99`); “just mention that one is available and maintainers might ask for it privately” (`S071.txt:100`) | Public text says only that a reproducer exists. The reproducer is sent privately if a maintainer asks. |
| How long may a fix's publication be deferred? | “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`) | A deferral record names the trigger (the start of the release process), the 7-day cap, and the 14-day extension only where criticality is agreed (`S071.txt:312`). The page states no other interval. |
| For what reason may publication be deferred? | “only valid reason for deferring the publication of a fix is to accommodate the logistics of QA and large scale rollouts” (`S071.txt:313-314`) | A deferral record names QA or rollout coordination as its reason. Other reasons are not supported by this page. |

## Overlap and novelty

**F02 (`knowledge/coordinated-disclosure-timelines.md`).** F02 already requires any timeline to name its policy, its clock trigger, its interval, the patch/publication relation and any extension (`coordinated-disclosure-timelines.md:7`), and forbids reading one coordinator's interval as the universal deadline (`coordinated-disclosure-timelines.md:8`). The kernel's 7-day cap is recorded under that rule and adds no new general timeline principle. F02 holds CERT/CC's 45-day and Project Zero's 90-day intervals (`coordinated-disclosure-timelines.md:22,24`); neither is a kernel interval, and neither may be transplanted (`coordinated-disclosure-timelines.md:17`).

**F04 (`knowledge/ai-assisted-finding-validation.md`).** F04 already holds that an AI-originated finding stays a candidate until a reproducible observation and a reviewer distinct from the producer exist (`ai-assisted-finding-validation.md:7-8`), and that a model-generated report is not proof of a vulnerability (`ai-assisted-finding-validation.md:34`). The kernel's version-currency and reproducer checks overlap that verification ground (`S071.txt:26-27`, `S071.txt:209`). F04 does not hold the channel rule: its only disclosure line tells the package to preserve “any applicable program restriction or disclosure requirement” (`ai-assisted-finding-validation.md:16`), and it says nothing about treating an AI-found bug as public.

**F15 (`knowledge/vendor-third-party-finding-coordination.md`).** F15 asks which party coordinates a multi-vendor finding and reads no clock or contact into an intake route. The kernel page is an upstream project's own intake, not a vendor programme. Its recipient rule is maintainers first, with the security team as a fallback: “it's possible to send your report to the Linux kernel security team only” (`S071.txt:169-170`), and only when the right maintainers cannot be identified. That is a recipient rule, not a statement of who coordinates; F15's worksheet line applies to it unchanged.

**What is new here.**

1. **The required-items intake contract.** The page lists the fields a report must carry, and states the consequence of omitting one (`S071.txt:17-21`). A project's own mandatory report-field list with a stated rejection consequence is not held by any existing knowledge entry. The only "required field" text in the knowledge set belongs to a CVE record schema and to the RFC 9116 standard, not to a project's intake.
2. **The AI-assisted-report duties.** The page sets a MUST list for the AI assistant: a plain-text report with the four required items, a temporary recipient section, and a reproducer and fix that are tested before sending (`S071.txt:239-241`, `S071.txt:195-196`, `S071.txt:207-209`, `S071.txt:213-218`). F04 covers verification; it does not cover report-format or channel duties.
3. **The 7/14-day cap as an upstream-maintainer rule.** The cap is a ceiling on deferring a fix's publication, measured from the start of the release process (`S071.txt:310`). The page sets this against the linux-distros clock: “for the kernel security team occasional embargoes (as subject to a maximum allowed number of days) start from the availability of a fix” (`S071.txt:342-344`), whereas for linux-distros “they start from the initial post to the list regardless of the availability of a fix” (`S071.txt:345-346`). The two trigger events differ, so a package must record which one applies.

## Limits

- One project's rule: the Linux kernel security team's page, as pinned. It is not law, not a rule for other kernel-adjacent lists, distributions or vendors, and not general guidance.
- The pinned capture is the RST source fetched from `docs.kernel.org/_sources/process/security-bugs.rst.txt` (`corpus/source-snapshots/round-45/manifest.json`, S071), not the rendered HTML at the canonical URL. The recheck confirms the pinned bytes (sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`) and the quoted spans only; it does not confirm the live page still reads the same.
- Version: the pinned capture carries no version label. A search for `7.3` in `S071.txt` returns nothing, so this entry records no page version.
- The page cross-refers to documents not captured here (`threat-model.rst`, `reporting-issues.rst`, `submitting-patches.rst`, `coding-assistants.rst`, the kres repository, `get_maintainer.pl`). This entry does not evaluate them.
- "The start of the release process" is not defined in S071.txt, and this entry does not define it.
- The quotes are curated spans from the pinned capture, not a complete audit of the page.
- Documentation only. This entry directs no probing, testing, scanning or submission against any target.

## Falsifiable package rule

A kernel report package is supported by this entry only if all three checks pass. It fails the rule if any one fails.

- (a) It names a commit ID or an exact upstream version, not a distro label or a time-dependent label (`S071.txt:20-24`).
- (b) It carries the four required items. Any AI-found finding is marked as treated public for channel purposes, and its reproducer is withheld from public text (`S071.txt:95-100`, `S071.txt:114-117`).
- (c) Any deferral of a fix's publication states the trigger as the start of the release process, a cap of 7 calendar days, a 14-day extension only with agreed criticality, and a QA or rollout reason (`S071.txt:309-314`).

Falsifier: a package that records a deferral longer than 14 calendar days, or measures the deferral from the report date instead of the start of the release process, contradicts check (c) and is unsupported by this page.

## Rejected over-generalization

**Rejected:** “Every kernel bug may be embargoed for 7 days from the day it is reported.”

The page's clock starts at “the start of the release process” (`S071.txt:310-311`). The postponement is “at the request of the reporter or an affected party” (`S071.txt:309-310`), the page states a preference for early release (`S071.txt:308-309`), and the 7-day figure caps a postponement. It is not a reporter's deadline and does not run from the report date.

**Rejected:** “An AI-found bug is publicly known, so its fix is released immediately.”

The immediate-release sentence covers “Fixes for publicly known bugs are released immediately” (`S071.txt:305-306`). The AI rule says the finder “must treat it as public” (`S071.txt:95-96`), and the contacts section lists AI-based discovery as an example of issues considered public (`S071.txt:116-117`). Neither sentence says that an AI-found bug is already publicly known, so the immediate-release rule does not follow.

**Rejected:** "The kernel's 7-day figure is the same clock as ISO 29147's 7-day acknowledgement."

The ISO 29147 entry holds a 7-day acknowledgement-of-receipt expectation (`iso-29147-divergence-and-clause-crosswalk.md:48`). It is a different event and a different duty from the kernel's 7-day cap on deferring a fix's publication.
