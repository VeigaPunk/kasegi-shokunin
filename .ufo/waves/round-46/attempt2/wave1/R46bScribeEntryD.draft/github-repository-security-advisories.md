# GitHub repository security advisories: the maintainer-side advisory lifecycle

source: S074 — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — sections: About repository security advisories; CVE identification numbers; Publication of security advisories; Importance of fix versions
verified-at: 2026-10-29
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074 # 90d

## Scope and decision rule

This entry records the maintainer side of one GitHub Docs page: how the maintainers of a public
repository take a security vulnerability from a private draft to a published advisory. The capture
is the whole body of that page (S074.txt:1-42, 42 lines); nothing here is a statement about any
other platform, about coordinated disclosure in general, or about any particular repository.

The page's own summary of the actor and the object is the entry's definition:
“Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S074.txt:10`)

The maintainer's decision rule, as the page states it, has three ordered obligations: draft the
advisory before publishing it; request the CVE identification number while the advisory is still
private; and add a fix version to the advisory before publication. Drafting comes first:
“Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.” (`S074.txt:12`)
The fix is built in a private workspace rather than in the public repository:
“Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`)
Publication is a separate act, taken once a patch exists:
“Publish the security advisory to alert your community of the vulnerability once a patch is released.” (`S074.txt:14`)

| id | observed question | ground |
|---|---|---|
| G1 | What may maintainers do privately with the advisory? | “Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project.” (`S074.txt:10`) |
| G2 | Where is the fix built before publication? | “Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`) |
| G3 | Who assigns the CVE identification number? | “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S074.txt:24`) |
| G4 | How quickly is a CVE request answered? | “GitHub usually reviews the request within 72 hours.” (`S074.txt:25`) |
| G5 | Does the CVE request itself publish the advisory? | “Requesting a CVE identification number doesn't make your security advisory public.” (`S074.txt:25`) |
| G6 | What if another CNA already covers the project? | “GitHub cannot assign CVEs to your project if it is covered by another CNA.” (`S074.txt:26`) |
| G7 | Who may be credited on the advisory? | “You can give credit to individuals who contributed to a security advisory.” (`S074.txt:17`) |
| G8 | What becomes visible once the advisory is published? | “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” (`S074.txt:31`) |
| G9 | What must the advisory carry before it is published? | “you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`) |

The numbering step sits between drafting and publication. GitHub is itself the numbering authority
for these advisories: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S074.txt:24`)
A maintainer asks GitHub rather than self-issuing, and the page gives a clock for that ask:
“GitHub usually reviews the request within 72 hours.” (`S074.txt:25`)
Asking does not disclose, so the ask can be made while the advisory is still a draft:
“Requesting a CVE identification number doesn't make your security advisory public.” (`S074.txt:25`)
The platform states its own limit on that authority, which a package must respect rather than
paper over: “GitHub cannot assign CVEs to your project if it is covered by another CNA.” (`S074.txt:26`)

The page also records who else may be named on the advisory and what a reader sees after
publication. Credit is granted to contributors:
“You can give credit to individuals who contributed to a security advisory.” (`S074.txt:17`)
At publication the advisory data and the accepted credits are public, while the discussion history
stays with collaborators: “Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted.” (`S074.txt:31`)
“Collaborators can view the conversation history of the advisory.” (`S074.txt:32`)

