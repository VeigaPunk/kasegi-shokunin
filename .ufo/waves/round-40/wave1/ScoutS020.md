# ScoutS020 — round 40, source row S020 (DOJ CCIPS VDP Framework)

## Verdict
**Decide: MINE (do not reject).** S020 is reachable, substantive, and teaches ground the lane does not hold (US CFAA exposure framing, third-party/cloud-hosted authorization limit, the DOJ's four policy commitments). Capture and manifest record delivered; the SOURCES row is ScribeRows' to write.

## Fetch (observed)
- URL: https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline=
- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`: HTTP 200, `content-type: application/pdf`, 140909 bytes, raw sha256 `d0cfa766a29328e120be7187435d09e5aef374c80bcbf0b1bd7a167c16e51ee7`, no redirect (url_effective = request URL), `content-disposition: inline; filename=csu-vulnerability-program-framework-final.pdf`, server date `Mon, 26 Oct 2026 21:15:56 GMT`. curl fetch time 2026-10-26T21:15:55Z.
- Committed-capture fetch with the lane's own `corpus/instruments/capture-source.py --id S020 --kind pdf` (scratch out): `S020 status=200 fetched_bytes=140909 snapshot_bytes=16693 sha256=8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c utc=2026-10-26T21:16:10Z`. The curl bytes run through `pdf_to_text()` reproduce the identical snapshot (checked: same bytes, same sha). 319 lines.
- Document: "A Framework for a Vulnerability Disclosure Program for Online Systems", Version 1.0 (July 2017), DOJ Criminal Division CCIPS Cybersecurity Unit (L1-L8).

## (a) Reachable and substantive? Yes
200 OK, real PDF text (pdftotext ok, 16.7 KB of text, 319 lines). Structure: Step 1 Design (L44), Step 2 Plan administration (L167), Step 3 Draft policy (L229), Step 4 Implement (L307). Not a landing page, no paywall.

## (b) New ground vs the lane? Yes
- `grep -il "doj|justice|CCIPS|1030|CFAA"` over corpus/knowledge/*.md and README.md: no hits (only SOURCES.md, which holds the S020 queued row itself). `grep -n "DOJ|CFAA|Department of Justice|CCIPS" knowledge/*.md`: no hits.
- Closest held ground: F03 `authorization-safe-harbor-and-scope.md` (S006/S007/S008 — platform/CISA text; L39 says the sources "do not resolve third-party asset ownership, external legal protection"); F09 `authorised-testing-rules-of-engagement.md` + `statutory-authorization-and-unauthorized-access.md` (S032-S035; Japanese 不正アクセス禁止法 and NIST SP 800-115; the statutory file L46 reasons about third-party-operated assets from the Japanese statute). None carries a US-government author's own statement of the CFAA frame or the DOJ commitments.
- What S020 adds, with capture anchors:
  - L73-L76: CFAA elements (18 U.S.C. § 1030(e)(2), "without authorization or in excess of authorization"; not limited to domestic conduct) — the US statutory counterpart to F09's Japanese statute.
  - L135-L137 / L142-L148 (Step 1.C): third-party interests: components/data implicating third parties are excluded or need additional authorization; cloud-provider example, a service-level contract may address it, counsel decides. Directly the question the SOURCES row asks (can the org authorize testing of supplier-hosted assets).
  - L232-L240 (Step 3.A): describe authorized and unauthorized conduct in plain terms; list unauthorized techniques; limits on accessing/copying/retaining data.
  - L282-L296 (Step 3.D): the four commitments an org can make: no civil action or law-enforcement complaint for accidental good-faith violations; policy-consistent activity is "authorized" under the CFAA; org will state publicly/to court that a third-party-sued researcher complied.
  - L145-L166 pointers to 18F, NTIA, ISO 29147 (not read; do not cite as content).
- Limit to record: 2017 document; the capture contains no case law and no statement of current DOJ charging policy (the 2022 policy is a different document, not opened). It says "may" (guidance), not a safe harbor.
- Frontier fit: extends F03/F09 (authorization) rather than a new F-row by itself; it can join a new frontier with other rows or become a cross-reference in an existing entry (L1/Scribe call).

## (c) Located quote (22 words) — source-recheck verified
> Absent an agreement with the cloud service provider, the organization implementing the vulnerability disclosure program may lack the authority to authorize others

Anchor: capture L142-L145 (starts mid-line L142, Step 1 item C.1, cloud-storage example). Second single-line quote available (10 words, L232, Step 3.A): "Describe authorized and unauthorized conduct in plain, easily understood terms." (occurs once).

Verification run (scratch copy of capture + the manifest record wrapped in a `{schema_version, sources:[...]}` file):
```
S020:sha256 OK
S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
exit=0
```

## Deliverables (beside this receipt)
- `ScoutS020.capture.txt` — byte-identical to the instrument snapshot S020.txt; 319 lines; 16693 bytes; sha256 `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c`. To land as `corpus/source-snapshots/round-40/S020.txt`.
- `ScoutS020.manifest-record.json` — one source object (37 lines; sha256 `06fe885da1dcaa063b14dcbfc328d0be5355b391b76a4a587c4634750d750b6b`) in the round-39 manifest shape with the requested fields: fetched_utc `2026-10-26T21:16:10Z`, sha256 (snapshot) `8fc334be…5458c`, lines 319, files `["S020.txt"]`, url, status 200, size_bytes 16693; plus fetched_bytes/raw_bytes 140909, raw_sha256, snapshot_sha256, normalized, http block, and Q1 with anchor 142. Not wrapped in `schema_version`/`sources`; the L1 inserts it into the round-40 `manifest.json` `sources` array (path stem S020 == id).

## Tools
No installs. pdftotext (poppler) already at /usr/bin; capture-source.py and source-recheck.py run read-only against scratch. Disk guard idle before fetch. No lane files other than this receipt and the two deliverables were written; scratch dir removed at yield.
