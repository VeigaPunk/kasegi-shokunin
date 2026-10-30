<!--
# GitHub repository security advisories: the maintainer-side advisory lifecycle

source: S076 — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — Repository security advisories; About repository security advisories; CVE identification numbers; Publication of security advisories; Dependabot alerts for published security advisories; Importance of fix versions; prose at corpus/source-snapshots/round-47/S076.txt lines 558-600 (sha256 9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38)
verified-at: 2026-10-29
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S076 # 90d

## Scope and decision rule

This entry records one maintainer-side lifecycle: the route a project's maintainers take inside GitHub from a
privately known vulnerability to a published advisory their community can act on. The source is a single GitHub
Docs overview page; its prose spans S076.txt:558-600 inside a capture that also carries page chrome (nav, “Copy markdown” (`S076.txt:559`), TOC and footer lines such as S076.txt:556, S076.txt:559 and S076.txt:601-610). The page states its own
three-phase summary in one sentence: “You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.” (`S076.txt:558`)
The page bounds the feature to public repositories: “Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com” (`S076.txt:561`)
The maintainer-side definition is explicit: “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S076.txt:568`)

Decision rule for a maintainer's package advisory step (the page states the CVE request before the fix-version material, so the numbering below is this entry's, not the page's order):

1. Draft before publish. “Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.” (`S076.txt:570`) The draft is where the private discussion happens, so no advisory detail may be public before that draft is published.
2. Fix in the temporary private fork before publish. “Privately collaborate to fix the vulnerability in a temporary private fork.” (`S076.txt:571`)
3. Fix version before publish. “Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory.” (`S076.txt:596`)
4. CVE request while private. “Requesting a CVE identification number doesn't make your security advisory public.” (`S076.txt:583`) The request is made against the still-private advisory, and the assigning body on this route is GitHub itself: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S076.txt:582`) The request runs on its own service clock: “GitHub usually reviews the request within 72 hours.” (`S076.txt:583`)

Two different 72-hour statements appear in the capture and must not be merged into one deadline: the CVE-request
review clock above, and the post-publication Dependabot step “This process can take up to 72 hours and GitHub may contact you for more information.” (`S076.txt:594`)

| id | observed question | ground |
|---|---|---|
| G1 | What are repository security advisories for? | “You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.” (`S076.txt:558`) |
| G2 | Which repositories may use the feature? | “Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com” (`S076.txt:561`) |
| G3 | Who may privately discuss and fix the vulnerability? | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S076.txt:568`) |
| G4 | What is the first artefact the maintainer creates? | “Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.” (`S076.txt:570`) |
| G5 | Where is the fix developed before publication? | “Privately collaborate to fix the vulnerability in a temporary private fork.” (`S076.txt:571`) |
| G6 | When may the advisory be published? | “Publish the security advisory to alert your community of the vulnerability once a patch is released.” (`S076.txt:572`) |
| G7 | May an already disclosed finding be re-advertised here? | “You can also use repository security advisories to republish the details of a security vulnerability that you have already disclosed elsewhere” (`S076.txt:573`) |
| G8 | Who may be credited on the advisory? | “You can give credit to individuals who contributed to a security advisory.” (`S076.txt:575`) |
| G9 | Where does a repository-scoped advisory live afterwards? | “If you created a security advisory in your repository, the security advisory will stay in your repository.” (`S076.txt:577`) |
| G10 | Which database receives published advisories? | “We publish security advisories for any of the ecosystems supported by the dependency graph to the GitHub Advisory Database on github.com/advisories.” (`S076.txt:577`) |
| G11 | Does an npm advisory also reach the npm advisory list? | “If a security advisory is specifically for npm, we also publish the advisory to the npm security advisories.” (`S076.txt:578`) |
| G12 | Which body assigns CVE identification numbers on this route? | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S076.txt:582`) |
| G13 | What is the clock on a CVE request? | “GitHub usually reviews the request within 72 hours.” (`S076.txt:583`) |
| G14 | Does the CVE request publish the advisory? | “Requesting a CVE identification number doesn't make your security advisory public.” (`S076.txt:583`) |
| G15 | When is GitHub unable to assign the identifier? | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” (`S076.txt:584`) |
| G16 | What is public once the advisory is published? | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” (`S076.txt:589`) |
| G17 | Who may read the advisory conversation? | “Collaborators can view the conversation history of the advisory.” (`S076.txt:590`) |
| G18 | What runs after publication, and on whose clock? | “This process can take up to 72 hours and GitHub may contact you for more information.” (`S076.txt:594`) |
| G19 | What must the advisory carry at publication? | “you should add a fix version to a security advisory prior to publishing the advisory” (`S076.txt:596`) |

