# Linux kernel security-bugs reporting process

source: S071 — https://docs.kernel.org/process/security-bugs.html — sections Preparing your report; What qualifies as a security bug; Responsible use of AI to find bugs; Sending the report; Disclosure and embargoed information; Coordination with other groups; CVE assignment; Non-disclosure agreements; RST capture at `corpus/source-snapshots/round-45/S071.txt`.
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071 # 180d

## Scope and decision rule

This entry records one upstream project's own intake and disclosure rules: the Linux kernel security team's page on reporting security bugs to it. It is not a rule for other kernel lists, distributions or open-source projects, and it is not a general opinion on AI-assisted vulnerability research.

The page treats four items as mandatory: “The following information are absolutely necessary in any security bug report” (`S071.txt:17-18`). Those four are the affected version range, a description of the problem, a reproducer, and the conditions. Its other items (suspected location, proposed fix, mitigations) are described as highly desirable, not required. A package routed to the kernel security list is checked against the mandatory four and against the disclosure-channel duties in the table below before it is described as complete.

| Observed question | Kernel text | Package consequence |
|---|---|---|
| Which fields does intake require? | “The following information are absolutely necessary in any security bug report” (`S071.txt:17-18`) | Carry four mandatory fields: version range, description, reproducer, conditions. A report missing one is incomplete, not triaged. |
| Is a report without a version processed? | “with no version indication, your report will not be processed” (`S071.txt:20-21`) | A blank version field is a rejection condition on the package, not a gap to fill later. |
| Is a time-dependent label a version? | “Note that a time-dependent version such as "latest mainline" is not acceptable.” (`S071.txt:21-22`) | Record a commit ID or an exact version in that field. A label such as "latest" or "current mainline" does not satisfy it. |
| Is a distro-kernel version a version? | “Versions designating kernels not coming from kernel.org (such as distro kernels) are meaningless to maintainers and will not be processed.” (`S071.txt:23-25`) | A distro-kernel string alone does not satisfy the version field; the field needs a stable identifier such as a commit ID or an exact version (`S071.txt:22-23`). |
| Is a binary-only reproducer usable? | “Binary-only executables are not accepted.” (`S071.txt:39-40`) | The reproducer field must hold a form the page lists as an example: source code, shell script, sequence of instructions or file-system image (`S071.txt:37-39`). A binary-only artifact fails the field. |
| Does an unreproduced issue qualify as a security bug? | “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.” (`S071.txt:41-43`) | Record reproduction status. An issue with no reproduction is not classified as a security-bug report on the strength of its description. |
| Are triggering conditions required? | “if the bug depends on certain configuration options” (`S071.txt:45`) | The conditions field lists the configuration options, sysctls, permissions, timing or code modifications the bug depends on. A blank conditions field is a missing mandatory item. |
| Does an AI-assisted finding stay private? | “If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`) | Treat the package as public. Its reproducer does not go to any public channel; public text states only that a reproducer exists and that maintainers may request it. |
| May an AI-assisted reproducer be posted publicly? | “do not publicly share a reproducer, as this could cause unintended harm” (`S071.txt:99`) | The public text carries an availability statement, not the reproducer. |
| How long may a fix be held back before publication? | “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`) | The ceiling is 7 calendar days counted from the start of the release process. The 14-day extension is an exception, not a default. The clock does not start at report receipt. |
| What justifies a deferral? | “The only valid reason for deferring the publication of a fix is to accommodate the logistics of QA and large scale rollouts” (`S071.txt:312-314`) | A deferral note must name QA or rollout logistics. Any other reason is not the page's stated basis for deferral. |

## Overlap and novelty

Three knowledge entries already sit near this page. None of them holds the page's text, and none of them is a substitute for it.

