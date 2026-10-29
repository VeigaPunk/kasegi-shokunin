VERDICT: INFO

Seat R46bRevEntrySrc — pre-draft attack on the F29 ground (row S074, maintainer-side
GitHub repository security advisories). I read the full 42-line capture
(`corpus/source-snapshots/round-46-a2/S074.txt`, sha256 pinned in the manifest and in
`corpus/instruments/r46-f29-gate.py` PINS) and inventoried every claim a drafter of
`corpus/knowledge/github-repository-security-advisories.md` will be tempted to make that
this page does NOT support (M46-3 class). Below, each finding names the exact overclaim
wording to avoid, then what the page actually says, located.

Evidence commands I ran (all against the frozen snapshot):

    $ wc -l corpus/source-snapshots/round-46-a2/S074.txt
    42 corpus/source-snapshots/round-46-a2/S074.txt

    $ grep -n -i -E "\bAI\b|artificial intelligence|AI-assist|copilot" corpus/source-snapshots/round-46-a2/S074.txt; echo rc=$?
    rc=1

    $ grep -n -i -E "kernel|embargo|90-day|90 day" corpus/source-snapshots/round-46-a2/S074.txt; echo rc=$?
    rc=1

    $ grep -n -o -E "[0-9]+" corpus/source-snapshots/round-46-a2/S074.txt | sort -t: -k2 -n | uniq -c -f1
    2 25:72

    $ grep -n -E "72" corpus/source-snapshots/round-46-a2/S074.txt | cut -c1-120
    25:When you create a security advisory for a public repository on GitHub, you have the option of providing an existing C
    36:GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security

    $ grep -n -i -E "private repo|internal|all repositories|guarantee|always|must|required|automatic" corpus/source-snapshots/round-46-a2/S074.txt; echo rc=$?
    rc=1

Findings follow, grouped by the four M46-3 classes named in my brief.

## A. 'advisory' vs 'Advisory Database' conflations

F1. Overclaim to avoid: "Anyone can edit / submit changes to a repository security
    advisory." The page's editability sentence is about the Database, not the
    repository advisory. Page says (line 19): "Anyone can submit a change to an
    advisory published in the GitHub Advisory Database." The in-repository advisory is
    edited only under the maintainer doc's "you can edit the security advisory"
    (line 34, pointing to "Editing a repository security advisory"). Keep the two
    editable surfaces distinct.

F2. Overclaim to avoid: "Every published repository advisory appears in the GitHub
    Advisory Database." Page says (line 19): "If you created a security advisory in
    your repository, the security advisory will stay in your repository. We publish
    security advisories for any of the ecosystems supported by the dependency graph to
    the GitHub Advisory Database on github.com/advisories." — Database publication is
    conditioned on dependency-graph ecosystem support, and per line 36 it happens only
    after "GitHub will review each published security advisory, add it to the GitHub
    Advisory Database". The repository copy remains.

F3. Overclaim to avoid: "Publishing an advisory triggers Dependabot alerts to affected
    repositories" / "alerts are guaranteed". Page says (line 36): "may use the security
    advisory to send Dependabot alerts to affected repositories" — permissive "may",
    plus a fork carve-out: "If the security advisory comes from a fork, we'll only send
    an alert if the fork owns a package, published under a unique name, on a public
    package registry."

F4. Overclaim to avoid: "npm security advisories mirror GitHub repository advisories"
    (or "the npm list is canonical"). Page says (line 20): "If a security advisory is
    specifically for npm, we also publish the advisory to the npm security
    advisories." — npm-only, conditional.

F5. Overclaim to avoid: "A repository security advisory IS a CVE record / the form
    makes it a CVE." Page says (line 23): "The security advisory form on GitHub is a
    standardized form that matches the CVE description format." — form-shape match
    only. Also keep the three names apart: "GitHub Security Advisories" (line 23),
    "repository security advisories" (lines 3, 10), and the "GitHub Advisory Database"
    (lines 19, 36) are distinct things on this page.

## B. Deadlines the page does not give