## Overlap and novelty

Contrast with F28, the reporter-side twin of the same object. F28 records the route a person takes into a
repository's maintainers: corpus/knowledge/github-private-vulnerability-reporting.md:9 states that the reporter-side
flow is a route for a person who wants to report a security vulnerability privately to a repository's maintainers.
This entry's actor is the other side of the same object, the maintainer who owns the advisory, and its lifecycle
stage is the later one, running from the draft through publication, where F28's stage ends at the submitted report.
F28's own limits already record that its page does not state the maintainer-side flow, the CVE request or any
timeline: corpus/knowledge/github-private-vulnerability-reporting.md:39-40. The two entries are therefore a contrast
of coverage, not a conflict of policy: F28 holds the intake, this entry holds the advisory lifecycle, and neither
holds the other's stage. F28 further records the reporter page's own merge boundary, that only the repository
maintainer can merge from the temporary private fork into the parent repository
(corpus/knowledge/github-private-vulnerability-reporting.md:23); the maintainer's side of that same private fork is
the ground this entry holds at S076.txt:571.

Contrast with F07, the CVE Program's rules for numbering authorities. F07 holds the program's assignment scope:
corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13 holds that a local review separates technical
vulnerability determination, CNA assignment scope and identifier counting, and
corpus/knowledge/cna-assignment-and-vulnerability-rules.md:32 holds that a CNA must develop, document and operate
within a scope definition. That is authority-level scope, the question of who may assign at all. This entry holds
the platform's per-advisory request mechanics instead: GitHub assigns an identifier for one advisory on the
maintainer's request while that advisory is still private, on its own review clock, and it declines the assignment
when the project is covered by another numbering authority. F07's first-opportunity rule for the CNA with the most
appropriate scope is at corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36; the platform's own boundary
is at S076.txt:584. The contrast is again of coverage: F07 governs the assigner's authority, this entry governs the
request record, and the 72-hour review clock at S076.txt:583 is GitHub's service clock, not a CVE Program rule.

Third contrast, on clocks. corpus/knowledge/coordinated-disclosure-timelines.md:7-8 holds that a disclosure
timeline must name the policy or coordinator, the event that starts its clock, the stated interval and the
patch/publication relationship, and that one interval must not be presented as a universal deadline. The two
72-hour statements here are service clocks on GitHub's own machinery, the CVE request review at S076.txt:583 and
the Dependabot step at S076.txt:594; neither is a disclosure deadline, and neither starts a clock at publication.

What is new here: the maintainer-side lifecycle of a repository security advisory as one ordered rule (draft,
private fork, fix version, CVE request while private, credit, publication visibility, Advisory Database and npm
fan-out), the two separate 72-hour clocks, the other-CNA boundary at S076.txt:584, the credit rule at S076.txt:575,
and the publication-visibility split between public advisory data and collaborator-only conversation history. No
held entry records these.

## Limits

- One page, one actor. The prose is S076.txt:558-600; the capture also carries page chrome (S076.txt:556, S076.txt:559, S076.txt:562-566, S076.txt:601-610); it is GitHub's concept
  overview of the maintainer-side advisory lifecycle, not the operating manual and not a rule for other platforms.
- Four sibling pages are named by the capture but their bodies are not held here: the advisory form's fields and the
  creation flow (“Creating a repository security advisory” (`S076.txt:575`)), the REST API endpoints (“REST API
  endpoints for repository security advisories” (`S076.txt:574`)), the post-publication editing flow (“Editing a
  repository security advisory” (`S076.txt:592`)) and the Advisory Database's own edit flow (“Editing security
  advisories in the GitHub Advisory Database” (`S076.txt:577`)). Each appears in the capture as link text only.