The fix version is the third obligation, and the page ties it to what a user is then told:
“you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`)
Where no fix can be shipped, the page asks for that to be said plainly in the advisory rather
than left open: “Not planned, be clear about it in the advisory so that your users don't contact you to ask when a fix will be made.” (`S074.txt:42`)

## Overlap and novelty

Two entries already in this corpus sit next to this one, and both are contrasts of coverage
rather than conflicts of rule.

The reporter-side twin is held as F28:
corpus/knowledge/github-private-vulnerability-reporting.md:9-13 records the route by which an
outside researcher files a report, its enablement condition and the form fields the reporter
fills in. The actor there is the reporter, and the lifecycle stage is intake: the report is filed
and the reporter becomes a collaborator and a credited user on a proposed advisory
(corpus/knowledge/github-private-vulnerability-reporting.md:22-23). This entry holds the other
half of the same object: the maintainer drafts the advisory, collaborates in a private fork,
requests the identifier, grants credit and publishes, with the fix-version duty attached to
publication. The private fork is the one place the two pages meet — the reporter-side entry
holds the reporter's view of that fork and who may merge from it, this entry holds the
maintainer's own statement of what the fork is for — so the fork is recorded here as the
maintainer's collaboration workspace and not re-derived from the reporter's account.

The CVE-programme rule set is held as F07:
corpus/knowledge/cna-assignment-and-vulnerability-rules.md:9-13 holds the assignment-scope rule
for CNAs at programme level, separating technical vulnerability determination, assignment scope
and identifier counting. This entry does not restate that programme rule and does not apply it.
What is new here is the platform's per-advisory request mechanics: which CNA is asked (GitHub,
for a repository advisory it authored), the review clock on that ask, the fact that the ask is
non-disclosing, and the platform's own stated boundary when the project is already covered by
another CNA. F07 holds the programme's assignment scope; this entry holds one platform's
per-advisory request path and its limits.

## Limits

- The capture is the overview page only: S074.txt:1-42, and the whole capture is page body. The
  advisory form's own field list is not held here; the page only states that a form exists and
  what it is aligned to: “The security advisory form on GitHub is a standardized form that matches the CVE description format.” (`S074.txt:23`)
  The sibling page that carries the fields is named by the capture, not captured by it.
- The editing flow after publication is a sibling page too: “If you need to update or correct information in a security advisory that you've published, you can edit the security advisory.” (`S074.txt:34`)
  The capture names that page; it does not hold the edit steps.
- The REST API surface is named, not held: “You can also use the REST API to create, list, and update repository security advisories.” (`S074.txt:16`)
  The endpoint reference is a sibling page.
- The GitHub Advisory Database's own edit flow is named, not held:
  “Anyone can submit a change to an advisory published in the GitHub Advisory Database.” (`S074.txt:19`)
  The capture states that a change can be submitted; it does not state how.
- The capture is a documentation page, not a live check. The `recheck:` line above verifies the
  pinned capture's sha256 and the quotes pinned in the manifest; it does not verify GitHub's
  current page, and this entry asserts nothing about live behaviour.
- The page is GitHub's. Its statements about GitHub's own role as CNA, its 72-hour review and
  its advisory database are the platform describing itself, which is what this entry records and
  not an independent assessment of the platform's claims.
- This entry states nothing about reporter-side behaviour; that side is held separately as F28
  (corpus/knowledge/github-private-vulnerability-reporting.md:9-13).

## Falsifiable package rule

A package's advisory step is GitHub-conformant only if every clause below holds and each is
checkable against the captured page:

1. The advisory existed as a draft, and the private discussion of impact happened on that draft,
   before anything was published (“Create a draft security advisory, and use the draft to privately discuss the impact of the vulnerability on your project.” (`S074.txt:12`)).
2. The fix was developed out of public view, in a temporary private fork, not in the public
   repository (“Privately collaborate to fix the vulnerability in a temporary private fork.” (`S074.txt:13`)).
3. The CVE identification number was requested from GitHub, which is the numbering authority for
   these advisories (“GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.” (`S074.txt:24`)),
   and the request was made while the advisory was still private
   (“Requesting a CVE identification number doesn't make your security advisory public.” (`S074.txt:25`)).
4. A fix version was recorded in the advisory before publication, or the advisory states plainly
   that no fix is planned (“you should add a fix version to a security advisory prior to publishing the advisory” (`S074.txt:38`)).
5. Where the project is covered by another CNA, the package does not claim that GitHub assigned
   the identifier (“GitHub cannot assign CVEs to your project if it is covered by another CNA.” (`S074.txt:26`)).
6. Publication was a separate, later act taken once a patch existed
   (“Publish the security advisory to alert your community of the vulnerability once a patch is released.” (`S074.txt:14`)).

A package that names a CVE for a repository advisory without recording the request, or that
publishes without recording a fix version or an explicit statement that no fix is planned, fails
the rule. A package that reports a reporter's private report instead of the maintainer's
advisory step is out of this entry's scope and belongs to F28.
