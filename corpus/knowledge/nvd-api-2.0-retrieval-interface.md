# NVD API 2.0 — NIST's read-side retrieval interface over the NVD-enriched CVE record: the 2.0 response envelope, NVD's own CVSS served alongside the CNA's, CPE applicability configurations, CWE classification, change tracking, and the ingested CISA ADP SSVC block

source: S083 — https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-3094 — capture corpus/source-snapshots/round-52/S083.txt (1 line, 13077 bytes; sha256 5c35a51b103934778b94b385a060a26da53a7319e7339f85efcf646899a0e716; fetched 2026-11-01T04:18:04Z, HTTP 200, 13076 raw bytes — a live API response served by NIST's services host for exactly one record); manifest corpus/source-snapshots/round-52/manifest.json (12 assertions Q1-Q12, each exactly-once at its pinned anchor; single-line capture, so every anchor is line 1)
verified-at: 2026-11-01 (opened this round; the capture is one live response at one instant — the response carries its own `timestamp` and the record's `lastModified` is the interface's change-tracking, so the 90d row recheck exists to re-open the query, not to trust that NIST serves these bytes again)
ground: F33
recheck: (python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-52/manifest.json --source S083 || python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-52/manifest.json --source S083)   # interpreter-portable form (run from the lane root, no `cd` prefix); prints S083:sha256 OK then one S083:Q<n> OK line per pinned quote with its occurrences= count and anchor=1-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

This is NIST's own service speaking: the bytes are what the NVD Vulnerability Data API 2.0 returned for
one `cveId` query, read as evidence of the interface's response contract and of what NVD's enrichment
adds to a record it serves — nothing wider. The developer-hub documentation page is NOT the source of
record: it serves a JS application shell to this lane's instrument (2629 raw bytes collapsing to an
11-byte text snapshot; rejected row S084, wave receipt `.ufo/waves/round-52/controls/s084-hub-shell.txt`),
the same wall round-42's S066 anchor recorded ("the nvd.nist.gov developer page returned only the Angular
application shell"). Everything asserted below is pinned to the captured response bytes; what the capture
does not show (rate limits, authentication, the parameter surface beyond this query shape) is not
asserted anywhere.

## Claim 1 — the envelope is a retrieval contract, not a record

> "resultsPerPage":1,"startIndex":0,"totalResults":1,"format":"NVD_CVE","version":"2.0" — Q1, S083.txt:1

The response is paged and self-describing: `resultsPerPage` / `startIndex` / `totalResults` bound the
window, `format` names the payload family, `version` pins the API generation (2.0), and a `timestamp`
marks the serving instant. None of these keys exists in the CVE Record format itself (F25/S064: four
root properties `dataType`/`dataVersion`/`cveMetadata`/`containers` with `additionalProperties: false`),
and the record travels nested — `vulnerabilities[].cve` — rather than at the top level. The falsifiable
rule: a client that treats envelope fields as record properties, or that assumes one response holds the
whole result set without reading `totalResults` against `resultsPerPage`, is misreading this interface.

## Claim 2 — NVD serves its own analysis beside the CNA's, and names which is which

