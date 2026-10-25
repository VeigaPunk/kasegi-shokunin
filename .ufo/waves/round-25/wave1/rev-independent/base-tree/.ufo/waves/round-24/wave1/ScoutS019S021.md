# ScoutS019S021 — queued-source recon (S019, S020, S021, S023)

Seat: scout, read-only. Item: optional-source probing for the **next** round; nothing is admitted here. Access date for every observation below: **2026-10-25**. Lane HEAD read with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse master` → `c2480b143120364728b40397926ffcf30a7309c8`.

Rows come from `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md:25,26,27,29` (all four still `queued`, all dated 2026-10-19). Bodies are in `/tmp` only: `/tmp/r24s019/{f2df5fb8,fbd25994,8770ed64}.html`, `/tmp/r24s019/sp800-216.pdf`, `/tmp/r24s020/doj.pdf`. Nothing was written inside the lane tree except this report.

## Findings

1. **All four queued sources are openable today, with no redirect.** `curl -sS -L -o /dev/null -w '%{http_code} %{url_effective} %{size_download} %{content_type}'` on the four cited URLs, 2026-10-25:

   | row | http | bytes | content-type | effective URL |
   |---|---|---|---|---|
   | S019 | 200 | 44,658 | `text/html; charset=utf-8` | unchanged |
   | S020 | 200 | 140,909 | `application/pdf` | unchanged (`dl?inline=` returns the PDF directly, no 30x) |
   | S021 | 200 | 127,832 | `text/html; charset=utf-8` | unchanged |
   | S023 | 200 | 75,587 | `text/html; charset=utf-8` | unchanged |

   No dead link in this slice; no substitute URL is needed for any of the four.

2. **S019's landing page cannot carry an exactly-once quote from its abstract — the abstract is rendered three times.** In `/tmp/r24s019/f2df5fb8.html` the sentence `Formalizing actions to accept, assess, and manage vulnerability disclosure reports can help reduce known security vulnerabilities.` has **occ=3** after tag-strip + whitespace collapse (CSRC ships a collapsed copy, an expanded copy and a second expanded copy nested in the "See full abstract" / "Hide full abstract" block); `The framework allows for local resolution support while providing federal oversight` has occ=2, `This document recommends guidance for establishing a federal vulnerability disclosure framework` occ=2. Outside that triplicated block the page carries only chrome (`Document History:`, `None selected`, `None available`, gov-banner text), so **the landing page has zero exactly-once substantive prose**. The PDF linked from that same page — `href="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf"` in `f2df5fb8.html`, 200, 1,510,851 bytes, sha256 `363183f0…80b67f` — carries the identical abstract sentence at **occ=1**. A later round must pin the PDF (or the DOI `https://doi.org/10.6028/NIST.SP.800-216` target), not the landing page, if it wants a locatable quote.

3. **S019 has a version/date line in three independent forms.** `f2df5fb8.html`: `Date Published: May 2023`; `Planning Note (05/24/2023)`; meta `citation_publication_date` = `2023/05/24`; `Document History: 06/07/21: SP 800-216 (Draft) / 05/24/23: SP 800-216 (Final)`. The PDF repeats `May 2023` on its cover (`/tmp/r24s019/sp216.txt:34`). Row S019's registered "published 2023-05-24" is confirmed, and the draft→final pair is explicit, so a later capture can distinguish the draft from the final.

4. **S020 is a PDF with a version line, and its most on-point sentence is exactly once.** `pdftotext -layout` (`/tmp/r24s020/doj.txt:12`) gives `Version 1.0 (July 2017)` on the title page, immediately under the title `A Framework for a Vulnerability Disclosure Program for Online Systems`. Row S020's registered "Version 1.0, July 2017" is confirmed. The authorisation sentence at `/tmp/r24s020/doj.txt:290` is occ=1 under both `-layout` and `-raw` extraction. Note the sentence is only reachable through text extraction: the PDF is deflate-compressed, so a capture that pins the raw `.pdf` bytes cannot be grepped for a quote — pin the `pdftotext` extract alongside it.

5. **S021 carries a machine-readable issued date, and its scope-authority Q&A is exactly once even in raw bytes.** `<time datetime="2020-09-02T12:00:00Z">September 02, 2020</time>` in `/tmp/r24s019/fbd25994.html` (also present as the visible heading `September 02, 2020` at `/tmp/r24s019/s021.txt:78`). Row S021's "issued 2020-09-02" is confirmed. The chosen quote has **occ=1 in the raw HTML bytes and occ=1 in the tag-stripped text** — the easiest capture in this slice, no extraction step required.

