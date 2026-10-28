# Linux kernel security-bugs reporting process

source: S071 — https://docs.kernel.org/process/security-bugs.html — sections: Preparing your report; What qualifies as a security bug; Responsible use of AI to find bugs; Sending the report; Disclosure and embargoed information; Coordination with other groups; capture corpus/source-snapshots/round-45/S071.txt
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d

## Scope and decision rule

This entry records one upstream project's written reporting process: the Linux kernel security team's page on security bugs, captured as S071 (372 lines, sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`). It records what the page says a security-bug report must contain, what it says qualifies as a security bug, how it says AI-assisted findings are handled, and the disclosure ceiling it names. It is one project's process and binds no other project.

Decision rule: before a package is treated as a kernel security-bug submission, check it against the page's intake test. The page says “The following information are absolutely necessary in any security bug report” (`S071.txt:17-18`) and then lists the affected version range, the description, the reproducer and the conditions. Qualification is a separate test: “The security list exists for urgent bugs that grant an attacker a capability they are not supposed to have” (`S071.txt:89-90`). Where the page is unclear, its instruction is “err on the side of reporting privately” (`S071.txt:103-104`), and it adds that reporting ordinary bugs to the security list “does not make them move faster” (`S071.txt:105-106`).

## Observed questions against the kernel text

| observed question | kernel text | package consequence |
|---|---|---|
| Does the report name a version? | “with no version indication, your report will not be processed” (`S071.txt:20-21`) | Record a stable identifier in the package. Without one the page says the report will not be processed, so the package cannot claim a kernel submission. |
| Is a time-dependent label enough? | “A stable identifier such as a commit ID or an exact version is required” (`S071.txt:22-23`) | Replace any time-dependent label (the page's own example is a latest-mainline style label) with a commit ID or exact version before stating the affected range. |
| Is a distro kernel version enough? | “Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers and will not be processed” (`S071.txt:23-25`) | Record a kernel.org identifier. A distro version string does not satisfy this intake rule, and the package should say so rather than substitute it. |
| Was the bug checked on recent code? | “it is extremely important that vulnerabilities are verified on recent versions” (`S071.txt:26-27`) and “at least by verifying that the code has not changed since the version where it was detected” (`S071.txt:28-29`) | The package must show the code is unchanged since the detected version, or record that the check was not made. |
| Can the reproducer be a compiled binary? | “Binary-only executables are not accepted” (`S071.txt:39-40`); the accepted forms are “source code, shell script, sequence of instructions, file-system image etc” (`S071.txt:38-39`) | The reproducer must be in one of the listed forms. A binary-only artefact leaves the reproducer field unmet. |
| Is an issue that does not reproduce a security bug? | “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug” (`S071.txt:41-43`) | An unreproduced item is not a security-bug submission under this page. Keep it as a hypothesis with its status stated. |
| Does AI assistance change the disclosure treatment? | “If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`) | Mark the package as AI-assisted and record the public-treatment decision. The page's reason is that such bugs “systematically surface simultaneously across multiple researchers” (`S071.txt:97-98`). |
| Where may the reproducer go? | “do not publicly share a reproducer, as this could cause unintended harm” (`S071.txt:99`) and “the reproducer should only be shared upon maintainers' request” (`S071.txt:210-211`) | Hold the reproducer. The public text may say only that one is available; the page says maintainers “might ask for it privately” (`S071.txt:100-101`). |
| Is a public list the first stop? | “Do not send it to a public list at this stage” (`S071.txt:113-114`), with the exception “widely available automated vulnerability scanning tool that can be repeated by anyone, or use of AI-based tools” (`S071.txt:116-117`) | Default to the affected maintainers. A public-list step needs a recorded reason from the exception list, and AI use is one listed reason. |
| Who must be copied? | “If there are two or fewer recipients in your message, you must also always Cc: the Linux kernel security team” (`S071.txt:271-273`) | A package addressed to two or fewer maintainers must record the security-team Cc. |
| When may the report go only to the security team? | “it's possible to send your report to the Linux kernel security team only” (`S071.txt:169-170`), the page limiting this to “and only in this case” (`S071.txt:169`) | Only after the maintainer lookup has failed. The package must record that lookup. |
| How long may a fix be deferred? | “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`) | Record the clock start as the release process, which the page says begins once “a robust fix has been developed” (`S071.txt:305`). Do not record the report date as the start. |
| What justifies a deferral? | “The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA and large scale rollouts” (`S071.txt:312-314`) | A deferral reason outside QA and rollout logistics is not one the page allows; the package must flag it as unsupported by S071. |
| Is a CVE needed for intake? | “The security team does not assign CVEs, nor do we require them for reports or fixes” (`S071.txt:362-363`) | A missing CVE is not an intake defect. A CVE comes from the separate kernel CVE team on request. |

## Overlap and novelty

Existing holdings, restated without new claims:

- F02, `corpus/knowledge/coordinated-disclosure-timelines.md`, already holds the rule that a disclosure timeline must name its policy, its clock trigger, its interval and any extension. It records Project Zero's 90-day policy and its 14-day grace extension (S005) and CERT/CC's 45 days (S004). This entry reuses that rule and adds no clock from those sources. The kernel's 14-day figure is a different rule with a different trigger, and the page says so: its clock starts at release-process start, while the linux-distros clock starts at the initial post, “they start from the initial post to the list regardless of the availability of a fix” (`S071.txt:345-346`). Two 14-day figures in different policies must not be merged.
- F04, `corpus/knowledge/ai-assisted-finding-validation.md`, already holds that an AI-originated finding stays a candidate until a reproduction is recorded and a reviewer distinct from the producer confirms it, and that program-level restrictions must be preserved. This entry does not repeat that validation rule. It adds the kernel's own disclosure duty for AI-assisted finds (treat as public) and the report-content duties below.
- F15, `corpus/knowledge/vendor-third-party-finding-coordination.md`, already holds that a multi-party finding must name the party coordinating it. The kernel page gives its security team a receiving and forwarding role: “Your message may equally be forwarded as-is to the relevant maintainers” (`S071.txt:171-172`). That is consistent with F15 and adds no new principle.

What is NEW here, checked against the knowledge base (`grep -ril kernel corpus/knowledge` returns no file before this entry):

1. The kernel's required-fields intake contract: four items the page calls “absolutely necessary” (`S071.txt:17-18`), with the version-range refusal as the first gate (`S071.txt:20-21`).
2. The AI-assisted report duties. The page says an AI assistant MUST prepare a plain-text report containing the four items, “Prepare a plain-text report explaining the problem” (`S071.txt:241`), and start it with a temporary recipients section, “Start the report with a temporary section listing the recipients' addresses” (`S071.txt:246`). It also says reports must be converted to plain text, “always convert your report to plain text without any formatting decorations before sending it” (`S071.txt:195-196`).
3. The 7/14-day ceiling as an upstream maintainer's rule, with its clock start and its single listed deferral reason (`S071.txt:310-314`).

## Limits

- This is one project's process: the Linux kernel security team's page. It is not law, not a general vulnerability-disclosure standard, not guidance for other vendors or coordinators, and not evidence of how quickly the kernel responds in practice.
- The capture carries no version label. A search of `corpus/source-snapshots/round-45/S071.txt` for the string `7.3` returns no line, so this entry cites no version for the page. The fetch time (2026-10-28T20:52:44Z, manifest) and the sha256 pin the text, not a release number.
- The page says “The Linux kernel security team is not a formal body and therefore unable to enter any non-disclosure agreements” (`S071.txt:371-372`). A package must not promise a reporter an NDA on the kernel's behalf.
- The capture is the RST source (`docs.kernel.org/_sources/process/security-bugs.rst.txt`), not the rendered page. Quotations are checked against that text after whitespace and RST markup normalisation.
- No target, system or live reproduction is described or endorsed here. The entry documents the reporting process only.

## Falsifiable package rule

A package that claims to be a kernel security-bug submission must carry these checkable fields: (1) a kernel.org commit ID or exact version; (2) a description with the traces showing the behaviour; (3) a reproducer in the source, script, instruction-sequence or file-system-image form, recorded as run; (4) the triggering conditions. Any package missing (1) or (3) fails the page's intake test, and the rule predicts it will not be processed (`S071.txt:20-21`, `S071.txt:39-40`). If the package records AI assistance, it must also record public treatment and hold the reproducer (`S071.txt:95-96`, `S071.txt:210-211`). Falsifier: a re-capture in which lines 17-21 or 95-96 no longer carry those requirements, or a kernel statement that a version-less report is processed.

## Rejected over-generalisation

Rejected (this is my statement, not the page's): any bug an AI tool helped find is a kernel security bug and goes to the security team privately. S071 contradicts both halves. Its own classification is that “the majority of the bugs reported via the security team are just regular bugs” (`S071.txt:82-83`), so AI assistance does not classify a finding as a security bug; the threat-model test does (`S071.txt:89-93`). And for AI-assisted finds the page says to treat the bug as public, and lists AI use among the reasons a public-list step is allowed (`S071.txt:116-117`). The over-generalisation merges a disclosure-handling duty with a classification rule. Re-open only if the page is recaptured with different text at lines 82-96.