> "source":"nvd@nist.gov","type":"Primary" — Q5, S083.txt:1
> "cvssMetricV31":[{"source":"secalert@redhat.com","type":"Secondary","cvssData" — Q4, S083.txt:1

The same record's `metrics.cvssMetricV31` array carries TWO CVSS 3.1 assessments with per-item
provenance: the originating CNA's (Red Hat, `secalert@redhat.com`, `type: Secondary`) and NVD's own
(`nvd@nist.gov`, `type: Primary`). Enrichment here is attributed analysis, not overwrite: the NVD-side
metric is served alongside the CNA's, and the `type` cell is the only thing that tells a reader whose
judgment a number encodes. The falsifiable rules: "the NVD score" is ambiguous until the source/type
pair is read; a consumer that merges metric items without their provenance loses exactly the
CNA-vs-NVD distinction this API serves per item; and the same attribution shape repeats on the
weaknesses section (Q11 carries its own `source` and `type` beside the CWE value).

## Claim 3 — applicability and classification are structured, per-item, and tagged

> "operator":"OR","negate":false,"cpeMatch" — Q12, S083.txt:1
> "criteria":"cpe:2.3:a:tukaani:xz:5.6.0:*:*:*:*:*:*:*" — Q10, S083.txt:1

NVD's `configurations` section states vulnerability applicability as match trees: `nodes` with an
`operator` (OR), a `negate` flag, and `cpeMatch` entries that pair a CPE 2.3 criteria string with a
`vulnerable` flag and a `matchCriteriaId`. `weaknesses` carries the CWE classification (CWE-506 here)
with per-item provenance (Q11), `references` are tagged (`Vendor Advisory`, `Issue Tracking`, … — Q9, S083.txt:1),
and `descriptions` are multilingual (`lang: en` plus `lang: es` — Q8, S083.txt:1). The falsifiable rule: an
"NVD says X affects Y" claim should be traceable to a specific `cpeMatch` criteria + `vulnerable` flag,
not to the record's existence; the affected-version set here (xz 5.6.0 and 5.6.1 pinned as vulnerable)
is enumerative data a claim either quotes or does not.

## Claim 4 — the record is versioned state, and the CISA ADP SSVC data arrives as ingested data

> "published":"2024-03-29T17:15:21.150","lastModified":"2026-06-17T07:43:17.830","vulnStatus":"Modified" — Q3, S083.txt:1

Every response carries the record's state timeline: `published`, `lastModified`, and a `vulnStatus`
(`Modified` here — NVD's lifecycle vocabulary, not the CVE Record format's PUBLISHED/REJECTED states).
This record was modified over two years after publication, so a snapshot taken today is not the record
as published. The response also carries an `ssvcV203` block (Q6, S083.txt:1) — sourced
`134c704f-9b21-4f2e-91b3-4a467353bcc0`, `role: CISA Coordinator`, decision points
`exploitation: none / automatable: yes / technicalImpact: total` (Q7, S083.txt:1). Read it as what it claims to be:
an ingested copy of the CISA ADP enrichment (the F32 program's data, in the major.minor.patch version
encoding F32 documents), served downstream by NVD — not NVD-generated SSVC, and not the ADP container
itself. The falsifiable rules: an SSVC value in an NVD response is downstream mirror data whose
freshness is bounded by NVD's ingestion, and its authority chain runs CISA ADP → NVD, so a conflict
between that block and a CNA field resolves by F32's CNA-precedence rule, not by NVD's serving order.

## Distinctness — what this row adds beyond F05/F18/F19/F25/F30/F32 and the screen's downstream consumers

The pre-freeze neighbor screen (run before the round-52 freeze landed; the round-50 D1 lesson makes it
mandatory, and the round-51 closure's scope observation makes the downstream-consumer sweep part of it):
`grep -ric nvd` over corpus/knowledge/, corpus/README.md, PROVINCE.md, corpus/SOURCES.md and SKILL.md
names five knowledge files (receipt `.ufo/waves/round-52/controls/neighbor-screen-r52.txt`), and the
new sweep over `corpus/source-snapshots/` names the capture-level consumers. The adjacent ground is
named, not absorbed: F05 (S013/S014, CWE Top 25 methodology) consumes NVD as a **data source whose
CWE-mapping volume shifted** — this row is the interface that serves such data, not the methodology.
The CVE-bench entry (S025) feeds agents "a high-level description … as published in the NVD" — this row
is the retrieval contract for such descriptions, not the benchmark. F18 (S052) is the KEV catalog; an
NVD detail-page URL appears inside a KEV record's notes field, and this response serves no KEV fields at
all (`cisaExploitAdd`-class keys are absent from the captured record). F19 (EPSS) is not served by this
response. F25 (S064) is the CVE Record format — the envelope, the `vulnerabilities[].cve` nesting, the
NVD lifecycle vocabulary and the NVD-only sections are all outside it. F30 (S078) is the CVE Services
write path — this is a read-side retrieval interface over a downstream-enriched projection. F32 (S081)
is the CISA ADP program writing CVE records; Q6's SSVC block is that program's data after NVD ingested
it, which is exactly the downstream-consumer relationship F32's scope limit left to a row like this one.
S066 (the round-42 REJECTED schema row) is the flip this admission spends — its own flip text invited
exactly this ground ("re-open if a frontier targets NVD-specific enrichments (vulnStatus, evaluator*
fields, cisa* mirror fields, NVD-side metrics/weaknesses) or the API interface contract
(resultsPerPage/startIndex pagination)"); the row stays byte-identical and the spending is recorded
here, not by editing it.

## Limits

- One record (CVE-2024-3094), one instant (2026-11-01T04:18:04Z). The capture grounds the response
  CONTRACT as served, not current upstream content; `vulnStatus: Modified` plus the record's own
  2026-06-17 `lastModified` are the interface's statement that this data changes.
- Rate limits, authentication and the wider parameter surface are NOT asserted anywhere: the developer
  pages are JS-walled for this lane's instrument (S084) and the capture shows one query shape only.
- The `evaluatorComment` / `evaluatorSolution` / `evaluatorImpact` and `cisa*` mirror fields that
  S066's schema ground names are NOT present in this response (this record carries none), so no claim
  here rests on them; S066's schema artifact on csrc.nist.gov remains the natural next capture if a
  future claim needs that ground.
- The single-line capture pins all twelve anchors to line 1 (`anchor=1-ok`); uniqueness is carried by
  the exactly-once occurrence counts, re-verifiable from the manifest.
