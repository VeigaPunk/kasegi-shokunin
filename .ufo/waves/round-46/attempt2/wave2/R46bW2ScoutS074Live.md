VERDICT: DRAFT-READY

Seat: R46bW2ScoutS074Live — item: live-page recheck of the landed S074 entry
`corpus/knowledge/github-repository-security-advisories.md` against the LIVE
https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
(fallback: pinned capture `corpus/source-snapshots/round-46-a2/S074.txt`).

Result in one line: NO quote drift — all quoted spans are held by the live page
(C2 kill rule not triggered); two minor entry statements are not supported by
the page as written (M46-3 class, wording-level) → DRAFT-READY, not BROKEN.

## 0. Live-page re-open (recorded as required)

Command (run from scratch, TMPDIR=$SCRATCH/tmp):

    curl -sS -L --max-time 90 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" -o live.html -w 'http_code=%{http_code} final_url=%{url_effective} size_bytes=%{size_download} num_redirects=%{num_redirects}\n' 'https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories'

Quoted output:

    http_code=200 final_url=https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories size_bytes=582877 num_redirects=0

Header fetch (second request) quoted:

    HTTP/2 200
    content-type: text/html; charset=utf-8
    date: Fri, 30 Oct 2026 00:03:21 GMT
    x-served-by: cache-iad-kiad7000073-IAD, cache-gig2250056-GIG

Page identity (from the downloaded HTML): `<title>Repository security
advisories - GitHub Docs</title>`, `<h1>Repository security advisories</h1>`.
Final URL equals the request URL — no redirect, no content move.

Capture integrity: `sha256sum S074.txt` →
`1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039` (matches the
value pinned in the entry header); 42 lines, 7087 bytes.

## 1. Quote layer: NO DRIFT (artifact attacked: the entry's 45 “…” spans)

Instrument (new, scratch `check_quotes.py`): extracts every `“…”` span from the
landed entry with its claimed `S074.txt:N` anchor; strips the live HTML
block-aware (inline tags removed, block boundaries → newline); containment test
on whitespace-normalised text, with a punctuation-normalised tier reported
separately. The entry holds 45 quoted spans (27 distinct texts after
whitespace normalisation); the battery checked all 35 whitespace-distinct raw
variants — every check covers at least one variant of each of the 27 distinct
texts.

Result: **35/35 FOUND(ws-normalised) on the live page**, and every claimed
anchor line verified in the pinned capture:

    Q01 anchor=S074.txt:3  live=FOUND(ws-normalised) capture_lines=[3]
    Q02 anchor=S074.txt:6  live=FOUND(ws-normalised) capture_lines=[6]
    Q03 anchor=S074.txt:10 live=FOUND(ws-normalised) capture_lines=[10]
    Q04 anchor=S074.txt:12 live=FOUND(ws-normalised) capture_lines=[12]
    Q05 anchor=S074.txt:13 live=FOUND(ws-normalised) capture_lines=[13]
    Q06 anchor=S074.txt:38 live=FOUND(ws-normalised) capture_lines=[38]
    Q07 anchor=S074.txt:25 live=FOUND(ws-normalised) capture_lines=[25]
    Q08 anchor=S074.txt:24 live=FOUND(ws-normalised) capture_lines=[24]
    Q09 anchor=S074.txt:25 live=FOUND(ws-normalised) capture_lines=[25]
    Q10 anchor=S074.txt:36 live=FOUND(ws-normalised) capture_lines=[36]
    Q11 anchor=S074.txt:14 live=FOUND(ws-normalised) capture_lines=[14]
    Q12 anchor=S074.txt:15 live=FOUND(ws-normalised) capture_lines=[15]
    Q13 anchor=S074.txt:17 live=FOUND(ws-normalised) capture_lines=[17]
    Q14 anchor=S074.txt:19 live=FOUND(ws-normalised) capture_lines=[19]
    Q15 anchor=S074.txt:19 live=FOUND(ws-normalised) capture_lines=[19]
    Q16 anchor=S074.txt:20 live=FOUND(ws-normalised) capture_lines=[20]
    Q17 anchor=S074.txt:26 live=FOUND(ws-normalised) capture_lines=[26]
    Q18 anchor=S074.txt:31 live=FOUND(ws-normalised) capture_lines=[31]
    Q19 anchor=S074.txt:32 live=FOUND(ws-normalised) capture_lines=[32]
    Q20 anchor=S074.txt:38 live=FOUND(ws-normalised) capture_lines=[38]
    Q21 anchor=S074.txt:17 live=FOUND(ws-normalised) capture_lines=[17]   (link text)
    Q22 anchor=S074.txt:16 live=FOUND(ws-normalised) capture_lines=[16]   (link text)
    Q23 anchor=S074.txt:34 live=FOUND(ws-normalised) capture_lines=[34]   (link text)
    Q24 anchor=S074.txt:19 live=FOUND(ws-normalised) capture_lines=[19]   (link text)
    Q25 anchor=S074.txt:23 live=FOUND(ws-normalised) capture_lines=[23]
    Q26 anchor=S074.txt:16 live=FOUND(ws-normalised) capture_lines=[16]
    Q27 anchor=S074.txt:33 live=FOUND(ws-normalised) capture_lines=[33]
    (Q28–Q35 are the entry's repeat quotes; all FOUND at their repeated anchors.)

Instrument-honesty note (would-be false BROKEN): v1 of the instrument, which
replaced every tag with a space, returned NOT-FOUND for Q06/Q28 and Q15. That
was an instrument artifact, not drift — raw HTML quoted:

    Whenever possible, you should <strong>add a fix version to a security advisory prior to publishing the advisory</strong>. If you don't, …
    <a href="https://github.com/advisories">github.com/advisories</a>. Anyone can submit a change …

Inline `<strong>`/`<a>` at sentence end injected a space before the period
("advisory ." / "github.com/advisories ."). v2 (block-aware stripping) finds
both sentences verbatim. Both quotes are held by the live page.

Controls (same battery; instrument is not vacuously matching):

    neg-48h         [must-be-absent] "GitHub usually reviews the request within 48 hours."             live=NOT-FOUND capture_lines=[]
    neg-url-changes [must-be-absent] "The URL of a security advisory changes after publication."       live=NOT-FOUND capture_lines=[]
    neg-public-fork [must-be-absent] "Privately collaborate to fix the vulnerability in a temporary public fork." live=NOT-FOUND capture_lines=[]
    pos-capture-probe [must-be-present] "GitHub usually reviews the request within 72 hours."          live=FOUND(ws-normalised) capture_lines=[25]

## 2. F1 (M46-3 class, low): "in the order the page states it" is not the page's order for steps 3–4

Artifact attacked: entry § "Scope and decision rule", the line
"Decision rule for a maintainer's package advisory step, in the order the page
states it:" — the entry numbers 3 = fix version, 4 = CVE request.

Evidence (char offsets of the four steps in the tag-stripped LIVE article text,
instrument output quoted):

    offset    13981  Create a draft security advisory
    offset    14103  Privately collaborate to fix the vulnerability in a temporary private fork
    offset    16483  GitHub usually reviews the request within 72 hours
    offset    18729  you should add a fix version to a security advisory prior to publishing

The page's own order is draft → fork → (publish) → CVE request → … → fix
version ("Importance of fix versions" is the page's last section). The content
of all four steps is fully supported by the quotes (G4, G5, G13/G14, G19); the
relative order of steps 3 and 4 — fix version BEFORE CVE request — is the
entry's construction; the page never states it (the page's prose puts the CVE
request first, the fix-version duty last). The phrase "in the order the page
states it" therefore overstates for steps 3–4.

Suggested fix: renumber to the page's section order (draft, fork, CVE request,
fix version) or reword, e.g. "steps 1–2 in the page's stated order; the fix
version and the CVE request are both pre-publication duties the page states in
separate sections without ordering them relative to each other."

