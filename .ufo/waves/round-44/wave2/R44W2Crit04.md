# R44W2Crit04 — rejection attack on S070 (round 44, attempt 2, wave 2)

- seat: R44W2Crit04 (critic, leaf, read-only; no production edits)
- tree under attack: `8063547d0ce647d6f9eafc3c8d0a502616685218` (all `git show`/`git grep` citations below are at this commit; `git diff --stat 8063547d… -- corpus/SOURCES.md corpus/lessons/round-44.md` → empty, so working tree matches for the cited files)
- item: re-open `https://bughunters.google.com/about/rules/about-this-section`, judge the recorded rejection ("the accessible body is a JavaScript shell and the metadata is a directory welcome") and whether the recorded flip condition is specific enough for a non-author re-check. Quote what I can actually see.
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44W2Crit04/` (removed before yield)
- tooling: nothing installed or upgraded; stock `curl`/`jq`/`python3` only.

## 1. What the committed record says

- `corpus/SOURCES.md:76` (S070 row, tier C, status `rejected`, opened 2026-10-28, recheck `180d`, used-by `—`):
  > REJECTED: the page's accessible body is a JavaScript shell and its metadata is a directory welcome, not an operative program rule; flip: the page itself exposes a located, program-specific rule absent from the linked policy text.
  Anchor cell cites only: `meta description, opened 2026-10-28: “Welcome to Google's Bug Hunting community, learn more about hunting & reporting bugs you’ve found in Google products.”`
- `corpus/lessons/round-44.md:131` (attempt-2 gate, reject entry):
  > Reject — S070, tier C, `rejected`. … the accessible body is a JavaScript shell and the metadata is a directory welcome with no quotable rule. Flip condition: a readable, dated copy of the rules directory that carries a quotable rule text.