6. **S023 still has no publication date — and the page is demonstrably being edited.** Zero matches for `(January|…|December) [0-9]{1,2}, 20[0-9]{2}` in `8770ed64.html`, no `datePublished`/`dateModified` JSON-LD, no `<time>` element, no "last updated/reviewed/modified" line. Row S023's registered "page has no visible publication date" still holds. But the page now contains material the row does not describe: step `7. Known Exploited Vulnerabilities (KEV) Evaluation and Publication`, a `VDP vs CVD` contrast (`8770ed64.html` → stripped `:216-217`), and a VEP note (`:212`). So a row that cites this page has no way to tell a revision from the original: pin the fetched bytes plus the access date, never the URL alone.

7. **S023 contains a live verbatim defect that is a good fingerprint but a bad quote.** `vulnerabilities reported to CISA through the CVD process are no subject to VEP adjudication` (missing "t"; occ=1 in the stripped text, `8770ed64.html:1321` region). It is unique and would survive as a drift detector, but a knowledge entry must not quote a typo as the source's position. Use it only in a capture note.

8. **S023 numbering is still 1–7 as the row expects.** Stripped extract `:157-195`: `1. Vulnerability Report Submission`, `2. CVD Intake and Triage`, `3. CVD Coordination`, `4. CVE Record Determination (If Applicable)`, `5. Advisory Development and Publication Prep`, `6. Public Disclosure`, `7. Known Exploited Vulnerabilities (KEV) Evaluation and Publication`. The row's "The CVD Process, steps 1–7" anchor is intact, so the entry-level mapping in the row needs no change.

## Per-source records

| id | cited URL | status | bytes | sha256 (as fetched 2026-10-25) | version/date line visible today | exactly-once quote? |
|---|---|---|---|---|---|---|
| S019 | https://csrc.nist.gov/pubs/sp/800/216/final | 200 HTML (PDF 200, 1,510,851) | 44,658 (PDF 1,510,851) | `76317f97…dbe00337` (PDF `363183f0…8980b67f`) | `Date Published: May 2023` + `Planning Note (05/24/2023)` + `05/24/23: SP 800-216 (Final)` | **no on page (occ=3)**; **yes in PDF (occ=1)** |
| S020 | https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline= | 200 PDF | 140,909 | `d0cfa766…6e51ee7` | `Version 1.0 (July 2017)` (`doj.txt:12`) | yes (occ=1, extract only) |
| S021 | https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy | 200 HTML | 127,832 | `919a9c56…7b83df4a` | `<time datetime="2020-09-02…">September 02, 2020</time>` | yes (occ=1, raw bytes and text) |
| S023 | https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program | 200 HTML | 75,587 | `383792fd…5ca6da` | **none** — no date, no `<time>`, no `datePublished` | yes (occ=1, raw bytes and text) |

Hashes are of the bodies as fetched (curl already decoded gzip). If a later round pins a text extract instead, re-hash the extract; the manifest `sha256` must cover the pinned file.

## Exactly-once quote candidates (5-25 words)

Occurrence counts are after whitespace collapse (`" ".join(text.split())`), the same normalization `corpus/instruments/source-recheck.py:29-31` applies; every candidate below is occ=1 in the body named.

### S019 — NIST SP 800-216 (May 2023), from the PDF linked by the row

| # | quote | words | location | why it is usable |
|---|---|---|---|---|
| 1 | `Formalizing actions to accept, assess, and manage vulnerability disclosure reports can help reduce known security vulnerabilities.` | 16 | `/tmp/r24s019/sp216.txt:118` (Abstract) | The framework's own thesis, and it grounds "formalize intake/assessment/tracking" without needing the triplicated landing-page block. occ=1 in both `-layout` and `-raw`. |
| 2 | `The framework allows for local resolution support while providing federal oversight` | 11 | `/tmp/r24s019/sp216.txt:118` | occ=1 in the PDF; states the federal-oversight/local-resolution split the row's rationale implies. |
| 3 | `This document recommends guidance for establishing a federal vulnerability disclosure framework, properly handling vulnerability reports` | 15 | `/tmp/r24s019/sp216.txt:118` | occ=1 in the PDF; closest match to the row's "intake, assessment, tracking and communications" framing. |

Landing-page variants of 1-3 are **not** usable: occ=3 / occ=2 / occ=2 respectively (`f2df5fb8.html`).

