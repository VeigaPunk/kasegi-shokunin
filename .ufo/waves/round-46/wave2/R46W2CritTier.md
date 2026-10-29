VERDICT: HOLDS

# R46W2CritTier — row S073 tier, scope, dates and redirect (round 46, wave 2)

Seat: Tier critic (leaf, read-only). Tree attacked: commit 5437afeaf9b642c267bba3c31f00ae701e49da68, exported with `git archive ... corpus` into scratch. HEAD is 0d121a2, which differs from 5437afe only by five `.ufo/waves/round-46/wave2*` files (`git diff --stat` printed 5 files, 1241 insertions, no `corpus/` path), so the corpus is identical. No commits, no index changes, no edits to the lane. Scratch removed on exit.

Question: is GitHub Docs `docs.github.com/.../report-privately` tier A under SOURCES contract v1 for the scope "GitHub's own statement of the reporter-side private-reporting flow only"? Answer: **yes**, with the wording and anchor corrections in F5.

## F1 — The tier A rule admits this page kind (HOLDS)

Attacked: `corpus/SOURCES.md` S073 row, cells `kind`=`docs`, `tier`=`A`. Rule read from the fleet-root contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (the file QUALITY.md:7 and SOURCES.md point to; the lane-local copy does not exist).

Printed (contract lines 24-30):
```
24:  `kind` — `spec` · `docs` · `paper` · `code` · `tool` · `dataset` · `talk` · `book` ·
26:- `tier` — scoped to `scope`, never global. **A**: primary or authoritative for that scope
27:  (spec, official docs, source code, original paper, maintainer statement, the lane's own
28:  re-runnable gate output). **B**: strong secondary ...
30:  `community` is never A. Tier is curation, not truth: no NATO/GRADE labels on rows.
```
`official docs` is listed for A and `docs` is a legal kind, so the page fits both. It is not `community`. Its editing model is public (see F4), but that does not make it community content.

Census (contract lines 77-78) run on the 5437afe tree; output:
```
$ awk ... corpus/SOURCES.md   # tier/status/kind/tier-inflation check
(no lines printed)   exit=0
$ awk ... NF!=13 ...           # malformed rows
0
```

Editing and maintainer status (who can edit): the page footer is quoted in the capture at `corpus/source-snapshots/round-46/S073.txt:585`: "All Docs are open source. See something that's wrong or unclear? Submit a pull request." The source repository was checked read-only:
```
$ curl -sL https://api.github.com/repos/github/docs
"visibility": "public", "license": {... "spdx_id": "CC-BY-4.0" ...}
$ curl -sL https://raw.githubusercontent.com/github/docs/main/.github/CODEOWNERS
# Last matching pattern wins.
content/site-policy/ @github/site-policy-admins
```
CODEOWNERS names an owner only for `content/site-policy/`; `content/code-security/` has no declared owner. So the page is GitHub's own published docs, editable by pull request, merged by repository write-holders. It is not a repository maintainer's statement and must not be described as one. The row does not describe it as one (its scope excludes "maintainer handling"), so the tier survives.

Public-membership check on the three commit-author logins returned 404 for all three (`api.github.com/orgs/github/public_members/<login>`). That is a null result: it does not show they are not GitHub staff, and the row does not claim they are. Not claimed either way.

## F2 — Fetch, size and quote claims (HOLDS, one date limit)

Command and output, live row URL (`curl -sL -A <lane UA>`):
```
final=https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately http=200 bytes=577188
HTTP/2 200      (HEAD)   content-length: 577188   date: Wed, 28 Oct 2026 23:55:23 GMT
```
Manifest (`corpus/source-snapshots/round-46/manifest.json`): `"fetched_utc": "2026-10-28T22:56:49Z"`, `"bytes": 577188`, `"sha256": "66c96a61...df1930"`. The live byte count equals the manifest raw count, and final URL equals the row URL. The 22:56:49Z instant itself cannot be re-observed (LIMIT-1).

Capture checks (`sha256sum`, `wc -lc`):
```
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  corpus/source-snapshots/round-46/S073.txt
589 15568 corpus/source-snapshots/round-46/S073.txt
```
The row's body range holds: L556 heading "Privately reporting a security vulnerability"; L573 "By default, you must provide a summary, details, proof of concept, and impact statement."; L575 "At the bottom of the form, click Submit report."; L578 "Optionally, click Start a temporary private fork ..."; L583 is the last body line before "Back to top" at L584.

Quote-level discrimination (the 8 manifest quotes against the live page, tags stripped, entities decoded, Python `str.count`): each returned 1. Control, mutated quote "also the repository maintainer can merge changes from that private fork" returned 0 on the live page and 0 in the capture. Control, absent phrase "Last updated" returned 0 on the live page.

Page date metadata (live page, 577188 bytes): `grep -o -iE '(dateModified|datePublished|lastModified|last-modified|Last updated...)'` printed nothing. The page has no visible or machine-readable publication/revision date. The row's anchor therefore gives a fetch instant and a capture sha, not a page revision. That is the same situation S048 records as "the page shows no visible publication or revision date" (`corpus/SOURCES.md`, S048 row), which the lane already accepts; the stronger pin is in F4.

## F3 — Legacy redirect statement (TRUE as written)

The row says the legacy `.../security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability` URL "redirects to the row URL (HTTP 200, 1 redirect, checked 2026-10-28)".