F02 (`knowledge/coordinated-disclosure-timelines.md`) already holds the timeline discipline: name the policy, the trigger, the interval and any documented extension, and do not transplant another coordinator's interval (its Rule, lines 7-17). F02 also holds a 14-day figure, but that figure is Project Zero's grace extension, granted only when the developer commits to ship a fix within it (F02 evidence, line 25, citing S005). It is not the kernel's rule. The kernel's 14 days is an exceptional extension agreed on criticality (`S071.txt:310-311`, `S071.txt:312`).

F04 (`knowledge/ai-assisted-finding-validation.md`) already holds the validation side: an AI-originated finding stays a candidate until a reproducible observation and a reviewer distinct from its producer exist (its Rule, lines 7-8). F27 does not repeat that. The page's AI duties are a disclosure-channel rule and a report-form rule, which F04 does not hold.

F15 (`knowledge/vendor-third-party-finding-coordination.md`, and its corpus/README.md row) already holds the instruction to record which party coordinates a multi-vendor finding. F27 adds the kernel's own ordering rule for a different party: the kernel security team asks reporters not to contact linux-distros until a fix is accepted by the affected code's maintainers (`S071.txt:350`).

What is new here:

1. The kernel's intake contract. The page states mandatory fields and a rejection clause: a report with no version indication “will not be processed” (`S071.txt:21`), and an issue that cannot be reproduced is “not a security bug” by definition (`S071.txt:41-43`). F04's validation record checks and F02's timeline checks are Kasegi's own admission fields. The kernel's contract is an upstream maintainer's rule for accepting a report at all.
2. The AI-assisted report duties. The page says an AI-assisted finding must be treated as public (`S071.txt:95-96`), that its reproducer must not be posted publicly (`S071.txt:99`), and that the AI assistant MUST prepare a plain-text report that contains the four mandatory items (`S071.txt:239-242`). F04 holds no disclosure-channel rule for AI-found bugs.
3. The 7/14-day ceiling as an upstream-maintainer rule. Its trigger is the start of the release process, which begins only after “Once a robust fix has been developed, the release process starts” (`S071.txt:305`). F02's intervals run from other triggers (a report date, or a fix's availability under Project Zero's own policy). The kernel's ceiling is not transplanted from them.

## Limits

This is one project's rule, not law and not general guidance. It states what the Linux kernel security team asks of reporters, and says of other lists that “the respective policies and rules are different since” (`S071.txt:340`). It is not the policy of linux-distros or oss-security.

Version. The round assignment labels this page as version 7.3.0 at capture. The pinned capture does not carry that string: `grep -n "7\.3" corpus/source-snapshots/round-45/S071.txt` prints nothing. This entry therefore records no page version, and it does not rely on one.

Capture form. The manifest records the fetched URL as the RST source (`docs.kernel.org/_sources/process/security-bugs.rst.txt`), while the source line above names the rendered HTML page. The quotes are checked against the RST text, which is what the snapshot holds.

The page points to Documentation files (reporting-issues, threat-model, coding-assistants, submitting-patches, email-clients) that are not captured here. No statement in this entry depends on them.

Documentation only. This entry records published text. It directs no probing, scanning, contact, reporting or testing against any target.

## Falsifiable package rule

**Falsifiable package rule:** a package routed to the kernel security list must carry a version field holding a commit ID or an exact version, not a time-dependent label and not a distro-kernel string; a reproducer in source, script, instruction-sequence or image form, not a binary-only artifact; and a non-blank conditions field. If the finding was AI-assisted, its public text must contain no reproducer. Any embargo the package proposes must name a 7-day ceiling from the start of the release process, and a 14-day extension only with a stated criticality basis. The rule is falsified if a package failing any of these is cited as meeting the page's intake requirement, or if the quoted sentences stop appearing in the pinned capture under the recheck command above.

## Rejected over-generalization

**Rejected over-generalization:** “Every report sent to the kernel security list starts a 7-day clock when it is received.” Rejected because the page places the ceiling's start at the release process, which begins only after a robust fix exists (`S071.txt:305`, `S071.txt:310-311`), and it says the clock runs from the availability of a fix (`S071.txt:343-344`). Re-open only if the page changes its trigger in a later capture.