### S020 — DOJ Framework, Version 1.0 (July 2017)

| # | quote | words | location | why it is usable |
|---|---|---|---|---|
| 1 | `The organization considers activities conducted consistent with the policy to constitute “authorized” conduct under the Computer Fraud and Abuse Act.` | 20 | `/tmp/r24s020/doj.txt:290` (Step 3.D.2) | The framework's own statement that authorisation comes from the policy, not the safe-harbour paragraph; the sentence the row's rationale is about. occ=1 in `-layout` and `-raw`. |
| 2 | `the organization implementing the vulnerability disclosure program may lack the authority to authorize others to access the provider’s servers` | 19 | `/tmp/r24s020/doj.txt:150` (Step 1.C.1) | The supplier-hosted-asset limit the row asks about, in the framework's own words. occ=1. |
| 3 | `Describe authorized and unauthorized conduct in plain, easily understood terms.` | 10 | `/tmp/r24s020/doj.txt:239` (Step 3.A) | occ=1; the "express allowed and disallowed conduct plainly" limb of the row's rationale. |

### S021 — CISA BOD 20-01 (issued 2020-09-02)

| # | quote | words | location | why it is usable |
|---|---|---|---|---|
| 1 | `Your agency may not have the authority to authorize testing on e.g., the cloud infrastructure or software as a service you use.` | 22 | `/tmp/r24s019/s021.txt:484` (FAQ: service-provider systems) | Third-party authorisation stated by the directive that mandates the VDP; occ=1 in raw bytes and in stripped text. |
| 2 | `At least one internet-accessible production system or service must be in scope at the time of publication.` | 17 | `/tmp/r24s019/s021.txt:199` (Required Actions 3.a.i) | Minimum initial scope, with `production` defined later on the same page. occ=1. |
| 3 | `Contain guidelines to help vulnerability finders understand how to remain in scope of authorized testing.` | 15 | `/tmp/r24s019/s021.txt:206` | The "permitted testing" limb; occ=1. |

S021's scope-expansion ladder is also quotable and dated in-page: `At 2 years ( Friday, September 2, 2022 )` / `All internet-accessible systems or services must be in scope of your policy.` (`s021.txt:194-195`).

### S023 — CISA CVD Program page (undated)

| # | quote | words | location | why it is usable |
|---|---|---|---|---|
| 1 | `If referred, the report is valid but better handled by another organization or vendor, so CISA directs the reporter to the appropriate channel.` | 23 | `8770ed64.html` → stripped `:170` (step 2 outcome note) | Separates "invalid" from "out of scope / referred" — the intake-vs-triage distinction the row cites. occ=1 in raw bytes and in text. |
| 2 | `Once accepted, the case moves into coordinated disclosure where CISA performs:` | 11 | stripped `:172` (step 3) | Marks where triage ends and coordination starts. occ=1. |
| 3 | `CISA determines whether it should receive a CVE ID and identifies which CVE Numbering Authority (CNA) is responsible` | 18 | stripped `:181` (step 4) | The CVE-determination stage as a distinct step. occ=1. |

## Remaining unknowns

- **S023 has no document date in transport metadata either.** `curl -sSI -L` on the cited URL returns `HTTP/2 200`, `cache-control: private, no-cache, must-revalidate`, `expires:` and `date:` (both = server clock, 2026-10-25), `x-wcm-h: WCM-209-113`, and **no `last-modified`, no `etag`**. So neither the body nor the headers date this page; the only defensible provenance for a capture is the access date plus the body hash. Whether `x-wcm-h: WCM-209-113` is a stable content-revision identifier (which would be a substitute date proxy) is UNVERIFIED — I did not re-poll the page to see whether the value changes.
- **S019's headers carry no document date either** (`expires: -1`, no `last-modified`); its date must come from the body's `Planning Note`/`Document History`, which is what finding 3 records.
- **Whether the S019 PDF and the landing page stay in sync.** They agree today on the abstract sentence; the landing page's triple-render means a later re-read that greps the page will see count changes rather than content changes.
- **S020 has no in-page supersession marker.** `Version 1.0 (July 2017)` is the only version claim; nothing on the PDF states whether a newer version exists, and the row's `on-release` cadence cannot detect one from this URL alone.
- Nothing here is admitted, and no row status was changed. S022 and S024 are outside this item and were not probed.

## Tooling

No installs or upgrades; nothing needed installing. `curl` and `poppler-utils` (`pdftotext`) were already present.