F6. Overclaim to avoid: "GitHub reviews/answers vulnerability reports within 72
    hours." The page has exactly two 72-hour statements and neither is a report
    response time. Line 25: "GitHub usually reviews the request within 72 hours" —
    that is review of a CVE *request*, hedged with "usually", and review is not
    assignment ("If your security advisory is eligible for a CVE, GitHub will reserve
    a CVE identification number", line 25). Line 36: "This process can take up to 72
    hours" — that is the published-advisory review + Database addition + Dependabot
    process; "can take up to" is a ceiling, and "GitHub may contact you for more
    information." Do not merge the two into a single "GitHub's 72-hour SLA".

F7. Overclaim to avoid: "CVE details publish at the same time as the advisory." Page
    says (line 25): "We'll then publish the CVE details after you make your security
    advisory public." Line 27 adds a second step with no time given: "Once you've
    published the security advisory and GitHub has assigned a CVE identification
    number to the vulnerability, GitHub publishes the CVE to the MITRE database." No
    duration is stated for either step.

F8. Overclaim to avoid: "Maintainers must fix the vulnerability before publishing" /
    "the page mandates an embargo". Lines 39-42 list three postures and mandate none:
    "If a fix version is: Imminently available, and you are able to, wait to disclose
    the issue when the fix is ready. In development but not yet available, mention
    this in the advisory, and edit the advisory later, after publication. Not planned,
    be clear about it in the advisory..." There is no deadline, embargo, or minimum
    fix time anywhere on the page.

F9. Counts the page does not print: the only numeral in the capture is "72", twice
    (lines 25 and 36) — command output above. Any other number in a draft — ecosystem
    count, embargo days, severity/CVSS scores, collaborator limits, dates, "N hours
    total" — is unsourced by S074. Note also my sweep printed nothing (exit 1) for
    "guarantee|always|must|required|automatic": the page's modality is "can", "may",
    "usually", "whenever possible".

## C. Contrasts with the kernel / GitHub reporter pages the page does not state

F10. Overclaim to avoid: "GitHub automatically adds the reporter as a collaborator
     and credited user on the advisory." That is reporter-page (S073) content — see
     `corpus/knowledge/github-private-vulnerability-reporting.md` quoting
     "GitHub automatically adds the reporter of the vulnerability as a collaborator
     and as a credited user on the proposed advisory." (`S073.txt:577`). S074 states
     only: "You can give credit to individuals who contributed to a security
     advisory." (line 17, a maintainer action) and credits become visible only when
     "the credited users have accepted" (line 31). Nothing on S074 is automatic
     (sweep, exit 1).

F11. Overclaim to avoid: "Only the maintainer can merge changes from the temporary
     private fork." Also S073 content (per the sibling entry: `S073.txt:578` "only
     the repository maintainer can merge changes from that private fork into the
     parent repository"). S074 says only: "Privately collaborate to fix the
     vulnerability in a temporary private fork." (line 13) — no merge rule, no
     permission statement, and no statement of who can be invited to the fork.

F12. Overclaim to avoid: "Unlike the kernel process, GitHub keeps AI-assisted
     findings private (or public) inside advisories." S074 contains no AI mention at
     all (sweep for `\bAI\b|artificial intelligence|AI-assist|copilot`, exit 1; the
     kernel AI rule lives in the F27 kernel entry per the S073 entry's Overlap
     section). A draft may record "the page states no AI-handling rule"; it may not
     imply S074 takes any position.

F13. Overclaim to avoid: "Maintainers must enable repository security advisories" /
     "the feature must be turned on per-repository" (importing the private
     vulnerability reporting enablement precondition). S074 states only: "Repository
     security advisories and private vulnerability reporting are available for public
     repositories on GitHub.com" (line 6) — no enablement step is described on this
     page. PVR enablement is S073's fact, not S074's.

F14. Overclaim to avoid: any framing that the page covers the reporter's experience,
     submission form fields, or maintainer response obligations. Line 9 is the only
     reporter-side sentence and it is generic background ("when someone lets a
     maintainer know privately about a security vulnerability, the maintainer develops
     a fix, validates it, and notifies the users"), with "Coordinated disclosure of
     security vulnerabilities" as link text only. The actionable flow on this page is
     maintainer-side: draft (line 12), fork (line 13), publish (line 14).

## D. Capability / lifecycle overclaims

F15. Overclaim to avoid: "Available for all repositories, including private ones."
     Page says: "your public repository" (line 3), "available for public repositories
     on GitHub.com" (line 6), "maintainers of public repositories" (line 10). Sweep
     for "private repo|internal|all repositories" printed nothing (exit 1).

F16. Overclaim to avoid: "A CVE is required to create or publish an advisory." Page
     says (line 25): "you have the option of providing an existing CVE identification
     number"; requesting one "doesn't make your security advisory public"; assignment
     is conditional on eligibility. Nothing makes a CVE mandatory.

F17. Overclaim to avoid: "Any collaborator can request a CVE." Page says (line 25):
     "Anyone with admin permissions to a security advisory can request a CVE
     identification number."

F18. Overclaim to avoid: "GitHub assigns CVEs for any project on GitHub." Page says
     (line 24) "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign
     CVE identification numbers", but (line 26) "GitHub cannot assign CVEs to your
     project if it is covered by another CNA." The CNA authority is scoped.

F19. Overclaim to avoid: "The REST API can create, list, update, and delete
     advisories" (or "GraphQL"). Page says (line 16): "use the REST API to create,
     list, and update repository security advisories." Three verbs only.

F20. Overclaim to avoid: "Advisories can be imported / synced from another source."
     Page says (line 15): "republish the details of a security vulnerability that you
     have already disclosed elsewhere by copying and pasting the details ... into a
     new security advisory." Manual copy-paste, not import.

F21. Overclaim to avoid: "A security policy is required for / part of the advisory
     lifecycle." Page says (line 18): "You can create a security policy to give people
     instructions for reporting security vulnerabilities in your project." Optional
     and separate.

F22. Overclaim to avoid: "On publication the full discussion thread becomes public."
     Page says (lines 31-32): "Anyone can see the current version of the advisory
     data, as well as any advisory credits that the credited users have accepted.
     Collaborators can view the conversation history of the advisory." Conversation
     history is collaborators-only; the public sees current data plus accepted
     credits.

F23. Overclaim to avoid: "Editing a published advisory changes its URL." Page says
     (line 33): "The URL of a security advisory does not change after publication."

F24. Overclaim to avoid: "A fix version is required before publishing" (and its
     mirror, "no fix version means Dependabot stays silent"). Page says (line 38):
     "Whenever possible, you should add a fix version to a security advisory prior to
     publishing the advisory. If you don't, the advisory will be published without a
     fixed version, and Dependabot will alert your users about the issue, without
     offering any safe version to update to." A recommendation with a stated
     consequence; publishing without one is possible, and Dependabot still alerts.

F25. Overclaim to avoid: asserting draft-stage visibility rules ("collaborators can
     see drafts", "the reporter can see the draft"). The page states no pre-
     publication visibility rules at all; it says only that maintainers "privately
     discuss" (lines 3, 10) and then specifies post-publication levels (lines 30-32).
     Keep anything about draft visibility unrecorded.

## Do-nothing control

A drafter writing from the feature title plus the sibling entries alone would import
the reporter-page facts (auto collaborator/credit at S073.txt:577, maintainer-only
fork merge at S073.txt:578), the PVR enablement precondition, the kernel AI-handling
contrast, and generic embargo/SLA numbers — none of which are on S074 (sweeps above,
exit 1). That set of imported claims is exactly F6, F8-F13; this inventory exists only
because I read all 42 lines and ran the sweeps, so the control (no read) produces a
materially different, contaminated draft.

## Limitations

- Scope: I attacked S074 only (plus `manifest.json`, the f29 gate's pin/core lists,
  and the header/cross-references of `corpus/knowledge/github-private-vulnerability-reporting.md`
  to name the contrast temptations F10-F13). I did not re-verify S073 or the F27 kernel
  page content beyond what that sibling entry quotes.
- "The page does not state X" is keyword-proven only for the swept terms (AI, kernel,
  embargo, 90-day, CVSS, severity, reward, bounty, guarantee/always/must/required/
  automatic, and the digit census). Absence of any claim not covered by a sweep term
  rests on a full manual read of the 42 lines, not on an exhaustive phrase sweep.
- I did not run `r46-f29-gate.py` (no entry exists yet; it would fail H2 by design at
  this pre-draft stage) and made no edits outside this Report file. No scratch
  directory was created, so there is nothing to remove. No tools were installed.