## 3. F2 (M46-3 class, low): "the three cases … let a maintainer publish without a fix version" — only two do

Artifact attacked: entry § Limits, bullet "The fix-version duty is graded, not
absolute": "… and the three cases at S074.txt:40, S074.txt:41 and S074.txt:42
let a maintainer publish without a fix version."

Evidence (capture S074.txt:38-42, raw, sha-verified; identical wording confirmed
on the live page):

    38: Whenever possible, you should add a fix version to a security advisory prior to publishing the advisory. If you don't, …
    40: Imminently available, and you are able to, wait to disclose the issue when the fix is ready.
    41: In development but not yet available, mention this in the advisory, and edit the advisory later, after publication.
    42: Not planned, be clear about it in the advisory so that your users don't contact you to ask when a fix will be made. …

Case 40 instructs the maintainer to WAIT to disclose until the fix is ready —
it does not permit publishing without a fix version; only 41 and 42 do. The
entry's "the three cases … let a maintainer publish without a fix version" is
not fully supported by the page.

Suggested fix: "the two cases at S074.txt:41-42 let a maintainer publish
without a fix version; the third case (S074.txt:40) says to wait to disclose
until the fix is ready."

## 4. Entry Limits claims re-verified against the LIVE article text

Case-insensitive sweeps over the tag-stripped live article text (instrument
output quoted; capture column is the pinned body for comparison):

    sweep 'timeline':           live_hits=0 capture_hits=0
    sweep 'embargo':            live_hits=0 capture_hits=0
    sweep 'deadline':           live_hits=0 capture_hits=0
    sweep 'reward':             live_hits=0 capture_hits=0
    sweep 'bount':              live_hits=0 capture_hits=0
    sweep 'GitHub Enterprise':  live_hits=0 capture_hits=0

→ the entry's Limits claims "no disclosure deadline, no embargo and no reward …
nothing about GitHub Enterprise" still hold on the live page. Structure probes
all present on live: "Who can use this feature?", "About repository security
advisories", "CVE identification numbers", "Publication of security
advisories", "Dependabot alerts for published security advisories", "Importance
of fix versions", plus all four sibling-page link texts ("Creating a repository
security advisory", "REST API endpoints for repository security advisories",
"Editing a repository security advisory", "Editing security advisories in the
GitHub Advisory Database").

Nuance (not a finding): the live page contains exactly one `private repositor*`
hit, in the left-nav chrome — "Private repository enablement" (a CodeQL
troubleshooting nav item) — not article prose. The pinned capture is body-only,
so the entry's "says nothing about private repositories" holds for the article.

## 5. Limitations

- Two fetches of the live URL at 2026-10-30T00:03:21Z via Fastly cache
  (x-served-by cache-iad…/cache-gig…); a later re-fetch could see different
  edge state. No JS rendering was used; the article body is server-rendered
  HTML and that is what was checked. A js-gated page variant was not exercised.
- Quotes were checked against tag-stripped SSR HTML with whitespace
  normalisation, per the item. The punctuation-normalised tier existed but was
  never needed — all 35 hits matched under pure whitespace normalisation.
- F1's order evidence uses char offsets of the stripped article text (the
  page's section order); it is not a claim about visual TOC ordering.
- Not in this seat's item, not re-run here: the manifest Q1–Q9 recheck line,
  the round's claims-file counting commands, and the battery/selftest re-runs
  (other seats' items).
- No commits, no push, no git/jj/index mutation; no shared production files
  touched; only the report path named by the seat spec and scratch
  `/fast/scratch/hyaku/kasegi-r46/R46bW2ScoutS074Live/` (deleted on exit).
