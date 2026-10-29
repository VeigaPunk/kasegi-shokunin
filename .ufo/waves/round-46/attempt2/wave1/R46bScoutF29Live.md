VERDICT: HOLDS

# R46bScoutF29Live — S074 re-opened live (kasegi round 46, attempt 2, wave 1)

Scope of this seat: one item only — re-open the S074 source live, record URL/status, measure
drift against the pinned capture, and answer the ten entry questions from the LIVE page.
Nothing in the lane was edited; no git/jj mutation; no tooling installed (no pacman, no uv,
no npx); scratch `/fast/scratch/hyaku/kasegi-r46/R46bScoutF29Live/` removed after this file
was written. All paths below are absolute under `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

---

## F1 — Live fetch: HTTP status, final URL, redirect behaviour

**Attacked:** the source URL named in the card,
`https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`.

Command (scratch, `TMPDIR` set explicitly to the seat scratch):

```
curl -sS -L --max-redirs 10 -D "$S/live.headers" -o "$S/live.html" \
  -w 'status=%{http_code} final_url=%{url_effective} size=%{size_download} num_redirects=%{num_redirects}\n' \
  'https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories'
```

Printed output:

```
status=200 final_url=https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories size=582877 num_redirects=0
```

`wc -c "$S/live.html"` → `582877 /fast/scratch/hyaku/kasegi-r46/R46bScoutF29Live/live.html`

**Live final URL = the canonical `/code-security/concepts/vulnerability-reporting-and-management/…` URL (identical to the manifest's recorded `capture_url`/`final_url`); HTTP status = 200; zero redirects.**

Legacy-URL probes (the card says the URL "redirected from the /security-advisories/… at capture time"):

```
https://docs.github.com/en/security-advisories/repository-security-advisories/about-repository-security-advisories -> code=404 loc=
https://docs.github.com/en/security-advisories/repository-security-advisories -> code=404 loc=
https://docs.github.com/en/code-security/security-advisories/repository-security-advisories/about-repository-security-advisories -> code=301 loc=https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/about-repository-security-advisories -> code=301 loc=https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
```

The exact capture-time legacy slug is not recorded in the manifest (it stores the post-redirect
`final_url` only), so I probed the plausible shapes: two now answer **404**, two answer
**301 → the canonical URL**. The canonical URL itself answers 200 with no redirect hop.

## F2 — Byte/line drift against the pinned capture

**Attacked:** `corpus/source-snapshots/round-46-a2/S074.txt`, pin sha256
`1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`.

`sha256sum corpus/source-snapshots/round-46-a2/S074.txt` →
`1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039` — **the pinned file is
unchanged and matches the pin exactly**; `wc -lc` → `42 7087`.

Raw-page size check against the manifest's recorded fetch: manifest `bytes: 582877`,
live raw HTML `582877` → **the served page is byte-for-byte the same size as at capture time.**

The pinned capture is *not* a raw-HTML dump and *not* the `.md` variant; it is a
reader-style text rendering of the article body (42 lines, `## ` headings, no markdown link
syntax). I therefore compared by locating every pinned line inside the live page, in two
renderings:

Locator (`capture-source.py`'s own `html_to_text` over the live HTML, and the live markdown
`Accept: text/markdown` / `.md` variant — both return the identical 7807-byte markdown,
sha256 `8c2d763a6f7cf3ac0e16e45e850c3a5d157310831edbcc3f58d00f09f638b248`):

```
LIVE_HTML_RENDERED_LINES=610 LIVE_MD_LINES=68 PINNED_LINES=42
[live-rendered] pinned_lines=42 located_in_live=42 not_found=0
[live-markdown] pinned_lines=42 located_in_live=37 not_found=5
  MISS line=1 :: In this article
  MISS line=4 :: Copy markdown
  MISS line=5 :: ## Who can use this feature?
  MISS line=6 :: Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com
  MISS line=7 :: ## In this article
```

**Drift verdict: none in content.** All 42 pinned lines are located in the live page's
rendered body; the 5 lines absent from the *markdown* variant are page chrome / the
"Who can use this feature?" callout, which exist in the live HTML render.

Additions check (live article region vs pinned capture):

```
REGION live_html_lines[557..600] (44 lines)
```

— **no `ONLY_IN_LIVE` line was printed**: every live body line is already represented in the
pinned capture. The live region carries the same 42 body lines (44 rendered lines counting
the two repeated chrome headers).