- The form's field list is not on this page. The page says only that “The security advisory form on GitHub is a
  standardized form that matches the CVE description format.” (`S076.txt:581`) — it states the form's shape, not its
  fields, and the fields live on the sibling page named above.
- The API surface is not on this page either: “You can also use the REST API to create, list, and update repository
  security advisories.” (`S076.txt:574`) is a pointer to the endpoint list, not the endpoints.
- The page is silent where a package would want more. Sweep over the capture for disclosure-timing and reward
  vocabulary: `grep -n -i -E 'timeline|embargo|deadline|reward|bount' corpus/source-snapshots/round-47/S076.txt`
  printed nothing (grep exit 1). The page states no disclosure deadline, no embargo and no reward. It says nothing
  about private repositories, nothing about GitHub Enterprise, and nothing about who may request a CVE beyond
  administrators of an advisory (S076.txt:583).
- Publication visibility is only what the page lists: the advisory data and accepted credits are public, the
  conversation history is visible to collaborators, and the advisory URL does not change (“The URL of a security
  advisory does not change after publication.” (`S076.txt:591`)). The page states no retention period, no unpublish
  path and no takedown rule.
- The fix-version duty is graded, not absolute: “Whenever possible, you should add a fix version to a security
  advisory prior to publishing the advisory.” (`S076.txt:596`). Of the three cases that follow, only two —
  S076.txt:599 and S076.txt:600 — let a maintainer publish without a fix version; the first case (“Imminently available, and you are able to, wait to disclose the issue when the fix is ready.” (`S076.txt:598`)) forbids it. A package may record the duty and the two cases; it
  may not record that a fix version is mandatory.
- The page records no acceptance test and no review checklist; a package cannot lift one from this capture.
- Quote checks are exact-text checks against the pinned capture, not a live check. The `recheck:` line re-verifies
  the capture's sha256 and the twelve quotes pinned in the manifest (Q1-Q12, anchors S076.txt:568, 571, 575, 582, 583, 583,
  584, 589, 596, 598, 599 and 600); nothing here checks GitHub's current page.
- Documentation only. The entry instructs no advisory creation, no CVE request, no contact with GitHub or any
  maintainer, and no probing of any repository.

## Falsifiable package rule

A claim package's advisory step is GitHub-conformant only when all four of the following are recorded against the
target repository, each checked against the page's own line:

1. A draft advisory was created before publication, and the private discussion happened on that draft: “Create a
   draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your
   project.” (`S076.txt:570`) A package that records only a published advisory fails this step.
2. The fix was developed in the temporary private fork: “Privately collaborate to fix the vulnerability in a
   temporary private fork.” (`S076.txt:571`)
3. The CVE identification number was requested from GitHub while the advisory was still private: “Requesting a CVE
   identification number doesn't make your security advisory public.” (`S076.txt:583`) The package must also record
   GitHub as the assigning body on this route, “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign
   CVE identification numbers.” (`S076.txt:582`), and the boundary is COVERAGE by another CNA, not use of another
   authority's identifier — a project covered by its most-appropriate-scope CNA (the F07 rule:
   `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36`) is one “GitHub cannot assign CVEs to your
   project if it is covered by another CNA.” (`S076.txt:584`) applies to, whether or not that CNA has assigned an
   identifier yet. A package that treats the CVE request as the publication event fails on the request-does-not-publish line.
4. A fix version was added before publication: “you should add a fix version to a security advisory prior to
   publishing the advisory” (`S076.txt:596`)

A package that also states what is public after publication must record the split, not just the fact of
publication: “Anyone can see the current version of the advisory data, as well as any advisory credits that the
credited users have accepted.” (`S076.txt:589`) and “Collaborators can view the conversation history of the
advisory.” (`S076.txt:590`)

-->

# Admitted F29 lifecycle

All 42 lines are body **prose**; the whole capture is that **body**.
Follow the lifecycle in the order the page **states** it.
The three cases let a **maintainer** publish without a fix.
