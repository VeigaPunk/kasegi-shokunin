# ScoutHrefCheck: round 40 falsify wave 2 receipt

**Attacked:** every URL referenced by the new rows S060-S062 and by the nine decided rows' source cells (S016 S017 S019 S020 S021 S022 S023 S024 S025), at lane tip HEAD 3074c7679d6f527ec3930d7748ccce1dbae4a58a (`git show HEAD:corpus/SOURCES.md`; the untracked working-tree files are receipts only). I also checked the URLs the rows' knowledge entries cite, the superseder sources S029/S030, and every URL the new rows' evidence cells name (probes, listings, pages), because those cells record HTTP statuses, byte counts and sha256 values.

**Command:** `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o /dev/null -w '%{http_code} %{num_redirects} %{size_download} %{url_effective}'` (GET, follow redirects), plus a no-redirect first-hop GET. Fetched 2026-10-26T22:07:20Z to 22:07:42Z. Machine-readable table: `ScoutHrefCheck.tsv` beside this file.

## Table

| row | URL | kind | fetched UTC | HTTP final / first hop | redirects | bytes | verdict |
|---|---|---|---|---|---|---|---|
| S016 | `https://www.anthropic.com/coordinated-vulnerability-disclosure` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 164126 | OK |
| S017 | `https://projectzero.google/2025/07/reporting-transparency.html` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 14764 | OK |
| S019 | `https://csrc.nist.gov/pubs/sp/800/216/final` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 44658 | OK |
| S019 | `https://doi.org/10.6028/NIST.SP.800-216` | entry-ref | 2026-10-26T22:07:20Z | 200 / 302 | 1 | 1510851 | OK |
| S019 | `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-216.pdf` | entry-ref | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 1510851 | OK |
| S020 | `https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline=` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 140909 | OK |
| S021 | `https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 127832 | OK |
| S022 | `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 250107 | OK |
| S022 | `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf` | superseder-S030 | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 665517 | OK |
| S023 | `https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program` | row-source | 2026-10-26T22:07:20Z | 200 / 200 | 0 | 75587 | OK |
| S024 | `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` | row-source(=S029) | 2026-10-26T22:07:20Z | 202 / 202 | 0 | 0 | 2xx but AWS-WAF challenge (202, 0 B body): not a document fetch |
| S025 | `https://arxiv.org/abs/2503.17332` | row-source | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 44575 | OK |
| S025 | `https://arxiv.org/pdf/2503.17332` | entry-ref | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 602933 | OK |
| S025 | `https://github.com/uiuc-kanglab/cve-bench` | entry-ref | 2026-10-26T22:07:21Z | 404 / 404 | 0 | 266032 | **DEAD 404** (entry-ref quoted from paper; org is now uiuc-kang-lab) |
| S060 | `https://cyclonedx.org/docs/1.7/json/` | row-source | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 6419901 | OK |
| S061 | `https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf` | row-source | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 313386 | OK |
| S061 | `https://www.cisa.gov/resources-tools/resources/vulnerability-exploitability-exchange-vex-status-justification-document-june-2022` | row-cited-page(200 claimed) | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 56383 | OK |
| S061 | `https://www.cisa.gov/news-events/news/vulnerability-exploitability-exchange-vex-status-justifications` | row-cited-lead(404 claimed) | 2026-10-26T22:07:21Z | 404 / 404 | 0 | 46957 | 404 AS RECORDED in the row (expected; reproduces row claim) |
| S062 | `https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html` | row-source | 2026-10-26T22:07:21Z | 200 / 200 | 0 | 1231332 | OK |
| S062 | `https://docs.oasis-open.org/csaf/csaf/v2.1/csd04/csaf-v2.1-csd04.html` | row-cited(csd04/ byte-identical) | 2026-10-26T22:07:22Z | 200 / 200 | 0 | 1231332 | OK |
| S062 | `https://docs.oasis-open.org/csaf/csaf/v2.1/` | row-cited-dirlist | 2026-10-26T22:07:22Z | 200 / 200 | 0 | 1097 | OK |
| S062 | `https://docs.oasis-open.org/csaf/csaf/` | row-cited-parent-dirlist | 2026-10-26T22:07:22Z | 200 / 200 | 0 | 392 | OK |
| S062 | `https://docs.oasis-open.org/csaf/csaf/v2.1/os/` | row-cited-probe(404 claimed) | 2026-10-26T22:07:22Z | 404 / 404 | 0 | 41334 | 404 AS RECORDED in the row (expected; reproduces row claim) |
| S062 | `https://docs.oasis-open.org/csaf/csaf/v2.1/os/csaf-v2.1-os.html` | row-cited-flip-probe(404 claimed) | 2026-10-26T22:07:22Z | 404 / 404 | 0 | 41334 | 404 AS RECORDED in the row (expected; reproduces row claim) |

