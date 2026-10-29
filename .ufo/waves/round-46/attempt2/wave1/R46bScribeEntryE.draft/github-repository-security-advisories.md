# GitHub repository security advisories: the maintainer-side advisory lifecycle

source: S074 — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — section anchors: About repository security advisories (S074.txt:8-14), CVE identification numbers (S074.txt:22-27), Publication of security advisories (S074.txt:28-34), Importance of fix versions (S074.txt:37-42); text capture at `corpus/source-snapshots/round-46-a2/S074.txt`.
verified-at: 2026-10-29
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d

## Scope and decision rule

This entry records the maintainer side of one GitHub Docs overview page: what a repository maintainer may do with a security advisory from the private draft through publication, and what the platform says about CVE numbers, credit and fix versions. The page frames the feature as “You can use repository security advisories to privately discuss, fix, and publish information about security vulnerabilities in your public repository.” (`S074.txt:3`) and names the actor: “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S074.txt:10`)

Decision rule: a package may describe a maintainer's advisory step as GitHub-conformant only when the draft advisory exists before any publication, the CVE identification number is requested from GitHub while the advisory is still private, and a fix version is attached before publication. The page states the three obligations separately: the draft is the private workspace (“Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.” (`S074.txt:12`)), the fix is developed privately (“Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`)), and publication follows the patch (“Publish the security advisory to alert your community of the vulnerability once a patch is released.” (`S074.txt:14`)). Where another CNA covers the project, no GitHub-assigned identifier may be claimed.

| id | observed question | ground |
|---|---|---|
| G1 | What may maintainers do privately? | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S074.txt:10`) |
| G2 | Where is the fix developed? | “Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`) |
| G3 | Who may be credited? | “You can give credit to individuals who contributed to a security advisory.” (`S074.txt:17`) |
| G4 | Who assigns the CVE number? | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S074.txt:24`) |
| G5 | How long does a CVE request take? | “GitHub usually reviews the request within 72 hours.” (`S074.txt:25`) |
| G6 | Does the CVE request publish the advisory? | “Requesting a CVE identification number doesn't make your security advisory public.” (`S074.txt:25`) |
| G7 | What if another CNA covers the project? | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” (`S074.txt:26`) |
| G8 | Who sees the advisory after publication? | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” (`S074.txt:31`) |
| G9 | What must accompany publication? | “you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`) |

## Overlap and novelty

Contrast with the reporter-side flow held at corpus/knowledge/github-private-vulnerability-reporting.md:9-13: that entry's actor is the person reporting, its decision rule is gated on repository enablement, and its stage is intake and submission. This entry's actor is the repository maintainer and its stage is private drafting, forking, CVE request and publication. The contrast is of coverage, not of policy: neither page states the other's half of the flow, so neither absorbs the other. The reporter-side entry also states its own novelty at corpus/knowledge/github-private-vulnerability-reporting.md:35 as the reporter-side required-field list, the submission effects (including the maintainer-only merge from the temporary fork) and the enablement precondition; that fork row is a reporter-side effect, and no maintainer-side draft advisory, private-fork collaboration, credit or publication duty appears there.

Contrast with the CVE Program rule set held at corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13, which is program assignment scope: what a CNA may decide, under which scope definition, and how identifiers are counted. This entry holds the platform's per-advisory request route instead: a maintainer asks GitHub, in its capacity as CNA, for the identifier of one advisory while that advisory is still private. The two scopes meet only at the routing rule recorded at corpus/knowledge/cna-assignment-and-vulnerability-rules.md:36, which is the Program's first-opportunity duty; this entry records the platform mechanics of one request and the other-CNA boundary, not a program rule.

What is new here: the maintainer-side lifecycle of a GitHub repository security advisory as one ordered sequence — draft before publish, request the CVE while private, credit, publish with a fix version — together with the visibility levels after publication and the platform's own 72-hour review clock. No held entry records that sequence.

## Limits

This entry holds one overview page only. The sibling pages the capture names but does not hold are the form-field list (“The security advisory form on GitHub is a standardized form that matches the CVE description format.” (`S074.txt:23`); the fields themselves live on the sibling page “Creating a repository security advisory” (`S074.txt:17`)), the editing flow (“If you need to update or correct information in a security advisory that you've published, you can edit the security advisory.” (`S074.txt:34`)), the REST API (“You can also use the REST API to create, list, and update repository security advisories.” (`S074.txt:16`)) and the Advisory Database edit flow (“Anyone can submit a change to an advisory published in the GitHub Advisory Database.” (`S074.txt:19`)).

Sweep over the whole capture for material this overview does not hold: `grep -n -i -E 'reward|bount|embargo|safe harbor|deadline|timeline' corpus/source-snapshots/round-46-a2/S074.txt` printed nothing (grep exit 1). The page names no reporter-side route, no reward, no embargo and no response deadline other than the CVE review clock at `S074.txt:25`.

Quote checks are exact-text checks against the pinned capture, not a live check; the `recheck:` line re-verifies the capture's sha256 and the nine quotes pinned in the manifest (Q1-Q9 at `S074.txt:10`, `13`, `17`, `24`, `25`, `25`, `26`, `31`, `38`). Documentation only: this entry instructs no submission, no contact with any maintainer and no probing of any repository.

## Falsifiable package rule

A package advisory step is GitHub-conformant only if the package records all three: a private draft advisory in which the fix is developed (`S074.txt:12`, `S074.txt:13`), a CVE identification number requested from GitHub while the advisory is still private (`S074.txt:25`), and a fix version recorded before publication (`S074.txt:38`). A package that names a GitHub-assigned CVE for a project covered by another CNA fails this rule (`S074.txt:26`); a package that publishes without a fix version fails it (`S074.txt:38`); a package that treats the CVE request as publication fails it (`S074.txt:25`). A reviewer who checks only the presence of the words CVE and publish has not shown conformance.