- `corpus/lessons/round-44.md:22` repeats the same two grounds ("rejected because its accessible body is a JavaScript shell and its metadata is only a directory welcome").
- `corpus/SOURCES.md:105` (the sweep provenance): "Identified 2, screened 2, included 1 as S069 and rejected 1" — S070 was screened in the same sweep as S069.
- The lane's own capture convention for this host, same commit, `corpus/SOURCES.md:75` (S069 row): "official article API capture at corpus/source-snapshots/round-44/S069.txt, fetched 2026-10-28T18:53:38Z; sha256 0932279c…; … capture body extracted from preserved API JSON via `jq -r '.body'`" — i.e. for a bughunters page row, the page's text is the first-party article-API body.
- No knowledge entry cites S070: `git grep -n 'S070' 8063547d… -- corpus/knowledge` → 0 hits (matches the lesson's claim).
- `.ufo/reports/round-44/` does not exist at the attacked commit (`git ls-tree -r --name-only 8063547d… -- .ufo/reports` → only `round-21/kasegi.md`); the reject currently lives only in the registry row + lesson. Treated as mid-round state, not a defect.

## 2. What I can actually see (my re-open, 2026-10-28 ~20:04 GMT)

Commands (run from scratch dir; UA `Mozilla/5.0 (X11; Linux x86_64) … Chrome/131.0.0.0 Safari/537.36`):

```
curl -sS --max-time 60 -A "$UA" -D hdr.txt -o body.html -w '…' \
  'https://bughunters.google.com/about/rules/about-this-section'
curl -sS --max-time 60 -A "$UA" -o api.json -w '…' \
  'https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section'
```

Observed:

1. **Raw HTML fetch**: `http=200 bytes=3593`, `content-type: text/html; charset=utf-8`, `server: Google Frontend`, `date: Wed, 28 Oct 2026 20:04:48 GMT`; sha256 `1c49f4322b706198e2e79cff041f692af87d4dc2001d4ff0ca4fd22a7405386a`. Body structure: `<body class="mat-app-background"><app-root></app-root>` plus two `defer` script bundles (`…/third_party_js-bundle.js`, `…/app_bundle_prod.js`) — no server-rendered text. Reader-mode extraction of the same URL returns **metadata only, zero body text**: `title: Rules | Google Bug Hunters`, `meta-description: Welcome to Google's Bug Hunting community, learn more about hunting & reporting bugs you’ve found in Google products.` (plus og:/twitter: duplicates).
2. **Metadata quote fidelity**: decoded live meta description vs the row's quoted string → `match : True`, 117/117 chars (row's `Google's` matches the decoded `&#39;`; `you’ve` is literal U+2019 in the served HTML). The row's positive evidence is byte-faithful.
3. **First-party article API for the same URL** (the lane's own S069 convention): `http=200 bytes=10588 type=application/json`; keys `body, categories, documentId, public, title`; `documentId:"6744710187712512"`, `public:true`, `title:"About This Section"`. `jq -r '.body'` → 10,032 bytes / 312 lines of readable text, opening:
   > Welcome to the VRP rules section! Here, you’ll find an overview of the different vulnerability reward programs Google maintains, as well as guidance on related programs. …
   It is a directory welcome + per-program tables (program name / scope / where to report). Rule-language scan over all 312 lines: `grep -c -iE 'prohibit|disqualif'` → **0** (and no `eligib`/`must not`/`out of scope` hits). No operative rule text.
4. **The directory's Cloud VRP scope cell** (api body lines 146–151):
   > Cloud Vulnerability Reward Program (rules) … Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data … Use the standard form (report to Cloud VRP)
   The linked rules document is the **same document S069 pins**: `…/rest/v1/articles/about/rules/4849867320328192/cloud-vulnerability-reward-program-rules` → `{"documentId":"4849867320328192","title":"Cloud Vulnerability Reward Program Rules","public":true}`, identical to the committed `.ufo/waves/round-44/source-recon/S069.txt` documentId. S069's pinned policy text (snapshot lines 61–72) states the boundary the directory cell omits: "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services. … testing customer resources is strictly prohibited".

## 3. Findings

**F1 — agree (metadata ground).** The metadata *is* a directory/community welcome ("Welcome to Google's Bug Hunting community…", title "Rules | Google Bug Hunters"), quoted byte-faithfully in the row. No defect.

**F2 — agree, method-scoped (JS-shell ground).** The raw HTML fetch is genuinely a shell: 3,593 B, empty `<app-root>`, two deferred bundles, zero reader-extractable body text. True *of a bare-HTML fetch*. Limitation: I did not execute JavaScript, so I cannot rule out client-rendered content; the finding below does not depend on that.

**F3 — falsified as recorded: "the page's accessible body is a JavaScript shell" is false under the lane's own access convention for this host.** The same commit's S069 row establishes that a bughunters page's text is captured via the first-party article API (`/rest/v1/articles/<path>`, `jq -r '.body'`). Applying that identical convention to S070's URL returns HTTP 200 with a 10,588-byte JSON document carrying a 10,032-byte readable body. The row records only the meta description and never states which access method produced the "JavaScript shell" observation, nor that the API path was available. The lane's own wave-1 draft shows it knows better for this exact host: `.ufo/waves/round-44/wave1/R44Scribe5.md:219` drafted S071 — the HTML form of the sibling Cloud VRP rules page — with ground "REJECTED: JS shell; served bytes contain no rule text and cannot carry Q1–Q3", and the lane did **not** land that reject; it admitted the content via the API capture (S069) instead. Same host, same shell, opposite treatment; the S070 record does not disclose the divergence.

**F4 — the recorded grounds never examine the body, and the body is not only "navigation and metadata".** The row's own scope column asks "Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata", yet the anchor cell cites only the meta description. My re-open shows the API body supplies per-program **scope summaries** — for Cloud VRP, "Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data" — which (a) are content beyond navigation/metadata, and (b) state a **broader** scope than the operative rule S069 pins (which adds the Google-owned-infrastructure limitation and the customer-resource prohibition). A reader trusting the directory cell would over-believe Cloud VRP scope. The reject *outcome* still survives — the body contains zero rule language (`prohibit|disqualif` → 0 hits in 312 lines), so "not an operative program rule" holds — but the recorded evidence does not establish it; the decisive observation (what the body contains) is absent from the record.

**F5 — falsified: the flip condition is not specific enough for a non-author re-check, and it is recorded twice with divergent predicates.**
- Row flip (`corpus/SOURCES.md:76`): "the page itself exposes a located, program-specific rule absent from the linked policy text."
- Lesson flip (`corpus/lessons/round-44.md:131`): "a readable, dated copy of the rules directory that carries a quotable rule text."
These have different satisfaction conditions: the row's is a counterfactual test on the page plus an absence test; the lesson's is an acquisition requirement (find a dated readable copy). They can disagree: the API JSON has keys `body/categories/documentId/public/title` and **no date field**, so the page's own API copy can never satisfy the lesson's "dated" predicate while the row's flip does not require a date at all; conversely an archived dated copy would satisfy the lesson's flip without touching "the page itself".
Concrete divergent-reading case from my re-open: the directory body's Cloud VRP cell is *located* (api body lines 146–151), *program-specific* (names Cloud VRP), and *quotable* — but contains no rule language, and the scope fact it summarizes is present in the linked policy text (S069's document) in stricter wording. Under the row flip, a non-author must decide (i) whether the API body counts as "the page itself" (the lane's S069 convention says yes), (ii) whether a one-line scope summary is a "rule" (undefined threshold), and (iii) whether "absent from the linked policy text" means the *fact* (present, stricter) or the *text* (absent, broader wording). Under the lesson flip, the same non-author performs a different action (hunt a dated copy) with an undefined "quotable rule text" threshold. Neither predicate names the access method (decisive here: HTML shell vs 10 KB API body), the comparator document (resolvable in practice — the directory links documentId `4849867320328192`, which is S069's pinned document — but unnamed in the record), or the artifact a satisfying observation must produce (no snapshot/digest/locator requirement, unlike the admit-side discipline that pins sha256 + line locators). The row schedules a non-author recheck at `180d`, so the underspecification is operative, not theoretical. Compare the lane's own round-43 precedent (S068, `round-43-verifier-spotcheck.md` §4): a multi-ground reject whose flip names exact tokens ("status becomes `Reviewed`; or the curl package with per-version ranges / commit `c6ae07c6…`") — S070's record is materially weaker than the lane's own standard.