Only S060, S061 and S062 are new rows; SOURCES.md has no S063+. All nine decided rows' source cells returned 2xx (S024 caveat below). S022's v4.1.0 PDF and S030's v4.2.0 PDF both return 200.

## Findings

1. **Dead link (freshness, low severity): `https://github.com/uiuc-kanglab/cve-bench` returns HTTP 404**, and so does the org page `https://github.com/uiuc-kanglab`. It is not a SOURCES.md source cell. It appears in `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` line 10 as the paper's own link, quoted from capture `corpus/source-snapshots/round-40/S025.txt:282` ("Data and code are available at https://github.com/uiuc-kanglab/cve-bench."). The live repo is `https://github.com/uiuc-kang-lab/cve-bench` (200). The entry reproduces the paper faithfully, but it hands readers a dead pointer without saying so. Possible fix: note the `uiuc-kang-lab` spelling in the entry, or drop the repo URL.
2. **Caveat: `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` (S024, same URL as S029) returns HTTP 202 with a 0-byte body and `x-amzn-waf-action: challenge`.** I saw this on 3 consecutive plain-curl tries, with a Firefox UA, and on the `legal-content/EN/TXT/HTML/?uri=OJ:L_202402847` and `CELEX:32024R2847` variants. The status is 2xx, so the freshness criterion passes literally. But a non-browser client cannot re-open the document over HTTP from this host. The CELLAR URL `publications.europa.eu/resource/celex/32024R2847` returns 400. S024 is rejected and superseded by S029, so no mined entry depends on it.
3. No other dead or moved link. No row-source URL redirects. The only redirect is the entry-ref `doi.org/10.6028/NIST.SP.800-216`, which returns 302 to `nvlpubs.nist.gov/.../NIST.SP.800-216.pdf` (200, 1510851 B), the other URL that entry cites.

## Reproduced row claims (green re-runs)

Rows S060-S062 record statuses, byte counts and sha256 values in their evidence cells. I re-fetched each one live:
- S060 `cyclonedx.org/docs/1.7/json/`: HTTP 200, 6419901 B, matching the row's "raw 6419901 bytes". The raw sha256 now reads `2f14799d8d48a233d4a88cd161e3ab2028f1ef20c87ca24422b1424ab3a54a5f`. The row says the raw sha differs between fetches (Cloudflare email tokens) and pins the slice instead, so this is consistent and not a defect.
- S061 PDF: 313386 B, sha256 `9a4027c68674a99678bfd18d0897cdb213a2db59b568054b2b86439ff0cf513f`, matching the row. Publication page: HTTP 200, 56383 B, sha256 `2cb3a40b3d22102ca169d4003ba4e7fd7196a093b3978d17d4bea92437191b8c`, matching. Lead URL `news-events/news/vulnerability-exploitability-exchange-vex-status-justifications`: HTTP 404, 46957 B, sha256 `ec8e69c7486d0edd936482fab4437136ea91060a13662764cf04622f5c541a19`, matching. The row documents this 404 as a known bad lead, so it is not a dead link in the source cell.
- S062 `csaf-v2.1.html`: 200, 1231332 B, sha256 `fdb4bf015c75f01269c1ba346912fd558e8a168b607279b951b1fe5335f366b0`. `csd04/csaf-v2.1-csd04.html` has the identical sha256. The `v2.1/` listing is 1097 B, sha256 `5e59949c479ca03097be81259cb5bf168a857562991c73be3c826e7822f03775`; it lists csd01 28-May-2025, csd02 25-Feb-2026, csd03 11-Sep-2026, csd04 21-Oct-2026 and schema/, with no `os/`. The parent listing is 392 B, sha256 `64a9419639f60bd14d22b233b63743ef1ce81a9d70a1f5a875195a5c486ec94b`. `v2.1/os/` and `v2.1/os/csaf-v2.1-os.html` return 404, 41334 B, sha256 `e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731`. All of these match the row. The os/ 404 is the row's flip-monitor probe, so the monitor has not fired. The page's L424 and L495 carry "Committee Specification Draft 04 ... 21 October 2026".

## Verdict

Link freshness: 0 dead or moved links in any SOURCES.md source cell (S016-S025, S060-S062). 1 dead link in an entry (finding 1). 1 WAF-challenged 2xx (finding 2). Every S061/S062 recorded sha256 and byte count reproduces; the S060 byte count reproduces.

Scratch dir removed. No lane files were edited.