The lane's own recheck against the pinned snapshot:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
S074:Q2 OK occurrences=1 anchor=13-ok
S074:Q3 OK occurrences=1 anchor=17-ok
S074:Q4 OK occurrences=1 anchor=24-ok
S074:Q5 OK occurrences=1 anchor=25-ok
S074:Q6 OK occurrences=1 anchor=25-ok
S074:Q7 OK occurrences=1 anchor=26-ok
S074:Q8 OK occurrences=1 anchor=31-ok
S074:Q9 OK occurrences=1 anchor=38-ok
recheck_exit=0
```

## F3 — Control: the locator is not a do-nothing check

Same locator, run against a deliberately mutated copy of the live page (`72 hours` →
`72 h0urs`):

```
[mutated-live] pinned_lines=42 located_in_live=40 not_found=2
  MISS line=25 :: When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security v
  MISS line=36 :: GitHub will review each published security advisory, add it to the GitHub Advisory Database, and may use the security advisory to send Dependabot alerts to affe
```

A one-word change to the live page flips the verdict from `not_found=0` to `not_found=2`,
so the `42/42 located` result above is a measurement, not a tautology. The raw byte-count
agreement (582877 = manifest `bytes`) is a second, independent signal.

---

## F4 — The ten entry questions, answered from the LIVE page

Every quote below is verbatim from the live page; the capture line it sits on is given as
`S074.txt:N` (the capture is verified line-identical to the live body above). The live
rendered line numbers are added where they help a locator.

**(1) Who may create a repository security advisory, and on which repository visibility.**
The page scopes the whole feature to public repositories on GitHub.com and names the actor as
the repository's maintainers:

> "Repository security advisories and private vulnerability reporting are available for public repositories on GitHub.com" (`S074.txt:6`)

> "Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project." (`S074.txt:10`)

> "When you create a security advisory for a public repository on GitHub, you have the option of providing an existing CVE identification number for the security vulnerability." (`S074.txt:25`)

The page does not enumerate other creating roles (word counts over the body: `maintainer` 2,
`maintainers` 4, `permissions` 1, `admin` 1) and never mentions GitHub Enterprise / GHES
(`enterprise` 0, `GHES` 0) or private repositories (`private repositor` 0) beyond the
public-repository scoping sentence.

**(2) The temporary private fork, and who may merge it.**
The fork is the private venue in which the fix is developed:

> "Privately collaborate to fix the vulnerability in a temporary private fork." (`S074.txt:13`)

The only other fork statement is about Dependabot alerts, not merge rights:

> "If the security advisory comes from a fork, we'll only send an alert if the fork owns a package, published under a unique name, on a public package registry." (`S074.txt:36`)

**Who can merge it: the page does NOT say.** The word `merge` occurs **0** times in the live
body (and the body names no fork-merge sibling page). The site navigation in the live HTML
lists "Collaborate in a fork", "Add collaborators", "Remove collaborators" — navigation chrome,
not article content; do not quote them as page support.

**(3) GitHub's CNA status and what it authorizes.**

> "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers. For more information, see About CVE and CVE Numbering Authorities on the CVE website." (`S074.txt:24`)

Authorized scope on this page = assigning CVE identification numbers (and publishing the CVE
to MITRE after publication: "GitHub publishes the CVE to the MITRE database.", `S074.txt:27`).

**(4) The CVE request review clock.**

> "GitHub usually reviews the request within 72 hours." (`S074.txt:25`)

**Nuance the entry must not flatten:** the body contains **two** different 72-hour clocks
(`72 hours` count = 2). The second belongs to the post-publication Dependabot-alert process,
not to the CVE request:

> "This process can take up to 72 hours and GitHub may contact you for more information." (`S074.txt:36`)

**(5) Does requesting a CVE publish the advisory? — No.**

> "Requesting a CVE identification number doesn't make your security advisory public." (`S074.txt:25`)

> "We'll then publish the CVE details after you make your security advisory public." (`S074.txt:25`)

> "Anyone with admin permissions to a security advisory can request a CVE identification number." (`S074.txt:25`)

**(6) The other-CNA boundary.**

> "If you already have a CVE you want to use, for example, if you use a CVE Numbering Authority (CNA) other than GitHub, add the CVE to the security advisory form. This may happen, for example, if you want to get the advisory consistent with other communications you plan to send out at publication time. GitHub cannot assign CVEs to your project if it is covered by another CNA." (`S074.txt:26`)

**(7) The credit mechanics.**

> "You can give credit to individuals who contributed to a security advisory. For more information, see Creating a repository security advisory." (`S074.txt:17`)

> "Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted." (`S074.txt:31`)

So the page states two mechanics only: credit is given to contributing individuals, and a
credit becomes publicly visible once the credited user has **accepted** it. How to add a credit
and how acceptance is requested live on the sibling page "Creating a repository security
advisory", whose body the capture does not hold.

**(8) Publication visibility levels.**

> "When you publish a draft advisory from a public repository, visibility levels vary as follows:" (`S074.txt:30`)

> "Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted." (`S074.txt:31`)

> "Collaborators can view the conversation history of the advisory." (`S074.txt:32`)

> "The URL of a security advisory does not change after publication." (`S074.txt:33`)

**(9) The fix-version duty, and what happens without one.**

> "Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, the advisory will be published without a fixed version, and Dependabot will alert your users about the issue, without offering any safe version to update to." (`S074.txt:38`)

The page's three conditional paths: "Imminently available, and you are able to, wait to
disclose the issue when the fix is ready." (`S074.txt:40`) · "In development but not yet
available, mention this in the advisory, and edit the advisory later, after publication."
(`S074.txt:41`) · "Not planned, be clear about it in the advisory so that your users don't
contact you to ask when a fix will be made." (`S074.txt:42`).

**(10) What the page does NOT say, and which sibling pages it names.**
Not said on this page (word counts over the live body): the advisory form's **field list**
(`field` 0, `fields` 0); **who may merge** the temporary private fork (`merge` 0); what may be
edited after publication and by whom; the REST API's endpoint shapes/methods/payloads;
advisory **withdrawal or revocation** (`withdraw` 0, `revoke` 0); retention of an unpublished
advisory; CVE-eligibility criteria beyond "If your security advisory is eligible for a CVE";
GitHub Enterprise / GHES (`enterprise` 0, `GHES` 0). The page says only about the form:

> "The security advisory form on GitHub is a standardized form that matches the CVE description format." (`S074.txt:23`)

Sibling pages named by the body **as link text only** (their bodies are not held here):
"Coordinated disclosure of security vulnerabilities" (`S074.txt:9`) · "REST API endpoints for
repository security advisories" (`S074.txt:16`) · "Creating a repository security advisory"
(`S074.txt:17`) · "Adding a security policy to your repository" (`S074.txt:18`) · "Editing
security advisories in the GitHub Advisory Database" (`S074.txt:19`) · npmjs.com/advisories
(`S074.txt:20`) · GitHub Security Lab (`S074.txt:21`) · "About CVE and CVE Numbering
Authorities" on the CVE website (`S074.txt:24`) · "Editing a repository security advisory"
(`S074.txt:34`) · plus the MITRE database (`S074.txt:27`) and github.com/advisories
(`S074.txt:19`).

---

## F5 — Effect on C2's kill rule

C2's kill rule includes "if the non-author closure re-opening the page cannot locate the
cited quotes". This seat is that closure: it re-opened the page independently of the L1's
capture, and located **42/42** pinned lines including all **9/9** manifest quotes
(`source-recheck.py` exit 0). The live body holds no content the capture lacks, and the
capture holds nothing the live body lacks. **The kill rule does not fire.**

Two substantive cautions for the entry drafters (both page-level, both evidenced above):
(2b) the page never says who may merge the temporary private fork; and (4) the CVE-request
72-hour clock must not be merged with the separate 72-hour Dependabot-alert clock.

---

## Limitations

- **The pinned capture could not be re-derived byte-for-byte.** It is a reader-style text
  rendering of the article body; the lane's `capture-source.py --kind html` over the same
  bytes yields 610 lines (site chrome included) and `--kind text` over the `.md` variant
  yields markdown link syntax and ordered-list markers — neither reproduces the 7087-byte,
  42-line file. My comparison is therefore (a) the raw page byte count, 582877 = manifest
  `bytes`, and (b) line-level location of all 42 pinned lines in the live body plus the
  absence of any live body line missing from the capture. The content-equivalence claim
  rests on that, not on a reproduced snapshot digest.
- **The capture-time legacy URL slug is unknown.** The manifest stores only the post-redirect
  `final_url`; four candidate legacy shapes were probed (two 404, two 301 → canonical). I
  cannot re-verify the "it redirected at capture time" clause byte-for-byte, only that the
  canonical URL today serves 200 with zero redirects.
- The live page can change after this fetch (run on 2026-10-29 during wave 1 of round 46,
  attempt 2); the measurement is a point-in-time reading.
- The five chrome lines missing from the `.md` rendering exist in the live HTML; a future
  verifier using only the `.md` endpoint would see 37/42 and must not call that drift.
- Out of scope and not run by this seat: `r46-mutbat.py`, `r46-f29-gate.py`, the C1/C2
  counters and the integration export checks (L1/wave-2 seats own those).
- No tooling installed or upgraded (nothing via pacman, uv, npx or a release binary); no
  git/jj mutation, no commit, no push; the fleet repo, sibling lanes, `MANIFEST.json`,
  `.ufo/state` and `~/Projects/shokuknow` were not touched; scratch removed on exit.