## 4. Verdict (no inflation)

- The **reject outcome** (tier C; the directory is not a source of operative program rules) is **right** and survived my re-open, including the body the record never examined (zero rule language in 10,032 bytes).
- The **recorded rejection grounds** are **defective**: ground 1 ("accessible body is a JavaScript shell") is method-scoped, unstated as such, and false under the lane's own S069 capture convention for the same host; ground 2 addresses only metadata while the row's own question asks about the body, whose content (per-program scope summaries, one materially broader than the operative rule) is unrecorded.
- The **flip condition is not re-checkable by a non-author as written**: two divergent committed predicates, no access-method or comparator or artifact specification, and a "dated" requirement the page's own API copy cannot satisfy.

## 5. Smallest safe correction (proposal only; I made no edits)

Append one correction (round-44 erratum style, append-only) that (a) restates the reject ground with the method and the body finding — raw HTML 3,593 B shell; first-party article API body 10,588 B JSON, directory welcome + per-program scope/link tables, 0 rule-language hits — and (b) replaces both flip sentences with one decidable predicate, e.g.: "flip: any access path to this URL (raw HTML or `/rest/v1/articles/about/rules/about-this-section`) yields located rule language (prohibition/eligibility/disqualification text) not present in the program rules documents the directory links (e.g. documentId 4849867320328192); a satisfying observation is a pinned snapshot with sha256 and line locators, same discipline as an admit."

## 6. Limitations

- No JavaScript execution (no headless browser): the JS-shell judgment rests on served HTML structure + zero reader-extractable body text, not on a rendered check. Does not affect F3/F4/F5.
- I did not test archival copies (web.archive.org), so the lesson flip's "readable, dated copy" path is untested, only shown to be a different predicate than the row's.
- Live fetches are point-in-time (2026-10-28 ~20:04 GMT, `date` header quoted); sizes/digests quoted are of that fetch, saved in scratch and removed per seat rules — the report quotes are the durable record.
