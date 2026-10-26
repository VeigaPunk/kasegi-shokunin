# ScoutS021 receipt — round 40, row S021 (CISA BOD 20-01)

Decision recommendation: **mine** (not reject). Source reachable, substantive, and teaches ground the lane does not hold.

## (a) Reachable and substantive
- Command: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -D h.txt -o raw.html -w '%{http_code} %{content_type} %{size_download} %{url_effective} %{num_redirects}'` on the S021 URL.
- Observed: `200 text/html; charset=utf-8 127832 <same URL> 0` (no redirects). Response `date: Mon, 26 Oct 2026 21:15:57 GMT`; UTC fetch time **2026-10-26T21:15:57Z**. No Last-Modified/ETag/Content-Length/Server headers were returned (record carries null).
- raw bytes 127832, raw sha256 `fc7267288c8de400d433d911c3336fc573f65ea50d74d1b1a56f82a0cc998a5d`. A second fetch seconds later returned the identical 127832 bytes and identical sha256, and `html_to_text` of it equals the capture (True).
- Capture = `corpus/instruments/capture-source.py html_to_text()` (imported, not run as CLI) over the raw bytes: 432 lines, 58004 bytes, sha256 `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329`.
- Substantive: the page is the full web version of the directive (page date line L79 "September 02, 2020"; Background L99-L107; Required Actions L108-L171; CISA Actions L172-L180; Implementation Guide/Checklist L183-L196; VDP FAQ L257+; footnotes 1-23 L~300-L390 incl. target timelines 3 business days / 7 days / 90 days). Nav boilerplate L1-L91 and the "Related Directives" tail (L~392-L410, lists BOD 19-02 and 22-01 as "(Revoked)", dated Jun 10, 2026) are volatile site chrome, not BOD 20-01 itself; the BOD 20-01 page title carries no "Revoked" mark.

## (b) New ground vs the lane
Checked: `grep` over corpus/ for `BOD 20-01|bod-20-01|Vulnerabilities Equities|20-01`, and over corpus/knowledge for `vetted|U.S. citizens|Equities|median time|reasonably time-limited|anonymously|180 calendar|.gov registrar` (the latter: **zero hits** in corpus/knowledge).
- Existing holdings: S008 (CISA VDP *template*, F03, knowledge/authorization-safe-harbor-and-scope.md:38 says only "a CISA template ... aligned with BOD 20-01"); S003 snapshot note (BOD 20-01 requires FCEB agencies to publish VDPs, one sentence); round-22 lesson row for S021 (queued, quote L98-equivalent) and round-35 lesson note that kake rejected the BOD 20-01 *template*. No knowledge file holds the directive's own requirements. F01-F22 rows (CVSS, timelines, safe harbor, CNA, CRA, JP/CN, KEV/EPSS/SSVC, CSAF/VEX, Immunefi, MSVR) do not cover them.
- Ground the directive adds (all located in the capture): mandatory VDP elements (L119-L129: scope with >=1 production system, allowed/prohibited testing + no-PII-disclosure statement, report channel, anonymous-submission statement L125, no-legal-action commitment L126, acknowledgement-expectation statement L127, issuance date); the "must not" list (L130-L134: no PII required, no vetting/citizenship limit, no restriction of reporter disclosure beyond a time-limited response request, no Vulnerabilities Equities Process submission); 30/180/270-day and 2-year scope-expansion clock (L112, L117, L139-L140); handling-procedure obligations and target timelines (L141-L155, footnotes 3 business days / 7 days / 90 days); reporting metrics list (L161-L171, e.g. median time to remediate, reports >90 days). This is binding-regime ground distinct from the template (S008) and from vendor policies (F10).
- Caveat for mining: BOD 20-01 binds only FCEB agencies (L92-L95), not vendors or bounty programs; the table row's "Make scope ... explicit instead of relying on a generic bounty policy" is the lane's inference, the directive itself says VDP is "similar to, but distinct from" a bug bounty (L107). Nothing authorises testing.

## (c) Located quote (20 words, unique)
> restrict the reporter’s ability to disclose discovered vulnerabilities to others, except for a request for a reasonably time-limited response period.

Anchor: capture line **133** (Required Actions > Develop and Publish a VDP > "The policy, or implementation of policy, must not:" list, L130). Verified by `corpus/instruments/source-recheck.py` against a scratch manifest wrapping the record: `S021:sha256 OK` / `S021:Q1 OK occurrences=1 anchor=133-ok`, exit 0. Spare quotes if wanted: L125 "A clear statement that reporters may submit a report anonymously." and L132 "The policy must provide authorization to the general public."

## Deliverables (beside this receipt)
- `ScoutS021.capture.txt` — 432 lines, sha256 `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329` (byte-identical to the capture the record hashes; commit it as `corpus/source-snapshots/round-40/S021.txt` — record `path` is `S021.txt`).
- `ScoutS021.manifest-record.json` — 38 lines, sha256 `439d2fb63956fc21fe43b3b5989b1157ab9bedb5dec38216294391e0baa790f9`. One `sources[]` entry in the round-36..39 manifest shape (id, path, url, fetched_utc, fetched_bytes, snapshot_bytes, lines, sha256, normalized, raw_sha256, http{...}, quotes[]), plus the seat-requested `files`, `status`, `size_bytes`. Field meanings: `sha256`/`snapshot_bytes`/`size_bytes` = capture (58004 bytes); `fetched_bytes` = raw HTML 127832; `lines` = 432; `files` = ["S021.txt"]; `status` = 200. The L1 must wrap it in `{"schema_version":1,"purpose":...,"sources":[...]}` and set `path` to match the committed filename.

## Notes
- No SOURCES row written (ScribeRows owns it). Suggested status/row detail is the L1's call; recommendation: mined, with knowledge entry citing S021 (candidate home: knowledge/authorization-safe-harbor-and-scope.md or a new entry), keeping the FCEB-only scope caveat.
- No tools installed. No fetch other than the two curls above. Scratch /fast/scratch/hyaku/kasegi-r40/ScoutS021 removed after this receipt.