Command and printed output:
```
$ curl -sIL -A <lane UA> 'https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability' | grep -E "^(HTTP|location)"
HTTP/2 301 
location: /en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
HTTP/2 200 

$ curl -sL -A <lane UA> -o /dev/null -w 'hops=%{num_redirects} final=%{url_effective} http=%{http_code} size=%{size_download}\n' '<same legacy URL>'
hops=1 final=https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately http=200 size=577188
```
Control, a path that does not exist: `curl -sIL ... 'https://docs.github.com/en/code-security/r46-control-no-such-page' | grep -E "^(HTTP|location)"` printed `HTTP/2 404` and no location line. The redirect is therefore real and not a generic "any path" response.

Source of the redirect: the page file's frontmatter `redirect_from`, at `content/code-security/how-tos/report-and-fix-vulnerabilities/report-privately.md:12` (fetched from `raw.githubusercontent.com/github/docs/main/...`): `  - /code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability`. The row's abbreviated legacy path matches it.

## F4 — The row's scope sentences were last changed on 2026-10-02 (the anchor should say so)

The page file alone does not hold the scope sentences. The body includes `{% data reusables.security-advisory.reporting-a-vulnerability-non-admin %}` (`src.md`), and the default-fields sentence, the AI-assistance option and the temporary-fork sentence live in `data/reusables/security-advisory/reporting-a-vulnerability-non-admin.md`.

Commit `e85b5032f062ca8a54c489139c221d25e31db885` (2026-10-02T14:05:00Z, message "Structured, required proof-of-concept fields + Confidential team-only comments for private vulnerability reports (#63552)") touched both files. Printed patch lines from `api.github.com/repos/github/docs/commits/e85b5032f062ca8a54c489139c221d25e31db885`:
```
reporting-a-vulnerability-non-admin.md  (-) 1. Fill in the advisory details form.
                                        (-) > In this form, only the title and description are mandatory. ...
                                        (+) 1. If the repository has a security policy, review the policy displayed above the form.
                                        (+) 1. Fill in the vulnerability reporting form.
                                        (+)    > By default, you must provide a summary, details, proof of concept, and impact statement. ...
                                        (+) 1. Optionally, select **I used AI assistance to find or write up this report**.
report-privately.md                     (-) ... and you don’t need to follow the instructions in `SECURITY.md`.
                                        (+) ... If the repository has a security policy, the policy is displayed above the reporting form ...
```
Consequences: (a) the row's "the form's default fields" scope is true of the current revision only; a pre-2026-10-02 copy of this help says "only the title and description are mandatory", which contradicts the row. The row must therefore pin the revision. (b) The "AI assistance" option (capture L574) and the policy-displayed sentence (capture L564) are also from this commit. (c) The first sentence the row relies on for enablement, "Private vulnerability reporting is separate from a repository's SECURITY.md file. You can only report vulnerabilities privately for repositories where this feature is enabled." (capture L564), is unchanged by the commit; the commit only replaced the second half of that bullet. The quoted 13-word sentence survives.

Commit-level control: the parent text quoted above is the discriminator. Its `-` lines do not match the capture at L573, and its `+` lines do.

## F5 — Recommended tier and scope wording (survives), with located quotes

Tier: keep `docs | A`. Scope cell, recommended text (keep the existing exclusions):
> GitHub's own published docs statement of the reporter-side private-reporting flow only (who may report, the form's default fields, the AI-assistance option, submission and the temporary private fork); GitHub-published, not a repository maintainer's statement; not maintainer handling, the GitHub Advisory Database or CVE assignment

Anchor cell, add after the existing text:
> page shows no visible publication or revision date (live and capture); the default-fields, AI-assistance and temporary-fork sentences are in github/docs `data/reusables/security-advisory/reporting-a-vulnerability-non-admin.md`, last changed by commit e85b5032f0 (2026-10-02); the legacy URL 301s to the row URL (`curl -sIL`, 1 hop)

Located quotes for the entry and row (each ≤25 words, verified against the capture):
- "Anyone can privately report a security vulnerability to repository maintainers." (`S073.txt:560`, 11 words)
- "You can only report vulnerabilities privately for repositories where this feature is enabled." (`S073.txt:564`, 13 words)
- "By default, you must provide a summary, details, proof of concept, and impact statement." (`S073.txt:573`, 15 words)
- "All Docs are open source. See something that's wrong or unclear? Submit a pull request." (`S073.txt:585`, 15 words)
- "Note that only the repository maintainer can merge changes from that private fork into the parent repository." (`S073.txt:578`, 17 words)

Prose claims the entry should avoid: "maintainer statement" for this page, and any reading of "community" that treats the open PR model as making it non-A. The lane's `kind docs` plus tier A is correct; the attribution is GitHub's.

## Limitations

- LIMIT-1: The manifest fetch instant `2026-10-28T22:56:49Z` and the manifest raw sha256 were not re-observed. The manifest records only the snapshot sha, so the raw bytes match only by length (577188) and by the quote set, not by hash.
- LIMIT-2: I did not check github/docs branch protection or merge rights. CODEOWNERS is the only ownership source checked.
- LIMIT-3: GitHub staff status of the commit authors is unverified; the public-membership endpoint returned 404 for all three.
- LIMIT-4: I did not search whether the reusable file is included by other GitHub pages (no code-search access). The scope claim does not depend on it.
- LIMIT-5: The live page was read at `Wed, 28 Oct 2026 23:55:23 GMT`. Any later edit is outside this check.
- LIMIT-6: I did not run the lane's own `corpus/instruments/source-recheck.py` against S073 (not a tier question); the C1/C2 seats cover the entry gates.
